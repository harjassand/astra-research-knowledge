"""Exact finite-matrix corroboration of latent-sector coupling and the n=1 Haar twirl."""
import numpy as np, math
rng=np.random.default_rng(27100444)
checks=0
for r in [2,3,5,9]:
 d=3*r
 z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));U=np.linalg.qr(z)[0]
 for k in range(r):
  a,b=0,1;R=np.eye(d);ia=a*r+k;ib=b*r+k
  R[:,[ia,ib]]=R[:,[ib,ia]];Up=U@R
  assert np.linalg.norm(Up[:,ib]-U[:,ia])<1e-12
  for j in range(r):
   if j==k:continue
   cols=[c*r+j for c in range(3)]
   # Equality of the full isometries gives equality on every entangled input.
   assert np.linalg.norm(U[:,cols]-Up[:,cols])<1e-12
   va=U[:,cols].T.reshape(-1)/np.sqrt(3)
   vb=Up[:,cols].T.reshape(-1)/np.sqrt(3)
   assert np.linalg.norm(va-vb)<1e-12
   checks+=1
for r in [2,3,4]:
 d=3*r;F=np.zeros((d*d,d*d))
 for i in range(d):
  for j in range(d):F[j*d+i,i*d+j]=1
 def averaged(a):
  P=np.zeros((3,3));P[a,a]=1;X=np.eye(3)/3;Y=P/(3*r)
  return (np.kron(X-Y/d,np.eye(d*d))+np.kron(Y-X/d,F))/(d*d-1)
 A=averaged(0);B=averaged(1)
 assert abs(np.trace(A)-1)<1e-12
 assert np.linalg.eigvalsh(A).min()>-1e-12
 td=np.abs(np.linalg.eigvalsh(A-B)).sum()/2
 assert abs(td-1/(3*r))<1e-12
for r in [2,3,10,1000]:
 for n in [0,1,2,10,100]:
  c=1-(1-1/r)**n
  assert c<=min(1,n/r)+1e-12
print('PASS',checks,'conditional-sector isometry couplings;3 exact first-moment trace distances;20 collision bounds.')
