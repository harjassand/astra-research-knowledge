import json
import numpy as np
from scipy.linalg import eig,expm
from math import sqrt,log

def A(k):return np.array([[0,-1j*k*sqrt(2/3),0],[-1j*k*sqrt(2/3),0,-1j*k/sqrt(3)],[0,-1j*k/sqrt(3),-2]],complex)
def B(h):
 r,j,z=h
 return sqrt(6)*(j*j/2-sqrt(2)*r*z+z*z/2)
rows=[]
for k in [1,.3,.1,.03,.01,.003]:
 l,V=eig(A(k));i=np.argmin(l.imag);lam=l[i];r=V[:,i]/V[0,i]
 t=6*log(2)/k**2
 forcing=np.array([0,0,B(r)])
 second=(np.exp(2*lam*t)*np.eye(3)-expm(A(2*k)*t))@np.linalg.solve(2*lam*np.eye(3)-A(2*k),forcing)
 rows.append({'k':k,'t':t,'second_order_norm':float(np.linalg.norm(second)),'k_times_second_order_norm':float(k*np.linalg.norm(second)),'first_mode_norm':float(np.exp(lam.real*t)*np.linalg.norm(r))})
print(json.dumps(rows,indent=2))
