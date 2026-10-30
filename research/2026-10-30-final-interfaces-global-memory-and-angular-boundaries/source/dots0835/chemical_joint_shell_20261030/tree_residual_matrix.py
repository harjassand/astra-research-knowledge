import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigs
from joint_matrix import fall

HEIGHTS={4:[0,1,1,1,3],8:[0,1,2,3,3,4,5,5,6],12:[0,1,2,3,3,4,5,5,6,7,7,8,9]}
def matrix(R,K,alpha,eta=0):
 height=lambda b:HEIGHTS[K][b]
 states=[(c,b) for b in range(K+1) for c in range(R+height(b)+1)]
 ix={x:i for i,x in enumerate(states)};M=lil_matrix((len(states),)*2,dtype=float)
 for (c,b),i in ix.items():
  n=R+height(b);a=n-c
  inc=(6*fall(c,3)+a*fall(c,2)+7*fall(a,2)*c)*fall(b,4)
  dec=(12*a*fall(c,2)+fall(a,2)*c+fall(a,3))*fall(b,4)
  edges=[(c,b+1,1,1),(c,b+3,2,a*b),(c,b-4,-3,fall(a,3)*fall(b,4)),(c-1,b,0,inc),(c+1,b,0,dec)]
  for cc,bb,dn,rate in edges:
   if not rate:continue
   M[i,i]-=rate
   if (cc,bb) in ix:
    dr=dn-height(bb)+height(b)
    M[i,ix[(cc,bb)]]+=rate*R**(alpha*dr)*np.exp(eta*abs(dr))
 return M.tocsc()
if __name__=='__main__':
 for K in [4,8,12]:
  for R in [20,40,80,160]:
   for eta in [0,.01,.1]:
    M=matrix(R,K,.2,eta)
    vals=eigs(M,k=4,sigma=0,which='LM',return_eigenvectors=False,tol=1e-9)
    print(R,K,eta,max(vals.real),flush=True)
