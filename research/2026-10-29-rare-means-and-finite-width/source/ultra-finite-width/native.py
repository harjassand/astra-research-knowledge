"""Native Hubbard compiler; no Gaussian or collision closure.

Basis: all up orbitals, then all down orbitals; grade q has q of each.
The grade basis is rephased by (-1)**(q*(q-1)//2), making the onsite
source at site zero positive. All Hamiltonian entries are stored as the
EXACT INTEGERS 20*(H+shift*I). Mathematical/numerical contract: PROOF.md.
"""
import argparse
import hashlib
import itertools
import json
import math
import resource
import time
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy import sparse

HERE = Path(__file__).resolve().parent


def masks(L, q):
    return np.array([sum(1 << j for j in c)
                     for c in itertools.combinations(range(L), q)], dtype=np.int64)


def grid_edges(nx, ny):
    return [(x+nx*y, x+1+nx*y) for y in range(ny) for x in range(nx-1)] + [
        (x+nx*y, x+nx*(y+1)) for y in range(ny-1) for x in range(nx)]


def one_hop(ms, edges):
    lookup = {int(m): i for i, m in enumerate(ms)}
    rows, cols, vals = [], [], []
    for col, mm in enumerate(ms):
        m = int(mm)
        for i, j in edges:
            if ((m >> i) ^ (m >> j)) & 1:
                nn = m ^ (1 << i) ^ (1 << j)
                sign = -1 if (m & ((1 << j)-(1 << (i+1)))).bit_count() % 2 else 1
                rows.append(lookup[nn]); cols.append(col); vals.append(-20*sign)
    n = len(ms)
    return sparse.csr_matrix((np.array(vals, dtype=np.float64), (rows, cols)), shape=(n,n))


def compile_hubbard(nx, ny, cutoff, U=8):
    start = time.perf_counter()
    L = nx*ny
    if L > 60 or cutoff > L:
        raise ValueError('literal mask compiler requires L<=60 and cutoff<=L')
    edges = grid_edges(nx, ny)
    sector_masks = [masks(L,q) for q in range(cutoff+1)]
    dims = [len(x)**2 for x in sector_masks]
    off = np.cumsum([0]+dims).astype(np.int64)
    blocks, pairs = [], []
    shift = U*cutoff//2
    for q, ms in enumerate(sector_masks):
        n = len(ms)
        T = one_hop(ms, edges)
        I = sparse.eye(n, format='csr')
        diag = np.array([20*(U*((int(a)&int(b)).bit_count()-q)+shift)
                         for a in ms for b in ms], dtype=np.float64)
        blocks.append(sparse.kron(T,I,format='csr')+sparse.kron(I,T,format='csr')+
                      sparse.diags(diag,format='csr'))
        if q < cutoff:
            next_lookup = {int(m):i for i,m in enumerate(sector_masks[q+1])}
            src1 = np.flatnonzero((ms & 1)==0)
            dst1 = np.array([next_lookup[int(ms[i])|1] for i in src1],dtype=np.int64)
            src = (src1[:,None]*n+src1[None,:]).ravel()+off[q]
            nn = len(sector_masks[q+1])
            dst = (dst1[:,None]*nn+dst1[None,:]).ravel()+off[q+1]
            pairs.append((src,dst))
    H = sparse.block_diag(blocks,format='csr')
    if pairs:
        rows=np.concatenate([x for src,dst in pairs for x in (src,dst)])
        cols=np.concatenate([x for src,dst in pairs for x in (dst,src)])
        H += sparse.csr_matrix((np.ones(len(rows)),(rows,cols)),shape=H.shape)
    H.sort_indices()
    maxrow = int(np.max(np.asarray(abs(H).sum(axis=1))))
    d = int(np.max(np.diff(H.indptr)))
    receipt = dict(nx=nx,ny=ny,L=L,J='1',U=str(U),epsilon='1/20',theta='pi/2',
                   cutoff=cutoff,sector_dimensions=dims,dimension=int(off[-1]),
                   full_balanced_dimension=math.comb(2*L,L),edges=len(edges),
                   matrix_nnz=int(H.nnz),integer_scale=20,shift=shift,
                   integer_row_norm=maxrow,max_row_nonzeros=d,
                   compile_seconds=time.perf_counter()-start)
    return H, pairs, sector_masks, off, receipt


def exp_upper(x):
    """Exact positive rational upper enclosure of exp(x), x>=0."""
    if x < 0: raise ValueError('positive x')
    term=total=F(1)
    n=0
    while True:
        n+=1; term*=x/n; total+=term
        if n > 2*x and term < F(1,10**65):
            ratio=x/(n+1)
            return total+term*ratio/(1-ratio)


def remainder_upper(z, m):
    partial=sum((z**r/F(math.factorial(r)) for r in range(m)),F(0))
    return exp_upper(z)-partial


def gamma(n):
    nu=F(n,2**53)
    return nu/(1-nu)


def numerical_bound(receipt, total_time, steps, degree):
    a=F(receipt['integer_row_norm'])*total_time/(20*steps)
    rho=gamma(2*receipt['max_row_nonzeros']+8)
    trunc=exp_upper(a)*a**(degree+1)/math.factorial(degree+1)
    rounded=exp_upper(a*(1+rho))*(a*rho+gamma(degree+1))
    local=trunc+rounded+F(1,10**280)
    state=steps*local*exp_upper(steps*local)
    D=receipt['dimension']
    # Conservative sequential-double bound for all observable reductions.
    reduction=gamma(16*D+100)*(1+state)**2
    observable=2*state*(1+state)+reduction
    return dict(a=a,local=local,state=state,reduction=reduction,observable=observable)


def fraction_record(x):
    # Small rational upper prevents huge exact exp-series denominators in JSON.
    scale=10**45
    upper=F((x.numerator*scale+x.denominator-1)//x.denominator,scale)
    return {'upper_fraction':str(upper),'upper_float':float(upper)}


def evolve(H, t=F(10), steps=60, degree=36):
    D=H.shape[0]
    state=np.zeros(D,dtype=np.complex128); state[0]=1
    denom_base=F(20*steps,1)/t
    if denom_base.denominator != 1:
        raise ValueError('this receiver uses exactly representable integer denominators')
    den=int(denom_base)
    tic=time.perf_counter()
    for _ in range(steps):
        term=state.copy(); result=state.copy()
        for r in range(1,degree+1):
            term=H.dot(term)
            term *= -1j
            term /= den*r
            result += term
        state=result
    return state,time.perf_counter()-tic


def quantities(state, pairs, sector_masks, off):
    creation=sum((np.vdot(state[dst],state[src]) for src,dst in pairs),0j)
    nup=ndn=double=0.
    pops=[]
    for q,ms in enumerate(sector_masks):
        X=state[off[q]:off[q+1]].reshape(len(ms),len(ms))
        prob=abs(X)**2
        occ=(ms&1).astype(float)
        nup+=float(np.sum(prob*occ[:,None]));ndn+=float(np.sum(prob*occ[None,:]))
        double+=float(np.sum(prob*occ[:,None]*occ[None,:]))
        pops.append(float(np.sum(prob)))
    return dict(density_excess_at_source=2*creation.real,
                eta_y_at_source=creation.imag,defect_populations=pops,
                defect_nup=nup,defect_ndown=ndn,defect_double=double,
                anomalous_creation_real=creation.real,anomalous_creation_imag=creation.imag,
                wick_connected_diagnostic=double-nup*ndn-abs(creation)**2,
                norm_squared=float(np.vdot(state,state).real))


def main():
    a=argparse.ArgumentParser()
    a.add_argument('--nx',type=int,default=4);a.add_argument('--ny',type=int,default=4)
    a.add_argument('--cutoff',type=int,default=3)
    a.add_argument('--out',default='PREDICTION.json')
    args=a.parse_args()
    H,pairs,ms,off,r=compile_hubbard(args.nx,args.ny,args.cutoff)
    t=F(10);steps=60;degree=36
    nb=numerical_bound(r,t,steps,degree)
    r['propagation_contract']=dict(time=str(t),steps=steps,degree=degree,
          integer_matvecs=steps*degree,rounding_model='IEEE754 binary64 round-to-nearest, no overflow; underflow floor included',
          bounds={k:fraction_record(v) for k,v in nb.items()})
    state,sec=evolve(H,t,steps,degree)
    r['propagation_seconds']=sec
    r['observables']=quantities(state,pairs,ms,off)
    z=F(1,2);K=args.cutoff
    # State error and observable return-path error are independently available.
    tail_state=remainder_upper(z,K+1)
    tail_observable=2*remainder_upper(2*z,2*K+1)
    err=tail_observable+nb['observable']
    r['qualification']=dict(state_error_upper=fraction_record(tail_state),
          density_return_path_error_upper=fraction_record(tail_observable),
          density_total_error_upper=fraction_record(err),
          eta_y_total_error_upper=fraction_record(err/2),
          meaning='ideal finite Hubbard input; no state preparation/experiment acquired; not generic thermal prediction')
    r['peak_RSS_bytes']=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    r['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE/args.out).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'file':args.out,'dimension':r['dimension'],'seconds':sec,
                      'density_excess':r['observables']['density_excess_at_source'],
                      'eta_y':r['observables']['eta_y_at_source'],
                      'error':float(err),'wick':r['observables']['wick_connected_diagnostic']}))


if __name__=='__main__':main()
