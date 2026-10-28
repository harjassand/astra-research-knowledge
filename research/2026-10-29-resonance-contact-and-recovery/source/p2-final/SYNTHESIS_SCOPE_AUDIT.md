# Independent synthesis and scope audit

Reviewer: `producer-workspace/noise_challenge`. Scientific checkpoint: 29 October 2026 Australia/Brisbane.

## Verdict and exact synthesis versions

**PASS at the stated mathematical and resource scopes.** The synthesis accurately represents the actual reviewed results, preserves the adverse comparison and corrections, and does not promote covariance, a sufficient comparison allowance, or a retained-mode count into a device or computing-advantage claim. No scientific publication condition remains pending in this audit: the actual loss review and its receipt arrived and were read before this verdict.

Audited synthesis:

| File | SHA-256 |
|---|---|
| `README.md` | `8ab2672b821180e03ac719bad4ab31bf778d02b1ccc7c8e8fb2ccc3f60ecfaf2` |
| `SOURCE_DECISION_AND_CORRECTIONS.md` | `292bfe2204a3d4bab0b6280e00f425488813ee82bfc1c936a04bcaa4cba975c3` |
| `noise_challenge/ZERO_MEMORY_SIGN_CORRECTION.md` | `babfce5a23d63d30dc8c77ec0cc1a5914584e5c51d15f229e650d158d679e38c` |

This is an independent audit of the synthesis against the proofs and actual reviews, not another broad revalidation of every theorem. I previously independently reviewed the path theorem and active-Gaussian extension. I authored the separate zero-memory/loss notes, so their independent acceptance here is the actual review by `producer-workspace/code_alternative`, not my own approval. No authored proof or synthesis file was changed. No new numerical theorem validation, primary-literature priority survey, hardware validation, or external peer review is claimed.

## Actual review status and version consistency

I read the complete-record, alphabet, loss and amended-parity review texts and all six review receipts. The path/universality review records are my previously completed independent work. Direct SHA-256 checks confirm that all nine reviewed proof/correction versions below still match their actual review pins:

| Result / current proof | Proof SHA-256 |
|---|---|
| `measurement_frontier/NOISE_MEMORY_PATH_THEOREM.md` | `69b2b7ff8bf8750ebeb1da411eb5f44d41f6b1299e219c60d5f81a1834aab13d` |
| `PASSIVE_UNIVERSALITY.md` | `27e73c6793f3bc453608782e52bd447c8a80b2ac90d00903b0ca8fb92fad8847` |
| `COMPLETE_RECORD_CONVERSION.md` | `f02fceaedb0930c82ed4faeaebe108c9ceae3277ee0fa37bc0af499c416c7b1a` |
| `ALPHABET_NOISE_OPTIMIZATION.md` | `296e789618ef9808eb86e9d1046697ec2c9a53a09aebfb9d570493dc79c083bd` |
| `UNIFORM_DETECTION_FRONTIER.md` | `08efbd4078322633d75aa016776d130f9aa4c8b4b203fd699ef4301f26179f48` |
| `noise_challenge/LOSSY_BELL_WITH_EARLY_RECORD.md` | `5315b6328f3e3a1b4b4f86ff2e97964ab70a3b2462cd5f3c17de00593789e968` |
| `noise_challenge/ZERO_MEMORY_NOISE.md` | `52fda373107caa9cfaa1cc1887dfcd27bd6f0ef5e77d1ad4db560a39ac363405` |
| `code_alternative/PARITY_ASSISTED_CODE.md` | `8768511b2dc11f67b216c6531aa0168c199993f7ddf68dcb278a37c927307fcf` |
| `code_alternative/CORRECTION_TARGET_FACTOR.md` | `a6afe35b21dedf2d294e77bf53d7bcf3d25225781aa4d17f837d6f98266a74cd` |

The actual independent-review text pins are:

| Directory under `reviews/` | `INDEPENDENT_REVIEW.md` SHA-256 |
|---|---|
| `path_theorem/` | `899af9a1e03c4714732bc0095ce65262f20823f5a25c583d5b8c0b9f7ad0c527` |
| `universality/` | `8e097ead948ad8c052902c04e39fcb46f26e2b5fb4ca7fd104d4adf60d04b20c` |
| `complete_record/` | `60e33da49e872448b0bd276c77bae74c8bd48933c6b99fe7482e6b4b43f7ff6d` |
| `alphabet/` | `9993a4cafd3c8dd9528f946957c686a47d895096c42b321b5cca62e05ed528ff` |
| `loss/` | `02dc3d600f1a143e433a88b33f2d785694c40360baf7ab9c7033c94424fd481a` |
| `parity/` | `869ac3a35bd294984643245b335609ab2dbb6427ddfc271ce7404aed15ce805d` |

The loss receipt is `e96747406fe2a1453c7ae04c5efced6e7a346ef4120a54ca81905059a07cff05`. It accepts both the lossy receiver and root's uniform-efficiency corollary, records the separate scalar sign erratum, and reports the actual independent 8/54/90-case exact audit and isolated author replay. This is an arrived review, not an anticipated one. Authored headers remaining unchanged are not inconsistent with these later review records.

## 1. Main consequence and active universality

The central consequence is an exact finite-dimensional characterization and constructive realization of a declared final Gaussian measurement channel under causal storage constraints. The skew path is simultaneous across all cuts, and all quantum paths across a cut are counted. The claim is not that an arbitrary supplied field state can be simulated efficiently, nor that the global rank-constrained design problem has a general efficient optimizer.

The active extension is represented at its actual scope: finite fixed deterministic Gaussian dilations, fresh independent normal finite-covariance Gaussian supply and channels, fixed affine reporting and linear displacement feedforward. Passive synthesis attains the same **ideal retained canonical-mode versus final reported-POVM noise** set. This does not preserve active energy, fresh-mode count, temporary live width, gain/precision, fixed lossy hardware, quantum output states, or early output-release obligations. Adaptive axes, nonlinear reporting and non-Gaussian resources remain excluded. The README's later explicit class restriction governs its introductory shorthand about the strongest Gaussian alternative.

## 2. Reported measurement and full actual record

The synthesis explicitly separates two objects. The path theorem characterizes the declared reported Gaussian POVM, which can be a classical coarsening. The complete-record result uses the delivered augmented-feature receiver and its actual feedback, compares controlled unitaries on a specified independent detector supply, and only then applies the common full-record channel.

The bound `sqrt(1-exp(-max_z z^T N z))` is therefore not inferred from a Gaussian convolution's covariance. Its mathematical baseline retains the same receiver's record assemblage, including correlations with an initially correlated source/field/reference. It is not an input-independent classical record and does not apply to an arbitrary replacement raw refinement merely because its reported marginal is the same POVM. No independent-source assumption or original-field energy restriction is silently reintroduced.

The claim remains an ideal supplied-model bound. Physical optical errors acting on arbitrarily energetic fields require a separate input/control contract. The auxiliary source displacement is a comparison operation, not an acquired physical source-to-detector coupling. These distinctions are accurately preserved.

## 3. Optimization claims

The weighted trace formula is exact for a fixed path, and the two-batch singular-value tail is a genuine optimum in its declared ideal model. The three-batch trace comparison proves failure of greedy independent-cut selection; it does not prove the cheaper displayed path globally optimal.

The four sign-objective values are supported by actual independent exact primal/dual checks. The minimax theorem optimizes covariance on a fixed skew path for the full specified sign alphabet, with one common adversarial correlation matrix. The reported reversal from trace ranking to sign ranking survives covariance optimization on those paths. It is an optimum of a sufficient complete-instrument allowance, not a lower bound on actual corrected-channel error and not a global path optimum. The source-coordinate Hadamard rotation changes the supplied coupling family; it is not a free qubit relabeling.

The elliptope relaxation is described in the correct upper direction. Singular weighted subproblems can have unattained infima even though the full sign-cube program attains its minimum. The synthesis does not promise unavailable infinite-gain implementations or inexpensive exact sign optimization.

## 4. Detector and memory loss comparisons

The uniform-efficiency statement correctly applies only to the fixed passive/fresh-vacuum/common-efficiency model with otherwise ideal retained channels. The loss review directly supports its all-path extension and covariance transformation, including all-input/reference measurement statistics. It does not assert equality of inaccessible quantum loss complements.

In the Bell table, “exact optimum” means the **unweighted trace-noise optimum**, with the displayed isotropic covariance attaining it, as confirmed by the following trace-noise comparison and the actual review. It must not be read as a Loewner lower bound on every anisotropic feasible covariance. The tapped receiver is an explicitly constructed one-mode comparison under a specified storage channel, not an optimum over all coherent-memory strategies.

The pure-loss improvement for every positive transmissivity and the stated thermal-benefit condition are conditional covariance comparisons. Active squeezing before inefficient detection is excluded from that passive optimum and can change it; ideal Gaussian universality does not forbid that resource. The actual early record is retained, and the full raw covariance differs from its reported Bell marginal. A thermal covariance calculation alone does not inherit the independent-vacuum full-record source-erasure certificate.

## 5. Different mechanism, correction and ancestry

The parity route is preserved as an actually constructed alternative, not a list of suggestions. Its reviewed operator identity covers arbitrary known-sector correlations and true parity-refining fine outcomes. Noncommuting bounded contacts and a nondestructive core-sector boundary provide the stated mathematical extension and reuse principle.

The amended target-factor result is correctly distinguished from the failed original overextension of a system-only error-algebra obstruction. A known code-preserving diagonal target may factor from the symmetry-qualified error operation and survive recovery; the whole propagator need not obey the same parity covariance. This is not permission to relabel an unknown logical error as the desired gate. The many-body target control, known-sector preparation, complete charge collection, stabilizer instrument and untargeted error channels remain unacquired.

The synthesis correctly credits the one-qubit photon-parity eraser and notes that it already avoids repetition overhead. The full-family charge/rate statement is not a universal capacity limit. Josse-type tap/heterodyne/feedforward amplification is also credited as established machinery, and the new loss comparison is not presented as invention of an amplifier. The current source ledger states read scopes and archive gaps; this audit adds no historical-priority finding or newly acquired missing archive.

## 6. Preserved failures and review corrections

I checked the predecessor README and actual star review. They retain the stronger compatible one-hold returning-bus comparison and the actual adverse long-accumulator result. The current synthesis does not replace that result with the new Bell covariance comparison or imply that the failed gate schedule is now a superior architecture.

The repeated-cut sign correction is correct and explicitly governs the preserved authored note: arbitrary nonzero real `a,b` require `4m|ab|sqrt(w_Q w_P)`. The general absolute-trace theorem already has the correct sign behavior, and the saved examples use positive values. The synthesis lists the correction and does not silently rewrite the author pin or its review history.

The known failed inverse-gain comparator, per-cut greedy path, covariance objective, and target-algebra inference remain useful failures with their actual implications. None is elevated into a physical no-go theorem.

## 7. Evidence and remaining operational boundary

The review map reflects actual work: independent analytic reviews, isolated author-program replays, and separately written exact audits are distinguished in their receipts. Floating receiver residuals are diagnostics, exact rational checks concern finite algebra, and neither is a device tolerance or a total workload error bound. This audit did not repeat those executions or count itself as another independent solver.

The remaining essential interfaces are visible: physical coupling or exact symmetry, collection and no-return conditions, independent supply and startup charge, storage lifetime and loss, optical/readout gains, local-oscillator and classical-record resources, source coherence, controls, syndrome extraction, preparation, readout, reset, leakage, relaxation, scheduling and reuse. The results establish conditional general instruments and synthesis machinery. A scalable computing advantage remains unproved.

`REPRODUCE.md` exists at this checkpoint; its instructions are maintained separately by root and were not part of this scientific scope audit. There is no pending loss-review condition. Any later substantive revision to the two synthesis files should receive a new pin rather than inheriting this verdict without inspection.
