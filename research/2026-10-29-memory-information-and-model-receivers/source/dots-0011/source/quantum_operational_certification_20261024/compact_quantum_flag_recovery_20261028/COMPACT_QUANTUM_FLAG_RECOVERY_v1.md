# Compact recovery from Bell labels and a small quantum flag

28 October2026. New complete scoped construction; independent review pending. This removes the supplied tree and known-feature hypotheses from the preceding quantum-flag learner. The governing resource is the accessible flag dimension and a real Bell-label acquisition interface. Standard matrix concentration, state discrimination, POVM geometry and Pauli twirling are credited mechanisms; historical novelty or superiority to an equally informed conventional implementation is not claimed.

## 1. Two carefully separated source/comparator scopes

Let L contain n data qubits, d=2^n, and let G be an accessible r-dimensional flag register. The source is a fixed CPTP map N:L->L tensor G. Complete calls are independent and use the same source; each call may itself contain arbitrarily correlated noise across all n qubits. Arbitrary returning memory BETWEEN training and service calls is not covered.

For a general N define its normalized Choi state J_N and its diagonal Bell blocks

    sigma_x=(<Phi_x| tensor I_G) J_N (|Phi_x> tensor I_G),
    sigma_x>=0, sum_x Tr sigma_x=1,

where x ranges over the COMPLETE4^n Pauli basis and Phi_x=(I tensor P_x)Phi_d. These are physical subnormalized flag states obtained by a Bell measurement, not a reconstructed environment or a declared microscopic error unraveling.

A recovery in the class C measures G with a POVM {M_x}, then applies correction P_x to the returned L. For EVERY source N, including coherent off-diagonal Bell blocks,

    F_e(R_M N)=sum_x Tr(M_x sigma_x).                       (1)

This follows by moving the final Bell-fidelity projector backward through the conditional Pauli and flag instrument. Thus the theorem below learns the optimum within C for arbitrary N.

For the special Pauli-plus-flag source

    N(rho)=sum_x P_x rho P_x tensor sigma_x,                (2)

the class C attains the FULL-CPTP recovery optimum. Expand any recovery Kraus map in the full Pauli basis as K_b=sum_x P_x tensor <v_(b,x)|. Partial trace of the TP identity gives M_x=sum_b |v_(b,x)><v_(b,x)| with sum_x M_x=I_G. The Kraus fidelity formula yields(1); conversely every POVM implements a physical recovery. This is a collective d-dimensional Bell objective, not independent local oracles.

For a promised X-only source, extend sigma_x by zero outside its allowed subgroup. The full Kraus expansion is still over4^n Paulis; zero-label effects can be reassigned to any allowed correction without losing score. Ordinary bit-flip probes below then need only the allowed2^n labels. This source restriction is not inferred from those probes.

## 2. Actual acquisition, with its quantum-memory bill

For a general N, each training call prepares n Bell pairs, retains n reference halves, sends the data halves through N, and performs n two-qubit Bell measurements on data/reference pairs. The output is a label x and a flag in unnormalized state sigma_x. Measure the flag after this Bell readout with the stated tomography instrument. No unknown deployment payload is ever used as a sacrificed probe.

For a promised X-only Pauli-plus-flag source, ordinary |0>^n preparation and Z readout reveal x while leaving G available. This special interface needs no entangled reference halves. It does NOT reveal generic phase errors or coherent Bell labels.

Take r=2^g for the explicit flag readout construction. Draw a g-qubit Pauli W uniformly from its r^2 possibilities, measure its nonidentity factors locally, and record parity b; for W=I set b=1. For each possible label x define the actual single-call Hermitian estimator

    Y_x=r 1[label=x] b W,   E Y_x=sigma_x.

The unknown matrices are estimated by Shat_x=N^-1 sum_t Y_(t,x). Only observed labels need storage. Unobserved labels have Shat_x=0 exactly. No positivity projection or normalization is imposed: these are known Hermitian objective coefficients, not states to be physically prepared.

The estimates satisfy ||Y_x||<=r, ||sigma_x||<=1, centered norm<=2r, and

    E[(Y_x-sigma_x)^2]=r^2 p_x I-sigma_x^2 <=r^2 I,
    p_x=Tr sigma_x.

Applying the bounded self-adjoint matrix Bernstein theorem to both signs and union bounding A allowed labels gives

 Pr[max_x ||Shat_x-sigma_x||op>delta]
    <=2 A r exp[-N delta^2/(2r^2+(4r/3)delta)].             (3)

The primary theorem is Tropp, *User-Friendly Tail Bounds for Sums of Random Matrices*, arXiv1004.4389, Theorem6.1(ii), primary PDF pp23–24 inspected28October2026: https://tropp.caltech.edu/papers/Tro11-User-Friendly-preprint.pdf . All variance/range substitutions are displayed above. Independence is between complete source calls, not between label estimators.

For qubit flags the preceding pilot used its sharper explicit scalar-component concentration instead of(3). Both are legitimate acquisition interfaces; their constants must not be mixed.

## 3. One dummy label eliminates exponential enumeration

Let S be the labels actually observed. If any allowed label is unobserved, choose ONE such label x0 and include it with coefficient0. A first unseen word can be found by a hash/trie or scanning at most |S|+1 lexicographic labels; this costs polynomial time in N and n, not4^n enumeration. If every allowed label has been observed, add no dummy.

Solve the KNOWN finite SDP

    maximize sum_(x in S union {x0}) Tr(M_x Shat_x),
    M_x>=0, sum_x M_x=I_G.                                (4)

The objective coefficients may be indefinite. The feasible POVMs are nevertheless compact and physically valid. Every full-alphabet POVM has the same empirical objective after all unobserved-label effects are merged into x0, because all their coefficients are0. Hence(4) is exactly the full empirical optimum, not a truncated-distribution approximation. If no dummy exists, all labels are already represented.

The known matrix dimension is r, with at most N+1 outcomes and rational data. Strict feasible effects I/(N+1) and an explicit bounded scalar dual are available. Standard finite-precision SDP methods can produce a primal POVM and a dual matrix with a certified objective gap; precision, arithmetic, and physical synthesis are paid. This does not assume a source-dependent recovery oracle. A heuristic candidate can instead pass a direct primal/dual check, as the executed instance does.

## 4. Uniform regret does not grow with the number of labels

On the event max_x ||Shat_x-sigma_x||op<=delta, EVERY complete POVM satisfies

 |sum_x Tr[M_x(Shat_x-sigma_x)]|
     <=delta sum_x Tr M_x =r delta.                       (5)

If the returned feasible POVM is eta-optimal in(4), its actual recovery obeys

    max_(R in C) F_e(RN)-F_e(Rhat N) <=2r delta+eta.        (6)

Under(2) this is the FULL-CPTP oracle regret. It holds for data-selected candidates and zero-probability labels, since the event is simultaneous. No known feature, tree, state rank, lower probability floor or minimum oracle gap is required. For desired additive error epsilon and eta<=epsilon/2, choose delta=epsilon/(4r). Equation(3) gives

    N=O(r^4 epsilon^-2 [n+log(r/beta)])

for the displayed Pauli flag readout. Thus at fixed flag dimension the source-call cost is polynomial in the number of logical qubits. The theorem bounds ADDITIVE regret; it does not promise high fidelity when the source's best available recovery is poor.

PSD clipping would also work with a larger perturbation allowance, but is unnecessary. The dummy label is an actual allowed Pauli correction, not a fictitious zero-score physical outcome. Its true sigma may be nonzero; equation(5) already charges it on the uniform event.

## 5. At most r^2 physical correction outcomes

Any feasible finite POVM with more than r^2 nonzero effects has a real linear dependence sum_i c_i M_i=0, since Hermitian r×r matrices form an r^2-dimensional real vector space. Its coefficients have both signs because every nonzero effect has positive trace. Replace M_i by(1+t c_i)M_i over the maximal interval on which all factors remain nonnegative. Both endpoints preserve positivity and the sum I; at least one effect vanishes at either endpoint. The empirical objective is affine in t, so choose the endpoint whose value does not decrease. Repeat until at most r^2 effects remain.

Equivalently one can solve a finite weight LP against the original effects and take a basic optimum, avoiding uncontrolled intermediate rational-denominator growth. This pruning never worsens the certified empirical objective, so it preserves(6). It requires no structure in sigma_x.

Compile the retained effects by the explicit Naimark isometry

    V|psi>=sum_(i=1)^m |i> tensor sqrt(M_i)|psi>, m<=r^2.

Because sum M_i=I, V is an isometry. Complete its known columns to a unitary, implement it on G and a fresh outcome ancilla, measure the latter, and conditionally apply the selected n-qubit Pauli word. The expanded Hilbert space has dimension at most r^3; known matrix-function/synthesis precision is paid by eta or a separate whole-recovery implementation error. At fixed r this quantum control acts only on a constant-size flag plus the n local correction gates. Data are not passed through an arbitrary exponentially large recovery unitary. The generic compiler is a mathematical construction; only the rank-one qubit projector is concretely instantiated below.

The r^2 support count can be necessary. For r=2, take four equiprobable tetrahedral pure flags tau_i and four Pauli labels. Effects M_i=tau_i/2 attain score1/2 with dual Y=I/4. Equality forces each effect to be supported on its tau_i, and their affine independence forces all four effects. Thus a universal reduction to r rather than r^2 outcomes is false.

## 6. A sharp information-resource ceiling

Write sigma_x=p_x tau_x for p_x>0. For any POVM let y_x=Tr(M_x tau_x). Then0<=y_x<=1 and sum_x y_x<=sum_x Tr M_x=r. Therefore

    max_(R in C) F_e(RN) <= sum of the r largest p_x.      (7)

This is the full-CPTP ceiling for(2). It is sharp when the top r labels have mutually orthogonal flags and the corresponding orthogonal measurement returns them. A small flag cannot recover a diffuse exponential catalogue of full-payload Pauli errors. The learning theorem does not evade this obstruction, does not imply a universal quantum memory threshold, and does not optimize a redundant code or rate.

## 7. Exact same-data certificate, with no feature assumption

`certify_existing_measurement_v2.py` reads the already generated4,194,304 training records from the label-observed pilot, using their sufficient integer counts. It chooses the TWO GLOBAL highest-count words, numerically orders them, and uses the saved rational projective measurement. No root feature or chain model is used by this certificate.

There are53 observed words and one explicit unseen dummy00000101 (integer5). The code constructs a rational dual Y from the two candidate coefficients using

    Y_exact=(Shat_0+Shat_255+|Shat_0-Shat_255|)/2,

encloses its square root by exact integer arithmetic, and adds a rigorously bounded scalar slack. Exact2×2 principal-minor checks show Y>=Shat_x for all53 observed labels and Y>=0 for the dummy. The candidate effects are exactly positive and sumI. Their primal/dual gap is below3.672e-14. Thus the measured two-outcome decoder is a certified global empirical optimizer even when every observed word's flag is treated as unrelated.

The received component event has delta_p=.002 and delta_r=.005. Its operator-norm implication is

    delta<=(delta_p+sqrt(3)delta_r)/2,

so(6), at r=2, gives full-CPTP oracle regret at most .021320600001, with the SAME training failure bound below4.106e-5. The previous known-feature bound was .042641200001. This is a stronger conclusion from the same records, not a new independent experiment.

The actual implemented measurement and fresh65536-trial validation are unchanged:2201 failures passed the preset F_e>=.95 target for that bit-flip source. The posthoc actual score .9675410648 and oracle .9675416846 remain diagnostics; the no-flag full-CPTP oracle is .4965104825. Total original source calls remain4,259,840, corresponding to34,078,720 data-qubit exposures and one emitted flag per call. This analysis uses ZERO new source calls. The exact source/POVM controls are trusted; no hardware-control robustness is imported.

Version1 of the same-data check stopped before issuing a certificate because top-count ordering disagreed with the preserved measurement's numerical label ordering. Version2 fixes only that internal relabeling. Original data, measurement, statistical bounds and target are unchanged; the failed version is preserved.

## 8. Optional actual twirl and the coherent-frame bridge

A private outer Pauli twirl of an actual source N creates the physical source(2): choose an independent2n-bit key z, apply P_z before N and P_z on its data output afterward, then retire the key. The flag is retained. This dephases the source Choi state in the Bell basis and preserves Bell fidelity with identity/flag discard. It costs fresh randomness and both physical Pauli controls. Retaining/exposing the key or noisy controls changes the interface; exact formulas do not transfer silently.

Twirling can greatly reduce the ORIGINAL source's unconstrained optimal recovery. For N=Ad_(H^tensor n), the original inverse recovers perfectly, but its twirl has2^n equal Pauli labels. With r=1 its full-CPTP oracle is2^-n. Therefore this work does not claim globally optimal recovery of arbitrary coherent noise by blindly twirling it.

A positive composition avoids that error. Freeze ANY actually compiled coherent preconditioner C, with the flag retained or its final register declared. For its resulting channel Lambda=C N, identity/flag discard lies in C's Pauli-correction decoder class. The learned compact recovery satisfies

    F_e(Rhat Lambda) >= F_e(Tr_G Lambda)-2r delta-eta.

Thus it preserves the Bell performance already achieved by that actual preconditioner, up to acquisition/implementation regret. Bell-label acquisition for Lambda works even without physically twirling Lambda; its optimum is then the correction-class optimum. It does not become Lambda's unrestricted optimum unless Lambda has the diagonal form.

If desired, apply a private OUTER twirl to the COMPLETED service Tr_G Rhat C N. This preserves its Bell fidelity and makes the reduced returned data channel Pauli; its half-diamond distance to identity then equals1-F_e. Charge2n fresh private bits and pre/post physical Pauli operations, and retire the key. This is not a joint bath/key-preserving or indefinitely reusable memory guarantee. A data-selected C must be frozen before the new independent acquisition bank, or covered by a separate simultaneous policy argument. No earlier learned-frame records are reused without that justification.

## 9. What remains and conventional comparison

The new synthesis is compact learned recovery with an explicit quantum-side-information dimension and a full acquisition/implementation path. Its ingredients are conventional quantum decision theory, matrix Bernstein, Pauli sampling/twirling and Naimark compilation; a strong conventional learner given the same Bell probes, flag and controls can implement it. No empirical separation, historical novelty, new capacity formula or civilisation-scale completion is asserted.

Remaining boundaries are consequential: Bell-reference preparation/storage/readout, acquisition of a useful coherent preconditioner, accessible flag dimension/compression, honest physical POVM/correction control, and inter-call memory. The ordinary bit-flip pilot avoids Bell references only by its narrower supplied source family. The theorem does not reconstruct the full environment or full Choi matrix, and it cannot manufacture useful recoverability when ceiling(7) is small.
