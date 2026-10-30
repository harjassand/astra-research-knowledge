# Exact local collision charge for weak initiation
2026-10-30. New derivation. No finite-time elimination, no threshold assertion.

## Useful result
Weak initiation can be charged at **fourth**, rather than second, order in the all-idle sector if one gives overlapping activity an order-one credit but singleton activity only an order-epsilon-squared credit. This is an exact operator inequality at fixed epsilon. The local positive credit also admits a finite-depth multiplicative packaging, avoiding the known linear-credit |A|^2 noise defect; see `MULTIPLICATIVE_ACTIVITY_WEIGHT.md`.

The result does not establish useful DATA service. The isolated useful transaction resolvent is treated independently by root in `producer-workspace/local_resolvent_credit_root_20261030`. Combining that credit with this collision weight, including all cross terms and dirty-reset charge, remains necessary.

## Hypotheses (all substantive)
Let L0 be the fast generator with initiation disabled. There are commuting activity projections P_h such that:

1. Its Hamiltonians commute every P_h. Its separately resolved reset channels never create any P_h, and preserve the algebra block diagonal in their joint eigenspaces. In particular the complement of every P_h is absorbing.
2. There are finite-support Hermitian witnesses X_h with constants c,C>0 independent of h and volume:

   c P_h <= X_h <= C P_h,
   [X_h,P_j]=0 for all j,
   L0* X_h <= -P_h.

3. X_h supports have bounded radius and bounded incidence. A weak initiation is epsilon V*, where V* O=i[sum_h H_h,O], ||H_h||<=J, supports have bounded incidence, and [H_h,P_j]=0 for j != h. It may toggle P_h and may have a component inside P_h. Rates and constants are fixed independently of epsilon and system size.

These hypotheses are not inferred from a stationary low activity distribution. All inequalities hold on arbitrary states, including coherent/entangled activity sectors.

## Projection-product lemma
If P is a noncreating activity projection and X>=0 commutes P, then

   L0*(PX) <= P L0*(X) P.

Here the RHS and LHS are regarded on the P corner; the LHS vanishes on its complement. To see this, split each jump J into active/inactive blocks. No creation gives P J (1-P)=0. The gain retained by L0*(PX) omits the positive contribution

   (1-P)J P  adjoint  X_(1-P)  (1-P)J P

that appears in P L0*(X)P. The Hamiltonian and loss parts agree. Block-algebra preservation excludes unwanted cross blocks. The same statement applies to any product of the commuting P_h.

Consequently, for each selected adjacent pair e={h,j}, choose an orientation and put

   Y_e=P_j X_h.

Then c P_hP_j<=Y_e<=C P_hP_j, all activity projections commute Y_e, and

   L0*Y_e <= -P_hP_j.

No separate two-owner hitting-time theorem is required.

## Exact two-level hierarchy
For a bounded-degree selected pair graph E, define

   F_epsilon=A epsilon^2 sum_h X_h+B sum_(e in E)Y_e.

There are fixed constants A,B,c1,c2,C0 and epsilon0>0 such that for 0<epsilon<=epsilon0,

 (L0*+epsilon V*)F_epsilon
 <= -c1 A epsilon^2 sum_h P_h
    -c2 B sum_(e={h,j})P_hP_j
    +C0 A epsilon^4 N I.

A can be chosen after B, sufficiently large relative to B and the local incidence constants. The result is uniform in time and volume.

### Proof and order bookkeeping
The fast terms give the displayed negative terms with c1=c2=1 before allocating budgets.

For X_h, an initiation H_k with k!=h commutes P_h, so its commutator remains supported in P_h. Its contribution is O(A epsilon^3)P_h and is absorbed for small epsilon. The own initiation gives an active/idle offdiagonal block of norm O(A epsilon^3). Block Young, allocating O(A epsilon^2)P_h, leaves only O(A epsilon^4)(1-P_h).

For Y_{hj}, initiations other than h,j keep the pair corner fixed, giving O(B epsilon)P_hP_j. Initiation h has cross blocks between P_hP_j and (1-P_h)P_j, and initiation j is symmetric. Allocate a fixed fraction of B P_hP_j to block Young. The remainders are O(B epsilon^2)(P_h+P_j), NOT an identity term. Bounded pair degree and A sufficiently large absorb these into A epsilon^2 sum P_h.

All operators involved are local; the sum of incident norm constants is volume independent. This proves the inequality directly, without any stochastic-jump interpretation of the coherent initiation.

## Meaning and limitation
For a stationary state this bounds total pair activity by O(epsilon^4 N) and total singleton activity by O(epsilon^2 N). A transient integrated version follows by integrating the exact drift. Neither conclusion is a local-stochastic bound for all specified activity sets, nor a data-memory theorem.

A direct sum of F_epsilon times each animal weight would add an unwanted |A| factor and can produce |A|^2 perturbation sensitivity. Do not use that linear packaging. The companion positive finite-depth product is designed to avoid it.

## Regression
`check_collision_hierarchy.py` checks the exact dense-matrix inequality on paths of 2 through 6 independently reset qubits, with A=128, B=1, C0=8 and five epsilon values from .001 to .05. All 25 inequalities pass. This checks the Young hierarchy in a simple model, not the transactional compiler hypotheses.
