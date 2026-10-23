#!/usr/bin/env python3
"""Exact-rational admission checks for the proved noncommuting gap obstruction.

No optimizer or random search. The universal proof is in ROBUST_AUDIT.txt.
"""
from fractions import Fraction as F
import json
import time


def run():
    started = time.process_time()
    records = []
    for m in (2, 3, 10, 1001):
        c = F(m*m-1, m*m+1)
        s = F(2*m, m*m+1)
        gamma = 1-c
        assert c*c+s*s == 1
        # H on the Pauli-(X,Z) operator plane.
        h = ((1+c*c, -s*c), (-s*c, s*s))
        assert h[0][0]+h[1][1] == 2
        assert h[0][0]*h[1][1]-h[0][1]*h[1][0] == s*s
        assert gamma*gamma-2*gamma+s*s == 0
        # The bisector is proportional to X+m Z, trace zero and outside
        # the exact commutant. Its squared norm cancels in these ratios.
        assert h[0][0]+m*h[0][1] == gamma
        assert h[1][0]+m*h[1][1] == m*gamma
        accept_z = F(m*m, m*m+1)
        accept_tilted = (s+m*c)**2 / (m*m+1)
        assert accept_z == accept_tilted
        total_failure = 2-accept_z-accept_tilted
        assert total_failure == gamma == F(2, m*m+1)
        # Original unbisected Z example is retained too.
        assert 1-c*c == F(4*m*m, (m*m+1)**2)
        records.append({
            "M": m,
            "rank_bounds": [2, 2, 1],
            "gap": str(gamma),
            "accept_probabilities": [str(accept_z), str(accept_tilted), "1"],
            "summed_failure": str(total_failure),
            "half_trace_distance_to_every_exact_support_state": "1",
            "exact_checks": "PASS",
        })
    return {
        "status": "PASS",
        "arithmetic": "fractions.Fraction exact rational",
        "scope": "Finite replay of analytic factor calculation; no numerical search",
        "records": records,
        "cpu_seconds": time.process_time()-started,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
