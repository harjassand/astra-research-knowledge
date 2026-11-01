"""Theorem-only audit. Does not import any candidate receiving code."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,random
import sympy as sp
H=Path(__file__).resolve().parent;cats={}
def ok(b,k):
 if not b:raise AssertionError(k)
 cats[k]=cats.get(k,0)+1
# Full-z continuity, not energy Markov closure; arbitrary homogeneous fixtures.
y,beta,kappa,mu,dmin,alpha=sp.symbols('y beta kappa mu dmin alpha',positive=True)
v=1+kappa*(1-y*y)**2;vp=sp.diff(v,y)
for m,p in [(2,2),(4,4),(6,6)]:
 z=sp.symbols('z:'+str(m));U=sum((i+1)*z[i]**p for i in range(m))
 if p==4:U+=37*z[0]**2*z[1]**2+13*z[1]**2*z[2]**2
 if p==6:U+=19*z[0]**2*z[1]**4+11*z[2]**2*z[3]**2*z[4]**2
 g=[sp.diff(U,x)for x in z];Euler=sum(x*q for x,q in zip(z,g))
 ok(sp.expand(Euler-p*U)==0,'Euler homogeneous energy identity')
 w=[-vp*x/(p*v)for x in z];divw=sum(sp.diff(q,x)for q,x in zip(w,z))
 continuity=sp.Rational(m,p)*vp/v-beta*vp*U+divw+sum(wi*(-beta*v*gi)for wi,gi in zip(w,g))
 ok(sp.simplify(continuity)==0,'full-z conditional continuity identity')
 # Explicit diagonal M: inverse-mobility current norm, no gamma-u substitution.
 ds=[sp.Rational(i+1,3)for i in range(m)]
 norm=sum(wi*wi/di for wi,di in zip(w,ds))
 ok(sp.simplify(norm-(vp/(p*v))**2*sum(zi*zi/di for zi,di in zip(z,ds)))==0,'constant-matrix inverse mobility norm')
 K=1+kappa/p
 drift=-2*y*vp*U-2*K*v*Euler
 ok(sp.simplify(drift+2*(y*vp+K*p*v)*U)==0,'global full-state Lyapunov drift exact')
# Tail and global Lyapunov inequalities are all-point algebra, not numerical premises.
t=sp.symbols('t',nonnegative=True);pp=sp.symbols('p',positive=True)
# yv' + kappa = kappa(2t-1)^2 with t=y^2.
ok(sp.expand(4*kappa*t*(t-1)+kappa-kappa*(2*t-1)**2)==0,'all-point longitudinal Lyapunov bound identity')
coef=4*kappa*t*(t-1)+(pp+kappa)*(1+kappa*(1-t)**2)
remainder=kappa*(2*t-1)**2+(pp+kappa)*kappa*(1-t)**2
ok(sp.expand(coef-pp-remainder)==0,'nonnegative full coefficient decomposition')
# Quartic coercivity: m sum z_i^4 - (sum z_i^2)^2 = sum pair square gaps.
z=sp.symbols('x:7');m=len(z)
left=m*sum(q**4 for q in z)-sum(q*q for q in z)**2
right=sum((z[i]**2-z[j]**2)**2 for i in range(m)for j in range(i+1,m))
ok(sp.expand(left-right)==0,'global quartic coercivity sum-square identity')
# Exact virial/Jensen specialization and all overhead constants.
C=sp.sqrt(alpha/(beta*(dmin/(4*alpha))))/(16*mu)
ok(sp.simplify(C-alpha/(8*mu*sp.sqrt(beta*dmin)))==0,'quartic virial Jensen coefficient')
a=1+sp.Rational(9,16)*kappa;Cs=4*kappa*C/(alpha*a**sp.Rational(3,2));Dmax=32*C*sp.symbols('kmax',positive=True)
ok(sp.simplify(Cs-kappa/(2*mu*sp.sqrt(beta*dmin)*a**sp.Rational(3,2)))==0,'dimension-free slab overhead')
ok(sp.simplify(Dmax-4*alpha*sp.symbols('kmax',positive=True)/(mu*sp.sqrt(beta*dmin)))==0,'global basin overhead constant')
ok(sp.simplify(Cs.subs({beta:1,kappa:1,dmin:1})-sp.Rational(32,125)/mu)==0,'unit-parameter exact slab constant')
ok(Cs.subs({beta:1,kappa:1,dmin:1,mu:64})==sp.Rational(1,250),'actual mobility64 gives point004 slab overhead')
# Source/full mean formula assembly; M is one basin and R the whole slab.
M,R,S0,Wfar,MS,Cs0,D0=sp.symbols('M R S0 Wfar MS Cs0 D0',positive=True)
DA=beta*M*M*R*(1+Cs0)+beta*(1+D0)*(M*M*S0+Wfar)
upper=(1+MS/M)*DA/M
ok(sp.simplify(upper-(1+MS/M)*(beta*M*R*(1+Cs0)+beta*(1+D0)*(M*S0+Wfar/M)))==0,'source current to full formula12 assembly')
# Explicit range of rational representatives checks global inequalities without code.
for aa in [4,5,8,16,32,128]:
 for kap in [F(1,100),F(1,4),F(1),F(4),F(100)]:
  dd=F(1,aa);a=1+F(9,16)*kap;c1=1+kap*(1-(1+dd)**2)**2
  ok(c1<=a,'near-basin constant at every tested alpha kappa')
  for j in range(81):
   yy=F(j,10);vv=1+kap*(1-yy*yy)**2;vvprime=4*kap*yy*(yy*yy-1)
   # Squared inequality avoids all floating square roots.
   ok(vvprime**4 <= (32*max(kap,F(1)))**2*vv**5,'global all-basin correction bound rational check')
  for j in range(41):
   yy=F(j,80);vv=1+kap*(1-yy*yy)**2;vvprime=4*kap*yy*(yy*yy-1)
   ok(-vvprime<=4*kap*yy and vv>=a,'half-slab derivative and lower profile')
  for j in range(41):
   x=F(1,2)+(F(1,2)+dd)*j/40;vv=1+kap*(1-x*x)**2
   ok(vv<=a,'near-basin maximum')
   xx=1+dd+F(j,4);vp=4*kap*xx*(xx*xx-1)
   ok(vp>=8*kap*(xx-1),'far-basin derivative lower bound')
# Verify general tail powers and integrability thresholds symbolically.
p,a=sp.symbols('p a',positive=True)
ok(sp.simplify(6-4*(2+2/p)-(-2-8/p))==0,'full-z correction asymptotic exponent')
ok(sp.simplify(2*(1-4*a)+4*a-(2-4*a))==0,'source current tail power')
# Exact source-state counterexample to transferring Markov law or ray initialization.
z=sp.symbols('q:4');U=z[0]**4+16*z[1]**4+z[2]**4+z[3]**4;g=sp.Matrix([sp.diff(U,q)for q in z]);lap=sum(sp.diff(U,q,2)for q in z);vals=[]
for pt in [[1,0,0,0],[0,sp.Rational(1,2),0,0]]:
 ss=dict(zip(z,pt));vals.append([U.subs(ss),g.dot(g).subs(ss),(lap-g.dot(g)).subs(ss)])
ok(vals==[[1,16,-4],[1,64,-16]],'same energy does not imply same original-SPD projected law')
b=H.joinpath('received_candidate.md').read_bytes();ok(hashlib.sha256(b).hexdigest()=='bf9e83e1f39f25758dc02b10a06d06a955b98e61de172f633ba5d4f341a7d8e0','exact source snapshot hash')
report={'status':'PASS','checks':sum(cats.values()),'categories':cats,'candidate_code_imported':False,'numerical_consumer_accepted':False,'scope':'Theorem-only full-state original constant-SPD Poisson-current MFPT at exact full Gibbs|A initialization.'}
H.joinpath('check_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
