"""Exact rational certificate for the finite repeated-word error floor.

The Dyson and contraction inequalities are proved in REPORT.md. This checks
all rational arithmetic and the needed exponential inequality with a finite
positive Taylor sum; it does not perform a huge floating-point matrix power.
"""
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
import json

D=Path(__file__).resolve().parent
d=Q(1,10**9)
m=1/(4000*d**4)
assert m.denominator==1
m=int(m)
C5=Q(276**5,factorial(5))
R=C5*d**5+Q(35848**2,2)*d**8
x=33800*m*d**4
assert x==Q(169,20)
# e^x exceeds this positive partial Taylor sum.
exp_lower=sum((x**j/Q(factorial(j))) for j in range(31))
assert exp_lower>4000
assert m*R<Q(3337,10**6)
floor=1-Q(1,4000)-m*R
assert floor>Q(9964,10000)
# N=ceil(pi/(128 d^5)) exceeds 3/(128 d^5), which already exceeds m.
assert 3/(128*d**5)>m
out={'d':str(d),'m':str(m),'C5':str(C5),'exponent':str(x),
     'exp_partial_sum_terms':31,'exp_partial_sum_exceeds_4000':True,
     'mR_less_than':'3337/1000000','gate_error_strictly_greater_than':'9964/10000'}
print(json.dumps(out,indent=2))
(D/'finite_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
