"""Finite actual collision circuits: coherent reset interpolation and global parity.
This d=2 analogue corroborates dimension-independent algebra, not the theorem.
"""
import numpy as np
rng=np.random.default_rng(25127)
def randstate(n):
 a=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));a=a@a.conj().T;return a/np.trace(a)
def norm1(a):return np.linalg.svd(a,compute_uv=False).sum()
d=2;B=3;D=d*B;R=2;p=.23;q=1-p
P=np.diag([1.,1.,0.]);Q=np.kron(np.eye(d),P)
phi=np.zeros(D,complex)
for i in range(d):phi[i*B+i]=1/np.sqrt(d)
Phi=np.outer(phi,phi.conj());I=np.eye(D*R)
plus=np.ones((2,2))/2
bell=np.eye(d).reshape(d*d)/np.sqrt(d);bell=np.outer(bell,bell.conj())
Hc=np.array([[1,1],[1,-1]],complex)/np.sqrt(2)

def collision(a,sigma,h):
 blocks=a.reshape(2,D*R,2,D*R).transpose(0,2,1,3)
 out=np.zeros_like(blocks);c=np.cos(h);s=np.sin(h);sig=np.kron(sigma,np.eye(R))
 aa=blocks[1,1].reshape(D,R,D,R)
 red=np.trace(aa,axis1=0,axis2=2)
 out[0,0]=blocks[0,0]
 out[1,1]=c*c*blocks[1,1]+s*s*np.kron(sigma,red)+1j*c*s*(sig@blocks[1,1]-blocks[1,1]@sig)
 out[0,1]=c*blocks[0,1]-1j*s*blocks[0,1]@sig
 out[1,0]=c*blocks[1,0]+1j*s*sig@blocks[1,0]
 return out.transpose(0,2,1,3).reshape(2*D*R,2*D*R)

for rep in range(12):
 tau=randstate(B);taud=P@tau@P+(np.eye(B)-P)@tau@(np.eye(B)-P);tauo=tau-taud
 dn=q*norm1(tauo);beta=q*np.trace(P@tau).real
 assert dn*dn<=4*beta+1e-12
 rho=randstate(d);enc=np.zeros((B,B),complex);enc[:d,:d]=rho
 angles=[.13,.07,-.11];H=sum(h*h for h in angles)
 def programs(z):
  tz=taud+z*tauo
  omega=np.kron(np.eye(d)/d,p*P/d+q*tz)
  J=p*Phi+q*np.kron(np.eye(d)/d,tz)
  return (J+d*omega)/(d+1),omega
 def full(z):
  data=p*enc+q*(taud+z*tauo)
  a=np.kron(bell,data).reshape(d,d,B,d,d,B).transpose(1,2,0,4,5,3).reshape(D*R,D*R)
  a=np.kron(plus,a);T,omega=programs(z)
  for h in angles:
   a=collision(a,T,h);a=collision(a,omega,-h)
   gate=np.kron(Hc,I);a=gate@a@gate.conj().T
  aa=a.reshape(2,D*R,2,D*R)
  accepted=(aa[0,:,0,:]+aa[0,:,1,:]+aa[1,:,0,:]+aa[1,:,1,:])/2
  logical=np.trace(accepted.reshape(D,R,D,R),axis1=0,axis2=2)
  out=np.zeros((R+1,R+1),complex);out[:R,:R]=logical;out[R,R]=1-np.trace(logical)
  return out
 assert norm1(full(1)-full(-1))<1e-12
 assert norm1(full(1)-full(0))<=(16*H+72*H*H)*dn*dn+1e-12
 a=randstate(2*D*R);h=.17;dz=1e-3
 def pair(z):
  T,o=programs(z);return collision(collision(a,T,h),o,-h)
 first=(pair(dz)-pair(-dz))/(2*dz)
 second=(pair(dz)-2*pair(0)+pair(-dz))/(dz*dz)
 assert norm1(first)<=12*h*h*dn+1e-9
 assert norm1(second)<=8*h*h*dn*dn+1e-8
print('PASS12 coherent-reset circuits: global parity, quadratic Taylor charge, and signed-pair derivative bounds.')
