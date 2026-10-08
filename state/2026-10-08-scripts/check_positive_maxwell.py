from math import sqrt,log,pi,exp,erf
import numpy as np
from scipy.linalg import expm
from scipy.special import gammaln

def D(N,nu,c):
 s=c*log(N)/sqrt(N); ans=0
 for M in range(N%2,N+1,2):
  if M==0:continue
  k=np.arange(M+1); dn=(nu+1)*k*(M-k+1);up=nu*(M-k)*(k+1)
  Q=np.diag(-(dn+up))
  for i in range(M):Q[i+1,i]=up[i];Q[i,i+1]=dn[i+1]
  p=expm(s*Q)@(np.ones(M+1)/(M+1))
  q=nu/(nu+1);pp=q**k;pp/=pp.sum()
  d=np.abs(p-pp).sum()/2
  h=(N-M)//2
  w=(M+1)**2/(N/2+M/2+1)*np.exp(gammaln(N+1)-gammaln(h+1)-gammaln(N-h+1)-N*np.log(2))
  ans+=w*d
 return ans
for nu in [.2,1.]:
 for c in [.2,.5,1.,2.]:
  x=1/(2*c); lim=erf(x/sqrt(2))-sqrt(2/pi)*x*exp(-x*x/2)
  vals=[D(N,nu,c) for N in [16,32,64,96]]
  print(f'nu={nu} c={c} Maxwell={lim:.7f} finite N[16,32,64,96]={list(map(lambda z: round(z,7),vals))}',flush=True)
