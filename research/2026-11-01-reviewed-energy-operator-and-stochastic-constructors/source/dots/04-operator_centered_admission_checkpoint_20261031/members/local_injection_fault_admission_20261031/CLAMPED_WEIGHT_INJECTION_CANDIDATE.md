# Local source-creating interactions: clamped-weight candidate

Status: fresh ROOT derivation, UNREVIEWED. Intended to close the fixed-diffusion/source-creation gap without pretending its leading logical disturbance vanishes. This is not a new threshold or physical implementation claim. It uses ordinary inclusive fault amplitudes and the previously constructed common jump-history/Cauchy interface.

## 1. Model and distinction from the received guard theorem

Source qubits have positive loss rate lambda>0, nonnegative injection rate at most a, and coherent hopping lambda J on a graph with absolute incident sums at most beta<=1/8. A shared spectator may be present if its independent evolution and all charge-preserving real terms obey the already stated interaction-picture/domain premises. Markov loss/injection input fields are initialized; arbitrary finite source/system/reference initial correlations are allowed.

Each circuit location has duration at most tau, uses at most g source qubits, and each source belongs to at most one active location. For each assigned source cell at a location, combine ALL its unwanted terms into one Hermitian operator K_i(t); c bounds the norm of this TOTAL operator, not each member of an uncharged sum. The fixed schedule and source-cell sets are common to all controlled branches, and the same c bound holds uniformly on their retained control-register blocks. Each such aggregate operator has norm at most c. In local source blocks P=|0><0| and Q=|1><1| it has form

    K_i = [[0, C_i^dagger], [C_i, D_i]],
    ||C_i||,||D_i||<=c.

System/spectator coefficients can be noncommuting; system support is the actual bounded gate patch. Unlike the received theorem, K_i MAY CREATE source excitations. Only the ground compression P K_i P is zero. A ground-block residual is not free and would need an additional unprotected-error budget or an actually acquired target Hamiltonian. All real unselected interactions remain ON. Optional source-independent integrated local mismatch is epsilon_ctl.

Set b=c/sqrt(lambda) merely to compare with the fixed-diffusion convention c=sqrt(lambda)b. This is not an assumption that increasing loss must increase an actual coupling.

## 2. Real outside creation is a paid activation rate

For V_u=product_i(I+u_i n_i), 0<=u_i<=1, the real commutator from K_i has only off-diagonal source blocks, proportional to u_i C_i. The elementary2x2 operator Schur bound gives

    i[K_i,V_u] <= (4c^2/lambda) u_i V_u
                    +(lambda/4) u_i n_i V_rest.

Indeed, after factoring u_i V_rest, the diagonal majorant has entries alpha and alpha(1+u_i)+lambda/4 with alpha=4c^2/lambda, and their product is at least c^2. The same operator bound holds for arbitrary bounded system/spectator coefficients C_i, by the block norm inequality. D_i commutes with the charge weight.

Thus all real unselected source-creating couplings can be retained by spending one quarter of the local loss and using

    a_eff=a+4c^2/lambda.

This is a local activation budget, not an exterior-volume constant. It must be paid in the final bound.

## 3. Clamp selected source weights rather than divide by a vanishing u

Introduce complex parameters z_l for selected locations, |z_l|<=R. For a selected active source set u_i=1 during its whole selected interval. At a selected interval's endpoint in BACKWARD time, raise u_i to1 if necessary. Between such intervals, unselected coefficients follow

    du/ds=M u,  M=lambda[-(3/4)I+diag(d)+B],

except that selected active coordinates remain clamped at1. Here s is ordinary backward PHYSICAL time, B_ij=|J_ij|, d_i=sum_j B_ij. Define

    gamma0=3/4-2beta>=1/2.

M is Metzler and its row/column sums are <=-lambda gamma0. Starting from zero at the final time (with any terminal selected clamp immediately before it), the piecewise construction has0<=u_i<=1. A free coordinate reaching1 has negative derivative; a clamped coordinate is exactly1. All forward-time discontinuities of V are DOWNWARD, so they help, rather than invalidate, the weighted evolution comparison.

Equivalently, outside the jumps,

    du/ds=M u+f(s),

where f_i is zero off active selected coordinates, and on a clamped coordinate

    0<=f_i=-(M u)_i<=3lambda/4.

There are at most g|S| unit coordinate jumps, counted with multiplicity across selected intervals, and total active selected space-time volume at most g|S|tau. Hence positivity/column contraction imply

    sum_i u_i(0) <= g|S|[1+3/(4gamma0)],
    integral_0^T sum_i u_i(t)dt
       <=g|S|[1/(lambda gamma0)+3tau/(4gamma0)].          (1)

The first bound uses total impulse mass and the instantaneous forcing bound; the second integrates their decaying convolutions. These bounds are independent of total source size, exterior computation time and gaps between selected locations.

## 4. Complex selected creation uses local loss and an R-squared cost

At a selected source u_i=1, V_local=diag(I,2I). Its complex Hamiltonian contribution to the weighted norm generator is

    i z* K_i V_local-i V_local z K_i.

The off-diagonal block has norm at most3Rc. The QQ diagonal block is at most4Rc I_Q. Apply the operator Schur bound to the off-diagonal block with allocated QQ cost lambda/4. This contributes a scalar cost

    s_R=36 R^2 c^2/lambda

times V_local, plus(lambda/4)Q. If

    R<=lambda/(16c),

the QQ diagonal term costs at most another(lambda/4)Q. Hopping costs at most2beta lambda Q, which is at most(lambda/4)Q. Against the full selected-site loss -lambda Q, the remaining occupation coefficient is nonpositive. No derivative is required on a clamped selected coordinate. Injection is already bounded by a_eff u_i V, conservatively including its real-creation allowance even on selected cells.

For unselected coordinates, the real-creation bound of Section2 and the hopping inequality are canceled by the free M evolution. Real source-independent controls and all other admitted commuting terms cost no weight growth; selected control mismatch costs2R||Delta_l|| V.

## 5. Whole dilation and inclusive amplitude

Let

    C0=g[1+3/(4gamma0)]
       +a_eff g[1/(lambda gamma0)+3tau/(4gamma0)].

The common analytic jump-history dilation then obeys

    ||W(z)||^2 <=exp{|S|[C0+36R^2 c^2 g tau/lambda
                              +2R epsilon_ctl]}.

As before this is an initialized-isometry norm statement, not a classical source-path expectation or arbitrary input-field unitary norm. Reference extensions are automatic. Multivariate Cauchy extraction therefore gives

    ||E(S)|| <=eta(R)^|S|,
    eta(R)=exp[C0/2+18R^2 c^2 g tau/lambda
                     +R epsilon_ctl]/(R-1),
    1<R<=lambda/(16c).                                  (2)

This pays the nonzero leading noise: in the fixed-diffusion convention c=sqrt(lambda)b, the R-squared term is18R^2 b^2 g tau, which does NOT vanish as lambda increases. The theorem cannot make an O(b^2 tau) effective dissipator disappear.

A simple sufficient choice, when it is at least2, is

    R=min(lambda/(16c), sqrt(lambda)/(sqrt(72)c sqrt(g tau)),
          1/(2 epsilon_ctl)),

with the last cap omitted if epsilon_ctl=0. It gives

    eta <=2 exp(C0/2+3/4)
             max(16c/lambda, sqrt(72)c sqrt(g tau/lambda),
                 2 epsilon_ctl).

For epsilon_ctl=0 the exponent3/4 can be replaced by1/4. This is a conservative sufficient amplitude, not a threshold value or optimized cost. Degenerate c=0 or tau=0 cases are handled separately by ordinary control-only/no-exposure reasoning, not division by zero.

## 6. What must be independently checked

The clamped-weight supersolution is the central unfinished proof obligation: signs at weight jumps, the selected-coordinate loss allocation, column-convolution bounds and the simultaneous common-dilation receiving must all be audited. No local classical trajectory or product of marginal errors is being assumed. The selected weights depend on S only in the proof, not on a physical source monitor or exponential algorithm performed by the device.

The source-creating interaction is in the actual unwanted Hamiltonian and is complexified with its location; it is NOT moved into an uncounted source generator. All real outside creating interactions enter a_eff. An unguarded PP interaction remains ordinary unsuppressed noise, not a mean that can be silently removed.

If correct, the result would address the earlier gap: fast non-Gaussian quantum sources with centered creation interactions can supply a local all-order fault amplitude at the actual diffusion/activity scale, rather than at the large instantaneous Hamiltonian norm. Strong Gaussian-correlation and existing microscopic noise-admission methods remain mandatory comparisons. Historical novelty, physical realization and a useful hardware regime are unestablished.
