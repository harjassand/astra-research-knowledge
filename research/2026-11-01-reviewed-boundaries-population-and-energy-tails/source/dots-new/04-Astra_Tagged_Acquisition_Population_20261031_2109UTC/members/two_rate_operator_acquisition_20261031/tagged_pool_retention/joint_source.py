#!/usr/bin/env python3
"""Joint sampled source-row/block and pooled microscopic counts.

The learner receives only ordinary sufficient statistics of (chosen row,
destination label) calls. Private mixture/wiring never reaches the learner.
No missing historical tags are reconstructed. This generator makes NEW data.
"""
from pathlib import Path
import json,sys
from fractions import Fraction as F
import numpy as np
ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent;sys.path.insert(0,str(PARENT))
from large_routing_source import RoutingSource

class TaggedPoolSource:
    def __init__(self,n=4096,seed=6201001,degree=16):
        assert type(n) is int and n>=4 and n%4==0
        assert type(degree) is int and degree>=2 and degree&(degree-1)==0
        q=RoutingSource(n,degree=degree);q._tau=.04
        self.n=n;self.m=2;self.degree=degree;self.rng=np.random.default_rng(seed)
        self.adj=np.asarray(q._adj,dtype=np.int64);self.groups=np.asarray(q._groups,dtype=np.int64)
        self.which=np.asarray(q._which,dtype=np.int64);self.actions=np.asarray(q._actions,dtype=np.int64)
        self.glob=np.asarray(q._global,dtype=np.int64);self.reset=np.asarray(q._reset,dtype=np.int64)
        self.branch=[1-q._tau-2*q._noise,q._tau,q._noise,q._noise]
        # Same ideal multinomial argument law as the original _row_counts:
        # first three exact binary64 values, last category remaining mass.
        p=list(map(F,self.branch[:3]));p.append(1-sum(p));assert min(p)>=0
        assert F(float(p[3]))==p[3]
        self.branch[3]=float(p[3])  # explicitly normalized, same first-three argument law
        self.branch_exact=p;self.logical_calls=0;self.individual_macro_reset_draws=0;self.row_batches=0;self.allocated_macro_peak=0
    def public_task(self):
        return [int(x==1) for x in self.which],[int(x==0) for x in self.which],self.n//4
    def batch(self,a,part,N,which,r):
        assert type(a) is int and 0<=a<2 and type(N) is int and 0<=N<2**52
        assert all(isinstance(i,(int,np.integer)) and not isinstance(i,(bool,np.bool_)) for i in part)
        k=len(part);assert k>0 and k&(k-1)==0 and len(set(part))==k and min(part)>=0 and max(part)<self.n
        assert type(r) is int and r>0 and self.n*r<2**62 and len(which)==self.n and all(isinstance(v,(int,np.integer)) and not isinstance(v,(bool,np.bool_)) and 0<=int(v)<r for v in which)
        part=np.asarray(part,dtype=np.int64);which=np.asarray(which,dtype=np.int64)
        # Source-row choices are made before outcomes and are retained. The
        # power-of-two fixture blocks make these argument probabilities exact.
        sizes=self.rng.multinomial(N,np.full(k,1/k));branches=np.empty((k,4),dtype=np.int64)
        pooled=np.zeros(self.n,dtype=np.int64);tagged=np.zeros((k,r),dtype=np.int64)
        for pos,i in enumerate(part):
            br=self.rng.multinomial(int(sizes[pos]),self.branch);branches[pos]=br
            local=self.rng.multinomial(int(br[0]),np.full(self.degree,1/self.degree))
            js=self.adj[a,i];np.add.at(pooled,js,local);np.add.at(tagged[pos],which[js],local)
            j=self.glob[a,i];pooled[j]+=br[2];tagged[pos,which[j]]+=br[2]
        # Actually generate the macro/reset destination labels, preserving
        # their joint source-row/block metadata. This is not independent
        # generation of two marginals. The dominant local branch is compressed.
        for kind in (1,3):
            owners=np.repeat(np.arange(k,dtype=np.int64),branches[:,kind]);num=len(owners)
            if kind==1:
                groups=self.actions[a,self.which[part[owners]]]
                dest=self.groups[groups,self.rng.integers(self.n//4,size=num)]
            else:dest=self.reset[a,self.rng.integers(self.n//2,size=num)]
            pooled+=np.bincount(dest,minlength=self.n)
            tagged+=np.bincount(owners*r+which[dest],minlength=k*r).reshape(k,r)
            self.individual_macro_reset_draws+=num;self.allocated_macro_peak=max(self.allocated_macro_peak,num)
        assert int(pooled.sum())==int(tagged.sum())==N and np.array_equal(tagged.sum(axis=1),sizes)
        assert np.array_equal(tagged.sum(axis=0),np.bincount(which,weights=pooled,minlength=r).astype(np.int64))
        self.logical_calls+=N;self.row_batches+=k
        return {'a':a,'N':N,'source_rows':list(map(int,part)),'row_totals':list(map(int,sizes)),
                'row_block_counts':tagged.tolist(),'pooled_micro_counts':pooled.tolist()}
