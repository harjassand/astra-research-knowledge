# Independent statistics audit of frozen on site recovery

28 October 2026. Reviewer `producer-workspace/audit_count_pilot_fresh`.

**PASS at the fixed on-site-algebra and uniform-contrast scope.** Source `ordinary_onsite_two_axis_frozen_memory_recovery_20261028.md`, SHA-256 `7df4d169cc544b79456e7410da7ac3ec991482311a0d3831569efc573455dd53`. The earlier `c2691ea45067c5dda9d3ee19b5c94ccfaa4de8d23d46f01f1bbbf69ecb32feba` source is preserved. Its sole clarification defines all fine calls and physical replacement costs on missing/flagged/nonunique coarse matchings. No proof, rate or confidence formula changed.

This review covers actual record statistics, proper-rotation curvature, finite rational fitting, the record-good-event transfer to physically changed later memory and complete resource arithmetic. It is a deterministic train/freeze theorem for a narrower source family, not a private-terminal restatement of the wider-code theorem. The supplied fixed on-site algebra, positive conditional X/Z CP contrasts, complete current-port privacy and implementation interfaces remain assumptions. Full-CPTP optimality additionally needs the separate global CP-dominance promise. No source acquisition, random sampling, new pilot, hardware result or superiority to a conventional learner is claimed.

## 1 On site structure and actual fixed banks

Distinct independent logical qubit algebras cannot act on the same physical two-dimensional factor. For each matched site the true X/Z reflections anticommute and determine the correctly oriented Y reflection. A local SU(2) conjugation therefore realizes its SO(3) frame. After the matching permutation and these local inverse conjugations, the source encoding commutes with the complete logical matrix algebra, so it acts only on the spectator factor. This is stronger than a statement about two marginal expectations: it makes the eventual fitted receiver an actual product of local logical unitary errors, with all spectators discarded.

The w=1 specialization of the received martingale localization theorem uses d0=2, M0=n and beta0=beta/2. It gives precisely

`L0=ceil log2(8qn/beta)`, `N0=ceil(3072 L0/kappa^2)`.

A true site has signed contrast norm at least kappa, and every other site has exactly zero signed conditional mean. The prior theorem's kappa/8 trace-norm error and kappa/16 finite-score error therefore distinguish the true site uniquely at threshold kappa/2. Simultaneous confidence is at least 1-beta/2. It is not a conclusion from a successful guard alone.

All fine inputs and product measurements have a fixed schedule on every coarse history, including failures. The final clarification uses predetermined placeholder indices for unused fine accumulators and never deploys those fits; the future receiver instead resets q predetermined distinct output sites for a physical replacement. Thus undefined matching is neither an uncharged termination nor a postselected data set. All N1 fine calls and any fallback resets are paid.

## 2 Conditional two column estimator

Condition on the entire prior record, including the coarse matching. On a correct coarse history the matched output's Bloch response to its own input axis/sign is s lambda_j R e_j after averaging other fresh inputs. Both relevant contrasts are at least kappa for every resulting conditional quantum memory state. The fixed R does not depend on that history.

For each own input-axis and physical measurement-axis pair, the selection probability is (1/2)(1/3). The conditional mean of the actual measured sign b is s lambda_j R_aj. Hence

`F=6 s b e_a e_j^T`, `E[F | past]=R diag(lambda_X,0,lambda_Z)`.

Every individual F has Frobenius norm exactly 6. Its Y column is zero by the protocol, not because Y noise is assumed positive or estimated. Each centered increment has conditional squared Frobenius moment `36-||M_t||_F^2<=36`. Martingale orthogonality across different times gives

`E||N_i||_F^2<=36/N1`.

This remains true when the predictable contrasts and the memory state vary with the past. In particular the average contrast Dbar is random, but the error `Mhat-R Dbar` is still the average of conditional mean-zero increments. No fixed-channel iid assumption is being hidden in that centering.

All q learners may reuse the SAME full product-measurement record. Their current outcomes, source error labels and future histories may be correlated. The proof only conditions on prior records and uses marginal conditional means, never conditional independence of current learners. The exact fixture includes correlated two-logical Pauli errors and a non-reset weak quantum instrument with branch-dependent noise and different conditional memory populations.

## 3 Finite simultaneous confidence

A coordinate of F lies in [-6,6]. Conditional Hoeffding's lemma applied after subtracting its conditional mean has range length 12, giving mgf at most `exp(18 z^2)`. Iteration over the filtration and optimization yields

`Pr(|N_aj|>=t)<=2 exp[-N1 t^2/72]`.

There are six nonzero-coordinate positions per logical learner. Setting `t^2=kappa^2 epsilon/(48q)` gives `||N_i||_F^2<=kappa^2 epsilon/(8q)` whenever all coordinates satisfy this threshold. The exponent is `N1 kappa^2 epsilon/(3456q)`. The specified N1 makes it at least `(32/27)L1`, where `L1=ceil log2(24q/beta)`. Since log2 x>=ln x for x>=1, a union over 6q two-sided tails costs at most beta/2.

This argument may be conditioned on any complete correct coarse history because the fine bank is fresh and the contrast promise is uniform over its conditional memory. Integrating that conditional statement and adding coarse failure gives a joint ideal good-event probability at least 1-beta. No independence between coarse and fine errors, or between learners, is needed. The confidence event is unconditional over retained records, not a posterior inference after accepting a particular record.

## 4 Proper rotation curvature and exact Bell loss

For a proper rotation Q represented by quaternion (u0,ux,uy,uz),

`1-Q_YY=2(ux^2+uz^2)`,

`(1-Q_XX)+(1-Q_ZZ)=2(ux^2+uz^2+2uy^2)`.

Thus the unobserved Y error is controlled by the two observed axes. For D=diag(lambda_X,0,lambda_Z) with both nonzero entries at least kappa, and Q=R^T Rhat,

`<R-Rhat,RD> >=(kappa/4)||Rhat-R||_F^2`.

The proof does not assert the analogous result for O(3). Indeed diag(1,-1,1) is an improper matrix with zero two-axis objective gap but nonzero distance from identity. That exact failure is preserved in our fixture; proper rotations are enforced on every record, not after a successful determinant check.

A certified objective gap delta and Cauchy–Schwarz give

`(kappa/4)d_R^2<=||N||_F d_R+delta`.

Young's inequality `||N|| d_R<=(kappa/8)d_R^2+2||N||^2/kappa` implies

`d_R^2<=16||N||^2/kappa^2+8delta/kappa`.

For the corresponding actual inverse single-qubit unitary, its virtual Bell loss is exactly `d_R^2/8`. This follows either from the relative unit quaternion or from the Bloch rotation angle; global SU(2) signs do not change the channel. Hence

`ell_i<=2||N_i||_F^2/kappa^2+delta/kappa<=9epsilon/(32q)`

at the stated noise threshold and delta=kappa epsilon/(32q). No Y contrast, gauge eigenvalue floor or empirical eigenvalue separation enters.

## 5 Finite exactly physical fitting

I independently read the author-hosted Horn paper's proper-quaternion eigenproblem formulation. It is established conventional fitting machinery, not a new optimization principle. [Horn primary paper](https://people.csail.mit.edu/bkph/papers/Absolute_Orientation_Scanned.pdf). The separate primary-import note records the limited attribution and read. Every sign in K(M) was independently checked against the manuscript's particular convention `V(u)=u0 I-i u·sigma` and the Frobenius objective; these conventions must not be assumed interchangeable without that check.

For every unit u, `<R(u),M>=u^T K(M)u`. Therefore `||K(M)||op<=sqrt(3)||M||F`, and every empirical M has norm at most 6. Scaling by K/48+I/4 is consequently inside [0,I/2] even on arbitrarily bad records.

The received rational Jacobi primitive can be specialized to real two-coordinate rotations. A rational stereographic parameter t gives exactly rational `c=(1-t^2)/(1+t^2)` and `s=2t/(1+t^2)`, with c^2+s^2=1. No separately normalized floating vector is used. To make the unscaled K residual at most delta/2, it suffices to run the imported primitive with zeta=delta/24: its scaled residual zeta/4 becomes 12zeta after multiplying by 48.

Let D be the rational diagonal of Q^T KQ and choose a column of the exactly orthogonal Q with maximum diagonal label. Its Rayleigh quotient equals that label exactly. Weyl's norm bound gives `lambda_max(K)<=max diag(D)+delta/2`, so this rational unit quaternion meets the requested objective gap with slack. Its SU(2) matrix is exactly unitary and determinant one. Zero matrices, repeated top eigenvalues, rank-one empirical signals and bad fits remain physical. The finite primitive is gap-free; a possible true-signal gap is neither supplied nor used as an empirical safeguard.

Matrix size is fixed at four. The inputs are rational count averages with logarithmic N1 entry length, and the accuracy cost is polynomial in their bit length and log(1/delta). A fresh fit starts from that empirical mean, so no online product of denominators accumulates across source calls. Known one-qubit reference rotations are then compiled within the stated uniform service accuracy. Our four deterministic rational-Jacobi fixtures actually execute the finite step and certify each rotation, energy decrease, final backward residual, Rayleigh gap and SU(2) control exactly. Floating two-by-two angles only propose rational stereographic parameters; all acceptance checks are exact rational arithmetic. No physical data were sampled.

## 6 Why freezing transfers to later actual memory here

For a correctly acquired matching, the nominal receiver is the product of local inverse rotations on distinct genuine logical factors and a trace over spectators. On the virtual identity channel its logical error is a product unitary, irrespective of the source gauge state or its correlations with retained memory. Thus its FULL q-input Choi state has Bell loss

`ell0_joint=1-product_i(1-ell_i)<=sum_i ell_i<=9epsilon/32`.

This factorization is a property of the actual virtual receiver channel, not an assumption that the noisy source's marginal fidelities are independent. It includes arbitrary entanglement across the logical payload and reference in the usual channel/Choi formulation.

At any later actual conditional memory state, the emitted Pauli/gauge blocks still obey the source promise. The already received Bell-block comparison then bounds the fitted receiver's excess by this same state-independent ell0_joint. Under global CP dominance, ideal logical extraction is the strongest full-CPTP oracle for that SAME conditional memory. The future state can have changed completely; the common on-site algebra must not have drifted.

The useful good event should be defined as a set of retained records: the computed matching is correct and the resulting fixed rotations obey the true rotation-error bound. The event need not mention the latent Dbar or later memory. The fine-noise concentration event proves this record event has ideal probability at least 1-beta, but is not itself used as a conditional posterior or as a service-time assumption. The retained record/program must determine the nominal fit being implemented.

A calibration-record total-variation discrepancy at most nu_cal therefore changes the probability of that same record event by at most nu_cal. Every physically realized good record still gives the nominal uniform-memory bound, including for memory altered by imperfect calibration or intervening source dynamics. A separate whole-q-input half-diamond service error nu_svc, uniform for the selected nominal receiver at the physically actual pre-call memory, contributes at most nu_svc to its Bell loss. Hence

`actual mean excess<=9epsilon/32+beta+nu_cal+nu_svc`.

With beta<=epsilon/8 and nu_cal+nu_svc<=epsilon/4 this is at most 21epsilon/32<epsilon. For arbitrary beta the preceding explicit bound, not an epsilon-only claim, is the conclusion. Bad records are debited once and are never acceptance-conditioned away.

This transfer is not licensed for generic prequential comparators. It works because a record-defined rotation-error event is uniform over ALL future source memories. Here the comparator really is evaluated on the physically actual later occupation; no counterfactual oracle-history path is substituted. Full payload/reference independence is imposed only at the chosen future service boundary (or conditionally on the allowed classical record), not by presuming that a payload was safely stored through training. One arbitrary later simultaneous service is covered; repeated temporal payloads with shared memory require a separate analysis.

## 7 Finite call bit and control ledger

The worst-case source use is exactly the two fixed calibration banks plus one future payload: N0+N1+1. The block-call scale is `O(kappa^-2 log(qn/beta)+q kappa^-2 epsilon^-1 log(q/beta))`. Every calibration block still prepares q physical logical inputs and performs n local readouts. Thus near-linear q block count does not imply linear total qubit traffic or logarithmic readout cost.

For B=N0+N1, output-axis two-bit rejection has per-draw exhaustion probability 4^-r. At most nB draws and `r=ceil log2(4nB/nu_rng)` yield total failure at most nu_rng. Its prescribed physical fallback and probability belong inside nu_cal, not in a second free error budget. The ideal statistical law is coupled to the finite sampler until exhaustion; it is not conditioned on eventual success.

The stated bit cap `qN0+2qN1+2nB r` correctly pays coarse signs, fine own axes/signs and all output-axis trials. Optional service frames cost an additional 2q bits. There is no private terminal-time sampler or calibration quantum-reference bank. Local accumulators, six fine real coordinates per logical, optional raw record retention, known-matrix processing and every preparation/readout control are paid.

The nominal decoder consists of q single-qubit inverse rotations, no mixed extraction ancillas or controlled multi-qubit reflections. Unknown site matching is learned rather than supplied. Keeping outputs at learned sites requires no implicit endpoint movement; a required fixed layout pays a routing permutation, with O(nq) adjacent SWAPs a conservative cap. Replacement histories require q physical output resets. Any actual input storage during the one service, routing, source interface and compiled controls must fit the uniform service discrepancy. These implementation bounds are assumed interfaces, not certified by exact mathematical fixtures.

Optional private Pauli framing is applied to the whole nominal q-input service, then averaged. Its half-diamond distance equals global Bell loss only for that averaged Pauli channel. The ideal extraction's Pauli channel attains the smallest Bell loss and therefore the smallest possible half-diamond loss under the global dominance promise; any channel's half-diamond loss is at least its Bell-test failure. Imperfect actual frames use the separate complete service norm and triangle inequality. No untwirled or key-conditioned dimension-free diamond claim follows.

## 8 Independent evidence and receiving scope

The exact check enumerates 6,912 three-site Born terms for two conditional weak-instrument memory-population cases, including unknown swapped logical matching, local complex rotations and correlated two-logical Pauli errors. Its source instrument has a component with Y contrast -1/5, while both required X/Z CP contrasts remain positive. It checks 70 quaternion K identities, 50 proper two-axis curvature/Bell-loss cases, four finite exactly rational Jacobi fits including zero and repeated-top-eigenvalue inputs, nine adaptive scalar martingale histories, three record-TV transfer cases and 36 complete integer confidence/call/randomness budgets. It also preserves the improper-rotation counterexample.

The first full check passed all mathematical assertions and then reached its final frozen-source guard after the author had incorporated the requested total-fallback clarification. That guard stopped as intended; no result JSON was written. The earlier script is preserved. Updating only the source hash and rerunning identical mathematics produced the passing final result. No source data or random samples were generated, and author files were not edited by this reviewer.

Stable general-source main/statistics and proper-Jacobi receipts are used only for their named components; all 39 direct imported manifest entries were reverified. No forthcoming on-site main receipt is imported, preventing a dependency cycle. The equally informed conventional learner can use the identical estimator and controls. This result concerns a restricted on-site noisily rotated subsystem, not generic redundant-code discovery, arbitrary changing encodings or a demonstrated performance advantage.
