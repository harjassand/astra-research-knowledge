import numpy as np
from itertools import product

def normalized_poisson(Q,reward):
 M=Q.copy();v=reward.copy();M[0,:]=0;M[0,0]=1;v[0]=0
 return np.linalg.solve(M,v)
count=0
for D in range(1,9):
 k=1.7
 for ratio in [.0001,.001,.01,1/(8*D),1/(4*D)]:
  r=ratio*k
  if ratio>1/(4*D):continue
  Q=np.zeros((D+1,D+1))
  for j in range(D+1):
   rate=r if j==0 else k;Q[j,j]=-rate;Q[j,(j+1)%(D+1)]=rate
  pi=np.array([k]+[r]*D)/(k+D*r)
  assert np.max(np.abs(pi@Q))<1e-12
  for q in range(1,D+1):
   A=.031;epB=.004
   h=np.zeros(D+1);h[q]=epB*k
   K=Q.copy();dest=(q+1)%(D+1);K[q,dest]=0
   t=np.linalg.solve(-K,A*np.ones(D+1)+h)
   exact=[]
   for j in range(D+1):
    if j==0: val=A*(1/r+q/k)+epB
    elif j<=q:val=A*(q-j+1)/k+epB
    else:val=A*((D-j+1)/k+1/r+q/k)+epB
    exact.append(val)
   assert np.allclose(t,exact)
   KD=Q[1:q+1,1:q+1].copy();reward=np.zeros(q);reward[-1]=k*t[dest]+epB*k
   xi=np.linalg.solve(-KD,reward)
   assert np.allclose(xi,A*(1/r+D/k)+2*epB)
   det=np.zeros(D+1);det[q]=1
   hd=normalized_poisson(Q,-det+pi[q])
   assert np.max(np.abs(Q@hd+det-pi[q]))<1e-9
   assert np.ptp(hd)<=2*D/k+1e-9
   count+=1
  Q2=np.kron(Q,np.eye(D+1))+np.kron(np.eye(D+1),Q)
  overlap=np.array([int(i>0 and j>0) for i,j in product(range(D+1),repeat=2)])
  f=D*r/(k+D*r)
  hp=normalized_poisson(Q2,-overlap+f*f)
  assert np.max(np.abs(Q2@hp+overlap-f*f))<1e-9
  assert np.ptp(hp)<=8*D/k+1e-9
print(f'PASS: {count} own-clock readout/return cases, plus pair and detector Poisson checks for D=1,...,8.')
print('Validated exact t, xi, product-clock stationarity, centered equations, and uniform height bounds.')
print('Does not test quantum collision algebra or malformed native-clock transitions.')
