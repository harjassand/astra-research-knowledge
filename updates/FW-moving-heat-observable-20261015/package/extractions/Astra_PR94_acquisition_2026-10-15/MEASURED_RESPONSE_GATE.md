# Measured scalar-control acquisition gate

Date: 2026-10-15. Disposition: NOT PASSED. No raw configuration–response dataset was acquired, and no hardware benchmark was run. This is a bounded public-data search, not proof that no dataset exists.

## Source contract

Read N854 proof from the locally acquired source copy and COSTS_AND_COMPARATORS.txt at repository harjassand/astra-research-knowledge, commit 6fde70a4668f877bc9988bc8f20c570ef4513d08 (connector-reported blob 4604172a2f53579eb7945cb7b83e4c87e371a3d3). Its real, fixed-source/fixed-detector, calibrated additive-rank-one, ternary schedule cannot simply be applied to intensity-only or binary measurements.

## Sol et al. 2024

Primary source: https://pmc.ncbi.nlm.nih.gov/articles/PMC10987616/ (Nature Communications DOI 10.1038/s41467-024-46916-2).

The reciprocal cavity has 68 independently controlled binary meta-atoms, four antennas, and complex VNA scattering measurements; a fixed S31 channel is explicitly studied. Phase-retrieval experiments instead use intensity information. Local polarizabilities are fitted parameters. Operating frequency is around 5.2 GHz; measurement settings are 15 dBm and 1 kHz IF bandwidth. Unseen random configurations are used for validation. The availability statement points to the article/supplement; code is available by author request. The linked supplementary assets are a 24.3 MB information PDF and a peer-review PDF, not a raw measurement archive. No public raw control-bit/complex-response table was located.

Mismatch: binary hardware cannot supply N854's two distinct nonzero singleton levels. Fitted polarizabilities do not independently establish known additive control increments. Reciprocal data does not test generic nonreciprocal branch recovery. Intensity data does not supply signed amplitude or quadratures. Repeat/noise/settling records sufficient for the proposed certificate were not found.

## Virtual VNA 3.0

Primary source: https://arxiv.org/html/2503.07239v1 . Published version: https://doi.org/10.1109/TIM.2025.3598388 .

This work actually measures loaded responses of a nonreciprocal eight-port network, with four accessible ports and four controlled terminations. It uses three calibrated complex load reflections and coupled loads. The closed-form experiment uses 19 configurations; gradient descent uses 1000 random individual-load configurations and 400 coupled-load configurations. VNA settings: 401 frequencies, 450–700 MHz, 500 Hz IF bandwidth, 12 dBm. Calibration planes are at DUT ports. Load spectra are plotted. Thermal drift is identified as a possible error source; systematic noise-dependence exploration is left to future work. No raw-data link was found in arXiv v1 or the author's publication listing. The final IEEE landing page returned a robot-verification screen, so its supplementary assets were not inspected.

This is the closest potential fixed-entry dataset. However, plots of recovered/full ground-truth S are not the measured configuration-labelled loaded matrices. Their reconstruction errors do not establish held-out scalar-control accuracy or repeat noise bounds.

## Own mathematical/interface analysis

For diagonal load reflections r_i, selecting one fixed measured entry gives
f(r)=S_ab + S_aH (diag(1/r)-S_HH)^(-1) S_Hb.
With nonzero reference r_i0, set u_i=1/r_i-1/r_i0 and A=diag(1/r_i0)-S_HH. The variable part is exactly a complex diagonal-additive resolvent. The direct term can be retained as a fixed offset. Thus genuinely measured loaded entries can support an empirical complex-response test; synthesizing them from one measured full S cannot.

Gates before applying N854 unchanged:
- Complex coefficients/controls and per-actuator unequal complex level ratios require an explicit extension of the real positive-level theorem and its noise certificate. Taking Re(f) alone does not preserve the claimed real rank-one control form automatically.
- Select a fixed source/detector among accessible ports unaffected by the special accessible-to-hidden coupled-load operation. Prefer the diagonal-only settings. Coupled loads are outside the diagonal-control family and cannot be counted as valid heldouts for that theorem.
- For m=4, N854 needs 24 specific settings. The VNA closed-form schedule has only 15 diagonal settings plus four coupled ones, so it does not directly contain the complete N854 schedule. The 1000 random ternary draws range over only 81 unique control vectors; deduplication and configuration coverage are indispensable. Repeated control vectors could support an empirical repeat estimate only if the actual sequence and observations are supplied.
- Measured load spectra must be numerical, frequency-aligned, and calibrated at matching planes. Reflection values inferred from plots are insufficient for a tight certificate.

## Exact missing acquisition package

1. Frequency, immutable load-state vector, measurement order/time, and actual complex loaded scalar (or measured loaded matrix from which a single entry is selected) for each acquisition.
2. Numerical per-port load-reflection calibration, uncertainties/reference planes, and switch-state mapping.
3. Baseline/singleton/pair/triple coverage or permission to use a different matched fitting protocol; independently reserved joint-load configurations.
4. Repeat observations, averaging/integration settings, settling/reset timing, drift checks, and stable source/detector details.
5. For the original real theorem, real signed steady-state data and known additive ternary conductance increments, or a separately justified complex extension.

No author outreach, downloaded-code execution, purchases, or canonical edits were performed. No model-generated load responses were relabelled as measurements.

## Supplement acquisition receipt

The publisher-hosted Sol supplement was successfully downloaded and text-inspected: 25,462,008 bytes, 18 pages, SHA-256 bda418404c50822d819f17efd9a25cf1c85e8f1f98d133e8b2a4ac20d4cc4a1b. URL: https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-46916-2/MediaObjects/41467_2024_46916_MOESM1_ESM.pdf . It contains four supplementary figures, explanatory notes, and references; pdfdetach reports zero embedded files. No raw configuration–response array or numerical calibration table was found. Supplementary Note 4, p.16, expressly confirms that the two available polarizabilities are estimated from calibration data. Broader multi-bit applicability is a proposed method scope, not an extra measured level in this experiment. The PMC PDF URL returned a short HTML response instead, which was not treated as a PDF or dataset.
