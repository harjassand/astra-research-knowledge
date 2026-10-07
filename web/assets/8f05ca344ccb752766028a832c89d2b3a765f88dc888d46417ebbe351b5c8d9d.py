#!/usr/bin/env python3
"""Independent exact verifier of C07_S02's finite delta=5/4 certificates. Adapted by C07_S01 from C02_S01's frozen verifier.

No author code is imported or executed. Input exp enclosures are reacquired by
positive Taylor sums for exp(x/64), a geometric tail, reciprocal and exact
64th powers. LDL is checked by unrounded Fraction interval inclusions against
every saved pivot and lower-triangular entry, using the saved previously
verified entries only. All mathematical comparisons are exact rational ones.
"""
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import json
import math
import time

OWN = Path(__file__).resolve().parent
ROOT = OWN.parents[4]
SOURCE = ROOT / "work/cycle6/c07_s02/phase2/evidence/axial_delta5over4_finite_N63_P384.json"
EXPECTED_SOURCE_HASH = "f54fb418fbfbc73dc71458cb4da01aad0c98935de972ffd8d6474714bc357fb8"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_interval(pair, denominator):
    require(isinstance(pair, list) and len(pair) == 2, "invalid interval shape")
    require(all(isinstance(x, str) and str(int(x)) == x for x in pair),
            "interval endpoints must be canonical integer strings")
    result = tuple(Q(int(x), denominator) for x in pair)
    require(result[0] <= result[1], "interval endpoints reversed")
    return result


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def subtract(a, b):
    return a[0] - b[1], a[1] - b[0]


def multiply(a, b):
    corners = [x * y for x in a for y in b]
    return min(corners), max(corners)


def square(a):
    ends = [a[0] ** 2, a[1] ** 2]
    return (Q(0) if a[0] <= 0 <= a[1] else min(ends)), max(ends)


def divide(a, b):
    require(b[0] > 0, "division denominator not proved positive")
    corners = [x / y for x in a for y in b]
    return min(corners), max(corners)


def contains(outer, inner):
    return outer[0] <= inner[0] <= inner[1] <= outer[1]


def exact_exp_minus_bounds(x):
    """Reacquire exp(-x), independently of saved alternating-series metadata.

    For z=x/64 <=315/1024 and M=80, let S=sum_{j=0}^M z^j/j!.
    The positive remaining terms have successive ratio <=z/(M+2), so
      S <= exp(z) <= S + [z^(M+1)/(M+1)!]/[1-z/(M+2)].
    Reciprocation and exact 64th powers enclose exp(-x). No dyadic rounding is
    done in this acquisition, so it differs from the candidate algorithm.
    """
    require(0 <= x <= Q(315, 16), "input exponent outside declared finite scope")
    if x == 0:
        return Q(1), Q(1)
    z = x / 64
    total = term = Q(1)
    degree = 80
    for j in range(1, degree + 1):
        term *= z / j
        total += term
    next_term = term * z / (degree + 1)
    ratio = z / (degree + 2)
    require(0 < ratio < 1, "invalid geometric positive-series tail")
    upper = total + next_term / (1 - ratio)
    return (1 / upper) ** 64, (1 / total) ** 64


def check_matrix(N, matrix, q, D):
    shift = matrix["shift"]
    require(shift in (0, 1), "wrong Hankel shift")
    dimension = (N - shift) // 2 + 1
    require(matrix["dimension"] == dimension, "wrong Hankel dimension")
    require(len(matrix["diagonal_intervals"]) == dimension, "missing pivots")
    require(len(matrix["L_strict_lower_intervals"]) == dimension, "missing L rows")
    diagonal = [read_interval(x, D) for x in matrix["diagonal_intervals"]]
    lower = []
    for i, row in enumerate(matrix["L_strict_lower_intervals"]):
        require(len(row) == i, "missing or excess strict-lower entries")
        lower.append([read_interval(x, D) for x in row])
    checked_lower = 0
    for i in range(dimension):
        require(diagonal[i][0] > 0, f"nonpositive lower pivot N={N} shift={shift} i={i}")
        recurrence = q[2 * i + shift]
        for k in range(i):
            recurrence = subtract(recurrence, multiply(square(lower[i][k]), diagonal[k]))
        require(contains(diagonal[i], recurrence),
                f"pivot recurrence not enclosed N={N} shift={shift} i={i}")
        for j in range(i + 1, dimension):
            numerator = q[j + i + shift]
            for k in range(i):
                term = multiply(multiply(lower[j][k], lower[i][k]), diagonal[k])
                numerator = subtract(numerator, term)
            recurrence = divide(numerator, diagonal[i])
            require(contains(lower[j][i], recurrence),
                    f"L recurrence not enclosed N={N} shift={shift} j={j} i={i}")
            checked_lower += 1
    saved_min = int(matrix["minimum_lower_pivot_integer"])
    require(saved_min == min(int(x[0]) for x in matrix["diagonal_intervals"]),
            "incorrect declared minimum pivot")
    return {"N": N, "shift": shift, "dimension": dimension,
            "verified_pivots": dimension, "verified_strict_lower_entries": checked_lower,
            "minimum_lower_pivot_integer": str(saved_min)}


def verify(data, stop_N=None):
    require(data["delta"] == "5/4", "wrong target delta")
    require(data["precision_bits"] == 384, "unexpected precision")
    D = 2 ** 384
    require(data["denominator"] == str(D), "wrong interval denominator")
    require(data["max_N_requested"] == data["completed_max_N"] == 63,
            "finite case split does not close through N=63")
    require([case["N"] for case in data["cases"]] == list(range(2, 64)),
            "finite cases missing, repeated, or reordered")
    reports = []
    acquired_inputs = 0
    cache = {}
    for case in data["cases"]:
        N = case["N"]
        if stop_N is not None and N > stop_N:
            break
        require(len(case["q_intervals"]) == N + 1, "missing q input intervals")
        q = [read_interval(x, D) for x in case["q_intervals"]]
        for k, saved in enumerate(q):
            exponent = Q(5, 4) * Q((2 * k - N) ** 2, 4 * N)
            if exponent not in cache:
                cache[exponent] = exact_exp_minus_bounds(exponent)
            binomial = math.comb(N, k)
            independently_acquired = tuple(x / binomial for x in cache[exponent])
            require(contains(saved, independently_acquired),
                    f"input exp/binomial enclosure false N={N} k={k}")
            acquired_inputs += 1
        if N % 8 == 0:
            print(json.dumps({"progress_N": N, "acquired_q": acquired_inputs}), flush=True)
        require([m["shift"] for m in case["matrices"]] == [0, 1],
                "missing or repeated H0/H1")
        for matrix in case["matrices"]:
            reports.append(check_matrix(N, matrix, q, D))
    return {"verified_input_q_intervals": acquired_inputs,
            "distinct_independently_acquired_exponents": len(cache),
            "verified_matrices": len(reports),
            "verified_pivots": sum(x["verified_pivots"] for x in reports),
            "verified_strict_lower_entries": sum(x["verified_strict_lower_entries"] for x in reports),
            "matrix_reports": reports,
            "minimum_global_lower_pivot_integer": min((x["minimum_lower_pivot_integer"]
                                                        for x in reports), key=int)}


from independent_tail_constants import rational_constant_checks


def rejection_controls(data):
    controls = []
    altered = deepcopy(data)
    altered["delta"] = "1"
    controls.append(("wrong delta target", altered))
    altered = deepcopy(data)
    altered["cases"][0]["q_intervals"][1] = [str(2 ** 384), str(2 ** 384)]
    controls.append(("false exact central input q", altered))
    altered = deepcopy(data)
    altered["cases"][0]["matrices"][0]["diagonal_intervals"][1] = ["1", "1"]
    controls.append(("positive but false LDL pivot interval", altered))
    altered = deepcopy(data)
    altered["cases"][0]["matrices"][0]["L_strict_lower_intervals"][1][0] = ["0", "0"]
    controls.append(("false lower-triangular recurrence interval", altered))
    altered = deepcopy(data)
    altered["cases"].pop()
    controls.append(("missing finite case N63", altered))
    result = []
    for name, mutated in controls:
        try:
            verify(mutated, stop_N=2)
        except ValueError as error:
            result.append({"control": name, "status": "REJECTED", "reason": str(error)})
        else:
            raise ValueError(f"corrupted certificate accepted: {name}")
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--certificate", type=Path, default=SOURCE)
    args = ap.parse_args()
    start = time.perf_counter()
    raw = args.certificate.read_bytes()
    require(sha256(raw).hexdigest() == EXPECTED_SOURCE_HASH, "certificate changed from inspected source")
    data = json.loads(raw)
    result = {"status": "PASS independent exact rational verification",
              "certificate_path": str(args.certificate.resolve()),
              "certificate_sha256": sha256(raw).hexdigest(),
              "verifier_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "input_method": "positive Taylor exp(x/64) through degree80, exact geometric tail, reciprocal and exact 64th powers",
              "LDL_method": "unrounded Fraction interval recurrence inclusion for every saved entry, no author execution/import",
              "scope": "delta=5/4, N2..63 exact input and PSD certificates; uniform N>=64 is separately reconstructed in owned audit",
              "utc": datetime.now(timezone.utc).isoformat(),
              "adapted_source": "work/cycle6/c02_s01/axial/independent_delta1_verifier.py",
              "adapted_source_sha256": "3e62034789ebdd0cc9de0a52e743430077e6356cfaa075bfc9d170075c81892c",
              "rational_analytic_constants": rational_constant_checks()}
    result.update(verify(data))
    result["rejection_controls"] = rejection_controls(data)
    result["wall_seconds"] = time.perf_counter() - start
    output = OWN / "INDEPENDENT_DELTA5OVER4_CERTIFICATE_VERIFY.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "verified_input_q_intervals", "verified_matrices",
          "verified_pivots", "verified_strict_lower_entries", "wall_seconds")}, indent=2))


if __name__ == "__main__":
    main()
