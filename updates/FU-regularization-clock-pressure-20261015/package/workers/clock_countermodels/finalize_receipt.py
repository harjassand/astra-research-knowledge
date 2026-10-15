#!/usr/bin/env python3
"""Record this worker's scoped artifacts and verification, without changing inputs."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
SOURCE = ROOT / "sources" / "clock_pasted.txt"
WORKTREE = Path("/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-regularization-clock-pressure-20261015")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


result = json.loads((OUT/"results.json").read_text())
assert result["status"] == "PASS"
assert result["script_sha256"] == digest(OUT/"check_clock.py")
assert digest(SOURCE) == "460208a1a8acb52fdd1ddb410ed0fc0958d4924d629a25782806de462d8ed7eb"
head = subprocess.check_output(["git", "-C", str(WORKTREE), "rev-parse", "HEAD"], text=True).strip()
assert head == "0c789ca775808e23e57138b56a393ad1e58cb15c"

review = [
    {"name": "absorbing_centrality", "scope": "Primary preprint Section V Proposition 2 statement and pathwise argument; greedy benefit/cost discussion. No full-paper audit.", "text_line_ranges_read": [[350, 540], [747, 859]]},
    {"name": "kinetic_path_sampling", "scope": "Primary manuscript introduction, II E elimination/reverse randomization/waiting-time construction, conclusion cost and alternatives.", "text_line_ranges_read": [[210, 245], [645, 720], [1130, 1187]]},
    {"name": "ill_conditioned_chains", "scope": "Primary article partial GT formulas/initial support, fill, kPS and eigendecomposition cost/conditioning, conclusions.", "text_line_ranges_read": [[140, 190], [260, 292]]},
    {"name": "conditioned_markov", "scope": "Primary author manuscript bibliographic identity and Section 4 Theorem 4.3/Remark 4.4. General Doob machinery only.", "text_line_ranges_read": [[45, 72], [228, 255]]},
    {"name": "kulkarni_abstract", "scope": "Publisher abstract read through web tool; direct archival fetch returned 403. Complete algorithms/proofs not read.", "url": "https://pubsonline.informs.org/doi/abs/10.1287/opre.37.1.151"},
    {"name": "rare_events_pgt_selection", "scope": "Indexed primary publisher text on pGT selection/competing traps read in follow-up web search. Not a raw-data replay or full-paper audit.", "url": "https://pubs.rsc.org/en/content/articlehtml/2024/cp/d3cp04199a"},
]
(OUT/"primary_review_receipts.json").write_text(json.dumps(review, indent=2)+"\n")

receipt = {
    "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "worker": "clock_countermodels_v3",
    "input_source": {"path": str(SOURCE), "sha256": digest(SOURCE), "scope": "Full pasted text read as data; original producer ZIP absent."},
    "capital_worktree": {"path": str(WORKTREE), "verified_head": head, "modified_by_worker": False},
    "capital_proof_read": str(WORKTREE/"updates/FT-direction-transport-20261015/synthesis/transport_damage/PROOFS.md"),
    "independent_output": ["General stopped-clock/marginal/supermodularity/signed covariance proofs", "Cause-conditioned pGT clock and signed covariance", "Cause-specific joint deadline/exposure bands", "Necessary and sufficient common-row-clock incompatibility theorem", "Exact same-reduction/certificate/finite-moment relative-tail obstruction", "Rare-branch iid acquisition lower bound"],
    "validation": {"status": result["status"], "script_sha256_matches_results": True, "counts": result["counts"], "results_sha256": digest(OUT/"results.json"), "scope": "Bounded exact rational synthetic checks plus explicitly marked decimal survival diagnostics and one exact rational Taylor risk enclosure."},
    "not_established": ["Producer LJ38 replay", "External proof validation", "Historical novelty", "Physical Markov model or rare-rate acquisition", "Material/device performance", "End-to-end computational advantage", "Universal relative timing-tail guarantee"],
    "disposition": "SOURCE_DERIVED_AND_INDEPENDENT_EXTENSION_UNREVIEWED; FOUNDATIONAL_CAPABILITY_NOT_ACHIEVED"
}
(OUT/"receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
files = sorted(p for p in OUT.rglob("*") if p.is_file() and p.name != "SHA256SUMS.txt")
(OUT/"SHA256SUMS.txt").write_text("".join(f"{digest(p)}  {p.relative_to(OUT)}\n" for p in files))
print(json.dumps({"receipt": str(OUT/"receipt.json"), "manifest_files": len(files), "status": result["status"]}, indent=2))
