"""High-precision diagnostic of the critical scale; not interval certification."""
from decimal import Decimal as D, localcontext
from pathlib import Path
import json


def phi(n):
    return D(n)*D(n).ln()-D(n) if n else D(0)


def increment(n,d):
    if not n or n+d<=0:
        return phi(n+d)-phi(n)
    # Avoid subtracting two entropy values at a very large population.
    return D(d)*D(n).ln()+(D(n)+d)*(1+D(d)/D(n)).ln()-d


def drift(a,b,source,jump,k=1):
    rate=D(k)
    for n,y in zip((a,b),source):
        if n<y:return D(0)
        for j in range(y):rate*=n-j
    return rate*(increment(a,jump[0])+increment(b,jump[1]))


rows=[]
with localcontext() as ctx:
    ctx.prec=200
    for n in [10,100,1000,10**6,10**12,10**30]:
        a=n*n;b=n**3
        fast=drift(a,b,(3,0),(-3,2))+drift(a,b,(0,2),(3,-2))
        slow=drift(a,b,(1,1),(1,-1))+drift(a,b,(2,0),(-1,1))
        extreme=drift(a,b,(1,1),(1,-1),D('1e-12'))+drift(a,b,(2,0),(-1,1),D('1e12'))
        value=phi(a)+phi(b)+10
        assert fast>0
        assert fast+slow<0
        if n==10**30: assert fast+extreme<0
        rows.append({'n':str(n),'a':str(a),'b':str(b),'fast_drift_positive':True,
                     'fast_drift_over_n4':str(fast/D(n**4)),
                     'fast_only_entropy_drift_over_V':str(fast/value),
                     'complete_network_drift_negative':fast+slow<0,
                     'extreme_rate_network_drift_negative':fast+extreme<0})
out={'method':'Decimal arithmetic at200 digits; numerical diagnostic, not rigorous interval arithmetic or a proof.',
     'network':'3A<->2B plus A+B<->2A; all sources have order<=3 and exactly one pure cubic source.',
     'extreme_rates':'A+B->2A rate1e-12; 2A->A+B rate1e12; top rates1.',
     'critical_parameterization':'a=n^2,b=n^3,R=a^3/b^2=1',
     'rows':rows}
Path(__file__).with_name('critical_replay.json').write_text(json.dumps(out,indent=2)+'\n')
print('Critical replay passed; the fast-only aligned entropy fails Foster, while the full critical network is eventually negative.')
