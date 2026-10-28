"""Exact Q(omega) replay. No floating quantum entropy enters the certificate."""
from fractions import Fraction as Q
from pathlib import Path
import json,time
OUT=Path(__file__).resolve().parent/'outputs'
def q(x=0,y=0):return Q(x),Q(y)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return -x[0],-x[1]
def sub(x,y):return add(x,neg(y))
def mul(x,y):return x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]-x[1]*y[1]
def scale(x,s):return x[0]*s,x[1]*s
def conj(x):return x[0]-x[1],-x[1]
def wp(k):return [q(1),q(0,1),q(-1,-1)][k%3]
def zeros(n):return [[q() for _ in range(n)] for _ in range(n)]
def mm(a,b):return [[sumq(mul(x,y) for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def sumq(v):
 z=q()
 for x in v:z=add(z,x)
 return z
def tr(a):return sumq(a[i][i] for i in range(len(a)))
def sic(a,b):
 return [[scale(sub(q(int(d==e)),wp(b*(e-d)) if e==(-d-a)%3 else q()),Q(1,2)) for e in range(3)] for d in range(3)]
def bell(a,b):
 z=zeros(9)
 for i in range(3):
  for k in range(3):z[3*i+(i+a)%3][3*k+(k+a)%3]=scale(wp(b*(i-k)),Q(1,3))
 return z
def replay():
 start=time.perf_counter();ss=[sic(a,b) for a in range(3) for b in range(3)];bs=[bell(a,b) for a in range(3) for b in range(3)]
 unit_components=0
 for s,b in zip(ss,bs):
  assert mm(s,s)==s and tr(s)==q(1)
  for u in range(3):
   for d in range(3):
    i,j=(u+d)%3,(u+2*d)%3
    for v in range(3):
     for e in range(3):
      k,l=(v+e)%3,(v+2*e)%3
      actual=sub(q(Q(int(i==k and j==l),6)),scale(b[3*k+j][3*i+l],Q(1,2)))
      expected=scale(s[d][e],Q(int(u==v),3))
      assert actual==expected,(u,d,v,e,actual,expected)
      unit_components+=1
 for i in range(9):
  for j in range(9):
   assert tr(mm(ss[i],ss[j]))==q(1 if i==j else Q(1,4))
   assert tr(mm(bs[i],bs[j]))==q(int(i==j))
 for d in range(3):
  for e in range(3):assert sumq(s[d][e] for s in ss)==q(3*int(d==e))
 result={'field':'Q[omega]/(omega^2+omega+1)','basis_block_components':unit_components,
 'SIC_HS_pairs':81,'Bell_HS_pairs':81,'all_SIC_projectors':9,
 'exact_identity':'N(rho(p)) = permutation [I3/3 tensor sum p_ab S_ab] permutation*',
 'purity_identity':'Tr M(p)^2 = (1+3 sum p_ab^2)/4',
 'entropy_identity':'Delta(rho(p)) = 2 S(M(p)) - H(p)',
 'elapsed_seconds':time.perf_counter()-start}
 (OUT/'SIC_EXACT_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':replay()
