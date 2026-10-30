"""Local compatible trigonometric discovery only; no global claims from samples."""
import numpy as np
rng=np.random.default_rng(671)
N=12;xx,yy=np.meshgrid(np.arange(N)*2*np.pi/N,np.arange(N)*2*np.pi/N,indexing='ij');xy=np.array([xx.ravel(),yy.ravel()])
modes=np.array([(1,0),(0,1),(1,1),(1,-1),(2,0),(0,2)])
cs=np.cos(modes@xy);sn=np.sin(modes@xy)
# coefficients output x mode x cos/sin

def field(coef):
 grad=np.einsum('om,nm,mp->onp',coef[:,:,1],modes.T,cs)-np.einsum('om,nm,mp->onp',coef[:,:,0],modes.T,sn)
 hes=-np.einsum('om,nm,km,mp->onkp',coef[:,:,0],modes.T,modes.T,cs)-np.einsum('om,nm,km,mp->onkp',coef[:,:,1],modes.T,modes.T,sn)
 def conf(aa):return np.array([aa[0,0]+aa[1,1],aa[1,0]-aa[0,1],aa[0,0]-aa[1,1],aa[1,0]+aa[0,1]])
 G=conf(grad);H=np.array([conf(hes[:,:,ii]) for ii in range(2)])
 return G,H

def qmatrix(G,R):
 z=G[:2];w=G[2:];a=R[:2];b=R[2:];nn=G.shape[1]
 ZZ=np.zeros((2,5,nn));WW=ZZ.copy();ZZ[0,0]=1;ZZ[1,1]=1;ZZ[:,4]=z;WW[0,2]=1;WW[1,3]=1;WW[:,4]=w
 aa=np.sum(a*a,axis=0);bb=np.sum(b*b,axis=0);za=np.einsum('ilp,ip->lp',ZZ,a);wb=np.einsum('ilp,ip->lp',WW,b)
 K=4*np.einsum('p,ilp,ikp->lk',aa+bb,WW,WW)+4*np.einsum('p,ilp,ikp->lk',bb,ZZ,ZZ)+8*(za@wb.T+wb@za.T)+8*wb@wb.T
 # linear cubic score per matrix coordinate
 ac=a[0]+1j*a[1];bc=b[0]+1j*b[1];zl=ZZ[0]+1j*ZZ[1];wl=WW[0]+1j*WW[1]
 ell=np.sum(2*np.real(np.conj(zl)*bc**2)+4*np.real(np.conj(ac)*wl*bc),axis=1)
 return K/nn,ell/(2*nn),2*np.mean(aa+bb)

def critical(coef,heat=True):
 G,H=field(coef)
 if heat:
  vals=[qmatrix(G,R) for R in H];K=sum(a[0] for a in vals);b=sum(a[1] for a in vals);qe=sum(a[2] for a in vals)
 else:
  K0,b0,qe0=qmatrix(np.zeros_like(G),G);K=K0/2;b=b0/2;qe=qe0/2
  z=G[:2];w=G[2:];r=np.sum(z*z,axis=0);t=np.sum(w*w,axis=0);K[:4,4]=np.mean(np.vstack([4*z*t,4*w*(r+t)]),axis=1)/2;K[4,:4]=K[:4,4];K[4,4]=np.mean(t*t+2*r*t)
  b[4]=np.mean(np.real(np.conj(z[0]+1j*z[1])*(w[0]+1j*w[1])**2))/2
 try:
  aa=np.linalg.solve(K,b);val=b@aa/qe
 except np.linalg.LinAlgError:return -1,None
 return val,-aa
if __name__=='__main__':
 best=(-1,None,None)
 for ii in range(20000):
  cf=rng.normal(size=(2,len(modes),2));cf[:,3:]*=rng.random()*.5
  value,mean=critical(cf)
  if value>best[0]:best=(value,cf.copy(),mean.copy())
 print('best random heat',best[0],best[2],flush=True)
 cf=best[1];step=.1
 for ii in range(4000):
  trial=cf+step*rng.normal(size=cf.shape);trial/=np.linalg.norm(trial)
  vv,mean=critical(trial)
  if vv>critical(cf)[0]:cf=trial
  if ii%400==399:step*=.6
 v,mean=critical(cf);print('best polished heat',v,mean,'QC',critical(cf,False));print('coeff',cf.tolist());np.savez(__file__.replace('.py','.npz'),coef=cf,mean=mean,critical=v)
