#!/usr/bin/env python3
"""Full nonmutating generation/replay; exact unequal-N and interface tests."""
from pathlib import Path
import contextlib,hashlib,io,json,sys,time
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT))
import generate_tagged as gen
import receive_tagged as recv
import check_joint_law as joint
from joint_source import TaggedPoolSource
R=recv.R

def eq(a,b):
    a=dict(a);b=dict(b);a.pop('seconds',None);b.pop('seconds',None)
    assert json.dumps(a,sort_keys=True)==json.dumps(b,sort_keys=True)

def run():
    start=time.perf_counter();checks=0
    exact=joint.run();eq(exact,json.loads((ROOT/'joint_law_checks.json').read_text()));checks+=exact['checks']
    with contextlib.redirect_stdout(io.StringIO()):g,records=gen.run()
    eq(g,json.loads((ROOT/'tagged_generation.json').read_text()));checks+=1
    result=recv.run();eq(result,json.loads((ROOT/'tagged_received.json').read_text()));checks+=result['checks']+1
    assert result['first_admitted_prefix']==1;checks+=1
    stricter=recv.run(expected_record_tolerance=R(1,50));assert stricter['first_admitted_prefix']==2;checks+=1
    refused=recv.run(expected_record_tolerance=R(1,100));assert refused['status'].startswith('REFUSED');checks+=1
    # The actual fixed-witness radius is dominated even when source row counts
    # differ. Its own N_i is random but chosen independently of outcomes.
    K=R(21,2)
    for b in (R(1,2),R(9,10),R(1,10)):
        vB=b*(1-b)
        for Ns in ((3,5,7),(20,30,40)):
            for cs in ((0,0,0),tuple(N//2 for N in Ns),tuple(N-1 for N in Ns),Ns):
                tau=max(abs(R(c,N)-b) for c,N in zip(cs,Ns));cap=min(R(1,4),vB+tau);Nm=min(Ns)
                radius=recv.sqrt_up(2*K*cap/(Nm-1),bits=40)+7*K/(3*(Nm-1))
                for c,N in zip(cs,Ns):
                    x=R(c,N);actual=recv.sqrt_up(2*K*x*(1-x)/(N-1),bits=40)+7*K/(3*(N-1))
                    assert x*(1-x)<=cap and actual<=radius;checks+=1
    negatives=0
    for kw in [dict(expected_length=True),dict(expected_length=23),dict(expected_generators=1),dict(expected_confidence=.001),dict(expected_confidence=R(1,100)),dict(expected_task_sha256='bad'),dict(expected_record_tolerance=True)]:
        try:recv.run(**kw)
        except (AssertionError,ValueError,TypeError):negatives+=1
        else:raise AssertionError('external task alias accepted')
    q=TaggedPoolSource(4,degree=2)
    for args in [(True,[0,1],2,[0,0,1,1],2),(0,[0.,1],2,[0,0,1,1],2),(0,[0,1],True,[0,0,1,1],2),(0,[0,1],2,[0.,0,1,1],2),(0,[0,1],2,[0,0,1,1],2.)]:
        try:q.batch(*args)
        except (AssertionError,ValueError,TypeError):negatives+=1
        else:raise AssertionError('source alias accepted')
    peak=max(c for rec in records for c in rec['row_totals']).bit_length()
    return {'status':'PASS_NEW_TAGGED_FULL_REPLAY','exact_checks':checks,'interface_rejections':negatives,'fresh_observation_calls_new_in_this_checker':0,'actual_new_logical_calls_in_saved_experiment':g['logical_source_calls'],'actually_regenerated_macro_reset_labels':g['actually_generated_macro_reset_destination_labels'],'generation_is_reproduction_not_new_independent_evidence':True,'receiver_runs':3,'source_rows_metadata_each_record_max_count_bits':peak,'first_05_prefix':result['first_admitted_prefix'],'first_02_prefix':stricter['first_admitted_prefix'],'strict_01_refused':True,'source_statistics_extra_counters':result['row_metadata_extra_streaming_counter_entries'],'nominal_uint64_extra_counter_payload_bytes':8*result['row_metadata_extra_streaming_counter_entries'],'retained_joint_transcript_bytes':g['transcript_compressed_bytes'],'scope':'Whole author replay and exact source-law fixture tests. No independent review, physical/PRNG authentication, invented historical tags, or refund of prior acquisitions.','seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
if __name__=='__main__':
    out=run();(ROOT/'tagged_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
