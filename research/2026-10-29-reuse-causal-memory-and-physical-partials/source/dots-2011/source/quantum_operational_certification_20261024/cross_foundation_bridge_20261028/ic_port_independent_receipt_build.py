#!/usr/bin/env python3
"""Bind the independent scientific audit to checked local bytes. No source calls."""
from pathlib import Path
import hashlib, json

HERE = Path(__file__).resolve().parent
SOURCE = "IC_PORT_SHORT_DEPTH_COMPLETE_RECOVERY.md"
EXPECTED = "9481fa0a4df758dfc0a4fcb264d19629c463c1e1308617cf8166ea03b796ef10"
AUDIT = "IC_PORT_SHORT_DEPTH_COMPLETE_RECOVERY_INDEPENDENT_AUDIT.md"
FILES = [
    SOURCE,
    "IC_PORT_SHORT_DEPTH_COMPLETE_RECOVERY_pre_computability_record_clarification.md",
    AUDIT,
    "ic_port_independent_complete_check.py",
    "ic_port_independent_complete_check.json",
    "ic_port_independent_complete_check.log",
    "ic_port_independent_receipt_build.py",
    "ic_port_complete_kernel_check.py",
    "ic_port_complete_kernel_check.json",
    "ic_port_author_independent_replay.py",
    "ic_port_author_independent_replay.json",
    "ic_port_author_independent_replay.log",
    "SHORT_WORD_SEMIALGEBRAIC_PHYSICAL_PREDICTION.md",
    "SHORT_WORD_MODULUS_INDEPENDENT_RECEIPT.md",
    "SHORT_WORD_MODULUS_INDEPENDENT_RECEIPT.json",
]
def sha(name):
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()
assert sha(SOURCE) == EXPECTED, "Source changed: renewed scientific review required"
assert EXPECTED in (HERE / AUDIT).read_text()
ind = json.loads((HERE / "ic_port_independent_complete_check.json").read_text())
author = json.loads((HERE / "ic_port_complete_kernel_check.json").read_text())
assert ind["source_sha256"] == EXPECTED
assert ind["script_sha256"] == sha("ic_port_independent_complete_check.py")
assert author["source_sha256"] == EXPECTED, "Await author final-source result binding"
assert sha("ic_port_author_independent_replay.json") == sha("ic_port_complete_kernel_check.json")
assert sha("ic_port_independent_complete_check.json") == sha("ic_port_independent_complete_check.log")
out = {
    "status": "PASS_SCOPED_INDEPENDENT_RECEIPT",
    "reviewer": "producer-workspace/construct_complementary_fast_path",
    "date_utc": "2026-10-28",
    "source_sha256": EXPECTED,
    "source_original_sha256": "ace073d5ac56c030cf1535b632fea072ffb1e1809f721bd0af59733a919fefb2",
    "accepted": [
        "Declared ordinary complex-IC accessible quantum-port interface only",
        "Short-word equality implies every native-schedule/outcome multitime Choi kernel equality",
        "Complete prediction for finite entangled/recycling/caller-memory/adaptive controllers",
        "Fresh compact physical-pair semialgebraic modulus and rectangular complete-port hybrid",
        "Finite terminating exact count fitting with fully paid acquisition and preprocessing",
        "Fixed-service all-CPTP half-diamond recovery via explicit SDP and supplied physical compiler",
        "Ideal expected recordwise regret; actual record-averaged channel implementation guarantee",
    ],
    "not_received": [
        "Quantum conclusion for a classical-only or incomplete calibration interface",
        "Coherent native action labels or source-native classical outcome/environment amplitudes",
        "Rare normalized postselection or record-selected independent-input guarantees",
        "Actual expected conditional diamond regret from a single whole-map debit",
        "Generic efficiency, useful universal sample rate, priority or quantum advantage",
        "Execution of generic modulus QE, model acquisition, generic recovery SDP or physical synthesis",
    ],
    "required_clarifications_resolved": [
        "Terminating exact solving versus separately charged capped UNKNOWN abort mass",
        "Algebraic ideal descriptions or certified finite approximations with paid errors",
        "Explicit physical full-CPTP SDP and Kraus/Stinespring/compiler mechanism",
        "Retained complete calibration/selection records and reduced actual good-fit mass",
        "Record-averaged versus average record-conditioned diamond risk distinction",
        "Classical native actions/outcomes and finite positive parameter domains",
    ],
    "classical_receipt_not_inherited_for_quantum_interface": True,
    "source_edited_by_reviewer": False,
    "reviewer_supplied_SDP_and_implementation_clarification": True,
    "independent_code_imports_author_code": False,
    "blocking_findings": [],
    "independent_evidence": ind,
    "author_checks": {
        "role": "Supplementary exact diagnostics, not independent evidence",
        "status": author["status"],
        "source_sha256": author["source_sha256"],
        "independent_isolated_replay_byte_identical": True,
        "replay_is_new_independent_fixture_evidence": False,
    },
    "source_calls": 0,
    "episode_starts": 0,
    "random_draws": 0,
    "sampled_outcomes": 0,
    "hardware_executions": 0,
    "generic_modulus_QE_executed": False,
    "physical_candidate_fit_executed": False,
    "generic_recovery_optimizer_executed": False,
    "gate_synthesis_executed": False,
    "publication_or_upload_performed": False,
    "earlier_frozen_delivery_list_changed": False,
    "primary_sources_directly_inspected": [
        "https://arxiv.org/pdf/1811.07722",
        "https://journals.aps.org/prxquantum/pdf/10.1103/PRXQuantum.3.020344",
        "https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/improved-effective-lojasiewicz-inequality-and-applications/022BF859F5714FDA8050F6DC1992E48B",
        "https://cs.uwaterloo.ca/~watrous/Papers/SimplerSDPforCBnorm.pdf",
    ],
    "hashes": {name: sha(name) for name in FILES},
}
target = HERE / "IC_PORT_SHORT_DEPTH_COMPLETE_RECOVERY_INDEPENDENT_RECEIPT.json"
target.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({"receipt": target.name, "sha256": sha(target.name),
                  "source_sha256": EXPECTED, "status": out["status"]}, indent=2))
