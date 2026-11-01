#!/usr/bin/env python3
"""Goal-directed ordinary max-hazard certificate; no row-count union required."""
from pathlib import Path
import gzip,hashlib,json,sys
ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent;sys.path.insert(0,str(PARENT))
from retained_large_acquisition import R,clog2,eb_radius
BASE_SHA='dc7583f0aa94e06f7440a6109a2dbef128b1db35538664a1880f8a5c4c146568'
TASK_SHA='e1d5e9c1a83084d576c411e9586d43c7f4e309984cbd4e542477a9a1a3f5d428'
OBS_SHA='f9ec8eedc6465e9b552f48fdbe15f9f6e3e7ca9e2f78553e4d954d6b697fdd85'


def run(*,expected_length=24,expected_generators=2,expected_confidence=R(1,1000),expected_regret=R(113,2000),expected_task_sha256=TASK_SHA):
    assert type(expected_task_sha256) is str and expected_task_sha256==TASK_SHA
    assert type(expected_length) is int and expected_length==24
    assert type(expected_generators) is int and expected_generators==2
    assert not isinstance(expected_confidence,(bool,float)) and R(expected_confidence)==R(1,1000)
    assert not isinstance(expected_regret,(bool,float)) and R(expected_regret)>0
    base=(PARENT/'history_sensitive_4096_result.json').read_bytes();raw=(PARENT/'history_sensitive_4096_observations.json.gz').read_bytes()
    assert hashlib.sha256(base).hexdigest()==BASE_SHA and hashlib.sha256(raw).hexdigest()==OBS_SHA
    model=json.loads(base);records=json.loads(gzip.decompress(raw))['records']
    comparison=json.loads((ROOT/'interval_comparison_results.json').read_text());n=model['n'];m=model['m'];parts=model['partition']
    assert (model['length'],model['m'],R(model['fixture_tau']))==(expected_length,expected_generators,R(1,25))
    b=model['task_b'];ell=model['task_ell_numer'];den=model['task_ell_denominator']
    assert all(type(x) is int and x in (0,1) for x in b+ell) and sum(ell)==den>0
    assert hashlib.sha256(json.dumps({'b':b,'ell_numer':ell,'ell_denominator':den},sort_keys=True).encode()).hexdigest()==expected_task_sha256
    assert all(not b[i] for i in range(n) if ell[i])
    assert all(len({b[i] for i in p})==1 for p in parts)
    goal_blocks=[g for g,p in enumerate(parts) if b[p[0]]];counts=[[0]*n for _ in range(m)]
    pilots=[z for z in records if z['kind']=='pilot'];assert len(pilots)==m
    for a,z in enumerate(pilots):
        assert z['a']==a and z['N']==2048 and len(z['counts'])==n
        for row in z['counts']:assert len(row)==len(parts) and all(type(c) is int and c>=0 for c in row) and sum(row)==2048
        counts[a]=[sum(row[g] for g in goal_blocks) for row in z['counts']]
    N=2048;delta=R(expected_confidence);K=R(7,10)*clog2(2*6/(delta/2));transport=R(1,10**9)
    attempts=[];first=None;proposal_calls=sum(z['N'] for z in records if z['kind'] in ('column','coarse'))
    for turn,old in enumerate(comparison['attempts']):
        assert old['prefix_round']==turn and turn<6
        selected=[z for z in records if z['kind']=='incoming_pair' and z['turn']==turn]
        Ni=model['cross_rounds'][turn]['incoming_per_row_half'];reps=model['cross_rounds'][turn]['incoming_replicates']
        assert len(selected)==m*reps and sorted((z['a'],z['replicate']) for z in selected)==[(a,j) for a in range(m) for j in range(reps)]
        for z in selected:
            assert z['N']==Ni and len(z['counts'])==2
            for half in z['counts']:
                assert len(half)==n
                for i,row in enumerate(half):
                    assert len(row)==len(parts) and all(type(c) is int and c>=0 for c in row) and sum(row)==Ni
                    counts[z['a']][i]+=sum(row[g] for g in goal_blocks)
        N+=2*Ni*reps;assert N==old['per_row_samples']
        assert old['prospective_total_calls']==proposal_calls+m*n*N+(turn+1)*250000*expected_length
        c=max(v[i] for v in counts for i in range(n) if not b[i]);assert 0<=c<=N
        source_p=R(1) if 2*c>N else min(R(1),R(c,N)+eb_radius(c,N,K))
        p=min(R(1),source_p+transport);upper=1-(1-p)**expected_length
        ev=old['fresh_policy_evaluation'];assert R(ev['confidence'])==delta/6 and ev['episodes']==250000
        blob=(ROOT/('policy_outcomes_prefix'+str(turn)+'.bin')).read_bytes()
        assert hashlib.sha256(blob).hexdigest()==ev['outcome_bits_sha256'] and len(blob)==(ev['episodes']+7)//8
        assert sum(x.bit_count() for x in blob)==ev['successes']
        Nk=ev['episodes'];ck=ev['successes'];Ke=R(7,10)*clog2(4/(delta/6));rad=eb_radius(ck,Nk,Ke)
        lower=max(R(0),R(ck,Nk)-rad);assert str(lower)==ev['lower'] and str(Ke)==ev['K']
        gap=max(R(0),upper-lower);admit=gap<=R(expected_regret)
        if admit and first is None:first=turn
        attempts.append({'prefix_round':turn,'per_row_samples':N,'maximum_goal_count':c,'K':str(K),
          'observed_source_max_goal_probability_upper':str(source_p),'source_transport_reserve':str(transport),
          'target_max_goal_probability_upper':str(p),'true_optimum_upper':str(upper),'chosen_policy_value_lower':str(lower),
          'certified_regret':str(gap),'regret_float':float(gap),'admitted':bool(admit),
          'prospective_total_calls':proposal_calls+m*n*N+(turn+1)*250000*expected_length})
    assert len(attempts)==3
    return {'status':'PASS_GOAL_HAZARD_COMPARATOR' if first is not None else 'REFUSED_THIS_CERTIFICATE',
      'first_admitted_prefix':first,'requested_regret':str(expected_regret),'confidence':str(delta),
      'attempts':attempts,'accepted_history_comparator_regret':'0.05650530389526265',
      'base_task_sha256':hashlib.sha256(json.dumps({'b':b,'ell_numer':ell,'ell_denominator':den},sort_keys=True).encode()).hexdigest(),
      'fixed_original_task_only':True,'additional_probability_event':'None from the interval envelopes is used; hazard events total delta/2 across6 prefixes and evaluation events total delta/2 across3 attempts.',
      'scope':'Goal-specific expected-terminal-reward regret against all microscopic/history policies. Under authentic iid fixed-prefix rows and fresh-policy rollouts plus stated numerical source transport. Not yet independently reviewed; not a uniform guarantee for new adaptively chosen goals. No refund of original experiment; prospective method uses a strict observation subset plus its paid fresh evaluations.',
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'interval_generation_sha256':hashlib.sha256((ROOT/'interval_comparator.py').read_bytes()).hexdigest(),
      'interval_result_sha256':hashlib.sha256((ROOT/'interval_comparison_results.json').read_bytes()).hexdigest()}


if __name__=='__main__':
    out=run();(ROOT/'goal_hazard_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'attempts':[{k:a[k] for k in ['prefix_round','regret_float','admitted','prospective_total_calls']} for a in out['attempts']]},indent=2))
