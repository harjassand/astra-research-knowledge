"""Inspect returned routes and governing passages; never execute source programs.

Targets below are disclosed owner evaluation oracles, not blind discoveries.
Run on this evaluation's pinned scientific snapshot. Future versions require a
new assessment instead of silently reusing the old conclusions.
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from knowledge.model import encoded
from knowledge.retrieve import Library

BASE = Path(__file__).resolve().parent
SPECS = [
    ("Q01", "U712-state-accuracy-does-not-control-fisher-derivatives", 0, 57, 67,
     ["zero derivative", "uniform finite epsilon"],
     "Even pointwise exact agreement does not acquire the parameter derivative. The current sufficient variance budget is not a necessary preparation bound."),
    ("Q02", "U952-trigger-occupation-law-and-rare-read-cost", 0, 121, 175,
     ["ENTIRE observed", "Initial state 1", "Bellman map a contraction"],
     "Use the acquired confidence rectangle and paid global abort clock for this stated reset/trigger/read family. Actual-start prediction and uniform rare-state prediction have distinct costs; no general unknown-family predictor follows."),
    ("Q03", "U687-shared-gaussian-record-absorption", 0, 10, 127,
     ["Individually approximately Gaussian marginals are insufficient", "entire law", "epsilon_in + sum_i epsilon_i"],
     "The acquired joint Gaussian record, known covariance, exact pathwise child gauges, deterministic caps and positive precision slack enable the actual joint-output law and TV bound. Marginal laws do not supply these inputs."),
    ("Q04", "U1080-visible-local-outgoing-pair-pole", 0, 15, 56,
     ["unique simple pole", "no useful numerical lower", "neither an all-times"],
     "The actual continued response has a visible local pole under the frozen theorem's hypotheses. This is not a nonreal eigenvalue of the physical self-adjoint Hamiltonian, an evaluated tolerance, or a device lifetime."),
    ("Q05", "U946-positive-star-inverse-spectrum", 0, 227, 271,
     ["c_j", "narrow", "No equipment action"],
     "Construct the positive scalar star at strict interlacing endpoints. Precision, stiffness, materials, contacts and manufacturing robustness remain separate obligations; exact realization does not acquire a working thermal device."),
    ("Q06", "U747-fixed-box-global-regret", 0, 232, 254,
     ["640 cells cover the entire complement", "gradient_bound", "[0.9999,1.0001]"],
     "The actual fixed-box proof combines complete outside-cell exclusion with local curvature/gradient. Reuse the proof mechanism, and its numeric bound only in the exact model/box with supplied full residual norms and structural assumptions."),
    ("Q07", "U712-reversible-local-refresh-mean-rate", 0, 73, 95,
     ["beta^2 gamma n", "does not bound every path-likelihood estimator"],
     "The refresh-time bound applies to the stationary magnetization-mean procedure. It does not bound full-trajectory Fisher information or every estimator."),
    ("Q08", "U794-constant-spd-bilinear-sos-separator", 2, 99, 154,
     ["constant symmetric positive-definite", "state-dependent/nonlinear/nonlocal", "not a quasiconvexity counterexample"],
     "The exact symmetry/dual separator excludes the constant-SPD closed-quadratic bilinear-SOS certificate class. It does not settle quasiconvexity or exclude general diffusion/nonlocal methods."),
]


def main():
    library = Library()
    evaluated = json.loads((BASE / "PROPOSED_RESULTS.json").read_bytes())
    by_id = {row["case"]["id"]: row for row in evaluated["results"]}
    inspected = []
    for case, target, index, start, end, anchors, outcome in SPECS:
        menu = by_id[case]["methods"][0]["results"]
        via = None
        for hit in menu:
            if hit["id"] == target:
                via = target
                break
            packet = library.packet([hit["id"]], max_bytes=2**24)["packets"][0]
            if target in [unit["id"] for unit in packet["related_units"]]:
                via = hit["id"]
                break
        if via is None:
            raise ValueError("No returned target/family route for " + case)
        source = library.source(target, evidence_index=index, start=start, end=end, max_bytes=131072)
        for anchor in anchors:
            if anchor.lower() not in source["text"].lower():
                raise ValueError("Wrong scientific passage for " + case + ": " + anchor)
        record = library.resolve(target)
        inspected.append({"case": case, "via": via, "target": target,
                          "content_version": record["content_version"],
                          "source": source["source"], "usable_premise_and_limit": outcome,
                          "source_programs_executed": 0})
    output = {"scope": "Supervised source-informed returned-route and actual governing-passage inspection. Not blind discovery, proof reaudit, physical validation or universal applicability.",
              "input_version": library.manifest["input_version"], "observations": inspected}
    (BASE / "SOURCE_USE.json").write_bytes(encoded(output))
    print("Inspected", len(inspected), "actual scientific source routes")


if __name__ == "__main__":
    main()
