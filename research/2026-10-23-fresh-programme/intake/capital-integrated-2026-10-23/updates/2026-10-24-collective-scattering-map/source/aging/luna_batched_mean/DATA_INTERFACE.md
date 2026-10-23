# Frey et al. Figshare deposit: what can be reanalysed

## Acquisition result

The article links the public Figshare record [10.6084/m9.figshare.28855373](https://doi.org/10.6084/m9.figshare.28855373), version 1. Its public API record reports CC BY 4.0, no embargo, and 77 files totaling **17,356,264 bytes** (17.36 MB decimal). A preserved API response and complete file metadata are in [`FIGSHARE_METADATA.json`](FIGSHARE_METADATA.json).

**There are no detector speckle-frame images in the deposit.** The six `.png` files are rendered TTCF heatmaps; they are not raw intensity images. They display frame-versus-frame correlation and a normalized color scale, but are raster figure exports, not stored numerical TTCF matrices. I inspected `Ab480_Pt42p5_2_heating2_Scan_1_trc.png` (2,796,506 bytes; 1920×1440 RGBA): its plotted values are about 1.000–1.030 and both axes are frame number. A heatmap can support qualitative inspection or rough image digitization, but not a faithful numerical matrix reconstruction.

The article’s Methods state that this experiment used one fixed scattering-vector band, **|q| = 2.86 ± 0.05 Å⁻¹**, 0.01 s frame exposures, 24,000-frame correlation batches (240 s; 4 K), and half-batch overlap (12,000 frames; 120 s; 2 K). Thus these TTCFs are at one q band, not a set of numeric q-resolved matrices. The paper defines the TTCF as a pixel-averaged normalized intensity correlation. These data do not retain detector-pixel intensities or spatial speckle shifts.

## Deposited files and units

| Public file class | Count and size | What the files contain | Units / labels |
|---|---:|---|---|
| `*_event_cf.dat` | 65 × 16,801 B = 1,092,065 B | Each file has 96 rows and 7 whitespace-separated numeric columns, without a header. A representative file is in `data_sample/`. The repeated records are heating/cooling scan batches. | The README says “q data” are in column 1 and identifies columns 4–5 as g₂/error. However, the sampled column 1 runs from 0.01 to 158.725, matches the `t` grid in the figure-source workbook, and is consistent with the paper’s 0.01 s exposure and lag-time curves. I therefore treat it as **likely lag time τ in seconds**, while preserving the contradictory README label as unresolved. Columns 2–3 and 6–7 are additional numeric value/error-looking pairs that the deposit does not label. |
| TTCF `.png` | 6; total 14,271,102 B; individual sizes: 2,796,506; 2,127,247; 2,131,514; 2,445,541; 2,640,310; 2,129,984 B | Three heating and three cooling TTCF heatmap figure files. The article says each displayed TTCF uses 24,000 frames. | Frame/frame axes; 0.01 s per frame from Methods. Colorbar is normalized correlation, approximately 1.000–1.030 in the inspected image. The PNGs do not provide numeric matrix cells or q-resolved pixel data. |
| `Fig1 and 2 and 5 source data.xlsx` | 203,492 B | Three sheets: DSC traces, selected g₂ curves for Fig. 1, and selected figure source data. | Sheet labels include T (K), heat flow (arbitrary units), and `t` with g₂/error data. For the B1 heating curve (frames 480000–504000), the workbook’s 96-point g₂ series agrees with column 4 of its matching `.dat` file to a maximum absolute difference of 4.8×10⁻⁶; this supports the interpretation of columns 4–5 as the plotted g₂/error pair. |
| `Fig3 and 4 source data.xlsx` | 208,829 B | DSC traces, heating/cooling KWW and KWWmulti fit tables, and fragility comparison data. | T in K; τ, τ_C and τ_L in s; β values dimensionless; Fig. 4 also labels 1/T in K⁻¹ and viscosity in Pa·s. |
| DSC `.txt` scans | 2 × 790,000-ish B (790,205 B cooling; 790,147 B heating) | Ex-situ DSC cooling/heating scans. | The workbook’s matching source columns label T (K) and heat flow (arbitrary units). |
| `READ ME.txt` | 2 × 212 B | Duplicate short schema note. | The README’s “q” label for `.dat` column 1 conflicts with the numeric range, figure-sheet `t` labels, and experimental timing; the conflict is recorded rather than silently normalized. |

The workbooks and a representative TTCF PNG were downloaded for inspection; the full deposit was not bulk-downloaded. Small inspected files are in [`data_sample/`](data_sample/). The sample `.dat` files are the cooling 0–24,000-frame batch and heating B1 480,000–504,000-frame batch.

## Reanalysis boundary

The deposit supports analysis of the published one-dimensional g₂ lag curves over temperature and cooling/heating scan batches, plus qualitative inspection of six selected TTCF maps. It does **not** support a real affine-speckle-drift versus density-decorrelation reanalysis: there are no raw `I(pixel, frame)` images, no numeric two-time correlation arrays, and no q-resolved shift/cross-correlation data. Fitting the 1D g₂ curves again or digitizing a heatmap would not recover the missing spatial information and should not be reported as that reanalysis.

The separate 2026 Vit4/HC5966 route is not part of this deposit. Per the task scope, its reported raw ESRF archive/processed-on-request status was not pursued; no author was contacted and no archive was requested or authenticated.

## Source and sample record

- Article: [Nature Communications, DOI 10.1038/s41467-025-59767-2](https://doi.org/10.1038/s41467-025-59767-2). Its Data Availability statement points to the Figshare deposit. The full-text Methods and Fig. 1 caption state the fixed q, exposure, batch timing, and that each displayed TTCF covers 24,000 frames.
- Dataset: [Figshare record, DOI 10.6084/m9.figshare.28855373](https://doi.org/10.6084/m9.figshare.28855373); public metadata endpoint: [Figshare public API](https://api.figshare.com/v2/articles/28855373).
- The downloaded data and source sheets are research data, not an independently calibrated or validated new measurement. No affine-drift result is claimed.
