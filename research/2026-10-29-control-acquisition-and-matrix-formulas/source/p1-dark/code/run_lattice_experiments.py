"""Fresh finite-noise acquisition of complete laws and continuous decisions."""
from fractions import Fraction as F
from pathlib import Path
import json
import random
import sys
import time
import native_source as ns
import simplex_law as sl
import hypograph_control as hc

ROOT = Path(__file__).resolve().parents[1]
DELTA = F(1, 5)


def outward(interval, bits=48):
    scale = 1 << bits
    return F((interval[0] * scale).__floor__(), scale), F((interval[1] * scale).__ceil__(), scale)


def make_source(n, kind):
    if kind == "exact_pair":
        assert n == 2
        return ns.NativeSource([[1, 1], [0, 1]], label="exact_dark_pair")
    vectors = []
    for i in range(n):
        g = F(1) if i == 0 else (F(3, 4) if kind == "mixed" and i == n // 2 else F(0))
        b = [F(1), F(0), F(0), F(0)] if i < 2 else [
            F(((3 * i + 2 * j) % 5) - 2, 5) for j in range(4)]
        vectors.append([g] + b)
    return ns.NativeSource(vectors, label=f"{kind}_n{n}")


def heldout_commands(n, count=10):
    rng = random.Random(1009 + n)
    out = [[F(0)] * n]
    for j in range(count - 1):
        w = [rng.randrange(1, 10) for _ in range(n)]
        t = F((j % 5) + 1, 25)
        out.append([t * x / sum(w) for x in w])
    return out


def contains(iv, x):
    assert iv[0] <= x <= iv[1], (iv, x)


def verify_raw(source, oracle):
    for record in oracle.records:
        nominal = [F(0)] * source.n
        actual = nominal[:]
        for i, x in record["requested_sparse"]:
            nominal[i] = x
        for i, x in record["actual_sparse"]:
            actual[i] = x
        r = source.independent_response(actual)
        assert r == source.response(actual)
        contains(record["R_interval"], source.independent_response(nominal))
        assert abs(record["raw"] - (oracle._gain * r + oracle._offset)) <= oracle.read_error
    contains(oracle.alpha, oracle._gain)
    contains(oracle.beta, oracle._offset)


def run_case(n, degree, kind, eta, dac_bits=20, adc_bits=24):
    started = time.monotonic()
    source = make_source(n, kind)
    oracle = ns.CalibratedOracle(source, eta=eta, dac_bits=dac_bits,
                                adc_bits=adc_bits, G_bound=F(1),
                                Bdiag_bound=F(1), c0_lower=F(1, 2))
    law = sl.SimplexLaw(n, degree, G=F(1), kappa=F(1))
    raw_intervals = [outward(oracle.call(u)) for u in law.nodes]
    intervals = [outward((lo - F(3, 2), hi - F(3, 2))) for lo, hi in raw_intervals]
    law.ingest(intervals).transform()
    base_index = law.alphas.index((degree,) + (0,) * n)
    c_lower = max(F(1, 2), intervals[base_index][0])
    z_intervals = [outward((-1 / lo, -1 / hi)) for lo, hi in intervals]
    z_law = sl.SimplexLaw(n, degree, G=1 / c_lower, kappa=1 + 1 / c_lower)
    z_law.ingest(z_intervals).transform()
    source_count = len(oracle.records)
    heldout = heldout_commands(n)
    predictions = [{"u": u, "J": law.predict(u), "negative_Z": z_law.predict(u)} for u in heldout]
    tasks = []
    for utility in ("conductance", "compliance"):
        for task in range(3):
            if task == 0:
                prices = [F(17, 20) if i == 0 else F(0) for i in range(n)]
            elif task == 1:
                prices = [F((7 * i + 3) % 17, 40) for i in range(n)]
            else:
                prices = [F(0)] * n
            cert = hc.certify_task(law, prices, c_lower, dac_bits, utility)
            row = {"utility": utility, "task": task, "prices": prices, "certificate": cert}
            if utility == "compliance":
                row["direct_negative_Z_certificate_same_candidate"] = z_law.task_certificate(
                    prices, candidate=cert["candidate"]["command"])
            tasks.append(row)
    assert len(oracle.records) == source_count

    # Hidden source data only enters these post-decision checks.
    assert max(abs(v[0]) for v in source.vectors) <= 1
    assert max(ns.dot(v[1:], v[1:]) for v in source.vectors) <= 1
    dark = [i for i, v in enumerate(source.vectors) if v[0] == 0]
    assert dark
    for row in predictions:
        J = source.independent_response(row["u"]) - F(3, 2)
        for name, value in (("J", J), ("negative_Z", -1 / J)):
            for field in ("interpolation_interval", "bernstein_interval", "intersection_interval"):
                contains(row[name][field], value)
        row["checker_J"], row["checker_negative_Z"] = J, -1 / J
    for row in tasks:
        cert, prices = row["certificate"], row["prices"]
        x = cert["candidate"]["command"]
        Z, _, gradient_Zgain = source.state_and_gradient(x, prices)
        J = 1 / Z
        truth = hc.phi(J, row["utility"]) - ns.dot(prices, x)
        contains((cert["candidate"]["objective_lower_without_baseline"],
                  cert["global_objective_upper_without_baseline"]), truth)
        for option in cert["candidate_options"]:
            jo = source.independent_response(option["command"]) - F(3, 2)
            assert option["jensen_J_lower"] <= jo
            assert option["certified_J_lower"] <= jo
        for u in heldout:
            j = source.independent_response(u) - F(3, 2)
            assert hc.phi(j, row["utility"]) - ns.dot(prices, u) <= cert["global_objective_upper_without_baseline"]
        assert all((t * (1 << dac_bits)).denominator == 1 for t in x)
        row["checker_value_without_baseline"] = truth
        row["active_baseline_dark_controls"] = [i for i in dark if x[i]]
        if row["utility"] == "compliance":
            direct = row["direct_negative_Z_certificate_same_candidate"]
            contains((direct["candidate_lower_reward_without_baseline"],
                      direct["global_upper_reward_without_baseline"]), truth)
        # The exact pair has a known conductance-price optimum at (.09,.11).
        if kind == "exact_pair" and row["utility"] == "conductance" and row["task"] == 0:
            optimum = F(1) + F(27, 4000)
            actual_regret = optimum - truth
            assert 0 <= actual_regret <= cert["continuous_simplex_regret"]
            row["checker_exact_regret"] = actual_regret
    verify_raw(source, oracle)
    label = f"{kind}_n{n}_k{degree}_eta_{float(eta):.0e}_dac{dac_bits}"
    raw = {"scope": "Fresh synthetic source, no hardware operation.",
           "calibration": oracle.calibration, "alpha_interval": oracle.alpha,
           "beta_interval": oracle.beta, "raw_error_bound": eta,
           "warrants": {"G": F(1), "kappa": F(1), "c0_lower": F(1, 2)},
           "source_vectors_checker_only": source.vectors, "records": oracle.records,
           "J_intervals": intervals, "negative_Z_intervals": z_intervals}
    detail = {"label": label, "n": n, "degree": degree, "calibrated_c0_lower": c_lower,
              "baseline_dark_controls": dark, "J_uniform_bounds": law.uniform_bounds(),
              "negative_Z_uniform_bounds": z_law.uniform_bounds(),
              "J_bernstein_coefficients": law.bernstein_coefficients,
              "negative_Z_bernstein_coefficients": z_law.bernstein_coefficients,
              "ideal_costs": law.ideal_costs(), "physical_ledger": oracle.ledger(),
              "transform_cost": law.transform_cost, "predictions": predictions,
              "tasks": tasks, "all_exact_checks_passed": True,
              "seconds": round(time.monotonic() - started, 3)}
    (ROOT / "results" / (label + "_raw.json")).write_text(json.dumps(ns.jsonable(raw), separators=(",", ":")) + "\n")
    (ROOT / "results" / (label + "_results.json")).write_text(json.dumps(ns.jsonable(detail), indent=2) + "\n")
    summary = {"label": label, "total_readings": oracle.ledger()["total_scalar_readings"],
               "source_reactions": source_count, "dark_controls": len(dark),
               "J_interpolation_error": float(law.uniform_bounds()["interpolation_uniform_error"]),
               "J_positive_centered_error": float(law.uniform_bounds()["bernstein_centered_uniform_error"]),
               "negative_Z_interpolation_error": float(z_law.uniform_bounds()["interpolation_uniform_error"]),
               "later_source_readings": 0,
               "conductance_task_regrets": [float(t["certificate"]["continuous_simplex_regret"]) for t in tasks[:3]],
               "compliance_task_regrets": [float(t["certificate"]["continuous_simplex_regret"]) for t in tasks[3:]],
               "direct_compliance_regrets": [float(t["direct_negative_Z_certificate_same_candidate"]["continuous_simplex_regret"]) for t in tasks[3:]],
               "conductance_dark_active_counts": [len(t["active_baseline_dark_controls"]) for t in tasks[:3]],
               "seconds": detail["seconds"], "all_exact_checks_passed": True}
    print(json.dumps(summary), flush=True)
    return summary


def main():
    cases = [(2, 4, "exact_pair", F(1, 10**6)), (6, 3, "mixed", F(1, 10**6)),
             (6, 4, "mixed", F(1, 10**6)), (12, 3, "mostly_dark", F(1, 10**6)),
             (6, 4, "mixed", F(1, 10**3))]
    if len(sys.argv) > 1:
        cases = cases[:int(sys.argv[1])]
    rows = [run_case(*case) for case in cases]
    result = {"scope": "Calibrated full-law acquisition and continuous nonlinear control.",
              "comparator": "An equally informed conventional lattice/hypograph method can use the identical construction.",
              "cases": rows}
    tmp = ROOT / "results/LATTICE_RESULTS.json.tmp"
    tmp.write_text(json.dumps(result, indent=2) + "\n")
    tmp.replace(ROOT / "results/LATTICE_RESULTS.json")


if __name__ == "__main__":
    main()
