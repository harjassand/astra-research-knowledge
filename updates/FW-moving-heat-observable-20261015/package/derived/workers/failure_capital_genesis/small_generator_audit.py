"""Independent positive-uniformization check of tiny full target generators.

This enumerates small states only for a cross-check. It is not used by the
large sampler and is not a proof of the general theorem.
"""
import json,math
from fractions import Fraction as F
from pathlib import Path
from collective_bridge_certificate import prepare,run,expneg,decimal,frac,BITS


def exact_target_cdf(m):
    n=m['n'];absorbed=(1<<n)-1
    uniform=n*(1+m['beta']*F(n-1,n*n))
    mu=uniform*m['T'];rows=[]
    for mask in range(1<<n):
        s=mask.bit_count()
        if s==n:rows.append([(mask,F(1))]);continue
        failed=[j for j in range(n) if (mask>>j)&1]
        row=[];total=F(0)
        for i in range(n):
            if (mask>>i)&1:continue
            # Fresh definition-based hazard calculation, not cached columns.
            load=sum(int(m['wi'][i,j]) for j in failed)
            rate=F(n,n-s)*(1+m['beta']*F(load,m['denominator']))
            row.append((mask|(1<<i),rate/uniform));total+=rate/uniform
        assert total<=1
        row.append((mask,1-total));rows.append(row)
    dist=[F(0)]*(1<<n);dist[0]=1
    term=F(1);cdfsum=F(0);j=0
    while True:
        cdfsum+=term*dist[absorbed]
        nxt=term*mu/(j+1)
        if j+2>mu:
            tail=nxt/(1-mu/(j+2))
            if tail<F(1,1<<100):break
        new=[F(0)]*(1<<n)
        for source,v in enumerate(dist):
            if v:
                for dest,p in rows[source]:new[dest]+=v*p
        dist=new;term=nxt;j+=1
    elo,ehi=expneg(mu)
    return [F(elo,1<<BITS)*cdfsum,F(ehi,1<<BITS)*(cdfsum+tail)],j


if __name__=='__main__':
    results=[]
    for n in (4,5,6):
        m=prepare(n,n,F(1,5),F(2));prob,J=exact_target_cdf(m)
        out=run(n,n,F(1,5),F(2),3000,2026101510+n)
        confidence=[F(int(x['numerator']),int(x['denominator'])) for x in out['conditional_95pct_probability_exact']]
        enclosed=confidence[0]<=prob[0]<=prob[1]<=confidence[1]
        results.append(dict(n=n,exact_full_target_cdf=[decimal(x,i==1) for i,x in enumerate(prob)],
                            exact_full_target_rational_interval=[frac(x) for x in prob],uniformization_terms=J,
                            exact_target_over_reference_interval=[decimal(prob[0]/m['h'][1]),decimal(prob[1]/m['h'][0],True)],
                            likelihood_cap=decimal(m['C'],True),
                            fresh_3000_conditional_sample_mean=out['mean'],
                            new_sampler_confidence_interval=out['conditional_95pct_probability_interval'],
                            full_generator_interval_inside_sampler_95pct_interval=enclosed))
        assert enclosed
    saved={'scope':'Small exact rational full-generator consistency check; sampled confidence premise remains iid bits','results':results}
    Path('small_generator_audit.json').write_text(json.dumps(saved,indent=2)+'\n')
    print(json.dumps({**saved,'results':[{k:v for k,v in r.items() if k!='exact_full_target_rational_interval'} for r in results]},indent=2))
