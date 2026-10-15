if not __debug__:
    raise RuntimeError("Run without -O / PYTHONOPTIMIZE; validation assertions are required")
"""Recompute confidence endpoints from saved integer sufficient statistics."""
import json,sys
from fractions import Fraction as Q
import exact_intervals as c
for path in sys.argv[1:]:
 d=json.load(open(path));n=d['N'];s=int(d['sum_units']);ss=int(d['sum_squared_units']);scale=1<<d['scale_bits'];mean=Q(s,n*scale);v=Q(n*ss-s*s,n*(n-1)*scale*scale);x=Q(4383,1000);r=c.I.q(2*v*x/n).sqrt()+7*x/(3*(n-1));r=Q(r.h,c.S);b=Q(d['bias_exact'])
 lo=Q(d['M']['lo'])*max(Q(0),mean-r-b);hi=Q(d['M']['hi'])*min(Q(1),mean+r+b)
 assert lo==Q(d['probability_interval']['lo']);assert hi==Q(d['probability_interval']['hi'])
 print(path, 'exact rational endpoints verified',float(lo),float(hi))
