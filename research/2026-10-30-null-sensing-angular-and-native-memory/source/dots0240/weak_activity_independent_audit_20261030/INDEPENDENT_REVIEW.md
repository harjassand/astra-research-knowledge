# Independent audit of weak-first initiation activity machinery
2026-10-30. Reviewer: `producer-workspace/review_simple_compiler`.

## Verdict
**Scoped PASS** for the actual weak-first-edge / fast-on-site-acquisition-abort generator, its full-Hilbert finite local BUSY witnesses, the additive collision hierarchy, the bounded-depth multiplicative activity inequality, and the direct nonunital local-noise estimate.

No substantive defect was found in the three frozen files. The argument needs the actual resolved-reset block preservation, the corner-sensitive remainder estimates, and the nonunital noise proof; replacing any of those with an ordinary scalar norm estimate would not suffice. This receipt supplies explicit details of those points.

This is **not** a DATA-weighted recovery inequality or native-memory theorem. It is a distinct generator from the earlier conflict-leaf proposal and from the main slow-all-acquisition construction. No multiplication of the activity drift by an arbitrary animal factor is accepted here.

## Frozen sources
Author-confirmed snapshots, preserved in `reviewed_sources/`:
- `ONSITE_ABORT_BUSY_WITNESS.md`: SHA-256 `2a55994a717c7512365ef630e92d6d32a8f747be56637f9d5ae58997a4d072b0`.
- `COLLISION_HIERARCHY.md`: SHA-256 `fbc390de6ac5bef70dbbb0153403f9c85648e088090411083369d1460ba7c3c2`.
- `MULTIPLICATIVE_ACTIVITY_WEIGHT.md`: SHA-256 `1339bf405517b642181e880f1bf39fcc1f21e2ed85eda3f08267e3cbfccaba23`.

Actual generator: repaired hub/resource architecture plus reset-first transactional changes, plus **only** the first acquisition edge assigned amplitude epsilon and the declared new complete on-site `A_i -> Q0` aborts for i>=1. Later acquisition, cleanup, computation and verification rates stay fast. Coherent cleanup remains disabled in R. `FAST_ACTIVITY_REPAIR.md` is not governing. The source manifest identifies all proof dependencies read.

The author separately confirmed that the noise budget means the usual supportwise completely bounded norm of local Hermiticity-preserving identity-annihilating perturbation maps (or a dilation-stable equivalent), not an arbitrary representation-dependent sum of jump norms. This clarification is used below.

## 1. Actual BUSY invariance and the stronger block algebra
Let `R_h` be the projector onto A0, workspace zero, and absence of both own labels on every resource. Monitors are unrestricted. Set `P_h=I-R_h`.

The P_h commute on the full forest-frame Hilbert space: they are functions of clock/workspace-zero projectors and diagonal own-label tests, with no DATA dependence. At epsilon=0 all actual Hamiltonians commute every P_h. In particular:
- every A_i>=1, C, Q and R phase is busy independently of workspace;
- any A0 abort/cleanup edge has an own tag and is already busy;
- the sole fast Hamiltonian edge leaving truly ready A0 would have been the first acquisition, which is absent;
- external owners change only labels that are equally non-own for h.

Noncreation alone would not establish invariance of the entire joint block-diagonal observable algebra. The stronger actual reset structure does:
- terminal, abort, new acquisition-abort, commit and ready sources are wholly in the owner's busy corner;
- A0 refresh channels with s!=0 have wholly busy source; the s=0 channel preserves the ready/busy predicate;
- a z_h-to-free source is wholly busy for h, or leaves its predicate unchanged;
- a monitor Kraus operator commutes the flags;
- every other owner's flag is preserved separately.

For a joint-block-diagonal O, input matrix elements between distinct joint P masks therefore vanish in each reset gain. If masks differ at the reset's owner, either the relevant source is zero or the channel preserves that predicate; if they differ elsewhere, their target sectors remain orthogonal. Complete summed losses commute the masks. Actual forest payloads do not spoil this because the BUSY flags contain no DATA operator. This proves the full adjoint block-algebra statement, including coherent ownership masks and dirty workspace, rather than just Boolean no-creation.

The weak first-edge H_h commutes P_j for j!=h; it can toggle P_h or act within its busy corner. This is precisely the collision hypothesis.

## 2. A fast full-Hilbert return to Ready is earned
The new complete Ai abort is important. Every Ai>=1 can reset immediately without using a reverse first edge or waiting for a resource. For any projected configuration of h and its resources:
- R resets to Q0;
- an inconsistent ordinary phase has an enabled failed-test abort and reset;
- consistent C follows its finite forward circuit and terminal reset;
- Q removes only its own o/z labels, verifies absence, and ready-resets to A0;
- A0 with only dirty workspace refreshes.

No step requires an acquisition, clears another owner's tag, or relies on another owner making progress. A consistent C has all owned resources; its actual unitary gate blocks preserve norm on arbitrary DATA/workspace/reference input. Malformed C is handled by its genuine abort, not by an assumed recovery oracle. The final complete ready/refresh reset sets workspace zero with every own tag absent.

The proof patch consists of complete h and resource sites. Every boundary-crossing generator term is included in its finite norm budget, while disjoint exterior dynamics is kept as a CPTP semigroup. The actual full reset monitors, not effective dephasing, provide the flush and finite projected windows. Their label measurements do not measure workspace. Their strictly positive finite-window Gramian works with initially entangled monitors. The selected path bound is uniform in the arbitrary conditional exterior state.

All selected amplitudes and reset intensities are fast fixed constants. Thus for fixed T,p>0 independent of epsilon and system volume,

    exp(T L0*) P_h <= (1-p) P_h.

Ready is absorbing under L0, so earlier arrival is legitimate success. The source bound `m=Lmax+3 kmax+4` safely covers these paths. The new complete resets do not violate two-site-Hamiltonian/onsite-reset support: they are actual on-site clock/workspace transitions, not a multi-resource conditional reset.

## 3. Local witness construction, with relative rather than extensive errors
Because the flag is noncreating and its exits are local,

    L0* P_h = -A_h,   0<=A_h<=nu P_h.

Complete positivity gives `exp(tL0*)P_h>=exp(-nu t)P_h`. Hence the exact finite-time integral satisfies

    a P_h <= G_h <= T P_h,
    L0*G_h <= -p P_h,
    a=(1-exp(-nu T))/nu.

Every semigroup iterate stays in the P_h corner. More generally, positivity and `T_t*(P_h)<=P_h` imply that an operator supported in P_h remains there: apply the bound first to positive operators dominated by a scalar multiple of P_h, then extend linearly. Joint block-algebra preservation also gives commutation with every P_j.

The anchored polynomial/telescoping construction applies starting from the local observable P_h, not I. Each polynomial iterate is exactly corner-supported and in the joint block algebra. Consequently a norm error eta is also an order error bounded by eta P_h. The short-step local Taylor estimate uses only per-site incident generator norm and support growth. For arbitrarily large fixed T, the finite sequence of small Taylor steps remains finite-support; no large-T Taylor convergence assumption is needed.

The exact identity `L0*F_M=O_M-P_h` controls the derivative error directly. One must not apply the extensive generator to a small approximation error. Choosing the local approximation tolerance below the stated a,p margins yields

    (a/2)P_h<=F_h<=2T P_h,
    L0*F_h<=-(p/2)P_h,
    [F_h,P_j]=0.

After normalization this is the claimed `cP_h<=X_h<=CP_h`, `L0*X_h<=-P_h`. The fixed support radius and incidence can be enormous, but do not grow with volume or runtime. In malformed sectors X_h may act on DATA; no controller-only closure is required for the activity theorem or asserted by this receipt there.

## 4. Projection product and collision remainder support
For a product Q of the commuting activity projections, no-creation and block preservation also hold. If X>=0 commutes Q, comparison of active/inactive jump blocks gives

    L0*(QX) <= Q L0*(X) Q.

The difference is the negative of the omitted positive gain through an active-to-inactive exit. Hamiltonian and complete-loss terms agree; the block property removes off-diagonal terms. Therefore `Y_hj=P_j X_h` is positive, lies in the pair corner, and obeys `L0*Y_hj<=-P_hP_j`.

For completeness, the Young estimates use actual corner support, not only a norm bound:
- own singleton cross block has norm O(A epsilon^3), connecting P_h and its complement. Spending a fixed fraction of `A epsilon^2 P_h` leaves O(A epsilon^4)(I-P_h);
- another initiation preserves P_h, giving only O(A epsilon^3)P_h;
- a pair cross block from toggling h connects `P_hP_j` to `(I-P_h)P_j`. Spending a fraction of B P_hP_j leaves O(B epsilon^2)P_j, **not** an identity term;
- initiations preserving both pair flags stay in the pair corner.

Bounded incidence permits summation. Choose A sufficiently large relative to B, then epsilon small. This proves the exact additive inequality with the O(A epsilon^4 N) idle source. Stationary total-activity and integrated transient consequences are valid. No higher-order specified-set stochastic law follows merely from it.

## 5. Noncommuting finite-depth product: the fast remainder
The gates `exp(delta B Y_e)` and `exp(delta A epsilon^2 X_h)` are positive and invertible, but need not commute. Their bounded-depth product Y_U gives the positive `G_U=Y_U^*Y_U`. Since each gate commutes all flags, G_U does also. Minimum singular values multiply, so `I<=G_U`; upper singular-value bounds give the stated exponential-in-|U| comparison. Positivity of the ordered product itself is not assumed.

Use exact congruence `C(O)=Y_U^* O Y_U`. A disjoint gate cancels with its inverse in a local term; finite depth leaves only a bounded local cone. The transformed generator is an exact similarity, not a claim of Lindblad form or an approximation of long-time dynamics.

Here is an explicit justification for the sensitive fast remainder assertion. For each gate generator Z, define `M_Z(O)=ZO+OZ`. Expand the finite local similarity in these multiplication superoperators. Every word contains one occurrence of L0* and some multiplication operators; on I the zeroth-order term is zero. The linear term is `2 L0*Z`.

Each Z is supported in its flag corner and commutes every activity projector. Any product of gate operators is supported in the intersection of their corners. L0* maps an arbitrary operator supported in such an intersection back into that intersection, as established above. Multiplying by the remaining gate operators cannot enlarge it. Thus every nonzero word containing a pair gate is supported in that pair corner, even if gate operators do not commute internally. A word containing only singleton gates and at least two factors carries at least epsilon^4.

One may group all local-generator terms in a word before invoking corner preservation; the argument does not require a fortuitous termwise block property when only the whole L0* was assumed. Terms disjoint from that word's connected gate support vanish. Bounded depth and incidence then bound the local Taylor remainder, with no |U|^2 count, by

    C delta^2 [B^2 sum_e P_e
               +AB epsilon^2 sum_e P_e
               +A^2 epsilon^4 sum_h P_h].

Higher orders are absorbed in C for fixed bounded delta B and delta A epsilon^2. Choose delta small to absorb pair terms and then epsilon small to absorb singleton terms. This proves the claimed fast part, not merely a scalar O(delta^2)|U| estimate.

## 6. Exact weak part after congruence
Since all gates commute the flags, conjugating an initiation changes its local coefficients but not which flag it toggles. In the bounded local cone, resolve the finitely many joint flag sectors.

If a selected pair is present on both ends, the contribution is bounded in that pair corner. If a pair is created/removed, its other endpoint is still active; Young's remainder is singleton-supported. If neither end has any selected pair, every pair gate is exactly the identity on both ends. The difference from the original initiation then comes only from singleton gates and is O(delta A epsilon^3). Its Young remainder is O(delta A epsilon^4)I. Initiations with index outside U cannot toggle a selected endpoint and give only already-active-corner terms.

This finite block decomposition also handles multiple overlapping pair gates and noncommuting coefficients. Local inverse norms are uniform. The same order of choices—B, then A, then delta, then epsilon—gives the stated exact inequality for G_U with positive fixed a,b,C. No effective elimination or stochastic interpretation of the coherent first edge is used.

## 7. Direct nonunital cb-noise estimate
The source correctly does **not** apply a unital CP-dressing lemma. The congruence and its inverse are CP but generally nonunital, and a conjugated perturbation need not annihilate I.

A representation-free proof under the clarified budget is as follows. For each local HP term N_e*, finite-depth cancellation gives a map `Ntilde_e*=C^{-1}N_e*C` supported in a fixed enlarged system region (and the same retained bath), with

    ||Ntilde_e*||_cb <= K ||N_e*||_cb.

K depends only on the finite local gate cone and inverse norms. It does not depend on the number of selected anchors or animals.

Split the positive raw animal factor into its boundedly many local factors touched by this region, g, and the remaining product w. The usual bounded local-orbit ratio means `mI<=g<=MI` with M/m uniformly bounded. Untouched factors commute with the map's system support, and with g; the local bimodule property therefore gives

    Ntilde_e*(f_A)=w Ntilde_e*(g)
                 <= K ||N_e*||_cb (M/m) f_A.

This works for general HP maps, not merely one chosen Hamiltonian/jump representation. Shared-bath terms are included by the cb norm; every congruence gate is system-only. Bath-only identity-annihilating terms still vanish. The Hamiltonian and jump formulas in the source are consistent illustrations: in particular the transformed loss is not formed from `Jtilde^*Jtilde`.

Only perturbation supports meeting f_A or the selected gate cone contribute; otherwise the original identity-annihilation remains available after trivial cancellation. There are O(|A|) incident supports because |U(A)|=O(|A|), with fixed radius/incidence. Congruencing the inequality back yields

    N* F_A <= C_noise eta |A| F_A,
    F_A=Y_U^* f_A Y_U.

No commutation between f_A and the gates is required, and no extra |A| is introduced. This is the accepted noise statement. It alone says nothing about useful DATA drift of the sum of these F_A.

## 8. Regression evidence and scope
I reran the actual author's exhaustive BUSY fixture: 116,640 clock/lock/clean-dirty-workspace basis configurations, 643,320 directed transitions, and 233,280 clearing paths passed. Maximum selected path length was 11, below 13. This checks eligibility and Boolean invariance; the full coherent block and finite-monitor arguments above are indispensable additional proofs.

The independent `check_noncommuting_activity.py` uses three activity qubits and a shared auxiliary qubit. Its local positive witnesses do not commute (commutator norm 0.36), while all commute the activity projections. It verifies additive and multiplicative inequalities at four epsilon values, with fixed constants. The pair-containing fast remainder has exactly zero block outside the pair union; singleton remainder divided by delta^2 A^2 epsilon^4 stays approximately 13.38. It also checks a shared-bath Hamiltonian noise identity with f not commuting the gates. The transformed noise is genuinely nonunital (norm 0.01695 on I), and the exact formula residual is 1.81e-15. Scripts and JSON outputs are preserved. This is a regression of the abstract algebra, not a code-memory simulation.

## Explicit remaining obligations
- Combine useful DATA-recovery CP credit, animal surgery and activity charge without multiplying the controller inequality by an unjustified f_A.
- Pay the real DATA effects of dirty payload resets in that combined multiplicative observable.
- Establish the final clean acquisition/useful-service coverage and any native continuous-noise memory statement.
- Physical preparation/retrieval remains separate.

The present activity receipt does not silently promote any of those remaining claims. The author explicitly leaves the DATA synthesis outside the frozen module, and I have not audited it here.
