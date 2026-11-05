"""Exact small-model oracle calculation, not experimental observations.

Tests the new signed-output mixed derivative using a triangular moment ODE,
finite Chebyshev interpolation, and an explicit conservative resource evaluator.
"""
import json, math
from pathlib import Path
import numpy as np
import mpmath as mp
from check_output_calibration import pm, PAULI, ptrace, product_on, source_liouvillian
mp.mp.dps=70
HERE=Path(__file__).resolve().parent

def reset_matrix(n,site,output):
    d=2**n; out=np.zeros((d*d,d*d),complex)
    rest=[j for j in range(n) if j!=site]
    for j in range(d*d):
        x=np.zeros((d,d),complex); x.reshape(-1)[j]=1
        out[:,j]=product_on(output,[site],ptrace(x,rest,n),rest,n).reshape(-1)
    return out

def coefficients(h,r,label,scale,order=48):
    n=len(label); d=len(h); dd=d*d
    supp=[i for i,p in enumerate(label) if p!='I']; b=len(supp); i=supp[0]
    qp=next(x for x in 'XYZ' if x!=label[i]); qlabel=['I']*n; qlabel[i]=qp; q=pm(qlabel)
    factors=[1j*PAULI[label[j]]@PAULI[qp] if j==i else PAULI[label[j]] for j in supp]
    l=source_liouvillian(h,r,n); e=[reset_matrix(n,j,PAULI['I']/2) for j in range(n)]
    weighted=[reset_matrix(n,j,factors[z]/2) for z,j in enumerate(supp)]
    blocks=2**b; g=np.zeros((blocks*dd,blocks*dd),complex)
    for mask in range(blocks):
        a=l.copy()
        for z,j in enumerate(supp):
            if mask&(1<<z):
                a-=r*e[j]; old=mask^(1<<z)
                g[mask*dd:(mask+1)*dd,old*dd:(old+1)*dd]+=r*weighted[z]
        g[mask*dd:(mask+1)*dd,mask*dd:(mask+1)*dd]+=a
    v=np.zeros(blocks*dd,complex); v[:dd]=(np.eye(d)/d).reshape(-1)
    front=[]; term=v.copy()
    for a in range(order+1):
        front.append(term[(blocks-1)*dd:].copy()); term=(scale*g@term)/(a+1)
    back=[np.zeros(dd,complex)]; term=r*scale*q.T.reshape(-1); killed=l-r*e[i]
    for a in range(1,order+1):
        back.append(term.copy()); term=term@(scale*killed)/(a+1)
    c=np.zeros((order+1,order+1),complex)
    for a in range(1,order+1):
        for u in range(1,a+1):
            term=front[a-u].copy()
            for z in range(order+1):
                c[a,z]+=back[u]@term; term=(scale*l@term)/(z+1)
    assert np.max(abs(c.imag))<1e-14
    expected=2*r**(b+1)*scale**(b+2)*np.trace(pm(label)@h).real/d
    assert abs(c[b+1,1].real-expected)<1e-13
    return c.real,b+1

def weights(D,s):
    xs=[(1+mp.cos(mp.pi*l/D))/2 for l in range(D+1)]; out=[]
    for l in range(D+1):
        total=mp.mpf(0)
        for j in range(s,D+1):
            v=mp.mpf((-1)**(j+s))*2**s
            for a in range(s): v*=mp.mpf(j*j-a*a)/(2*a+1)
            total+=(mp.mpf('.5') if j in (0,D) else 1)*v*mp.cos(mp.pi*j*l/D)
        out.append(mp.mpf(2)/D*(mp.mpf('.5') if l in (0,D) else 1)*total)
    return xs,out

def interpolate(c,s,r,h,D):
    xs,ww=weights(D,s); _,wt=weights(D,1)
    cm=[[mp.mpf(str(x)) for x in row] for row in c]; value=mp.mpf(0)
    for a,x in enumerate(xs):
        for b,y in enumerate(xs):
            f=mp.mpf(0)
            for row in reversed(cm):
                fy=mp.mpf(0)
                for v in reversed(row): fy=fy*y+v
                f=f*x+fy
            value+=ww[a]*wt[b]*f
    return float(value/(2*math.factorial(s)*mp.mpf(str(r))**s*mp.mpf(str(h))**(s+1)))

def schedule(n,M,k,B,r,margin,eps):
    L=mp.mpf(2)*B+2*n*r; T=mp.log(400*n/eps**2)/margin; eta=eps/(100*M*T); h=1/(8*L); rows=[]
    for b in range(1,k+1):
        s=b+1; D=max(s,2)
        while True:
            W=4*(D+1)**2*(2*D*D/h)**(s+1)
            if 8*W*mp.power(4,-D)<=eta*math.factorial(s)*r**s: break
            D+=1
        zeta=eta*math.factorial(s)*r**s/(2*W); pmax=(r*h)**s
        N=mp.ceil(8*(pmax/zeta**2+1/zeta)*mp.log(200*M*(D+1)**2/eps))
        rows.append(dict(support=b,degree=D,log10_full_trials_upper=float(mp.log10(M*D*(D+1)*N)),
                         log10_samples_per_node=float(mp.log10(N)),mean_accuracy=str(zeta)))
    return dict(n=n,M=M,k=k,B_H=B,r=r,margin=margin,epsilon=eps,capture_time=str(T),
                coefficient_accuracy=str(eta),max_window_time=str(h),rows=rows,
                interpretation='Explicit loose theorem schedule, not an executed or competitive device.')

def main():
    theta={'XI':.37,'IY':-.23,'ZZ':.41,'XY':.19,'ZX':-.17}; H=sum(v*pm(p) for p,v in theta.items()); r=4.; h=.08; checks=[]
    for label in ['XI','IY','ZZ','XY','ZX','XX']:
        c,s=coefficients(H,r,label,h); rows=[]
        for D in [3,4,5,6,8,10]:
            if D<s: continue
            v=interpolate(c,s,r,h,D); rows.append(dict(degree=D,estimate=v,absolute_error=abs(v-theta.get(label,0.))))
        assert rows[-1]['absolute_error']<2e-7
        checks.append(dict(label=label,theta=theta.get(label,0.),mixed_derivative_order=[s,1],estimates=rows))
    result=dict(scope='Deterministic floating-point ideal-instrument calculation. Grid means are computed, not physically acquired. No theorem-scale sampling executed.',
                Taylor_truncation_order=48,
                diagnostic_window_scale=h,coefficient_checks=checks,
                conservative_theorem_schedule=schedule(2,15,2,sum(abs(x) for x in theta.values()),4.,2.46,.1))
    lam=mp.mpf(str(2*sum(abs(x) for x in theta.values())+4*r))
    mh=mp.mpf(str(h)); ds=10; ss=3; rr=mp.mpf(str(r)); order=48
    tail=2*mp.exp(3*lam*mh)*(2*lam*mh)**(order+1)/mp.factorial(order+1)
    norm=4*(ds+1)**2*(2*ds*ds/mh)**(ss+1)/(2*math.factorial(ss)*rr**ss)
    result['analytic_Taylor_tail_effect_upper_for_degree10']=str(norm*tail)
    result['tail_bound_scope']='Analytic truncation only; does not certify floating-point roundoff. The overall diagnostic is numerical.'
    (HERE/'finite_derivative_diagnostic.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
