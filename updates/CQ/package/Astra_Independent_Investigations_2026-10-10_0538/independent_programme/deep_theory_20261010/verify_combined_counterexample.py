"""Independent exact checker of the uniform-0/1 stationary averaging failure.
No floating point, optimization, or external data needed.
"""
import json
from pathlib import Path
from fractions import Fraction as F
import sympy as sp
BASE=Path(__file__).resolve().parent

def internal_graph():
 H=[[0]*16 for _ in range(16)]
 groups=[list(range(4)),list(range(4,7)),list(range(7,11)),list(range(11,15))]
 for b in range(4):
  for i in groups[b]:
   for j in groups[(b+1)%4]:H[i][j]=1
 for i in range(4):H[i][(i+1)%4]=1
 for j in range(4):H[15][j]=1
 assert [sum(row) for row in H]==[4]*16
 return H,groups

def graph_stats(A):
 n=len(A);out=[{j for j,x in enumerate(row) if x} for row in A]
 indeg=[sum(row[j] for row in A) for j in range(n)]
 for i in range(n):
  assert i not in out[i]
  assert all(i not in out[j] for j in out[i])
  assert all(i not in out[k] for j in out[i] for k in out[j])
 sec=[len(set().union(*(out[j] for j in out[i]))-out[i]-{i}) for i in range(n)]
 return out,indeg,sec

def check_scc(A):
 n=len(A)
 for rev in [False,True]:
  seen={0};todo=[0]
  while todo:
   u=todo.pop()
   for v in range(n):
    if (A[v][u] if rev else A[u][v]) and v not in seen:seen.add(v);todo.append(v)
  assert len(seen)==n

def verify(q,write_full=False):
 H,groups=internal_graph();R=16*q+4;N=3*q+1;n=16*N
 _,hi,hs=graph_stats(H)
 # Independently solve the 16 exact vertex equations, not the five-group formulas.
 sigma=(R*sp.eye(16)-sp.Matrix(H).T).inv()*(q*sp.ones(16,1))
 assert sum(sigma)==1 and all(x>0 for x in sigma)
 sf=[F(int(x.p),int(x.q)) for x in sigma]
 A=[[int((j//16-i//16)%N in range(1,q+1)) if i//16!=j//16 else H[i%16][j%16] for j in range(n)] for i in range(n)]
 out,din,sec=graph_stats(A);check_scc(A)
 assert all(len(s)==R for s in out)
 assert din==[16*q+hi[i%16] for i in range(n)]
 assert sec==[16*q+hs[i%16] for i in range(n)]
 pi=[sf[i%16]/N for i in range(n)]
 assert sum(pi)==1
 assert all(sum(pi[i]*A[i][j] for i in range(n))==R*pi[j] for j in range(n))
 mean_d=sum(pi[i]*din[i] for i in range(n));mean_s=sum(pi[i]*sec[i] for i in range(n));joint=mean_d+mean_s-2*R
 formula=-F(256*q**4-464*q**3-568*q*q-193*q-24,4*(4*q+1)*(256*q**3+240*q*q+84*q+13))
 assert joint==formula
 result={'q':q,'n':n,'r':R,'sigma':[str(x) for x in sf],'internal_indegrees':hi,'internal_second_counts':hs,'block_masses':{name:str(sum(sf[j] for j in g)) for name,g in zip(['A','B','C','D'],groups)},'source_mass':str(sf[15]),'mean_indegree':str(mean_d),'indegree_surplus':str(mean_d-R),'mean_second':str(mean_s),'second_surplus':str(mean_s-R),'joint_surplus':str(joint),'exact_stationarity':True,'row_regular':True,'oriented_triangle_free':True,'strongly_connected':True}
 if write_full:
  full=dict(result,A=A,pi=[str(x) for x in pi],indegrees=din,second_counts=sec)
  (BASE/f'independent_certificate_n{n}_r{R}.json').write_text(json.dumps(full,indent=2)+'\n')
 return result

if __name__=='__main__':
 records=[verify(q,write_full=q in (1,3)) for q in [1,2,3,4]]
 assert records[2]['joint_surplus']=='-2493/485524'
 (BASE/'combined_counterexample_verified.json').write_text(json.dumps(records,indent=2)+'\n')
 print(json.dumps([{k:v for k,v in row.items() if k not in ('sigma','internal_indegrees','internal_second_counts')} for row in records],indent=2))
