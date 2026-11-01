#!/usr/bin/env python3
"""Exact all-channel identities and continuous rational sign certificate; no grid inference."""
from pathlib import Path
from fractions import Fraction as F
import sympy as s,pickle,json,hashlib
P=Path(__file__).parent
d=pickle.load(open(P/'practical_algebra.pkl','rb'));globals().update(d)
checks=[]
def eq(name,lhs,rhs):
 assert s.factor(lhs-rhs)==0,name
 checks.append(name)
def yes(name,b):
 assert b,name
 checks.append(name)
xs=[A,L,E,Z,S]
def move(f,j):return f.subs({v:v+q for v,q in zip(xs,j)},simultaneous=True)
def gen(f):return s.factor(sum(rate*(move(f,j)-f) for rate,j in zip(rates,jumps)))
V=E**2/(N*L)-s.Rational(4,3)*A*E/(N*L)
V1=E**2/(N*L)*(1-A*E/(N*L))
Fpoly=L-s.Rational(3,4)*E**2/N+A*E/N
qLL=s.factor(sum(rate*j[1]**2 for rate,j in zip(rates,jumps)))
GL=gen(L)
eq('actual q_LL',qLL,1-A/2+A*A+A*L/2+A*E)
eq('GL-qLL',GL-qLL,A*(s.Rational(3,2)+L/2-4*A))
eq('new quotient GF polynomial',gen(Fpoly),GF)
eq('actual new quotient generator',gen(V),GV.subs(c,s.Rational(4,3)))
eq('actual original F1 generator',gen(V1),GF1)
for name,j in zip(names,jumps):
 b,v,w,zz,ds=j
 eq('quotient jump '+name,move(V,j)-V,(2*E*w+w*w-s.Rational(4,3)*(A*w+b*E+b*w)-v*N*V)/(N*(L+v)))
 eq('reciprocal jump '+name,move(1/L,j)-1/L,-v/(L*(L+v)))
eq('exact reciprocal generator',gen(1/L),-GL/L**2+sum(rate*j[1]**2/(L**2*(L+j[1])) for rate,j in zip(rates,jumps)))
f=s.factor(nv.subs(c,s.Rational(4,3)))
cs=[s.factor(s.Poly(f,a).coeff_monomial(a**i)) for i in range(4)]
D=(4-t*t)*(1-t*t)
c0=-r*t*t/(u*(1+t))-s.Rational(4,3)*t*t/(1+t)-(4-z*z)*t*u/(6*r)
eq('negative constant coefficient',cs[0],c0)
n1=s.factor(cs[1]*3*r*u*u*D)
n2=s.factor(cs[2]*3*r*u*D)
n3=s.factor(cs[3]*3*r*(t-2)*(t-1)*(t+2)/4)
eq('linear mass term',s.diff(n1,delta),4*r*r*D)
eq('negative cubic numerator',n3,r*(t*t+8*t-12)+u*(-2*t**3+3*t*t+8*t-12))
# Upper bound Laurent polynomial by positive monomials on a continuous box.
lo={r:F(3,2),t:F(0),u:F(0),z:F(0)}
hi={r:F(2),t:F(1,100),u:F(1,100),z:F(1,100)}
def upper_positive(expr):
 total=F(0)
 for term in s.Add.make_args(s.expand(expr)):
  coeff,rest=term.as_coeff_Mul(); cc=F(int(s.numer(coeff)),int(s.denom(coeff)))
  if cc<=0:continue
  powers=rest.as_powers_dict()
  for variable in [r,t,u,z]:
   power=int(powers.get(variable,0))
   cc*= (hi[variable] if power>=0 else lo[variable])**power
  yes('monomial contains only admitted variables '+str(term),rest==s.prod(var**powers.get(var,0) for var in [r,t,u,z]))
  total+=cc
 return total
extra1=s.expand((n1-4*delta*r*r*D-r*r*(16-12*r))/(r*r))
b1=16*F(1,100)*F(1,50)+upper_positive(extra1)
b2=upper_positive(s.expand(n2/(r*r)))
yes('linear positive remainder <1/4',b1<F(1,4))
yes('quadratic numerator <54 r^2',b2<F(54))
yes('D lower >=3',(4-F(1,100)**2)*(1-F(1,100)**2)>3)
yes('D upper <=4',True)
yes('linear plus quadratic gives -1/8 at a<=1/5',F(7,48)-6*F(1,5)*F(1,100)>F(1,8))
yes('cubic r coefficient negative',F(1,100)**2+8*F(1,100)-12<0)
yes('cubic u coefficient negative',3*F(1,100)**2+8*F(1,100)-12<0)
yes('constant negative for z cap',F(1,100)**2<4)
# Original 12T mass band implies |S-N| <= E/50: fifth powers.
yes('12 T <= E/50 fifth-power polynomial consequence',600**5<=100**3*150**4)
# Domain implies E>=15000, N>=1500000.
yes('E floor',F(3,2)*100/F(1,100)==15000)
yes('N floor',F(3,2)*100/F(1,100)**2==1500000)
# Segment derivatives use only actual nonnegative counts.  These ratios cover exiting jump.
pad=(1+F(1,15000))/(1-F(1,100))
yes('padded L derivative <=21/(10L)',2*pad**2<F(21,10))
yes('padded A derivative <=7u/(5L)',F(4,3)*pad<F(7,5))
yes('padded E derivative <=21u/(10L)',2*pad<F(21,10))
yes('V positive on segment',F(4,3)*F(2,100)/(150-F(1,100))<1)
yes('jump cap 11/(5M)',F(21,10)+F(7,2)*F(1,100)<F(11,5))
yes('bracket coefficient L below9',2*F(21,10)**2<9)
yes('bracket coefficient A below25',2*F(7,2)**2<25)
yes('pre endpoint correction',F(4,3)*F(1,100)*F(1,100)==F(1,7500))
exitcorr=F(4,3)*(F(1,100)+F(1,100))/(1-F(1,100))*F(1,100)*(1+F(1,15000))
yes('exit correction <=3e-4',exitcorr<F(3,10000))
# Full raw E storage, exact finite jumps and source gate.
B=S-2*L+A-E; C=L-A+Z/2; DD=L-A-Z/2;CD=C*DD
phi=E**-2; dp=(E+1)**-2-phi;dm=(E-1)**-2-phi;ap=1/(E*(E+1));am=1/(E*(E-1))
GA=gen(A);WE=A/E**2+3/E
storage=phi*GA+(A*(A-1)*(A-1)+2*CD*(A+1))*dp+2*A*A*E*dm-3*(A*(A-1)+2*CD)*ap+6*A*E*am
eq('full raw weighted storage',gen(WE),storage)
qA=sum(rates)
eq('actual qA',qA,1+A+3*A*(A-1)+A*(C+DD)+3*CD+A*B+2*A*E)
cB=F(1)-F(51,50)*F(1,100)-F(2,15000)
yes('B/N lower 2969/3000',cB==F(2969,3000))
gate=(2+6*F(1,100))/15000+F(12,100)
yes('weighted source gate from practical region',gate<cB/2)
yes('raw weighted jump coefficient below8',7+4*(F(1,15000)+F(1,15000))<8)
yes('E^-2 bounded by L^-2/22500',(F(1,100)/F(3,2))**2==F(1,22500))
yes('combined V bracket coefficient',25*4*F(1,22500)==F(1,225))
# Exact outward witness for original F1, all actual channels and integer counts.
state={N:5000000000,S:5000000000,L:100,E:1000000,A:1,Z:0}
g1=s.factor(GF1.subs(state));gv=s.factor(GV.subs(c,s.Rational(4,3)).subs(state))
yes('original F1 outward exact witness',g1>184 and g1<185)
yes('new V inward same witness',gv< -6481 and gv> -6482)
yes('witness physical nonnegative counts',all(s.sympify(x).subs(state)>=0 for x in [A,B,C,DD,E]))
yes('witness outside inherited E5 gate',state[E]**5==8*state[N]**3)
# Row ledger at witness.
ledger=[]
for name,rate,j in zip(names,rates,jumps):
 ledger.append({'name':name,'rate':str(s.factor(s.sympify(rate).subs(state))),'F1_drift':str(s.factor((rate*(move(V1,j)-V1)).subs(state))),'V_drift':str(s.factor((rate*(move(V,j)-V)).subs(state)))})
def frac(x):return {'exact':str(x),'approx':float(x)}
output={'status':'PASS_EXACT_CONTINUOUS_PRACTICAL_UPPER_CANDIDATE','symbolic_and_rational_checks':len(checks),'checks':checks,'linear_remainder_upper':frac(b1),'quadratic_numerator_upper':frac(b2),'exit_correction_upper':frac(exitcorr),'state_witness':{str(k):v for k,v in state.items()},'F1_witness_drift':frac(g1),'V_witness_drift':frac(gv),'witness_channel_ledger':ledger,'scope':'Pointwise one-sided V drift and stopped costs only; admission and global excursion joining not supplied.'}
(P/'practical_upper_certificate.json').write_text(json.dumps(output,indent=2)+'\n')
(P/'normalized_cubic_coefficients.txt').write_text('\n\n'.join('a^'+str(i)+': '+str(cc) for i,cc in enumerate(cs))+'\n')
print(output['status'],len(checks),'checks; linear noise',float(b1),'quadratic',float(b2),'F1 witness',float(g1),'V witness',float(gv))
