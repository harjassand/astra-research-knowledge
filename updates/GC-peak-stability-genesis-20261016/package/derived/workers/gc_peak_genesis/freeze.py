"""Integrity receipts only. Does not certify theorem correctness or novelty."""
import datetime
import hashlib
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
R = HERE.parent.parent
W = pathlib.Path("/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016")
EXPECTED = "9dbe934e5475f415c2d160a6c0715534aafa546b"
head = subprocess.check_output(["git", "-C", str(W), "rev-parse", "HEAD"], text=True).strip()
assert head == EXPECTED, (head, EXPECTED)

paths = [
    W / "AGENTS.md",
    W / "00_START_HERE.txt",
    W / "frontier/dossiers/N890.txt",
    W / "updates/GB-dots-capital-genesis-20261016/package/derived/workers/gb_finite_rate_genesis/COST_AND_INCUMBENT.md",
    W / "updates/GB-dots-capital-genesis-20261016/package/derived/workers/gb_finite_rate_genesis/SHARP_POISSON_SYNDROME_THEOREM.md",
    W / "updates/GB-dots-capital-genesis-20261016/package/derived/workers/gb_primary_prior/REPORT.md",
    W / "updates/GB-dots-capital-genesis-20261016/package/originals/Dots/finite_rate_joint_syndrome_2026-10-15/tracked_control/FOURIER_INTERFACE_ADDENDUM.md",
    W / "updates/GB-dots-capital-genesis-20261016/package/originals/Dots/measurement_memory_handoff_2026-10-15/measurement/DETERMINISTIC_MEASUREMENT_CELL_COROLLARY.md",
    R / "originals/shared_bath/pr104_bath_audit/PEAK_RATE_CERTIFICATE_ADDENDUM.md",
    R / "originals/shared_bath/pr104_bath_audit/AUDIT_SUMMARY.md",
    R / "originals/shared_bath/pr104_bath_audit/check_peak_cap.py",
    R / "originals/Astra_shared_bath_peak_cap_2026-10-16.zip",
]


def receipt(path):
    data = path.read_bytes()
    return dict(path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


now = datetime.datetime.now(datetime.timezone.utc).isoformat()
inputs = dict(status="READ_ONLY_INPUT_RECEIPTS", capital_head=head, created_at=now,
              source_scripts_executed=False, note="The incoming ZIP is hashed as provenance; selected extracted local files were read. No input is edited.",
              files=[receipt(path) for path in paths])
(HERE / "INPUT_RECEIPTS.json").write_text(json.dumps(inputs, indent=2) + "\n")
checks = json.loads((HERE / "CHECK_RESULTS.json").read_text())
assert checks["status"] == "PASS"
files = [path for path in HERE.iterdir() if path.is_file() and path.name != "FROZEN_MANIFEST.json"]
manifest = dict(status="FROZEN", created_at=now, capital_head=head,
                scope="Authored analytic proofs and finite diagnostics only; external correctness, historical priority and acquired physical implementation UNKNOWN.",
                no_worktree_or_input_edits=True, no_subagents_spawned=True,
                files=[receipt(path) for path in sorted(files)])
(HERE / "FROZEN_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps(dict(status="FROZEN", files=len(files), manifest=str(HERE / "FROZEN_MANIFEST.json")), indent=2))
