"""Replay the research package in an isolated new directory, preserving evidence."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--include-posterior-sampling", action="store_true")
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    output = args.output.resolve()
    if output.exists():
        raise SystemExit("Choose a new output directory; existing results are preserved.")
    output.mkdir(parents=True)
    for folder in (Path("."), Path("control"), Path("learning"), Path("computation")):
        (output/folder).mkdir(exist_ok=True)
        for path in (source/folder).glob("*.py"):
            if path.name != "replay.py":
                shutil.copy2(path, output/folder/path.name)
    shutil.copy2(source/"learning"/"learned_cubic_model.npz",
                 output/"learning"/"learned_cubic_model.npz")
    programs = [
        ["control/control_cap_checks.py"],
        ["learning/check_hermite_fixed.py"],
        ["learning/check_cubic_hardness.py"],
        ["learning/learn_quantized_cubic.py"],
        ["finite_precision.py"],
        ["finite_actuator.py"],
        ["computation/noisy_control_checks.py"],
        ["computation/posterior_certificate.py", "--output", "computation/posterior_results.json"],
    ]
    if not args.include_posterior_sampling:
        programs[-1].append("--skip-sampling")
    records = []
    for index, program in enumerate(programs, 1):
        started = time.perf_counter()
        result = subprocess.run([sys.executable, *program], cwd=output,
                                capture_output=True, text=True)
        log = output/f"replay_{index:02d}.log"
        log.write_text(result.stdout+"\nSTDERR\n"+result.stderr)
        record = dict(program=program, returncode=result.returncode,
                      elapsed_seconds=time.perf_counter()-started, log=log.name)
        records.append(record)
        print(json.dumps(record), flush=True)
        if result.returncode:
            break
    summary = dict(status="PASS" if len(records)==len(programs) and
                   all(row["returncode"]==0 for row in records) else "FAIL",
                   independent_output=str(output), programs=records,
                   posterior_sampling_included=args.include_posterior_sampling,
                   scope="Numerical replay supports the included proofs. No physical deployment or runtime advantage is certified.")
    (output/"replay_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    if summary["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
