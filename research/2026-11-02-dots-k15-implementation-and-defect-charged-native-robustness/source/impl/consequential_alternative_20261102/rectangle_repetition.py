import sys,math,json,numpy as np
from scipy.optimize import minimize
from scipy.special import expit
sys.path.insert(0,'producer-workspace/consequential_alternative_20261102')
from analog_quantization import bins,grad,HALF
from flagged_repetition import counts,h2,entropy_deficit_bias,entropy_from_llr

def quant(v,B):
 cons={'type':'ineq','fun':lambda t:np.diff(t)-1e-9,'jac':lambda t:np.diff(np.eye(len(t)),axis=0)}
 t=np.linspace(0,HALF,B+1)[1:-1]
 sol=minimize(lambda t:bins(v,t)[0],t,jac=lambda t:grad(v,t),bounds=[(1e-9,HALF-1e-9)]*(B-1),constraints=cons,method='SLSQP',options={'ftol':3e-14,'maxiter':600})
 hh,w,e,p=bins(v,sol.x)
 return {'v':v,'B':B,'thresholds':sol.x.tolist(),'H':hh,'w':w.tolist(),'p':p.tolist(),'success':bool(sol.success)}

def components(n,rec):
 w=np.array(rec['w']);p=np.array(rec['p'])
 c,lc=counts(n,len(w));phw=np.exp(lc+c@np.log(w));tt=np.exp(c@np.log(1-2*p));phase=phw@entropy_deficit_bias(tt)
 mass=np.column_stack([w*(1-p),w*p]).ravel();ll=np.column_stack([np.log((1-p)/p),np.log(p/(1-p))]).ravel()
 c,lc=counts(n,len(mass));ww=np.exp(lc+c@np.log(mass));post=expit(c@ll);bit=ww@entropy_from_llr(c@ll)
 return float(phase),float(bit)

if __name__=='__main__':
 out=[]
 for v in [.3681,.37]:
  for B,N in [(4,20),(8,8),(16,5),(32,3)]:
   for r in [1.5,2.,2.5,3.,3.5,4.,5.,6.]:
    small=quant(v/r,B);large=quant(v*r,B);rows=[]
    for n in range(1,N+1):
     phs,bts=components(n,small);phl,btl=components(n,large)
     rows.append({'n':n,'Ic_phase_low':phs-btl,'Ic_phase_high':phl-bts})
    rec={'v':v,'r':r,'B':B,'small':small,'large':large,'records':rows};out.append(rec)
    print(json.dumps({'v':v,'r':r,'B':B,'best':max(rows,key=lambda a:max(a['Ic_phase_low'],a['Ic_phase_high']))}),flush=True)
    json.dump(out,open('producer-workspace/rectangle_repetition_results.json','w'),indent=2)
