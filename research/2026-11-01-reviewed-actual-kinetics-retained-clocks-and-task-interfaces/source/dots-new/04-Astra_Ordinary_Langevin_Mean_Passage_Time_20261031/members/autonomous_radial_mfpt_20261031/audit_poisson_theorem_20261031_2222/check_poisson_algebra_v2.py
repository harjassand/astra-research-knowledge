#!/usr/bin/env python3
"""Independent theorem checks, no candidate implementation imports."""
import sympy as S
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
checks=[]
def eq(n,a,b=0):
 r=S.cancel(a-b);assert r==0,(n,r);checks.append(n)
def truth(n,a):
 assert a,n;checks.append(n)
y,u,k,beta,gamma,alpha=S.symbols('y u k beta gamma alpha',positive=True)
v=1+k*(1-y*y)**2;vp=S.diff(v,y)
q=v**(-alpha);pi=(beta*v)**alpha*u**(alpha-1)*S.exp(-beta*v*u)/S.gamma(alpha)
w=-vp*u/v
# Work with exact log derivatives to avoid unneeded noninteger-power expansion.
eq('Gamma transport identity',alpha*vp/v-beta*vp*u+S.diff(w,u)+w*((alpha-1)/u-beta*v),0)
eq('dual transverse expectation',vp**2/(gamma*v**2)*(alpha/(beta*v)),alpha*vp**2/(beta*gamma*v**3))
eq('gain Lyapunov bracket',2*y*vp+(gamma+2*k)*v-gamma,2*(y*vp+k)+(gamma+2*k)*(v-1))
eq('yvprime lower certificate',y*vp+k,k*(2*y*y-1)**2)
W=v**alpha
# Algebra before cancellation avoids powers with symbolic alpha.
V=S.symbols('V',positive=True);Dv=S.symbols('Dv',real=True)
eq('slab transport factor',S.powsimp(alpha*Dv**2*V**(alpha-3)/(beta*gamma) / ((-Dv/(beta*gamma*V**2))*(-alpha*V**(alpha-1)*Dv)),force=False),1)
# Correct source and current constants in closed scalar certificate.
M,R,a,S0,S1,Wfar,Ms=S.symbols('M R a S0 S1 Wfar Ms',positive=True)
slab=beta*M*M*R*(1+4*k/(beta*gamma*a*a))
near=beta*M*M*S0+alpha/gamma*M*M*S1
far=beta*Wfar+alpha/gamma*M/(alpha-1)**2
formula=(1+a**(-alpha)/M)*(beta*M*R*(1+4*k/(beta*gamma*a*a))+beta*M*S0+beta*Wfar/M+alpha/gamma*M*S1+alpha/(gamma*(alpha-1)**2))
eq('formula nine assembly',(1+a**(-alpha)/M)*(slab+near+far)/M,formula)
eq('far source second-power exponent',2*(1-alpha)+alpha-3,-alpha-1)
eq('far source first-power exponent',2*(1-alpha)+alpha,2-alpha)
eq('tail current asymptotic exponent',2*(1-4*alpha)+4*alpha,2-4*alpha)
eq('trial boundary-pairing exponent',2+1-4*alpha,3-4*alpha)
eq('trial square integrability exponent',4-4*alpha,4-4*alpha)
eq('gamma512 slab overhead',(4*k/(beta*gamma*(1+S.Rational(9,16)*k)**2)).subs({k:1,beta:1,gamma:512}),S.Rational(2,625))
eq('gaingeneral slab overhead',(4*k/(beta*gamma*(1+S.Rational(9,16)*k)**2)).subs({k:1,beta:1}),1024/(625*gamma))
truth('near endpoint square bound',Q(81,256)<Q(9,16))
truth('near derivative bound',Q(45,16)<4)
# Entire monotonicity inequalities are proved in receipt; exact rational points supplement.
for aa in range(4,25):
 d=Q(1,aa)
 for kap in [Q(1,10),Q(1),Q(10)]:
  vv=lambda x:1+kap*(1-x*x)**2
  dd=lambda x:4*kap*x*(x*x-1)
  av=vv(Q(1,2));cv=vv(1+d)
  truth('c<=a '+str((aa,kap)),cv<=av)
  for j in range(33):
   x=Q(1,2)+(Q(1,2)+d)*Q(j,32)
   truth('near v bound '+str((aa,kap,j)),vv(x)<=av)
   truth('near derivative bound '+str((aa,kap,j)),abs(dd(x))<=4*kap)
  for x in [1+d,Q(3,2),Q(2),Q(10)]:
   truth('far derivative lower '+str((aa,kap,x)),dd(x)>=8*kap*(x-1))
   truth('far convexity '+str((aa,kap,x)),kap*(12*x*x-4)>0)
# The assembled upper is >= discarded-tail lower for positive inputs.
for aa in [4,8,16]:
 vals={alpha:aa,k:Q(1),beta:Q(1),gamma:Q(512),M:Q(1,3),R:Q(10),a:Q(25,16),S0:Q(1,2),S1:Q(2),Wfar:Q(1,64)}
 truth('positive upper extras alpha'+str(aa),formula.subs(vals)> (beta*M*R).subs(vals))
row=json.loads((HERE/'input_hash.json').read_text());data=(HERE/'received_initial_candidate.md').read_bytes()
truth('received source binding',hashlib.sha256(data).hexdigest()==row['sha256'] and len(data)==row['bytes'])
report={'status':'PASS','exact_assertions':len(checks),'scope':'theorem algebra and representative rational inequalities only; no candidate code or numerical MFPT certificate accepted','checks':checks}
(HERE/'check_results_v2.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
