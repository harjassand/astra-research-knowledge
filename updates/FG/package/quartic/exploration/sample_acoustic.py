import numpy as np, scipy.linalg as la, itertools, os,time
from heat_sos import solve
BASE=os.path.dirname(__file__)
def acoustic(p,k):
 A,B,C,E,G,H,L,M,N=p
 M11=np.array([[12*A,3*G,0,3*L],[3*G,2*C+2*E,-L,N],[0,-L,4*A,G],[3*L,N,G,2*C]])
 M12=np.array([[3*G,2*C+2*E,-L,N],[2*C+2*E,3*H,-N,M],[-L,-N,G,E],[N,M,E,H]])
 M22=np.array([[2*C+2*E,3*H,-N,M],[3*H,12*B,-3*M,0],[-N,-3*M,2*C,H],[M,0,H,4*B]])
 K=np.zeros((4,4))
 for val,(i,j) in zip(k,itertools.combinations(range(4),2)):K[i,j]=val;K[j,i]=-val
 return np.block([[M11,M12+K],[M12-K,M22]])
D=np.stack([acoustic(np.eye(15)[j,:9],np.eye(15)[j,9:]) for j in range(15)])
ij=np.array(list(itertools.combinations_with_replacement(range(8),2)));i,j=ij.T;sf=np.where(i==j,1,np.sqrt(2))
def sv(G):return G[i,j]*sf
def sm(x):
 G=np.zeros((8,8));G[i,j]=x/sf;G[j,i]=x/sf;return G
T=np.stack([sv(d) for d in D],axis=1)
R,_=la.qr(T,mode='economic');tr=R.T@sv(np.eye(8));trn=tr@tr
R0=la.null_space(tr.reshape(1,-1));RR=R@R0;g0=R@tr/trn
pinv=la.pinv(T)
def extreme(c,steps=3000):
 cost=pinv.T@np.r_[c,np.zeros(6)];step=1/max(1,la.norm(cost))
 def aff(g):return g0+RR@(RR.T@(g-step*cost))
 def psd(g):
  v,U=la.eigh(sm(g),check_finite=False);return sv((U*np.maximum(v,0))@U.T)
 x=g0.copy()
 for k in range(steps):
  y=psd(x);z=aff(2*y-x);x+=z-y
 q=g0+RR@(RR.T@y);p=pinv@q
 return p,la.eigvalsh(sm(q))[0],la.norm(q-y)
if __name__=='__main__':
 rng=np.random.default_rng(6172);results=[]
 for seed in range(25):
  z,mn,res=extreme(rng.normal(size=9))
  p=z[:9];p=p/max(abs(p))
  G,c,hist,err=solve(p,maxiter=5000,tol=1e-8,margin=0)
  print(seed,'Qev/res',mn,res,'heat',hist[-1],'p',np.round(p,4),flush=True)
  results.append(dict(p=p,K=z[9:]/max(abs(z[:9])),heatG=G,heatc=c,heatresult=hist[-1],Qresult=[mn,res]))
 np.savez(BASE+'/random_heat_trials.npz',results=np.array(results,dtype=object))
