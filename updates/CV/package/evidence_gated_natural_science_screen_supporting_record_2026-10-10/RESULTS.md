# Evidence-gated screen result

Date: 2026-10-10 UTC

## Decision

No mechanism passes the discovery gate. I am not claiming a foundational discovery and do not recommend Sol escalation. The most useful result is a quantitative conservation test showing that the proposed nodule-driven water-electrolysis explanation for “dark oxygen” is not established by its published evidence.

## Three initial, materially different candidates

1. **X-ray quasi-periodic eruptions:** compact-object disk impacts versus accretion-disk limit cycles. A periodic impact clock is testable, but an orbital-impact causal mechanism is already in the primary literature and timing alone is non-identifying.
2. **Abrupt cosmogenic-isotope excursions:** solar-particle events versus photon transients, galactic-particle changes, and archive/transport effects. The consulted primary study already attributes its event to solar particles with a carbon-cycle model; this screen found no new source mechanism.
3. **Inner-core waveform changes:** rigid differential rotation versus local boundary change and subsurface scatterers. The recent primary paper proposes local deformation or melting/freezing but treats those as alternatives; its data coverage does not exclude changing interior scatterers. The raw waveform archive could not be downloaded, so the frozen independent-station test was not run.

The original preanalysis gives the observables, alternatives, quantitative predictions, nuisance assumptions, and falsification gates for these candidates. The screen then pivoted to a fourth candidate with a direct conservation test.

## Dark-oxygen pivot

The primary paper reports oxygen increasing in some abyssal chamber experiments and ex-situ incubations, then hypothesizes that polymetallic nodules electrolyze seawater. It reports nodule-probe potentials up to 0.95 V, states an oxygen-evolution requirement of 1.23 V plus about 0.37 V overpotential for site conditions, and acknowledges that the energy source and operational mechanism remain unresolved. It reports no integrated current/charge or H2 production.

For the paper's reported 1.7–18 mmol O2 m-2 d-1 rates, Faraday's law requires 7.6–80.4 mA m-2 if the oxygen is made by water splitting, with a minimum reversible power of 9.3–98.9 mW m-2 (12.2–128.6 mW m-2 using the paper's stated 1.60 V operating value). The matching chamber current is 0.37–3.89 mA. The article's maximum 0.95 V potential, if it represented the complete loaded electrolysis cell, would be below the 1.23 V reversible minimum. But the published measurements are open-circuit probe differences on recovered nodules, not loaded voltage/current in the oxygen-producing experiment. The core prediction therefore lacks the measurements needed to identify or close the mechanism.

The oxygen observation itself remains unsettled. A 2025 peer-reviewed critique disputes chamber ventilation, voltage interpretation, and replication; the critique discloses commercial interests that also warrant caution. Crossref records an April 2026 Editor's Note saying aspects of the original paper are under editorial consideration. I treat these as an active dispute, not as a verified reanalysis of raw data. The original article's source-data attachments and Dryad archive are publicly linked, but the attachments triggered a PMC anti-bot page and the execution network returned HTTP 403 for Dryad. I did not acquire the scientific data or compute a raw-data hash.

## What would discriminate the mechanism

A future independent record would need, in the same pressure-controlled and properly ventilated sealed chamber, calibrated oxygen measurements plus H2, potential under load, integrated current, and the nodule redox-state inventory. Blinded nodule-free and inert-rock controls should start at verified ambient bottom-water oxygen; a water-oxygen isotope tracer could identify the oxygen source. The electrolysis mechanism would have to close the `4 e- per O2` charge budget, the `2 H2 per O2` product ratio, and the energy budget within measurement uncertainty. A positive oxygen signal alone would not pass.

No physical experiment was run or requested. This is a prospective specification only.

## Artifacts and provenance

- [PREANALYSIS.md](PREANALYSIS.md): original three-candidate protocol, frozen SHA-256 in `FREEZE.sha256`.
- [DARK_OXYGEN_PREANALYSIS.md](DARK_OXYGEN_PREANALYSIS.md): pivot test frozen before opening the primary paper, hash recorded in `FREEZE.sha256`.
- [DERIVATIONS.md](DERIVATIONS.md): physical derivations and limits.
- [dark_oxygen_budget.py](dark_oxygen_budget.py) and [dark_oxygen_budget.json](dark_oxygen_budget.json): reproducible modest calculation from reported paper values, not raw-data analysis.
- [SOURCES.md](SOURCES.md): repository revision, source pins, access notes, and raw-data status.

The Astra repository was not edited. No protected or excluded topic was reopened. No raw scientific file, physical experiment, researcher contact, new account, paid compute job, publication, push, merge, or task automation was created.
