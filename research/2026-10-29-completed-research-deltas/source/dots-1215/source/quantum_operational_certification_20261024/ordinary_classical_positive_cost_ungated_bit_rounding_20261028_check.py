#!/usr/bin/env python3
"""Exact scoped checks; not a production SDP or Gaussian sampler."""
from pathlib import Path
import hashlib,json
import sympy as sp
import numpy as np
rng=np.random.default_rng(281104)
worst=1.;margins=[];cases=0
for n in range(1,13):
 for repeat in range(10):
  aa=[int(v) for v in rng.integers(-9,10,size=n)]
  if not any(aa):aa[0]=1
  T=sp.Integer(sum(abs(x) for x in aa))**2;tr=sum(x*x for x in aa)
  assert tr<=T<=n*tr
  w=[sp.Rational(int(v),3) for v in rng.integers(0,30,size=n)];m=sp.Rational(repeat+1,7);c=m+sum(w)/2
  s=[1 if x>=0 else -1 for x in aa]
  zplus=[(1+x)//2 for x in s];zminus=[1-x for x in zplus]
  a0=sp.Rational((-1)**repeat,100)*sum(abs(x) for x in aa)
  assert a0*a0<T/64
  nums=[(a0+sum(ai*zi for ai,zi in zip(aa,z)))**2 for z in [zplus,zminus]]
  costs=[m+sum(wi*zi for wi,zi in zip(w,z)) for z in [zplus,zminus]]
  EN=sum(nums)/2;Eu=sum(costs)/2;t=T/(128*c)
  assert Eu==c and EN>=3*T/64 and EN-t*Eu>=5*T/128
  assert max(nums)<=(2*n+sp.Rational(1,32))*T
  success=sp.Rational(sum(int(bool(N>t*u)) for N,u in zip(nums,costs)),2)
  assert success>=sp.Rational(1,128*n)
  worst=min(worst,float(success));margins.append(float((EN-t*Eu)/T));cases+=1
for n in range(1,101):
 assert sp.Rational(5,512*n+4)>=sp.Rational(1,128*n)
 assert sp.Rational(1,128*n)-sp.Rational(1,512*n)>=sp.Rational(1,256*n)
for eta in [sp.Rational(1,8),sp.Rational(1,16),sp.Rational(1,1000)]:
 assert (1-sp.Rational(1,8))/(1+eta)>=sp.Rational(1,2)
p=Path(__file__).resolve().parent/'ordinary_classical_positive_cost_ungated_bit_rounding_20261028.md'
out={'status':'PASS_AUTHOR_UNGATED_BIT_POLYNOMIAL_ROUNDING','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exact_rank_one_SDP_and_affine_rounding_cases':cases,'exact_trial_cap_inequality_cases':100,'exact_feasibility_repair_cases':3,'minimum_two_outcome_success_probability':worst,'minimum_affine_margin_over_T':min(margins),'scope':'Exact reduced-cube algebra/cap evidence; no production general SDP/Gaussian sampler, CPTP transfer, or independent receipt.'}
p.with_name(p.stem+'_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
