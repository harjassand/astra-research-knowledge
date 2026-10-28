# Bounded centers without changing the log-det barrier: a precision refinement

2026-10-28. ROOT CONSTRUCTION CANDIDATE, independent review pending. This changes the CENTER update domain of the received small-loss learner, not its source interface or target. It addresses the adverse pilot's conservative O(N)-bit precision bill, not its flat N512 learning or general-decoder control costs. The received source and all pilot evidence remain unchanged.

## 1. Domain and comparator

Use the received Pauli affine coordinates C(theta), k=2d, D=3d^2, Tr(E_a E_b)=k delta_ab and C0=I_k/k. Keep the ORIGINAL regularizer phi(theta)=-log det C(theta), not -log det(C-mu I). Keep eta=gamma/(64D^2), zeta=epsilon/16, delta=eta epsilon/64, and the same private terminal or separately justified service interface. This changed learner induces its OWN actual occupation law; the same comparator definition/source-cap form does not mean numerical identity with the earlier learner’s R_N.

Restrict only CENTER updates to

    K_zeta={C=zeta C0+(1-zeta)Z: Z>=0,Tr_out Z=I_d/d},
    mu=zeta/k.

Thus every center has C>=mu I. The received comparator C_*=(1-zeta)C_D+zeta C0 ALREADY belongs to this domain; its divergence and additive zeta debit are unchanged. No source-noise/gauge eigenvalue floor is introduced.

At a center use the same exact rational whitening certificate (1/2)I<=V^T H V<=I, exact inverse dual, and played actions theta +/- V e_i/2. These actions need NOT belong to K_zeta; they belong to the original physical CPTP body and have C_play>=C_center/2>=mu I/2 by the Dikin bound. Their mean is the center, and the same acquired-bit unbiasedness and small-loss second moment hold. Confusing the center constraint with the played-action domain would destroy the argument.

## 2. Constrained mirror step

For each acquired g solve, over K_zeta,

    f_t(theta)=eta <g,theta>+B_phi(theta,theta_t).

The exact minimizer theta^+ satisfies a variational inequality, NOT zero tangent gradient. For any feasible comparator u,

    <grad f_t(theta^+),theta^+-u> <=0.

Normal-cone terms have the favorable sign. Taking u=theta_t, the standard self-concordant monotonicity inequality gives, with r=||theta^+-theta_t||_(H_t) and a=eta||g||_(H_t^-1),

    r^2/(1+r) <= a r, hence r<=a/(1-a).

The received deterministic estimate ||g||_(H_t^-1)<=2sqrt(2)D and eta above give a<1/16, hence r<1/15. This remains valid when the minimizer lies on the CENTER floor. It does not require the floor to be a barrier boundary.

For a rational approximate center theta', require a certified approximate variational inequality

    sup_(u in K_zeta) <grad f_t(theta'),theta'-u> <=delta,
    ||theta'-theta_t||_(H_t)<=1/2.

The received three-point mirror inequality then has precisely the same +delta error term, so its regret proof, comparator shrink, source horizon and actual-bit/terminal transfer remain unchanged. This is the only optimization-certificate replacement.

## 3. Uniform finite conditioning and a constructive certificate

On the center domain,

    k I<=H<=k mu^-2 I,
    ||grad f_t||_2<=3k/mu,    ||Hess f_t||<=k/mu^2.

The first two follow from the Pauli coordinate isometry, C<=I, C>=mu I, the received whitening bound and the stated eta. Constants are conservative. The coordinate diameter is at most one.

A feasible point with objective gap at most xi from the exact constrained minimum has coordinate distance at most sqrt(2xi/k). The exact minimizer's variational inequality and the uniform gradient/Hessian bounds imply

    sup_u <grad f_t(theta'),theta'-u>
       <=(3k/mu+k/mu^2)sqrt(2xi/k)
       <=4sqrt(2k xi)/mu^2.

Choose

    xi <= min{delta^2 mu^4/(512k), mu^2/512}.

Then the variational error is at most delta/4. The approximation's H_t-distance from the minimizer is at most sqrt(2xi)/mu<=1/16. Combined with r<1/15 it stays strictly within radius1/2. These margins permit finite solve/rounding slack; no unbounded accuracy search is needed.

Implement a known convex weak optimization in the variable Z, with C=mu I+(1-zeta)Z. The objective is smooth and finite on the entire compact CPTP Z body because C>=mu I. That body has the usual known rational Slater center, and its spectrahedral separation is finite. Log determinants are evaluated from rational determinants with certified scalar-log precision; gradients are rational inverse matrices. Request objective gap xi/4 with controlled feasibility residual. Round Z on a fixed dyadic grid and use the received exact rational TP/PSD repair in its UNNORMALIZED variable K=dZ, followed by normalization. Its bound ||Delta Z||_F<=9 rho applies with repair residual parameter rho at most xi mu/(1000k) and finer entry mesh; rho is distinct from the previously fixed variational tolerance delta. The repair perturbation and uniform gradient bound leave final objective gap below xi. This is a paid finite known convex task, not a new source oracle or a claim that a production solver has executed it.

The approximate variational inequality can also be CHECKED: grad f_t(theta') is rational, and its supremum over K_zeta is a known linear CPTP SDP. A rational dual-feasible upper certificate with optimization error at most delta/4 is accepted when its upper bound is <=delta; the point with true residual<=delta/4 permits an upper bound <=delta/2. No exact delta/4 acceptance threshold is required. Thus one need not mistake a nonzero constrained gradient for solver failure. The radial and TP/floor guards are exact rational matrix tests.

Whitening now uses the fixed mu in the received rational Cholesky construction. Every matrix inverse, grid, objective tolerance, Slater radius and residual has bit length polynomial in d, input bit lengths, log(1/epsilon), log(1/gamma); there is no artificial 2^-N learner floor. Every center is re-emitted in a fixed post-repair denominator family derived from the prescribed dyadic solver grid and rational shrink/repair parameters, preventing recursive denominator growth; the repaired center itself need not lie on a dyadic grid. Finite quantum compilation over N calls additionally pays log(N/nu) accuracy. The total number of rounds and per-round classical/control operations still count.

## 4. Consequences and non-consequences

If independently received, this supplies the SAME conservative small-loss source cap and relative terminal risk with a much smaller worst-case finite-precision prescription. The comparator's existing zeta loss pays the deliberate center floor. The old exponential floor remains valid for its original algorithm; this note does not retroactively change its proof or the audited pilot.

It does not improve eta, show useful learning at N512, implement elementary quantum gates, remove dense decoder application on every probe, or prove a practical advantage. On the observed pilot centers, the new center floor would be far below their actual eigenvalues; similar floating trajectories would be unsurprising but have not been run. This is a theoretical control/precision improvement awaiting independent review, not new numerical evidence.

Governing unchanged source: ordinary_prequential_small_loss_decoder_bandit_20261028.md, SHA256 6edb6a3af1118947c1a864113a24d77eef437386eafb7d8694a4aa651dc8d1dc. The standard constrained-mirror-descent argument is credited as conventional; the intended new obligation is the fully paid physical learner's finite precision repair.
