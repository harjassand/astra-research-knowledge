"""Bounded full cubic compiler and matched raw-body control fixtures."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import sys
import time

import fixed_degree as fd
ac=fd.ac
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from run_comparisons import Teacher as QuadTeacher

HERE=Path(__file__).resolve().parent


class Teacher:
    def __init__(self,n,r,d,seed,prefix_length=None):
        start=time.perf_counter()
        self.n,self.r,self.d,self.h=n,r,d,n-r
        self.k=self.h if prefix_length is None else prefix_length
        self.arbitrary_suffix=prefix_length is not None
        rng=random.Random(seed)
        self.rows=[1 << j for j in range(n)]
        for _ in range(12*n):
            i,j=rng.sample(range(n),2)
            self.rows[i] ^= self.rows[j]
        self.offset=rng.getrandbits(n)
        self.hidden=[]
        for i in range(self.k):
            allowed=list(range(i))+list(range(self.h,n))
            terms={1 << i}
            for mask in fd.points(len(allowed),d):
                if rng.getrandbits(1):
                    terms.add(ac.combine([1 << j for j in allowed],mask))
            self.hidden.append(fd.Polynomial(n,d,terms))
        self.calls=self.rank_requests=self.fresh_ranks=0
        self.cache={}
        self.callback_seconds=0.0
        self.setup_seconds=time.perf_counter()-start
        self.seed=seed
    def rank(self,x):
        self.rank_requests+=1
        if x not in self.cache:
            self.fresh_ranks+=1
            u=ac.linear(self.rows,x)^self.offset
            prefix=0
            for q in self.hidden:
                prefix=(prefix<<1)|q(u)
            if self.arbitrary_suffix:
                m=self.n-self.k
                value=(prefix<<m)|QuadTeacher._demo_suffix(u>>self.k,prefix,m)
            else:
                value=(prefix<<self.r)|(u>>self.h)
            self.cache[x]=value
        return self.cache[x]
    def query(self,x,y):
        start=time.perf_counter()
        self.calls+=1
        answer=self.rank(x)<self.rank(y)
        self.callback_seconds+=time.perf_counter()-start
        return answer
    def receipt(self):
        return dict(comparison_calls=self.calls,fresh_ranks=self.fresh_ranks,
                    rank_requests=self.rank_requests,cached_points=len(self.cache),
                    logical_cache_bits=2*self.n*len(self.cache),
                    query_argument_bits=2*self.n*self.calls,answer_bits=self.calls,
                    setup_seconds=self.setup_seconds,callback_seconds=self.callback_seconds,
                    source_class='synthetic hidden-affine degree-bounded triangular prefix',
                    actual_source_defect_promise=self.r,
                    class_acquisition='supplied, not acquired',physical_fair_entropy='not acquired')


def check_parameters(cfg):
    beta=Fraction.from_float(cfg['beta'])
    n,r,d,m=cfg['n'],cfg['r'],cfg['degree'],cfg['stages']
    if not m:
        return dict(exact_budget_checks=True)
    p=Fraction(1,1 << (r+1))
    assert (1-p)**cfg['R']<=beta/(4*m)
    raw_delta=beta/((2 if cfg['mode']=='raw_body' else 4)*m*cfg['R'])
    assert (1-Fraction(1,1 << (2*d)))**cfg['raw_t']<=raw_delta
    if cfg['mode']=='safe_subspace':
        mem_delta=beta/(4*m*max(cfg['member_trial_caps']))
        assert (1-Fraction(1,1 << (d-1)))**cfg['member_t']<=mem_delta
        # Chernoff mgf with lambda=log2: exp[-pN(1-log2)/2] < exp[-pN/8].
        # Exact alternative mgf after taking powers to clear p denominator.
        for k,N in enumerate(cfg['member_trial_caps']):
            target=cfg['h']-k
            assert N*p>=2*target
            # exp inequality is checked numerically with a large safety margin;
            # the exact actual-binomial tail below uses rational arithmetic.
            # Sum probabilities of <target successes under Ber(p), via recurrence.
            term=(1-p)**N
            tail=term
            for j in range(1,target):
                term=term*Fraction(N-j+1,j)*p/(1-p)
                tail+=term
            assert tail<=beta/(8*m)
    H,P=cfg['tournament_total_attempt_cap'],cfg['tournament_pair_count_cap']
    if P:
        assert H>=4*P
        assert Fraction(16,27)**H<=(beta/8)**4
    return dict(exact_budget_checks=True)


def truth_bodies(source,count):
    vals=[{} for _ in range(count)]
    for x in fd.points(source.n,source.d):
        rank=source.rank(x)
        for i in range(count):
            vals[i][x]=(rank>>(source.n-i-1))&1
    return [fd.interpolate(v,source.n,source.d) for v in vals]


def verify(source,out,model,prefix,prefix_length):
    start=time.perf_counter()
    n,r,d=out['parameters']['n'],out['parameters']['r'],source.d
    fresh,calls=source.fresh_ranks,source.calls
    count=n if prefix_length is None else prefix_length
    truth=truth_bodies(source,count)
    assert [q.body() for q in model]==[q.body() for q in truth]
    inv=ac.matrix_inverse(source.rows,n)
    flag=[ac.linear(inv,1 << j) for j in range(source.h)]
    for i,q in enumerate(truth[:len(prefix.q)]):
        assert q.toggles(flag[i])
        assert all(q.invariant(v) for v in flag[i+1:])
    assert sum(s['exact_update']['constant_translation_codimension'] for s in out['stages'])==out['stages'][-1]['defect_after']<=r
    sampler=prefix.sampler()
    assert sampler.k<=sampler.d<=sampler.k+r
    for q,F in zip(prefix.q,sampler.F):
        factor=fd.interpolate({x:F(ac.linear(sampler.L,x)) for x in fd.points(n,d)},n,d)
        assert factor.body()==q.body()
    rng=random.Random(source.seed+7000000)
    targets={0,(1 << len(prefix.q))-1,rng.getrandbits(len(prefix.q))}
    for target in targets:
        seeds=[rng.getrandbits(n-len(prefix.q)) for _ in range(16)]
        outputs=[sampler.sample_from_seed(target,s) for s in seeds]
        assert len(set(outputs))==len(set(seeds))
        assert all(source.rank(x)>>(n-len(prefix.q))==target for x in outputs)
    ranks=[rng.getrandbits(n) for _ in range(128)]
    if prefix_length is None:
        def learned_rank(x):
            value=0
            for q in model:
                value=(value<<1)|q(x)
            return value
        assert all(learned_rank(x)==source.rank(x) for x in ranks)
        inverse_targets=[rng.getrandbits(n) for _ in range(32)]
        for target in inverse_targets:
            hits=[x for x in sampler.fiber(target>>r) if learned_rank(x)==target]
            assert len(hits)==1 and source.rank(hits[0])==target
    else:
        assert all(sampler.prefix(x)==source.rank(x)>>(n-prefix_length) for x in ranks)
        inverse_targets=[]
    full_kernel_checked=0
    if n<=8:
        exact={v for v in range(1 << n) if all(q.invariant(v) for q in prefix.q)}
        found={ac.combine(prefix.S,bits) for bits in range(1 << len(prefix.S))}
        assert exact==found
        full_kernel_checked=1 << n
    # Independently check that full update retained EVERY future source toggle,
    # including directions that the W sampler never needed to acquire.
    retained=ac.echelon(prefix.S,n)[0]
    for v in flag[len(prefix.q):]:
        assert len(ac.echelon(retained+[v],n)[0])==len(retained)
    out['verification']=dict(all_raw_bodies_equal=True,body_count=count,
                anchors_per_body=fd.M(n,d),sampled_rank_points=len(ranks),rank_errors=0,
                inverse_targets=len(inverse_targets),inverse_errors=0,
                exact_full_stabilizer_vectors_checked=full_kernel_checked,
                factor_identity_coefficients_checked=len(prefix.q)*fd.M(n,d),
                quotient_dimension=sampler.d,prefix_entropy_bits=n-len(prefix.q),
                all_future_source_toggles_retained=True,
                post_return_fresh_ranks=source.fresh_ranks-fresh,
                source_comparisons=source.calls-calls,seconds=time.perf_counter()-start)
    assert source.calls==calls
    return out


def run(n,r,d,seed,mode,prefix_length=None,source_r=None):
    source=Teacher(n,r if source_r is None else source_r,d,seed,prefix_length)
    out,model,prefix=fd.acquire(n,r,d,source.query,seed+1000000,n**-2,prefix_length,mode)
    out['source']=source.receipt()
    out['case']=dict(n=n,r=r,degree=d,seed=seed,mode=mode,prefix_length=prefix_length,source_r=source_r)
    out['parameter_checks']=check_parameters(out['parameters'])
    out['learner_local_seconds_estimate']=max(0,out['acquisition_seconds']-source.callback_seconds)
    if model is not None:
        out=verify(source,out,model,prefix,prefix_length)
    out['logical_output_bits']=len(model or [])*fd.M(n,d)+n*len(prefix.toggles)
    return out


def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',default='8:3:3:940083')
    parser.add_argument('--modes',default='safe_subspace,raw_body')
    parser.add_argument('--prefix-k',type=int)
    parser.add_argument('--source-r',type=int)
    args=parser.parse_args()
    n,r,d,seed=map(int,args.case.split(':'))
    label=f'n{n}_r{r}_d{d}_seed{seed}'
    if args.prefix_k is not None:label+=f'_prefix{args.prefix_k}'
    if args.source_r is not None:label+=f'_source_r{args.source_r}'
    receipt=dict(scope='full comparison-only fixed-degree synthetic prototype; not class recognition or physical acquisition',
        source_hashes={f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in ('fixed_degree.py','run_degree.py')},cases=[])
    for mode in args.modes.split(','):
        out=run(n,r,d,seed,mode,args.prefix_k,args.source_r)
        receipt['cases'].append(out)
        (HERE/f'receipt_{label}.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print(json.dumps(dict(n=n,r=r,d=d,mode=mode,status=out['status'],queries=out['comparison_calls'],
              bodies=out.get('verification',{}).get('all_raw_bodies_equal'),
              seconds=round(out['acquisition_seconds'],3))),flush=True)


if __name__=='__main__':
    main()
