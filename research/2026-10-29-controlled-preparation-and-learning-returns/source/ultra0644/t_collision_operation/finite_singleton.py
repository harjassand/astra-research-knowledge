"""Compile/run a Haar-free singleton with four exp-coins and integer table.

Finite-group spectral/Bernstein machinery is ordinary prior. Its exact
positive composition with the kinetic receiver is the claimed interface.
Only the exp comparisons remain real/random primitives at runtime; no
floating probability clipping, matrix exponential or Choi synthesis.
"""
from fractions import Fraction
from math import lcm
from pathlib import Path
from time import perf_counter
import json
import sympy as s
import numpy as np


def compile_program():
    rx=s.Matrix([[1,0,0],[0,0,-1],[0,1,0]])
    ry=s.Matrix([[0,0,1],[0,1,0],[-1,0,0]])
    rotations=[rx,rx.T,ry,ry.T]
    group=[s.eye(3)];index={tuple(group[0]):0};i=0
    while i<len(group):
        for r in rotations:
            g=r*group[i];key=tuple(g)
            if key not in index:index[key]=len(group);group.append(g)
        i+=1
    assert len(group)==24
    q=s.zeros(24)
    for j,g in enumerate(group):
        q[j,j]-=s.Rational(1,2)
        for r in rotations:q[index[tuple(r*g)],j]+=s.Rational(1,8)
    rates=[-s.Rational(j,4) for j in range(5)]
    assert set(q.eigenvals())==set(rates)
    assert q==q.T and all(sum(q[:,j])==0 for j in range(24))
    e=s.zeros(24,1);e[0]=1;coefficients=[]
    for rate in rates:
        v=e
        for other in rates:
            if other!=rate:v=(q-other*s.eye(24))*v/(rate-other)
        assert q*v==rate*v
        coefficients.append(v)
    assert sum(coefficients,s.zeros(24,1))==e
    bernstein=s.Matrix(24,5,lambda g,k:sum(coefficients[j][g]*s.binomial(k,j)/s.binomial(4,j)
                                            for j in range(k+1)))
    assert min(bernstein)>=0 and max(bernstein)<=1
    assert all(sum(bernstein[:,k])==1 for k in range(5))
    x=s.Symbol('x')
    for g in range(24):
        poly=sum(coefficients[j][g]*x**j for j in range(5))
        mixture=sum(bernstein[g,k]*s.binomial(4,k)*x**k*(1-x)**(4-k) for k in range(5))
        assert s.expand(poly-mixture)==0
    columns=[]
    for k in range(5):
        denominator=lcm(*[int(s.denom(bernstein[g,k])) for g in range(24)])
        weights=[int(denominator*bernstein[g,k]) for g in range(24)]
        assert sum(weights)==denominator and min(weights)>=0
        columns.append(dict(denominator=denominator,weights=weights))
    return dict(scope='Exact finite positive singleton program, no Haar or Choi input',
          group=[list(map(int,g)) for g in group],columns=columns,
          group_states=24,bernstein_degree=4,exp_coin_mean='exp(-t/4)',
          rates=[str(r) for r in rates],
          source_generator='left multiply ±x/±y quarter-turn at total rate1/2',
          exact_checks='all spectral vectors, polynomial identities, nonnegative normalized Bernstein columns',
          real_random_primitives_per_query=4,
          integer_categorical_denominators=[c['denominator'] for c in columns],
          runtime='K counts four independent Exp(1)>=t/4 events; choose group with integer columnK; query F1(g^Tz)')


class FiniteSingleton:
    def __init__(self,program):
        self.program=program
        self.group=np.asarray(program['group'],int).reshape(24,3,3)
        self.cumulative=[np.cumsum(col['weights']) for col in program['columns']]
        self.denominators=[col['denominator'] for col in program['columns']]
        self.exp_draws=self.integer_draws=self.initial_queries=0

    def sample(self,z,t,initial_f1,rng):
        if not np.isfinite(t) or t<0:raise ValueError('finite t>=0 required')
        k=int(np.count_nonzero(rng.exponential(size=4)>=t/4))
        self.exp_draws+=4
        u=int(rng.integers(self.denominators[k]));self.integer_draws+=1
        g=int(np.searchsorted(self.cumulative[k],u,side='right'))
        self.initial_queries+=1
        return initial_f1(self.group[g].T@z)


def main():
    started=perf_counter();program=compile_program();compiled=perf_counter()-started
    path=Path(__file__).parent/'outputs'/'FINITE_SINGLETON_PROGRAM.json'
    path.write_text(json.dumps(program,indent=2)+'\n')
    sampler=FiniteSingleton(program);rng=np.random.default_rng(2026102908)
    z=np.array([.6,.48+.64j,0]);m=np.array([[.5,.125,0],[.125,-.25,.0625],[0,.0625,.125]])
    assert np.linalg.norm(m,2)<1
    tick=perf_counter()
    values=np.array([sampler.sample(z,3.,lambda w:w@m@w,rng) for _ in range(20000)])
    elapsed=perf_counter()-tick
    # Independent ordinary9x9 covariance propagator for this known-M control.
    from scipy.linalg import expm
    rx=np.array([[1,0,0],[0,0,-1],[0,1,0]])
    ry=np.array([[0,0,1],[0,1,0],[-1,0,0]])
    generator=sum(np.kron(r,r) for r in [rx,rx.T,ry,ry.T])/8-np.eye(9)/2
    target=z@(expm(3*generator)@m.ravel()).reshape(3,3)@z
    stats=[]
    for part in ['real','imag']:
        a=getattr(values,part);truth=float(getattr(target,part));se=float(a.std(ddof=1)/np.sqrt(len(a)))
        stats.append(dict(part=part,mean=float(a.mean()),reference=truth,stderr=se,z=(float(a.mean())-truth)/se))
    receipt=dict(scope='Exact positive program plus one floating execution, not a full-law benchmark',
        compile_seconds=compiled,run_seconds=elapsed,observations=stats,
        exp_draws=sampler.exp_draws,integer_draws=sampler.integer_draws,
        initial_queries=sampler.initial_queries,
        columns_denominators=sampler.denominators,seed=2026102908,
        bit_scope='Integer tables exact; continuous exp comparisons/source arithmetic are floating, not fair-bit certified',
        ordinary_scope='Known-M q1 may be computed directly much cheaper; no estimator dominance claimed')
    out=path.with_name('FINITE_SINGLETON_EXECUTION.json')
    out.write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
