"""Exact small checks of a CLIQUE reduction, not an empirical hardness claim.

Proof is in SOURCE_NORMALIZATION_AND_COMPLEXITY.md. Fraction arithmetic only.
No hidden states, sampling, source binaries or approximate eigenvalues.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse,json,random,time
from source_normalization_cut import inverse,mv,dot,serial

def instance(n,edges,k):
 deg=[0]*n
 for i,j in edges:deg[i]+=1;deg[j]+=1
 eps=F(1,256*n**3)
 b=[[F(0) for _ in range(n)] for _ in range(n)]
 for i in range(n):b[i][i]=n-F(2,3)*deg[i]
 for i,j in edges:b[i][j]=b[j][i]=F(1)
 a=[[F(int(i==j))-eps*b[i][j] for j in range(n)] for i in range(n)]
 assert all(sum(row)>0 for row in a)
 assert all(a[i][i]>sum(abs(a[i][j]) for j in range(n) if j!=i) for i in range(n))
 g=inverse(a);assert all(z>=0 for row in g for z in row)
 constant=F(n*n)+F(2,3)*len(edges)
 qbase=F(n+3*k)+eps*(constant+3*n*k)
 tail_bound=16*n**3*eps**2/(1-2*n*eps)
 assert 0<tail_bound<eps/4
 rows=[];max_edges=-1;max_q=F(-1)
 for chosen in combinations(range(n),k):
  S=set(chosen);s=[F(1+int(i in S)) for i in range(n)]
  es=sum(i in S and j in S for i,j in edges)
  assert dot(s,mv(b,s))==constant+3*n*k+2*es
  q=dot(s,mv(g,s));tail=q-qbase-2*eps*es
  assert 0<=tail<=tail_bound
  rows.append((es,q));max_edges=max(max_edges,es);max_q=max(max_q,q)
 recovered=(max_q-qbase)//(2*eps)
 assert recovered==max_edges
 K=k*(k-1)//2;threshold=qbase+2*eps*K-eps/2
 assert (max_q>threshold)==(max_edges==K)
 # Approximation error of either sign, bounded as in the theorem.
 for perturb in [-eps/5,eps/5]:
  approximate=max_q+perturb
  assert (approximate-qbase+eps/2)//(2*eps)==max_edges
 return dict(n=n,k=k,edges=len(edges),epsilon=eps,source_mass=n+k,maximum_edges=max_edges,
  optimal_mean=max_q/(n+k),certified_tail_bound=tail_bound,exact_recovery=recovered,
  clique_decision=max_q>threshold,vertices_checked=len(rows))

def main(out):
 st=time.monotonic();rng=random.Random(2026101402);rows=[]
 for n in range(2,9):
  for case in range(5):
   edges=[(i,j) for i in range(n) for j in range(i) if rng.random()<.5]
   for k in sorted(set([2,n//2,n])):rows.append(instance(n,edges,k))
 result=dict(status='PASS',cases=len(rows),vertices_checked=sum(x['vertices_checked'] for x in rows),seconds=time.monotonic()-st,
  scope='Finite rational implementation checks of the written reduction. Conditional complexity claim assumes standard NP-completeness of CLIQUE. No constant-accuracy hardness or molecular experiment.',rows=rows)
 out.mkdir(parents=True,exist_ok=True);(out/'CORRELATED_SOURCE_HARDNESS_RESULTS.json').write_text(json.dumps(serial(result),indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True);main(p.parse_args().output_dir)
