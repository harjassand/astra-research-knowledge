"""Independent exact rational checks, using only input.json and witness JSONs.
No float or interval library is trusted. Algebraic atom definitions and dual
inequalities are proved in RESULT.txt; this program checks their input facts.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time
start=time.perf_counter();cpu=time.process_time()
f=lambda z:F(int(z['numerator']),int(z['denominator']))
inp=json.loads(Path('input.json').read_text());D=int(inp['jacobi']['denominator'])
aI=list(map(int,inp['jacobi']['diagonal_int']));bI=list(map(int,inp['jacobi']['offdiagonal_int']))
a=[F(z,D) for z in aI];b=[F(z,D) for z in bI];bs=[z*z for z in b]
S=f(inp['S']);x=f(inp['x']);assert S==f(inp['M'])+f(inp['tau'])+f(inp['operator_error'])
assert len(a)==64 and len(b)==63 and all(z>0 for z in b)
def R(t):
 p=1/(t-a[0])
 for ai,bi in zip(a[1:],bs):p=1/(t-ai-bi*p)
 return p
for sign in [-1,1]:
 p=S+sign*a[0];assert p>0
 for ai,bi in zip(a[1:],bs):p=S+sign*ai-bi/p;assert p>0
# Independent rational interval arithmetic.
def add(u,v):return (u[0]+v[0],u[1]+v[1])
def sub(u,v):return (u[0]-v[1],u[1]-v[0])
def mul(u,v):
 z=[u[0]*v[0],u[0]*v[1],u[1]*v[0],u[1]*v[1]];return (min(z),max(z))
def sq(u):return (F(0) if u[0]<=0<=u[1] else min(u[0]**2,u[1]**2),max(u[0]**2,u[1]**2))
def pt(v):return(v,v)
def weight(lo,hi,v):
 z=(lo,hi);prev=pt(F(1));curr=mul(sub(z,pt(a[0])),pt(1/b[0]));s=add(prev,sq(curr))
 for k in range(1,63):
  nxt=mul(sub(mul(sub(z,pt(a[k])),curr),mul(pt(b[k-1]),prev)),pt(1/b[k]))
  prev,curr=curr,nxt;s=add(s,sq(curr))
 num=sub(mul(sub(z,pt(a[63])),curr),mul(pt(b[62]),prev));s=add(s,mul(sq(num),pt(1/v)))
 return (1/s[1],1/s[0])
results=[]
for name in ['maximum_witness','near_infimum_witness']:
 w=json.loads(Path(name+'.json').read_text());y=f(w['prescribed_node']);v=f(w['last_offdiagonal_squared']);d=f(w['last_diagonal'])
 assert v==(S-y)/(R(S)-R(y)) and d==y-v*R(y) and v>0
 assert S-d-v*R(S)==0 and d+S+v*R(-S)>0
 # Exact LDL sign changes, independently written in rational continued-fraction
 # form. Endpoint determinants are zero; count only interior bracket endpoints.
 def count(t):
  prev=F(1);curr=a[0]-t;seq=[prev,curr]
  for ai,bi in zip(a[1:]+[d],bs+[v]):
   prev,curr=curr,(ai-t)*curr-bi*prev;seq.append(curr)
  signs=[1 if z>0 else -1 for z in seq if z]
  return sum(u!=v for u,v in zip(signs,signs[1:])),curr==0
 assert count(y)==(1,True);assert count(S)==(64,True)
 nodes=w['nodes'];assert len(nodes)==65
 for i,n in enumerate(nodes):
  lo,hi=f(n['lower']),f(n['upper'])
  if lo==hi:assert count(lo)==(i,True)
  else:assert count(lo)==(i,False) and count(hi)==(i+1,False)
  if i:assert f(nodes[i-1]['upper'])<lo
 assert f(nodes[0]['upper'])<x and x<=y<f(nodes[2]['lower'])
 verified=[]
 for k in [0,1]:
  n=nodes[k];lo,hi=weight(f(n['lower']),f(n['upper']),v)
  assert F(n['weight_lower'])<=lo<=hi<=F(n['weight_upper'])
  verified.append((lo,hi))
 # CDF relation checked with rational arithmetic, including threshold atom.
 cdf=add(verified[0],verified[1]) if y==x else verified[0]
 assert F(w['cdf_at_x']['lower'])<=cdf[0]<=cdf[1]<=F(w['cdf_at_x']['upper'])
 results.append({'name':name,'all65_root_isolators_checked':True,'support_Schur_checked':True,'first_two_weights_exact_rational_interval_checked':True,'CDF_checked':True})
print(json.dumps({'PASS':True,'witnesses':results,'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu},indent=2))
