import numpy as np
from itertools import product
for m in range(1,9):
 eps=1/m**2
 minratio=1e9; err=0
 for ss in product((0,1),repeat=m):
  # y = alpha + coeff @ x
  alpha=1.; coeff=np.zeros(m); A=eps*np.eye(m); beta=np.zeros(m)
  for i,s in enumerate(ss):
   A[i,:]-=eps*coeff
   beta[i]=eps*alpha
   if s==0: alpha=0.;coeff=np.eye(m)[i]
   else: coeff=coeff-np.eye(m)[i]
  mineig=np.linalg.eigvalsh((A+A.T)/2)[0]
  minratio=min(minratio,mineig/(eps/(2*m*m)))
  u=np.random.default_rng(sum((i+1)*s for i,s in enumerate(ss))+m).random(m)
  f=alpha+coeff@np.linalg.solve(A+np.diag(u),beta)
  exact=np.prod([u[i]/(eps+u[i]) if s else eps/(eps+u[i]) for i,s in enumerate(ss)])
  err=max(err,abs(f-exact))
 print(m,'min eig / bound',minratio,'max transfer error',err)
