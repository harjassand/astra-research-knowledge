# Second independent adversarial audit of the 18-qubit exclusion

Date: 5 November 2026. Scope: arbitrary complex rank-two subspaces of the **fully symmetric** n-qubit Hilbert space, with exact correction of arbitrary errors on at most two physical qubits. This means every codeword lies in Sym^n(C^2), not merely that the code projector commutes with permutations. Subsystem codes, approximate correction, higher local dimension, and general nonsymmetric qubit codes are outside the statement.

## Verdict

No substantive gap was found in the necessary relaxation, its conventions or normalization, or the corrected rigorous dual separator. The corrected n=18 witness replays with the same strict positive contradiction margin, greater than 0.0000690847. Independently reconstructed complex product-basis tests support all recoupling conventions; three exact Clebsch-Gordan sum checks at the actual spin j=9 also pass. Those tests supplement the general identities below rather than replace them.

The exact lower-length LP separators were independently rechecked from factorial 6j formulas. A separate fresh reconstruction verifies the published 19-qubit code, including exact root existence and all 50 reduced KL equations. Taken together, these establish minimum length 19 under the stated fully symmetric exact-correction definition, subject to the explicit analytic representation identities and the supplied exact arithmetic certificate. This is not a claim of novelty, a general quantum-code optimum, a practical decoder, or a formal proof-assistant verification.

## 1. Physical errors and arbitrary complex codes

Write j=n/2, D=n+1, and let P=P^dagger=P^2 have rank K=2 on V_j=Sym^n(C^2). Exact correction of all weight-at-most-two Pauli errors is equivalent, by Knill-Laflamme, to scalar compression of every Pauli of weight at most four: every such Pauli is a product of two weight-at-most-two errors, and all their products have weight at most four.

Between symmetric vectors a physical operator can be replaced by its permutation average. The compressed weight-at-most-four operators span precisely the irreducible operator tensor sectors of rank r=0,...,4. One direction follows by expanding degree-at-most-four collective-spin polynomials into local Pauli products. Conversely, the highest component of rank r is proportional to J_+^r, a nonzero sum of distinct-site weight-r raising products for r<=n; collective rotations span its full rank-r irrep. The degree filtration decomposes into ranks no larger than its degree. Thus every candidate code must obey

    P E P = Tr(P E) P / 2

for every operator E in ranks below five. No real, parity, time-reversal, stabilizer, or sparse-support condition is used. Conversely, these complete rank conditions suffice for the original arbitrary two-error correction requirement; the subsequent relaxation itself is only necessary, not sufficient for existence of a code.

## 2. Enumerator, pair, and triple normalizations

For Hilbert-Schmidt orthonormal spin tensors T_rq, define

    a_r=(D/4) sum_q |Tr(P T_rq)|^2.

Then a_r>=0, a_0=1 and sum_r a_r=D/2, by Tr P=Tr P^2=2. Define the conventional companion enumerator

    b_r=(D/2) sum_q Tr(P T_rq^dagger P T_rq).

The SU(2) MacWilliams relation is b=2Ma, where

    M_kl=(2k+1)(-1)^(n+k+l) {j j k; j j l}.

Cauchy-Schwarz gives b>=a; detection makes equality in each tested rank. The coefficient convention and normalization were independently checked by direct tensor operators on genuinely complex random P at n=1,...,4, not by using the saved transform table.

Let X2=twirl(P tensor P), and let w_l=Tr(Pi_l X2) be its **total** pair-spin weights. Then

    w=(4/D) M diag((-1)^r) a,    sum_l w_l=4.

In the pair-spin l sector, X2 equals w_l/(2l+1) times the identity. Let X3=twirl(P tensor P tensor P). It has trace 8, not trace one. In the coupled basis ((j,j)l,j)J it has blocks I_(2J+1) tensor R_J. The identity Tr_3 X3=2 X2 yields

    sum_J (2J+1) (R_J)_ll = 2 w_l.

Consequently B12=X2 tensor I has multiplicity blocks diag(w_l/(2l+1)). No extra factor 2 or D belongs in these complement blocks. Direct product-basis tests confirm all these identities.

## 3. Copy symmetries do not discard legitimate rank-two codes

P tensor P tensor P commutes with copy permutations. The alternating copy sector vanishes because wedge^3(range P)=0. It is **not** permissible to keep only the fully symmetric copy sector; the proposed model correctly retains the standard S3 sector as well.

In each J block, the copy swaps are the real matrices

    V=S12=diag((-1)^(n-l)),
    U=S23,
    U_ll'=(-1)^(n+l+l') sqrt((2l+1)(2l'+1)) {j j l; j J l'}.

The group-average symmetric and alternating projectors used in the verifier are the exact S3 projectors. If Qp spans the V=+1 part of the standard sector, then Qm=(2/sqrt(3)) P_- U Qp is its corresponding partner. Every positive real commutant block has the form

    R_J=Qs A_J Qs^T + Qp B_J Qp^T + Qm B_J Qm^T,
    A_J>=0, B_J>=0.

Nonorthogonal projected frames are allowed. The exact frame ranks and positive Gram lower bounds certify that they span the intended spaces. The standard trace must include both Qp and Qm, as the verifier does.

Real blocks are a legitimate relaxation of complex codes. All retained maps and equations have real coefficients, so taking the entrywise real part of feasible Hermitian blocks preserves those equations and positivity. Equivalently, conjugating a physical code in the real Dicke basis preserves the physical error space; its enumerator a is unchanged, and averaging the two twirled triple operators produces Re R. The average need not itself be the tensor cube of a projector. That is harmless for a necessary-condition relaxation. No assertion that every code is real is needed.

## 4. Lifted KL identity and its exact 6j convention

Before twirling, define

    Q0=(P tensor P tensor P)(S23-I/2).

For any detectable E on copy three,

    Tr_3[Q0(I tensor I tensor E)]
      =P tensor [P E P-Tr(P E)P/2]=0.

Collective rotations preserve each tensor rank, and S23 commutes with those rotations. Hence the same equation holds for Q=X3(S23-I/2). Its multiplicity blocks are R_J(U_J-I/2).

Here is an explicit convention check rather than an unspecified appeal to a 6j formula. Define a normalized rank-r transition tensor from V_l' to V_l by

    (A_(rq)^(l,l'))_(m,m')=(-1)^(l'-m') <l m,l' -m'|r q>,

and define T_rq on V_j by the identical formula with l=l'=j. For E_(ll')^J=sum_M |(l,j)JM><(l',j)JM|, the q=0 Hilbert-Schmidt contraction is

    Tr[(A_(r0)^(l,l') tensor T_(r0))^dagger E_(ll')^J]
      =(-1)^(l'+j+J)(2J+1) {l j J; j l' r}.

Expanding the left side gives four Clebsch-Gordan coefficients. Replacing them by their defining 3j symbols and using the tetrahedral 6j contraction gives the displayed identity. Explicitly, the summand is

    (-1)^(l'-m+j-mu)
    <l m,l' -m|r0><j mu,j -mu|r0>
    <l m,j mu|J,m+mu><l' m,j mu|J,m+mu>.

Thus, with

    C_(Jr)^(l,l')=(-1)^(l'+j+J+r) {l j J; j l' r},

the q=0 contraction is (-1)^r sum_J(2J+1) C_(Jr) Q_(J,ll'). Rotational covariance supplies the other q components. The harmless common sign (-1)^r does not affect the zero equation. This is precisely the implemented coefficient. After realification Q is real symmetric; the code's transposed entry Q_(lp,l) is the same. Before realification the conjugate equations likewise vanish.

The independent checks compare the **whole J-dependent coefficient vector**, not merely one code's zero residual. They cover 119 allowed triples (l,l',r) at n=1,...,4. Three additional n=18 cases verify the exact CG sum minus the proposed 6j value is identically zero in symbolic arithmetic, including off-diagonal l,l' and rank four.

## 5. PPT and complement constraints are necessary

Define Theta(A)=Y A^T Y^dagger on V_j, with Y|m>=(-1)^(j-m)|-m>. This is transpose followed by a fixed unitary, not a positivity-preserving operation on an arbitrary entangled bipartite state. Here its use is valid because X3 is a mixture of the copy-product positive operators P_U tensor P_U tensor P_U. Its copy-three Theta image is therefore positive. The same argument applies to the positive copy-product P_U tensor P_U tensor (I-P_U).

Theta is covariant under spin-j rotations, so it commutes with the collective twirl. On a rank-r operator tensor it acts by (-1)^r. Racah orthogonality gives

    sum_J(2J+1) C_(Jr) C_(Js)=delta_(rs)/(2r+1).

Changing each rank component by (-1)^r and applying the inverse transform yields

    Theta_3(R)_(J,ll')
      =sum_(J',r) (2J'+1)(2r+1)(-1)^r
         C_(Jr) C_(J'r) R_(J',ll').

This is the original rank-sum map restored by the rigorous verifier. It is not a guessed shortcut or a spin-reversal symmetry of the code. Both

    Theta_3(R)>=0,
    B12-R>=0,
    B12-Theta_3(R)>=0

are necessary, with the B12 normalization from Section 2. The last two inequalities follow by twirling P tensor P tensor (I-P) before and after partial time reversal. Arbitrary complex invariant matrices, without S3 or positivity assumptions, were also used to independently check the full linear Theta map in the product basis.

## 6. Exact dual separator and residual bound

I read and replayed `audit_residual/verify_interval_dual.py` in a separate directory. It uses integer centers and radii over 2^192. The 6j coefficients are rebuilt from rational factorial sums and integer-square-root enclosures. Every supplied matrix multiplier is defined as an exact dyadic factor times its transpose, hence is PSD; scalar inequality multipliers are nonnegative. The frame rank checks use exact projector traces and strictly positive Gram enclosures. The original rank-sum coefficients, including entries omitted by the numerical sparsification, are all restored.

The standard equality orientation is Marg(R)-2w=0. The corrected witness reverses the exported sixth equality multiplier to match that orientation. This is a legitimate equality-dual sign correction; the final proof uses the corrected file only. No epsilon-stationarity equation is needed for the zero-slack infeasibility argument.

For any feasible relaxation point the resulting Lagrangian obeys L<=0. The reconstructed affine identity is

    L=c+r_a dot a+sum_i Tr(r_i X_i).

The residuals cannot be discarded, but they are rigorously bounded. Since a>=0 and sum a=D/2, their first contribution is at most (D/2)||r_a||_infinity. For the PSD multiplicity variables X_i, the Gram bounds g_i and trace(X3)=8 give a total contribution at most

    8 max_i ||r_i||_operator / [(2J_i+1)g_i].

The verifier uses a row-sum operator-norm upper bound after symmetrizing each residual. Every matrix product and square root is enclosed; integer floors/ceilings are directed outward. Its positive contradiction margin includes both residual contributions. There is no assumption that floating dual residuals vanish.

Corrected witness SHA256:

    0fec2978c5c7141ea7d119fce811c237dbb817a819c494041d8802bfa1ebdbd9

Fresh replay result:

    c=19912604860857/288230376151711744,
    c-residual_budget approximately 0.00006908479009717404,
    c-residual_budget > 690847/10^10 exactly.

The authoritative strict comparison is the exact Fraction in `interval_certificate.json`, not the rounded decimal shown above. Numerical optimizer status is not used as a proof premise. Standard correctness of the representation identities and of the exact-arithmetic implementation remains part of the stated trust boundary; this is not a proof-assistant extraction.

## 7. Lower lengths, genuine 19-qubit control, and prior art

`check_lp_factorial.py` independently rebuilds the rational transforms and verifies every supplied nonnegative dual identity. It excludes n=9,...,17 and correctly does not exclude n=18. Elementary Singleton covers n<9; the stronger general binary Rains shadow bound already gives n>=11, so Singleton must not be called the strongest general incumbent. The relevant stronger same-scope comparator is the evaluated intrinsic LP (with its exact surviving n=18 shadow-feasible point), not Singleton alone.

The separate report `symmetric19_audit/INDEPENDENT_REVIEW.md` independently reconstructs Aydin-Alekseyev-Barg's 19-qubit code. A fresh rational contraction proof gives an exact root box contained in the existing certificate's box. All 50 four-qubit reduced logical KL equations are present exactly once and are verified; a nonzero five-site Z witness gives distance exactly five. The existence proof is not based only on printed rounded coefficients. The codeword ansatz is AAB Eq. (31), with the coefficient system in Eq. (32).

Primary sources checked include AAB, Quantum 8, 1321 (2024), https://doi.org/10.22331/q-2024-04-30-1321 ; Bond et al., https://arxiv.org/html/2603.10981v1#S3.SS1 ; Kubischta-Teixeira, https://arxiv.org/html/2604.16023v2 ; Teixeira, https://arxiv.org/abs/2605.15372 ; and Rains, https://arxiv.org/abs/quant-ph/9611001 . The 2026 numerical paper still treats sharp general minimality as conjectural. AAB's shorter-code statement is restricted to its real PR-form setting. No earlier unrestricted minimal-19 theorem was found in this bounded search; exhaustive priority is not certified.

## 8. Reproduction files and final scope

- `check_complex_recoupling.py` and `complex_recoupling_results.json`: independent full product-basis checks on complex inputs, with maximum discrepancy about 1.07e-14.
- `check_exact_recoupling_identity.py` and `exact_recoupling_identity_results.json`: exact actual-n=18 coefficient checks.
- `verify_interval_dual_replay.py`, `interval_certificate.json`, and `interval_replay.log`: unchanged verifier source, separately replayed against the corrected witness.
- `check_lp_factorial.py` and `lp_factorial_results.json`: independent factorial-form lower-length audit.

No constructor, original auditor, solver, or positive-control file was modified by this second audit. The result excludes every complex rank-two exact two-error code **inside the fully symmetric subspace** at length 18. Feasibility of a relaxation would not establish a code; the positive 19-qubit result comes from its separate exact construction. No performance, implementation-cost, fault-tolerant-overhead, or broad quantum-code optimality claim follows.
