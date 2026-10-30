"""Actual finite graph-CZ, bulk H, pointer CNOT-readout dictionary."""
import numpy as np,json
# n=2, T=1, CSS H_Z=[11], H_X=[]; code layers 0..2.
# vertices 0..5 data, 6,7 Z-check ancillas at outer layers.
edges=[(0,2),(1,3),(2,4),(3,5),(6,0),(6,1),(7,4),(7,5)]
boundary=[0,1,4,5];bulk=[2,3,6,7];nb=len(boundary);nk=len(bulk);N=8
embed=lambda v,sites:sum(((v>>j)&1)<<i for j,i in enumerate(sites))
phase=lambda x,a:1-2*((x&a).bit_count()%2)
M=np.empty((1<<nb,1<<nk))
for b in range(1<<nb):
 for k in range(1<<nk):
  x=embed(b,boundary)|embed(k,bulk)
  M[b,k]=(-1)**sum(((x>>i)&1)*((x>>j)&1) for i,j in edges)/np.sqrt(1<<N)
H=np.array([[phase(k,s) for s in range(1<<nk)] for k in range(1<<nk)])/np.sqrt(1<<nk)
ideal=M@H
res=0.;cases=0
for a in range(1<<N):
 ab=sum(((a>>i)&1)<<j for j,i in enumerate(boundary));ak=sum(((a>>i)&1)<<j for j,i in enumerate(bulk))
 actual_pre_pointer=np.array([[M[b,k]*phase(embed(b,boundary)|embed(k,bulk),a) for k in range(1<<nk)] for b in range(1<<nb)])@H
 for c in range(1<<nk):
  for m in range(1<<nk):
   # CNOT copies the post-H computational bit, with input pointer c.
   actual=actual_pre_pointer[:,m^c]
   predicted=np.array([phase(b,ab) for b in range(1<<nb)])*ideal[:,m^c^ak]
   res=max(res,float(np.linalg.norm(actual-predicted)));cases+=1
assert res<1e-12
print(json.dumps(dict(result='PASS',graph_vertices=N,pointers=nk,defect_record_branches=cases,max_dictionary_residual=res,scope='exact finite source dictionary, not cluster threshold or autonomous preparation'),indent=2))
