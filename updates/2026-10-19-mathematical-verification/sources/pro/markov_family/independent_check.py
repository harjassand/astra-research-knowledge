#!/usr/bin/env python3
"""Independent Decimal and optional SciPy checks, not an interval certificate.

Run with --matrix to also check exp(Q), the rates, and entropy edge by edge.
The exact certification is performed by certify_entropy.py.
"""
from decimal import Decimal as D, getcontext
import argparse
import json

getcontext().prec = 80


def atan(x):
    total = D(0)
    power = x
    k = 0
    while True:
        term = power / (2*k + 1)
        total += term if k % 2 == 0 else -term
        if abs(term) < D('1e-82'):
            return total
        power *= x*x
        k += 1


PI = 16*atan(D(1)/5)-4*atan(D(1)/239)
LOG2 = D(2).ln()
A_PARAM, B_PARAM = 8*LOG2, 18*LOG2


def value_derivative(x):
    s = (2*(x*x+4*PI*PI)).sqrt()
    sp = 2*x/s
    c1, c2 = B_PARAM-x, B_PARAM+3*x
    l1 = ((c1+s)/(c1-s)).ln()
    l2 = ((c2+2*s)/(c2-2*s)).ln()
    value = s*(2*l1+l2)/4
    derivative = sp*(2*l1+l2)/4 + s*((c1*sp+s)/(c1*c1-s*s)
                                       +(c2*sp-3*s)/(c2*c2-4*s*s))
    return value, derivative


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--matrix', action='store_true')
    args = parser.parse_args()
    lo, hi = D('2.29'), D('2.30')
    assert value_derivative(lo)[1] < 0 < value_derivative(hi)[1]
    for _ in range(260):
        mid = (lo+hi)/2
        if value_derivative(mid)[1] < 0:
            lo = mid
        else:
            hi = mid
    root = (lo+hi)/2
    value = value_derivative(root)[0]
    bound = 3/(44*LOG2)*(LOG2*LOG2/2+8*PI*PI)
    assert D('26.178911678346') < value < D('26.178911678347')
    result = {'status':'PASS', 'arithmetic':'80-digit Decimal; numerical check only',
              'critical_point':format(root,'.69f'), 'minimum_entropy':format(value,'.68f'),
              'general_entropy_bound':format(bound,'.69f')}
    if args.matrix:
        import numpy as np
        from scipy.linalg import expm
        a, b = float(A_PARAM), float(B_PARAM)
        x = float(root)
        u = np.array([1,1,-1,-1])/2
        v = np.array([1,-1,0,0])/np.sqrt(2)
        w = np.array([0,0,1,-1])/np.sqrt(2)
        L = -a*np.outer(v,v)-b*(np.outer(u,u)+np.outer(w,w))
        r = np.sqrt(x*x+4*np.pi*np.pi)
        Q = L+x*(np.outer(u,u)-np.outer(w,w))+r*(np.outer(u,w)-np.outer(w,u))
        P = np.array([[264193,260097,262143,262143],
                      [260097,264193,262143,262143],
                      [262143,262143,262147,262143],
                      [262143,262143,262143,262147]],dtype=float)/(2**20)
        residual = float(np.max(np.abs(expm(Q)-P)))
        offdiagonal = Q[~np.eye(4,dtype=bool)]
        direct = sum((Q[i,j]-Q[j,i])/4*np.log(Q[i,j]/Q[j,i])
                     for i in range(4) for j in range(i+1,4))
        assert residual < 2e-14
        assert float(offdiagonal.min()) > 0
        assert float(np.max(np.abs(Q.sum(axis=1)))) < 2e-14
        assert abs(direct-float(value)) < 2e-12
        result['matrix_check'] = {'exponential_max_error':residual,
             'smallest_offdiagonal_rate':float(offdiagonal.min()),
             'edgewise_entropy':float(direct),
             'scalar_vs_edgewise_entropy_error':float(abs(direct-float(value)))}
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
