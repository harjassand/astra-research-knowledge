import numpy as np,json
from pathlib import Path
out=Path(__file__).parent
N=1
ns=np.arange(-N,N+1);D=len(ns)
def matrix(S):
 theta=2*np.pi*np.arange(S)/S
 # exact integer-grid floor decisions; equality follows the chosen half-open convention
 k=np.arange(S); diff=(k[:,None]-k[None,:])%S
 jump=np.where(2*diff<S,1.,-1.)
 a=.3*np.sin(theta[:,None])+.4*np.cos(theta[None,:])+.2*jump
 b=.25*np.sin(theta)
 A=np.empty((S,S,2,2),complex)
 A[:,:,0,0]=np.cos(a)*np.exp(1j*b)[None,:]
 A[:,:,1,1]=np.cos(a)*np.exp(-1j*b)[None,:]
 A[:,:,0,1]=1j*np.sin(a)*np.exp(-1j*b)[None,:]
 A[:,:,1,0]=1j*np.sin(a)*np.exp(1j*b)[None,:]
 C=np.einsum('nt,tsab->snab',np.exp(-1j*ns[:,None]*theta[None,:]),A)/S
 C=C.reshape(S,D*2,2)
 K=C@C.conj().transpose(0,2,1)
 ans=np.empty((D,D*2,D,D*2),complex)
 for i,n in enumerate(ns):
  for j,m in enumerate(ns):
   ans[i,:,j,:]=np.einsum('s,sab->ab',np.exp(1j*(m-n)*theta),K)/S
 return ans.reshape(D*D*2,D*D*2)
ref=matrix(2048)
errs={str(s):float(np.linalg.norm(matrix(s)-ref,2)) for s in [16,32,64,128,256,512]}
rng=np.random.default_rng(71)
q=np.array([n+f for n in ns for f in [0,1]])
z=rng.normal(size=(len(q),len(q)))+1j*rng.normal(size=(len(q),len(q)))
z=(z+z.conj().T)/2
pin=z*(q[:,None]==q[None,:])
M=16
avg=sum(np.exp(2j*np.pi*j*(q[:,None]-q[None,:])/M)*z for j in range(M))/M
result={'N':N,'two_rotor_reset_operator_errors_vs_S2048':errs,'exact_charge_mask_commutator':float(np.linalg.norm(q[:,None]*pin-pin*q[None,:])),'charge_copy_equals_discrete_twirl':float(np.linalg.norm(pin-avg)),'note':'Small operator-norm validation, not astronomical Wilson compilation. Dense matrices used only in this test.'}
(out/'polynomial_grid_compiler_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
