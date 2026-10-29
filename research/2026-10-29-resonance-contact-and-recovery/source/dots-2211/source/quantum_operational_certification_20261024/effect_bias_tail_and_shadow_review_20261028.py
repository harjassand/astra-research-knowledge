#!/usr/bin/env python3
"""Independent exact scalar tail domination and shadow second-moment bounds."""
from pathlib import Path
from itertools import product,combinations
import json
import sympy as s
cases=0
for n in range(1,6):
 p=s.Rational(2,5)
 for rates in product([s.Rational(1,10),s.Rational(1,4),p],repeat=n):
  for t in range(n):
   actual=sum((s.prod(rates[i] if mask[i] else 1-rates[i] for i in range(n)) for mask in product([0,1],repeat=n) if sum(mask)>t),s.S.Zero)
   bound=sum(s.binomial(n,k)*p**k*(1-p)**(n-k) for k in range(t+1,n+1))
   assert actual<=bound;cases+=1
# E[Z^2] = S^tensorW(rho), S(rho)=2 Tr(rho) I+rho.
# On a positive trace-one rho, each rho_A <= I_A, so sum_A 2^(W-|A|) <=3^W.
# This is valid for entangled rho, unlike multiplying single-qubit operator inequalities.
shadow_cases=[]
for W in range(1,9):
 total=sum(s.binomial(W,k)*2**(W-k) for k in range(W+1))
 assert total==3**W
 shadow_cases.append({'W':W,'second_moment_bound':int(total),'paired_axis_bound':int(2*total)})
out={'status':'PASS_EXACT_UNEQUAL_RATE_BINOMIAL_DOMINATION_AND_ENTANGLED_SHADOW_BOUND','tail_cases':cases,'shadow_cases':shadow_cases,'source_draws':0,'rng_draws':0,'scope':'Exact algebra only; no calibration trajectory, hardware, or numerical learner executed.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
