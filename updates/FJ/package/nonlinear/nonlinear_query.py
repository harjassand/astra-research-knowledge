"""Bounded, tangent-resummed correction sampling: reproducible research prototype.

Equation on the periodic interval [0, 2*pi):
    -u'' + u + 25*u**4 = 26 + 10*g(x),
    g(x) = .45*cos(x) + .30*cos(7*x) + .25*sin(13*x).

The two predictors are constructed without using the nonlinear reference solution.
The Monte Carlo sampler uses exact-in-law Brownian endpoints at exponential times
in the mathematical model; this implementation uses ordinary floating point.
No claim of historical novelty, interval-verified floating-point output, or
superiority over modern deterministic solvers is made.

Run: python nonlinear_query.py --samples 200000 --output results.json
Dependencies: numpy, numba. Numba compilation is excluded from query timing
and reported separately. The reference calculation is only a numerical check.
"""
from __future__ import annotations
import argparse
import json
import math
import time
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
from numba import njit


@dataclass(frozen=True)
class Certificate:
    predictor: int
    radius: float
    residual_bound: float
    tangent_lower: float
    proposal_rate: float
    b2: float
    b3: float
    b4: float
    envelope_slack: float
    nonlinear_slope: float
    offspring_bound: float
    expected_node_bound: float


def certificate(predictor: int, radius: float | None = None) -> Certificate:
    """Global analytic bounds; neither grid search nor a solved field is used."""
    if predictor == 0:
        h = .125 if radius is None else radius
        R, low, high, b2, b3, b4 = 10., 101., 101., 150., 100., 25.
    elif predictor == 1:
        h = .011 if radius is None else radius
        amp = 10. * (.45 / 102. + .30 / 150. + .25 / 270.)
        vlo, vhi = 1. - amp, 1. + amp
        R = 25. * (6. * amp**2 + 4. * amp**3 + amp**4)
        low, high = 1. + 100. * vlo**3, 1. + 100. * vhi**3
        b2, b3, b4 = 150. * vhi**2, 100. * vhi, 25.
    else:
        raise ValueError('predictor must be 0 or 1')
    if not math.isfinite(h) or h <= 0:
        raise ValueError('radius must be positive and finite')
    slack = low * h - R - (b2*h*h + b3*h**3 + b4*h**4)
    slope = 2.*b2*h + 3.*b3*h*h + 4.*b4*h**3
    if slack < 0 or slope >= low:
        raise ValueError(f'Certificate rejected: slack={slack:g}, slope={slope:g}, '
                         f'tangent_lower={low:g}')
    q = 1. - (low - slope) / high
    return Certificate(predictor,h,R,low,high,b2,b3,b4,slack,slope,q,1./(1.-q))


@njit
def base_and_residual(x: float, predictor: int):
    c1, c7, s13 = math.cos(x), math.cos(7.*x), math.sin(13.*x)
    if predictor == 0:
        return 1., 10.*(.45*c1 + .30*c7 + .25*s13)
    e0 = 10.*(.45*c1/102. + .30*c7/150. + .25*s13/270.)
    # The screened linear correction solves (-d_xx+101)*e0 = 10*g exactly.
    # Evaluating the algebraic remainder avoids cancellation of large terms.
    return 1.+e0, -25.*(6.*e0*e0 + 4.*e0**3 + e0**4)


@njit
def sample_corrections(x: float, n: int, seed: int, predictor: int,
                       h: float, R: float, rate: float,
                       B2: float, B3: float, B4: float):
    np.random.seed(seed)
    vals = np.empty(n)
    node_counts = np.empty(n, dtype=np.int64)
    p0 = R/(rate*h)
    p2, p3, p4 = B2*h/rate, B3*h*h/rate, B4*h**3/rate
    max_pending = 0
    for sample in range(n):
        pending = [x]
        weight, nodes = 1., 0
        while len(pending):
            if len(pending) > max_pending:
                max_pending = len(pending)
            xx = pending.pop()
            tau = np.random.exponential(1./rate)
            y = (xx + math.sqrt(2.*tau)*np.random.normal()) % (2.*math.pi)
            v, residual = base_and_residual(y, predictor)
            tangent = 1.+100.*v**3
            p1 = 1.-tangent/rate
            total = p0+p1+p2+p3+p4
            # Abort rather than clip or silently condition on successful paths.
            if p1 < -1.e-12 or total > 1.+1.e-12:
                raise ValueError('Local sampling probabilities violate certificate')
            draw = np.random.random()
            nodes += 1
            if draw < p0:
                weight *= residual/R
            elif draw < p0+p1:
                pending.append(y)
            elif draw < p0+p1+p2:
                weight *= -(150.*v*v)/B2
                pending.append(y); pending.append(y)
            elif draw < p0+p1+p2+p3:
                weight *= -(100.*v)/B3
                pending.append(y); pending.append(y); pending.append(y)
            elif draw < total:
                weight *= -25./B4
                for _ in range(4):
                    pending.append(y)
            else:
                weight = 0.
                break  # a zero factor annihilates the whole product
        vals[sample] = h*weight
        node_counts[sample] = nodes
    return vals, node_counts, max_pending


def spectral_reference(xq: float, n: int):
    """Full-field FFT fixed-point baseline and non-validated numerical reference."""
    x = 2.*np.pi*np.arange(n)/n
    k = np.fft.fftfreq(n, d=1./n)
    r = 10.*(.45*np.cos(x)+.30*np.cos(7.*x)+.25*np.sin(13.*x))
    e = np.zeros(n)
    start = time.perf_counter()
    for iteration in range(1,2001):
        nonlin = 150.*e**2+100.*e**3+25.*e**4
        new = np.fft.ifft(np.fft.fft(r-nonlin)/(101.+k*k)).real
        difference = float(np.max(np.abs(new-e)))
        e = new
        if difference < 2.e-15:
            break
    else:
        raise RuntimeError('Reference solver failed to converge')
    coefficients = np.fft.fft(e)/n
    value = 1.+float(np.real(np.sum(coefficients*np.exp(1j*k*xq))))
    duration = time.perf_counter()-start
    lap = np.fft.ifft(-(k*k)*np.fft.fft(e)).real
    residual = -lap+101.*e+150.*e**2+100.*e**3+25.*e**4-r
    return {'grid':n, 'value':value, 'iterations':iteration,
            'seconds':duration, 'collocation_residual_sup':float(np.max(np.abs(residual))),
            'last_iteration_difference':difference}


def run(samples: int = 200000) -> dict:
    if samples < 2:
        raise ValueError('at least two samples required')
    xq=.5
    c0=certificate(0)
    compile_start=time.perf_counter()
    sample_corrections(xq,1,123,c0.predictor,c0.radius,c0.residual_bound,
                       c0.proposal_rate,c0.b2,c0.b3,c0.b4)
    compile_seconds=time.perf_counter()-compile_start
    refs=[spectral_reference(xq,n) for n in (256,512,1024,2048)]
    reference=refs[-1]['value']
    results=[]
    for mode in (0,1):
        c=certificate(mode)
        start=time.perf_counter()
        vals,nodes,pending=sample_corrections(
            xq,samples,20261014+mode,c.predictor,c.radius,c.residual_bound,
            c.proposal_rate,c.b2,c.b3,c.b4)
        seconds=time.perf_counter()-start
        v,_=base_and_residual(xq,mode)
        estimate=v+float(np.mean(vals))
        variance=float(np.var(vals,ddof=1))
        # Valid for ideal iid samples with the proved range [-h,h].
        half_width=c.radius*math.sqrt(2.*math.log(2./.05)/samples)
        assert np.max(np.abs(vals)) <= c.radius*(1.+1.e-12)
        results.append({'certificate':asdict(c),'samples':samples,
                        'predictor_at_query':v,'estimate':estimate,
                        'error_vs_numerical_reference':estimate-reference,
                        'sample_variance':variance,'standard_error':math.sqrt(variance/samples),
                        'hoeffding_95_half_width_ideal_arithmetic':half_width,
                        'mean_nodes':float(np.mean(nodes)),'max_nodes':int(np.max(nodes)),
                        'max_pending':int(pending),'query_seconds_excluding_compilation':seconds,
                        'within_hoeffding_interval_vs_reference':abs(estimate-reference)<=half_width})
    rejected=[]
    for h in (.05,.30):
        try:
            certificate(0,h)
            rejected.append({'radius':h,'rejected':False})
        except ValueError as exc:
            rejected.append({'radius':h,'rejected':True,'reason':str(exc)})
    return {'equation':'-u_xx + u + 25u^4 = 26 + 10(.45cos x + .30cos 7x + .25sin 13x)',
            'domain':'periodic [0,2pi)', 'query':xq,
            'seed_base':20261014, 'compilation_seconds':compile_seconds,
            'reference_is_interval_verified':False,'spectral_references':refs,
            'results':results,'negative_tests':rejected,
            'limitations':['synthetic scalar model; not an engineering validation',
                           'theory uses exact arithmetic and exact random draws',
                           'FFT baseline is substantially faster in this one-dimensional example',
                           'prior-art novelty and stronger-baseline superiority are not established']}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--samples',type=int,default=200000)
    parser.add_argument('--output',type=Path,default=Path('results.json'))
    args=parser.parse_args()
    result=run(args.samples)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
