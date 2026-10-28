"""Refine the saved finite-lattice records; acquire no additional readings."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from math import prod
import json
import sys
import time
import native_source as ns
import simplex_law as sl
import hypograph_control as hc
from polynomial_curvature import CurvatureLaw, multinomial

ROOT = Path(__file__).resolve().parents[1]


def decoded(value):
    if isinstance(value, dict):
        return {k: decoded(v) for k, v in value.items()}
    if isinstance(value, list):
        return [decoded(v) for v in value]
    if isinstance(value, str):
        try:
            return F(value)
        except ValueError:
            return value
    return value


def independent_derivatives(curve, u):
    """Differentiate original monomials, independently of difference coefficients."""
    law = curve.law
    lam = [1 - sum(u) / law.delta] + [x / law.delta for x in u]

    def partial(alpha, indices):
        powers, multiplier = list(alpha), F(1)
        for j in indices:
            multiplier *= powers[j]
            powers[j] -= 1
            if not multiplier:
                return F(0)
        return multiplier * prod(x**a for x, a in zip(lam, powers))

    coefficients = [b * multinomial(a) for a, b in zip(law.alphas, law.bernstein_coefficients)]
    value = sum((b * partial(a, []) for a, b in zip(law.alphas, coefficients)), F(0))
    gradient = [sum((b * (partial(a, [i + 1]) - partial(a, [0]))
                    for a, b in zip(law.alphas, coefficients)), F(0)) / law.delta
                for i in range(law.n)]
    p, grad = curve.exact_value_gradient(u)
    assert value == p and gradient == grad
    hweights = curve.weights(u, curve.hess_alphas)
    pairs = {(0, 0), (0, law.n - 1), (law.n - 1, law.n - 1)}
    for i, j in pairs:
        direct = sum((b * (partial(a, [i + 1, j + 1]) - partial(a, [i + 1, 0])
                          - partial(a, [0, j + 1]) + partial(a, [0, 0]))
                      for a, b in zip(law.alphas, coefficients)), F(0)) / law.delta**2
        from_coefficients = sum((w * matrix[i][j] for w, matrix in zip(hweights, curve.hess)), F(0))
        assert direct == from_coefficients
    return {"exact_value_checks": 1, "exact_gradient_entries": law.n,
            "exact_hessian_entries": len(pairs)}


def run_case(label):
    started = time.monotonic()
    raw_path = ROOT / "results" / (label + "_raw.json")
    raw_bytes = raw_path.read_bytes()
    raw = decoded(json.loads(raw_bytes))
    previous = decoded(json.loads((ROOT / "results" / (label + "_results.json")).read_text()))
    law = sl.SimplexLaw(previous["n"], previous["degree"], G=raw["warrants"]["G"],
                        kappa=raw["warrants"]["kappa"])
    law.ingest(raw["J_intervals"]).transform()
    assert law.bernstein_coefficients == previous["J_bernstein_coefficients"]
    curve_started = time.monotonic()
    curve = CurvatureLaw(law)
    curve_seconds = time.monotonic() - curve_started
    derivative_checks = independent_derivatives(curve, [law.delta / (law.n + 1)] * law.n)
    rows = []
    for task in previous["tasks"]:
        old = task["certificate"]
        utility, prices = task["utility"], task["prices"]
        old_command = old["candidate"]["command"]
        proposal = curve.propose(prices, old_command, utility)
        certificates = [curve.certificate(x, prices, previous["calibrated_c0_lower"], utility)
                        for x in (old_command, proposal["command"])]
        uppers = [old["global_objective_upper_without_baseline"]] + [
            c["global_objective_upper_without_baseline"] for c in certificates]
        candidates = [{"origin": "prior_hypograph", "command": old_command,
                       "objective_lower_without_baseline": old["candidate"]["objective_lower_without_baseline"]}]
        candidates.extend({"origin": "curvature_" + origin, "command": c["command"],
                           "objective_lower_without_baseline": c["objective_lower_without_baseline"]}
                          for origin, c in zip(("old_command", "new_command"), certificates))
        chosen = max(candidates, key=lambda x: x["objective_lower_without_baseline"])
        upper = min(uppers)
        regret = upper - chosen["objective_lower_without_baseline"]
        assert 0 <= regret <= old["continuous_simplex_regret"]
        rows.append({"utility": utility, "task": task["task"], "prices": prices,
                     "proposal": proposal, "curvature_certificates": certificates,
                     "candidate": chosen, "global_objective_upper_without_baseline": upper,
                     "continuous_simplex_regret": regret,
                     "previous_hypograph_regret": old["continuous_simplex_regret"]})

    # Only the checker now accesses a synthetic microscopic realization.
    source = ns.NativeSource(raw["source_vectors_checker_only"], label=label + "_checker")
    for row in rows:
        candidate = row["candidate"]
        command = candidate["command"]
        truth = hc.phi(source.independent_response(command) - F(3, 2), row["utility"]) - hc.dot(row["prices"], command)
        lower, upper = candidate["objective_lower_without_baseline"], row["global_objective_upper_without_baseline"]
        assert lower <= truth <= upper
        assert all((x * (1 << 20)).denominator == 1 for x in command)
        for c in row["curvature_certificates"]:
            for old_point in previous["predictions"]:
                u = old_point["u"]
                objective = hc.phi(old_point["checker_J"], row["utility"]) - hc.dot(row["prices"], u)
                assert objective <= c["global_objective_upper_without_baseline"]
        row["checker_value_without_baseline"] = truth
        row["active_baseline_dark_controls"] = [i for i in previous["baseline_dark_controls"] if command[i]]
        if label.startswith("exact_pair") and row["utility"] == "conductance" and row["task"] == 0:
            regret = F(1) + F(27, 4000) - truth
            assert 0 <= regret <= row["continuous_simplex_regret"]
            row["checker_exact_regret"] = regret
    assert raw_path.read_bytes() == raw_bytes
    detail = {"label": label, "acquisition_sha256": sha256(raw_bytes).hexdigest(),
              "extra_source_readings": 0, "source_gradients_acquired": 0,
              "scope": "Exact certificate using acquired polynomial; source data used only after decisions in checks.",
              "upper_hessian_bound": curve.mu, "hessian_coefficient_matrices": curve.hess,
              "positive_LDL_pivots": curve.pivots,
              "curvature_setup_seconds": round(curve_seconds, 6),
              "curvature_verification_attempts": curve.verification_attempts,
              "eigen_proposal_failure": curve.eigen_proposal_failure,
              "float_proposal_failure": curve.float_proposal_failure,
              "matrix_count": len(curve.hess), "matrix_order": law.n,
              "derivative_checks": derivative_checks, "tasks": rows,
              "all_exact_checks_passed": True, "seconds": round(time.monotonic() - started, 3)}
    (ROOT / "results" / (label + "_curvature.json")).write_text(json.dumps(ns.jsonable(detail), indent=2) + "\n")
    summary = {"label": label, "extra_source_readings": 0,
               "matrix_count": len(curve.hess), "matrix_order": law.n,
               "upper_hessian_bound": float(curve.mu),
               "conductance_regrets": [float(t["continuous_simplex_regret"]) for t in rows[:3]],
               "compliance_regrets": [float(t["continuous_simplex_regret"]) for t in rows[3:]],
               "dark_active_counts": [len(t["active_baseline_dark_controls"]) for t in rows],
               "curvature_setup_seconds": round(curve_seconds, 6),
               "seconds": detail["seconds"], "all_exact_checks_passed": True}
    print(json.dumps(summary), flush=True)
    return summary


def main():
    saved = json.loads((ROOT / "results/LATTICE_RESULTS.json").read_text())
    cases = saved["cases"]
    if len(sys.argv) > 1:
        cases = cases[:int(sys.argv[1])]
    rows = [run_case(c["label"]) for c in cases]
    result = {"scope": "Offline refinement from unchanged acquired raw data, no source-gradient acquisition.",
              "cases": rows}
    destination = ROOT / "results/CURVATURE_RESULTS.json"
    tmp = destination.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(result, indent=2) + "\n")
    tmp.replace(destination)


if __name__ == "__main__":
    main()
