"""Exact rational and elementary boundary challenges to endpoint PROOF.txt.

Independent audit; this is not a search for a new resource theorem.
"""
from fractions import Fraction as F
import json, math, time, resource, sys
from pathlib import Path

start = time.perf_counter()
cpu = time.process_time()

# Exact survival-sum rounding, independently of floating point ceil.
rounding_cases = 0
for denominator in range(2, 61):
    for numerator in range(1, denominator):
        delta = F(numerator, denominator)
        x = 1 / delta
        N = (x.numerator + x.denominator - 1) // x.denominator
        mu_lower = sum((max(F(0), 1 - i * delta) for i in range(N)), F(0))
        h = N - x
        reference = x / 2 + F(1, 2)
        assert mu_lower - reference == delta * h * (1 - h) / 2
        assert N - 1 <= x
        rounding_cases += 1

# The kappa<1 strong-converse branch: use the exact all-positive event.
# Set m=1 since every expression is homogeneous in m.
branch_cases = 0
for mu in [F(1), F(11,10), F(3,2), F(2), F(7,2)]:
    for gamma in [F(1,10), F(1,2), F(1), F(2), F(6)]:
        kappa = mu - gamma / 2
        if kappa < 1:
            # B(1)-R >= gamma-(mu-1), even when R<C-gamma.
            assert gamma - (mu - 1) > gamma / 2
            branch_cases += 1

# Fully explicit N=1 expected-supply gamble. With Q=D^t, the separable
# chi_Q=Q^-1 sum |jj><jj| commutes with Phi_Q; its distance from Phi_Q
# is exactly 1-1/Q. Supply Phi_Q with probability q, else rank 1 and chi_Q.
# ALL outcomes are averaged and the coin is erased.
gamble_cases = []
epsilon = F(1, 4)
for D in [2, 3, 5]:
    for t in [1, 2, 4, 8, 16]:
        Q = D ** t
        pure_to_chi = 1 - F(1, Q)
        q = 1 - epsilon / pure_to_chi
        assert 0 <= q <= 1
        exact_global_error = (1 - q) * pure_to_chi
        assert exact_global_error == epsilon
        # Strong-converse expected-resource chord, using exact target accept=1.
        # Actual accept law is q+(1-q)/Q; bound E min(1,M/Q) is exact.
        accept = q + (1-q) / Q
        assert accept == 1 - epsilon
        b = t * math.log(D)
        c = float(q) * b
        simple_chord_lower = b * (1 - float(epsilon) - math.exp(-b))
        sharp_chord_lower = simple_chord_lower / (1 - math.exp(-b))
        assert c >= simple_chord_lower - 1e-12
        assert abs(c - sharp_chord_lower) < 1e-12
        gamble_cases.append({"D": D, "copies": t,
                             "exact_error": str(exact_global_error),
                             "success_probability": str(q),
                             "normalized_expected_cost": float(q),
                             "limiting_normalized_cost": 1-float(epsilon)})

raw_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
out = {"status": "PASS", "exact_survival_rounding_cases": rounding_cases,
       "kappa_below_one_exact_test_cases": branch_cases,
       "exact_N1_erased_coin_expected_resource_cases": gamble_cases,
       "wall_seconds": time.perf_counter()-start,
       "cpu_seconds": time.process_time()-cpu,
       "peak_RSS_bytes": int(raw_rss if sys.platform == 'darwin' else raw_rss*1024),
       "scope": "Independent finite algebra checks; no historical novelty or physical access claim"}
Path(__file__).with_name("RESULT.json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps({k: out[k] for k in ["status", "wall_seconds", "cpu_seconds", "peak_RSS_bytes"]}))
