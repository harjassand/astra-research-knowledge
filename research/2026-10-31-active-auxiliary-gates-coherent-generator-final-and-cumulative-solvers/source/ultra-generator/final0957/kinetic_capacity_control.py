#!/usr/bin/env python3
"""Exact generator controls and a frozen pair of synthetic kinetic records.

No physical apparatus, elapsed-time record, mean activity or dissipation
is inferred. --prepare freezes the power calculation before --acquire.
--verify replays existing records and never draws a replacement.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'outputs/coherent_generator'
sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'work'))
from kinetic import evaluate,from_counts,lower_probability,at_least,checkpoints
from coherent_generator_control import identity,mm,mv,inverse,inspection
from ctmc_reflection_control import CountedBits,exp_negative_bounds,dyadic_enclose


def dump(path,data):path.write_text(json.dumps(data,indent=2)+'\n')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def adjoint(A,pi):
    return [[pi[j]*A[j][i]/pi[i] for j in range(len(pi))] for i in range(len(pi))]


def rational_model(n):
    pi=[Q(i+1,n*(n+1)//2) for i in range(n)]
    J=[[pi[i]*pi[j]/3 if i!=j else Q(0) for j in range(n)] for i in range(n)]
    circulation=min(pi)/20
    for i in range(n):J[i][(i+1)%n]+=circulation
    for i in range(n):J[i][i]=pi[i]-sum(J[i])
    P=[[x/pi[i] for x in row] for i,row in enumerate(J)]
    assert all(x>=0 for row in P for x in row)
    assert all(sum(row)==1 for row in P)
    assert [sum(J[i][j] for i in range(n)) for j in range(n)]==pi
    return P,pi


def algebra_controls():
    identities=mgfs=sharp=0
    for n in (2,3,5):
        P,pi=rational_model(n);I=identity(n);Ps=adjoint(P,pi)
        for cap,clock in ((Q(1,2),Q(1)),(Q(1),Q(2,3)),(Q(3),Q(1))):
            s=cap/(cap+clock);r=cap/(clock+2*cap);c=1-r
            A=[[I[i][j]-s*P[i][j] for j in range(n)] for i in range(n)]
            Ai=inverse(A)
            C=mm([[P[i][j]-s*I[i][j] for j in range(n)] for i in range(n)],Ai)
            B=inspection(P,cap,clock)
            assert B==[[c*I[i][j]+r*C[i][j] for j in range(n)] for i in range(n)]
            CsC=mm(adjoint(C,pi),C);PsP=mm(Ps,P)
            defect=[[I[i][j]-CsC[i][j] for j in range(n)] for i in range(n)]
            rhs=mm(mm(adjoint(Ai,pi),[[I[i][j]-PsP[i][j] for j in range(n)] for i in range(n)]),Ai)
            assert defect==[[(1-s*s)*x for x in row] for row in rhs]
            identities+=2
            for labels in ([i%2 for i in range(n)],[int(i>=n//2) for i in range(n)]):
                for a in (Q(3,2),Q(3)):
                    T=[[B[i][j]*(a if labels[i]!=labels[j] else 1) for j in range(n)] for i in range(n)]
                    v=[Q(1)]*n
                    for N in range(1,10):
                        v=mv(T,v)
                        assert sum(p*x for p,x in zip(pi,v))<=(1-r+r*a)**N
                        mgfs+=1
    for cap,clock in ((Q(1),Q(1)),(Q(4),Q(1)),(Q(2,3),Q(7,3))):
        P=[[Q(0),Q(1)],[Q(1),Q(0)]];B=inspection(P,cap,clock);r=cap/(clock+2*cap)
        for a in (Q(4,3),Q(2),Q(5)):
            T=[[B[i][j]*(a if i!=j else 1) for j in range(2)] for i in range(2)]
            v=[Q(1),Q(1)]
            for N in range(1,13):
                v=mv(T,v);assert sum(v)/2==(1-r+r*a)**N;sharp+=1
    # Without stationary preparation, even a reciprocal bounded generator
    # can violate the stationary one-edge sharp bound.
    P=[[Q(0),Q(1)],[Q(1,10),Q(9,10)]];B=inspection(P,Q(1),Q(1))
    assert B[0][1]==Q(10,21)>Q(1,3)
    assert B[0][1]<=Q(1,2)  # the weaker conditional hazard remains valid
    # Noiseless deterministic readout is indispensable: an iid fair noisy
    # sensor has change probability 1/2 even when the physical generator is 0.
    assert Q(1,2)>Q(0)
    q,_=lower_probability(1,1,Q(1,4),Q(1),24)
    assert q<=Q(1,4)<=q+Q(1,2**24)
    rate=from_counts(1000,444,Q(1),Q(1,1000000))
    scaled=from_counts(1000,444,Q(7,3),Q(1,1000000))
    assert Q(scaled['lower_rate'])==Q(7,3)*Q(rate['lower_rate'])
    assert from_counts(1000,1000,Q(1),Q(1,100))['all_finite_caps_rejected_under_model']
    assert from_counts(1000,0)['lower_rate']=='0'
    return {'disk_and_defect_exact_identities':identities,'nonuniform_dependent_exact_mgfs':mgfs,
            'sharp_equilibrium_two_state_exact_mgfs':sharp,
            'nonstationary_counterexample_flip_probability':str(B[0][1]),
            'stationary_null_bound_violated_by_nonstationary_start':'1/3',
            'stochastic_sensor_exclusion':'iid fair sensor can flip with probability 1/2 at Q=0',
            'exact_Chernoff_equality_bracket':True,'physical_time_unit_scaling':'7/3',
            'incompatible_record_flag_and_zero_changes_checked':True}


def power_proof():
    N=98304;alpha=Q(1,80);target=Q(3);source=Q(4);clock=Q(1)
    for j,n in checkpoints():
        if n>=N:break
    assert n==N
    allocation=alpha/Q(j*(j+1));left=0;right=N
    while left<right:
        mid=(left+right)//2
        if at_least(from_counts(N,mid,clock,allocation)['lower_rate'],target):right=mid
        else:left=mid+1
    critical=left
    assert not at_least(from_counts(N,critical-1,clock,allocation)['lower_rate'],target)
    assert at_least(from_counts(N,critical,clock,allocation)['lower_rate'],target)
    mean=N*source/(clock+2*source);gap=mean-critical
    assert gap>0
    exponent=2*gap*gap/N
    lo,hi=exp_negative_bounds(exponent,160)
    failure=dyadic_enclose(lo,hi,96)[1]
    assert failure+alpha<Q(1,40)
    return {'interval_cap':N,'observations_per_record':N+1,'checkpoint_index':j,
            'target_maximum_escape_rate':str(target),'source_escape_rate':str(source),
            'null_escape_rate':'1','inspection_rate':str(clock),'per_band_risk':str(alpha),
            'paired_primary_band_risk':'1/40','checkpoint_risk':str(allocation),
            'source_exact_observed_flip_probability':'4/9','source_critical_flip_count':critical,
            'source_power_failure_upper':str(failure),'source_power_failure_preview':float(failure),
            'source_power_or_primary_band_failure_upper':str(failure+alpha),
            'seeds':[2026110113,2026110114],
            'source_power_premise':'exact two-state resolvent; iid flips used for source power only',
            'timing_contract':'competing event types; exponential durations marginalized; expected duration only',
            'physical_entropy_rates_both':'0',
            'ordinary_incumbents':['conditional row_hazard, same schedule and risk',
                                    'correctly specified equilibrium two-state binomial inference: identical sharp calibration'],
            'sampling_advantage_over_correct_two_state_incumbent':False}


def frozen_hashes():
    paths=[Path(__file__),HERE/'kinetic.py',HERE/'METROLOGY.txt',
           ROOT/'outputs/entropy_witnesses/checkpoint_band.py',ROOT/'outputs/entropy_witnesses/entropy_cone.py',
           ROOT/'work/ctmc_reflection_control.py',ROOT/'work/coherent_generator_control.py']
    return {str(p.relative_to(ROOT)):digest(p) for p in paths}


def sample(N,rate,seed):
    assert isinstance(rate,int) and rate>=1
    start=time.perf_counter();bits=CountedBits(seed);state=bits.below(2);record=[state];jumps=0
    while len(record)<=N:
        event=bits.below(rate+1)
        if event<rate:state=1-state;jumps+=1
        else:record.append(state)
    return record,{'seed':seed,'stationary_preparations':1,'observations':len(record),
                   'inspection_intervals':N,'latent_updates':jumps,'event_type_draws':jumps+N,
                   'PRNG_bits_including_rejections_and_initial_state':bits.bits,
                   'expected_model_duration':str(N),'realized_duration_acquired':False,
                   'waiting_times_marginalized':True,'CPU_elapsed_seconds':time.perf_counter()-start,
                   'actual_maximum_escape_rate':str(rate),'actual_entropy_production_rate':'0',
                   'synthetic':True,'physical_experiment':False}


def analyse(design,acquisitions):
    start=time.perf_counter();out=[]
    for name,rate in (('kinetic_source',Q(4)),('kinetic_null',Q(1))):
        path=HERE/(name+'.json');record=json.loads(path.read_text())
        assert digest(path)==acquisitions[name]['record_SHA256']
        new=evaluate(iter(record),Q(1),Q(1,80),'coherent',Q(3),True)
        old=evaluate(iter(record),Q(1),Q(1,80),'row_hazard',Q(3),True)
        coverage=all(p['lower_rate']!='infinity' and Q(p['lower_rate'])<=rate for p in new['history'])
        dominance=all(at_least(p['lower_rate'],q['lower_rate']) for p,q in zip(new['history'],old['history']))
        assert len(new['history'])==design['power']['checkpoint_index']
        # Prefix replay checks the optional stopping interface on the very
        # same acquired bits. It does not count as a new source acquisition.
        crossing=new['first_threshold_crossing'];replay=None
        if crossing:
            n=crossing['intervals'];short=evaluate(iter(record[:n+1]),Q(1),Q(1,80),'coherent',Q(3))
            assert short['lower_rate']==crossing['lower_rate']
            replay={'intervals':n,'same_endpoint':True,'new_acquisitions':0}
        out.append({'name':name,'acquisition':acquisitions[name],'coherent':new,'row_hazard':old,
                    'primary_band_covered_actual_max_rate_at_all_checkpoints':coverage,
                    'coherent_dominates_row_hazard_on_this_record':dominance,'stopped_prefix_replay':replay,
                    'correct_two_state_binomial_incumbent':'same endpoints as coherent by sharp exact mgf'})
    return {'status':'KINETIC_CAPACITY_CONTROLS_COMPLETED','design':design,'records':out,
            'analysis_CPU_elapsed_seconds':time.perf_counter()-start,
            'aggregate_new_acquisitions':{'stationary_preparations':2,
                'observations':sum(x['observations'] for x in acquisitions.values()),
                'inspection_intervals':sum(x['inspection_intervals'] for x in acquisitions.values()),
                'latent_updates':sum(x['latent_updates'] for x in acquisitions.values()),
                'PRNG_bits':sum(x['PRNG_bits_including_rejections_and_initial_state'] for x in acquisitions.values()),
                'expected_model_duration':str(sum(Q(x['expected_model_duration']) for x in acquisitions.values())),
                'realized_elapsed_time_acquired':False,'physical_experiments':0},
            'claim_boundary':'maximum escape rate only; neither mean activity nor entropy production',
            'all_draws_retained':True,'calibration_and_stationary_preparation_acquired':False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['prepare','acquire','verify']);args=p.parse_args()
    designpath=HERE/'kinetic_design.json';acqpath=HERE/'kinetic_acquisition.json'
    if args.mode=='prepare':
        if designpath.exists():raise RuntimeError('frozen design already exists; preserve it')
        start=time.perf_counter();controls=algebra_controls();power=power_proof()
        design={'frozen_before_draws':True,'power':power,'exact_controls':controls,
                'code_and_proof_SHA256':frozen_hashes(),'preparation_CPU_elapsed_seconds':time.perf_counter()-start,
                'new_acquisitions':0}
        dump(designpath,design)
        print(json.dumps({'mode':'prepared','power':power,'controls':controls},indent=2));return
    design=json.loads(designpath.read_text())
    assert frozen_hashes()==design['code_and_proof_SHA256'],'frozen implementation changed'
    if args.mode=='acquire':
        paths=[acqpath,HERE/'kinetic_source.json',HERE/'kinetic_null.json']
        if any(path.exists() for path in paths):raise RuntimeError('existing draw found; use verify and retain all draws')
        acquisitions={}
        for name,rate,seed in [('kinetic_source',4,2026110113),('kinetic_null',1,2026110114)]:
            record,cost=sample(design['power']['interval_cap'],rate,seed)
            path=HERE/(name+'.json');dump(path,record);cost['record_SHA256']=digest(path)
            acquisitions[name]=cost;dump(acqpath,acquisitions)
            print(json.dumps({'acquired':name,'cost':cost}),flush=True)
    else:
        assert algebra_controls()==design['exact_controls']
        acquisitions=json.loads(acqpath.read_text())
    receipt=analyse(design,acquisitions)
    dump(HERE/('kinetic_receipt.json' if args.mode=='acquire' else 'kinetic_replay.json'),receipt)
    print(json.dumps({'status':receipt['status'],'mode':args.mode,
                     'records':[{'name':x['name'],'new':x['coherent']['lower_preview'],
                                 'row_hazard':x['row_hazard']['lower_preview'],
                                 'first_crossing':x['coherent']['first_threshold_crossing'],
                                 'coverage':x['primary_band_covered_actual_max_rate_at_all_checkpoints']}
                                for x in receipt['records']],
                     'aggregate_new_acquisitions':receipt['aggregate_new_acquisitions'],
                     'analysis_seconds':receipt['analysis_CPU_elapsed_seconds']},indent=2))


if __name__=='__main__':main()
