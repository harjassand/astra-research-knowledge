#!/usr/bin/env python3
"""Replay bounded calculations on a disposable authored-file copy.

Does not execute acquired source documents or mutate worker outputs. CPU times
come from /usr/bin/time for each child and do not measure model inference.
"""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

PACKET = Path(__file__).resolve().parents[1]
JOBS = [
    ("guard", "workers/decision_control/verify_guard_bound.py", []),
    ("native", "workers/native_computation/verify_bounds.py", []),
    ("snapshot", "workers/snapshot_statistics/stats_plan.py", []),
    ("graph", "workers/clearance_topology/graph_audit.py", ["--max-n", "6"]),
    ("hydraulics", "workers/clearance_topology/hydraulic_audit.py", []),
    ("manufacturing", "workers/manufacturing/clearance_fixture.py", []),
    ("thermal_accounting", "workers/physical_information/verify_accounting.py", []),
    ("physical_adversary", "workers/physical_adversary/audit_calculations.py", []),
    ("competitor", "workers/competitors/charge_crossover.py", []),
    ("blind_transport", "workers/blind_channel_adversary/check_transport.py", []),
    ("erasure", "root/verify_erasure_design.py", []),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    start = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="astra-scientific-power-replay-") as tmp:
        scratch = Path(tmp)
        for src in PACKET.rglob("*"):
            if src.is_file() and src.suffix in {".py", ".json", ".md"} and "__pycache__" not in src.parts:
                dst = scratch/src.relative_to(PACKET)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

        def run(job):
            name, rel, args = job
            script = scratch/rel
            begun = time.perf_counter()
            cmd = ["/usr/bin/time", "-p", sys.executable, str(script), *args]
            try:
                p = subprocess.run(cmd, cwd=script.parent, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
                timings = dict((k, float(v)) for k, v in re.findall(
                    r"(?m)^(real|user|sys)\s+([0-9.]+)\s*$", p.stderr))
                generated = {}
                for path in script.parent.glob("*.json"):
                    before = PACKET/path.relative_to(scratch)
                    if not before.exists() or digest(before) != digest(path):
                        generated[path.name] = {"sha256":digest(path), "size_bytes":path.stat().st_size}
                return {"name":name,"script":rel,"script_sha256":digest(PACKET/rel),
                        "exit_code":p.returncode,"elapsed_seconds":time.perf_counter()-begun,
                        "child_times_seconds":timings,"stdout":p.stdout,"stderr":p.stderr,
                        "generated_in_disposable_copy":generated}
            except subprocess.TimeoutExpired as e:
                return {"name":name,"script":rel,"script_sha256":digest(PACKET/rel),
                        "exit_code":None,"status":"TIMEOUT_60_SECONDS",
                        "elapsed_seconds":time.perf_counter()-begun,
                        "stdout":str(e.stdout),"stderr":str(e.stderr)}

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            receipts = list(pool.map(run, JOBS))
    data = {"schema":"astra.scientific-power.replay.v1",
            "scope":"Bounded calculation replay; no proof, novelty, apparatus or mission validation",
            "python_executable":sys.executable,"python_version":sys.version,
            "parallelism":4,"elapsed_wall_seconds":time.perf_counter()-start,
            "all_passed":all(x.get("exit_code")==0 for x in receipts),
            "child_cpu_user_seconds":sum(x.get("child_times_seconds",{}).get("user",0) for x in receipts),
            "child_cpu_system_seconds":sum(x.get("child_times_seconds",{}).get("sys",0) for x in receipts),
            "receipts":receipts}
    (PACKET/"root/REPLAY_RECEIPTS.json").write_text(json.dumps(data,indent=2)+"\n")
    print(json.dumps({k:v for k,v in data.items() if k!="receipts"},indent=2))
    for x in receipts:
        print(json.dumps({"name":x["name"],"exit_code":x.get("exit_code"),
                          "elapsed_seconds":x["elapsed_seconds"]}))
    if not data["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
