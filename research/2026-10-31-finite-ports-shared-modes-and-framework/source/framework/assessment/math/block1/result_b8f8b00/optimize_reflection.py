import numpy as np
rng=np.random.default_rng(521)
def val(z):
 s,u,v=z;a=1+s+u;b=(1-s-v)/2;c=1.5-s;p=s/4+u+v/4
 if min(s,u,v,b)<-1e-12:return -1
 G=np.array([[a,p,-p],[p,b,.5-p],[-p,.5-p,c]])
 if np.linalg.eigvalsh(G)[0]<-1e-12:return -1
 return u+v
best=(-1,None)
for _ in range(150000):
 z=rng.random(3);z[1]*=2;z[2]*=1-z[0]
 vv=val(z)
 if vv>best[0]:best=(vv,z)
print('random',best)
z=best[1].copy();step=.1
for it in range(1500):
 ds=np.array([rng.normal(size=3) for _ in range(100)]);ds/=np.linalg.norm(ds,axis=1)[:,None]
 ds=np.vstack([ds,np.eye(3),-np.eye(3)])
 candidates=z+step*ds;vals=[val(zz) for zz in candidates];ii=np.argmax(vals)
 if vals[ii]>val(z):z=candidates[ii]
 else:step*=.8
 if step<1e-10:break
print('opt',val(z),z,'lambda',1/(4*val(z)))
s,u,v=z;a=1+s+u;b=(1-s-v)/2;c=1.5-s;p=s/4+u+v/4
G=np.array([[a,p,-p],[p,b,.5-p],[-p,.5-p,c]])
print('eig',np.linalg.eigvalsh(G),'G',G,'q1,q3',8*a-12,4-4*b)
