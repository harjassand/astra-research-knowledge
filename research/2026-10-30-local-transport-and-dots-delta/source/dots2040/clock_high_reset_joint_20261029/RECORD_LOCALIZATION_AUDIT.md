# Weighted-coefficient audit of finite-window record localization

This note audits the parent's proposed spatial localization bound. It is a conservative fixed-window/fixed-region estimate; its exponential dependence on monitored spacetime volume is not a threshold-level product-fault theorem.

Let X be the monitored set, |X|=r. For each nonidentity basis string B_S, weight its coefficient by

 w_a(S)=exp[a max_{y in S}dist(y,X)],     w_a(empty)=1.

Let C=C(D) be the unweighted Hamiltonian column bound, and assume

 lambda_a=kappa/2-Cg exp(2a)>0.

A guarded-drive star intersecting S can enlarge max-distance by at most two. Thus the weighted full generator logarithmic norm has weighted-support loss at least lambda_a W_a. A monitored jump at x in X inserts n_x only on strings having I at x, and does not increase w_a; its weighted coefficient norm is at most kappa.

## All-record majorant

Unravel only the r monitored jumps, retaining all other emissions in the generator. Each branch is a word of monitored jump labels and their ordered times, separated by killed semigroups K*=L*-sum_{x in X}J_x*. Sum absolute weighted coefficient norms over all branches. This can be defined first by the finite jump-number Dyson expansion, then by its absolutely convergent limit.

Removing the monitored J terms from L costs at most kappa r in the coefficient norm; inserting/summing monitored jumps costs another kappa r. Consequently the resulting positive coefficient majorant obeys

 F_a'(s)<=-lambda_a W_a(s)+2kappa r F_a(s),   F_a(0)=1.

Here W_a includes support-size times the weighted absolute coefficients over the same branches. Multiplying by exp(-2kappa r s) and integrating gives

 integral_0^h exp(-2kappa r s)W_a(s)ds <=1/lambda_a.       (1)

The same majorant bounds any selected record event, but it is important to use the all-record majorant before selecting the event: independently taking norms of record effects after cancellations need not satisfy the differential inequality.

## Comparison with a graph cut

Let B_R(X) be the retained neighborhood and compare the full graph with the graph obtained by removing edges across its boundary. Extend the cut dynamics to the exterior as well; do NOT discard an extensive exterior generator. Both full and cut dynamics have the same on-site damping. Only boundary Hamiltonian stars differ.

Their generator difference Delta annihilates all basis strings whose support lies strictly within distance R-2 of X. A safe column bound is

 ||Delta A||_c <=2Cg exp[-a(R-2)] W_a(A).                 (2)

The factor 2 allows both full and modified boundary stars. The precise integer offset can be improved with a boundary convention, but R-2 is conservative for star interactions of graph diameter two.

Duhamel expansion on the record-valued instrument inserts Delta at time s. The remaining unweighted record-branch propagator has norm at most exp[2kappa r(h-s)]. Summing absolute differences over output records and applying (1),(2) gives

 total record coefficient discrepancy
 <=(2Cg/lambda_a) exp[2kappa r h-a(R-2)].                 (3)

Therefore, for any initial state and any event B of the monitored record during [0,h], its probabilities under the full and cut dynamics differ by at most the right side of (3), capped at one. The derivation also bounds the l1 discrepancy of the full classical record distributions, conservatively without a factor 1/2 improvement.

## Consequence from all-ready initial state

If several monitored regions have pairwise disjoint retained neighborhoods, cutting all boundaries makes their record laws independent from the all-ready product state. Applying (3) with their union as X yields an additive approximation of their joint event probability by the product of their cut-neighborhood event probabilities. The bound is useful for fixed number/size/duration of regions as separation R grows.

Caution: the displayed error grows as exp(2kappa r h) in total monitored size. Even a sharper linear-in-r localization error would remain additive unless further work establishes relative/all-orders control. Neither (3) nor ordinary spatial clustering permits claiming P(all m sites miss their window)<=p^m uniformly in m.
