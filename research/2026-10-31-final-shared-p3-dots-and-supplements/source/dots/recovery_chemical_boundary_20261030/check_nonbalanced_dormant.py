import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla, json, math
from pathlib import Path
out=[]
for n in [8,16,32,64]:
 states=[(a,n-a-d,d) for d in range(1,n+1) for a in range(n-d+1)]
 # Positive d inactive state occurs only at n=d=1, absent here.
 ix={x:i for i,x in enumerate(states)}; rows=[];cols=[];data=[]
 rhs=np.zeros((len(states),4))
 for x,i in ix.items():
  a,c,d=x; A=a+2; rates=[(a*(a-1),(-1,0,1)),(a*d,(1,0,-1)),(a*d,(-1,1,0)),(c*d,(1,-1,0)),(a*(a-1),(-2,0,2)),(d*(d-1),(1,0,-1))]
  kill=a*(a-1); total=kill
  # columns: dormant probability, inverse-A dormant reward s=2, all-exit s=2, physical time normalized by (B)_q without connector stopping
  if kill: rhs[i,2]+=kill*(1+a-2)**-2
  rhs[i,3]=1/(A*(A-1))
  for rate,delta in rates:
   if rate==0:continue
   y=tuple(xx+dd for xx,dd in zip(x,delta));total+=rate
   if y[2]==0:
    rhs[i,0]+=rate;rhs[i,1]+=rate*(1+y[0]+2)**-2;rhs[i,2]+=rate*(1+y[0]+2)**-2
   else: rows.append(i);cols.append(ix[y]);data.append(-rate)
  rows.append(i);cols.append(i);data.append(total)
 Q=sp.csr_matrix((data,(rows,cols)),shape=(len(states),len(states)))
 sol=sla.spsolve(Q,rhs)
 f=np.array([(1+a+2)**-2 for a,c,d in states]);fm=np.array([(1+a+2)**-4 for a,c,d in states]);fp=np.array([(1+a+2)**-3 for a,c,d in states]);
 out.append(dict(n=n,states=len(states),dormant_prob_max=float(sol[:,0].max()),profile_ratio_max=float((sol[:,2]/f).max()),power_gain_ratio_max=float((sol[:,1]/fp).max()),physical_time_ratio_max=float((sol[:,3]/fm).max()),residual_max=float(np.max(np.abs(Q@sol-rhs)))))
# Rank of full stoichiometric changes in (A,C,D,B)
changes=np.array([[-1,0,1,0],[1,0,-1,0],[-1,1,0,0],[1,-1,0,0],[-2,0,2,0],[1,0,-1,0],[1,0,0,1],[3,0,0,4],[-4,0,0,-5]])
result={'unit_rates':True,'a0':2,'m':4,'q':5,'rank':int(np.linalg.matrix_rank(changes)),'complexes':6,'linkage_classes':1,'deficiency':6-1-int(np.linalg.matrix_rank(changes)),'operational_positive_D_stopped_tests':out,'scope':'Finite-shell falsification, not proof, full-network recurrence, or historical novelty.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
