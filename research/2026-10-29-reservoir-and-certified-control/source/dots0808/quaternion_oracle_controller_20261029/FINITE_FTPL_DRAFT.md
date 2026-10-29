# Finite perturbed-leader controller using certified quaternion optimization
2026-10-29. New author derivation, review pending. A finite complete oracle contract is supplied by QUARTIC_ORACLE_v1.md; fast SOS success alone is insufficient. This draft is a fixed-comparator controller, not yet a drift-tracking replacement.

## Feature and feedback bounds
Letphi(q) contain the35 degree4 monomials of a unit quaternion. Setx(q)=(phi(q)+1)/2, soK={x(q)} is compact in[0,1]^d,d=35. Convexity ofK is unnecessary for linear minimization; a returned action is always an actual rational-unit-quaternion rotation, not a convex combination requiring SDP rounding.

Subtract the known action-independent3/4 from the one-shot loss estimator. Its homogeneous polynomial is
 hhat(q)=−(9/4)yz Q(q)R_ab(q)−(81/4)yzuv R_ab(q)R_cd(q).
The coefficient l1 norm is at most360, becauseQ,R_ab each have coefficient l1 norm at most4. Therefore ghat=2 coeff(hhat) has||ghat||_1<=L0=720 and ghat dotx differs fromhhat by an action-independent constant.

With probe probabilityp, useg_t=1_probe ghat_t/p and0 for other roles. Conditional on the actual past, this feedback is independent of the current perturbation/action: probe inputs/settings do not depend on the chosen candidate, the source map is fixed before private controls, and service/validation feedback iszero. Its conditional mean produces the actual current delta loss up to the cancelling constant. MoreoverE||g_t||_1<=L0 andE||g_t||_1²<=L0²/p. All role-specific capped keys must use the accepted neutral pre-role schedule.

## Ideal uniform smoothing and exact-optimizer regret
Writephi0(w)=min_{x inK}w dotx, andPhi(w)=E_Z phi0(w+Z), whereZ is uniform on[-R,R]^d. Uniform-box convolution gives a differentiable concave potential with
 gradPhi(w)=E_Z argmin_x(w+Z)dotx
(up to irrelevant null sets/ties). Translation total variation is at most||v||_1/(2R). Since each action coordinate lies in[0,1],
 ||gradPhi(w+v)−gradPhi(w)||_infinity<=||v||_1/(2R).
Integration alongg gives
 <gradPhi(w),g> <=Phi(w+g)−Phi(w)+||g||_1²/(4R).
LetG_t=sum_{r<=t}g_r. For fresh independent perturbations each round, the current feedback independence above permits conditional expectation, even though the future source and future losses depend on past actual actions. Telescoping yields expected regret to ANY fixedx* inK at most
 dR/4 +T L0²/(4Rp).
IndeedPhi(G_T)<=G_T dotx* bymean-zeroZ, and−Phi(0)<=dR/4. This is actual-history external regret, not counterfactual policy regret or a hindsight-selected frame claim.

## Approximate certified minimizers: explicit bias, not an assumed T epsilon term
Suppose a measurable action mapx_tilde(w) satisfiesw dotx_tilde<=phi0(w)+epsilon at every input. For any coordinatei andh>0, approximate optimality implies
 [phi0(w+h e_i)−phi0(w)−epsilon]/h <=x_tilde_i(w)
 <=[phi0(w)−phi0(w−h e_i)+epsilon]/h.
Averaging over uniformZ and using the preceding gradient Lipschitz bound gives
 |E x_tilde_i(G+Z)−partial_i Phi(G)|<=epsilon/h+h/(4R).
Chooseh=2sqrt(R epsilon). Thus the additional expected loss per round is at most||g_t||_1 sqrt(epsilon/R). This argument requires only a globally certified additive objective gap, not a stable numerical argmin or unique frame.

## Finite-bit perturbations and rational physical candidates
Draw each perturbation coordinate uniformly from theM midpoints of[-R,R], withM a power of2. Coupling to ideal uniformZ gives coordinate rounding error<=R/M. An oracle with gap epsilon_oracle at the rounded input is an epsilon_total-optimizer at the ideal input, where
 epsilon_total<=epsilon_oracle+dR/M.
The additive constant inw dotx means the actual quartic query is(1/2)sum_j w_j phi_j(q). The exact SOS/grid oracle therefore supplies precisely the required gap. It returns a rational unit quaternion, hence an actual local rotation.

Choose rationalR within a factor2 ofL0 sqrt(T/(dp)), epsilon_oracle=R/(4T²), and power-of-twoM>=4dT². Thenepsilon_total<=R/(2T²), and the total approximate/rounding regret allowance is at mostL0. A conservative resulting per-edge true-delta bound is
 E sum_t delta_t(C_t) <=E sum_t delta_t(C*) +L0 sqrt(dT/p)+L0. (P1)
The comparator can be any fixed rotation, without a net approximation term. Rational conservative bounds specifyR without an exact square-root oracle. Forn−1 independent star controllers, sum(P1); the choices remain globally consistent by fixing the root frame.

## Operational and execution limits
Insert this cumulative loss in the existing Poincare/orbit and matching/outer-code readiness theorem. Model-free accepted soundness is unchanged; exact common symmetry gives zero comparator defect, approximate symmetry gives the robust actual-history term. The same full-path conventional baseline can use this controller.

The complete oracle must actually meet every requested gap. Optional numerical-finder failure routes to complete exact enumeration, not a role/action-dependent abort. A declared finite resource cap that aborts some hard perturbations needs its OWN operational bias/readiness analysis; it cannot be silently treated as a neutral sampler. This is why six quick certificates do not prove a uniformly fast controller. For fixedp (or inverse-polynomial probe probability), query coefficient sizes and required inverse accuracies are polynomial inT and1/p, making the exhaustive fallback finite polynomial in those numeric parameters and their rational arithmetic costs but potentially far worse than the accepted expert net. Runtime can itself leak the fresh perturbation/candidate or change the current source through an internal clock. To retain the pre-call nonanticipation premise, pad execution to a deterministic schedule based only on past/horizon bounds, or provide a genuine isolated source-clock/control interface. For example query coefficient l1 norm is at most(T L0/p+dR)/2, giving a finite predetermined exhaustive-grid bound at the selected tolerance. Padding to this enormous worst case can erase the observed fast-path runtime benefit. Candidate-dependent timeouts are NOT neutral aborts. Physical gate synthesis, candidate privacy, buffering and control errors remain separately charged. No online FTPL quantum experiment or practical runtime advantage is asserted by this proof draft.
