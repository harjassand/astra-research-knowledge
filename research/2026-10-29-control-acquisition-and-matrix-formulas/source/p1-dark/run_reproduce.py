"""Reproduce this continuation from its archive without network or equipment."""
from pathlib import Path
from hashlib import sha256
import json
import platform
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent
PRIOR_NAME = "Astra_P1_Operational_Response_Continuation.zip"
PRIOR_SHA = "b4b1f44234e8fea08bc5c2596527ffe4588fc03ad61285d23eb95f5fde77f549"


def bootstrap():
    prior = WORK / "preserved" / PRIOR_NAME
    if not prior.exists():
        prior = WORK / PRIOR_NAME
    assert sha256(prior.read_bytes()).hexdigest() == PRIOR_SHA
    with zipfile.ZipFile(prior) as archive:
        selected = [name for name in archive.namelist()
                    if name.startswith("p1_next/") and not name.endswith("/")]
        assert selected
        for name in selected:
            assert ".." not in Path(name).parts and not Path(name).is_absolute()
            destination = WORK / name
            payload = archive.read(name)
            if destination.exists():
                assert destination.read_bytes() == payload, "Prior version differs: " + name
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(payload)
    return {"prior_archive_sha256": PRIOR_SHA, "prior_files_checked_or_extracted": len(selected)}


def main():
    import numpy
    import scipy
    prior = bootstrap()
    scripts = ["code/simplex_law_checks.py", "selection/inference_determinant_tail_checks.py",
               "shifted_checks.py", "reviews/determinant_review_checks.py",
               "reviews/curvature_review_checks.py", "reviews/curvature_correction_checks.py",
               "code/run_lattice_experiments.py", "code/run_curvature_refinement.py",
               "code/summarize_costs.py"]
    receipt = {"scope": "Finite software reproduction only; no physical operation or whole-proof audit.",
               "python": sys.version, "platform": platform.platform(),
               "numpy": numpy.__version__, "scipy": scipy.__version__,
               "prior": prior, "commands": []}
    logs = ROOT / "results" / "reproduction_logs"
    logs.mkdir(parents=True, exist_ok=True)
    for relative in scripts:
        path = ROOT / relative
        started = time.monotonic()
        run = subprocess.run([sys.executable, str(path)], cwd=WORK,
                             text=True, capture_output=True, timeout=300)
        elapsed = time.monotonic() - started
        log = logs / (path.stem + ".txt")
        log.write_text(run.stdout + ("\nSTDERR\n" + run.stderr if run.stderr else ""))
        row = {"script": relative, "script_sha256": sha256(path.read_bytes()).hexdigest(),
               "exit_code": run.returncode, "seconds": round(elapsed, 4),
               "output_sha256": sha256(log.read_bytes()).hexdigest()}
        receipt["commands"].append(row)
        print(json.dumps(row), flush=True)
        assert run.returncode == 0, run.stderr
    receipt["all_passed"] = True
    (ROOT / "results/REPRODUCTION_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    main()
