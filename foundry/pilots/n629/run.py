"""Serial, bounded, stdlib-only pilot runner for macOS/Linux.

Runs untouched source scripts in temporary copies. wait4 measures each child,
including failed children. CPU/address-space limits apply to each child. The
wall-clock timeout covers startup/imports as well as computation.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import resource
import shutil
import signal
import subprocess
import sys
import tempfile
import time

from common import PILOT, REVISION, ROOT, SOURCE, dump, sha


def measure(command, cwd, stem, wall_limit=120, cpu_limit=100):
    start = time.perf_counter()
    started = datetime.now(timezone.utc).isoformat()
    limits = {"wall_seconds": wall_limit, "cpu_seconds": cpu_limit,
              "address_space_bytes": None if sys.platform == "darwin" else 1024**3,
              "rss_guard_bytes": 256*1024**2, "rss_guard_poll_seconds": .2,
              "memory_limit_note": "Darwin rejects RLIMIT_AS on this host; RSS guard is sampled and can overshoot" if sys.platform == "darwin" else "RLIMIT_AS plus sampled RSS guard"}
    def limit():
        os.setsid()
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit+1))
        if sys.platform != "darwin":
            resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    with stem.with_suffix(".stdout.txt").open("wb") as out, stem.with_suffix(".stderr.txt").open("wb") as err:
        child = subprocess.Popen(command, cwd=cwd, stdout=out, stderr=err, env=env, preexec_fn=limit)
        timed_out = False
        memory_limited = False
        next_memory_check = start
        while True:
            pid, status, usage = os.wait4(child.pid, os.WNOHANG)
            if pid:
                break
            if time.perf_counter()-start > wall_limit:
                timed_out = True
                os.killpg(child.pid, signal.SIGKILL)
                _, status, usage = os.wait4(child.pid, 0)
                break
            if time.perf_counter() >= next_memory_check:
                sampled = subprocess.run(["ps", "-o", "rss=", "-p", str(child.pid)], capture_output=True, text=True)
                if sampled.stdout.strip() and int(sampled.stdout.strip())*1024 > limits["rss_guard_bytes"]:
                    memory_limited = True
                    os.killpg(child.pid, signal.SIGKILL)
                    _, status, usage = os.wait4(child.pid, 0)
                    break
                next_memory_check = time.perf_counter()+.2
            time.sleep(.02)
        child.returncode = os.waitstatus_to_exitcode(status)
    receipt = {"command": command, "cwd": str(cwd), "started_at": started,
               "status": "memory_limit" if memory_limited else ("timed_out" if timed_out else ("passed" if child.returncode == 0 else "failed")),
               "exit_code": child.returncode, "wall_seconds": time.perf_counter()-start,
               "cpu_seconds": usage.ru_utime+usage.ru_stime,
               "peak_rss_bytes": usage.ru_maxrss * (1 if sys.platform == "darwin" else 1024),
               "limits": limits, "stdout_sha256": sha(stem.with_suffix(".stdout.txt")),
               "stderr_sha256": sha(stem.with_suffix(".stderr.txt"))}
    dump(stem.with_suffix(".receipt.json"), receipt)
    return receipt


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main(output):
    # Fresh paths preserve failures and prevent silent replacement of evidence.
    output.mkdir(parents=True, exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    source_paths = sorted(SOURCE.iterdir())
    records = [{"path": str(p.relative_to(ROOT)), "sha256": sha(p), "bytes": p.stat().st_size,
                "hash_kind": "original_utf8_bytes"} for p in source_paths if p.is_file()]
    for entry in json.loads((SOURCE/"MANIFEST.json").read_text())["files"]:
        assert sha(SOURCE/entry["name"]) == entry["sha256"]
        assert (SOURCE/entry["name"]).stat().st_size == entry["bytes"]
    # Require exact pinned source files even when running from the PR commit.
    context_paths = ["00_START_HERE.txt", "AGENTS.md", "evaluation/PROTOCOL.md", "frontier/SCHEMA.md",
                     "evaluation/templates/PROOF_GATES.json", "evaluation/templates/CHECKER_RECEIPT.json",
                     "state/branches.tsv", "state/branches/primitive-genesis.txt", "state/branches/theoretical-pro.txt",
                     "cards/N629-binary-additive-sunflower-good-pairs-fpt-sampler.txt",
                     "frontier/cards/N629-binary-additive-sunflower-good-pairs-fpt-sampler.json",
                     "frontier/dossiers/N629.txt",
                     "frontier/gates/G-CS-N629.json", "updates/CS/README.md"]
    for path in [r["path"] for r in records] + context_paths:
        original = subprocess.check_output(["git", "show", f"{REVISION}:{path}"], cwd=ROOT)
        assert original == (ROOT/path).read_bytes(), ("changed pinned input", path)
    environment = {"source_revision": REVISION, "checkout_head": git("rev-parse", "HEAD"),
                   "branch": git("branch", "--show-current"), "python": sys.version,
                   "python_executable": sys.executable, "python_flags": str(sys.flags),
                   "platform": platform.platform(), "machine": platform.machine(),
                   "processor": platform.processor(), "cpu_count": os.cpu_count(),
                   "stdlib_only": True, "hash_seed_for_children": "0", "started_at": started,
                   "git_version": git("--version"), "source_records": records,
                   "context_records": [{"path": p, "sha256": sha(ROOT/p), "bytes": (ROOT/p).stat().st_size}
                                       for p in context_paths],
                   "implementation_records": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p), "bytes": p.stat().st_size}
                                              for p in sorted(PILOT.glob("*.py"))],
                   "resource_scope": "Child-process measurements only. Interactive agent, Git clone, preparation and review costs are not measured; no comparative model/cost eligibility claim.",
                   "additional_model_agents": 0, "paid_model_api_calls": 0}
    dump(output/"environment.json", environment)
    receipts, reproductions = [], []
    with tempfile.TemporaryDirectory(prefix="n629-source-") as temp:
        copied = Path(temp)/"original"
        copied.mkdir()
        for file in SOURCE.glob("*.py"):
            shutil.copyfile(file, copied/file.name)
        for script, result_file in [("fpt_sampler.py", "fpt_sampler_results.json"),
                                    ("verify_gate.py", "verification_results.json"),
                                    ("exact_m5.py", "exact_m5_results.json")]:
            stem = output/script.removesuffix(".py")
            receipt = measure([sys.executable, "-B", script], copied, stem)
            receipts.append(receipt)
            record = {"script": script, "source_command": "python " + script, "receipt": stem.name+".receipt.json"}
            if (copied/result_file).exists():
                shutil.copyfile(copied/result_file, output/result_file)
                observed = json.loads((copied/result_file).read_text())
                historical = json.loads((SOURCE/result_file).read_text())
                observed.pop("seconds", None)
                historical.pop("seconds", None)
                record["matches_archived_result_except_seconds"] = observed == historical
            else:
                record["matches_archived_result_except_seconds"] = False
            reproductions.append(record)
    checks = measure([sys.executable, "-B", str(PILOT/"check.py"), str(output/"checks.json")], ROOT, output/"checks", wall_limit=180, cpu_limit=160)
    receipts.append(checks)
    from benchmark import SCENARIOS
    benchmarks = []
    for index, case in enumerate(SCENARIOS):
        for method in ("fpt", "brute", "rejection"):
            for replicate in range(3):
                stem = output/f"bench_{case['id']}_{method}_{replicate}"
                receipt = measure([sys.executable, "-B", str(PILOT/"benchmark.py"), str(index), method, str(replicate)], ROOT, stem, wall_limit=45, cpu_limit=40)
                receipts.append(receipt)
                row = {"scenario": case["id"], "method": method, "replicate": replicate, "receipt": stem.name+".receipt.json"}
                if receipt["exit_code"] == 0:
                    row.update(json.loads(stem.with_suffix(".stdout.txt").read_text()))
                else:
                    row["status"] = receipt["status"]
                row.update(process_wall_seconds=receipt["wall_seconds"], cpu_seconds=receipt["cpu_seconds"], peak_rss_bytes=receipt["peak_rss_bytes"])
                benchmarks.append(row)
    # Cross-method exact counts and analytic product cases; retain any discrepancy.
    for case in SCENARIOS:
        counts = {row["exact_count"] for row in benchmarks if row["scenario"] == case["id"] and "exact_count" in row}
        assert len(counts) <= 1, (case["id"], counts)
        if case["id"] == "large_m30_w3":
            assert counts == {(4**10-3*2**10+3)**3}
    dump(output/"reproductions.json", reproductions)
    dump(output/"benchmarks.json", benchmarks)
    source_unchanged = all(sha(ROOT/r["path"]) == r["sha256"] for r in records)
    successful = (source_unchanged and all(r["status"] == "passed" for r in receipts)
                  and all(r["matches_archived_result_except_seconds"] for r in reproductions)
                  and all(r["status"] in ("passed", "skipped_pair_budget") for r in benchmarks))
    summary = {"kind": "finite_diagnostic", "status": "passed" if successful else "failed",
               "source_revision": REVISION, "started_at": started, "ended_at": datetime.now(timezone.utc).isoformat(),
               "source_bytes_unchanged": source_unchanged, "child_processes": len(receipts),
               "child_cpu_seconds": sum(r["cpu_seconds"] for r in receipts),
               "child_wall_seconds": sum(r["wall_seconds"] for r in receipts),
               "peak_child_rss_bytes": max(r["peak_rss_bytes"] for r in receipts),
               "independent_scientific_verification": False,
               "scientific_discovery_evidence": False,
               "benchmark_skips": [r for r in benchmarks if r["status"] != "passed"],
               "failed_receipts": [r for r in receipts if r["status"] != "passed"]}
    dump(output/"summary.json", summary)
    dump(output/"artifact_manifest.json", [{"path": p.name, "sha256": sha(p), "bytes": p.stat().st_size}
                                          for p in sorted(output.iterdir()) if p.is_file()])
    print(json.dumps(summary, indent=2))
    return 0 if successful else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Fresh output directory; existing directories are refused")
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error("output already exists; choose a fresh path to preserve prior evidence")
    try:
        exit_code = main(output)
    except Exception:
        import traceback
        output.mkdir(parents=True, exist_ok=True)
        dump(output/"harness_failure.json", {"status": "failed", "traceback": traceback.format_exc(),
                                           "command": sys.argv, "kind": "implementation_failure"})
        raise
    raise SystemExit(exit_code)
