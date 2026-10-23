# Astra B3 evidence capsule

**Decision:** retain the validated physical pISO correction; close this bounded trial without an accepted aggregate core-versus-cusp conclusion. The nominal reserved-data score favors the corrected core in aggregate, but NGC5585 fails the prespecified predictive-adequacy gate under both tested error kernels. See `REPORT.md` and `results/FINAL_DECISION.json`.

## Quick receipt and saved-evidence replay

Run from an extracted copy:

```bash
python verify_packet.py
```

This needs only the Python standard library. It verifies every recorded file hash, checks the pinned original sources, and recomputes the saved score/acceptance arithmetic from the retained fit outputs. Expected result: integrity passed, 42 fits, saved decision replayed, physical discrimination not accepted. It does not run a new fit or the publication's native sampler.

## Scientific reproduction

The executed environment was Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, Matplotlib 3.10.8 and dynesty 3.0.0. Exact dynesty source and its license are included under `vendor/`; other scientific dependencies are specified in `requirements.txt`.

```bash
python independent_model_checks.py
python run_fresh.py /absolute/path/to/a/new/output_directory
```

The destination must not exist. The script copies the required code and inputs and executes validation, development, outer-only fitting, fixed full-data scoring and diagnostics in order. It uses no download or paid service. Original run: 42 fits, 6,359,462 likelihood evaluations, approximately 9.43 minutes summed elapsed fitting stages with three worker processes on the recorded environment. Actual rerun time varies.

Do not change `--nlive` or `--dlogz` against the delivered `results/` and call it a fresh run: the executed `analysis.py` intentionally remains unchanged and has a label-only cache. The fresh-directory wrapper avoids that issue. Preserve original results for any accuracy comparison.

## Files to inspect

| Path | Purpose |
| --- | --- |
| `REPORT.md` | Complete scientific decision, methods, results, costs and limits |
| `PREREGISTRATION.txt` | Frozen local scientific contract |
| `PREOPEN_PROCEDURAL_RECORD.json` | Code identities and limited historical-summary exposure disclosures |
| `analysis.py` | Exact executed new NumPy/SciPy/dynesty implementation |
| `improvement/correct_piso.patch` | Minimal correction against the pinned public source |
| `improvement/fit_nfw_iso_corrected.py` | Clearly marked derivative source, not a claimed native sampler replay |
| `sparc_admission_source/` | Unchanged public measurements, source code and small article source |
| `results/fits/` | All 42 fit summaries and weighted posterior arrays |
| `results/predictive/` | Outer-trained reserved-vector predictions |
| `results/decision.json` | Raw frozen-rule result |
| `results/FINAL_DECISION.json` | Scoped final scientific decision |
| `results/numerical_audit.json` | Direct conditional-density cross-checks and simulation-error checks |
| `results/figures/` | Standalone PNG/PDF scientific plots |
| `provenance/` | Primary source lineage, units, rights and licenses |
| `diffusion_sources/` | Bounded second-case source/metadata evidence; no trajectory analysis |
| `implementation_audit.txt`, `final_decision_review.txt` | Internal independent reviews and limitations |
| `independent_model_checks.py`, `.json` | Executable synthetic likelihood/physics audit and original receipt |
| `MANIFEST_SHA256.json` | Integrity manifest for every delivered file except the manifest itself |

SPARC input rights are not relabelled. Retain the original citations and notices. The published fitting code and derivative correction carry GPLv3-or-later notices; the full license is in `provenance/COPYING_GPL-3.0.txt`. New analysis code is likewise marked GPLv3-or-later. The source article's attribution and the vendored dependency's separate license remain in their source notices.

The previous R3/anMC transfer stays closed. This capsule contains an independent data-led B3 calculation. It does not claim a new physical experiment, general dark-matter discovery, historical novelty or external adoption.
