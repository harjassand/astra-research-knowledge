"""Acquired Gaussian-mean channel: explicit general theorem, float execution.

The ideal-real guarantee and full accounting are in
ACQUIRED_CAPPED_GAUSSIAN_CHANNEL.md. This module's binary floating outputs
are diagnostics; no TV claim against an unrounded continuous law is made.
Only `source(point)` provides source information. The algorithm does not
evaluate means, derivatives, Hessians, potentials, or conditional laws.
"""
from dataclasses import dataclass, asdict
from fractions import Fraction
from math import sqrt, ceil, log, log2, exp, pi, erf
from random import Random
from pathlib import Path
import csv
import json

ROOT=Path(__file__).resolve().parent

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def norm(a): return sqrt(dot(a,a))
def add(a,b): return [x+y for x,y in zip(a,b)]
def sub(a,b): return [x-y for x,y in zip(a,b)]
def scale(a,c): return [c*x for x in a]

class GaussianSeeds:
    def __init__(self,seed):
        self.rng=Random(seed)
        self.scalar_gaussians=0
    def gaussian(self):
        self.scalar_gaussians+=1
        return self.rng.gauss(0,1)
    def vector(self,d): return [self.gaussian() for _ in range(d)]
    def uniform(self):
        a,b,c=self.gaussian(),self.gaussian(),self.gaussian()
        radius=sqrt(a*a+b*b+c*c)
        return .5 if radius==0 else min(1.,max(0.,.5*(1+a/radius)))

@dataclass(frozen=True)
class Parameters:
    dimension:int
    lipschitz:float
    sigma:float
    epsilon:float
    p:int
    M:int
    alpha:float
    K:int
    B:float
    A:int
    J:int
    s:float
    r:float
    poisson_degree:int
    query_cap:int

def parameters(d,L,sigma,epsilon):
    assert d>=1 and L>0 and sigma>0 and 0<epsilon<=.25
    rho=L/sigma
    p=2*ceil(log(128/epsilon)/log(16))
    Rp=sqrt(d*p)+p
    M=ceil(256*(1+rho*rho)*Rp)
    alpha=2*rho*rho/M
    K=max(1,ceil(log(64*d/epsilon)/log(1/alpha)))
    A=ceil(log2(64/epsilon))
    J=ceil(log2(64*A/epsilon))
    s=epsilon/(32*max(1,rho)*sqrt(d))
    r=s*epsilon/(192*max(1,alpha*d))
    degree=ceil(log2(128*A/epsilon))
    if degree%2==0: degree+=1
    qcap=1+A*(M+8*J*K)
    return Parameters(d,L,sigma,epsilon,p,M,alpha,K,.25,A,J,s,r,degree,qcap)

def poisson_table(par):
    # Odd alternating Taylor polynomial is a certified rational lower bound.
    total=Fraction(1)
    term=Fraction(1)
    for k in range(1,par.poisson_degree+1):
        term *= Fraction(-1,2*k)
        total += term
    assert 0<total<1
    p0=total
    mass=p0
    cumulative=Fraction(0)
    table=[]
    for j in range(par.J+1):
        if j: mass *= Fraction(1,2*j)
        cumulative += mass
        table.append(cumulative)
    assert cumulative<=1
    return table

def draw_capped_poisson(table,seeds):
    # Fraction conversion preserves the sampled floating uniform exactly;
    # an ideal implementation compares its exact real uniform directly.
    u=Fraction.from_float(seeds.uniform())
    for j,cumulative in enumerate(table):
        if u<cumulative: return j
    return None

def uniform_index(seeds,size):
    # Binary interval comparisons, so no floor-of-an-oracle-real primitive.
    u=seeds.uniform()
    low=0;high=size
    while high-low>1:
        middle=(low+high)//2
        if u*size<middle: high=middle
        else: low=middle
    return low

class CountedSource:
    def __init__(self,fn,d):
        self.fn=fn;self.d=d;self.calls=0
    def __call__(self,x):
        assert len(x)==self.d
        self.calls+=1
        out=list(self.fn(x))
        assert len(out)==self.d
        return out

class BrownianBridges:
    def __init__(self,endpoints,seeds):
        self.seeds=seeds
        self.d=len(endpoints[0])
        self.paths=[[(0.,[0.]*self.d),(1.,g)] for g in endpoints]
        self.added_points=0
    def at(self,i,t):
        path=self.paths[i]
        for j,(right_t,right_x) in enumerate(path):
            if t==right_t: return right_x
            if t<right_t:
                left_t,left_x=path[j-1]
                gap=right_t-left_t
                wt=(t-left_t)/gap
                sd=sqrt(max(0.,(t-left_t)*(right_t-t)/gap))
                z=self.seeds.vector(self.d)
                x=[(1-wt)*a+wt*b+sd*c for a,b,c in zip(left_x,right_x,z)]
                path.insert(j,(t,x))
                self.added_points+=1
                return x
        return path[-1][1]  # Gaussian-uniform null endpoint convention.

def homogeneous_secant(source,center,smoothing,v,xi,r):
    nv=norm(v)
    base=add(center,scale(xi,smoothing))
    if nv==0:
        source(base);source(base)
        return [0.]*len(v)
    shift=scale(v,r/nv)
    gp=source(add(base,shift))
    gm=source(sub(base,shift))
    return scale(sub(gp,gm),nv/(2*r))

class CovarianceMap:
    """One realized odd Lipschitz map, reusable at different directions."""
    def __init__(self,source,bridges,seeds,par):
        self.source=source;self.par=par
        i=uniform_index(seeds,par.M)
        t=seeds.uniform()
        self.center=bridges.at(i,t)
        self.smoothing=sqrt(1-t+par.s*par.s)
        self.xi1=seeds.vector(par.dimension)
        self.xi2=seeds.vector(par.dimension)
    def __call__(self,v):
        a=homogeneous_secant(self.source,self.center,self.smoothing,v,self.xi1,self.par.r)
        b=homogeneous_secant(self.source,self.center,self.smoothing,a,self.xi2,self.par.r)
        return scale(b,1/(self.par.M*self.par.sigma*self.par.sigma))

def likelihood_estimator(source,bridges,Z,seeds,par):
    zp=seeds.vector(par.dimension)
    v=list(Z);vp=list(zp)
    ans=0.
    for k in range(1,par.K+1):
        action=CovarianceMap(source,bridges,seeds,par)
        v=action(v)
        vp=action(vp)  # Same map and same bridge anchor, not a new draw.
        ans += .5*(dot(zp,vp)/k-dot(Z,v))
    return ans

def sample_gaussian_mean(source,d,L,sigma,epsilon,seed):
    """Return one output and complete accounting; `source` is value-only."""
    counted=CountedSource(source,d)
    seeds=GaussianSeeds(seed)
    offset=counted([0.]*d)
    if L==0 or (L/sigma)*sqrt(d)<=epsilon/8:
        y=add(offset,scale(seeds.vector(d),sigma))
        return y,{'source_queries':1,'query_cap':1,'easy_small_lipschitz':True,
                  'scalar_gaussians':seeds.scalar_gaussians,'terminated_by_cap':False}
    par=parameters(d,L,sigma,epsilon)
    table=poisson_table(par)
    attempts=0;factors=0;bridgepoints=0;max_abs_W=0.;caps=False
    y=list(offset)
    for attempt in range(par.A):
        attempts+=1
        endpoints=[seeds.vector(d) for _ in range(par.M)]
        bridges=BrownianBridges(endpoints,seeds)
        # Pay the full M proposal values even if this proposal is rejected.
        sums=[0.]*d
        for gpoint in endpoints:
            value=counted(gpoint)
            for j in range(d): sums[j]+=value[j]-offset[j]
        Z=seeds.vector(d)
        n=draw_capped_poisson(table,seeds)
        if n is None:
            caps=True
            break
        probability=1.
        for _ in range(n):
            before=counted.calls
            W=likelihood_estimator(counted,bridges,Z,seeds,par)
            assert counted.calls-before==8*par.K
            factors+=1
            max_abs_W=max(max_abs_W,abs(W))
            wc=max(-par.B,min(par.B,W))
            probability*=(par.B+wc)/(2*par.B)
        bridgepoints+=bridges.added_points
        if seeds.uniform()<probability:
            y=[offset[j]+sums[j]/par.M+sigma*Z[j] for j in range(d)]
            break
    else:
        caps=True
    assert counted.calls<=par.query_cap
    assert factors<=par.A*par.J
    details=asdict(par)
    details.update(source_queries=counted.calls,attempts=attempts,
                   likelihood_factors=factors,paired_covariance_steps=factors*par.K,
                   brownian_points=bridgepoints,scalar_gaussians=seeds.scalar_gaussians,
                   max_abs_likelihood_estimator=max_abs_W,terminated_by_cap=caps)
    return y,details

def orthogonal_matrix(d,rng):
    rows=[]
    for _ in range(d):
        v=[rng.gauss(0,1) for _ in range(d)]
        for q in rows: v=sub(v,scale(q,dot(q,v)))
        v=scale(v,1/norm(v));rows.append(v)
    return rows

def matvec(Q,v): return [dot(q,v) for q in Q]
def transpose_matvec(Q,v):
    return [sum(Q[i][j]*v[i] for i in range(len(v))) for j in range(len(v))]

def test_source(d,seed):
    """Noncommuting rotated clipping gradients; global Lipschitz bound one."""
    rng=Random(seed)
    Q=orthogonal_matrix(d,rng);R=orthogonal_matrix(d,rng)
    b=[rng.gauss(0,.8) for _ in range(d)]
    c=[rng.gauss(0,.8) for _ in range(d)]
    offset=[10+i/3 for i in range(d)]
    def source(x):
        qx=matvec(Q,x);rx=matvec(R,x)
        q=transpose_matvec(Q,[max(-1,min(1,u+v)) for u,v in zip(qx,b)])
        r=transpose_matvec(R,[max(-1,min(1,u+v)) for u,v in zip(rx,c)])
        return [a+.5*(u+v) for a,u,v in zip(offset,q,r)]
    return source

def proof_parameter_checks():
    count=0
    for d in (1,2,8,16,100,10**6):
        for rho in (.01,.1,1,10):
            for eps in (.25,.1,1e-4,1e-10):
                par=parameters(d,rho,1.,eps)
                ep=5*par.alpha*(sqrt(d*par.p)+par.p)+3*par.alpha**2*d
                trunc=4*d*par.alpha**(par.K+1)
                bias=12*(par.r/par.s)*par.alpha*d
                clipping=6*par.B*(ep/par.B)**par.p
                smooth=2*rho*par.s*sqrt(d)
                assert par.alpha<=.25 and ep<=par.B/4
                assert trunc<=eps/16*(1+1e-10)
                assert bias<=eps/16*(1+1e-10)
                assert smooth<=eps/16*(1+1e-10)
                assert trunc+bias+clipping+smooth<eps/4
                # Exact rational Poisson lower polynomial and elementary remainder.
                tab=poisson_table(par)
                rem=Fraction(1,2)**(par.poisson_degree+1)
                assert float(rem)<=eps/(128*par.A)
                assert tab[-1]<=1
                assert 2**(-par.A)<=eps/64*(1+1e-10)
                assert par.A*2**(-par.J)<=eps/64*(1+1e-10)
                count+=1
    return count

def action_contract_checks():
    rng=Random(20261027)
    d=8;fn=test_source(d,9181);source=CountedSource(fn,d)
    max_lip=0.;max_norm=0.
    for _ in range(200):
        c=[rng.gauss(0,1) for _ in range(d)]
        xi=[rng.gauss(0,1) for _ in range(d)]
        v=[rng.gauss(0,1) for _ in range(d)]
        w=add(v,[rng.gauss(0,.2) for _ in range(d)])
        before=source.calls
        dv=homogeneous_secant(source,c,.7,v,xi,.03)
        dw=homogeneous_secant(source,c,.7,w,xi,.03)
        dm=homogeneous_secant(source,c,.7,scale(v,-1),xi,.03)
        assert source.calls-before==6
        assert norm(add(dv,dm))<1e-10
        lip=norm(sub(dv,dw))/norm(sub(v,w))
        ratio=norm(dv)/norm(v)
        assert lip<=sqrt(2)+1e-9 and ratio<=1+1e-9
        max_lip=max(max_lip,lip);max_norm=max(max_norm,ratio)
    before=source.calls
    z=homogeneous_secant(source,[0.]*d,.7,[0.]*d,[0.]*d,.03)
    assert z==[0.]*d and source.calls-before==2
    return source.calls,max_lip,max_norm

def null_event_checks():
    class ZeroSeeds(GaussianSeeds):
        def gaussian(self):
            self.scalar_gaussians+=1
            return 0.
    seeds=ZeroSeeds(0)
    assert seeds.uniform()==.5
    class FixedUniform:
        def __init__(self,u): self.u=u
        def uniform(self): return self.u
    for size in (1,2,7,100):
        assert uniform_index(FixedUniform(0.),size)==0
        assert uniform_index(FixedUniform(1.),size)==size-1
    par=parameters(4,1.,2.,.2)
    source=CountedSource(test_source(4,9191),4)
    paths=BrownianBridges([[0.]*4 for _ in range(par.M)],seeds)
    assert paths.at(0,0.)==[0.]*4 and paths.at(0,1.)==[0.]*4
    point=paths.at(0,.5)
    count=paths.added_points
    assert paths.at(0,.5)==point and paths.added_points==count
    action=CovarianceMap(source,paths,seeds,par)
    a=action([0.]*4);b=action([0.]*4)
    assert a==[0.]*4 and b==[0.]*4 and source.calls==8
    # Same realized map also retains both stored smoothing seeds on nonzero inputs.
    xi1=list(action.xi1);xi2=list(action.xi2)
    action([1.,0.,0.,0.]);action([-1.,0.,0.,0.])
    assert action.xi1==xi1 and action.xi2==xi2 and source.calls==16
    return source.calls

def main():
    nchecks=proof_parameter_checks()
    action_queries,max_lip,max_norm=action_contract_checks()
    null_queries=null_event_checks()
    rows=[];outputs=[];total=action_queries+null_queries
    for d,eps,count in [(4,.2,4),(16,.1,4)]:
        source=test_source(d,7400+d)
        for j in range(count):
            y,details=sample_gaussian_mean(source,d,1.,2.,eps,2026102700+100*d+j)
            total+=details['source_queries']
            details['output_number']=j
            rows.append(details)
            outputs.append({'dimension':d,'epsilon':eps,'output_number':j,'output':y})
    with (ROOT/'capped_channel_execution.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    # Ordinary numeric data; no serialization is required by the research method.
    with (ROOT/'capped_channel_outputs.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['dimension','epsilon','output_number','coordinate','value'])
        for item in outputs:
            for k,v in enumerate(item['output']):
                writer.writerow([item['dimension'],item['epsilon'],item['output_number'],k,v])
    out=[
        'ACQUIRED CAPPED GAUSSIAN-MEAN CHANNEL EXECUTION',
        f'Explicit proof-parameter inequalities checked in {nchecks} parameter cases.',
        f'Action-contract checks: 200 multidimensional reused-seed pairs, {action_queries} charged values.',
        f'Largest observed homogeneous-map Lipschitz ratio {max_lip:.15g} (theorem bound sqrt(2)).',
        f'Largest observed action norm ratio {max_norm:.15g} (theorem bound 1).',
        f'Null-event controls passed: zero Gaussian triple, uniform endpoints, retained bridge endpoints/repeated times, zero-direction paired map; {null_queries} charged values.',
        'Source family: sum of two noncommuting rotated clipping gradients, with unknown offsets to the sampler.',
        'Only source(point), public dimension/Lipschitz bound, target sigma and epsilon enter the sampler.',
    ]
    for row in rows:
        out.append(f"d={row['dimension']} eps={row['epsilon']} output={row['output_number']}: values={row['source_queries']} <= cap={row['query_cap']}; attempts={row['attempts']}; factors={row['likelihood_factors']}; covariance word steps={row['paired_covariance_steps']}; bridge points={row['brownian_points']}; capped={row['terminated_by_cap']}")
    out.extend([
        f'Total charged synthetic values including contract checks: {total}.',
        'Every actual source call was counted; fitting/source-dependent precomputation cost is zero.',
        'The full-law certificate is the general analytical proof, not these finite output samples.',
        'The executable uses binary floating arithmetic; finite-bit/rounded-target TV is a separate obligation.',
    ])
    text='\n'.join(out)+'\n'
    (ROOT/'CAPPED_CHANNEL_RESULTS.txt').write_text(text)
    print(text,end='')

if __name__=='__main__':main()
