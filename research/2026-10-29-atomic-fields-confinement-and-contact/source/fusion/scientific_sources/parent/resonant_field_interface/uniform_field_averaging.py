"""Exact Fourier corrector/rational bounds for a uniform-y vacuum perturbation."""
import sympy as s
from fractions import Fraction as F
from pathlib import Path
import json,time
from source_geometry import geometry
start=time.monotonic();z,a,b,X=geometry()
def phi(v):return s.diff(v,z)*s.I*z
def lam(v):return s.diff(v,a)/(2*a)
Xp=X.applyfunc(phi);Xl=X.applyfunc(lam);Xb=X.diff(b)
A=s.Matrix([X[2]/2,0,-X[0]/2])
Ap=A.dot(Xp);Al=A.dot(Xl);Ab=A.dot(Xb)
gl=s.cancel(2*a*a*(s.diff(Ap,b)-phi(Ab)))
gb=s.cancel(2*a*a*(phi(Al)-lam(Ap)))
gp=s.cancel(Xp[1])
assert s.cancel(gl-2*a*a*(Xb.cross(Xp))[1])==0
assert s.cancel(gb-2*a*a*(Xp.cross(Xl))[1])==0
def fourier(v):
    p=s.Poly(s.cancel(v*z**40),z,domain='EX')
    return {k[0]-40:s.cancel(c)for k,c in p.terms()if c!=0}
fb=fourier(gb);fl=fourier(gl);fp=fourier(gp)
G=-8*a**6*(9-a*a+a**4-a**6)/(1+a*a)**7
assert s.cancel(fb.get(0,0)-G)==0
assert fl.get(0,0)==0
chi={k:s.cancel(-c/(s.I*k))for k,c in fb.items()if k}
assert all(s.cancel(s.I*k*c+fb[k])==0 for k,c in chi.items())
assert all(s.cancel(chi[-k]-s.conjugate(c))==0 for k,c in chi.items())
print('Exact mean drift and periodic corrector PASS.',flush=True)
# Larger box encloses the source-certified ellipse; geometric validity is
# assumed only on that ellipse. Arithmetic bounds hold on the larger box.
box={a:(F(1,3),F(1,2)),b:(-F(2,25),F(3,25))}
def plus(x,y):return x[0]+y[0],x[1]+y[1]
def times(x,y):
    v=[p*q for p in x for q in y];return min(v),max(v)
def interval(e):
    if e in box:return box[e]
    if e.is_Rational:
        q=F(int(e.p),int(e.q));return q,q
    if e.is_Add:
        v=(F(0),F(0))
        for q in e.args:v=plus(v,interval(q))
        return v
    if e.is_Mul:
        v=(F(1),F(1))
        for q in e.args:v=times(v,interval(q))
        return v
    if e.is_Pow and e.exp.is_Integer:
        x=interval(e.base);n=int(e.exp)
        if n<0:
            assert not x[0]<=0<=x[1],e
            x=(1/x[1],1/x[0]);n=-n
        v=(F(1),F(1))
        for _ in range(n):v=times(v,x)
        return v
    raise ValueError(e)
def bound(c):
    re,im=s.expand_complex(c).as_real_imag();result=F(0)
    for p in (re,im):
        lo,hi=interval(s.factor(s.cancel(p)));result+=max(abs(lo),abs(hi))
    return result
def norm(d):return sum((bound(c)for c in d.values()),F(0))
C={'gl':norm(fl),'gb':norm(fb),'gp':norm(fp),'chi':norm(chi),
   'chi_lambda':norm({k:lam(c)for k,c in chi.items()}),
   'chi_beta':norm({k:s.diff(c,b)for k,c in chi.items()})}
m=F(8)*F(1,3)**6*(F(9)-F(1,4)-F(1,64))/(1+F(1,4))**7
M=C['chi_lambda']*C['gl']+C['chi_beta']*C['gb']+C['gb']*C['gp']
maximum=min(1/(2*C['gp']),m/(4*M));assert maximum>0
out={'status':'EXACT_FOURIER_IDENTITIES_AND_RATIONAL_BOUND_PASS',
     'source':'Lopez2610.29921v1; source-certified embedding assumed',
     'mean_beta_drift':str(G),'box':'a in[1/3,1/2]; beta in[-2/25,3/25]',
     'bounds':{k:str(v)for k,v in C.items()},'negative_mean_magnitude_lower':str(m),
     'second_order_numerator_bound':str(M),'positive_delta_max':str(maximum),
     'positive_delta_max_decimal':float(maximum),
     'corrector_fourier':{str(k):str(v)for k,v in chi.items()},
     'seconds':time.monotonic()-start}
Path(__file__).with_name('AVERAGING_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k not in ['corrector_fourier','bounds']},indent=2),flush=True)
