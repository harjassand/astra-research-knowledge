# Coefficientwise rooted moment family through repeated capture stages
30 October 2026, 17:22 UTC. Atomic receiving calculation supporting a signed-map moment-family norm. Quantum DATA is retained as arbitrary bath here; a quantum consumer witness is NOT silently appended.

For remaining good-phase records let Z_j(t)=1+K V_j(t) be the actual mixed/rooted test in its prescribed parameter and copy frame. Reserve fractions of the local negative drift for all noise and parameter derivatives. The previous root proof then gives constants gamma_j(t)>0 and z_*j(t)>=1 with z_*j<=M, where M=1+small is fixed independently of block size/stage count, such that the WHOLE subset family

 F_R(t)=product_(j in R) Z_j(t)

obeys, coefficientwise,

 (partial_t+L^*)F_R
  <=-sum_(j in R)gamma_j F_R
     +sum_(j in R)gamma_j z_*j F_(R without j).       (CF1)

This is not inferred from multiplying scalar expectations. Nominal moves act in one record, the rooted negative term is W_j>=V_j, and the bounded-leg product-orbit noise bound is absorbed BEFORE replacing K W_j by Z_j-1. Its constants are uniform in R. Atomic quantum read couplings are diagonal in classical Z and commute these tests, so Q may be an arbitrary retained bath. Complete-loss phase compression only subtracts positive outgoing gains because the tests commute the cuts (in the actual PRE frame during copying).

For a fixed interval, positive CP comparison of this cooperative subset system gives the OPERATOR inequality

 T^*F_R,out <=sum_(A subset R)
       [product_(j in A)a_j][product_(j in R without A)b_j] F_A,in,

 a_j=exp(-integral gamma_j),
 b_j=integral gamma_j(u) z_*j(u)
                  exp(-integral_(u to end)gamma_j) du.            (CF2)

The comparison can be proved by the finite triangular subset hierarchy and variation of constants; all off-diagonal coefficients are nonnegative. It assumes no independence of records or baths. Since z_*j<=M,

 b_j<=(1-a_j)M.

Thus initial JOINT bounds Tr(F_A rho)<=M^|A| imply the same bounds at the endpoint for every R. The normalized row sum is at most product_(j in R)(a_j+b_j/M)<=1. Stage pullbacks for soft attachment and graph copy are nonincreasing positive operator maps, so composition preserves the same invariant family. There is no multiplication of an A>1 marginal constant over log n stages.

Gamma and z_* may vary along the sharpening path. Use their actual values, not b_max/gamma_min, which could ruin the small ratio. One may equivalently use backward affine factors a_j(t)Z_j(t)+b_j(t)I for a fixed terminal test; the subset-family form is more convenient for a positive-block norm on signed components.

If phase weights are carried only on designated FUTURE-marked records D, their global phase transport adds a common integrating factor a_D(t) to every equation of this family. Divide it out before applying (CF2). The local phase/root joint-move identity preserves both budgets. The cost is the geometric pre-mark selected volume from GLOBAL_ATOMIC_PHASE_TRANSPORT.md, not the final volume of records that remain unmarked.

## Signed-map receiving scope
The root's proposed positive-block norm keeps positive Y_L,Y_R with [[Y_L,X],[X^dagger,Y_R]]>=0 and ALL moment-family bounds on Y_L,Y_R. Complete positivity plus (CF2) contracts that norm. Weighted cross-map/phase-drop estimates must be proved in this same norm; a statement only about one positive marginal is insufficient.

For a fixed terminal marked set D inside a tested set S, only paths through subsets of D contribute to v_D. Records S without D remain phase-killed throughout but need ROOT-ONLY metrics, while records in D carry the extra phase metrics until their own marks. This is the intended way to avoid an exp(n_final) unmarked phase-weight factor in final-port tail estimates. A compatible insertion bound and the actual final instrument remain necessary.

## Quantum consumer caveat
If F_Q is multiplied into the test, every unmarked boundary record that drives a quantum hub needs its rooted credit. A family omitting such a record cannot pay its wrong-read perturbation. Therefore (CF1) must not be relabeled a quantum-consumer family. One possible larger receiving norm uses a BASE softened joint quantum witness containing all unmarked boundary-port factors, with additional subset factors only for final read tails; that composition requires its own operator proof.
