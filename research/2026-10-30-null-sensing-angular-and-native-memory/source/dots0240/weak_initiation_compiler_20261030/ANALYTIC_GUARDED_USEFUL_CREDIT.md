# Analytic guarded useful-DATA credit: actual construction and block orders
2026-10-30. Clean legal range only. The physical generator is the weak-first-edge / fast on-site acquisition-abort variant in `ONSITE_ABORT_BUSY_WITNESS.md`.

## 1. Actual payload and overlap graph
Use the accepted Tanner local orbit-minimizing idempotent CPTP recovery Phi_h. Its resource set contains the FULL raw-syndrome read footprint as well as every correction target. Join h,j whenever these resource sets intersect. Thus nonadjacent Phi_h,Phi_j commute as full channels, not merely on classical syndromes. In the legal forest frame the successful terminal gain is exactly J_clock,h(.)J_clock,h^dagger tensored with Phi_h. Acquisition abort and cleanup gains are DATA identity. This factorization is NOT asserted in malformed mask sectors.

Put d_h=(I-Phi_h*)V>=0 for the accepted full-animal potential. No claim is made that every individual animal factor is Phi_h-monotone.

## 2. Finite isolated normalizer required
Freeze every neighbor of h ready. The remaining isolated clock/lock/monitor system is finite. Delete only h's SUCCESSFUL terminal gains from its scalar clock generator and call the result K_h,epsilon. Retain all identity-DATA acquisition aborts and cleanup/ready returns. Let

  K_h,epsilon* R_h,epsilon=-I.

The construction below uses the following FINITE resolvent certificate:

  R_h,epsilon>=0;
  Rmax_h,epsilon=r_h,epsilon+C_h >= ||R_h,epsilon||;
  r_h,epsilon=c_h epsilon^(-2)+O(1), c_h>0;
  Ready R_h,epsilon Ready=r_h,epsilon Ready+O(1);
  Ready R_h,epsilon Busy=O(epsilon^(-1));
  epsilon^2 R_h,epsilon is analytic and covariant under clean activity parity.

All constants are local and volume independent. Root has proved this certificate exactly for its four-phase regenerative fixture. The new general native-chain proof is `GENERAL_ISOLATED_RESOLVENT.md`, now submitted for independent review: it checks the actual relative weak-hop monitor event, the simple idle monitor mode, and the absence of first-order coupling to the degenerate cleanup sector. No terminal tail with uncontrolled epsilon powers is substituted.

Choose beta_h=b_h epsilon^2 with b_h fixed and beta_h Rmax_h<=1/2, and set

  S_h=(1-beta_h Rmax_h)I+beta_h R_h,   B_h=I-S_h.

Then 1/2 I<=S_h<=I and 0<=B_h<=1/2 I. The Ready block of B_h is O(epsilon^2), its Ready/Busy block is O(epsilon), and it has a finite O(1) Busy limit. The exact killed drift is

  K_h* S_h=-(1-beta_h Rmax_h) A_terminal,h-beta_h I.

The completed excursion channel is generally p Phi_h+(1-p)Id and is NOT idempotent. Idempotence is used only for the successful Phi_h in this killed-event calculation.

## 3. Analytic CP credit without a principal-square-root singularity
The usual two-outcome credit with sqrt(B_h) need not be analytic at epsilon=0: B_h has zero eigenvalues in ready and post-terminal cleanup sectors, and its principal square root can contain |epsilon|. Do not infer odd/even Taylor orders from covariance alone in that formula.

Instead use a VIRTUAL controller reset in its B branch. On the isolated controller/data tensor product let E_ready(O)=<ready|O|ready>, retaining all DATA and spectator registers. A fixed ready density matrix may replace the vector. Define

  Q_h,epsilon(O)=sqrt(S_h) O sqrt(S_h)
                 + B_h tensor Phi_h*(E_ready(O)).       (3.1)

The second term means the tensor embedding of the positive controller effect B_h and the CP ready-evaluation/DATA map; it is a CP map. The first term is CP and analytic because S_h>=I/2. Both terms sum to I on I, so Q_h is unital CP. Formula (3.1) is analytic whenever S_h is, since its second term is LINEAR in B_h. It is covariant under clean activity parity if the ready state is parity invariant. No physical reset or measurement is being added: this is an observable-dressing map only.

For DATA-only V, exactly

  Q_h(V)=Phi_h*V+S_h d_h=V-B_h d_h.

Consequently, with Q_h,t=(1-t)Id+t Q_h and fixed 0<t<1/4,

  L_isolated* Q_h,t(V)
   =-[(1-t beta_h Rmax_h)A_terminal,h+t beta_h I]d_h.    (3.2)

The interpolation is unital CP and uniformly invertible as a LINEAR map (Neumann series around Id); no inverse-CP assertion is needed.

## 4. Actual local guard and full circuit
Let the guard require every overlap-neighbor of h to be ready. On this finite guarded sector the legal local controller space is isometric to the isolated h controller times spectators. Embed (3.1) through that isometry. Set S=I and the B branch to zero outside the guard; retain the sqrt(S) cross-sector action. Equivalently the B branch is the isolated-block CP compression, ready evaluation, and reinsertion. This makes a well-defined local unital CP map on the entire clean local clock space.

Order these guarded maps by a fixed finite coloring of their enlarged supports. Their composition T_epsilon is an exact bounded-depth unital CP circuit. Its maps are local, analytic, parity covariant and uniformly linearly invertible. The constants depend on finite neighborhoods, not system size or animal size.

At epsilon=0 the map is identity on every ready hub. It acts only on isolated busy hubs. Such hubs have pairwise disjoint full DATA footprints. Its virtual reset can erase an isolated busy hub, but cannot expose a previously blocked ACTIVE neighbor: an isolated busy hub has no active neighbor. Thus the ordered circuit at zero reduces, on each activity-mask block, to commuting isolated useful credits.

## 5. Earned low-order cancellation structure
Use a buffered local support X containing every guard and local generator term relevant to a linked contribution. Let I_X be its all-ready projection, C_X its collision projection (some ADJACENT pair both busy), and U_X=I-I_X-C_X. U_X includes arbitrarily many mutually nonadjacent busy hubs; it is not a global single-busy projection.

The following orders follow from the actual guarded construction, subject to the finite isolated normalizer in Section 2:

* **All-ready diagonal:** the epsilon^2 coefficient is exactly the sum of isolated useful terms -t b_h d_h. Cross-h contributions cannot return to the all-ready block at second order. Clean parity eliminates odd diagonal powers. The remaining local contribution is O(epsilon^4).
* **All-ready to collision-free busy:** the epsilon coefficient is the isolated cancellation (3.2), hence zero. Two distinct nonadjacent initiations at order epsilon^2 factor into disjoint isolated channels; their generator derivative again gives no all-ready/two-busy term at that order. Higher numbers of created offdiagonal busy labels need at least that many first-order factors. Therefore this block starts at O(epsilon^3).
* **All-ready to collision:** two neighboring initiations are necessary; this block is O(epsilon^2).
* **Collision-free busy corner:** retain the exact negative isolated terms from (3.2), including CP images under other disjoint useful credits. The remaining positive part is O(epsilon^2). It is important NOT to subtract only the epsilon=0 negative term and norm-bound its first derivative: derivatives of a negative CP family can be O(epsilon), while the whole family remains negative.
* **Collision-free busy to collision:** one weak initiation can make a neighboring pair, so the block is O(epsilon).
* **Collision corner:** a fixed O(1) local bound suffices.

Why there is no hidden O(1) sign problem: at epsilon=0, fast evolution of isolated transactions obeys (3.2); a return-ready event can only open additional useful credits, each mapping V to V-B_h,0 d_h<=V. If opening occurs for an active neighbor, the source already contains a collision and is charged there. Within the collision-free corner, opening concerns ready neighbors and their credit differs from identity only at O(epsilon^2).

These are LOCAL coefficient statements. Standard finite-depth linked expansion cancels disjoint circuit factors; every remainder term has fixed support/incidence and fixed local norm. When applied to the animal potential, relative local norms are supplied by the existing bounded-patch animal orbit estimate. A complete global DATA drift still has to combine these terms with the separately proved activity-weighted animal completion and dirty-sector surgery; this file does not silently perform that last combination.

## 6. Exact matching to the activity charge
The orders above are precisely compatible with the activity hierarchy:

  pair diagonal O(1) -> fixed pair credit;
  U/C cross O(epsilon) -> pair budget + O(epsilon^2) busy;
  I/C cross O(epsilon^2) -> pair budget + O(epsilon^4) ready;
  U/U positive O(epsilon^2) -> epsilon^2 singleton credit;
  I/U cross O(epsilon^3) -> epsilon^2 singleton budget + O(epsilon^4) ready.

A missing intended d_h service because a neighbor is busy is also an O(epsilon^2) busy-supported term, not an all-ready source. Only O(epsilon^4) remains in the all-ready sector, below the leading O(epsilon^2) useful drift. This is an exact local drift strategy, not a finite-time elimination error accumulated over memory lifetime.

## 7. Regression and boundaries
`check_guarded_data_blocks_analytic.py` computes the complete two-hub CP circuit and exact generator on a 12-state clean shared-lock model. It uses two NONCOMMUTING full-idempotent, monotone three-state DATA channels. The measured block powers match Section 5 down to epsilon=.003125; the collision-free busy positive block is nonzero O(epsilon^2), as allowed. The original principal-square-root variant is also retained for comparison.

This fixture is not the Tanner code or the full physical native compilation. It does not itself certify the native-chain normalizer (handled by the separate general proof), the full weighted basin, or dirty-sector compatibility. In particular full malformed-Hilbert activity parity is false in general and is NOT used here.
