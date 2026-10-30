import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigs
from joint_matrix import fall

def matrix(N,K,alpha):
 M=lil_matrix(((N+1)*(K+1),)*2,dtype=float)
 def idx(c,b):return c*(K+1)+b
 for c in range(N+1):
  a=N-c
  for b in range(K+1):
   i=idx(c,b)
   M[i,i]-=1+a*b+fall(a,3)*fall(b,4)
   if b+1<=K and a>=1:M[i,idx(c,b+1)]+=N**alpha
   if b+3<=K and a>=3:M[i,idx(c,b+3)]+=(a-2)*b*fall(N,2)**alpha
   if b>=4:M[i,idx(c,b-4)]+=fall(a+3,3)*fall(b,4)/(fall(N+3,3)**alpha)
   inc=(6*fall(c,3)+a*fall(c,2)+7*fall(a,2)*c)*fall(b,4)
   dec=(12*a*fall(c,2)+fall(a,2)*c+fall(a,3))*fall(b,4)
   M[i,i]-=inc+dec
   if c>=1:M[i,idx(c-1,b)]+=inc
   if c<N:M[i,idx(c+1,b)]+=dec
 return M.tocsc()
if __name__=='__main__':
 for K in [4,5,8]:
  for N in [10,20,40,80,160]:
   for alpha in [.05,.2,.5]:
    M=matrix(N,K,alpha)
    v=eigs(M,k=4,sigma=0,which='LM',return_eigenvectors=False,tol=1e-9)
    print(N,K,alpha,max(v.real),flush=True)
