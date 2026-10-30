"""Replay the authored finite evidence. Run without Python -O.

Requires Python >=3.10 and NumPy. No external source, credentials, or network
is used. Ordinary proofs in the report/audits establish the general results;
this runner checks the retained finite calculations and execution paths.
"""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import platform
import subprocess
import sys
import time


def main():
    if not __debug__:
        raise SystemExit("Run without -O: the evidence uses assertions.")
    import numpy as np
    root = Path(__file__).resolve().parent
    out = root / "replay"
    out.mkdir(exist_ok=True)
    scripts = [
        "alternative/check_gaussian_quadratic.py",
        "alternative/check_noisy_uv.py",
        "alternative/check_model_robustness.py",
        "feedback/feedback_checks.py",
        "acquisition/group_acquisition.py",
        "two_round_quadratic.py",
    ]
    receipt = {
        "started": datetime.now(ZoneInfo("Australia/Brisbane")).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scope": "Seeded finite proof checks and fully charged synthetic executions; no device or runtime dominance claim.",
        "scripts": [],
    }
    for relative in scripts:
        path = root / relative
        name = path.stem
        start = time.perf_counter()
        result = subprocess.run([sys.executable, str(path)], cwd=root,
                                text=True, capture_output=True)
        elapsed = time.perf_counter() - start
        (out / (name + "_stdout.txt")).write_text(result.stdout)
        (out / (name + "_stderr.txt")).write_text(result.stderr)
        item = {"path": relative,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "returncode": result.returncode,
                "wall_seconds": elapsed}
        receipt["scripts"].append(item)
        if result.returncode == 0:
            decoded = json.loads(result.stdout)
            if decoded.get("status", "PASS") != "PASS":
                raise AssertionError(f"Failed status in {relative}")
            # This companion intentionally prints its result rather than
            # overwriting a file, so the runner saves its canonical record.
            if relative == "feedback/feedback_checks.py":
                (path.parent / "feedback_results.json").write_text(
                    json.dumps(decoded, indent=2) + "\n")
            print(f"PASS {relative} ({elapsed:.3f} s)", flush=True)
        else:
            receipt["status"] = "FAIL"
            (out / "replay_receipt.json").write_text(
                json.dumps(receipt, indent=2) + "\n")
            print(result.stderr, file=sys.stderr)
            raise SystemExit(result.returncode)
    receipt["status"] = "PASS"
    receipt["finished"] = datetime.now(ZoneInfo("Australia/Brisbane")).isoformat()
    receipt["total_wall_seconds"] = sum(r["wall_seconds"] for r in receipt["scripts"])
    (out / "replay_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "scripts": len(scripts),
                      "total_wall_seconds": receipt["total_wall_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
