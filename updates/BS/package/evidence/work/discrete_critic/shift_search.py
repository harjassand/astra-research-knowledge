import json,numpy as np
from fractions import Fraction
c=json.load(open('work/hidden_equilibrium/certificate.txt'));a=lambda k:np.array([[float(Fraction(t)) for t in row] for row in c[k]])
v=a('points');H=a('H');z=a('farkas_z');L=a('L');V=np.column_stack([np.ones(5),v[:,0],v[:,1],v[:,0]**2,v[:,0]*v[:,1]]);Vi=np.linalg.inv(V)
def calc(s,verbose=False):
 zz=z-s;Z=np.zeros((10,8));t=np.sum(zz*v,axis=1);Z[:5,0]=-5*t/6;Z[:5,1:3]=zz;Z[:5,3:]=t[:,None]/6;b=np.einsum('ij,ij->i',Z,-H@L);q=Vi@b[:5];zi=np.vstack([zz,[[0,0]]]);di=np.max(np.linalg.norm(zi[:,None,:]-zi[None,:,:],axis=2));grad=max(np.linalg.norm(Z@L.T[:,1:3],axis=1));ln=np.linalg.norm(q[1:3]);val=di+grad+ln
 if verbose:print('shift',s,'obj',val,'q',q,'Zmax',max(np.linalg.norm(Z,axis=1)),'diam',di,'grad',grad,'lin',ln)
 return val
best=(1e10,None)
for x in np.linspace(.6,1,41):
 for y in np.linspace(-.4,.3,71):
  val=calc([x,y])
  if val<best[0]:best=val,np.array([x,y])
for _ in range(3):
 s=best[1]
 for x in np.linspace(s[0]-.01,s[0]+.01,21):
  for y in np.linspace(s[1]-.01,s[1]+.01,21):
   val=calc([x,y])
   if val<best[0]:best=val,np.array([x,y])
calc(best[1],True);calc(np.array([.8,0]),True);calc(np.array([.82,0]),True);calc(np.array([.79,-.01]),True)
