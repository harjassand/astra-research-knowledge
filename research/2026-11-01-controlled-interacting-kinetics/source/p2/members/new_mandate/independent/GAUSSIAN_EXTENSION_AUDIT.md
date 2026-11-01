# Independent audit of the root's interacting-reference construction

2026-11-01. This audits the root-owned synthesis; it does not claim priority for its ideas. The product-reference construction and failures remain in CONSTRUCTION.md.

## Verdict

The operator theorem is sound under the stated common-equilibrium, bounded-contrast assumptions. The root's sharper Neumann relative bound and Chebyshev approximation are correct. The complete computational claim must retain the local-word count, the quadrature count raised to the word length, the local fermion expansion, and arbitrary-precision costs. A route exists with polynomial dependence on log(stiffness), rather than stiffness, at fixed interaction contrast and requested accuracy.

The meaningful distinction is algebraic evaluation of a stiff interacting semigroup and its insertion amplitudes. Merely avoiding first-arrival trajectories is already supplied by target-start relaxation/return estimators, as the conventional collaborator established. Neither renewal, Neumann inversion, Chebyshev approximation, Gaussian simulation, nor tensor compression is individually a novelty claim.

## 1. Conventions and exact scalar

Take Q to act on probability columns, with stationary pi and detailed balance. Let

    K=-diag(pi)^(-1/2) Q diag(pi)^(1/2),
    g=sqrt(pi), P=I-gg^T, G=K^+.

Then K is symmetric positive semidefinite, g is its unit stationary vector, and for a singleton b, with initial distribution pi conditioned outside b,

    E tau_b = G_bb/[pi_b(1-pi_b)].

This is not the mean from a freely chosen initial microstate. The singleton target and initial law are part of the service.

Let K0 be the root's finite-temperature, disordered, reversible Glauber/domain-wall reference. An edge multiplier a_e equal in both directions of an edge preserves the same pi. If m<=a_e<=M, then

    mK0 <= K <= MK0

as quadratic forms. Set c=(m+M)/2, L=cK0, E=K-L, R=L^+, and

    C=R^(1/2) E R^(1/2), rho=(M-m)/(M+m).

On g-perp, ||C||<=rho<1. With h=R^(1/2)|b>,

    G_bb = <h,(I+C)^(-1)h>.

Every complete local edge-modification piece E_i annihilates g separately, because its two directions satisfy the same detailed balance relation. Symmetry also gives g^T E_i=0. This is stronger than only E g=0 and is essential for segmentwise tail control.

## 2. Sharp scalar relative bounds

The Neumann degree-K approximation has exact remainder

    <h,(-C)^(K+1)(I+C)^(-1)h>.

Since C commutes with its positive inverse and |x|<=rho on its spectrum,

    |remainder| <= rho^(K+1) G_bb.

This improves the loose norm-factor bound in the earlier independent report. It is tight as a scalar spectral inequality.

For H=K0^(-1/2) K K0^(-1/2), spectrum in [m,M], the classical constrained Chebyshev polynomial

    p_K(x) = [1-T_(K+1)((M+m-2x)/(M-m)) /
                 T_(K+1)((M+m)/(M-m))]/x

is a polynomial of degree K because its numerator vanishes at x=0. Its pointwise relative inverse error is at most

    e_K = 1/|T_(K+1)((M+m)/(M-m))|.

Integrating against the positive spectral measure of a quadratic form preserves the same relative bound. The convergence parameter is

    (sqrt(M)-sqrt(m))/(sqrt(M)+sqrt(m)).

This is established Chebyshev approximation machinery. The proposed contribution is the scalar moment representation that avoids forming a many-body Krylov vector.

## 3. Local insertion integrals and their important cancellation

For k>=1,

    <b,R(E R)^k b>
     = sum_(i1,...,ik) integral_[0,infinity)^(k+1)
       <b|e^(-L t0) E_i1 e^(-L t1) ... E_ik e^(-L tk)|b> dt.

Stationary-projector terms vanish next to each E_i. If the reference gap on the relevant parity sector is delta, v_i=||E_i||, and B=sum_i v_i, then the absolute sum of the cube-truncation tails is bounded by

    (k+1)(1-pi_b) B^k exp(-delta T)/delta^(k+1).

Also G_bb >= (1-pi_b)/(M Lambda0), where Lambda0 bounds the top nonzero eigenvalue of K0. These combine to a relative tail bound with no pi_b^-1 factor.

**Do not integrate individual fermionic monomials to infinity separately.** A complete E_i kills g; a monomial in its Gaussian/Wick expansion usually does not. Separate monomial integrals can diverge even though the complete operator-word integral converges. Use a common finite quadrature or finite cube, sum the complete local-operator word, and invoke the tail bound for that word. This also matters for floating-point cancellation at late times.

## 4. Explicit inverse quadrature with logarithmic stiffness dependence

One can avoid an unspecified multidimensional adaptive integration oracle. Suppose the reference spectrum on g-perp lies in [delta,Lambda], with kappa=Lambda/delta. For eta in (0,1), set

    t_min=eta/(4 Lambda),
    t_max=delta^(-1) log(4/eta),
    t_(j+1)=(1+eta/2)t_j,
    w_j=t_(j+1)-t_j,

shortening the final interval at t_max. Define f(x)=sum_j w_j exp(-x t_j).

For any x in [delta,Lambda], the omitted near-zero integral has relative error <=eta/4 and the tail has relative error <=eta/4. Monotonicity gives a lower rectangle sum larger than the retained integral. On each cell, t_j>=t/(1+eta/2), so the entire rectangle sum is bounded above by integral_0^infinity exp[-xt/(1+eta/2)]dt. Hence

    (1-eta/2)/x <= f(x) <= (1+eta/2)/x.

The number q of exponentials is

    O(eta^-1 [log(kappa)+log(1/eta)+log log(1/eta)]).

There is no factor delta^-1 in q. Each exponent can be evaluated algebraically at its possibly very large physical time. Faster positive exponential-sum constructions are available in the primary literature, but this elementary construction already proves the necessary dependence.

Set R_tilde=sum_j w_j(e^(-L t_j)-gg^T). This approximates R relatively on g-perp. At order k>=1, all stationary projectors disappear against E_i, so a coefficient becomes a finite sum of q^(k+1) Gaussian insertion amplitudes. The k=0 coefficient must retain the stationary subtraction.

### Propagation of relative quadrature error

Write R_tilde=R^(1/2)(I+D)R^(1/2), ||D||<=eta. Replacing all k+1 resolvents in a scalar moment changes that moment by at most

    rho^k [(1+eta)^(k+1)-1] <b,Rb>.

This bound is independent of delta and pi_b.

A cleaner argument, especially with the Chebyshev polynomial, treats the computed moments as exact moments of

    K_tilde=R_tilde^(-1)+E

on g-perp. Then

    ||K^(-1/2)(K_tilde-K)K^(-1/2)||
       <= d=eta/[(1-eta)(1-rho)].

For d<1, the corresponding inverse quadratic-form error is at most d/(1-d). The preconditioned perturbation based on R_tilde has norm <=(1+eta)rho, so applying the usual polynomial approximation on that slightly enlarged interval gives a complete combined bound. Thus eta=O(epsilon(1-rho)) suffices; it need not shrink with the reference gap or exponentially with polynomial degree. Polynomial coefficient cancellation is charged to arithmetic precision rather than to the number of quadrature nodes.

## 5. Bounded Gaussian amplitude evaluation and precision

The formal Heisenberg representation can contain exp(+epsilon_j t), even though e^(-Lt) is a contraction. Using that formula without stabilization would not earn a bit-cost claim at huge t.

There is a constructive bounded alternative. In the normal-mode representation, with zero ground energy,

    L=sum_j epsilon_j d_j^dagger d_j.

Each attenuation diag(1,exp(-epsilon_j t)) is exactly the vacuum-to-vacuum block of a number-conserving fermionic beam splitter with a fresh vacuum ancilla and cos(theta)=exp(-epsilon_j t). Diagonalizing Bogoliubov transformations are Gaussian unitaries. Every local fermion monomial can be expanded into a finite sum of Majorana products; Majorana operators have norm one and preserve Gaussian/Pin structure, with parity tracked.

Thus each insertion word is a finite sum of Fock-to-Fock amplitudes of bounded Gaussian circuits on O(n(k+1)) modes, using fresh ancillas for the semigroup segments. Intermediate vacuum projections can be postponed because the ancillas do not participate again. Gaussian amplitudes are computed by determinant/Pfaffian machinery with polynomial matrix dimensions; no growing imaginary-time chart is required. This is established fermionic linear-optics machinery used as a mathematical evaluator, not a quantum hardware proposal.

The local expansion count must be included: a general r-mode operator needs at most 4^r fermionic/Majorana basis terms. The cost at order k is therefore of the form

    n^k * 4^(rk) * q^(k+1) * poly(n,k),

up to choices of basis and reusable contractions. The polynomial includes the augmented Gaussian circuit size. Stating n^k poly(n,k) without quadrature and local expansion factors would hide costs.

The sum of quadrature weights is O(delta^-1 log(1/eta)). The absolute sum of local monomial coefficients is at worst 4^r times a local norm scale. Therefore the absolute sum of all expanded terms is bounded by powers of these scales. Relative cancellation can be large in numerical value, but its **logarithm** costs O(k log(kappa)+k log n+rk log(1/pi_b)+log(1/epsilon)) precision bits, with additional polynomial dimension factors depending on the chosen Pfaffian algorithm. There is no need for a number of bits proportional to kappa or pi_b^-1.

For a rigorous bit-complexity claim, specify efficiently evaluable microscopic coefficients and a certified spectral bracket. Symmetric small-matrix eigenvalue computation can establish the bracket to absolute accuracy proportional to delta using additional O(log(kappa)) precision bits. A merely computable real-valued input law without an evaluation-cost bound is insufficient. Floating-point covariance formulas and adaptive quadrature are useful evidence but do not themselves implement this certified-arithmetic route.

## 6. Strong conventional comparison and honest scope

Masetti and Robol (2019), https://arxiv.org/pdf/1907.02449 , already split a local Kronecker-sum reference from interactions, use exponential-sum inverses and Neumann expansions, supply an accelerated iteration, and implement the method in https://github.com/numpi/kaes . Their practical large-state advantage depends on controlled tensor ranks. The root's reference is itself interacting and Gaussian, and scalar coefficient evaluation needs no hypothesis of a low-rank many-body solution tensor. That is a concrete difference in representation and theorem scope, not proof of practical superiority.

Braess and Hackbusch (2005), https://files-www.mis.mpg.de/mpi-typo3/preprints/2004/preprint2004_75.pdf , provide established exponential-sum inverse machinery. Bravyi (2004/2005), https://arxiv.org/abs/quant-ph/0404180 , provides Gaussian-map and fermionic linear-optics machinery including projective operations. These should be named as ingredients.

The theorem covers bounded kinetic modifications that preserve a known equilibrium law, around an earned tractable reference. It excludes genuinely new hard constraints at m=0 and does not give a uniform practical algorithm as M/m diverges. It does not yet cover general energetic interactions changing pi, arbitrary target sets, arbitrary starting distributions, or an unknown generator inferred from partial physical observations. Microscopic rates are the physical inputs, and their correctness for an actual material remains a separate scientific claim.

## 7. Executed independent audit

`audit_gaussian_extension.py` independently constructs every local generator from the root's rates, then uses a different perturbation,

    a_i=exp[0.7(2 x_(i+2)-1)(2 x_(i+3)-1)].

This is a two-spectator, non-Gaussian kinetic modifier with m=exp(-0.7), M=exp(0.7). For n=4,6,8, the audit checked local detailed balance and E_i g=0, generalized spectral bounds, the physical mean against the killed-generator solve, the sharper Neumann bound through degree 8, the Chebyshev relative bound through degree 8, and the elementary positive exponential-sum bound. All passed. Maximum local stationary residual was 1.92e-16.

These checks independently support the algebra; they are not interval proofs.

## 8. A discriminating stiffness family must retain slow observable weight

A small global spectral gap alone does not prove that a target-start relaxation estimator is costly for the chosen b. Its return kernel may have negligible slow-mode weight. A useful family within the ring is to set two separated attempt rates to epsilon and keep the rest O(1). At epsilon=0, the fast pair-flip graph splits into two wall segments, conserving their parities. The no-wall target lies in one parity class; the equilibrium weight of the incompatible class can remain O(1). A genuine epsilon^-1 contribution to the hitting time then survives.

One slow edge is insufficient because the remaining pair-flip graph is still connected. Strong conventional multiscale/adiabatic reduction should be compared on the two-edge family: it can exploit the exposed parity classes. A substantial theory cannot declare a universal practical advantage from the global gap bound alone.

## 9. Broader service: equilibrium fluctuation integrals

The root proposed the extension from the singleton return source to any centered source f with g^T f=0 and f!=0. This extension is valid:

    chi_f=<f,K^+ f>.

The same sharp relative polynomial and relative quadrature bounds apply. Replace (1-pi_b) in the tail by ||f||^2 and use

    chi_f >= ||f||^2/(M Lambda0).

The norm cancels in the relative tail estimate. If f is a sum of L explicitly given Gaussian-compatible endpoint terms, each coefficient needs at most L^2 times the previous amplitude work. A bounded-degree Majorana monomial acting on a Gaussian state is such an endpoint; so are finite sums of these. Endpoints must remain in the physical parity sector. The stationary subtraction must be retained for the zero-insertion term unless every source term is individually centered.

Relative numerical accuracy also needs a source-condition parameter. If f=sum_l a_l |phi_l>, with ||phi_l||<=1, define

    kappa_f=(sum_l |a_l|)^2/||f||^2.

Nearly cancelling source components can make kappa_f large. The arithmetic cost gains log(kappa_f) bits; this must not be hidden behind the phrase “polynomially many source terms.” A zero source has chi=0 and no meaningful relative-error requirement.

### Physical interpretation

For a real physical observable A(x), let f_x=[A(x)-<A>_pi]sqrt(pi_x). Then

    C_A(t)=Cov_pi(A(X_t),A(X_0))=<f,e^(-Kt)f>,
    chi_A=integral_0^infinity C_A(t)dt.

For a finite reversible chain, C_A(t) is a nonnegative spectral sum of decaying exponentials. With the two-sided spectral-density convention S_A(omega)=integral_R exp(i omega t) C_A(t)dt,

    S_A(0)=2 chi_A.

The exact variance identity

    Var(integral_0^T A(X_t)dt)=2 integral_0^T (T-t) C_A(t)dt

also gives T Var(time-average A)->2 chi_A. This is equilibrium integrated noise and Poisson response. It does not alone establish thermal conductivity, static heat capacity, or a driven nonequilibrium transport law. Cross-responses formed by subtracting positive quadratic forms need separate cancellation accounting.

### Energy is an especially clean source

For wall energy A=2 sum_i J_i eta_i and the real convention c=U d+V d^dagger, set

    B=U^T diag(2J_i) V, F=B-B^T.

After centering, the vacuum part cancels exactly and

    f=sum_(a<b) F_ab d_a^dagger d_b^dagger g,
    Var_pi(A)=sum_(a<b)|F_ab|^2,
    chi_0=sum_(a<b)|F_ab|^2/(epsilon_a+epsilon_b).

There is no extra 1/2 when summing only a<b; an all-index sum uses 1/2. Every pair-excitation source term is already orthogonal to g. The reference chi is computed using O(n^2) terms, without a large state vector.

For insertion coefficients, A=sum_i2J_i eta_i-<A> provides O(n) local quadratic endpoint terms. This avoids unnecessarily treating the O(n^2) quasiparticle expansion as independent endpoints and then squaring that count. Both approaches are polynomial, but the local observable representation is more economical.

Independent checks were added to `audit_gaussian_extension.py`: the Gaussian variance and chi formulas match dense reversible calculations for n=4,6,8, and the degree-six Chebyshev enclosure also holds for this energy source under the two-spectator non-Gaussian perturbation. A separate random-model check found relative errors below 8e-15 for the reference formulas. The source is unchanged by the kinetic perturbation because the exact equilibrium law is unchanged.
