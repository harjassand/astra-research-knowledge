#!/usr/bin/env python3
"""Independent diagnostic implementation of the composed observation channel.

Exact Fractions verify supplied source and hard-cap certificates. Sampling and
the optional FFT comparator use floats: this is NOT a continuous-TV validated
executable. The theorem concerns exact-real primitives / a suitably certified
rounded implementation. No supplied scientific code is imported.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import math
import platform
import time

import numpy as np


def ceiling(x):
    return -(-x.numerator // x.denominator)


def min_power(base, target):
    """Smallest n>=0 with rational base**n>=target, without logarithms."""
    assert base > 1 and target > 0
    lo, hi = 0, 1
    while base**hi < target:
        hi *= 2
    while lo < hi:
        mid = (lo + hi) // 2
        if base**mid >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo


def certificates(r, sigma, epsilon):
    h = F(1, 8)
    V = F(101)
    Rsource = F(10)
    psource = Rsource / (V * h)
    branches = {2: F(150) * h / V, 3: F(100) * h**2 / V, 4: F(25) * h**3 / V}
    p0 = 1 - sum(branches.values())
    q = sum(k * p for k, p in branches.items())
    assert p0 >= psource and q == F(5425, 12928) < 1
    assert Rsource + F(150)*h**2 + F(100)*h**3 + F(25)*h**4 <= V*h
    s = F(3, 2)
    fs = p0 + sum(p * s**k for k, p in branches.items())
    assert fs == F(1051417, 827392)
    z = s / fs
    assert z == F(1241088, 1051417) > 1
    # Independent exact nonuniform PGF certificate.
    tA, tB, z2 = F(11, 10), F(28, 25), F(352, 351)
    fA = F(3, 8) + F(5, 16)*tA + F(5, 16)*tA*tA
    fB = F(1, 4) + F(3, 8)*tA + F(3, 8)*tA*tA
    assert z2*fA <= tA and z2*fB <= tB

    radius2 = r*h*h/(sigma*sigma)
    eg = epsilon/2
    delta = epsilon/2
    # Exact sufficient m: e^-x <= 2^-floor(x), with m=ceil(8R²*j).
    j = 1
    while True:
        m = max(1, ceiling(8*radius2*j))
        clipping_bound = F(10*m, 2**j)
        if clipping_bound <= eg:
            break
        j += 1
    assert m >= radius2 and F(m, 1)/(8*radius2) >= j
    K = min_power(F(8, 7), F(3*m, 1)/delta)
    B0 = m*K
    Jcap = min_power(F(2), F(24*B0, 1)/delta)
    B = B0*Jcap*r
    ncap = min_power(z, F(3*B, 1)*s/delta)
    assert m*F(7, 8)**K <= delta/3
    assert B0*F(8, 2**Jcap) <= delta/3
    assert B*s*z**(-ncap) <= delta/3
    return dict(h=h, psource=psource, branches=branches, q=q, s=s, z=z,
                radius2=radius2, m=m, K=K, Jcap=Jcap, B=B, ncap=ncap,
                exact_clipping_bound=clipping_bound, epsilon_g=eg, delta=delta)


class CapReached(Exception):
    def __init__(self, reason, completed_nodes=0):
        super().__init__(reason)
        self.completed_nodes = completed_nodes


def correction(x, rng, c):
    """DFS product tree with an explicit stack and a deterministic node cap."""
    stack = []
    nodes = 0
    current = x
    while True:
        nodes += 1
        if nodes > c['ncap']:
            raise CapReached('coordinate_tree', nodes-1)
        y = (current + math.sqrt(2*rng.exponential(1/101))*rng.normal()) % (2*math.pi)
        u = rng.random()
        if u < float(c['psource']):
            val = .45*math.cos(y) + .30*math.cos(7*y) + .25*math.sin(13*y)
            assert abs(val) <= 1
        else:
            degree = 0
            threshold = float(c['psource'])
            for k, p in c['branches'].items():
                threshold += float(p)
                if u < threshold:
                    degree = k
                    break
            if degree:
                stack.append([y, degree-1, 1.0])
                current = y
                continue
            val = 0.0
        while stack:
            frame = stack[-1]
            frame[2] *= val
            if frame[1] == 0 or val == 0:
                val = -frame[2]
                stack.pop()
            else:
                frame[1] -= 1
                current = frame[0]
                break
        else:
            assert abs(val) <= 1
            return float(c['h'])*val, nodes


def capped_poisson(rng, cap):
    u = rng.random()
    p = math.exp(-2)
    cumulative = p
    for j in range(cap+1):
        if u <= cumulative:
            return j
        p *= 2/(j+1)
        cumulative += p
    raise CapReached('Poisson_degree')


def channel(xs, sigma, rng, c):
    out = np.zeros(len(xs))
    calls = nodes = attempts = 0
    try:
        for factor in range(c['m']):
            for trial in range(c['K']):
                attempts += 1
                y = rng.normal(size=len(xs))/math.sqrt(c['m'])
                degree = capped_poisson(rng, c['Jcap'])
                accept = 1.0
                for unused in range(degree):
                    vec = []
                    calls += 1
                    for x in xs:
                        v, work = correction(x, rng, c)
                        nodes += work
                        vec.append(v/sigma)
                    accept *= (1+max(-1.0, min(1.0, float(y @ np.asarray(vec)))))/2
                if rng.random() <= accept:
                    out += y
                    break
            else:
                raise CapReached('factor_proposals')
        assert nodes <= c['B']*c['ncap']
        return 1+sigma*out, dict(calls=calls, nodes=nodes, attempts=attempts, abort=None)
    except CapReached as e:
        nodes += e.completed_nodes
        assert nodes <= c['B']*c['ncap']
        return np.ones(len(xs)), dict(calls=calls, nodes=nodes, attempts=attempts, abort=str(e))


def self_tests(c):
    class ForcedRNG:
        def __init__(self):
            self.values = iter([.80, .10, .10])
        def exponential(self, scale):
            return 0.0
        def normal(self):
            return 0.0
        def random(self):
            return next(self.values)
    # A degree-two root needs three nodes. A two-node cap must retain its cost.
    short = dict(c, ncap=2)
    try:
        correction(0.0, ForcedRNG(), short)
        raise AssertionError('Expected tree cap')
    except CapReached as e:
        assert e.completed_nodes == 2 and str(e) == 'coordinate_tree'
    val, nodes = correction(0.0, ForcedRNG(), dict(c, ncap=3))
    assert nodes == 3 and abs(val) <= float(c['h'])
    assert min_power(F(8, 7), F(64, 49)) == 2
    return ['exact polynomial enclosure and offspring probabilities',
            'exact uniform and nonuniform PGF moment certificates',
            'exact rational clipping/proposal/Poisson/tree cap budgets',
            'forced tree abort preserves all completed node costs',
            'forced complete product tree retains bounded output']


def fft_diagnostic(xs, n):
    grid = 2*math.pi*np.arange(n)/n
    freq = np.fft.fftfreq(n, 1/n)
    forcing = 10*(.45*np.cos(grid)+.30*np.cos(7*grid)+.25*np.sin(13*grid))
    e = np.zeros(n)
    for steps in range(300):
        rhs = forcing - 150*e*e - 100*e**3 - 25*e**4
        new = np.fft.ifft(np.fft.fft(rhs)/(freq*freq+101)).real
        if np.max(np.abs(new-e)) < 2e-15:
            e = new
            break
        e = new
    coefficients = np.fft.fft(e)/n
    return [float(1+np.sum(coefficients*np.exp(1j*freq*x)).real) for x in xs]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--outputs', type=int, default=800)
    ap.add_argument('--seed', type=int, default=144281)
    ap.add_argument('--sigma', default='1/4')
    ap.add_argument('--epsilon', default='1/20')
    ap.add_argument('--output-dir', type=Path, required=True)
    a = ap.parse_args()
    assert a.outputs > 1
    sigma, epsilon = F(a.sigma), F(a.epsilon)
    assert sigma > 0 and 0 < epsilon < 1
    xs = [.5, 1.25]
    c = certificates(len(xs), sigma, epsilon)
    checked = self_tests(c)
    rng = np.random.default_rng(a.seed)
    start = time.monotonic()
    samples = []
    work = []
    for unused in range(a.outputs):
        value, receipt = channel(xs, float(sigma), rng, c)
        samples.append(value)
        work.append(receipt)
    samples = np.asarray(samples)
    reference128 = fft_diagnostic(xs, 128)
    reference256 = fft_diagnostic(xs, 256)
    report = dict(status='PASS_EXACT_CERTIFICATES_AND_FLOAT_DIAGNOSTIC',
        python=platform.python_version(), numpy=np.__version__, seconds=time.monotonic()-start,
        model='-u"+u+25u^4=26+10(.45cosx+.30cos7x+.25sin13x), periodic; v=1,h=1/8',
        points=xs, observation_sigma=str(sigma), ideal_law_epsilon=str(epsilon), outputs=a.outputs, seed=a.seed,
        checks=checked,
        exact_certificate={k: str(v) if isinstance(v, F) else v for k, v in c.items() if k != 'branches'},
        expected_vector_acquisitions_bound=2*math.e**2*c['m'],
        expected_PDE_nodes_bound=2*math.e**2*c['m']*len(xs)/float(1-c['q']),
        every_execution_PDE_node_cap=c['B']*c['ncap'],
        observed=dict(vector_acquisitions=sum(x['calls'] for x in work), nodes=sum(x['nodes'] for x in work),
            proposals=sum(x['attempts'] for x in work), aborts=sum(x['abort'] is not None for x in work),
            max_nodes_per_output=max(x['nodes'] for x in work), mean=samples.mean(axis=0).tolist(),
            covariance=np.cov(samples, rowvar=False).tolist()),
        FFT_reference=dict(n128=reference128, n256=reference256,
            scope='Independent discretized fixed-point diagnostic, not interval-validated solution or full-law certificate.'),
        scope='Fractions verify enclosure, offspring/PGF, rational outer cap and total ideal TV-budget inequalities. '
              'Float sampling/FFT moments are diagnostic only, not continuous-TV validation, physical evidence or superiority. '
              'Known FORS/Gaussian factory is composed with the supplied bounded PDE oracle; no new generic sampler claimed.')
    a.output_dir.mkdir(parents=True, exist_ok=True)
    (a.output_dir/'OBSERVATION_CHANNEL_RESULTS.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], m=c['m'], cap=c['B']*c['ncap'],
        outputs=a.outputs, nodes=report['observed']['nodes'], aborts=report['observed']['aborts'],
        mean=report['observed']['mean'], reference=reference256, seconds=report['seconds'])))


if __name__ == '__main__':
    main()
