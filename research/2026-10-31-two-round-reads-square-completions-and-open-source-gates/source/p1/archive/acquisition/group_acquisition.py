"""Scalar-query acquisition for adaptive-risk-competitive quadratic prediction.

The learner sees only chosen Boolean evaluations, not the coefficient table.
The source in the paid diagnostic has small integer coefficients; all source
values, block sums, medians, contrasts, and the final predictor are exact.
Vectorization batches independent scalar calls; every row is charged.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
import heapq
import json
import math
from pathlib import Path
import time
import numpy as np


class IntegerQuadraticSource:
    def __init__(self, n, constant, linear, edges):
        self.n, self.constant = n, int(constant)
        self.linear, self.edges = dict(linear), dict(edges)
        self.scalar_calls = 0
        self.input_signs_received = 0
        self.source_term_evaluations = 0

    def __call__(self, xs):
        xs = np.asarray(xs, dtype=np.int8)
        if xs.ndim == 1:
            xs = xs[None, :]
        assert xs.shape[1] == self.n
        assert np.all((xs == 1) | (xs == -1))
        self.scalar_calls += len(xs)
        self.input_signs_received += xs.size
        self.source_term_evaluations += len(xs)*(1+len(self.linear)+len(self.edges))
        out = np.full(len(xs), self.constant, dtype=np.int64)
        for i,a in self.linear.items():
            out += a*xs[:,i].astype(np.int64)
        for (i,j),a in self.edges.items():
            out += a*(xs[:,i]*xs[:,j]).astype(np.int64)
        # Diagnostic integer bounds keep every subsequent block sum in int64.
        assert np.max(np.abs(out), initial=0) < 1000000
        return out


class GroupReader:
    def __init__(self, observe, n, alpha, seed):
        self.observe, self.n = observe, n
        self.block = 288  # 32/(1/3)^2; Var(nonnegative energy)<=8 mean^2.
        self.blocks = math.ceil(8*math.log(6*n/alpha))
        if self.blocks % 2 == 0:
            self.blocks += 1
        self.rng = np.random.default_rng(seed)
        self.random_sign_bits = 0
        self.records = []

    def read(self, indices, kind):
        indices = list(indices)
        m = self.block*self.blocks
        x = (2*self.rng.integers(0,2,size=(m,self.n),dtype=np.int8)-1)
        y = x.copy()
        if indices:
            y[:,indices] = (2*self.rng.integers(0,2,size=(m,len(indices)),dtype=np.int8)-1)
        xf, yf = x.copy(), y.copy()
        xf[:,indices] *= -1
        yf[:,indices] *= -1
        f0,f1,f2,f3 = (self.observe(z) for z in (x,xf,y,yf))
        assert np.all((f0-f1)%2 == 0)
        assert np.all((f0+f1-f2-f3)%2 == 0)
        u = (f0-f1)//2
        v = (f0+f1-f2-f3)//2
        if kind == "mass":
            numerators, denominator = u*u+v*v, self.block
        else:
            assert kind == "coverage"
            numerators, denominator = 2*u*u+v*v, 2*self.block
        means = [F(int(z), denominator)
                 for z in numerators.reshape(self.blocks,self.block).sum(axis=1)]
        estimate = sorted(means)[self.blocks//2]
        self.random_sign_bits += m*(self.n+len(indices))
        self.records.append({"indices":indices,"kind":kind,"estimate":str(estimate),
                             "contexts":m,"scalar_calls":4*m})
        return estimate


def selected_nonconstant(observe,n,selected):
    pos = np.ones(n,dtype=np.int8)
    inputs = [pos, -pos]
    for i in selected:
        x = pos.copy(); x[i] = -1
        inputs.extend([x,-x])
    pairs = list(combinations(selected,2))
    for i,j in pairs:
        x = pos.copy(); x[i] = x[j] = -1
        inputs.append(x)
    fs = [int(v) for v in observe(np.stack(inputs))]
    fp,fm = fs[:2]
    linear,edges,singles = {},{},{}
    p=2
    for i in selected:
        singles[i] = fs[p]
        linear[i] = F(fp-fm-fs[p]+fs[p+1],4)
        p+=2
    for i,j in pairs:
        edges[i,j] = F(fp-singles[i]-singles[j]+fs[p],4)
        p+=1
    assert p == len(fs)
    return linear,edges,len(fs)


def acquire(observe,n,k,epsilon,alpha=0.1,seed=20261101):
    """The stated exact-source algorithm, including all confidence constants."""
    k,epsilon = F(k),F(epsilon)
    assert k>0 and 0<epsilon<=1
    cap=min(n,math.ceil(288*k/(epsilon*epsilon)))
    height=(n-1).bit_length()
    expansion_cap=min(n-1,math.floor(height*(cap+768*k/(epsilon*epsilon))))
    reader=GroupReader(observe,n,alpha,seed)
    selected=[]
    heap=[]
    root=reader.read(range(n),"mass")
    heapq.heappush(heap,(-F(3,2)*root,0,n))
    residual=reader.read(range(n),"coverage")
    lower=F(3,4)*residual
    expansions=0
    reason=""
    while heap:
        upper=-heap[0][0]
        if upper<=epsilon*epsilon*lower/(96*k):
            reason="residual_certificate"
            break
        upper_negative,left,right=heapq.heappop(heap)
        if right-left==1:
            selected.append(left)
            if len(selected)>=cap:
                reason="ranked_prefix_cap"
                break
            outside=[i for i in range(n) if i not in selected]
            residual=reader.read(outside,"coverage")
            lower=F(3,4)*residual
        else:
            # This guard cannot fire on the simultaneous calibration event.
            # It makes the advertised source-call budget unconditional.
            if expansions>=expansion_cap:
                reason="confidence_budget_abort"
                break
            expansions+=1
            middle=(left+right)//2
            for a,b in [(left,middle),(middle,right)]:
                value=reader.read(range(a,b),"mass")
                heapq.heappush(heap,(-F(3,2)*value,a,b))
    if not reason:
        reason="all_coordinates_observed"
    linear,edges,coefficient_calls=selected_nonconstant(observe,n,selected)
    # The diagnostic source is integer, hence its recovered coefficients are.
    assert all(v.denominator==1 for v in list(linear.values())+list(edges.values()))
    mean_block=math.ceil(4*(2+epsilon)/epsilon)
    mean_blocks=math.ceil(8*math.log(2/alpha))
    if mean_blocks%2==0:
        mean_blocks+=1
    count=mean_block*mean_blocks
    x=2*reader.rng.integers(0,2,size=(count,n),dtype=np.int8)-1
    values=observe(x).copy()
    for i,a in linear.items():
        values-=int(a)*x[:,i]
    for (i,j),a in edges.items():
        values-=int(a)*(x[:,i]*x[:,j])
    means=[F(int(z),mean_block) for z in values.reshape(mean_blocks,mean_block).sum(axis=1)]
    constant=sorted(means)[mean_blocks//2]
    reader.random_sign_bits+=count*n
    return {"selected":selected,"constant":constant,"linear":linear,"edges":edges,
            "records":reader.records,"cap":cap,"expansions":expansions,
            "expansion_cap":expansion_cap,"reason":reason,
            "group_blocks":reader.blocks,"group_block_size":reader.block,
            "coefficient_calls":coefficient_calls,"mean_calls":count,
            "mean_block_size":mean_block,"mean_blocks":mean_blocks,
            "random_sign_bits":reader.random_sign_bits}


def exact_group_identities():
    rng=np.random.default_rng(814)
    cases=0
    worst_mass=F(0); worst_coverage=F(0)
    for repetition in range(8):
        n=4
        aa={i:int(rng.integers(-3,4)) for i in range(n)}
        bb={(i,j):int(rng.integers(-3,4)) for i,j in combinations(range(n),2)}
        src=IntegerQuadraticSource(n,2,aa,bb)
        inf=[aa[i]**2+sum(v*v for ij,v in bb.items() if i in ij) for i in range(n)]
        for mask in range(1<<n):
            A=[i for i in range(n) if (mask>>i)&1]
            xs=[];xfs=[];ys=[];yfs=[]
            for xx in product([-1,1],repeat=n):
                for yy in product([-1,1],repeat=len(A)):
                    x=np.array(xx,dtype=np.int8); y=x.copy(); y[A]=yy
                    xf=x.copy(); xf[A]*=-1
                    yf=y.copy(); yf[A]*=-1
                    xs.append(x);xfs.append(xf);ys.append(y);yfs.append(yf)
            f0,f1,f2,f3=(src(np.stack(z)) for z in (xs,xfs,ys,yfs))
            u=(f0-f1)//2; v=(f0+f1-f2-f3)//2
            j=u*u+v*v; c2=2*u*u+v*v; m=len(j)
            J=sum(inf[i] for i in A)
            C=sum(v*v for i,v in aa.items() if i in A)+sum(v*v for ij,v in bb.items() if any(i in A for i in ij))
            assert F(int(j.sum()),m)==J
            assert F(int(c2.sum()),2*m)==C
            ej2=F(int((j*j).sum()),m)
            ec2=F(int((c2*c2).sum()),4*m)
            assert ej2<=9*J*J
            assert ec2<=9*C*C
            if J: worst_mass=max(worst_mass,ej2/(J*J))
            if C: worst_coverage=max(worst_coverage,ec2/(C*C))
            cases+=1
    return {"group_models":cases,"all_mass_and_coverage_identities_exact":True,
            "all_relative_second_moment_bounds_pass":True,
            "max_mass_ratio":float(worst_mass),"max_coverage_ratio":float(worst_coverage)}


def noisy_group_check():
    # Exact eight-sign readout-noise enumeration at one nontrivial group.
    n=3; A=[0,1]; sigma=F(1,2)
    src=IntegerQuadraticSource(n,2,{0:1,1:-2},{(0,1):2,(1,2):-1})
    true=[]; noisy=[]
    for x in product([-1,1],repeat=n):
        for yy in product([-1,1],repeat=len(A)):
            z=np.array(x,dtype=np.int8); y=z.copy(); y[A]=yy
            zf=z.copy(); zf[A]*=-1
            yf=y.copy(); yf[A]*=-1
            vals=[F(int(v)) for v in src(np.stack([z,zf,y,yf]))]
            u=(vals[0]-vals[1])/2
            v=(vals[0]+vals[1]-vals[2]-vals[3])/2
            true.append(u*u+v*v)
            for eps in product([-1,1],repeat=8):
                first=[vals[i]+sigma*eps[i] for i in range(4)]
                second=[vals[i]+sigma*eps[i+4] for i in range(4)]
                uu=(first[0]-first[1])/2; vv=sum(first[:2])/2-sum(first[2:])/2
                ww=(second[0]-second[1])/2; zz=sum(second[:2])/2-sum(second[2:])/2
                noisy.append(uu*ww+vv*zz)
    J=sum(true)/len(true)
    mean=sum(noisy)/len(noisy)
    variance=sum((w-J)**2 for w in noisy)/len(noisy)
    bound=8*J*J+2*sigma*sigma*J+F(5,4)*sigma**4
    assert mean==J and variance<=bound
    return {"enumerated_noisy_records":len(noisy),"mean_exact":str(mean),
            "variance_exact":str(variance),"variance_bound":str(bound),"pass":True}


def optimal_expected_risk_small(src,budget):
    active=sorted(set(src.linear)|{i for ij in src.edges for i in ij})
    assert len(active)<=4
    def risk(state):
        fixed={i:s for i,s in zip(active,state) if s}
        free=[i for i in active if i not in fixed]
        return sum(F(src.linear.get(i,0)+sum(v*fixed[j] for ij,v in src.edges.items()
                     for j in ij if i in ij and j!=i and j in fixed))**2 for i in free)+sum(
                     F(v*v) for (i,j),v in src.edges.items() if i in free and j in free)
    @lru_cache(None)
    def frontier(state):
        candidates={(F(0),risk(state))}
        for ix,s in enumerate(state):
            if s:continue
            sm=list(state);sm[ix]=-1
            sp=list(state);sp[ix]=1
            for cm,rm in frontier(tuple(sm)):
                for cp,rp in frontier(tuple(sp)):
                    candidates.add((1+(cm+cp)/2,(rm+rp)/2))
        return tuple((c,r) for c,r in candidates if not any(
            cc<=c and rr<=r and (cc<c or rr<r) for cc,rr in candidates))
    points=frontier((0,)*len(active))
    result=min(r for c,r in points if c<=budget)
    for c,r in points:
        for cc,rr in points:
            if c<=budget<=cc and c<cc:
                result=min(result, r+(rr-r)*(budget-c)/(cc-c))
    return result,len(points)


def paid_pipeline():
    src=IntegerQuadraticSource(16,3,{7:2,12:-1},{(7,13):3})
    k=F(1,100); eps=F(1)
    t=time.perf_counter()
    result=acquire(src,16,k,eps,alpha=.1)
    elapsed=time.perf_counter()-t
    # Source-aware verification is outside the learner.
    I=[F(src.linear.get(i,0)**2+sum(v*v for ij,v in src.edges.items() if i in ij)) for i in range(16)]
    all_events=True
    for row in result["records"]:
        A=set(row["indices"])
        truth=(sum(I[i] for i in A) if row["kind"]=="mass" else
               sum(F(v*v) for i,v in src.linear.items() if i in A)+
               sum(F(v*v) for ij,v in src.edges.items() if any(i in A for i in ij)))
        estimate=F(row["estimate"])
        all_events &= F(2,3)*truth<=estimate<=F(4,3)*truth
    assert all_events
    selected=set(result["selected"])
    risk=sum(F(v*v) for i,v in src.linear.items() if i not in selected)+sum(
        F(v*v) for ij,v in src.edges.items() if not set(ij)<=selected)
    assert all(result["linear"][i]==src.linear.get(i,0) for i in selected)
    assert all(v==src.edges.get(tuple(sorted(ij)),0) for ij,v in result["edges"].items())
    actual_risk=risk+(result["constant"]-src.constant)**2
    optimum,frontier_count=optimal_expected_risk_small(src,k)
    assert actual_risk<=(1+eps)*optimum
    group_calls=sum(r["scalar_calls"] for r in result["records"])
    assert src.scalar_calls==group_calls+result["coefficient_calls"]+result["mean_calls"]
    return {"n":16,"expected_adaptive_budget":str(k),"epsilon":str(eps),
            "confidence_parameter":.1,"selected":result["selected"],"cap":result["cap"],
            "stop_reason":result["reason"],"group_or_coverage_estimates":len(result["records"]),
            "tree_expansions":result["expansions"],"blocks":result["group_blocks"],
            "unconditional_expansion_cap":result["expansion_cap"],
            "contexts_per_block":result["group_block_size"],
            "group_scalar_calls":group_calls,"selected_coefficient_calls":result["coefficient_calls"],
            "intercept_calls":result["mean_calls"],"total_scalar_calls":src.scalar_calls,
            "dense_input_signs_received":src.input_signs_received,
            "independent_random_sign_bits":result["random_sign_bits"],
            "source_term_evaluations":src.source_term_evaluations,
            "all_realized_calibration_events_hold":all_events,"actual_risk":str(actual_risk),
            "optimal_expected_budget_risk":str(optimum),"small_policy_frontier_size":frontier_count,
            "wall_seconds":elapsed,"full_interpolation_calls":1+16+16*15//2,
            "interpretation":"Complete paid exact-value diagnostic, not a practical speedup. The expected comparison budget is deliberately fractional."}


if __name__=="__main__":
    start=time.perf_counter()
    result={"exact_group_checks":exact_group_identities(),
            "noisy_group_check":noisy_group_check(),"paid_pipeline":paid_pipeline()}
    result["total_wall_seconds"]=time.perf_counter()-start
    output=Path(__file__).with_name("results.json")
    output.write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
