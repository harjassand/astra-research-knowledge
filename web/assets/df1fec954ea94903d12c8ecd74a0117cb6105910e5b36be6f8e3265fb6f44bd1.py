"""Rational-interval HS-positivity certificate for a d=5 full-support Q.

The exact star polynomial is checked by d5_nonuniform_weight_exact.py. It
puts the simple largest root alpha in (15,16), with every other block
eigenvalue below 10. This file certifies that a rational charge-zero vector
is close enough to its top eigenvector to prove all transfer coefficients of
the twirled, swap/parity-averaged marginal positive. No all-Q claim is made.
"""
from fractions import Fraction as F
from math import isqrt

D=5
reps=[]
for slope in range(D): reps.extend([(1,slope),(2,(2*slope)%D)])
reps.extend([(0,1),(0,2)])
weights=[F(1,2)]*12
weights[0]=F(1)
# Rationalized top eigenvector in the charge-zero block, rounded to 1e-9.
qdata=[
 (570188695,0),(18773321,0),(638412,0),(638412,0),(18773321,0),
 (294481008,0),(294481008,0),(9705866,0),(638412,0),(9705866,0),
 (285413553,0),(18773321,0),(285413553,0),(9705866,0),(9705866,0),
 (285413553,0),(9705866,0),(9705866,0),(285413553,0),(18773321,0),
 (294481008,0),(9705866,0),(638412,0),(9705866,0),(294481008,0)]

SCALE=10**50
class I:
    def __init__(self,lo,hi=None): self.lo=F(lo); self.hi=F(lo if hi is None else hi)
    def __add__(self,o): o=ii(o); return I(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self): return I(-self.hi,-self.lo)
    def __sub__(self,o): return self+(-ii(o))
    def __rsub__(self,o): return ii(o)-self
    def __mul__(self,o):
        o=ii(o); z=(self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi)
        return I(min(z),max(z))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=ii(o); assert o.lo>0 or o.hi<0
        return self*I(1/o.hi,1/o.lo)
    def upper_abs(self): return max(abs(self.lo),abs(self.hi))
    def square(self):
        hi=max(self.lo*self.lo,self.hi*self.hi)
        lo=F(0) if self.lo<=0<=self.hi else min(self.lo*self.lo,self.hi*self.hi)
        return I(lo,hi)
def ii(x): return x if isinstance(x,I) else I(x)
def sqrtq(q):
    q=F(q); assert q>=0
    n,d=q.numerator,q.denominator
    k=isqrt((n*SCALE*SCALE)//d); lo=F(k,SCALE)
    hi=F(k+int(k*k*d<n*SCALE*SCALE),SCALE)
    assert lo*lo<=q<=hi*hi
    return I(lo,hi)
def sqrti(x):
    assert x.lo>=0
    lo=sqrtq(x.lo).lo; hi=sqrtq(x.hi).hi
    return I(lo,hi)
class C:
    def __init__(self,re=0,im=0): self.re=ii(re); self.im=ii(im)
    def __add__(self,o):
        o=cc(o); return C(self.re+o.re,self.im+o.im)
    __radd__=__add__
    def __neg__(self): return C(-self.re,-self.im)
    def __sub__(self,o): return self+(-cc(o))
    def __mul__(self,o):
        o=cc(o); return C(self.re*o.re-self.im*o.im,self.re*o.im+self.im*o.re)
    __rmul__=__mul__
    def conj(self): return C(self.re,-self.im)
def cc(x): return x if isinstance(x,C) else C(x,0)
ZERO=C(0); ONE=C(1)

rt5=sqrti(I(5))
c1=(rt5-I(1))/4; c2=-(rt5+I(1))/4
s1=sqrti((I(10)+2*rt5)/16); s2=sqrti((I(10)-2*rt5)/16)
cos=[I(1),c1,c2,c2,c1]
sin=[I(0),s1,s2,-s2,-s1]
zeta=[C(cos[k],sin[k]) for k in range(D)]
def matmul(A,B):
    n,m,p=len(A),len(B),len(B[0]); out=[[ZERO for _ in range(p)] for _ in range(n)]
    for i in range(n):
        for k in range(m):
            if A[i][k].re.lo==A[i][k].re.hi==0 and A[i][k].im.lo==A[i][k].im.hi==0: continue
            for j in range(p): out[i][j]=out[i][j]+A[i][k]*B[k][j]
    return out
def matpow(A,n):
    out=[[ONE if i==j else ZERO for j in range(D)] for i in range(D)]
    for _ in range(n): out=matmul(out,A)
    return out
X=[[ONE if i==(j+1)%D else ZERO for j in range(D)] for i in range(D)]
Z=[[zeta[j] if i==j else ZERO for j in range(D)] for i in range(D)]
def W(a,b):
    t=(3*a*b)%D
    phase=[[zeta[t] if i==j else ZERO for j in range(D)] for i in range(D)]
    return matmul(matmul(phase,matpow(X,a)),matpow(Z,b))
def adj(A): return [[A[j][i].conj() for j in range(len(A))] for i in range(len(A))]

basis=[(r,a,(r-a)%D) for r in range(D) for a in range(D)]
assert len(basis)==25 and all((a+b-r)%D==0 for r,a,b in basis)
q=[C(F(a,10**9),F(b,10**9)) for a,b in qdata]
N=sum((x.re*x.re+x.im*x.im for x in q),I(0))
# Exact charge-zero compression of the four star terms for each selected mode.
H=[[ZERO for _ in basis] for _ in basis]
for weight,(a,b) in zip(weights,reps):
    U=W(a,b); Ud=adj(U)
    for oi,(ro,ao,bo) in enumerate(basis):
        for ji,(ri,ai,bi) in enumerate(basis):
            v=ZERO
            if bo==bi: v=v+U[ri][ro]*Ud[ao][ai]+Ud[ri][ro]*U[ao][ai]
            if ao==ai: v=v+U[ri][ro]*Ud[bo][bi]+Ud[ri][ro]*U[bo][bi]
            H[oi][ji]=H[oi][ji]+weight*v
Hq=[sum((H[i][j]*q[j] for j in range(25)),ZERO) for i in range(25)]
mu_raw=sum((q[i].conj()*Hq[i] for i in range(25)),ZERO).re
nu_raw=sum((v.re*v.re+v.im*v.im for v in Hq),I(0))
assert mu_raw.lo>0

# Exact rational bracket for the unique top cubic root alpha of the block factor.
alo=F(1520314675649,10**11) # 15.20314675649
ahi=F(1520314675650,10**11) # 15.20314675650

def cubic_interval(x):
    return x*x*x-I(F(31,2))*x*x+I(F(17,4))*x+4
assert cubic_interval(I(alo)).hi<0
assert cubic_interval(I(ahi)).lo>0
# Bound ||(H-alpha I)q/sqrt(N)||^2 using monotonicity in alpha (alpha>Rayleigh quotient).
res2=(nu_raw-2*alo*mu_raw+I(ahi*ahi)*N)/N
assert res2.hi>=0
res=sqrti(I(0,res2.hi)).hi
gap=alo-10
err=2*res/gap
assert err<F(1,10**3), (float(res),float(err))

# For the twirled state, Weyl-invariant Choi transfer coefficient at g is the
# average of the reference/output-A and reference/output-B correlations.
# Parity averaging takes the real part; each observable has operator norm 1.
lam_lows=[]
lam_intervals=[]
for a in range(D):
  for b in range(D):
    if (a,b)==(0,0): continue
    U=W(a,b); Ud=adj(U)
    era=ZERO; erb=ZERO
    for oi,(ro,ao,bo) in enumerate(basis):
      for ji,(ri,ai,bi) in enumerate(basis):
        if bo==bi: era=era+q[oi].conj()*U[ri][ro]*Ud[ao][ai]*q[ji]
        if ao==ai: erb=erb+q[oi].conj()*U[ri][ro]*Ud[bo][bi]*q[ji]
    approx=((era.re+erb.re)/2)/N
    exact_lower=approx.lo-err
    lam_lows.append(exact_lower)
    lam_intervals.append(approx)
assert min(lam_lows)>0
print('||q||^2 interval',float(N.lo),float(N.hi))
print('Rayleigh quotient interval',float((mu_raw/N).lo),float((mu_raw/N).hi))
print('residual upper',float(res),'spectral gap lower',float(gap),'trace-distance channel-moment error',float(err))
print('minimum rational lower bound on all 24 transfer coefficients',float(min(lam_lows)))
print('approximate transfer range',float(min(v.lo for v in lam_intervals)),float(max(v.hi for v in lam_intervals)))
print('twirled marginal is HS-positive for this selected d=5 Q: CERTIFIED')
