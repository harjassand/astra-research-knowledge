"""Exact multinomial formulas, numerical inputs/evaluation; not a certificate."""
import math,json,itertools
import numpy as np
from scipy.special import gammaln,expit,xlogy
from scipy.optimize import minimize_scalar
from numpy.polynomial.legendre import leggauss
from functools import lru_cache

def h2(p):
 p=np.clip(p,0,1)
 return -(xlogy(p,p)+xlogy(1-p,1-p))/np.log(2)

@lru_cache(maxsize=6)
def counts(n,m):
 if m==1:return np.array([[n]],dtype=np.int16),np.array([0.])
 size=math.comb(n+m-1,m-1)
 cuts=np.fromiter(itertools.chain.from_iterable(itertools.combinations(range(n+m-1),m-1)),dtype=np.int16,count=size*(m-1)).reshape(size,m-1)
 a=np.diff(np.column_stack([np.full(size,-1,dtype=np.int16),cuts,np.full(size,n+m-1,dtype=np.int16)]),axis=1)-1
 logcoef=gammaln(n+1)-gammaln(a+1).sum(axis=1)
 return a,logcoef

def expectation_data(n,mass,tt,ll):
 mass=np.asarray(mass);tt=np.asarray(tt);ll=np.asarray(ll)
 mask=mass>1e-16;mass=mass[mask];tt=tt[mask];ll=ll[mask]
 c,lc=counts(n,len(mass))
 weight=np.exp(lc+c@np.log(mass))
 tabs=np.exp(c@np.log(np.maximum(abs(tt),1e-300)))
 post=expit(c@ll)
 return weight,tabs,post,c@ll

def rep_data(n,w,p,orientation=3):
 # p rows [I,X,Y,Z]; choose computational Z axis = selected orientation.
 others=[x for x in [1,2,3] if x!=orientation]
 a=p[:,0];d=p[:,orientation];b=p[:,others[0]];cc=p[:,others[1]]
 r0=a+d;r1=b+cc
 mass=np.column_stack([w*r0,w*r1]).ravel()
 tt=np.column_stack([(a-d)/r0,(b-cc)/r1]).ravel()
 ll=np.column_stack([np.log(r0/r1),np.log(r1/r0)]).ravel()
 return expectation_data(n,mass,tt,ll)

def entropy_deficit_bias(t):
 t=np.minimum(abs(np.asarray(t)),1.)
 # 1-h2((1+t)/2), positive series avoids cancellation near t=0.
 small=t<1e-3;ans=np.empty_like(t)
 x=t[small]**2
 ans[small]=(x/2+x*x/12+x**3/30+x**4/56)/np.log(2)
 big=t[~small]
 ans[~small]=(xlogy(1+big,1+big)+xlogy(1-big,1-big))/(2*np.log(2))
 return ans

def entropy_from_llr(ll):
 a=abs(np.asarray(ll))
 return (np.log1p(np.exp(-a))+a*expit(-a))/np.log(2)

def evaluate(data,lam=.5):
 w,t,p,ll=data;z=2*lam-1
 if lam==.5:return float(w@(entropy_deficit_bias(t)-entropy_from_llr(ll)))
 if lam==0 or lam==1:return 0.
 bias=np.sqrt(z*z+(1-z*z)*t*t)
 return float(w@(h2((1-lam)+z*p)-1+entropy_deficit_bias(bias)-entropy_from_llr(ll)))

def optimize_mix(data):
 # Search equal mixture and interior local extrema; boundary pure state is 0.
 grid=np.r_[.00001,.0001,.001,.01,np.linspace(.025,.5,20)]
 vals=np.array([evaluate(data,x) for x in grid])
 j=np.argmax(vals); l=max(0,j-1);r=min(len(grid)-1,j+1)
 if l<r:
  sol=minimize_scalar(lambda x:-evaluate(data,x),bounds=(grid[l],grid[r]),method='bounded',options={'xatol':1e-8})
  if -sol.fun>vals[j]:return {'lambda':float(sol.x),'Ic':float(-sol.fun),'Ic_equal':evaluate(data,.5)}
 return {'lambda':float(grid[j]),'Ic':float(vals[j]),'Ic_equal':evaluate(data,.5)}

def grid_channel(v,N=64,ratio=1.0):
 x,z=leggauss(N); H=math.sqrt(math.pi)/2;s=(x+1)*H/2;weights=z*H/2
 m=np.arange(-10,11)
 arr=[]
 for vv in [v/ratio,v*ratio]:
  ff=np.exp(-(s[:,None]+m*math.sqrt(math.pi))**2/(2*vv))/math.sqrt(2*math.pi*vv)
  g=ff.sum(1);p=ff[:,m%2!=0].sum(1)/g;ww=2*weights*g;ww/=ww.sum();arr.append((ww,p))
 a,b=np.meshgrid(arr[0][1],arr[1][1],indexing='ij')
 vec=np.stack([(1-a)*(1-b),a*(1-b),a*b,(1-a)*b],axis=-1).reshape(-1,4)
 return (arr[0][0][:,None]*arr[1][0][None,:]).ravel(),vec,s

def cluster(v,K,N=64,starts=40,ratio=1.0):
 w,p,s=grid_channel(v,N,ratio);rng=np.random.default_rng(928394+K)
 best=None
 for run in range(starts):
  centers=p[rng.choice(len(w),K,replace=False,p=w)].copy()
  for it in range(200):
   labels=np.argmin(-p@np.log(np.maximum(centers,1e-300)).T,axis=1)
   mass=np.bincount(labels,weights=w,minlength=K)
   if np.any(mass<1e-12):break
   new=np.array([(w[labels==k,None]*p[labels==k]).sum(0)/mass[k] for k in range(K)])
   if np.max(abs(new-centers))<1e-14:centers=new;break
   centers=new
  if np.any(mass<1e-12):continue
  ent=float(-np.sum(mass[:,None]*xlogy(centers,centers))/np.log(2))
  if best is None or ent<best['entropy']:
   best={'v':v,'ratio':ratio,'K':K,'N':N,'entropy':ent,'Ic_one_use':1-ent,'w':mass.tolist(),'pauli':centers.tolist(),'labels':labels.reshape(N,N).tolist(),'grid':s.tolist()}
 return best

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--v',type=float,default=.3679);parser.add_argument('--K',type=int,default=4);parser.add_argument('--maxn',type=int,default=15);parser.add_argument('--out',required=True);args=parser.parse_args()
 cl=cluster(args.v,args.K);w=np.array(cl['w']);p=np.array(cl['pauli']);results=[]
 for n in list(range(1,args.maxn+1)):
  for ori in [1,2,3]:
   data=rep_data(n,w,p,ori);ans=optimize_mix(data);ans.update(n=n,orientation=ori,probability_sum=float(data[0].sum()));results.append(ans)
 cl['repetition']=results
 with open(args.out,'w') as f:json.dump(cl,f,indent=2)
 print(json.dumps({'v':args.v,'K':args.K,'Ic1':cl['Ic_one_use'],'w':cl['w'],'pauli':cl['pauli'],'best_equal':max(results,key=lambda a:a['Ic_equal']),'best_nontrivial_mixture':max(results,key=lambda a:a['Ic'])},indent=2),flush=True)
