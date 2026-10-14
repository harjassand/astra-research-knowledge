# Delta audit read ledger

Audit window: 2026-10-14 local session. All conclusions in `REPORT.md` concern the exact certificate snapshot recorded below. The root note changed once during the audit; both versions are retained in `input/`.

## Primary target and versions

| Read | Version / exact scope | SHA-256 | Notes |
|---|---|---|---|
| `work/FK-root/THERMAL_TRANSITION_CERTIFICATE.md` | 117 lines; current root snapshot copied at 2026-10-14 20:57 local; exact copy `input/THERMAL_TRANSITION_CERTIFICATE.md` | `bc0c8c73a7ed62161c27842d6bfdcdc26c8b70f3e13be60a536896d293402dcb` | Read in full. Compared against the initial snapshot; only §8 comparator wording/attribution changed. |
| Initial target snapshot | 117 lines; exact copy `input/THERMAL_TRANSITION_CERTIFICATE.87d8b580.md` | `87d8b580bf8ffc4520fa89476ed024bf05d08bc006f5382477c3146031a20e35` | Initially copied and read in full. The changed comparator paragraph is not part of the four mathematical claims audited here. |
| `work/FK_PIN.json` | Full file, source pin fields | `828d12ae103d0714e4372b8d2ceba3e0bb0c83aadf4f762fdcd911837c8408d8` | Reports capital checkout/cumulative PR head `4c47df1fda950e27e48295689dd642194bfac046`; this was checked with `git rev-parse`. |

## Capital instructions and route records

Capital checkout `work/astra-capital` was at Git HEAD `4c47df1fda950e27e48295689dd642194bfac046` (commit subject: “Integrate bounded nonlinear observation, contact compensation and hydraulic assay capital”; timestamp `2026-10-14T20:20:14+10:00`). The N786/N788 dossier metadata itself records snapshot base `b34e22e8f8ef8bd853595952fcbd9c74c5ace306`; this metadata was preserved rather than conflated with the checked-out HEAD.

| Read | Exact scope | SHA-256 | Use |
|---|---|---|---|
| `work/astra-capital/00_START_HERE.txt` | Full file | `4a91985ece91557af12ba5c216e7fe17cf5dd000596e9a0c73b0b6705498f360` | Task-first and claim-scope protocol. |
| `work/astra-capital/AGENTS.md` | Full file | `581cdda103fed0c87acdb0ee527bd5ba174f55b1baa0cbfe60b177d52027ee7d` | Capital evidence and status instructions. |
| `work/astra-capital/state/CONTINUITY.md` | Full file | `040c4ac42162802bd2fb4f9e8069e6ca034ccbee63cffc7b43f4c745dac0b297` | Current-checkpoint and claim-status boundaries. |
| `work/astra-capital/frontier/dossiers/N788.txt` | Lines 1–70 | `a55caf8e2b86c0a720ec0f13218a69b9a5351042b7920990c5a893c7380d1eeb` | Actual loaded Gibbs histogram is a required input; its acquisition is open; local stationarity does not certify hidden-sector weights. |
| `work/astra-capital/frontier/dossiers/N786.txt` | Lines 1–70 | `5f4affb5b9f3a286e8845722cb4c6474df29fccc8ced00aeec13f175e1aaf4c0` | Scoped finite-order vacuum-information obstruction and supplied-order reconstruction boundary. |
| `work/astra-capital/updates/FC/synthesis/design/REPORT.md` | Lines 1–80 | `6ccfa9989ea966e0dfc0535bd9111c28489b79cccd32ef5c36df9a808021b71b` | Capital synthesis: loaded equilibrium histogram changes the information interface, but acquisition/calibration remain necessary. |
| `work/astra-capital/updates/FC/synthesis/design/PREPARATION_OBSTRUCTION.md` | Full file, 121 lines | `133fbae533adfea9785ba9d76facec613c122e04b2c862ce71c8ee55445fe9f8` | Exact fixed-charge/local-stationarity hidden-sector countermodel and its limited A-only access claim. |

## Executable exact checks

Independent script: `checks/exact_delta_checks.py`. It does not import or call the root numerical checker. Command:

```text
work/FE-hidden-gate/venv/bin/python work/FK-anchor-audit/delta/checks/exact_delta_checks.py
```

Runtime: Python `3.14.3`, SymPy `1.14.0`. Exit status: `0` (`PASS`). The script writes `checks/exact_delta_results.json`. It checks exact rational sector weights, detailed balance and folded means; a degenerate-space energy-commuting Kraus counterexample to a weaker-than-stated QND condition; one exact finite clipping fixture; and the exact cosine-measure Matsubara identity. It is not a proof of the global operator or measure theorems.

## Not read / not asserted

The root numerical checker `work/FK-root/verify_thermal_transition.py` and its result JSON were not read or executed. The comparator papers cited in §8 were not opened in this delta; the added Sun/QPE attribution sentence in the current target snapshot is therefore recorded as source text, not independently verified. No exhaustive novelty, priority, physical implementation, or total-cost claim was attempted.
