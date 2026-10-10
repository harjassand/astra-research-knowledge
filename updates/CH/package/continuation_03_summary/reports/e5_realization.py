#!/usr/bin/env python3
"""Finite, physical cutoff-erasure evaluation of a thermal attenuator.

No SciPy, no thermal-environment truncation, and no renormalization of a
trace-decreasing Fock projection. Floating-point outputs are diagnostics, not
interval certificates. Source baseline: https://arxiv.org/html/2607.27449v1.

The caller supplies a purification coefficient matrix C[a,n], with
sum(abs(C)**2)=1. The retained RB matrix and the reference erasure block are
returned separately. They form a direct sum, with no discarded probabilities.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from dataclasses import dataclass

import numpy as np


def hbits(x):
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    positive = x > 0
    y[positive] = -x[positive] * np.log2(x[positive])
    return y


def entropy(matrix):
    ev = np.linalg.eigvalsh((matrix + matrix.conj().T) / 2)
    if ev.min(initial=0) < -2e-11:
        raise ArithmeticError(f"Nonpositive matrix: minimum eigenvalue {ev.min()}")
    return float(hbits(np.maximum(ev, 0)).sum()), ev


def amp_tail(s: int, cutoff: int, gain: float) -> float:
    """Exact finite expression for the amplifier output probability > cutoff.

    Negative-binomial tail = P[Binomial(cutoff+1,1/gain) <= s]. This
    expression avoids subtracting a nearly-one retained probability.
    """
    if s > cutoff:
        return 1.0
    p, q = 1 / gain, (gain - 1) / gain
    if q == 0:
        return 0.0
    return math.fsum(math.comb(cutoff + 1, j) * p**j * q**(cutoff + 1 - j)
                     for j in range(s + 1))


@dataclass
class ThermalCutoff:
    eta: float
    nu: float
    input_max: int
    cutoff: int

    def __post_init__(self):
        if not 0 < self.eta < 1 or self.nu < 0:
            raise ValueError("Require 0 < eta < 1 and nu >= 0")
        if self.input_max < 0 or self.cutoff < 0:
            raise ValueError("Cutoffs must be nonnegative")
        self.gain = 1 + (1 - self.eta) * self.nu
        self.tau = self.eta / self.gain
        self.d = self.input_max + 1
        self.b = self.cutoff + 1
        self.terms = []
        retained = np.zeros(self.d)
        for lost in range(self.d):
            for added in range(self.b):
                n = np.arange(lost, min(self.d, self.cutoff + lost - added + 1))
                if not len(n):
                    continue
                m = n - lost + added
                coefs = np.array([
                    math.sqrt(math.comb(int(ni), lost)
                              * (1-self.tau)**lost * self.tau**(int(ni)-lost)
                              * math.comb(int(mi), added)
                              * (self.gain-1)**added / self.gain**(int(mi)+1))
                    for ni, mi in zip(n, m)])
                if np.any(coefs):
                    self.terms.append((n, m, coefs))
                    retained[n] += coefs**2
        self.tail = np.array([
            math.fsum(math.comb(n, lost) * (1-self.tau)**lost
                      * self.tau**(n-lost) * amp_tail(n-lost, self.cutoff, self.gain)
                      for lost in range(n+1))
            for n in range(self.d)])
        self.tp_residual = float(np.max(abs(retained + self.tail - 1)))

    def apply_purification(self, C: np.ndarray):
        C = np.asarray(C, dtype=complex)
        if C.ndim != 2 or C.shape[1] != self.d:
            raise ValueError(f"C must have shape (reference_rank,{self.d})")
        if abs(np.vdot(C, C).real - 1) > 1e-10:
            raise ValueError("Purification is not normalized")
        rank = C.shape[0]
        vectors = np.zeros((len(self.terms), rank, self.b), dtype=complex)
        for t, (n, m, coefs) in enumerate(self.terms):
            vectors[t][:, m] = C[:, n] * coefs[None, :]
        flattened = vectors.reshape(len(self.terms), rank*self.b)
        retained_rb = flattened.T @ flattened.conj()
        erased_r = (C*self.tail[None, :]) @ C.conj().T
        retained_b = np.einsum('abad->bd', retained_rb.reshape(rank, self.b, rank, self.b))
        p_erased = float(np.trace(erased_r).real)
        sb0, eb0 = entropy(retained_b)
        srb0, erb0 = entropy(retained_rb)
        sre, ere = entropy(erased_r)
        sb = sb0 + float(hbits(p_erased))
        srb = srb0 + sre
        rhoa = C.T @ C.conj()
        energy = float(np.dot(np.arange(self.d), np.diag(rhoa).real))
        return {
            "ic_bits_per_use": sb-srb,
            "S_B": sb, "S_RB": srb,
            "p_erasure": p_erased, "energy_photons": energy,
            "reference_dimension": rank, "input_fock_dimension": self.d,
            "input_support_count": int(np.count_nonzero(np.diag(rhoa).real > 1e-18)),
            "output_dimension_including_flag": self.b+1,
            "joint_dimension_including_flag": rank*(self.b+1),
            "retained_kraus_count": len(self.terms),
            "tp_residual": self.tp_residual,
            "trace_B": float(np.trace(retained_b).real+p_erased),
            "trace_RB": float(np.trace(retained_rb).real+np.trace(erased_r).real),
            "minimum_eigenvalue": float(min(eb0.min(), erb0.min(), ere.min())),
            "workspace_vector_bytes": int(vectors.nbytes),
            "retained_rb": retained_rb, "erased_r": erased_r,
            "retained_b": retained_b,
        }

    def matrix_unit(self, n: int, m: int):
        """Apply the channel to |n><m|, including its physical flag."""
        out = np.zeros((self.b+1, self.b+1), dtype=complex)
        for ns, ms, cs in self.terms:
            ix = np.flatnonzero(ns == n)
            iy = np.flatnonzero(ns == m)
            if len(ix) and len(iy):
                out[ms[ix[0]], ms[iy[0]]] += cs[ix[0]]*cs[iy[0]]
        if n == m:
            out[-1, -1] = self.tail[n]
        return out


def purification(rows, weights, d):
    C = np.zeros((len(rows), d), dtype=complex)
    for a, (row, weight) in enumerate(zip(rows, weights)):
        norm = math.sqrt(math.fsum(float(abs(c)**2) for c in row.values()))
        for n, c in row.items():
            C[a, n] = math.sqrt(weight)*c/norm
    return C


def serializable(result):
    return {k: v for k, v in result.items() if not isinstance(v, np.ndarray)}


def baselines():
    start = time.monotonic()
    small = ThermalCutoff(.8, 1, 9, 11)
    C = purification([{0:5,4:-4,8:2}, {1:6,5:-5,9:2}], [1/3,2/3], 10)
    first = serializable(small.apply_purification(C))
    first.update(name="published_eta_0.8_M11", elapsed_s=time.monotonic()-start)
    start = time.monotonic()
    aa = [313,-717,1627,-3027,4551,-5436,4983,-3270,1324,-220]
    bb = [361,-895,1938,-3422,4866,-5464,4646,-2754,945,-106]
    C2 = purification([dict(zip(range(0,40,4),aa)),dict(zip(range(1,41,4),bb))],
                      [67/182,115/182], 38)
    second = serializable(ThermalCutoff(.7841,1,37,50).apply_purification(C2))
    second.update(name="published_eta_0.7841_M50", elapsed_s=time.monotonic()-start)
    pure = serializable(small.apply_purification(C[:1]/math.sqrt(1/3)))
    pure["name"] = "pure_state_zero_control"
    return [first, second, pure]


def repetition_data(eta, nu, n0, n1, cutoff):
    """Local ingredients for |n0>^L / |n1>^L repetition encoding.

    Phase covariance makes the off-diagonal matrix a single band. The full
    reference-output matrix is a direct sum of 2x2 blocks and isolated
    diagonal entries, allowing exact type counting instead of b**L storage.
    """
    if n1 <= n0:
        raise ValueError("Require n1 > n0")
    channel = ThermalCutoff(eta,nu,n1,cutoff)
    d0 = channel.matrix_unit(n0,n0).diagonal().real
    d1 = channel.matrix_unit(n1,n1).diagonal().real
    cross = channel.matrix_unit(n0,n1)
    shift = n1-n0
    x = np.array([cross[i,i+shift].real for i in range(cutoff-shift+1)])
    return d0,d1,x,shift,channel.tp_residual


def product_types(probabilities, length):
    """Products and multinomial multiplicities for symmetric tensor powers.

    probabilities has shape (number_of_distributions, alphabet_size).
    Multiplicity is represented as float; the calculation is diagnostic.
    """
    probabilities = np.asarray(probabilities)
    rows, alphabet = probabilities.shape
    count = math.comb(length+alphabet-1, alphabet-1)
    products = np.empty((rows,count),dtype=float)
    multiplicities = np.empty(count,dtype=float)
    factorials = [math.factorial(i) for i in range(length+1)]
    power = probabilities[:,:,None] ** np.arange(length+1)[None,None,:]
    cursor = 0

    def visit(index,remaining,values,denom):
        nonlocal cursor
        if index == alphabet-1:
            products[:,cursor] = values*power[:,index,remaining]
            multiplicities[cursor] = factorials[length]/(denom*factorials[remaining])
            cursor += 1
            return
        for number in range(remaining+1):
            visit(index+1,remaining-number,values*power[:,index,number],
                  denom*factorials[number])
    visit(0,length,np.ones(rows),1)
    assert cursor == count
    return products,multiplicities


def repetition_prepare(eta,nu,n0,n1,cutoff,length):
    start = time.monotonic()
    d0,d1,x,shift,tp_residual = repetition_data(eta,nu,n0,n1,cutoff)
    diagonal,mults = product_types(np.array([d0,d1]),length)
    edge,mults_edge = product_types(np.array([d0[:len(x)],d1[shift:shift+len(x)],x]),length)
    return {
        "d0":d0,"d1":d1,"diagonal":diagonal,"multiplicities":mults,
        "edge":edge,"edge_multiplicities":mults_edge,
        "eta":eta,"nu":nu,"n0":n0,"n1":n1,"cutoff":cutoff,"length":length,
        "tp_residual":tp_residual,"prepare_seconds":time.monotonic()-start,
        "type_workspace_bytes":diagonal.nbytes+mults.nbytes+edge.nbytes+mults_edge.nbytes,
    }


def repetition_evaluate(prepared, p):
    """Unconditional coherent information; all local erasure patterns included."""
    z = prepared
    d0,d1 = z["d0"],z["d1"]
    L = z["length"]
    bdiag = p*z["diagonal"][0]+(1-p)*z["diagonal"][1]
    sb = float(np.dot(z["multiplicities"],hbits(bdiag)))
    sdiag = float(hbits(p)+hbits(1-p)+L*(p*hbits(d0).sum()+(1-p)*hbits(d1).sum()))
    a = p*z["edge"][0]
    b = (1-p)*z["edge"][1]
    c = math.sqrt(p*(1-p))*z["edge"][2]
    gap = np.sqrt((a-b)**2+4*c*c)
    larger = (a+b+gap)/2
    # determinant/larger is stable when the small eigenvalue is tiny.
    smaller = np.divide(a*b-c*c,larger,out=np.zeros_like(larger),where=larger>0)
    if smaller.min(initial=0) < -1e-12:
        raise ArithmeticError("Repetition block failed positivity check")
    correction = float(np.dot(z["edge_multiplicities"],
                       hbits(larger)+hbits(np.maximum(smaller,0))-hbits(a)-hbits(b)))
    srb = sdiag+correction
    return {"eta":z["eta"],"nu":z["nu"],"n0":z["n0"],"n1":z["n1"],
            "cutoff":z["cutoff"],"length":L,"weight_n0":p,
            "ic_bits_per_block":sb-srb,"ic_bits_per_use":(sb-srb)/L,
            "S_B":sb,"S_RB":srb,
            "energy_photons_per_block":L*(p*z["n0"]+(1-p)*z["n1"]),
            "p_at_least_one_erasure":1-(1-d0[-1])**L*p-(1-d1[-1])**L*(1-p),
            "logical_dimension":2,"joint_dimension_with_local_flags":2*len(d0)**L,
            "output_type_count":len(z["multiplicities"]),
            "edge_type_count":len(z["edge_multiplicities"]),
            "type_workspace_bytes":z["type_workspace_bytes"],
            "prepare_seconds":z["prepare_seconds"],"tp_residual":z["tp_residual"]}


def repetition_scan():
    """Bounded structural scan, including symmetric and highly biased inputs."""
    weights = sorted(set([.5,.2,.8,.05,.95,.01,.99,.001,.999,.00001,.99999]))
    output = []
    for eta in [.75,.7501,.755,.76,.77,.7841,.8]:
        for n0,n1,L,M in [(0,1,1,14),(0,1,2,14),(0,1,4,14),(0,1,6,12),
                          (0,1,8,10),(0,2,1,18),(0,2,2,18),(0,2,4,14),
                          (0,4,1,24),(0,4,2,24),(1,2,1,18),(1,2,2,18)]:
            prepared = repetition_prepare(eta,1,n0,n1,M,L)
            results = [repetition_evaluate(prepared,p) for p in weights]
            best = max(results,key=lambda r:r["ic_bits_per_use"])
            symmetric = next(r for r in results if r["weight_n0"] == .5)
            best["symmetric_ic_bits_per_use"] = symmetric["ic_bits_per_use"]
            output.append(best)
            print(json.dumps(best),flush=True)
    return output


def rails(eta,m):
    """Exact one-photon-m-rail code followed by total-one-photon acceptance."""
    gain = 2-eta
    a = eta/gain**(m+2)
    b = 2*(1-eta)**2/gain**(m+2)
    success = a+m*b
    alpha = a/success
    choi_probs = np.array([alpha+(1-alpha)/m**2]+[(1-alpha)/m**2]*(m*m-1))
    ic = success*(math.log2(m)-hbits(choi_probs).sum())-(1-success)*math.log2(m)
    return {"eta":eta,"rail_modes":m,"success_probability":success,
            "conditional_depolarizing_alpha":alpha,"ic_bits_per_block":float(ic),
            "ic_bits_per_use":float(ic/m),"energy_per_block":1,
            "absolute_erasure_upper_bound_bits_per_block":(2*success-1)*math.log2(m)}


def entropy_blocks(matrix, groups):
    """Use mathematically exact covariance/flag sectors, not thresholded entries."""
    value, minev = 0.0, 1.0
    for indices in groups.values():
        block = matrix[np.ix_(indices,indices)]
        ent, ev = entropy(block)
        value += ent
        minev = min(minev,float(ev.min()))
    return value,minev


def two_mode_evaluate(channel, C, fixed_total=None):
    """Apply two independent physical cutoff channels to an arbitrary pure RA.

    C has shape (reference_dimension,input_dimension,input_dimension).
    If every occupied input vector has the same total photon number, exact
    global-phase sectors make entropy evaluation much cheaper. Local erasure
    patterns are separate physical sectors and are all retained in the sum.
    """
    start = time.monotonic()
    C = np.asarray(C,dtype=complex)
    r,d,d2 = C.shape
    if d != channel.d or d2 != d or abs(np.vdot(C,C).real-1)>1e-10:
        raise ValueError("Invalid two-mode purification")
    b = channel.b+1
    T = np.zeros((b,b,d,d),dtype=complex)
    for ns,ms,cs in channel.terms:
        T[ms[:,None],ms[None,:],ns[:,None],ns[None,:]] += cs[:,None]*cs[None,:]
    T[-1,-1,np.arange(d),np.arange(d)] = channel.tail
    first = np.einsum('rij,skl,acik->rajscl',C,C.conj(),T,optimize=True)
    jt = np.einsum('rajscl,bdjl->rabscd',first,T,optimize=True)
    joint = jt.reshape(r*b*b,r*b*b)
    output = np.einsum('rabrcd->abcd',jt).reshape(b*b,b*b)
    if fixed_total is not None:
        for _,i,j in np.argwhere(C != 0):
            if i+j != fixed_total:
                raise ValueError("Incorrect fixed_total promise")
        bgroups = {}
        jgroups = {}
        for i in range(b):
            for j in range(b):
                if i == b-1 or j == b-1:
                    sector = ('flag',i,j)
                else:
                    sector = ('total',i+j)
                index = i*b+j
                bgroups.setdefault(sector,[]).append(index)
                jgroups.setdefault(sector,[]).extend(a*b*b+index for a in range(r))
        sb,minb = entropy_blocks(output,bgroups)
        srb,minrb = entropy_blocks(joint,jgroups)
        largest_block = max(map(len,jgroups.values()))
    else:
        sb,eb = entropy(output)
        srb,erb = entropy(joint)
        minb,minrb = float(eb.min()),float(erb.min())
        largest_block = len(joint)
    ii,jj = np.indices((d,d))
    energy = float(np.sum(abs(C)**2*(ii+jj)[None,:,:]))
    obdiag = output.diagonal().real.reshape(b,b)
    p_any_flag = float(obdiag[-1,:].sum()+obdiag[:,-1].sum()-obdiag[-1,-1])
    return {"eta":channel.eta,"nu":channel.nu,"modes":2,"cutoff_per_mode":channel.cutoff,
            "ic_bits_per_block":sb-srb,"ic_bits_per_use":(sb-srb)/2,
            "S_B":sb,"S_RB":srb,"energy_photons_per_block":energy,
            "p_at_least_one_erasure":p_any_flag,"success_probability_unconditional":1.0,
            "reference_dimension":r,"input_fock_dimension_per_mode":d,
            "occupied_input_basis_vectors":int(np.count_nonzero(np.sum(abs(C)**2,axis=0)>1e-18)),
            "output_dimension_with_flags":b*b,"joint_dimension_with_flags":r*b*b,
            "largest_entropy_block":largest_block,"tp_residual_local":channel.tp_residual,
            "trace_B":float(np.trace(output).real),"trace_RB":float(np.trace(joint).real),
            "minimum_eigenvalue":min(minb,minrb),
            "explicit_tensor_workspace_bytes":T.nbytes+first.nbytes+jt.nbytes+output.nbytes,
            "evaluation_seconds":time.monotonic()-start}


def binomial_code(K, spacing, phase, p):
    """Orthogonal parity codewords with N=K*spacing photons in two modes.

    phase=0 gives binomial moment matching, and exp(i*phase*j**2) applies
    a nonlinear number phase. This is a scalable support family, not an
    assertion that its coherent information approaches the AD boundary.
    """
    N = K*spacing
    C = np.zeros((2,N+1,N+1),dtype=complex)
    for j in range(K+1):
        parity = j%2
        weight = p if parity == 0 else 1-p
        C[parity,j*spacing,(K-j)*spacing] = (
            math.sqrt(weight*math.comb(K,j)/2**(K-1))*np.exp(1j*phase*j*j))
    return C


def two_mode_fixed_total_evaluate(channel,C,N):
    """Sparse-band alternative: O(r**2*M**3 + d**2*M) stored scalars.

    The full two-mode reference-output density matrix is never allocated.
    All local flag patterns are included. The only promise is exact total
    input photon number N, verified from the supplied coefficient tensor.
    """
    start = time.monotonic()
    C = np.asarray(C,dtype=complex)
    r,d,d2 = C.shape
    if d != channel.d or d2 != d or N >= d:
        raise ValueError('Incompatible input dimensions')
    for _,i,j in np.argwhere(C != 0):
        if i+j != N:
            raise ValueError('Input does not have the promised total photon number')
    if abs(np.vdot(C,C).real-1)>1e-10:
        raise ValueError('Input is not normalized')
    M = channel.cutoff
    w = np.stack([C[:,n,N-n] for n in range(N+1)],axis=1)
    band = np.zeros((d,d,M+1),dtype=float)
    for ns,ms,cs in channel.terms:
        band[ns[:,None],ns[None,:],ms[:,None]] += cs[:,None]*cs[None,:]
    retained_blocks = []
    occupied = np.flatnonzero(np.any(w != 0,axis=0))
    for total in range(2*M+1):
        left = np.arange(max(0,total-M),min(M,total)+1)
        size = len(left)
        block = np.zeros((r*size,r*size),dtype=complex)
        for n in occupied:
            for k in occupied:
                shift = k-n
                right_left = left+shift
                valid = (right_left>=left[0]) & (right_left<=left[-1])
                aa = left[valid]
                cc = right_left[valid]
                vals = band[n,k,aa]*band[N-n,N-k,total-aa]
                if not np.any(vals):
                    continue
                ia,ic = aa-left[0],cc-left[0]
                for a in range(r):
                    if w[a,n] == 0:
                        continue
                    for b in range(r):
                        coefficient = w[a,n]*w[b,k].conj()
                        if coefficient != 0:
                            block[a*size+ia,b*size+ic] += coefficient*vals
        retained_blocks.append(block)
    flag_blocks = []
    for out in range(M+1):
        flag_first = np.zeros((r,r),complex)
        flag_second = np.zeros((r,r),complex)
        for n in occupied:
            ref = w[:,n,None]*w[:,n,None].conj().T
            flag_first += ref*channel.tail[n]*band[N-n,N-n,out]
            flag_second += ref*band[n,n,out]*channel.tail[N-n]
        flag_blocks.extend([flag_first,flag_second])
    both_flags = np.zeros((r,r),complex)
    for n in occupied:
        both_flags += w[:,n,None]*w[:,n,None].conj().T*channel.tail[n]*channel.tail[N-n]
    flag_blocks.append(both_flags)
    sb,srb,trace,minev = 0.,0.,0.,1.
    for block in retained_blocks:
        size = len(block)//r
        output_block = np.einsum('aiaj->ij',block.reshape(r,size,r,size))
        eb,evb = entropy(output_block)
        ej,evj = entropy(block)
        sb += eb
        srb += ej
        trace += float(np.trace(block).real)
        minev = min(minev,float(evb.min()),float(evj.min()))
    p_any_flag = 0.
    for block in flag_blocks:
        mass = float(np.trace(block).real)
        sb += float(hbits(mass))
        ent,ev = entropy(block)
        srb += ent
        trace += mass
        p_any_flag += mass
        minev = min(minev,float(ev.min()))
    stored = band.nbytes+sum(x.nbytes for x in retained_blocks+flag_blocks)+C.nbytes+w.nbytes
    return {'eta':channel.eta,'nu':channel.nu,'modes':2,'cutoff_per_mode':M,
            'ic_bits_per_block':sb-srb,'ic_bits_per_use':(sb-srb)/2,'S_B':sb,'S_RB':srb,
            'energy_photons_per_block':float(N),'p_at_least_one_erasure':p_any_flag,
            'success_probability_unconditional':1.,'reference_dimension':r,
            'input_fock_dimension_per_mode':d,'occupied_input_basis_vectors':len(occupied),
            'output_dimension_with_flags':(M+2)**2,'joint_dimension_with_flags':r*(M+2)**2,
            'largest_entropy_block':max(map(len,retained_blocks+flag_blocks)),
            'tp_residual_local':channel.tp_residual,'trace_B':trace,'trace_RB':trace,
            'minimum_eigenvalue':minev,'explicit_tensor_workspace_bytes':stored,
            'evaluation_seconds':time.monotonic()-start,'engine':'sparse_exact_sectors'}


def binomial_scan():
    output = []
    for eta in [.75,.7501,.76,.77,.7841,.8]:
        for K,spacing in [(2,2),(3,2),(4,2),(2,3)]:
            N = K*spacing
            M = max(14,N+10)
            channel = ThermalCutoff(eta,1,N,M)
            phases = [0] if K == 2 else [0,math.pi/8,math.pi/4]
            for phase in phases:
                trials = []
                for p in [.2,.5,.8]:
                    result = two_mode_evaluate(channel,binomial_code(K,spacing,phase,p),fixed_total=N)
                    result.update(K=K,spacing=spacing,phase=phase,weight_even=p)
                    trials.append(result)
                best = max(trials,key=lambda row:row['ic_bits_per_use'])
                best['symmetric_ic_bits_per_use'] = trials[1]['ic_bits_per_use']
                output.append(best)
                print(json.dumps(best),flush=True)
    return output


def compact_scaling():
    import resource
    rows = []
    for eta in [.7501,.76,.7841,.8]:
        for N in [24,32,48,64]:
            channel = ThermalCutoff(eta,1,N,N+10)
            row = two_mode_fixed_total_evaluate(channel,binomial_code(N//2,2,0,.5),N)
            row.update(K=N//2,spacing=2,phase=0,weight_even=.5,
                       ru_maxrss_raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            rows.append(row)
            print(json.dumps(row),flush=True)
    return rows


def high_precision_published(which, digits=80):
    """Independent mpmath arithmetic/eigensolver, still not interval arithmetic."""
    import mpmath as mp
    start = time.monotonic()
    mp.mp.dps = digits
    if which == 'small':
        eta = mp.mpf(4)/5
        M,weights = 11,[mp.mpf(1)/3,mp.mpf(2)/3]
        rows = [{0:5,4:-4,8:2},{1:6,5:-5,9:2}]
    elif which == 'strong':
        eta = mp.mpf(7841)/10000
        M,weights = 50,[mp.mpf(67)/182,mp.mpf(115)/182]
        aa = [313,-717,1627,-3027,4551,-5436,4983,-3270,1324,-220]
        bb = [361,-895,1938,-3422,4866,-5464,4646,-2754,945,-106]
        rows = [dict(zip(range(0,40,4),aa)),dict(zip(range(1,41,4),bb))]
    else:
        raise ValueError('which must be small or strong')
    G = 2-eta
    tau = eta/G
    N = max(max(row) for row in rows)
    B = M+2
    coeffs = [{n:mp.sqrt(weights[a])*c/mp.sqrt(sum(v*v for v in row.values()))
               for n,c in row.items()} for a,row in enumerate(rows)]
    joint = mp.matrix(2*B)
    for lost in range(N+1):
        for added in range(M+1):
            v = []
            for a in range(2):
                for n,c in coeffs[a].items():
                    out = n-lost+added
                    if n >= lost and out <= M:
                        amp = mp.sqrt(mp.mpf(math.comb(n,lost))*(1-tau)**lost*tau**(n-lost)
                                      *math.comb(out,added)*(G-1)**added/G**(out+1))
                        v.append((a*B+out,c*amp))
            for i,ci in v:
                for j,cj in v:
                    joint[i,j] += ci*cj
    q,pamp = (G-1)/G,1/G
    for n in range(N+1):
        tail = mp.mpf(0)
        for lost in range(n+1):
            s = n-lost
            amp_tail_exact = (mp.mpf(1) if s > M else
                mp.fsum(math.comb(M+1,j)*pamp**j*q**(M+1-j) for j in range(s+1)))
            tail += math.comb(n,lost)*(1-tau)**lost*tau**s*amp_tail_exact
        for a in range(2):
            for b in range(2):
                joint[a*B+M+1,b*B+M+1] += coeffs[a].get(n,0)*coeffs[b].get(n,0)*tail
    output = mp.matrix(B)
    for i in range(B):
        for j in range(B):
            output[i,j] = joint[i,j]+joint[B+i,B+j]
    bgroups = [[i for i in range(M+1) if i%4 == sector] for sector in range(4)]+[[M+1]]
    jgroups = [[a*B+i for a in range(2) for i in range(M+1) if (i-a)%4 == sector]
               for sector in range(4)]+[[M+1,2*B-1]]

    def mp_entropy_blocks(matrix,groups):
        contributions = []
        for group in groups:
            block = mp.matrix([[matrix[i,j] for j in group] for i in group])
            eig = mp.eigsy(block,eigvals_only=True)
            contributions.extend(-v*mp.log(v,2) for v in eig if v > 0)
        return mp.fsum(contributions)
    sb = mp_entropy_blocks(output,bgroups)
    srb = mp_entropy_blocks(joint,jgroups)
    return {'name':which,'precision_decimal_digits':digits,'S_B':mp.nstr(sb,digits),
            'S_RB':mp.nstr(srb,digits),'ic_bits_per_use':mp.nstr(sb-srb,digits),
            'trace_B':mp.nstr(mp.fsum(output[i,i] for i in range(B)),digits),
            'trace_RB':mp.nstr(mp.fsum(joint[i,i] for i in range(2*B)),digits),
            'elapsed_seconds':time.monotonic()-start,'interval_certified':False}


def consistency():
    """Meaningful controls: positivity, trace, and direct-vs-type evaluation."""
    result = {}
    z = repetition_prepare(.77,1,0,1,7,1)
    p = .37
    by_type = repetition_evaluate(z,p)["ic_bits_per_use"]
    C = purification([{0:1},{1:1}],[p,1-p],2)
    direct = ThermalCutoff(.77,1,1,7).apply_purification(C)["ic_bits_per_use"]
    result["length_one_type_vs_direct_error"] = abs(by_type-direct)
    assert result["length_one_type_vs_direct_error"] < 2e-12
    d0,d1,x,shift,_ = repetition_data(.77,1,0,1,5)
    X = np.diag(x,shift)
    X = np.pad(X,((0,1),(0,1)))
    A = p*np.diag(np.kron(d0,d0))
    D = (1-p)*np.diag(np.kron(d1,d1))
    cross = math.sqrt(p*(1-p))*np.kron(X,X)
    joint = np.block([[A,cross],[cross.T,D]])
    direct2 = entropy(A+D)[0]-entropy(joint)[0]
    type2 = repetition_evaluate(repetition_prepare(.77,1,0,1,5,2),p)["ic_bits_per_block"]
    result["length_two_type_vs_full_matrix_error"] = abs(direct2-type2)
    assert result["length_two_type_vs_full_matrix_error"] < 2e-12
    channel = ThermalCutoff(.77,1,1,5)
    pure2 = np.zeros((1,2,2),complex)
    pure2[0,0,1],pure2[0,1,0] = 1/math.sqrt(2),1j/math.sqrt(2)
    generic_pure = two_mode_evaluate(channel,pure2)
    blocked_pure = two_mode_evaluate(channel,pure2,fixed_total=1)
    result['two_mode_pure_state_ic_error'] = abs(generic_pure['ic_bits_per_block'])
    result['fixed_total_vs_full_eigenspectrum_error'] = abs(generic_pure['S_RB']-blocked_pure['S_RB'])
    product1 = purification([{0:1},{1:1}],[.37,.63],2)
    product2 = np.einsum('ri,sj->rsij',product1,product1).reshape(4,2,2)
    product_result = two_mode_evaluate(channel,product2)
    single_result = channel.apply_purification(product1)
    result['two_mode_product_additivity_error'] = abs(product_result['ic_bits_per_block']-2*single_result['ic_bits_per_use'])
    channel4 = ThermalCutoff(.77,1,4,10)
    C4 = binomial_code(2,2,math.pi/8,.37)
    full4 = two_mode_evaluate(channel4,C4,fixed_total=4)
    sparse4 = two_mode_fixed_total_evaluate(channel4,C4,4)
    result['sparse_sector_vs_full_matrix_error'] = abs(full4['ic_bits_per_block']-sparse4['ic_bits_per_block'])
    rng = np.random.default_rng(12087)
    columns = rng.normal(size=(5,2))+1j*rng.normal(size=(5,2))
    basis,_ = np.linalg.qr(columns)
    Crand = np.zeros((2,5,5),complex)
    for n in range(5):
        Crand[:,n,4-n] = basis[n,:]*np.sqrt([.37,.63])
    fullrand = two_mode_evaluate(channel4,Crand,fixed_total=4)
    sparserand = two_mode_fixed_total_evaluate(channel4,Crand,4)
    result['sparse_sector_complex_random_vs_full_error'] = abs(fullrand['ic_bits_per_block']-sparserand['ic_bits_per_block'])
    assert max(result.values()) < 2e-11
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode",choices=["baseline","scan","binomial","compact","highprec","rails","controls"])
    args = parser.parse_args()
    if args.mode == "baseline":
        for row in baselines():
            print(json.dumps(row),flush=True)
    elif args.mode == "scan":
        repetition_scan()
    elif args.mode == 'binomial':
        binomial_scan()
    elif args.mode == 'compact':
        compact_scaling()
    elif args.mode == 'highprec':
        for which in ['small','strong']:
            print(json.dumps(high_precision_published(which)),flush=True)
    elif args.mode == "rails":
        for eta in [.75,.7501,.76,.77,.7841,.8]:
            for m in [2,3,4,8,16]:
                print(json.dumps(rails(eta,m)))
    else:
        print(json.dumps(consistency()))


if __name__ == "__main__":
    main()
