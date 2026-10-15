"""Exact rational feasibility checks for two observationally compatible RC models."""
from fractions import Fraction as F
import csv,json,time,math
import numpy as np
from scipy.optimize import nnls
from mpmath import iv
from compact_model import BASE,make_problem
iv.dps=45

def I(x):return iv.mpf(x.numerator)/x.denominator if isinstance(x,F) else iv.mpf(x)

def exact_feature(s,f):
 q=1-s; r=f*100
 d1=q*q+s*s; dh=q*q+10000*s*s; B=q**3+s*s*(10000-s)
 fac=d1*dh/((q*q+r*r*s*s)*B)
 return fac*q,-fac*r*s

def exact_target(s,t):
 if s==0:return I(1)
 a=2*iv.pi*I(F(str(t))/100)
 if s==1:return a/I(F(9999,10000))
 q=1-s; d1=q*q+s*s; dh=q*q+10000*s*s; B=q**3+s*s*(10000-s)
 return (1-iv.exp(-a*I(q/s)))*I(d1*dh/(q*B))

rr=json.loads((BASE/'results/compact_lp.json').read_text())[-2:]
records=[]; t0=time.perf_counter()
for rec in rr:
 s,f,A,y,bounds,phi=make_problem(rec['fmax_hz'],len(rec['nodes'])-2,rec['eps_mohm'])
 nnA=np.column_stack([A,-A[:,-1]]); xb,_=nnls(nnA,y,maxiter=30000)
 interior=xb[:-1].copy(); interior[-1]-=xb[-1]
 assert np.max(abs(A@interior-y))<rec['eps_mohm']
 nodes=[F(str(x)) for x in rec['nodes']]; freqs=[F(str(x)) for x in rec['frequencies']]
 rows=list(csv.DictReader(open(BASE/'data/cell_001_eis.csv')))
 rows=[r for r in rows if F(r['frequency_hz'])<=F(str(rec['fmax_hz']))]
 yr=[1000*F(r['Z_real_ohm']) for r in rows]; yi=[1000*F(r['Z_imag_ohm']) for r in rows]
 for key in ['lower','upper']:
  x=rec[key]['primal']; theta=F(999999,1000000)
  coefs=[theta*max(F(str(c)),0)+(1-theta)*max(F(str(d)),0) for c,d in zip(x[:-1],interior[:-1])]
  ell=theta*F(str(x[-1]))+(1-theta)*F(str(interior[-1]))
  active=[(s,c) for s,c in zip(nodes,coefs) if c]
  errors=[]
  for j,fq in enumerate(freqs):
   real=F(0); imag=ell*fq/max(freqs)
   for ss,c in active:
    re,im=exact_feature(ss,fq); real+=c*re; imag+=c*im
   errors.extend([abs(real-yr[j]),abs(imag-yi[j])])
  error=max(errors); assert error<F(str(rec['eps_mohm'])), 'Witness violates input box'
  q=sum((I(c)*exact_target(ss,rec['time_s']) for ss,c in active),I(0))
  records.append({'time_s':rec['time_s'],'side':key,'status':'exact-rational-feasible','eps_mohm':rec['eps_mohm'],'max_component_error_mohm':float(error),'response_interval_mohm':[math.nextafter(float(q.a),-math.inf),math.nextafter(float(q.b),math.inf)],'signed_inductance_coefficient_mohm':str(ell),'inductance_H_approx':float(ell)/(1000*2*np.pi*float(max(freqs))),'components':[{'compact_node':str(ss),'positive_mass_mohm':str(c)} for ss,c in active]})
  print({k:v for k,v in records[-1].items() if k not in ['components','signed_inductance_coefficient_mohm']},flush=True)
(BASE/'results/feasible_witnesses.json').write_text(json.dumps(records,indent=2))
print('elapsed_seconds',time.perf_counter()-t0)
