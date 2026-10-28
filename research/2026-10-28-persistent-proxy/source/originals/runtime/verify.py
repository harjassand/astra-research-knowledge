"""Exact finite certificates; this is not a general theorem or novelty audit."""
from fractions import Fraction as F
from itertools import product as cartesian_product
from pathlib import Path
from math import comb
import hashlib
import json
import platform
import resource
import time

from operation import (matrix, product, compile_by_classifier, compositions,
                       type_probability, source_two_proxy_output,
                       common_part_output)

ROOT = Path(__file__).resolve().parent


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def subtract(a, b):
    return [[v - w for v, w in zip(arow, brow)] for arow, brow in zip(a, b)]


def tv_columns(a, b):
    return [sum(abs(a[y][x] - b[y][x]) for y in range(len(a))) / 2
            for x in range(len(a[0]))]


def exact_rank(a):
    a = [row[:] for row in a]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        divisor = a[row][col]
        a[row] = [v / divisor for v in a[row]]
        for i in range(row + 1, len(a)):
            scale = a[i][col]
            a[i] = [v - scale * w for v, w in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def main():
    started = time.perf_counter()
    artifact = json.loads((ROOT / "NONDEGRADED_COMPILED.json").read_text())
    k, ell, u = map(matrix, (artifact["K"], artifact["L"], artifact["U"]))
    expected_hashes = {
        "PROOF.md": "33007e1215fd91118e35be36b07b50ea3096b936b3c33c8e519b058d50ad4eb9",
        "RESULT.md": "126d5df6dda1108cc543320ae854400a5689ac222b759d50601d1fed30e253f5",
        "SEQUENTIAL_REVIEW.md": "4a02a45016e38c65fb873e2a482fed5e66023101b30366c391b9ba842e658ebe",
        "NONDEGRADED_COMPILED.json": "463bb5721b11f0a63d3e236ff992daca34da9e2bbf4ac63b92f08ce11415f984",
    }
    assert all(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected
               for name, expected in expected_hashes.items())
    for a in (k, ell):
        assert all(v >= 0 for row in a for v in row)
        assert all(sum(row[x] for row in a) == 1 for x in range(3))
    residual = subtract(k, product(u, ell))
    q_inputs = [1 - sum(product(u, ell)[y][x] for y in range(3))
                for x in range(3)]
    assert all(v >= 0 for row in residual for v in row)
    assert q_inputs == [F(3, 40)] * 3

    # Independently check the displayed exact dual, not a solver status string.
    alpha = matrix([[F(5, 2), 0, 0], [0, F(1, 2), F(1, 2)],
                    [0, F(1, 2), F(1, 2)]])
    pi = [F(0), F(1, 2), F(1, 2)]
    dual_slacks = [[sum((alpha[y][x] - pi[x]) * ell[z][x]
                           for x in range(3)) for z in range(3)]
                   for y in range(3)]
    dual_bound = 1 - sum(alpha[y][x] * k[y][x]
                         for y in range(3) for x in range(3))
    assert all(v >= 0 for row in dual_slacks for v in row)
    assert dual_bound == F(3, 40)

    h2 = [[comb(2, c) * ell[0][x] ** c * (1 - ell[0][x]) ** (2 - c)
           for x in range(3)] for c in range(3)]
    v2 = matrix([[F(13, 25), F(17, 100), 0],
                 [F(6, 25), F(83, 200), F(1, 2)],
                 [F(6, 25), F(83, 200), F(1, 2)]])
    assert product(v2, h2) == k
    assert all(sum(row[c] for row in v2) == 1 for c in range(3))
    classifier_runs = []
    for r in (1, 2):
        compiled = compile_by_classifier(k, ell, r)
        assert compiled["identity_checked"]
        assert compiled["stochastic"] == (r == 2)
        classifier_runs.append({key: compiled[key] for key in
                                ("repeats", "confusion", "post", "stochastic")})

    common = [min(row) for row in k]
    common_q = 1 - sum(common)
    assert common_q == F(11, 40)
    common_residual = [[(row[x] - b) / common_q for x in range(3)]
                       for row, b in zip(k, common)]
    assert all(v >= 0 for row in common_residual for v in row)
    assert all(sum(row[x] for row in common_residual) == 1 for x in range(3))
    assert [[b + common_q * row[x] for x in range(3)]
            for b, row in zip(common, common_residual)] == k

    drifts = []
    for delta in (F(1, 600), F(-1, 600), F(1, 60000), F(-1, 60000)):
        drift = [[ell[z][x] + (delta if z == 0 else -delta / 2)
                  for x in range(3)] for z in range(3)]
        drift_h = [[comb(2, c) * drift[0][x] ** c * (1 - drift[0][x]) ** (2 - c)
                    for x in range(3)] for c in range(3)]
        actual_two = product(v2, drift_h)
        nominal_runtime = [[v + d for v, d in zip(arow, drow)]
                           for arow, drow in zip(product(u, drift), residual)]
        assert all(error > 0 for error in tv_columns(actual_two, k))
        assert tv_columns(nominal_runtime, k) == [F(2, 5) * abs(delta)] * 3
        drifts.append({"signed_delta": delta,
                       "input_channel_tv": tv_columns(drift, ell),
                       "two_record_output_tv": tv_columns(actual_two, k),
                       "one_record_nominal_runtime_tv": tv_columns(nominal_runtime, k)})

    # Finite unisolvent calibration sets, wholly inside TV radius 1/600.
    interpolation = []
    for budget in range(1, 5):
        types = list(compositions(budget, 3))
        step = F(1, 600 * budget)
        for x in range(3):
            base = [ell[z][x] for z in range(3)]
            points = [[base[0] + step * i, base[1] + step * j,
                       base[2] - step * (i + j)]
                      for i in range(budget + 1)
                      for j in range(budget + 1 - i)]
            assert all(min(p) > 0 and sum(p) == 1 for p in points)
            assert max(sum(abs(a - b) for a, b in zip(p, base)) / 2
                       for p in points) <= F(1, 600)
            evaluation = [[type_probability(t, p) for t in types] for p in points]
            rank = exact_rank(evaluation)
            assert rank == len(types) == comb(budget + 2, 2)
            interpolation.append({"budget": budget, "input": x,
                                  "types": len(types), "rank": rank,
                                  "max_tv_radius": F(1, 600)})

    # A smooth ordinary Bernoulli-factory escape: certify its rational formula,
    # endpoint derivatives, range, and that the source uncertainty is on plateaux.
    # General factory existence/rate is imported from Holtz-Nazarov-Peres Thm 8;
    # no factory implementation or measured expected runtime is claimed here.
    smoothstep = [F(0), F(0), F(0), F(10), F(-15), F(6)]
    def derivative(coefficients):
        return [i * c for i, c in enumerate(coefficients)][1:]
    def evaluate(coefficients, x):
        return sum((c * x ** i for i, c in enumerate(coefficients)), F(0))
    d1, d2 = derivative(smoothstep), derivative(derivative(smoothstep))
    assert evaluate(smoothstep, F(0)) == 0
    assert evaluate(smoothstep, F(1)) == 1
    assert all(evaluate(d, endpoint) == 0 for d in (d1, d2)
               for endpoint in (F(0), F(1)))
    assert d1 == [F(0), F(0), F(30), F(-60), F(30)]
    assert F(1, 6) + F(1, 600) < F(1, 4)
    assert F(2, 3) - F(1, 600) > F(7, 12)

    # Runtime callback audit on every proxy word. No statistical success rate.
    class FixedBits:
        def getrandbits(self, bits):
            return 0
    callback_checks = 0
    for word in cartesian_product(range(3), repeat=2):
        seen = []
        def proxy():
            z = word[len(seen)]
            seen.append(z)
            return z
        result = source_two_proxy_output(proxy, FixedBits())
        assert len(seen) == 2 and result in (0, 1, 2)
        callback_checks += 1
    raw_calls = []
    def raw():
        raw_calls.append(1)
        return 0
    common_part_output(k, raw, FixedBits())
    assert not raw_calls  # The no-read branch does not invoke an already-paid raw service.

    result = {
        "status": "EXACT_SCOPED_CERTIFICATES_PASS; NO_NOVELTY_OR_PRACTICAL_ADVANTAGE_CLAIM",
        "pin": "e1e2272165c8548326c31bb11817c28f871d21e9",
        "source_hashes_checked": expected_hashes,
        "one_record": {"q": q_inputs, "dual_bound": dual_bound,
                       "dual_slacks": dual_slacks},
        "two_record": {"q": F(0), "cheap_calls": 2, "count_channel": h2,
                       "postprocessor": v2, "output_channel": product(v2, h2),
                       "zero_raw_minimum_fixed_cheap_calls": 2,
                       "callback_paths_checked": callback_checks},
        "ordinary_classifier_inversion": classifier_runs,
        "fixed_finite_budget_open_uncertainty": {
            "q_lower_and_attained": common_q,
            "common_subdistribution": common,
            "raw_residual_distribution": common_residual,
            "scope": "Any finite hard cheap-call budget B; proof in PROOF_EXTENSION.md. Not an unbounded-stopping lower bound.",
            "finite_interpolation_checks": interpolation},
        "drift_counterexamples": drifts,
        "unbounded_ordinary_escape": {
            "source": "https://arxiv.org/pdf/0808.1936",
            "theorem": 8, "smoothness_exponent": "5/2",
            "tail_order": "O(n^(-5/4))", "finite_expected_cheap_calls": True,
            "raw_q": F(0),
            "implementation": "Explicit rational factory.py and margin-sensitive factory_lazy.py now implemented; factory/lazy_verification_results.json carry their separate scoped finite checks. General derivations are pending independent review.",
            "transition": [F(1, 4), F(7, 12)],
            "low_plateau": F(49, 120), "high_plateau": F(2, 15),
            "smoothstep_coefficients": smoothstep},
        "runtime": {"python": platform.python_version(),
                    "wall_s": time.perf_counter() - started,
                    "peak_rss_bytes_macos": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
    }
    (ROOT / "verification_results.json").write_text(json.dumps(encode(result), indent=2) + "\n")
    print(json.dumps(encode({"status": result["status"],
                             "q_one": F(3, 40), "q_two": F(0),
                             "q_bounded_robust": common_q,
                             "unbounded_robust_escape": "explicit ordinary factory and lazy repair implemented; computational-cost proof uses a positive stationary plateau margin",
                             "runtime": result["runtime"]}), indent=2))


if __name__ == "__main__":
    main()
