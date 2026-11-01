#!/usr/bin/env python3
"""Exact literal-channel identities and outward-safe gate-sum evaluation."""
import json
from decimal import Decimal as D, localcontext, ROUND_CEILING
from pathlib import Path
import sympy as s

A,B,C,F,E=s.symbols('A B C D E', nonnegative=True)
x=s.Matrix([A,B,C,F,E]); L=A+(C+F)/2; Z=C-F
rows=[(1,[1,0,0,0,0]),(A,[-1,0,0,0,0]),
 (A*(A-1),[-1,0,1,0,0]),(A*C,[1,0,-1,0,0]),
 (A*(A-1),[-1,0,0,1,0]),(A*F,[1,0,0,-1,0]),
 (A*(A-1),[-1,0,0,0,1]),(A*E,[1,0,0,0,-1]),
 (A*E,[-1,0,1,1,-1]),(2*C*F,[1,0,-1,-1,1]),
 (C*F,[1,1,-1,-1,0]),(A*B,[-1,-1,1,1,0])]
def delta(f,mark):
 return s.expand(f.subs(dict(zip(x,x+s.Matrix(mark))),simultaneous=True)-f)
def G(f):return s.expand(sum(rate*delta(f,v) for rate,v in rows))
def q(f):return s.expand(sum(rate*delta(f,v)**2 for rate,v in rows))
checks={
 'GA':(G(A),1-A-3*A*(A-1)+A*(C+F)+3*C*F-A*B),
 'GL':(G(L),1+A+A*L-3*A*A+A*E),
 'qLL':(q(L),1-A/2+A*A+A*L/2+A*E),
 'GZ':(G(Z),-A*Z), 'qZ':(q(Z),2*A*(L-1)),
 'A_up':(sum(rate for rate,v in rows if v[0]==1),1+A*(C+F)+A*E+3*C*F),
 'A_down':(sum(rate for rate,v in rows if v[0]==-1),A+3*A*(A-1)+A*E+A*B),
 'E_up':(sum(rate for rate,v in rows if v[4]==1),A*(A-1)+2*C*F),
 'GL_minus_qLL':(G(L)-q(L),A*(s.Rational(3,2)+L/2-4*A))}
for name,(got,want) in checks.items():assert s.expand(got-want)==0,name
assert all(abs(v[0])==1 for rate,v in rows)
assert all(abs(delta(L,v))<=1 and abs(delta(Z,v))<=1 for rate,v in rows)

def run(power):
 with localcontext() as c:
  c.prec=90
  N=D(10)**power;T=(N.ln()/5).exp(); m0=D(400); ln2=D(2).ln()
  def expupper(y):
   # A positive upper replacement avoids underflow and silently deleted tails.
   return D('1e-4000') if y < D(-9200) else y.exp()*(1+D('1e-80'))
  H0=2*m0*(1+3*m0*m0)/(D('.9')*N-2*m0)
  rho0=(1+3*m0*m0+8*m0**3+2*m0)/(D('.9')*N)
  startup={'A':2*m0*(1+3*m0*m0)*rho0**2,
   'marks':(4+2*m0)*H0,'E':expupper(-(8*ln2-4)*m0**3),
   'time':expupper(-(1-ln2)*m0)}
  total={k:D(0) for k in ['A','Z','floor','time','birth','source']};stages=[]
  m=m0
  while m<N/5000:
   h=m/400;U=min(2*m,N/5000);d=min(4*m,4*T)
   eb=min(128*m**3,2*(N*m).sqrt(),N/100).to_integral_value(rounding=ROUND_CEILING)
   r=1+3*U*U;b=eb+2*U;rho=(r/h+b)/(D('.9')*N)
   assert 0<rho<D('.545')
   loga=(1+d*(r+b*(h-1))).ln()+(h+1)*rho.ln()
   # Stage 0 may start at A=2; its initial excursion costs rho, not rho^2.
   a_initial_extra=rho-rho*rho if m==m0 else D(0)
   DD=(2 if m==m0 else h)+2*(eb+1)+d; v=8*U*DD/(D('.9')*N); dz=h+1
   ratio=dz/v;asinh=(ratio+(1+ratio*ratio).sqrt()).ln()
   logz=ln2-dz*asinh+(v*v+dz*dz).sqrt()-v
   probs={'A':expupper(loga)+a_initial_extra,'Z':expupper(logz),
    'floor':expupper(-ln2*m/2),'time':expupper(ln2*(m+1)-4*(2*ln2-1)*m),
    'birth':expupper(-(128*ln2-64)*m**3),'source':expupper(-DD/124)}
   for key,val in probs.items():total[key]+=val
   stages.append({'m':str(m),'h':str(h),'U':str(U),'Ebar':str(eb),
    'rho':str(rho),'vZ':str(v),'probabilities':{k:str(v) for k,v in probs.items()}})
   m*=2
  value=sum(startup.values())+sum(total.values())
  # Round upward to ten significant decimal digits.
  quantum=D(10)**(value.adjusted()-9)
  rounded=value.quantize(quantum,rounding=ROUND_CEILING)
  return {'N':str(N),'T':str(T),'stage_count':len(stages),
   'startup':{k:str(v) for k,v in startup.items()},
   'stage_sums':{k:str(v) for k,v in total.items()},'sum':str(value),
   'outward_table_bound':str(rounded),'stages':stages}

out={'status':'PASS_AUTHOR_ACTUAL_GATES_ALGEBRA_AND_NUMBERS_NOT_INDEPENDENT_RECEIPT',
 'exact_identity_checks':list(checks),'results':[run(p) for p in range(20,26)]}
path=Path(__file__).with_name('actual_gates_checks.json');path.write_text(json.dumps(out,indent=2)+'\n')
for row in out['results']:print(row['N'],row['outward_table_bound'],row['stage_count'])
