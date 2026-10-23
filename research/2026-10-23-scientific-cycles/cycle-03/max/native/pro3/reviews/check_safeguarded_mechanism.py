"""Exact diagnostics for the first-hit argument; no universal claim rests on these.

The script includes a rational counterexample to the tempting but false
linear proposal-density bound q L^t <= (t+1) q.  It does not mutate inputs.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import random
import resource
import time


def vm(v, a):
    return [sum(v[i] * a[i][j] for i in range(len(v)))
            for j in range(len(v))]


def step(v, a, n):
    for _ in range(n):
        v = vm(v, a)
    return v


def mh(r, w):
    n = len(w)
    a = [[r[i][j] * min(F(1), w[j] / w[i])
          for j in range(n)] for i in range(n)]
    for i in range(n):
        a[i][i] += 1 - sum(a[i])
    return a


def rational(x):
    return str(x.numerator) + "/" + str(x.denominator)


def main():
    wall = time.perf_counter()
    cpu = time.process_time()
    rng = random.Random(20261022)
    chains = decompositions = inequality_checks = 0
    for n in (3, 4, 6):
        for instance in range(5):
            ints = [rng.randint(1, 40) for _ in range(n)]
            q = [F(i, sum(ints)) for i in ints]
            w0 = [F(rng.randint(1, 100), rng.randint(1, 100))
                  for _ in range(n)]
            z = sum(q[i] * w0[i] for i in range(n))
            w = [u / z for u in w0]
            pi = [q[i] * w[i] for i in range(n)]
            flow = [[F(0) for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(i):
                    flow[i][j] = flow[j][i] = F(rng.randint(1, 9))
            scale = 2 * max(sum(flow[i]) / q[i] for i in range(n))
            r = [[flow[i][j] / (scale * q[i]) for j in range(n)]
                 for i in range(n)]
            for i in range(n):
                r[i][i] = 1 - sum(r[i])
            assert vm(q, r) == q
            assert all(q[i] * r[i][j] == q[j] * r[j][i]
                       for i in range(n) for j in range(n))
            l = mh(r, w)
            g = mh([q[:] for _ in range(n)], w)
            alpha = F(1, 2)
            c = [[(F(i == j) + alpha * g[i][j]
                   + (1 - alpha) * l[i][j]) / 2
                  for j in range(n)] for i in range(n)]
            assert vm(pi, l) == pi and vm(pi, c) == pi
            assert all(vm(q, l)[j] <= 2 * q[j] for j in range(n))
            assert all(vm(q, c)[j] <= F(3, 2) * q[j] for j in range(n))
            inequality_checks += 2 * n
            chains += 1
            sorted_w = sorted(set(w))
            thresholds = [(sorted_w[j] + sorted_w[j+1]) / 2
                          for j in range(len(sorted_w)-1)]
            for h in thresholds:
                low = [i for i in range(n) if w[i] < h]
                high = [i for i in range(n) if w[i] >= h]
                b = sum(q[i] for i in low)
                theta = 1 - alpha * (1 - b) / 2
                for s in (0, 1, 2, 4, 7):
                    low_law = [q[i] if i in low else F(0)
                               for i in range(n)]
                    hit_laws = [[q[i] if i in high else F(0)
                                 for i in range(n)]]
                    for j in range(1, s+1):
                        moved = vm(low_law, c)
                        hit_laws.append([moved[i] if i in high else F(0)
                                         for i in range(n)])
                        low_law = [moved[i] if i in low else F(0)
                                   for i in range(n)]
                    actual = step(q, c, s)
                    reconstructed = low_law[:]
                    for j, nu in enumerate(hit_laws):
                        assert all(nu[i] <= F(3, 2)**j * pi[i] / h
                                   for i in range(n))
                        inequality_checks += n
                        propagated = step(nu, c, s-j)
                        reconstructed = [reconstructed[i] + propagated[i]
                                         for i in range(n)]
                    assert reconstructed == actual
                    assert sum(low_law) <= b * theta**s
                    assert all(actual[i] <= F(3, 2)**s * q[i]
                               for i in range(n))
                    geometric = sum(F(3, 2)**j for j in range(s+1))
                    for i in low:
                        assert actual[i] <= b * theta**s + pi[i] * geometric / h
                    inequality_checks += 1 + n + len(low)
                    decompositions += 1

    # Rational positive finite counterexample, separate from the above checks.
    q = [F(99, 100), F(1, 2000), F(19, 2000)]
    r = [[F(98849, 99000), F(13, 99000), F(23, 16500)],
         [F(13, 50), F(6, 25), F(1, 2)],
         [F(69, 475), F(1, 38), F(787, 950)]]
    raw = [F(1), F(2200), F(17)]
    z = sum(q[i] * raw[i] for i in range(3))
    w = [x/z for x in raw]
    pi = [q[i]*w[i] for i in range(3)]
    l = mh(r, w)
    assert vm(q, r) == q
    assert vm(pi, l) == pi
    mu = step(q, l, 12)
    ratio = mu[1] / q[1]
    assert ratio > 13
    result = {
        "status": "PASS",
        "seed": 20261022,
        "chains": chains,
        "exact_first_hit_decompositions": decompositions,
        "exact_scalar_inequality_checks": inequality_checks,
        "linear_domination_counterexample": {
            "claim_rejected": "q L^t <= (t+1) q",
            "q": [rational(x) for x in q],
            "R": [[rational(x) for x in row] for row in r],
            "raw_W": [rational(x) for x in raw],
            "pi": [rational(x) for x in pi],
            "t": 12,
            "state_zero_based": 1,
            "density_ratio_exact": rational(ratio),
            "density_ratio_rounded": float(ratio),
            "proposed_upper_bound": 13,
            "forward_KL_rounded": sum(float(pi[i])*math.log(float(w[i]))
                                      for i in range(3)),
        },
        "resources": {
            "wall_seconds": time.perf_counter() - wall,
            "cpu_seconds": time.process_time() - cpu,
            "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
    }
    destination = Path(__file__).with_name("safeguarded_mechanism_checks.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
