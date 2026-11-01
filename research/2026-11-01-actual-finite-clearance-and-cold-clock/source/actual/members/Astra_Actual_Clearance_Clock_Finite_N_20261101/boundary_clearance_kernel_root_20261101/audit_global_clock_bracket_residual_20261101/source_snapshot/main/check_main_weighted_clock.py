#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import sympy as s,json
P=Path(__file__).parent
A,L,E,Z,S=s.symbols('A L E Z S');C=L-A+Z/2;D=L-A-Z/2;B=S-2*L+A-E
rates=[1,A,A*(A-1),A*C,A*(A-1),A*D,A*(A-1),A*E,A*E,2*C*D,C*D,A*B]
v=[1,-1,-F(1,2),F(1,2),-F(1,2),F(1,2),-1,1,0,0,0,0]
GL=s.expand(sum(q*j for q,j in zip(rates,v)));qLL=s.expand(sum(q*j*j for q,j in zip(rates,v)))
assert s.expand(GL-(1+A+A*L+A*E-3*A*A))==0
assert s.expand(qLL-(1-A/2+A*A+A*L/2+A*E))==0
assert s.expand(GL-qLL-A*(s.Rational(3,2)+L/2-4*A))==0
# R(T) decreases for T>1; endpoint rational tests cover continuous T intervals.
R10=F(10,9)**5;Rbig=F(10000,9999)**5
assert R10<2 and R10**2<3
assert Rbig<F(1001,1000) and Rbig**2<F(1003,1000)
assert F(5,2)*F(1001,1000)<3
# Exact lower thresholds and Freedman exponent constants.
assert F(5,4)**2/(2*(15+F(5,12)))>F(1,20)
assert 4-F(5,4)-F(25600,17100)>=F(5,4)
assert F(5,4)**2/(2*(24+F(5,12)))>F(1,32)
assert F(9997,10000)*F(3,2)-F(5,4)-F(25600,171*10000**2)>F(1,5)
assert F(1,5)**2/(2*(F(3009,2000)+F(1,15)))>F(1,80)
def psi(x):return F(1) if x<=1 else x**-5
def H(x):return F(5,4)-x if x<=1 else F(1,4)*x**-4
n=0
for T in [10,11,100,10000,100000]:
 R=F(T,T-1)**5
 xs=[F(0),F(1,2*T),F(1,T),F(1,10),1-F(1,T),1-F(1,2*T),F(1),1+F(1,2*T),1+F(1,T),F(10),F(10000),F(10**10)]
 for x in xs:
  for v in [-F(1),-F(1,2),F(0),F(1,2),F(1)]:
   d=v/T;y=x+d
   if y<0:continue
   rem=H(y)-H(x)+psi(x)*d
   assert 0<=rem<=F(5,2)*R*psi(x)*d*d
   assert abs(H(y)-H(x))<=abs(d)
   assert (H(y)-H(x))**2<=R*R*psi(x)*d*d
   n+=1
out={'status':'PASS_EXACT_MAIN_WEIGHTED_CLOCK','all_channel_symbolic_identities':3,'rational_continuous_constant_checks':10,'exact_finite_jump_regressions':n,'R10':str(R10),'R10000':str(Rbig),'scope':'Bounded primitive plus conditional actual occupation clocks; physical/source gate acquisition not supplied.'}
(P/'main_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
