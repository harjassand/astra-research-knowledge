#!/usr/bin/env python3
"""Verify the selected release; optional scientific replays use a temporary copy."""
import argparse
import datetime
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent
EXACT = [
    ("kinetic-algebra-rank", "reviews/kinetic_proof/independent_exact_check.py", True),
    ("kinetic-independent-box", "reviews/kinetic_certificate/independent_certificate_check.py", True),
    ("independent-scalar-intervals", "reviews/pro_certificates/independent_arithmetic.py", True),
    ("source-entropy-certificate", "sources/pro/markov_family/certify_entropy.py", True),
    ("source-hidden-certificate", "sources/pro/hidden_state/certify_hidden_bounds.py", True),
    ("source-decimal-scalar", "sources/pro/markov_family/independent_check.py", True),
]
ADDITIONAL = [
    ("markov-all-logarithms-and-intervals", "reviews/markov_proof/disposable/independent_check.py", False),
    ("embedding-selected-counterexamples", "reviews/embedding_prior/independent_embedding_audit.py", False),
    ("source-kinetic-jacobian", "sources/ultra/workers/kinetic_realization/fixed_hazard_jacobian.py", False),
    ("source-kinetic-collision", "sources/ultra/workers/kinetic_frontier/exact_collision_certificate.py", False),
    ("general-entropy-diagnostics", "reviews/general_entropy/check_general_entropy.py", False),
    ("hidden-entropy-diagnostics", "reviews/hidden_proof/audit_checks.py", False),
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def integrity():
    manifest = json.loads((ROOT / "FILES.json").read_text())
    expected = set()
    for item in manifest["files"]:
        relative = Path(item["path"])
        assert not relative.is_absolute() and ".." not in relative.parts
        path = ROOT / relative
        assert path.is_file() and not path.is_symlink(), relative
        data = path.read_bytes()
        assert len(data) == item["bytes"] and digest(data) == item["sha256"], relative
        expected.add(relative.as_posix())
    excluded = {"FILES.json", "REPLAY.json"}
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and p.name not in excluded and "__pycache__" not in p.parts}
    assert actual == expected, (sorted(actual - expected), sorted(expected - actual))
    provenance = json.loads((ROOT / "PROVENANCE.json").read_text())
    copied = 0
    for item in provenance["files"]:
        if item["treatment"] == "unchanged_bytes":
            assert digest((ROOT / item["path"]).read_bytes()) == item["original_sha256"], item["path"]
            copied += 1
    return {"retained_files_checked": len(expected), "unchanged_byte_copies_checked": copied}


def links():
    checked = 0
    # Original research sources are retained verbatim; review/publication navigation is checked here.
    for path in [ROOT / "README.md", *sorted((ROOT / "reviews").rglob("*.md"))]:
        for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", path.read_text()):
            target = target.strip("<>")
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0])
            assert (path.parent / target).is_file(), (path.relative_to(ROOT).as_posix(), target)
            checked += 1
    return checked


def replay(mode):
    results = []
    with tempfile.TemporaryDirectory(prefix="astra-selected-math-") as directory:
        copy = Path(directory) / "release"
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns("__pycache__"))
        for name, relative, isolated in EXACT + (ADDITIONAL if mode == "all" else []):
            start = time.monotonic()
            flags = ["-I", "-B"] if isolated else ["-E", "-B"]
            run = subprocess.run([sys.executable, *flags, str(copy / relative)], cwd=copy, text=True, capture_output=True, timeout=180)
            item = {
                "name": name, "script": relative, "flags": flags,
                "exit_code": run.returncode, "elapsed_seconds": round(time.monotonic() - start, 4),
                "stdout_sha256": digest(run.stdout.encode()),
                "stderr": run.stderr.replace(directory, "<temporary-copy>"),
            }
            if run.returncode:
                item["stdout_tail"] = run.stdout[-2000:].replace(directory, "<temporary-copy>")
                results.append(item)
                raise RuntimeError(json.dumps({"replay_failure": item}, indent=2))
            # Exact source outputs must reproduce the archived mathematical receipts.
            archive = {
                "source-entropy-certificate": "sources/pro/markov_family/certified_result.json",
                "source-hidden-certificate": "sources/pro/hidden_state/certified_bounds.json",
            }.get(name)
            if archive:
                assert json.loads(run.stdout) == json.loads((ROOT / archive).read_text()), name
                item["archived_json_values_match"] = True
            if name == "embedding-selected-counterexamples":
                receipt = json.loads((copy / "reviews/embedding_prior/independent_checks.json").read_text())
                assert receipt["all_symbolic_checks_pass"]
                item["exact_symbolic_check_count"] = len(receipt["symbolic_checks"])
            results.append(item)
            print(name + ": PASS", flush=True)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", choices=("exact", "all"))
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    assert not sys.flags.optimize, "Assertions must be enabled"
    initial = integrity()
    dependencies = {}
    for name in ("sympy", "mpmath", "numpy", "scipy"):
        try:
            dependencies[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            dependencies[name] = "UNAVAILABLE"
    result = {"status": "PASS", "created_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "scope": "File/provenance integrity and named finite replays only; no universal proof, novelty, external expert or experimental certification",
              "python": platform.python_version(), "platform": platform.system(), "architecture": platform.machine(), "dependencies": dependencies,
              "integrity": initial, "local_markdown_links_checked": links(), "mode": args.replay or "integrity", "runs": []}
    if args.replay:
        result["runs"] = replay(args.replay)
        assert integrity() == initial, "Retained release changed during replay"
    if args.receipt:
        with args.receipt.open("x") as handle:
            json.dump(result, handle, indent=2)
            handle.write("\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
