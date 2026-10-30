"""Actual compatible Fourier search for a failure of ordinary-heat monotonicity.
Such a failure is a method obstruction, not a quasiconvexity counterexample.
"""
import numpy as np
from pathlib import Path
rng=np.random.default_rng(171823);N=12;xx,yy=np.meshgrid(np.arange(N)*2*np.pi/N,np.arange(N)*2*np.pi/N,indexing='ij');xx=xx.ravel();yy=yy.ravel()
ks=np.array([[1,0],[0,1],[1,1]],int)
co=np.cos(ks[:,0,None]*xx+ks[:,1,None]*yy);si=np.sin(ks[:,0,None]*xx+ks[:,1,None]*yy)
def fields(amps):
 # Gradient [[a,b],[c,d]] of sum amps*sin(k.x).
 a=amps[:,0]*ks[:,0];b=amps[:,0]*ks[:,1];c=amps[:,1]*ks[:,0];d=amps[:,1]*ks[:,1]
 rr=np.array([a+d,c-b,a-d,c+b]).T
 G=rr.T@co;HH=np.array([-(rr*ks[:,j,None]).T@si for j in range(2)])
 return G,HH

def hf(a,h):
 z=a[:2];w=a[2:];zh=h[:2];wh=h[2:];r=np.sum(z*z,axis=0);t=np.sum(w*w,axis=0);zz=np.sum(z*zh,axis=0);ww=np.sum(w*wh,axis=0)
 return 4*t*np.sum(zh*zh,axis=0)+16*zz*ww+4*(t+r)*np.sum(wh*wh,axis=0)+8*ww*ww

def score(amps,details=False):
 G,HH=fields(amps);Hs=[]
 for h in HH:
  zh=h[:2];wh=h[2:];r=np.sum(zh*zh,axis=0);t=np.sum(wh*wh,axis=0)
  H=np.zeros((4,4));H[:2,:2]=4*np.mean(t)*np.eye(2);H[:2,2:]=8*zh@wh.T/(N*N);H[2:,:2]=H[:2,2:].T;H[2:,2:]=4*np.mean(t+r)*np.eye(2)+8*wh@wh.T/(N*N);Hs.append(H)
 H=sum(Hs);l=np.zeros(4);wc=np.zeros(4);f=0.;c=0.;norm=0.
 for h in HH:
  z=G[:2];w=G[2:];zh=h[:2];wh=h[2:];zz=np.sum(z*zh,axis=0);ww=np.sum(w*wh,axis=0);zh2=np.sum(zh*zh,axis=0);wh2=np.sum(wh*wh,axis=0)
  gradz=16*zh*ww+8*z*wh2;gradw=8*w*(zh2+wh2)+16*wh*(zz+ww);l+=.5*np.mean(np.vstack([gradz,gradw]),axis=1)
  wc+=np.array([np.mean(wh[0]**2-wh[1]**2),np.mean(2*wh[0]*wh[1]),np.mean(2*(zh[0]*wh[0]+zh[1]*wh[1])),np.mean(2*(zh[1]*wh[0]-zh[0]*wh[1]))])
  f+=np.mean(hf(G,h));c+=np.mean(4*zh[0]*(w[0]*wh[0]-w[1]*wh[1])+4*zh[1]*(w[1]*wh[0]+w[0]*wh[1])+2*z[0]*(wh[0]**2-wh[1]**2)+4*z[1]*wh[0]*wh[1]);norm+=np.mean(np.sum(h*h,axis=0))
 try:sol=np.linalg.solve(H,np.column_stack([l,wc]))
 except np.linalg.LinAlgError:return -1
 aa=f-l@sol[:,0];rr=c-2*l@sol[:,1];required=(wc@sol[:,1]+rr*rr/(4*aa))/(2*norm) if aa>1e-12 else -1
 if details:return required,(aa,rr,norm,H,l,wc)
 return required
best=(-1,None)
for i in range(12000):
 amps=rng.normal(size=(3,2));amps/=np.linalg.norm(amps);value=score(amps)
 if value>best[0]:best=value,amps.copy()
 if i%2000==0:print('random',i,best,flush=True)
print('random best',best,flush=True)
step=.15
for it in range(3000):
 amps=best[1]+step*rng.normal(size=(3,2));amps/=np.linalg.norm(amps);value=score(amps)
 if value>best[0]:best=value,amps.copy()
 if it%500==0:step*=.6;print('local',it,best,flush=True)
print('FINAL',best,score(best[1],True),flush=True)
np.savez(Path(__file__).with_name('heat_shape_result.npz'),amps=best[1],threshold=best[0])
