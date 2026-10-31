"""Finite scalar diagnostics only; not a coherent circuit or proof backend."""
import json, math
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad
from pathlib import Path

def transition(a,b,t):
    nu=a+b; z=math.exp(-nu*t)
    return np.array([[b/nu+a/nu*z,a/nu*(-math.expm1(-nu*t))],
                     [b/nu*(-math.expm1(-nu*t)),a/nu+b/nu*z]])

def check():
    rows=[]
    for a,b in [(1,1),(.01,10),(.001,100),(3,7)]:
      nu=a+b; pi=[b/nu,a/nu]
      for nt in [.01,.5,3,20]:
       t=nt/nu; z=math.exp(-nt); one=-math.expm1(-nt)
       P=transition(a,b,t); worst=0.; pgferr=0.
       for i in range(2):
        ts=math.log(1/pi[i])/nu
        if t>=ts:
         x=math.exp(-nu*(t-ts)); weights=[x,1-pi[i]*x]
        else:
         y=math.exp(-nu*(ts-t)); weights=[1,y-pi[i]]
        atom=weights[0]/sum(weights)
        assert sum(weights)/2>=.5-1e-13
        assert abs(atom-z/P[i,i])<1e-12
        for j in range(2):
         an=z/P[i,j] if i==j else 0.
         for frac in [.1,.5,.9]:
          v=frac*t
          before=(math.exp(-nu*(t-v))-z)/one
          pred=(1-an)*(before*np.eye(2)[j]+(1-before)*transition(a,b,v)[i])+an*np.eye(2)[i]
          truth=transition(a,b,v)[i]*transition(a,b,t-v)[:,j]/P[i,j]
          worst=max(worst,float(np.max(np.abs(pred-truth))))
         # Visible-jump generating function. A self refresh contributes NO mark.
         w=.7
         tilted=np.array([[-a,a*w],[b*w,-b]])
         def integrand(u):
          row=expm(tilted*u)[i]
          return nu*math.exp(-nu*(t-u))/one*sum(row[k]*(w if k!=j else 1) for k in range(2))
         pred=an+(1-an)*quad(integrand,0,t,epsabs=1e-12,epsrel=1e-12)[0]
         truth=expm(tilted*t)[i,j]/P[i,j]
         pgferr=max(pgferr,abs(pred-truth))
       assert worst<1e-11 and pgferr<1e-10
       rows.append(dict(q0=a,q1=b,nu_t=nt,midpoint_max_error=worst,visible_count_pgf_error=pgferr))
    event=[]
    for c,r in [(1,8),(1,100),(1,1e6),(.001,10)]:
     de=r-2*c; nu=math.sqrt(de*de+8*c*c); d=(nu+de)/2;s=2*c*c/d
     a0=(c+s)/d; ts=math.log(1/a0)/nu
     for t in [0,ts*.1,ts*(1-1e-10),ts,ts*(1+1e-10),2*ts,20*ts]:
      if t<ts:
       y=math.exp(-nu*(ts-t)); wp=c/(c+s)*(y-a0);wq=1+s/(c+s)*y
      else:
       x=math.exp(-nu*(t-ts));wp=c/(c+s)*(1-a0*x);wq=s/(c+s)+x
      z=math.exp(-nu*t); exact=c*(-math.expm1(-nu*t))/(c+s+(d-c)*z)
      assert min(wp,wq)>-1e-14 and max(wp,wq)<=2+1e-14
      assert (wp+wq)/4>=.25-1e-13
      err=abs(wp/(wp+wq)-exact);assert err<1e-12
      event.append(dict(c=c,r=r,t_over_threshold=t/ts,acceptance=(wp+wq)/4,error=err))
    return dict(scope='Scalar deterministic diagnostic; no finite-bit quantum backend or practical cost assertion.',bridge_cases=rows,event_race_cases=event)
if __name__=='__main__':
 out=check(); path=Path(__file__).with_name('last_refresh_bridge_checks.json');path.write_text(json.dumps(out,indent=2)+'\n');print(len(out['bridge_cases']),len(out['event_race_cases']),'PASS')
