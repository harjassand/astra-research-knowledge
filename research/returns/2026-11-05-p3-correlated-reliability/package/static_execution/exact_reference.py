"""Exponential reference used only after/beside acquisition for <=18 bits.

This module is not imported by gibbs_static. No acquisition probability or
sample is calculated from its enumerated states or its exact partition sums.
"""
from fractions import Fraction as F
from gibbs_static import BinaryGibbs, Network

class ExactReference:
    def __init__(self,model:BinaryGibbs,network:Network):
        if model.m>18:raise ValueError('reference limited to at most 2^18 states')
        self.model=model;self.network=network
        self.weights=tuple(model.weight(x) for x in range(1<<model.m))
        self.Z=sum(self.weights,F(0))
        self.fail_weight=sum((w for x,w in enumerate(self.weights) if network.disconnected(x)),F(0))
        self.p=self.fail_weight/self.Z
    def partition(self,pins:dict[int,int])->F:
        return sum((w for x,w in enumerate(self.weights) if all(((x>>i)&1)==v for i,v in pins.items())),F(0))
    def marginal(self,i:int,pins:dict[int,int]|None=None)->F:
        p={} if pins is None else dict(pins)
        if i in p:return F(p[i])
        den=self.partition(p);p[i]=1
        return self.partition(p)/den
    def conditional_failure_marginals(self):
        return [sum((w for x,w in enumerate(self.weights) if self.network.disconnected(x) and ((x>>i)&1)),F(0))/self.fail_weight for i in range(self.model.m)]
    def independent_same_marginals_failure(self)->F:
        marg=[self.marginal(i) for i in range(self.model.m)]
        out=F(0)
        for x in range(1<<self.model.m):
            if not self.network.disconnected(x):continue
            w=F(1)
            for i,p in enumerate(marg):w*=p if ((x>>i)&1) else 1-p
            out+=w
        return out
    def conditional_empirical_tv(self,hist,n):
        return sum((abs(F(hist.get(x,0),n)-(w/self.fail_weight if self.network.disconnected(x) else F(0))) for x,w in enumerate(self.weights)),F(0))/2
