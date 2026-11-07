"""Stronger signed Schur audit and matched factor-residual interval comparator.

Guarantee scope: exact real matrix whose entries are the saved IEEE-754 H
values. Uses the standard IEEE rounding model, no under/overflow, and BLAS
dot products with at most n multiplications/additions. Not an end-to-end
certificate for the exact decimal FCIDUMP integral transformation.
"""
import time
START=time.perf_counter()
import json
import math
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy import linalg,sparse
from scipy.sparse.linalg import eigsh
from pyscf import lib

lib.num_threads(1)
BASE=Path(__file__).resolve().parent
OUT={"guarantee_scope":"exact real matrix with saved floating-point H entries, standard IEEE rounding-model assumptions; FCIDUMP-to-H transformation and physical model error are outside certificate", "claim":"NOT_ACHIEVED", "arithmetic_assumptions":["IEEE binary64 round-to-nearest basic operations", "BLAS dot products obey standard gamma_n bound", "no overflow, underflow, or nonfinite values", "error formulas conservatively rounded upward"]}


def up(x):
    return float(np.nextafter(float(x),np.inf))


def down(x):
    return float(np.nextafter(float(x),-np.inf))


def gamma(k):
    u=Fraction(1,2**53)
    return up(float(k*u/(1-k*u)))


def add(*x):
    return up(math.fsum(x))


def mul(a,b):
    return up(a*b)


def ni(A):
    """Upward infinity norm bound for a matrix of stored exact floats."""
    if not A.size:return 0.
    raw=float(np.sum(np.abs(A),axis=1).max())
    return up(float(Fraction.from_float(raw)/(1-Fraction.from_float(gamma(A.shape[1])))))


def n1(A):
    return ni(A.T)


def dot_bound(F):
    return mul(gamma(F.shape[1]),mul(ni(F),n1(F)))


def residual_factor_bound(A,shift,F):
    K=F@F.T
    R=A-K
    R[np.diag_indices_from(R)]-=shift
    # Product error plus the two floating subtractions in each entry.
    err=add(dot_bound(F),mul(gamma(3),add(ni(A),abs(shift),ni(K))))
    delta=add(ni(R),err)
    return delta,dict(computed_residual_norm=ni(R),rounding_allowance=err)


def rayleigh_upper(H,v):
    v=np.asarray(v,dtype=float)
    v1=up(math.fsum(np.abs(v).tolist()))
    denom=float(v@v)
    derr=mul(gamma(len(v)),up(float(Fraction.from_float(denom)/(1-Fraction.from_float(gamma(len(v)))))))
    numerator=float(v@(H@v))
    # Deliberately coarse absolute error bound avoids cancellation assumptions.
    nerr=mul(gamma(2*len(v)+2),mul(ni(H),mul(v1,v1)))
    candidates=[(Fraction.from_float(numerator)+sn*Fraction.from_float(nerr))/(Fraction.from_float(denom)+sd*Fraction.from_float(derr)) for sn in [-1,1] for sd in [-1,1]]
    return up(float(max(candidates))),dict(rayleigh=numerator/denom,numerator_error_bound=nerr,denominator_error_bound=derr)


def safe_diag(C,w):
    """C >= diag(D) via weighted pairwise square completion.

    D_i=C_ii-sum_{j!=i}|C_ij| w_j/w_i. Ratios, products, sum
    are rounded outward using conservative gamma bounds.
    """
    off=np.abs(C).copy();np.fill_diagonal(off,0.)
    raw=(off@w)/w
    g=Fraction.from_float(gamma(C.shape[1]+3))
    sums_upper=np.asarray([up(float(Fraction.from_float(float(x))/(1-g))) for x in raw])
    D=np.nextafter(np.diag(C)-sums_upper,-np.inf)
    return D


def schur_root(A,B,D):
    upper=float(linalg.eigh(A,subset_by_index=[0,0],eigvals_only=True)[0])
    lo=min(float(np.diag(A).min()-np.abs(A-np.diag(np.diag(A))).sum(axis=1).max()-np.abs(B).sum(axis=1).max()),float(D.min()-np.abs(B).sum(axis=0).max()))-1
    hi=min(upper,float(D.min()))-1e-9
    for _ in range(36):
        x=(lo+hi)/2
        T=B/np.sqrt(D-x)[None,:]
        Q=A-T@T.T
        Q[np.diag_indices_from(Q)]-=x
        e=float(linalg.eigh(Q,subset_by_index=[0,0],eigvals_only=True,check_finite=False)[0])
        if e>0:lo=x
        else:hi=x
    return down(lo-1e-7)


def certify_schur(A,B,D,shift):
    d=D-shift
    if d.min()<=0:raise ValueError('complement diagonal not positive')
    s=np.sqrt(d)
    T=B/s[None,:]
    Q=A-T@T.T
    Q[np.diag_indices_from(Q)]-=shift
    F=np.tril(linalg.cholesky(Q,lower=True,check_finite=False))
    K=F@F.T+T@T.T
    R=A-K;R[np.diag_indices_from(R)]-=shift
    # Product and sum errors in the top-left block.
    err_A=add(dot_bound(F),dot_bound(T),mul(gamma(4),add(ni(A),abs(shift),mul(ni(F),n1(F)),mul(ni(T),n1(T)))))
    da=add(ni(R),err_A)
    E=B-T*s[None,:]
    # One product/subtraction per entry in the off-diagonal residual.
    eerr_inf=mul(gamma(3),add(ni(B),mul(ni(T),float(s.max()))))
    eerr_one=mul(gamma(3),add(n1(B),mul(n1(T),float(s.max()))))
    ei=add(ni(E),eerr_inf);eo=add(n1(E),eerr_one)
    diag_res=np.abs(d-s*s)
    dd=add(float(diag_res.max()),mul(gamma(3),add(float(np.abs(D).max()),abs(shift),float((s*s).max()))))
    delta=max(add(da,ei),add(eo,dd))
    # Exact PSD factors plus C-diag(D) give H >= shift-delta.
    return down(shift-delta),dict(factor_residual_bound=delta,top_left=da,off_row=ei,off_column=eo,diagonal=dd)


def save():
    OUT['elapsed_seconds']=time.perf_counter()-START
    (BASE/'STRONG_AUDIT.json').write_text(json.dumps(OUT,indent=2))
    print(json.dumps(OUT),flush=True)


def main():
    t=time.perf_counter()
    data=np.load(BASE/'hamiltonian.npz');H=data['H'];addr=data['addresses']
    j=json.loads((BASE/'BENCHMARK.json').read_text())
    OUT['matrix_load_seconds']=time.perf_counter()-t
    fullv=np.load(BASE/'reference_vector.npy').ravel()[addr]
    t=time.perf_counter()
    u,ud=rayleigh_upper(H,fullv)
    shift=u-1e-6
    F=np.tril(linalg.cholesky(H-np.eye(len(H))*shift,lower=True,check_finite=False))
    delta,detail=residual_factor_bound(H,shift,F)
    low=down(shift-delta)
    OUT['verified_full_factor_comparator']=dict(lower=low,upper=u,width=u-low,wall_seconds=time.perf_counter()-t,detail=detail,rayleigh=ud,additional_costs='same full matrix acquisition plus the FCI vector solve; all previously measured')
    save()
    # Same residual/PT2 determinant selection as first benchmark, no reference vector.
    P=np.argsort(np.diag(H))[:1].tolist();ids=np.arange(len(H));rows=[]
    for size in [128,512]:
        t=time.perf_counter()
        while len(P)<size:
            p=np.asarray(P);q=np.setdiff1d(ids,p)
            e,v=linalg.eigh(H[np.ix_(p,p)],subset_by_index=[0,0])
            r=H[np.ix_(q,p)]@v[:,0]
            score=r*r/np.maximum(np.diag(H)[q]-e[0],1e-8)
            P.extend(q[np.argsort(score)[::-1][:min(size-len(P),max(1,len(P)))]].tolist())
        selection_seconds=time.perf_counter()-t
        p=np.asarray(P);q=np.setdiff1d(ids,p)
        A=H[np.ix_(p,p)];B=H[np.ix_(p,q)];C=H[np.ix_(q,q)]
        e,v=linalg.eigh(A,subset_by_index=[0,0]);vec=np.zeros(len(H));vec[p]=v[:,0]
        u,ud=rayleigh_upper(H,vec)
        schemes=[]
        weights=[('unscaled',np.ones(len(C)))]
        # Access to the full complement is charged here, never supplied freely.
        cabs=np.diag(np.diag(C)+np.abs(np.diag(C)))-np.abs(C)
        ew,vw=eigsh(sparse.csr_matrix(cabs),k=1,which='SA',tol=1e-9)
        for floor in [1e-2,1e-6,1e-8]:weights.append((f'perron_floor_{floor}',np.maximum(np.abs(vw[:,0]),floor)))
        for name,w in weights:
            tc=time.perf_counter();D=safe_diag(C,w)
            shift=schur_root(A,B,D)
            low,detail=certify_schur(A,B,D,shift)
            schemes.append(dict(weights=name,lower=low,upper=u,width=u-low,lower_error_to_reference=float(j['reference_energy']-low),wall_seconds=time.perf_counter()-tc,detail=detail,min_diagonal_floor=float(D.min())))
        rows.append(dict(size=size,selection_seconds=selection_seconds,total_seconds=time.perf_counter()-t,upper=u,upper_reference_error=float(u-j['reference_energy']),rayleigh=ud,schemes=schemes))
        OUT['signed_schur']=rows
        save()
    OUT['decision']='STOP scalar/block comparison certificate as enabling capability on this instance: no new operation or advantage established. Keep benchmark access and verified matrix-interval comparator.'
    save()


if __name__=='__main__':main()
