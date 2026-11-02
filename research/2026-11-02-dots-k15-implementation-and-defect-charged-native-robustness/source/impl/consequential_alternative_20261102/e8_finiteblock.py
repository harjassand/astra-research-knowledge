import numpy as np, json
from scipy.special import ndtri, expit, xlogy
from scipy.stats import qmc
from e8_squeezed import gf

def entropy(p):return -(xlogy(p,p)+xlogy(1-p,1-p))/np.log(2)
def calc(v,n,vec,logs=None,power=15,seed=41):
 if logs is None:logs=np.zeros(4)
 scale=np.exp(np.array([u for x in logs for u in [x,-x]]));vs=v/scale**2
 u=qmc.Sobol(8*n,scramble=True,seed=seed).random_base2(power)
 x=ndtri(u).reshape(-1,8)*np.sqrt(v/(2*np.pi))/scale
 jvec=vec.reshape(4,2)[:,::-1]*np.array([-1,1]);t=jvec.reshape(8)/2
 rr=[];ll=[]
 for i in range(0,len(x),8192):
  a=x[i:i+8192];g,f=gf(a,vs,vec);gt,_=gf(a+t,vs,vec);rr.extend(f/g);ll.extend(np.log(gt/g))
 r=np.array(rr).reshape(-1,n).prod(axis=1);l=np.array(ll).reshape(-1,n).sum(axis=1)
 values=1-entropy((1+r)/2)-entropy(expit(l))
 return {'v':v,'n':n,'vec':vec.tolist(),'logs':list(logs),'Ic':float(values.mean()),'stderr_iid_proxy':float(values.std()/np.sqrt(len(values))),'power':power}
if __name__=='__main__':
 out=[]
 for vec in [np.array([1,-1,0,0,0,0,0,0]),np.array([2,0,0,0,0,0,0,0])]:
  for n in [1,2,3,5,10]:
   row=calc(.37,n,vec);out.append(row);print(json.dumps(row),flush=True)
 open('producer-workspace/e8_finiteblock_results.json','w').write(json.dumps(out,indent=2))
