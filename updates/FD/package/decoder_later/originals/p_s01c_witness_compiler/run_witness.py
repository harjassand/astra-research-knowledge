#!/usr/bin/env python3
"""Full chosen-pair compiler fixtures; truth access is confined to this harness."""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import time

import witness_compiler as wc
fd,ac=wc.fd,wc.ac
import run_degree as reference

HERE=Path(__file__).resolve().parent


class Teacher(reference.Teacher):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.work=defaultdict(int)
    def rank(self,x):
        if x not in self.cache:
            self.work['affine_coordinate_parities']+=self.n
            self.work['hidden_polynomial_evaluations']+=len(self.hidden)
            self.work['hidden_anf_monomial_tests']+=sum(len(q.terms) for q in self.hidden)
            self.work['rank_output_bits']+=self.n
            if self.arbitrary_suffix:
                self.work['demo_suffix_evaluations']+=1
        return super().rank(x)
    def receipt(self):
        out=super().receipt()
        out.update(source_work=dict(self.work),
                   source_dense_anf_candidate_draws=sum(fd.M(i+self.r,self.d) for i in range(self.k)),
                   source_affine_setup_row_xors=12*self.n,
                   source_model_logical_bits=self.n*self.n+self.n+len(self.hidden)*fd.M(self.n,self.d),
                   suffix_promise='arbitrary bijective demo suffix; no rank model claim' if self.arbitrary_suffix
                        else 'all outputs degree bounded; defect tail linear')
        out['source_bit_work_charged_proxy']=self.n*(self.work['affine_coordinate_parities']+
             self.work['hidden_anf_monomial_tests'])+self.work['rank_output_bits']
        out['source_bit_work_proxy_scope']='n-bit AND/parity or monomial tests plus output; excludes Python/cache overhead'
        return out
    def pin(self):
        body=dict(n=self.n,r=self.r,d=self.d,k=self.k,seed=self.seed,rows=self.rows,
                  offset=self.offset,hidden_terms=[sorted(q.terms) for q in self.hidden],
                  arbitrary_suffix=self.arbitrary_suffix)
        return hashlib.sha256(json.dumps(body,sort_keys=True).encode()).hexdigest()


def rational_checks(cfg):
    beta=Fraction.from_float(cfg['beta'])
    m,r,d=cfg['stages'],cfg['r'],cfg['degree']
    if not m:
        return dict(exact_rational_budgets=True)
    p=Fraction(1,1 << (r+1))
    assert (1-p)**cfg['R']<=beta/(4*m)
    assert (1-Fraction(1,1 << (2*d)))**cfg['raw_t']<=beta/(4*m*cfg['R']**2)
    if r:
        assert (m+r)*(1-Fraction(1,1 << d))**cfg['outer_L']<=beta/(8*cfg['R'])
        if r>=2:
            nu=Fraction(1,1 << (r-1))
            assert cfg['n']*(1 << r)*(1-nu)**cfg['period_L_max']<=beta/(8*r*cfg['R'])
    P,H=cfg['tournament_pair_count_cap'],cfg['tournament_total_attempt_cap']
    if P:
        assert P<=H/4 and Fraction(16,27)**H<=(beta/4)**4
    if cfg['mode']=='safe_W':
        Nmax=max(cfg['member_trial_caps'])
        assert (1-Fraction(1,1 << (d-1)))**cfg['member_t']<=beta/(8*m*cfg['R']*Nmax)
        for k,N in enumerate(cfg['member_trial_caps']):
            target=cfg['h']-k
            term=(1-p)**N
            tail=term
            for j in range(1,target):
                term*=Fraction(N-j+1,j)*p/(1-p)
                tail+=term
            assert tail<=beta/(8*m)
    assert cfg['failure_bound']<=cfg['beta']+1e-15
    return dict(exact_rational_budgets=True,first_wrong_bounds_separate=True)


def execution(model,prefix,source,prefix_length):
    """Source-free acquired-model execution, followed by separately charged truth checks."""
    sampler=fd.Sampler(prefix.q,prefix.toggles,prefix.S,source.n,ac.Meter())
    d,n,k=sampler.d,source.n,len(prefix.q)
    meter=sampler.meter
    rng=random.Random(source.seed+78000000)
    before_comparisons=source.calls
    before_fresh=source.fresh_ranks
    before_ranks=source.rank_requests
    start=time.perf_counter()
    checks=128 if n>8 else 1 << n
    raw_points=list(range(1 << n)) if n<=8 else [rng.getrandbits(n) for _ in range(checks)]
    def rank(x):
        value=0
        for q in model:
            value=(value << 1)|q(x,meter)
        meter.add('full_rank_outputs')
        return value
    local_values=[rank(x) if prefix_length is None else sampler.prefix(x) for x in raw_points]
    full=prefix_length is None
    acquired_tail_bits=n-k
    inverse_targets=[rng.getrandbits(n) for _ in range(32)] if full else []
    inverses=[]
    for target in inverse_targets:
        hits=[x for x in sampler.fiber(target >> acquired_tail_bits) if rank(x)==target]
        assert len(hits)==1
        inverses.append(hits[0])
    fibers=[]
    for target in {0,(1 << k)-1,rng.getrandbits(k)}:
        seeds=[rng.getrandbits(n-k) for _ in range(16)]
        outputs=[sampler.sample_from_seed(target,seed) for seed in seeds]
        assert len(set(outputs))==len(set(seeds))
        fibers.append((target,outputs))
    local_seconds=time.perf_counter()-start
    # Actual retained static compact representation; dense acquisition objects
    # are not part of this payload, though they remain in the harness for audits.
    payload=dict(quotient_dimension=d,prefix_bits=k,
        compact_polynomial_coefficient_bits=k*fd.M(d,source.d),
        compact_polynomial_sparse_index_bits=sum(len(F.terms)*max(1,d) for F in sampler.F),
        L_bits=n*d,B_bits=(n-d)*d,quotient_toggle_bits=k*d,
        quotient_complement_bits=(d-k)*d,
        coordinate_index_bits=n*max(1,(n-1).bit_length()),
        entropy_bits_per_sample=n-k,
        no_dense_raw_polynomial_or_stabilizer_fields=True,
        full_tail_coefficient_bits=acquired_tail_bits*fd.M(n,source.d) if full else 0)
    # Test-only source ranks after all local operations are finished.
    truth=[source.rank(x) if full else source.rank(x)>>(n-k) for x in raw_points]
    assert truth==local_values
    assert all(source.rank(x)==target for x,target in zip(inverses,inverse_targets))
    for target,outputs in fibers:
        assert all(source.rank(x)>>(n-k)==target for x in outputs)
    assert source.calls==before_comparisons
    return dict(source_comparisons=0,local_seconds=local_seconds,local_operations=dict(meter.ops),
                rank_or_prefix_points=checks,rank_or_prefix_errors=0,
                inverse_targets=len(inverse_targets),inverse_errors=0,
                sampled_fiber_seed_pairs=sum(len(outputs) for _,outputs in fibers),
                compact_payload=payload,
                test_only_truth_rank_requests=source.rank_requests-before_ranks,
                test_only_truth_fresh_ranks=source.fresh_ranks-before_fresh)


def verify(source,out,model,prefix,prefix_length):
    start=time.perf_counter()
    n,r,d=source.n,out['parameters']['r'],source.d
    before=dict(calls=source.calls,ranks=source.rank_requests,fresh=source.fresh_ranks)
    count=n if prefix_length is None else prefix_length
    truth=reference.truth_bodies(source,count)
    assert [q.body() for q in model]==[q.body() for q in truth]
    flag_inv=ac.matrix_inverse(source.rows,n)
    hidden_flag=[ac.linear(flag_inv,1 << j) for j in range(source.h)]
    acquired=[]
    S=[1 << j for j in range(n)]
    constant_spaces=[]
    for stage,q in zip(out['stages'],truth):
        assert q.toggles(stage['direction'])
        assert all(previous.invariant(stage['direction']) for previous in acquired)
        C,_=fd.translation_filtration(q,S,constant_only=True)
        if out['case']['mode']=='witness':
            learned=stage['reconstruction']['constant_space_basis']
            assert len(learned)==len(C)
            assert all(wc.contains(v,C,n) for v in learned)
            constant_spaces.append(dict(stage=stage['stage'],dimension=len(C),exact=True))
        S,_=fd.translation_filtration(q,C)
        acquired.append(q)
    assert len(S)==len(prefix.S) and all(wc.contains(v,S,n) for v in prefix.S)
    for v in hidden_flag[len(prefix.q):]:
        assert wc.contains(v,prefix.S,n)
    defect=sum(stage['exact_update']['constant_translation_codimension'] for stage in out['stages'])
    assert defect==n-len(prefix.q)-len(prefix.S)<=r
    if out['case']['mode']=='witness':
        assert defect==out['witness_totals']['global_drop']
        assert out['witness_totals']['paid_dictionaries']<=defect<=r
    sampler=prefix.sampler()
    for q,F in zip(prefix.q,sampler.F):
        factor=fd.interpolate({x:F(ac.linear(sampler.L,x)) for x in fd.points(n,d)},n,d)
        assert factor.body()==q.body()
    actual_degree=max((m.bit_count() for q in truth for m in q.terms),default=0)
    assert actual_degree<=d
    if n<=8:
        exact={v for v in range(1 << n) if all(q.invariant(v) for q in prefix.q)}
        found={ac.combine(prefix.S,bits) for bits in range(1 << len(prefix.S))}
        assert exact==found
    # All full coefficient-body equalities are exact under degree promise; the
    # smaller rank/inverse checks exercise execution and do not replace them.
    out['verification']=dict(all_raw_bodies_equal=True,body_count=count,
        raw_coefficient_positions_checked=count*fd.M(n,d),actual_output_degree=actual_degree,
        exact_all_constant_spaces=constant_spaces,full_stabilizer_exact_by_filtration=True,
        exhaustive_stabilizer_vectors=(1 << n) if n<=8 else 0,
        all_future_hidden_toggles_retained=True,
        factor_identity_coefficients_checked=len(prefix.q)*fd.M(n,d),
        source_comparisons=source.calls-before['calls'],
        test_only_truth_rank_requests=source.rank_requests-before['ranks'],
        test_only_truth_fresh_ranks=source.fresh_ranks-before['fresh'],
        seconds=time.perf_counter()-start)
    assert out['verification']['source_comparisons']==0
    out['execution']=execution(model,prefix,source,prefix_length)
    return out


def resource_proxy(out,n):
    ops=out['local_operations']
    # Conservative width for the listed XOR/AND/popcount events. It is a scoped
    # bit-operation proxy, not a complete measurement of Python instructions.
    events=('gf2_row_xors','basis_xors','anf_monomial_tests','shifted_monomial_terms',
            'parity_calls','scatter_coordinate_bits')
    out['local_bit_work_charged_proxy']=2*n*sum(ops.get(key,0) for key in events)
    out['bit_work_proxy_events']=list(events)
    out['bit_work_proxy_limit']='scoped listed integer operations only; Python loops/hash/cache overhead excluded; wall time also reported'
    out['acquisition_dense_payload_bits']=len(out['model_bodies'] or [])*fd.M(n,out['parameters']['degree'])+n*(
        len(out['acquired_toggle_vectors'])+len(out['acquired_stabilizer_basis']))
    return out


def run(n,r,d,seed,mode,prefix_length=None,source_r=None,forced=False):
    source=Teacher(n,r if source_r is None else source_r,d,seed,prefix_length)
    source_pin=source.pin()
    out,model,prefix=wc.acquire(n,r,d,source.query,seed+1000000,n**-2,prefix_length,mode,forced)
    out['case']=dict(n=n,r=r,degree=d,seed=seed,mode=mode,prefix_length=prefix_length,
                     source_r=source_r,forced_failure=forced)
    out['source_pin']=source_pin
    out['source_acquisition']=source.receipt()
    out['parameter_checks']=rational_checks(out['parameters'])
    out['learner_local_seconds_estimate']=max(0,out['acquisition_seconds']-source.callback_seconds)
    if model is not None:
        out=verify(source,out,model,prefix,prefix_length)
    else:
        out['verification']=dict(returned_model=False,reason=out['reason'])
    out['source_after_test_only_verification']=source.receipt()
    return resource_proxy(out,n)


def summary(case):
    return dict(n=case['case']['n'],r=case['case']['r'],d=case['case']['degree'],
        prefix_length=case['case']['prefix_length'],mode=case['case']['mode'],
        status=case['status'],reason=case['reason'],comparisons=case['comparison_calls'],
        fresh_source_ranks=case['source_acquisition']['fresh_ranks'],
        source_cache_bits=case['source_acquisition']['logical_cache_bits'],
        query_argument_bits=case['source_acquisition']['query_argument_bits'],
        local_bit_work_charged_proxy=case['local_bit_work_charged_proxy'],
        source_bit_work_charged_proxy=case['source_acquisition']['source_bit_work_charged_proxy'],
        witness_totals=case['witness_totals'],
        raw_or_tournament_comparisons=sum(v for k,v in case['source_calls_by_phase'].items()
                if k in ('raw_pair_validation','certified_zero_tournament')),
        reconstruction_comparisons=sum(v for k,v in case['source_calls_by_phase'].items()
                if k not in ('raw_pair_validation','certified_zero_tournament','tail_enumeration')),
        tail_comparisons=case['source_calls_by_phase'].get('tail_enumeration',0),
        all_bodies_equal=case['verification'].get('all_raw_bodies_equal'),
        actual_output_degree=case['verification'].get('actual_output_degree'),
        acquisition_seconds=round(case['acquisition_seconds'],6),
        learner_local_seconds_estimate=round(case['learner_local_seconds_estimate'],6))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',default='8:3:3:940083')
    parser.add_argument('--modes',default='witness,safe_W,raw_body')
    parser.add_argument('--prefix-k',type=int)
    parser.add_argument('--source-r',type=int)
    parser.add_argument('--force-zero',action='store_true')
    args=parser.parse_args()
    n,r,d,seed=map(int,args.case.split(':'))
    label=f'n{n}_r{r}_d{d}_seed{seed}'
    if args.prefix_k is not None: label+=f'_prefix{args.prefix_k}'
    if args.source_r is not None: label+=f'_source_r{args.source_r}'
    if args.force_zero:label+='_force_zero'
    receipt=dict(scope='whole comparator-only synthetic acquisition; finite execution, not class recognition',
        beta=n**-2,precision='exact GF(2) and strict integer rank comparisons',
        modes=args.modes.split(','),cases=[],source_hashes={
            str(path.relative_to(HERE)):hashlib.sha256(path.read_bytes()).hexdigest()
            for path in [HERE/'witness_compiler.py',HERE/'run_witness.py']+
                list((HERE/'reference_snapshot').rglob('*.py'))})
    for mode in receipt['modes']:
        case=run(n,r,d,seed,mode,args.prefix_k,args.source_r,args.force_zero)
        receipt['cases'].append(case)
        pins={entry['source_pin'] for entry in receipt['cases']}
        assert len(pins)==1
        # On the retained exact fixtures all acquisition bodies are correct; the
        # common raw/tournament transcript must therefore be identical.
        completed=[entry for entry in receipt['cases'] if entry['status'].startswith('returned')]
        if len(completed)>1:
            assert len({tuple(entry['acquired_toggle_vectors']) for entry in completed})==1
            assert len({sum(v for k,v in entry['source_calls_by_phase'].items()
                if k in ('raw_pair_validation','certified_zero_tournament')) for entry in completed})==1
        (HERE/f'receipt_{label}.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print(json.dumps(summary(case)),flush=True)


if __name__=='__main__':
    main()
