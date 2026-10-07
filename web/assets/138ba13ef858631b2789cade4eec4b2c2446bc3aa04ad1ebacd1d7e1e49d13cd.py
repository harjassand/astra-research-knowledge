import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np,json
from pathlib import Path
X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex);I=np.eye(2)
gs=[np.kron(X,I),np.kron(Y,I),np.kron(Z,X),np.kron(Z,Y),np.kron(Z,Z)]
d=4
K=sum(np.kron(G.T,np.kron(G,np.eye(d))+np.kron(np.eye(d),G)) for G in gs)
ev,u=np.linalg.eigh(K)
w=u[:,ev>ev[-1]-1e-9];rho=w@w.conj().T/w.shape[1]
lambdab=ev[-1]/10
# A: the ten Hermitian bivectors, normalized to G^2=I.
as_=[1j*gs[i]@gs[j] for i in range(5) for j in range(i+1,5)]
KA=sum(np.kron(G.T,np.kron(G,np.eye(d))+np.kron(np.eye(d),G)) for G in as_)
lambdaa=np.trace(rho@KA).real/20
# partial marginal R and B to ensure bistochastic and covariance, positivity
choi=np.trace(rho.reshape(d,d,d,d,d,d),axis1=2,axis2=5).reshape(d*d,d*d)
mr=np.trace(choi.reshape(d,d,d,d),axis1=1,axis2=3)
mb=np.trace(choi.reshape(d,d,d,d),axis1=0,axis2=2)
r=dict(Kmax=float(ev[-1]),multiplicity=w.shape[1],lambda_clifford=float(lambdab),lambda_bivector=float(lambdaa),positive=bool(lambdab>=0 and lambdaa>=0),R_marginal_residual=float(np.linalg.norm(mr-np.eye(d)/d)),B_marginal_residual=float(np.linalg.norm(mb-np.eye(d)/d)),c_required_clifford=float((1-.2)/(1-lambdab)),eigenvalues=[float(x) for x in sorted(set(np.round(ev,9)))])
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps(r,indent=2))
