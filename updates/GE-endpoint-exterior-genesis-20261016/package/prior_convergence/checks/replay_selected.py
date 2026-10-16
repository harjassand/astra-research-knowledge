"""Root replays of selected scientific assertions, with actual local CPU receipts."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import re
import subprocess
import time

BASE = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
CASES = [
    ("s01_controller_repair/check_moat_repair.py", "Finite two-counter repair and local gate-debt check"),
    ("s01_controller_repair/check_interleavings.py", "Finite separated-fault and exterior-progress trajectories"),
    ("s01_controller_repair/check_color_program.py", "Finite single-site color and static-program predicates"),
    ("l03_counter_repair/patch_completion_check.py", "Exact trusted-collar ambiguity and counter-edit invariant"),
    ("s04_scientific_invention/two_pulse_echo_replay.py", "Exact survival aliases and finite-moment kinetic reconstruction"),
    ("s04_scientific_invention/two_pulse_finite_time_replay.py", "Noiseless positive-duration reconstruction fixture"),
    ("s05_independent_challenger/dark_echo.py", "Synthetic finite-count classifier, dark-echo identity and matched likelihood"),
    ("s06_controller_adversary/s01_program_split_trace.py", "Two-fault program-copy no-service counterexample"),
    ("s06_controller_adversary/weighted_episode.py", "Exact quantitative noisy-wait counterexample to all-path exact safety"),
    ("s07_scientific_adversary/pulse_gauge.py", "Exact control-law similarity ambiguity and minimality counterexample"),
]

def run(case):
    rel, scope = case
    path = BASE / "workers" / rel
    started = time.time()
    result = subprocess.run(
        ["/usr/bin/time", "-p", "python3", str(path)],
        cwd=path.parent, text=True, capture_output=True, timeout=180,
    )
    log = result.stdout + "\nSTDERR\n" + result.stderr
    logfile = OUT / (path.parent.name + "__" + path.stem + ".log")
    logfile.write_text(log)
    timings = {m.group(1): float(m.group(2))
               for m in re.finditer(r"^(real|user|sys) ([0-9.]+)$", result.stderr, re.M)}
    return {
        "script": str(path.relative_to(BASE)), "scope": scope,
        "exit_code": result.returncode,
        "wall_seconds_observed": time.time() - started,
        "local_process_time_seconds": timings,
        "script_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "log": str(logfile.relative_to(BASE)),
        "log_sha256": hashlib.sha256(log.encode()).hexdigest(),
    }

if __name__ == "__main__":
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as pool:
        receipts = list(pool.map(run, CASES))
    payload = {
        "scope": "Root-selected finite/symbolic/numerical replays only; no asymptotic proof, physical validation or priority certification",
        "parallelism": 4,
        "root_replay_wall_seconds": time.time() - start,
        "sum_process_user_seconds": sum(r["local_process_time_seconds"].get("user", 0) for r in receipts),
        "sum_process_sys_seconds": sum(r["local_process_time_seconds"].get("sys", 0) for r in receipts),
        "inference_compute_and_tokens": "not exposed; local script CPU is not model inference",
        "previous_root_replay": "l02_history_algebra/history_closure.py passed earlier in this campaign; timing not captured",
        "receipts": receipts,
        "all_exit_zero": all(r["exit_code"] == 0 for r in receipts),
    }
    target = OUT / "ROOT_REPLAY_RECEIPTS.json"
    target.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({k: v for k, v in payload.items() if k != "receipts"}, indent=2))
    for r in receipts:
        print(r["exit_code"], r["script"], r["local_process_time_seconds"])
    raise SystemExit(0 if payload["all_exit_zero"] else 1)
