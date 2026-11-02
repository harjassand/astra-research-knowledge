import numpy as np
from scipy.special import ndtri
from scipy.stats import qmc
from scipy.optimize import differential_evolution, minimize
import json
z=np.arange(-4,5)
zsign=(-1.)**z

def gf(x,vs,vec):
 g=np.zeros(len(x)); f=np.zeros(len(x)); parity=np.array(vec)%2
 for h in [0,.5]:
  w=np.exp(-np.pi/vs[None,:,None]*(x[:,:,None]+h+z)**2)
  A=w.sum(axis=2);B=(w*zsign).sum(axis=2)
  g+=(A.prod(axis=1)+B.prod(axis=1))/2
  X=np.where(parity[None,:],B,A);Y=np.where(parity[None,:],A,B)
  f+=np.cos(np.pi*h*sum(vec))*(X.prod(axis=1)+Y.prod(axis=1))/2
 return g,f

def evaluate(logs, v, vec, raw):
 scale=np.exp(np.array([u for x in logs for u in [x,-x]]));vs=v/scale**2
 x=raw*np.sqrt(v/(2*np.pi))/scale
 jvec=vec.reshape(4,2)[:,::-1]*np.array([-1,1]);t=jvec.reshape(8)/2
 rr=[]
 for i in range(0,len(x),8192):
  a=x[i:i+8192];g,f=gf(a,vs,vec);gt,_=gf(a+t,vs,vec);rr.extend(((f/g)**2-2*np.sqrt(gt*g)/(gt+g)))
 return float(np.mean(rr))
if __name__=='__main__':
 raw=ndtri(qmc.Sobol(8,scramble=True,seed=13).random_base2(13)); out=[]
 vectors=[np.array(x) for x in [[1,-1,0,0,0,0,0,0],[1,0,-1,0,0,0,0,0],[2,0,0,0,0,0,0,0]]]
 for vec in vectors:
  fun=lambda logs:-evaluate(logs,.37,vec,raw)
  opt=differential_evolution(fun,[(-.8,.8)]*4,maxiter=25,popsize=4,polish=True,tol=.0003,seed=1)
  row={'vec':vec.tolist(),'logs':opt.x.tolist(),'gap_diagnostic':-opt.fun};print(json.dumps(row),flush=True)
  ref=ndtri(qmc.Sobol(8,scramble=True,seed=234).random_base2(18)); row['gap_refined_bounded']=evaluate(opt.x,.37,vec,ref);out.append(row);print('refined',row['gap_refined_bounded'],flush=True)
 open('producer-workspace/e8_squeeze_results.json','w').write(json.dumps(out,indent=2))
