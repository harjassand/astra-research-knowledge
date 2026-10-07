"""Small exact checks for the identity-anchored grouped-DPP mapping.

The only imported sampler is c03_l09's phase-2 copy of c01_s03's source.
This is finite diagnostic evidence, not a proof of the stated identities.
"""
from fractions import Fraction as Q
from itertools import combinations
import importlib.util
import json
from pathlib import Path
from random import Random


def c(x=0, y=0):
    return (Q(x), Q(y))


ZERO = c()
ONE = c(1)


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def neg(x):
    return (-x[0], -x[1])


def sub(x, y):
    return add(x, neg(y))


def mul(x, y):
    return (x[0]*y[0] - x[1]*y[1], x[0]*y[1] + x[1]*y[0])


def conj(x):
    return (x[0], -x[1])


def div(x, y):
    den = y[0]*y[0] + y[1]*y[1]
    assert den
    return ( (x[0]*y[0] + x[1]*y[1])/den,
             (x[1]*y[0] - x[0]*y[1])/den )


def det(M):
    A = [row[:] for row in M]
    n = len(A)
    if n == 0:
        return ONE
    sign, value = 1, ONE
    for j in range(n):
        p = next((r for r in range(j, n) if A[r][j] != ZERO), None)
        if p is None:
            return ZERO
        if p != j:
            A[j], A[p] = A[p], A[j]
            sign = -sign
        pivot = A[j][j]
        value = mul(value, pivot)
        for r in range(j+1, n):
            if A[r][j] == ZERO:
                continue
            factor = div(A[r][j], pivot)
            for q in range(j+1, n):
                A[r][q] = sub(A[r][q], mul(factor, A[j][q]))
            A[r][j] = ZERO
    return value if sign == 1 else neg(value)


def abs_sq(z):
    out = z[0]*z[0] + z[1]*z[1]
    assert out >= 0
    return out


def matmul(A, B):
    return [[sum_complex(mul(A[i][h], B[h][j])
                         for h in range(len(B)))
             for j in range(len(B[0]))]
            for i in range(len(A))]


def sum_complex(xs):
    out = ZERO
    for x in xs:
        out = add(out, x)
    return out


def grouped_weight(F, S):
    n, k = len(F), len(S)
    # W_S has alternating columns e_i and row_i(F)^T, in increasing i order.
    cols = []
    for i in S:
        cols.append([ONE if r == i else ZERO for r in range(n)])
        cols.append(F[i][:])
    gram = [[sum_complex(mul(conj(cols[a][r]), cols[b][r])
                         for r in range(n))
             for b in range(2*k)]
            for a in range(2*k)]
    d = det(gram)
    assert d[1] == 0 and d[0] >= 0
    return d[0]


def minor(F, I, J):
    return det([[F[i][j] for j in J] for i in I])


def row_group_weight(F, S):
    n, k = len(F), len(S)
    complement = [j for j in range(n) if j not in S]
    return sum((abs_sq(minor(F, list(S), list(J)))
                for J in combinations(complement, k)), Q(0))


def pfaffian(A):
    n = len(A)
    if n == 0:
        return ONE
    assert n % 2 == 0
    out = ZERO
    for j in range(1, n):
        rows = [r for r in range(1, n) if r != j]
        cols = [q for q in range(1, n) if q != j]
        submatrix = [[A[r][q] for q in cols] for r in rows]
        term = mul(A[0][j], pfaffian(submatrix))
        out = add(out, term if j % 2 else neg(term))
    return out


def vector_group_weight(groups, S):
    chosen = [v for i in S for v in groups[i]]
    r, t = len(chosen[0]), len(chosen)
    gram = [[sum_complex(mul(conj(chosen[a][j]), chosen[b][j])
                         for j in range(r))
             for b in range(t)]
            for a in range(t)]
    d = det(gram)
    assert d[1] == 0 and d[0] >= 0
    return d[0]


def rank(A):
    A = [row[:] for row in A]
    if not A:
        return 0
    rows, cols, pivot_row = len(A), len(A[0]), 0
    for col in range(cols):
        p = next((r for r in range(pivot_row, rows)
                  if A[r][col] != ZERO), None)
        if p is None:
            continue
        A[pivot_row], A[p] = A[p], A[pivot_row]
        for r in range(pivot_row+1, rows):
            if A[r][col] == ZERO:
                continue
            factor = div(A[r][col], A[pivot_row][col])
            for j in range(col, cols):
                A[r][j] = sub(A[r][j], mul(factor, A[pivot_row][j]))
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def generic_pfaffian_sample(groups, signs, k):
    d = len(groups[0][0])
    A = [[ZERO for _ in range(d)] for _ in range(d)]
    for s, (a, b) in zip(signs, groups):
        for i in range(d):
            for j in range(d):
                wedge = sub(mul(a[i], b[j]), mul(b[i], a[j]))
                A[i][j] = add(A[i][j], (s*wedge[0], s*wedge[1]))
    return sum((abs_sq(pfaffian([[A[i][j] for j in R] for i in R]))
                for R in combinations(range(d), 2*k)), Q(0))


def check_matrix(F, k):
    n = len(F)
    all_sets = list(combinations(range(n), k))
    direct = {}
    mapped = {}
    for S in all_sets:
        direct[S] = grouped_weight(F, S)
        mapped[S] = row_group_weight(F, S)
        assert direct[S] == mapped[S], (S, direct[S], mapped[S])
    return {
        "n": n,
        "k": k,
        "group_sets_checked": len(all_sets),
        "mapping_equal_for_all_sets": True,
        "partition_from_gram": str(sum(direct.values(), Q(0))),
        "partition_from_disjoint_minors": str(sum(mapped.values(), Q(0))),
        "positive_support_sets": sum(w > 0 for w in direct.values()),
    }


def main():
    matrices = [
        [[c(1), c(2), c(0), c(-1)],
         [c(0), c(1), c(2), c(1)],
         [c(1), c(0), c(1), c(2)],
         [c(2), c(-1), c(0), c(1)]],
        [[c(1, 1), c(0), c(2, -1), c(1)],
         [c(0, 1), c(2), c(1, 1), c(-1)],
         [c(1), c(-1, 1), c(0, 1), c(2)],
         [c(2, 0), c(1, -1), c(1), c(0, 1)]],
    ]
    reports = []
    for F in matrices:
        n = len(F)
        for k in (1, 2):
            reports.append(check_matrix(F, k))

    # Generic two-vector groups: the random-sign Pfaffian norm is an unbiased
    # estimator of the grouped-DPP partition function, with the crude M bound.
    groups = [
        ([c(1), c(0), c(1, 1), c(2)], [c(0), c(1), c(1), c(-1, 1)]),
        # Duplicate group 0 so S={0,1} is a concrete infeasible parity set.
        ([c(1), c(0), c(1, 1), c(2)], [c(0), c(1), c(1), c(-1, 1)]),
        ([c(1, 1), c(1), c(0), c(-1)], [c(2), c(0, 1), c(1), c(1, 1)]),
        ([c(1), c(2), c(1, -1), c(0)], [c(0, 1), c(1), c(2, 1), c(1)]),
    ]
    k = 2
    sets = list(combinations(range(len(groups)), k))
    weights = {S: vector_group_weight(groups, S) for S in sets}
    Z = sum(weights.values(), Q(0))
    assert Z > 0
    parity_support = {}
    for S in sets:
        chosen = [v for i in S for v in groups[i]]
        columns = [[chosen[j][r] for j in range(2*k)]
                   for r in range(len(groups[0][0]))]
        parity_support[S] = rank(columns) == 2*k
        assert (weights[S] > 0) == parity_support[S]
    sign_values = [generic_pfaffian_sample(groups, signs, k)
                   for signs in __import__("itertools").product((-1, 1), repeat=len(groups))]
    generic_bound = __import__("math").comb(len(groups), k)
    assert sum(sign_values, Q(0))/len(sign_values) == Z
    assert max(sign_values) <= generic_bound*Z
    generic_check = {
        "ambient_dimension": len(groups[0][0]),
        "group_count": len(groups),
        "k": k,
        "group_sets_checked": len(sets),
        "sign_words_exhausted": len(sign_values),
        "partition_from_gram": str(Z),
        "mean_pfaffian_sample": str(sum(sign_values, Q(0))/len(sign_values)),
        "pointwise_Cauchy_bound_M": generic_bound,
        "max_sample_over_partition": str(max(sign_values)/Z),
        "support_equals_linear_matroid_parity_feasibility": True,
        "feasible_group_sets": sum(parity_support.values()),
        "unbiased_and_bound_checks": True,
    }

    # Use only the copy placed in our own revisions before executing the source.
    src = Path(__file__).with_name("low_sector_sampler_phase2_copy.py")
    spec = importlib.util.spec_from_file_location("low_sector_sampler_phase2_copy", src)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    int_F = [[1, 2, 0, -1], [0, 1, 2, 1], [1, 0, 1, 2], [2, -1, 0, 1]]
    sampler = module.LowSector(int_F)
    source_norms = {}
    for k in (1, 2):
        # Enumerate all 2^n sign words: this is exact for this small diagnostic.
        estimate = sampler.estimate(k, Q(1, 2), Q(1, 2),
                                    enumerate_if_cheaper=True)
        exact_partition = sum((row_group_weight(matrices[0], S)
                               for S in combinations(range(n), k)), Q(0))
        assert estimate == exact_partition
        source_norms[str(k)] = str(estimate)

    # Sample only as a support smoke test. This does not validate the TV theorem.
    rng = Random(211)
    sample_records = []
    for _ in range(48):
        sample_records.append(sampler.born_sample(
            2, Q(1, 20), rng=rng, enumerate_if_cheaper=True))
    supported = {S for S in combinations(range(4), 2)
                 if row_group_weight(matrices[0], S) > 0}
    bad = []
    for record in sample_records:
        if record["status"] == "OK":
            if tuple(record["I"]) not in supported:
                bad.append(record)
    assert not bad

    out = {
        "status": "PASS",
        "checks": reports,
        "generic_grouped_dpp_pfaffian_check": generic_check,
        "copied_source_exact_norms": source_norms,
        "copied_source_sampler_smoke": {
            "draws": len(sample_records),
            "ok": sum(r["status"] == "OK" for r in sample_records),
            "fail": sum(r["status"] == "FAIL" for r in sample_records),
            "unsupported_successes": len(bad),
            "diagnostic_only": True,
        },
    }
    target = Path(__file__).with_name("grouped_dpp_identity_checks.json")
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
