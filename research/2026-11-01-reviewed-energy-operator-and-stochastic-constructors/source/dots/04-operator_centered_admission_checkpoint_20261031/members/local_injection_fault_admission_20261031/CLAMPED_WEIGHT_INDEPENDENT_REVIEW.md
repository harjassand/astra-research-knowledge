# Independent mathematical review: clamped source-creating fault admission

31 October 2026. Reviewer: continue_autonomous_control, distinct from the root construction author. Full actual source read and all displayed allocations reconstructed. Scope: concrete qubit model and initialized common-dilation inclusive amplitudes. No hardware, threshold-value, historical novelty or generic raw-operator compiler acceptance.

## Bound source and disposition

`CLAMPED_WEIGHT_INJECTION_CANDIDATE.md`, SHA256
`7b6d1e35a77432d8e9a8003c94fea4316a003dd8f2a1aefc053d62de6998fa24`.

**PASS under its stated model and the precise receiving readings below.** I found no load-bearing algebraic defect. In particular, the real outside creating interactions are not dropped, the weight jumps have the correct forward sign, and the simultaneous selected-history norm does not follow from an invalid product of marginal bounds.

## 1. Local block inequalities

Write the actual source-cell unwanted Hamiltonian as K=[[0,C^dagger],[C,D]], with ||C||,||D||<=c. The supplied full bound ||K||<=c is sufficient for both block bounds. K acts on this cell and the declared system patch/spectator, not on undeclared other guard charges.

For V=diag(I,(1+u)I), the real commutator i[K,V] has off-diagonal magnitude uC and zero diagonal. Factoring u, the proposed majorant has diagonal blocks alpha I and [alpha(1+u)+lambda/4]I, alpha=4c^2/lambda. Their scalar product is at least c^2. The operator Schur inequality therefore proves

  i[K,V] <= alpha u V+(lambda/4)u Q.

This remains true for operator-valued C on shared spectator/system space and arbitrary entangled input vectors. At u=0 both sides vanish. It is a genuine activation/loss tradeoff, not a bound by a global number of outside terms: the scalar is alpha*u, summed later through the weight's selected-volume estimate. With at most one active location per source, the quarter-loss is not spent multiple times at one time.

At a selected coordinate u=1 and |z|<=R, the exact upper-right block of i z* K V-i V z K is i(2z*−z)C^dagger. Its norm is at most3Rc. The QQ block is4 Im(z)D, bounded above by4Rc Q. The off-diagonal part is bounded by s_R V+(lambda/4)Q with s_R=36R^2c^2/lambda because

  s_R(2s_R+lambda/4) >= 9R^2c^2.

The cap R<=lambda/(16c) bounds the QQ diagonal by another lambda/4 Q. Transport contributes at most2 beta lambda Q on a clamped coordinate, at most lambda/4 Q for beta<=1/8. The full loss is -lambda Q, so these three allocations leave nonpositive slack. There is no derivative contribution on a clamped coordinate. Adding the positive real-activation allowance even on a selected coordinate is merely conservative; it does not spend another quarter-loss there.

## 2. Clamped supersolution and its discontinuities

In backward physical time, M=lambda[-3/4 I+diag(d)+B] is Metzler with row and column sums at most -lambda gamma0, gamma0=3/4−2 beta>=1/2. At a free coordinate first reaching1, its derivative is at most -lambda gamma0<0. A selected coordinate is held at1. Its compensating forcing is

  f_i=lambda[3/4−d_i−sum_j B_ij u_j],

which lies between lambda gamma0 and3lambda/4. It is zero off active selected coordinates. Thus both positivity and0<=u<=1 are justified, not assumed.

On entering a selected interval backward, the coordinate is raised by at most1. There are at most g|S| such impulses counted with multiplicity. At the same physical time viewed forward, this is a DOWNWARD jump of V. For a positive tilted state, Tr(V rho) consequently decreases there; this is the helpful direction for an upper comparison. A selected interval ending at the final computation time is handled by the terminal backward clamp followed by the forward drop to V(T)=I. Adjacent selected intervals may produce a zero-size impulse. Neither case requires removing the final interval or giving the final weight an uncharged value.

The variation-of-constants representation includes both the positive impulse measure and f. Column contraction gives the integral bounds, while the instantaneous forcing sum is at most(3lambda/4)g|S|. Specifically,

  sum u(initial) <= g|S| + (3/(4 gamma0))g|S|,
  integral sum u(t)dt <= g|S|/(lambda gamma0)
                          +3g|S|tau/(4 gamma0).

The impulse term in the first inequality is bounded by its total mass; the forcing term uses integration of exp(-lambda gamma0 t). The second follows by Fubini and total forcing-time mass at most(3lambda/4)g|S|tau. No exterior computation duration or source count enters these estimates.

## 3. Whole initialized dilation and controls

For free coordinates, the backward derivative cancels the transport and remaining3lambda/4 occupation drift after the real creating-interaction inequality. For selected coordinates, Section1 supplies the direct negative occupation slack. The remaining weighted growth is

  a_eff sum_i u_i(t) + s_R times number of active selected incidences
  +2R sum_selected ||Delta_l(t)||,

where a_eff=a+4c^2/lambda. Integrating and using V(initial)<=exp(sum u(initial))I proves the source's squared-dilation estimate with its displayed C0. This is uniform over arbitrary finite source/system/reference correlations. Shared spectators fit only with the supplied bounded coefficient/interaction-picture premises; the loss/injection fields remain initialized as specified.

All real unselected source-creating interactions remain ON. Their contribution is paid in a_eff. The source dissipator itself remains ON when a selected coupling is set to zero. The family W(z) is a single analytic jump-history dilation, not a separately chosen Kraus representation for each z. Bounded finite coefficients give a common compact-z history-sector majorant. Thus multivariate Cauchy extraction applies to the actual inclusive fault amplitudes.

Intended system-only Hamiltonians and coherently dilated system-only instruments commute with V. Their actual implementation, schedule, patch support, idle coverage and control residual assumptions remain those of the source. Arbitrary faulty source controls or omitted system-bath terms are not supplied by this review. Source-independent Delta_l commutes with V; a ground-block/system residual cannot be discarded as a mean.

The initialized-isometry scope is the one already received by ordinary inclusive-amplitude fault tolerance. This is not a norm statement for arbitrary incoming Markov fields or arbitrary extensions of the dilation to such fields.

## 4. Radius, physical units and unavoidable noise scale

Taking square roots and applying the Cauchy factor1/(R−1) gives exactly

  eta(R)=exp[C0/2+18R^2c^2g tau/lambda+R epsilon_ctl]/(R−1).

For the proposed minimum radius, the quadratic exponent is at most1/4 and the control exponent at most1/2. If R>=2, 1/(R−1)<=2/R, so the displayed max bound and its constants follow. With no control residual the added exponent can indeed be1/4 rather than3/4. The c=0 and zero-exposure cases must use their separate ordinary branches; the divisions are not interpreted there.

At fixed diffusion c=sqrt(lambda)b, the error scale includes b sqrt(g tau) and the activation a+4b^2. Increasing lambda alone does not remove that nonzero logical disturbance. At fixed physical c, suppression can scale with c sqrt(tau/lambda), in addition to the warm/transient c/lambda term. The physical loss, actual injection and all controls must still be acquired. No operating point or threshold is selected by this review.

## 5. Independent diagnostics, not numerical proof

`check_clamped_weight_independent.py` tests100 random operator-valued local Schur inequalities and three complete selected-history cross-Gram calculations for two lossy guards plus a system qubit. The selected source is used in two separated windows; both creating couplings, hopping, injection and a noncommuting intended system Hamiltonian stay ON between them. The diagnostic reconstructs W_a^dagger W_b through the COMMON jump cross-generator and sums the inclusive coefficients, rather than checking one reduced initial state.

At loss256,1024,4096 the computed inclusive amplitudes are approximately1.30e-4,3.63e-5,9.31e-6; the sufficient eta^2 bounds are approximately.0943,.0219,.00529. The small matrix exponential errors are not interval-certified, so these are only algebraic/implementation diagnostics. The operator proof above carries the result.

## 6. Acquisition and ordinary comparison boundary

This result genuinely differs from the previous annihilating-guard premise: an invertible X coupling has PXP=0 for the lossy ground but cannot satisfy XP=0. The existing raw common-kernel frontend therefore does NOT already implement this new certificate. A future frontend must acquire charge candidates from actual loss/return operators and verify the centered compression plus all clamped loss/activation allocations. It must pay finite search and UNKNOWN outcomes. No such executable generalization is accepted here.

Ordinary Gaussian-correlation and non-Markovian local-threshold theory remain strong comparators. This candidate supplies one non-Gaussian microscopic admission calculation under specific real loss/injection/locality premises, not a new definition of local noise, a new threshold theorem, or a historical priority conclusion. It does not reconstruct a useful logical task, hardware guard or FT consumer by itself.
