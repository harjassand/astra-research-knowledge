#!/usr/bin/env python3
"""Reproduce bounded diagnostics in isolated copies; this is not proof checking."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
PACKAGE = Path(__file__).resolve().parent.parent
if (PACKAGE / "proofs").is_dir():
    SOURCE = PACKAGE / "proofs"
    REPLAY_ROOT = Path(tempfile.mkdtemp(prefix="research-replay-"))
    STAGE, OUT = REPLAY_ROOT / "scratch", REPLAY_ROOT / "results"
else:
    SOURCE = ROOT / "work" / "agents"
    STAGE = ROOT / "work" / "replay" / STAMP
    OUT = ROOT / "outputs" / "research" / "verification" / STAMP
SCRIPTS = [
    "chem_geometry/order5/check_order5.py",
    "chem_order5_blind/exact_checks.py",
    "chem_order5_blind/almost_sure/exact_checks.py",
    "chemistry_audit/independent_checks.py",
    "excursion_exact/finite_check.py",
    "rate_phase_blind/finite_checks.py",
    "cubic_audit/exact_checks.py",
    "centered_blind/verify_centered.py",
    "centered_audit/check_independent.py",
    "centered_audit/exact_counterexamples.py",
    "sharp_centered/verify_sharp_centered.py",
    "qudit_blind/check_interfaces.py",
    "collective_concentration/verify_concentration_normalizations.py",
    "concentration_blind/verify_concentration.py",
    "heat_upper_blind/diagnostic.py",
    "heat_upper_blind/calibration_diagnostic.py",
    "cubic_one_pure_audit/exact_faces.py",
    "cubic_one_pure_audit/critical_replay.py",
    "calibration_audit/exact_checks.py",
    "sharp_centered_audit/independent_checks.py",
    "curie_weiss/exact_marginals.py",
    "critical_window_blind/verify_critical_window.py",
    "critical_quantitative_audit/check_critical.py",
]
READONLY_DEPENDENCIES = {
    "critical_quantitative_audit/check_critical.py": [
        "curie_weiss/CRITICAL_PROOF_FROZEN.md",
    ],
}


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def replay(name):
    src = SOURCE / name
    slug = name.replace("/", "__").removesuffix(".py")
    stage_for_script = STAGE / slug
    target = stage_for_script / name
    target.parent.mkdir(parents=True, exist_ok=True)
    for sibling in src.parent.glob("*.py"):
        shutil.copy2(sibling, target.parent / sibling.name)
    for dependency in READONLY_DEPENDENCIES.get(name, []):
        dependency_target = stage_for_script / dependency
        dependency_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE / dependency, dependency_target)
    started = time.monotonic()
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1",
               MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONHASHSEED="0")
    try:
        proc = subprocess.run([sys.executable, str(target)], cwd=target.parent,
                              env=env, text=True, capture_output=True, timeout=240)
        code, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
        status = "PASS_EXIT" if code == 0 else "FAIL_EXIT"
    except subprocess.TimeoutExpired as err:
        code, status = None, "TIMEOUT"
        stdout = err.stdout or ""
        stderr = err.stderr or ""
        if isinstance(stdout, bytes): stdout = stdout.decode(errors="replace")
        if isinstance(stderr, bytes): stderr = stderr.decode(errors="replace")
    (OUT / f"{slug}.stdout.txt").write_text(stdout)
    (OUT / f"{slug}.stderr.txt").write_text(stderr)
    generated = []
    for path in target.parent.glob("*.json"):
        dest = OUT / slug / path.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        generated.append({"path": dest.relative_to(OUT).as_posix(), "sha256": digest(dest)})
    return {"script": name, "script_sha256": digest(src), "status": status,
            "exit_code": code, "seconds": round(time.monotonic()-started, 3),
            "stdout": f"{slug}.stdout.txt", "stderr": f"{slug}.stderr.txt",
            "generated": generated,
            "interpretation": "Reproduction of the script's scoped exact/numerical diagnostics, not proof certification or external review."}


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    STAGE.mkdir(parents=True, exist_ok=True)
    selected = sys.argv[1:] or SCRIPTS
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(replay, selected))
    payload = {"started_utc": STAMP, "finished_utc": datetime.now(timezone.utc).isoformat(),
               "python": sys.version, "parallel_processes": 2,
               "isolation": "Scripts copied into a separate scratch tree; frozen research inputs not modified.",
               "results": results}
    (OUT / "REPLAY.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"report": str(OUT / "REPLAY.json"),
                      "passed": sum(r["status"] == "PASS_EXIT" for r in results),
                      "total": len(results),
                      "failures": [r["script"] for r in results if r["status"] != "PASS_EXIT"]}))
    sys.exit(any(r["status"] != "PASS_EXIT" for r in results))
