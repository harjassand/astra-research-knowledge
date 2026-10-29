# Independent receiving: derived holdout Schur recovery endpoint

28 October2026. PASS_SCOPED_DERIVED_NATIVE_HOLDOUT_CERTIFICATE. This separate receipt covers new files added after the frozen localization-demo receipt; it does not retroactively redefine that experiment.

Read derive_holdout_schur.py, HOLDOUT_SCHUR_NOTE.md and HOLDOUT_SCHUR_CERTIFICATE.json. The physical candidate quaternion and selected site are taken only from main_8192; larger_65536 supplies the validation contrasts and its already declared simultaneous coefficient radius. No SOURCE_ONLY parameters, true rotation, oracle score or generator probabilities enter the endpoint. Source-data separation and raw records were previously independently audited.

Reconstructed the physical candidate via a separate rational rotation formula, verifying SO(3), and formed its rank-one Bell projection exactly. Checked P²=P, TrP=1 and P Qsym P=0. Since Z=(I-P)Qsym P has rank at most one, its squared operator norm equals TrZ†Z. Recomputed the exact rational value and verified the saved upper norm by squaring. Recomputed all15 principal minors of W-kappahat(I-P); all are nonnegative. Thus the transverse lower bound is rigorously feasible, not merely a floating eigensolver estimate.

For qubit contrasts C_j=(m_j.sigma)/2, simultaneous coordinate errors<=eta imply operator error<=sqrt(3)eta/2. The saved rational a upper-bounds this quantity. Hence the received6a perturbation bounds give the stated positive kappa_cert and z_cert. The saved scalar shift satisfies lambda(kappa_cert+lambda)>=z_cert² exactly, so the Schur dual is valid. Withd2, native regret is bounded bylambda/2:

    580175473307511791/16000000000000000000
      = .03626096708171949...

The quadratic relaxation .03824863425265222 is also valid and weaker. Independent exact program/result: `holdout_schur_independent_check_20261028.py/.json`.

The local comparison is against every CPTP decoder on the selected physical qubit for the SAME actual channel as the holdout. Extending to the full two-output oracle additionally uses successful main-bank localization and the declared stationary source across banks; the conservative main-plus-holdout failure union is.02. These are coverage guarantees of the mathematical procedure, not posterior probabilities conditional on acceptance. The endpoint was derived after the initial demonstration and is explicitly labeled as such. No additional data were generated, no unknown payload was processed, and no decoder hardware/compilation was executed.

No gap found at this scope. No arbitrary future-memory, changed-channel, complete-operation or practical-comparative claim is received. Actual implementation error would require its own allowance.
