import numpy as np,scipy.linalg as la,pickle,itertools,os
from sample_acoustic import T
BASE=os.path.dirname(__file__)
with open(BASE+'/c4_heat_symbolic.pkl','rb') as f:z=pickle.load(f)
C=np.array(z['C']).astype(float);Cb=np.array(z['P']*z['EA']).astype(float);Cd=np.array(z['P']*z['EM']).astype(float)
ij=np.array(list(itertools.combinations_with_replacement(range(6),2)));i,j=ij.T;sf=np.where(i==j,1,np.sqrt(2))
D=np.c_[C/sf,Cd];pinv=la.pinv(Cb);pmap=pinv@D;left=la.null_space(Cb.T).T
A0=left@D;tr=np.array([32,8,4,0.])@pmap
AA=np.r_[A0,tr[None,:]];bb=np.r_[np.zeros(len(A0)),1.]
U,s,R=la.svd(AA,full_matrices=False);n=(s>1e-9).sum();U=U[:,:n];s=s[:n];R=R[:n];g0=R.T@((U.T@bb)/s)
def sm(g):
 G=np.zeros((6,6));G[i,j]=g[:21]/sf;G[j,i]=g[:21]/sf;return G
def sv(G):return G[i,j]*sf
def opt_heat(c,steps):
 cost=c@pmap;step=1/max(la.norm(cost),1);x=g0.copy()
 for k in range(steps):
  val,V=la.eigh(sm(x));y=np.r_[sv((V*np.maximum(val,0))@V.T),max(x[-1],0)]
  v=2*y-x-step*cost;v+=g0-R.T@(R@v);x+=v-y
 gg=y+g0-R.T@(R@y);p=pmap@gg
 return c@p,p,la.norm(gg-y),la.eigvalsh(sm(gg))[0]
# acoustic optimizer
P=np.zeros((15,7));P[0,0]=P[1,0]=1;P[2,1]=1;P[3,2]=1;P[6,3]=P[7,3]=1;P[9,4]=1;P[10,5]=P[13,5]=1;P[14,6]=1
TT=T@P;QQ,_=la.qr(TT,mode='economic');ii,jj=np.array(list(itertools.combinations_with_replacement(range(8),2))).T;sf8=np.where(ii==jj,1,np.sqrt(2))
def sv8(G):return G[ii,jj]*sf8
def sm8(x):
 G=np.zeros((8,8));G[ii,jj]=x/sf8;G[jj,ii]=x/sf8;return G
tr8=QQ.T@sv8(np.eye(8));R8=QQ@la.null_space(tr8[None,:]);g8=QQ@tr8/(tr8@tr8);p8=la.pinv(TT)
def opt_ac(c,steps):
 cost=p8.T@np.r_[c,np.zeros(3)];step=1/max(la.norm(cost),1);x=g8.copy()
 for k in range(steps):
  val,V=la.eigh(sm8(x));y=sv8((V*np.maximum(val,0))@V.T);v=g8+R8@(R8.T@(2*y-x-step*cost));x+=v-y
 gg=g8+R8@(R8.T@y);p=(p8@gg)[:4]
 return c@p,p,la.norm(gg-y),la.eigvalsh(sm8(gg))[0]
if __name__=='__main__':
 rng=np.random.default_rng(1182)
 for k in range(15):
  c=rng.normal(size=4)
  ac=opt_ac(c,8000);ht=opt_heat(c,30000)
  print(k,'objective gap',ht[0]-ac[0],'ac',ac[0],ac[2:],'heat',ht[0],ht[2:],'p',ac[1]/max(abs(ac[1])),flush=True)
