"""All-time rejection extension for b/a < 3/2, floating-point prototype.

The mathematical sampling construction is exact with exact primitives.
This implementation is NOT an exact-real/interval-certified implementation.
The linear Bernoulli factory is a credited implementation of Mark Huber,
'Nearly optimal Bernoulli factories for linear functions', Section 2.2,
arXiv:1308.1562v2; CPC 25 (2016), 577-591. It is not an Astra invention.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import exp, log, log1p, sqrt
from typing import Callable
import numpy as np
from scipy.special import eval_genlaguerre
from collision_dual import VarianceSampler, moment_sample

@dataclass
class Work:
    proposals: int = 0
    input_coins: int = 0
    total_degree: int = 0
    effective_splits: int = 0


def linear_bernoulli_factory(coin: Callable[[], bool], multiplier: float,
                             margin: float, rng: np.random.Generator) -> bool:
    """Huber 2013/2014 linear factory. Require multiplier*p <= 1-margin.

    No iteration cap: adding one without a failure output would bias the law.
    Floating underflow/overflow raises rather than silently truncating a run.
    """
    if not (multiplier > 1 and 0 < margin < 1):
        raise ValueError('Require multiplier>1 and 0<margin<1.')
    # Preserve the initialization order in Huber's published pseudocode.
    threshold = 4.6/margin
    eps = min(margin, .644)
    i = 1
    c = multiplier
    while True:
        # A repeat-until loop: every factory stage makes at least one input
        # coin call, even if a previous geometric jump overshot the threshold.
        while True:
            b = coin()
            if b:
                i -= 1
            else:
                i += int(rng.geometric((c-1)/c))-1
            if i == 0 or i >= threshold:
                break
        if i == 0:
            return True
        log_survival = -i*log1p(eps/2)
        if rng.random() >= exp(log_survival):
            return False
        c *= 1+eps/2
        eps /= 2
        threshold *= 2
        if eps == 0 or not np.isfinite(threshold):
            raise FloatingPointError('Factory exceeded floating-point precision.')


def parameters(a: float, b: float, rho: float) -> tuple[float,float,float,float]:
    if not (0 < a < b < 1.5*a):
        raise ValueError('This finite-mean theorem requires 0<a<b<1.5*a.')
    r = 1-a/b
    if not r < rho < 2*a/b-1:
        raise ValueError('Require 1-a/b < rho < 2*a/b-1.')
    g=b*(1+rho)
    c=((1+rho)/(1-rho))**1.5/(1-r/rho)
    integral=(a*b/(g*(2*a-g)))**1.5
    return r,g,c,integral


def exact_velocity_ideal_prototype(t: float, a: float, b: float, rho: float,
                                  initial: VarianceSampler, rng: np.random.Generator
                                  ) -> tuple[np.ndarray, Work]:
    """Sample by the ideal-exact construction, using floating primitives here.

    Return velocity and measured work. Do not describe the executable's output
    as bit-exact or TV-certified: interval arithmetic is not implemented.
    """
    if not (np.isfinite(t) and t >= 0):
        raise ValueError('t must be finite and nonnegative.')
    r,g,c,_=parameters(a,b,rho)
    work=Work()
    while True:
        work.proposals += 1
        v=sqrt(g)*rng.normal(size=3)
        sq=float(v@v)
        x=sq/(2*b)
        lower=(g/b)**1.5*exp(-sq*.5*(1/a-1/g))
        margin=lower/c
        if margin == 0:
            raise FloatingPointError('Proposal lower bound underflow; use interval arithmetic.')
        def coin() -> bool:
            work.input_coins += 1
            k=int(rng.geometric(1-r/rho))-1
            work.total_degree += k
            h,splits,_=moment_sample(k,t,a,b,initial,rng)
            work.effective_splits += splits
            # Cauchy coefficient bound proves abs(normalized) <= 1 in real arithmetic.
            normalized=(1-rho)**1.5*exp(-x*rho/(1+rho))*rho**k*float(eval_genlaguerre(k,.5,x))*h
            if not np.isfinite(normalized) or abs(normalized)>1+1e-12:
                raise FloatingPointError('Signed-envelope calculation violated its bound.')
            return bool(rng.random() < (1-normalized)/2)
        # Input mean=(1-f_t(v)/(C q_g(v)))/2. Complement of doubling gives
        # an acceptance coin with probability f_t(v)/(C q_g(v)).
        if not linear_bernoulli_factory(coin,2.,margin,rng):
            return v,work
