# Certified adaptive constitutive acquisition by primal and dual cells

7 November 2026. Follow-up to the principal's proposed dual-cell attack. The independent auditor separately checked the conditional source matching. This note strengthens the coefficient-acquisition result in `FOLLOWUP.md`; it does not remove the independent finite-N hydrodynamic or arbitrary-force gaps.

## Achieved operation

In one-dimensional finite-range uniformly elliptic product-reversible speed-change exclusion, finite noisy local-rate acquisition followed by polynomial local Monte Carlo produces a **certified density-uniform interval for the nonlinear diffusivity**. The stopping test uses observed primal/dual interval width and requires no supplied numerical homogenization convergence constants. The published algebraic convergence theorem proves termination and a polynomial complexity bound at fixed physical class parameters. It is used for runtime, not as an unevaluated error term in the returned interval.

The principal identified the dual representation. The exact normalization, conditional sampling, error bounds and adaptive uniform-density construction below close it. This remains a composition with established homogenization and spectral-gap theory; historical novelty and practical advantage are unestablished.

## 1. Source objects, normalizations and exact finite-scale order

Use Funaki–Gu–Wang [2404.12234v3](https://arxiv.org/html/2404.12234v3), Proposition 4.1 and (4.1)–(4.11). Let Lambda be a cube of volume V, Gamma=Lambda^+, and E=overline(Lambda^*) its issued bonds. In one dimension Lambda={0,...,L-1}, Gamma={0,...,L}, E={(x,x+1):0<=x<L}. The primal diffusivity is

\[
U_L(\rho)=\overline D(\rho,\Lambda)
=\frac{1}{2\chi(\rho)V}\inf_{f\in\mathcal F_0(\Lambda^-)}
 \mathbb E_\rho\sum_{b\in E}c_b[\pi_b(\ell+f)]^2,
\quad\chi(\rho)=\rho(1-\rho). \tag{D1}
\]

It is exactly the open-cell marked-current coefficient from `FOLLOWUP.md`, divided by 2chi. The dual quantity is

\[
\nu_*(\rho,\Lambda,q)
=\frac{1}{2\chi V}\sup_u\mathbb E_\rho\sum_{b\in E}
 [ (\pi_b\ell_q)(\pi_bu)-\tfrac12c_b(\pi_bu)^2]
=\tfrac12q\overline D_*^{-1}(\rho,\Lambda)q. \tag{D2}
\]

For q=1 define H_L=overline D_*^(-1). Both U_L and H_L are nonincreasing along the exactly tiled cubes L=3^j by Proposition 4.1(4). Proposition 5.1 gives the same conductivity limit for the primal and dual families; Proposition 6.9 identifies it with the hydrodynamic conductivity. Consequently, at EVERY such finite scale,

\[
1/H_L(\rho)\le D(\rho)\le U_L(\rho),
\qquad 1\le U_L,1/H_L,D\le\lambda. \tag{D3}
\]

This is the essential certified finite-scale bracket. One does not infer it from two consecutive estimates looking similar. The exact issued-bond tiling and the source's common-limit identification are load-bearing. No arbitrary domain, periodic cell or changed boundary convention is substituted. The source algebraic convergence is not required to compute (D3), but does prove its width tends to zero polynomially in L uniformly on a compact density interval.

## 2. The dual cell is CLOSED; its outside is frozen

Let S=N_r(Gamma), Z=S minus Gamma. At the start of every independent run sample eta_Gamma and zeta_Z independently as Bernoulli(rho). **Hold zeta fixed throughout that run.** Evolve all sites of Gamma by exchanges along E with the rates c_b(eta_Gamma,zeta). This differs from the open primal cell, whose ghost bits are refreshed at each proposal. Confusing these two constructions invalidates the matching.

Conditional on the conserved count k in Gamma and the outside zeta, the stationary law is uniform on the k-particle shell. Product initialization automatically samples precisely the correct binomial count mixture; no rare shell is postselected and no table of all counts/outside patterns is enumerated.

Let G_c=-sum_(b in E)c_b pi_b and G_1=-sum_(b in E)pi_b, and put g_q=G_1 ell_q. In one dimension with q=1,

\[
g(\eta)=\eta_L-\eta_0,\qquad |g|\le1. \tag{D4}
\]

For every fixed count, g has mean zero. Empty and full shells have g=0. More generally g is a known boundary sum, computable from the cell geometry, with a polynomial supremum bound. Reversibility on each shell gives

\[
\sum_b\langle\pi_b\ell_q,\pi_bu\rangle
=2\langle g_q,u\rangle,
\quad\tfrac12\sum_b\langle c_b(\pi_bu)^2\rangle=\langle u,G_cu\rangle.
\]

Therefore the conditional dual optimization is

\[
\sup_u[2\langle g,u\rangle-\langle u,G_cu\rangle]
=\langle g,G_c^{-1}g\rangle,\qquad G_cu=g. \tag{D5}
\]

The inverse is on the mean-zero space of each count shell. The conditional maximizer may depend on k and zeta; Proposition 4.1(1), (4.9)–(4.11) allows these optimizers to be pasted into a single local function independent of rho. Thus the full product average gives exactly

\[
H_L(\rho)=\frac{\mathbb E_{k,\zeta}\langle g,G_c^{-1}g\rangle_{k,\zeta}}
{\chi(\rho)V}. \tag{D6}
\]

The factor is 1/(chi V), whereas nu_* is half of this expression. These normalizations are verified independently in the exact diagnostics below.

## 3. A fully numeric polynomial cell-gap bound

The issued graph on Gamma is connected. For every k and zeta, c_b>=1 implies its Dirichlet form dominates unit-rate symmetric exclusion on this finite graph. Caputo–Liggett–Richthammer's spectral-gap theorem equates the latter gap to the unit-rate random-walk gap. The primary v3 [PDF](https://arxiv.org/pdf/0906.1238v3) has main Theorem **1.2** and its exclusion consequence in **section 1.2.3**. The numbering Theorem 1.1/section 4.1.1 belongs to a different version and must not be mixed with this pin. All hypotheses hold: a finite connected undirected graph, symmetric unit edge weights, and a fixed particle count; uniform-shell stationarity remains valid after fixing zeta.

For a path of n=L+1 vertices, a deliberately weak explicit bound is

\[
\gamma_c\ge n^{-2}. \tag{D7}
\]

One can use the exact path eigenvalue 2[1-cos(pi/n)] instead. A general connected issued graph with n vertices and diameter d_G has random-walk gap at least 1/n^2 when d_G<=n-1, up to an inessential conservative factor: write uniform variance as (2n^2)^(-1)sum_(x,y)(f(x)-f(y))^2, telescope along shortest paths, and bound every edge's ordered-pair congestion by n^2. This gives the safe fully explicit bound 1/n^2. For clarity the operational theorem here uses the one-dimensional path. No homogenization constant and no minimum shell probability enters (D7).

## 4. Bounded finite-exposure dual estimator

Each conditional chain is stationary. Its spectral theorem implies

\[
H_L=\frac1{\chi V}\int_0^\infty\mathbb E[g(X_0)g(X_t)]dt,
\quad
0\le H_L-H_{L,\tau}
\le\frac{G_{max}^2e^{-\gamma_c\tau}}{\chi V\gamma_c}. \tag{D8}
\]

This uses mean zero on every shell, not just cancellation after mixing different conserved counts. The right side is explicit. In 1D G_max=1. Choose tau by the logarithm of this bound to make the tail <=e_H/4.

A practical estimator needs only one random-time readout. Independently choose S uniform in [0,tau], run the closed cell to S, and record

\[
Y_H=\frac{\tau}{\chi V}g(X_0)g(X_S). \tag{D9}
\]

Its expectation is H_(L,tau), and |Y_H|<=tau G_max^2/(chi V). Averaging M_H fresh runs and Hoeffding gives a two-sided statistical interval of radius e_H/4 with

M_H=O([tau G_max^2/(chi V)]^2 e_H^(-2)log(2/alpha_H)).

Add the nonnegative tail only to the upper endpoint. Clip H to [1/lambda,1]; its upper confidence endpoint H^+ is strictly positive, so 1/H^+ is a certified lower diffusivity bound.

In the digital version g is exact and the acquired table supplies rates; Poisson proposals have rate <=lambda V and act on O(V) bits. A hard proposal cap and finite-bit random-time/probability errors add explicit budgets. No matrix on 2^(L+1) states is built. Physical two-time readout is also possible under a declared nondestructive classical detector: use independent calibrated unbiased scores for the boundary occupations at the two times. If score magnitude is <=G_max/v_*, their product is unbiased and its bound increases by v_*^(-2). Initialization, frozen outside clamps, measurement, holding, detector calibration and systematic-bias refinement must all be paid. Unknown correlated detector noise does not preserve (D9).

For a physical source deviating from the declared product law by path/source TV e, the bounded score expectation changes by at most 2tau G_max^2 e/(chi V v_*^2). Thus inverse-polynomial preparation/control errors suffice at these polynomial durations, but are not automatically supplied. Acquiring a constant-radius microscopic table and simulating digitally avoids needing large physical closed cells.

## 5. The primal upper endpoint is particularly simple

The open-cell current formula in `FOLLOWUP.md` gives

\[
\frac{\mathbb EJ_\tau^2}{2\chi V\tau}\ge U_L,
\quad
0\le\frac{\mathbb EJ_\tau^2}{2\chi V\tau}-U_L
\le\frac{\lambda}{2\chi g_{open}\tau},
\quad g_{open}\ge a^2/(12L^2). \tag{D10}
\]

Therefore an upper statistical confidence endpoint for the finite-duration current-square mean is already a valid upper endpoint U^+ for U_L: no unknown asymptotic bias is subtracted. The explicit bias bound determines a sufficiently long exposure for efficient stopping. The correct noisy weighted-current square subtraction and total marked self-event convention remain as repaired in `FOLLOWUP.md`. In the scalar 1D theorem the nonzero marks are simply +/-1.

All primal variance caps and sample counts in that file are explicit polynomial functions of L, a^(-1), lambda, e_U^(-1), detector contrast and confidence. One may use the wasteful W,H,M recipe there or a directly verified tighter Poisson cap.

## 6. Density-uniform confidence intervals without a hidden modulus

Fix rho in [a,1-a]. Let m be the number of bits in the enlarged local envelope required by both cells. At fixed r, m=O(L). The normalized primal and dual variational quantities satisfy, for p,q in this interval,

\[
e^{-\theta}U_L(q)\le U_L(p)\le e^\theta U_L(q),
\quad
e^{-\theta}H_L(q)\le H_L(p)\le e^\theta H_L(q),
\quad\theta=(m+2)|p-q|/a. \tag{D11}
\]

For the primal, compare the Bernoulli weights of every nonnegative variational objective before taking infima, then include the chi normalization. For the dual, its conditional optimum w(k,zeta)=<g,G_c^(-1)g> is nonnegative and independent of rho, so the same product likelihood-ratio bound applies after averaging w; again include chi. The +2 pays the two factors in chi=rho(1-rho). This argument is not a bound on the signed finite-time single-run score; it is a modulus for the exact dual coefficient.

At scale L, choose density mesh radius h_L<=a epsilon/[C lambda(m+2)] and compute U^+,H^+ at every grid point. For any p nearest q, the interval

\[
I_L(p)=\left[e^{-\theta}/H_L^+(q),\ e^\theta U_L^+(q)\right]\cap[1,\lambda] \tag{D12}
\]

contains D(p) on the joint cell confidence event. Thus it is a uniform interval function on the ENTIRE density interval. The number of grid points is O(lambda m/(a epsilon)), polynomial. Only the observed endpoints enter the stopping test. There is no unknown D derivative or uncomputed functional.

## 7. Acquired-rate uncertainty and actual stopping algorithm

Acquire the local microscopic table to relative error eta<=epsilon/(64lambda), with one confidence event as in `FOLLOWUP.md`. Clip the acquired table to [1,lambda]. Its own homogenized diffusivity satisfies

(1-eta)D_true <=D_acquired <=(1+eta)D_true

by variational monotonicity. The primal/dual cell procedure computes certified bounds for D_acquired. Inflate any interval [ell,u] to

\[
[\ell/(1+\eta),\ u/(1-\eta)]\cap[1,\lambda]. \tag{D13}
\]

This retains a controllable O(lambda eta) noise floor. Alternatively use separate monotone lower/upper rate tables. No larger physical system is used to improve the error by assumption.

For target epsilon, perform stages j=1,2,... with L_j=3^j. At each stage:

1. Choose the density grid and explicit cell time/statistical error budgets, e.g. e_U<=epsilon/128 and e_H<=epsilon/(128lambda^2), with analogous width slack for (D11) and the rate inflation.
2. Acquire both finite-cell confidence endpoints for every grid point, using fresh digital randomness and all known caps. Allocate total failure probability alpha_j=alpha*2^(-(j+1)^2), distributed across that stage's finite cells. Its sum is <alpha.
3. Form the uniformly widened, rate-inflated intervals (D12)–(D13). Stop if their maximum width is <=epsilon. Return those intervals or their midpoint as an epsilon-accurate constitutive table. If an interval is inconsistent, continue/refine and retain the diagnostic rather than invent an endpoint.

On the one joint event, EVERY returned interval is valid, including at the data-selected stopping stage. This remains true without knowing any numerical homogenization constants. The published density-uniform algebraic convergence guarantees that the true primal-dual width is <=epsilon/4 at a scale L_* polynomial in epsilon^(-1) for the fixed physical class. The other error budgets fit the remaining slack, so a statistically good stage at or beyond L_* stops.

Per-stage costs are polynomial in L_j, epsilon^(-1), a^(-1), lambda and log(1/alpha_j). Therefore the accumulated work through the first such scale is polynomial in inverse accuracy at fixed class parameters. The constants/exponent depend on the published convergence theorem but need not be known by the algorithm. If an expected-runtime statement is desired, the squared-exponential alpha_j schedule is useful: after the convergence scale, reaching stage j+1 requires a statistical failure at stage j. Stage work grows only exponentially in j times a polynomial in j, while alpha_j decays as 2^(-j^2), so its expected tail is summable. This argument is conditional on the fixed acquired rate table; every clipped table satisfies the same ellipticity/range class, so it does not require a successful rate-learning event for termination. Correctness for the true material additionally uses that event.

This distinction matters: the procedure supplies an effective, observed stopping certificate; the theorem supplies a class-dependent polynomial complexity assurance. It does not supply a convenient numeric worst-case runtime constant or an optimized exponent. No unknown asymptotic constant appears in the returned error interval.

## 8. Scope earned and remaining gaps

At a chosen accuracy and confidence, the retained finite constitutive table covers all densities in [a,1-a]. A finite alphabet of microscopic kinetic laws can be acquired and certified once each. The same tables support new smooth product preparations and new finite homogeneous kinetic protocols through the nonlinear PDE solver in `FOLLOWUP.md`. The primitive-error and Galerkin estimates there are constructive and need no homogenization rate constant.

The numeric finite-N hydrodynamic constants in C17/C18 remain a separate limitation. Observed coefficient bracketing does not certify the finite-N hydrodynamic error. Arbitrary spatial/time force drives still require a verified driven entropy/corrector theorem. Initial source promises, physical same-law transfer, detector refinements, all reset/hold/control/heat/work costs and an equal-information incumbent remain explicit. This note closes the **effective conductivity stopping** gap only; it must not be presented as closing those other gates.

## 9. Exact diagnostic

`check_dual_bracket.py` checks 24 exact-fraction cells at L=3,5, rho=1/3,1/2,2/3, for both gradient rates 1+a(eta_(x-1)+eta_(x+2)) and nongradient rates 1+a eta_(x-1)eta_(x+2), with a=0,1. It solves only tiny diagnostic Poisson equations conditional on frozen outside/count and verifies the normalization, 1<=1/H<=U<=lambda, SSEP equality, and, in the gradient subclass, the known infinite-volume D=1+2a rho lying in the bracket. `dual_bracket_check.json` retains all values. All 24 cases pass.

The open primal cells at L=3,5 happen to have zero refreshed-ghost drift and hence zero Poisson correction, even for this nongradient rate. To avoid using only that easy special case, the script also checks the nongradient L=7, rho=1/2, a=1 cell: its exact primal value is 276736825/222538988, strictly below the uncorrected activity value 5/4. This passes a genuinely nonzero Green–Kubo-correction stress test. The earlier nine-cell current diagnostic remains valid but should not be described as having tested a nonzero corrector.

The algorithm above does not enumerate these states. The diagnostic checks factors, signs, frozen-vs-refreshed boundaries and the specific known comparator; it does not prove the infinite-volume source theorem or historical priority.
