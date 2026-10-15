"""Root's local-query rejection transfer, on the certificate's dyadic bridge.

Poisson counts and rational coins are exact under iid fair bits. The bridge's
count truncation and time grid are retained approximations. This probe reports
operation counts and acceptance, not an exact continuous-path implementation.
"""
import argparse,bisect,json,random,time
from fractions import Fraction as F
from pathlib import Path
from collective_bridge_certificate import prepare,expneg,frac,decimal,COIN


def poisson(z,rng):
    if z==0:return 0
    bits=64;R=rng.getrandbits(bits);precision=512
    lo,hi=expneg(z,precision);term=total=F(1);j=0
    while True:
        flo=F(lo,1<<precision)*total;fhi=F(hi,1<<precision)*total
        if F(R+1,1<<bits)<=flo:return j
        if F(R,1<<bits)>=fhi:
            j+=1;term*=z/j;total+=term
        else:
            R=(R<<64)+rng.getrandbits(64);bits+=64
            precision=max(precision,bits+128);lo,hi=expneg(z,precision)


def proposal(m,rng):
    d=bisect.bisect_right(m['cumulative'],rng.randrange(m['total']))
    count=m['k']+d
    ticks=sorted(2*rng.getrandbits(COIN)+1 for _ in range(count))[:m['k']]
    labels=rng.sample(range(m['n']),m['n'])
    history=[];queries=0;entry_reads=0
    for s,i in enumerate(labels[:m['k']]):
        load=int(m['wi'][i,history].sum()) if s else 0
        queries+=1;entry_reads+=s
        q=(1+m['beta']*F(load,m['denominator']))/(1+m['beta']*F(s,m['n']**2))
        if rng.randrange(q.denominator)>=q.numerator:
            return False,queries,entry_reads,0
        history.append(i)
    # Stage envelopes use c_s=beta*s/n², so total intensity is
    # sum_s (beta*s/n)*Delta t_s. No aggregate η values are queried.
    cumulative=[];total=0;last=0
    for s,tick in enumerate(ticks):
        total+=s*(tick-last);cumulative.append(total);last=tick
    z=m['beta']*m['T']*F(total,m['n']*(1<<(COIN+1)))
    marks=poisson(z,rng)
    for _ in range(marks):
        s=bisect.bisect_right(cumulative,rng.randrange(total))
        i=labels[s+rng.randrange(m['n']-s)]
        load=int(m['wi'][i,labels[:s]].sum())
        queries+=1;entry_reads+=s
        reject=F(load,s*m['mod'])
        if rng.randrange(reject.denominator)<reject.numerator:
            return False,queries,entry_reads,marks
    return True,queries,entry_reads,marks


def run(N,seed,n=400):
    start=time.monotonic();m=prepare(n,n,F(1,5),F(2));prep=time.monotonic()-start
    rng=random.Random(seed);accepted=0;queries=0;entries=0;marks=0
    start=time.monotonic()
    for _ in range(N):
        success,q,e,v=proposal(m,rng);accepted+=success;queries+=q;entries+=e;marks+=v
    elapsed=time.monotonic()-start
    return dict(scope='Local-query rejection on finite count-truncated, dyadic-time reference. Exact Poisson/rational coins conditional on iid bits; no exact continuous-path claim.',
                n=n,k=n,T=frac(m['T']),beta=frac(m['beta']),proposals_fixed=N,seed=seed,
                accepted=accepted,acceptance=accepted/N,guaranteed_ideal_acceptance_lower=decimal(1/m['C']),
                ideal_C=decimal(m['C'],True),local_eta_queries=queries,interaction_entry_reads=entries,
                mean_local_eta_queries_per_proposal=queries/N,mean_interaction_entry_reads_per_proposal=entries/N,
                poisson_marks_in_jump_passed_proposals=marks,
                query_cost='Each dense eta_i query reads s known interaction entries at stage s. Input read/store n² entries is charged separately. No aggregate column sums are used by proposal.',
                input_read_entries=n*n,prepare_seconds=prep,proposal_seconds=elapsed,
                matrix_sha256=m['matrix_sha256'],count_conditional_tv_upper=decimal(m['conditional_tail'],True),
                note='Stage-specific cap product improves root uniform e^beta envelope to this C; early jump rejection avoids later queries.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--N',type=int,default=2000)
    p.add_argument('--seed',type=int,default=2026101504);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();out=run(a.N,a.seed);a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
