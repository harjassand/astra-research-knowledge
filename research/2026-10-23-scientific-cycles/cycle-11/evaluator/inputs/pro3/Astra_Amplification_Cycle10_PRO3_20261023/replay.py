#!/usr/bin/env python3
"""Check Cycle10 integrity and frozen status; no historical suite is executed."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile


def digest(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--new-precision", action="store_true",
                        help="Also replay only the new two-state diagnostic in a fresh directory")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "MANIFEST.json").read_text())
    for rec in manifest["files"]:
        p = root / rec["path"]
        assert p.resolve().is_relative_to(root), rec["path"]
        assert not p.is_symlink(), rec["path"]
        assert digest(p) == (rec["bytes"], rec["sha256"]), rec["path"]
    archive = root / "sources" / "Astra_Amplification_Cycle9_PRO3_20261022.zip"
    assert digest(archive) == (3121759, "959dcd192aef8487bcd19fcb3466fe6ea6360d4780c3b9a8c892d04b8af03299")
    review = json.loads((root / "reviews" / "CRITICAL_TRANSPORT_REVIEW.receipt.json").read_text())
    assert digest(root / "CRITICAL_TRANSPORT_THEOREM.md") == (review["principal"]["bytes"], review["principal"]["sha256"])
    assert digest(root / "reviews" / "CRITICAL_TRANSPORT_REVIEW.md") == (review["review"]["bytes"], review["review"]["sha256"])
    assert review["verdict"] == "ACCEPT_WITH_EXPLICIT_SCOPE"
    records = root / "inputs" / "precedessor_exact"
    expansion = json.loads((records / "expansion_native32.json").read_text())
    coalescence = json.loads((records / "coalescence_native5462.json").read_text())
    assert expansion["KL"]["admitted_under_frozen_K"] is True
    assert expansion["all_frozen_gates_pass"] is True
    assert coalescence["KL"]["admitted_under_frozen_K"] is False
    assert coalescence["KL"]["nonadmission_proved"] is True
    assert coalescence["all_frozen_gates_pass"] is False
    result = {"payload_hashes_pass": len(manifest["files"]),
              "original_cycle9_bytes_unchanged": True,
              "principal_review_bound": True,
              "expansion_admitted": True,
              "coalescence_nonadmission_preserved": True,
              "historical_scientific_suites_executed": 0,
              "new_precision_executed": False}
    if args.new_precision:
        out = Path(tempfile.mkdtemp(prefix="astra_pro3_cycle10_precision_"))
        code = out / "precision_two_state.py"
        shutil.copy2(root / "contributors" / "precision_two_state.py", code)
        subprocess.run([sys.executable, str(code)], check=True)
        result["new_precision_executed"] = True
        result["new_precision_output_directory"] = str(out)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
