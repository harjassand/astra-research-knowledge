#!/usr/bin/env python3
"""Receive new joint metadata, including unequal random per-row sample counts."""
from pathlib import Path
import gzip,hashlib,json,sys,time
import sympy as s
ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent;sys.path.insert(0,str(PARENT))
from retained_large_acquisition import R,clog2,eb_radius,sqrt_up,median_repetitions,upper_squared,outgoing_stat
from large_routing_source import acquire_partition
BASE_SHA='dc7583f0aa94e06f7440a6109a2dbef128b1db35538664a1880f8a5c4c146568'
OLD_OBS_SHA='f9ec8eedc6465e9b552f48fdbe15f9f6e3e7ca9e2f78553e4d954d6b697fdd85'
TAGGED_SHA='cfc7c620b7aa352c382b722b880531c668fdfce94b545bd35e7dfa8c83629e45'
TASK_SHA='e1d5e9c1a83084d576c411e9586d43c7f4e309984cbd4e542477a9a1a3f5d428'

def run(*,expected_length=24,expected_generators=2,expected_confidence=R(1,1000),expected_record_tolerance=R(1,20),expected_task_sha256=TASK_SHA):
    start=time.perf_counter();checks=0
    def ck(v):
        nonlocal checks
        assert v;checks+=1
    ck(type(expected_length) is int and expected_length==24 and type(expected_generators) is int and expected_generators==2)
    ck(not isinstance(expected_confidence,(bool,float)) and R(expected_confidence)==R(1,1000))
    ck(not isinstance(expected_record_tolerance,(bool,float)) and R(expected_record_tolerance)>0)
    ck(type(expected_task_sha256) is str and expected_task_sha256==TASK_SHA)
    raw=(PARENT/'history_sensitive_4096_result.json').read_bytes();old=(PARENT/'history_sensitive_4096_observations.json.gz').read_bytes();new=(ROOT/'tagged_observations.json.gz').read_bytes()
    ck(hashlib.sha256(raw).hexdigest()==BASE_SHA and hashlib.sha256(old).hexdigest()==OLD_OBS_SHA and hashlib.sha256(new).hexdigest()==TAGGED_SHA)
    model=json.loads(raw);old_records=json.loads(gzip.decompress(old))['records'];tagged=json.loads(gzip.decompress(new));records=tagged['records']
    n=model['n'];m=model['m'];delta=R(expected_confidence);L=expected_length;b=model['task_b'];ell=model['task_ell_numer'];den=model['task_ell_denominator']
    ck(hashlib.sha256(json.dumps({'b':b,'ell_numer':ell,'ell_denominator':den},sort_keys=True).encode()).hexdigest()==TASK_SHA)
    ck((model['length'],m,R(model['delta']))==(L,expected_generators,delta))
    cols=[z for z in old_records if z['kind']=='column'];coarse=[z for z in old_records if z['kind']=='coarse'];ck(len(cols)==len(coarse)==m)
    K0=clog2(2*m*n/(delta/8));N0=64*n*K0;B=R(1)
    for a,row in enumerate(cols):
        ck((row['a'],row['N'])==(a,N0) and len(row['counts'])==n)
        ck(all(type(c) is int and c>=0 for c in row['counts']) and sum(row['counts'])==N0)
        B=max(B,max(R(n*(2*c+8*K0),N0) for c in row['counts']))
    B=min(R(n),B);ck(B==R(model['column_sum_upper']))
    for a,row in enumerate(coarse):
        ck(row['a']==a and len(row['counts'])==n and sum(c for rs in row['counts'] for j,c in rs)==row['N'])
    parts,which,proposal=acquire_partition([z['counts'] for z in coarse],b,ell);r=len(parts)
    ck(parts==tagged['partition']==model['partition'] and r==tagged['r'] and n==tagged['n'])
    ck(all(len({ell[i] for i in p})==1 for p in parts) and sum(ell)==den)
    rowcounts=[[[0]*r for i in range(n)] for a in range(m)];totals=[[0]*n for a in range(m)]
    K=R(7,10)*clog2(2*6/(delta/2));used=0;logical=0;attempts=[];first=None
    discovery=sum(z['N'] for z in cols+coarse)
    for turn in range(3):
        dv=delta/(4*(turn+1)*(turn+2));N=1_000_000*4**turn;reps=median_repetitions(dv/(2*m*r));outs=[];fine=[]
        for a in range(m):
            for g,part in enumerate(parts):
                kap=B*n/len(part);statistics=[];pooled_blocks=[0]*r
                for rep in range(reps):
                    z=records[used];used+=1
                    ck((z['a'],z['group'],z['turn'],z['replicate'],z['N'])==(a,g,turn,rep,N))
                    ck(z['source_rows']==part and len(z['row_totals'])==len(z['row_block_counts'])==len(part))
                    micro=z['pooled_micro_counts'];ck(len(micro)==n and all(type(c) is int and c>=0 for c in micro) and sum(micro)==N)
                    ck(all(type(c) is int and c>=0 for c in z['row_totals']) and sum(z['row_totals'])==N)
                    joint_blocks=[0]*r
                    for i,Ni,cs in zip(part,z['row_totals'],z['row_block_counts']):
                        ck(len(cs)==r and all(type(c) is int and c>=0 for c in cs) and sum(cs)==Ni)
                        totals[a][i]+=Ni
                        for h,c in enumerate(cs):rowcounts[a][i][h]+=c;joint_blocks[h]+=c
                    marginal=[sum(micro[i] for i in p) for p in parts];ck(marginal==joint_blocks)
                    for h,c in enumerate(marginal):pooled_blocks[h]+=c
                    statistics.append(upper_squared(outgoing_stat(micro,parts),4*kap/N,2*kap*n/(N*(N-1))))
                    logical+=N
                outs.append(sorted(statistics)[reps//2]);fine.append((a,g,N*reps,pooled_blocks))
        Nmin=min(x for row in totals for x in row);Nmax=max(x for row in totals for x in row);ck(Nmin>=2)
        ck(all(sum(rowcounts[a][i])==totals[a][i] for a in range(m) for i in range(n)))
        eout=sqrt_up(max(outs),bits=40);Kf=clog2(4*m*r*r/dv);d=R(0);operators=[s.zeros(r) for a in range(m)]
        for a,g,Nf,cs in fine:
            for h,c in enumerate(cs):operators[a][g,h]=R(c,Nf)
            d=max(d,sum(eb_radius(c,Nf,Kf) for c in cs))
        tau=R(0);vB=R(0);witness=None
        for a in range(m):
            for g,part in enumerate(parts):
                pmax=max(operators[a].row(g));vB=max(vB,pmax*(1-pmax) if pmax>=R(1,2) else R(1,4))
                Nf=N*reps;center=[int(operators[a][g,h]*Nf) for h in range(r)]
                for i in part:
                    Ni=totals[a][i];v=R(sum(abs(rowcounts[a][i][h]*Nf-center[h]*Ni) for h in range(r)),2*Ni*Nf)
                    if v>tau:tau=v;witness={'action':a,'block':g,'row':i,'N_i':Ni}
        vhat=min(R(1,4),vB+tau);rad=sqrt_up(2*K*vhat/(Nmin-1),bits=40)+7*K/(3*(Nmin-1));cin=min(R(1),tau+rad+d/2)
        z=tail=R(0);caps=[]
        for j in range(L):caps.append(str(z));tail+=eout*z;z=min(R(1),cin+(1+eout)*z)
        error=L*d+tail;admit=error<=R(expected_record_tolerance)
        if admit and first is None:first=turn
        attempts.append({'prefix':turn,'pooled_forward_calls_cumulative':logical,'prospective_total_calls':discovery+logical,'per_row_samples_min':Nmin,'per_row_samples_max':Nmax,'incoming_K':str(K),'empirical_max_row_TV':str(tau),'coarse_variance_envelope':str(vB),'incoming_radius':str(rad),'incoming_TV_bound':str(cin),'incoming_empirical_witness':witness,'outgoing_Hdual_bound':str(eout),'fine_l1_bound':str(d),'caps_before_steps':caps,'record_error_bound':str(error),'record_error_float':float(error),'admitted':bool(admit),'coarse_operators':[[[str(x) for x in A.row(g)] for g in range(r)] for A in operators]})
    ck(used==len(records) and logical==2504000000)
    return {'status':'PASS_NEW_TAGGED_POOL_CERTIFICATE' if first is not None else 'REFUSED_NEW_TAGGED_POOL_CERTIFICATE','checks':checks,'first_admitted_prefix':first,'requested_record_tolerance':str(expected_record_tolerance),'confidence':str(delta),'failure_budget_upper':str(R(53,56)*delta),'attempts':attempts,'new_logical_source_calls_actually_generated':logical,'prior_discovery_column_coarse_calls':discovery,'actual_prior_full_acquisition_not_refunded':model['logical_forward_calls'],'new_norm_probes':0,'incoming_only_new_source_calls':0,'historical_tags_reconstructed':False,'row_metadata_extra_streaming_counter_entries':m*n*(r+1),'scope':'New tagged observations; conditional row confidence given outcome-independent source-row counts. Same budget as norm-free proof, using N_min conservatively. Pooled and tagged statistics are correlated; union bound, not independence. All three batches actually generated even if earlier prefix passes. No historical tags invented and no practical/historical novelty claim.','seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'tagged_transcript_sha256':TAGGED_SHA}
if __name__=='__main__':
    out=run();(ROOT/'tagged_received.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='attempts'},indent=2));print([(a['prefix'],a['record_error_float'],a['prospective_total_calls']) for a in out['attempts']])
