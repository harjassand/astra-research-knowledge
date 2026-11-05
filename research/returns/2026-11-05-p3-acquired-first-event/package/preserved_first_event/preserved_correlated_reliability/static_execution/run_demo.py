"""One actual acquisition demonstration; exact enumeration is validation only."""
from collections import Counter
from dataclasses import asdict
from fractions import Fraction as F
from pathlib import Path
import json,time,sys
from gibbs_static import (fixture,PinnedHeatbath,HeavyPrefixPartitions,
    CutUnionAcquisition,pins_of_mask,RationalBits,RandomCapError)
from exact_reference import ExactReference

HERE=Path(__file__).resolve().parent

def jvalue(v):
    if isinstance(v,F):return {'numerator':str(v.numerator),'denominator':str(v.denominator),'decimal':float(v)}
    if isinstance(v,dict):return {str(k):jvalue(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [jvalue(x) for x in v]
    return v

def save(name,x):
    p=HERE/name;tmp=p.with_suffix(p.suffix+'.tmp')
    tmp.write_text(json.dumps(jvalue(x),indent=2)+'\n');tmp.replace(p)

def main():
    started=time.perf_counter()
    model,network=fixture();cuts=network.all_cuts()
    assert model.chi<1 and model.logarithmic_contrast(3)
    print('fixture ready',float(model.chi),len(cuts),flush=True)
    ref_start=time.perf_counter();reference=ExactReference(model,network)
    # These checks exhaust only this explicit fixture. They do not acquire
    # its partition functions for the algorithm.
    max_conditional_error=F(0)
    for x in range(1<<model.m):
        for i in range(model.m):
            lo=x&~(1<<i);hi=lo|(1<<i)
            direct=reference.weights[hi]/(reference.weights[lo]+reference.weights[hi])
            max_conditional_error=max(max_conditional_error,abs(direct-model.conditional(i,x)))
        mult=sum((x&c)==c for c in cuts)
        assert mult==2**(network.components(x)-1)-1
        assert bool(mult)==network.disconnected(x)
    assert max_conditional_error==0
    zcuts_exact=[reference.partition(pins_of_mask(c,model.m)) for c in cuts]
    sum_exact=sum(zcuts_exact,F(0))
    inv_exact=F(0)
    for c in cuts:
        for x,w in enumerate(reference.weights):
            if (x&c)==c:
                mult=sum((x&cc)==cc for cc in cuts)
                inv_exact+=w/(sum_exact*mult)
    assert sum_exact*inv_exact==reference.fail_weight
    ref_seconds=time.perf_counter()-ref_start
    print('exact reference p =',float(reference.p),'identity checks passed',flush=True)
    save('RUN_PROGRESS.json',{'status':'reference complete, acquisition running','p_exact':reference.p,'reference_seconds':ref_seconds})

    sampler=PinnedHeatbath(model,seed=20261104)
    partitions=HeavyPrefixPartitions(sampler,stage_halfwidth=F(1,40),tau=F(1,10000),delta=F(1,100),max_stages=320)
    acquire_start=time.perf_counter()
    engine=CutUnionAcquisition(model,network,cuts,partitions,seed=20261105)
    partition_seconds=time.perf_counter()-acquire_start
    partition_counts={'draws':sampler.total_draws,'heatbath_updates':sampler.total_updates,
        'sampled_stages':partitions.used_stages,'samples_per_stage':partitions.n_per_stage}
    records=[]
    for z,exact,label in [(engine.z0,reference.Z,'unconditioned')]+[(z,e,f'cut {c}') for z,e,c in zip(engine.zcuts,zcuts_exact,cuts)]:
        records.append({'query':label,'pins':z.pins,'configuration':z.state,
            'estimate':z.estimate,'lower':z.lower,'upper':z.upper,'exact':exact,
            'relative_error':z.estimate/exact-1,'interval_contains_exact':z.lower<=exact<=z.upper,
            'new_draws':z.draws,'branches':[asdict(b) for b in z.branches]})
    print('partitions acquired',partition_counts,'seconds',partition_seconds,flush=True)
    save('RUN_PROGRESS.json',{'status':'partitions acquired','partition_counts':partition_counts,'partition_seconds':partition_seconds,
        'all_intervals_contain_exact':all(r['interval_contains_exact'] for r in records)})

    estimate_start=time.perf_counter()
    before=(sampler.total_draws,sampler.total_updates)
    estimate=engine.estimate_probability(n=8192,tau=F(1,10**7),delta=F(1,100),halfwidth=F(1,32))
    estimate_seconds=time.perf_counter()-estimate_start
    estimate_counts={'draws':sampler.total_draws-before[0],'heatbath_updates':sampler.total_updates-before[1]}
    print('p estimate',float(estimate.estimate),'relative error',float(estimate.estimate/reference.p-1),flush=True)

    conditional_start=time.perf_counter();before=(sampler.total_draws,sampler.total_updates)
    states,conditional_info=engine.conditional_samples(n=8192,tau=F(1,10**8),abort_delta=F(1,10**6))
    hist=Counter(states)
    assert all(network.disconnected(x) for x in states)
    conditional_seconds=time.perf_counter()-conditional_start
    conditional_counts={'draws':sampler.total_draws-before[0],'heatbath_updates':sampler.total_updates-before[1]}
    exact_marginals=reference.conditional_failure_marginals()
    empirical_marginals=[F(sum(n for x,n in hist.items() if (x>>i)&1),len(states)) for i in range(model.m)]
    conditional_tv_empirical=reference.conditional_empirical_tv(hist,len(states))
    independent_probability=reference.independent_same_marginals_failure()
    maxden=max(q.denominator.bit_length() for tab in model.conditionals for q in tab)
    payload={
      'status':'completed','scope':'Static acquisition only; no dynamics or CDF simulation.',
      'randomness':'Reproducible PRNG diagnostic. Mathematical probability guarantees assume independent fair random words/bits.',
      'fixture':{'vertices':network.n,'edges':network.edges,'binary_variables':model.m,'reference_states':1<<model.m,
        'cuts':cuts,'factor_tables':[{'scope':f.scope,'values':f.values} for f in model.factors],
        'dobrushin_chi':model.chi,'dobrushin_rows':[sum(r.values(),F(0)) for r in model.influences],
        'logarithmic_contrast_c':3,'logarithmic_contrast_exactly_verified':True,'ordinary_odds_contrast':model.odds_contrast(),
        'q_lower':model.qlo,'q_upper':model.qhi,'rational_cut_weights':model.cut_weights,
        'max_transition_denominator_bits':maxden},
      'reference':{'partition':reference.Z,'failure_probability':reference.p,'cut_union_overcount':sum_exact/reference.fail_weight,
        'inverse_multiplicity_mean':inv_exact,'independent_same_marginals_failure':independent_probability,
        'correlated_over_independent_ratio':reference.p/independent_probability,
        'all_1024_states_cut_identity':True,'all_10240_local_conditionals_exact':True,'inverse_multiplicity_identity_exact':True},
      'execution_settings':{'initialization':'Fresh chain at pinned bits and all unpinned bits zero on every draw.',
        'sampled_marginal_halfwidth':partitions.halfwidth,'partition_sampler_tau':partitions.tau,
        'partition_confidence_failure_budget':partitions.delta,'max_sampled_stages':partitions.max_stages,
        'samples_per_sampled_stage':partitions.n_per_stage,'union_inverse_mean_halfwidth':F(1,32),
        'union_mean_failure_budget':F(1,100),'union_sampler_tau':F(1,10**7),'conditional_sampler_tau':F(1,10**8),
        'all_cut_enumeration':'All 31 cuts explicitly enumerated only for this small fixture; generic near-cut listing is not implemented here.',
        'point_estimates_vs_certificates':'Actual intervals are reported. This diagnostic execution does not claim the parent theorem fixed global epsilon schedule was executed.'},
      'partition_acquisition':{'counts':partition_counts,'queries':records,
        'all_intervals_contain_exact':all(r['interval_contains_exact'] for r in records),
        'max_point_relative_error':max(abs(r['relative_error']) for r in records),
        'categorical_denominator_bits':engine.cat.total.bit_length()},
      'union_acquisition':{**asdict(estimate),'exact':reference.p,
        'relative_error':estimate.estimate/reference.p-1,'interval_contains_exact':estimate.lower<=reference.p<=estimate.upper,
        'interval_lower_over_exact':estimate.lower/reference.p,'interval_upper_over_exact':estimate.upper/reference.p,
        'counts':estimate_counts},
      'conditional_acquisition':{'accepted':len(states),'all_outputs_fail':True,'histogram':dict(hist),
        'exact_marginals':exact_marginals,'empirical_marginals':empirical_marginals,
        'max_marginal_abs_error':max(abs(a-b) for a,b in zip(empirical_marginals,exact_marginals)),
        'empirical_histogram_TV':conditional_tv_empirical,
        'note':'Empirical histogram distance includes finite output sampling noise; it is not a proof of output-law TV.',
        **conditional_info,'counts':conditional_counts},
      'primitive_counts':{'total_pinned_draws':sampler.total_draws,'total_heatbath_updates':sampler.total_updates,
        'heatbath_random_integer_operations':sampler.total_random_calls,'heatbath_64bit_prng_words':sampler.total_random_words64,
        'python_random_integer_operations':engine.rng.calls,'python_prng_bits':engine.rng.bits,
        'heatbath_random_cap_abort_bound':sampler.total_cap_abort_bound,
        'python_random_cap_abort_bound':F(engine.rng.operation_cap,1<<engine.rng.retries),
        'sample_batches':len(sampler.batches),'max_steps_per_chain':max(b['steps'] for b in sampler.batches),
        'min_steps_per_nontrivial_chain':min(b['steps'] for b in sampler.batches if b['steps']>0)},
      'conservative_parent_schedule_not_executed':HeavyPrefixPartitions.worst_case_plan(model,len(cuts)+1,F(1,10),F(1,100)),
      'wall_seconds':{'reference_and_exact_identity_checks':ref_seconds,'partition_acquisition':partition_seconds,
        'union_acquisition':estimate_seconds,'conditional_acquisition':conditional_seconds,'total':time.perf_counter()-started}
    }
    save('results.json',payload)
    save('RUN_PROGRESS.json',{'status':'completed','results':'results.json','total_seconds':payload['wall_seconds']['total']})
    concise={'p_exact':float(reference.p),'p_estimate':float(estimate.estimate),'relative_error':float(estimate.estimate/reference.p-1),
        'confidence_interval':[float(estimate.lower),float(estimate.upper)],
        'conditional_outputs':len(states),'empirical_conditional_tv':float(conditional_tv_empirical),
        'max_conditional_marginal_error':float(payload['conditional_acquisition']['max_marginal_abs_error']),
        'counts':payload['primitive_counts'],'wall_seconds':payload['wall_seconds']}
    print(json.dumps(jvalue(concise),indent=2),flush=True)

if __name__=='__main__':main()
