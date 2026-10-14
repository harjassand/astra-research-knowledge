from fractions import Fraction
import numpy as np
from scipy.linalg import null_space
from scipy.optimize import minimize
# variables ordered r,s,p,q
vars=range(4)
def comps(total,n=4,prefix=()):
 if n==1:return [prefix+(total,)]
 out=[]
 for j in range(total+1):out+=comps(total-j,n-1,prefix+(j,))
 return out
M2=comps(2);M4=comps(4); ix={e:i for i,e in enumerate(M4)}
# R=(...)/24 in (r,s,p,q); coefficients from independent formula.
terms={
 (0,0,4,0):101,(0,0,0,4):101,(0,0,2,2):404,
 (0,0,3,1):696,(0,0,2,0):444,(0,0,0,2):444,
 (0,0,1,0):0,
 (0,0,0,0):0,
 (0,0,0,0):0,
}
# explicit coefficient map in exponents (r,s,p,q)
terms={
 (0,0,4,0):101/24, (0,0,0,4):101/24,(0,0,2,2):101/6,
 (1,0,3,0):-29/2,(0,1,0,3):29/2,
 (0,1,2,1):29,(1,0,1,2):-29,(1,1,1,1):-50,
 (2,0,2,0):37/2,(0,2,2,0):12,(2,0,0,2):12,(0,2,0,2):37/2,
 (1,2,1,0):-24,(2,1,0,1):24,
 (4,0,0,0):11/4,(0,4,0,0):11/4,(2,2,0,0):11,
}
b=np.array([terms.get(e,0.) for e in M4])
inds=[(i,j) for i in range(10) for j in range(i,10)]
A=np.zeros((len(M4),len(inds)))
for k,(i,j) in enumerate(inds):
 e=tuple(a+b for a,b in zip(M2[i],M2[j]));A[ix[e],k]+=1 if i==j else 2
print('A rank',np.linalg.matrix_rank(A),'rows',A.shape)
# Orthonormal affine projection.
Ap=np.linalg.pinv(A)
def toQ(x):
 Qm=np.zeros((10,10))
 for v,(i,j) in zip(x,inds):Qm[i,j]=Qm[j,i]=v
 return Qm
def tox(Qm):return np.array([Qm[i,j] for i,j in inds])
def pa(x):return x+Ap@(b-A@x)
def psd(x):
 Qm=toQ(x);e,V=np.linalg.eigh(Qm);return tox((V*np.maximum(e,0))@V.T)
x=pa(np.zeros(len(inds))); p=np.zeros_like(x);qcor=np.zeros_like(x)
for it in range(200000):
 y=pa(x+p);p=x+p-y
 xn=psd(y+qcor);qcor=y+qcor-xn
 err=np.linalg.norm(xn-x);res=np.linalg.norm(A@xn-b);mine=np.linalg.eigvalsh(toQ(xn)).min()
 x=xn
 if it%10000==0:print(it,err,res,mine)
 if err<1e-12 and res<1e-10 and mine>-1e-9:break
print('done',it,'res',np.linalg.norm(A@x-b),'mineig',np.linalg.eigvalsh(toQ(x)).min())
np.save('work/FO-continuous-calibration/gram_numeric.npy',toQ(x))
print(toQ(x))
