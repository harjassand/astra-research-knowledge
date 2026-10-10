"""Native adaptive two-exponential commutator-free fourth-order baseline.

Formula: Blanes and Moan, Applied Numerical Mathematics 56 (2006), 1519-1537.
https://personales.upv.es/~serblaza/2006APNUM.pdf
This is an independent native implementation, not author software. Double
precision plus step doubling is empirical, not a rigorous error certificate.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from prototype_numpy import D2,D1,D0,I

def run(B,f,s,seconds=30,safety=.04):
 start=time.perf_counter();end=2.**(B-1);length=2*end;kappa=2.**f;tol=2.**(-s)
 count={'hamiltonian_evaluations':0,'eigensystems':0,'accepted_steps':0,'rejected_steps':0};u=-end;h=min(.05,length);U=I.copy();status='complete_uncertified';reason=None;accumulated_indicator=0.
 g1=(3-2*np.sqrt(3))/12;g2=(3+2*np.sqrt(3))/12;c1=.5-np.sqrt(3)/6;c2=.5+np.sqrt(3)/6
 def H(t):count['hamiltonian_evaluations']+=1;return kappa*(t*t*D2+t*D1+D0)
 def E(A):
  vals,Q=np.linalg.eigh(A);count['eigensystems']+=1
  return (Q*np.exp(-1j*vals))@Q.conj().T
 def step(t,d):
  A1=H(t+c1*d);A2=H(t+c2*d)
  return E(d*(g1*A1+g2*A2))@E(d*(g2*A1+g1*A2))
 while u<end:
  if time.perf_counter()-start>seconds:status='censored';reason='native baseline row budget exceeded';break
  h=min(h,end-u)
  full=step(u,h);half=step(u+h/2,h/2)@step(u,h/2)
  err=np.linalg.norm(full-half,2)/15;local=safety*tol*h/length
  if err<=local or h<1e-14:
   U=half@U;u+=h;count['accepted_steps']+=1;accumulated_indicator+=err
  else:count['rejected_steps']+=1
  factor=np.clip(.9*(local/max(err,1e-300))**.2,.2,3.)
  h*=factor
 result={'B':B,'f':f,'s':s,'method':'native adaptive two-exponential CF4 with step doubling','formula_source':'https://personales.upv.es/~serblaza/2006APNUM.pdf','certified':False,'status':status,'reason':reason,'seconds':time.perf_counter()-start,'counters':count,'step_doubling_safety':safety,'summed_local_error_indicators_uncertified':accumulated_indicator}
 if status=='complete_uncertified':result.update(endpoint=[[[float(x.real),float(x.imag)] for x in row] for row in U],unitarity_defect_frobenius=float(np.linalg.norm(U.conj().T@U-I)))
 return result,U
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--B',type=int,default=6);ap.add_argument('--f',type=int,default=0);ap.add_argument('--s',type=int,default=20);ap.add_argument('--seconds',type=float,default=30);ap.add_argument('--safety',type=float,default=.04);ap.add_argument('--tag',default='');a=ap.parse_args()
 r,U=run(a.B,a.f,a.s,a.seconds,a.safety)
 other=Path(__file__).with_name(f'numpy_B{a.B}_f{a.f}_s{a.s}.json')
 if r['status']=='complete_uncertified' and other.exists():
  x=json.loads(other.read_text())
  if 'endpoint' in x:
   V=np.array([[complex(*v) for v in row] for row in x['endpoint']]);r['observed_disagreement_from_normal_form']=float(np.linalg.norm(U-V,2))
 Path(__file__).with_name(f'cf4_B{a.B}_f{a.f}_s{a.s}{a.tag}.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items() if k!='endpoint'},indent=2))
