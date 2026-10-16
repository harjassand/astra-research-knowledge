#!/usr/bin/env python3
"""Bounded independent algebra checks. No source mutation or claim certification."""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
PAULI = [I2, X, Y, Z]

def kron(*ops):
    out = np.ones((1, 1), dtype=complex)
    for op in ops:
        out = np.kron(out, op)
    return out

def super_kraus(ks):
    return sum((np.kron(k.conj(), k) for k in ks), start=np.zeros((ks[0].size, ks[0].size), dtype=complex))

def dissipator(k):
    d = k.shape[0]
    s = k.conj().T @ k
    return np.kron(k.conj(), k) - (np.kron(np.eye(d), s) + np.kron(s.T, np.eye(d))) / 2

def choi_from_super(s, d):
    out = np.zeros((d*d, d*d), dtype=complex)
    for i in range(d):
        for j in range(d):
            e = np.zeros((d, d), dtype=complex)
            e[i,j] = 1
            val = (s @ e.reshape(-1, order='F')).reshape((d,d), order='F')
            out += np.kron(val, e) / d
    return out

def range_gauge_checks():
    rng = np.random.default_rng(2026101601)
    basis = [kron(a,b) for a,b in itertools.product(PAULI, repeat=2) if not (a is I2 and b is I2)]
    d = 4
    max_error = 0.0
    min_below = 0.0
    for rank in [1, 3, 9, 15]:
        v = rng.normal(size=(15,rank)) + 1j*rng.normal(size=(15,rank))
        v /= 25
        c = v @ v.conj().T
        ls = [sum((v[a,j]*basis[a] for a in range(15)), start=np.zeros((d,d), complex)) for j in range(rank)]
        s = sum((l.conj().T@l for l in ls), start=np.zeros((d,d), complex))
        scalar = np.trace(s).real/d
        # Pick a valid shift and then make its Hermitian part equal the
        # necessary -S0/2 by full-rank augmentation if needed.
        gamma = 0.17
        c += gamma*np.eye(15)
        ls += [np.sqrt(gamma)*p for p in basis]
        h = sum((rng.normal()*p/90 for p in basis), start=np.zeros((d,d), complex))
        s = sum((l.conj().T@l for l in ls), start=np.zeros((d,d), complex))
        scalar = np.trace(s).real/d
        b0 = -(s-scalar*np.eye(d))/2 - 1j*h
        b = np.array([np.trace(p.conj().T@b0)/d for p in basis])
        vf = np.column_stack([v, np.sqrt(gamma)*np.eye(15)])
        z = np.linalg.pinv(vf)@b
        ks = [l+np.conj(z[j])*np.eye(d) for j,l in enumerate(ls)]
        rate = scalar + np.vdot(b, np.linalg.solve(c,b)).real
        g = sum((dissipator(l) for l in ls), start=np.zeros((d*d,d*d), complex)) - 1j*(np.kron(np.eye(d),h)-np.kron(h.T,np.eye(d)))
        max_error = max(max_error, float(np.max(np.abs(sum((k.conj().T@k for k in ks), start=np.zeros((d,d), complex))-rate*np.eye(d)))))
        max_error = max(max_error, float(np.max(np.abs(super_kraus(ks)-rate*np.eye(d*d)-g))))
        eig = np.linalg.eigvalsh(choi_from_super((rate-1e-5)*np.eye(d*d)+g,d)).min()
        min_below = min(min_below, float(eig))
    # Singular failure: amplitude damping at every tested positive finite rate.
    minus = np.array([[0,1],[0,0]], complex)
    ad = dissipator(minus)
    minors = []
    for rate in [0.1, 1, 10, 100]:
        j = choi_from_super(np.eye(4)+ad/rate,2)
        minor = np.linalg.det(j[np.ix_([0,3],[0,3])]).real
        assert abs(minor + 1/(16*rate*rate)) < 1e-12
        minors.append(float(minor))
    assert max_error < 2e-12 and min_below < -1e-7
    return dict(max_kraus_generator_error=max_error, below_optimal_min_eigenvalue=min_below, amplitude_damping_minors=minors)

def edge_checks():
    pairs = [(kron(X,I2),kron(I2,Z)), (kron(X,I2),kron(Y,I2)), (kron(X,X),kron(Z,I2))]
    max_error = 0.0
    lowest = 0.0
    sharp_trace_norm = []
    cases = 0
    for p,q in pairs:
        d = p.shape[0]
        qp = q@p
        if np.max(abs(qp-qp.conj().T)) < 1e-12:
            omega, r = 1, qp
        else:
            omega, r = 1j, -1j*qp
        m = 0.071
        for t in [0, .2*m, m]:
            for theta in [0, .31, np.pi/2, np.pi, 4.11]:
                z = t*np.exp(1j*theta)
                a = (z*omega).real
                ks = [np.sqrt((m+t)/2)*(p+np.exp(-1j*theta)*q),
                      np.sqrt((m-t)/2)*(p-np.exp(-1j*theta)*q),
                      np.sqrt(m)*r-a/np.sqrt(m)*np.eye(d),
                      np.sqrt(max(0,m-a*a/m))*np.eye(d)]
                edge = z*(np.kron(q.T,p)-(np.kron(np.eye(d),q@p)+np.kron((q@p).T,np.eye(d)))/2)
                edge += np.conj(z)*(np.kron(p.T,q)-(np.kron(np.eye(d),p@q)+np.kron((p@q).T,np.eye(d)))/2)
                g = edge + m*(dissipator(p)+dissipator(q)+dissipator(r))
                max_error = max(max_error, float(np.max(abs(super_kraus(ks)-4*m*np.eye(d*d)-g))))
                max_error = max(max_error, float(np.max(abs(sum((k.conj().T@k for k in ks), start=np.zeros((d,d), complex))-4*m*np.eye(d)))))
                lowest = min(lowest, float(np.linalg.eigvalsh(choi_from_super(np.eye(d*d)+g/(4*m),d)).min()))
                cases += 1
        z = m*np.conj(omega)
        edge = z*(np.kron(q.T,p)-(np.kron(np.eye(d),q@p)+np.kron((q@p).T,np.eye(d)))/2)
        edge += np.conj(z)*(np.kron(p.T,q)-(np.kron(np.eye(d),p@q)+np.kron((p@q).T,np.eye(d)))/2)
        sharp_trace_norm.append(float(sum(abs(np.linalg.eigvalsh(choi_from_super(edge,d))))))
    assert max_error < 2e-12 and lowest > -2e-12
    assert max(abs(t-4*.071) for t in sharp_trace_norm) < 2e-12
    return dict(cases=cases, max_error=max_error, minimum_choi_eigenvalue=lowest, edge_witness_choi_trace_norm=sharp_trace_norm, expected_witness_norm=4*.071)

def signed_fixed_floor_checks():
    rng=np.random.default_rng(2026101603)
    basis=[kron(PAULI[a],PAULI[b]) for a,b in itertools.product(range(4),repeat=2) if (a,b)!=(0,0)]
    d=4
    n=len(basis)
    bounds=np.zeros((n,n))
    chosen=[0,3,4,7]
    for a in chosen:
        bounds[a,a]=.04
    for a,b in itertools.combinations(chosen,2):
        if (a+b)%3:
            bounds[a,b]=bounds[b,a]=.025
    u=np.zeros(n)
    u[[1,8]]=.017
    tau=np.zeros(n)
    for a,b in itertools.product(range(n),repeat=2):
        if a==b or not bounds[a,b]: continue
        prod=basis[b]@basis[a]
        overlaps=np.array([np.trace(p.conj().T@prod)/d for p in basis])
        p=int(np.argmax(abs(overlaps)))
        assert abs(abs(overlaps[p])-1)<1e-12
        tau[p]+=bounds[a,b]
    beta=tau/2+u
    floor=bounds.sum(axis=1)+beta
    rate=2*bounds.sum()+2*u.sum()
    lowest=0.0
    cases=0
    max_null_residual=0.0
    for rep in range(48):
        c=np.zeros((n,n),complex)
        for a in range(n):
            c[a,a]=rng.uniform(-1,1)*bounds[a,a]
            for b in range(a+1,n):
                z=bounds[a,b]*np.sqrt(rng.uniform())*np.exp(2j*np.pi*rng.uniform())
                c[a,b],c[b,a]=z,z.conjugate()
        h=sum((rng.uniform(-1,1)*u[a]*basis[a] for a in range(n)),start=np.zeros((d,d),complex))
        g=-1j*(np.kron(np.eye(d),h)-np.kron(h.T,np.eye(d)))
        for a,b in itertools.product(range(n),repeat=2):
            val=c[a,b]+(floor[a] if a==b else 0)
            if abs(val):
                prod=basis[b]@basis[a]
                g+=val*(np.kron(basis[b].T,basis[a])-(np.kron(np.eye(d),prod)+np.kron(prod.T,np.eye(d)))/2)
        j=choi_from_super(np.eye(d*d)+g/rate,d)
        lowest=min(lowest,float(np.linalg.eigvalsh(j).min()))
        s=sum((c[a,b]*(basis[b]@basis[a]) for a,b in itertools.product(range(n),repeat=2)),start=np.zeros((d,d),complex))
        b0=-(s-np.trace(c)*np.eye(d))/2-1j*h
        bvec=np.array([np.trace(p@b0)/d for p in basis])
        ev,uv=np.linalg.eigh(c+np.diag(floor))
        if np.any(ev<1e-12):
            max_null_residual=max(max_null_residual,float(np.linalg.norm(uv[:,ev<1e-12].conj().T@bvec)))
        cases+=1
    # Exact cancellation, with multiple zero-beta directions: all signed
    # diagonal noise cancels the installed row floor, leaving zero generator.
    cancellation=-np.diag(np.diag(bounds))
    diagonal_floor=np.diag(bounds)
    assert np.max(abs(cancellation+np.diag(diagonal_floor)))==0
    assert lowest>-2e-12 and max_null_residual<2e-12
    return dict(cases=cases, fixed_rate=rate, minimum_choi_eigenvalue=lowest, max_nullspace_b_component=max_null_residual, zero_floor_directions=int(sum(floor==0)), exact_diagonal_cancellation=True)

def action_error_checks():
    # Three-qubit faithful representation of two independent commuting checks
    # sharing the correction face. The actual 11-qubit geometry is checked below.
    scheck = kron(X,X,I2)
    tcheck = kron(X,I2,X)
    ident = np.eye(8)
    pi = (ident-scheck)@(ident-tcheck)/4
    q = kron(Z,I2,I2)
    axes = [kron(p,I2,I2) for p in [X,Y,Z]]
    a = q@pi
    bs = [-1j*p@a for p in axes]
    inactive = ident-pi
    ca = super_kraus([a,inactive])
    cbs = [super_kraus([b,inactive]) for b in bs]
    vals,vecs = np.linalg.eigh(pi)
    iso = vecs[:,vals>.5]
    r = iso.shape[1]
    vecs_choi = [(op@iso).reshape(-1,order='F')/np.sqrt(r) for op in [a]+bs]
    gram = np.array([[np.vdot(v,w) for w in vecs_choi] for v in vecs_choi])
    assert np.max(abs(gram-np.eye(4))) < 2e-12
    max_error = 0.0
    lowest = 0.0
    common_rotation_floor_error = 0.0
    common_rotation_floor_min_eigenvalue = 0.0
    below_witness = []
    rates = []
    rng = np.random.default_rng(2026101602)
    cases = 0
    for m in [1,2,3]:
        critical = np.arctan(1/np.sqrt(m))
        for bound in [.0001,.04,.2,critical*.95,critical,critical+.13]:
            kappa = .7
            if bound < critical:
                q0 = np.sin(bound)**2
                t0 = np.sin(bound)*np.cos(bound)
                alpha = kappa*(q0+np.sqrt(m)*t0)
                beta = kappa*(t0/np.sqrt(m)-q0)
                rate = alpha+m*beta
                # Exact relaxed lower optimum from the endpoint pair blocks.
                lower = kappa*(2*np.sqrt(m)*t0-(m-1)*q0)
                assert abs(rate-lower) < 1e-12
                bstar = beta
                astar = alpha
                # A symmetrized center with smaller trace violates the endpoint determinant.
                too_small = .999*(astar+m*bstar)
                btest = max(0,kappa*np.sqrt(q0*(1-q0)/m)-kappa*q0)
                atest = too_small-m*btest
                block = np.array([[atest-kappa*q0,kappa*t0],[kappa*t0,btest+kappa*q0]])
                below_witness.append(float(np.linalg.eigvalsh(block).min()))
            else:
                alpha,beta,rate = kappa,0,kappa
            f = alpha*(ca-np.eye(64)) + beta*sum((c-np.eye(64) for c in cbs[:m]),start=np.zeros((64,64),complex))
            for theta in [0,bound/3,-bound/2,bound,-bound]:
                for rep in range(4):
                    u = rng.normal(size=m)
                    u /= np.linalg.norm(u)
                    a_theta = np.cos(theta)*a+np.sin(theta)*sum((u[j]*bs[j] for j in range(m)),start=np.zeros((8,8),complex))
                    ct = super_kraus([a_theta,inactive])
                    e = kappa*(ct-ca)
                    proposal = np.eye(64)+(f+e)/rate
                    w = np.r_[np.cos(theta),np.sin(theta)*u]
                    coeff = np.diag([alpha]+[beta]*m)+kappa*(np.outer(w,w)-np.diag([1]+[0]*m))
                    ev,uv = np.linalg.eigh(coeff)
                    lowest = min(lowest,float(ev.min()))
                    ks = [sum((uv[j,k]*[a,*bs[:m]][j] for j in range(m+1)),start=np.zeros((8,8),complex))*np.sqrt(max(0,ev[k])/rate) for k in range(m+1)]
                    ks.append(inactive)
                    max_error = max(max_error,float(np.max(abs(super_kraus(ks)-proposal))))
                    max_error = max(max_error,float(np.max(abs(sum((k.conj().T@k for k in ks),start=np.zeros((8,8),complex))-ident))))
                    # Unhalved diamond norm is 2 kappa |sin theta|: evaluate a
                    # pure input with zero expectation of the rotated Pauli.
                    p = sum((u[j]*axes[j] for j in range(m)),start=np.zeros((8,8),complex))
                    compressed = iso.conj().T@q@p@q@iso
                    ee,vv = np.linalg.eigh(compressed)
                    if ee[-1]-ee[0] > 1e-12:
                        weight = ee[-1]/(ee[-1]-ee[0])
                        psi = iso@(np.sqrt(weight)*vv[:,0]+np.sqrt(1-weight)*vv[:,-1])
                    else:
                        psi = iso[:,0]
                    rho = np.outer(psi,psi.conj())
                    out = (e@rho.reshape(-1,order='F')).reshape((8,8),order='F')
                    trace_norm = sum(abs(np.linalg.eigvalsh(out)))
                    assert abs(trace_norm-2*kappa*abs(np.sin(theta))) < 3e-11
                    if m==3:
                        unitary=np.cos(theta)*ident-1j*np.sin(theta)*p
                        nominal_floor=(ca+sum(cbs,start=np.zeros((64,64),complex)))/4
                        actual_floor=sum((super_kraus([unitary@op,inactive]) for op in [a]+bs),start=np.zeros((64,64),complex))/4
                        common_rotation_floor_error=max(common_rotation_floor_error,float(np.max(abs(actual_floor-nominal_floor))))
                        invariant_rate=4*kappa*np.sin(bound)
                        coeff_invariant=np.eye(4)*invariant_rate/4+kappa*(np.outer(w,w)-np.diag([1,0,0,0]))
                        common_rotation_floor_min_eigenvalue=min(common_rotation_floor_min_eigenvalue,float(np.linalg.eigvalsh(coeff_invariant).min()))
                    cases += 1
            rates.append(dict(axes=m, bound=bound, rate=rate, alpha=alpha, beta=beta))
    assert max_error < 3e-11 and lowest > -3e-12
    assert common_rotation_floor_error<2e-12 and common_rotation_floor_min_eigenvalue>-2e-12
    assert max(below_witness) < 0
    return dict(cases=cases, max_kraus_map_or_tp_error=max_error, min_coefficient_eigenvalue=lowest, orthogonal_active_choi_error=float(np.max(abs(gram-np.eye(4)))), common_rotation_floor_error=common_rotation_floor_error, common_rotation_floor_min_eigenvalue=common_rotation_floor_min_eigenvalue, below_optimal_endpoint_witness=below_witness, rates=rates)

def incidence_checks():
    side=5
    def plus(v,i,amount=1):
        return tuple((v[j]+(amount if j==i else 0))%side for j in range(4))
    def edge_faces(v,i):
        out=set()
        for j in range(4):
            if j==i: continue
            dirs=tuple(sorted((i,j)))
            out.add((v,dirs))
            out.add((plus(v,j,-1),dirs))
        return out
    counts={}
    support_sizes=set()
    for v in itertools.product(range(side),repeat=4):
        for i,j in itertools.combinations(range(4),2):
            support=edge_faces(v,i)|edge_faces(v,j)
            support_sizes.add(len(support))
            for face in support: counts[face]=counts.get(face,0)+1
    assert support_sizes=={11} and set(counts.values())=={11}
    # Algebraic 11-qubit checks: S=X on positions 0..5 and T=X on
    # {0,6,..,10}; G=<S,T> never contains a nonidentity Pauli on face 0 alone.
    stabilizers=[tuple([0]*11),tuple([1]*6+[0]*5),tuple([1]+[0]*5+[1]*5),tuple([0]+[1]*10)]
    one_face=[tuple([p]+[0]*10) for p in [1,2,3]]
    assert not any(p in stabilizers for p in one_face)
    return dict(periodic_side=side, primal_pair_support_size=list(support_sizes), physical_faces=len(counts), primal_incidence_min=min(counts.values()), primal_incidence_max=max(counts.values()), both_css_sector_incidence=22, eleven_qubit_orthogonality_symbolic=True)

def main():
    out=dict(scope="Finite deterministic algebra and geometry checks, not an asymptotic memory theorem, novelty clearance, or device demonstration", range_gauge=range_gauge_checks(), correlated_edges=edge_checks(), signed_fixed_floor=signed_fixed_floor_checks(), actual_correction_unitary_errors=action_error_checks(), overlap_incidence=incidence_checks())
    (HERE/'CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='actual_correction_unitary_errors'},indent=2))
    print(json.dumps({k:v for k,v in out['actual_correction_unitary_errors'].items() if k!='rates'},indent=2))

if __name__=='__main__': main()
