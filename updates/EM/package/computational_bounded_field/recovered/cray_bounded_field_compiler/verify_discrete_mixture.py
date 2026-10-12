#!/usr/bin/env python3
"""Small rank-one test of the rejection-free bounded-field mixture.

This deliberately enumerates the base spins and uses non-certified mpmath
Gaussian interval arithmetic. It verifies complete output probabilities on
small fixtures, not the general polynomial implementation.
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
import time
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
from verify_compiler import Cell, to_mp, mp_logsum, log_normal_interval


def ceil_log2_rational(x: F) -> int:
    if x <= 0:
        raise ValueError('logarithm input must be positive')
    k = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    while F(2) ** k < x:
        k += 1
    while k > 0 and F(2) ** (k - 1) >= x:
        k -= 1
    return k


def compile_cells(a: list[F], h: list[F], j0: list[list[F]], eps: F):
    n = len(a)
    if not 0 < eps < 1:
        raise ValueError('eps must lie in (0,1)')
    spins = list(itertools.product((-1, 1), repeat=n))
    energies = [sum(j0[i][j] * x[i] * x[j] for i in range(n) for j in range(n))/2 for x in spins]
    R = max(sum(abs(j0[i][j]) for j in range(n) if j != i) for i in range(n))
    L = math.ceil(R) + ceil_log2_rational(F(8*n)/eps)
    intervals = math.ceil(F(16*n*L)/eps)
    step = F(2*L, intervals)
    knots = [F(-L) + k*step for k in range(intervals+1)]
    endpoints = sorted({(t-h[i])/a[i] for i in range(n) if a[i] for t in knots})
    bounds = [None, *endpoints, None]
    cells = []
    spin_log_base = []
    for left,right in zip(bounds[:-1], bounds[1:]):
        y = right-1 if left is None else (left+1 if right is None else (left+right)/2)
        c=[]; d=F(0); e=F(0)
        for ai,hi in zip(a,h):
            ell=hi+ai*y
            if ell >= L:
                c.append(F(L)); d+=ai; e+=hi-L
            elif ell <= -L:
                c.append(F(-L)); d-=ai; e+=-hi-L
            else:
                k=(ell+L)//step
                c.append(F(-L)+(F(k)+F(1,2))*step)
        logs=[to_mp(en+sum(ci*xi for ci,xi in zip(c,x))) for en,x in zip(energies,spins)]
        z=mp_logsum(logs)
        cells.append(Cell(left,right,c,d,e,z))
        spin_log_base.append(logs)
    return spins,energies,cells,spin_log_base,L,R


def mass_and_output_test(a,h,j0,eps,variance,prepared):
    spins,energies,cells,spin_log_base,L,R = prepared
    k=to_mp(variance); rootk=mp.sqrt(k)
    log_g=[]; weights=[]
    for cell in cells:
        d=to_mp(cell.d); e=to_mp(cell.e); mean=k*d
        lo=-mp.inf if cell.left is None else (to_mp(cell.left)-mean)/rootk
        hi=mp.inf if cell.right is None else (to_mp(cell.right)-mean)/rootk
        g=e+k*d*d/2+mp.log(2*mp.pi*k)/2+log_normal_interval(lo,hi)
        log_g.append(g); weights.append(g+cell.log_z_base)
    log_q=mp_logsum(weights)
    proposed=[]
    for j in range(len(spins)):
        proposed.append(mp.exp(mp_logsum([g+logs[j] for g,logs in zip(log_g,spin_log_base)])-log_q))
    target_logs=[]
    for en,x in zip(energies,spins):
        proj=sum(ai*xi for ai,xi in zip(a,x))
        target_logs.append(to_mp(en+variance*proj*proj/2+sum(hi*xi for hi,xi in zip(h,x))))
    log_z=mp_logsum(target_logs)
    target=[mp.exp(z-log_z) for z in target_logs]
    tv=mp.fsum(abs(p-q) for p,q in zip(proposed,target))/2
    estimate=log_q-mp.log(2*mp.pi*k)/2
    error=estimate-log_z
    b=to_mp(eps)/16
    rho=len(a)*mp.exp(-2*(L-to_mp(R)))
    tv_bound=1-(1-rho)*mp.exp(-2*b)
    log_bound=b-mp.log(1-rho)
    assert tv <= tv_bound+mp.mpf('1e-35')
    assert abs(error) <= log_bound+mp.mpf('1e-35')
    assert tv <= to_mp(eps)/4+mp.mpf('1e-35')
    return {'variance_rational':str(variance),'epsilon_rational':str(eps),
            'n':len(a),'cells':len(cells),'L':L,
            'exact_small_system_log_Z':mp.nstr(log_z,30),
            'mixture_TV_error':mp.nstr(tv,24),
            'proved_ideal_TV_bound':mp.nstr(tv_bound,24),
            'signed_log_Z_error':mp.nstr(error,24),
            'proved_absolute_log_Z_error_bound':mp.nstr(log_bound,24),
            'output_probability_sum_error':mp.nstr(abs(mp.fsum(proposed)-1),10)}


def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,default=Path('mixture_results.json'))
    args=p.parse_args(); mp.mp.dps=90; start=time.perf_counter()
    a=[F(1),F(-2,3),F(5,7)]; h=[F(2,5),F(-1,3),F(3,8)]
    v=[F(1),F(-1),F(2)]; j0=[[vi*vj/20 for vj in v] for vi in v]
    eps=F(1,4); prepared=compile_cells(a,h,j0,eps)
    cases=[mass_and_output_test(a,h,j0,eps,k,prepared) for k in [F(1,2**30),F(1),F(2**30)]]
    result={'status':'finite_complete_output_checks_passed_not_general_validation',
            'precision_decimal_digits':mp.mp.dps,'cases':cases,
            'elapsed_seconds':time.perf_counter()-start,
            'limitations':['Exhaustive small base state enumeration.','No generic convex-volume FPRAS implemented.',
                           'mpmath interval masses are not certified interval arithmetic.',
                           'No comparison with optimised specialised algorithms.']}
    args.output.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))

if __name__=='__main__': main()
