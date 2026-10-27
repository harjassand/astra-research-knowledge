#!/usr/bin/env python3
"""Read-only source-bound stored-field, root, ledger and scoped AC replay.

Historical path strings are rebound in memory; scientific source bytes remain
unchanged. This deliberately does not acquire fresh moments or rerun missing
original-law geometry/DAG acquisitions. See README.md for the exact boundary.
"""
from __future__ import annotations
import argparse
import builtins
import contextlib
import hashlib
import io
import json
import os
import pathlib
import runpy
import subprocess
import sys
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
HISTORICAL_PREFIX = "/workspace/scratch/57d8dd795b13"
MORREY = "morrey_law_first_stress_20261026/cube_brownian_completion"
ADOPTED = MORREY + "/fully_corrective141_half_K48/"
SCRIPTS = [
    "fully_corrective141_half_K48/independent_root_check.py",
    "fully_corrective141_half_K48/independent_ledger_check.py",
    "fully_corrective141_half_K48/independent_field_reassembly.py",
    "receive_corrective141_half_arithmetic_plan.py",
    "receive_corrective141_half_full_Gram.py",
    "receive_tree_completable_posterior.py",
    "same_law_AC/independent_guarded_posterior_check.py",
    "same_law_AC/independent_shear_covariance_check.py",
    "receive_posterior_hull_bulk_ceiling.py",
    "receive_same_law_box_overlap.py",
    "same_law_AC/independent_heat_kernel_check.py",
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(source_root, fields):
    import numpy as np
    BasePath = pathlib.Path
    source_root = source_root.resolve()
    seen = set()
    matches = []
    normalized_texts = set()

    def logical(path):
        p = BasePath(path).absolute()
        return p.relative_to(source_root).as_posix()

    def map_path(path):
        if not isinstance(path, (str, os.PathLike)):
            return path
        s = os.fspath(path).replace(HISTORICAL_PREFIX, str(source_root))
        rel = s.removeprefix(str(source_root) + "/")
        if rel in [ADOPTED + "candidate_volume_nodes.npy", ADOPTED + "candidate_face_means.npy"]:
            return str(fields / BasePath(s).name)
        return s

    def record(path):
        if isinstance(path, (str, os.PathLike)):
            p = BasePath(path).absolute()
            if p.is_relative_to(source_root) and p.is_file():
                seen.add(p.relative_to(source_root).as_posix())

    def normalized(obj):
        if isinstance(obj, dict):
            # Wall-clock duration is not a scientific identity claim.
            return {k: normalized(v) for k, v in obj.items() if k != "seconds"}
        if isinstance(obj, list):
            return [normalized(v) for v in obj]
        return obj

    class BoundPath(type(BasePath())):
        def __new__(cls, *args):
            return object.__new__(cls)

        def __init__(self, *args):
            args = tuple(str(a).replace(HISTORICAL_PREFIX, str(source_root))
                         if isinstance(a, (str, os.PathLike)) else a for a in args)
            super().__init__(*args)

        def exists(self):
            return BasePath(map_path(str(self))).exists()

        def read_text(self, *args, **kwargs):
            raw = super().read_text(*args, **kwargs)
            if HISTORICAL_PREFIX in raw:
                normalized_texts.add(logical(self))
            return raw.replace(HISTORICAL_PREFIX, str(source_root))

        def write_text(self, data, *args, **kwargs):
            before, after = json.loads(self.read_text()), json.loads(data)
            rel = logical(self)
            if rel == MORREY + "/same_law_AC/compatible_box_overlap_receipt.json":
                # The exact stored scalar, Taylor patch bound and gain are
                # fixed. Only the independently recomputed gradient contraction
                # may differ; accept it only through its actual certified cap.
                gradient_key = "guarded_gradient_L1_upper"
                changes, patch_checks = [], []
                r = Fraction(1, 8192)
                scalar_allowance = Fraction(1, 2**29)
                gradient_cap = Fraction(1, 1000)
                per_coordinate_gradient_guard = Fraction(1, 2**20)
                taylor_allowance = 150 * r * r
                for old, new in zip(before["disjoint_negative_patches"], after["disjoint_negative_patches"], strict=True):
                    assert old["center"] == new["center"]
                    # Every other patch field must remain exactly equal.
                    assert {k: v for k, v in old.items() if k != gradient_key} == {k: v for k, v in new.items() if k != gradient_key}
                    assert Fraction(new["radius_infinity"]) == r
                    old_gradient, new_gradient = Fraction(old[gradient_key]), Fraction(new[gradient_key])
                    node = Fraction(new["stored_scalar"])
                    bound = Fraction(new["scalar_upper_on_patch"])
                    q = Fraction(new["negative_scalar_lower"])
                    alpha = Fraction(new["combined_Loewner_alpha"])
                    gradient_slack = gradient_cap - new_gradient
                    negativity_slack = -q - bound
                    alpha_slack = q - alpha
                    assert old_gradient < gradient_cap and gradient_slack > 0
                    assert new_gradient >= 3 * per_coordinate_gradient_guard
                    assert q == Fraction(1, 200000)
                    assert bound == node + scalar_allowance + gradient_cap * r + taylor_allowance
                    assert negativity_slack > 0 and alpha_slack > 0
                    assert Fraction(new["gain_lower"]) == 3 * alpha * (2*r)**3
                    delta = new_gradient - old_gradient
                    if delta:
                        changes.append({"patch_center": new["center"], "field": gradient_key,
                                        "old": old[gradient_key], "new": new[gradient_key],
                                        "signed_difference": str(delta), "absolute_difference": str(abs(delta)),
                                        "certified_gradient_cap_minus_new_bound": str(gradient_slack),
                                        "scalar_negativity_margin_minus_q_minus_bound": str(negativity_slack)})
                    patch_checks.append({"patch_center": new["center"],
                                         "stored_scalar_exact": True, "scalar_upper_on_patch_exact": True,
                                         "gain_lower_exact": True,
                                         "gradient_cap_minus_new_bound": str(gradient_slack),
                                         "scalar_negativity_margin_minus_q_minus_bound": str(negativity_slack),
                                         "q_minus_alpha": str(alpha_slack)})
                    old.pop(gradient_key)
                    new.pop(gradient_key)
                assert normalized(before) == normalized(after), rel
                matches.append({"path": rel, "comparison": "exact_stored_scalar_patch_bound_and_gain_with_guarded_gradient_replay",
                                "changed_field_count": len(changes), "changed_fields": changes,
                                "maximum_gradient_contraction_difference": str(max((Fraction(c["absolute_difference"]) for c in changes), default=Fraction())),
                                "minimum_gradient_cap_slack": str(min(Fraction(c["gradient_cap_minus_new_bound"]) for c in patch_checks)),
                                "minimum_scalar_negativity_margin": str(min(Fraction(c["scalar_negativity_margin_minus_q_minus_bound"]) for c in patch_checks)),
                                "arithmetic_envelope": {
                                    "patch_radius": str(r),
                                    "per_coordinate_derivative_numeric_guard": str(per_coordinate_gradient_guard),
                                    "aggregate_guard_already_in_gradient_bound": str(3*per_coordinate_gradient_guard),
                                    "gradient_cap": str(gradient_cap), "stored_scalar_allowance": str(scalar_allowance),
                                    "linear_patch_allowance": str(gradient_cap*r), "taylor_allowance_150_r_squared": str(taylor_allowance),
                                    "negative_scalar_threshold_q": "1/200000",
                                    "gain_formula": "3 * alpha * (2*r)^3", "acceptance_premise": "Positive actual certified gradient, scalar-negativity and q-alpha margins; discrepancy magnitude is diagnostic only."},
                                "patch_checks": patch_checks,
                                "strict_finite_bulk_reduction_lower_exact": after["strict_finite_bulk_reduction_lower"],
                                "certified_gain_and_all_other_fields_equal": True})
            else:
                assert normalized(before) == normalized(after), rel
                matches.append({"path": rel, "comparison": "exact_scientific_fields",
                                "ignored_fields": ["seconds"]})
            return len(data)

    real_open, io_open, save = builtins.open, io.open, np.save
    cwd = os.getcwd()
    old_path = sys.path[:]
    previous_dont_write = sys.dont_write_bytecode

    def open_read(path, *args, **kwargs):
        record(path)
        mode = args[0] if args else kwargs.get("mode", "r")
        if isinstance(mode, str) and any(c in mode for c in "wax+"):
            raise ValueError("Scientific replay writes are forbidden: " + str(path))
        return real_open(map_path(path), *args, **kwargs)

    def io_open_read(path, *args, **kwargs):
        record(path)
        mode = args[0] if args else kwargs.get("mode", "r")
        if isinstance(mode, str) and any(c in mode for c in "wax+"):
            raise ValueError("Scientific replay writes are forbidden: " + str(path))
        return io_open(map_path(path), *args, **kwargs)

    def compare_array(path, array, *args, **kwargs):
        record(path)
        assert np.array_equal(np.load(map_path(path)), array), str(path)
        matches.append({"path": logical(path), "comparison": "exact_array_values"})

    try:
        pathlib.Path = BoundPath
        builtins.open, io.open, np.save = open_read, io_open_read, compare_array
        sys.dont_write_bytecode = True
        os.chdir(source_root)
        p = source_root / MORREY
        sys.path.insert(0, str(p))
        checks = []
        for name in SCRIPTS:
            path = p / name
            seen.add(path.relative_to(source_root).as_posix())
            print("BEGIN", name, flush=True)
            runpy.run_path(str(path), run_name="__main__")
            checks.append({"script": path.relative_to(source_root).as_posix(), "sha256": sha(path), "status": "PASS"})
        for module_name in ["damped_arithmetic_primitives", "finite_heat_coefficient_error", "outward_binary64", "certified_w1_receiver"]:
            module = sys.modules.get(module_name)
            if module and getattr(module, "__file__", None):
                seen.add(logical(module.__file__))
    finally:
        pathlib.Path = BasePath
        builtins.open, io.open, np.save = real_open, io_open, save
        sys.path[:] = old_path
        sys.dont_write_bytecode = previous_dont_write
        os.chdir(cwd)
    return {"checks": checks, "comparisons": matches,
            "historical_binding": {"from": HISTORICAL_PREFIX, "to": "--source-root (in memory only)",
                                   "byte_hashes": "Always original unmodified file bytes",
                                   "normalized_text_paths": sorted(normalized_texts)},
            "read_inputs": sorted(seen)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=pathlib.Path, default=HERE.parent / "source")
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    source_root = args.source_root.resolve()
    output = args.output.resolve()
    # Pin every retained replay input, including imports and documented fixtures.
    inputs = json.loads((HERE / "INPUTS.json").read_text())["inputs"]
    for row in inputs:
        path = source_root / row["path"]
        assert path.stat().st_size == row["bytes"], row["path"]
        assert sha(path) == row["sha256"], row["path"]
    output.mkdir(parents=True, exist_ok=False)
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    # This known helper executes only two hash-bound field functions; it does
    # not call the fresh moment-acquisition producer.
    command = [sys.executable, "-B", str(HERE / "reproduce_adopted141_fields.py"),
               "--research-root", str(source_root), "--output", str(output / "fields")]
    with (output / "stored_fields.log").open("w") as log:
        subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=True)
    stored_fields = json.loads((output / "fields/reproduction_report.json").read_text())
    assert all(row["bitwise_original_match"] for row in stored_fields["outputs"])
    with (output / "scientific_replay.log").open("w") as log, contextlib.redirect_stdout(log):
        report = replay(source_root, output / "fields")
    report["scope"] = "Stored moments and current exact root/ledger/Gram arithmetic plus stated compact same-law algebra; no fresh moment acquisition, original law/DAG reconstruction, optimizer or Morrey solution."
    report["adopted_negative_stress_certificate"] = {
        "source_status": "Original version-bound independently received adopted141 certificate",
        "replay_status": "Exact stored-field hashes, root and ledger arithmetic, and fullK96 Gram/outward sums reproduced",
        "negative_stress_upper": "0.004714574814154892",
        "optional_overlap_credit_applied": False,
        "scope": "Certified negative-stress upper only; no W1, affinity, PSD membership or Morrey solution."}
    report["optional_same_law_overlap"] = {
        "source_status": "Separate independently received compatible-box overlap result at frozen source scope",
        "replay_status": "Exact stored scalars, patch upper bounds and certified gain; only gradient-contraction bounds may differ, with every actual certificate margin rechecked",
        "certified_gain_exact": json.loads((source_root / MORREY / "same_law_AC/compatible_box_overlap_receipt.json").read_text())["strict_finite_bulk_reduction_lower"],
        "certified_gain_decimal": "2.1346001363868332e-20",
        "adopted_into_displayed_negative_stress_upper": False,
        "scope": "Optional tiny local finite-bulk credit, separate from the adopted N certificate; no material new N adoption."}
    report["fresh_moment_acquisition"] = "NOT_RERUN"
    report["original_geometry_and_DAG_reconstruction"] = "NOT_RERUN: required geometry/DAG fixtures explicitly omitted in fixed packet"
    report["stored_fields"] = stored_fields
    (output / "replay_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"checks_passed": len(report["checks"]), "stored_fields": len(report["stored_fields"]["outputs"]),
                      "report": str(output / "replay_report.json"), "fresh_moments": "NOT_RERUN"}, indent=2))


if __name__ == "__main__":
    main()
