# Independent theorem review: engineered radial kinetic lift

## Verdict and review boundary

**PASS for the mathematical lift and fixed clamped-protocol formulas after the raw-sign correction.** No executable consumer, finite CDF certificate, full-state numerical trajectory, adaptive controller, or physical implementation is accepted by this review.

The mathematical check boundary is `EXACT_KINETIC_LIFT_CANDIDATE.md` SHA-256 `c2118c15d73355d85fd4a0f9fb63464d79400231bea5915ac51e480fe5ad4300` (10,896 bytes). The first source `e14bda94da6bd3993045d1fbeeed439b6a9ffbff058dbdd3fcc47f2204070dc0` omitted an explicit sign restriction on mixed coefficients. I reported that omission; the author preserved it as `EXACT_KINETIC_LIFT_BEFORE_GRAMMAR_CORRECTION.md` and added strictly positive listed coefficients, with omitted terms zero.

A separate citation-location correction was also requested: in the linked arXiv v3, Lelièvre–Santet–Stoltz Remark 2 simplifies the divergence for constant gradient norm; Proposition 2 equation (20), not Remark 2, supplies projected diffusion scaling. This does not affect any lift equation. The final source binding, if corrected, is recorded separately rather than silently changing this derivation receipt. Both exact sources used for the 147-check run are preserved in `source_snapshots/`.

## 1. Declared dynamics, not a reduction of the earlier Euclidean process

The mathematical state space is D=R x (R^m minus {0}), with positive initial energy. U is positive, coercive, homogeneous of even degree p, alpha=m/p>=1, beta,kappa>0, and v=1+kappa(1-y^2)^2. A finite collection of C^2 tangent fields and finite nonnegative coefficients defines T=sum c_a X_a X_a^T, where X_a.grad U=0 on D.

The actual transverse tensor is M=zz^T/(p^2 U)+T. Its generator is the declared divergence-form generator, whose Itô drift is -M grad_z F+beta^-1 div M and whose covariance is 2M/beta. Omitting div M changes the process and invalidates the conclusion. This tensor generally differs substantially from the earlier constant-SPD mobility, even at identical potential and Gibbs law. The theorem specifies an engineered kinetic model; it does not acquire an actual physical actuator or authenticate a measured process from U alone.

On every compact subset of D the explicit radial and tangent noise columns and drift are locally Lipschitz. U>0 off zero removes the radial denominator there. Thus a unique strong local full-state SDE exists up to its lifetime, even when T=0 and the matrix is degenerate.

## 2. Exact pointwise energy closure

Euler's two identities are z.grad U=pU and z^T Hess(U)z=p(p-1)U. They give

    div M_rad=(m+1-p)z/(p^2 U),
    M_rad grad U=z/p,
    grad U^T M_rad grad U=U.

The radial energy drift has three terms:

    beta^-1(div M_rad).grad U
      + beta^-1 M_rad:Hess(U) - v grad U^T M_rad grad U
    = (m+1-p)/(beta p) + (p-1)/(beta p) - vU
    = alpha/beta-vU.

The radial energy noise is exactly sqrt(2U/beta) times the named radial Brownian motion, not merely a martingale with an averaged variance.

For tangent dynamics, T grad U=0 identically. Differentiating this identity gives

    (div T).grad U + T:Hess(U)=div(T grad U)=0.

The transverse force term also vanishes, as does every tangent noise coefficient in dU. Consequently the whole divergence-form tangent generator annihilates every g(U). Div X_a need not vanish. The coefficient cancellation is pointwise and holds for non-divergence-free tangent fixtures as well; there is no unretained Itô energy correction.

Independence of the longitudinal and radial driving Brownian motions gives zero y/U cross variation. Thus the full projected generator is exactly

    G=beta^-1 partial_yy-v'(y)u partial_y
        +(alpha/beta-v(y)u) partial_u +(u/beta) partial_uu.

Its coefficients are locally Lipschitz for u>0. After the global join below, strong uniqueness proves equality of the entire projected path law for every deterministic initial state, and by conditioning for every nonanticipating initial probability law supported on U>0 with the same (y,U) pushforward. Arbitrary initial moments are unnecessary: one may condition/localize on finite initial states. No Gibbs initialization, equilibrium conditional averaging, fast angular mixing, or angular spectral gap is assumed.

A different noise square root yielding the same full generator has the same law by the full local well-posedness/global continuation; the explicit radial-column representation is a convenient strong construction, not an unobservable hidden equilibrium assumption.

## 3. Nonexplosion and origin avoidance

Take c=2kappa+1 and W=1+y^2+cu. Since yv'>=-kappa and v>=1,

    GW=(2+c alpha)/beta-[2yv'+cv]u
       <=(2+c alpha)/beta-u.

Use stopped processes with u>=epsilon and W<=R. Optional expectation bounds the probability of exit through W=R before a fixed horizon, uniformly in the tangent coefficients and in the lower-energy cutoff. This precludes escape to infinity once the origin boundary is excluded. Coercivity U>=a||z||^p makes bounded u imply bounded z. Conversely a finite upper spherical bound U(z)<=A||z||^p, which exists by polynomial homogeneity and compactness of the unit sphere, makes positive lower u imply distance from z=0. A bounded macrostate with positive lower energy therefore confines the full state to a compact subset of D, where even large tangent coefficients and derivatives are bounded. No unexplained angular finite-time explosion can occur inside that compact set.

Before stopping y in a bounded set, put A(t)=integral_0^t v(Y_r)dr and Q=e^A u. Direct Itô calculus gives

    dQ=(alpha/beta)e^A dt+sqrt(2e^A Q/beta)dB_t.

The increasing adapted time change s(t)=integral_0^t e^A/beta dr turns this into dQ=alpha ds+sqrt(2Q)dB_s. Hence 2Q is squared Bessel of dimension 2alpha. The time-changed Brownian need not remain independent of the other time-changed noise for this boundary argument; no such independence is used.

For alpha=1, log Q is a scale function. For alpha>1, Q^(1-alpha) is a scale function. Stopping between epsilon and a fixed upper level gives a probability of hitting epsilon before that upper level tending to zero as epsilon decreases to zero. This includes the critical alpha=1 case. Since A and s are finite over a bounded-y finite horizon, u cannot hit zero there. Combine this with the W exit estimate to remove the stops: the full SDE has infinite lifetime and positive u on every compact time interval. This closes the process argument rather than merely manipulating a formal generator.

For alpha<1, the scalar origin is accessible and the singular full lift requires a separate continuation/interface. Returning UNKNOWN is justified. Non-hitting for alpha>=1 does not imply a uniform separation from zero over infinite time, a bounded actuator, or a numerically stable discretization.

## 4. Gibbs symmetry and stationarity, including degenerate tangent motion

Homogeneous volume scaling gives the energy pushforward of Lebesgue measure as a positive constant times u^(alpha-1)du. Thus the full Gibbs law projects to

    rho(y,u) proportional to u^(alpha-1) exp(-beta v(y)u).

Integrating u gives a constant times v(y)^(-alpha), which has tail |y|^(-4alpha). It is integrable for alpha>=1. The full Gibbs partition is finite because U is coercive. No angular normalizer must be evaluated to state the normalized projected law.

The reduced reversible flux check is exact:

    beta^-1 partial_y log rho=-v'u,
    [partial_u(u rho)]/(beta rho)=alpha/beta-vu.

For the full process, integration by parts on compactly supported functions in D gives the symmetric nonnegative energy form with coefficients diag(1,M). Degeneracy does not defeat this argument: its finite sum-of-squares form is closable, with smooth locally bounded fields and positive smooth Gibbs weight. The associated local diffusion agrees with the locally unique SDE. The proved absence of both finite-time infinity escape and origin killing makes this minimal process conservative. Symmetry plus P_t1=1 and finite Gibbs mass gives invariance by integral P_t f dmu=integral f P_t1 dmu=integral f dmu.

No assertion of uniqueness of invariant law, ergodicity, full-Gibbs sampling, or mixing time follows when T is degenerate. With T=0, for example, angular rays remain frozen although the exact (y,u) law and Gibbs invariance are valid.

## 5. All-pair tangent program and raw acquisition

For X_ij=(partial_j U)e_i-(partial_i U)e_j, mixed-partial symmetry gives div X_ij=0, and X_ij.grad U=0 exactly. Summing all unordered pairs with common c_t yields

    T=c_t(||g||^2 I-g g^T),
    div T=c_t[H g-(Delta U)g],
    g=grad U, H=Hess U.

For z!=0, Euler implies z.g=pU>0, hence g!=0. If c_t>0, T has kernel span(g). A vector annihilated by both T and the radial quadratic form would be proportional to g and orthogonal to z, hence zero. Therefore the full M is SPD at every nonzero point. This is pointwise ellipticity only; it gives no uniform conditioning bound near zero or infinity.

The proposed tangent square root sqrt(c_t)||g||(I-g g^T/||g||^2) squares to T because the parenthesis is an orthogonal projection. It uses m Gaussian coordinates rather than one for every pair, but computing g and applying the projection still costs real work. The radial column must be added independently with the factor sqrt(2/beta). Full-state drift evaluation also requires the stated derivatives/divergence, not merely U.

The corrected first raw grammar has p in {2,4}, strictly positive listed rational coefficients, even exponents, homogeneous degree p, and every pure coordinate monomial present. Thus every mixed atom is nonnegative, and

    U>=d_min sum_i |z_i|^p
      >=d_min m^(1-p/2)||z||^p.

The sign correction was necessary: z1^4+z2^4-3z1^2z2^2 has even exponents and positive pure coefficients but is negative at (1,1). It is not enough to say that signs are checked without specifying their accepted set. The corrected sufficient grammar is sound and deliberately incomplete. No basis finder or arbitrary polynomial positivity oracle is accepted.

The implementation still must actually read and bind all coefficients/exponents, dimensions/degrees/budgets, the declared mobility and tangent schema, beta/kappa, initial energy, and protocol. This audit establishes why those checks suffice mathematically; it does not certify that the current code enforces them. An externally supplied energy is a declared initialization unless its equality to the actual U(z0) has been checked or otherwise justified.

## 6. Fixed clamped protocols and ordinary CIR formulas

The autonomous coupled Y/u process does not have a frozen-y CIR transition. Section 5 correctly changes the task to a finite externally specified piecewise-constant clamp, with fixed positive durations. On each segment, du=(alpha/beta-v_j u)dt+sqrt(2u/beta)dB.

For one segment e=exp(-v_j t_j), b=(1-e)/(beta v_j), the ordinary conditional Laplace transform is

    (1+b theta)^(-alpha) exp[-e u theta/(1+b theta)].

Composing it with a preceding transform of the same form gives E_new=e E_old and B_new=e B_old+b, exactly as claimed. Differentiating the final log transform at zero gives mean E u0+alpha B and variance 2EBu0+alpha B^2.

The Poisson/Gamma mixture is also exact: with lambda=E u0/B, mixing Gamma(alpha+N,rate 1) against Poisson(lambda) and scaling by B reproduces the displayed Laplace transform. For integer alpha, the integer-shape Gamma CDF is exactly 1-exp(-x)sum_(k=0)^(alpha+n-1)x^k/k!, giving equation (5). Its infinite Poisson sum still needs a finite, outward numerical tail/error certificate before any numerical answer is accepted. This audit does not supply that implementation.

The formulas hold for a fixed finite protocol. They do not automatically hold with random E/B obtained from state-dependent or angle-dependent adaptive feedback. A macro-adapted policy can define a separate closed controlled SDE when its assumptions are stated, but that does not turn its terminal law into the same deterministic affine transform. Angular feedback can itself reintroduce angular information. Feedback robustness and numerical/physical control error therefore remain outside acceptance.

At a clamp jump, z and u remain fixed while the energy changes by (v_new-v_old)u. This is work, not free heat. Producing a y clamp, reading energy, realizing the tensor/noise and divergence drift, and controlling stiffness are substantive implementation requirements. No autonomous barrier-hitting distribution or practical acceleration of the earlier constant-mobility model follows.

## 7. Strong ordinary comparisons and independently checked attribution

I independently inspected the cited primary sources, rather than treating their titles as evidence:

- [Bussi–Donadio–Parrinello](https://arxiv.org/pdf/0803.4060), equations (4)–(7) and Appendix A, already supply energy-rescaling diffusions with Gamma stationary law and an exact frozen-parameter propagator from OU coordinates. Their full sampling statement uses an ergodicity assumption. The [author's algorithm page](https://sites.google.com/site/giovannibussi/Research/algorithms) explicitly warns about the Appendix Gamma-scale typo. The present mixture was checked directly and does not inherit that typo.
- [Lelièvre–Santet–Stoltz v3](https://arxiv.org/html/2410.00525v3), Proposition 2 equation (20) and Remark 1, supply projected diffusion scaling and tangent-direction freedom. Their general effective drift uses conditional quantities. The present Euler construction closes both coefficients pointwise. Remark 2 in this version concerns a constant-gradient-norm divergence simplification, so the candidate's original attribution to that remark was inaccurate.
- [Legoll–Lelièvre](https://arxiv.org/pdf/0906.4865), Section 1.2 and Proposition 3.1, discuss the generic non-Markov projection problem and quantitative conditional-mixing assumptions for approximation. Those assumptions are not needed for this exact pointwise closure, but their removal here is bought by the restrictive engineered mobility, not by solving the generic projection problem.

For Gaussian U=||z||^2/2 under ordinary gamma I, direct Itô calculus gives du=gamma(m/beta-2vu)dt+2sqrt(gamma u/beta)dB. At gamma=1/2 this is precisely the same quotient equation. The Gaussian comparator therefore gets the same potential/protocol and ordinary scalar engine; no advantage over it is claimed. A general homogeneous lift with a different actual mobility is the scoped mathematical extension. No new generic Markov-function theorem, new noncentral-Gamma engine, priority conclusion, or independent algorithmic separation is established.

## 8. Independent checks and deliverables

The independent symbolic script passed **147 exact assertions**. It checks Euler/radial divergence/drift identities for degree-two and degree-four fixtures; all-pair tensor/divergence and square-root identities; non-divergence-free tangent cancellations; representative exact SPD principal minors; reversible projected flux; Lyapunov and Bessel scale identities; affine transform composition, moments and Poisson mixture exponent; integer-Gamma CDF derivatives; the omitted-sign counterexample; and both source bindings. General statements are proved above, not replaced by finite fixtures.

No candidate implementation is imported. The original check script/results retain the source state at execution time. `replay_check_lift_algebra.py` instead reads the preserved immutable source snapshots, so the same checks remain reproducible after the author's citation-only correction. Its separate output avoids overwriting the first result.

The unfinished finite CDF consumer, autonomous first-passage solver, empirical model acquisition, approximate-mobility robustness, controller design and physical deployment remain separate open tasks. All earlier accepted conductance and latency sources retain their exact scope.
