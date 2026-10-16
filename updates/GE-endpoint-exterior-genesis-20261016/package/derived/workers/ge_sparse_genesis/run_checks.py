"""Bounded deterministic tests and complete witness delivery; own code only."""
from copy import deepcopy
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
import platform
import resource
import sys
import time

from erlang_certificate import certify
from check_receipts import check, independently_build_killed

BASE = Path(__file__).resolve().parent
ORIGINALS = BASE.parent.parent / "originals"


def dense_rational_solve(a, b):
    """Independent exact Gaussian elimination for bounded reference checks."""
    n = len(b)
    m = [[F(x) for x in row] + [F(rhs)] for row, rhs in zip(a, b)]
    for j in range(n):
        assert m[j][j]
        for i in range(j + 1, n):
            multiplier = m[i][j] / m[j][j]
            for ell in range(j, n + 1):
                m[i][ell] -= multiplier * m[j][ell]
    answer = [F(0)] * n
    for i in range(n - 1, -1, -1):
        answer[i] = (m[i][-1] - sum(m[i][j] * answer[j] for j in range(i + 1, n))) / m[i][i]
    return answer


def reference_checks():
    coordinates = 0
    cases = 0
    for n in range(3, 7):
        for topology in ["path", "star"]:
            edges = [(j, j + 1) for j in range(n - 1)] if topology == "path" else [(0, j) for j in range(1, n)]
            rates = [(j + 1) ** 2 for j in range(len(edges))]
            if n % 2:
                rates[0] = 0
            if topology == "star":
                rates[-1] = 10 ** 15
            comparison = [r + (j % 2) * 7 for j, r in enumerate(rates)]
            data = certify(n, edges, rates, comparison, shape=4, shift=5)
            check(data)
            for r, witnesses, residuals in zip([rates, comparison], data["dyadic_solve_witnesses"], data["residual_receipts"]):
                h, _ = independently_build_killed(n, edges, r)
                d = len(h)
                a = [[h[i].get(j, 0) + (5 if i == j else 0) for j in range(d)] for i in range(d)]
                true = [F(1)] * d
                q = 1 << data["precision_bits"]
                for v, receipt in zip(witnesses, residuals):
                    true = dense_rational_solve(a, [5 * x for x in true])
                    e = F(receipt["accumulated_error_exact"])
                    assert all(abs(t - F(z, q)) <= e for t, z in zip(true, v))
                    coordinates += d
            cases += 1
    invalid = [
        (3, [(0, 1)], [-1]),
        (3, [(0, 1)], [F(1, 2)]),
        (3, [(0, 1), (1, 0)], [1, 1]),
    ]
    for n, e, r in invalid:
        try:
            certify(n, e, r, r, shape=4)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid input accepted")
    return dict(exact_reference_graphs=cases, exact_reference_component_enclosures=coordinates,
                invalid_inputs_rejected=len(invalid), disconnected_zero_rate_case=True)


def write_case(name, n, edges, r, q):
    begin = time.perf_counter()
    data = certify(n, edges, r, q, shape=16, shift=20)
    data["case"] = name
    data["proposer_sha256"] = hashlib.sha256((BASE / "erlang_certificate.py").read_bytes()).hexdigest()
    target = BASE / (name + "_certified.json")
    target.write_text(json.dumps(data, indent=2) + "\n")
    generation_delivery = time.perf_counter() - begin
    independent = check(json.loads(target.read_text()))
    return data, dict(case=name, receipt=target.name, receipt_bytes=target.stat().st_size,
                      receipt_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                      generation_and_delivery_seconds=generation_delivery,
                      independent_checker=independent)


def main():
    begin = time.perf_counter()
    source_files = [ORIGINALS / "exterior/interchange_path_exterior/exterior_receipt.json",
                    ORIGINALS / "pair/fair_bit_sampler_results.json"]
    input_hashes = {str(p.relative_to(ORIGINALS)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files}
    n = 20
    path = [(j, j + 1) for j in range(n - 1)]
    source, sr = write_case("source20", n, path, [10 ** j for j in range(n - 1)], [1, 10] + [10 ** n] * (n - 3))
    branch = [(0, 1), (1, 2), (2, 3), (2, 4), (2, 5)]
    branching, br = write_case("branch6", 6, branch, [1, 10, 100, 1000, 10000], [1, 10, 1000000, 1000000, 1000000])
    ungapped, ur = write_case("ungapped6", 6, branch, [1] * 5, [1, 1, 1000000, 1000000, 1000000])
    assert source["finite_generator_certified"] and branching["finite_generator_certified"]
    assert not ungapped["finite_generator_certified"]
    corrupt = deepcopy(source)
    corrupt["dyadic_solve_witnesses"][0][0][0] += 1 << corrupt["precision_bits"]
    try:
        check(corrupt)
    except AssertionError:
        corruption_rejected = True
    else:
        raise AssertionError("corrupted witness accepted")
    ref = reference_checks()
    # Read exact source errors as DATA; execute no original source module.
    inherited20 = json.loads(source_files[0].read_text())
    inherited6 = json.loads(source_files[1].read_text())
    compositions = []
    for label, data, tail, sampling, reason in [
        ("source20", source, F(inherited20["classical_tail_exact"]), F(inherited20["sampler_error_exact"]),
         "unchanged receiving 18-site fast-path Aldous tail and n=20 finite-bit boundary-shuffle sampler"),
        ("branch6", branching, F(241, 1000000), F(inherited6["total_sampler_TV_bound"]),
         "fast four-star gap W via receiving Aldous equality; tail<=1/W+10(10+2)*2/W; same n=6 boundary-shuffle sampler"),
    ]:
        upper = F(data["Duhamel_upper_exact"]) + tail + sampling
        assert upper <= F(1, 20)
        compositions.append(dict(case=label, Duhamel_upper_exact=data["Duhamel_upper_exact"],
                                 classical_averaging_tail_exact=str(tail), finite_bit_sampler_error_exact=str(sampling),
                                 total_full_endpoint_TV_upper_exact=str(upper), total_upper_float=float(upper),
                                 certified=True, inherited_contract=reason,
                                 certificate_scope="uniform initial permutation and every color projection, horizon 1; independent fair-bit sampler assumption"))
    comp = BASE / "full_sampler_compositions.json"
    comp.write_text(json.dumps(compositions, indent=2) + "\n")
    unchanged = all(hashlib.sha256(p.read_bytes()).hexdigest() == input_hashes[str(p.relative_to(ORIGINALS))] for p in source_files)
    assert unchanged
    receipt = dict(status="bounded checks passed; no general superiority or physical claim",
                   run_time_seconds=time.perf_counter() - begin, python=sys.version,
                   platform=platform.platform(), peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   cases=[sr, br, ur], reference_checks=ref, corrupted_witness_rejected=corruption_rejected,
                   full_sampler_totals=[dict(case=c["case"], upper=c["total_upper_float"]) for c in compositions],
                   source_data_sha256=input_hashes, source_data_unchanged=unchanged,
                   source_code_executed=False, third_party_fulltexts_used=False, packages_installed=False)
    (BASE / "bounded_check_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: receipt[k] for k in ["status", "run_time_seconds", "reference_checks", "corrupted_witness_rejected", "full_sampler_totals"]}), flush=True)


if __name__ == "__main__":
    main()
