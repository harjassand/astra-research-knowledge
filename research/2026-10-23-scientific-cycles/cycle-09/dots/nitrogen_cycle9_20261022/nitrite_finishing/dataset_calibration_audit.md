# New primary-data access: calibration and inventory audit

2026-10-22. Source: https://doi.org/10.5281/zenodo.17965118 . Parent retrieved metadata and ten CSVs through the actual Zenodo API; this audit reads those shared files, without another download or a refit. Supersedes the earlier statement that the dataset was unavailable. SI PDF remains uninspected.

## Record provenance
Metadata publication_date = 2025-12-17; created 2025-12-17T15:44:50.649136+00:00; modified 2025-12-23T18:35:00.086450+00:00. Record 17965118, concept 17965117, revision 6, version index 0 and is_last true in the retrieved metadata. License CC BY 4.0. Dataset predates the article's 19 May 2026 publication; this does not itself establish the dataset is obsolete, but differences must remain visible.

## Content-to-article mapping
Mappings are inferred from explicit CSV content plus matching published descriptions, not from a supplied readme.
- Figure_1.csv: radius/time series; likely published SI Figure S1 (3.5 micrometre stability), not current main Figure 1. Its time-column units are not labeled; radius unit explicitly nm.
- Figure_2A.csv and Figure_2B.csv: Raman shift/intensity pairs, likely published Figure 1a/b, early/late. Both span 326.224–1568.713 cm^-1. Strong perchlorate peak near 933.246; early data have nitrite around 814 and broad 1311 region, little nitrate; late data show nitrate near 1046.984 and reduced nitrite features. No per-spectrum time labels in CSV, so early/late assignment is consistent rather than independently timestamped.
- Figure_2C.csv: bulk IC, labeled 1MNaNO2_15min, 1MNaNO2_100min, 1mM NaNO3; published Figure 1c. IMPORTANT: 15 min label differs from article's 10 min.
- Figure_2D.csv: 5um and 3.5um nitrate time traces; published Figure 1d.
- Figure_3.csv: five calibration pairs, published SI Figure S2, NOT current main Figure 3. Header explicitly C_NaNO3 (bulk), ratio NO3/ClO4.
- Figure_4.csv: time/air, time/25mM KSCN_air, time/N2; published main Figure 2. This supplies the previously missing scavenger concentration: 25 mM KSCN in 2026, not the unidentified scavenger in 2025.
- Figure_5.csv: pH5/pH9; published main Figure 3.
- Figure_6A.csv: time/1M, 0.875M, 0.75M, 0.65M, 0.5M; published main Figure 4 left. IMPORTANT: 0.65 M label differs from 625 mM in Table 1 and Figure_6B.csv.
- Figure_6B.csv: NO2- [mM], A; published main Figure 4 right. Nonblank rows (1000,843),(875,730),(750,268),(625,177),(500,145); extra rows 815 and 850 have no A and are not observations of zero yield.

## Actual calibration data (no refit performed)
C_NaNO3_bulk_mM, nitrate/perchlorate signal ratio
202.117647058824,0.123936082081996
400.235294117647,0.326846828515086
605.411764705883,0.481468979711849
799.294117647059,0.584405104431595
1010.82352941176,0.803410528489918

Published methods specify nitrate band integral at 1050 cm^-1 divided by perchlorate integral at 932 cm^-1; calibrants contain nominal 1 M perchlorate. CSV label supplies the ratio but does not separately state integration windows, baseline code, per-droplet uncertainties, or sample raw ratios at every kinetic time. It should not be described as an independently measured absolute concentration/volume calibration.

## Load-bearing implication
Let R = I_NO3/I_ClO4 = b + s*(n_NO3/n_ClO4). Calibration fixes n_NO3/n_ClO4 using feed nitrate concentration divided by the common 1000 mM perchlorate reference. Applying its inverse therefore produces C_eq = 1000 mM*(n_NO3/n_ClO4), a reference-equivalent molarity. It is not automatically the actual in-droplet molarity C_actual = n_NO3/V_current.

With conserved co-aerosolized perchlorate and initial feed ratio n_NO2,0/n_ClO4,0 = C_NO2,feed/1000 mM, y = C_eq/C_NO2,feed = n_NO3/n_NO2,0. Any common evaporation or water uptake cancels exactly. No radius measurement is required for this cancellation. Pre-trap nitrite/HONO loss without perchlorate loss cannot manufacture a larger amount of nitrate per original feed N; it reduces the available N. Consequently an authentic tracer-normalized y > 1/3 is positive evidence against pure disproportionation as the sole source of nitrate, even without measured outlet-N closure.

The existing dataset now makes this interpretation substantially stronger than a purely hypothetical internal-standard suggestion. Still, absent processing scripts or a full raw time-resolved spectral series, it does not independently establish that every plotted kinetic concentration was calculated by that exact inverse calibration with no subsequent volume rescaling. The published methods are consistent with doing so.

## Independent challenge conditions, not reasons to assume failure
1. Selective aerosolization/segregation changing initial N/perchlorate ratio would break the feed-ratio denominator. Common water evaporation would not.
2. Perchlorate consumption/loss would inflate nitrate/perchlorate ratio. Article's stability/nonreaction statement supports conservation, but these CSVs do not separately quantify a chlorine balance. A changing raw perchlorate peak alone is insufficient evidence of consumption, because optical coupling/intensity changes.
3. Matrix, refractive-index, concentration or morphology dependence of relative Raman response could make calibrant and reacting-drop response factors unequal. Calibration salt matrix versus nitrite-rich sample mismatch needs consideration, not automatic rejection.
4. Baseline/intercept, integration windows and stimulated Raman contamination affect ratio inference; an unquantified systematic calibration error is not a measured low yield.
5. Pre-existing nitrate contamination/background must be subtracted or bounded. Initial droplet spectrum has little nitrate and bulk IC provides qualitative evidence; no explicit limit of detection/blank-nitrate molar budget is supplied here.
6. New gas-phase nitrogen influx would violate closed starting-N inventory; the stated experiment supplies bottled air/N2, not HONO dosing, which makes such an alternative less direct than in the 2025 HONO uptake operation.
7. Dataset/article discrepancies (15 vs 10 min; 650 vs 625 mM; 361/500 vs 56%) must not be silently corrected. Parent is auditing curve fits separately.

Even after rejecting pure disproportionation, no-zero-NO conclusion follows: oxidation and disproportionation may coexist, and NO can be made then reoxidized. No mM qualification or full plant balance follows from concentrated-droplet chemistry.

## Radius caveat
Figure_1.csv contains substantial excursions (examples 2605 nm and 4765 nm), interspersed with long stretches near 3475 nm. This audit has not decided which are physical versus WGM-fitting artifacts, nor applied filtering. Do not use the entire series uncritically as a precise volume-conservation certificate. This issue does not negate common-volume cancellation in a valid internal-standard ratio.
