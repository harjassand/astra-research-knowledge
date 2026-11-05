import numpy as np, json
p=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
phi=np.array([1,0,0,1])/np.sqrt(2); Phi=np.outer(phi,phi)
def swap(n,i,j):
 d=2**n; inds=np.arange(d);f=((inds>>(n-1-i))^(inds>>(n-1-j)))&1; pp=inds^(f<<(n-1-i))^(f<<(n-1-j)); return np.eye(d)[pp]
I4=np.eye(4); I2=np.eye(2); J=np.kron(I4,phi.reshape(4,1)); Oef=1j*(np.kron(p[3],I2)@Phi-Phi@np.kron(p[3],I2)); O=np.kron(I4,Oef)
ZSmZMt=np.kron(p[3],I2)-np.kron(I2,p[3].T)
for theta in [.1,.03,.01,.003,.001]:
 c=np.cos(theta);s=np.sin(theta);D=1+3*s*s
 K=(c*I4-2j*s*Phi)/np.sqrt(D);L=2*s*(I4-Phi)/np.sqrt(D)
 U=c*np.eye(16)+1j*s*swap(4,0,2)
 KK=np.kron(np.kron(I2,K),I2);LL=np.kron(np.kron(I2,L),I2)
 A=J.conj().T@U.conj().T@(KK.conj().T@O@KK+LL.conj().T@O@LL)@U@J
 e1=np.linalg.norm(A-theta*ZSmZMt,2); dep=0
 t=(1+s*s)/D
 for X in p:
  out=(K@np.kron(I2/2,X)@K.conj().T+L@np.kron(I2/2,X)@L.conj().T).reshape(2,2,2,2)
  out=np.einsum('aiaj->ij',out)
  dep=max(dep,np.linalg.norm(out-t*X-(1-t)*np.trace(X)*I2/2))
 print(json.dumps(dict(theta=theta,remainder_over_theta2=e1/theta**2,effect_norm_over_theta=np.linalg.norm(A,2)/theta,depolarizing_residual=dep,lambda_value=(s*np.sqrt(2+3*s*s)+s*s)/D)))
