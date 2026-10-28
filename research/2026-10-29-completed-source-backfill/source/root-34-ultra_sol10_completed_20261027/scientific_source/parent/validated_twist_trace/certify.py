"""Solver-independent trace certificate for a finite physical spin-two ring.

The eigensolver proposes dyadic V,Lambda. Arbitrary-precision integer
Gram/residual calculations supply every accuracy bound. No eigenpair
backward-error promise or floating point BLAS accuracy assumption is used.
The demonstrator uses four sites and the exact unit twist (3+4i)/5.
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import itertools, math, json, time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import scipy.linalg as la

ROOT=Path(__file__).resolve().parent
HQ=1<<40
VQ=1<<40
S=1<<96
SQ=1<<80
sqrt_lo=F(math.isqrt(6*SQ*SQ),SQ)
sqrt_hi=sqrt_lo+F(1,SQ)
assert sqrt_lo*sqrt_lo <= 6 <= sqrt_hi*sqrt_hi

def ceilq(x): return -((-x.numerator)//x.denominator)
def nearest(x): return (2*x.numerator+x.denominator)//(2*x.denominator)
def serial(x): return str(x.numerator)+'/'+str(x.denominator)

def exp_interval(x):
    """Outward fixed-point enclosure, returned as integers divided by S."""
    if x < 0:
        lo,hi=exp_interval(-x)
        return S*S//hi, (S*S+lo-1)//lo
    k=0
    while x > F(1,2): x/=2; k+=1
    term=F(1); total=F(1); degree=28
    for j in range(1,degree+1):
        term=term*x/j; total+=term
    next_term=term*x/(degree+1)
    tail=next_term/(1-x/F(degree+2))
    lo=(total*S).numerator//(total*S).denominator
    hi=ceilq((total+tail)*S)
    for _ in range(k):
        lo=lo*lo//S; hi=(hi*hi+S-1)//S
    assert 0 < lo <= hi
    return lo,hi

def sector(n,mag):
    states=[w for w in itertools.product(range(-2,3),repeat=n) if sum(w)==mag]
    lookup={w:i for i,w in enumerate(states)}; d=len(states)
    # Each entry has exact Gaussian rational form a+b*sqrt(6).
    ar=[[F(0) for _ in states] for _ in states]
    br=[[F(0) for _ in states] for _ in states]
    ai=[[F(0) for _ in states] for _ in states]
    bi=[[F(0) for _ in states] for _ in states]
    for col,w in enumerate(states):
        ar[col][col]=F(sum(w[j]*w[(j+1)%n] for j in range(n)))
        for j in range(n):
            jj=(j+1)%n
            for step in (-1,1):
                a,b=w[j],w[jj]
                if not(-2<=a+step<=2 and -2<=b-step<=2): continue
                v=list(w);v[j]+=step;v[jj]-=step; row=lookup[tuple(v)]
                rad=(6-a*(a+step))*(6-b*(b-step))//4
                if rad==6: integer,root=0,1
                else:
                    integer=math.isqrt(rad);root=0;assert integer**2==rad
                zr,zi=(F(3,5),F(4*step,5)) if j==n-1 else (F(1),F(0))
                ar[row][col]+=integer*zr; br[row][col]+=root*zr
                ai[row][col]+=integer*zi; bi[row][col]+=root*zi
    qr=np.zeros((d,d),dtype=np.int64); qi=np.zeros((d,d),dtype=np.int64)
    errs=[[F(0) for _ in states] for _ in states]
    for row in range(d):
        for col in range(d):
            for aa,bb,qq in ((ar,br,qr),(ai,bi,qi)):
                a,b=aa[row][col],bb[row][col]
                low,high=sorted((a+b*sqrt_lo,a+b*sqrt_hi))
                q=nearest((low+high)*HQ/2);qq[row,col]=q
                errs[row][col]+=max(abs(F(q,HQ)-low),abs(F(q,HQ)-high))
    assert np.array_equal(qr,qr.T) and np.array_equal(qi,-qi.T)
    eta=max(map(sum,errs))
    trace1=sum(ar[j][j] for j in range(d))
    assert all(br[j][j]==ai[j][j]==bi[j][j]==0 for j in range(d))
    trace2=sum(ar[i][j]**2+6*br[i][j]**2+ai[i][j]**2+6*bi[i][j]**2 for i in range(d) for j in range(d))
    trace2_root=sum(2*(ar[i][j]*br[i][j]+ai[i][j]*bi[i][j]) for i in range(d) for j in range(d))
    return qr,qi,eta,(trace1,trace2,trace2_root)

def integer_maxsum(a,axis):
    # Python integer accumulation even when a diagnostic bound exceeds int64.
    return max(sum(abs(int(v)) for v in row) for row in (a if axis==1 else a.T))

def certify_block(qr,qi,eta,beta):
    d=len(qr)
    vals,vecs=la.eigh((qr+1j*qi)/HQ,check_finite=False)
    vr=np.rint(vecs.real*VQ).astype(np.int64)
    vi=np.rint(vecs.imag*VQ).astype(np.int64)
    lam=np.rint(vals*HQ).astype(np.int64)
    assert np.max(np.abs(vr)) <= VQ and np.max(np.abs(vi)) <= VQ
    # Python-integer array products permit a finer proposal denominator
    # without overflow. The small physical demonstration charges this cost.
    qr=qr.astype(object);qi=qi.astype(object)
    vr=vr.astype(object);vi=vi.astype(object);lam=lam.astype(object)
    max_col_square=max(sum(int(x)**2+int(y)**2 for x,y in zip(vr[:,j],vi[:,j])) for j in range(d))
    gr=vr.T@vr+vi.T@vi-np.eye(d,dtype=object)*(VQ*VQ)
    gi=vr.T@vi-vi.T@vr
    # Record intermediate magnitude bounds although Python integers do not
    # overflow. The initial storage still fits int64 before promotion.
    row_bound=integer_maxsum(np.abs(qr)+np.abs(qi),1)
    vmax=max(int(np.max(abs(vr))),int(np.max(abs(vi))))
    residual_integer_bound=(row_bound+max(map(abs,map(int,lam))))*vmax
    rr=qr@vr-qi@vi-vr*lam[np.newaxis,:]
    ri=qr@vi+qi@vr-vi*lam[np.newaxis,:]
    gram_abs=np.abs(gr)+np.abs(gi)
    res_abs=np.abs(rr)+np.abs(ri)
    epsilon=F(integer_maxsum(gram_abs,1),VQ*VQ)
    residual=F(max(integer_maxsum(res_abs,1),integer_maxsum(res_abs,0)),HQ*VQ)
    hn=F(row_bound,HQ); ln=F(max(map(abs,map(int,lam))),HQ)
    assert epsilon <= F(1,2)
    delta=eta+residual+F(3,2)*epsilon*(hn+ln)
    slo=shi=0
    for l in lam:
        lo,hi=exp_interval(-beta*F(int(l),HQ));slo+=lo;shi+=hi
    elo,ehi=exp_interval(beta*delta)
    lower=F(slo,S)*F(S,ehi);upper=F(shi,S)*F(ehi,S)
    return {'dimension':d,'eta':serial(eta),'epsilon':serial(epsilon),
            'residual':serial(residual),'delta':serial(delta),
            'H0_norm_bound':serial(hn),'Lambda_norm_bound':serial(ln),
            'max_column_square_integer':str(max_col_square),
            'residual_integer_bound':str(residual_integer_bound),
            'integer_product_arithmetic':'arbitrary precision Python integers',
            'lower':serial(lower),'upper':serial(upper),
            'solver_accuracy_assumed':False},lower,upper

def main():
    start=time.monotonic();n=4;beta=F(3);rows=[];lo=hi=F(0)
    controls=[F(0),F(0),F(0)]
    for mag in range(-2*n,2*n+1):
        qr,qi,eta,moments=sector(n,mag)
        controls=[x+y for x,y in zip(controls,moments)]
        record,l,u=certify_block(qr,qi,eta,beta)
        record['magnetization']=mag;rows.append(record);lo+=l;hi+=u
    assert sum(r['dimension'] for r in rows)==5**n
    assert controls==[F(0),F(n*5**n*12),F(0)]
    result={'status':'RIGOROUS_TRACE_ENCLOSURE_FROM_EXACT_DYADIC_RESIDUALS',
            'physical_model':'periodic spin-two H=sum S_i dot S_(i+1), four sites, closing XY twist (3+4i)/5',
            'beta':serial(beta),'all_states':5**n,'sector_records':rows,
            'exact_full_state_controls':{'Tr_H':serial(controls[0]),'Tr_H_squared':serial(controls[1]),'sqrt6_coefficient_Tr_H_squared':serial(controls[2]),'independent_bond_formula':'n*5^n*s^2(s+1)^2/3 = 30000'},
            'trace_lower':serial(lo),'trace_upper':serial(hi),
            'relative_width_upper':serial((hi-lo)/lo),
            'display_only':{'lower':float(lo),'upper':float(hi),'relative_width':float((hi-lo)/lo),
                            'maximum_delta':max(float(F(r['delta'])) for r in rows)},
            'seconds':time.monotonic()-start,
            'scope':'Finite physical trace enclosure. No next connected thermal input or gap acquired; no novelty of residual/Weyl validation claimed.'}
    (ROOT/'TRACE_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','display_only','seconds')},indent=2))

if __name__=='__main__':main()
