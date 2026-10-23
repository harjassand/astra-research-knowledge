"""Bounded exact check of a separately proved all-k Rayleigh witness."""
from itertools import product
from fractions import Fraction
from math import comb
import json, time, resource

def unmatched(bits):
    h=d=0
    for bit in bits:
        if bit:h+=1
        elif h:h-=1
        else:d+=1
    return h,d

def run(max_k=12):
    start=time.perf_counter();rows=[]
    for k in range(2,max_k+1):
        oriented_critical=0
        for bits in product((0,1),repeat=k):
            for i in range(k):
                if bits[i]:continue
                h,_=unmatched(bits[:i])
                for j in range(i+1,k):
                    if not bits[j]:continue
                    _,d=unmatched(bits[i+1:j])
                    oriented_critical += (h==d)
        rayleigh=Fraction(oriented_critical,2**k)
        C=sum((Fraction((k-1-n)*comb(n,n//2),2**n)
               if n%2==0 else Fraction(0)) for n in range(k-1))
        assert rayleigh==C/4
        rows.append({'k':k,'oriented_critical_count':oriented_critical,
                     'rayleigh_exact':str(rayleigh),'C_exact':str(C),
                     'identity':True})
    return {'rows':rows,'wall_seconds':time.perf_counter()-start,
            'peak_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'scope':'Exact bounded token/count check; all-k proof is separate',
            'discovery_inference_review_cost':'unknown'}

if __name__=='__main__':
    result=run()
    path=__file__.replace('.py','.json')
    open(path,'w').write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
