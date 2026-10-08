from fractions import Fraction as F
from itertools import product
from pathlib import Path
from collections import Counter
import json
from parity_lift_check import trace

def pf(M):
 A=[row.copy() for row in M];n=len(A);r=F(1)
 assert n%2==0
 for k in range(0,n,2):
  p=next((j for j in range(k+1,n) if A[k][j]),None)
  if p is None:return F(0)
  if p!=k+1:
   A[p],A[k+1]=A[k+1],A[p]
   for row in A:row[p],row[k+1]=row[k+1],row[p]
   r=-r
  a=A[k][k+1];r*=a
  for i in range(k+2,n):
   for j in range(i+1,n):
    A[i][j]+=(A[k+1][i]*A[k][j]-A[k][i]*A[k+1][j])/a
    A[j][i]=-A[i][j]
 return r

def network(n,edges):
 m=len(edges);wires=[]
 for z in range(n):
  occ=[(k,0 if z==i else 1) for k,(i,j) in enumerate(edges) if z in (i,j)]
  if not occ:continue
  for t,(k,port) in enumerate(occ):
   kn,pn=occ[(t+1)%len(occ)]
   wires.append((4*k+port,4*kn+pn+2))
 return wires

def mat(edges,wires,signs):
 m=len(edges);A=[[F(0) for _ in range(4*m)] for _ in range(4*m)]
 # a=4,c=4,d=1,b=9. Uncomplemented local Pfaffian matrix.
 for k in range(m):
  for i,j,x in [(0,1,F(1,2)),(2,3,F(1,2)),(0,2,F(3,2)),(1,3,F(3,2)),(0,3,F(1)),(1,2,F(1))]:
   A[4*k+i][4*k+j]=x;A[4*k+j][4*k+i]=-x
 for (i,j),s in zip(wires,signs):
  if i>j:i,j=j,i
  A[i][j]+=s;A[j][i]-=s
 return A

def physical(n,edges):
 coeff={'a':F(4),'c':F(4),'d':F(1)};Z=F(0)
 for word in product('acd',repeat=len(edges)):
  t,_=trace(n,edges,word);w=F(t)
  for q in word:w*=coeff[q]
  Z+=w
 return Z

def main():
 results=[]
 for name,n,edges in [
  ('one_gate',2,[(0,1)]),
  ('D2_topology',2,[(0,1),(0,1)]),
  ('triangle',3,[(0,1),(0,2),(1,2)]),
  ('four_cycle',4,[(0,1),(1,2),(2,3),(3,0)]),
  ('interleaved_bowtie',5,[(0,1),(0,3),(0,2),(0,4),(1,2),(3,4)])]:
  wires=network(n,edges);N=2**len(wires);S=F(0);S2=F(0);counts=Counter()
  for signs in product([-1,1],repeat=len(wires)):
   val=pf(mat(edges,wires,signs))**2
   S+=val;S2+=val**2;counts[str(val)]+=1
  mean=S/N;second=S2/N;Z=physical(n,edges);lift=F(4)**len(edges)*mean
  assert Z==lift,(name,Z,lift)
  r={'name':name,'qubits':n,'gates':len(edges),'wires':len(wires),'weights':{'a':'4','b':'9','c':'4','d':'1'},'sign_assignments':N,'physical_Z':str(Z),'lift_Z':str(lift),'mean_det':str(mean),'second_moment_det':str(second),'relative_second_moment':str(second/mean**2),'relative_variance':str(second/mean**2-1),'positive_support_fraction':str(F(N-counts['0'],N)),'det_distribution':dict(sorted(counts.items(),key=lambda kv:F(kv[0])))}
  results.append(r)
  print(json.dumps({k:v for k,v in r.items() if k!='det_distribution'}))
 Path('work/agents/epr_parity/results/pfaffian_lift.json').write_text(json.dumps({'proof_status':'Parseval coefficient argument; all listed finite cases exact-rational verified','results':results},indent=2)+'\n')

if __name__ == "__main__": main()
