"""All-order killed BARW reference sampler and shared exact score functions.

Target: w_i=(1-L*R/3)/2 * (1-gamma*s_i*(L+R)/2),
gamma=(n*n-1)/(n*n+1), on a periodic n-site Ising chain.
No cutoff in particle number, perturbative order, excursion length or radius.

Integer h-transform sampling pays for the true transformed path length.
Static endpoint scores are enclosed by outward dyadic arithmetic.
The old standalone run() is exploratory: its original confidence calculation
was superseded after audit. Use certify_all_order.py or stream_response.py
for the corrected four-tail exact rational confidence calculation. The exact
score and interval functions in this file are shared by those final backends.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import time
from fractions import Fraction as F
from pathlib import Path


def potential_num(s, n):
    """h(S)=this integer/n; linear work in the odd particle count."""
    if len(s) == 1:
        return 0
    gaps = [s[i+1]-s[i] for i in range(len(s)-1)] + [n+s[0]-s[-1]]
    pref = [0, 0]
    pairs = [[0, 0], [0, 0]]
    answer = 0
    for k, g in enumerate(gaps):
        p = k & 1
        answer += g*pairs[p][1-p]
        for q in (0, 1):
            pairs[q][p] += pref[q]*g
        pref[p] += g
    return answer


def toggled(s, a, b):
    t = set(s)
    t.symmetric_difference_update((a, b))
    return tuple(sorted(t))


class Dyadic:
    """Positive interval arithmetic; integer units are 2**(-bits)."""
    def __init__(self, bits):
        self.bits = bits
        self.scale = 1 << bits

    def frac(self, x):
        q, r = divmod(x.numerator*self.scale, x.denominator)
        return q, q+(r != 0)

    def mul(self, x, y):
        lo = x[0]*y[0]//self.scale
        hi = (x[1]*y[1]+self.scale-1)//self.scale
        return lo, hi

    def div(self, x, y):
        assert y[0] > 0 and x[0] >= 0
        return (x[0]*self.scale//y[1],
                (x[1]*self.scale+y[0]-1)//y[0])

    def power(self, x, k):
        out = (self.scale, self.scale)
        while k:
            if k & 1:
                out = self.mul(out, x)
            k >>= 1
            if k:
                x = self.mul(x, x)
        return out


def alpha_interval(s, n, bits=100):
    """Cov(M, spin_product(S))/Cov(M,sigma_0), with positive gap sums."""
    d = Dyadic(bits)
    z = d.scale
    t = d.frac(F(n-1, n+1))
    gaps = [s[i+1]-s[i] for i in range(len(s)-1)] + [n+s[0]-s[-1]]
    # At the first spin, alternate complementary arcs; see proof note.
    exponent = sum(gaps[j] for j in range(1, len(gaps), 2))
    sums = [0, 0]
    cache = {}
    def power(k):
        if k not in cache:
            cache[k] = d.power(t, k)
        return cache[k]
    for j, gap in enumerate(gaps):
        slope = 1 if j % 2 == 0 else -1
        lo_e = min(exponent, exponent+slope*(gap-1))
        hi_e = max(exponent, exponent+slope*(gap-1))
        p, q, r = power(lo_e), power(n-hi_e), power(gap)
        term = d.mul((p[0]+q[0], p[1]+q[1]), (z-r[1], z-r[0]))
        sums[0] += term[0]
        sums[1] += term[1]
        exponent += slope*gap
    tn = power(n)
    denominator = d.mul((z+t[0], z+t[1]), (z-tn[1], z-tn[0]))
    ans = d.div(tuple(sums), denominator)
    return max(0, ans[0]), min(z, ans[1]), z


def excursion(n, rng):
    """One exact h-transformed path. Return terminal state and actual work."""
    s = (0, 1, 2)
    h = n-2
    rate_den = 3*(n*n+1)
    events = 0
    max_particles = 3
    h_evaluations = 0
    while True:
        count = len(s)
        # Full killed dual diagonal is N. Includes the killing channel.
        denominator = count*rate_den*h
        x = rng.randrange(denominator)
        events += 1
        destination = None
        for i in s:
            left, right = (i-1) % n, (i+1) % n
            for u, v, rate_num in ((i, left, n*n-1),
                                    (i, right, n*n-1),
                                    (left, right, n*n+1)):
                nxt = toggled(s, u, v)
                hn = potential_num(nxt, n)
                h_evaluations += 1
                weight = rate_num*hn
                if x < weight:
                    destination, new_h = nxt, hn
                    break
                x -= weight
            if destination is not None:
                break
        if destination is None:
            return s, h, events, max_particles, h_evaluations
        s, h = destination, new_h
        max_particles = max(max_particles, len(s))


def scores(n, s, hnum, bits=100):
    a = F(n*n-1, 3*(n*n+1))
    b = F(1, 3)
    kappa = F(4, 3*(n*n+1))
    a0, c0 = a+2*b/n, a+b
    theta0, h0 = a0/c0, F(n-2, n)
    number = len(s)
    h = F(hnum, n)
    hh = a0*number-c0+kappa*number*h
    u = h0*number/hh
    al, au, scale = alpha_interval(s, n, bits)
    rl, ru = h0*F(al, scale)/hh, h0*F(au, scale)/hh
    wl, wu = rl-theta0*u+h0/c0, ru-theta0*u+h0/c0
    assert wu >= 0
    wmax = h0/c0
    return u, max(F(0), wl), min(wmax, wu)


def dyadic_outer(x, bits):
    scale = 1 << bits
    q, r = divmod(x.numerator*scale, x.denominator)
    return q, q+(r != 0)


def bernstein(mean, variance, width, samples, failure):
    # Maurer-Pontil empirical Bernstein: unbiased sample variance.
    # A conservative 1e-12 relative/absolute upward allowance covers these
    # reported float64 elementary operations; exact sums are saved as well.
    log = math.log(2/failure)
    r = math.sqrt(2*variance*log/samples)+7*width*log/(3*(samples-1))
    return r+(1+abs(r))*1e-12


def run(n, samples, seed, failure=0.05, bits=100):
    assert n >= 4 and samples >= 2
    started = time.perf_counter()
    rng = random.Random(seed)
    b = F(1, 3)
    a = F(n*n-1, 3*(n*n+1))
    a0, c0 = a+2*b/n, a+b
    theta0, h0 = a0/c0, F(n-2, n)
    c = (2*a-b+6*b/n)/3
    umax, wmax = h0/c, h0/c0
    # Exact sums of dyadic lower/upper score brackets and midpoint squares.
    sums = {q: 0 for q in ('ul', 'uu', 'wl', 'wu', 'u2', 'w2')}
    scale = 1 << bits
    total_events = max_events = max_particles = total_h_evaluations = 0
    for sample in range(samples):
        s, hn, ev, particles, he = excursion(n, rng)
        u, wl, wu = scores(n, s, hn, bits)
        ul, uu = dyadic_outer(u, bits)
        wli, _ = dyadic_outer(wl, bits)
        _, wui = dyadic_outer(wu, bits)
        sums['ul'] += ul; sums['uu'] += uu
        sums['wl'] += wli; sums['wu'] += wui
        # Midpoint data has twice the dyadic scale.
        sums['u2'] += (ul+uu)**2
        sums['w2'] += (wli+wui)**2
        total_events += ev
        total_h_evaluations += he
        max_events = max(max_events, ev)
        max_particles = max(max_particles, particles)
    means, variances, score_radii = {}, {}, {}
    for key in ('u', 'w'):
        total = sums[key+'l']+sums[key+'u']
        means[key] = float(F(total, 2*scale*samples))
        # Exact unbiased sample variance for the midpoint scores.
        var = F(samples*sums[key+'2']-total*total,
                4*scale*scale*samples*(samples-1))
        variances[key] = float(var)
        score_radii[key] = float(F(sums[key+'u']-sums[key+'l'], 2*scale*samples))
    urad = bernstein(means['u'], variances['u'], float(umax), samples, failure/2)+score_radii['u']
    wrad = bernstein(means['w'], variances['w'], float(wmax), samples, failure/2)+score_radii['w']
    ul, uu = max(0.0, means['u']-urad), min(float(umax), means['u']+urad)
    wl, wu = max(0.0, means['w']-wrad), min(float(wmax), means['w']+wrad)
    # theta = kappa*chi/Var(M), ratio uncertainty propagated monotonically.
    lower = float(theta0)+float(b)*wl/(1+float(b)*uu)-1e-12
    upper = float(theta0)+float(b)*wu/(1+float(b)*ul)+1e-12
    point = float(theta0)+float(b)*means['w']/(1+float(b)*means['u'])
    # A conservative proved hmax <= n^2/6 and E int N <= h0/c.
    u0=F((n-2)*(n-1),6*n)
    expected_event_bound=3*u0/(2*a*h0)*(1+b*h0/c)
    result = {
        'n': n, 'samples': samples, 'seed': seed,
        'confidence_at_least': None,
        'status': 'Exploratory legacy confidence; use certify_all_order.py for an authoritative interval.',
        'theta_definition': 'kappa * chi_M / Var(M), kappa=4/(3*(n*n+1))',
        'theta_interval': [lower, upper], 'theta_point': point,
        'relative_interval_width': (upper-lower)/lower,
        'theta0': float(theta0),
        'mean_U': means['u'], 'variance_U': variances['u'],
        'mean_W': means['w'], 'variance_W': variances['w'],
        'U_score_range': [0, float(umax)], 'W_score_range': [0, float(wmax)],
        'mean_events': total_events/samples, 'total_events': total_events,
        'max_events': max_events, 'max_active_particles': max_particles,
        'potential_evaluations': total_h_evaluations,
        'proved_expected_event_bound': float(expected_event_bound),
        'score_roundoff_radii': score_radii,
        'dyadic_bits': bits,
        'exact_dyadic_sums': {key: str(value) for key, value in sums.items()},
        'elapsed_seconds': time.perf_counter()-started,
        'limitations': [
            'This legacy standalone confidence calculation is diagnostic only.',
            'No particle/order/time/radius cutoff; work is actual transformed work.',
            'The separately proved all-order expected event bound is linear in n.',
            'Rounded displayed confidence endpoints include an explicit numerical allowance.'
        ]
    }
    print(json.dumps({k: v for k, v in result.items() if k != 'exact_dyadic_sums'}), flush=True)
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--n', type=int, default=64)
    p.add_argument('--samples', type=int, default=2000)
    p.add_argument('--seed', type=int, default=20261101)
    p.add_argument('--output', type=str)
    args = p.parse_args()
    record = run(args.n, args.samples, args.seed)
    if args.output:
        Path(args.output).write_text(json.dumps(record, indent=2)+'\n')
