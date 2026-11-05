"""Assemble this exchange and preserve the prior complete archive byte for byte."""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys, zipfile

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "deliverables"
TARGET = OUT / "thermal_register_research_package"
TARGET.mkdir(exist_ok=True)

files = [
    "reusable_register_opening.md", "calibration_operation.md",
    "calibration_audit.md", "verify_register.py", "register_verification.json",
    "build_report.py", "report_text.txt", "verify_all.py", "build_package.py",
    "sampler_route/sampler_obstruction.md",
    "sampler_route/bdl_matrices.py",
    "sampler_route/two_square_minor.py",
    "sampler_route/two_square_fano.json",
    "sampler_route/fano_dual_exact.json",
    "sampler_route/verify_two_square_fano.py",
    "sampler_route/verify_lawrence_minor.py",
    "sampler_route/reusable_register_audit.md",
    "sampler_route/verify_cover_and_adaptive_clock.py",
    "decoding_route/central_quotient_and_recent_decoding.md",
    "decoding_route/qd_hdqi_obstruction_audit.md",
    "decoding_route/matroid_bridge_audit.md",
    "decoding_route/audit_matroid_subdivision.py",
    "decoding_route/matroid_subdivision_audit.json",
    "decoding_route/verify_central_quotient.py",
    "decoding_route/central_quotient_verification.json",
    "intervention_route/FINITE_RESET_AND_MARK.md",
    "intervention_route/finite_reset.py",
    "intervention_route/finite_reset_results.json",
    "sources/p1_original_return.txt",
    "sources/p1_selection_brief.tex",
    "sources/p1_csw_bdl_comparison.md",
    "sources/p2_original_return.txt",
    "sources/p2_readme.md",
    "sources/p2_hard_families.md",
    "figures/finite_window_pulses.png",
    "figures/finite_window_pulses.svg",
]
for relative in files:
    dest = TARGET / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / relative, dest)
for name in ["FINITE_POINTER_REALIZATION.md", "LOCAL_THERMAL_INTERVENTION_THEOREM.md"]:
    shutil.copy2(ROOT / "intervention_route" / name, TARGET / "sources" / name)
shutil.copy2(OUT / "Astra_Thermal_Register_Exchange.pdf", TARGET)

prior = OUT / "Astra_Burst_Recoverability_Research_Package.zip"
digest = hashlib.sha256(prior.read_bytes()).hexdigest()
expected = "e8f3e86af3829f6ab9e948e77b51e759aaa4ad14c2ca500549fb2f95150e4eee"
assert digest == expected, "Preserved archive byte identity differs from prior receipt."
(TARGET / "preserved").mkdir(exist_ok=True)
shutil.copy2(prior, TARGET / "preserved" / prior.name)
(TARGET / "PRESERVATION_RECEIPT.json").write_text(json.dumps({
    "file": "preserved/" + prior.name,
    "bytes": prior.stat().st_size,
    "sha256": digest,
    "scope": "Preserved byte for byte; contains the productive-control, direct-prevention and first-event predecessor archives. Nested manifests were not re-audited."
}, indent=2)+"\n")

repo = "https://github.com/harjassand/astra-research-knowledge/blob/"
pin = "e9bd2054d8e396d82dc89d59b9851f1827fc55ef"
paths = {
    "p1_original_return.txt": "2026-11-05-p1-thermal-memory-opening/P1_OPPORTUNITY_OPENING_20261105_RETURN.txt",
    "p1_selection_brief.tex": "2026-11-05-p1-thermal-memory-opening/package/selection_brief.tex",
    "p1_csw_bdl_comparison.md": "2026-11-05-p1-thermal-memory-opening/package/csw_bdl_comparison.md",
    "p2_original_return.txt": "2026-11-05-p2-intervention-stream-opening/P2_OPPORTUNITY_OPENING_20261105_RETURN.txt",
    "p2_readme.md": "2026-11-05-p2-intervention-stream-opening/README.md",
    "p2_hard_families.md": "2026-11-05-p2-intervention-stream-opening/hard-families-and-comparators.md",
}
sources = {name: repo+pin+"/research/returns/"+path for name,path in paths.items()}
for name in ["FINITE_POINTER_REALIZATION.md", "LOCAL_THERMAL_INTERVENTION_THEOREM.md"]:
    sources[name] = repo+"3629d4ca14f495fb6999d2cd9bdd89a2be8c34ba/research/returns/2026-11-05-p2-local-thermal-trials/package/thermal/"+name
sources["primary_research"] = [
    "https://arxiv.org/html/2605.10943v1",
    "https://arxiv.org/html/2510.08446v4",
    "https://arxiv.org/abs/1010.6231",
    "https://arxiv.org/pdf/2610.03566",
    "https://arxiv.org/pdf/2610.06667v2",
    "https://arxiv.org/abs/0804.1571",
    "https://arxiv.org/html/2510.08533v2",
    "https://arxiv.org/abs/1809.03191",
]
(TARGET / "SOURCES.json").write_text(json.dumps(sources, indent=2)+"\n")
(TARGET / "README.txt").write_text("""ASTRA: A REUSABLE THERMAL QUANTUM REGISTER
Constructive exchange completed 5 November 2026.

Start with Astra_Thermal_Register_Exchange.pdf (21 pages).

The selected result is a source-conditional reusable quantum register for an
entire classically scheduled adaptive campaign, with a once-paid thermal
initialization budget. The actual-coordinate extensive matroid obstruction
settles the published regular/near-graphic sampler comparison. A separate
complete-relation-code obstruction addresses QD-HDQI. The accepted history
compiler remains an efficient loader. New compatible operations include
canonical TFD preparation, central-sector transduction and a finite harmonic
reset-and-mark companion.

Completed proofs:
  sampler_route/sampler_obstruction.md
  reusable_register_opening.md
  calibration_operation.md
  decoding_route/central_quotient_and_recent_decoding.md
  decoding_route/qd_hdqi_obstruction_audit.md
  intervention_route/FINITE_RESET_AND_MARK.md
Independent audits are adjacent to these notes.

Reproduce:
  python verify_all.py
Requires Python 3 and NumPy, SciPy, mpmath. Exact binary/rational checks do not
require the CMR discovery software. The executed receipt records environment
versions, script hashes, outputs and the finite numerical residual.

Rebuild the report in this directory:
  python build_report.py .
Also requires ReportLab, matplotlib, Pillow and DejaVu fonts in the path used
by the builder. The mathematical report's equations are rasterized at 240 dpi.

Scope:
  No claim that CSW is torpid or that all Gibbs samplers fail.
  No constant-rate faulty-control threshold or general noncommuting
  fabrication robustness. The long-time Pauli-Davies model is supplied.
  TFD preparation is distinct from the classical-syndrome holding theorem.
  The harmonic companion is a calibrated finite loaded endpoint operation,
  with range, actuator, reset, uncertainty and classical-validity costs.
  The positive burst-recovery recurrence remains unproved.

Sources:
  Exact governing Astra returns and companion files are in sources/.
  SOURCES.json records commit pins and primary research URLs.
  Third-party full-paper retrieval dumps are not redistributed.

Preservation:
  The complete previous burst research ZIP is included unchanged, already
  nesting all productive-control, direct-prevention and first-event material.
  The preservation receipt verifies byte identity only; predecessor
  manifests were not re-audited.

The SHA256 manifest covers every delivered file except itself. Build scripts
and the verification receipt are included; private delivery helpers, caches
and unrelated working diagnostics are excluded.
""")
subprocess.run([sys.executable, str(TARGET / "verify_all.py")], check=True, cwd=TARGET)
for cache in TARGET.rglob("__pycache__"):
    shutil.rmtree(cache)
manifest = {}
for p in sorted(TARGET.rglob("*")):
    if p.is_file() and p.name != "SHA256_MANIFEST.json":
        manifest[str(p.relative_to(TARGET))] = {
            "bytes": p.stat().st_size,
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        }
(TARGET / "SHA256_MANIFEST.json").write_text(json.dumps(manifest, indent=2)+"\n")
archive = OUT / "Astra_Thermal_Register_Research_Package.zip"
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for p in sorted(TARGET.rglob("*")):
        if p.is_file():
            z.write(p, str(p.relative_to(TARGET)))
print(json.dumps({
    "archive": str(archive), "bytes": archive.stat().st_size,
    "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
    "files": len(manifest)+1,
    "preserved_sha256": digest
}, indent=2))
