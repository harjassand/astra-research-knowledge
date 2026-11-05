"""Bind completed artifacts and preserve the earlier package byte-for-byte."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
WARM_NAME = "acquired_passive_environment_research_package.zip"
WARM_HASH = "98350f429ad0abff06f908b4bcaac9a14d0ea59e105760884a44d083fb7673e5"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    warm = ROOT / "warm" / WARM_NAME
    if not warm.exists():
        warm = ROOT.parent / WARM_NAME
    assert warm.is_file() and sha(warm) == WARM_HASH
    assert warm.stat().st_size == 5423526
    contract = json.loads((ROOT / "bridge/operation_contract_verification.json").read_text())
    assert contract["checks_passed"] == 58
    for name, digest in contract["input_sha256"].items():
        assert sha(ROOT / "bridge" / name) == digest, name
    planner = json.loads((ROOT / "structural/robust_planner_verification.json").read_text())
    assert planner["gap_exact"] == "0"
    assert planner["parametric_duality_gap_identically_zero"]
    assert planner["planner_certificate_sha256"] == sha(ROOT / "structural/robust_planner_certificate.json")
    pathcheck = json.loads((ROOT / "structural/robust_planner_path_verification.json").read_text())
    assert pathcheck["verified"]
    assert pathcheck["path_sha256"] == sha(ROOT / "structural/robust_planner_prediction_path.json")
    assert pathcheck["planner_certificate_sha256"] == planner["planner_certificate_sha256"]
    table_hash = sha(ROOT / "bridge/acquired_step_response.json")
    assert planner["acquired_table_sha256"] == table_hash == pathcheck["table_sha256"]
    receipt = {
        "status": "complete finite conditional construction with joined execution",
        "selected_operation": "randomized predictive preparation and acquired response for a passive locally dissipative scalar LTI port",
        "response_table_sha256": table_hash,
        "report_sha256": sha(ROOT / "predictive_preparation.pdf"),
        "contract_checks": 58,
        "all_variation_at_most_one_error": contract["prediction"]["all_W_at_most_one_bound_exact"],
        "executed_query_error": contract["prediction"]["actual_query_bound_exact"],
        "conditional_success": contract["prediction"]["conditional_success_exact"],
        "planner_exact_gap": "0",
        "planner_all_time_band": ["-3/10", "3/10"],
        "warm_sha256": WARM_HASH,
        "evidence": {
            "analytic": "finite operation within declared physical and metrology contracts",
            "exact": "parameter implications, acquired polynomial identity, LP primal-dual and parametric certificates",
            "floating": "source and sensor illustration; not interval validated",
            "entropy": "PRNG illustration; physical private entropy remains a contract",
            "deployment": "one retained-source query simulated; planner counterfactual only",
            "historical_priority": "not established"
        }
    }
    (ROOT / "COMPLETE_OPERATION_RECEIPT.json").write_text(json.dumps(receipt, indent=2)+"\n")
    files = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or "__pycache__" in p.parts or "warm" in p.relative_to(ROOT).parts:
            continue
        if p.name == "MANIFEST.json" or p.suffix in {".pyc", ".log", ".aux", ".out", ".toc"}:
            continue
        files.append(p)
    manifest = {"format": "sha256", "files": [
        {"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size, "sha256": sha(p)} for p in files
    ]}
    manifest["files"].append({"path": "warm/"+WARM_NAME, "bytes": warm.stat().st_size, "sha256": WARM_HASH})
    mf = ROOT / "MANIFEST.json"
    mf.write_text(json.dumps(manifest, indent=2)+"\n")
    target = ROOT.parent / "predictive_preparation_research_package.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED, compresslevel=8) as z:
        for p in files+[mf]:
            z.write(p, str(p.relative_to(ROOT)))
        z.write(warm, "warm/"+WARM_NAME)
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        assert hashlib.sha256(z.read("warm/"+WARM_NAME)).hexdigest() == WARM_HASH
        for item in manifest["files"]:
            data=z.read(item["path"])
            assert len(data)==item["bytes"]
            assert hashlib.sha256(data).hexdigest()==item["sha256"]
    result={"archive": str(target), "bytes":target.stat().st_size,"sha256":sha(target),
            "members":len(manifest["files"])+1,"warm_preserved":True}
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
