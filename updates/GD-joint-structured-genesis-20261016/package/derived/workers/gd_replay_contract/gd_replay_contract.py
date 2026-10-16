#!/usr/bin/env python3
"""Fail-closed runner for a root-reviewed JSON replay plan.

This utility orchestrates explicitly listed receiving checks. It does not
define scientific checks or infer what their outputs mean.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


PLAN_SCHEMA = "gd-replay-plan/v1"
RECEIPT_SCHEMA = "gd-replay-receipt/v1"
PYTHON_TOKEN = "{python}"
PROBE_TIMEOUT = 20
MAX_CHECK_TIMEOUT = 600
MAX_LOG_CHARS = 16000
OUTPUT_RULES = ("stdout_contains", "stdout_exact", "stderr_contains",
                "stderr_exact", "json_files")


class PlanError(ValueError):
    """The plan is ambiguous or does not meet the fail-closed contract."""


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(x, str) for x in value):
        raise PlanError(f"{label} must be a list of strings")
    return value


def _validate_plan(plan: Any) -> dict[str, Any]:
    if not isinstance(plan, dict) or plan.get("schema") != PLAN_SCHEMA:
        raise PlanError(f"plan schema must be {PLAN_SCHEMA!r}")
    mandatory = plan.get("mandatory")
    optional = plan.get("optional", [])
    if not isinstance(mandatory, list) or not isinstance(optional, list):
        raise PlanError("mandatory and optional must be lists")
    ids: set[str] = set()
    for section, rows in (("mandatory", mandatory), ("optional", optional)):
        for i, row in enumerate(rows):
            label = f"{section}[{i}]"
            if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
                raise PlanError(f"{label} requires a nonempty id")
            if row["id"] in ids:
                raise PlanError(f"duplicate check id: {row['id']}")
            ids.add(row["id"])
            deps = row.get("required_modules", [])
            _string_list(deps, f"{label}.required_modules")
            if section == "optional":
                if "argv" in row or "command" in row:
                    raise PlanError(f"{label} is intentionally omitted and cannot declare a command")
                if not isinstance(row.get("reason"), str) or not row["reason"]:
                    raise PlanError(f"{label} requires a reason for omission")
                continue

            argv = _string_list(row.get("argv"), f"{label}.argv")
            if len(argv) < 2 or argv[0] != PYTHON_TOKEN:
                raise PlanError(f"{label}.argv must start with {PYTHON_TOKEN!r} and include a checker")
            cwd = row.get("cwd", ".")
            if not isinstance(cwd, str):
                raise PlanError(f"{label}.cwd must be a path string")
            timeout = row.get("timeout_seconds", 120)
            if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not 0 < timeout <= MAX_CHECK_TIMEOUT:
                raise PlanError(f"{label}.timeout_seconds must be in (0, {MAX_CHECK_TIMEOUT}]")
            accept = row.get("accept")
            if not isinstance(accept, dict) or not any(k in accept for k in OUTPUT_RULES):
                raise PlanError(f"{label}.accept requires an explicit output predicate")
            for key in ("stdout_contains", "stderr_contains"):
                if key in accept:
                    values = _string_list(accept[key], f"{label}.accept.{key}")
                    if not values:
                        raise PlanError(f"{label}.accept.{key} cannot be empty")
            for key in ("stdout_exact", "stderr_exact"):
                if key in accept and not isinstance(accept[key], str):
                    raise PlanError(f"{label}.accept.{key} must be a string")
            if "json_files" in accept:
                files = accept["json_files"]
                if not isinstance(files, list) or not files:
                    raise PlanError(f"{label}.accept.json_files must be a nonempty list")
                for item in files:
                    if (not isinstance(item, dict) or not isinstance(item.get("path"), str)
                            or not ("equals" in item) ^ ("fields" in item)):
                        raise PlanError(f"{label}.accept.json_files entries need path and exactly one of equals/fields")
                    if "fields" in item and (not isinstance(item["fields"], dict) or not item["fields"]):
                        raise PlanError(f"{label}.accept.json_files fields must be a nonempty object")
            fresh = row.get("fresh_outputs", [])
            _string_list(fresh, f"{label}.fresh_outputs")
            if len(set(fresh)) != len(fresh):
                raise PlanError(f"{label}.fresh_outputs must not contain duplicates")
    return plan


def _selected_executable(requested: str) -> str | None:
    found = shutil.which(requested)
    if found is None and os.path.isfile(requested) and os.access(requested, os.X_OK):
        found = os.path.abspath(requested)
    return os.path.abspath(found) if found else None


def _probe(executable: str, modules: list[str]) -> dict[str, Any]:
    source = r'''import importlib, importlib.metadata, json, sys
names = json.loads(sys.argv[1])
found = {}
for name in names:
    try:
        module = importlib.import_module(name)
        version = getattr(module, "__version__", None)
        if version is None:
            root = name.split(".", 1)[0]
            for dist in importlib.metadata.packages_distributions().get(root, []):
                try:
                    version = importlib.metadata.version(dist)
                    break
                except importlib.metadata.PackageNotFoundError:
                    pass
        found[name] = {"available": True, "version": str(version) if version is not None else None}
    except Exception as exc:
        found[name] = {"available": False, "version": None,
                       "error": type(exc).__name__ + ": " + str(exc)}
print(json.dumps({"executable": sys.executable, "version": sys.version,
                  "prefix": sys.prefix, "base_prefix": sys.base_prefix,
                  "modules": found}, sort_keys=True))
'''
    started = time.monotonic()
    try:
        result = subprocess.run([executable, "-c", source, json.dumps(modules)],
                                capture_output=True, text=True, timeout=PROBE_TIMEOUT)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "PROBE_FAILED", "elapsed_seconds": round(time.monotonic() - started, 6),
                "error": f"{type(exc).__name__}: {exc}"}
    elapsed = round(time.monotonic() - started, 6)
    if result.returncode != 0:
        return {"status": "PROBE_FAILED", "exit_code": result.returncode,
                "elapsed_seconds": elapsed, "stderr": result.stderr[-MAX_LOG_CHARS:]}
    try:
        details = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return {"status": "PROBE_FAILED", "elapsed_seconds": elapsed,
                "error": f"invalid probe JSON: {exc}", "stdout": result.stdout[-MAX_LOG_CHARS:]}
    return {"status": "OK", "elapsed_seconds": elapsed, **details}


def _fingerprint(path: Path) -> dict[str, Any] | None:
    try:
        stat = path.stat()
        if not path.is_file():
            return {"kind": "not_file", "mtime_ns": stat.st_mtime_ns}
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return {"sha256": digest, "size": stat.st_size, "mtime_ns": stat.st_mtime_ns,
                "ctime_ns": stat.st_ctime_ns, "inode": getattr(stat, "st_ino", None)}
    except FileNotFoundError:
        return None


def _path(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else base / path


def _deep_contains(actual: Any, expected: Any) -> bool:
    if isinstance(expected, dict):
        return (isinstance(actual, dict) and all(k in actual and _deep_contains(actual[k], v)
                                                 for k, v in expected.items()))
    return actual == expected


def _accept_output(accept: dict[str, Any], cwd: Path, stdout: str,
                   stderr: str) -> list[str]:
    errors: list[str] = []
    for needle in accept.get("stdout_contains", []):
        if needle not in stdout:
            errors.append(f"stdout is missing required text {needle!r}")
    if "stdout_exact" in accept and stdout != accept["stdout_exact"]:
        errors.append("stdout does not match the required exact text")
    for needle in accept.get("stderr_contains", []):
        if needle not in stderr:
            errors.append(f"stderr is missing required text {needle!r}")
    if "stderr_exact" in accept and stderr != accept["stderr_exact"]:
        errors.append("stderr does not match the required exact text")
    for spec in accept.get("json_files", []):
        path = _path(cwd, spec["path"])
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"cannot read accepted JSON {spec['path']!r}: {exc}")
            continue
        if "equals" in spec and value != spec["equals"]:
            errors.append(f"JSON {spec['path']!r} does not equal the accepted value")
        if "fields" in spec and not _deep_contains(value, spec["fields"]):
            errors.append(f"JSON {spec['path']!r} does not contain the accepted fields")
    return errors


def _excerpt(value: str) -> tuple[str, bool]:
    return value[:MAX_LOG_CHARS], len(value) > MAX_LOG_CHARS


def _run_check(row: dict[str, Any], plan_dir: Path, executable: str | None,
               probe: dict[str, Any]) -> dict[str, Any]:
    check_id = row["id"]
    deps = row.get("required_modules", [])
    module_info = probe.get("modules", {}) if probe.get("status") == "OK" else {}
    diagnostics = {name: module_info.get(name, {"available": None, "version": None}) for name in deps}
    result: dict[str, Any] = {"id": check_id, "status": "BLOCKED", "required_modules": deps,
                              "dependency_diagnostics": diagnostics}
    if executable is None or probe.get("status") != "OK":
        result["reason"] = "selected checker interpreter could not be probed"
        return result
    missing = [name for name, info in diagnostics.items() if not info.get("available")]
    if missing:
        result["reason"] = "missing or unimportable mandatory modules: " + ", ".join(missing)
        return result
    cwd = _path(plan_dir, row.get("cwd", ".")).absolute()
    result["cwd"] = str(cwd)
    if not cwd.is_dir():
        result["reason"] = "checker working directory does not exist"
        return result
    argv = [executable, *row["argv"][1:]]
    result["argv"] = argv
    accepted_json = [item["path"] for item in row["accept"].get("json_files", [])]
    tracked_outputs = list(dict.fromkeys([*row.get("fresh_outputs", []), *accepted_json]))
    before = {name: _fingerprint(_path(cwd, name)) for name in tracked_outputs}
    started = time.monotonic()
    try:
        proc = subprocess.run(argv, cwd=cwd, capture_output=True, text=True,
                              timeout=row.get("timeout_seconds", 120))
    except FileNotFoundError as exc:
        result["reason"] = f"checker could not be started: {exc}"
        return result
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        err = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        result.update({"status": "FAIL", "reason": "checker timed out",
                       "elapsed_seconds": round(time.monotonic() - started, 6)})
        result["stdout"], result["stdout_truncated"] = _excerpt(out)
        result["stderr"], result["stderr_truncated"] = _excerpt(err)
        return result
    elapsed = round(time.monotonic() - started, 6)
    out, out_truncated = _excerpt(proc.stdout)
    err, err_truncated = _excerpt(proc.stderr)
    result.update({"exit_code": proc.returncode, "elapsed_seconds": elapsed,
                   "stdout": out, "stdout_truncated": out_truncated,
                   "stderr": err, "stderr_truncated": err_truncated})
    after = {name: _fingerprint(_path(cwd, name)) for name in tracked_outputs}
    freshness = {name: before[name] != after[name] and after[name] is not None for name in before}
    result["fresh_outputs"] = freshness
    errors = _accept_output(row["accept"], cwd, proc.stdout, proc.stderr)
    errors.extend(f"fresh output {name!r} was not changed by this run" for name, fresh in freshness.items() if not fresh)
    if proc.returncode != 0:
        errors.insert(0, f"checker exited with status {proc.returncode}")
    result["acceptance_errors"] = errors
    result["output_accepted"] = not errors
    result["status"] = "PASS" if not errors else "FAIL"
    return result


def run_plan(plan_path: str | Path, selected_python: str) -> dict[str, Any]:
    source_path = Path(plan_path).absolute()
    raw_plan = source_path.read_bytes()
    plan = _validate_plan(json.loads(raw_plan))
    modules = sorted({module for section in ("mandatory", "optional")
                      for row in plan.get(section, []) for module in row.get("required_modules", [])})
    invocation = _selected_executable(selected_python)
    probe = _probe(invocation, modules) if invocation else {"status": "PROBE_FAILED", "error": "selected Python not found or not executable"}
    checker = {"requested": selected_python, "invocation": invocation,
               "realpath": os.path.realpath(invocation) if invocation else None, **probe}
    mandatory = [_run_check(row, source_path.parent, invocation, probe) for row in plan["mandatory"]]
    optional = []
    module_info = probe.get("modules", {}) if probe.get("status") == "OK" else {}
    for row in plan.get("optional", []):
        optional.append({"id": row["id"], "status": "NOT_RUN", "reason": row["reason"],
                         "command": None,
                         "dependency_diagnostics": {name: module_info.get(name, {"available": None, "version": None})
                                                    for name in row.get("required_modules", [])}})
    if any(row["status"] == "FAIL" for row in mandatory):
        aggregate = "FAIL"
    elif not mandatory or any(row["status"] != "PASS" for row in mandatory):
        aggregate = "INCOMPLETE"
    else:
        aggregate = "PASS"
    return {
        "schema": RECEIPT_SCHEMA,
        "plan": {"path": str(source_path), "sha256": hashlib.sha256(raw_plan).hexdigest()},
        "aggregate": aggregate,
        "provenance": {
            "launcher": {"executable": sys.executable, "realpath": os.path.realpath(sys.executable),
                         "version": sys.version},
            "checker_interpreter": checker,
        },
        "mandatory": mandatory,
        "optional": optional,
        "scope": "Execution and plan-defined output acceptance only; no scientific proof or external validation.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path, help="root-reviewed JSON plan")
    parser.add_argument("--python", required=True, help="exact selected checker Python executable")
    parser.add_argument("--receipt", type=Path, help="optional path to write the replay receipt")
    args = parser.parse_args(argv)
    try:
        receipt = run_plan(args.plan, args.python)
    except (OSError, json.JSONDecodeError, PlanError) as exc:
        parser.exit(64, f"plan error: {exc}\n")
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return {"PASS": 0, "FAIL": 1, "INCOMPLETE": 2}[receipt["aggregate"]]


if __name__ == "__main__":
    raise SystemExit(main())
