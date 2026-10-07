"""Exact small-instance and structured checks for treewidth_filtered_parity.py."""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations, permutations
import importlib.util
import json
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("treewidth_filtered_parity", ROOT / "treewidth_filtered_parity.py")
tw = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(tw)


def det(A):
    n = len(A)
    if n == 0:
        return tw.ONE
    total = tw.ZERO
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = tw.ONE
        for i, j in enumerate(p):
            term = tw.qmul(term, A[i][j])
        total = tw.qadd(total, tw.qneg(term) if inversions & 1 else term)
    return total


def direct_counts(F, t, allowed):
    n = len(F)
    out = [Q(0)] * (n + 1)
    for k in range(n + 1):
        for I in combinations(range(n), k):
            for J in combinations(range(n), k):
                local = ["0"] * n
                for i in I:
                    local[i] = "u"
                for j in J:
                    local[j] = "d" if local[j] == "0" else "ud"
                if any(local[i] not in allowed[i] for i in range(n)):
                    continue
                minor = det([[F[i][j] for j in J] for i in I])
                mass = minor[0] * minor[0] + minor[1] * minor[1]
                for i in set(I) & set(J):
                    mass *= t[i]
                out[k] += mass
    return out


def poly_add(a, b):
    out = [Q(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] += x
    for i, x in enumerate(b):
        out[i] += x
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def path_transfer(F, t):
    """Independent two-state recurrence for F[i,i+1] and zero elsewhere."""
    n = len(F)
    if n == 0:
        return [Q(1)]
    prev0, prev1 = [Q(1)], [Q(0)]
    for i in range(n - 1):
        next0 = poly_add(prev0, prev1)
        scaled0 = [Q(0)] + prev0
        scaled1 = [Q(0)] + [x * t[i] for x in prev1]
        next1 = [x * abs2(F[i][i + 1]) for x in poly_add(scaled0, scaled1)]
        prev0, prev1 = next0, next1
    out = poly_add(prev0, prev1)
    return out + [Q(0)] * (n + 1 - len(out))


def abs2(z):
    return z[0] * z[0] + z[1] * z[1]


def run():
    rng = random.Random(202610071309)
    values = [tw.ZERO, tw.qc(1), tw.qc(-1, 1), tw.qc(Q(1, 2), Q(-1, 3))]
    random_full = 0
    random_restricted = 0
    order_checks = 0
    for n in range(1, 5):
        for _ in range(30):
            F = [[rng.choice(values) if rng.random() < 0.78 else tw.ZERO for _ in range(n)] for _ in range(n)]
            t = [Q(rng.choice((0, 1, 2, 3)), rng.choice((1, 1, 2, 3))) for _ in range(n)]
            all_allowed = [set(tw.LOCAL_STATES) for _ in range(n)]
            order = list(range(n))
            rng.shuffle(order)
            got = tw.counts(F, t, all_allowed, order)
            expected = direct_counts(F, t, all_allowed)
            assert got == expected, (n, F, t, got, expected)
            random_full += 1

            restricted = [set(s for s in tw.LOCAL_STATES if rng.random() < 0.68) for _ in range(n)]
            if any(not s for s in restricted):
                restricted[rng.randrange(n)] = {"0"}
            got_r = tw.counts(F, t, restricted, order)
            expected_r = direct_counts(F, t, restricted)
            assert got_r == expected_r, (n, F, t, restricted, got_r, expected_r)
            random_restricted += 1

            other = list(reversed(order))
            assert tw.counts(F, t, restricted, other) == got_r
            order_checks += 1

    # Diagonal-only support checks that intersections and diagonal entries are
    # retained when t>0; c_1 is 1*3 + 4*5 and c_2 is 1*4*3*5.
    Fd = [[tw.qc(1), tw.ZERO], [tw.ZERO, tw.qc(2)]]
    td = [Q(3), Q(5)]
    diagonal = tw.counts(Fd, td)
    assert diagonal == [Q(1), Q(23), Q(60)]

    # A 32-site connected support path has elimination width one. Compare the
    # Grassmann contraction with the independent functional two-state transfer.
    n = 32
    Fp = [[tw.ZERO for _ in range(n)] for _ in range(n)]
    tp = [Q(i % 5 + 1, i % 3 + 1) for i in range(n)]
    for i in range(n - 1):
        Fp[i][i + 1] = tw.qc(Q(i + 1, i % 4 + 1), Q((-1) ** i, i % 3 + 1))
    natural = list(range(n))
    width = tw.elimination_width(Fp, natural)
    assert width == 1
    path_got = tw.counts(Fp, tp, order=natural)
    path_expected = path_transfer(Fp, tp)
    assert path_got == path_expected

    # Exact self-reduction smoke check. It proves only that samples are legal
    # and supported; correctness of the law follows from exact completion-mass
    # chain rule, not this finite sample.
    rng_sample = random.Random(5150)
    sample_F = [[tw.qc(1), tw.qc(1, 1)], [tw.qc(2), tw.qc(1)]]
    sample_t = [Q(3, 2), Q(2)]
    sample_counts = tw.counts(sample_F, sample_t)
    positive_k = max(k for k, value in enumerate(sample_counts) if value)
    samples = 40
    for _ in range(samples):
        states = tw.sample_sector(sample_F, sample_t, positive_k, rng=rng_sample)
        assert all(state in tw.LOCAL_STATES for state in states)
        assert direct_counts(sample_F, sample_t, [{s} for s in states])[positive_k] > 0

    result = {
        "status": "PASS",
        "random_full_vectors_vs_direct_minors": random_full,
        "random_local_restrictions_vs_direct_minors": random_restricted,
        "elimination_order_invariance_checks": order_checks,
        "diagonal_attraction_fixture": [str(x) for x in diagonal],
        "path_sites": n,
        "path_elimination_width": width,
        "path_transfer_coefficients_match": True,
        "exact_self_reduction_supported_samples": samples,
        "sampled_sector": positive_k,
        "scope": "finite exact diagnostics; no novelty or asymptotic claim is inferred from the checks",
    }
    out = ROOT / "treewidth_filtered_parity_checks.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
