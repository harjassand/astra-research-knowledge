#!/usr/bin/env python3
"""Acquire complete-cell references and exact finite stationary comparisons.

The finite cell is NOT substituted for the full uncontrolled generator.
"""
from collections import defaultdict,deque
from fractions import Fraction as F
from math import factorial,prod
from pathlib import Path
import json
import sympy as sp
from coverability_clock import cubic,rate_at

P=Path(__file__).resolve().parent

def graph_data(raw):
    adj=defaultdict(list);complexes=set()
    for i,(y,z,k) in enumerate(raw):adj[y].append((z,i));complexes|={y,z}
    def path(src,dst):
        queue=deque([src]);back={src:None}
        while queue:
            x=queue.popleft()
            if x==dst:break
            for z,i in adj[x]:
                if z not in back:back[z]=(x,i);queue.append(z)
        assert dst in back,'raw graph is not weakly reversible'
        out=[];x=dst
        while back[x] is not None:u,i=back[x];out.append(i);x=u
        return list(reversed(out))
    k0=[0]*len(raw)
    for i,(y,z,k) in enumerate(raw):
        for j in [i]+path(z,y):k0[j]+=1
    assert min(k0)>0
    bal=defaultdict(int)
    for (y,z,k),c in zip(raw,k0):bal[y]-=c;bal[z]+=c
    assert not any(bal.values())
    linked={}
    for y in complexes:
        queue=[y];seen={y}
        for v in queue:
            for w,i in adj[v]:
                if w not in seen:seen.add(w);queue.append(w)
        linked[y]=[i for i,(v,w,k) in enumerate(raw) if v in seen]
    return k0,linked

def word_cell(raw,start,word):
    k0,linked=graph_data(raw);blocks=set();x=start
    for i in word:
        y,z,k=raw[i];assert rate_at(x,y,k)>0
        residual=tuple(a-b for a,b in zip(x,y))
        blocks.add((tuple(linked[y]),residual))
        x=tuple(a-u+v for a,u,v in zip(x,y,z))
    return blocks,x,k0

def build(raw,blocks,k0,translation=(0,0,0),reference=False):
    edges=defaultdict(F);states=set()
    for indices,residual in blocks:
        r=tuple(a+b for a,b in zip(residual,translation))
        for i in indices:
            y,z,k=raw[i];src=tuple(a+b for a,b in zip(r,y));dst=tuple(a+b for a,b in zip(r,z))
            q=F(rate_at(src,y,k0[i] if reference else k))
            assert q>0
            edges[src,dst]+=q;states|={src,dst}
    states=sorted(states);index={s:i for i,s in enumerate(states)}
    Q=sp.zeros(len(states))
    for (src,dst),q in edges.items():
        i,j=index[src],index[dst];Q[i,j]+=sp.Rational(q.numerator,q.denominator);Q[i,i]-=sp.Rational(q.numerator,q.denominator)
    return states,index,Q

def pi_relative(Q):
    A=Q.T.copy();rhs=sp.zeros(Q.rows,1)
    A[-1,:]=sp.ones(1,Q.rows);rhs[-1]=1
    pi=list(A.inv()*rhs)
    assert all(v>0 for v in pi)
    assert sp.Matrix(1,Q.rows,pi)*Q==sp.zeros(1,Q.rows)
    return pi

if __name__=='__main__':
    raw=cubic();witnesses=json.loads((P/'results/deletion_words.json').read_text())['words'];rows=[]
    for witness in witnesses:
        start=tuple(witness['source']);word=witness['word'];blocks,end,k0=word_cell(raw,start,word)
        a=min(k/F(kref) for (y,z,k),kref in zip(raw,k0));b=max(k/F(kref) for (y,z,k),kref in zip(raw,k0))
        checks=[]
        for tr in [(0,0,0),(0,3,0),(0,10,0),(0,0,5)]:
            states,ix,Q=build(raw,blocks,k0,tr);s=tuple(x+y for x,y in zip(start,tr));t=tuple(x+y for x,y in zip(end,tr))
            states0,ix0,Q0=build(raw,blocks,k0,tr,True);assert states0==states
            mu=[sp.Rational(1,prod(factorial(v) for v in x)) for x in states]
            assert sp.Matrix(1,len(states),mu)*Q0==sp.zeros(1,len(states))
            pi=pi_relative(Q);ratio=pi[ix[s]]/pi[ix[t]];r0=mu[ix[s]]/mu[ix[t]]
            C=(b/a)**(len(states)-1)
            assert F(r0)/C<=F(ratio)<=C*F(r0)
            checks.append({'translation':tr,'states':len(states),'pi_start_over_end':str(ratio),'reference_start_over_end':str(r0),'tree_comparison_verified':True})
        rows.append({'basis_source':start,'basis_target':end,'blocks':len(blocks),'cell_states':checks[0]['states'],
                     'balanced_reference_rates':k0,'rate_ratio_min':str(a),'rate_ratio_max':str(b),
                     'constant_tree_bound':str(C),'checks':checks})
        print(start,'blocks',len(blocks),'states',checks[0]['states'],'exact checks',len(checks),flush=True)
    (P/'results/translated_cells.json').write_text(json.dumps({'scope':'Acquired exact constant-size complete translated cells; competing omitted cells are not controlled by this calculation.','results':rows},indent=2)+'\n')
