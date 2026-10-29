# Independent receiving review: one jointly compressed payload batch

2026-10-29. Reviewer `producer-workspace/review_history_program_bounds`. **ACCEPT the direct batch error statement and the conditional-noise distinction. No outer-code/rate theorem is received.**

This receipt depends on the corrected single-payload recovery receipt and its reference-joint compression interface. N training inputs are independently prepared Choi inputs; the M payloads may have an arbitrary joint state with an external reference. One compression on all N+M encoded outputs gives the exact latent representation

`integral J_U^tensorN tensor (A_U^tensorM tensor id_reference)(rho) dU`.

The same U acts on every register. A complete training record t has likelihood independent of rho. Conditional on U,t, applying the learned physical recovery separately to all small output registers gives the tensor-product **channel** `C_(U,t)^tensorM`, where `C_(U,t)=R_t A_U`. Entangled inputs/outputs need not be product states. Fresh ideal dilation ancillas implement those local recovery copies; any implementation correlations must be included in the full batch error budget.

On the good training event, `halfdiamond(C_(U,t),id)<=e0=k sqrt(3delta)`. Telescoping the tensor powers and using the diamond norm1 of each channel gives joint error at most M e0 for arbitrary entanglement/reference. The training-bad event is one shared event of weight at most beta; its conditional joint channel is still CPTP, so it contributes at most beta once. Averaging the latent/training distribution and adding the **entire batch** implementation budget gamma yields

`halfdiamond(batch,id_(k^M)) <= M e0 + beta + gamma`.

No independence of the calibration errors is assumed. Gamma must include all M recovery implementations and the larger N+M compression, not merely reuse a single-payload synthesis budget. For a fixed overall error target as M grows, e0 must decrease accordingly; the elementary tomography cost N consequently grows with M. The assertion that one training block is shared does not establish a constant training cost for arbitrary batch size at fixed global accuracy.

Each source call has independent junk under the memoryless promise. All training and payload registers must be retained through the one joint operation, paying at least `(N+M)log D` output storage plus training references/work and decoding latency. The learned small matrix belongs to that batch's frame. Independent later compression creates a different frame, so no reusable decoder for future original-D outputs follows.

## Pauli/Weyl statement

Supply independent uniform logical Weyl keys on each payload before its source encoding and matching inverse corrections after decoding. Conditional on U,t, and **averaging those independent keys**, each logical channel is its Weyl twirl: its normalized Choi matrix is diagonal in the Weyl/Bell basis, hence it is a Pauli/Weyl mixture. Product key distributions and the conditional tensor-product channel give a product of these twirled channels. This remains valid in composite dimension for the standard finite Weyl unitary error basis. It is not an assertion conditioned on each individual key, nor on the unconditional averaged calibration channel.

Twirling contracts the distance to identity. A Pauli/Weyl channel's total nonidentity error probability equals its half-diamond distance, by the Bell-state lower bound and mixture triangle upper bound. Thus the existing good-event certificate can provide a uniform conditional noise bound. An actual outer-code construction, its overhead, locality, implementation errors, success criterion and rate still need proof; none is supplied or implied here.

The shared-Z example is correct. With probability beta applying Z to every payload gives a two-error probability beta, while independent copies of its averaged one-use channel give beta². The two-use channels differ in half-diamond distance exactly `2 beta(1-beta)`, as seen by their diagonal product-Bell distributions. Therefore substituting independent copies of the averaged channel is invalid.

`independent_checks.py` verifies exact shared-calibration error formulas, this counterexample, qubit/qutrit Weyl/Bell diagonality, and tensor-channel bounds on entangled small inputs. These supplement the derivation; they are not an outer-code simulation, hardware run or large-N+M compression execution. The source draft is preserved and hash-bound by the receipt.
