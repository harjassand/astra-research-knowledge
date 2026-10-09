import numpy as np
from scipy.optimize import minimize

def S(r):
 e=np.linalg.eigvalsh(r); e=e[e>1e-14];return -np.sum(e*np.log2(e))
def h(x):
 return -(x*np.log2(max(x,1e-300))+(1-x)*np.log2(max(1-x,1e-300)))
def obj(v,d=2):
 z=v[:2*d*d]+1j*v[2*d*d:]; z=z.reshape(2,d,d); z/=np.linalg.norm(z,axis=(1,2))[:,None,None]
 p=0.5; b=np.array([t@t.conj().T for t in z]);e=np.array([t.T@t.conj() for t in z]);
 c=abs(np.vdot(z[0],z[1])); chi=h((1+c)/2);acc=1-h((1-np.sqrt(max(0,1-c*c)))/2)
 return -(S(b.mean(0))+S(e.mean(0))-sum(S(t) for t in b)-chi-acc)
