import numpy as np
from sdp_objective import Bs,sv,sm

def run(r,steps=20000,tol=1e-9):
 Q0=Bs[0]+Bs[1]+2*r*Bs[3]
 mats=[Bs[2]-Bs[3],Bs[6],Bs[7],Bs[8]]+Bs[9:]
 B=np.column_stack([sv(x) for x in mats]); pin=np.linalg.pinv(B);U=np.linalg.qr(B)[0];P=U@U.T
 x0=(np.eye(36)-P)@sv(Q0);c=pin.T@np.r_[1,1,1,0,np.zeros(6)]
 y=x0.copy();z=np.zeros_like(y)
 for it in range(steps):
  x=x0+P@(y-z-c)
  d,v=np.linalg.eigh(sm(x+z));yp=sv((v*np.maximum(d,0))@v.T)
  z+=x-yp; pr=np.linalg.norm(x-yp);du=np.linalg.norm(yp-y);y=yp
  if it%100==0 and pr<tol and du<tol:break
 a=pin@(x-sv(Q0));
 return a,sm(x),it,pr,du
if __name__=='__main__':
 for r in [1.,1.2,1.5,2.,2.5,2.9]:
  a,Q,it,pr,du=run(r)
  print(r,a[:4], 'F(I)',2+sum(a[:3]),'eval',np.linalg.eigvalsh(Q),it,pr,du,flush=True)
  np.savez(f'/mnt/data/astra_meta_genesis/canonical_{r}.npz',a=a,Q=Q)
