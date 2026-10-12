"""Rational upper confidence radii; log and square-root inequalities checked exactly."""
from fractions import Fraction
from math import isqrt, ceil, log

def upper_log_integer(x: Fraction) -> int:
    if x<=1:return 0
    # Floating log proposes an integer only. A finite, positive Taylor sum
    # supplies an exact rational proof that exp(t) > x; t increases if needed.
    t=max(1,ceil(log(float(x))))
    while True:
        term=Fraction(1);total=term
        # Terms through this degree are enough for the moderate confidence budgets
        # in the benchmark; failure merely increments t and retries.
        for j in range(1,20*t+100):
            term*=Fraction(t,j);total+=term
            if total>x:return t
        t+=1

def upper_sqrt(x: Fraction, digits: int=12) -> Fraction:
    if x<0:raise ValueError('Negative square root.')
    scale=10**digits
    a=x.numerator*scale*scale;b=x.denominator
    lo=isqrt(a//b)
    if lo*lo*b<a:lo+=1
    result=Fraction(lo,scale)
    assert result*result>=x
    return result

def calibration_radii(samples:int,k:int,delta:Fraction,bg:Fraction,rho:Fraction):
    if samples<1 or k<1 or not 0<delta<1 or bg<0 or rho<=0:raise ValueError('Invalid parameters.')
    d=(k+1)**2+k;t=upper_log_integer(Fraction(2*d)/delta)
    eta=upper_sqrt(Fraction(t,2*samples))
    er=(bg+rho)*(2*upper_sqrt(Fraction(t,samples))+Fraction(t,samples))
    return eta,er,dict(log_upper_integer=t,union_quantities=d,
                      endpoint_radius_exact=str(eta),flux_radius_exact=str(er),
                      proof='exp(t)>2D/delta by positive rational Taylor sum; square-root upper inequalities checked by integer squares.')

def validation_radius(samples:int,delta:Fraction):
    t=upper_log_integer(Fraction(2)/delta)
    return upper_sqrt(Fraction(t,2*samples))
