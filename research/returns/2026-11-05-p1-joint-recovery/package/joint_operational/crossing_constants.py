#!/usr/bin/env python3
"""Stable evaluation of the finite constants in crossing_normalization_analysis.md."""
import argparse
import json
import math


def logsumexp(values):
    maximum = max(values)
    return maximum+math.log(sum(math.exp(x-maximum) for x in values))


def constants(n, u):
    if n < 1 or u <= 0:
        raise ValueError('Require n >= 1 and u > 0.')
    loga = lambda k: .5*math.log(u*u+k*k)
    logw = [(loga(2*j-1)+loga(2*j)-math.log(u))*n for j in range(n+1)]
    suma = sum(loga(2*j) for j in range(n+1))
    grid_terms = []
    for j in range(n+1):
        logd = -n*math.log(2)-math.lgamma(j+1)-math.lgamma(n-j+1)
        logell = logd+suma-loga(2*j)
        grid_terms.append(logw[j]+logsumexp([logd, logell]))
    logk = logsumexp(grid_terms)
    logf = .5*sum(math.log1p(u*u/(4*k*k)) for k in range(1, n))
    logdelta_bar = (math.log(2*n/u)-logf-math.lgamma(n+1)
                    +n*(math.log(u)-math.log(4-2/n)-math.log(n)))
    beta = -math.expm1(logw[0]-logw[n])
    logdelta = logdelta_bar-logsumexp([math.log(beta), logw[0]+logdelta_bar])
    loggap = math.log(6)-math.log(n*(n+1)*(2*n+1))-2*logk
    return dict(n=n,u=u,log_grid_constant=logk,log_gap_bound=loggap,
                log_scalar_certificate_delta=logdelta,
                grid_exponent_ratio=logk/(n*math.log(n)) if n>1 else None,
                certificate_exponent_ratio=-logdelta/(n*math.log(n)) if n>1 else None)


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--u', type=float, default=1.)
    parser.add_argument('--n', type=int, nargs='+', default=[2, 4, 8, 16, 32, 64])
    args=parser.parse_args()
    print(json.dumps([constants(n,args.u) for n in args.n], indent=2))
