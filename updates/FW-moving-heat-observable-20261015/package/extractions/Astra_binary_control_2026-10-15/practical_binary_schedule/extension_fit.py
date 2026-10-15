import numpy as np,itertools,json
from scipy.optimize import least_squares
out=[]
for k in [3,4,5,6]:
 rng=np.random.default_rng(32+k); B=rng.normal(0,.12,(k,k));np.fill_diagonal(B,0);a=rng.uniform(.7,1.4,k);astar=1.2; truth=rng.normal(0,.2,2*k); contexts=[]
 for mask in range(1,1<<k):
  T=np.array([i for i in range(k) if mask>>i&1]);inv=np.linalg.inv(np.eye(len(T))+B[np.ix_(T,T)]);p=inv@np.ones(len(T));q=a[T]@inv;contexts.append((T,inv,p,q))
 def response(x):
  return np.array([(astar-q@x[k+T])*(1-x[T]@p)/(1-x[T]@inv@x[k+T]) for T,inv,p,q in contexts])
 target=response(truth)
 def fun(x):return response(x)-target
 sols=[];errors=[]
 for j in range(50):
  fit=least_squares(fun,rng.normal(0,.4,2*k),max_nfev=1000,ftol=1e-11,xtol=1e-11,gtol=1e-11)
  err=np.max(np.abs(fit.fun));errors.append(float(err))
  if err<1e-8 and all(np.linalg.norm(fit.x-y)>1e-4 for y in sols):sols.append(fit.x)
 result={'k':k,'solutions_found':len(sols),'distance_to_truth':[float(np.linalg.norm(x-truth)) for x in sols],'max_residual':max(errors),'all_runs_converged':all(e<1e-8 for e in errors)};out.append(result);print(result,flush=True)
open('/workspace/shared/practical_binary_schedule/extension_fit.json','w').write(json.dumps(out,indent=2))
