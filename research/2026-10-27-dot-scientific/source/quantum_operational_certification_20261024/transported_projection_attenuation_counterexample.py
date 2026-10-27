"""Small target weight does not imply a stationary-style relative population bound for transported effects."""
import numpy as np
from scipy.linalg import expm
h=.1;d=3
X=np.array([[0,1,0],[1,0,0],[0,0,0.]])
Q=np.diag([1.,1.,0]);Xc=np.array([[0.,1.],[1.,0.]])
Pi=(np.kron(np.eye(2),Q)+np.kron(Xc,X))/2
cp=np.array([1.,1.])/np.sqrt(2);dm=np.array([1.,-1.,0.])/np.sqrt(2)
v=np.kron(cp,dm)
C=np.diag([0.,1.])
for p in [1e-3,1e-5,1e-7,1e-9]:
 sigma=np.diag([2*p,3*p,1-5*p]);rho=np.diag([p,p,1-2*p]);H=4*sigma-6*rho
 # Pi is obtained from I_control tensor |+><+| by a controlled H evolution and known control gates.
 # Its weighted partial trace is exactly(5p/2)I_control.
 W=2.5*p
 U=expm(-1j*h*np.kron(C,sigma));vin=U.conj().T@v
 R=np.outer(vin,vin.conj())
 K=np.eye(2*d)+(np.cos(h)-1)*np.kron(C,np.eye(d))-1j*np.sin(h)*np.kron(C,sigma)
 out=K@R@K.conj().T
 block=R[d:,d:];res=sigma*np.trace(block)-sigma@block@sigma
 out[d:,d:]+=np.sin(h)**2*res
 actual=np.trace(Pi@out).real;ideal=np.vdot(v,Pi@v).real
 assert abs(ideal)<1e-12
 print(f'p={p:.0e} w={W:.2g} actual={actual:.12g} ratio_to_h2w={actual/(h*h*W):.6g}')
print('Nonzero p->0 floor:',(1-np.cos(h))**2/4,'=O(h^4), not O(h^2 w).')
def collision(R,s,angle):
 K=np.eye(2*d)+(np.cos(angle)-1)*np.kron(C,np.eye(d))-1j*np.sin(angle)*np.kron(C,s)
 out=K@R@K.conj().T;b=R[d:,d:]
 out[d:,d:]+=np.sin(angle)**2*(s*np.trace(b)-s@b@s)
 return out
delta=.01
for p in [1e-5,1e-7,1e-9]:
 sigma=np.diag([2*p,3*p,1-5*p]);rho=np.diag([p,p,1-2*p]);H=4*sigma-6*rho
 U=expm(-1j*delta*np.kron(C,H));vin=U.conj().T@v;R=np.outer(vin,vin.conj())
 out=collision(collision(R,sigma,4*delta),rho,-6*delta)
 actual=np.trace(Pi@out).real
 print(f'PAIRED p={p:.0e} actual={actual:.12g} ratio_to_delta2w={actual/(delta**2*2.5*p):.6g}')
print('Paired p->0 floor:',(1-np.cos(4*delta)*np.cos(6*delta))**2/4)
cm=np.array([1.,-1.])/np.sqrt(2);dp=np.array([1.,1.,0.])/np.sqrt(2)
for p in [1e-2,1e-3,1e-4,1e-5]:
 delta=p
 sigma=np.diag([2*p,3*p,1-5*p]);rho=np.diag([p,p,1-2*p]);H=4*sigma-6*rho
 vnear=np.kron(np.sqrt(p)*cp+np.sqrt(1-p)*cm,dp)
 U=expm(-1j*delta*np.kron(C,H));vin=U.conj().T@vnear;R=np.outer(vin,vin.conj())
 out=collision(collision(R,sigma,4*delta),rho,-6*delta)
 actual=np.trace(Pi@out).real;ideal=np.vdot(vnear,Pi@vnear).real
 print(f'LINKED delta=p={p:.0e} excess={actual-ideal:.12g} excess/[delta2(r+w)]={(actual-ideal)/(delta**2*(ideal+2.5*p)):.6g}')
