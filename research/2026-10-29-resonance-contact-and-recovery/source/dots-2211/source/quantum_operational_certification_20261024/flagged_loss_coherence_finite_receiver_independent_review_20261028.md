# Independent review: finite coherence-only receiver acquisition

2026-10-28. Reviewer `producer-workspace/review_general_face`.

**Disposition: cleared at its structured, conditional finite-acquisition and physical receiver-construction scope.** No load-bearing mathematical defect remained after review. This receipt does not establish historical priority, practical superiority, efficient scaling in qubit count, hardware execution or arbitrary-noise protection. It is a substantive internal mathematical/code review, not formal verification.

## Governing claims challenged and checked

1. **Physical promise.** The stated conditional map is CPTP and its contrast is `s_h u_0 u_1†`. A fixed unknown frame and nonnegative real coherence coefficient are essential. The specified receiver is CPTP, including when the actual flag state is rank-deficient. Its extension onto unseen complement directions is a chosen family rule, not statistical identification of an unrestricted unique optimizer. Its native composite is logical dephasing with entanglement fidelity `(1+s_h)/2`.
2. **Finite design rather than Haar access.** The d=4 Pauli classes form five commuting disjoint classes, and the exact script verifies their mutual unbiasedness. The odd-prime chirp construction matches the primary finite construction. The manuscript restricts complete MUB existence to the supplied prime-power interface, and pays setting selection, finite tables and measurement compilation. Capped rejection sampling preserves exact uniformity on accepted settings; its abort probability is separately allocated.
3. **Estimator phase and moments.** The `(+x,-x,+y,-y)` coefficients `(1,-1,i,-i)` produce `|0><1|`, not its adjoint. The factor 2 is necessary. From the finite 2-design identity, `E[Y]=rho` and `E[Y²]=(d−1)rho+dI`; consequently both rectangular second moments of the contrast estimator are at most `4(2d−1)I`. Subtracting the conditional mean only subtracts a PSD term. The increment bound `2d+1` is valid.
4. **Retained-memory concentration.** I independently read Tropp Corollary 1.3 and its dilation passage. The correct dimension factor is `2d`, and both predictable quadratic variations are controlled by `T*4(2d−1)`. The displayed conservative root implies the stated tail probability. The target is the predictable average, not a stationary channel. Fresh probe independence and current private settings are load-bearing. Summable repeated-bank budgets cover adaptive acceptance.
5. **Control error.** With the manuscript's half-L1 total-variation convention, mean bias `4d beta`, second-moment inflation `8d² beta`, and robust increment bound `4d` are conservative and sufficient. This comparison must hold conditional on each actual history; it is not a free calibration assumption. The matrix arithmetic allowance and nonvanishing systematic-bias floor are separately visible.
6. **Observed guard and phases.** Hermitian dilation has the unique positive eigenvalue `s_bar`; on its positive-eigenvector complement the spectrum is nonpositive. The residual equation therefore gives sine error at most `eta/a`, using the *observed* positive singular value. The coupled singular pair must share one phase. The raw-frame Frobenius bound `2eta/a`, positivity guard and nearest-isometry polar step imply operator error `4eta/a`. Independent singular-vector phase choices would invalidate the conclusion, and are explicitly forbidden.
7. **Full physical receiver.** The compressed channel difference has diamond norm at most twice the phase-aligned frame distance; the reset functional contributes at most another twice that distance. Therefore the half-diamond guarantee `8eta/a` is sound. This is full receiver substitution on arbitrary joint inputs, not future fidelity/capacity certification. The two-column QR count is at most `2d−3` complex two-level rotations plus column phases; it does not assume a full unknown environment operation. Coarse code/complement measurement and reset implement the intended map. A two-level rotation is not claimed to be a hardware-native gate.
8. **Resources and scope.** The statistical dimension dependence follows from the displayed radius under a positive eventual bank-average coherence floor and vanishing statistical/numerical errors. Positive calibration bias may prevent any prescribed small error. Dense table, accumulation, SVD, measurement and synthesis costs are disclosed. An equally informed conventional learner can use exactly the same statistic and receiver; no comparative superiority is inferred.

## Review-driven clarification

I requested removal of language implying a quantified sample advantage over full-environment reconstruction without an equivalent baseline; the source now explicitly avoids that inference. No theorem correction was required. The construction remains conditional on the family promise, including fixed V and phase-controlled nonnegative s_h. Passing a singular-value consistency check does not verify that promise.

## Reproduced and independent evidence

- Independently reran `..._exact_20261028.py`: exact d=4 finite-MUB identities, rank-one and rank-two flag instances, estimator moments, full receiver TP/action and fidelity all pass. Its 200 numerical perturbation checks are stress tests, not the proof.
- Independently reran the 250,000-shot ordinary-record adaptive-drift pilot. It accepts the declared loose half-diamond target 0.5, with certified upper bound **0.4481941161**, radius **0.0388560768**, and observed leading singular value **0.6935579988**. The hidden-frame diagnostic error **0.0158502373** is not used by its learner. The result is pseudorandom ideal-control simulation, not laboratory observation or a high-fidelity memory result.
- Wrote the separately bound independent check script: 300 complex perturbation/frame/QR trials at d=3,4,5,8,16. All perturbation bounds pass. Actual two-level counts are 3,5,7,13,29, respectively. Largest QR frame residual is `1.3516903470091818e-15`; largest complete compression/reset action discrepancy is `5.780422543648881e-15`. This validates conventions and the implemented finite mechanism numerically; it does not certify finite-gate synthesis error.

## Primary source checks

- [Klappenecker–Rötteler, quant-ph/0502031](https://arxiv.org/pdf/quant-ph/0502031): independently read Theorem 3 (complete MUB union is a projective 2-design) and the finite construction passages. Used only for the design interface.
- [Tropp, ECP16 (2011)](https://tropp.caltech.edu/papers/Tro11-Freedmans-Inequality.pdf): independently read Corollary 1.3, both predictable variances, the rectangular dimension prefactor and Hermitian dilation reduction. Used only for the concentration theorem.

## Cleared scientific change and limits

The result replaces generic support/dual-gap acquisition for this promised flagged-loss family with an acquired coherence statistic, removing a positive flag eigenvalue requirement and constructing a complete nonunitary receiver from finite ordinary measurements. It does not supersede the previous generic theorem or extend it to arbitrary unknown recovery families. Changing V, uncontrolled coherence phases, unknown control calibration, scalable near-perfect preservation and unrestricted oracle identification remain unresolved or excluded.

## SHA-256 bindings

- `flagged_loss_coherence_finite_receiver_20261028.md`: `00db1c1f22c20ba7c49b91691ab9778c6405a45682ab34d0fa97bfcfc60e6069`
- `flagged_loss_coherence_finite_receiver_exact_20261028.py`: `d22b08c34e33dedf3abd11db9375dd97c2a74b187aec89ed6c3d897dcc5d4907`
- `flagged_loss_coherence_finite_receiver_exact_20261028.json`: `fca23ff8073883a9225b52a8eb843f45ad44a25e531be7c3b8d226761ecc4853`
- `flagged_loss_coherence_finite_receiver_pilot_20261028.py`: `c18488b6374005e8a783599eeccc4a0dec191ba86f5ed35edd1257eac5c8485e`
- `flagged_loss_coherence_finite_receiver_pilot_20261028.json`: `abed8bfa04b27c43911f06bf04abb0dcbe9e9ad38f4c10535d1bfa2d0442cc1c`
- `flagged_loss_coherence_finite_receiver_independent_check_20261028.py`: `7da8a88064271a78bc76d39367f8ad028505bfcc33edbf832d4228e569a9c16f`
- `flagged_loss_coherence_finite_receiver_independent_check_20261028.json`: `e0e292c850d422d3c164ab926d2f150d279099a6679f99ab4c3b07b9f94e0749`
