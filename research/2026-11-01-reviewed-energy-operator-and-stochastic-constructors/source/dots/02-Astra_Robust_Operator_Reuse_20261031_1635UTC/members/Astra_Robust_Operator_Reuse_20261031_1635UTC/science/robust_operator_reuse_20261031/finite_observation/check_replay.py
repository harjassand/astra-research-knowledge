#!/usr/bin/env python3
"""Executable author checks; synthetic truth appears only in test/evaluation."""
import copy
import itertools
import json
from pathlib import Path
import random
import re
import time
import numpy as np
import sympy as sp
from robust_replay import *
from learn import fixture


def actual(A,b,ell,word):
    x=b
    for a in word:x=A[a]*x
    return (ell.T*x)[0]


def noncommon_fixture():
    A,b,ell=fixture();A=[sp.Matrix(X) for X in A]
    A[0][0,0]-=sp.Rational(1,100000);A[0][0,1]+=sp.Rational(1,100000)
    A[1][1,1]-=sp.Rational(1,50000);A[1][1,2]+=sp.Rational(1,50000)
    assert all(X*sp.ones(12,1)==sp.ones(12,1) for X in A)
    assert sp.Matrix.vstack(*[X.T-sp.eye(12) for X in A]).nullspace()==[]
    return A,b,ell


def candidate(boxes,b,ell,h,directions,L,tol,q=30):
    basis=[]
    for x in [sp.ones(len(h),1),b,sp.diag(*h).inv()*ell]+directions:
        # A numerical proposal close to a prior span need not be expanded.
        v=residual(x,basis,h)
        if inner(v,v,h)<sp.Rational(1,2**40):continue
        append_basis(x,basis,h)
    V=sp.Matrix.hstack(*basis);B,scales=stable_blocks(centers(boxes),V,h)
    cert=certificate(boxes,b,ell,V,h,B,L,q)
    model={'basis':V,'metric':h,'operators':B,'boxes':boxes,'certificate':cert,'tolerance':tol,'ledger':{}}
    return model,{'rank':V.cols,'bound':float(cert['bound']),'pass':bool(cert['bound']<=tol),'stabilizing_scales':scales}


def random_range(boxes,b,ell,h,L,tol):
    start=time.perf_counter();C=centers(boxes);H=sp.diag(*h);adj=[H.inv()*A.T*H for A in C]
    rng=random.Random(771);dirs=[sp.Matrix([rng.choice([-1,1]) for _ in h]) for _ in range(2)]
    rows=[];mvps=0;verification_mvps=0
    for q in range(9):
        if q:
            dirs=[sum((adj[a]*C[a]*x for a in range(len(C))),sp.zeros(len(h),1))/len(C) for x in dirs]
            mvps+=2*len(C)*len(dirs)
        model,row=candidate(boxes,b,ell,h,dirs,L,tol);row['power']=q;rows.append(row)
        verification_mvps+=2*len(C)*row['rank']
        if row['pass']:
            model['ledger']={'acquisition_seconds':time.perf_counter()-start,'power_actions':mvps,
                             'all_candidate_verification_actions':verification_mvps,'candidate_dense_center_projection_blocks':2*len(C)*len(rows),'trials':rows}
            return model
    return {'admitted':False,'ledger':{'acquisition_seconds':time.perf_counter()-start,'trials':rows,'power_actions':mvps,'all_candidate_verification_actions':verification_mvps}}


def spectral(boxes,b,ell,h,L,tol):
    start=time.perf_counter();C=centers(boxes);root=np.sqrt(np.array(h,dtype=float).reshape(-1))
    tilde=[root[:,None]*np.array(A,dtype=float)/root[None,:] for A in C]
    normal=sum(A.T@A for A in tilde)/len(C);_,V=np.linalg.eigh(normal)
    dirs=[];rows=[]
    for j in range(1,len(h)+1):
        v=V[:,-j]/root
        dirs.append(sp.Matrix([sp.Rational(round(float(x)*2**24),2**24) for x in v]))
        model,row=candidate(boxes,b,ell,h,dirs,L,tol);row['eigendirections']=j;rows.append(row)
        if row['pass']:
            model['ledger']={'acquisition_seconds':time.perf_counter()-start,'trials':rows,
                             'scope':'Dense joint-normal eigensolve paid in time; float eigendirections are proposals only, followed by exact certification.'}
            return model
    return {'admitted':False,'ledger':{'acquisition_seconds':time.perf_counter()-start,'trials':rows}}


def bitmax(arrays):
    return max((max(abs(int(x.p)).bit_length(),int(x.q).bit_length()) for A in arrays for x in A),default=0)


def tune_grid(model,b,ell):
    start=time.perf_counter();old=model['certificate'];G=old['gram'];r=old['rank'];L=old['length']
    scale=old['normleft']*(L+1)*sqrt_up(max(G[i,i] for i in range(r))*r)+1
    for p in range(1,old['query_bits']+1):
        if old['model_bound']+scale*sp.Rational(1,2**(p+1))<=model['tolerance']:break
    model['certificate']=certificate(model['boxes'],b,ell,model['basis'],model['metric'],model['operators'],L,p)
    model['ledger']['query_grid_tuning_seconds']=time.perf_counter()-start
    model['ledger']['chosen_query_fractional_bits']=p
    return model


def prefix_replay(operators,u,output,words,p):
    start=time.perf_counter();compiled=compile_integer_replay(operators,u,output,p)
    compilation_seconds=time.perf_counter()-start
    start=time.perf_counter();cache={():compiled['initial_grid_state']};answers=[];actions=0;maxacc=0
    for word in words:
        key=()
        for a in word:
            nxt=key+(a,)
            if nxt not in cache:
                cache[nxt],acc=integer_step(compiled['operators'][a],cache[key]);actions+=1;maxacc=max(maxacc,acc)
            key=nxt
        outgrid,acc=integer_step(compiled['output'],cache[key]);maxacc=max(maxacc,acc)
        answers.append(sp.Rational(outgrid[0],1<<p))
    sec=time.perf_counter()-start
    payload=json.dumps({'grid_fractional_bits':p,'states':list(cache.values())},separators=(',',':')).encode()
    statebits=max([p+1]+[abs(x).bit_length() for v in cache.values() for x in v])
    return answers,{'seconds':sec,'integer_backend_compilation_seconds':compilation_seconds,
                    'common_denominator_coefficient_bits':compiled['common_denominator_coefficient_bits'],
                    'maximum_intermediate_accumulator_bits':maxacc,'retained_prefixes':len(cache),'new_vector_products':actions,
                    'retained_state_entries':sum(len(v) for v in cache.values()),'retained_state_integer_bits':statebits,
                    'retained_state_payload_bytes':len(payload),'operator_integer_bits':bitmax(operators),
                    'input_output_integer_bits':bitmax([u,output])}


def storage_ledger(model):
    rec=encode_model(model);payload=json.dumps(rec,separators=(',',':')).encode()
    def bits(x):
        if type(x) is int:return abs(x).bit_length()
        if type(x) is list:return max((bits(y) for y in x),default=0)
        if type(x) is dict:return max((bits(y) for y in x.values()),default=0)
        if type(x) is str and re.fullmatch(r'-?[0-9]+(?:/[1-9][0-9]*)?',x):
            y=sp.Rational(x);return max(abs(int(y.p)).bit_length(),int(y.q).bit_length())
        return 0
    return {'serialized_certificate_bytes':len(payload),'maximum_serialized_rational_integer_bits':bits(rec),
            'basis_entry_integer_bits':bitmax([model['basis']]),
            'scope':'All serialized certificate rationals scanned; peak acquisition intermediates are not fully instrumented.'}


def run():
    tic=time.perf_counter();checks=0
    A,b,ell=noncommon_fixture();L=30;tol=sp.Rational(1,100);oracle=OutwardOracle(A)
    model=acquire(oracle,b,ell,L,tol);assert 'certificate' in model;checks+=1
    model=tune_grid(model,b,ell)
    record=encode_model(model);boxes=model['boxes'];h=model['metric'];cert=model['certificate']
    assert verify(boxes,b,ell,record,expected_length=L,expected_tolerance=tol);checks+=1
    assert not verify(boxes,b,ell,record,expected_length=L+1,expected_tolerance=tol);checks+=1
    assert not verify(boxes,b,ell,record,expected_length=L,expected_tolerance=tol/2);checks+=1
    for key,value in [('length',True),('query_bits',True),('bound','0'),('tolerance',True)]:
        wrong=copy.deepcopy(record);wrong[key]=value
        assert not verify(boxes,b,ell,wrong,expected_length=L,expected_tolerance=tol);checks+=1
    wrong=copy.deepcopy(record);wrong['operators'][0]=encode_matrix(2*sp.eye(cert['rank']))
    assert not verify(boxes,b,ell,wrong,expected_length=L,expected_tolerance=tol);checks+=1
    wrong=copy.deepcopy(record);wrong['basis'][0][0]=[True,1]
    assert not verify(boxes,b,ell,wrong,expected_length=L,expected_tolerance=tol);checks+=1
    malformed=copy.deepcopy(boxes);malformed[0]=(sp.ones(12),sp.ones(12))
    assert not verify(malformed,b,ell,record,expected_length=L,expected_tolerance=tol);checks+=1
    low_budget=acquire(OutwardOracle(A),b,ell,L,tol,precisions=(8,12))
    assert low_budget['admitted'] is False;checks+=1
    # Exhaustive short words for the true family, centers, and another feasible
    # family inside the same observations; the bound is genuinely set-valued.
    C=centers(boxes);other=[(X+Y)/2 for X,Y in zip(A,C)]
    exhaustive_max=sp.Rational(0)
    for family in (A,C,other):
        for length in range(7):
            for word in itertools.product(range(2),repeat=length):
                ans,_=replay(model,word);err=abs(ans-actual(family,b,ell,word))
                assert err<=cert['bound'];exhaustive_max=max(exhaustive_max,err);checks+=1
    # An adaptively chosen realized word, with no independent query union bound.
    word=[];adaptive=[]
    for step in range(L):
        ans,_=replay(model,word);word.append(int(bool(ans>sp.Rational(1,100))))
        ans,ledger=replay(model,word);err=abs(ans-actual(A,b,ell,word))
        assert err<=cert['bound'];checks+=1;adaptive.append({'length':len(word),'error':float(err)})
    # A poor metric with no gap still gets a capped, nonexponential bound.
    D=[sp.Matrix([[1,0,0,0],[1,0,0,0],[0,1,0,0],[0,0,1,0]]),sp.Matrix([[0,0,1,0],[0,0,0,1],[0,1,0,0],[1,0,0,0]])]
    hh=sp.Matrix([1,1,1,997])/1000;bb=sp.eye(4)[:,0];ll=sp.eye(4)[:,1]
    bad,_=candidate([(X,X) for X in D],bb,ll,hh,[],1000,sp.Rational(10**20))
    bc=bad['certificate'];assert bc['alpha']>1;checks+=1
    assert bc['model_bound']<=bc['normleft']*bc['maxb']*1000*(bc['discrepancy']+bc['leave']);checks+=1
    for length in range(6):
        for w in itertools.product(range(2),repeat=length):
            assert abs(replay(bad,w)[0]-actual(D,bb,ll,w))<=bc['bound'];checks+=1
    # Fixed-precision ambiguity: the same row boxes contain two incompatible
    # true task answers, even if no computation or learning cost is charged.
    lower=[]
    for horizon in (2,10,100):
        eps=sp.Rational(1,100);p=4*eps/horizon
        gap=1-(1-p)**horizon
        assert gap>=3*eps and gap>2*eps;checks+=1
        lower.append({'horizon':horizon,'tolerance':str(eps),'common_entry_halfwidth':str(p/2),'answer_gap':float(gap)})
    # Identical retained observations, robust certificate, and bounded-bit
    # arithmetic for ordinary range/spectral/Krylov and full-space methods.
    rng=random.Random(8421)
    words=[[0]*L,[1]*L,[0,1]*15,[1,0]*15]+[[rng.randrange(2) for _ in range(L)] for _ in range(36)]
    truth=[actual(A,b,ell,w) for w in words]
    for full_p in range(1,31):
        full_bound=cert['observation_bound']+(sum(abs(x) for x in ell)*(L+1)+1)*sp.Rational(1,2**(full_p+1))
        if full_bound<=tol:break
    full,full_ledger=prefix_replay(C,b,ell,words,full_p);full_ledger['chosen_query_fractional_bits']=full_p
    assert full_bound<=tol and all(abs(x-y)<=full_bound for x,y in zip(full,truth));checks+=1
    rows={'retained_full_space_stochastic_center':{'bound':float(full_bound),'queries':full_ledger,
          'scope':'Receives all same observations, retained prefixes, and infinity-norm observation bound; no reduction acquisition required.'}}
    methods=[('ordinary_retained_bidirectional_Krylov',model),('retained_randomized_joint_normal_range',random_range(boxes,b,ell,h,L,tol)),
             ('retained_pooled_normal_spectral',spectral(boxes,b,ell,h,L,tol))]
    for label,md in methods:
        if 'certificate' not in md:rows[label]={'admitted':False,'acquisition':md['ledger']};continue
        md=tune_grid(md,b,ell)
        check_start=time.perf_counter();assert verify(boxes,b,ell,encode_model(md),expected_length=L,expected_tolerance=tol);checks+=1
        verification_seconds=time.perf_counter()-check_start
        cc=md['certificate'];answers,ql=prefix_replay(md['operators'],cc['right'],cc['output'],words,cc['query_bits'])
        assert all(x==replay(md,w)[0] for x,w in zip(answers,words));checks+=1
        err=max(abs(x-y) for x,y in zip(answers,truth));assert err<=cc['bound'];checks+=1
        rows[label]={'admitted':True,'rank':cc['rank'],'bound':float(cc['bound']),'queries':ql,'actual_max_error':float(err),
                     'extra_certificate_verification_seconds':verification_seconds,'storage':storage_ledger(md),'acquisition':md['ledger']}
    Path('replay_certificate.json').write_text(json.dumps(record,indent=2)+'\n')
    Path('observation_fixture.json').write_text(json.dumps({'boxes':[[encode_matrix(X) for X in pair] for pair in boxes],
                     'b':encode_matrix(b),'ell':encode_matrix(ell),'scope':'Observed finite intervals only; truth not needed by verifier.'},indent=2)+'\n')
    return {'checks':checks,'elapsed_seconds':time.perf_counter()-tic,'main_certificate':{k:str(v) for k,v in cert.items() if k not in ('gram','right','output')},
            'no_common_stationary_law':True,'short_exhaustive_words_per_family':127,'families_in_same_box':3,
            'exhaustive_max_error':float(exhaustive_max),'adaptive_max_error':max(row['error'] for row in adaptive),
            'capped_bad_metric':{'alpha':float(bc['alpha']),'horizon':1000,'bound':float(bc['bound'])},
            'fixed_precision_obstruction':lower,'methods':rows,
            'scope':'Synthetic ordinary-method comparison, not a new learner or practical broad superiority. Samples/real solver cost not executed; oracle output bits and all candidate computation are charged separately.'}


if __name__=='__main__':
    result=run();Path('replay_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
