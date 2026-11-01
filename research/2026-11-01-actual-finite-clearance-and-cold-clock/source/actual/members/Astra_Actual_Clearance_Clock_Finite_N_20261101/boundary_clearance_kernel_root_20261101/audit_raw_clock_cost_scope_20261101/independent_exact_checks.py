#!/usr/bin/env python3
"""Raw receiver and literal event-interface algebra, not component acquisition."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import hashlib,json
import sympy as s

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
EXPECTED={
 'RAW_CLOCK_RECEIVER_ADDENDUM.md':'8300fe7a019e5739ba644a7eaecd87b7c317c3716694d0a5b3967e3bde6cd153',
 'LITERAL_EVENT_COST_AND_OUTPUT_SCOPE.md':'41f5dd470451a483c635cc9105fd6f532efbdebaea0843c223e2d63eb3b7658c',
 'FINITE_CLOCK_ENDPOINT_RECEIVER.md':'0018c24de9dfa6cf2757a42cbfd3d1b8cb7d37369f46cf2fa5e0f9fac9228919',
}
hashes={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in EXPECTED}
assert hashes==EXPECTED
tail_sum=sum((F(6**k,factorial(k)) for k in range(18)),F(0))
assert tail_sum>400
j,v=s.symbols('j v',nonnegative=True)
general=j*6/3+s.sqrt(2*v*6+(j*6/3)**2)
special=2*j+s.sqrt(12*v+4*j*j)
assert s.simplify(general-special)==0
assert s.simplify(special**2-12*(v+j*special/3))==0

deltas=[(1,0,0,0,0),(-1,0,0,0,0),(-1,0,1,0,0),(1,0,-1,0,0),
        (-1,0,0,1,0),(1,0,0,-1,0),(-1,0,0,0,1),(1,0,0,0,-1),
        (-1,0,1,1,-1),(1,0,-1,-1,1),(1,1,-1,-1,0),(-1,-1,1,1,0)]
lm=[F(h[0])+F(h[2]+h[3],2) for h in deltas]
em=[h[4] for h in deltas]
assert max(map(abs,lm))==1
assert max(map(abs,em))==1
N=10**25
literal=F(N,5000)-1
assert literal==2*10**21-1
assert F(N,100)>=literal

result={
 'status':'PASS_CONDITIONAL_RAW_RECEIVER_AND_LITERAL_EVENT_SCOPE',
 'source_sha256':hashes,
 'exp6_positive_partial_sum':str(tail_sum),
 'exp6_partial_sum_margin_over_400':str(tail_sum-400),
 'log6_freedman_specialization_residual':'0',
 'literal_L_marks':[str(h) for h in lm],'literal_E_marks':em,
 'literal_event_lower_bound_at_N_1e25':str(literal),
 'pending_r_v_j_accepted':False,
 'pending_numerical_join_accepted':False,
 'uniform_general_prediction_complexity_claim_accepted':False,
 'all_assertions_passed':True,
}
(HERE/'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
