# A positive matrix confidence set without Bures-learning its completion

27 October 2026. Exact representation and convex-update/robust-decision subroutines. This is NOT a completed generic adaptive acquisition algorithm or a source-count theorem.

## 1. A compact positive lift can represent uncertainty, rather than a learned state

Use one common k-dimensional receiver frame and the four real quaternion coefficients. On `C4_control tensor C2_logical-reference tensor Ck_output`, form a Hermitian block matrix H=(H_ij) with

`H>=0`,

`Tr_output H_ii=I_2/2`,

`Tr_output(H_ij+H_ji)=0` for i<j.                            (1)

For every real unit x, contraction of the control factor gives

`J_x(H)=sum_ij x_i x_j H_ij`.

Equation (1) implies J_x>=0 and Tr_output J_x=I_2/2, so it is the NORMALIZED Choi state of a qubit-input CPTP channel. Also Tr H=4, hence this set is compact with O(k^2) real matrix coordinates. No continuum positivity oracle over S3 is necessary.

The true physical source is included. With B_ai=N_a E_i V0, take H_ij=(1/2)sum_a |B_ai>><<B_aj|. Its block Gram is PSD; the actual quaternion isometry makes the real-control trace identities (1) hold. This is an EXISTENCE construction from unknown Kraus amplitudes, not a preparation or tomography oracle. It remains valid in the common virtual frame after the received online compiler.

If the known physical overlaps are actually supplied/computed at paid cost, one may additionally impose

`Tr_output H_ij=(V0^* E_j^* E_i V0)^T/2`.

They are linear restrictions. Without them, (1) is a legitimate OUTER prediction class: it can contain per-encoder CPTP families not realizable by the exact supplied global hardware, but contains the truth and preserves physicality of every real-x predicted channel. This enlargement must not be confused with proving a new hardware implementation for each candidate. Known complex overlap amplitudes are not assumed free to compute.

## 2. Ordinary observations make linear confidence cuts

For an ordinary preparation P, encoder x, and output effect M, the outcome probability is

`2 Tr[H (xx^T tensor P^T tensor M)]`.

In particular for a fixed physical decoder D, define

`Q_D=I_(2k)-(id_2 tensor D^*)(Phi_2)`.

Because D^* is unital and 0<=Phi<=I, Q_D>=0. Its actual Bell loss is

`ell_D(x)=Tr[H (xx^T tensor Q_D)]`.                          (2)

This agrees with the nonnegative six-state scalar experiment. Each such mean is linear in H and lies in [0,1] on (1). Thus a valid scalar confidence interval from actual data appends TWO LINEAR constraints to the matrix feasible set. Matrix uncertainty is stored by a PSD constraint plus polynomially many linear cuts, not an exponentially large decoder or parameter net.

Adaptive statistical validity must come from the actual chosen confidence procedure. For example, conditionally valid fixed-batch intervals with a summable allocated failure budget remain valid under prior-history-dependent actions. This note does not assign an unproved fast-radius or sample bound to those intervals. General collective measurements on many output copies may have probabilities nonlinear in H; they are NOT silently covered by this single-output linear-cut statement.

Crucially, using H as a positive FEASIBILITY variable does not require Bures-learning any particular completion. Invisible control-antisymmetric coordinates remain nuisance variables in the set. The separate Tiles obstruction rules out a generic fast completion-Bures intermediary; it does not invalidate this convex confidence representation.

## 3. Finite positive model updates

Given the cuts, finding a feasible H, a central positive candidate, or optimizing any fixed linear functional of H is an SDP of matrix size 8k with polynomially many constraints. Boundary feasibility and numerical precision still need a contract; they are not an exact-real oracle.

A simple paid finite variant expands every acquired mean interval by an explicit rational zeta>0 without clipping the expanded endpoints. Let

`H_c=I_(8k)/(2k)`.

It obeys (1) and is positive definite. On any history where the unexpanded confidence set contains H_true, the mixture `(1-zeta/2)H_true+(zeta/2)H_c` (take zeta<=1) lies inside the expanded inequalities with margin at least zeta/2 because every measured mean is in [0,1]. Its minimum eigenvalue is at least zeta/(4k). In the affine space (1), bounded known measurement norms then give a polynomial-bit Slater/inner-radius bound, while trace H=4 gives an outer-radius bound. Standard finite SDP weak optimization/feasibility can therefore be implemented in polynomial bit complexity in k, cut count, coefficient bits, and log(1/zeta) at explicitly requested objective tolerance. On inconsistent bad histories it may return INCONCLUSIVE; the statistical procedure must charge those histories.

The expansion is part of the maintained confidence set. It may worsen later uncertainty; no assertion that its operational effect is merely zeta is made. Finite rational model descriptions can be rounded inward using this margin. If the optional exact-overlap constraints make H_c infeasible, use an actually supplied positive center for that smaller affine class or retain the outer class (1); do not assume the same center works.

## 4. Robust decoder selection is convex at each encoder

Let V be a nonempty compact convex confidence set of the preceding form. The six-state linear map from H to the decoder LOSS COEFFICIENT is

`L_x(H)=(3/2) T_x(H)^T`,

where T_x(H) is obtained from J_x(H) by the actual six-state measure-and-prepare construction. It is linear in H and PSD. Write the decoder set

`C>=0`, `Tr_output C=I_k`.

For a FIXED x, the worst-case risk of the best robust decoder is

`P_x=min_C max_(H in V) Tr[L_x(H) C]`.

The domains are compact convex and the objective is bilinear. Sion minimax, or finite-dimensional convex duality, gives

`P_x=max_(H in V) min_C Tr[L_x(H) C]`

`   =max_(H in V,Y) Tr Y`

`     subject to L_x(H)-Y tensor I_2 >=0`.                   (3)

The last program is a SINGLE SDP. For finite polynomial-bit decoder extraction, use Section3's expanded Slater contract (or an explicitly supplied equivalent regularity/conditioning contract), not nonempty compactness alone. Its dual then recovers a robust feasible decoder under certified finite primal/dual treatment. One may also explicitly dualize the inner max over V in the first program. Negative Y is allowed; no unjustified positivity restriction is imposed.

For every fixed H,C the loss quadratic has B between0 andI, hence is 2-Lipschitz on the unit sphere. Taking max over H and min over C preserves that Lipschitz constant, so P_x is 2-Lipschitz. A chord-h encoder net therefore costs at most2h in the ROBUST objective; quadratic stationarity is not automatically available for this minimax landscape. Scanning such a polynomial-size encoder net and solving (3) at each point gives an executable decoder/encoder with a valid worst-case UPPER risk certificate over V. No exponential decoder-policy list appears. Known coefficients and arithmetic, the number of cuts, and the chosen encoder-net resolution must all be charged.

This upper certificate becomes near-optimal if V is already narrow on a true optimal policy. For example if at some near-optimal grid x_* and true comparator C_* every H in V satisfies

`Tr[L_(x_*)(H) C_*] <= (1+gamma)ell_*+epsilon`,

then the robust selected policy satisfies the same upper bound, up to its paid grid/SDP errors. This is a sufficient confidence condition, not a proof that the proposed updates achieve it quickly.

## 5. The exact unclosed acquisition step

A positive convex confidence set and polynomial robust decisions do NOT yet give a fast localization algorithm. In particular:

* Optimistic global risk involves `min_(H in V,C) Tr[L_x(H) C]`, a JOINT bilinear minimization. It is not the convex program (3).
* Choosing the most informative model/policy disagreement involves H and C together. The separately received pairwise root-risk SDP primitive assumes TWO given models, not a free global maximization over all of V.
* A central feasible H may be far from the best informative/optimistic model. Volume reduction or local Fisher information alone does not prove that only O_tilde(k^2/(gamma epsilon)) ordinary source calls suffice.
* Convex feasibility of a PSD completion does not make its entangled zero witnesses nonnegative accessible ordinary tests. The Tiles operational-cone obstruction explicitly separates those notions.

The remaining theorem needed is a paid exploration/localization rule that shrinks task risk on a true comparator at the target rate while retaining polynomially represented uncertainty. This note closes only the whole-sphere positivity, model-update, and robust-policy computational pieces. All virtual-coordinate measurements and deployed decoders must use the SAME retained quantum frame; matrix feasibility is not a classical physical support-alignment procedure. This note makes no computational hardness claim or universal ordinary-access lower bound.
