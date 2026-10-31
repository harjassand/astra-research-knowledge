#!/usr/bin/env python3
"""Exact rational positivity controls for the proved entropy lower bound."""
from fractions import Fraction as F
from math import isqrt
import json

out=[]
for n in [16,256,65536,10**50]:
    q=isqrt(n)
    assert q*q==n and n>=16
    # log n <= sqrt n for n>=16: sqrt n-log n is increasing for n>=4,
    # and log16=4log2<4. No floating logarithm or trajectory simulation.
    lower=2*F(n**3,n+1)-n*q
    assert lower>0
    out.append({'n':n,'exact_lower_using_log_n_le_sqrt_n':str(lower),'positive':True})
print(json.dumps({'scope':'unit rates except alpha3=2, mu=1; standard unweighted entropy; analytic inequality, no simulation',
                  'checks':out},indent=2,sort_keys=True),end='')
