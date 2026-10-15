"""Copy-first bounded replay; never executes research scripts on source evidence."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import time


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = Path(__file__).resolve().parents[1]
    dest = Path(tempfile.mkdtemp(prefix="astra-foundational-replay-")) / "campaign"
    omitted = {"sources", "replays", "__pycache__", ".DS_Store"}
    def ignore(folder, names):
        return [n for n in names if n in omitted or n.endswith((".pdf", ".png", ".pyc"))]
    shutil.copytree(source, dest, ignore=ignore)
    specs = [
        ("root/isotope_renewal.py", []),
        ("workers/physical_path/calculate.py", []),
        ("workers/scientific_operation/verify_operation.py", []),
        ("workers/foundational_math/verify_phase_clock.py", []),
        ("workers/foundational_math/verify_hidden_spectrum.py", []),
        ("workers/foundational_math/search_partial_injections.py", ["4"]),
        ("workers/abelian_sampler_audit/exact_audit.py", []),
        ("workers/capital_routes/n610_ring_benchmark.py", []),
    ]
    logdir = source / "replays"
    logdir.mkdir(exist_ok=True)
    def run(spec):
        rel, args = spec
        path = dest / rel
        if not path.exists():
            return {"script": rel, "status": "MISSING", "exit_code": None}
        argv = [sys.executable, "-B", str(path), *args]
        start = time.perf_counter()
        try:
            proc = subprocess.run(argv, cwd=path.parent, text=True, capture_output=True, timeout=180)
            stdout, stderr = proc.stdout, proc.stderr
            code = proc.returncode
            status = "PASS" if code == 0 else "FAIL"
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout or ""
            stderr = exc.stderr or ""
            if isinstance(stdout, bytes): stdout = stdout.decode(errors="replace")
            if isinstance(stderr, bytes): stderr = stderr.decode(errors="replace")
            code, status = None, "TIMEOUT"
        elapsed = time.perf_counter() - start
        stem = rel.replace("/", "__").removesuffix(".py")
        stdout_path = logdir / (stem + ".stdout.txt")
        stderr_path = logdir / (stem + ".stderr.txt")
        stdout_path.write_text(stdout)
        stderr_path.write_text(stderr)
        return {"script": rel, "args": args, "sha256": digest(source / rel),
                "status": status, "exit_code": code, "elapsed_wall_seconds": elapsed,
                "stdout": str(stdout_path.relative_to(source)),
                "stderr": str(stderr_path.relative_to(source)),
                "scope": "bounded synthetic/arithmetic/model computation; no laboratory or formal/novelty validation"}
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, specs))
    receipt = {"schema": "astra.foundational-capability.replay.v1",
               "method": "copy first; four independent subprocess slots; source reports unchanged",
               "python": sys.version, "executable": sys.executable, "platform": platform.platform(),
               "disposable_copy": str(dest), "omitted": sorted(omitted),
               "elapsed_wall_seconds": time.perf_counter()-start,
               "pure_inference_time_seconds": None, "model_tokens": None, "inference_energy_joules": None,
               "results": results, "all_passed": all(r["status"] == "PASS" for r in results)}
    out = source / "root/REPLAY_RECEIPTS.json"
    out.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"receipt": str(out), "all_passed": receipt["all_passed"],
                      "elapsed_wall_seconds": receipt["elapsed_wall_seconds"],
                      "results": [{"script":r["script"],"status":r["status"]} for r in results]}, indent=2))


if __name__ == "__main__":
    main()
