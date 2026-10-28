from fractions import Fraction as F
from pathlib import Path
from itertools import product as words
import json, random, resource, time
import factory
import factory_lazy as lazy
from verify import exact_rank

def encode(v):
    if isinstance(v,F): return str(v)
    if isinstance(v,dict): return {str(k):encode(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)): return [encode(x) for x in v]
    return v

def pow2(j):
    return F(2**j) if j>=0 else F(1,2**(-j))

class WordBits:
    def __init__(self,word,length): self.word,self.length,self.used=word,length,0
    def getrandbits(self,n):
        value=0
        for _ in range(n):
            value <<= 1
            if self.used<self.length: value |= (self.word>>(self.length-self.used-1))&1
            self.used+=1
        return value

def exp_bounds(x,terms=100):
    total=term=F(1)
    for j in range(1,terms+1):
        term*=x/j
        total+=term
    return total,total+(term*x/(terms+1))/(1-x/(terms+2))

def main():
    started=time.perf_counter()
    for j in range(-20,21):
        assert lazy.ceil_log2_fraction(pow2(j))==j
        assert lazy.ceil_log2_fraction(pow2(j)*F(3,2))==j+1
        assert lazy.ceil_log2_fraction(pow2(j)*F(3,4))==j
    uniform=[]
    for exponent in range(2,7):
        length=exponent+3
        for offset in (-4,-1,0,1,4):
            p=F(1,2)+offset*pow2(-length)
            heads=0
            for word in range(2**length):
                rng=WordBits(word,length)
                stats={'uniform_bits':0,'exact_elevations':0,'lazy_resolutions':0}
                heads+=lazy.close_half_decision(exponent,lambda:p,rng,stats)
                assert rng.used<=length
            assert F(heads,2**length)==p
            uniform.append([exponent,str(p),2**length])
    intervals=[]
    for n,k in [(4096,0),(4096,683),(4096,2731),(4096,4096),(16384,2731),(16384,10923)]:
        m,x=n//4,F(k,n)
        gap=F(1,4)-x if x<=F(1,4) else x-F(7,12)
        ratio=(F(11,40)+F(297,8)/(8*m))/(2*(factory.radius(m)-factory.radius(n)))
        power=2*m*gap**2
        exponent=power.numerator//power.denominator-lazy.ceil_log2_fraction(ratio)
        p=lazy.conditional_stop_probability(n,k)
        assert abs(p-F(1,2))<=pow2(-exponent)
        old=factory.elevated_center(m,n,k)-factory.radius(m)
        new=factory.center(n,k)-factory.radius(n)
        assert old+2*(factory.radius(m)-factory.radius(n))*p==new
        intervals.append({'degree':n,'heads':k,'dyadic_radius_exponent':exponent})
    profiles=[]
    for numerator in (99,101,399,401):
        cheap_rng=random.Random(91000+numerator)
        private_rng=random.Random(81000+numerator)
        calls=0
        def proxy():
            nonlocal calls
            calls+=1
            return 0 if cheap_rng.randrange(600)<numerator else 1
        exact=fast=0
        degrees=[]
        start=time.perf_counter()
        for _ in range(24):
            stats={}
            assert lazy.factory_output(proxy,private_rng,stats=stats) in (0,1,2)
            degrees.append(stats['degree'])
            exact+=stats['exact_elevations']; fast+=stats['lazy_resolutions']
        profiles.append({'p':F(numerator,600),'outputs':24,'cheap_calls':calls,
                         'degrees':degrees,'exact_elevations':exact,'lazy_resolutions':fast,
                         'wall_s':time.perf_counter()-start,
                         'scope':'Finite seeded Python-PRNG diagnostic, not exact-law or physical evidence'})
    # Force the rare exact-sum branch using the SAME saved uniform prefix.
    rare_stats={'uniform_bits':0,'exact_elevations':0,'lazy_resolutions':0}
    lazy.stop_coin(4096,683,WordBits((1<<100)-1,101),rare_stats)
    assert rare_stats['exact_elevations']==1
    prefix_ranks=[]
    for length in (1,2,3):
        delta=F(1,600*length)
        base=[F(2,3),F(1,6),F(1,6)]
        points=[base,[base[0]+delta,base[1],base[2]-delta],
                     [base[0],base[1]+delta,base[2]-delta]]
        table=[]
        strings=list(words(range(3),repeat=length))
        for choices in strings:
            row=[]
            for word in strings:
                value=F(1)
                for t in range(length): value*=points[choices[t]][word[t]]
                row.append(value)
            table.append(row)
        rank=exact_rank(table)
        assert rank==3**length
        prefix_ranks.append({'prefix_length':length,'rank':rank,'total_tv_perturbation_budget':F(1,600)})
    # Exact rational certificates for the ordinary approximate comparator.
    gap=F(149,600)
    low102,high102=exp_bounds(2*102*gap**2)
    low101,high101=exp_bounds(2*101*gap**2)
    assert F(11,40)/low102 < F(1,10**6)
    assert F(11,40)/high101 > F(1,10**6)
    # Full-TV-ball overlap and common-part lower-bound value.
    midpoint=[F(5,12),F(5,12),F(1,6)]
    l0=[F(2,3),F(1,6),F(1,6)]; l1=[F(1,6),F(2,3),F(1,6)]
    assert all(sum(abs(a-b) for a,b in zip(midpoint,l))/2==F(1,4) for l in (l0,l1))
    result={'status':'EXACT_LAZY_FACTORY_FINITE_CHECKS_PASS; GENERAL_PROOFS_PENDING_INDEPENDENT_AUDIT',
            'uniform_prefix_enumerations':uniform,'exact_interval_checks':intervals,
            'rare_exact_fallback_path':rare_stats,'independent_prefix_perturbation_ranks':prefix_ranks,
            'expected_cheap_calls':F(44351,32),'raw_calls':0,
            'finite_expected_full_bit_work_scope':'Stationary iid stream with positive plateau margin; at TV radius1/600 margin49/600; analytic proof in PROOF_EXTENSION.md',
            'finite_prng_profiles':profiles,
            'ordinary_approximate_comparator':{'cheap_calls':102,'raw_calls':0,'tv_tolerance':F(1,10**6),
                'certified_bound_upper_float_for_display':float(F(11,40)/low102),
                '101_call_bound_lower_float_for_display':float(F(11,40)/high101),
                'certificate':'Exact rational Taylor exp bounds at 100 terms; minimum integer certified by this Hoeffding expression',
                'scope':'Also covers predictable per-draw bias in the separated intervals; no exact-law claim'},
            'runtime':{'wall_s':time.perf_counter()-started,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
    (Path(__file__).resolve().parent/'lazy_verification_results.json').write_text(json.dumps(encode(result),indent=2)+'\n')
    print(json.dumps(encode({'status':result['status'],'profiles':profiles,
                            'approximate_comparator':result['ordinary_approximate_comparator'],
                            'runtime':result['runtime']}),indent=2))

if __name__=='__main__': main()
