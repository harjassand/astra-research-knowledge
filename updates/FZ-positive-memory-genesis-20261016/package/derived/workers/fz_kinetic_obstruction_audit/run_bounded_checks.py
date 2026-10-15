"""Run only fixed-size algebra checks in the audit directory, with hard timeouts."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
env = os.environ.copy()
env.update(PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
records = []
for relative, timeout in [("replay/verify_algebra.py", 45), ("audit_checks.py", 45)]:
    script = ROOT / relative
    cwd = script.parent
    cmd = [sys.executable, "-B", str(script)]
    start = time.perf_counter()
    timed_out = False
    try:
        result = subprocess.run(cmd, cwd=cwd, env=env, text=True,
                                capture_output=True, timeout=timeout, check=False)
        code, stdout, stderr = result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as error:
        timed_out = True
        code = None
        stdout = error.stdout or ""
        stderr = error.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
    elapsed = time.perf_counter() - start
    stem = script.stem
    (ROOT / f"{stem}.stdout.txt").write_text(stdout)
    (ROOT / f"{stem}.stderr.txt").write_text(stderr)
    record = {"command": cmd, "cwd": str(cwd), "timeout_seconds": timeout,
              "elapsed_wall_seconds": elapsed, "exit_code": code,
              "timed_out": timed_out,
              "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
              "stdout_file": f"{stem}.stdout.txt", "stderr_file": f"{stem}.stderr.txt"}
    records.append(record)
    print(json.dumps(record), flush=True)
receipt = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "scope": "Copied original algebra script and independent fixed-size checks only. No kinetics or FSP execution.",
           "runs": records}
(ROOT / "replay_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
sys.exit(0 if all(r["exit_code"] == 0 and not r["timed_out"] for r in records) else 1)
