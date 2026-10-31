#!/usr/bin/env python3
"""Exact replay of saved counts, not a verifier of iid/randomness provenance.

Typed scientific-record API. This is not an adversarial arbitrary-JSON parser.
Requested task/horizon/tolerance are independently bound by the caller.
"""
from pathlib import Path
import argparse
import copy
import gzip
import hashlib
import json
import sys
import time
import sympy as s
from large_acquisition import (R,clog2,eb_radius,sqrt_up,compression,upper_norm,
                               median_repetitions,upper_squared,incoming_stat,
                               outgoing_stat,compile_integer_replay,integer_step,integer_output)
from large_routing_source import RoutingSource,acquire_partition

ROOT=Path(__file__).resolve().parent


def replay(out,records,*,expected_b,expected_ell_num,expected_ell_den,expected_length,expected_tolerance):
    checks=0
    def ck(ok):
        nonlocal checks
        assert ok;checks+=1
    ck(type(expected_length) is int and out['length']==expected_length)
    ck(not isinstance(expected_tolerance,(bool,float)) and R(out['epsilon'])==R(expected_tolerance))
    ck(out['task_b']==expected_b and out['task_ell_numer']==expected_ell_num and out['task_ell_denominator']==expected_ell_den)
    n=out['n'];m=out['m'];L=expected_length;eps=R(expected_tolerance);delta=R(out['delta'])
    ck(n==len(expected_b)==len(expected_ell_num));ck(sum(expected_ell_num)==expected_ell_den)
    grouped={}
    for x in records:grouped.setdefault(x['kind'],[]).append(x)
    ck(set(grouped)=={'column','coarse','pilot','incoming_pair','outgoing','fine'})
    K0=clog2(2*m*n/(delta/8));N0=64*n*K0;B=R(1)
    ck(len(grouped['column'])==m)
    for a,x in enumerate(grouped['column']):
        ck(x['N']==N0 and x['a']==a and len(x['counts'])==n)
        ck(all(type(c) is int and c>=0 for c in x['counts']) and sum(x['counts'])==N0)
        B=max(B,max(R(n*(2*c+8*K0),N0) for c in x['counts']))
    B=min(R(n),B);ck(B==R(out['column_sum_upper']));t=R(1,4);Kc=K0
    Nc=int(s.ceiling(Kc*(2*n*B+R(4,3)*n*t)/t**2));ck(Nc==out['coarse_sample_size'])
    ck(len(grouped['coarse'])==m);coarse=[]
    for a,x in enumerate(grouped['coarse']):ck(x['a']==a and x['N']==Nc);coarse.append(x['counts'])
    parts,which,proposal=acquire_partition(coarse,expected_b,expected_ell_num)
    ck(parts==out['partition'] and proposal==out['proposal']);r=len(parts);pi=R(min(map(len,parts)),n)
    ck(r==out['rank'] and pi==R(out['pi_min']))
    ck(all(len({(expected_b[i],expected_ell_num[i]) for i in p})==1 for p in parts))
    norms=[]
    for a,x in enumerate(out['norm_certificates']):
        z=upper_norm(coarse[a],Nc,parts,delta/(8*m),forced_probe=x['probe'])
        for key in z:
            if key!='execution_seconds':ck(z[key]==x[key])
        norms.append(R(z['upper']))
    alpha=max(norms)+t;ck(alpha==R(out['alpha']) and alpha<1)
    Np=2048;Kp=clog2(2*m*n*r/(delta/8));pilots=[]
    ck(len(grouped['pilot'])==m)
    for a,x in enumerate(grouped['pilot']):
        ck(x['a']==a and x['N']==Np and len(x['counts'])==n)
        traces=[]
        for row in x['counts']:
            ck(len(row)==r and all(type(c) is int and c>=0 for c in row) and sum(row)==Np)
            lower=max(max(R(0),R(c,Np)-eb_radius(c,Np,Kp)) for c in row)
            traces.append(min(R(1),2*(1-lower))/pi)
        pilots.append((max(traces),sum(traces)))
        ck(str(pilots[-1][0])==out['covariance_pilots'][a]['sigma'])
        ck(str(pilots[-1][1])==out['covariance_pilots'][a]['T'])
    used_in=used_out=0
    for turn,summary in enumerate(out['cross_rounds']):
        dv=delta/(4*(turn+1)*(turn+2));Ni=512*2**turn;No=1_000_000*4**turn
        ki=median_repetitions(dv/(2*m));ko=median_repetitions(dv/(2*m*r));ins=[];outs=[]
        for a in range(m):
            sigma,T=pilots[a];stats=[]
            for k in range(ki):
                x=grouped['incoming_pair'][used_in];used_in+=1
                ck((x['a'],x['turn'],x['replicate'],x['N'])==(a,turn,k,Ni))
                left,right=x['counts'];ck(len(left)==n)
                value=incoming_stat(left,right,parts)
                stats.append(upper_squared(value,2*sigma/(n*Ni),sigma*T/(n*n*Ni*Ni)))
            ins.append(sorted(stats)[ki//2])
            for g,part in enumerate(parts):
                kap=B*n/len(part);stats=[]
                for k in range(ko):
                    x=grouped['outgoing'][used_out];used_out+=1
                    ck((x['a'],x['turn'],x['group'],x['replicate'],x['N'])==(a,turn,g,k,No))
                    ck(len(x['counts'])==n and sum(x['counts'])==No)
                    stats.append(upper_squared(outgoing_stat(x['counts'],parts),4*kap/No,2*kap*n/(No*(No-1))))
                outs.append(sorted(stats)[ko//2])
        enter=sqrt_up(max(ins),bits=40);leave=sqrt_up(max(outs),bits=40);comp=compression(enter,leave,alpha,L)
        ck(R(summary['enter'])==enter and R(summary['leave'])==leave and R(summary['compression_bound'])==comp)
        ck(summary['status']==('PASS' if comp<=eps/3 else 'FAIL_THIS_SUFFICIENT_CERTIFICATE'))
        ck((comp<=eps/3)==(turn==len(out['cross_rounds'])-1))
    ck(used_in==len(grouped['incoming_pair']) and used_out==len(grouped['outgoing']))
    used=0
    for turn,summary in enumerate(out['fine_rounds']):
        df=delta/(4*(turn+1)*(turn+2));K=clog2(4*m*r*r/df);N=1_000_000*2**turn;d=R(0);operators=[]
        for a in range(m):
            M=s.zeros(r)
            for g in range(r):
                x=grouped['fine'][used];used+=1
                ck((x['a'],x['group'],x['turn'],x['N'])==(a,g,turn,N))
                counts=x['counts'];ck(len(counts)==r and sum(counts)==N)
                for j,c in enumerate(counts):M[g,j]=R(c,N)
                d=max(d,sum(eb_radius(c,N,K) for c in counts))
            ck(min(M)>=0 and M*s.ones(r,1)==s.ones(r,1));operators.append(M)
        ck(str(d)==summary['row_l1_radius'] and str(L*d)==summary['propagated_bound'])
        ck((L*d<=eps/3)==(turn==len(out['fine_rounds'])-1))
    ck(used==len(grouped['fine']));p=1
    while R(L+2,2**(p+1))>eps/3:p+=1
    execution=R(L+2,2**(p+1));total=comp+L*d+execution
    ck(str(total)==out['total_bound'] and total<=eps)
    u=s.Matrix([expected_b[p[0]] for p in parts]);ell=s.Matrix([R(sum(expected_ell_num[i] for i in p),expected_ell_den) for p in parts])
    compiled=compile_integer_replay(operators,u,ell,p);ck(compiled==out['compiled'])
    count=0
    for x in records:
        count+=x['N']*(2*n if x['kind']=='incoming_pair' else n if x['kind']=='pilot' else 1)
    ck(count==out['logical_forward_calls']==sum(x['logical_forward_calls'] for x in out['source_ledger']))
    return checks


def extra_checks(out):
    checks=0
    def ck(ok):
        nonlocal checks
        assert ok;checks+=1
    # The source is recreated only for AFTER-acquisition numerical falsification.
    source=RoutingSource(out['n']);b,e,den=source.public_task();compiled=out['compiled'];worst=0.
    words=[[],[0],[1],[0,1],[1,0],out['screening']['best_word'],out['screening']['worst_word']]
    words += [[(i//d)%2 for i in range(out['length'])] for d in (1,2,3,5)]
    for word in words:
        truth=b[:];state=compiled['initial_grid_state'][:]
        for a in word:truth=source.apply_truth(a,truth);state,_=integer_step(compiled['operators'][a],state)
        want=sum(truth[i] for i in range(len(e)) if e[i])/den
        error=abs(float(integer_output(compiled,state))-want);worst=max(worst,error)
        ck(error<float(R(out['total_bound'])))
    # Rare-input coherence is not hidden in a metric. Current projection does
    # not preserve a singleton initial state; forcing it changes pi_min.
    n=out['n'];parts=out['partition'];i=parts[0][0];ck(len(parts[0])>1)
    singleton_residual_l1=2*R(len(parts[0])-1,len(parts[0]));ck(singleton_residual_l1>1)
    rare_kappa=R(out['column_sum_upper'])*n;balanced_kappa=R(out['column_sum_upper'])/R(out['pi_min'])
    ck(rare_kappa/balanced_kappa==min(map(len,parts)))
    # An actual stochastic bad-column example, not a claimed lower bound.
    c=R(1,4);bad_B=1+(n-1)*c;ck(bad_B>=n/4)
    # Stochastic != L2 contraction, even on an orthogonal complement.
    A=s.Matrix([[1,0,0,0]]*3+[[0,1,0,0]]);P=s.ones(4)/4;Q=s.eye(4)-P
    F=Q*A*Q;ck((F.T*F).trace()>1)
    return {'checks':checks,'maximum_numerical_truth_error':worst,
            'truth_scope':'Floating posthoc fixture evaluation, not an exact full-world proof or acquisition input.',
            'singleton_projection_residual_l1':str(singleton_residual_l1),
            'singleton_outgoing_kappa_penalty':str(rare_kappa/balanced_kappa),
            'bad_column_example_B':str(bad_B),
            'bad_column_scope':'Constant point-reset mass restores B=Theta(n); spectral acquisition may become quadratic.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--n',type=int,default=4096);args=parser.parse_args();start=time.perf_counter()
    stem='large_'+str(args.n);out=json.loads((ROOT/(stem+'_result.json')).read_text())
    raw=(ROOT/(stem+'_observations.json.gz')).read_bytes();assert hashlib.sha256(raw).hexdigest()==out['transcript_gzip_sha256']
    records=json.loads(gzip.decompress(raw))['records'];b=out['task_b'];e=out['task_ell_numer'];den=out['task_ell_denominator']
    checks=replay(out,records,expected_b=b,expected_ell_num=e,expected_ell_den=den,expected_length=24,expected_tolerance=R(1,50))
    # Task substitution must fail before costly norm replay.
    for L,eps in [(23,R(1,50)),(24,R(1,25)),(True,R(1,50)),(24,.02)]:
        try:replay(out,records,expected_b=b,expected_ell_num=e,expected_ell_den=den,expected_length=L,expected_tolerance=eps)
        except AssertionError:checks+=1
        else:raise AssertionError('task substitution admitted')
    extra=extra_checks(out);checks+=extra['checks']
    max_count=max(c for x in records for c in ([x['N']]))
    result={'status':'PASS','checks':checks,'n':args.n,'extra':extra,
            'maximum_batch_denominator_bits':max_count.bit_length(),
            'seconds':time.perf_counter()-start,
            'scope':'Exact replay under external authentic iid/freshness premises; no independent review. Synthetic aggregate generation is not actual billion-call execution.',
            'bound_source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                                  [Path(__file__),ROOT/'large_acquisition.py',ROOT/'large_routing_source.py',ROOT/'quadratic_leakage.py',ROOT/'sparse_norm_probe.py',ROOT/(stem+'_result.json')]}}
    (ROOT/(stem+'_replay_checks.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
