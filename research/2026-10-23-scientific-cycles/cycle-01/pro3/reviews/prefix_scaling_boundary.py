"""Exact rational check of the prescribed integer prefix near ceiling boundaries.

K=log(2), alpha=1/2 imply b*=1/2 and gamma=2/3.  This checks
candidate/update accounting only, not the universal mixing theorem.
"""
from fractions import Fraction
from pathlib import Path
import json
import resource
import time

start = time.perf_counter()
cpu = time.process_time()
b = Fraction(1, 2)
gamma = Fraction(2, 3)
rows = []
for r in (1, 2, 10, 100, 1000):
    boundary = gamma * b**r
    for direction in (-1, 0, 1):
        eps = boundary * (1 + direction * Fraction(1, 2**40))
        # Exact implementation of ceil(log(gamma/eps)/log(2)), via powers.
        k = 0
        while gamma * b**k > eps:
            k += 1
        n = max(1, k + 1)
        expected = r + 2 if direction == -1 else r + 1
        floor = gamma * b**n
        assert n == expected
        assert floor <= b * eps
        rows.append({"r": r, "side": direction, "candidates": n,
                     "prefix_updates": n - 1,
                     "exact_floor_over_eps": str(floor / eps),
                     "assertions_passed": True})
out = {"scope": "Exact integer-boundary diagnostic; not universal mixing proof",
       "K": "log(2)", "alpha": "1/2", "b_star": "1/2", "gamma": "2/3",
       "cases": rows, "wall_seconds": time.perf_counter() - start,
       "cpu_seconds": time.process_time() - cpu,
       "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
path = Path(__file__).with_name("prefix_scaling_boundary_results.json")
path.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({"cases": len(rows), "all_passed": True,
                  "wall_seconds": out["wall_seconds"], "cpu_seconds": out["cpu_seconds"],
                  "peak_rss_kib": out["peak_rss_kib"]}))
