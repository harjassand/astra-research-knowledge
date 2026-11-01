#!/usr/bin/env python3
"""Exhaustively execute the actual tiny source with exact sampling branches."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import factorial
import hashlib,json,sys
import numpy as np
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT))
from joint_source import TaggedPoolSource

class Choice(Exception):
    def __init__(self,outcomes):self.outcomes=outcomes

def compositions(N,k):
    if k==1:yield (N,);return
    for c in range(N+1):
        for rest in compositions(N-c,k-1):yield (c,)+rest

class ExactRNG:
    def __init__(self,path):self.path=path;self.used=0
    def choose(self,options):
        if self.used==len(self.path):raise Choice(options)
        j=self.path[self.used];self.used+=1;return options[j][0]
    def multinomial(self,N,p):
        ps=[F(float(x)) for x in p[:-1]];ps.append(1-sum(ps));out=[]
        for cs in compositions(N,len(ps)):
            prob=F(factorial(N))
            for c,p in zip(cs,ps):prob*=p**c;prob/=factorial(c)
            if prob:out.append((np.array(cs,dtype=np.int64),prob))
        return self.choose(out)
    def integers(self,high,size):
        return self.choose([(np.array(xs,dtype=np.int64),F(1,high**size)) for xs in product(range(high),repeat=size)])

def key(out):return json.dumps({k:out[k] for k in ('row_totals','row_block_counts','pooled_micro_counts')},sort_keys=True)

def run():
    checks=0;cases=[]
    for a,part,which in [(0,[0,2],[0,0,1,1]),(1,[1,3],[0,1,0,1])]:
        queue=[([],F(1))];law={};leaves=0
        while queue:
            path,prob=queue.pop();q=TaggedPoolSource(4,degree=2);q.rng=ExactRNG(path)
            try:out=q.batch(a,part,2,which,2)
            except Choice as branch:
                for j,(v,p) in enumerate(branch.outcomes):queue.append((path+[j],prob*p))
            else:law[key(out)]=law.get(key(out),F(0))+prob;leaves+=1
        q=TaggedPoolSource(4,degree=2);events=[]
        for pos,i in enumerate(part):
            weights=[F(0)]*4
            for j in q.adj[a,i]:weights[int(j)]+=q.branch_exact[0]/q.degree
            g=q.actions[a,q.which[i]]
            for j in q.groups[g]:weights[int(j)]+=q.branch_exact[1]/len(q.groups[g])
            weights[int(q.glob[a,i])]+=q.branch_exact[2]
            for j in q.reset[a]:weights[int(j)]+=q.branch_exact[3]/len(q.reset[a])
            assert sum(weights)==1;checks+=1
            for j,p in enumerate(weights):
                if p:events.append((pos,j,p/len(part)))
        ordinary={}
        for left,right in product(events,repeat=2):
            totals=[0]*2;tagged=[[0,0] for _ in part];micro=[0]*4;prob=F(1)
            for pos,j,p in (left,right):totals[pos]+=1;tagged[pos][which[j]]+=1;micro[j]+=1;prob*=p
            k=key({'row_totals':totals,'row_block_counts':tagged,'pooled_micro_counts':micro});ordinary[k]=ordinary.get(k,F(0))+prob
        assert law==ordinary and sum(law.values())==1;checks+=len(law)+2
        cases.append({'action':a,'mixed_source_rows':part,'observed_partition_labels':which,'exact_sampler_execution_leaves':leaves,'joint_statistics_outcomes':len(law),'law_equals_independent_ordinary_transitions':True})
    return {'status':'PASS_EXACT_JOINT_GENERATOR_LAW','checks':checks,'cases':cases,'scope':'Actual generator executed with exact exhaustive ideal sampling branches for N=2 and mixed blocks. General hierarchical law has an ordinary proof; real PRNG ideality is not authenticated.','source_sha256':hashlib.sha256((ROOT/'joint_source.py').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
if __name__=='__main__':
    out=run();(ROOT/'joint_law_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
