import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np,itertools,json
from pathlib import Path
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1])
ps=[np.kron(A,B)for A in [I,X,Y,Z]for B in [I,X,Y,Z]][1:]
labels=[a+b for a in ['I','X','Y','Z']for b in ['I','X','Y','Z']][1:]
ant=np.array([[np.linalg.norm(A@B+B@A)<1e-8 for B in ps]for A in ps])
records=[];seen=[]
for ss in itertools.combinations(range(15),5):
 g=ant[np.ix_(ss,ss)]
 if np.all(g.sum(axis=0)==2):
  # A two-regular graph on five vertices is a five-cycle.
  seen.append(ss)
  if len(seen)>=8:break
ks=[np.kron(G.T,np.kron(G,np.eye(4))+np.kron(np.eye(4),G))for G in ps]
for ss in seen:
 K=sum(ks[i]for i in ss);e,u=np.linalg.eigh(K);v=u[:,e>e[-1]-1e-9];rho=v@v.conj().T/v.shape[1]
 lam=[float(np.trace(rho@k).real/2)for k in ks]
 records.append({'subset':[labels[i]for i in ss],'starmax':float(e[-1]),'positive_HS':min(lam)>-1e-8,'lambda_min':min(lam),'lambda_all':dict(zip(labels,lam)),'c2_slack_using_theta_upper':float(5+np.sqrt(5)-e[-1]),'c2_slack_if_Ceq2':float(7-e[-1]),'top_multiplicity':v.shape[1]})
Path(__file__).with_suffix('.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(records,indent=2))
