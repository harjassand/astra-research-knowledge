"""Small exact-structure log-det SDP solver used for discovery, not certificates."""
import numpy as np
from scipy.linalg import null_space

def matrix(x):
 A,B,C,E,G,H,L,M,N=x[:9]
 m11=np.array([[12*A,3*G,0,3*L],[3*G,2*C+2*E,-L,N],[0,-L,4*A,G],[3*L,N,G,2*C]])
 m12=np.array([[3*G,2*C+2*E,-L,N],[2*C+2*E,3*H,-N,M],[-L,-N,G,E],[N,M,E,H]])
 m22=np.array([[2*C+2*E,3*H,-N,M],[3*H,12*B,-3*M,0],[-N,-3*M,2*C,H],[M,0,H,4*B]])
 K=np.zeros((4,4))
 for k,(i,j) in zip(x[9:],[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]):K[i,j]=k;K[j,i]=-k
 return np.block([[m11,m12+K],[m12-K,m22]])
Bs=np.array([matrix(np.eye(15)[i]) for i in range(15)])
tr=Bs.trace(axis1=1,axis2=2)
Z=null_space(tr[None,:]);Fs=np.einsum('ia,ijk->ajk',Z,Bs)
x0=np.array([1,1,2,0,0,0,0,0,0,1,0,0,0,0,0],float);x0/=tr@x0
Q0=matrix(x0)

def solve(c,mumin=1e-9):
 c=np.r_[c,np.zeros(6)]
 scale=max(np.linalg.norm(c),1e-12);c=c/scale
 cy=Z.T@c;y=np.zeros(14)
 mus=np.geomspace(.02,mumin,9)
 for mu in mus:
  for it in range(70):
   Q=Q0+np.einsum('a,ajk->jk',y,Fs);inv=np.linalg.inv(Q)
   grad=cy-mu*np.einsum('ij,aji->a',inv,Fs)
   invF=np.einsum('ij,ajk->aik',inv,Fs)
   hes=mu*np.einsum('aij,bji->ab',invF,invF)
   try: step=np.linalg.solve(hes,-grad)
   except np.linalg.LinAlgError:step=np.linalg.lstsq(hes,-grad,rcond=1e-13)[0]
   dec=-grad@step
   if dec<1e-15:break
   val=cy@y-mu*np.linalg.slogdet(Q)[1];alpha=1.
   for j in range(80):
    yn=y+alpha*step;Qn=Q0+np.einsum('a,ajk->jk',yn,Fs)
    try:ch=np.linalg.cholesky(Qn)
    except np.linalg.LinAlgError:alpha*=.5;continue
    vn=cy@yn-2*mu*np.log(np.diag(ch)).sum()
    if vn<=val+1e-3*alpha*grad@step:break
    alpha*=.5
   y=yn
 x=x0+Z@y
 return x,float(c@x*scale),float(np.linalg.eigvalsh(matrix(x))[0])
if __name__=='__main__':
 print('initial min eig',np.linalg.eigvalsh(Q0)[0])
 for i in range(3):
  c=np.random.default_rng(i).normal(size=9);x,v,e=solve(c)
  print(v,e,'trace',tr@x,x[:9])
