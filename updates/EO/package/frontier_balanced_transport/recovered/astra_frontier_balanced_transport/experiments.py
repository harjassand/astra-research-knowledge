"""Executed diagnostics. Rational certificates are separated from float comparisons."""
import json, time
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
from pauli_core import *

ROOT=Path(__file__).parent

def matrix(O,n):
    N=1<<n
    out=np.zeros((N,N),complex)
    for (x,z),v in O.items():
        ph=1j**((x&z).bit_count())
        for j in range(N):
            out[j^x,j]+=float(v)*ph*((-1)**((z&j).bit_count()))
    return out

def direct_response(H,J,n,gamma):
    """Sparse full-sector Liouvillian solves; floating diagnostic, NOT certificate."""
    h=matrix(H,n); jmat=matrix(J,n); result=0.; maxres=0.; sizes=[]
    for charge in range(1,n):
        states=[s for s in range(1<<n) if s.bit_count()==charge]
        m=len(states); sizes.append(m*m)
        hs=sparse.csc_matrix(h[np.ix_(states,states)])
        js=jmat[np.ix_(states,states)]
        Id=sparse.eye(m,format='csc')
        rates=np.array([2*float(gamma)*(x^y).bit_count() for y in states for x in states])
        B=-1j*(sparse.kron(Id,hs)-sparse.kron(hs.T,Id))+sparse.diags(rates)
        vI=np.eye(m).reshape(-1,order='F')
        col=sparse.csc_matrix(vI[:,None])
        aug=sparse.bmat([[B,col],[col.T,None]],format='csc')
        rhs=np.r_[js.reshape(-1,order='F'),0.]
        sol=spsolve(aug,rhs)
        maxres=max(maxres,float(np.linalg.norm(aug@sol-rhs)))
        result+=float(np.vdot(rhs[:-1],sol[:-1]).real)/(1<<n)/n
    return result,maxres,sizes

def optimal_upper_basis(H,J,raw,n,edges,gamma):
    """Find a rational upper trial; exact pressure + exact certificates afterwards."""
    # Baseline pressure ensures PA Sinv(J-Aphi0)=0. May vanish by symmetry.
    _,base,_,_=compile_pair(H,J,{},n,edges,gamma)
    basis=[]
    for g0 in raw:
        # pressure linear-affine correction; subtract baseline to get linear direction
        _,g,_,_=compile_pair(H,J,g0,n,edges,gamma)
        basis.append(add(g,scale(base,-1)))
    y0=add(J,scale(A(H,base),-1))
    a=[A(H,g) for g in basis]
    m=len(basis)
    C=sp.Matrix([[inner(a[i],Sinv(a[j],gamma))+inner(basis[i],S(basis[j],gamma)) for j in range(m)] for i in range(m)])
    r=sp.Matrix([inner(a[i],Sinv(y0,gamma))-inner(basis[i],S(base,gamma)) for i in range(m)])
    # Exact independent column selection if a trial basis is redundant.
    piv=C.rref()[1]
    coef=[Q(0)]*m
    if piv:
        cc=C.extract(piv,piv).inv()*r.extract(piv,[0])
        for p,v in zip(piv,cc): coef[p]=Q(int(sp.numer(v)),int(sp.denom(v)))
    g=add(base,*[scale(b,c) for b,c in zip(basis,coef)])
    f=Sinv(add(J,scale(A(H,g),-1)),gamma)
    assert not P(A(H,f))
    return f,g,coef

def rational_record(x): return {'exact':str(x),'float':float(x)}

def main():
    log={'status':'Exact rational identities and certificates; floating full-state comparisons separately labeled',
         'model':'periodic chain H=-t/2 sum(XX+YY)+U/4 sum ZZ_1+V/4 sum ZZ_2, J=t/2 sum(XY-YX)',
         'conventions':'normalized Hilbert-Schmidt inner product; kappa=Tr(J B^-1 J)/(n 2^n); gamma*(Z O Z-O); d=4 gamma',
         'exact_algebra':[], 'numerics':[], 'pressure_tests':[]}
    for n in (7,8,11,17):
        H,J,Hhop,edges=model(n)
        assert not A(Hhop,J)
        assert norm2(J)/n==Q(1,2)
        assert norm2(A(H,J))/norm2(J)==5
        gamma=Q(1,2)
        for m in (1,3,7,11):
            phi={(0,m):Q(2,3)}
            lhs=scale(P(A(H,Sinv(A(H,phi),gamma))),-1)
            assert lhs==M_diagonal(phi,edges,gamma)
        f=scale(J,Q(2,9))
        low,up,gap=certificate(H,J,f,{},n,gamma)
        assert low==Q(1,9) and up==Q(1,4)
        log['exact_algebra'].append({'n':n,'a':'1/2','v':'5','D_lower':'4/9','D_upper':'1','verified_M_sources':4})
    # A hand-built inhomogeneous source tests nontrivial diagonal correction.
    n=7; gamma=Q(1,2)
    H,J,_,edges=model(n,fields=[Q(i%3-1,3) for i in range(n)])
    raw=scale(A(H,J),Q(-1,10))
    f,g,phi,report=compile_pair(H,J,raw,n,edges,gamma)
    low,up,gap=certificate(H,J,f,g,n,gamma)
    log['pressure_tests'].append({'n':n,'phi_terms':len(phi),'blocks':report,'balanced_exactly':True,
       'gap_identity_exact':True,'raw_trial_lower':rational_record(low),'raw_trial_upper':rational_record(up)})
    for n in (7,8):
        H,J,_,edges=model(n); gamma=Q(1,2)
        aj=A(H,J)
        # Krylov-even directions. Do not imply system-size-uniform closure.
        raw=[aj]
        ak=aj
        for depth in (1,2):
            if depth==2:
                ak=off(A(H,A(H,ak)))
                raw.append(ak)
            tic=time.perf_counter()
            f,g,coef=optimal_upper_basis(H,J,raw,n,edges,gamma)
            low,up,gap=certificate(H,J,f,g,n,gamma)
            log['numerics'].append({'n':n,'trial_directions':depth,
                 'kappa_lower_exact':str(low),'kappa_upper_exact':str(up),
                 'D_lower':float(4*low),'D_upper':float(4*up),'width':float(4*gap),
                 'f_terms':len(f),'g_terms':len(g),'coefficient_bit_max':max([max(abs(c.numerator).bit_length(),c.denominator.bit_length()) for c in coef]+[0]),
                 'certificate_seconds':time.perf_counter()-tic})
        tic=time.perf_counter(); kappa,res,sizes=direct_response(H,J,n,gamma)
        log['numerics'].append({'n':n,'diagnostic':'floating full-sector solve','kappa':kappa,'D':4*kappa,
                   'linear_residual':res,'max_sector_superoperator_dimension':max(sizes),
                   'seconds':time.perf_counter()-tic})
        # Exact free-chain reference is a normalization check.
        H0,J0,_,edges0=model(n,U=Q(0),V=Q(0))
        assert not A(H0,J0)
        ff=scale(J0,Q(1,2))
        lo,hi,_=certificate(H0,J0,ff,{},n,gamma)
        assert lo==hi==Q(1,4)
    log['design_decision']={'t':'1','U':'4','V':'1','d_target':'2','D_target_lower':'4/9',
       'd_reference':'16','D_reference_upper':'1/8','guaranteed_ratio_lower':'32/9',
       'interpretation':'Physical dephasing differs; no zero-noise extrapolation. Bound maximizer is not claimed true optimizer.'}
    (ROOT/'checks.json').write_text(json.dumps(log,indent=2))
    print(json.dumps(log,indent=2))
if __name__=='__main__': main()
