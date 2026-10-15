#!/usr/bin/env python3
"""Run only statically inspected bounded scripts in the disposable replay tree."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import os
import platform
import subprocess
import sys
import time

A = Path(__file__).resolve().parents[1]
E = A / "execution_tree"
R = E / "research"
ORIGINAL_R = A.parents[1]
ORIGINAL_W = Path("/Users/harjas/Documents/ChatGPT/ultra/work/astra-global-completion-axis-20261015")
PYTHON = ORIGINAL_R / ".venv/bin/python"
ENV = dict(os.environ)
ENV.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1", "PYTHONHASHSEED": "0",
            "PYTHONPATH": str(A / "control"), "ASTRA_REPLAY_WRITE_ROOT": str(E),
            "ASTRA_REPLAY_ORIGINAL_R": str(ORIGINAL_R), "ASTRA_REPLAY_ORIGINAL_W": str(ORIGINAL_W),
            "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1"})
LOGS = A / "runs"
LOGS.mkdir(exist_ok=False)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def put(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(value if isinstance(value, bytes) else (json.dumps(value, ensure_ascii=False, indent=2)+"\n").encode())


def metadata(path):
    if not path.is_file():
        return {"exists": False}
    data = path.read_bytes()
    return {"exists": True, "bytes": len(data), "sha256": sha(data), "mtime_ns": path.stat().st_mtime_ns}


# Arguments, output paths and bounded purpose were inspected before execution.
# The positive-r1 checker follows its fresh reconstruction, and compiler CLI
# regression follows the fresh nonshear and self-check runs in the same copy.
JOBS = [
    ("source_global_structure", "sources/global_compatible_positivity/verify_global_structure.py", [],
     ["GLOBAL_VERIFICATION.json", "SIMPLE_NONPOLYCONVEX_EXAMPLE.json"], None),
    ("global_reconstruction", "workers/global_completion_reconstruction/reconstruct_global_completion.py", [],
     ["RECONSTRUCTION_RECEIPT.json", "POSITIVE_R1_COMPLETION.json"], 70),
    ("receiving_reconstruction", "workers/global_completion_reconstruction/reconstruct_receiving_sharp.py", [],
     ["RECEIVING_SHARP_RECEIPT.json"], 28),
    ("non_polyconvex_completion", "workers/global_completion_reconstruction/verify_no_polyconvex_completion.py", [],
     ["NONPOLYCONVEX_COMPLETION_RECEIPT.json"], 44),
    ("positive_r1_export", "workers/global_completion_reconstruction/verify_positive_r1_export.py", [],
     ["POSITIVE_R1_EXPORT_RECEIPT.json"], None),
    ("nonshear_construction", "workers/full_invariant_genesis/verify_theorem.py", [],
     ["EXACT_RECEIPT.json"], 47),
    ("nonshear_independent", "workers/nonshear_face_independent_audit/verify.py", [],
     ["verification.json", "receipt.json"], 29),
    ("corrected_compiler_self_check", "workers/full_invariant_genesis/flat_completion_compiler.py", ["--self-check"],
     ["GENERAL_COMPILER_RECEIPT.json"], 14),
    ("corrected_compiler_cli", "workers/full_invariant_genesis/PARSER_CLI_REPLAY.v0002.py", [],
     ["PARSER_CLI_RECEIPT.v0002.json"], 6),
    ("general_independent_math", "workers/general_flat_completion_independent_audit/verify.py", [],
     ["verification.json", "receipt.json"], None),
    ("general_independent_implementation", "workers/general_flat_completion_independent_audit/verify_implementation.py", [],
     ["implementation_verification.json", "implementation_receipt.json"], 76),
    ("output_heat", "workers/output_heat_rank_preservation/verify_output_heat.py", [],
     ["VERIFICATION.json"], 28),
    ("positive_branch", "workers/positive_branch_new_operation/verify_new_operation.py", [],
     ["EXACT_VERIFICATION.json", "PROJECTION_COUNTEREXAMPLE.json"], 43),
    ("strict_exact_reductions", "workers/sharp_boundary_coercivity/EXACT_REDUCTIONS.py", [],
     ["EXACT_REDUCTIONS.json"], None),
    ("strict_kernel", "workers/global_completion_reconstruction/sharp_strict_audit/check_kernel_and_scaling.py", [],
     ["EXACT_AUDIT_RECEIPT.json"], 19),
    ("order_volume", "root/check_order_volume_identification.py", [],
     ["ORDER_VOLUME_CHECK.json"], 20),
    ("axis_limits", "workers/axis_control_genesis/axis_limits.py", [],
     ["results.json"], None),
    ("axis_measurement_design", "workers/axis_evidence_adversary/check_measurement_design.py", [],
     ["measurement_results.json"], None),
    ("priority_receiving", "workers/compatible_positivity_priority/verify_receiving_deductions.py", [],
     ["derived/RECEIVING_RECEIPT.json", "derived/RECEIVING_ALGEBRA.json"], 20),
    ("projection", "workers/projection_claim_audit/checks.py", [], ["checks.json"], 19),
]

inspection = []
for name, relative, args, outputs, expected in JOBS:
    script = R / relative
    source = script.read_bytes()
    syntax = ast.parse(source.decode(), filename=str(script))
    relevant = [{"line": i, "text": line} for i, line in enumerate(source.decode().splitlines(), 1)
                if any(k in line for k in ("argparse", "add_argument", "sys.argv", "read_text", "read_bytes", "write_text", "write_bytes", "subprocess.run", "Path("))]
    inspection.append({"name": name, "script": relative, "execution_sha256": sha(source),
                       "arguments": args, "declared_output_paths": outputs, "expected_aggregate_check_count": expected,
                       "ast_parsed": True, "interface_and_io_lines": relevant,
                       "execution_policy": "No optimizer or acquisition/network entry point. Writes confined by inherited Python audit guard."})
put(A / "CLI_INSPECTION.v0001.json", {"scripts": inspection, "inspection_before_replay": True})

runtime_cmd = [str(PYTHON), "-B", "-c", "import sys,platform,json,sympy,numpy,sitecustomize; print(json.dumps({'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'sympy':sympy.__version__,'numpy':numpy.__version__,'guard':sitecustomize.__file__,'dont_write_bytecode':sys.dont_write_bytecode}))"]
runtime = subprocess.run(runtime_cmd, cwd=E, env=ENV, capture_output=True, timeout=30)
put(A / "ENVIRONMENT.v0001.json", {"command": runtime_cmd, "exit_code": runtime.returncode,
    "stdout": runtime.stdout.decode(errors="replace"), "stderr": runtime.stderr.decode(errors="replace"),
    "controlled_environment": {k: ENV[k] for k in ("PYTHONDONTWRITEBYTECODE", "PYTHONNOUSERSITE", "PYTHONHASHSEED", "PYTHONPATH", "ASTRA_REPLAY_WRITE_ROOT", "ASTRA_REPLAY_ORIGINAL_R", "ASTRA_REPLAY_ORIGINAL_W", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS")},
    "guard_sha256": sha((A / "control/sitecustomize.py").read_bytes()),
    "runner_sha256": sha(Path(__file__).read_bytes())})
if runtime.returncode:
    raise SystemExit("Disposable runtime probe failed; receipt preserved.")

# Only the two argparse entry points support --help safely. Positional/no-CLI
# scripts were inspected statically and are never given a spurious --help path.
for number, relative in enumerate(("workers/full_invariant_genesis/flat_completion_compiler.py", "workers/output_heat_rank_preservation/verify_output_heat.py"), 1):
    command = [str(PYTHON), "-B", str(R / relative), "--help"]
    outcome = subprocess.run(command, cwd=(R / relative).parent, env=ENV, capture_output=True, timeout=30)
    put(A / f"CLI_HELP.{number:04d}.json", {"command": command, "exit_code": outcome.returncode,
        "stdout": outcome.stdout.decode(errors="replace"), "stderr": outcome.stderr.decode(errors="replace")})
    if outcome.returncode:
        raise SystemExit("CLI help failed; receipt preserved.")


def count(document):
    for key in ("check_count", "exact_check_count", "number_of_checks", "count", "exact_checks", "checks"):
        value = document.get(key)
        if type(value) is int:
            return value, key
        if isinstance(value, (list, dict)):
            return len(value), key
    return None, None


results = []
for number, (name, relative, args, outputs, expected) in enumerate(JOBS, 1):
    script = R / relative
    paths = [script.parent / item for item in outputs]
    before = {str(p.relative_to(E)): metadata(p) for p in paths}
    command = [str(PYTHON), "-B", str(script), *args]
    started = time.monotonic()
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    timed_out = False
    try:
        outcome = subprocess.run(command, cwd=script.parent, env=ENV, capture_output=True, timeout=120)
        code, stdout, stderr = outcome.returncode, outcome.stdout, outcome.stderr
    except subprocess.TimeoutExpired as error:
        timed_out = True
        code, stdout, stderr = None, error.stdout or b"", error.stderr or b""
    elapsed = time.monotonic() - started
    directory = LOGS / f"{number:04d}_{name}"
    put(directory / "stdout.txt", stdout)
    put(directory / "stderr.txt", stderr)
    after = {str(p.relative_to(E)): metadata(p) for p in paths}
    summaries = []
    for p in paths:
        if not p.is_file():
            summaries.append({"path": str(p.relative_to(E)), "exists": False})
            continue
        try:
            document = json.loads(p.read_bytes())
        except (ValueError, UnicodeDecodeError):
            continue
        n, key = count(document)
        summaries.append({"path": str(p.relative_to(E)), "status": document.get("status"),
                          "reported_check_count": n, "count_field": key,
                          "modified_during_command": before[str(p.relative_to(E))].get("mtime_ns") != after[str(p.relative_to(E))].get("mtime_ns")})
    primary_count = summaries[0].get("reported_check_count") if summaries else None
    expected_match = expected is None or primary_count == expected
    outputs_present = all(p.is_file() for p in paths)
    status = "PASS_SCOPED_REPLAY" if code == 0 and expected_match and outputs_present else "REPLAY_FAILURE"
    result = {"name": name, "status": status, "started_at_utc": stamp, "command": command,
        "cwd": str(script.parent), "execution_script_sha256": sha(script.read_bytes()), "exit_code": code,
        "timed_out": timed_out, "timeout_seconds": 120, "elapsed_seconds": elapsed,
        "stdout_sha256": sha(stdout), "stderr_sha256": sha(stderr), "output_before": before, "output_after": after,
        "output_summaries": summaries, "expected_aggregate_check_count": expected,
        "expected_count_match": expected_match, "all_declared_outputs_present": outputs_present,
        "scope": "Exact script replay/output integrity only; no theorem correctness, external review, historical priority or physical validation inferred."}
    put(directory / "receipt.json", result)
    results.append(result)
    print(json.dumps({"number": number, "name": name, "status": status, "exit_code": code,
                      "reported_checks": primary_count, "elapsed_seconds": round(elapsed, 3)}), flush=True)

copy = json.loads((A / "COPY_MANIFEST.v0001.json").read_bytes())
originals = []
snapshot = []
for item in copy["files"]:
    p = Path(item["original_absolute_path"])
    originals.append({"path": str(p), "matches_initial_sha256": p.is_file() and sha(p.read_bytes()) == item["sha256"]})
    p = A / item["snapshot_path"]
    snapshot.append({"path": str(p.relative_to(A)), "matches_initial_sha256": p.is_file() and sha(p.read_bytes()) == item["sha256"]})
summary = {"schema": "astra.root-disposable-replay-audit.v1", "status": "ALL_REQUESTED_SCOPED_REPLAYS_PASS" if all(x["status"] == "PASS_SCOPED_REPLAY" for x in results) else "REPLAY_FAILURES_RETAINED",
    "requested_replay_jobs": 19, "performed_replay_jobs": len(results), "additional_dependency_math_replay": "general_independent_math",
    "pass_count": sum(x["status"] == "PASS_SCOPED_REPLAY" for x in results),
    "failures": [x["name"] for x in results if x["status"] != "PASS_SCOPED_REPLAY"],
    "results": results, "originals_hash_recheck": originals,
    "all_originals_unchanged_since_copy": all(x["matches_initial_sha256"] for x in originals),
    "source_snapshot_hash_recheck": snapshot, "all_snapshot_bytes_unchanged": all(x["matches_initial_sha256"] for x in snapshot),
    "execution_path_patches": "EXECUTION_PATH_PATCHES.v0001.json",
    "omitted_scripts": [{"script": "workers/sharp_boundary_coercivity/verify_universal_frozen.py", "reason": "Redundant with requested fresh independent receiving reconstruction of the identical pinned universal certificate; strict exact reductions and independent kernel audit were both replayed."},
                        {"scripts": "Acquisition, extraction, optimization/exploration and integration/publication entry points", "reason": "Outside this bounded replay audit; no network, optimizer or live-state action authorized here."}],
    "scope": "Disposable local replay and exact integrity only. Analytic arguments, universal theorem correctness, novelty, physical feasibility and practical advantage are not established by these runs."}
put(A / "AUDIT_SUMMARY.v0001.json", summary)
print(json.dumps({k: summary[k] for k in ("status", "performed_replay_jobs", "pass_count", "failures", "all_originals_unchanged_since_copy", "all_snapshot_bytes_unchanged")}), flush=True)
