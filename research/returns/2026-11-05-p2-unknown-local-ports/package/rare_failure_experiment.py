"""Synthetic intervention experiment for a local reciprocal collision register.

This is a model calculation, not a physical experiment. Multinomial counts are
drawn directly; the number of represented trials is not the number of PRNG calls.
The general all-terminal Karger algorithm is not implemented here.
Dependencies: Python 3, NumPy, SciPy, Matplotlib.
"""
from __future__ import annotations

import itertools
import json
import math
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.linalg import eigh

OUT = Path(__file__).resolve().parent


def bit(x, i):
    return (x >> i) & 1


def local(x, sites):
    return sum(bit(x, i) << j for j, i in enumerate(sites))


def replace(x, sites, u):
    for j, i in enumerate(sites):
        x = (x & ~(1 << i)) | (bit(u, j) << i)
    return x


def connected(x, edges, vertices):
    reached = {0}
    while True:
        old = len(reached)
        for i, (a, b) in enumerate(edges):
            if not bit(x, i) and (a in reached or b in reached):
                reached.update((a, b))
        if len(reached) == old:
            return len(reached) == vertices


def stationary(m, p):
    return [p ** x.bit_count() * (1-p) ** (m-x.bit_count())
            for x in range(1 << m)]


def pair_exchange_rates(k, p, attempt, exchange):
    """One reciprocal pulse exchanging all k paired occupations together.

    Independent Bernoulli-p ancilla bits produce upward probability s*p**k
    and downward probability s*(1-p)**k. All other input rows are unchanged.
    """
    d = 1 << k
    rates = [[Fraction(0) for _ in range(d)] for _ in range(d)]
    rates[0][-1] = attempt * exchange * p**k
    rates[-1][0] = attempt * exchange * (1-p)**k
    return rates


def acquire(rates, p, attempt, n, log_budget, rng):
    d = len(rates)
    k = d.bit_length()-1
    weights = stationary(k, p)
    counts = []
    for u in range(d):
        probs = np.array([float(rates[u][v]/attempt) for v in range(d)])
        probs[u] = max(0., 1-float(probs.sum()))
        probs /= probs.sum()
        counts.append(rng.multinomial(n, probs).tolist())
    fitted = [[Fraction(0) for _ in range(d)] for _ in range(d)]
    radii = np.zeros((d, d))
    intervals = []
    # Hoeffding plus an additional zero-count upper bound. Union bound uses
    # 3*J*exp(-log_budget) <= alpha over J unordered local endpoint pairs.
    radius = math.sqrt(log_budget/(2*n))
    for u in range(d):
        for v in range(u+1, d):
            hi, lo = (u, v) if weights[u] <= weights[v] else (v, u)
            estimate = Fraction(counts[hi][lo], n)
            ef = float(estimate)
            low = max(0., ef-radius)
            high = min(1., ef+radius)
            if counts[hi][lo] == 0:
                high = min(high, log_budget/n)
            # These outward numerical margins exceed ordinary roundoff; this
            # program is numerical evidence, not a directed-arithmetic proof.
            low = max(0., low-1e-13)
            high = min(1., high+1e-13)
            fitted[hi][lo] = attempt*estimate
            fitted[lo][hi] = fitted[hi][lo]*weights[hi]/weights[lo]
            width = float(attempt)*max(ef-low, high-ef)
            radii[hi, lo] = width
            radii[lo, hi] = width*float(weights[hi]/weights[lo])
            intervals.append(dict(source=hi, destination=lo,
                count=counts[hi][lo], trials=n,
                probability_estimate=ef, probability_low=low,
                probability_high=high))
    return fitted, dict(counts=counts, intervals=intervals,
        maximum_error_exit=float(radii.sum(axis=1).max()),
        represented_trials=d*n, downhill_hoeffding_radius=radius)


def generator(m, p, gamma, blocks, local_rates):
    d = 1 << m
    q = [[Fraction(0) for _ in range(d)] for _ in range(d)]
    for x in range(d):
        for i in range(m):
            q[x][x ^ (1 << i)] += gamma*(1-p if bit(x, i) else p)
        for sites, rates in zip(blocks, local_rates):
            u = local(x, sites)
            for v in range(1 << len(sites)):
                if v != u and rates[u][v]:
                    q[x][replace(x, sites, v)] += rates[u][v]
        q[x][x] = -sum(q[x])
    return q


def decimal_number(x):
    return Decimal(x.numerator)/Decimal(x.denominator)


def solve_mean(q, safe, precision):
    with localcontext() as ctx:
        ctx.prec = precision
        a = [[-decimal_number(q[x][y]) for y in safe]+[Decimal(1)]
             for x in safe]
        size = len(safe)
        for col in range(size):
            pivot = max(range(col, size), key=lambda row: abs(a[row][col]))
            a[col], a[pivot] = a[pivot], a[col]
            piv = a[col][col]
            if not piv:
                raise ArithmeticError('Singular killed generator')
            for row in range(col+1, size):
                if not a[row][col]:
                    continue
                ratio = a[row][col]/piv
                a[row][col] = Decimal(0)
                for j in range(col+1, size+1):
                    a[row][j] -= ratio*a[col][j]
        solution = [Decimal(0)]*size
        for row in reversed(range(size)):
            solution[row] = (a[row][-1]-sum(a[row][j]*solution[j]
                             for j in range(row+1, size)))/a[row][row]
        return +solution[safe.index(0)]


def form_diagnostic(q, fitted, baseline, pi):
    pi_f = np.array([float(x) for x in pi])
    s = np.sqrt(pi_f)
    def symmetric_minus_q(x):
        a = -np.array([[float(z) for z in row] for row in x])
        a = s[:, None]*a/s[None, :]
        return (a+a.T)/2
    v = s.copy()
    v[0] -= 1
    householder = np.eye(len(s))-2*np.outer(v, v)/np.dot(v, v)
    b = householder[:, 1:]
    h0 = b.T@symmetric_minus_q(baseline)@b
    diff = b.T@(symmetric_minus_q(q)-symmetric_minus_q(fitted))@b
    eigenvalues = eigh(diff, h0, eigvals_only=True)
    return float(np.max(np.abs(eigenvalues)))


def run_case(name, edges, vertices, blocks, p, n, seed, alpha=.01):
    m = len(edges)
    gamma, attempt, exchange = Fraction(1), Fraction(4), Fraction(1,2)
    rng = np.random.default_rng(seed)
    pairs = sum((1 << len(s))*((1 << len(s))-1)//2 for s in blocks)
    log_budget = math.log(3*pairs/alpha)+1e-9
    true_rates = [pair_exchange_rates(len(s), p, attempt, exchange) for s in blocks]
    fitted_rates, acquisitions = [], []
    for rates in true_rates:
        f, a = acquire(rates, p, attempt, n, log_budget, rng)
        fitted_rates.append(f)
        acquisitions.append(a)
    true_q = generator(m, p, gamma, blocks, true_rates)
    fitted_q = generator(m, p, gamma, blocks, fitted_rates)
    baseline_q = generator(m, p, gamma, [], [])
    pi = stationary(m, p)
    safe = [x for x in range(1 << m) if connected(x, edges, vertices)]
    p_fail = sum(pi[x] for x in range(1 << m) if x not in safe)
    per_site = [2*sum(a['maximum_error_exit'] for sites, a in zip(blocks, acquisitions)
                     if i in sites)/float(gamma) for i in range(m)]
    rho = max(per_site)
    if rho >= 1:
        raise ArithmeticError('Acquisition insufficient for form certificate')
    means = {}
    for label, q in [('true',true_q), ('fitted',fitted_q), ('independent_only',baseline_q)]:
        value = solve_mean(q, safe, 90)
        check = solve_mean(q, safe, 125)
        discrepancy = abs((value-check)/check)
        if discrepancy > Decimal('1e-65'):
            raise ArithmeticError('Precision check failed')
        means[label] = str(check)
    # Uniformization bound valid for both the true and fitted model.
    fitted_port_caps = [max(sum(row) for row in rates) for rates in fitted_rates]
    uniform_rate = 2*(m*gamma+sum(max(attempt, cap) for cap in fitted_port_caps))
    kappa = float(pi[0])
    rare_ratio_upper = float(uniform_rate*p_fail/(1-p_fail)/gamma)
    if rare_ratio_upper <= kappa/16:
        condition_bound = 2/math.sqrt(kappa)
        branch = 'rare fixed-start resolvent bound'
    else:
        condition_bound = 4/(math.sqrt(float(gamma/uniform_rate))*kappa)
        branch = 'general fixed-start resolvent bound'
    zeta = condition_bound*rho/(1-rho)
    if zeta >= 1:
        raise ArithmeticError('Acquisition insufficient for mean certificate')
    with localcontext() as ctx:
        ctx.prec = 100
        fit_mean = Decimal(means['fitted'])
        z = Decimal(str(zeta))+Decimal('1e-12')
        lower, upper = fit_mean*(1-z), fit_mean*(1+z)
        true_m = Decimal(means['true'])
        mean_ratio = Decimal(means['independent_only'])/true_m
        inside = lower <= true_m <= upper
    form_actual = form_diagnostic(true_q, fitted_q, baseline_q, pi)
    result = dict(name=name, components=m, vertices=vertices,
        local_blocks=[list(s) for s in blocks], states=1 << m, safe_states=len(safe),
        p_numerator=p.numerator, p_denominator=p.denominator,
        native_refresh_rate=float(gamma), collision_attempt_rate=float(attempt),
        true_exchange_probability=float(exchange), alpha=alpha, seed=seed,
        trials_per_local_input=n,
        represented_collision_trials=sum(a['represented_trials'] for a in acquisitions),
        acquisitions=acquisitions,
        stationary_failure_probability=float(p_fail), initial_mass=kappa,
        uniformization_rate=float(uniform_rate),
        rare_eigenvalue_ratio_upper=rare_ratio_upper,
        form_error_bound=rho, actual_form_error_diagnostic=form_actual,
        fixed_start_condition_bound=condition_bound, relative_mean_radius=zeta,
        means=means, confidence_lower=str(lower), confidence_upper=str(upper),
        confidence_ratio=float(upper/lower), true_mean_in_interval=inside,
        independent_prediction_factor=float(mean_ratio), branch=branch,
        upward_cooperative_rate=float(true_rates[0][0][-1]),
        total_forward_cooperative_observations=sum(a['counts'][0][-1] for a in acquisitions),
        status='Synthetic multinomial data; numerical arithmetic diagnostics; no physical measurement')
    if not inside or form_actual > rho*(1+1e-6):
        raise AssertionError('Demonstration diagnostic failed')
    return result


def main():
    two = run_case('Two redundant components', [(0,1),(0,1)], 2,
                   [(0,1)], Fraction(1,2**40), 1_000_000, 20261105)
    edges = list(itertools.combinations(range(4), 2))
    stars = [tuple(i for i,e in enumerate(edges) if v in e) for v in range(4)]
    k4 = run_case('K4 with four unknown three-component ports', edges, 4,
                 stars, Fraction(1,2**20), 8_000_000, 20261106)
    # Independent exact analytic identity for the two-component operating model.
    with localcontext() as ctx:
        ctx.prec = 100
        p = Decimal(1)/(Decimal(2)**40)
        exact = (1+2*p)/(p*p*4)
        if abs((Decimal(two['means']['true'])-exact)/exact) > Decimal('1e-80'):
            raise AssertionError('Two-component analytic formula failed')
    data = dict(date='2026-11-05', cases=[two,k4],
        confidence_scope='Each case separately has a 99% ideal sampling guarantee; the two-case union is at least 98%.',
        executed='Direct multinomial count simulation and 90/125-digit killed-generator solves; no general Karger implementation')
    (OUT/'results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps([{k:c[k] for k in ['name','represented_collision_trials',
        'stationary_failure_probability','form_error_bound','actual_form_error_diagnostic',
        'means','confidence_lower','confidence_upper','confidence_ratio',
        'independent_prediction_factor','upward_cooperative_rate',
        'total_forward_cooperative_observations']} for c in data['cases']],indent=2))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1,2,figsize=(10.5,4.2),layout='constrained')
    for ax,c in zip(axes,data['cases']):
        truth = float(c['means']['true'])
        vals = [float(c['means']['independent_only'])/truth,
                float(c['means']['fitted'])/truth,1.]
        ax.barh([2,1,0],vals,color=['#a5aeb9','#176a8b','#229887'],height=.5)
        lo,hi = float(c['confidence_lower'])/truth,float(c['confidence_upper'])/truth
        ax.errorbar(vals[1],1,xerr=[[vals[1]-lo],[hi-vals[1]]],fmt='none',
                    ecolor='#102f43',capsize=7,linewidth=2)
        ax.set_yticks([2,1,0],['Independent only','Acquired model + bound','Known synthetic truth'])
        ax.set_xlabel('Predicted mean / true model mean')
        ax.set_title('2 components' if c['components']==2 else 'K4, 6 components')
        ax.axvline(1,color='#102f43',alpha=.35,linestyle='--')
        ax.spines[['top','right']].set_visible(False)
        ax.set_xlim(0,max(vals)*1.12)
    fig.suptitle('Prepared recovery exposes cooperative failure channels',fontsize=14)
    fig.savefig(OUT/'intervention_results.pdf')
    fig.savefig(OUT/'intervention_results.png',dpi=180)


if __name__=='__main__':
    main()
