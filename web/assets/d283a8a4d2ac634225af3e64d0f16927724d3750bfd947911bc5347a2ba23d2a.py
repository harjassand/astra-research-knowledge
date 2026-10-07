#!/usr/bin/env python3
"""Independent rational audit of delivered symmetric/whole Gibbs ensembles.

Imports no peer code. Reacquires exponentials by alternating exp(-y) bounds,
then directed dyadic squaring. Whole N<=3 targets use the symmetric projector
and its orthogonal complement, independently of the author's J^2 constructor.
"""
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import math
import time

OWN = Path(__file__).resolve().parent
ROOT = OWN.parents[4]
PEER = ROOT / "work/cycle6/c03_s01/implementation"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def rational(record):
    return Q(int(record["numerator"]), int(record["denominator"]))


def encode(x):
    return {"numerator": str(x.numerator), "denominator": str(x.denominator)}


def dyadic_floor(x, bits):
    scale = 2 ** bits
    return Q((x.numerator * scale) // x.denominator, scale)


def dyadic_ceil(x, bits):
    scale = 2 ** bits
    z = x.numerator * scale
    return Q(-((-z) // x.denominator), scale)


@lru_cache(maxsize=8192)
def independent_exp_minus(x, precision=256):
    need(x >= 0, "negative input exponent")
    if x == 0:
        return Q(1), Q(1)
    y, steps = x, 0
    while y > Q(1, 8):
        y /= 2
        steps += 1
    working = precision + steps + 12
    threshold = Q(1, 2 ** (working + 8))
    term = total = even = Q(1)
    j = 0
    while True:
        j += 1
        term *= y / j
        total += (-1 if j % 2 else 1) * term
        if j % 2 == 0:
            even = total
        elif term < threshold:
            break
    lo, hi = dyadic_floor(total, working), dyadic_ceil(even, working)
    need(0 <= lo <= hi <= 1, "invalid alternating exp input bracket")
    for _ in range(steps):
        lo = dyadic_floor(lo * lo, working)
        hi = min(Q(1), dyadic_ceil(hi * hi, working))
    need(hi - lo < Q(1, 2 ** precision), "independent exponential width failed")
    return lo, hi


def interval_divide(a, positive):
    need(positive[0] > 0, "nonpositive normalization interval")
    corners = [x / y for x in a for y in positive]
    return min(corners), max(corners)


@lru_cache(maxsize=2048)
def normalized_target(n, delta, h):
    logs = [(-delta * Q((2 * k - n) ** 2, 4 * n) + h * Q(2 * k - n, 2))
            if n else Q(0) for k in range(n + 1)]
    top = max(logs)
    values = [independent_exp_minus(top - x) for x in logs]
    normalizer = sum(a for a, _ in values), sum(b for _, b in values)
    need(normalizer[0] >= 1, "shifted symmetric denominator lower bound failed")
    return [interval_divide(v, normalizer) for v in values]


@lru_cache(maxsize=512)
def candidate_populations(n, bits, nodes, weights):
    scale = 2 ** bits
    need(len(nodes) == len(weights) > 0, "invalid node/weight count")
    need(all(0 <= x <= scale for x in nodes), "node outside support")
    need(all(w >= 0 for w in weights) and sum(weights) == scale,
         "weights are not a nonnegative dyadic simplex")
    result = []
    common = scale ** (n + 1)
    for k in range(n + 1):
        numerator = sum(w * math.comb(n, k) * x ** k * (scale - x) ** (n - k)
                        for x, w in zip(nodes, weights))
        result.append(Q(numerator, common))
    need(sum(result) == 1 and min(result) >= 0, "candidate populations invalid")
    return tuple(result)


def phase_parameters(n, bits):
    modulus = n + 1
    if modulus & (modulus - 1) == 0:
        return (modulus - 1).bit_length(), Q(0)
    return bits, Q(modulus, 2 ** (bits + 1))


def verify_symmetric(model):
    n, bits = model["n"], model["node_weight_bits"]
    need(isinstance(n, int) and 0 <= n <= 64 and isinstance(bits, int) and bits > 0,
         "illegal implementation size/bit scope")
    delta, h, epsilon = map(rational, (model["delta"], model["h"], model["epsilon"]))
    need(0 <= delta <= 1 and 0 < epsilon < 1, "illegal symmetric parameter scope")
    need(model["phase_modulus"] == n + 1, "phase modulus does not match n+1")
    nodes = tuple(int(x) for x in model["node_integers"])
    weights = tuple(int(x) for x in model["weight_integers"])
    candidate = candidate_populations(n, bits, nodes, weights)
    cert = model["certificate"]
    claimed = rational(cert["target_trace_distance_upper"])
    if cert["kind"] == "EXACT_ENDPOINT_TAIL_CERTIFICATE":
        b = cert["threshold_bits"]
        need(n > 0 and b > 0 and abs(h) - delta >= b, "invalid endpoint cutoff")
        endpoint = n if h >= 0 else 0
        need(candidate[endpoint] == 1, "endpoint branch does not output the endpoint")
        acquired_bound = Q(1, 2 ** b - 1)
    else:
        need(cert["kind"] == "EXACT_RATIONAL_POSTERIOR_CERTIFICATE", "unknown posterior kind")
        target = normalized_target(n, delta, h)
        individual = [max(abs(q - a), abs(q - b)) for q, (a, b) in zip(candidate, target)]
        acquired_bound = sum(individual) / 2
        need(2 * acquired_bound <= rational(cert["population_l1_upper"]), "population L1 certificate false")
        need(max(individual) <= rational(cert["max_population_error_upper"]), "population maximum certificate false")
    need(acquired_bound <= claimed, "independently acquired symmetric trace bound exceeds certificate")
    density_bits = model["density_bits"]
    need(isinstance(density_bits, int) and density_bits > 0, "invalid finite density precision")
    density = Q(8 * n, 2 ** density_bits)
    pb, phase = phase_parameters(n, bits)
    need(pb == model["phase_sampling_bits"], "phase random-bit count inconsistent")
    need(model["predetermined_random_bits_per_sample"] == bits + pb, "sample random budget inconsistent")
    need(phase <= rational(model["phase_uniform_TV_upper"]), "phase TV underreported")
    need(density <= rational(model["finite_density_trace_distance_upper"]), "local density error underreported")
    bound = claimed + density + phase
    need(bound <= rational(model["total_output_trace_distance_upper"]) <= epsilon,
         "symmetric total trace bound false")
    return candidate, {"n": n, "delta": encode(delta), "h": encode(h),
            "independent_trace_distance_upper": encode(acquired_bound),
            "claimed_trace_distance_upper": encode(claimed),
            "fair_bits": bits + pb, "certificate_kind": cert["kind"]}


def whole_candidate(N, branches, inner_populations):
    size = 2 ** N
    result = [[Q(0) for _ in range(size)] for _ in range(size)]
    for branch, population in zip(branches, inner_populations):
        k, u, mass = branch["k"], branch["u"], rational(branch["probability"])
        need(0 <= k <= N and 0 <= u <= N - k, "invalid physical subset type")
        for subset in combinations(range(N), k):
            complement = [site for site in range(N) if site not in subset]
            for one_sites in combinations(complement, u):
                offset = sum(2 ** site for site in one_sites)
                for ell in range(k + 1):
                    basis = [offset + sum(2 ** site for site in excitations)
                             for excitations in combinations(subset, ell)]
                    entry = mass * population[ell] / (math.comb(N, k) * math.comb(N - k, u)
                                                     * math.comb(k, ell))
                    for a in basis:
                        for b in basis:
                            result[a][b] += entry
    need(sum(result[i][i] for i in range(size)) == 1, "whole candidate not trace one")
    return result


def independent_whole_target(N, alpha, delta, h):
    """N<=3: only the symmetric spin and its complementary spin occur.

    Within each Hamming block, P_sym is the all-ones matrix/binom(N,k),
    while the other projector is I-P_sym. No peer J^2 or projector data used.
    """
    need(1 <= N <= 3, "whole finite fixture scope exceeded")
    upper_spin = Q(N, 2)
    upper_eigen = upper_spin * (upper_spin + 1)
    lower_spin = upper_spin - 1
    lower_eigen = lower_spin * (lower_spin + 1)
    records = []
    for k in range(N + 1):
        dim, m = math.comb(N, k), Q(2 * k - N, 2)
        common = -delta * m * m / N + h * m
        records.append((k, "symmetric", 1, alpha * upper_eigen / N + common))
        if dim > 1:
            records.append((k, "complement", dim - 1, alpha * lower_eigen / N + common))
    top = max(x[3] for x in records)
    values = {(k, kind): independent_exp_minus(top - exponent)
              for k, kind, _, exponent in records}
    normalizer = (sum(mult * values[k, kind][0] for k, kind, mult, _ in records),
                  sum(mult * values[k, kind][1] for k, kind, mult, _ in records))
    size = 2 ** N
    result = []
    for i in range(size):
        row = []
        for j in range(size):
            k = i.bit_count()
            if k != j.bit_count():
                row.append((Q(0), Q(0)))
                continue
            dim = math.comb(N, k)
            a, b = values[k, "symmetric"]
            lo, hi = a / dim, b / dim
            if dim > 1:
                coefficient = Q(int(i == j)) - Q(1, dim)
                a, b = values[k, "complement"]
                lo += coefficient * (a if coefficient >= 0 else b)
                hi += coefficient * (b if coefficient >= 0 else a)
            row.append(interval_divide((lo, hi), normalizer))
        result.append(row)
    return result


def verify_local_density(local):
    a, b = map(rational, local["diagonal"])
    re, im = map(rational, (local["upper_right_real"], local["upper_right_imag"]))
    need(a >= 0 and b >= 0 and a + b == 1 and re * re + im * im <= a * b,
         "sampled local density is not exact PSD trace one")


def verify_whole(record):
    N = record["N"]
    def param(name):
        return rational(record[name]) if isinstance(record[name], dict) else Q(record[name])
    alpha, delta, h, epsilon = map(param, ("alpha", "delta", "h", "epsilon"))
    reconstructed = "branches" not in record
    if reconstructed:
        # Earlier bounded receipts saved all acquisition data, but omitted the
        # rounded branch vector. Reconstruct its exact documented floor/last-
        # residual law from those saved rational inputs, without peer imports.
        weights = [rational(x) for x in record["K_weights"]]
        values = [rational(x) for x in record["branch_metadata"]["N_exponential_values"]]
        need(len(weights) == len(values) == N + 1 and min(weights) >= 0 and sum(weights) == 1,
             "saved branch reconstruction data invalid")
        branches, raw_masses = [], []
        for k in range(N + 1):
            for u in range(N - k + 1):
                branches.append({"k": k, "u": u})
                raw_masses.append(weights[k] * Q(math.comb(N - k, u), (k + 1) * 2 ** (N - k))
                                  * sum(values[u:u + k + 1]))
        normalizer = sum(raw_masses)
        need(normalizer == rational(record["branch_metadata"]["scaled_normalizer"]),
             "saved branch normalizer does not reconstruct")
        scale = 2 ** record["branch_metadata"]["outer_bits"]
        masses = [dyadic_floor(raw / normalizer, record["branch_metadata"]["outer_bits"])
                  for raw in raw_masses[:-1]]
        masses.append(1 - sum(masses))
        for branch, mass in zip(branches, masses):
            branch["probability"] = encode(mass)
    else:
        branches = record["branches"]
    models = record["Dicke_models"]
    need(len(branches) == len(models), "conditional model count mismatch")
    probabilities = [rational(b["probability"]) for b in branches]
    need(min(probabilities) >= 0 and sum(probabilities) == 1, "whole branch simplex false")
    need(all(p.denominator & (p.denominator - 1) == 0 for p in probabilities),
         "whole branch weights not exact finite-bit dyadics")
    populations, inner_reports = [], []
    for branch, model in zip(branches, models):
        k, u = branch["k"], branch["u"]
        need(model["n"] == k, "conditional physical site count mismatch")
        m = Q(2 * u - (N - k), 2)
        need(rational(model["delta"]) == delta * Q(k, N), "wrong subset axial parameter")
        need(rational(model["h"]) == h - 2 * delta * m / N, "wrong conditional field")
        p, receipt = verify_symmetric(model)
        populations.append(p)
        inner_reports.append(receipt)
    candidate = whole_candidate(N, branches, populations)
    target = independent_whole_target(N, alpha, delta, h)
    raw = sum(max(abs(candidate[i][j] - target[i][j][0]), abs(candidate[i][j] - target[i][j][1]))
              for i in range(2 ** N) for j in range(2 ** N)) / 2
    matrix_name = ("full_matrix_trace_distance_upper" if "full_matrix_trace_distance_upper" in record
                   else "full_matrix_rational_certificate_trace_distance_upper")
    need(raw <= rational(record[matrix_name]), "independent whole matrix certificate fails")
    rank_bits = record.get("uniform_rank_bits", 128)
    need(rank_bits >= 0, "negative rank bits")
    preparation = Q(0)
    for branch, model, mass in zip(branches, models, probabilities):
        k, u = branch["k"], branch["u"]
        _, phase = phase_parameters(k, model["node_weight_bits"])
        density = Q(8 * k, 2 ** model["density_bits"])
        preparation += mass * (Q(math.comb(N, k) + math.comb(N - k, u), 2 ** (rank_bits + 1))
                               + phase + density)
    need(preparation <= rational(record["finite_sampler_additional_error_upper"]),
         "whole finite-sampler error underreported")
    total = rational(record[matrix_name]) + preparation
    need(total <= rational(record["total_target_trace_distance_upper"]) <= epsilon,
         "whole physical target bound false")
    samples = record.get("samples", [])
    for sample in samples:
        for density in sample["local_density_matrices"]:
            verify_local_density(density)
    outer_bits = max(p.denominator.bit_length() - 1 for p in probabilities)
    max_inner = max(x["fair_bits"] for x in inner_reports)
    max_random_budget = outer_bits + 2 * rank_bits + max_inner
    if "predetermined_random_bits_per_sample" in record:
        need(record["outer_sampling_bits"] == outer_bits and record["max_inner_sampling_bits"] == max_inner
             and record["predetermined_random_bits_per_sample"] == max_random_budget,
             "whole predetermined random budget inconsistent")
        for sample in samples:
            need(sample["random_bits_consumed"] == max_random_budget,
                 "sample reports wrong whole random budget")
    return {"N": N, "alpha": encode(alpha), "delta": encode(delta), "h": encode(h),
            "branches": len(branches), "independent_matrix_trace_distance_upper": encode(raw),
            "branch_law_reconstructed_from_saved_rational_acquisition": reconstructed,
            "matrix_certificate_upper": record[matrix_name],
            "finite_sampler_additional_error_upper": encode(preparation),
            "predetermined_max_fair_bits": max_random_budget,
            "verified_sample_local_densities": sum(len(s["local_density_matrices"]) for s in samples)}


def load_source(filename):
    raw = (PEER / filename).read_bytes()
    return json.loads(raw), {"path": str(PEER / filename), "sha256": sha256(raw).hexdigest(),
                             "bytes": len(raw)}


def main():
    start = time.perf_counter()
    sources, symmetric_reports, whole_reports = [], [], []
    for filename in ("certified_models.json", "delta1_checks.json"):
        data, fingerprint = load_source(filename)
        sources.append(fingerprint)
        for model in data["models"]:
            _, receipt = verify_symmetric(model)
            receipt["source"] = filename
            symmetric_reports.append(receipt)
    for filename in ("finite_alpha_checks.json", "finite_alpha_delta1_checks.json"):
        data, fingerprint = load_source(filename)
        sources.append(fingerprint)
        for record in data["records"]:
            receipt = verify_whole(record)
            receipt["source"] = filename
            whole_reports.append(receipt)
    data, fingerprint = load_source("whole_gibbs_sampler.json")
    sources.append(fingerprint)
    model = deepcopy(data["model"])
    model["samples"] = data["samples"]
    receipt = verify_whole(model)
    receipt["source"] = "whole_gibbs_sampler.json"
    whole_reports.append(receipt)
    data, fingerprint = load_source("whole_api_checks.json")
    sources.append(fingerprint)
    for example in data["examples"]:
        model = deepcopy(example["model"])
        model["samples"] = example["samples"]
        receipt = verify_whole(model)
        receipt["source"] = "whole_api_checks.json"
        whole_reports.append(receipt)
    # This corruption passed the originally reviewed author verifier.
    data, _ = load_source("delta1_checks.json")
    corrupt = deepcopy(next(m for m in data["models"] if m["n"] == 8))
    corrupt["phase_modulus"] = 1
    try:
        verify_symmetric(corrupt)
    except ValueError as error:
        rejection = {"phase_modulus_corruption": "REJECTED", "reason": str(error)}
    else:
        raise ValueError("own independent checker accepted the phase counterexample")
    result = {"status": "PASS unmutated delivered outputs independently verified",
              "utc": datetime.now(timezone.utc).isoformat(),
              "method": "no peer imports or execution; different exact exp acquisition; N<=3 symmetric/complement projectors for whole target",
              "code_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "sources": sources, "symmetric_models": len(symmetric_reports),
              "whole_integrations": len(whole_reports),
              "whole_delta1_integrations": sum(Q(int(x["delta"]["numerator"]), int(x["delta"]["denominator"])) == 1
                                               for x in whole_reports),
              "symmetric_reports": symmetric_reports, "whole_reports": whole_reports,
              "rejection_control": rejection,
              "limitations": "proves delivered finite posterior outputs only; generic bit-complexity proof audited separately; local density approximation reviewed analytically, sampled matrices also tested exactly",
              "wall_seconds": time.perf_counter() - start}
    (OWN / "INDEPENDENT_POSTERIOR_VERIFY.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "symmetric_models", "whole_integrations",
                                           "whole_delta1_integrations", "wall_seconds")}, indent=2))


if __name__ == "__main__":
    main()
