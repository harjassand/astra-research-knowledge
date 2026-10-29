import numpy as np,json
from scipy.integrate import quad
rng=np.random.default_rng(202610291302);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);mx=0;rotres=0;petzres=0;count=0
S=lambda a:-sum(v*np.log(v) for v in np.linalg.eigvalsh(a) if v>1e-14)
T=lambda a,b:.5*sum(abs(np.linalg.eigvalsh(a-b)))
for gamma in [.5,.6,.8,.95,.999]:
 eta=1-gamma;sigma=np.array([eta,1])/(1+eta);K=[X@np.diag([1,np.sqrt(eta)]),X@np.array([[0,np.sqrt(gamma)],[0,0]])];F=lambda a:sum(k@a@k.conj().T for k in K)
 for k in K:petzres=max(petzres,np.linalg.norm(np.diag(np.sqrt(sigma))@k.conj().T@np.diag(1/np.sqrt(sigma))-k))
 e01=np.array([[0,1],[0,0]],complex)
 for t in [-2,-.7,0,1.3]:
  u=np.diag(np.exp(.5j*t*np.log(sigma)));R=[u@k@u.conj().T for k in K];out=sum(r@F(e01)@r.conj().T for r in R);rotres=max(rotres,np.linalg.norm(out-eta*np.exp(1j*t*np.log(eta))*e01))
 kap=quad(lambda t:np.pi/(2*(np.cosh(np.pi*t)+1))*np.cos(t*np.log(eta)),-30,30,epsabs=1e-13)[0]
 for d in [1,2,4]:
  A=[np.kron(k,np.eye(d)) for k in K];zz=np.kron(Z,np.eye(d));ls=np.kron(np.diag(np.log(sigma)),np.eye(d))
  for _ in range(100):
   g=rng.normal(size=(2*d,2*d))+1j*rng.normal(size=(2*d,2*d));rho=g@g.conj().T;rho/=np.trace(rho);out=sum(k@rho@k.conj().T for k in A);L=S(out)-S(rho)+np.trace((out-rho)@ls).real;deph=(rho+zz@rho@zz)/2;distance=T(rho,deph);ratio=distance*gamma/np.sqrt(max(L,1e-30));mx=max(mx,ratio);count+=1;assert ratio<=1+1e-10
out={'count':count,'max_distance_gamma_over_sqrt_loss':mx,'max_rotated_map_residual':rotres,'max_petz_Kraus_residual':petzres,'scope':'floating diagnostic, not proof or interval certificate'}
print(out);open('CHECKS.json','w').write(json.dumps(out,indent=2)+'\n')
