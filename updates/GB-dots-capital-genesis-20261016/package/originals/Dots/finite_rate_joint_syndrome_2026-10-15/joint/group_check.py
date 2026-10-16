import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np,json
from pathlib import Path
from scipy.linalg import expm
results=[]
for k in [1,2,3]:
 d=2**k;J=.03;g=1.;beta=2*g-2*(d-2)*J
 M=np.zeros((d*d,d*d))
 for a in range(d):
  for b in range(d):
   s=a*d+b;M[s,s]=-2*g*(a^b).bit_count()
   for c in range(d):
    if c!=a:M[s,c*d+b]=J
    if c!=b:M[s,a*d+c]=J
 for t in [.05,.5,2.,10.]:
  u=expm(t*M)[:,0].reshape(d,d);A=float(np.trace(u));B=float(u.sum()-A);q=float(A-u[0,0]);omega=np.sqrt(beta*beta/4+4*(d-1)*J*J)
  abar=np.exp(-beta*t/2)*(np.cosh(omega*t)+beta/(2*omega)*np.sinh(omega*t));simple=np.expm1(4*(d-1)*J*J*t/beta)
  assert q<=A-1+1e-12 and A<=abar+1e-12 and abar-1<=simple+1e-12
  # Check the grouped differential coefficient inequalities on this exact u.
  du=(M@u.reshape(-1)).reshape(d,d);Adot=float(np.trace(du));Bdot=float(du.sum()-Adot)
  assert abs(Adot-2*J*B)<1e-12
  assert Bdot<=2*(d-1)*J*A-beta*B+1e-12
  results.append({'k':k,'d':d,'J':J,'gamma':g,'beta':beta,'t':t,'exact_local_majorant_q':q,'scalar_transient_bound':float(abar-1),'simple_exponential_bound':float(simple)})
Path(__file__).with_name('group_checks.json').write_text(json.dumps(results,indent=2));print('12 grouped majorant checks passed; max q/simple bound',max(r['exact_local_majorant_q']/r['simple_exponential_bound'] for r in results))
