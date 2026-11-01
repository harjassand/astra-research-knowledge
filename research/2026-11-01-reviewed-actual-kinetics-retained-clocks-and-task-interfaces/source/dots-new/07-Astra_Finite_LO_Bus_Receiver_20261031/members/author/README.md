# Finite-LO bus receiver: author continuation

Ordinary weak-field homodyne with finite photon-number resolution replaces the ideal quadrature measurement for the already accepted vacuum three-sector bus. This is a mathematical instrument construction, not a detector acquisition, novelty claim or architectural advantage.

Read `FINITE_LO_RECEIVING_AND_BOUNDARY.md`, then the unchanged root candidate. The exact grid specifies finite LO photons, count cap, readout latency, correction table/precision and continuing data noise. Mean4 LO photons and total count cap20 give upper **0.009134838999948075**, including an additional readout-time unit and the separately supplied residual 0.001 allowance. All failures are retained. The fixed-cap optimum is not achieved by sending LO energy to infinity.

The same apparatus must actually provide .999 mean efficiency, calibrated modal/phase overlap, correct low-count instrument and specified response. Published weak-field homodyne is direct ordinary precedent, not evidence those specifications have been acquired. Arbitrary warm-apparatus correction does not follow from this vacuum/coherent-signal calculation. No physical threshold, platform feasibility, or universal gate architecture is established.

Scripts: `python certify_finite_lo.py`; `python test_finite_lo.py`. The first uses exact rational/dyadic intervals and the byte-identical imported accepted certifier; the second runs 487 diagnostic/high-precision/finite-table checks. NumPy, SciPy and mpmath are used only in diagnostics. Run in a COPY to preserve snapshots.

Accepted dependency: `Astra_Desired_Bus_Gate_and_Ordinary_Eraser_20261031.zip`, SHA256 140a0521116d8051176dbbf7576570c1d50faf980bd1e3cbbab26179f43db232; qualified binding 3ea9c10a2626b8f0d99edf89f662a3378d50ca8729a03b23003fb98a47f72a86 controls its non-Gaussian record-noise correction. This continuation does not invoke that rejected variance-only identification. Its two imported source files are byte-identical to the accepted originals.

Stop receiver-fixture expansion here unless whole review finds a defect. The next consequential choice is an actual interaction/observation service not already supplied by ordinary low-loss closed buses, coherent reuse, encoded or variable-B alternatives; a cheaper symbolic source-class argument alone is not that choice.
