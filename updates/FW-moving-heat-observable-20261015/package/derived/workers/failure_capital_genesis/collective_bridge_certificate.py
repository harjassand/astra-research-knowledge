"""Finite-error collective count bridge for a pinned rational dense model.

All claimed arithmetic after integer-model construction is integer/Fraction.
NumPy only performs exact int64 row/column sums, whose range is checked.
Fixed finite count truncation is approximate and its conditional TV is charged.
Seeded PRNG is a replay aid, not proof of the independent fair-bit premise.
"""
import argparse, bisect, hashlib, json, math, random, time
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path
import numpy as np

BITS=512
COIN=64
TAIL=F(1,1<<100)
WEIGHT_BITS=32


def ceildiv(a,b): return -(-a//b)


def decimal(x, upward=False):
    x=F(x)
    with localcontext() as ctx:
        ctx.prec=55
        ctx.rounding='ROUND_CEILING' if upward else 'ROUND_FLOOR'
        return str(Decimal(x.numerator)/Decimal(x.denominator))


def frac(x):
    return {'numerator':str(x.numerator),'denominator':str(x.denominator)}


def expneg(x,bits=BITS):
    """Enclose exp(-x) at fixed binary scale, with integer Taylor arithmetic."""
    assert x>=0
    squares=0
    while x>F(1,2):
        x/=2;squares+=1
    scale=1<<bits;lo=hi=scale;tl=tu=scale
    for j in range(1,81):
        tl=tl*x.numerator//(x.denominator*j)
        tu=ceildiv(tu*x.numerator,x.denominator*j)
        if j%2:lo-=tu;hi-=tl
        else:lo+=tl;hi+=tu
    rem=ceildiv(tu*x.numerator,x.denominator*81)
    lo=max(0,lo-rem);hi=min(scale,hi)
    for _ in range(squares):
        lo=lo*lo//scale;hi=ceildiv(hi*hi,scale)
    return lo,hi


def prepare(n,k,T,beta):
    assert 1<=k<=n and 0<T<1 and 0<beta<=4
    # Fixed explicit heterogeneous rational matrix; all off-diagonal rows differ.
    # This is an input family, not a physically acquired interaction law.
    mod=65521
    wi=np.empty((n,n),dtype=np.int64)
    for i in range(n):
        for j in range(n):
            wi[i,j]=0 if i==j else ((7919*(i+1)+104729*(j+1)+97*(i+1)*(j+1))%mod)
    assert wi.min()>=0 and wi.max()<mod and n*n*mod<(1<<63)
    columns=[int(x) for x in wi.sum(axis=0)]
    assert len(set(columns))>1 # Count alone cannot lump the target process.
    denominator=mod*n*n
    mu=n*T
    assert mu<k+1
    terms=[F(1)];partial=F(1);d=0
    while True:
        nxt=terms[-1]*mu/(k+d+1)
        tail=nxt/(1-mu/(k+d+2))
        if tail/partial<=TAIL:break
        terms.append(nxt);partial+=nxt;d+=1
    common=math.lcm(*(x.denominator for x in terms))
    ints=[x.numerator*(common//x.denominator) for x in terms]
    cumulative=[];total=0
    for x in ints:total+=x;cumulative.append(total)
    exp_lo,exp_hi=expneg(mu)
    prefactor=mu**k/math.factorial(k)
    hlo=F(exp_lo,1<<BITS)*prefactor*partial
    hhi=F(exp_hi,1<<BITS)*prefactor*(partial+tail)
    C=math.prod(1+beta*F(s,n*n) for s in range(k))
    lcm=math.lcm(*(n-s for s in range(k)))
    scales=[lcm//(n-s) for s in range(k)]
    M=beta*F(k-1,n)
    eta=T/F(1<<(COIN+1))
    zeta=F(1,1<<180)
    bias=C*(tail/partial+2*k*M*eta)+zeta+F(1,1<<WEIGHT_BITS)
    return dict(n=n,k=k,T=T,beta=beta,mod=mod,wi=wi,columns=columns,
                denominator=denominator,mu=mu,D=d,partial=partial,tail=tail,
                conditional_tail=tail/partial,cumulative=cumulative,total=total,
                h=[hlo,hhi],C=C,lcm=lcm,scales=scales,M=M,eta=eta,zeta=zeta,
                bias=bias,matrix_sha256=hashlib.sha256(wi.astype('<i8').tobytes()).hexdigest())


def sample(m,rng):
    d=bisect.bisect_right(m['cumulative'],rng.randrange(m['total']))
    N=m['k']+d
    # Given N, the Poisson event times are ordered independent uniform draws.
    ticks=sorted(2*rng.getrandbits(COIN)+1 for _ in range(N))[:m['k']]
    labels=rng.sample(range(m['n']),m['k'])
    history=[];S=0;HH=0;last=0;J=F(1)
    for s,(tick,i) in enumerate(zip(ticks,labels)):
        HH+=S*(tick-last)*m['scales'][s]
        load=int(m['wi'][i,history].sum()) if s else 0
        colremoved=int(m['wi'][history,i].sum()) if s else 0
        J*=1+m['beta']*F(load,m['denominator'])
        S+=m['columns'][i]-colremoved-load
        assert 0<=S<=m['n']*m['n']*m['mod']
        history.append(i);last=tick
    H=(m['beta']*m['n']*m['T']*HH
       /F(m['denominator']*(1<<(COIN+1))*m['lcm']))
    assert 0<=H<=m['M']*m['T']
    elo,ehi=expneg(H)
    lo=J*F(elo,1<<BITS);hi=min(m['C'],J*F(ehi,1<<BITS))
    assert lo<=hi and hi-lo<=m['zeta']
    value=(lo+hi)/2
    v=(value.numerator*(1<<WEIGHT_BITS))//value.denominator
    assert 0<=F(v,1<<WEIGHT_BITS)<=m['C']
    return v,N


def run(n,k,T,beta,N,seed):
    assert __debug__,'Certificate assertions must remain enabled'
    start=time.monotonic();m=prepare(n,k,T,beta);prep=time.monotonic()-start
    rng=random.Random(seed);sumv=0;sumsq=0;maxN=0;minv=None;maxv=0
    start=time.monotonic()
    for _ in range(N):
        v,count=sample(m,rng);sumv+=v;sumsq+=v*v;maxN=max(maxN,count)
        minv=v if minv is None else min(minv,v);maxv=max(maxv,v)
    elapsed=time.monotonic()-start
    mean=F(sumv,N*(1<<WEIGHT_BITS))
    variance=(F(sumsq,1<<(2*WEIGHT_BITS))-N*mean*mean)/(N-1)
    logupper=F(4383,1000);term=total=F(1)
    for j in range(1,40):term*=logupper/j;total+=term
    assert total>80
    radicand=2*variance*logupper/N;scale=1<<128
    root=math.isqrt(ceildiv(radicand.numerator*scale*scale,radicand.denominator))+1
    radius=F(root,scale)+7*m['C']*logupper/(3*(N-1))
    lower=m['h'][0]*max(F(1),mean-radius-m['bias'])
    upper=m['h'][1]*min(m['C'],mean+radius+m['bias'])
    out=dict(scope='Certified numerical-bias and fixed-N confidence calculation for supplied rational model; coverage conditional on iid fair bits. Seeded PRNG is replay only.',
             model='a_i(x) = n/(n-|x|) * (1 + beta sum_failed wi[i,j]/(65521 n²)), wi exact modular integers',
             n=n,k=k,T=frac(T),beta=frac(beta),matrix_sha256=m['matrix_sha256'],
             input_storage_bytes=m['wi'].nbytes,input_read_entries=n*n,
             count_reference='constant total rate n, uniform distinct event labels',
             uniformization_mu=frac(m['mu']),count_truncation_excess_D=m['D'],
             count_conditional_tv_upper=decimal(m['conditional_tail'],True),
             count_conditional_tv_exact=frac(m['conditional_tail']),
             maximum_count_observed=maxN,clock_bits=COIN,elementary_kernel_bits=BITS,
             reference_probability_interval=[decimal(m['h'][0]),decimal(m['h'][1],True)],
             reference_probability_exact=[frac(x) for x in m['h']],
             likelihood_cap=decimal(m['C'],True),likelihood_cap_exact=frac(m['C']),
             guaranteed_relative_second_moment_upper=decimal(m['C'],True),
             normalized_numerical_bias_upper=decimal(m['bias'],True),normalized_numerical_bias_exact=frac(m['bias']),
             samples_fixed=N,seed=seed,weight_bits=WEIGHT_BITS,sum_weight_units=sumv,sum_squared_weight_units=sumsq,
             mean=decimal(mean),variance=decimal(variance),minimum_weight=decimal(F(minv,1<<WEIGHT_BITS)),maximum_weight=decimal(F(maxv,1<<WEIGHT_BITS)),
             empirical_bernstein_radius_upper=decimal(radius,True),empirical_bernstein_radius_exact=frac(radius),
             conditional_95pct_probability_interval=[decimal(lower),decimal(upper,True)],
             conditional_95pct_probability_exact=[frac(lower),frac(upper)],
             relative_halfwidth_vs_lower_upper=decimal((upper-lower)/(2*lower),True),
             prepare_seconds=prep,sampling_seconds=elapsed,
             source_independence='No source scripts imported or source outputs used to decide this new model probability')
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=400)
    p.add_argument('--k',type=int);p.add_argument('--T',default='1/5');p.add_argument('--beta',default='2')
    p.add_argument('--N',type=int,default=100);p.add_argument('--seed',type=int,default=2026101502)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();out=run(a.n,a.k or a.n,F(a.T),F(a.beta),a.N,a.seed)
    a.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({key:out[key] for key in ['n','k','samples_fixed','seed','reference_probability_interval','likelihood_cap','count_conditional_tv_upper','normalized_numerical_bias_upper','mean','variance','conditional_95pct_probability_interval','relative_halfwidth_vs_lower_upper','prepare_seconds','sampling_seconds']},indent=2))
