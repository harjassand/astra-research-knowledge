#!/usr/bin/env python3
"""Sparse, task-weighted observation admission. Ordinary model-based exploration.

The synthetic sampler returns multinomial counts, distributed exactly as a
batch of iid row draws. ALL implied individual draws are charged. Generating
aggregated simulation counts is not a measured physical acquisition backend.
"""
from fractions import Fraction as F
import copy
import json
import math
from pathlib import Path
import time
import numpy as np


def ceil_log2(x):
    n,d=x.numerator,x.denominator;k=0
    while d<n:d*=2;k+=1
    return k


def bellman(centers,radii,initial,m,L):
    states=set(initial)
    for (i,a),row in centers.items():states.add(i);states.update(row)
    states=sorted(states);V=[{i:F(0) for i in states}];policy=[]
    for t in range(1,L+1):
        vals={};pol={}
        for i in states:
            options=[]
            for a in range(m):
                row=centers.get((i,a),{i:F(1)});r=radii.get((i,a),F(2))
                options.append(r+sum(p*V[-1][j] for j,p in row.items()))
            a=max(range(m),key=lambda a:options[a]);pol[i]=a;vals[i]=min(F(2),options[a])
        V.append(vals);policy.append(pol)
    value=sum(p*V[L][i] for i,p in initial.items())
    occupancy={};dist=initial.copy()
    for remaining in range(L,0,-1):
        nxt={}
        for i,p in dist.items():
            a=policy[remaining-1][i];key=(i,a);occupancy[key]=occupancy.get(key,F(0))+p
            for j,q in centers.get(key,{i:F(1)}).items():nxt[j]=nxt.get(j,F(0))+p*q
        dist=nxt
    scores={key:w*radii.get(key,F(2)) for key,w in occupancy.items()}
    return value,scores,len(states)


class SyntheticCounts:
    def __init__(self):
        # The learner receives only named-row samples, not this active set.
        self.labels=[17,731,9001,42,65003,105,999999937]
        self._index={x:i for i,x in enumerate(self.labels)}
        self.rng=np.random.default_rng(9741);self.draws=0;self.calls=0
    def distribution(self,i,a):
        if i not in self._index:return {i:F(1)}
        j=self._index[i];n=len(self.labels)
        return {self.labels[(j+1+a)%n]:F(1,4),self.labels[(j+3+2*a)%n]:F(3,4)}
    def sample(self,i,a,N):
        row=self.distribution(i,a);labels=list(row)
        counts=self.rng.multinomial(N,[float(row[j]) for j in labels]);self.draws+=N;self.calls+=1
        return {j:int(k) for j,k in zip(labels,counts) if k}


def acquire(sampler,initial,m,L,tolerance,delta=F(1,1000),max_calls=180):
    centers={};radii={};knowledge={};visits={};ledger=[];start=time.perf_counter()
    for call in range(max_calls+1):
        risk,scores,nstates=bellman(centers,radii,initial,m,L)
        if risk/2<=tolerance:
            return centers,radii,{'admitted':True,'observation_bound':str(risk/2),'row_updates':len(ledger),
                                 'length':L,'tolerance':str(tolerance),'failure_probability':str(delta),
                                 'logical_iid_draws':sampler.draws,'center_states':nstates,'stored_center_entries':sum(len(r) for r in centers.values()),
                                 'elapsed_aggregated_simulation_seconds':time.perf_counter()-start,'ledger':ledger}
        if call==max_calls:break
        key=max(sorted(scores),key=lambda key:scores[key]);i,a=key
        visits[key]=visits.get(key,0)+1;p=2+visits[key];zeta=F(1,2**p)
        train=sampler.sample(i,a,64)
        S=knowledge.get(key,set())|set(train)|{i}
        # Telescoping failure allocation sums to delta over all adaptive calls.
        dc=delta/F((call+1)*(call+2));K=ceil_log2(F(2*(len(S)+1))/dc)
        N=math.ceil(F(K,2)/zeta**2)
        validation=sampler.sample(i,a,N)
        q=F(sum(v for j,v in validation.items() if j not in S),N)
        center={j:F(validation.get(j,0),N) for j in S}
        center[i]=center.get(i,F(0))+q;center={j:p for j,p in center.items() if p}
        assert sum(center.values())==1
        radius=min(F(2),(len(S)+1)*zeta+2*q)
        centers[key]=center;radii[key]=radius
        knowledge[key]=S|set(validation)
        ledger.append({'call':call,'row':[i,a],'prior_risk_bound':str(risk/2),'support_bins':len(S),
                       'zeta':str(zeta),'failure_allocation':str(dc),'training_draws':64,'validation_draws':N,
                       'training_counts':[[j,v] for j,v in sorted(train.items())],
                       'validation_counts':[[j,v] for j,v in sorted(validation.items())],
                       'unseen_validation_fraction':str(q),'row_l1_radius':str(radius)})
    return centers,radii,{'admitted':False,'logical_iid_draws':sampler.draws,'row_updates':len(ledger),'ledger':ledger,
                          'scope':'INCONCLUSIVE at declared row-update budget.'}


def value(rows,initial,b,word):
    dist=initial.copy()
    for a in word:
        nxt={}
        for i,p in dist.items():
            for j,q in rows(i,a).items():nxt[j]=nxt.get(j,F(0))+p*q
        dist=nxt
    return sum(p*b(i) for i,p in dist.items())


def verify_record(record,initial,m,*,expected_length,expected_tolerance,expected_delta):
    """Check admission conditional on authentic iid data, not data provenance."""
    try:
        if type(record) is not dict or record['admitted'] is not True:return False
        if type(m) is not int or m<1 or type(initial) is not dict or not initial:return False
        if any(type(i) is not int or i<0 or isinstance(p,(bool,float)) or not isinstance(p,(int,F)) or p<0 for i,p in initial.items()):return False
        if sum(initial.values())!=1:return False
        if type(expected_length) is not int or expected_length<0:return False
        if type(record['length']) is not int or record['length']!=expected_length:return False
        if isinstance(expected_tolerance,(bool,float)) or isinstance(expected_delta,(bool,float)):return False
        tol=F(expected_tolerance);delta=F(expected_delta)
        if not 0<delta<1 or tol<=0:return False
        if type(record['tolerance']) is not str or F(record['tolerance'])!=tol:return False
        if type(record['failure_probability']) is not str or F(record['failure_probability'])!=delta:return False
        centers={};radii={};knowledge={};draws=0
        def counts(pairs,N):
            if type(N) is not int or N<1 or type(pairs) is not list:raise ValueError('count input')
            out={}
            for pair in pairs:
                if type(pair) is not list or len(pair)!=2:raise ValueError('count pair')
                j,k=pair
                if type(j) is not int or j<0 or type(k) is not int or k<1 or j in out:raise ValueError('count alias/duplicate')
                out[j]=k
            if sum(out.values())!=N:raise ValueError('batch total')
            return out
        for call,row in enumerate(record['ledger']):
            if type(row['call']) is not int or row['call']!=call:return False
            i,a=row['row']
            if type(i) is not int or i<0 or type(a) is not int or not 0<=a<m:return False
            key=(i,a);train=counts(row['training_counts'],row['training_draws'])
            validation=counts(row['validation_counts'],row['validation_draws']);N=row['validation_draws']
            S=knowledge.get(key,set())|set(train)|{i}
            if type(row['zeta']) is not str or type(row['failure_allocation']) is not str:return False
            zeta=F(row['zeta']);dc=delta/F((call+1)*(call+2))
            if zeta<=0 or F(row['failure_allocation'])!=dc:return False
            K=ceil_log2(F(2*(len(S)+1))/dc)
            if N<F(K,2)/zeta**2:return False
            q=F(sum(v for j,v in validation.items() if j not in S),N)
            center={j:F(validation.get(j,0),N) for j in S};center[i]=center.get(i,F(0))+q
            centers[key]={j:p for j,p in center.items() if p};radii[key]=min(F(2),(len(S)+1)*zeta+2*q)
            if type(row['row_l1_radius']) is not str or F(row['row_l1_radius'])!=radii[key]:return False
            knowledge[key]=S|set(validation);draws+=row['training_draws']+N
        risk,_,_=bellman(centers,radii,initial,m,expected_length)
        if type(record['observation_bound']) is not str or F(record['observation_bound'])!=risk/2:return False
        if type(record['logical_iid_draws']) is not int or record['logical_iid_draws']!=draws:return False
        return bool(risk/2<=tol)
    except (KeyError,TypeError,ValueError,IndexError,AttributeError,ZeroDivisionError):return False


def run():
    sampler=SyntheticCounts();initial={17:F(1)};m=2;L=12;tol=F(1,10)
    centers,radii,result=acquire(sampler,initial,m,L,tol)
    assert result['admitted'];checks=1
    assert verify_record(result,initial,m,expected_length=L,expected_tolerance=tol,expected_delta=F(1,1000));checks+=1
    for key,val in [('length',True),('tolerance',True),('observation_bound','0'),('logical_iid_draws',True)]:
        wrong=copy.deepcopy(result);wrong[key]=val
        assert not verify_record(wrong,initial,m,expected_length=L,expected_tolerance=tol,expected_delta=F(1,1000));checks+=1
    for key,val in [('validation_draws',True),('failure_allocation','1'),('row_l1_radius','0')]:
        wrong=copy.deepcopy(result);wrong['ledger'][0][key]=val
        assert not verify_record(wrong,initial,m,expected_length=L,expected_tolerance=tol,expected_delta=F(1,1000));checks+=1
    wrong=copy.deepcopy(result);wrong['ledger'][0]['validation_counts'][0][1]=True
    assert not verify_record(wrong,initial,m,expected_length=L,expected_tolerance=tol,expected_delta=F(1,1000));checks+=1
    assert not verify_record(result,initial,m,expected_length=L+1,expected_tolerance=tol,expected_delta=F(1,1000));checks+=1
    assert not verify_record(result,initial,m,expected_length=L,expected_tolerance=tol/2,expected_delta=F(1,1000));checks+=1
    # This checks the simulated draw realization, not a replacement for the
    # simultaneous confidence proof or a claim of universal empirical coverage.
    for key,C in centers.items():
        A=sampler.distribution(*key);alllabels=set(A)|set(C)
        assert sum(abs(A.get(j,F(0))-C.get(j,F(0))) for j in alllabels)<=radii[key];checks+=1
    center=lambda i,a:centers.get((i,a),{i:F(1)})
    b=lambda i:F(i==65003);worst=F(0)
    # Full enumeration here is a test only, never used by acquisition.
    for k in range(2**L):
        word=[(k>>j)&1 for j in range(L)]
        err=abs(value(sampler.distribution,initial,b,word)-value(center,initial,b,word))
        assert err<=F(result['observation_bound']);worst=max(worst,err);checks+=1
    # Unseen-state hazard: an unobserved label does not need to be enumerated,
    # but its possible mass must stay in the observed predecessor's radius.
    C={(0,0):{0:F(1)}};R={(0,0):F(1,50)};risk,_,_=bellman(C,R,{0:F(1)},1,10)
    hidden=lambda i,a:({0:F(99,100),999999999:F(1,100)} if i==0 else {i:F(1)})
    err=value(hidden,{0:F(1)},lambda i:F(i==999999999),[0]*10)
    assert err<=risk/2;checks+=1
    naive,_,_=bellman(C,{(0,0):F(0)},{0:F(1)},1,10)
    assert naive==0 and err>0;checks+=1
    result.update({'checks':checks,'universe_label_bound':10**9,'initial_labels_supplied':[17],
                   'maximum_enumerated_word_error':float(worst),'enumerated_words':2**L,
                   'scope':'Sparse probe locations acquired from row samples and a paid Bellman overapproximation. Counts simulate many iid draws in aggregate; logical sample cost is explicit. No rank discovery or superiority over ordinary model-based exploration is claimed.'})
    return result


if __name__=='__main__':
    out=run();Path('risk_frontier_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
