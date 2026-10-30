"""Numerical falsification check only; proof is in RELATIVE_OCCUPATION_GAP.md."""
import numpy as np,json
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
out=[]
for N in [10,30,100,300,1000,3000]:
 a=np.arange(1,N+1,dtype=float);c=N-a
 b=2*a*c*np.maximum(c-1,0)+a*np.maximum(a-1,0)*c
 d=a*np.maximum(a-1,0)*c+3*a*np.maximum(a-1,0)*np.maximum(a-2,0)
 kill=a*np.maximum(a-1,0)*np.maximum(a-2,0)
 M=diags([-(d[1:]),b+d+kill,-b[:-1]],[-1,0,1],format='csc')
 T=spsolve(M,np.ones(N));U=spsolve(M,a)
 out.append(dict(N=N,min_T=float(T.min()),min_U=float(U.min()),T1=float(T[0]),U1=float(U[0]),scaled_T1=float(T[0]*N*N/np.log(N)),max_ratio=float(np.max(T/U)),scaled_ratio=float(np.max(T/U)*N**(1/3)/np.log(N))))
print(json.dumps(out,indent=2))
