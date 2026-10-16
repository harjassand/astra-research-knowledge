#!/usr/bin/env python3
"""Replay selected public-package checks in disposable package copies.

The runner treats child output as bounded replay evidence. It never edits the
package supplied by the caller and does not interpret any document as an
instruction. See REPLAY_PUBLIC_EVIDENCE_README.md for the run contract.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
import time
from fractions import Fraction


SCRIPT_DIR = Path(__file__).resolve().parent
FIXTURES = SCRIPT_DIR / "REPLAY_PUBLIC_EVIDENCE_FIXTURES.json"
LEGACY_PRIOR_NAME = "2026-10-16-convergence-genesis-v1"
EXCLUDED_PARTS = {"__pycache__", "acquired_excluded_from_publication", ".git"}
NUMERICAL_WARNING = re.compile(
    r"runtimewarning|floating.?point|numerical warning|overflow|underflow|"
    r"divide by zero|invalid value|loss of (?:precision|significance)|"
    r"ill.conditioned|round.?off|inaccurate|singular matrix",
    re.IGNORECASE,
)
WARNING_LINE = re.compile(r"\bwarning\b|runtimewarning|numericalwarning", re.IGNORECASE)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def json_read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def stable_hash_map(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not root.is_dir():
        return result
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in EXCLUDED_PARTS for part in rel.parts) or path.suffix == ".pyc":
            continue
        if path.is_symlink():
            result[rel.as_posix()] = "SYMLINK:" + os.readlink(path)
        elif path.is_file():
            result[rel.as_posix()] = sha256_file(path)
    return result


def package_layout_ok(package: Path) -> tuple[bool, str]:
    required = [
        package / "derived/root/direct_average.py",
        package / "derived/workers/ge_sparse_genesis/audit_root_composition.py",
        package / "originals",
    ]
    missing = [str(path.relative_to(package)) for path in required if not path.exists()]
    if missing:
        return False, "missing published package paths: " + ", ".join(missing)
    return True, "published package layout present"


def copy_package_safely(source: Path, destination: Path) -> dict[str, object]:
    """Copy ordinary package files; do not follow source symlinks or caches."""
    if not source.is_dir():
        raise FileNotFoundError(f"package root is not a directory: {source}")
    destination.mkdir(parents=True, exist_ok=False)
    excluded: list[str] = []
    for item in sorted(source.rglob("*")):
        rel = item.relative_to(source)
        rel_parts = rel.parts
        if any(part in EXCLUDED_PARTS for part in rel_parts) or item.suffix == ".pyc":
            excluded.append(rel.as_posix())
            continue
        if item.is_symlink():
            # Symlinks in a package are omitted rather than followed. The two
            # required compatibility links are created inside this copy below.
            excluded.append(rel.as_posix() + " [symlink]")
            continue
        target = destination / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(item, target)
    aliases: list[str] = []
    derived = destination / "derived"
    originals = destination / "originals"
    original_aliases = (("pair", Path("expanded/pair")),
                        ("exterior", Path("expanded/interchange_path_exterior")))
    for alias_name, relative_target in original_aliases:
        alias = originals / alias_name
        target = originals / relative_target
        if not alias.exists() and target.is_dir():
            alias.symlink_to(relative_target, target_is_directory=True)
            aliases.append(f"originals/{alias_name} -> {relative_target.as_posix()}")
    derived_originals = derived / "originals"
    if originals.is_dir() and not derived_originals.exists():
        # Existing checks use package/derived/originals while the published
        # layout stores that tree at package/originals.
        derived_originals.symlink_to(Path("../originals"), target_is_directory=True)
        aliases.append("derived/originals -> ../originals")
    legacy = destination / LEGACY_PRIOR_NAME
    prior = destination / "prior_convergence"
    if not legacy.exists() and prior.is_dir():
        legacy.symlink_to(Path("prior_convergence"), target_is_directory=True)
        aliases.append(f"{LEGACY_PRIOR_NAME} -> prior_convergence")
    return {"excluded_paths": excluded, "compatibility_aliases": aliases}


def numerical_warnings(stdout: str, stderr: str) -> tuple[list[str], list[str]]:
    warning_lines: list[str] = []
    numerical_lines: list[str] = []
    for line in (stdout + "\n" + stderr).splitlines():
        if WARNING_LINE.search(line):
            warning_lines.append(line)
            if NUMERICAL_WARNING.search(line):
                numerical_lines.append(line)
    return warning_lines, numerical_lines


def aggregate_status(statuses: list[str], mandatory: list[bool] | None = None) -> str:
    if mandatory is None:
        mandatory = [True] * len(statuses)
    blocking = [s for s, required in zip(statuses, mandatory) if required]
    if "FAIL" in blocking:
        return "FAIL"
    if any(s != "PASS" for s in blocking):
        return "INCOMPLETE"
    return "PASS"


def child_status(*, missing: bool, timed_out: bool, returncode: int | None,
                 predicate_ok: bool | None, numerical_warning: bool,
                 dependency_missing: bool = False) -> str:
    if missing or timed_out or dependency_missing:
        return "INCOMPLETE"
    if returncode != 0:
        return "FAIL"
    if predicate_ok is False:
        return "FAIL"
    if predicate_ok is None:
        return "INCOMPLETE"
    if numerical_warning:
        return "QUALIFIED"
    return "PASS"


def sparse_receipt_predicate(data: dict, result: dict) -> bool:
    """Check exact receipt/checker agreement; also used by deterministic fixtures."""
    try:
        n = int(data["graph"]["n"])
        k = int(data["shape"])
        bound = Fraction(data["Duhamel_upper_exact"])
        tolerance = Fraction(data["tolerance_exact"])
        return (
            result.get("checked") is True
            and result.get("pair_states") == n * (n - 1) // 2
            and result.get("exact_shifted_residuals") == 2 * (k - 1)
            and result.get("bound_exact") == str(bound)
            and data.get("finite_generator_certified") is (bound <= tolerance)
        )
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return False


def run_self_test() -> int:
    try:
        fixture = json_read(FIXTURES)
        sparse = fixture["sparse_receipt_predicate"]
        valid = sparse_receipt_predicate(sparse["valid"]["receipt"], sparse["valid"]["checker_result"])
        corrupt = sparse_receipt_predicate(sparse["corrupt"]["receipt"], sparse["corrupt"]["checker_result"])
        if valid is not True or corrupt is not False:
            print(json.dumps({"status": "FAIL", "fixture": "sparse receipt predicate"}))
            return 1
        observed = []
        for case in fixture["aggregation_cases"]:
            got = aggregate_status(case["statuses"], case.get("mandatory"))
            observed.append({"name": case["name"], "status": got})
            if got != case["expected"]:
                print(json.dumps({"status": "FAIL", "cases": observed}, indent=2))
                return 1
        print(json.dumps({"status": "PASS", "corrupt_receipt_rejected": True,
                          "missing_check_is_incomplete": True, "aggregation_cases": observed}, indent=2))
        return 0
    except Exception as exc:  # fixtures are part of the runner's test contract
        print(json.dumps({"status": "FAIL", "error": f"{type(exc).__name__}: {exc}"}))
        return 1


class Replay:
    def __init__(self, package: Path, output: Path, python: str, timeout: int, samples: int):
        self.package = package
        self.output = output
        self.python = python
        self.timeout = timeout
        self.samples = samples
        self.logs = output / "logs"
        self.artifacts = output / "artifacts"
        self.scratch = output / ".scratch"
        self.logs.mkdir()
        self.artifacts.mkdir()
        self.scratch.mkdir()
        self.checks: list[dict[str, object]] = []
        self._step_counter = 0
        self.package_ok, self.package_reason = package_layout_ok(package)
        self.source_hashes_before = stable_hash_map(package)
        self.copy_metadata: dict[str, object] = {"excluded_paths": [], "compatibility_aliases": []}

    def new_copy(self, check_id: str) -> tuple[tempfile.TemporaryDirectory, Path] | None:
        if not self.package_ok:
            return None
        td = tempfile.TemporaryDirectory(prefix=f"{check_id}-", dir=self.scratch)
        clone = Path(td.name) / "package"
        try:
            meta = copy_package_safely(self.package, clone)
            # Exclusion and alias sets are stable across copies. Record one copy.
            if not self.copy_metadata["excluded_paths"]:
                self.copy_metadata = meta
        except Exception:
            td.cleanup()
            raise
        return td, clone

    def missing_record(self, check_id: str, mandatory: bool, reason: str) -> dict[str, object]:
        row = {"id": check_id, "mandatory": mandatory, "status": "INCOMPLETE",
               "reason": reason, "children": [], "predicate": {"passed": None}}
        self.checks.append(row)
        return row

    def run_child(self, check_id: str, child_id: str, clone: Path, script_rel: str,
                  args: list[str] | None = None, timeout: int | None = None) -> dict[str, object]:
        self._step_counter += 1
        step_name = f"{check_id}__{child_id}"
        script = clone / script_rel
        if not script.is_file():
            return {"id": child_id, "status": "INCOMPLETE", "missing": str(PurePosixPath(script_rel)),
                    "returncode": None, "timeout": False, "stdout_log": None, "stderr_log": None,
                    "warnings": [], "numerical_warnings": []}
        argv = [self.python, str(script)] + (args or [])
        env = os.environ.copy()
        env["PYTHONWARNINGS"] = "default"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        start = time.monotonic()
        timed_out = False
        returncode: int | None = None
        out = ""
        err = ""
        try:
            completed = subprocess.run(
                argv,
                cwd=str(script.parent),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout or self.timeout,
                check=False,
            )
            returncode = completed.returncode
            out, err = completed.stdout, completed.stderr
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            out = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            err = exc.stderr.decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        elapsed = time.monotonic() - start
        warnings, numeric = numerical_warnings(out, err)
        out_path = self.logs / f"{step_name}.stdout.txt"
        err_path = self.logs / f"{step_name}.stderr.txt"
        out_path.write_text(out, encoding="utf-8")
        err_path.write_text(err, encoding="utf-8")
        missing_dep = bool(re.search(r"No module named ['\"](?:numpy|sympy)['\"]", err))
        process_ok = (returncode == 0 and not timed_out) if returncode is not None else None
        status = child_status(missing=False, timed_out=timed_out, returncode=returncode,
                              predicate_ok=process_ok, numerical_warning=bool(numeric),
                              dependency_missing=missing_dep)
        return {"id": child_id, "status": status, "returncode": returncode,
                "timeout": timed_out, "elapsed_seconds_diagnostic": elapsed,
                "stdout_log": str(out_path.relative_to(self.output)),
                "stderr_log": str(err_path.relative_to(self.output)),
                "warnings": warnings, "numerical_warnings": numeric,
                "command": [self.python, f"{{PACKAGE}}/{PurePosixPath(script_rel).as_posix()}"] + (args or [])}

    def save_artifacts(self, check_id: str, clone: Path, rel_paths: list[str]) -> list[str]:
        target_root = self.artifacts / check_id
        target_root.mkdir(parents=True, exist_ok=True)
        saved: list[str] = []
        for rel in rel_paths:
            src = clone / rel
            if src.is_file():
                dst = target_root / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)
                saved.append(str(dst.relative_to(self.output)))
        return saved

    @staticmethod
    def predicate_ok(row: dict, passed: bool | None, summary: str) -> None:
        row["predicate"] = {"passed": passed, "summary": summary}

    def finish(self, check_id: str, mandatory: bool, children: list[dict],
               predicate_passed: bool | None, predicate_summary: str,
               reason: str | None = None, artifacts: list[str] | None = None) -> dict:
        child_statuses = [str(child.get("status", "INCOMPLETE")) for child in children]
        if any(status == "FAIL" for status in child_statuses):
            status = "FAIL"
        elif any(status == "INCOMPLETE" for status in child_statuses):
            status = "INCOMPLETE"
        elif predicate_passed is False:
            status = "FAIL"
        elif any(status == "QUALIFIED" for status in child_statuses):
            status = "QUALIFIED"
        elif predicate_passed is None:
            status = "INCOMPLETE"
        elif any(status != "PASS" for status in child_statuses):
            status = "INCOMPLETE"
        else:
            status = "PASS"
        row = {"id": check_id, "mandatory": mandatory, "status": status,
               "children": children, "predicate": {"passed": predicate_passed,
                                                    "summary": predicate_summary}}
        if reason:
            row["reason"] = reason
        if artifacts:
            row["artifacts"] = artifacts
        self.checks.append(row)
        return row

    def run_direct_average(self) -> dict:
        check_id = "direct_average_path6"
        missing = self.missing_package_files(["derived/root/direct_average.py",
                                              "derived/root/DIRECT_PATH6.json",
                                              "derived/root/DEPENDENCY_RECEIPT.json",
                                              "derived/root/DEPENDENCY_erlang_certificate.v0001.py"])
        if missing:
            return self.missing_record(check_id, True, missing)
        td_clone = self.new_copy(check_id)
        if td_clone is None:
            return self.missing_record(check_id, True, self.package_reason)
        td, clone = td_clone
        try:
            root = clone / "derived/root"
            dependency = json_read(root / "DEPENDENCY_RECEIPT.json")
            dep_path = root / dependency["snapshot"]
            dep_ok = dep_path.is_file() and sha256_file(dep_path) == dependency["sha256"]
            if not dep_ok:
                return self.finish(check_id, True, [], False,
                                   "dependency receipt hash matches its exact named snapshot", artifacts=[])
            generated = root / "REPLAY_DIRECT_PATH6.json"
            child = self.run_child(check_id, "generator", clone, "derived/root/direct_average.py",
                                  ["--case", "path6", "--output", str(generated)])
            data = json_read(generated) if generated.is_file() else None
            expected = json_read(root / "DIRECT_PATH6.json")
            ok = bool(data) and data.get("case") == "path6" \
                and data.get("actual_fast_components") == [[0], [1], [2, 3, 4, 5]] \
                and data.get("direct_average_certified_at_005") is True \
                and isinstance(data.get("direct_average_TV_upper_display"), (int, float)) \
                and math.isfinite(data["direct_average_TV_upper_display"]) \
                and data["direct_average_TV_upper_display"] <= 0.05 \
                and all(data.get(key) == expected.get(key) for key in
                        ("case", "actual_fast_components", "direct_average_TV_upper_display",
                         "direct_average_certified_at_005", "script_sha256"))
            children = [child]
            artifacts = self.save_artifacts(check_id, clone, ["derived/root/REPLAY_DIRECT_PATH6.json"])
            return self.finish(check_id, True, children, ok,
                               "path6 regenerated with matching stable receipt fields, expected components, and displayed bound <= 0.05",
                               artifacts=artifacts)
        except Exception as exc:
            return self.finish(check_id, True, [], False,
                               f"direct-average replay encountered {type(exc).__name__}: {exc}")
        finally:
            td.cleanup()

    def run_root_composition(self) -> dict:
        check_id = "root_composition_audit"
        required = ["derived/workers/ge_sparse_genesis/audit_root_composition.py"] + [
            f"derived/root/{name}" for name in
            ("DIRECT_PATH6.json", "DIRECT_BRANCH6.json", "DIRECT_PATH20.json")]
        missing = self.missing_package_files(required)
        if missing:
            return self.missing_record(check_id, True, missing)
        td_clone = self.new_copy(check_id)
        if td_clone is None:
            return self.missing_record(check_id, True, self.package_reason)
        td, clone = td_clone
        try:
            child = self.run_child(check_id, "audit", clone,
                                   "derived/workers/ge_sparse_genesis/audit_root_composition.py")
            path = clone / "derived/workers/ge_sparse_genesis/root_composition_audit_receipt.json"
            data = json_read(path) if path.is_file() else None
            entries = data.get("exact_checks", []) if isinstance(data, dict) else []
            expected = ["DIRECT_PATH6.json", "DIRECT_BRANCH6.json", "DIRECT_PATH20.json"]
            ok = bool(data) and data.get("root_code_executed") is False \
                and data.get("root_sources_modified") is False \
                and [entry.get("input") for entry in entries] == expected \
                and all(entry.get("checked") is True and entry.get("upper_exact")
                        and entry.get("input_sha256") == sha256_file(clone / "derived/root" / entry["input"])
                        for entry in entries)
            artifacts = self.save_artifacts(check_id, clone,
                ["derived/workers/ge_sparse_genesis/root_composition_audit_receipt.json"])
            return self.finish(check_id, True, [child], ok,
                               "all three requested root receipts independently checked and byte hashes match copied inputs",
                               artifacts=artifacts)
        except Exception as exc:
            return self.finish(check_id, True, [], False,
                               f"root composition audit encountered {type(exc).__name__}: {exc}")
        finally:
            td.cleanup()

    def run_sparse_receipt(self, name: str) -> dict:
        check_id = f"sparse_receipt_{name}"
        rel = f"derived/workers/ge_sparse_genesis/{name}_certified.json"
        script_rel = "derived/workers/ge_sparse_genesis/check_receipts.py"
        missing = self.missing_package_files([rel, script_rel])
        if missing:
            return self.missing_record(check_id, True, missing)
        td_clone = self.new_copy(check_id)
        if td_clone is None:
            return self.missing_record(check_id, True, self.package_reason)
        td, clone = td_clone
        try:
            generated_rel = f"derived/workers/ge_sparse_genesis/{name}_replay_check.json"
            child = self.run_child(check_id, "checker", clone, script_rel,
                                  [str(clone / rel), "--output", str(clone / generated_rel)])
            receipt = json_read(clone / rel)
            result = json_read(clone / generated_rel) if (clone / generated_rel).is_file() else None
            ok = bool(result) and sparse_receipt_predicate(receipt, result)
            artifacts = self.save_artifacts(check_id, clone, [generated_rel])
            return self.finish(check_id, True, [child], ok,
                               "checker output agrees exactly with the receipt's rational bound, state count, residual count, and certification boolean",
                               artifacts=artifacts)
        except Exception as exc:
            return self.finish(check_id, True, [], False,
                               f"sparse receipt replay encountered {type(exc).__name__}: {exc}")
        finally:
            td.cleanup()

    def run_sampler_adversary(self) -> dict:
        check_id = "sampler_adversary_exact_checks"
        rel = "derived/workers/ge_sampler_adversary/exact_checks.py"
        missing = self.missing_package_files([rel])
        if missing:
            return self.missing_record(check_id, True, missing)
        td_clone = self.new_copy(check_id)
        if td_clone is None:
            return self.missing_record(check_id, True, self.package_reason)
        td, clone = td_clone
        try:
            child = self.run_child(check_id, "exact_checks", clone, rel)
            folder = clone / "derived/workers/ge_sampler_adversary"
            data = json_read(folder / "exactchecks.json") if (folder / "exactchecks.json").is_file() else None
            hashes = json_read(folder / "sourcehashes.json") if (folder / "sourcehashes.json").is_file() else None
            sections = ("coupling", "inversion", "rounding", "direct_limit",
                        "minimal_resolvent_transforms", "sampler_error_formulas", "green_strengthening")
            ok = isinstance(data, dict) and data.get("status") == "EXACT_CHECKS_PASS" \
                and data.get("proof_status") == "INTERNAL_RECONSTRUCTION_NOT_FORMAL" \
                and all(data.get(key) for key in sections) \
                and isinstance(data.get("counterexamples"), dict) and len(data["counterexamples"]) >= 4 \
                and isinstance(hashes, list) and len(hashes) > 0 \
                and all(re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", "")) for row in hashes)
            artifact_paths = self.save_artifacts(check_id, clone,
                ["derived/workers/ge_sampler_adversary/exactchecks.json",
                 "derived/workers/ge_sampler_adversary/sourcehashes.json"])
            return self.finish(check_id, True, [child], ok,
                               "exact-check status and required reconstruction sections present; source hashes are well-formed",
                               artifacts=artifact_paths)
        except Exception as exc:
            return self.finish(check_id, True, [], False,
                               f"sampler adversary replay encountered {type(exc).__name__}: {exc}")
        finally:
            td.cleanup()

    def run_exterior_group(self) -> dict:
        check_id = "exterior_checks_and_small_receiver"
        check_rel = "derived/workers/ge_exterior_genesis/checks.py"
        receive_rel = "derived/workers/ge_exterior_genesis/receive.py"
        sampler_rel = "derived/workers/ge_exterior_genesis/sampler.py"
        originals = ["originals/exterior/interchange_path_exterior/EXTERIOR_CERTIFIER_REPORT.md",
                     "originals/exterior/interchange_path_exterior/cycle_extension/PROOF.md",
                     "originals/pair/PAIR_CERTIFIED_AVERAGING_REPORT.md"]
        missing = self.missing_package_files([check_rel, receive_rel, sampler_rel] + originals)
        if missing:
            return self.missing_record(check_id, True, missing)
        td_clone = self.new_copy(check_id)
        if td_clone is None:
            return self.missing_record(check_id, True, self.package_reason)
        td, clone = td_clone
        try:
            children = [self.run_child(check_id, "checks", clone, check_rel)]
            folder = clone / "derived/workers/ge_exterior_genesis"
            receipt_path = folder / "checks_receipt.json"
            data = json_read(receipt_path) if receipt_path.is_file() else None
            required_counts = ("generator_identities", "positive_cover_identities",
                               "rank_one_interchange_swap_identities",
                               "polynomial_pfaffian_vs_explicit_minor_checks",
                               "fixed_prefix_block_pfaffian_checks", "bounded_integer_sampler_checks",
                               "one_hole_exception_checks")
            hashes_ok = isinstance(data, dict) and all(
                data.get("input_sha256", {}).get(key) == sha256_file(clone / key)
                for key in originals)
            finite_cases = data.get("finite_bit_count_cases", []) if isinstance(data, dict) else []
            checks_ok = isinstance(data, dict) and data.get("status") == "PASS" \
                and all(isinstance(data.get(key), int) and data[key] > 0 for key in required_counts) \
                and len(finite_cases) == 4 \
                and all(int(case["survival_lower_bound"]["numerator"]) > 0 for case in finite_cases) \
                and len(data.get("arbitrary_graph_interchange_parity_cases", [])) == 2 \
                and all(case.get("all_exact_comparisons_passed") is True
                        for case in data["arbitrary_graph_interchange_parity_cases"]) \
                and data.get("parity_rate_perturbation_certificate", {}).get("all_exact_comparisons_passed") is True \
                and hashes_ok
            # The receiver consumes the fresh check receipt above and samples a
            # deliberately small requested number of finite endpoints.
            children.append(self.run_child(check_id, "receiver", clone, receive_rel,
                                           ["--case", "3", "--samples", str(self.samples)]))
            receiver_path = folder / "full_endpoint_receiver_receipt.json"
            receiver = json_read(receiver_path) if receiver_path.is_file() else None
            endpoints = receiver.get("first_ten_endpoints", []) if isinstance(receiver, dict) else []
            receive_ok = isinstance(receiver, dict) and receiver.get("status") == "PASS" \
                and receiver.get("case") == "cycle_k4_antiperiodic" \
                and receiver.get("samples") == self.samples \
                and len(endpoints) == min(self.samples, 10) \
                and all(isinstance(e, list) and len(e) == 4 and e == sorted(set(e))
                        and all(isinstance(x, int) and 0 <= x < 6 for x in e) for e in endpoints) \
                and receiver.get("maximum_decisions_observed", 10**9) <= 9 \
                and receiver.get("inference_time_seconds") == "UNKNOWN" \
                and receiver.get("model_token_usage") == "UNKNOWN"
            artifacts = self.save_artifacts(check_id, clone,
                ["derived/workers/ge_exterior_genesis/checks_receipt.json",
                 "derived/workers/ge_exterior_genesis/full_endpoint_receiver_receipt.json"])
            return self.finish(check_id, True, children, bool(checks_ok and receive_ok),
                               "exact finite receipt predicates pass and the small sample receipt has valid sorted unique endpoints",
                               artifacts=artifacts)
        except Exception as exc:
            return self.finish(check_id, True, [], False,
                               f"exterior replay encountered {type(exc).__name__}: {exc}")
        finally:
            td.cleanup()

    def run_controller_exact(self) -> dict:
        check_id = "controller_exact_receiving_checks"
        script_rel = "derived/workers/ge_controller_adversary/exact_receiving_checks.py"
        required = [script_rel, "prior_convergence/MANIFEST.json"]
        prior_files = [
            "MANIFEST.json", "CLAIM_LEDGER.json", "CONTINUATION_HANDOFF.md",
            "root/ALL_HISTORY_CHANNEL_CONTRACT.md",
            "workers/s01_controller_repair/REPORT.md",
            "workers/s01_controller_repair/TRANSITION_TABLE.md",
            "workers/s01_controller_repair/check_radius2_decoder.py",
            "workers/s03_history_interface/FINITE_DISCHARGE.md",
            "workers/s03_history_interface/REPORT.md",
            "workers/s03_history_interface/finite_discharge_check.py",
            "workers/s03_history_interface/quantum_recovery_check.py",
            "workers/s06_controller_adversary/REPORT.md",
            "workers/s06_controller_adversary/S03_BANK_CLEAR_AUDIT.md",
            "workers/s06_controller_adversary/FINAL_AUDIT_ADDENDUM.md",
            "workers/l02_history_algebra/REPORT.md",
            "workers/l02_history_algebra/history_closure.py",
            "workers/l03_counter_repair/REPORT.md",
            "workers/l03_counter_repair/FOLLOWUP.md",
            "sources/l01/2601.20818v3/source/SM.tex",
            "sources/l01/2610.05589v1/source/submission.tex",
            "sources/l01/astra-capital/github_commit.json",
        ]
        if self.package.is_dir() and (self.package / "prior_convergence").is_dir():
            required.extend("prior_convergence/" + rel for rel in prior_files)
        missing = self.missing_package_files(required)
        if missing:
            return self.missing_record(check_id, True, missing)
        td_clone = self.new_copy(check_id)
        if td_clone is None:
            return self.missing_record(check_id, True, self.package_reason)
        td, clone = td_clone
        try:
            child = self.run_child(check_id, "exact", clone, script_rel)
            folder = clone / "derived/workers/ge_controller_adversary"
            checks = json_read(folder / "CHECKS.json") if (folder / "CHECKS.json").is_file() else None
            rows = json_read(folder / "INPUT_HASHES.json") if (folder / "INPUT_HASHES.json").is_file() else None
            quantum = checks.get("quantum", {}) if isinstance(checks, dict) else {}
            counter = checks.get("counter", {}) if isinstance(checks, dict) else {}
            receiving = checks.get("receiving_boundaries", {}) if isinstance(checks, dict) else {}
            manifest_rows = [row for row in rows if str(row.get("path", "")).endswith("/MANIFEST.json")] \
                if isinstance(rows, list) else []
            manifested_rows = [row for row in rows if row not in manifest_rows] \
                if isinstance(rows, list) else []
            manifest_ok = isinstance(rows, list) and len(rows) == 21 and len(manifest_rows) == 1 \
                and manifest_rows[0].get("matches_supplied_manifest") is None \
                and len(manifested_rows) == 20 and all(
                    row.get("matches_supplied_manifest") is True
                    and re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", ""))
                    for row in manifested_rows)
            ok = isinstance(checks, dict) and checks.get("worker") == "ge_controller_adversary" \
                and checks.get("source_handling") == "DATA; no supplied/acquired code executed" \
                and quantum.get("encoding_isometry") is True \
                and quantum.get("cyclic_clifford_code_preservation_and_stabilizer_products") is True \
                and quantum.get("all_961_cross_Grams_exactly_scalar") is True \
                and counter.get("three_counter_fault_trap") \
                and counter.get("two_history_fork") \
                and receiving.get("omitted_no_jump_counterexample", {}).get("actual_accepted_channel_is_identity") is False \
                and receiving.get("empty_terminal_span") \
                and receiving.get("zero_decoder_family") \
                and manifest_ok
            artifacts = self.save_artifacts(check_id, clone,
                ["derived/workers/ge_controller_adversary/CHECKS.json",
                 "derived/workers/ge_controller_adversary/INPUT_HASHES.json"])
            return self.finish(check_id, True, [child], bool(ok),
                               "exact algebra markers, expected negative controls, and all 20 manifest-backed source hashes were checked",
                               artifacts=artifacts)
        except Exception as exc:
            return self.finish(check_id, True, [], False,
                               f"controller exact replay encountered {type(exc).__name__}: {exc}")
        finally:
            td.cleanup()

    def run_reusable_maps(self) -> dict:
        check_id = "controller_reusable_maps"
        rel = "derived/workers/ge_controller_adversary/check_reusable_maps.py"
        needed = [rel, "derived/workers/ge_controller_genesis/REUSABLE_RECEIVER.md",
                  "derived/workers/ge_controller_genesis/PROOF.md",
                  "derived/workers/ge_controller_independent/SPEC_PROOF.md"]
        missing = self.missing_package_files(needed)
        if missing:
            return self.missing_record(check_id, True, missing)
        if self.dependencies.get("sympy", {}).get("available") is not True:
            return self.missing_record(check_id, True, "selected interpreter cannot import SymPy")
        td_clone = self.new_copy(check_id)
        if td_clone is None:
            return self.missing_record(check_id, True, self.package_reason)
        td, clone = td_clone
        try:
            child = self.run_child(check_id, "reusable", clone, rel)
            folder = clone / "derived/workers/ge_controller_adversary"
            data = json_read(folder / "REUSABLE_CHECKS.json") if (folder / "REUSABLE_CHECKS.json").is_file() else None
            hashes = json_read(folder / "REUSABLE_INPUT_HASHES.json") if (folder / "REUSABLE_INPUT_HASHES.json").is_file() else None
            truth_keys = ["independent_move_A_to_B_and_B_to_A_TP",
                          "clean_two_move_composition_retains_CX_in_A_and_vacates_B",
                          "genesis_onsite_microstep_TP_dimension_72",
                          "genesis_all_32_partial_masks_suffix_and_hold_undo_checked",
                          "genesis_phase_mod4_alone_does_not_identify_cumulative_logical_channel",
                          "genesis_killed_chain_trace_determinant_and_initial_derivative"]
            ok = isinstance(data, dict) and data.get("arithmetic") == "exact SymPy 1.14.0; no tolerances" \
                and all(data.get(key) is True for key in truth_keys) \
                and data.get("independent_phase_vectors_checked") == 243 \
                and data.get("genesis_robust_plurality_tests") == 80 \
                and data.get("max_clean_phase_changes_plus_commit") == 11 \
                and data.get("logical_CX_channel_order") == 3 \
                and data.get("alternating_logical_history_channel_period") == 6 \
                and isinstance(hashes, list) and len(hashes) == 3 \
                and all(re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", "")) for row in hashes)
            artifacts = self.save_artifacts(check_id, clone,
                ["derived/workers/ge_controller_adversary/REUSABLE_CHECKS.json",
                 "derived/workers/ge_controller_adversary/REUSABLE_INPUT_HASHES.json"])
            return self.finish(check_id, True, [child], bool(ok),
                               "reusable exact identities, bounded phase counts, and three input hashes match expected predicates",
                               artifacts=artifacts)
        except Exception as exc:
            return self.finish(check_id, True, [], False,
                               f"reusable-map replay encountered {type(exc).__name__}: {exc}")
        finally:
            td.cleanup()

    def run_recycler(self) -> dict:
        check_id = "controller_independent_recycler"
        rel = "derived/workers/ge_controller_independent/check_recycler.py"
        missing = self.missing_package_files([rel])
        if missing:
            return self.missing_record(check_id, True, missing)
        if self.dependencies.get("numpy", {}).get("available") is not True:
            return self.missing_record(check_id, True, "selected interpreter cannot import NumPy")
        td_clone = self.new_copy(check_id)
        if td_clone is None:
            return self.missing_record(check_id, True, self.package_reason)
        td, clone = td_clone
        try:
            child = self.run_child(check_id, "recycler", clone, rel)
            result_path = clone / "derived/workers/ge_controller_independent/RESULTS.json"
            data = json_read(result_path) if result_path.is_file() else None
            c = data.get("controller", {}) if isinstance(data, dict) else {}
            q = data.get("quantum", {}) if isinstance(data, dict) else {}
            ok = isinstance(data, dict) and data.get("status") == "PASS_FINITE_DIAGNOSTICS_ONLY" \
                and c.get("phase_states") == 243 \
                and c.get("all_states_have_clean_retirement") is True \
                and c.get("max_mean_service_exact") == "51929339/10800000" \
                and c.get("all_canonical_boundaries_use_same_A_banks") is True \
                and q.get("phase_frames_checked") == 243 \
                and q.get("qutrit_error_images") == 26 \
                and math.isfinite(float(q.get("orthogonal_error_isometry_max_residual"))) \
                and float(q.get("orthogonal_error_isometry_max_residual")) < 1e-10
            artifacts = self.save_artifacts(check_id, clone,
                ["derived/workers/ge_controller_independent/RESULTS.json"])
            return self.finish(check_id, True, [child], bool(ok),
                               "finite recycler diagnostics and controller/quantum counts satisfy explicit bounded predicates",
                               artifacts=artifacts)
        except Exception as exc:
            return self.finish(check_id, True, [], False,
                               f"independent recycler replay encountered {type(exc).__name__}: {exc}")
        finally:
            td.cleanup()

    def run_genesis_receiver(self) -> dict:
        check_id = "controller_genesis_receiver"
        rel = "derived/workers/ge_controller_genesis/check_receiver.py"
        missing = self.missing_package_files([rel])
        if missing:
            return self.missing_record(check_id, True, missing)
        td_clone = self.new_copy(check_id)
        if td_clone is None:
            return self.missing_record(check_id, True, self.package_reason)
        td, clone = td_clone
        try:
            child = self.run_child(check_id, "receiver", clone, rel)
            folder = clone / "derived/workers/ge_controller_genesis"
            data = json_read(folder / "CHECK_RESULTS.json") if (folder / "CHECK_RESULTS.json").is_file() else None
            negative = data.get("wrong_majority_negative_control", {}) if isinstance(data, dict) else {}
            ok = isinstance(data, dict) and data.get("status") == "PASS_WITH_EXPLICIT_BOUNDARIES" \
                and data.get("orthogonal_recovery_images") == 26 \
                and data.get("exact_diagonal_gram_blocks") == 676 \
                and data.get("generic_single_qutrit_error_maps") == 31 \
                and data.get("exact_generic_KL_blocks") == 961 \
                and data.get("classical_full_domain_states") == 32768 \
                and data.get("one_site_controller_perturbation_cuts") == 5120 \
                and data.get("noise_formula_numeric_checks") == 96 \
                and negative.get("result", "").find("FAILS as expected") >= 0
            artifacts = self.save_artifacts(check_id, clone,
                ["derived/workers/ge_controller_genesis/CHECK_RESULTS.json",
                 "derived/workers/ge_controller_genesis/CONTROLLER_TABLE.json"])
            return self.finish(check_id, True, [child], bool(ok),
                               "bounded controller/genesis counts match and the deliberate wrong-majority negative control remains failing",
                               artifacts=artifacts)
        except Exception as exc:
            return self.finish(check_id, True, [], False,
                               f"genesis receiver replay encountered {type(exc).__name__}: {exc}")
        finally:
            td.cleanup()

    def run_reciprocal_completion(self) -> dict:
        check_id = "reciprocal_completion_exact_checks"
        worker = "derived/workers/ge_sampler_adversary"
        script_rel = worker + "/reciprocal_completion_checks.py"
        old_files = ["REPORT.md", "PROOF_RECONSTRUCTION.md",
                     "DIRECT_LIMIT_INDEPENDENT_ADDENDUM.md", "ROOT_COMPOSITION_AUDIT.md",
                     "GREEN_SATURATION_STRENGTHENING.md", "exact_checks.py",
                     "exactchecks.json", "sourcehashes.json"]
        audit_rel = worker + "/RECIPROCAL_COMPLETION_AUDIT.md"
        required = [script_rel, audit_rel, "derived/root/RECIPROCAL_RATE_METRIC.md"] \
            + [f"{worker}/{name}" for name in old_files]
        missing = self.missing_package_files(required)
        if missing:
            return self.missing_record(check_id, True, missing)
        td_clone = self.new_copy(check_id)
        if td_clone is None:
            return self.missing_record(check_id, True, self.package_reason)
        td, clone = td_clone
        try:
            child = self.run_child(check_id, "exact", clone, script_rel)
            folder = clone / worker
            result_path = folder / "reciprocal_completion_checks.json"
            sources_path = folder / "reciprocal_completion_sources.json"
            data = json_read(result_path) if result_path.is_file() else None
            sources = json_read(sources_path) if sources_path.is_file() else None
            averaging = data.get("averaging", {}) if isinstance(data, dict) else {}
            approaches = data.get("approaches", {}).get("examples", []) if isinstance(data, dict) else []
            allocation = data.get("allocation", {}) if isinstance(data, dict) else {}
            quantum = data.get("quantum", {}) if isinstance(data, dict) else {}
            grouped: dict[int, list[tuple[int, Fraction]]] = {}
            for row in approaches:
                grouped.setdefault(int(row["sequence"]), []).append(
                    (int(row["index"]), Fraction(row["reciprocal_distance_to_uniform_boost_exact"])))
            approach_ok = len(approaches) == 15 and set(grouped) == {0, 1, 2} and all(
                [index for index, _ in sorted(rows)] == [2, 4, 8, 16, 32]
                and all(a[1] > b[1] for a, b in zip(sorted(rows), sorted(rows)[1:]))
                for rows in grouped.values())
            source_old = sources.get("old_frozen_files", {}) if isinstance(sources, dict) else {}
            old_hashes_ok = set(source_old) == set(old_files) and all(
                source_old[name].get("sha256") == sha256_file(folder / name)
                and source_old[name].get("bytes") == (folder / name).stat().st_size
                for name in old_files)
            audited = sources.get("audited_source", {}) if isinstance(sources, dict) else {}
            checker = sources.get("checker_source", {}) if isinstance(sources, dict) else {}
            audit_source = sources.get("audit_source", {}) if isinstance(sources, dict) else {}
            source_hashes_ok = audited.get("sha256") == sha256_file(clone / "derived/root/RECIPROCAL_RATE_METRIC.md") \
                and checker.get("sha256") == sha256_file(clone / script_rel) \
                and audit_source.get("sha256") == sha256_file(clone / audit_rel)
            ok = isinstance(data, dict) and data.get("status") == "EXACT_CHECKS_PASS" \
                and data.get("old_frozen_files_unchanged") is True \
                and averaging.get("triangle_boundary_noninjectivity_examples") == 4 \
                and averaging.get("dimer_retained_rate_aggregation_examples") == 3 \
                and averaging.get("exact_projection_idempotence_and_kernel_checks") is True \
                and approach_ok \
                and allocation.get("exact_square_root_optimum") == "845/2" \
                and allocation.get("rational_allocation_comparisons") == 99 \
                and len(allocation.get("rational_square_root_receipts", [])) == 3 \
                and all(Fraction(row["exact_error_budget"]) == Fraction(1, 10)
                        for row in allocation["rational_square_root_receipts"]) \
                and quantum.get("classical_TV_exact") == "1/12" \
                and quantum.get("output_trace_distance_exact") == "1/12" \
                and quantum.get("diamond_upper_exact") == "1/6" \
                and quantum.get("diamond_lower_from_this_input_exact") == "1/6" \
                and old_hashes_ok and source_hashes_ok
            artifacts = self.save_artifacts(check_id, clone,
                [worker + "/reciprocal_completion_checks.json",
                 worker + "/reciprocal_completion_sources.json"])
            return self.finish(check_id, True, [child], bool(ok),
                               "reciprocal exact identities, monotone finite approaches, allocation optimum, quantum mixture bound, and frozen/source hashes match explicit predicates",
                               artifacts=artifacts)
        except Exception as exc:
            return self.finish(check_id, True, [], False,
                               f"reciprocal completion replay encountered {type(exc).__name__}: {exc}")
        finally:
            td.cleanup()

    def run_source_sampler_finish(self) -> dict:
        check_id = "source_sampler_finish_direct"
        rel = "derived/root/finish_direct_receipts.py"
        required = [rel, "derived/root/DIRECT_FULL_SAMPLER_RECEIPT.json",
                    "originals/pair/fair_bit_sampler.py"]
        missing = self.missing_package_files(required)
        if missing:
            return self.missing_record(check_id, False, missing)
        td_clone = self.new_copy(check_id)
        if td_clone is None:
            return self.missing_record(check_id, False, self.package_reason)
        td, clone = td_clone
        try:
            child = self.run_child(check_id, "finish", clone, rel)
            root = clone / "derived/root"
            generated = root / "DIRECT_FULL_SAMPLER_RECEIPT.json"
            prior = json_read(generated) if generated.is_file() else None
            expected = json_read(self.package / "derived/root/DIRECT_FULL_SAMPLER_RECEIPT.json")
            # This runner executes only in the clone. The existing receipt is
            # therefore preserved in the package supplied by the caller.
            ok = isinstance(prior, dict) and prior == expected \
                and prior.get("schema") == "astra.ge-direct-full-sampler.v1" \
                and len(prior.get("results", [])) == 3 \
                and all(row.get("input") in {"DIRECT_PATH6.json", "DIRECT_BRANCH6.json", "DIRECT_PATH20.json"}
                        and bool(row.get("full_sampler_TV_upper_exact")) for row in prior["results"])
            artifacts = self.save_artifacts(check_id, clone,
                ["derived/root/DIRECT_FULL_SAMPLER_RECEIPT.json"])
            return self.finish(check_id, False, [child], bool(ok),
                               "optional source sampler composition produced three exact full-sampler bounds",
                               artifacts=artifacts)
        except Exception as exc:
            return self.finish(check_id, False, [], False,
                               f"optional source sampler replay encountered {type(exc).__name__}: {exc}")
        finally:
            td.cleanup()

    def missing_package_files(self, rel_paths: list[str]) -> str | None:
        if not self.package_ok:
            return self.package_reason
        def exists_with_preserved_layout(rel: str) -> bool:
            candidates = [self.package / rel]
            aliases = (
                ("originals/pair/", "originals/expanded/pair/"),
                ("originals/exterior/", "originals/expanded/interchange_path_exterior/"),
                ("derived/originals/pair/", "originals/expanded/pair/"),
                ("derived/originals/exterior/", "originals/expanded/interchange_path_exterior/"),
            )
            for prefix, target in aliases:
                if rel.startswith(prefix):
                    candidates.append(self.package / target / rel[len(prefix):])
            return any(path.exists() for path in candidates)

        missing = [rel for rel in rel_paths if not exists_with_preserved_layout(rel)]
        return "missing required package files: " + ", ".join(missing) if missing else None

    def probe_dependencies(self) -> dict[str, object]:
        probe_code = "\n".join([
            "import importlib.util, json, platform, sys",
            "out = {'python': sys.version, 'executable': sys.executable, 'platform': platform.platform()}",
            "mods = {}",
            "for name in ('numpy', 'sympy'):",
            "    spec = importlib.util.find_spec(name)",
            "    item = {'available': spec is not None, 'version': None}",
            "    if spec is not None:",
            "        try:",
            "            mod = __import__(name)",
            "            item['version'] = getattr(mod, '__version__', 'unknown')",
            "        except Exception as exc:",
            "            item = {'available': False, 'error': type(exc).__name__ + ': ' + str(exc)}",
            "    mods[name] = item",
            "out['dependencies'] = mods",
            "print(json.dumps(out))",
        ])
        try:
            p = subprocess.run([self.python, "-c", probe_code], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace",
                               timeout=min(self.timeout, 120), check=False)
            stdout, stderr, code = p.stdout, p.stderr, p.returncode
        except subprocess.TimeoutExpired:
            self.dependencies = {"numpy": {"available": False}, "sympy": {"available": False}}
            self.probe = {"status": "INCOMPLETE", "reason": "interpreter dependency probe timed out"}
            return self.probe
        warnings, numerical = numerical_warnings(stdout, stderr)
        (self.logs / "interpreter_probe.stdout.txt").write_text(stdout, encoding="utf-8")
        (self.logs / "interpreter_probe.stderr.txt").write_text(stderr, encoding="utf-8")
        try:
            parsed = json.loads(stdout.strip().splitlines()[-1]) if stdout.strip() else {}
        except Exception:
            parsed = {}
        self.dependencies = parsed.get("dependencies", {}) if isinstance(parsed, dict) else {}
        status = "PASS" if code == 0 and isinstance(parsed, dict) and parsed.get("python") else "INCOMPLETE"
        if numerical:
            status = "QUALIFIED"
        self.probe = {"status": status, "returncode": code, "python": parsed.get("python"),
                      "executable_reported_by_interpreter": parsed.get("executable"),
                      "platform": parsed.get("platform"), "dependencies": self.dependencies,
                      "warnings": warnings, "numerical_warnings": numerical,
                      "stdout_log": "logs/interpreter_probe.stdout.txt",
                      "stderr_log": "logs/interpreter_probe.stderr.txt"}
        return self.probe

    def execute(self, include_source_sampler: bool) -> dict[str, object]:
        self.probe_dependencies()
        if self.package_ok:
            self.run_direct_average()
            self.run_root_composition()
            for name in ("branch6", "source20", "ungapped6"):
                self.run_sparse_receipt(name)
            self.run_sampler_adversary()
            self.run_exterior_group()
            self.run_controller_exact()
            self.run_reusable_maps()
            self.run_recycler()
            self.run_genesis_receiver()
            self.run_reciprocal_completion()
            if include_source_sampler:
                self.run_source_sampler_finish()
            else:
                self.checks.append({"id": "source_sampler_finish_direct", "mandatory": False,
                                    "status": "NOT_RUN", "reason": "optional source sampler execution not requested",
                                    "children": [], "predicate": {"passed": None}})
        else:
            required_ids = ["direct_average_path6", "root_composition_audit", "sparse_receipt_branch6",
                            "sparse_receipt_source20", "sparse_receipt_ungapped6",
                            "sampler_adversary_exact_checks", "exterior_checks_and_small_receiver",
                            "controller_exact_receiving_checks", "controller_reusable_maps",
                            "controller_independent_recycler", "controller_genesis_receiver",
                            "reciprocal_completion_exact_checks"]
            for check_id in required_ids:
                self.missing_record(check_id, True, self.package_reason)
        after = stable_hash_map(self.package)
        source_stable = self.package_ok and self.source_hashes_before == after
        integrity = {"status": "PASS" if source_stable else "INCOMPLETE",
                     "source_package_unchanged": source_stable,
                     "before_file_count": len(self.source_hashes_before),
                     "after_file_count": len(after),
                     "before_sha256_map": self.source_hashes_before,
                     "after_sha256_map": after}
        statuses = [str(row["status"]) for row in self.checks] + [str(integrity["status"]), str(self.probe["status"])]
        mandatory = [bool(row.get("mandatory", False)) for row in self.checks] + [True, True]
        overall = aggregate_status(statuses, mandatory)
        shutil.rmtree(self.scratch, ignore_errors=True)
        return {"schema": "astra.ge-public-evidence-replay.v1", "status": overall,
                "scope": "bounded local replay of selected package scripts with semantic predicates; not proof, novelty, external validation, or a capability claim",
                "selected_interpreter": self.python, "timeout_seconds_per_child": self.timeout,
                "small_receiver_sample_count": self.samples,
                "package_root": str(self.package), "package_layout_status": "PASS" if self.package_ok else "INCOMPLETE",
                "package_layout_reason": self.package_reason,
                "interpreter_probe": self.probe,
                "package_copy_policy": {"fresh_copy_per_check": True,
                                         "source_symlinks_followed": False,
                                         "excluded_parts": sorted(EXCLUDED_PARTS) + ["*.pyc"],
                                         "excluded_path_count": len(self.copy_metadata.get("excluded_paths", [])),
                                         "compatibility_aliases_created_only_in_copy": self.copy_metadata.get("compatibility_aliases", [])},
                "source_integrity": integrity,
                "checks": self.checks}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", type=Path, help="published package root with derived/ and originals/")
    parser.add_argument("--output-dir", type=Path, help="new, empty output directory outside the package root")
    parser.add_argument("--python", default=sys.executable,
                        help="selected Python executable used for every child and dependency probe (default: this runner's interpreter)")
    parser.add_argument("--timeout", type=int, default=120, help="seconds per child process; maximum 120")
    parser.add_argument("--receiver-samples", type=int, default=8,
                        help="small finite receiver sample count; default 8")
    parser.add_argument("--include-source-sampler-finish", action="store_true",
                        help="also run root/finish_direct_receipts.py in a disposable copy (optional source import)")
    parser.add_argument("--self-test", action="store_true", help="run deterministic runner predicate/aggregation fixtures")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    if args.package_root is None or args.output_dir is None:
        parser.error("--package-root and --output-dir are required unless --self-test is selected")
    if not (1 <= args.timeout <= 120):
        parser.error("--timeout must be between 1 and 120 seconds")
    if args.receiver_samples < 1 or args.receiver_samples > 10_000:
        parser.error("--receiver-samples must be between 1 and 10000")
    package = args.package_root.expanduser().resolve()
    output = args.output_dir.expanduser().resolve()
    if output == package or package in output.parents:
        parser.error("--output-dir must be outside the package root")
    if output.exists():
        parser.error("--output-dir must not already exist; replay output is create-only")
    output.mkdir(parents=True, exist_ok=False)
    replay = Replay(package, output, args.python, args.timeout, args.receiver_samples)
    result = replay.execute(args.include_source_sampler_finish)
    target = output / "PUBLIC_EVIDENCE_REPLAY.v0001.json"
    with target.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"status": result["status"],
                      "checks": [{"id": row["id"], "status": row["status"],
                                  "mandatory": row.get("mandatory", False)} for row in result["checks"]],
                      "source_package_unchanged": result["source_integrity"]["source_package_unchanged"],
                      "receipt": str(target)}, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
