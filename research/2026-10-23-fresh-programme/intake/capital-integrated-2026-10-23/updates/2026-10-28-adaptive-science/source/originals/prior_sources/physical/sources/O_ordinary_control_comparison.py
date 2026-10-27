"""Same-information ordinary schedule search for the three-contact architecture.

This is a numerical incumbent, not a proof of global schedule optimality. Both
designs have C=1, mean total contact conductance=1, off/on=.001, three constant
contact phases per period, identical installed contacts, and the same ideal
omission of actuator costs. Period and all three duty fractions are optimized.
"""
from pathlib import Path
import csv
import itertools
import numpy as np
from scipy.optimize import differential_evolution
from thermal_network import leaky_shuttle

ROOT = Path(__file__).resolve().parent


def ordinary_scalar_response(period, fractions, order, eps=.001):
    # Direct scalar contact integration; no circulant or equal-duty formula.
    on = 1/(1+2*eps)
    off = eps*on
    durations = period*np.asarray(fractions)
    vectors = []
    for j in order:
        b = np.full(3, off)
        b[j] = on
        vectors.append(b)
    V = np.zeros(3)
    for tau, b in zip(durations, vectors):
        r = np.exp(-tau)
        V = r*V + (-np.expm1(-tau))*b
    X = V/(-np.expm1(-period))
    Q = np.zeros((3, 3))
    for tau, b in zip(durations, vectors):
        one_minus_r = -np.expm1(-tau)
        integral = one_minus_r*X+(tau-one_minus_r)*b
        Q += tau*np.diag(b)-np.outer(b, integral)
        X = np.exp(-tau)*X+one_minus_r*b
    return Q/period


def score(Y):
    return min(-Y[(i+1) % 3, i]+Y[(i-1) % 3, i] for i in range(3))


def decode(x):
    weights = np.exp([x[1], x[2], 0.])
    return np.exp(x[0]), weights/weights.sum()


def main():
    rows = []
    for k, order in enumerate(itertools.permutations(range(3))):
        def objective(x):
            P, fractions = decode(x)
            return -score(ordinary_scalar_response(P, fractions, order))
        sol = differential_evolution(objective, [(-4., 4.5), (-3., 3.), (-3., 3.)],
                                     seed=2026102700+k, popsize=12, maxiter=180,
                                     tol=1.e-9, polish=True)
        P, fractions = decode(sol.x)
        Y = ordinary_scalar_response(P, fractions, order)
        rows.append(dict(method='ordinary numerical control search', order=''.join(map(str, order)),
            period=P, fraction_0=fractions[0], fraction_1=fractions[1], fraction_2=fractions[2],
            minimum_cyclic_directional_excess=score(Y), objective_evaluations=sol.nfev,
            converged=bool(sol.success)))
    P = 5.617671518912385
    Y = leaky_shuttle(3, 1/1.002, .001/1.002, 1., P)
    direct = ordinary_scalar_response(P, np.ones(3)/3, (0, 1, 2))
    assert np.max(np.abs(Y-direct)) < 1.e-13
    rows.append(dict(method='derived equal-duty construction', order='012', period=P,
        fraction_0=1/3, fraction_1=1/3, fraction_2=1/3,
        minimum_cyclic_directional_excess=score(Y), objective_evaluations=0, converged=True))
    with (ROOT/'ordinary_control_comparison.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    best = max(r['minimum_cyclic_directional_excess'] for r in rows[:-1])
    report = (f'Ordinary best found score: {best:.16g}\n'
              f'Derived construction score: {score(Y):.16g}\n'
              f'Construction minus ordinary best: {score(Y)-best:.16g}\n'
              'The ordinary controller reaches the construction; no algorithmic '
              'or throughput advantage is demonstrated. Numerical search is not '
              'a proof of global schedule optimality.\n')
    (ROOT/'ORDINARY_COMPARISON.txt').write_text(report)
    print(report)


if __name__ == '__main__':
    main()
