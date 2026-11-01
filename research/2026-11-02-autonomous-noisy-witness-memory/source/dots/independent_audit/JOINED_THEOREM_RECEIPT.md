# Independent whole-join receipt: Tanner witness memory

2026-11-01. **Mathematical PASS for the stated abstract graph-local, encoded-input/decoded-output theorem, conditional on the independently received LZ-family controller facts.** No new counterexample or missing algebraic transfer was found. This is not a practical hardware, Euclidean-locality, efficient-readout, or novelty certification.

## Frozen inputs actually read

- Joined author theorem: `JOINED_TANNER_MEMORY_DRAFT.md`, SHA256 6bbb3700e00ae00bfcd88776b8e032980a6f73de7fcd8c01cd5c1e7b2bee517b.
- Instance author's `TANNER_WITNESS_DOWNHILL_CONTROLLER.md`, SHA256 9f04d241d3dfd5d62fe3457f98c550d5edfc6644e75261aa3435357759f619ef; read the construction, basin, local-branch, and ground-subsystem passages relevant to the join.
- Separate instance audit `INDEPENDENT_RECEIPT.md`, SHA256 251379281f2dc7f636c452a17afa0a53b32b1295ac1c261c54e96e882b1b13ae, and its companion `ALGEBRA_RECEIPT.md`.
- My preceding abstract audit and exact two-step-boundary counterexample/repair.

This review independently checks the composition. It does not independently reprove the imported LZ expansion theorem, nor promote the instance audit into a certified finite hardware example. Its restriction to the specified sufficiently-large-fixed-Delta robust primal/dual quantum Tanner family is essential.

## 1. Joint syndrome and arbitrary gauge states

The imported Clifford calculation shows that, after U†, compatibility and copy-agreement labels are functions only of original stabilizer eigenvalues and auxiliary pair-disagreement eigenvalues. They are central stabilizer-syndrome data, not free pair-gauge values. The ground subspace is the entire enlarged stabilizer zero-syndrome sector U(C_original tensor K_aux), with protected logical information and coherent auxiliary gauge degrees of freedom.

For the actual controller, repair tie-breaking can depend only on compatibility discrepancy, and reduction tie-breaking only on local copy disagreement. Thus the required branch projectors can indeed be functions of these central joint labels. Using finer raw gauge values is not necessary to implement the specified selection rule. This matters: the joined theorem's central-projector convention is sufficient for its all-gauge statement, rather than an assumption that witnesses are classical.

Every valid joint syndrome has Pauli representatives from ground. A chosen representative maps the entire ground sector, including all gauge states, onto its syndrome sector. Consequently a pointwise enabled-rate/drift inequality depending only on those labels extends to an operator inequality on the whole sector and to arbitrary coherent superpositions. The imported basin premise applies to a label whenever ONE Pauli representative has sufficiently small weight; it need not be the unknown actual error history.

## 2. Minimum syndrome weight and the barrier

The joined definition

    r(s)=minimum weight of ANY enlarged-system Pauli carrying ground syndrome to s

is appropriate and avoids an unnecessary dependence on an actual logical/gauge history. It is a minimum SYNDROME weight, not a claim that all errors with syndrome s have the same logical effect.

Suppose 0<r(s)<=R_n/2 and W(s)<r(s)/b_c. At each positive-W label in the admitted basin, the positive extensive drift supplies at least one genuine downhill branch. Choose such branches successively. Each lowers the integer-valued W by at least one, so termination takes at most W(s)<r(s)/b_c steps. Before termination the accumulated correction Pauli has weight <r(s); composing it with an initial minimum representative gives a representative of every intermediate syndrome of weight <2r(s)<=R_n. Thus every needed subsequent downhill step remains in the STRICT imported basin. There is no circular appeal to drift outside the basin.

At termination W=0 is ground syndrome. If C is the accumulated correction, then C† itself is a Pauli representative of the initial syndrome, of weight <r(s), a contradiction. No logical-distance argument is required for this minimum-ANY-syndrome formulation; the contradiction is stronger and remains valid for every gauge state. Hence W(s)>=r(s)/b_c throughout r(s)<=R_n/2. The r=0 case is immediate from nonnegativity.

For every admitted Pauli T of weight <=w, |r(s^T)-r(s)|<=w by composing representatives in either direction. Start at ground in the component W<B_n, where B_n=R_n/(8b_c). If a path first reaches r>=R_n/4, its previous radius is <R_n/4 and w<R_n/4, so this first crossing has r<R_n/2. The preceding barrier inequality gives W>=R_n/(4b_c)>B_n, contradiction. Therefore EVERY label in the connected below-cutoff component has r<R_n/4. Disconnected low-potential labels are not silently declared correctable.

## 3. Protected flatness from dressed distance

Choose a minimum representative E_s for each label in that component. For an admitted edge T:s→t,

    E_t† T E_s

has zero enlarged syndrome and weight <R_n/2+w. With R_n<=d_protected/8 and w<R_n/4 this is safely below d_protected. A zero-syndrome Pauli below dressed protected distance lies in the gauge group, up to phase, rather than implementing a nontrivial protected logical Pauli. This is an operator statement on the whole ground subsystem, not an assertion about one gauge basis vector.

Thus canonical decoding by E_s makes every compressed admitted Pauli act as identity on protected information tensor a syndrome/gauge operation. The same holds for the joint-syndrome branch projectors. This independently earns the flat-component premise required by the abstract coherent-memory proof. The representatives need not be physically prepared or computed by the autonomous controller.

The common admitted alphabet must include every Pauli component of full conditional jumps, including their conditioning supports, as well as all physical and witness perturbations. The join explicitly distinguishes its bounded full-support w from the smaller b_c used solely for the descent sequence. Both are fixed constants for fixed Delta.

## 4. Normalized local channel and ideal/reflected agreement

At each vertex/type the branch projectors are mutually orthogonal. Complete them with a no-update branch Pi_0, and define Phi_v with Kraus operators T_ell Pi_ell (T_0=I). Their adjoint products sum to I, so Phi_v is CPTP and

    kappa(Phi_v-id)=sum_ell D[sqrt(kappa) T_ell Pi_ell].

This is one rate-kappa attempt channel per vertex/type, not a full attempt clock for every truth-table possibility. The active branches supply precisely the rate counted by the extensive-move bound. The no-update branch may dephase syndrome coherences, but has zero F drift, is protected-logical trivial, and does not spoil the argument.

All branches remain in the low-potential component from an input in that component: active branches descend and inactive branches do not move. Their L†L=kappa Pi_ell are diagonal and commute with Q. Hence ideal original and reflected generators agree exactly on Q-supported states, including off-diagonal syndrome/gauge coherences. This addresses the fact that not literally every Kraus branch is strictly downhill after completing Phi_v to a channel.

## 5. Constants and coherent-noise consumer

The imported drift constant is kappa(1-exp(-a))/K, with K=8Delta^4+2Delta^2+1. Using theta=beta/2 gives

    g=kappa theta(1-exp(-a))/K,
    u=2h sinh(ab/2)+gamma(exp(ab)-1).

Under u<=g/2, the conservative reflected exponential-moment constant 1+g/(g-u) is <=3. The corrected TWO-step shell is W>=B_n-2b. The independently proved joint-state Duhamel bound therefore becomes exactly

    ||rho_actual(T)-rho_ref(T)||_1
      <=sqrt(3) n(2h+4gamma) T exp(ab) exp(-a beta n/4).

The exp(ab) factor is the two-step-shell margin, not an omitted dimension-dependent cost. This bound uses true operator norms and trace-norm contractivity, remains valid with arbitrary reference systems, and does not posit a Gibbs state or replace coherent noise by stochastic jumps.

Fixed positive noise ratios satisfying the inequality exist mathematically: as a decreases to zero, u/g tends to Kb(h+gamma)/(kappa theta). Choosing the latter sufficiently below 1/2 leaves a small positive a satisfying the displayed condition. This proves existence of a constant-ratio regime, not a useful numerical threshold.

For T_n=exp(a beta n/8), the upper bound is a fixed prefactor times n exp(-a beta n/8), which tends to zero. All parameters entering that exponent remain fixed with n in the stated family. No n-growing correction rate was inserted.

## 6. Original n, enlarged size, and operational scope

All basin and noise formulas use ORIGINAL data-qubit count n. There are 5n physical data/witness qubits; per-enlarged-qubit perturbation strengths must therefore include the factor five and the finite Pauli-expansion/support incidence factors in h and gamma. Rewriting the exponent in total size N=5n only changes its constant. Original positive protected rate becomes a still-positive rate divided by five; the two auxiliary equality-pair gauge qubits per original site do not count as protected information.

The initial state must already lie in the encoded W=0 subsystem. Arbitrary logical/reference entanglement and arbitrary coherent gauge states are covered. Preparing this encoded state is not supplied by the lifetime proof.

The terminal canonical syndrome/frame decoder is a mathematical CPTP recovery map, extended arbitrarily outside the protected component. The trace-norm bound survives it. The proof does not establish an efficient minimum-representative algorithm, noisy final-decoder implementation, or a free fault-tolerant readout. These are genuine charged operations, not part of the autonomous storage interval proved here.

With a fixed bath input independent of the unknown logical state, the result has the usual restricted-code channel/diamond interpretation. Correlated initial baths still admit the stated joint-state and decoded-output comparison, but do not automatically define a system-only channel. Only well-defined actual propagators and the specified bounded local coupling model are covered. Unmodeled apparatus, arbitrary controller-jump miscalibration, and unknown reset services are not included merely by naming them noise.

## Acceptance and stop boundary

The whole mathematical transfer passes: imported local witness drift plus minimum-syndrome confinement and protected dressed distance supplies the flat component needed by the corrected coherent boundary argument. The earlier one-step-shell error remains preserved and is NOT reused.

The useful-hardware gate remains failed/unearned. This is a bounded-degree expander-interaction result with enormous fixed support/truth-table and threshold constants. No fixed-density Euclidean routing, native few-body realization, experimentally calibrated device, or superiority over a matched active Tanner memory is certified. Historical novelty is also outside this receipt.

The requested whole-join audit is closed. No additional formal polishing or experimental claim is needed to state this qualified abstract result.
