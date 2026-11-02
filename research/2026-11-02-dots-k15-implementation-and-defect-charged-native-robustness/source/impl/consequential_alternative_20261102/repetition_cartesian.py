import sys,json,math,numpy as np
from scipy.special import expit
from scipy.optimize import minimize_scalar
sys.path.insert(0,'producer-workspace/consequential_alternative_20261102')
from flagged_repetition import counts,h2,expectation_data,entropy_deficit_bias,entropy_from_llr
from analog_quantization import one

def rep(n,w,p,lam=.5):
 c,lc=counts(n,len(w));phw=np.exp(lc+c@np.log(w));tt=np.exp(c@np.log(1-2*p));z=2*lam-1
 phase=phw@h2((1+np.sqrt(z*z+(1-z*z)*tt*tt))/2)
 mass=np.column_stack([w*(1-p),w*p]).ravel();ll=np.column_stack([np.log((1-p)/p),np.log(p/(1-p))]).ravel()
 cc,lc=counts(n,len(mass));ww=np.exp(lc+cc@np.log(mass));post=expit(cc@ll)
 if lam==.5:return float(phw@entropy_deficit_bias(tt)-ww@entropy_from_llr(cc@ll))
 return float(ww@(h2((1-lam)+z*post)-h2(post))-phase)

out=[]
for v in [.3679,.37]:
 conf=one(v)
 for b in conf['records']:
  w=np.array(b['w']);p=np.array(b['p']);B=b['B'];N={2:50,3:30,4:20}[B]
  vals=[]
  for n in range(1,N+1):
   value=rep(n,w,p);vals.append({'n':n,'Ic':value,'rate':value/n})
  obj={'v':v,'B_per_quadrature':B,'totalflags':B*B,'w':w.tolist(),'p':p.tolist(),'records':vals};out.append(obj)
  print(v,B,'n3',vals[2],'n6',vals[5],'best',max(vals,key=lambda d:d['Ic']),flush=True)
json.dump(out,open('producer-workspace/repetition_cartesian_results.json','w'),indent=2)
