# Constructor follow-up: acquired local nonlinear transport

7 November 2026. Written after reading the frozen peer reports. The initial report and its disclosure/exposure accounting remain unchanged.

Later constructive extension: `DUAL_ADAPTIVE_BRACKET.md` supplies a primal/dual observed stopping certificate for density-uniform conductivity acquisition, removing the need to supply numeric homogenization constants to the coefficient algorithm. References below to that particular coefficient-stopping limitation record the earlier stage and are superseded by the linked note. The separate finite-N hydrodynamic constants and arbitrary-force extension remain open.

## Outcome and exact status

The stronger local route has a real constructive operation: **the finite-cell conductivity is estimable in polynomial time and samples without enumerating its exponentially many microscopic configurations**. Its cell gap is derived from the physical exchange rates and explicit Bernoulli reservoirs. A finitely acquired local rate table drives a kinetic Monte Carlo sampler for all these cells. In one dimension the acquired constitutive law has a computable nonlinear PDE solver with an energy error certificate requiring no unknown smoothness modulus. New finite sequences of homogeneous kinetic controls can be obtained by an explicit entropy restart argument.

This is a constructive composition of established homogenization with new derivations of acquisition/error accounting, not a new foundational physical mechanism. Numeric constants in the imported homogenization/hydrodynamic theorem have not been extracted; its entire 109-page proof has not been independently re-established. Arbitrary new weak external force fields are not covered by the imported theorem or by the kinetic-control concatenation. Hardware, favorable full cost and historical novelty are NOT_ESTABLISHED. The broad objective remains OPEN.

## 1. Current governing source

The primary source is Funaki–Gu–Wang, [arXiv:2404.12234v3](https://arxiv.org/html/2404.12234v3), 14 January 2026. The frozen initial used the older v2; preserve both. In v3, Hypothesis 1.1 requires known finite range, translation invariance, rates in [1,lambda], and independence of the two exchanged occupancies. Theorem 1.3 constructs density-uniform correctors. Theorem 1.5 gives algebraic finite-cell conductivity convergence. Theorem 1.4 gives a quantitative H^(-alpha) hydrodynamic error for alpha>d/2, uniformly for individual times in [0,T], under its smooth-profile/normalized-entropy source condition. Proposition 7.1 supplies corrector support <=n and sup norm <=C n^2 log n. Section 7.3 gives the entropy estimate needed for restart.

No arbitrary external-force theorem is stated there. The finite-cell experiment below is matched exactly to its variational coefficient rather than substituted from a periodic or differently bounded cell.

Pins in `sources/`:

- `funaki_gu_wang_2404.12234v2.html`: SHA256 `390d164e8bea5bc0063170e0c79fdd11f43af1464795b1e72ac0a2e616d310bd`.
- `funaki_gu_wang_2404.12234v3.html`: SHA256 `18350f0690e9bb0bb58ce3068f3407b752edc6c98dafc84ccb16b7c5d53252d2`.
- `funaki_gu_wang_2404.12234v3.txt` is an inspection aid retaining math alt text.

## 2. Exact marked-current realization of the finite-cell coefficient

This lemma works in any fixed lattice dimension d. Let V=|Lambda_L|, I=Lambda_L^- (remove its outermost layer), and E=overline(Lambda_L^*) for the source's issued-bond convention, so |E|=dV. Enlarge to a finite set S containing all sites needed to evaluate these local rates, and put G=S minus I. At fixed interaction range, |S|<=C_(d,r)V. Fix rho in [a,1-a], a>0, and |xi|<=1.

The persistent state is eta_I. At each proposal independently draw all ghost bits eta_G as Bernoulli(rho), select a bond b={x,x+e_i}, accept its exchange at rate c_b(eta), update only eta_I to (eta^b)_I and record

\[
d_b(\eta)=\xi\cdot e_i(\eta_x-\eta_{x+e_i}). \tag{C1}
\]

Ghost-to-ghost events may have nonzero marks without changing eta_I. **They must be recorded**. Dropping them changes the coefficient. An exact digital implementation uses a Poisson proposal clock of rate R=lambda dV, a uniform issued bond, fresh ghost bits, and acceptance probability c_b/lambda. This is a local simulation on O(V) bits. A physical implementation would require paid, controllable reservoir refresh and a current counter; it is not automatically a passive finite piece of the original material.

The persistent stationary law is pi=Bernoulli(rho)^I. The marked process is reversible: reverse an exchange and simultaneously replace ghost bits by their exchanged values. The product weight and c_b are unchanged because c_b does not depend on endpoint occupancies, while d changes sign. This pairing includes persistent-state self events.

Write L for the persistent generator, G_0=-L, J_t for the sum of marks,

\[
j(x)=\sum_{\text{marked moves }x\to y}r(x,y,d)d,
\qquad A=\mathbb E_\pi\sum r d^2\le\lambda dV.
\]

All sums average ghost configurations. Marked reversibility gives, for any interior function f,

\[
\mathbb E_\pi\sum r[d+f(y)-f(x)]^2
=A-4\langle j,f\rangle_\pi+2\langle f,G_0f\rangle_\pi. \tag{C2}
\]

The mean of j is zero. Minimization on mean-zero functions yields f=G_0^(-1)j and

\[
v_L(\rho,\xi):=\lim_{t\to\infty}\frac{\mathbb E_\pi J_t^2}{t}
=A-2\langle j,G_0^{-1}j\rangle
=\inf_f\mathbb E_\pi\sum r[d+\nabla f]^2. \tag{C3}
\]

**Matching proof:** d_b=pi_b ell_xi, f ranges over exactly F_0(Lambda_L^-), and averaging interior plus ghosts is the full Bernoulli expectation. Thus v_L/V=xi.cbar(rho,Lambda_L).xi in the source's (1.25). It is neither a periodic approximation nor an arbitrary-boundary one. The normalization is c=1 => cbar=2rho(1-rho)I.

## 3. Polynomial cell gap and finite-exposure bias

### 3.1 The gap is physically derived

A conservative explicit comparison gives

\[
g_L\ge a^2/(12L^2). \tag{C4}
\]

For integer cubes large enough to contain an interior, the proof uses only the following operations. Bernoulli variance tensorizes:

Var_pi f <=rho(1-rho) sum_(x in I) E_pi[f(eta^x)-f(eta)]^2.

Move the spin at x along a straight first-coordinate path to the boundary, flip it using the Bernoulli reservoir, then reverse the swaps. The path has at most 2L+1 moves. Swaps preserve pi. After the single flip the pushed-forward density is at most a^(-1) times pi. Each edge in a column belongs to at most L paths and is used at most twice. Telescoping/Cauchy–Schwarz bounds the product variance by C L^2/a times the sum of internal-swap and boundary-flip square differences. Actual internal rates are >=1, and averaged boundary flip rates are >=a, so the Dirichlet form dominates a/2 times that sum. Enlarging constants gives (C4); tiny cells can be treated separately. No thermodynamic-volume gap is being assumed. The full material retains its diffusive conserved field.

### 3.2 Exact finite-duration control

Define the marked tilted generator L_z f(x)=sum_(y,d) r(x,y,d)[e^(zd)f(y)-f(x)], with the sum including all marked self events y=x. Thus its subtraction uses the total marked-event intensity, not just the exit intensity of the persistent state; at z=0 the self terms cancel. Twice differentiating E_pi exp(zJ_t)=<1,exp(tL_z)1> and using <1,L'_0f>=-<j,f> gives

\[
\mathbb E_\pi J_t^2=At-2\int_0^t(t-s)\langle j,e^{-sG_0}j\rangle ds. \tag{C5}
\]

The spectral theorem and (C3) imply

\[
0\le\frac{\mathbb EJ_t^2}{t}-v_L
=\frac2t\langle j,G_0^{-2}(1-e^{-tG_0})j\rangle
\le\frac{A}{g_Lt}. \tag{C6}
\]

The last step uses 2<j,G_0^(-1)j><=A, since the variational infimum is nonnegative. Conductivity finite-exposure error <=delta follows from

\[
\tau\ge\lambda d/(g_L\delta)=O(\lambda dL^2/(a^2\delta)). \tag{C7}
\]

Initialization is a paid product placement of O(V) Bernoulli bits, not waiting for macroscopic equilibrium.

### 3.3 Finite noisy records and exact counts

For a physical cell assay suppose every current-carrying exchange is counted, its bond orientation is recorded, and the particle-motion sign is independently flipped by a calibrated detector of contrast v>=v_*>0. Write a_l=xi.e_(i_l) for the known directional weight of event l, so its true mark is d_l=a_l sigma_l with sigma_l in {-1,1}. Given the true trajectory, put Q=sum_l a_l Y_l/v and K_2=sum_l a_l^2=sum_l d_l^2. Then

\[
S=\{Q^2-K_2(v^{-2}-1)\}/(V\tau) \tag{C8}
\]

is unbiased for J_tau^2/(Vtau). Indeed the conditional detector variance is (v^(-2)-1)sum_l a_l^2. For one dimension or a unit coordinate direction all nonzero marks have magnitude one, and K_2 is simply their count K; substituting K for K_2 for a general matrix direction would be wrong. Events with a_l=0 contribute zero. The subtraction is essential: squaring a visibility-corrected noisy current alone creates false conductivity. This contract does not silently cover uncounted or mislocated jumps. Distinct physical runs must be fresh; correlations within each run are handled by (C5). Since |a_l|<=1 and K_2<=K, every cap and polynomial resource bound below is unchanged.

Cap a run if its proposal count exceeds H. A Poisson variable of mean Rtau dominates that count. Its explicit tail and fourth moment permit H=C[Rtau+log(MQ_rho d^2/delta_A)] with truncation bias <=delta/8. On the cap event |S|<=B_S=C H^2/(v_*^2 Vtau). Hoeffding needs

\[
M\ge C B_S^2\delta^{-2}\log(2Q_\rho d^2/\delta_A). \tag{C9}
\]

All counts are polynomial in L,a^(-1),lambda,delta^(-1),v_*^(-1), with logarithmic confidence factors. The occurrence of M inside log is removed by any sufficiently large explicit polynomial upper count, or by computing and verifying a Poisson quantile for a proposed finite M. Per density/direction expected updates are MRtau; naive ghost refresh costs O(MRtau |G|). Memory is O(V+local-table size), plus summaries or raw evidence as retained. Hard caps and finite-bit probability simulation add declared failure/bias budgets.

For a deliberately wasteful completely explicit choice, take tau>=1, delta<=1, let q be the total number of density/direction cells, and set W=max(2,Rtau,q/delta_A,delta^(-1),v_*^(-1)), H=ceil(100W^2), M=ceil(10^12 W^20). Then |S|<=4H^2/(v_*^2 Vtau)<=C W^6, Hoeffding error <=delta/4 holds jointly over q cells, and Mq times the Poisson tail beyond H is smaller than delta_A/4. The omitted-tail expectation is bounded by the Poisson factorial-moment identities E[K(K-1)1_(K>H)]=mu^2 P(Pois(mu)>H-2), E[K1_(K>H)]=mu P(Pois(mu)>H-1), mu<=W; the bound (e mu/H)^H makes it <=delta/8. This gives an explicit polynomial construction without solving an implicit sample-count inequality; practical implementations should use the much smaller verified quantile/count calculation.

The digital version sets v=1 and uses acquired rates. It needs no new specimens after local-table acquisition, and charges all random proposals and arithmetic. This is the simplest operational algorithm. For an actual noisy cell, unknown systematic current/source errors can be amplified by squaring and are not removed by more runs. A calibrated path-TV error e changes the capped statistic by at most 2B_S e. All control, preparation and readout refinement needed to reach that inverse-polynomial budget must be charged.

## 4. Uniform densities, controls and corrector queries

Let m=|S|. For p,q in [a,1-a], every Bernoulli product likelihood ratio on S lies in exp(+-m|p-q|/a). Apply this to each nonnegative variational objective before taking infima:

\[
e^{-\theta}v_L(q,\xi)\le v_L(p,\xi)\le e^\theta v_L(q,\xi),
\qquad\theta=m|p-q|/a. \tag{C10}
\]

Because v_L/V<=lambda d, density spacing a delta/(C lambda d m) gives a uniform covering with Q_rho=O(lambda d m/(a delta)) entries. Only O(d^2) directions are needed for matrix conductivity. Affine combinations of finitely many acquired rate tables can be queried directly by the same cell sampler; relative rate comparison also provides a uniform control modulus.

The finite-cell Poisson corrector has polynomial *query evaluation*, although listing all 2^|I| values is exponential. Since pi_min>=a^|I| and |j|<=R,

|P_tj(x)|<=R min(1,a^(-|I|/2)e^(-g_Lt)),
f(x)=integral_0^infinity P_tj(x)dt.

Take tau_f >=g_L^(-1)[(|I|/2)log(1/a)+log(R/(g_L epsilon_f))]. The remaining tail is <=epsilon_f uniformly in x. Starting the acquired-cell simulator at a queried x and averaging integrals of the known j estimates f(x); every integral is bounded by Rtau_f. O(R^2tau_f^2 epsilon_f^(-2)log(1/delta_f)) runs suffice. This does not mean a finite array has stored an entire arbitrary corrector, or that the source's density-free corrector has already been assembled. The PDE predictor only needs conductivity. The use of log(pi_min^(-1)) is polynomial in volume; substituting pi_min^(-1) would unnecessarily make the bound exponential.

The corrector sampling estimate first treats its specified finite rate table as exact; simulating an acquired table computes that table's corrector. A true-table comparison can also be paid polynomially. Let T_mix bound the mean-zero inverse-generator infinity norm; the conservative full infinity-operator estimate is T_mix<=g_L^(-1)[2+|I|log(1/a)], obtained by integrating min(2,a^(-|I|/2)e^(-g_Lt)). Use the analogous That_mix for the acquired table. Relative rate error eta gives ||deltaj||infty<=eta R and ||deltaG||infty-to-infty<=2eta R. The identity Ghat(fhat-f)=deltaj-deltaG f therefore gives ||fhat-f||infty<=eta R That_mix(1+2R T_mix). Refine eta to fit the allocated corrector error. This extra precision is unnecessary for the sharper conductivity monotonicity estimate (C11).

## 5. Noisy acquisition of the microscopic law

Known finite range, translation invariance and the local Markov update architecture are physical structural promises, not conclusions certified against arbitrary hidden-range models. At fixed r,d there are only P=d*2^O(r^d) local patterns. For each prepare a constant-radius pattern with central bond 10. Short native evolution gives

P(central exchange by h)=c(pattern)h+O(C_(d,r)lambda^2h^2).

The bias follows by integrating the probability that a relevant local update has changed the hazard; a constant-radius buffer or a standard bounded-rate influence estimate handles exterior updates. Alternatively count central-bond events. Known nonzero detector contrasts permit corrected bounded scores. With h=Theta(eta), inverse-polynomial preparation/clock bias budgets and O(eta^(-4)log(P/delta_A)) fresh releases per pattern, the elementary estimator attains absolute rate error eta. Efficient event-time estimators may improve the exponent. Reset, clamps if used, clocks, readout, calibration and refinement costs multiply the actual counts. A residual score bias divided by h is a real floor.

Clip estimates to [1,lambda] in the containing dictionary; endpoint independence and reverse-bond consistency must be preserved. On the one uniform rate event, eta<1 gives

\[
(1-\eta)\mathbf c(\rho)\preceq\widehat{\mathbf c}(\rho)
\preceq(1+\eta)\mathbf c(\rho), \tag{C11}
\]

and likewise for every finite-cell coefficient. This follows immediately by comparing all nonnegative variational objectives before minimizing. It is uniform in density and convex combinations of finitely many calibrated tables. In 1D comparison with SSEP gives 1<=D<=lambda, hence |Dhat-D|<=lambda eta before cell/statistical errors. This avoids extensive physical-state sensitivity.

Given valid numerical constants C_h,gamma_h from Theorem 1.5, choose L >=(C_h/delta_c)^(1/gamma_h). Combining (C6),(C9),(C10),(C11), then dividing by 2rho(1-rho), gives a uniform D approximation on [a,1-a]. The division costs at most [2a(1-a)]^(-1). Clip Dhat to [1,lambda], interpolate and integrate its explicit table to an increasing primitive Ahat. Choose the density cutoff to contain the whole PDE trajectory; unforced scalar diffusion preserves the initial range. Do not extrapolate unacquired endpoint behavior.

Only the primitive up to an additive constant matters. For coefficient-error comparison choose A(a)=Ahat(a)=0, so its uniform error on the acquired interval is at most its length times the diffusivity error. For numerical convex-energy bounds Ahat can separately be shifted to Ahat(0)=0 after its elliptic extension; neither the PDE nor its Fourier ODE changes. This avoids charging an unknown integral through unacquired densities.

At fixed class parameters and valid source exponents, all operations are polynomial in inverse coefficient accuracy. The exponent can be very large. The paper does not provide a turnkey numeric pair C_h,gamma_h, and I have not extracted them. This is a proved reduction conditional on effective imported constants, not a numeric certificate service already completed today.

## 6. Fully computable one-dimensional nonlinear PDE

Put A'=D in [1,lambda]. For equal-mass solutions u_t=partial_xx A_t(u) and uhat_t=partial_xx Ahat_t(uhat), assume sup_(t,rho)|A_t-Ahat_t|<=delta_D. Let E=||u-uhat||_dotH^-1^2 and lambda_1=(2pi)^2. Testing with the inverse Laplacian gives

E'<=-||u-uhat||_2^2+delta_D^2<=-lambda_1 E+delta_D^2,

hence

\[
E(t)\le e^{-\lambda_1t}E(0)+\delta_D^2/\lambda_1. \tag{C12}
\]

This horizon-free coefficient-error improvement was supplied by the principal during follow-up; the calculation independently checks. It holds across arbitrary finite kinetic switches. With lower ellipticity a_D instead of 1, replace decay by a_D lambda_1 and the floor by delta_D^2/(a_D^2 lambda_1). Add mass mismatch separately.

An explicit spatial solver avoids a hidden smoothness oracle. Extend Ahat globally with derivative in [1,lambda], let P_M project onto Fourier modes |k|<=M, and solve the nonlinear finite ODE

\[
\dot w_M=P_M\partial_{xx}\widehat A_t(w_M),\qquad w_M(0)=P_Mu_0. \tag{C13}
\]

Write r=(I-P_M)uhat and e=P_Muhat-w_M. Then

(1/2)d||e||_dotH^-1^2/dt
=-<e,Ahat(uhat)-Ahat(w_M)>
<=-(1/2)||uhat-w_M||_2^2+(lambda^2/2)||r||_2^2.

The L2 energy law gives integral_0^T||partial_x uhat||_2^2<=||u0||_2^2/2, independently of switching. Therefore

\[
\sup_{t\le T}\|\widehat u_t-w_M(t)\|_{\dot H^{-1}}
\le C\lambda\|u_0\|_2/[2\pi(M+1)]. \tag{C14}
\]

This uses only the uniform ellipticity/Lipschitz primitive, not derivatives of learned D. The retained state dimension increases with accuracy and its ODE remains nonlinear.

For time computation, (C13) is a convex gradient flow in H^(-1), with gradient Lipschitz beta_M=lambda(2pi M)^2. Explicit Euler maps are nonexpansive in that norm for Delta<=1/beta_M. Taking also Delta<=1/[lambda^2(2pi M)^2] makes the L2 energy nonincrease: expand one step and use ||partial_xx P_M Ahat(w)||_2<=2pi M lambda||partial_xw||_2. Align steps with all K control switches. On the exact Galerkin path, integral_0^T||dot w_M||_H^-1^2<=Klambda||u0||_2^2/2, by summing the convex energy dissipation over pieces while L2 never grows. Nonexpansive Euler telescoping gives the conservative temporal error

\[
E_{time}\le C\beta_M\Delta\sqrt{K\lambda T}\|u_0\|_2. \tag{C15}
\]

Certified quadrature of the explicit Lipschitz Ahat composed with a finite trigonometric polynomial computes its Fourier coefficients with a polynomial modulus in M, precision and the known L2 bound. Per-step H^(-1) arithmetic error theta adds at most (#steps)theta. Thus M=O(lambda/epsilon), inverse-polynomial Delta and theta provide a polynomial algorithm in inverse accuracy, T and finite control-list length. Input profile integration, new-control description length and probability/bit precision are paid. A bounded weak readout of H^1 norm <=1 inherits these errors directly.

## 7. New preparation and new kinetic-drive theorem

### Product source is sufficient; no thermal oracle

The source theorem's reference measure has a corrector exponent

R_N=N^(-1)sum_x partial_x logit(rho0(x/N)) tau_x F_N.

A smooth-profile Bernoulli product already differs in normalized relative entropy by <=C||F_N||infty/N. With the source's F_N=Phi_floor(N^s), 0<s<1/[8(d+2)^2], this is O(N^(2s-1)logN). The user need not prepare the second-order corrected state.

If independently prepared site probabilities differ from the desired rho0(x/N) by at most zeta, their normalized product KL is <=C_a zeta^2; add the same corrector term. Section 7.3's bound is affine in initial entropy before Gronwall, so the weak-observable error has an extra C_T zeta term. One can instead take polynomially shrinking zeta_N to satisfy the literal initial condition in Theorem 1.4. Correlated writer noise requires its own entropy bound; single-site mean accuracy is insufficient. A global writer-TV budget zeta_TV can be converted using finite-alphabet entropy continuity to normalized entropy O(zeta_TV)+h(zeta_TV)/N, not by claiming independent errors.

Every new source pays N placements, independent random bits, calibrated thermal pins/resets, achieved precision, clocks, work/heat and detector refinement. If the physical target is actually run, its N^2T microscopic horizon also pays its N-site holding, local update, drive, readout and reset costs. In 1D its expected number of native update opportunities is O(lambda N^3T). Numerical prediction does not reenact that horizon.

### New homogeneous kinetic sequences

Fix a finite alphabet of homogeneous local exchange tables c^(1),...,c^(q), each satisfying Hypothesis 1.1 and acquired once. A future query gives a previously unperformed finite sequence (a_1,t_1),...,(a_K,t_K), total macroscopic duration T. On piece j the physical generator is N^2 L_(c^(a_j)) and the PDE is

\[
\partial_t\rho=\partial_{xx}A_{a_j}(\rho). \tag{C16}
\]

This is a new driven protocol preserving the common homogeneous Bernoulli equilibrium family. It is not arbitrary force or thermodynamic driving.

At a switch, the old and new corrected reference measures for the SAME current smooth profile have the same product part. Their log density ratio per volume is bounded by C[||F_N^old||infty+||F_N^new||infty]/N=O(N^(2s-1)logN). Hence the new initial normalized entropy is bounded by the old final normalized entropy plus this amount. Apply the source's quantitative entropy estimate on each piece and iterate. For each fixed finite protocol, finite alphabet and smooth source there are C_*,kappa_*>0 such that

\[
\sup_{t\le T}\mathbb E\|\rho_t^N-\rho_t\|_{H^{-1}}^2
\le C_*[\zeta^2+N^{-\kappa_*}]. \tag{C17}
\]

The proof needs that entropy-reference switch; empirical-density convergence alone would not justify restarting. Constants can worsen with K, T and the intermediate profile bounds. No fixed all-protocol/all-horizon microscopic constant is asserted. Uniformity over a bounded protocol class requires actually tracing those dependencies. Every finite protocol is legitimate without presuming it appeared in acquisition.

On the one uniform microscopic-table event, for any declared protocol and mean-zero weak phi with ||phi||_H1<=1,

\[
\mathbb E|\langle\phi,\rho_t^N\rangle-\langle\phi,\rho_t^{num}\rangle|
\le\sqrt{C_*}(\zeta+N^{-\kappa_*/2})
+\delta_D/\sqrt{\lambda_1}+C\lambda/M+E_{time}+E_{arithmetic}. \tag{C18}
\]

Add the mass mode, source and detector errors as applicable. Markov/Chebyshev yields an individual-specimen probability. With effective imported constants this is a size/horizon/noise/preparation/control/all-count theorem for local interacting conserved matter. Numeric constant extraction is still missing for an operational certificate. The PDE error is horizon-free at fixed coefficient error; the microscopic switched-hydrodynamic estimate is not thereby uniform over unrestricted K,T.

## 8. Why arbitrary weak external-force driving is still open here

Tilting bond rates by exp[E(t,x/N).e_i(eta_x-eta_y)/(2N)] formally suggests

partial_t rho=partial_x[D(rho)partial_xrho-chi(rho)D(rho)E],

with the chosen force normalization and chi=rho(1-rho). Acquiring equilibrium conductivity does not establish this driven quantitative hydrodynamic theorem.

Two shortcuts are invalid. A finite-drive current is not its derivative: a remainder bound involving cell generator norms and inverse gap must be proved, and its inverse-polynomial drive amplitude/relaxation/readout costs charged. Equilibrium variance avoids this extrapolation for acquiring the coefficient, not for proving the driven infinite-volume law. Also, a weak O(1/N) perturbation over N^2 time has path relative entropy of order N^d, so the full driven path is not close in TV to the unforced path. One cannot inherit (C17) by a small path coupling.

The constructive missing operation is the second-order entropy/corrector cancellation with the new space/time field, its drive-modified corrector, time derivatives and PDE density bounds. The finite-cell coefficients and their uncertainties are now computable. An actual quantitative driven proof and effective constants remain required. General nonproduct Gibbs measures require an additional physical conditional-mixing derivation; the present product-reversible class does not solve that automatically.

## 9. Principal mass-metric lemma check

I independently checked `../principal/MASS_METRIC_REPAIR.md` in finite dimensions. The resolvent identity and bounds are correct. Douglas factorization justifies replacing the noncommuting C square root by the A square root. The left inner contour arc includes the common zero mode. Constant 8d/(1-d) is safe. An elementary bound for the ray integral is integral_1^infinity e^(-r/2)/r dr <=e^(-1/2)log2+e^(-1)<1 by splitting at 2. This confirms the fixed-control repair; it does not extend itself to arbitrarily switched metrics.

## 10. Diagnostic and ledger

`check_cell_current.py` uses exact fractions in a diagnostic with three active spins and fresh ghosts. Nine combinations of rho and the nongradient rate 1+a eta_(x-1)eta_(x+2) verify marked reversibility, Poisson equation, Green–Kubo = Dirichlet objective, nonnegativity, SSEP factor 2rho(1-rho), and the conservative gap bound. `cell_current_check.json` preserves the output. Enumeration is only a sign/factor/boundary diagnostic; the proposed algorithm uses kinetic Monte Carlo.

The principal identified the general-direction detector correction and tilted-generator notation after this report's first review. Both are repaired above. A new exact detector diagnostic uses weights 1/2 and 1/3, true signs +1 and -1, and contrast 1/2: K_2 subtraction has mean 1/36, exactly the target squared current, whereas replacing K_2 by the event count gives -44/9. This explicitly checks the correction rather than relying on the one-dimensional/unit-weight cell tests.

Proved in this follow-up: exact cell matching; current identity and duration bias; derived polynomial gap; density coverage; local-rate error monotonicity; polynomial corrector query sampling; 1D PDE coefficient, space and time error estimates; source-reference switch and finite kinetic-drive concatenation conditional on the imported entropy estimate.

Imported, not reproved: quantitative homogenization and unforced quantitative entropy/hydrodynamic limit at their exact uniformly elliptic, finite-range, product-reversible scope.

Conditional/open: effective constants, full arbitrary-new-force driven hydro, physical acquisition/refinement realization, matched full-cost advantage and historical priority. C17 is an imported-entropy/finite-switch extension with no operational numeric certificate until the constants and complete applicability checks are supplied. The finite-cell matching/acquisition theorem is the strongest local operation actually proved here. This is a useful acquired local constitutive operation, but it must not be renamed a generic new principle of emergent matter.
