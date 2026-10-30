# Clean native weak-initiation effective drift: explicit first-order construction
2026-10-30. New synthesis candidate for independent review. This uses actual native phase structure and an exact LOCAL similarity; it is not a finite-time adiabatic-elimination estimate. Full dirty-sector surgery remains separate.

## 1. Fixed apparatus and earned inputs
Use the exact weak-first-acquisition / complete A_i>=1 abort apparatus of `ONSITE_ABORT_BUSY_WITNESS.md`, on its all-good forest-frame range. Later rates may be small but are fixed independently of epsilon. The canonical payload is the accepted idempotent Tanner orbit-minimizing Phi_h, including the full raw-syndrome read footprint.

Use the general isolated resolvent from `GENERAL_ISOLATED_RESOLVENT.md`, the analytic guarded CP map Q_h from `ANALYTIC_GUARDED_USEFUL_CREDIT.md`, and the reviewed activity witnesses/products. Write beta_h=b_h epsilon^2, with fixed min_h b_h>0. All clean controller coefficients are DATA independent; this does not extend automatically to malformed masks.

For each animal choose the fixed globally ordered activity circuit Y_A, G_A=Y_A^dagger Y_A, and V_G=sum_A G_A f_A, W_G=sum_A |A|G_A f_A. Choose anchors/selected physical-overlap pairs with the bounded-extension property in the native constructor's `ANIMAL_LOCAL_ACTIVITY_WEIGHT_CHARGE.md`.

That operator-valued completion lemma gives both nonpositive clean terminal DATA drift for V_G and nonnegative

    D_h^G=(I-Phi_h*)V_G.

The reviewed controller hierarchy, weighted by that lemma, supplies negative singleton/pair charges of sizes delta A epsilon^2 and delta B, with idle source O(delta A epsilon^4)W_G.

## 2. Exact C-family structure removes the apparent inverse-positivity trap
The full isolated K_epsilon* preserves the operator algebra block diagonal in the three blocks (I direct-sum A), C, Q. Coherent initiation connects only I/A. Every inter-family connection is a separately resolved irreversible reset. Starting from I, its resolvent therefore has NO (I/A)-to-C or Q-to-C coherence, for any epsilon.

Moreover R_C is the mean lifetime for the fast committed C chain killed at its terminal. It is exactly independent of epsilon and uniformly bounded. Put

    s_h,epsilon=1-beta_h Rmax_h,epsilon >=1/2.

Then exactly

    S_h|C=s_h,epsilon I_C+beta_h R_C,
    sqrt(S_h)|C=sqrt(s_h,epsilon)I_C+O(epsilon^2).

Let A_h be the successful terminal intensity, supported in C. The virtual-ready-reset gain of Q_h(A_h d_h) is zero, and the square-root branch gives

    Q_h(A_h d_h)=s_h,epsilon A_h d_h+beta_h E_h d_h,    (2.1)

where E_h is Hermitian, supported in C, and has a fixed norm bound. This is an exact definition of E_h, not a truncated equality; boundedness follows by the uniformly Lipschitz square root on S>=I/2.

The isolated exact DATA credit says L_h*Q_h(V)=-s_h,epsilon A_h d_h-beta_h d_h. Since L_h*V=-A_h d_h, equation (2.1) proves

    [L_h*,Q_h]V=-beta_h d_h+beta_h E_h d_h.            (2.2)

Thus the positive error is O(epsilon^2) on a BUSY C source. There is NO unpaid O(1) own-terminal error from applying the inverse circuit. This is stronger and simpler than transferring positivity through T^{-1}.

## 3. Other first-order commutators are explicit
Let G_h^ready be the guard that all overlap-neighbors of h are ready.

* Own h terms commute the guard. Their contribution is G_h^ready times (2.2).
* A neighboring successful terminal leaves its owner busy (C->Q). The h-credit is exactly identity on both source and target, so its commutator on V is ZERO.
* Other fast neighbor terms preserve busy/ready status and cannot change the enabled isolated block; their commutators on V vanish.
* A neighbor's DATA-free ready return can open h's guard. It contributes

      -J_ready^dagger B_h(out) J_ready d_h <=0.

  This is a negative operator because B_h>=0 and d_h>=0; no sampled clock path is invoked.
* Disjoint generator/credit pairs commute as superoperators, since the graph contains FULL read/write footprints.
* A neighboring weak initiation contributes exactly

      -i epsilon [H_j,B_h^guard] d_h.                 (3.1)

The own-ready/busy blocks of B_h have norms O(epsilon^2), O(epsilon), O(1). Since H_j toggles only P_j and h/j are adjacent, (3.1) has: O(epsilon) independent-busy/collision blocks; O(epsilon^2) ready/collision and singleton-swap blocks; O(epsilon^3) ready/singleton blocks. All coefficients are bounded local operators.

Replacing G_h^ready d_h by d_h loses only an O(epsilon^2) term supported on a nearby busy flag. The existing bounded-patch animal mass estimate charges both this missing service and the E_h term to singleton activity mass.

## 4. Exact finite-depth similarity and its generic remainder
Set Z_h=Q_h-Id and use the interpolated factors Id+t Z_h, ordered by a fixed finite support coloring. For t<1/4 they are unital CP and uniformly linearly invertible. Let T be their bounded-depth product. Exact local conjugation gives

    T^{-1} L* T=L*+t sum_h[L*,Z_h]+R_t,

where R_t is a bounded-incidence sum of fixed-support HP identity-annihilating maps with local cb norm <=C t^2. This is an exact identity at fixed parameters, uniformly in time and volume. No global generator norm appears.

For each animal, conjugating a local remainder through Y_A involves only a bounded number of nearby gates; all disjoint gates cancel. Therefore R_t(V_G)<=C t^2 W_G in the direct nonunital relative norm.

## 5. Moving the first-order recovery calculation through animal-local weights
For any fixed local commutator F_h=[L*,Z_h],

    Ad_(Y_A)^{-1} F_h Ad_(Y_A)-F_h

has local relative norm O(delta), because only a bounded number of nearby activity gates remain after cancellation. Summing over animals and incident local terms costs O(t delta)W_G, not ||G_A-I|| and not |A|^2. This is an operator-map comparison; no global expansion of G_A is used.

The principal negative -beta_h d_h becomes -beta_h D_h^G. Activity projections commute every Y_A, so all busy/collision error blocks retain their flag corners and are paid by the existing weighted charges.

One additional sign subtlety must be handled: weights Y_A^dagger K_h Y_A on the negative ready-opening term do NOT inherit a relative comparison merely from G_B≈G_A when K_h is singular. Remove the boundedly many activity gates in K_h's support and their finite circuit cone. The remaining outer weight Ghat_A commutes K_h and still satisfies the same bounded-extension comparison. Operator-valued full-animal completion then proves the negative sign for K_h Ghat_A. Restoring the omitted gates costs only the already allowed O(t delta)W_G. Thus no invalid order comparison through a singular K_h is used.

## 6. Weighted Young budgets
Let M_1 and M_2 denote the local weighted singleton and adjacent-pair masses paid by the activity drift. Before generic remainders, equations (2)-(3) yield useful loss -t beta_min sum_h D_h^G, plus:

* O(t epsilon^2) M_1 (own C error, missing guards, and singleton swaps);
* pair/single cross of size O(t epsilon), paid by delta B M_2 plus O(t^2 epsilon^2/(delta B))M_1;
* ready/pair cross O(t epsilon^2), paid by pair budget plus O(t^2 epsilon^4/(delta B))W_G;
* ready/single cross O(t epsilon^3), paid by delta A epsilon^2 M_1 plus O(t^2 epsilon^4/(delta A))W_G.

Bounded patch completion converts each d_h-bearing local error to the relevant local weighted mass with uniform constants. No independent-density or stochastic-collision assumption is used.

## 7. Compatible fixed parameters, including room for dirty surgery
Use the rate hierarchy suggested by root:

    t=c epsilon^2,    delta=d epsilon^2,
    c << d << sqrt(c b_min),

with the inequalities strengthened by the finite local/coverage constants. Choose B fixed and A large enough for the pair-to-single activity hierarchy. Choose c small relative to b_min, then d between the corresponding constant multiples of c and sqrt(c b_min), and finally epsilon small.

Useful service has scale c b_min epsilon^4. Generic t^2 and mixed t delta remainders have coefficients c^2 and cd at epsilon^4 and are absorbable. This also leaves room for an independent dirty-surgery clean-side cost O((t+delta)^2), since d^2<<c b_min. Activity's idle source is now d A epsilon^6. The weak cross ready sources are O((c^2/d)epsilon^6), while all singleton errors are absorbed by d A epsilon^4 using d>>c and A sufficiently large. Pair service is d B epsilon^2 and is stronger still.

All choices are fixed numbers independent of volume and memory time. There is no accumulated approximation error.

## 8. Result and precise remaining boundary
Subject to the reviewed weighted SSF/FGL coverage with the activity circuit's small exponential-per-added-vertex comparison factor, the preceding clean local inequalities give

    (T^{-1}L*T)V_G <= -a epsilon^4 W_G+b N I

with a>0 independent of volume. Applying the POSITIVE unital T gives the exact clean-range drift

    L* T(V_G) <= -a epsilon^4 T(W_G)+b N I.

The weighted coverage is stable under the local G_B/G_A comparison by reserving the usual animal exponent margin; for large component completions the extra cost is exp(C delta times added size), not an uncontrolled global condition number.

This closes the CLEAN native acquisition/service mechanism at the level of a synthesis candidate requiring independent review of Sections 3-6. Full-Hilbert dirty surgery, its actual transformed-generator compatibility, basin stopping, and the final logical interface must still be combined separately. The clean scalar-clock factorization and clean parity are not asserted on malformed masks.
