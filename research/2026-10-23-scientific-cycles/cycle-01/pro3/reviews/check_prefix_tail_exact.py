"""Exact-rational diagnostics for the initial-IMH first-high identity.

All numerical assertions use fractions.Fraction. The general proof is in
prefix_tail_challenge.md; these finite instances do not establish it.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import random
import resource
import time


def rowmat(p, A):
    return [sum((p[i] * A[i][j] for i in range(len(p))), F(0))
            for j in range(len(p))]


def add(x, y):
    return [a + b for a, b in zip(x, y)]


def scale(c, x):
    return [c * a for a in x]


def mh(q, W, allowed=None):
    n = len(q)
    allowed = [True] * n if allowed is None else allowed
    b = sum((q[j] for j in range(n) if allowed[j]), F(0))
    A = [[F(0) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and allowed[j]:
                A[i][j] = q[j] * min(F(1), W[j] / W[i])
        A[i][i] = b - sum(A[i], F(0))
    return A


def main():
    wall = time.perf_counter()
    cpu = time.process_time()
    rng = random.Random(20261021)
    checked = 0
    nonempty_tail = 0
    reset_identity_checks = 0
    strict_bound_cases = 0
    maximum_tail_ratio = F(0)
    for case in range(30):
        n = 3 + case % 4
        pc = [rng.randint(1, 100) for _ in range(n)]
        qc = [rng.randint(1, 100) for _ in range(n)]
        pi = [F(x, sum(pc)) for x in pc]
        q = [F(x, sum(qc)) for x in qc]
        W = [p / z for p, z in zip(pi, q)]
        G = mh(q, W)
        assert rowmat(pi, G) == pi
        for h in [F(1, 4), F(1, 2), F(1), F(2), F(4)]:
            low = [w < h for w in W]
            D = [w < h / 2 for w in W]
            b = sum((x for x, yes in zip(q, low) if yes), F(0))
            pD = sum((x for x, yes in zip(pi, D) if yes), F(0))
            lo = [x if yes else F(0) for x, yes in zip(q, low)]
            hi = [x if not yes else F(0) for x, yes in zip(q, low)]
            Gl = mh(q, W, low)
            all_low = lo
            mu = q
            high_powers = [hi]
            for m in range(8):
                if m:
                    mu = rowmat(mu, G)
                    all_low = rowmat(all_low, Gl)
                    high_powers.append(rowmat(high_powers[-1], G))
                rhs = list(all_low)
                for j in range(m + 1):
                    rhs = add(rhs, scale(b**j, high_powers[m - j]))
                assert rhs == mu, (case, h, m, rhs, mu)
                reset_identity_checks += 1
                assert sum(all_low, F(0)) == b**(m + 1)
                assert all(x <= (m + 1) * z for x, z in zip(mu, q))
                mass = sum((x for x, yes in zip(mu, D) if yes), F(0))
                geometric = sum((b**j for j in range(m)), F(0))
                bound = b**(m + 1) + geometric * pD / h
                assert mass <= bound, (case, h, m, mass, bound)
                checked += 1
                nonempty_tail += int(0 < pD < 1 and 0 < b < 1)
                strict_bound_cases += int(0 < mass and bound < 1)
                if bound:
                    maximum_tail_ratio = max(maximum_tail_ratio, mass / bound)
    result = {
        "result": "PASS",
        "seed": 20261021,
        "chains": 30,
        "thresholds_per_chain": 5,
        "prefix_transitions": list(range(8)),
        "exact_reset_identity_checks": reset_identity_checks,
        "exact_tail_bound_checks": checked,
        "checks_with_nonempty_proper_low_tail_and_high_set": nonempty_tail,
        "checks_with_positive_tail_and_bound_below_one": strict_bound_cases,
        "max_tail_to_bound_ratio_exact": str(maximum_tail_ratio),
        "arithmetic": "fractions.Fraction; no tolerance and no floating-point assertions",
        "wall_seconds": time.perf_counter() - wall,
        "cpu_seconds": time.process_time() - cpu,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "scope": "Finite diagnostics only; arbitrary-space proof is written separately."
    }
    p = Path(__file__).with_name("prefix_tail_exact_results.json")
    p.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
