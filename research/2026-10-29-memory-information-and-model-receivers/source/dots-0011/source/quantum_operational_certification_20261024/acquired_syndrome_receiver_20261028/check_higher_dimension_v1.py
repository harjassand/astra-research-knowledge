#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import numpy as np,json
HERE=Path(__file__).parent;rng=np.random.default_rng(202610282307);rows=[]
for d in [3,5,7]:
 def N(x):return (np.trace(x)*np.eye(d)-x.T)/(d-1)
 U=np.zeros((d,d));U[0,0]=1
 for a in range(1,d,2):U[a,a+1]=1;U[a+1,a]=-1
 Ks=[]
 for i in range(d):
  for j in range(i+1,d):
   K=np.zeros((d,d));K[i,j]=1/np.sqrt(d-1);K[j,i]=-1/np.sqrt(d-1);Ks.append(K)
 tp=np.max(abs(sum(K.T@K for K in Ks)-np.eye(d)))
 attained=sum(abs(np.trace(U@K))**2 for K in Ks)/d**2
 cand=sum(abs(np.trace(L@K))**2 for L in Ks for K in Ks)/d**2
 assert abs(attained-float(F(2,d*d)))<1e-12 and abs(cand-float(F(2,d*(d-1))))<1e-12
 err=0.;worst_excess=-1.
 for _ in range(100):
  Z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));V,_=np.linalg.qr(Z)
  val=sum(abs(np.trace(V@K))**2 for K in Ks)/d**2
  formula=(d-np.trace(V@V.conj()).real)/(d*d*(d-1));err=max(err,abs(val-formula));worst_excess=max(worst_excess,val-float(F(2,d*d)))
  assert val<=float(F(2,d*d))+1e-12 and abs(val-formula)<1e-12
  assert np.max(abs(N(N(Z))-((d-2)*np.trace(Z)*np.eye(d)+Z)/(d-1)**2))<1e-12
 rows.append({'d':d,'unitary_optimum_exact':str(F(2,d*d)),'candidate_CPTP_value_exact':str(F(2,d*(d-1))),'attaining_unitary_value':attained,'CPTP_candidate_value':cand,'Kraus_TP_error':float(tp),'random_formula_max_error':err,'random_max_excess':worst_excess})
(HERE/'higher_dimension_check_v1.json').write_text(json.dumps({'status':'PASS_EXACT_FORMULAS_AND_FLOATING_CHANNEL_CHECKS','rows':rows},indent=2)+'\n');print(json.dumps(rows,indent=2))
