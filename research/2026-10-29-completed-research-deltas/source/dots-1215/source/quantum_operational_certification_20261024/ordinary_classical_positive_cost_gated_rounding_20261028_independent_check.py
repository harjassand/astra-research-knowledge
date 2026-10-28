#!/usr/bin/env python3
"""Independent checks of frozen gated-rounding proof; not a production SDP/sampler."""
from pathlib import Path
import hashlib,json,itertools,math
from fractions import Fraction as Q
import numpy as np
import sympy as sp
import mpmath as mp
mp.mp.dps=65
base=Path(__file__).resolve().parent
src='ordinary_classical_positive_cost_gated_rounding_20261028.md'
new='ordinary_classical_positive_cost_gated_rounding_log_improvement_20261028.md'
rng=np.random.default_rng(281051)
def f(q): return float(q)
def trace(A,B): return sum(A[i,j]*B[j,i] for i in range(A.rows) for j in range(A.cols))
def digest(p): return hashlib.sha256((base/p).read_bytes()).hexdigest()
def mpq(x): return mp.mpf(str(sp.numer(x)))/mp.mpf(str(sp.denom(x)))
def signcov(Y):
    n=Y.rows
    return np.array([[float(2*mp.asin(max(mp.mpf(-1),min(mp.mpf(1),mpq(Y[i,j]))))/mp.pi) for j in range(n)] for i in range(n)])
min_loewner=1.;min_parallel=1.;orig_caps=[];parallel_caps=[];count_group=0;cube_count=0;tail_cases=0;empty_cases=0
for case in range(84):
    n=3+case%6
    levels=rng.integers(1,7,size=n).tolist()
    if case%7==0: levels=[20]*n
    elif case%7==1: levels[-1]=24
    roots=[sp.Rational(int(rng.choice([4,6,7])),8)*sp.Rational(1,2**j) for j in levels]
    p=sp.Matrix([r*r for r in roots])
    v=sp.Matrix([r*sp.Rational(int(rng.choice([-2,-1,1,2])),4) for r in roots])
    vv=sp.Matrix([r*sp.Rational(int(rng.choice([-1,1])),4) for r in roots])
    residual=[p[i]-p[i]**2-v[i]**2-vv[i]**2 for i in range(n)]
    assert all(x>0 for x in residual)
    Mrest=p*p.T+v*v.T+vv*vv.T+sp.diag(*residual)
    M=sp.zeros(n+1);M[0,0]=1;M[0,1:]=p.T;M[1:,0]=p;M[1:,1:]=Mrest
    assert all(M[i+1,i+1]==p[i] for i in range(n))
    G=sp.Matrix(rng.integers(-3,4,size=(4,n+1)).tolist())
    if case%3!=0:G[:,0]=sp.zeros(4,1)
    if case%7 not in [0,1]:
        for i in range(n):G[:,i+1]*=2**levels[i]
    A=G.T*G;a=max(sp.Integer(1),sp.trace(A));m=sp.Rational([1,4,12][case%3],4)
    w=[sp.Integer(2)**int(j) for j in rng.integers(0,11,size=n)]
    d=m+sum(w[i]*p[i] for i in range(n));S=trace(A,M);F=S/d;R0=A[0,0]/m
    delta=min(sp.Rational(1,2),m/(64*a*n));keep=[i for i in range(n) if p[i]>=delta];tail=[i for i in range(n) if p[i]<delta]
    tail_cases+=bool(tail);empty_cases+=not keep
    groups={}
    for i in keep:
        upper=sp.Integer(1)
        while p[i]<=upper/2:upper/=2
        groups.setdefault(upper,[]).append(i)
    L=len(groups);Skeep=trace(A.extract([i+1 for i in keep],[i+1 for i in keep]),Mrest.extract(keep,keep)) if keep else sp.Integer(0)
    Stail=trace(A.extract([i+1 for i in tail],[i+1 for i in tail]),Mrest.extract(tail,tail)) if tail else sp.Integer(0)
    assert Stail<=m/64 and S<=2*A[0,0]+4*Skeep+m/16
    if F>=1 and R0<F/4:assert L>0 and Skeep/d>=F/16
    allmu=np.zeros(n);allcov=np.zeros((n,n));blockM=np.zeros((n,n));infos=[]
    for upper,I in groups.items():
        MI=Mrest.extract(I,I);Y=MI/upper+sp.diag(*[1-p[i]/upper for i in I]);assert all(Y[j,j]==1 for j in range(len(I)))
        Esgn=signcov(Y);pf=f(upper);mu=np.full(len(I),pf/2);cov=pf*Esgn/4+pf*(1-pf)*np.ones((len(I),len(I)))/4
        moment=cov+np.outer(mu,mu);MI_np=np.array(MI,dtype=float)
        eig=np.linalg.eigvalsh(moment-MI_np/(2*math.pi))[0]/max(1,np.linalg.norm(MI_np));min_loewner=min(min_loewner,eig)
        assert eig>-2e-12
        eigc=np.linalg.eigvalsh(cov-MI_np/(2*math.pi))[0]/max(1,np.linalg.norm(MI_np));assert eigc>-2e-12
        allmu[I]=mu;allcov[np.ix_(I,I)]=cov;blockM[np.ix_(I,I)]=MI_np
        AI=A.extract([i+1 for i in I],[i+1 for i in I]);SI=trace(AI,MI);ci=m+sum(w[i]*p[i] for i in I)
        EN=f(A[0,0])+2*np.dot(np.array([A[0,i+1] for i in I],dtype=float),mu)+np.sum(np.array(AI,dtype=float)*moment)
        Eu=f(m)+np.dot(np.array([w[i] for i in I],dtype=float),mu)
        assert max(f(R0),EN/Eu)+1e-9>=f(SI/ci)/(8*math.pi)
        infos.append((SI/ci,EN,Eu));count_group+=1
    if L:
        diff=allcov+np.outer(allmu,allmu)-blockM/(2*math.pi)
        mine=np.linalg.eigvalsh(diff)[0]/max(1,np.linalg.norm(blockM));min_parallel=min(min_parallel,mine);assert mine>-2e-12
        EN=f(A[0,0])+2*np.dot(np.array(A[0,1:],dtype=float).ravel(),allmu)+np.sum(np.array(A[1:,1:],dtype=float)*(allcov+np.outer(allmu,allmu)))
        Eu=f(m)+np.dot(np.array(w,dtype=float),allmu)
        assert Eu<=f(d)+1e-9
        if F>=1:
            t=f(F)/(4096*L*L)
            if f(R0)<t:
                _,Eg,ug=max(infos,key=lambda x:x[0]);ratio=(Eg-2*t*ug)/(t*f(m));orig_caps.append(ratio);assert ratio>13-1e-8
            t=f(F)/(1024*L)
            if f(R0)<t:
                ratio=(EN-2*t*Eu)/(t*f(m));parallel_caps.append(ratio);assert ratio>6-1e-8
            assert max(f(R0),EN/Eu)+1e-9>=f(F)/(32*math.pi*L)
    if case<48:
        best=0.
        for bits in itertools.product([0,1],repeat=n):
            z=sp.Matrix([1,*bits]);val=(z.T*A*z)[0]/(m+sum(w[i]*bits[i] for i in range(n)));best=max(best,f(val))
        if F>=1 and L:assert best+1e-9>=f(F)/(32*math.pi*L)
        cube_count+=1
# Exact logarithmic gap family, including explicit RLT violation.
gaps=[]
for n in range(1,65):
    p=[sp.Rational(1,4**i) for i in range(1,n+1)];r=[sp.Rational(1,2**i) for i in range(1,n+1)]
    S=sum(r)**2+sp.Rational(n*n+n,2)-sum(p);F=S/(n+1)
    assert F>=sp.Rational(n,2)
    a=sum(4**i for i in range(1,n+1));assert a>0
    if n<=11:
        best=max(sp.Rational(sum(2**i*z for i,z in enumerate(bits,1))**2,1+sum(4**i*z for i,z in enumerate(bits,1))) for bits in itertools.product([0,1],repeat=n))
        assert best<4;gaps.append({'n':n,'moment_ratio':str(F),'exact_cube_max':str(best)})
assert sp.Rational(1,4)*sp.Rational(1,16)+sp.Rational(1,2)*sp.Rational(1,2)*sp.Rational(1,4)==sp.Rational(5,64)>sp.Rational(1,16)
common={'feasible_PSD_moment_cases':84,'group_moment_checks':count_group,'exhaustive_cube_cases':cube_count,'tail_cases':tail_cases,'empty_retained_cases':empty_cases,'minimum_group_normalized_Loewner_eigenvalue':min_loewner,'minimum_parallel_normalized_Loewner_eigenvalue':min_parallel,'original_finite_margin_cases':len(orig_caps),'minimum_original_margin_over_tm':min(orig_caps),'parallel_finite_margin_cases':len(parallel_caps),'minimum_parallel_margin_over_tm':min(parallel_caps)}
out={'status':'RECEIVED_INDEPENDENT_CHECK_PASS','source_sha256':digest(src),**common,'scope':'Analytic receiving plus exact rational budgets and numerical arcsine diagnostics; no production SDP, hardware, or CPTP transfer.'}
(base/(src[:-3]+'_independent_check.json')).write_text(json.dumps(out,indent=2)+'\n')
out2={'status':'PASS_AUTHOR_LOG_IMPROVEMENT_AND_BASIC_SDP_GAP','source_sha256':digest(new),**common,'exact_gap_family_cases':64,'exhaustive_gap_cube_cases':len(gaps),'RLT_pairwise_violation':'M12=5/64 > p2=1/16','small_gap_values':gaps,'scope':'O(log) product-cube rounding; gap only for BASIC PSD moments; cap polynomial in numerical a and 1/m, not arbitrary coefficient bit length.'}
(base/(new[:-3]+'_check.json')).write_text(json.dumps(out2,indent=2)+'\n')
print(json.dumps(out,indent=2));print(json.dumps(out2,indent=2))
