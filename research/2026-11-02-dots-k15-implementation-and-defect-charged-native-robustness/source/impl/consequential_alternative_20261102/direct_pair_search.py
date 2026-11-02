import numpy as np, math,json,time
from scipy.special import comb
from scipy.stats import binom,nbinom
from scipy.optimize import minimize_scalar,minimize
from numpy.linalg import eigh

def elem(m,n,eta,M=64):
 G=2-eta;tau=eta/G;out=np.zeros((M+2,M+2))
 for l in range(min(m,n)+1):
  loss=np.sqrt(comb(m,l)*comb(n,l))*(1-tau)**l*tau**((m+n)/2-l)
  a=m-l;b=n-l
  for k in range(M-max(a,b)+1):
   amp=np.sqrt(comb(a+k,k)*comb(b+k,k))*(G-1)**k/G**((a+b)/2+k+1)
   out[a+k,b+k]+=loss*amp
 if m==n:
  out[-1,-1]=sum(binom.pmf(l,m,1-tau)*nbinom.sf(M-(m-l),m-l+1,1/G) for l in range(m+1))
 return out
class Pair:
 def __init__(self,e=.78,k=10,M=64):
  self.e=e;self.k=k;self.M=M;self.n0=np.arange(k)*4;self.n1=self.n0+1
  self.T00=np.array([[elem(m,n,e,M) for n in self.n0] for m in self.n0])
  self.T11=np.array([[elem(m,n,e,M) for n in self.n1] for m in self.n1])
  self.T01=np.array([[elem(m,n,e,M) for n in self.n1] for m in self.n0])
 def ops(self,z):
  x=z[:self.k];x=x/np.linalg.norm(x);y=z[self.k:];y=y/np.linalg.norm(y)
  B0=np.einsum('i,j,ijab->ab',x,x,self.T00,optimize=True);B1=np.einsum('i,j,ijab->ab',y,y,self.T11,optimize=True);X=np.einsum('i,j,ijab->ab',x,y,self.T01,optimize=True)
  return B0,B1,X
 def calc(self,z,cut=1e-14):
  B0,B1,X=self.ops(z)
  l0,U0=eigh(B0);l1,U1=eigh(B1)
  i0=l0>cut;i1=l1>cut;l0=l0[i0];l1=l1[i1];U0=U0[:,i0];U1=U1[:,i1]
  o=(U0.T@U1)**2;x=(U0.T@X@U1)**2
  L0=np.log(l0)[:,None];L1=np.log(l1)[None,:]
  def cb(s):return np.sum(o*np.exp(s*L0+(1-s)*L1))
  def ce(s):return np.sum(x*np.exp((s-1)*L0-s*L1))
  r0=minimize_scalar(cb,bounds=(.01,.99),method='bounded');r1=minimize_scalar(ce,bounds=(.01,.99),method='bounded')
  return {'CB':float(r0.fun),'CE':float(r1.fun),'gap':float(r1.fun-r0.fun),'sB':r0.x,'sE':r1.x,'trace0':np.trace(B0),'trace1':np.trace(B1),'min0':float(l0.min()),'min1':float(l1.min())}
 def objective(self,z):
  r=self.calc(z);return np.log(r['CB']/r['CE'])

if __name__=='__main__':
 a=np.array([313,-717,1627,-3027,4551,-5436,4983,-3270,1324,-220]);b=np.array([361,-895,1938,-3422,4866,-5464,4646,-2754,945,-106]);z=np.r_[a/np.linalg.norm(a),b/np.linalg.norm(b)]
 out=[]
 for e in [.75,.77,.78,.7818,.7841,.8]:
  p=Pair(e=e);r=p.calc(z);r['eta']=e;print(r,flush=True);out.append(r)
 open('producer-workspace/direct_pair_primary_seed_results.json','w').write(json.dumps(out,indent=2))
 p=Pair(e=.78)
 t=time.time();result=minimize(p.objective,z,method='BFGS',options={'maxiter':100,'gtol':1e-7});print('opt',result.fun,p.calc(result.x),'time',time.time()-t,flush=True)
 out={'z':result.x.tolist(),'objective':float(result.fun),'calc':p.calc(result.x),'nit':result.nit,'success':str(result.success),'message':str(result.message)}
 open('producer-workspace/direct_pair_optimized_results.json','w').write(json.dumps(out,indent=2))
