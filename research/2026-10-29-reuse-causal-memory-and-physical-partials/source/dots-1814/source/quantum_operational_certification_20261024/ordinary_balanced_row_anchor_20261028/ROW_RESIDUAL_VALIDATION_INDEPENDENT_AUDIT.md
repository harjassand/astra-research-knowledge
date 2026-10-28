# Independent receiving: ordinary row residual validation and fallback

28 October 2026. **PASS with the explicitly bound implementation-probability clarification below.**

Reviewed source: `ORDINARY_ROW_RESIDUAL_VALIDATION_AND_FALLBACK.md`, SHA-256 `67712222c80855995bd0ded173d4a2f9a1663bdf405f8ec7898f894c7917d442`. The source was not edited. The author accepted the receiving clarification in `FAST_PATH_RESOURCE_EVENT_IMPLEMENTATION_CLARIFICATION.md`, SHA-256 `cea657a43f9b6fac5a9567a285de21676e523b0cb54b1b2f768332896f74d3b0`. Only its one-stage residual-route clarification is received here; its statements about the separately pending automatic schedule do not receive that extra theorem.

## 1. The physical positive lift and actual observations

The fixed actual source, four-real-coordinate linear encoder, and ordinary six-state loss preparation admit a single linear purification. Explicitly use source Kraus index and ordinary probe label as environment indices, with the receiver-local anti-state register included in the observed loss-state register. Each purification column is linear in x. Consequently row maps G_i exist with `B_i=Re(G_i^*G_i)` and `sum_i B_i=I_4`. This is a property of the actual physical preparation, not of an arbitrary positive matrix-valued quadratic, and it is not an acquired positive completion.

For any learned rational unit v_i, `Tr[B_i(I-v_iv_i^T)]` is exactly the squared Frobenius norm of the discarded row map `G_i(I-v_iv_i^T)`. It is nonnegative even when the learned direction is inaccurate or B_i has rank greater than one. A uniform choice among three orthogonal selectors in v_i's kernel, followed by the actual loss-coordinate measurement, therefore has mean S/(3d) after the uniformly sampled row index. A row not retained contributes a deliberate zero and consumes its declared ordinary call. No unobserved rejection or rare-success denominator occurs.

The discarded-coordinate experiment has mean Lambda/4 because its selector second moment is I_4/4. These identities use actual physical probabilities, not signed tomography corrections or an empirical eigenvalue difference. In particular they provide variance at most the mean without a spectral floor.

The rational Householder denominator is `2(1+|v_1|)>=2`; its last three columns are exactly orthonormal and orthogonal to v. No eigenbasis or source-gap approximation is required. The receiver basis is the supplied physical basis. The validation can use up to 3d additional actual settings; it is not claimed to have constant support. All source-input selectors remain classical ordinary choices.

## 2. Soundness and statistical chronology

The candidate set, directions, and anchor are frozen before either validation bank. Conditional on that full record, the source is fixed and reset and the fresh outcomes have the claimed Bernoulli means. This holds for arbitrary candidate-generation errors; soundness does not use true leading directions or exact rank-one rows.

For the threshold test, stochastic monotonicity reduces false acceptance at p>u to p=u. The lower tail is at most `exp(-nu/8)`. If p<=u/4, rejection is bounded by the upper tail at p=u/4, at most `exp(-nu/12)`. The factor 64 and finite ceilings give slack for both inequalities. Comparing an integer count with the rational threshold preserves these event inclusions; no floating estimate determines the test.

The two uniform conditional bounds average to false-acceptance mass at most 2beta_0. This is an unconditional mass bound. Dividing it by a small acceptance probability would not yield the same conditional confidence, and neither the source nor this receipt does so.

The later Bures bank is fresh after both pilot and validation. Its conditional rank and failure guarantees apply to the actual selected anchor. A possible mixture over earlier records remains a mixture of product experiments; no tensor power of an averaged state is inserted.

## 3. Coherent task transfer

With the learned row projection, `Phi_x=Rhat_x Phi_x0` exactly. The actual common purification gives both `||Psi_x-P Psi_x||<=sqrt(Lambda)` and `||P Psi_x-Phi_x||<=sqrt(S)`. Since the known candidate balance bounds `||Rhat_x||<=2/sqrt(kappa)`, the retained-anchor mismatch is at most `3sqrt(S/kappa)`.

For the SAME full-CPTP decoder, `||(3/2)C^T||<=3` turns these into the two root-risk terms in the source. Every lost cross-coordinate coherence is paid. P is a mathematical projector on the auxiliary loss-state representation, not an imposed payload measurement or a pinched comparator. One Uhlmann alignment with the actual anchor adds the stated bank term, uniformly in x and every decoder.

The certified thresholds yield exactly `297 gamma epsilon/2^24`, which is below `gamma epsilon/32768`. The known-coefficient optimizer uses `b=6/kappa`, a positive quadratic surrogate, and the already received finite full-CPTP feasibility repair. It need not repair the surrogate into a normalized channel. Its optimization and root-risk arithmetic give `27epsilon/32768<epsilon/1024` on correct accepted histories.

## 4. Fresh generic fallback and full-history risk

I read the received clipped generic learner's local Bell-risk and fixed-cap contracts, and reverified all sixteen entries of its independent receipt. Its mathematical/control primitives are imports, not a new tomography or compilation review here.

For this fallback the physical output basis is already known. Use the identity frame and, if its displayed dimension convention is needed, the trivial valid encoded-Choi rank bound `R_fallback=2k`. Every qubit-input/k-output Choi matrix has rank at most 2k, so `k<=8R_fallback` and `r_fallback=d=2k` hold without a physical compression or structural promise. This does not degrade its stated k^4 bound. The fast Bures bank can separately retain a sharper supplied r. Thus no unsupported k=O(R) relation for the physical register is inferred.

Rejection is determined before any fallback samples. Fresh fallback data can therefore use its uniform expected guarantee conditional on each rejected record. Multiplying by rejection probability and summing the accepted branch is valid. The accepted branch pays false-acceptance mass once and the later bank's failure mass once. The exact budget is

`epsilon/512 + 2epsilon/2048 + epsilon/512 = 5epsilon/1024`.

Every selected policy is physical, so bad histories cost at most one Bell loss. This proves the arbitrary-source risk theorem with a generic fallback, without any rank-one or balance promise. Without that fallback, only the selective accepted-branch statement is available.

## 5. Fast completeness, finite controls, and the receiving clarification

On the balanced exact-row subclass the received weighted count proof, with the larger pilot cap, gives `Lambda<=Lambda_max/4` and `S<=S_max/256` on its good event. The rational anchor search succeeds there. These are sufficient for the two tests to accept with the claimed ideal-reference probability. They are not necessary conditions for acceptance and are not presumed on arbitrary sources.

The fast cap is a high-probability EARLY-COMPLETION bound. The deterministic reserved cap additionally includes the received generic k^4 fallback and is fixed before data. Failed histories are not given an expected-stopping refund. All controls, sampler bits, candidate search, actual row-dependent selectors, matrix bank, optimization, decoder synthesis and memory fit that worst-case horizon.

**Clarification raised in this review and accepted by the author:** finite implementation changes the distribution of the branch-decision record, not only the final payload channel. Accordingly the source's displayed `1-beta_t-2beta_0` fast-completion probability is first the ideal reference experiment's statistical probability. To transfer the resource-event claim, allocate a complete predecision instrument/record discrepancy `nu_pre<=epsilon/1024` INSIDE the existing total epsilon/2 implementation allowance. The same bounded-bit sampler and finite controls can meet this by greater predetermined precision; it changes no source cap. A process-distance bound that only discarded the decision record would not by itself justify this event claim; the predecision allowance must retain that classical record.

Using the conservative event difference at most nu_pre gives actual fast-completion failure at most

`epsilon/512 + epsilon/1024 + epsilon/1024 = epsilon/256`.

This replaces the unadjusted ideal probability when speaking of actual finite-control source usage. It is not an additional final-channel debit outside epsilon/2. The arbitrary-source payload-risk bound and deterministic worst-case source cap are unchanged. The implementation clarification is version-bound in the receipt; the original source bytes remain preserved.

## 6. Independent evidence and scope

The new deterministic script `row_anchor_validation_independent_checks.py/.json` uses a physical source family different from the author's: two rational-amplitude unitary Kraus branches move selector rows differently and introduce complex phases. It preserves one actual six-state purification over all encoder probes. Twelve source models, 48 encoder tests, 432 actual row-kernel expectation identities, 27 exact rational Householder constructions, 12 finite binomial tail evaluations, and 128 exact acceptance/fallback mixture cases pass. The largest physical algebra residual is below 2e-16. The same script supplies exact count/net/budget checks for the companion acquired-anchor result.

There were no RNG draws, sampled source outcomes, aggregate simulated trial banks, actual source calls, production SDP executions, or hardware experiments in this independent evidence. Binomial CDF evaluation is not trial sampling. Author aggregate-count diagnostics are a distinct evidence class and are not relabeled here.

Received scope is: an honest ordinary positive-residual validation route, arbitrary-source expected-risk soundness through a fresh generic fallback, and fast completion on the stated balanced exact-row subclass, all in a known physical receiver basis. It does not establish generic fast acceptance, arbitrary-basis acquisition, a universal k^2 worst-case learner, a fixed-public-record certificate, or a separation from an equally informed conventional protocol. The full decoder remains coherent CPTP and the protected-reference/coherent-selector interface has not been strengthened. The approximate-row and automatic-schedule manuscripts remain outside this receipt.
