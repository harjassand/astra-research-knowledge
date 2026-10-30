import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigs
from scipy.linalg import eigvals

def fall(n,k):
 z=1
 for j in range(k): z*=max(n-j,0)
 return z

def matrix(N,K,alpha):
 size=(N+1)*(K+1);M=lil_matrix((size,size),dtype=float)
 def idx(c,b):return c*(K+1)+b
 for c in range(N+1):
  a=N-c
  for b in range(K+1):
   i=idx(c,b)
   # (deltaC,deltaB,deltaN,rate)
   edges=[(0,1,1,1),(0,3,2,a*b),(0,-4,-3,fall(a,3)*fall(b,4))]
   # A increases/C decreases:6 C3 + A C2 +7 A2 C
   inc=(6*fall(c,3)+a*fall(c,2)+7*fall(a,2)*c)*fall(b,4)
   dec=(12*a*fall(c,2)+fall(a,2)*c+fall(a,3))*fall(b,4)
   edges +=[(-1,0,0,inc),(1,0,0,dec)]
   for dc,db,dn,rate in edges:
    if not rate:continue
    M[i,i]-=rate
    cc,bb=c+dc,b+db
    if 0<=cc<=N and 0<=bb<=K:M[i,idx(cc,bb)]+=rate*N**(alpha*dn)
 return M.tocsc()
if __name__=='__main__':
 for K in [4,5,8]:
  for N in [10,20,40,80]:
   for alpha in [.05,.2,.5]:
    M=matrix(N,K,alpha)
    # shift-invert around zero targets slow spectral modes
    try:
     vals=eigs(M,k=4,sigma=0,which='LM',return_eigenvectors=False,tol=1e-9)
     value=max(vals.real)
     print(N,K,alpha,value,flush=True)
    except Exception as e:print('ERROR',N,K,alpha,str(e),flush=True)
