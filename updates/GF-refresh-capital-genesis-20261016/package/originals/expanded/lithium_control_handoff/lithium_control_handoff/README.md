# Lithium extraction: a reproducible control benchmark

## What this delivers
An evidence-based benchmark for comparing electrochemical control schedules, with an audit of charge dose and lithium inventory. It does **not** establish a new separation technology or a superior new schedule.

### Findings that survive the audit
- The exact Figure4c constant-current and 4-second-on/8-second-rest traces reproduce the released workbook. Their recorded negative charge increments sum to **2.87215 and1.38684mAh**, respectively. The pulse/CC ratio is**0.48286**. Net negative charge, after positive increments, gives a separate ratio**0.48888**. Preparation and duration also differ. This comparison does not isolate rest timing at matched dose and state.
- Figure5A's ten-cycle processing formulas sum to **12.77004 forCC and10.25738 forpulse**, ratio**0.803238**, in formula-implied mg/g units. Absolute dilution and liquid inventory remain unresolved. Improved retention relative to each mode's own first cycle is compatible with lower cumulative recovery over these ten cycles. This is not a lifetime endpoint or equal-time throughput comparison.
- The two comparisons are different experiments. Do not divide Figure5A lithium totals by Figure4c charge. Do not count instrumental readings as independent electrode experiments.

These qualifications do not refute the paper's measured selectivity or retention results. They define what those comparisons can establish.

## Closest measured response and incumbent
The Oct12,2026 ACS paper already optimizes pulse/rest operation and discusses loss of benefit during excessive rest:
https://doi.org/10.1021/acssuschemeng.6c04447

The2024 Nature Communications paper measures non-faradaic Li-to-Na exchange as a function of particle size and initial lithiation:
https://www.nature.com/articles/s41467-024-49191-3
Its time series begins at0.25hours. It cannot supply a measured exchange law for1–12second rests. Pulse/rest and reverse-pulse strategies also appear in2020 prior art:
https://doi.org/10.1016/j.joule.2020.05.017

## Missing operation and decisive test
The useful proposed operation is species-aware selection of rest, cutoff, and release timing that improves recovered lithium over electrode life. Its success is unverified. It needs both a calibrated matched-state response and an electrode durable in the actual competing-ion feed.

The decisive response matrix should have:
- Rows: CC and the published4s-on/rest schedules, followed by any proposed state-aware schedule.
- Controlled blocks: same electrode formulation/batch, initial Li and Na occupancy, feed composition, temperature, flow, and electrode age. Separate matched-total-charge tests from matched-clock-time tests; they answer different questions.
- Measured columns: realized current and cell voltage; Li/Na inventory before and after individual rests and recovery; receiver baseline/dilution/volume; feed, rinse and sampling losses; terminal electrode inventory; phosphate/iron dissolution; cumulative recovered Li and usable capacity versus cycle.

A new schedule passes only if its species-resolved inventory closes and its cumulative recovered lithium per initial full-electrode mass improves against the published pulse incumbent at the relevant dose/time and durability constraints. Propagate measured uncertainties; do not substitute a fitted short-time exchange rate from hour-scale data. Present data allow the dose and accounting audit below, but do not populate that causal response matrix.

## Contents and reproduction
Nine unmodified source members are included: five workbooks and the exact twoMPR/twoMPS files. SOURCE_SUBSET_MANIFEST.json records their original relative paths, byte counts and SHA256 hashes. This is a small subset of the1.51GB source ZIP, not the complete dataset.

Newly authored Python scripts require Python3, NumPy and openpyxl. No acquired executable code is included or executed. From this directory run:

    python recover_mpr_pair.py
    python verify_pair.py
    python quantify_pair.py
    python reconcile_icp.py

Scripts locate inputs relative to themselves. The narrow MPR reader supports only the verified observed layout and asserts its structure. Do not generalize it to arbitrary files. replay_*.txt records a fresh successful run; decoded CSVs and JSON metrics are derived outputs. The charge report explains transition intervals, sparse sampling, conditional voltage interpretation and the distinction between negative-increment sums and net charge. The ICP report explains unresolved absolute calibration and raw-to-processing discrepancies.

Original reports have been retained with a clarification that ICP absolute mg/g values are formula-implied. No source workbook has been edited.

## Attribution and license
Original data: Bin Wang, Burcu Tan, Antje Quade and Volker Presser, “dataset for Selective electrochemical lithium-ion extraction from low-grade lithium sources with optimized pulsed operation,”2026, DOI10.5281/zenodo.23064370.
https://zenodo.org/records/23064370

The source record declares Creative Commons Attribution4.0 International:
https://creativecommons.org/licenses/by/4.0/
Original source members are unmodified; this packet adds selection, analysis, derived tables and documentation. ORIGINAL_ZENODO_METADATA.json preserves the retrieved attribution/license metadata and full-source ZIP checksum. The full ZIP was not downloaded or independently checksum-validated; included-member SHA256 hashes were validated after copying. New analysis was prepared for Astra and this private handoff. No public license is granted for that new analysis. No author endorsement is implied.
