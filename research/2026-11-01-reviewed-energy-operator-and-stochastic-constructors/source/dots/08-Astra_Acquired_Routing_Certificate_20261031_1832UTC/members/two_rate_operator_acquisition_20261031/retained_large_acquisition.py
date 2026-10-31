#!/usr/bin/env python3
"""Retained outgoing observations jointly certify leaks and fine action.

Synthetic multinomial batches represent (and charge) ordinary forward queries;
their cheap simulation wall time is NOT the time to acquire those transitions.
No hidden source groups, matrices or adjoints are read by acquire().
"""
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import math
import random
import sys
import time
import sympy as s
from large_routing_source import RoutingSource,acquire_partition
from quadratic_leakage import (R,sqrt_up,median_repetitions,upper_squared,
                               incoming_stat,outgoing_stat)
from sparse_norm_probe import upper_norm

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'robust_operator_reuse_20261031'/'finite_observation'))
from robust_replay import compile_integer_replay,integer_step,integer_output


def clog2(x):
    x=R(x);k=0
    while 2**k<x:k+=1
    return k


def eb_radius(c,N,K):
    """Two/one sided union allocation is in K; Maurer--Pontil Thm 4."""
    if type(c) is not int or type(N) is not int or not 0<=c<=N or N<2:
        raise ValueError('Bernoulli counts')
    variance=R(c*(N-c),N*(N-1))
    return min(R(1),sqrt_up(2*variance*K/N,bits=40)+R(7*K,3*(N-1)))


def compression(enter,leave,alpha,L):
    t=R(0);total=R(0)
    for _ in range(L):total+=t;t=min(R(1),alpha*t+enter)
    return leave*total


def acquire(source,b,ell_num,ell_den,L,eps,delta=R(1,1000),rank_cap=16):
    start=time.perf_counter();n=len(b);m=source.generators;records=[]
    if any(x not in (0,1) or type(x) is not int for x in b+ell_num):raise ValueError('indicator fixture task')
    if sum(ell_num)!=ell_den or not any(b):raise ValueError('normalized initial distribution')
    def record(kind,a,N,counts,**kw):
        records.append({'kind':kind,'a':a,'N':N,'counts':counts,**kw})
    K0=clog2(2*m*n/(delta/8));N0=64*n*K0;B=R(1)
    for a in range(m):
        rows,col=source.uniform_batch(a,N0,'column_bound');record('column',a,N0,col)
        B=max(B,max(R(n*(2*x+8*K0),N0) for x in col))
    B=min(R(n),B);radius=R(1,4);Kc=clog2(2*m*n/(delta/8))
    Nc=int(s.ceiling(Kc*(2*n*B+R(4,3)*n*radius)/radius**2));coarse=[]
    for a in range(m):
        rows,_=source.uniform_batch(a,Nc,'sparse_coarse');coarse.append(rows);record('coarse',a,Nc,rows)
    parts,which,proposal=acquire_partition(coarse,b,ell_num);r=len(parts)
    if r>rank_cap:return {'status':'INCONCLUSIVE_RANK_CAP','proposal':proposal},records
    if any(len({(b[i],ell_num[i]) for i in part})!=1 for part in parts):raise AssertionError('task compatibility')
    pi_min=R(min(map(len,parts)),n)
    norm=[]
    for a in range(m):
        # The seeds specify reproducible mock independent streams; real
        # randomness and nonanticipation remain external protocol premises.
        x=upper_norm(coarse[a],Nc,parts,delta/(8*m),seed=982451653+a)
        norm.append(x)
    alpha=max(R(x['upper']) for x in norm)+radius
    if alpha>=1:return {'status':'INCONCLUSIVE_COMPLEMENT','alpha':str(alpha),'proposal':proposal},records
    Npilot=2048;Kp=clog2(2*m*n*r/(delta/8));pilots=[]
    for a in range(m):
        counts=source.row_block_batch(a,Npilot,which,r,'covariance_pilot');record('pilot',a,Npilot,counts)
        traces=[]
        for row in counts:
            lower=max(max(R(0),R(c,Npilot)-eb_radius(c,Npilot,Kp)) for c in row)
            traces.append(min(R(1),2*(1-lower))/pi_min)
        pilots.append({'sigma':str(max(traces)),'T':str(sum(traces)),'K':Kp})
    cross=[];chosen=None;fine=[]
    for turn in range(6):
        dv=delta/(4*(turn+1)*(turn+2));Nin=512*2**turn;Nout=1_000_000*4**turn
        kin=median_repetitions(dv/(2*m));kout=median_repetitions(dv/(2*m*r));in_uppers=[];out_uppers=[];fine_counts=[]
        for a in range(m):
            sigma=R(pilots[a]['sigma']);T=R(pilots[a]['T']);stats=[]
            for k in range(kin):
                left=source.row_block_batch(a,Nin,which,r,'incoming_'+str(turn)+'_'+str(k)+'_L')
                right=source.row_block_batch(a,Nin,which,r,'incoming_'+str(turn)+'_'+str(k)+'_R')
                record('incoming_pair',a,Nin,[left,right],turn=turn,replicate=k)
                value=incoming_stat(left,right,parts)
                stats.append(upper_squared(value,2*sigma/(n*Nin),sigma*T/(n*n*Nin*Nin)))
            in_uppers.append(sorted(stats)[kin//2])
            for g,part in enumerate(parts):
                kappa=B*n/len(part);stats=[];pooled=[0]*r
                for k in range(kout):
                    counts=source.pooled_batch(a,part,Nout,'outgoing_'+str(turn)+'_'+str(g)+'_'+str(k))
                    record('outgoing',a,Nout,counts,turn=turn,group=g,replicate=k)
                    for h,dest in enumerate(parts):pooled[h]+=sum(counts[i] for i in dest)
                    stats.append(upper_squared(outgoing_stat(counts,parts),4*kappa/Nout,
                                               2*kappa*n/(Nout*(Nout-1))))
                out_uppers.append(sorted(stats)[kout//2])
                fine_counts.append((a,g,Nout*kout,pooled))
        enter=sqrt_up(max(in_uppers),bits=40);leave=sqrt_up(max(out_uppers),bits=40)
        comp=compression(enter,leave,alpha,L)
        # Same observations, separate simultaneous fine-confidence event.
        # Correlation with the leakage statistic does not invalidate a union bound.
        df=delta/(4*(turn+1)*(turn+2));Kf=clog2(4*m*r*r/df)
        operators=[s.zeros(r) for _ in range(m)];d=R(0)
        for a,g,Nf,counts in fine_counts:
            for j,c in enumerate(counts):operators[a][g,j]=R(c,Nf)
            d=max(d,sum(eb_radius(c,Nf,Kf) for c in counts))
        fine.append({'round':turn,'delta':str(df),'per_block':Nout*kout,'K':Kf,
                     'row_l1_radius':str(d),'propagated_bound':str(L*d),
                     'source':'RETAINED_CURRENT_ROUND_OUTGOING_COUNTS_NO_NEW_CALLS'})
        cross.append({'round':turn,'delta':str(dv),'incoming_per_row_half':Nin,
                      'outgoing_per_pooled_batch':Nout,'incoming_replicates':kin,'outgoing_replicates':kout,
                      'enter_squared':str(max(in_uppers)),'leave_squared':str(max(out_uppers)),
                      'enter':str(enter),'leave':str(leave),'compression_bound':str(comp),
                      'status':'PASS' if comp+L*d<eps else 'FAIL_THIS_SUFFICIENT_CERTIFICATE'})
        print('cross',n,turn,float(enter),float(leave),float(comp),flush=True)
        if comp+L*d<eps:chosen=(enter,leave,comp);break
    if chosen is None:return {'status':'INCONCLUSIVE_LEAKAGE','cross':cross},records
    enter,leave,comp=chosen;p=1
    while R(L+2,2**(p+1))>eps-comp-L*d:p+=1
    execution=R(L+2,2**(p+1));total=comp+L*d+execution
    u=s.Matrix([b[part[0]] for part in parts]);output=s.Matrix([R(sum(ell_num[i] for i in part),ell_den) for part in parts])
    compiled=compile_integer_replay(operators,u,output,p)
    assert total<=eps
    out={'status':'PASS','n':n,'m':m,'rank':r,'length':L,'epsilon':str(eps),'delta':str(delta),
         'task_b':b,'task_ell_numer':ell_num,'task_ell_denominator':ell_den,
         'partition':parts,'proposal':proposal,'pi_min':str(pi_min),'column_sum_upper':str(B),
         'coarse_sample_size':Nc,'coarse_spectral_radius':str(radius),
         'norm_certificates':norm,'alpha':str(alpha),'covariance_pilots':pilots,
         'cross_rounds':cross,'fine_rounds':fine,'compression_bound':str(comp),
         'fine_bound':str(L*d),'execution_bound':str(execution),'total_bound':str(total),
         'compiled':compiled,'logical_forward_calls':sum(x['logical_forward_calls'] for x in source.ledger),
         'source_ledger':source.ledger[:],'sparse_norm_integer_products':sum(x['sparse_integer_products'] for x in norm),
         'sparse_norm_peak_accumulator_bits':max(x['peak_integer_accumulator_bits'] for x in norm),
         'acquisition_simulation_seconds':time.perf_counter()-start,
         'confidence_allocation':{'column':'delta/8','coarse':'delta/8','fresh_norm':'delta/8','covariance_pilot':'delta/8',
                                  'quadratic_validation':'delta/4 over fresh rounds 1/((t+1)(t+2))',
                                  'fine_model':'delta/4 over the same fixed outgoing batches; union over rounds 1/((t+1)(t+2)); no independence from leak statistics needed'},
         'provenance_premise':'Authentic iid transitions; every batch size, public partition and support fixed before its observations; norm probes independent after coarse matrix and partition lock.',
         'scope':'Ordinary sparse community proposal plus acquired two-sided certificate, with retained outgoing counts reused for fine action. Not a new clustering algorithm, no historical novelty or practical-advantage claim.'}
    return out,records


def screen(out,Q=50000,seed=451):
    """Explicit-list best schedule, not free/unrestricted planning."""
    start=time.perf_counter();rng=random.Random(seed);L=out['length'];compiled=out['compiled'];m=out['m']
    words=[tuple([0]*L),tuple([1]*L),tuple(i%2 for i in range(L))]
    words += [tuple(rng.randrange(m) for _ in range(L)) for _ in range(Q-len(words))]
    cache={():compiled['initial_grid_state']};best=None;worst=None;peak=0
    for word in words:
        for j,a in enumerate(word):
            prefix=word[:j+1]
            if prefix not in cache:
                state,bits=integer_step(compiled['operators'][a],cache[word[:j]])
                cache[prefix]=state;peak=max(peak,bits)
        score=integer_output(compiled,cache[word])
        if best is None or score>best[0]:best=(score,word)
        if worst is None or score<worst[0]:worst=(score,word)
    eps=R(out['epsilon']);delta=R(out['delta']);distinct=len(set(words))
    # MC has to share chronological trajectory prefixes, not reversed
    # observable-column prefixes. Both trie sizes are explicitly counted.
    chronological={()}
    for word in words:
        rev=word[::-1]
        for j in range(L):chronological.add(rev[:j+1])
    Nmc=int(s.ceiling(clog2(2*distinct/delta)/(2*eps**2)))
    result={'supplied_schedules':Q,'distinct_schedules':distinct,'word_input_symbols':Q*L,
            'word_list_sha256':hashlib.sha256(bytes(a for w in words for a in w)).hexdigest(),
            'model_prefix_states':len(cache),'model_integer_matrix_scalar_products':(len(cache)-1)*out['rank']**2,
            'retained_prefix_integer_entries':sum(len(x) for x in cache.values()),
            'query_peak_accumulator_bits':peak,'best_score':str(best[0]),'best_word':list(best[1]),
            'worst_score':str(worst[0]),'worst_word':list(worst[1]),
            'certified_list_best_regret':str(2*eps),'constant_epsilon_predictor_ruled_out_by_certificate':bool(best[0]-worst[0]>4*eps),
            'screening_seconds':time.perf_counter()-start,
            'direct_MC_sufficient_rollouts_per_schedule':Nmc,
            'direct_MC_sufficient_forward_calls':distinct*L*Nmc,
            'retained_chronological_MC_trie_nodes':len(chronological),
            'retained_MC_prefix_sufficient_forward_calls':(len(chronological)-1)*Nmc,
            'MC_qualification':'Hoeffding sufficient budgets, not lower bounds. A shared prefix rollout tree gives valid individual marginals and union confidence; it retains all work. Variance-aware adaptive MC may be cheaper.',
            'same_certificate_comparator':'Ordinary retained community/spectral/Krylov/range code can use the same acquired certificate and gets the same admitted capability; certificate contribution is not erased by this.'}
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--n',type=int,default=1024)
    parser.add_argument('--queries',type=int,default=50000);args=parser.parse_args()
    source=RoutingSource(args.n);b,e,den=source.public_task()
    out,records=acquire(source,b,e,den,24,R(1,50))
    if out['status']=='PASS':out['screening']=screen(out,args.queries)
    out['source_hashes']={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
                          ['retained_large_acquisition.py','large_routing_source.py','quadratic_leakage.py','sparse_norm_probe.py']}
    stem='retained_large_'+str(args.n)
    raw=json.dumps({'n':args.n,'records':records},separators=(',',':')).encode();compressed=gzip.compress(raw,mtime=0)
    (ROOT/(stem+'_observations.json.gz')).write_bytes(compressed)
    out['transcript_uncompressed_bytes']=len(raw);out['transcript_gzip_bytes']=len(compressed)
    out['transcript_gzip_sha256']=hashlib.sha256(compressed).hexdigest()
    out['compiled_payload_bytes']=len(json.dumps(out.get('compiled'),separators=(',',':')).encode())
    (ROOT/(stem+'_result.json')).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','n','rank','logical_forward_calls','alpha','total_bound',
                       'acquisition_simulation_seconds','transcript_gzip_bytes','sparse_norm_integer_products'] if k in out},indent=2))


if __name__=='__main__':main()
