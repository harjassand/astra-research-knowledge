"""Finite, untruncated immigration-clock resolvents for a conservative module.

Default example: a deficiency-one, non-complex-balanced four-complex cycle,
with 0 <-> A. Also retains the deficiency-zero three-cycle as a control.
The event clock has actual rate one; internal and true-death clocks are retained.
"""
import argparse
from fractions import Fraction
import json
from math import prod
from pathlib import Path
import time

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import splu


THREE_CYCLE = [((2, 1, 0), (0, 2, 1), 1),
               ((0, 2, 1), (1, 0, 2), 1),
               ((1, 0, 2), (2, 1, 0), 1)]
FOUR_CYCLE = [((2, 1, 0), (0, 2, 1), 1),
              ((0, 2, 1), (1, 0, 2), 2),
              ((1, 0, 2), (1, 1, 1), 3),
              ((1, 1, 1), (2, 1, 0), 5)]


def falling(x, k):
    return prod(range(x-k+1, x+1)) if x >= k else 0


def shell(n, reactions):
    states = [(a, b, n-a-b) for a in range(n+1) for b in range(n-a+1)]
    index = {x: i for i, x in enumerate(states)}
    rows, cols, vals = [], [], []
    edges = []
    for i, x in enumerate(states):
        outgoing = []
        for src, dst, coefficient in reactions:
            rate = coefficient*prod(falling(xx, yy) for xx, yy in zip(x, src))
            if rate:
                target = tuple(xx+zz-yy for xx, yy, zz in zip(x, src, dst))
                j = index[target]
                outgoing.append((j, rate))
                rows.append(i); cols.append(j); vals.append(-rate)
        diag = 1+x[0]+sum(rate for _, rate in outgoing)
        rows.append(i); cols.append(i); vals.append(diag)
        edges.append(outgoing)
    mat = coo_matrix((vals, (rows, cols)), shape=(len(states), len(states))).tocsc()
    return states, index, edges, mat, splu(mat)


def run(nmax, births, exact_residual, reactions):
    limit = nmax+births
    shells = [shell(n, reactions) for n in range(limit+1)]
    previous = [np.full(len(s[0]), n, dtype=float) for n, s in enumerate(shells)]
    max_error = Fraction(0)
    summaries = []
    all_results = []
    for k in range(1, births+1):
        current = []
        residual_max = Fraction(0)
        for n in range(limit-k+1):
            states, index, edges, mat, factor = shells[n]
            next_index = shells[n+1][1]
            rhs = np.array([previous[n+1][next_index[(a+1,b,c)]] for a,b,c in states])
            if n:
                lower_index = shells[n-1][1]
                for i, (a,b,c) in enumerate(states):
                    if a: rhs[i] += a*current[n-1][lower_index[(a-1,b,c)]]
            value = factor.solve(rhs)
            current.append(value)
            if exact_residual:
                vf = [Fraction(float(v)) for v in value]
                for i, (a,b,c) in enumerate(states):
                    residual = (1+a+sum(rate for _,rate in edges[i]))*vf[i]
                    residual -= sum(rate*vf[j] for j,rate in edges[i])
                    residual -= Fraction(float(previous[n+1][next_index[(a+1,b,c)]]))
                    if a:
                        residual -= a*Fraction(float(current[n-1][lower_index[(a-1,b,c)]]))
                    residual_max = max(residual_max, abs(residual))
        # Global downward generator has killed row sum one. Its resolvent's
        # infinity norm is <= 1; errors of the previous-birth RHS add once.
        max_error += residual_max
        rows = []
        for n in range(1, min(nmax, len(current)-1)+1):
            states, index, *_ = shells[n]
            # The A-only class is positive recurrent trivially. Include it;
            # these are bounds over every actual count state in the shell.
            drift = current[n]-n
            worst = int(np.argmax(drift))
            rows.append(dict(n=n, worst_drift=float(drift[worst]),
                             worst_state=states[worst],
                             corner_B=float(drift[index[(0,n,0)]]),
                             corner_C=float(drift[index[(0,0,n)]])))
        summaries.append(dict(births=k, exact_residual_bound=str(residual_max),
                              uniform_solution_error_bound=str(max_error), rows=rows))
        print(json.dumps(dict(births=k, uniform_error=float(max_error),
                              last=rows[-1])), flush=True)
        all_results.append(current)
        previous = current
    return dict(network=reactions, port_rates='lambda=mu=1, falling-factorial',
                maximum_initial_total=nmax, births=births,
                finite_access='No truncation: N can only decrease between immigration events.',
                residual_validation=exact_residual,
                summaries=summaries), all_results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nmax', type=int, default=35)
    ap.add_argument('--births', type=int, default=3)
    ap.add_argument('--exact-residual', action='store_true')
    ap.add_argument('--network', choices=['three-cycle-control', 'four-cycle'], default='four-cycle')
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    start = time.monotonic()
    reactions = THREE_CYCLE if args.network == 'three-cycle-control' else FOUR_CYCLE
    result, arrays = run(args.nmax, args.births, args.exact_residual, reactions)
    result['seconds'] = time.monotonic()-start
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/'resolvent.json').write_text(json.dumps(result, indent=2)+'\n')
    np.savez(args.out/'values.npz', **{
        f'k{k+1}_n{n}': a for k, shell_values in enumerate(arrays)
        for n,a in enumerate(shell_values)})


if __name__ == '__main__':
    main()
