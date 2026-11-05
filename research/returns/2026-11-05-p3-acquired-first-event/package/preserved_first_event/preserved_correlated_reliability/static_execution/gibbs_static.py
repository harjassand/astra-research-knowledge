"""Static rare-failure acquisition from an explicit positive rational Gibbs law.

The reference enumerator is deliberately in a separate module. This module
uses local factor tables, ordinary pinned heat bath, and graph cuts only.
Every numerical model calculation is rational. Logarithms for run budgets
are replaced by exact integer upper bounds. Statistical guarantees assume
independent fair bits; seeded PRNG execution is a reproducible diagnostic.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from fractions import Fraction as F
from functools import reduce
from math import gcd, lcm
from pathlib import Path
import json
import random
import subprocess
from typing import Iterable

HERE=Path(__file__).resolve().parent

def ceil_f(x:F)->int:
    return -((-x.numerator)//x.denominator)

def floor_log2(x:F)->int:
    if x<=0: raise ValueError('log requires positivity')
    k=x.numerator.bit_length()-x.denominator.bit_length()
    y=F(1<<k) if k>=0 else F(1,1<<(-k))
    return k if x>=y else k-1

def ceil_log2(x:F)->int:
    k=floor_log2(x)
    y=F(1<<k) if k>=0 else F(1,1<<(-k))
    return k if x==y else k+1

def dyadic_bound(q:F)->F:
    """w <= -ln(q) <= 9w/8, computed without a logarithm."""
    if not 0<q<1: raise ValueError('strict probability required')
    s=floor_log2(1/q)
    y=q*(1<<s)
    z=(1-y)/(1+y)
    return F(2*s,3)+2*z

@dataclass(frozen=True)
class Factor:
    scope:tuple[int,...]
    values:tuple[F,...]
    def __post_init__(self):
        if len(set(self.scope))!=len(self.scope) or len(self.values)!=(1<<len(self.scope)):
            raise ValueError('malformed factor table')
        if any(v<=0 for v in self.values): raise ValueError('full support requires positive factors')
    def at(self,x:int)->F:
        z=sum(((x>>j)&1)<<k for k,j in enumerate(self.scope))
        return self.values[z]

class BinaryGibbs:
    def __init__(self,m:int,factors:Iterable[Factor]):
        if m<1: raise ValueError('at least one variable required')
        self.m=m;self.factors=tuple(factors)
        if any(j<0 or j>=m for f in self.factors for j in f.scope):raise ValueError('factor variable out of range')
        self.neighbors=[];self.conditionals=[]
        self.qlo=[];self.qhi=[];self.influences=[]
        for i in range(m):
            incident=[f for f in self.factors if i in f.scope]
            nb=tuple(sorted({j for f in incident for j in f.scope if j!=i}))
            tab=[]
            for b in range(1<<len(nb)):
                x=sum(((b>>k)&1)<<j for k,j in enumerate(nb))
                w0=F(1);w1=F(1)
                for f in incident:w0*=f.at(x);w1*=f.at(x|(1<<i))
                tab.append(w1/(w0+w1))
            self.neighbors.append(nb);self.conditionals.append(tuple(tab))
            self.qlo.append(min(tab));self.qhi.append(max(tab))
            row={j:max(abs(tab[b]-tab[b^(1<<k)]) for b in range(len(tab))) for k,j in enumerate(nb)}
            self.influences.append(row)
        self.chi=max(sum(row.values(),F(0)) for row in self.influences)
        self.cut_weights=tuple(dyadic_bound(q) for q in self.qhi)
    def weight(self,x:int)->F:
        w=F(1)
        for f in self.factors:w*=f.at(x)
        return w
    def conditional(self,i:int,x:int)->F:
        z=sum(((x>>j)&1)<<k for k,j in enumerate(self.neighbors[i]))
        return self.conditionals[i][z]
    def validate_pins(self,pins:dict[int,int]):
        if any(i<0 or i>=self.m or v not in (0,1) for i,v in pins.items()):raise ValueError('bad pins')
    def conditional_range(self,i:int,pins:dict[int,int])->tuple[F,F]:
        self.validate_pins(pins)
        if i in pins:return F(pins[i]),F(pins[i])
        values=[]
        for b,q in enumerate(self.conditionals[i]):
            if all(j not in pins or ((b>>k)&1)==pins[j] for k,j in enumerate(self.neighbors[i])):
                values.append(q)
        return min(values),max(values)
    def logarithmic_contrast(self,c:int)->bool:
        return c>=1 and all(lo>=hi**c for lo,hi in zip(self.qlo,self.qhi))
    def odds_contrast(self)->F:
        return max((hi/(1-hi))/(lo/(1-lo)) for lo,hi in zip(self.qlo,self.qhi))
    def mixing_plan(self,pins:dict[int,int],tau:F)->dict:
        self.validate_pins(pins)
        if not 0<tau<1:raise ValueError('TV tolerance must be strictly between 0 and 1')
        if self.chi>=1:raise ValueError('Dobrushin uniqueness not certified')
        p=self.m-len(pins)
        if not p:return {'active':0,'steps':0,'tv_bound':F(0),'log2_budget':0}
        L=max(0,ceil_log2(F(p)/tau))
        steps=ceil_f(F(p*L)/(1-self.chi))
        return {'active':p,'steps':steps,'tv_bound':F(p,1<<L),'log2_budget':L}

class RandomCapError(RuntimeError):pass

class RationalBits:
    """Uniform integer rejection with a fixed per-operation cap."""
    def __init__(self,seed:int,retries:int=80,operation_cap:int=10**9):
        self.rng=random.Random(seed);self.retries=retries;self.operation_cap=operation_cap
        self.calls=0;self.bits=0;self.rejected=0
    def below(self,n:int)->int:
        if n<1:raise ValueError('positive integer required')
        self.calls+=1
        if self.calls>self.operation_cap:raise RandomCapError('random operation cap exceeded')
        if n==1:return 0
        b=(n-1).bit_length()
        for _ in range(self.retries):
            z=self.rng.getrandbits(b);self.bits+=b
            if z<n:return z
            self.rejected+=1
        raise RandomCapError('integer-rejection cap exceeded; no biased fallback')
    def bernoulli(self,p:F)->bool:
        if not 0<=p<=1:raise ValueError('invalid probability')
        return self.below(p.denominator)<p.numerator
    @property
    def abort_bound(self)->F:return F(self.operation_cap,1<<self.retries)

@dataclass
class SampleBatch:
    hist:Counter
    states:list[int]
    n:int
    steps:int
    tv_bound:F
    random_calls:int
    random_bits_or_words:int
    random_unit:str
    random_cap_abort_bound:F
    backend:str

class PinnedHeatbath:
    def __init__(self,model:BinaryGibbs,seed:int=1,native:bool=True):
        self.model=model;self.seed_rng=random.Random(seed);self.native=native
        self.batches=[];self.total_updates=0;self.total_draws=0
        self.total_random_calls=0;self.total_random_words64=0;self.total_python_bits=0
        self.total_cap_abort_bound=F(0)
        self.binary=HERE/'pinned_heatbath'
        native_ok=model.m<=60 and all(q.denominator.bit_length()<=128 for t in model.conditionals for q in t)
        self.native=native and native_ok
        self.model_text=''
        if self.native:
            src=HERE/'pinned_heatbath.cpp'
            if not self.binary.exists() or self.binary.stat().st_mtime<src.stat().st_mtime:
                subprocess.run(['c++','-O3','-std=c++17',str(src),'-o',str(self.binary)],check=True)
            out=[str(model.m)]
            for nb,tab in zip(model.neighbors,model.conditionals):
                out.append(' '.join([str(len(nb)),*(str(x) for x in nb)]))
                out.append(str(len(tab)))
                out.extend(f'{q.numerator} {q.denominator}' for q in tab)
            self.model_text='\n'.join(out)+'\n'
    def sample(self,pins:dict[int,int],n:int,tau:F,delta_bits:F=F(1,10**12),keep_states:bool=False)->SampleBatch:
        if n<1:raise ValueError('positive draw count required')
        plan=self.model.mixing_plan(pins,tau);steps=plan['steps']
        cap=max(1,2*n*steps)
        retries=max(1,ceil_log2(F(cap)/delta_bits))
        pinmask=sum(1<<i for i in pins);pinvals=sum(v<<i for i,v in pins.items())
        seed=self.seed_rng.getrandbits(64)
        if self.native:
            params=f'{pinmask} {pinvals} {steps} {n} {seed} {cap} {retries} {int(keep_states)}\n'
            run=subprocess.run([str(self.binary)],input=self.model_text+params,text=True,capture_output=True)
            if run.returncode:raise RandomCapError(run.stderr.strip())
            r=json.loads(run.stdout)
            batch=SampleBatch(Counter(dict(r['hist'])),r['states'],n,steps,plan['tv_bound'],r['calls'],r['words64'],'64-bit words',F(cap,1<<retries),'native exact-u128')
            self.total_random_words64+=r['words64']
        else:
            rng=RationalBits(seed,retries,cap);active=[i for i in range(self.model.m) if i not in pins]
            hist=Counter();states=[]
            for _ in range(n):
                x=pinvals
                for _ in range(steps):
                    i=active[rng.below(len(active))]
                    b=rng.bernoulli(self.model.conditional(i,x))
                    x=(x&~(1<<i))|(int(b)<<i)
                hist[x]+=1
                if keep_states:states.append(x)
            batch=SampleBatch(hist,states,n,steps,plan['tv_bound'],rng.calls,rng.bits,'bits',F(cap,1<<retries),'python exact-Fraction')
            self.total_python_bits+=rng.bits
        self.total_draws+=n;self.total_updates+=n*steps;self.total_random_calls+=batch.random_calls
        self.total_cap_abort_bound+=batch.random_cap_abort_bound
        self.batches.append({'n':n,'pins':dict(pins),'steps':steps,'backend':batch.backend})
        return batch

@dataclass
class BranchEstimate:
    variable:int
    selected:int
    estimate:F
    lower:F
    upper:F
    method:str
    draws:int

@dataclass
class PartitionEstimate:
    pins:dict[int,int]
    state:int
    point_weight:F
    estimate:F
    lower:F
    upper:F
    branches:list[BranchEstimate]
    draws:int

class HeavyPrefixPartitions:
    """Estimate Z_A=W(x*)/pi_A(x*) with adaptive empirical-heavy branches.

    On each estimated marginal, Hoeffding error plus the proved sampler TV
    yields a confidence interval. Deterministic local conditional envelopes
    can replace sampling when narrow. Intervals are multiplied and inverted
    exactly. At most max_stages sampled stages are allowed, making the
    confidence union bound and finite random budget explicit.
    """
    def __init__(self,sampler:PinnedHeatbath,stage_halfwidth:F=F(1,40),tau:F=F(1,10000),
                 delta:F=F(1,100),max_stages:int=320,order:Iterable[int]|None=None):
        if not 0<tau<stage_halfwidth<F(1,4):raise ValueError('need 0<tau<halfwidth<1/4')
        self.sampler=sampler;self.model=sampler.model;self.halfwidth=stage_halfwidth;self.tau=tau
        self.delta=delta;self.max_stages=max_stages;self.used_stages=0
        self.order=tuple(range(self.model.m) if order is None else order)
        if sorted(self.order)!=list(range(self.model.m)):raise ValueError('order must permute variables')
        L=ceil_log2(F(2*max_stages)/delta)
        t=stage_halfwidth-tau
        self.n_per_stage=ceil_f(F(L)/(2*t*t))
        self.cache={};self.marginal_cache={}
    @staticmethod
    def worst_case_plan(model:BinaryGibbs,queries:int,epsilon:F,delta:F)->dict:
        # Root's simple fixed global schedule, intentionally conservative.
        u=epsilon/(16*model.m);tau=u/2;M=queries*model.m
        n=ceil_f(F(2*ceil_log2(F(2*M)/delta))/(u*u))
        steps=model.mixing_plan({},tau)['steps']
        return {'queries':queries,'max_stages':M,'stage_halfwidth':u,'sampler_tau':tau,
                'draws_per_stage':n,'max_pinned_draws':M*n,'max_heatbath_updates':M*n*steps}
    def estimate(self,base_pins:dict[int,int])->PartitionEstimate:
        self.model.validate_pins(base_pins);key=tuple(sorted(base_pins.items()))
        if key in self.cache:return self.cache[key]
        pins=dict(base_pins);p_est=p_lo=p_hi=F(1);branches=[];draws=0
        for i in self.order:
            if i in pins:continue
            lo,hi=self.model.conditional_range(i,pins)
            if hi-lo<=2*self.halfwidth:
                mean=(lo+hi)/2;method='exact local envelope';n=0
            else:
                mk=(tuple(sorted(pins.items())),i)
                if mk not in self.marginal_cache:
                    if self.used_stages>=self.max_stages:raise RuntimeError('statistical stage cap exceeded')
                    self.used_stages+=1
                    b=self.sampler.sample(pins,self.n_per_stage,self.tau,
                        delta_bits=F(1,10**12*self.max_stages))
                    rawobs=F(sum(n for x,n in b.hist.items() if (x>>i)&1),b.n)
                    # Projection onto an exact admissible interval cannot
                    # increase error from the true marginal.
                    obs=min(hi,max(lo,rawobs))
                    obslo=max(lo,obs-self.halfwidth);obshi=min(hi,obs+self.halfwidth)
                    # The projected mean lies inside the exact envelope;
                    # retain a defensive consistency check on the intersection.
                    if obslo>obshi:raise RuntimeError('observed confidence interval conflicts with exact envelope')
                    self.marginal_cache[mk]=(obs,obslo,obshi)
                    n=b.n;draws+=n
                else:n=0
                mean,lo,hi=self.marginal_cache[mk];method='sampled empirical heavy'
            choice=int(mean>=F(1,2))
            phat=mean if choice else 1-mean
            plo,phi=(lo,hi) if choice else (1-hi,1-lo)
            if plo<=0:raise RuntimeError('heavy branch has nonpositive certified lower mass')
            branches.append(BranchEstimate(i,choice,phat,plo,phi,method,n))
            pins[i]=choice;p_est*=phat;p_lo*=plo;p_hi*=phi
        state=sum(v<<i for i,v in pins.items());w=self.model.weight(state)
        result=PartitionEstimate(dict(base_pins),state,w,w/p_est,w/p_hi,w/p_lo,branches,draws)
        self.cache[key]=result
        return result

class Network:
    def __init__(self,n:int,edges:Iterable[tuple[int,int]]):
        self.n=n;self.edges=tuple(edges)
        if n<2 or any(u<0 or v<0 or u>=n or v>=n or u==v for u,v in self.edges):raise ValueError('bad network')
        if self.components(0)!=1:raise ValueError('network must start connected')
    def components(self,x:int)->int:
        parent=list(range(self.n))
        def root(i):
            while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
            return i
        for e,(u,v) in enumerate(self.edges):
            if not (x>>e)&1:
                a,b=root(u),root(v)
                if a!=b:parent[b]=a
        return len({root(i) for i in range(self.n)})
    def disconnected(self,x:int)->bool:return self.components(x)>1
    def all_cuts(self,max_vertices:int=20)->tuple[int,...]:
        """Explicit exponential enumeration, used only when n is small.

        Generic near-minimum-cut enumeration belongs to root's global theorem;
        this routine is not mislabelled polynomial in an arbitrary graph.
        """
        if self.n>max_vertices:raise ValueError('all-cut enumerator exceeds explicit size cap')
        cuts=[]
        # Vertex 0 is excluded, identifying each cut with one of its sides.
        for subset in range(1,1<<(self.n-1)):
            side=subset<<1
            cut=sum(1<<e for e,(u,v) in enumerate(self.edges) if ((side>>u)&1)!=((side>>v)&1))
            cuts.append(cut)
        return tuple(sorted(set(cuts)))

def pins_of_mask(mask:int,m:int)->dict[int,int]:return {i:1 for i in range(m) if (mask>>i)&1}

class IntegerCategorical:
    def __init__(self,weights:Iterable[F]):
        w=tuple(weights)
        if not w or any(x<=0 for x in w):raise ValueError('positive weights required')
        den=lcm(*(x.denominator for x in w))
        a=[x.numerator*(den//x.denominator) for x in w]
        g=reduce(gcd,a);self.weights=tuple(x//g for x in a)
        self.total=sum(self.weights);self.cumulative=[];t=0
        for x in self.weights:t+=x;self.cumulative.append(t)
    def draw(self,rng:RationalBits)->int:
        from bisect import bisect_right
        return bisect_right(self.cumulative,rng.below(self.total))

@dataclass
class UnionEstimate:
    estimate:F
    lower:F
    upper:F
    inverse_mean:F
    inverse_lower:F
    inverse_upper:F
    proposals:int
    multiplicities:dict[int,int]
    conditional_weight_tv_bound:F

class CutUnionAcquisition:
    def __init__(self,model:BinaryGibbs,network:Network,cuts:Iterable[int],
                 partitions:HeavyPrefixPartitions,seed:int=11,operation_cap:int=10**8):
        self.model=model;self.network=network;self.cuts=tuple(dict.fromkeys(cuts))
        if len(network.edges)!=model.m or not self.cuts:raise ValueError('network/cut mismatch')
        if any(c<=0 or c>=(1<<model.m) for c in self.cuts):raise ValueError('invalid cut mask')
        self.partitions=partitions;self.sampler=partitions.sampler
        self.rng=RationalBits(seed,100,operation_cap)
        self.z0=partitions.estimate({})
        self.zcuts=[partitions.estimate(pins_of_mask(c,model.m)) for c in self.cuts]
        self.S=sum((z.estimate for z in self.zcuts),F(0))
        self.cat=IntegerCategorical(z.estimate for z in self.zcuts)
        self.slo=min(z.estimate/z.upper for z in self.zcuts)
        self.shi=max(z.estimate/z.lower for z in self.zcuts)
    def multiplicity(self,x:int)->int:return sum((x&c)==c for c in self.cuts)
    def proposal_batch(self,n:int,tau:F)->list[int]:
        # Independent cut choices, then independent fresh restarted chains.
        choices=[self.cat.draw(self.rng) for _ in range(n)]
        requests=Counter(choices);pools={}
        for j,count in requests.items():
            batch=self.sampler.sample(pins_of_mask(self.cuts[j],self.model.m),count,tau,
                delta_bits=F(1,10**15),keep_states=True)
            pools[j]=iter(batch.states)
        return [next(pools[j]) for j in choices]
    def estimate_probability(self,n:int=8192,tau:F=F(1,10**7),
                             delta:F=F(1,100),halfwidth:F|None=None)->UnionEstimate:
        if halfwidth is None:halfwidth=F(1,32)
        L=ceil_log2(2/delta)
        # This CI is valid only if n meets the displayed Hoeffding schedule.
        if n<ceil_f(F(L)/(2*halfwidth**2)):raise ValueError('insufficient samples for requested inverse-mean confidence interval')
        states=self.proposal_batch(n,tau)
        mult=Counter(self.multiplicity(x) for x in states)
        if 0 in mult:raise RuntimeError('pinned proposal outside supplied cut union')
        mean=sum((F(k,c) for c,k in mult.items()),F(0))/n
        J=len(self.cuts)
        alo=max(F(1,J),mean-halfwidth-tau)
        ahi=min(F(1),mean+halfwidth+tau)
        estimate=self.S*mean/self.z0.estimate
        lower=self.S*alo/(self.shi*self.z0.upper)
        upper=self.S*ahi/(self.slo*self.z0.lower)
        tv=min(F(1),(self.shi-self.slo)/(2*self.slo))
        return UnionEstimate(estimate,lower,upper,mean,alo,ahi,n,dict(mult),tv)
    def conditional_samples(self,n:int,tau:F=F(1,10**8),
                            abort_delta:F=F(1,10**6))->tuple[list[int],dict]:
        J=len(self.cuts);per_output_cap=J*ceil_log2(F(n)/abort_delta)
        total_cap=n*per_output_cap
        accepted=[];consecutive=0;generated=0;used=0
        while len(accepted)<n:
            batchsize=min(max(32,2*(n-len(accepted))),total_cap-generated)
            if batchsize<=0:raise RandomCapError('conditional rejection total cap exceeded')
            batch=self.proposal_batch(batchsize,tau);generated+=batchsize
            for x in batch:
                used+=1;c=self.multiplicity(x)
                if c<1:raise RuntimeError('proposal outside cut union')
                if self.rng.below(c)==0:
                    accepted.append(x);consecutive=0
                    if len(accepted)==n:break
                else:
                    consecutive+=1
                    if consecutive>=per_output_cap:raise RandomCapError('conditional rejection per-output cap exceeded')
        weight_tv=min(F(1),(self.shi-self.slo)/(2*self.slo))
        return accepted,{'generated_proposals':generated,'used_proposals':used,
          'per_output_proposal_cap':per_output_cap,'worst_case_total_proposal_cap':total_cap,
          'rejection_abort_bound':abort_delta,'per_output_weight_tv_bound':weight_tv,
          'per_output_mixing_tv_bound':2*J*tau,
          'joint_output_tv_bound_via_union':min(F(1),n*(weight_tv+2*J*tau))}

def fixture()->tuple[BinaryGibbs,Network]:
    edges=((0,1),(1,2),(1,3),(3,4),(4,5),(0,2),(2,3),(2,4),(3,5),(0,5))
    fields=[F(1,2**90),F(3,2**96),F(5,2**89),F(7,5*2**92),F(2,3*2**89),
            F(1,5),F(2,7),F(1,4),F(3,8),F(1,6)]
    factors=[Factor((i,),(F(1),h)) for i,h in enumerate(fields)]
    interactions=((0,5,F(5,3)),(1,6,F(3,2)),(2,7,F(7,4)),(3,8,F(4,3)),(4,9,F(8,5)),
                  (5,6,F(2)),(6,8,F(3,2)),(7,9,F(7,4)),(8,9,F(4,3)),(0,1,F(2**40)))
    factors.extend(Factor((i,j),(F(1),F(1),F(1),c)) for i,j,c in interactions)
    return BinaryGibbs(10,factors),Network(6,edges)

if __name__=='__main__':
    model,net=fixture()
    print(json.dumps({'m':model.m,'n':net.n,'chi':float(model.chi),
      'logarithmic_contrast_c3_verified':model.logarithmic_contrast(3),
      'odds_contrast':float(model.odds_contrast()),'cuts':len(net.all_cuts())},indent=2))
