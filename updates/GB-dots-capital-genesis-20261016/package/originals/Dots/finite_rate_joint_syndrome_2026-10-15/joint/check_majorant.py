import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np,json
from scipy.linalg import expm,block_diag
from pathlib import Path
rng=np.random.default_rng(213121);Z=np.diag([1.,-1.]);I=np.eye(2)
def rn(d):
 A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));return A/np.linalg.norm(A,2)
def rh(d):
 A=rn(d);A+=A.conj().T;return A/np.linalg.norm(A,2)
def epsilon(J,g,t):return J*J/g*(t+np.expm1(-2*g*t)/(2*g))
def qplus(J,g,t):
 a=np.sqrt(g*g+4*J*J);return (np.exp(-g*t)*(np.cosh(a*t)+g/a*np.sinh(a*t))-1)/2
best={'ratio_to_sharp_product':0}; max_majorant_ratio=0; max_formula_error=0
for k in range(2400):
 J=10**rng.uniform(-1.5,.1,2);g=10**rng.uniform(-.5,.5,2);t=10**rng.uniform(-1,.5);d=2;n=4*d
 H0=block_diag(*[3*rh(d) for _ in range(4)]);V=[np.zeros((n,n),complex) for _ in range(2)]
 for i in range(2):
  bit=2 if i==0 else 1
  for s in range(4):
   if s&bit:continue
   r=s^bit;A=J[i]*rn(d);V[i][s*d:(s+1)*d,r*d:(r+1)*d]=A;V[i][r*d:(r+1)*d,s*d:(s+1)*d]=A.conj().T
 H=H0+sum(V);S=[np.kron(np.kron(Z,I),I),np.kron(np.kron(I,Z),I)]
 L=1j*(np.kron(np.eye(n),H)-np.kron(H.T,np.eye(n)))+sum(g[i]*(np.kron(S[i].T,S[i])-np.eye(n*n)) for i in range(2))
 M=np.diag([0.]*(3*d)+[1.]*d);F=(expm(t*L)@M.reshape(-1,order='F')).reshape((n,n),order='F')[:d,:d];p=np.linalg.eigvalsh((F+F.conj().T)/2)[-1]
 epsprod=np.prod([epsilon(J[i],g[i],t) for i in range(2)]);qprod=np.prod([qplus(J[i],g[i],t) for i in range(2)])
 ratio=p/epsprod;max_majorant_ratio=max(max_majorant_ratio,p/qprod)
 assert p<=qprod+1e-12
 if ratio>best['ratio_to_sharp_product']:
  best={'ratio_to_sharp_product':float(ratio),'p':float(p),'epsilon_product':float(epsprod),'qplus_product':float(qprod),'J':J.tolist(),'gamma':g.tolist(),'t':float(t),'iteration':k}
  np.savez(Path(__file__).with_name('best_conditional.npz'),H0=H0,V1=V[0],V2=V[1],J=J,g=g,t=t)
 if ratio>1.000001:break
for J,g,t in [(.1,1.,.2),(.2,.8,2.),(1.,1.,.1)]:
 M=np.array([[0,J,J,0],[J,-2*g,0,J],[J,0,-2*g,J],[0,J,J,0]])
 actual=expm(M*t)[3,0];max_formula_error=max(max_formula_error,abs(actual-qplus(J,g,t)))
result={'conditional_edge_instances':k+1,'best':best,'max_majorant_ratio':float(max_majorant_ratio),'max_majorant_formula_error':float(max_formula_error)}
Path(__file__).with_name('majorant_checks.json').write_text(json.dumps(result,indent=2));print(result)
