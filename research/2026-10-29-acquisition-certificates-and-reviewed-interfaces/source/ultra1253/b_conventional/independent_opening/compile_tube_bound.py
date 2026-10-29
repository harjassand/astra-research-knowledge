"""Exact scalar composition of Eq(17), consuming the frozen native norms."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import time

start=time.perf_counter()
here=Path(__file__).resolve().parent
raw=(here/'RESULT.json').read_bytes()
source=json.loads(raw)
M,f,g=[F(source['native_norm_bounds'][k]) for k in ['Q','f','g']]
a=F(1,128)
assert (M+a)**2<17

def add(p,q):
    return [(p[j] if j<len(p) else F(0))+(q[j] if j<len(q) else F(0))
            for j in range(max(len(p),len(q)))]

def mul(p,q):
    out=[F(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q): out[i+j]+=x*y
    return out

def scale(p,s): return [x*s for x in p]

v=[M+a,F(1)]
v2=mul(v,v)
v4=mul(v2,v2)
ac=g+256*f
p=mul(add(scale(v2,2),v4),[f+(2*M+a)*ac,ac])
assert len(p)==6 and all(c>=0 for c in p)
# e^(M+a)^2 < e^17 < 3^17; no floating exponential is a premise.
bound=3**17*sum(c*math.factorial(j) for j,c in enumerate(p))
out={
    'status':'FIXED_GLOBAL_COMPLEX_TUBE_BOUND_ACQUIRED',
    'input_result_sha256':hashlib.sha256(raw).hexdigest(),
    'tube':'||Im q||_2 < 1/128, over every real position',
    'supremum_bound_rational':str(bound),
    'supremum_bound_decimal_display':float(bound),
    'proof_of_exponential_overpay':'(M+1/128)^2<17 and e<3, exactly checked first inequality',
    'polynomial_degree':len(p)-1,
    'new_model_cases':0,'new_trajectories':0,
    'execution_seconds':time.perf_counter()-start,
    'compiler_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(here/'TUBE_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','tube','supremum_bound_decimal_display','execution_seconds']},indent=2))
