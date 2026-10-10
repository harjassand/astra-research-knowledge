"""Verify exact pair distances/MST and subset-BFS reset lengths for proxy extensions."""
from reset_potential_search import pair_dist,mst,reset_bfs,image
import json

def cerny(m):
 return [tuple((i+1)%m for i in range(m)),tuple(0 if i==m-1 else i for i in range(m))]

def proxy_extend(A):
 m=len(A[0]); assert len(A)>=2
 B=[]
 for j,f in enumerate(A):
  B.append(tuple(f)+tuple(f[i if j==0 else i+1] for i in range(m-1)))
 return B

def main():
 out=[]
 for m in range(2,13):
  A=cerny(m);B=proxy_extend(A);n=2*m-1
  assert all(set(f)==set(g) for f,g in zip(A,B))
  d,_=pair_dist(B);w,reached=reset_bfs(B)
  edges=[]
  for i in range(m-1):
   p=m+i
   assert B[0][i]==B[0][p]
   assert B[1][i+1]==B[1][p]
   edges +=[(i,p),(p,i+1)]
  p=mst(tuple(range(n)),d)
  assert p==n-1
  assert len(w)==(m-1)**2
  record={'core_states':m,'states':n,'mst':p,'reset_length':len(w),'formula':(m-1)**2,'reset_word':''.join('ab'[x] for x in w),'reachable_subsets_examined':reached,'A':B,'unit_tree':edges}
  out.append(record)
  print(m,n,p,len(w),reached,flush=True)
 json.dump({'verified':out,'scope':'Finite checks support, but do not replace, the all-m theorem proved in RESET_PROXY_THEOREM.md.'},open('independent_programme/fresh_theory_20261010/proxy_extension_results.json','w'),indent=2)
if __name__=='__main__':main()
