# Random-matching singlet survival, 2026-10-29

New-to-this-program construction: testing preservation of an exponentially large
spin-zero space using only random paired singlet preparation and paired Bell
readout. The all-n coefficient is (n+2)/(n-1) for the full singlet space, and
(d/K)(n+2)/(n-1) for a fixed K-dimensional singlet subcode. The full-space
coefficient is exactly sharp under a physical partial SWAP.

Status at creation: complete author proof and reproducible checks; independent
review pending. Any later independent review receipt must be read separately.
No historical priority, hardware advantage or general unknown-noise recovery
claim is made.

Governing files:
1. PROOF_MATCHING_SURVIVAL_v1.md: exact spectral and arbitrary CPTP/subcode proof.
2. EXACT_PARTIAL_SWAP_SHARPNESS_v2.md: strengthens the Section 4 small-angle
   argument to exact saturation; v1 otherwise remains intact.
3. COMPARATOR_AND_RESOURCE_SCOPE_v3.md: required conventional two-basis
   comparison and complete preparation/readout/routing scope.
4. check_matching_survival_v1.py and .json: reproducible finite diagnostics.

The program checked 31,839 partition inequalities through n=120, complete
matching Gram spectra at n=4,6,8,10, and 96 arbitrary complex CPTP/leakage and
subcode examples. Floating-point results are numerical checks, not proofs or
physical observations. The all-n argument is the governing proof.

Run: OPENBLAS_NUM_THREADS=1 python3 check_matching_survival_v1.py
Requires Python 3, NumPy and SciPy. No file downloads or hidden data are needed.

Dependencies: Collins–Matsumoto arXiv:0903.5143 Eq.3.6, Lemma4.3, Eq.4.6
for the known orthogonal Gram spectrum. Other program dependencies are not
needed to reproduce this isolated theorem; transferring it to existing
sequential guards or acquired encoders requires their governing hypotheses.
The separate focused primary comparator note is
../matching_prior_art_20261029/PRIMARY_COMPARATOR_NOTE.md.

What remains: independent review; complete guarded-operation substitution and
matched-resource comparison; hardware/noisy routing/calibration construction;
historical novelty assessment. It certifies a channel's action on a chosen
space, not a full environment model or arbitrary future dynamics.
