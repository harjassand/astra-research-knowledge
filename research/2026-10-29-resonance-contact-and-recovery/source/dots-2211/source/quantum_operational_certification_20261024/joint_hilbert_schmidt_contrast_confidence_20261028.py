#!/usr/bin/env python3
"""Exact record/dilation constants and conservative same-bank HS diagnostics."""
from pathlib import Path
import json,hashlib,itertools,math
import sympy as s
import numpy as np
I=s.eye(2);P=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
count=0
for w in [1,2,3]:
 for axes in itertools.product(range(3),repeat=w):
  for signs in itertools.product([-1,1],repeat=w):
   Z=s.ones(1,1)
   for a,b in zip(axes,signs):Z=s.kronecker_product(Z,(I+3*b*P[a])/2)
   assert s.trace(Z.H*Z)==5**w;assert 9*s.trace(Z.H*Z)==9*5**w;count+=1
# Exact real Hermitian basis with rational sqrt2 normalization; dilation equals vector norm.
x=s.Matrix([s.Rational(1,3),s.Rational(-2,5),s.Rational(3,7)])
D=s.zeros(4);D[0,1:]=x.T;D[1:,0]=x
assert D*D==s.diag((x.T*x)[0],1,1,1).multiply_elementwise(s.diag(1,0,0,0))+s.BlockDiagMatrix(s.zeros(1),x*x.T).as_explicit()
# Exact log allowance for Q<=32 and beta=.01.
L=12;Q=32;beta=s.Rational(1,100);target=49*Q/beta
partial=sum((s.Rational(L)**k/s.factorial(k) for k in range(40)),s.S.Zero);assert partial>target
R=s.Integer(17);v=s.Integer(225);Nlist=[4096,16384,65536,262144,1048576,2097152,4194304,8388608]
forecast=[]
def bound(N):
 real=(float(R)*L/3+math.sqrt((float(R)*L/3)**2+2*N*float(v)*L))/N
 upper=s.Rational(math.ceil(real*10**12)+1,10**12)
 assert N*upper*upper-2*R*L*upper/3-2*v*L>=0
 return real,upper
for N in Nlist:
 eta,up=bound(N);forecast.append({'N':N,'HS_radius_float':eta,'certified_rational_HS_upper':str(up),'conditional_regret_at_kappa_0_04_residual_0_004':float((up+s.Rational(1,250))**2/(8*s.Rational(1,25)))})
pilot=Path(__file__).parent/'noncommuting_variational_sampling_pilot_20261028'
data=json.loads((pilot/'convex_rounding_results.json').read_text());rows=[]
for r in data['runs']:
 eta,up=bound(r['N']);k=r['provisional_float_kappa'];e=r['rounded_candidate_residual']+float(up)
 rows.append({'bank':r['bank'],'N':r['N'],'joint_HS_radius':float(up),'observed_fit_residual':r['rounded_candidate_residual'],'provisional_float_kappa':k,'new_inverse_bound':2*e/k if k>0 else None,'new_native_oracle_regret_bound_unclipped':e*e/(8*k) if k>0 else None,'passes_one_percent_native_regret':k>0 and e*e/(8*k)<=.01})
out={'status':'PASS_RECORD_CONSTANTS_AND_RATIONAL_HS_RADIUS_CHECKS','source_outcomes':0,'reused_existing_bank_diagnostics_only':True,'exact_shadow_norm_cases':count,'dilation_dimension_w2':49,'increment_bound_w2':17,'variance_bound_w2':225,'L':12,'predeclared_union_capacity_Q':32,'total_beta':'1/100','exp12_lower_bound_exceeds_union_target':True,'forecast':forecast,'existing_bank_diagnostics':rows,'all_existing_banks_fail_one_percent_target':not any(r['passes_one_percent_native_regret'] for r in rows),'scope':'Exact constants/rational radius checks and reanalysis of numerical pilot fits. Statistical theorem requires separate review; no new acquisition or retroactive hardware/physical-control certification.','sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_suffix('.md'),pilot/'convex_rounding_results.json']}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
