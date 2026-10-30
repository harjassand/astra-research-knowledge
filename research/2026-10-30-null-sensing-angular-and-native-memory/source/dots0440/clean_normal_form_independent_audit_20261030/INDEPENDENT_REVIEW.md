# Independent clean DATA/activity normal-form audit
2026-10-30. Reviewer: `producer-workspace/review_simple_compiler`.

## Verdict and important scope
**Scoped PASS for the actual clean, raw-basin-restricted DATA/activity drift**, with the explicit locality and basin-order qualifications in sections 2 and 10 below. The new first-order similarity route works; the earlier direct-family argument is not used as a substitute.

The review found one missing order-transfer justification in the manuscript: coverage holds in a safe syndrome basin, not on the whole clean Hilbert space, so applying T to it requires basin invariance. I reported this before repair. Here the actual deterministic raw-syndrome payload and controller-only credit do preserve the accepted raw-V sublevel basin, so the gap is repairable without changing the physical generator or source. The receipt proves that step.

No counterexample was found to the weighted terminal completion, singular-opening cavity, local t*delta/t^2 bounds, weighted Young budgets, or parameter hierarchy. The result does **not** include full-Hilbert dirty surgery, arbitrary-noise leakage out of the clean controller range, basin killing/stopping, or a final native memory/physical retrieval theorem.

## 1. Exact reviewed versions
Frozen principal source:
- `CLEAN_EFFECTIVE_NORMAL_FORM.md`: SHA-256 `1cbd3a81130f8ba419696587a669b5d975402b9153412ae4c2b95bbf6aace19c`.

Frozen supplements:
- `NORMAL_FORM_MONITOR_ACCOUNTING.md`: `65247448608ab1a90e5cb4a00f449078b1a31c23885d4205b136c870f8ae05ed`.
- `SINGULAR_OPENING_CAVITY_LEMMA.md`: `bf8cdc20e6d9d239b4830c48c272c4b1fdf69545b647c4c49fbff03c21cd47ae`.
- `WEIGHTED_COVERAGE_MARGIN.md`: `2b4f662aed35d16cc848bbe93536341ce0e184b710286c54fbcec66e53f8281e`.

Needed native-constructor lemmas reviewed at these exact versions:
- `ANIMAL_LOCAL_ACTIVITY_WEIGHT_CHARGE.md`: `9b14b288c85c06f362dc51c4f206beb819b25de0ced48888dbc34402a83d763a`.
- `CONTROLLER_ONLY_ACTIVITY_EXTENSION.md`: `76fc918ddccafd1613a981d9b9fb5fba411c2e5cb8f0d341262897d6332eea66`.

Copies and a complete dependency manifest are saved. The already accepted activity, isolated-resolvent and analytic-CP inputs are imported at their reviewed hashes. I also read the actual weighted-progress completion/coverage proof rather than assuming that arbitrary weights preserve it. Dirty cavity candidates were not needed for the clean theorem and are not certified here.

## 2. The coefficient maps really have finite local extensions
On the all-good forest range the scalar controller algebra closes: Hamiltonians are DATA-free; the complete clean terminal is a fixed controller jump tensored with the intended Phi_h. This includes coherent clean controller states, not only a sampled classical schedule. The activity witnesses restricted to this range are therefore controller-only.

To make the local cb estimates literal, use the stated finite-support extension: pinch the full witness in the commuting local history flags and take the normalized conditional expectation over its DATA support. The resulting Xbar is positive, controller-only, flag-preserving and obeys the same `cP_h<=Xbar_h<=CP_h`. It agrees with the original witness on the clean range. No dirty drift is claimed for this extension.

The useful CP map is identity outside its finite local all-B-good buffer and isolated neighbor-ready sector, with its local no-jump cross-sector action retained. It is not compressed by the global all-good projector. Its finite local isometry/virtual reset preserves the global clean range. The author explicitly confirmed this interpretation during review.

Consequently all activity gates and useful maps admit bounded-support, bounded-incidence extensions with uniform local cb bounds. Their induced maps on the clean range agree with the intended ones. Since each useful map is near identity in the outer interpolation parameter, its linear inverse also induces the correct clean-range quotient map by its convergent Neumann series. This does not require the inverse to be positive.

## 3. Weighted zero-order physical monotonicity is earned
Use one global finite coloring/order for every selected animal circuit. Choose U(A) as a union of fixed-radius anchor neighborhoods, with radius large enough to cover every affected payload and neighboring weak/guard-error anchor. Let E(A) contain the induced physical-overlap pairs. A bounded local completion changes only boundedly many selected gates; a component completion of m vertices changes O(m) gates. The gate support/color rule is independent of A.

Finite-depth cancellation in the quotient gives

    exp(-C delta m) G_A <= G_(A union D) <= exp(C delta m) G_A,
    I<=G_A<=exp(C delta |A|)I.

This is a congruence/singular-value bound, not order monotonicity of a noncommuting product. The global color rule is essential.

For the actual clean generator, replacing each successful terminal DATA channel by identity defines a scalar controller generator L_c. Since G_A is controller-only and f_A is DATA-diagonal, the exact product identity is

    L_phys*(G_A f_A)
      =f_A L_c*G_A
       +sum_j J_j^*G_A J_j (Phi_j*f_A-f_A).

It uses the complete workspace-resolved terminal instrument and uniform summed losses. There is no independent scheduling assumption.

Fixing a raw syndrome, the factors `J_j^*G_A J_j` are positive controller operators. Their completed-animal comparisons follow by pulling the preceding G inequality through J_j. The original scalar source-to-completed-target charge can therefore be performed in Loewner order, with its fixed extra factor exp(C delta |D_j|). Its strict move margin absorbs that factor. This proves both nonpositive physical terminal DATA drift and, by the same proof with J=I,

    D_h^G=(I-Phi_h*)V_G>=0.

It is not necessary for every individual f_A to be Phi_h-monotone. The proof specifically charges its positive increments against different completed animals.

Multiplying the scalar activity inequality by f_A and summing is now justified by the exact identity and this nonpositive terminal term. Thus the actual clean L supplies weighted singleton/pair charges with strengths delta A epsilon^2 and delta B, and an idle source O(delta A epsilon^4)W_G.

## 4. Each actual first-order commutator is accounted for once
The own isolated cancellation was independently verified in the preceding useful-credit receipt. R_C is exactly epsilon-independent, S_C=s0 I+beta R_C, and ready evaluation annihilates the terminal intensity. Thus

    [L_h*,Q_h]V=-beta_h d_h+beta_h E_h d_h,
    ||E_h||<=C, E_h supported on C.

For a FIXED h commutator, its isolated core includes every physical resource-monitor term on R_h once. On the neighbor-ready guard these are the actual isolated monitored dynamics. They are not exterior spectator terms. Repeating this grouping separately for different h does not assert, and must not be rewritten as, `L=sum_h L_isolated,h`.

The other actual clean cases check out:
- a neighboring terminal remains busy, C->Q, so the h-credit is identity on both source and target; its commutator on DATA-only V is exactly zero, despite overlapping noncommuting DATA channels;
- other fast neighboring moves preserve that owner's busy flag; where the h guard is enabled their own-tag transitions are absent or act only on scalar spectator coordinates, and otherwise h's credit is identity;
- a DATA-free ready return can open the guard and yields exactly `-J_ready^* B_h(out) J_ready d_h`, a nonpositive raw operator;
- disjoint full-footprint maps commute;
- a weak neighboring initiation yields `-i epsilon[H_j,B_h^guard]d_h`.

The latter block orders follow from B_ready=O(epsilon^2), B_ready,busy=O(epsilon), B_busy=O(1), and the fact that H_j toggles only j on the clean range. They are O(epsilon) independent-busy/collision, O(epsilon^2) ready/collision and singleton-swap, and O(epsilon^3) ready/singleton. Shared resource monitors are already in the fixed-h core and are not falsely assigned to this list of vanishing exterior terms.

Removing the neighbor-ready guard from the negative useful demand loses at most a nearby-busy-supported O(epsilon^2) charge. The own C remainder is also busy-supported. Enlarged anchor selection ensures all such endpoints belong to the activity masses of each affected animal.

## 5. Exact similarity, not an inverse-positivity argument
Let each interpolated useful factor be `Id+t Z_h`, Z_h=Q_h-Id. For t<1/4, its inverse is a uniformly bounded LOCAL linear map by the Neumann series. Disjoint maps commute through a local generator term and cancel with their inverse in the exact similarity. Bounded depth leaves only a fixed local cone.

Expanding that finite local cone in t gives

    T^{-1}L*T=L*+t sum_h[L*,Z_h]+R_t,

where R_t is a bounded-incidence sum of local HP identity-annihilating maps of cb norm at most C t^2. This is uniform in epsilon in its fixed small interval because Q_h is uniformly bounded and local; no 1/epsilon norm is introduced by its underlying resolvent. No extensive generator/inverse norm is used.

For V_G, conjugate each local map through the relevant animal circuit. Only a fixed number of gates in its local cone remain; the transformed map may be nonunital. The direct local relative-norm argument applies: separate untouched animal factors, bound the finitely touched positive factors by their uniform orbit ratio, and use the local cb norm. Only O(|A|) supports contribute for an animal. Therefore

    R_t(V_G)<=C t^2 W_G.

This is an estimate on the exact remainder map. At no point is a negative operator pushed through T^{-1} using an invalid positivity claim.

## 6. Moving through animal weights and the singular-opening repair
For a local first-order commutator F_h, conjugation through the activity circuit differs from F_h by O(delta) in the local relative norm. The proof is a finite local product estimate: gates and inverses remaining in that cone are `I+O(delta)`. It is not an estimate of the extensive norm `||G_A-I||`. Summation costs O(t delta)W_G.

Because all Y_A are controller-only, the weighted principal term is exactly

    -beta_h sum_A G_A(f_A-Phi_h*f_A)=-beta_h D_h^G.

Every activity projection commutes Y_A. Thus busy/collision corners of the remaining bounded local coefficients survive the congruence. The signed individual differences `d_h,A=f_A-Phi_h*f_A` have a uniform local ratio `|d_h,A|<=C f_A` on affected animals; unaffected animals contribute zero. This supplies the local positive mass used in the Young estimates without pretending d_h,A>=0.

The ready-opening coefficient K>=0 can be singular. Comparing G_B with G_A does NOT imply a relative comparison of `Y_B^*K Y_B` with `Y_A^*K Y_A`. The supplied omission lemma repairs exactly this problem:
1. Delete the fixed catalog of gates touching supp(K), optionally with its bounded circuit cone. The rule is independent of A.
2. The remaining Yhat_A commutes K and has the same bounded-extension property.
3. For `Z_A=Yhat_A Y_A^{-1}`, local cancellation gives `||Z_A-I||<=C delta`.
4. Therefore

    +/-[Y_A^*K Y_A-K Ghat_A] <= C delta ||K|| G_A.

There is no inverse or spectral lower bound of K. Operator-valued full-animal completion proves `sum_A Ghat_A d_h,A>=0`; multiplying by commuting K preserves positivity. Restoring the deleted gates costs only O(t delta)W_G using the signed local ratio. This establishes the negative opening contribution modulo the explicitly budgeted local error.

## 7. Weighted Young estimates and anchor incidence
For each affected animal, apply Young after congruencing to its positive weight `f_A G_A`. The activity projections commute that weight, so all source/target corners are genuine orthogonal blocks. Local orbit ratios bound the signed d_h,A coefficient. This gives:

    t epsilon    cross: pair budget + C t^2 epsilon^2/(delta B) M_1,
    t epsilon^2  cross: pair budget + C t^2 epsilon^4/(delta B) W_G,
    t epsilon^3  cross: singleton budget + C t^2 epsilon^4/(delta A) W_G.

Own-C, missing-guard and singleton-swap errors cost C t epsilon^2 M_1. The chosen U(A) must include every h/j appearing in such a local error whenever Phi_h affects A; choosing a sufficiently large fixed anchor radius does so. The selected pair graph must include the actual overlapping pair {h,j}. These choices preserve bounded incidence and bounded change under adding a patch.

All summations then use each local incidence only a fixed number of times. No independent collision probability, no small-activity stationary distribution, and no |A|^2 factor is assumed.

## 8. Parameter compatibility is genuine
Fix physical rates, animal parameters/margins, code geometry and the activity witnesses first. Fix B and choose A large enough for the existing collision hierarchy. Let b=min_h b_h>0. All constants below may depend badly on those fixed choices.

Set `t=c epsilon^2`, `delta=d epsilon^2`. One explicit qualitative choice is

    c=rho^4 b,   d=rho^3 b

with rho sufficiently small relative to ALL fixed constants. Then

    c/d=rho,
    c^2/(cb)=rho^4,
    cd/(cb)=rho^3,
    d^2/(cb)=rho^2.

Thus singleton errors are absorbed because c/d is small, while t^2 and t*delta errors are smaller than the useful c b epsilon^4 coverage margin. There is also parameter room for a separately proved O((t+delta)^2) clean-side dirty-surgery cost; that room is not itself a proof of dirty surgery.

The activity idle source is d A epsilon^6; the Young ready sources are O((c^2/d)epsilon^6). After c,d are fixed, choose epsilon sufficiently small to absorb these into the useful epsilon^4 term, meet all gate/normalizer bounds, and satisfy the fixed coverage margin. All parameters remain strictly positive constants independent of volume and elapsed time. There is no accumulated simulation error.

## 9. Weighted coverage, including large containers
The original full-animal coverage proof uses two different completions. Both must be checked.

For bounded move completion, the extra exp(C delta |D_h|) factor is absorbed by the strict per-move ratio, retaining a fixed positive paying-animal charge in D_h^G.

For poor-component completion `A -> A union J_C`, the original exponent is `xi=alpha-(1-c)>0`, after choosing c near one. A container of size j costs at most exp(C delta j) in the controller weight, so the preimage bound becomes `2^j theta^(xi j) exp(C delta j)`. Reserving a strict part of the original exponent and taking delta small makes it summable exactly as before. Rich animals incur only the bounded move factor. Sparse animals gain at most exp(C delta |A|); the original sparse-entropy margin absorbs that too.

For an operator proof, fix a raw syndrome and an arbitrary controller vector u. The positive scalar values `<u,G_A u>` satisfy every required ratio. Apply each completion/counting step to these values. Since the resulting inequality holds for every u, it is a Loewner inequality. No simultaneous diagonalization of the G_A is used.

This yields

    sum_h D_h^G >= c_cov W_G-b_cov N I

on the accepted safe small-component/raw-sublevel basin, with changed fixed constants. It does not assert confinement or coverage for arbitrary large-error clean syndromes. Empty history-token/dummy vertices use the already accepted enlarged-graph constants.

## 10. The repaired basin-order step
The manuscript's last “apply positive T” step is valid only after specifying an invariant basin. A restriction to arbitrary small-component configurations alone is insufficient: a CP map might move their support outside the set where coverage was proved.

Choose the accepted raw-V sublevel projection P_raw whose sectors are guaranteed to have safe components. Every actual Phi_h has a deterministic raw-syndrome output, and the full untruncated raw animal potential weakly decreases on that output. Hence **each Kraus branch** of Phi_h preserves this sublevel. This deterministic output property is stronger than the mere inequality Phi_h*V<=V; the latter alone would not imply spectral-basin invariance.

The survival coefficient, readiness/history guards and virtual controller reset are DATA-independent. Their other branch uses the same Phi_h. Thus every useful CP factor preserves the raw basin in the Schrödinger picture. It also preserves the global all-good range by its local guarded construction. Their composition T_* therefore preserves the intersection of clean and raw-basin supports.

The effective drift inequality is consequently

    P [(T^{-1}L*T)V_G] P
      <= P[-a epsilon^4 W_G+b N I]P,

with P this intersection. For any state rho supported in P, T_*rho is again supported there; applying the inequality to T_*rho gives

    P L*T(V_G) P <= P[-a epsilon^4 T(W_G)+b N I]P.

Unitality of T handles the constant term. This is the exact clean-basin drift accepted here. It does not require a physical projection, discard a bath, or assert that T^{-1} is positive. Subsequent killed-basin/logical/noise composition remains a separate obligation.

## 11. Regression evidence
The new independent `check_operator_animal_charge.py` uses all seven animals of a three-vertex clique and noncommuting positive controller weights. All 22 strict-surplus moves give positive completed charges, also after a fixed controller-reset pullback. The controller weights genuinely fail to commute.

The same test exhibits the singular shortcut failure: for K=diag(1,0) and a small positive mixing gate, `det(Y^* K Y-0.9 K)=-0.0002601<0`, despite the nearby invertible G weights. The cavity difference divided by delta remains bounded (about 1.0172). This supports the exact omission proof, not a claim that singular factors can be divided out.

The author's 27-state one-way-commit fixture is a useful diagnostic of the raw first-order identity and t^2 remainder. It uses an abstract cleanup/reset model and direct dephasing, so it is not treated as physical-native evidence. The actual monitor/isolated structure was established analytically and in the separate prior actual-monitor regression.

## Remaining scope
This receipt closes the clean DATA/activity synthesis at the explicitly stated raw basin, including parameter compatibility and exact positive order transfer. It does not certify the separate full dirty cavity/surgery theorem, arbitrary common-bath noise once dirty sectors are populated, a barrier/stopping theorem for the final full observable, or noisy physical preparation/readout. No result from the old direct-family §5 is needed to justify this new proof.
