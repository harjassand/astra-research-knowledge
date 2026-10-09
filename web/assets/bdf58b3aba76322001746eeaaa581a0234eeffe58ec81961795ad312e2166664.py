#!/usr/bin/env python3
"""Replay exact block construction and scalar constants, not the quantum proof."""
from fractions import Fraction as F
from pathlib import Path
import json
import math

a=F(1,8)
rows=[]
for n in (1,2,4,8,16,32):
    d=8*2**n*math.factorial(n+1)
    p=[a/F(j*(j+1)) for j in range(1,n+1)]
    q=[p[j-1]/2**j for j in range(1,n+1)]
    counts=[d*v for v in q]
    assert all(v.denominator==1 and v>0 for v in counts)
    p0=1-sum(p,F(0)); q0=1-sum(q,F(0)); n0=d*q0
    l0=p0/q0
    assert n0.denominator==1 and n0>0
    assert n0+sum(counts,F(0))==d
    assert p0+sum(p,F(0))==q0+sum(q,F(0))==1
    assert p0>F(7,8) and q0>F(15,16) and F(7,8)<l0<1
    assert p0==1-a*F(n,n+1)
    for k in range(1,n+2):
        tail=sum(p[k-1:],F(0))
        assert tail==a*(F(1,k)-F(1,n+1))
        assert tail<=a/k
    harmonic=sum((F(1,j) for j in range(1,n+2)),F(0))
    cap_ln2=sum((F(j)*p[j-1] for j in range(1,n+1)),F(0))
    assert cap_ln2==a*(harmonic-1)
    assert l0!=2
    rows.append({
      'N':n,'dimension':str(d),'P0':str(p0),'Q0':str(q0),
      'lambda0':str(l0),'block_counts':[str(v.numerator) for v in counts],
      'bulk_count':str(n0.numerator),
      'exact_capacity_expression':f'({cap_ln2})*ln(2)+({p0})*ln({l0})',
      'discrete_tail_certificate':'tail(k)=a*(1/k-1/(N+1)) <= a/k',
      'normalization_and_integrality':'PASS'
    })

# All transcendental comparisons in the proof are reduced to these exact
# rational/power inequalities plus elementary monotonicity and exp(x)>=1+x.
checks={
 'tail_constant_6a_less_1':6*a<1,
 'Xi_sqrt2_upper_square':F(3,2)**2>2,
 'Xi_coefficient_less_6':F(9,4)*F(3,2)+1<6,
 'beta_sqrt48_upper_square':7**2>48,
 'beta_coefficient_less_24':(1+F(3,2))*7+2*F(3,2)+2<24,
 'eta_reference_prefactor_less_2':F(8,7)<2,
 'exp_coefficient_193over24_less_9':F(193,24)<9,
 '24_root_upper_threehalves':24<F(3,2)**192,
 '2_power193over192_upper_3':2**193<3**192,
 'prefactor_bound_684_less_1000':152*F(3,2)*3<1000,
 'optimization_derivative_772_less_13824':F(193,384)*1536==772<13824,
 'epsilon_exponent':F(1)+F(1,192)==F(193,192),
 'ratio_power':F(193,192)/2==F(193,384),
 'optimized_exponent':F(9,13824)-F(1,768)==-F(1,1536),
 'boundary_exponent':F(13824,1536)==9,
 '1000expminus9_less_1':F(5,2)**9>1000,
 '400_constant_squared':9*13824==124416<160000,
 'large_branch_is_trivial':13824<400**2,
 'binary_swapped_center':F(5,8)+F(3,8)==1,
}
assert all(checks.values()),checks

result={
 'status':'EXACT_CONSTRUCTION_AND_CONSTANT_REPLAY_PASS',
 'scope':'Specified exact block constructions and scalar constant reductions; general effect/radius/theorem proofs are in the text',
 'arithmetic':'Python fractions.Fraction and integers; no floating arithmetic',
 'no_optimizer_or_random_scan':True,
 'analytic_observational_radius_upper_bound':'1 nat for every N',
 'analytic_capacity_divergence':'(ln2/8)*(H_(N+1)-1)+P0 ln(lambda0) tends to infinity',
 'constant_checks':checks,
 'construction_replays':rows
}
out=Path(__file__).resolve().parent/'SEPARATION_AND_CONSTANT_REPLAY.json'
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'construction_replays':len(rows),
                  'exact_constant_checks':len(checks),'output':str(out)},indent=2))
