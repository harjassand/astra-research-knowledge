"""Finite-fair-bit version of the boundary shuffle endpoint sampler.
Sampler theorem assumes independent uniform bits. The runnable default uses
Python's system-backed secrets.randbits. A seeded source is for diagnostics only.
"""
from fractions import Fraction as F
import math,bisect,secrets,json,time
from pathlib import Path
OUT=Path(__file__).resolve().parent
BITS=64;Q=1<<BITS;MAX_COUNT=64;REJECTIONS=32

def table():
    term=F(1);S=term
    for j in range(1,161):term*=F(11,j);S+=term
    nextterm=term*F(11,161)
    exp_upper=S+nextterm/(1-F(11,162))
    p0lo=1/exp_upper;p0hi=1/S
    a=F(1);counts=[];width=F(0)
    for k in range(MAX_COUNT+1):
        if k:a*=F(11,k)
        counts.append((p0lo*a*Q).__floor__());width+=(p0hi-p0lo)*a
    tail=F(11**65,math.factorial(65))/(1-F(11,66))
    count_error=tail+width+F(MAX_COUNT+1,Q)
    counts[0]+=Q-sum(counts)
    cdf=[];v=0
    for c in counts:v+=c;cdf.append(v)
    assert v==Q
    rejection_error=MAX_COUNT*F(5,16)**REJECTIONS+F(1,4)**REJECTIONS
    return cdf,count_error,rejection_error

CDF,COUNT_ERROR,REJECTION_ERROR=table()

def uniform(m,bits):
    n=(m-1).bit_length()
    for _ in range(REJECTIONS):
        u=bits(n)
        if u<m:return u
    return 0 # Failure is explicitly included in the TV budget.

def sample_one(initial=(0,1,2,3,4,5),bits=secrets.randbits):
    assert len(initial)>=3
    n=len(initial);block_size=n-2
    x=list(initial);N=bisect.bisect_right(CDF,bits(BITS))
    for _ in range(N):
        if uniform(11,bits)==0:x[0],x[1]=x[1],x[0]
        else:
            pos=2+uniform(block_size,bits);x[1],x[pos]=x[pos],x[1]
    for pos in range(n-1,2,-1):
        j=2+uniform(pos-1,bits);x[pos],x[j]=x[j],x[pos]
    return x,N

def sampler_error(n):
    def reject(m):
        k=(m-1).bit_length();return F((1<<k)-m,1<<k)**REJECTIONS
    return COUNT_ERROR+MAX_COUNT*(reject(11)+reject(n-2))+sum((reject(m) for m in range(2,n-1)),F(0))

if __name__=='__main__':
    start=time.perf_counter();r=[sample_one() for _ in range(1000)]
    assert all(sorted(x)==list(range(6)) for x,n in r)
    result=dict(count_bits=BITS,max_count=MAX_COUNT,max_rejections=REJECTIONS,poisson_approx_TV_bound=str(COUNT_ERROR),uniform_rejection_TV_bound=str(REJECTION_ERROR),total_sampler_TV_bound=str(COUNT_ERROR+REJECTION_ERROR),total_sampler_TV_bound_float=float(COUNT_ERROR+REJECTION_ERROR),samples_checked=len(r),labels_conserved=True,mean_attempts=sum(n for x,n in r)/len(r),seconds=time.perf_counter()-start,randomness_assumption='independent uniform bits; system secrets.randbits used by this run')
    result['general_formula_error_6']=float(sampler_error(6))
    start=time.perf_counter();larger=[sample_one(tuple(range(12))) for _ in range(10000)]
    result['twelve_site']={'samples_checked':len(larger),'labels_conserved':all(sorted(x)==list(range(12)) for x,n in larger),'mean_attempts':sum(n for x,n in larger)/len(larger),'seconds':time.perf_counter()-start,'sampler_TV_bound_exact':str(sampler_error(12)),'sampler_TV_bound_float':float(sampler_error(12))}
    print(json.dumps({k:v for k,v in result.items() if not k.endswith('_bound')}),flush=True);(OUT/'fair_bit_sampler_results.json').write_text(json.dumps(result,indent=2))
