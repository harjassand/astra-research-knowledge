import numpy as np, scipy.linalg as la, os
BASE=os.path.dirname(__file__)
z=np.load(BASE+'/heat_matrices.npz');i,j=z['ij'].T;sf=np.where(i==j,1,np.sqrt(2))
def sv(G):return G[i,j]*sf
def sm(g):
 G=np.zeros((24,24));G[i,j]=g[:300]/sf;G[j,i]=g[:300]/sf;return G
Eminor=z['E'][:,2]-z['E'][:,3]
B=z['P']@np.c_[z['T'],Eminor]
U,s,R=la.svd(B,full_matrices=False);n=(s>1e-9).sum();U=U[:,:n];s=s[:n];R=R[:n]
def solve(p,maxiter=10000,tol=1e-8,margin=0):
 rhs=z['P']@z['E']@np.asarray(p);g0=R.T@((U.T@rhs)/s)
 def aff(g):return g+g0-R.T@(R@g)
 def psd(g):
  v,O=la.eigh(sm(g),check_finite=False);return np.r_[sv((O*np.maximum(v,margin))@O.T),max(0,g[-1])]
 x=g0.copy()
 for k in range(maxiter):
  y=psd(x);v=aff(2*y-x);x+=v-y
  if k%100==0 or k==maxiter-1:
   gg=aff(y);err=la.norm(gg-y)
   if err<tol:break
 G=sm(gg);c=la.lstsq(z['N'],z['T']@gg[:300]+gg[-1]*Eminor-z['E']@p)[0]
 return G,c,float(gg[-1]),[k,float(la.eigvalsh(G)[0]),float(err)]
if __name__=='__main__':
 from sample_acoustic import T,D
 import itertools
 # project onto c4 acoustic subspace by selecting its parameters
 P=np.zeros((15,7));P[0,0]=P[1,0]=1;P[2,1]=1;P[3,2]=1;P[6,3]=P[7,3]=1
 # K entries (01,02,03,12,13,23)
 P[9,4]=1;P[10,5]=P[13,5]=1;P[14,6]=1
 TT=T@P
 RR,_=la.qr(TT,mode='economic');si,sj=np.array(list(itertools.combinations_with_replacement(range(8),2))).T;sf8=np.where(si==sj,1,np.sqrt(2))
 def sv8(G):return G[si,sj]*sf8
 def sm8(g):
  G=np.zeros((8,8));G[si,sj]=g/sf8;G[sj,si]=g/sf8;return G
 tr=RR.T@sv8(np.eye(8));R0=la.null_space(tr[None,:]);RS=RR@R0;g0=RR@tr/(tr@tr);pinv=la.pinv(TT)
 rng=np.random.default_rng(1182);res=[]
 for seed in range(25):
  cost=pinv.T@np.r_[rng.normal(size=4),[0]*3];step=1/max(la.norm(cost),1);x=g0.copy()
  for k in range(5000):
   val,V=la.eigh(sm8(x));y=sv8((V*np.maximum(val,0))@V.T)
   zz=g0+RS@(RS.T@(2*y-x-step*cost));x+=zz-y
  g=g0+RS@(RS.T@y);params=pinv@g;p=(P@params)[:9];p=p/max(abs(p))
  G,c,d,diag=solve(p,maxiter=6000)
  print(seed,np.round(p[[0,2,3,6]],5),diag,'delta',d,'Q',la.eigvalsh(sm8(g))[0],flush=True)
  res.append(dict(p=p,G=G,c=c,d=d,diag=diag))
 np.savez(BASE+'/c4_heat_trials.npz',results=np.array(res,dtype=object))
