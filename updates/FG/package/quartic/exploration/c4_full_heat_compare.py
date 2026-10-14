import numpy as np,scipy.linalg as la,os
from c4_compare_cones import opt_ac
BASE=os.path.dirname(__file__);z=np.load(BASE+'/heat_matrices.npz');i,j=z['ij'].T;sf=np.where(i==j,1,np.sqrt(2))
E=z['E'];P=z['P'];Cb=P@np.stack([E[:,0]+E[:,1],E[:,2],E[:,3],E[:,6]+E[:,7]],axis=1);D=P@np.c_[z['T'],E[:,2]-E[:,3]];pinv=la.pinv(Cb);pmap=pinv@D;A0=la.null_space(Cb.T).T@D;tr=np.array([32,8,4,0.])@pmap
AA=np.r_[A0,tr[None,:]];bb=np.r_[np.zeros(len(A0)),1.];U,s,R=la.svd(AA,full_matrices=False);rank=(s>1e-9).sum();U=U[:,:rank];s=s[:rank];R=R[:rank];g0=R.T@((U.T@bb)/s)
def sm(g):
 G=np.zeros((24,24));G[i,j]=g[:300]/sf;G[j,i]=g[:300]/sf;return G
def sv(G):return G[i,j]*sf
def opt_full(c,steps=50000):
 cost=c@pmap;step=3/max(la.norm(cost),1);x=g0.copy()
 for k in range(steps):
  val,V=la.eigh(sm(x),check_finite=False);y=np.r_[sv((V*np.maximum(val,0))@V.T),max(x[-1],0)]
  v=2*y-x-step*cost;v+=g0-R.T@(R@v);x+=v-y
 gg=y+g0-R.T@(R@y);p=pmap@gg
 return c@p,p,la.norm(gg-y),la.eigvalsh(sm(gg))[0]
if __name__=='__main__':
 rng=np.random.default_rng(1182)
 for k in range(12):
  c=rng.normal(size=4)
  if k not in [5,8,10,11]:continue
  ac=opt_ac(c,10000);ht=opt_full(c,40000)
  print(k,'gap',ht[0]-ac[0], 'ROC',ac,'heat',ht,flush=True)
