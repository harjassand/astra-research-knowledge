"""Check transverse collective variance and its inverse-fifth-power macroscopic-time tail."""
import numpy as np
from math import sqrt,pi,exp
from scipy.integrate import quad
from scipy.linalg import expm
from scipy.special import gammaln
from macroscopic_polarization import mean_y

def kernel(z):
 if z<1e-4: return 1/6-z*z/60
 # integrate over u directly for numerical stability at z<35
 return quad(lambda u: (u*(1-u)*exp(z))/(u+(1-u)*exp(z))**2,0,1,epsabs=1e-12)[0]

def limiting(c):
 return quad(lambda x:sqrt(2/pi)*x**4*exp(-x*x/2)*kernel(c*x),0,12,epsabs=1e-10)[0]

C=4*pi**4/5*sqrt(2/pi)
print('predicted c^5 * limiting V(c) constant',C)
for c in [0,1,2,3,5,10,20]:
 val=limiting(c)
 print('c=',c,'Vlim=',val,'c^5 Vlim=',val*c**5)

def finite(N,nu,c):
 s=c/sqrt(N);ans=0
 for M in range(N%2,N+1,2):
  j=M/2;k=np.arange(M+1)
  dn=(nu+1)*k*(M-k+1);up=nu*(M-k)*(k+1)
  Q=np.diag(-(dn+up))
  for i in range(M):Q[i+1,i]=up[i];Q[i,i+1]=dn[i+1]
  p=expm(s*Q)@(np.ones(M+1)/(M+1))
  h=(N-M)//2
  w=(M+1)**2/(N/2+M/2+1)*np.exp(gammaln(N+1)-gammaln(h+1)-gammaln(N-h+1)-N*np.log(2))
  m=k-j;ans+=w*(j*(j+1)-(m*m)@p)/N
 return ans
for nu in [0,.2,1]:
 for c in [2,5,10]:
  arr=[finite(N,nu,c) for N in [16,32,64,96]]
  print('nu',nu,'c',c,'Vlim',limiting(c),'finite',arr,flush=True)
