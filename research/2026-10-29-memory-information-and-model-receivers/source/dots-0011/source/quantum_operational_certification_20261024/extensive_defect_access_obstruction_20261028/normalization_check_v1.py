import numpy as np,json
out=[]
for N in [2,4,8,16,32]:
 K=2;d=N*K
 F=[np.kron(np.diag([float(j==i) for j in range(N)]),np.eye(K))*np.sqrt(N) for i in range(N)]
 B=np.concatenate(F,axis=1)
 C=np.kron(np.ones((N,1))/np.sqrt(N),np.eye(K))
 W=np.concatenate([f@C for f in F],axis=1)
 out.append(dict(N=N,K=K,full_norm=float(np.linalg.norm(B,2)),encoded_norm=float(np.linalg.norm(W,2)),encoded_isometry_error=float(np.linalg.norm(W.T@W-np.eye(d))),row_identity_error=float(np.linalg.norm(B@B.T-N*np.eye(d)))))
print(json.dumps(out,indent=2))
