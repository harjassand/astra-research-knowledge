import numpy as np, sympy as sp, scipy.linalg as la,itertools,os
BASE=os.path.dirname(__file__)
def build():
 z=np.load(BASE+'/heat_matrices.npz');a=sp.symbols('a b c d');h=sp.symbols('h0:6');x=[a[0],a[2]];y=[a[1],a[3]];hs=[[h[i],h[3+i]] for i in range(3)]
 pairsA=list(itertools.combinations_with_replacement(range(4),2));pairsH=list(itertools.combinations_with_replacement(range(6),2))
 def ex(pair,n):
  ans=[0]*n
  for i in pair:ans[i]+=1
  return tuple(ans)
 mon=[ex(p,4)+ex(q,6) for p in pairsA for q in pairsH];idx={e:i for i,e in enumerate(mon)}
 def vec(f):
  v=np.zeros(210)
  for e,c in sp.Poly(sp.expand(f),*(a+h)).terms():v[idx[e]]=c
  return v
 vals=[v[0]*hh[0]+v[1]*hh[1] for v in [x,y] for hh in hs]+[v[0]*hh[1]-v[1]*hh[0] for v in [x,y] for hh in hs]
 ij=np.array(list(itertools.combinations_with_replacement(range(12),2)));T=np.stack([vec(vals[i]*vals[j])*(1 if i==j else np.sqrt(2)) for i,j in ij],axis=1)
 B=z['P']@np.c_[T,z['E'][:,2]-z['E'][:,3]]
 U,s,R=la.svd(B,full_matrices=False);rank=(s>1e-9).sum()
 np.savez(BASE+'/scalar_matrices.npz',T=T,U=U[:,:rank],s=s[:rank],R=R[:rank],ij=ij)
 print('scalar rank',rank)
def solve(p,maxiter=10000,tol=1e-8):
 z=np.load(BASE+'/heat_matrices.npz');v=np.load(BASE+'/scalar_matrices.npz');i,j=v['ij'].T;sf=np.where(i==j,1,np.sqrt(2));R=v['R']
 def sm(g):
  G=np.zeros((12,12));G[i,j]=g[:78]/sf;G[j,i]=g[:78]/sf;return G
 def sv(G):return G[i,j]*sf
 b=z['P']@z['E']@p;g0=R.T@((v['U'].T@b)/v['s'])
 consistency=np.linalg.norm(b-v['U']@(v['U'].T@b))
 def aff(g):return g+g0-R.T@(R@g)
 def psd(g):
  val,V=la.eigh(sm(g),check_finite=False);return np.r_[sv((V*np.maximum(val,0))@V.T),max(g[-1],0)]
 x=g0.copy()
 for k in range(maxiter):
  y=psd(x);w=aff(2*y-x);x+=w-y
  if k%100==0 or k==maxiter-1:
   gg=aff(y);res=la.norm(gg-y)
   if res<tol:break
 G=sm(gg)
 return G,gg[-1],[k,float(la.eigvalsh(G)[0]),float(res),float(consistency)]
if __name__=='__main__':
 if not os.path.exists(BASE+'/scalar_matrices.npz'):build()
 p=np.array([1,1,3.5,.5,0,0,-2.9,-2.9,0]);G,d,diag=solve(p)
 print('Fstar',diag,d);np.savez(BASE+'/scalar_Fstar.npz',G=G,d=d,p=p)
 for i,v in enumerate(np.load(BASE+'/c4_heat_trials.npz',allow_pickle=True)['results']):
  G,d,diag=solve(v['p'],3000)
  print(i,diag,d,flush=True)
