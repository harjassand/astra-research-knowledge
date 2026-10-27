from pathlib import Path
from itertools import combinations
import numpy as np,json
from edge_retarget_check import graph,balanced_cycles
OUT=Path(__file__).parent;rng=np.random.default_rng(2710);records=[]
for n in [5,6]:
 edges,adj=graph(n);flow=balanced_cycles(edges,adj);total=np.zeros(5);maxpop=0.;naivepop=0.
 for number in range(n+1):
  states=[s for s in range(1<<n) if s.bit_count()==number];m=len(states)
  if m==1:continue
  ix={s:i for i,s in enumerate(states)};H=np.zeros((m,m));J=np.zeros((m,m),complex);f0=np.zeros((m,m),complex);fa=np.zeros((m,m),complex)
  for u,v in combinations(states,2):
   if (u,v) not in edges:continue
   site,amp=edges[u,v];a=float(amp);i,j=ix[u],ix[v];H[i,j]=H[j,i]=-a
   direction=1 if ((u>>site)&1)==1 else -1
   J[i,j]=1j*a*direction;J[j,i]=-J[i,j]
   value=float(flow[u,v]);f0[i,j]=1j*value;f0[j,i]=-f0[i,j];fa[i,j]=f0[i,j]/a;fa[j,i]=-fa[i,j]
  for s in states:H[ix[s],ix[s]]=sum(4*((s>>i)&1)*((s>>((i+1)%n))&1)+.7*((s>>i)&1)*((s>>((i+2)%n))&1) for i in range(n))
  g=rng.normal(size=(m,m))*.02;g=(g+g.T)/2
  rate=np.array([((u^v).bit_count()) for u in states for v in states],float)
  inv=np.zeros_like(rate);np.divide(1.,rate,out=inv,where=rate>0)
  A=-1j*(np.kron(H,np.eye(m))-np.kron(np.eye(m),H.T));B=np.diag(rate)+A
  eye=np.eye(m).ravel();proj=np.outer(eye,eye)/m
  j=J.ravel();f=fa.ravel();gv=g.ravel();af=A@f;ag=A@gv
  maxpop=max(maxpop,float(np.max(np.abs(np.diag(af.reshape(m,m))))));naivepop=max(naivepop,float(np.max(np.abs(np.diag((A@f0.ravel()).reshape(m,m))))))
  x=np.linalg.solve(B+proj,j);pair=lambda a,b:float(np.vdot(a,b).real)
  kap=pair(j,x);lo=2*pair(j,f)-pair(f,rate*f)-pair(af,inv*af);up=pair(j-ag,inv*(j-ag))+pair(gv,rate*gv)
  r1=rate*f+ag-j;r2=rate*gv+af;gap=pair(r1,inv*r1)+pair(r2,inv*r2)
  assert lo<=kap+1e-9 and kap<=up+1e-9 and abs((up-lo)-gap)<1e-9
  total+=np.array([lo,kap,up,gap,up-lo])/(n*(1<<n))
 rec={'n':n,'per_site_normalized_trace_lower':float(total[0]),'response':float(total[1]),'upper':float(total[2]),'gap_identity_error':float(abs(total[3]-total[4])),'retargeted_population_defect':maxpop,'naive_population_defect':naivepop,'status':'NUMERICAL_DIAGNOSTIC_PASS'}
 records.append(rec);print(json.dumps(rec),flush=True)
(OUT/'RESPONSE_BOUND_CHECKS.json').write_text(json.dumps(records,indent=2)+'\n')
