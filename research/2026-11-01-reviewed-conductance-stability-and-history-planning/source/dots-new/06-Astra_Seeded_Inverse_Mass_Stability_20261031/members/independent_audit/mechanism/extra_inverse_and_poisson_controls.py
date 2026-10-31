#!/usr/bin/env python3
from exact_seeded_checks import inverse,comps,ff
from fractions import Fraction as F
from math import prod
import json
cap=inverse('inverse_c_cap_one',[1,10**8,1,1,1,1,2,1],limit=10)
assert cap['c']=='1'
first=inverse('eta_initial_trial_already_sufficient',[1,1,1,F(1,10**6),1,1,2,1],limit=10)
assert len(first['eta_trials'])==1
z=(0,0,0);A=(1,0,0);AAB=(2,1,0);ABB=(1,2,0);AAC=(2,0,1);ACC=(1,0,2)
raw=[(z,A,F(1)),(A,z,F(1)),(AAB,ABB,F(1)),(ABB,AAB,F(1)),(AAC,ACC,F(2)),(ACC,AAC,F(1)),(ABB,ACC,F(4)),(ACC,ABB,F(1))]
means=(F(1),F(1),F(2))
def balance_polynomial(rs,x):return sum(k*(prod(z0**(u0-v0) for z0,u0,v0 in zip(means,u,v))*ff(x,v)-ff(x,u)) for u,v,k in rs)
checks=0
for N in range(13):
 for x in comps(N,3):assert balance_polynomial(raw,x)==0;checks+=1
incompatible=raw[:-2]+[(ABB,ACC,F(1)),(ACC,ABB,F(1))]
res=balance_polynomial(incompatible,(1,2,1));assert res==6
print(json.dumps({'inverse_cap_and_initial_pass_cases':[cap,first],
 'compatible_product_Poisson_adjoint_polynomial_checks':checks,
 'incompatible_neutral_pair_nonzero_adjoint_residual_at_1_2_1':str(res),
 'product_form_scope':'Specific product-Poisson law, including its restriction to the positive-satellite class; not all non-Poisson factorized laws.'},indent=2))
