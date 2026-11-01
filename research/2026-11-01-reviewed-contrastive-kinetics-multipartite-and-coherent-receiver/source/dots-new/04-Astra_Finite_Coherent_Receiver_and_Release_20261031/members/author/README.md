# Pending finite-rate coherent receiver and released-output candidate

Author candidate for whole independent review; not accepted hardware or a new cancellation mechanism. This directory is separate from the accepted monitored-phase package. Ordinary coherent feed-forward is the mechanism; ordinary exact coherent projection and variance-sensitive overlap geometry are the strongest analysis routes.

Read:
1. `FINITE_RATE_COHERENT_ERASER_CANDIDATE.md`: actual finite source + finite-bandwidth conditional cavity, routing/internal loss, source/cavity initialization, complete-field comparison, exact finite-time retained-cavity formula, phase and resource costs.
2. `VARIANCE_REFINED_COHERENCE_ROOT.md`: separately authored root geometric lemma, SHA256144f70e7e19e0c65d0dbcb515bbdf57de7b886d0d667257e7a331e9a5f337331. The candidate consumes the same contraction/complex-coherence bound, not a competing formula.
3. `FINITE_RELEASE_INTERFACE_CANDIDATE.md`: paid finite receiver chi-off ramp, source-blind SWAP into a separate memory, continuing original source and actual retained correlations. No fictitious reset or source-coupling shutoff.
4. `scalar_budget_certificates.json` and `release_budget_certificate.json`: exact sufficient supplied-model budgets. The 70-row grid preserves failures. The full release example has total diamond upper0.009690440319143791 against target0.01, but its source/receiver/routing/SWAP/initialization/residual component services are supplied specifications, not acquired hardware.

Important selection limit: the unwanted source in this candidate does not supply the desired graph gates. Avoidance/isolation or a different ordinary architecture may beat this extra receiver. The unchanged-source comparison is not broad architectural advantage. A next capability task should require the source/mediator to supply an otherwise unavailable useful interaction and compare against ordinary closed-trajectory quantum-bus / no-knowledge-eraser gates at equal access and cost.

Scripts (run COPIES in a fresh scratch directory if preserving review snapshots):
- `exact_source_overlap.py`: 2x2 exact initialized source/entire-field coherent projection enclosure, no Fock cutoff.
- `certify_scalar_budget.py`: exact rational comparison grid; retains generic and sharper bounds.
- `certify_release.py`: exact finite-switch/correlated-source-SWAP/remaining-error budget.
- `check_coherent_cascade.py`: 3 exact symbolic checks and six actual finite-cavity numerical diagnostics; cutoff agreement is NOT an infinite-mode certificate.
- `test_coherent_receiver.py`: exact overlap-generator/geometry checks, high-precision and higher-bit interval replay, loss/phase tests, actual finite-source cascade checks, and correlated-source finite SWAP diagnostics.

Dependencies: Python, NumPy, SciPy, SymPy, mpmath. Certificates use exact rational/Gaussian integer-style arithmetic; diagnostic expm paths remain floating. No opaque hardware calibration, source output tomography or experiment was performed. No earlier accepted source file was changed. Historical `WORKING_COHERENT_ROUTE.md` is deliberately excluded from the strict candidate manifest: it is an exploratory all-time-scattering note, not this finite-time proof.
