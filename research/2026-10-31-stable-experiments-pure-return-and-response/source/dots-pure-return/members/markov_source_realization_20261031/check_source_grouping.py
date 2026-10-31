import sympy as s
import json
from pathlib import Path

def check(pi,w,name):
 d=len(pi); psi=s.Matrix([s.sqrt(p) for p in pi]); P=psi*psi.T
 q=s.zeros(d)
 for x in range(d):
  for y in range(d):
   if x!=y:q[x,y]=w[x,y]/pi[x]
  q[x,x]=-sum(q[x,y] for y in range(d) if y!=x)
 jumps=[]
 for x in range(d):
  L=s.zeros(d)
  for y in range(d):
   if y!=x:
    L[y,x]=s.sqrt(q[x,y]); L[y,y]=-s.sqrt(q[y,x])
  jumps.append(L)
 C=sum((L.T*L for L in jumps),s.zeros(d))
 R=sum((L.T*P*L for L in jumps),s.zeros(d))
 B=s.zeros(d)
 for x in range(d):
  for y in range(d):
   if x!=y:B[x,y]=-s.sqrt(w[x,y])
  B[x,x]=sum(s.sqrt(pi[y]*w[x,y]/pi[x]) for y in range(d) if y!=x)
 zero=lambda A:all(s.simplify(t)==0 for t in A)
 assert all(zero(L*psi) for L in jumps)
 assert zero(R-B*B)
 for y in range(d):
  D=s.zeros(d);D[y,y]=1
  out=sum((L.T*D*L for L in jumps),s.zeros(d))-(C*D+D*C)/2
  assert zero(out-s.diag(*[q[x,y] for x in range(d)]))
 support=[1+sum(q[x,y]!=0 for y in range(d) if y!=x) for x in range(d)]
 trace_bound=sum(2*(-q[x,x])*sum(pi[y] for y in range(d) if y==x or q[x,y]!=0) for x in range(d))
 assert s.simplify(trace_bound-s.trace(R))>=0
 return {'name':name,'d':d,'C_trace':str(s.simplify(s.trace(C))),'R_trace':str(s.simplify(s.trace(R))),'universal_trace_bound':str(s.simplify(trace_bound)),'exact_dark_diagonal_closure_and_return_square':True}

out=[]
for d in [2,3,4,5]:
 pi=[s.Rational(1,d)]*d; w=s.zeros(d)
 for x in range(d):
  for y in range(d):
   if x!=y:w[x,y]=s.Rational(1,d*d)
 out.append(check(pi,w,'uniform_reset_'+str(d)))
for d in [4,5,6]:
 pi=[s.Rational(1,d)]*d; w=s.zeros(d)
 for x in range(d):w[x,(x+1)%d]=w[(x+1)%d,x]=s.Rational(1,d)
 out.append(check(pi,w,'cycle_unit_rates_'+str(d)))
pi=[s.Rational(1,6),s.Rational(1,3),s.Rational(1,2)]
w=s.Matrix([[0,1,4],[1,0,9],[4,9,0]])
out.append(check(pi,w,'nonuniform_three_state'))
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
