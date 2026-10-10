"""Exact stationary joint sampler for finite-depth triangular stochastic dynamics.

Independent event at each site-time: Haar uniform reset with probability s>0,
fixed residual reset with probability r, or stratified gate otherwise.

Each layer 0,...,c-1 evolves affinely in parents' *same* layer,
plus an arbitrary evaluable nonlinear forcing of strictly lower layers.

The state is finite field F_q^c (q prime in implementation).
An exact joint stationary sample of finitely many coordinates at any times
is recovered with backward rank absorption, retaining nonlinear terms as a DAG.
For fixed c, expected oracle work polynomial in output size, parent count, 1/s
and cost of evaluating forcing functions; independent of total n sites under
local random access. The theory requires ideal uniform random bits; Python's
PRNG here is for reproducible numerical testing, not cryptographic randomness.

This research code is not independently verified or historically priority-cleared.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from math import lcm
from collections import defaultdict
import random


def basis_contains(basis, vec, q):
    w=list(vec)
    for p, b in sorted(basis.items()):
        if w[p]:
            a=w[p]
            w=[(x-a*y)%q for x,y in zip(w,b)]
    return not any(w)


def add_basis(basis, vec, q):
    w=list(vec)
    for p, b in sorted(basis.items()):
        if w[p]:
            a=w[p]
            w=[(x-a*y)%q for x,y in zip(w,b)]
    for p,x in enumerate(w):
        if x:
            inv=pow(x,-1,q)
            basis[p]=tuple(v*inv%q for v in w)
            return True
    return False


def add_vec(dct, key, vec, multiplier, q):
    if multiplier%q==0: return
    if key not in dct:dct[key]=[0]*len(vec)
    w=dct[key]
    for j,v in enumerate(vec):w[j]=(w[j]+multiplier*v)%q
    if not any(w):dct.pop(key)


@dataclass
class StratifiedModel:
    n:int
    c:int
    q:int
    s:object
    r:object
    parents:object
    coeffs:object
    forcing:object
    residual:object

    def input_sites(self,i):
        return tuple(self.parents(i)) if callable(self.parents) else tuple(self.parents[i])
    def layer_coeffs(self,i,ell):
        return tuple(self.coeffs(i,ell)) if callable(self.coeffs) else tuple(self.coeffs[i][ell])
    def layer_forcing(self,i,ell,lower_vectors):
        return int(self.forcing(i,ell,lower_vectors))%self.q
    def residual_state(self,i):
        return tuple(self.residual(i)) if callable(self.residual) else tuple(self.residual)

    def validate(self):
        if not (self.n>=1 and self.c>=1 and self.q>=2):raise ValueError('Invalid dimensions')
        s,r=Fraction(str(self.s)),Fraction(str(self.r))
        if not (0<s<=1 and 0<=r and s+r<=1):raise ValueError('Invalid probabilities')
        for x in range(min(self.n,20)):
            K=len(self.input_sites(x))
            assert all(0<=j<self.n for j in self.input_sites(x))
            for ell in range(self.c):
                assert len(self.layer_coeffs(x,ell))==K
        return True


class EventOracle:
    def __init__(self,model,rng):
        self.model,self.rng=model,rng
        s,r=Fraction(str(model.s)),Fraction(str(model.r))
        self.d=lcm(s.denominator,r.denominator)
        self.S=int(s*self.d)
        self.R=int(r*self.d)
        self.events={}
        self.fresh=0
        self.parent_lookups=0
        self.force_evaluations=0

    def event(self,z):
        if z in self.events:return self.events[z],False
        self.fresh+=1
        a=self.rng.randrange(self.d)
        if a<self.S:ev=('haar',None)
        elif a<self.S+self.R:ev=('residual',self.model.residual_state(z[0]))
        else:ev=('gate',None)
        self.events[z]=ev
        return ev,True


def layer_resolve(model,queries,ell,oracle):
    """Conditioned on categories, affine output equals offset(lower)+Haar(span(B)).

    queries list of (site,time,layer), all same ell. Returns terms for nonlinear
    offset, known constants, Haar basis, and raw lower coordinate prerequisites.
    """
    q=model.q
    m=len(queries)
    pending={}
    for ix,(site,t,L) in enumerate(queries):
        assert L==ell
        w=[0]*m;w[ix]=1
        add_vec(pending,(site,t),w,1,q)
    rank_basis={}
    terms=[]           # (vector, site,time), representing coefficient * F_i^ell
    constants=[0]*m
    examined=0
    while pending:
        z=max(pending,key=lambda x:(x[1],x[0]))
        vec=pending.pop(z)
        if basis_contains(rank_basis,vec,q):continue
        examined+=1
        (kind,val),_new=oracle.event(z)
        if kind=='haar':
            add_basis(rank_basis,vec,q)
        elif kind=='residual':
            a=val[ell]%q
            if a:
                for i,v in enumerate(vec):constants[i]=(constants[i]+a*v)%q
        else:
            parents=model.input_sites(z[0]); co=model.layer_coeffs(z[0],ell)
            oracle.parent_lookups+=len(parents)
            terms.append((tuple(vec),z,parents))
            for j,a in zip(parents,co):
                add_vec(pending,(j,z[1]-1),vec,int(a),q)
    req=set()
    if ell:
        for vec,z,parents in terms:
            if not any(vec):continue
            for j in parents:
                for h in range(ell):req.add((j,z[1]-1,h))
    else:
        assert not req
    return constants,terms,rank_basis,sorted(req),examined


def sample_coordinates(model,targets,rng=None,diagnostics=False):
    """Exact stationary joint sample of (site,time,layer) coordinate targets.

    Permits arbitrary query times and common ancestors; queries may repeat.
    """
    rng=rng if rng is not None else random.Random()
    oracle=EventOracle(model,rng)
    targets=list(targets)
    for site,t,ell in targets:
        assert 0<=site<model.n and 0<=ell<model.c
    diagnostics_layers=[]
    def solve(ell,requested):
        if not requested:return []
        if ell<0:raise RuntimeError('Impossible unresolved negative layer')
        top=[(ix,key) for ix,key in enumerate(requested) if key[2]==ell]
        if not top:return solve(ell-1,requested)
        rest=[(ix,key) for ix,key in enumerate(requested) if key[2]<ell]
        assert len(top)+len(rest)==len(requested)
        constants, terms, basis, prerequisites, nvisits=layer_resolve(model,[key for ix,key in top],ell,oracle)
        needs=[key for ix,key in rest]
        known=set(needs)
        for p in prerequisites:
            if p not in known:needs.append(p);known.add(p)
        lower=solve(ell-1,needs) if needs else []
        env=dict(zip(needs,lower))
        ans=list(constants)
        for vec,(site,t),parents in terms:
            rows=[tuple(env[(j,t-1,h)] for h in range(ell)) for j in parents]
            y=model.layer_forcing(site,ell,rows)
            oracle.force_evaluations+=1
            if y:
                for ix,v in enumerate(vec):ans[ix]=(ans[ix]+v*y)%model.q
        for basisvec in basis.values():
            coeff=rng.randrange(model.q)
            for ix,v in enumerate(basisvec):ans[ix]=(ans[ix]+coeff*v)%model.q
        out=[0]*len(requested)
        for (ix,key),v in zip(top,ans):out[ix]=v
        for ix,key in rest:out[ix]=env[key]
        diagnostics_layers.append({'layer':ell,'raw_targets':len(top),'lower_prerequisites':len(prerequisites),
                                  'rank':len(basis),'event_visits':nvisits})
        return out
    values=solve(model.c-1,targets)
    if diagnostics:
        return values, {'fresh_events':oracle.fresh, 'parent_lookups':oracle.parent_lookups,
                        'forcing_calls':oracle.force_evaluations,
                        'layers':diagnostics_layers}
    return values


def sample_states(model,site_time, rng=None, diagnostics=False):
    site_time=list(site_time)
    queries=[(j,t,ell) for j,t in site_time for ell in range(model.c)]
    vals,info=sample_coordinates(model,queries,rng,True)
    states={z:tuple(vals[i*model.c:(i+1)*model.c]) for i,z in enumerate(site_time)}
    return (states,info) if diagnostics else states


def evolve(model,prev,rng=None):
    """Finite-state synchronous forward transition for independent verification."""
    rng=rng or random.Random()
    oracle=EventOracle(model,rng)
    out=[]
    for i in range(model.n):
        (kind,value),_=oracle.event((i,0))
        if kind=='haar':out.append(tuple(rng.randrange(model.q) for _ in range(model.c)))
        elif kind=='residual':out.append(tuple(int(x)%model.q for x in value))
        else:
            pp=model.input_sites(i)
            rr=[]
            for ell in range(model.c):
                a=sum(int(w)*prev[j][ell] for w,j in zip(model.layer_coeffs(i,ell),pp))
                a+=model.layer_forcing(i,ell, [tuple(prev[j][:ell]) for j in pp])
                rr.append(a%model.q)
            out.append(tuple(rr))
    return tuple(out)


if __name__=='__main__':
    M=StratifiedModel(n=2,c=3,q=2,s='0.19',r='0.08',parents={0:(0,1,1),1:(0,0,1)},
      coeffs=lambda i,h:(1,1,h%2),
      forcing=lambda i,h,rows: (int(i==1) if h==0 else (rows[0][0]*rows[1][0] if h==1 else rows[0][0]*rows[1][1])),
      residual=(1,0,1))
    M.validate()
    r=random.Random(818)
    for _ in range(4): print(sample_states(M,[(0,0),(1,0)],r,True))
