"""Outward rational binary-entropy bounds. Decimal logs are bracketed under
their documented correct-rounding contract; square roots use integer isqrt.
This module is newly written and reads no predecessor files.
"""
from fractions import Fraction as Q
from decimal import Decimal as D,Context,ROUND_FLOOR,ROUND_CEILING,ROUND_HALF_EVEN
from math import isqrt
from functools import lru_cache

DOWN=Context(prec=60,rounding=ROUND_FLOOR)
UP=Context(prec=60,rounding=ROUND_CEILING)
NEAR=Context(prec=60,rounding=ROUND_HALF_EVEN)
BITS=44


def floor_grid(x,bits=BITS):
    x=Q(x); m=1<<bits
    return Q((x.numerator*m)//x.denominator,m)


def ceil_grid(x,bits=BITS): return -floor_grid(-x,bits)


def sqrt_interval(s,bits=64):
    s=Q(s); assert s>=0
    m=1<<bits; v=isqrt((s.numerator*m*m)//s.denominator)
    lo=Q(v,m)
    return lo,(lo if lo*lo==s else Q(v+1,m))


@lru_cache(maxsize=None)
def log_interval(x):
    x=Q(x); assert x>0
    a=DOWN.divide(D(x.numerator),D(x.denominator))
    b=UP.divide(D(x.numerator),D(x.denominator))
    return Q(NEAR.next_minus(NEAR.ln(a))),Q(NEAR.next_plus(NEAR.ln(b)))


@lru_cache(maxsize=None)
def binary_entropy(p):
    p=Q(p); assert 0<=p<=1
    lo=Q(0); hi=Q(0)
    for x in (p,1-p):
        if x:
            a,b=log_interval(x); lo-=x*b; hi-=x*a
    return floor_grid(lo),ceil_grid(hi)


@lru_cache(maxsize=None)
def entropy_of_squared_radius(s):
    s=Q(s); assert 0<=s<=1
    lo,hi=sqrt_interval(s)
    hi=min(Q(1),hi)
    lower=binary_entropy((1+hi)/2)[0]
    upper=binary_entropy((1+lo)/2)[1]
    return lower,upper


@lru_cache(maxsize=None)
def log_two_cosh_upper(x):
    """Upper bound for log(2 cosh(x)), x rational and nonnegative."""
    x=Q(x); assert x>=0
    a=DOWN.divide(D((-2*x).numerator),D((-2*x).denominator))
    b=UP.divide(D((-2*x).numerator),D((-2*x).denominator))
    eh=Q(NEAR.next_plus(NEAR.exp(b)))
    return ceil_grid(x+log_interval(1+eh)[1])
