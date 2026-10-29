# Global curvature pays a normal-fluid field sampler, not an ordered phase

29 October 2026. Independent analytic construction; review pending. The bounded-cut packet is frozen and has separately passed root review. No new normal-fluid fixture is run here: the physical qualifier below changed the destination before such a computation.

## 1. Native input and the missing mixing operation

Use the actual stable conjugate-flavor model `H=b†Tb+c†conjugate(T)c+sum_i U_i(nb_i-nc_i)^2`, with T>=0, U_i>=0. At L symmetric imaginary-time slices, whiten the HS fields x in R^(ML), and put

`theta_(i,l)=sqrt(2 beta U_i/L) x_(i,l)`,

`B(x)=F_L ... F_1`, `F_l=exp[-(beta/L)T] diag(exp(i theta_l))`.

Cyclic collection of symmetric half steps preserves the canonical trace; every factor is a contraction. For fixed phi and `z=r exp(i phi)`, r<1, define

`f(x)=log |det(I-zB(x))|^(-2)`.

The conditional grand field potential is `V_alpha(x)=|x|^2/2-alpha f(x)`, with alpha in [0,1]. This section supplies the actual global curvature condition; log-concave sampling is an established ordinary method, not a new generic algorithm.

## 2. Uniform first and second derivatives of the product

For a direction v, set `a_l=||diag(sqrt(2 beta U_i/L)v_(i,l))||F`. Then

`sum_l a_l <=sqrt(2 beta Umax)||v||2`.

A first derivative inserts one diagonal generator, so

`||B'[v]||F<=sum_l a_l<=sqrt(2 beta Umax)||v||2`.

A same-slice second derivative has trace norm at most a_l^2. Two distinct slice insertions have trace norm at most a_l a_k, by Schatten Cauchy--Schwarz with all intervening contractions retained. Summing both orders gives

`||B''[v,v]||1<=(sum_l a_l)^2<=2 beta Umax ||v||2^2`.

These bounds have NO volume, topology, hopping-norm or slice-count factor. They do not require commuting hopping and phase factors.

Write R=(I-zB)^(-1), so ||R||<=1/(1-r). Exact differentiation gives

`f''[v,v]=2 Re Tr[R z B''+R z B' R z B']`.

The trace-norm and Frobenius estimates yield

`|f''[v,v]|<=chi ||v||2^2`,

`chi=4 beta Umax r/(1-r)^2`.                         (1)

Consequently for chi<1 all V_alpha have Hessian between `mu I` and `ell I`, where mu=1-chi and ell=1+chi. This applies on arbitrary graphs and to arbitrary PSD kinetic bandwidth. It is a sufficient weak-thermal-interaction/dilute-fugacity condition, not a statement about strong-interaction ordering.

Also

`-2M ln(1+r)<=f(x)<=-2M ln(1-r)`,

so its range is at most `R_M=2M ln[(1+r)/(1-r)]`. Differentiating in a unit direction and using trace/Frobenius duality gives

`||grad f||2<=G=2r sqrt(2 beta Umax M)/(1-r)`.

The gradient perturbation therefore scales with sqrt(M), not sqrt(ML).

## 3. Acquire the native gradient rather than postulate an oracle

Let `P_(l-1)=F_(l-1)...F_1` and `S_l=F_L...F_(l+1)`. The exact coordinate formula is

`partial_(i,l)f=-2 sqrt(2 beta U_i/L) Im[(P_(l-1) R z S_l F_l)_(ii)]`.

Prefix/suffix multiplication and one uniformly conditioned solve acquire every component in O(L M^3) arithmetic and O(L M^2) straightforward storage. Checkpointing may reduce storage but is not free here. No inverse of a poorly conditioned hopping exponential is used. Its exact known contraction and the singular-value interval [1-r,1+r] of I-zB pay finite precision. Matrix exponentials consume the supplied T and beta/L, not an unspecified physical model or gradient sensor.

## 4. A full finite-time/discrete-Langevin TV receiver

This is a conservative explicit construction using ordinary Bakry--Emery entropy contraction, Girsanov and Pinsker. It is not an executed hot loop or a claim of optimal sampler complexity. Dalalyan, arXiv:1412.7392, is an established nonasymptotic Langevin comparator.

Start the Langevin diffusion `dX=-grad V_alpha(X)dt+sqrt(2)dW` from the standard Gaussian. Its initial relative entropy to pi_alpha is at most R_M. Strong convexity gives

`TV(Law(X_t),pi_alpha)<=sqrt(R_M/2) exp(-mu t)`.

For a requested TV budget eta, take

`t>=mu^(-1) ln[max(2,2sqrt(R_M/2)/eta)]`.

The following Euler chain is an actual finite operation:

`Y_(k+1)=Y_k-h grad V_alpha(Y_k)+sqrt(2h)xi_k`.

For h<=1/2, convexity of the squared norm and the global gradient-perturbation bound give

`E|Y_k|^2<=G^2+2d`, `E|grad V_alpha(Y_k)|^2<=H2=4G^2+4d`,

where d=ML. Use the continuous interpolation with frozen drift on each step. Its path relative entropy with respect to the true Langevin diffusion is at most

`(ell^2 t/4)[h^2 H2/3+d h]`.                         (2)

Indeed a within-step increment has second moment at most `s^2 H2+2ds`; Lipschitz drift, integration in s and Girsanov give (2). Globally Lipschitz drifts and finite second moments justify the identity by localization. The initial laws coincide. Pinsker and data processing bound the endpoint TV by the square root of half (2).

It suffices to choose an integer number of steps n with h=t/n and

`h<=min(1/2, eta^2/[4ell^2 t(d+H2)])`.

The exact diffusion's error is at most eta/2, and the discretization error is below eta/2. All t,h,n are acquired from native quantities, with polynomial dimension/accuracy cost. A tiny formal h is not represented as an experimentally or computationally useful choice; more advanced established MALA/HMC methods may be far stronger.

Numerical gradient errors add an explicit Girsanov drift-error budget, e.g. uniform gradient error a costs at most O(t a^2) path entropy. Truncated normal quantiles, directed matrix arithmetic, and a declared rounded-output law give a finite-bit approximation. Discrete samples are not asserted TV-close to an unrounded continuous density. No end-to-end interval/fair-bit execution is claimed.

## 5. Paid normalization, with no pressure oracle

For alpha from zero to one the same strong-convexity condition persists. Center f by its known lower bound. Divide [0,1] into `S=ceil(max(1,R_M))=O(M)` intervals. Each adjacent ratio is an expectation under pi_alpha of a positive variable in [1,e]. Independent fresh Langevin runs with allocated TV budgets acquire those bounded means to relative error O(epsilon/S), with a union confidence budget. Multiply their ratios in log space and restore the known centering scalar.

The number of stages, samples, steps per sample, density/gradient evaluations and precision bits are all polynomial at fixed mu>0,r,beta and qualified source norms. This is ordinary annealing with the MISSING native mixing/gradient interface now supplied. It does not assume successive target samples for free.

For exact balance rather than the ordinary two-flavor grand ensemble, fixed phi samplers can feed the positive phase-grid/normalizer operation of the frozen bounded-cut proof, replacing its recursive sampler. Canonical selection still consumes its actual count probability. This is not an unrestricted fixed-density theorem.

## 6. Strong ordinary comparison and the physical ceiling

Primary canonical AFQMC already uses correlated fields and sophisticated updates. Finite-temperature MPO methods and interaction-picture/hopping clusters are strong ordinary alternatives. This theorem neither benchmarks nor excludes them. It removes a separator assumption for the positive FIELD-law sampler when (1) holds. Weak-Gaussian/Borel/cluster constructions are also competent alternatives; absence of a matching theorem in a bounded search is not novelty evidence.

One tempting application is a large-kinetic-bandwidth two-dimensional flat band: T=J B†B for the unsigned vertex-edge incidence of a triangular lattice. There are M=3N edge modes, and B B†=6I+A_tri has spectrum in [3,12]. Hence there are exactly 2N zero flat-band modes and a dispersive gap3J, with positive frustrated hopping triangles. Equation (1) is independent of beta J. This algebra identifies a genuine bulk class beyond a narrow bounded-cut admission; no actual material/device or ordered phase follows.

The crucial qualifier is stronger than the curvature estimate. At every field/phase cut the covariance `C=zB(I-zB)^(-1)` has norm at most `c=r/(1-r)`. The exact opposite-flavor pair density matrix is the positive physical average of

`C^T tensor conjugate(C)^T`.

Individual matrices need not be Hermitian or positive; their operator norm is at most c^2. Positive joint determinant weights and the triangle inequality therefore imply

`||Gamma_pair||op<=c^2`, `||gamma_onebody||op<=c`.       (3)

These bounds cover the FULL opposite-flavor pair space, not only onsite or one fixed pairing profile. They survive finite-sector/number-tail passage to exact Gibbs at fixed r<1. At exact balance integrate the positive common-phase weight first. Thus fixed r excludes any divergent pair eigenvalue in that grand state, not merely macroscopic Bose condensation.

If a target has `lambda_max(Gamma_pair)>=s M^a`, a>0, then c^2>=sM^a. But `chi=4beta Umax c(1+c)>=4beta Umax sM^a`. The present curvature gate would require `beta Umax<1/(4sM^a)`. It does NOT acquire a fixed-interaction ordered paired phase by increasing beta J alone. For a canonical sector of grand mass b one only inherits `||Gamma_pair,K||<=c^2/b`; the b factor cannot be dropped.

The normal-fluid operation is useful at its earned scope, but not the higher-leverage ordered-matter destination. A nonperturbative interacting critical-number/mode operation as r approaches its stability boundary remains necessary. This is not a hardness claim and does not prohibit different canonical or continuous-time methods.

## 7. Current achieved scope

Constructed: global native curvature and gradient bounds; an explicit discrete-Langevin TV/bit interface; annealed normalizers on any topology at chi<1; and an exact physical order ceiling identifying why this is not the desired ordered-phase acquisition. No extra normal-fluid fixture or sampler was run after discovering that ceiling. Historical priority and practical advantage are unestablished.

The continuation in `critical_boson_mode/` attacks the actual critical number gate, granting the incumbent exact free-mode and fixed-rank conditioning. It is separate from this completed normal-fluid proof.
