"""Physical principal-angle spectrum replay for flat logical rank k>=3."""
import numpy as np
rng=np.random.default_rng(261026120)
def unit(n):return np.linalg.qr(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))[0]
def f(a):
 e=np.linalg.eigvalsh((a+a.conj().T)/2);assert e.min()>-1e-11
 e=e[e>1e-14];return np.dot(e,np.log(e))
def eig2(S,P):
 z=np.sqrt(max(S*S-4*P,0));return [(S-z)/2,(S+z)/2]
maxerr=0.;count=0
for k in [3,4,7]:
 for rep in range(8):
  p=rng.uniform(.05,.95);q=1-p;theta=rng.uniform(.05,.95);ls=rng.dirichlet(np.ones(3))
  gm=np.zeros((3,k),complex);gm[:,:3]=np.diag(np.sqrt(ls));gm=unit(3)@gm@unit(k).T
  n=3*k+1;flag=np.r_[np.sqrt(theta)*gm.reshape(-1),np.sqrt(1-theta)]
  pm=np.zeros((3*n,3*n),complex)
  for l in range(k):
   vec=np.zeros((3,n),complex)
   for i in range(3):vec[i,k*i+l]=1/np.sqrt(3)
   vec=vec.reshape(-1);pm+=np.outer(vec,vec.conj())
  A=p*pm/k+q*np.kron(np.eye(3),np.outer(flag,flag.conj()))/3
  ar=A.reshape(3,n,3,n);R=np.einsum('aiaj->ij',ar);L=np.kron(np.eye(3),R)-ar.transpose(2,1,0,3).reshape(3*n,3*n)
  c=p*q/(9*k);ai=p/k+q/3;ao=2*p/(3*k);so=ao+2*q/3;r=p/(3*k)
  targets=[sum((eig2(ai,c*(3-theta*l)) for l in ls),[])+[p/k]*(k-3),sum((eig2(so,2*c*(2-theta+theta*l)) for l in ls),[])+[ao]*(3*k-3),eig2(r+q,r*q*(1-theta))+[r]*(3*k-1)]
  for matrix,es in zip([A,L,R],targets):
   expected=np.sort(np.r_[es,np.zeros(matrix.shape[0]-len(es))]);error=np.max(abs(np.linalg.eigvalsh(matrix)-expected));maxerr=max(maxerr,error);assert error<2e-12
  delta=f(A)+f(R)-f(L)+np.log(4/3)
  tau=q+p/k
  assert delta>=p*p*q*theta/(36*k*k*tau*tau)-1e-12
  count+=1
print({'status':'PASS','cases':count,'logical_ranks':[3,4,7],'maximum_spectral_error':maxerr})
