"""Exact rational positivity and certified entropy separation for dilation.

No numerical packages are needed. Every logarithm is bracketed by a
finite rational atanh series, with its positive tail bounded explicitly.
"""
from fractions import Fraction as F
from math import comb


def log_unit_interval(x, terms=40):
    """Assume 1 <= x <= 2; return rational lower and upper log bounds."""
    assert 1 <= x <= 2
    y = (x - 1) / (x + 1)
    lower = 2 * sum((y ** (2*j + 1) / (2*j + 1) for j in range(terms)), F(0))
    upper = lower + 2 * y ** (2*terms + 1) / ((2*terms + 1) * (1 - y*y))
    return lower, upper


LOG2 = log_unit_interval(F(2))


def log_bounds(x):
    x = F(x)
    power = 0
    while x < 1:
        x *= 2
        power -= 1
    while x > 2:
        x /= 2
        power += 1
    low, high = log_unit_interval(x)
    if power >= 0:
        return low + power*LOG2[0], high + power*LOG2[1]
    return low + power*LOG2[1], high + power*LOG2[0]


def entropy_bounds(probabilities):
    low = F(0)
    high = F(0)
    for p in probabilities:
        lp, hp = log_bounds(p)
        low -= p * hp
        high -= p * lp
    return low, high


def g_bounds(r):
    lr, hr = log_bounds(r)
    l1, h1 = log_bounds(r+1)
    return (r+1)*l1-r*hr, (r+1)*h1-r*lr


def q(m):
    return F(16*(198*m*m+324*m+1), 3125*5**m)


if __name__ == '__main__':
    # Exact characteristic-function mapping. The Weyl polynomial of a
    # number-diagonal state supported on 0,1,2 is
    # 1-(p1+2*p2)*s+(p2/2)*s^2 times exp(-s/2).
    pin = [F(15,100), F(74,100), F(11,100)]
    poly_in = [sum(pin), -(pin[1]+2*pin[2]), pin[2]/2]
    assert poly_in == [F(1), -F(24,25), F(11,200)]
    t = F(3,2)
    poly_dilated = [coef*t**j for j,coef in enumerate(poly_in)]
    assert poly_dilated == [F(1), -F(36,25), F(99,800)]
    alpha = [F(4,625), F(522,625), F(99,625)]
    poly_alpha = [sum(alpha), -(alpha[1]+2*alpha[2]), alpha[2]/2]
    assert poly_alpha == [F(1), -F(144,125), F(99,1250)]
    amp_gain = F(5,4)
    assert 2*amp_gain-1 == t
    assert [coef*amp_gain**j for j,coef in enumerate(poly_alpha)] == poly_dilated
    # The ordinary vacuum amplifier sends number k to shifted NB(k+1).
    # Its mixture alpha has exactly the displayed q_m, as polynomial
    # coefficient identities valid for every integer m>=0 show.
    x = 1-1/amp_gain
    q_coef = [F(16,3125), F(16*324,3125), F(16*198,3125)]
    mixture_coef = [alpha[0]*(1-x),
                    alpha[1]*(1-x)**2/x-alpha[2]*(1-x)**3/(2*x*x),
                    alpha[2]*(1-x)**3/(2*x*x)]
    assert mixture_coef == q_coef
    # Exact normalization uses sum x^m, sum m*x^m and sum m^2*x^m.
    assert x == F(1,5)
    s0 = 1/(1-x)
    s1 = x/(1-x)**2
    s2 = x*(1+x)/(1-x)**3
    s3 = x*(1+4*x+x*x)/(1-x)**4
    assert F(16,3125)*(198*s2+324*s1+s0) == 1
    assert F(16,3125)*(198*s3+324*s2+s1) == F(169,100)
    # Every coefficient in 198*m^2+324*m+1 is positive: all q_m > 0.
    sin_low, sin_high = entropy_bounds(pin)
    gin_low, gin_high = g_bounds(F(1,3))
    assert sin_low > gin_high
    cutoff = 30
    out_low, out_high = entropy_bounds([q(m) for m in range(cutoff+1)])
    # For m>=31: q(m)=K*P(m)*x^m and -log q(m)<=m*log5+log(1/K).
    # Shift m=31+k and sum the resulting positive cubic exactly.
    start = cutoff+1
    p0 = 198*start*start+324*start+1
    p1 = 396*start+324
    p2 = 198
    sum_p = p0*s0+p1*s1+p2*s2
    sum_mp = start*sum_p+p0*s1+p1*s2+p2*s3
    log5_high = log_bounds(F(5))[1]
    logk_high = log_bounds(F(3125,16))[1]
    tail_upper = F(16,3125)*x**start*(log5_high*sum_mp+logk_high*sum_p)
    out_high += tail_upper
    gout_low, gout_high = g_bounds(F(3,4))
    assert out_high < gout_low
    print('Input entropy interval:',float(sin_low),float(sin_high))
    print('g(1/3) interval:',float(gin_low),float(gin_high))
    print('Output entropy interval:',float(out_low),float(out_high))
    print('Output entropy tail bound:',float(tail_upper))
    print('g(3/4) interval:',float(gout_low),float(gout_high))
    print('Certified entropy gap >',float(gout_low-out_high))
    print('CERTIFIED: dilation mapping, ordinary amplifier preparation, positivity, normalization, finite energy, and strict separation.')
