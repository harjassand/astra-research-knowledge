# Independent controls and packing receipt: approximately local joint recovery

28 October 2026. **PASS.** Reviewed source:

`ordinary_approximately_local_joint_recovery_20261028.md`

SHA256 `1ae8d8f836d366268a4c8f182b9c8b679ba77aea9fde5ebe669e5e576ad74c4d`.

This source-specific review extends the separate analytic proof in `approximate_local_algebra_packing_controls_audit_20261028.md`. Its deterministic check and receipt remain unchanged. No new source calls, sampled outcomes, source actorproducer-workspace/private files, or changes to received manuscripts were made. The final source adds explicit parameter/confidence domains and says A is uniformly bounded in q at fixed w; the preceding fully read candidate had hash `a0e38162574d447a890cdadc2d6e29677b8c2a74b8ad9400e0eef24352afe444`. Those precision edits do not change the protocol or mathematical constants.

## 1. Exact scope and inherited physical interface

The reviewed theorem retains an exact compatible global logical Pauli algebra, a fixed common unitary/gauge source, independent reset calls, positive aggregate X/Z margins, known physical output coordinates, a supplied four-real-coordinate encoder family, and paid ordinary input/readout controls. It only relaxes physical locality of the true generators to state-weighted local reflection witnesses. Tau is a supplied bound, not a fit-based or holdout-based model test. A separate global identity-dominance promise is still required for the unrestricted noisy-source oracle comparison.

The received Bures instruments, rational Choi feasibility repair, finite backward spectral measurements, finite controlled-reflection compilation, active scalar encoder design, and whole-process operational-error convention are imported with their existing contracts. This review does not turn those imports into free elementary measurements or free efficient hardware synthesis.

## 2. Approximate coarse acquisition is justified

For a patch disjoint from the proxy interval, invariance of the partial trace under the local proxy Z reflection and true global anticommutation give

`2||X^J||_1 <= ||V X V - B X B||_1 <= 2 tau`.

Each term in the split `(V-B)XV + BX(V-B)` is bounded by tau through Hilbert–Schmidt Cauchy–Schwarz with R: R commutes with the true logical generators, `R<=rho`, `Tr R<=1`, and `Tr R(V-B)^2<=tau^2`. Neither locality of the true B nor a positive eigenvalue floor is used.

On the proxy interval, testing the contrast with its local X reflection gives `||X^I||_1 >= kappa-tau`. With `tau<=kappa/8`, the imported `kappa/8` statistical contrast error and `kappa/16` numerical score error produce the stated separated scores `11kappa/16` and `5kappa/16`. The threshold kappa/2 therefore returns an overlapping interval on the paid good event. Expansion by w-1 at each endpoint contains the true proxy interval and all fine width-w candidates. It does not locate the potentially nonlocal exact generator.

## 3. Both packing proofs and integer schedule pass

The standalone audit proves the local proxy extraction inequality

`ell0(D0) <= 2 delta_X + (3/4)delta_Z <= 11 tau^2/4`

against the ideal global logical extraction. Exact true support is unnecessary. The local proxy isometry is physical even when the two proxy reflections fail to anticommute.

The Bell-reference information proof is correct: individual local decoders are used separately on the same virtual premeasurement state; Fano/Araki–Lieb yield `I(R_i:J)>=2-2f`, product reference marginals and SSA give `sum I(R_i:J)<=I(R_S:J)`, and the output dimension bounds the latter by 2L. No simultaneous decoding or cloning is assumed.

The source's analytic guard is valid: for `u=11/256`, `f(u)<=u log2(3e/u)<8u=11/32<1/2`, because `e<3` and `2304/11<256`. Hence safe packing `s<=2L` follows from the already supplied `tau<=kappa/8<=1/8`. The independent one-axis proof gives the stronger `s[1-h2(tau^2/4)]<=L` by binary Fano, independent classical bits, and the Holevo dimension bound. It is explicitly a proof-only ensemble, not a learner oracle.

Therefore the stated integer choices are safe:

`W=min(n,3w-2)`, `C=min(q,4W-2)`,

`S=W+2(C-1)(W-1)`, `K=min(q,2S)`, `A=min(q,K^2)`.

They handle `q=1`, `w=1`, clipped boundaries, and repeated envelopes. A left-endpoint sweep achieves the actual overlap coloring. Exceeding the observable cap invokes a paid physical replacement, not rejection sampling or a retrospective membership certificate. The known envelopes and all actual candidate controls remain the objects being colored.

## 4. Approximate CPTP comparator and error constants pass

The true ideal decoder is not asserted to be a local SDP point. The feasible local proxy decoder supplies `r0<=11tau^2/4`. The source's four-state variance estimate is justified by

`(A-A0)^2 <= 2(A-B)^2 + 2(A0-B)^2`

and each decoder's `Tr rho(A_j-B_j)^2<=4ell0`. Summing the two signs and two axes gives the displayed `32(ell0+ell0_0)<=64(r+r0)/kappa`.

The pointwise Uhlmann comparison is uniform over fitted candidate observables and introduces no new independence claim. Starting from the source's square-root inequality, Young's inequality gives exactly

`r <= 2r0 + 39m/kappa + (3/2)zeta`

before its conservative rounding. With `m=kappa^2 eta/512`, `zeta<=m`, and the received tournament bound, the displayed coefficients follow:

`r_selected <= 11tau^2 + (53/128)kappa eta`,

`ell0_i <= 22tau^2/kappa + (53/64)eta`.

The finite sign-rounding step is also sound:

`4(sqrt(a)+sqrt(eta)/2)^2 <= 5a+5eta`

and `a<=4ell0_i` yield `delta_ji<=440tau^2/kappa+25eta`. The source correctly distinguishes these learned-reflection bounds from merely having a proxy witness. Exact rational/reference controls and paid finite synthesis survive every statistical history; no source eigenvalue floor is assumed.

## 5. Nonlocal ideal generators: the critical causal repair is present

The source deletes outside-cone blocks **only from the actual local receiver**. It then compares that restricted receiver with the ideal logical-SWAP subset on the same indices. This is the required repair; copying ideal support deletion from the exact-local theorem would be false.

The ideal subset contains the target label. Complete ideal swaps on distinct compatible logical factors commute and transfer its Bell half perfectly, despite being physically nonlocal proof devices. Every ideal elementary prefix leaves `rho tensor I_A/2^q` invariant. The full logical reference, gauge purifier and receiver-mixture purifiers remain retained in the proof; the actual learned prefix is not asserted to have that marginal.

Thus the elementary errors remain `delta_Z/2,delta_X/2,delta_Z/2`. Actual cone sizes and forward multiplicities are both at most K. The marginal hybrid followed by the commuting Bell-projector union bound gives

`ell0_joint <= 3 min(q,K^2) sum_i(delta_Zi+delta_Xi/2)`.

Substitution yields the displayed floor `1980qA tau^2/kappa` plus `(225/2)qA eta`. The separately retained global dominance and four-anchor quadratic domination multiply these terms by four, producing `7920qA tau^2/kappa+450qA eta`. At fixed w, A is uniformly bounded in q, not necessarily literally constant at the small-q minima. A nonzero per-logical structural tail still accumulates with q.

## 6. Physical pooled law, routing, finite cap and service conversion

Approximate locality does not alter the received paired-pool marginal argument. The source keeps two real reset calls per antithetic pair, independent anchors, disjoint physical patch reuse, an own-state-bank record firewall, and a union bound over individual estimators. Joint banks can remain correlated. All estimates freeze before ERM. Fresh comparison pools use iid current labels/calls and past-only contender adaptation; the antithetic state pool is not repurposed as an iid comparison stream.

Actual receiver controls remain local and paid: three controlled reflections per label, four Hadamards, q distinct freshly mixed ancillas, and restored/tracked routing. The imported end-block routing witness bounds routing by `2(n+q)` SWAPs per label and restores physical/output identities. Abstract color depth is not physical depth. Nonlocal ideal controls occur only in the mathematical comparison.

The source cap retains all coarse calls, fine pools, tournaments, fresh global encoder acquisition, and one final payload:

`2q c N0 + 4C c1 N_B + C(R_max-1)N_pair + N_count + 1`.

The `R_max=1` branch omits the otherwise undefined h/t/log/comparison formulas. Strictly positive beta allocations and `0<=nu<=epsilon/8` are explicit. Every failed or terminated history remains physical and all executed calls count. Whole-process finite compilation and routing discrepancy is not an extra uncharged failure event.

The new receiver is frozen before a fresh global known-Clifford ordinary test and encoder design; old marginal tests or holdouts are not recycled. The acquired scalar is the actual global Bell-risk scalar with its dimension-independent factor, under paid entangled-within-input preparation and global inverse-Clifford readout. The active encoder's relative comparison multiplies the decoder floor by `(1+gamma)`, as in the source. The remaining `450qA eta`, scalar additive penalty, statistical bad events and operational discrepancy fit inside epsilon under the imported allocations.

The theorem charges `qN_total` logical input-qubit uses, `nN_total` output exposures, the extensive number of local estimators, quantum storage and cross-copy controls. The fixed-w linear block-call statement is not a linear total-qubit-traffic statement. Increasing w to suppress a quasi-local tail must also increase the displayed `4^w` cost. Untwirled Bell loss is not a dimension-free diamond certificate; an optional discarded-key twirl remains a separately paid changed service. Equally informed conventional subsystem learning receives the same construction.

## 7. Evidence and disposition

The standalone deterministic check already passed exact rational extraction/nonlocality identities and 8,934 small interval families. It was not rerun for the two prose-domain precision edits; neither edit affects those checks. Its files remain bound separately and are included in the current receipt manifest.

No remaining mathematical or physical-controls correction is requested. This is a conditional theorem review under the explicit source, access, structural-tail and resource promises, not a source-family validation, hardware claim, or new sample-based demonstration.
