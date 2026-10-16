# Measured Zeno response evidence bundle

Read `REPORT.md` first. Two primary experiments are kept separate:

1. Slichter et al. (2016): continuous single-transmon energy readout suppresses driven transitions; raw measurement data were not acquired.
2. Kalb et al. (2016): discrete, nonselective joint-spin projections suppress quasi-static dephasing. This is the closest interface to the unread-channel refinement; missing physical outcome records are no longer a theorem obstruction. Exact full-joint pinching and fresh/no-return reservoir composition remain unqualified. No public raw dataset was acquired.

## Contents

- `sources/`: licensed published papers, Kalb supplement, publisher/PMC article HTML, and PDF-to-text extractions.
- `figures/`: rendered pages used to verify units, figures, and cost caveats.
- `derived/slichter2016_fig4_experimental_digitized.csv`: 114 **published experimental symbols** reconstructed from the PDF. This is a digitized summary dataset, **not raw observations or author source data**. It cannot support independent dwell-time fitting or joint-event inference. The drive differs slightly across measurement-strength sweeps.
- `derived/digitization_calibration.json`: source checksum and tick coordinates.
- `extract_slichter_figure4.py`: our read-only PDF-vector extraction, requiring the already available PyMuPDF. It executes no author code.
- `PROVENANCE.json`, `SHA256SUMS`: source identity, access/license boundaries, and integrity.

Digitization is approximate. Conservatively treat coordinates at roughly 0.02 MHz / 0.02 μs⁻¹ resolution; do not interpret extra CSV digits as experimental accuracy. Very small rates are poorly resolved on the linear axis. Plotted intervals were reconstructed, not recomputed, and no claim of raw-data reproducibility is made.

The article licenses and original attribution remain attached to the source works. The evidence does not certify exact full-joint syndrome channels, isolated discarded reservoirs, arbitrary-bath uniformity, or the many-parent operator inequality.
