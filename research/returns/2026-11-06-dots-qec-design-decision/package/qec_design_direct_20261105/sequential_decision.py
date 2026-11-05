"""Exact anytime mixture confidence sequence around the acquired tuple kernel."""
import argparse, hashlib, json, math, resource, sys, time
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import numpy as np
from scipy.optimize import brentq
from scipy.special import gammaln
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'qec_fault_tuple_20261105'))
from exact_sampler import FaultTupleProposal, CountedBits
ALPHA=F(1,3000); TARGET=F(1,10**12)

def outside(n,k,a,D):
    """Exact g(a/D)<=alpha where g=(n+1) choose(n,k) p^k(1-p)^(n-k)."""
    return (n+1)*math.comb(n,k)*pow(a,k)*pow(D-a,n-k)*ALPHA.denominator <= pow(D,n)*ALPHA.numerator

def confidence_sequence(n,k,bits=30):
    D=1<<bits
    const=math.log(n+1)+gammaln(n+1)-gammaln(k+1)-gammaln(n-k+1)-math.log(float(ALPHA))
    def fn(p):
        if p<=0:return -math.inf if k else const
        if p>=1:return -math.inf if k<n else const
        return const+k*math.log(p)+(n-k)*math.log1p(-p)
    mode=k/n
    if k==0:lo=0
    else:
        try: lo=max(0,math.floor(D*brentq(fn,0,mode,xtol=1e-15)))
        except Exception:lo=0
        if lo/D>mode or not outside(n,k,lo,D):
            a,b=0,min(D,math.floor(mode*D))
            while b-a>1:
                mid=(a+b)//2
                if outside(n,k,mid,D):a=mid
                else:b=mid
            lo=a
    if k==n:hi=D
    else:
        try:hi=min(D,math.ceil(D*brentq(fn,mode,1,xtol=1e-15)))
        except Exception:hi=D
        if hi/D<mode or not outside(n,k,hi,D):
            a,b=max(0,math.ceil(mode*D)),D
            while b-a>1:
                mid=(a+b)//2
                if outside(n,k,mid,D):b=mid
                else:a=mid
            hi=b
    assert (k==0 or outside(n,k,lo,D)) and (k==n or outside(n,k,hi,D))
    assert F(lo,D)<=F(k,n)<=F(hi,D)
    return F(lo,D),F(hi,D)

def run(d,maxshots=100000,batch=250):
    started=time.perf_counter(); P=FaultTupleProposal(ROOT/'qec_fault_tuple_20261105'/f'd{d}')
    seed={19:202611051919,23:202611052323}[d];rng=CountedBits(seed)
    tv=F(P.meta['conversion_TV_upper_exact']); counts=Counter();records=[];decoder_calls=steps=0
    confidence_seconds=0.;sampling_seconds=0.;decision='inconclusive';n=0
    while n<maxshots:
        t=time.perf_counter()
        for _ in range(min(batch,maxshots-n)):
            value,kind,length,decoded,score=P.trial(rng); counts[kind]+=1;decoder_calls+=decoded;steps+=length;n+=1
        sampling_seconds+=time.perf_counter()-t;t=time.perf_counter()
        lo,hi=confidence_sequence(n,counts['accepted']);L=max(F(0),P.Z*lo-tv);U=min(F(1),P.Z*hi+tv)
        confidence_seconds+=time.perf_counter()-t
        if U<=TARGET:decision='pass'
        elif L>TARGET:decision='reject'
        record={'n':n,'k':counts['accepted'],'failure_interval_exact':[str(L),str(U)],'failure_interval_float':[float(L),float(U)],'decision':decision}
        records.append(record);print(json.dumps(record),flush=True)
        (ROOT/f'd{d}_partial.json').write_text(json.dumps(records,indent=2)+'\n')
        if decision!='inconclusive':break
    result={'distance':d,'rounds':d,'target_exact':str(TARGET),'alpha_exact':str(ALPHA),'method':'uniform-beta likelihood mixture anytime confidence sequence; exact outward endpoint checks','seed':seed,'shots':n,'maxshots':maxshots,'batch':batch,'counts':dict(counts),'decision':decision,'failure_interval_exact':[str(L),str(U)],'failure_interval_float':[float(L),float(U)],'acceptance_interval_exact':[str(lo),str(hi)],'normalizer_exact':str(P.Z),'normalizer_float':float(P.Z),'conversion_TV_upper_exact':str(tv),'conversion_TV_upper':float(tv),'interval_includes_conversion_bias':True,'finite_length_tail':0,'sampling_seconds':sampling_seconds,'confidence_seconds':confidence_seconds,'total_seconds':time.perf_counter()-started,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'decoder_calls':decoder_calls,'fault_steps':steps,'endpoint_selection':dict(P.prefix.counters),'requested_random_bits':rng.summary(),'input_hashes':P.hashes,'implementation_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'inspection_records':records,'scope':'Single selected Z-memory observable only. Conditional on ideal independent bits and acquired decoder contract. Reproducible PRNG execution, not hardware validation.'}
    (ROOT/f'd{d}_decision.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--distance',type=int,required=True);v=a.parse_args();run(v.distance)
