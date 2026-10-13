"""Fixed-degree comparison compiler: sampled safe subspace + exact filtration.

Only the comparison callback crosses the learner boundary. Raw ANFs and exact
stabilizers are computed locally. Degree>=3 is the intended new theorem lane;
the sharper quadratic bilinear implementation remains separate and preserved.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import math
import random
import sys
import time
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import adaptive_compiler as ac


def M(n,d):
    return sum(math.comb(n,j) for j in range(min(n,d)+1))


def points(n,d):
    return [sum(1 << j for j in choice) for size in range(min(n,d)+1)
            for choice in combinations(range(n),size)]


@dataclass
class Polynomial:
    n:int
    degree_bound:int
    terms:set

    def __call__(self,x,meter=None):
        value=0
        for monomial in self.terms:
            value ^= int((monomial & x)==monomial)
        if meter is not None:
            meter.add('polynomial_evaluations')
            meter.add('anf_monomial_tests',len(self.terms))
        return value

    def delta(self,v,meter=None):
        terms=set()
        for monomial in self.terms:
            available=monomial & v
            sub=available
            while sub:
                target=monomial ^ sub
                if target in terms:
                    terms.remove(target)
                else:
                    terms.add(target)
                sub=(sub-1)&available
                if meter is not None:
                    meter.add('shifted_monomial_terms')
        if meter is not None:
            meter.add('exact_derivative_polynomials')
        return Polynomial(self.n,max(0,self.degree_bound-1),terms)

    def invariant(self,v,meter=None):
        return not self.delta(v,meter).terms

    def toggles(self,v,meter=None):
        return self.delta(v,meter).terms=={0}

    def body(self):
        return dict(n=self.n,degree_bound=self.degree_bound,terms=sorted(self.terms))


def interpolate(values,n,d,meter=None):
    terms=set()
    for mask in points(n,d):
        coefficient=0
        sub=mask
        while True:
            coefficient ^= values[sub]
            if not sub:
                break
            sub=(sub-1)&mask
        if coefficient:
            terms.add(mask)
    if meter is not None:
        meter.add('anf_interpolations')
        meter.add('anf_output_coefficients',M(n,d))
    return Polynomial(n,d,terms)


def translation_filtration(poly,V,meter=None,constant_only=False):
    """Exact full translation kernel; no solving nonlinear equations in v.

On V where degree(Delta_v poly)<=ell, the degree-ell coefficient map is
linear in v. Recover that map on a V basis, then take its GF(2) kernel.
Stopping before ell=0 gives constant-derivative directions instead of periods.
"""
    V=list(V)
    stages=[]
    for ell in range(poly.degree_bound-1,0 if constant_only else -1,-1):
        equations={}
        before=len(V)
        for j,v in enumerate(V):
            derivative=poly.delta(v,meter)
            if any(mask.bit_count()>ell for mask in derivative.terms):
                raise ArithmeticError('descending derivative-degree invariant failed')
            for mask in derivative.terms:
                if mask.bit_count()==ell:
                    equations[mask]=equations.get(mask,0)|(1 << j)
        null=ac.kernel(list(equations.values()),len(V),meter)
        V=[ac.combine(V,bits,meter) for bits in null]
        stages.append(dict(derivative_degree=ell,dimension_before=before,
                           dimension_after=len(V),coefficient_equations=len(equations)))
    return V,stages


class Sampler:
    def __init__(self,polys,toggles,S,n,meter=None):
        self.n,self.k=n,len(polys)
        self.meter=meter
        self.L,self.pivots=ac.echelon(ac.kernel(S,n,meter),n,meter)
        self.d=len(self.L)
        pivot_set=set(self.pivots)
        self.free=[j for j in range(n) if j not in pivot_set]
        self.B=[sum(((row >> j)&1) << a for a,j in enumerate(self.free)) for row in self.L]
        pivot_mask=sum(1 << j for j in self.pivots)
        self.F=[]
        for q in polys:
            restricted={sum(((m >> j)&1) << a for a,j in enumerate(self.pivots))
                        for m in q.terms if m & ~pivot_mask==0}
            self.F.append(Polynomial(self.d,q.degree_bound,restricted))
        self.a=[ac.linear(self.L,v,meter) for v in toggles]
        self.W=ac.complement(self.a,self.d,meter)
        if len(self.W)!=self.d-self.k:
            raise ArithmeticError('quotient own-toggle independence failed')
        self.random_bits=n-self.k

    def sample_from_seed(self,target,seed):
        qdim=self.d-self.k
        z=ac.combine(self.W,seed&((1 << qdim)-1),self.meter)
        for i,(f,a) in enumerate(zip(self.F,self.a)):
            if f(z,self.meter)!=((target>>(self.k-i-1))&1):
                z ^= a
        free_seed=seed>>qdim
        p=z^ac.linear(self.B,free_seed,self.meter)
        return ac._scatter(p,self.pivots,self.meter)|ac._scatter(free_seed,self.free,self.meter)

    def sample(self,target,rng,meter=None):
        if meter is not None:
            meter.add('prefix_fiber_random_bits',self.random_bits)
        return self.sample_from_seed(target,rng.getrandbits(self.random_bits))

    def fiber(self,target):
        for seed in range(1 << self.random_bits):
            yield self.sample_from_seed(target,seed)

    def prefix(self,x):
        z,out=ac.linear(self.L,x,self.meter),0
        for f in self.F:
            out=(out<<1)|f(z,self.meter)
        return out


class Prefix:
    def __init__(self,n,meter):
        self.n,self.meter=n,meter
        self.q,self.toggles=[],[]
        self.S=[1 << j for j in range(n)]
    def sampler(self):
        return Sampler(self.q,self.toggles,self.S,self.n,self.meter)
    def prefix(self,x):
        out=0
        for q in self.q:
            out=(out<<1)|q(x,self.meter)
        return out
    def add(self,q,v):
        if not q.toggles(v,self.meter) or not all(p.invariant(v,self.meter) for p in self.q):
            raise ArithmeticError('own-toggle or previous-prefix invariance failed')
        before=len(self.S)
        D,constant_steps=translation_filtration(q,self.S,self.meter,constant_only=True)
        newS,response_steps=translation_filtration(q,D,self.meter,constant_only=False)
        # The second call is redundant above degree zero but intentionally
        # proves/checks the exact full kernel rather than retaining sampled W.
        a=before-len(D)
        if len(newS)!=before-a-1:
            raise ArithmeticError('general stabilizer defect identity failed')
        self.q.append(q)
        self.toggles.append(v)
        self.S=newS
        return dict(constant_translation_dimension=len(D),constant_translation_codimension=a,
                    stabilizer_dimension=len(newS),filtration=constant_steps+response_steps)


def parameters(n,r,d,beta,prefix_length=None,mode='safe_subspace'):
    if d<2 or not 0<=r<=n or not 0<beta<=.5:
        raise ValueError('require degree>=2, 0<=r<=n, beta in (0,1/2]')
    h=n-r
    m=h if prefix_length is None else prefix_length
    if not 0<=m<=h or mode not in ('safe_subspace','raw_body'):
        raise ValueError('invalid prefix count or mode')
    p=2.0**(-r-1)
    R=math.ceil(math.log(4*m/beta)/p) if m else 0
    delta_raw=beta/((2 if mode=='raw_body' else 4)*m*R) if m else 0
    raw_t=math.ceil(math.log(1/delta_raw)/(-math.log1p(-2.0**(-2*d)))) if m else 0
    P=sum(n-k-1 for k in range(m))
    leading=sum(M(k+r,d) for k in range(m)) if mode=='safe_subspace' else m*M(n,d)
    tail=0 if prefix_length is not None else M(n,d)*((1 << r)-1)
    # Raw cap/false pass/membership false pass each get beta/4;
    # safe-subspace growth and global tournament caps each get beta/8.
    trial_caps=[math.ceil((2*(h-k)+8*math.log(8*m/beta))/p) for k in range(m)]
    Nmax=max(trial_caps,default=0)
    delta_member=beta/(4*m*Nmax) if m else 0
    member_t=math.ceil(math.log(1/delta_member)/(-math.log1p(-2.0**(-(d-1))))) if m else 0
    H=math.ceil(4*P+8*math.log(8/beta)) if P else 0
    local_queries=sum(1+trial_caps[k]*(1+2*member_t)+(h-k) for k in range(m)) if mode=='safe_subspace' else 0
    return dict(n=n,r=r,degree=d,beta=beta,h=h,stages=m,prefix_only=prefix_length is not None,
                mode=mode,p=p,R=R,raw_t=raw_t,delta_raw=delta_raw,
                member_trial_caps=trial_caps,member_t=member_t,delta_member=delta_member,
                tournament_pair_count_cap=P,tournament_total_attempt_cap=H,
                leading_interpolation_cap=leading,tail_comparisons=tail,
                worst_comparison_bound=leading+local_queries+3*m*R*raw_t+tail+2*H+P,
                failure_budget=dict(raw_cap=beta/4,false_raw=beta/(2 if mode=='raw_body' else 4),
                                    false_membership=0 if mode=='raw_body' else beta/4,
                                    member_growth=0 if mode=='raw_body' else beta/8,
                                    tournament_cap=beta/8,total=7*beta/8 if mode=='raw_body' else beta))


def reconstruct(n,r,d,k,v,prefix,source,rng,cfg,meter):
    h,sdim=cfg['h'],len(prefix.S)
    target=h-k
    residual=sdim-target
    source.phase='member_base'
    q0=ac.core._label(source,v,0)
    W=[] if residual else list(prefix.S)
    trials=tests=accepted=0
    while len(W)<target and trials<cfg['member_trial_caps'][k]:
        trials+=1
        s=ac.combine(prefix.S,rng.getrandbits(sdim),meter)
        meter.add('membership_direction_random_bits',sdim)
        if len(ac.echelon(W+[s],n,meter)[0])==len(W):
            continue
        source.phase='constant_derivative_tests'
        response=ac.core._label(source,v,s)^q0
        passed=True
        for _ in range(cfg['member_t']):
            x=rng.getrandbits(n)
            meter.add('membership_probe_random_bits',n)
            tests+=1
            if ac.core._label(source,v,x^s)^ac.core._label(source,v,x)^response:
                passed=False
                break
        if passed:
            W.append(s)
            accepted+=1
    if len(W)<target:
        return None,dict(status='UNKNOWN',reason='member_progress_cap',trials=trials)
    U=ac.complement(W,n,meter)
    if len(U)!=k+r:
        raise ArithmeticError('safe-subspace quotient dimension failed')
    source.phase='quotient_interpolation'
    values={0:q0}
    for mask in points(len(U),d)[1:]:
        values[mask]=ac.core._label(source,v,ac.combine(U,mask,meter))
    qU=interpolate(values,len(U),d,meter)
    source.phase='safe_subspace_responses'
    responses=sum((ac.core._label(source,v,s)^q0) << j for j,s in enumerate(W))
    basis=U+W
    rows=[sum(((basis[j]>>i)&1) << j for j in range(n)) for i in range(n)]
    coordinates=ac.matrix_inverse(rows,n,meter)
    u=len(U)
    def f(x):
        c=ac.linear(coordinates,x,meter)
        return qU(c&((1 << u)-1),meter)^ac.parity(responses&(c>>u),meter)
    raw=interpolate({x:f(x) for x in points(n,d)},n,d,meter)
    if not raw.toggles(v,meter) or not all(q.invariant(v,meter) for q in prefix.q):
        return None,dict(status='UNKNOWN',reason='post_interpolation_toggle_gate')
    return raw,dict(status='accepted',sampled_safe_dimension=len(W),
                    actual_target_dimension=target,member_trials=trials,
                    member_point_tests=tests,accepted_independent_samples=accepted,
                    quotient_dimension=len(U),quotient_anchor_count=M(len(U),d),
                    source_free_known_constant_subspace=(residual==0))


def acquire(n,r,d,query,seed,beta=.01,prefix_length=None,mode='safe_subspace'):
    start=time.perf_counter()
    cfg=parameters(n,r,d,beta,prefix_length,mode)
    source,meter=ac.Source(query),ac.Meter()
    prefix=Prefix(n,meter)
    stages=[]
    match_state=dict(attempts=0,matches=0)
    def finish(status,reason=None,model=None):
        out=dict(status=status,reason=reason,parameters=cfg,comparison_calls=source.calls,
                 source_calls_by_phase=dict(source.by_phase),local_operations=dict(meter.ops),
                 random_bits={k:v for k,v in meter.ops.items() if k.endswith('random_bits')},
                 stages=stages,acquisition_seconds=time.perf_counter()-start,
                 acquired_toggle_vectors=prefix.toggles,acquired_stabilizer_basis=prefix.S,
                 model_bodies=[q.body() for q in model] if model is not None else None,
                 tournament_totals=match_state)
        if source.calls>cfg['worst_comparison_bound']:
            raise ArithmeticError('full fixed-degree comparison cap exceeded')
        return out,model,prefix
    for k in range(cfg['stages']):
        before=len(prefix.S)
        if not cfg['h']-k<=before<=n-k:
            return finish('UNKNOWN','stabilizer_dimension_guard')
        raw_rng=random.Random(seed+1000003*(k+1))
        member_rng=random.Random(seed+1900033*(k+1))
        certified_zero=before==cfg['h']-k
        if certified_zero:
            winner,trials,reason=ac._select_certified_zero(prefix.S,k,source,raw_rng,cfg,meter,match_state)
            if reason:
                return finish('UNKNOWN',reason)
        else:
            sampler=prefix.sampler()
            winner=None
            trials=[]
            for j in range(cfg['R']):
                v=ac.combine(prefix.S,raw_rng.getrandbits(before),meter)
                meter.add('direction_random_bits',before)
                if not v:
                    continue
                source.phase='raw_pair_validation'
                passed=True
                for test in range(cfg['raw_t']):
                    if not ac.core._pair_test(k,v,sampler,source,raw_rng,meter):
                        passed=False
                        break
                trials.append(dict(direction=v,passed=passed,pair_tests=test+1))
                if passed:
                    winner=v
                    break
            if winner is None:
                return finish('UNKNOWN','raw_direction_cap')
        if mode=='raw_body':
            source.phase='raw_interpolation'
            q=interpolate({x:ac.core._label(source,winner,x) for x in points(n,d)},n,d,meter)
            rec=dict(status='accepted',raw_anchor_count=M(n,d))
            if not q.toggles(winner,meter) or not all(old.invariant(winner,meter) for old in prefix.q):
                return finish('UNKNOWN','post_interpolation_toggle_gate')
        else:
            q,rec=reconstruct(n,r,d,k,winner,prefix,source,member_rng,cfg,meter)
            if q is None:
                return finish('UNKNOWN',rec['reason'])
        update=prefix.add(q,winner)
        after=len(prefix.S)
        if n-(k+1)-after>r:
            return finish('UNKNOWN','stabilizer_defect_guard')
        stages.append(dict(stage=k,selector='certified_zero_tournament' if certified_zero else 'raw_paired_cut',
                           dimension_S_before=before,dimension_S_after=after,
                           defect_before=n-k-before,defect_after=n-k-1-after,
                           direction=winner,trials=trials,reconstruction=rec,exact_update=update))
    if prefix_length is not None:
        return finish('returned_prefix',model=list(prefix.q))
    source.phase='tail_enumeration'
    sampler=prefix.sampler()
    values=[{} for _ in range(r)]
    for x in points(n,d):
        local=sum(source(y,x) for y in sampler.fiber(prefix.prefix(x)) if y!=x)
        for j in range(r):
            values[j][x]=(local>>(r-j-1))&1
    if source.by_phase['tail_enumeration']!=cfg['tail_comparisons']:
        raise ArithmeticError('tail accounting failed')
    model=list(prefix.q)+[interpolate(v,n,d,meter) for v in values]
    return finish('returned_model',model=model)
