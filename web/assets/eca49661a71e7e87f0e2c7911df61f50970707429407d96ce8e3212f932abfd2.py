#!/usr/bin/env python3
"""
Independent finite-generator check for the balanced-rate return-chain moment lemma.

Network (base coordinates a,b), lambda=mu=1 by default:
  (a,b) -> (a,b+1)         rate lambda
  (a,b) -> (a+1,b-1)       rate lambda*b
  (a,b) -> (a-1,b-2)       rate kappa*a*b*(b-1)

From (a,1), solve the finite killed-generator Dirichlet system until
the first hit of b=0 or escape from (a-window..a+window, b=1..bmax).
Initial time at b=0 adds zero population increment and is omitted.

NO stochastic simulation, no inferred proof from finite samples. Reported
moments omit contributions on artificial boundary escape; the returned
escape probability does not, by itself, bound the escaped population payoff.

Requirements: numpy and scipy. Run: python verify_return.py
"""
import argparse
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve


def killed_return(a, kappa, lam=1.0, window=13, bmax=9):
    if a < 0 or kappa <= 0 or lam <= 0 or window < 1 or bmax < 2:
        raise ValueError("Invalid parameters")

    points = [
        (aa, b)
        for aa in range(max(0, a - window), a + window + 1)
        for b in range(1, bmax + 1)
    ]
    ix = {pt: i for i, pt in enumerate(points)}
    rows, cols, data = [], [], []
    # right-hand columns: first moment, second raw moment,
    # artificial escape probability, actual b=0 return probability
    rhs = np.zeros((len(points), 4), dtype=np.float64)
    for i, (aa, b) in enumerate(points):
        possible = [((aa, b + 1), lam), ((aa + 1, b - 1), lam * b)]
        if aa >= 1 and b >= 2:
            possible.append(((aa - 1, b - 2), kappa * aa * b * (b - 1)))
        total = 0.0
        for target, rate in possible:
            total += rate
            na, nb = target
            if nb == 0:
                change = na - a
                rhs[i, 0] += rate * change
                rhs[i, 1] += rate * change * change
                rhs[i, 3] += rate
            elif target in ix:
                rows.append(i)
                cols.append(ix[target])
                data.append(-rate)
            else:
                rhs[i, 2] += rate
        rows.append(i)
        cols.append(i)
        data.append(total)
    mat = sp.csc_matrix((data, (rows, cols)), shape=(len(points), len(points)))
    solution = spsolve(mat, rhs)[ix[(a, 1)]]
    first, second, escaped, returned = map(float, solution)
    return {
        "a": a, "kappa": kappa, "lambda": lam,
        "a_times_first": a * first,
        "raw_second": second,
        "escape_prob": escaped,
        "return_prob": returned,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lambda-rate", type=float, default=1.0)
    parser.add_argument("--window", type=int, default=13)
    parser.add_argument("--bmax", type=int, default=9)
    args = parser.parse_args()
    lam = args.lambda_rate

    print("finite killed-generator return moments; lambda=mu=", lam)
    print("columns: kappa, a, a*E[Delta A], E[(Delta A)^2],"
          " truncation escape probability, asymptotic lambda/kappa")
    for kappa in (lam / 2, lam, 2 * lam, 4 * lam):
        for a in (20, 100, 300):
            x = killed_return(a, kappa, lam, args.window, args.bmax)
            print(f"{kappa:6g} {a:4d} {x['a_times_first']: .10f} "
                  f"{x['raw_second']: .10f} "
                  f"{x['escape_prob']: .3e} "
                  f"{lam / kappa: .10f}")
            assert abs(x["return_prob"] + x["escape_prob"] - 1) < 5e-9
            assert x["escape_prob"] < 1e-8

        # At a=300 convergence is visible to the quoted 1/x asymptotics.
        t = killed_return(300, kappa, lam, args.window, args.bmax)
        assert abs(t["a_times_first"] - lam/kappa) < 0.025 * (lam/kappa)
        assert abs(t["raw_second"] - 1) < 0.015

    print("Finite numerical checks PASS. No asymptotic theorem certified.")


if __name__ == "__main__":
    main()
