#!/usr/bin/env python3
"""Independent exact-Fraction row regressions plus exact stopped-cost algebra."""
from fractions import Fraction as F
from pathlib import Path
import sympy as s,json
P=Path(__file__).parent
rows=[(1,1,0,0,1),(-1,-1,0,0,-1),(-1,F(-1,2),0,1,0),(1,F(1,2),0,-1,0),(-1,F(-1,2),0,-1,0),(1,F(1,2),0,1,0),(-1,-1,1,0,0),(1,1,-1,0,0),(-1,0,-1,0,0),(1,0,1,0,0),(1,0,0,0,0),(-1,0,0,0,0)]
def rates(x):
 A,L,E,Z,S,N=x;C=L-A+Z/2;D=L-A-Z/2;B=S-2*L+A-E
 return [F(1),A,A*(A-1),A*C,A*(A-1),A*D,A*(A-1),A*E,A*E,2*C*D,C*D,A*B]
def move(x,j):return tuple(y+z for y,z in zip(x[:5],j))+(x[5],)
def V(x):A,L,E,Z,S,N=x;return (E*E-F(4,3)*A*E)/(N*L)
def WL(x):return 1/x[1]
def WE(x):return x[0]/x[2]**2+3/x[2]
def G(x,fn):return sum(rate*(fn(move(x,j))-fn(x)) for rate,j in zip(rates(x),rows))
def Q(x,fn):return sum(rate*(fn(move(x,j))-fn(x))**2 for rate,j in zip(rates(x),rows))
ns=nc=nr=0
for r in [F(3,2),F(9,5),F(2)]:
 for L in [F(100),F(10000),F(100000000)]:
  for u in [F(1,100),F(1,10000),F(1,100000000)]:
   N=r*L/u**2;E=r*L/u
   for A in sorted(set([F(0),F(1),L/100,L/5])):
    for Z in sorted(set([F(0),F(2)*(L//200)])):
     for sg in [-1,0,1]:
      S=N+sg*E/50;x=(A,L,E,Z,S,N)
      C=L-A+Z/2;D=L-A-Z/2;B=S-2*L+A-E
      assert all(v.denominator==1 for v in [A,C,D,E,B,N,S])
      assert all(v>=0 for v in rates(x))
      upper=-r/(L+1)-F(4,3)*E/(N*(L+1))-(4*L*L-Z*Z)/(6*N*L)-A*E/(8*L)
      assert G(x,V)<=upper; ns+=1
      if A>L/100:continue
      qll=sum(rate*j[1]**2 for rate,j in zip(rates(x),rows));qa=sum(rates(x));qe=(A*B/2+C*D)/E**2
      assert G(x,WL)<=-F(98,99)*qll/L**2
      assert Q(x,WL)<=qll/L**2/F(99)**2
      assert G(x,WE)<=1/E**2-qe
      assert Q(x,WE)<=64/E**4*(1+3*A*B+3*C*D)
      assert Q(x,V)<=9*qll/L**2+25*u*u*qa/L**2
      assert qa<=1+3*A*B+3*C*D
      nc+=1
      for rate,j in zip(rates(x),rows):
       if rate==0:continue
       y=move(x,j)
       assert abs(V(y)-V(x))<=F(11,500)
       assert 0<=y[2]**2/(N*y[1])-V(y)<F(3,10000)
       assert abs(WE(y)-WE(x))<=8/E**2
       assert abs(WL(y)-WL(x))<=F(1,9900)
       nr+=1
# Continuous cost simplifications, not samples.
M,L0,DE,m=s.symbols('M L0 DE m',positive=True)
k=(M-2)/(M-1);ql=2/(k*L0);x=1/L0;j=1/(M*(M-1));vv=ql/(M-1)**2
ex=s.factor(x*x/(2*(vv+j*x/3)))
assert s.factor(ex-3*M*(M-1)*(M-2)/(2*L0*(7*M-2)))==0
lo=s.factor(ex.subs(L0,2*M)-M/10)
assert s.factor(lo-(M*M-41*M+30)/(20*(7*M-2)))==0
assert 100**2-41*100+30>0
assert F(1,2)/(64*13+F(8,3))>F(1,1670)
assert F(9)+F(1,225)+F(1200,22500)==F(2038,225)
out={'status':'PASS_EXACT_STOPPED_CLOCK_AND_ROW_REGRESSIONS','drift_states':ns,'full_cost_states':nc,'active_row_jumps':nr,'exact_cost_algebra_checks':5,'note':'Row regressions supplement but do not replace the continuous sign certificate. Gate acquisition and global excursion joining remain separate.'}
(P/'stopped_clock_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
