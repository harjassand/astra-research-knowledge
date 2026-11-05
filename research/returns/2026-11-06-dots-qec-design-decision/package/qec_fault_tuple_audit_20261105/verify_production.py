"""Exact CI readback and instrumented replay of both frozen fixed runs."""
import sys,json,math,time,hashlib,importlib.util
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import numpy as np
P=Path(__file__).resolve().parent;root=P.parent;src=root/'qec_fault_tuple_20261105'
spec=importlib.util.spec_from_file_location('audited_tuple_sampler',src/'exact_sampler.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
started=time.perf_counter();manifest=[]
for line in (src/'PRECOMMIT_SHA256SUMS').read_text().splitlines():
    expected,path=line.split(None,1)
    assert hashlib.sha256((root/path).read_bytes()).hexdigest()==expected
    manifest.append(path)
rows=[]
for d,n,seed in [(13,20000,202611051913),(21,10000,202611052921)]:
    t0=time.perf_counter();r=json.loads((src/f'production_d{d}_{n}.json').read_text())
    meta=json.loads((src/f'd{d}'/'parameters.json').read_text());G=json.loads((src/f'd{d}'/'input_graph.json').read_text())
    assert r['shots']==n and r['seed']==seed and sum(r['counts'].values())==n
    assert r['implementation_sha256']==hashlib.sha256((src/'exact_sampler.py').read_bytes()).hexdigest()
    Z=F(meta['Z_exact']);tv=F(meta['conversion_TV_upper_exact']);assert Z==F(r['normalizer_exact'])
    lo,hi=map(F,r['interval']['acceptance_exact']);L,U=map(F,r['interval']['failure_probability_exact'])
    assert L==max(F(0),Z*lo-tv) and U==min(F(1),Z*hi+tv)
    assert [float(L),float(U)]==r['interval']['failure_probability_float']
    assert float(Z*F(r['counts']['accepted'],n))==r['point_estimate_rounded_model']
    assert r['interval']['finite_length_tail']==0 and r['interval']['alpha_exact']=='1/1000'
    x=r['counts']['accepted'];denbase=1<<24;den=denbase**n;jl=int(lo*denbase);ju=int(hi*denbase)
    def reverse_cdf(k,j):
        term=math.comb(n,k)*j**k*(denbase-j)**(n-k);total=term
        for ell in range(k,0,-1):
            term,remainder=divmod(term*ell*(denbase-j),(n-ell+1)*j)
            assert remainder==0;total+=term
        return total
    assert (den-reverse_cdf(x-1,jl))*2000<=den
    assert reverse_cdf(x,ju)*2000<=den
    assert (den-reverse_cdf(x-1,jl+1))*2000>den
    assert reverse_cdf(x,ju-1)*2000>den
    print(json.dumps({'distance':d,'stage':'exact confidence readback passed','seconds':time.perf_counter()-t0}),flush=True)
    proposal=module.FaultTupleProposal(src/f'd{d}')
    original_decode=proposal.model.decode;original_witness=proposal.model.witness
    colmask=[sum(1<<j for j in e['detectors']) for e in G['errors']]
    labels=[e['logical'] for e in G['errors']]
    event={'decoder_calls':0,'zero_residual_syndromes':0,'original_L0_failures':0};last=[None]
    def checked_decode(e):
        c=original_decode(e);res=e^c;sy=logical=0
        for j in np.flatnonzero(res):sy^=colmask[j];logical^=labels[j]
        assert sy==0 and logical==int(res[proposal.model.cut].sum())%2
        event['decoder_calls']+=1;event['zero_residual_syndromes']+=1
        event['original_L0_failures']+=logical;last[0]=logical;return c
    def checked_witness(e):
        w=original_witness(e);assert bool(w)==bool(last[0])
        if w:assert sum(G['costs'][j]*(2*int(e[j])-1) for j in w)>=0
        return w
    proposal.model.decode=checked_decode;proposal.model.witness=checked_witness
    rng=module.CountedBits(seed);counts=Counter({k:0 for k in r['counts']});steps=decoded=maxsteps=0;maxscore=-10**100
    for i in range(n):
        value,kind,length,used,score=proposal.trial(rng)
        assert value==int(kind=='accepted');counts[kind]+=1;steps+=length;decoded+=used
        maxsteps=max(maxsteps,length);maxscore=max(maxscore,score)
    assert dict(counts)==r['counts'] and steps/n==r['mean_fault_steps']
    assert decoded==r['decoder_calls']==event['decoder_calls']
    assert maxsteps==r['maximum_fault_steps_including_repeat']
    assert maxscore==r['maximum_terminal_or_rejection_score']
    assert rng.summary()==r['random_bits'] and dict(proposal.prefix.counters)==r['endpoint_selection']
    assert event['original_L0_failures']==counts['accepted']+counts['other_witness']
    resource=json.loads((src/f'production_d{d}_{n}_process_resources.json').read_text())
    assert resource['exit_code']==0 and resource['kill_reason'] is None
    assert resource['shots']==n and resource['seed']==seed
    assert resource['full_subprocess_wall_seconds']<1200 and resource['full_subprocess_peak_rss_kib']<2*1024*1024
    assert resource['precommit_manifest_sha256']==hashlib.sha256((src/'PRECOMMIT_SHA256SUMS').read_bytes()).hexdigest()
    row={'distance':d,'shots':n,'seed':seed,'counts_reproduced':dict(counts),
         'event_checks':event,'all_random_bit_and_categorical_counts_reproduced':True,
         'CP_dyadic_numerators':[jl,ju],'CP_denominator':denbase,
         'exact_normalizer':str(Z),'conversion_TV_exact':str(tv),
         'failure_interval_exact':[str(L),str(U)],'failure_interval_float':[float(L),float(U)],
         'production_whole_process_seconds':resource['full_subprocess_wall_seconds'],
         'production_peak_RSS_KiB':resource['full_subprocess_peak_rss_kib'],
         'audit_seconds':time.perf_counter()-t0}
    if d==21:
        assert L>F(1,10**12)
        row['precommitted_target']='P_failure <= 1e-12 per 21-round block'
        row['target_decision']='Fails target in the stated model at individual 99.9% confidence'
    rows.append(row);print(json.dumps({'distance':d,'stage':'all production categories, event and random-bit counts reproduced','seconds':row['audit_seconds']}),flush=True)
out={'status':'PASS: both frozen runs independently read back and fully replayed',
     'manifest_entries_verified':len(manifest),'individual_confidence':.999,
     'two_interval_simultaneous_confidence_at_least':.998,'runs':rows,
     'elapsed_seconds':time.perf_counter()-started,
     'scope':'Fixed projected rational circuit models and decoder; no hardware or optimized-competitor performance claim. Full setup accounting remains separate.'}
(P/'production_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
