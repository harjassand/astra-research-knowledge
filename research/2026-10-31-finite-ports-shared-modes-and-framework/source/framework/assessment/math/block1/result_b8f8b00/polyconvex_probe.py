import numpy as np
rng=np.random.default_rng(981);lam=(3+np.sqrt(3))/24

def P(A):
 x,y,u,v=np.moveaxis(A,-1,0);r=x*x+y*y;t=u*u+v*v
 return t*t+2*r*t+x*(u*u-v*v)+2*y*u*v+lam*(r+t)
def DP(A):
 x,y,u,v=A;r=x*x+y*y;t=u*u+v*v
 return np.array([4*x*t+u*u-v*v+2*lam*x,4*y*t+2*u*v+2*lam*y,4*u*(r+t)+2*x*u+2*y*v+2*lam*u,4*v*(r+t)-2*x*v+2*y*u+2*lam*v])
def probe(A,B):
 D=B-A;delta=np.sum(D[:,:2]**2,axis=1)-np.sum(D[:,2:]**2,axis=1);gap=P(B)-P(A)-D@DP(A)
 pos=delta>1e-10;neg=delta< -1e-10
 ratios=gap/delta;up=np.where(pos,ratios,np.inf);lo=np.where(neg,ratios,-np.inf);iu=up.argmin();il=lo.argmax()
 return lo[il]-up[iu],B[il],B[iu],lo[il],up[iu]
best=(-np.inf,None)
for ii in range(1000):
 A=rng.normal(size=4)*rng.choice([.1,.25,.5,1,2,4]);B=A+rng.normal(size=(2000,4))*rng.choice([.01,.1,.3,.6,1,2]);res=probe(A,B)
 if res[0]>best[0]:best=(res[0],A,res)
 if res[0]>1e-6:break
print('best',best)
np.savez(__file__.replace('.py','.npz'),A=best[1],loB=best[2][1],upB=best[2][2],gap=best[0])
