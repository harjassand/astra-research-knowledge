#!/usr/bin/env python3
"""Verify the frozen payload, and optionally reproduce only Cycle9 checks.

Hash checks are provenance checks, not mathematical proof verification.
The preserved frozen coalescence fixture intentionally fails KL admission.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def scientific_signature(result):
    """Exclude only observed process times/RSS, not scientific outcomes."""
    return sha(json.dumps({k: v for k, v in result.items() if k != "cost"},
                          sort_keys=True, separators=(",", ":")).encode())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-checks", action="store_true",
                        help="Reproduce the two frozen new fixtures; preserve expected KL failure")
    args = parser.parse_args()
    manifest = read_json(ROOT / "MANIFEST.json")
    entries = manifest["files"]
    for item in entries:
        path = ROOT / item["path"]
        require(path.resolve().is_relative_to(ROOT), "Unsafe manifest path")
        data = path.read_bytes()
        require(len(data) == item["bytes"], "Size mismatch: " + item["path"])
        require(sha(data) == item["sha256"], "Hash mismatch: " + item["path"])

    original = ROOT / "sources/Astra_Amplification_Cycle8_PRO3_20261022.zip"
    require(original.stat().st_size == 2582117, "Original source size changed")
    require(sha(original.read_bytes()) ==
            "f2f21967f361266a42f03cac6a51e3e5e16ec6f22593756f5c1bbed881753fdb",
            "Original source identity changed")
    receipt = read_json(ROOT / "reviews/SHARP_RATE_REVIEW.receipt.json")
    proof = (ROOT / "SHARP_DISTORTION_RATE.md").read_bytes()
    review = (ROOT / "reviews/SHARP_RATE_REVIEW.md").read_bytes()
    require(sha(proof) == receipt["principal_source"]["sha256"],
            "Review is not bound to this proof")
    require(sha(review) == receipt["review_source"]["sha256"], "Review text mismatch")

    expected = {}
    for name in ("expansion_native32", "coalescence_native5462"):
        result = read_json(ROOT / "evidence/exact" / (name + ".json"))
        require(result["model_checks_pass"] and not result["identity_and_inequality_failures"],
                "Recorded native model checks failed: " + name)
        expected[name] = result
    require(expected["expansion_native32"]["KL"]["admitted_under_frozen_K"],
            "Frozen expansion admission changed")
    failed = expected["coalescence_native5462"]
    require(not failed["KL"]["admitted_under_frozen_K"] and failed["KL"]["nonadmission_proved"],
            "Expected proved coalescence nonadmission was lost")
    require(read_json(ROOT / "evidence/exact/RUN_RESULT.json")["execution_exit_code"] == 1,
            "Original failed scientific gate was relabelled")

    output = {"payload_files_verified": len(entries), "original_source_unchanged": True,
              "review_bound_to_current_proof": True,
              "frozen_admission_pattern": {"expansion_native32": "admitted",
                                            "coalescence_native5462": "proved nonadmitted"},
              "historical_suites_run": 0, "new_checks_executed": False,
              "hash_verification_is_mathematical_proof": False}
    if args.execute_checks:
        with tempfile.TemporaryDirectory(prefix="astra_pro3_cycle9_replay_") as temp:
            directory = Path(temp) / "exact"
            child = subprocess.run([sys.executable, str(ROOT / "code/exact_checks.py"),
                                    "--output-dir", str(directory)],
                                   capture_output=True, text=True, check=False)
            require(child.returncode == 1,
                    "Expected one scientific admission failure; child output:\n" + child.stdout + child.stderr)
            signatures = {}
            for name, result in expected.items():
                actual = read_json(directory / (name + ".json"))
                signature = scientific_signature(actual)
                require(signature == scientific_signature(result),
                        "Substantive exact outcome mismatch: " + name)
                signatures[name] = signature
            output.update({"new_checks_executed": True, "child_exit_code": child.returncode,
                           "expected_failed_admission_reproduced": True,
                           "substantive_result_signatures": signatures,
                           "fresh_process_receipt": read_json(directory / "RESOURCE_RECEIPT.json")})
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, OSError) as exc:
        print("VERIFICATION FAILED: " + str(exc), file=sys.stderr)
        raise SystemExit(2)
