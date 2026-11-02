import numpy as np
from scipy.linalg import expm, logm, eigh
from scipy.integrate import quad_vec
I=np.eye(2); X=np.array([[0,1],[1,0]]); Z=np.diag([1.,-1.]); n=3

def op(items):
 a=np.array([[1.]])
 for j in range(n): a=np.kron(a,items.get(j,I))
 return a
H=0.7*(op({0:Z,1:Z})+op({1:Z,2:Z}))+0.11*op({0:X})+0.07*op({1:X,2:X})
G=expm(-1.3*H); G/=np.trace(G)
Ps=[op({j:X}) for j in range(n)]; rates=np.array([.002,.0025,.0015]); ts=-np.log(1-2*rates)/2

def sigma(u):
 a=G.copy()
 for P,t in zip(Ps,ts):
  r=np.exp(2*u*t); a=(1+r)*a/2+(1-r)*(P@a@P)/2
 return a
u=.4; S=sigma(u); K=-logm(S); vals,U=eigh(K); B=0*K
for t,P in zip(ts,Ps):
 T=expm(K/2)@P@expm(-K/2); B+=t*(np.eye(2**n)-T@T.conj().T)
w=vals[:,None]-vals[None,:]; f=np.ones_like(w); nz=np.abs(w)>1e-10; f[nz]=w[nz]/(2*np.sinh(w[nz]/2)); rhs=-U@(f*(U.conj().T@B@U))@U.conj().T
h=1e-5; fd=(-logm(sigma(u+h))+logm(sigma(u-h)))/(2*h)
integral,err=quad_vec(lambda s: (np.pi/2)/np.cosh(np.pi*s)**2*expm(1j*s*K)@B@expm(-1j*s*K),-8,8,epsabs=1e-11)
print('minimum preimage eigenvalue',np.linalg.eigvalsh(sigma(1)).min())
print('Frechet versus finite difference operator norm',np.linalg.norm(rhs-fd,2))
print('kernel integral versus spectral f operator norm',np.linalg.norm(-integral-rhs,2))
print('quadrature error estimate',err)
