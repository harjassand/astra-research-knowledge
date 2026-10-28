# Training-to-full-qutrit-holdout bridge without an accuracy-exponent loss

27 October 2026. Local post-cutoff. Root probability construction, independently checked and written by the source verifier; separate receiving requested.

Dependencies: `unknown_reset_relative_projector_receiver_root.md`, its source audit, `unknown_orthogonal_reset_reusable_recovery_theorem.md`, and `full_qutrit_unentangled_holdout_verification.md`.

Use the promised unknown reversible/orthogonal-reset source with actual signal weight p>=p0. On a good relative-learning event let Lmax bound every learned positive-band projector risk. The deterministic receiver construction has Lmax<=10eta p. Its decoder is held fixed before independent holdout begins.

## 1. Probability-level genuine and reset errors

For any pure logical input psi, purify its unnormalized genuine source branch, of total mass p, including the mixed flag and all local Bell/measurement registers. The received retained-isometry hybrid, including controlled known corrections, gives an ACTUAL vector difference from the ideal genuine decoder bounded by

 ||u_actual-u_ideal||<=sum_{j=1}^9 sqrt(2L_j)
                      <=9sqrt(2Lmax).

The ideal genuine output is accepted with qutrit state psi. Consequently both of the following orthogonal outcome projections annihilate u_ideal:

 - final accepted flag AND qutrit projector I-P_psi;
 - final erasure flag.

For each, its actual probability is therefore at most the squared vector difference, namely162Lmax. This is a probability estimate, not the square-root trace-distance estimate used for an arbitrary output test. All environments are retained until after the projection argument; tracing them out does not change these probabilities.

Separately the received always-reject reset hybrid bounds total accepted reset mass by81Lmax. Its wrong accepted mass is no larger. Thus, averaging the pure-input statements over the known qutrit2design,

 b<=243Lmax,                                          (1)
 p-162Lmax<=a<=p+81Lmax,
 |a-p|<=162Lmax<=243Lmax.                             (2)

Here a is ACTUAL average acceptance and b is ACTUAL unconditional accepted mismatch, precisely the quantities in the holdout theorem. No unknown p or training-success flag is observed by the test.

## 2. Compatible training and holdout accuracies

For target holdout relative accuracy0<nu<=1, train the receiver with the existing construction's parameter

 nu_train=nu/8,
 eta=nu_train²/100000=nu²/6,400,000.

On the good training event, (1)--(2) and Lmax<=10eta p give

 b<=2430eta p=(243/640000)nu² p,
 a>=p-2430eta p>=3p/4.

The latter uses deliberately weaker constants than (2), but retains enough slack. In particular

 q=b/a <=(81/160000)nu² <nu²/1536,                    (3)

since81*1536=124416<160000. Using only a>=p/2 would lose this particular numerical slack, so the stronger three-quarter estimate is used explicitly.

Run the fresh holdout theorem with supplied ACCEPTANCE floor p0/2, not p0. The actual a>=3p/4>=p0/2 meets its completeness premise even at p=p0. Its deterministic cap becomes ceil(5m/(2p0)); its certified lower acceptance is at least p0/4. The certificate targets G_a at actual acceptance a, and does not silently identify a with p.

Conditional on every good training output, the held-out verifier therefore passes with its stated high probability and certifies complete qutrit error<=nu a. Soundness of an issued certificate also applies to bad training outputs because the holdout theorem is uniform over every fixed accepted CP map.

## 3. Confidence and resources

Choose the training good-event failure probability beta_train and holdout failure probability beta_hold separately. The acquired relative estimator allows arbitrary confidence by changing only its logarithmic batch factor; no change of eta is required. With probability at least1-beta_train-beta_hold, training is good and the independent holdout issues a valid certificate. False certification itself is bounded by beta_hold even without conditioning on training success.

Training at nu/8 multiplies its leading accuracy factor by the constant8^4, and preserves

 O(sr/(p0 nu^4) polylogs).

Holdout has deterministic cap O(log(1/beta_hold)/(p0 nu²)), and expected/high-probability actual-throughput cost O(log(1/beta_hold)/(a nu²)). Both accepted and rejected extra source calls are charged. Training and verification systems are discarded; the acquired classical decoder remains reusable.

The probability-level bridge is essential: replacing (1) with the generic trace-distance bound would only give b=O(sqrt(eta)p), forcing eta=O(nu^4) and an unnecessary nu^-8 training exponent. The actual wrong-output projection annihilating the ideal branch avoids that loss.

This is not a structural-promise certification, a guarantee for nonstationary future uses, or a claim that every nu-good device passes the verifier. The actual promised construction is shown to satisfy its explicit small-mismatch completeness margin. No entangled holdout probes or observable bad-training flag is assumed.
