import numpy as np
rng=np.random.default_rng(617)
def calc(z):
 s,u,v=z;a=1+s+u;b=(1-s-v)/2;c=1.5-s;p=s/4+u+v/4
 G=np.array([[a,p,-p],[p,b,.5-p],[-p,.5-p,c]])
 H=G[:2,:2]+np.diag([v,0]);ww=G[:2,2]
 if min(s,u,v,b)<-1e-10 or np.linalg.eigvalsh(G)[0]<-1e-10:return -1
 try:return 1.5-ww@np.linalg.solve(H,ww)
 except np.linalg.LinAlgError:return -1
best=(-1,None)
for _ in range(100000):
 z=rng.random(3);z[1]*=.5;z[2]*=1-z[0]
 k=calc(z)
 if k>best[0]:best=(k,z)
print('random',best,'lambda',1/(4*best[0]),flush=True)
z=best[1].copy(); step=.05
for it in range(1000):
 candidates=[z+step*np.array(delta) for delta in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1),(1,1,0),(1,-1,0),(-1,1,0),(-1,-1,0),(1,0,1),(-1,0,1),(1,0,-1),(-1,0,-1),(0,1,1),(0,-1,1),(0,1,-1),(0,-1,-1)]]
 vals=[calc(zz) for zz in candidates];idx=np.argmax(vals)
 if vals[idx]>calc(z):z=candidates[idx]
 else:step*=.8
 if step<1e-12:break
print('polish',calc(z),z,'lambda',1/(4*calc(z)))
s,u,v=z;a=1+s+u;b=(1-s-v)/2;c=1.5-s;p=s/4+u+v/4
print('G',np.array([[a,p,-p],[p,b,.5-p],[-p,.5-p,c]]),'q1 q3',8*a-12,4-4*b)
