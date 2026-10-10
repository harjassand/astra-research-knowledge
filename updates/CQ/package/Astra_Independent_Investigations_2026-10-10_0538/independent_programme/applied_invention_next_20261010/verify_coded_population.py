"""Exact tests for the coded-population identification construction.

Synthetic mathematical tests only. No experimental validation, novelty claim,
or claim of efficient access to a state-dependent neutral barcode writer.
"""
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path
import random
import sympy as sp


def derivative_test():
    n, q, degree, sparsity = 128, 7, 2, 2
    # Degree <= 2 over F_7: any pair collides at at most two points.
    # q > (s + 1)*degree guarantees the required isolation row.
    words = []
    for i in range(n):
        cs = [i % q, (i // q) % q, (i // q**2) % q]
        words.append([(cs[0] + cs[1]*a + cs[2]*a*a) % q for a in range(q)])
    W = [[int(words[i][a] == b) for i in range(n)]
         for a in range(q) for b in range(q)]
    p = [Q(1 + i % 5) for i in range(n)]
    A = [[Q(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        candidates = [(i+1) % n, (17*i+3) % n, (i+2) % n, (i+3) % n]
        pred = []
        for k in candidates:
            if k != i and k not in pred:
                pred.append(k)
            if len(pred) == sparsity:
                break
        for z, k in enumerate(pred):
            A[i][k] = Q(1 + (i + z) % 7, 3 + z)
        A[i][i] = Q((13*i) % 17 - 8)  # unrestricted varying diagonal
    base_derivative = [sum(A[i][k]*p[k] for k in range(n)) for i in range(n)]
    tag_derivatives = [[sum(A[i][k]*p[k]*w[k] for k in range(n))
                        for i in range(n)] for w in W]
    fractions_derivative = [[(tag_derivatives[j][i] - W[j][i]*base_derivative[i])/p[i]
                             for i in range(n)] for j in range(len(W))]
    compared = 0
    for i in range(n):
        for k in range(n):
            if k == i:
                continue
            rows = [j for j in range(len(W)) if W[j][i] == 0 and W[j][k] == 1]
            assert rows
            observed = min(fractions_derivative[j][i] for j in rows)
            expected = A[i][k]*p[k]/p[i]
            assert observed == expected, (i, k, observed, expected)
            compared += 1
    # A bounded perturbation passes through the min decoder without amplification.
    eps = Q(1, 1000)
    noisy = [[v + eps*Q(((j+11*i) % 7)-3, 3) for i, v in enumerate(row)]
             for j, row in enumerate(fractions_derivative)]
    max_err = Q(0)
    for i in range(n):
        for k in range(n):
            if k == i:
                continue
            rows = [j for j in range(len(W)) if W[j][i] == 0 and W[j][k] == 1]
            e = abs(min(noisy[j][i] for j in rows) - A[i][k]*p[k]/p[i])
            assert e <= eps
            max_err = max(max_err, e)
    return dict(n=n, tags=len(W), sparsity=sparsity, exact_rate_checks=compared,
                all_passed=True, min_decoder_linf_error=str(max_err),
                input_linf_error_bound=str(eps))


def finite_interval_test():
    n, s, m = 8, 2, 4
    rng = random.Random(20261010)
    A = sp.zeros(n)
    # A Metzler matrix with distinct integer diagonal. T = log(2).
    # exp(A*T) is rational by exact spectral interpolation.
    for i in range(n):
        A[i, i] = -(i+1)
        for k in range(max(0, i-s), i):
            A[i, k] = sp.Rational(1 + (3*i+k) % 5, 7)
    E = sp.zeros(n)
    I = sp.eye(n)
    for i in range(n):
        d = -(i+1)
        projector = I
        for j in range(n):
            if i != j:
                dj = -(j+1)
                projector = projector*(A - dj*I)/(d-dj)
        E += sp.Rational(1, 2**(i+1))*projector
    M = A.inv()*(E-I)
    assert A*M == E-I
    p = sp.Matrix([sp.Rational(i+1, 3) for i in range(n)])
    W = sp.Matrix([[sp.Rational(rng.randrange(1, 100), 101) for _ in range(n)]
                   for _ in range(m)])
    U0 = M*p
    U = M*sp.diag(*p)*W.T
    H0 = (E-I)*p
    H = (E-I)*sp.diag(*p)*W.T
    assert min(U0) > 0
    F = sp.diag(*[1/u for u in U0])*U
    all_minor_count = 0
    recovered_rows = 0
    for i in range(n):
        other = [k for k in range(n) if k != i]
        Z = sp.Matrix([[U[k,j] - F[i,j]*U0[k] for k in other] for j in range(m)])
        D = sp.Matrix([H[i,j] - F[i,j]*H0[i] for j in range(m)])
        truth = sp.Matrix([A[i,k] for k in other])
        assert Z*truth == D
        # Explicitly check the complete 2s-column independence condition.
        for cols in combinations(range(n-1), 2*s):
            assert Z[:, list(cols)].det() != 0
            all_minor_count += 1
        # Exhaustive support decoder; exponential in s, no hidden fast-solver claim.
        solutions = set()
        for size in range(s+1):
            for cols in combinations(range(n-1), size):
                if not cols:
                    if D == sp.zeros(m, 1):
                        solutions.add(tuple([sp.Rational(0)]*(n-1)))
                    continue
                Zs = Z[:, list(cols)]
                if Zs.row_join(D).rank() != Zs.rank():
                    continue
                vals = (Zs.T*Zs).inv()*Zs.T*D
                if min(vals) < 0:
                    continue
                candidate = [sp.Rational(0)]*(n-1)
                for k, v in zip(cols, vals):
                    candidate[k] = v
                solutions.add(tuple(candidate))
        assert solutions == {tuple(truth)}
        recovered_rows += 1
    return dict(n=n, tags=m, sparsity=s, horizon="log(2)",
                exact_rational_integral_identity=True,
                full_spark_minors_checked=all_minor_count,
                uniquely_recovered_rows=recovered_rows,
                all_passed=True,
                decoder="exhaustive supports of size <= 2; not a polynomial-time claim")


if __name__ == "__main__":
    results = dict(derivative=derivative_test(), finite_interval=finite_interval_test(),
                   scope="Exact synthetic algebra only; no physical or novel-capability validation")
    path = Path(__file__).with_name("coded_population_exact_results.json")
    path.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
