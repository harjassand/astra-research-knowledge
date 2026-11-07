# Hostile review: acquired local conserved transport

Auditor, 7 November 2026. Reviewed constructor/FOLLOWUP.md initially at SHA256 a021718b23d28aba61faea5c4e39453f2d77b41be6516a959eeb56578193f508 and its repaired version ee7f7664000688683ee51ae808556efa60cf40287eb842bba7219e9e19987a06; also constructor/DUAL_ADAPTIVE_BRACKET.md SHA256 f1c50e5edf076ed24d4cd105c746a322940e687a45691dfd76597c5b0eb27247. The auditor's independent initial bytes remain unchanged. This review supplies proofs and constructive corrections; finite tests supplement them.

## 1. Verdict and earned scope

The exact primal marked-current cell, the polynomial cell-gap mechanism, finite-duration bias, corrected noisy square, density coverage, and one-dimensional nonlinear PDE discretization are mathematically sound after the stated repairs. The finite-alphabet entropy-reference restart is a valid bridge at the imported theorem's smooth/product-reversible scope and for each fixed finite protocol; it does not provide effective finite-N constants by itself.

The new dual-cell operation is also sound: the whole Lambda^+ must persist, while its outer environment stays frozen for each run. Conditional Poisson inversion, a numeric polynomial gap and a bounded correlation estimator give a computable dual endpoint. Combined with the source's finite-scale order and common limit, adaptive primal–dual stopping certifies the density-uniform diffusivity without needing numeric homogenization constants in the returned interval. The published quantitative convergence is used for complexity/termination. This closes the effective coefficient-stopping operation; it does not close the separate finite-N hydrodynamic, arbitrary-force or apparatus/advantage operations.

The elementary algebraic corrections were real: the tilted generator must subtract the total marked-event intensity, including self marks; and general weighted directions require a sum of squared mark magnitudes in the detector correction. Both were repaired before the reviewed current versions. Neither invalidates the repaired cell construction.

The mechanism remains a constructive combination of established non-gradient hydrodynamics, variational homogenization, reversible Poisson equations, spectral gaps and Monte Carlo. Historical novelty and favorable physical full cost are not established. The positive mathematical operation should nevertheless be preserved at its actual local, conserved, nonlinear scope.

## 2. Primary-source match and exact primal boundary law

The governing primary source is Funaki–Gu–Wang, arXiv:2404.12234v3, 14 January 2026, https://arxiv.org/html/2404.12234v3 . Its precise hypotheses are finite known range, spatial translation covariance, 1<=c_b<=lambda, and independence from the two exchanged occupancies. It is a speed-change exclusion process reversible under every homogeneous Bernoulli product law. No general Gibbs interaction or external-force theorem is imported.

Source (1.25)–(1.27) gives

xi.cbar(rho,Lambda).xi = (1/V)inf_f E_rho sum_(b in E)c_b[pi_b(ell_xi+f)]^2,

where f ranges over exactly F_0(Lambda^-), E=issued bonds overline(Lambda^*), V=|Lambda|. Source (1.40)–(1.42) defines Lambda^- by deleting the outer layer, E as {x,x+e_i} for x in Lambda, and Gamma=Lambda^+. Thus |E|=dV exactly. The open primal cell keeps only I=Lambda^- and freshly samples every required outside bit from Bernoulli(rho) at each proposal. Its stationary law is Bernoulli(rho)^I.

Reversal is a bijection on an exchange event together with its fresh outside configuration: globally swap the two endpoint bits. Product weight is preserved, c_b is unchanged by endpoint independence, and the mark changes sign. This proves marked reversibility, including events whose two endpoints lie outside I. Such events may carry a nonzero mark while leaving the persistent state unchanged. They contribute to the current variance and must not be discarded.

For a function f of the persistent interior, the event objective is exactly E_rho sum c_b[d_b+f(y)-f(x)]^2. Averaging persistent and fresh bits is the full Bernoulli expectation on the source envelope. Therefore minimizing over all persistent f is exactly the source's F_0(Lambda^-) problem, and v_L/V=xi.cbar.xi. It is neither a periodic cell nor a specimen with an arbitrary fixed boundary. For c=1, the normalization is cbar=2rho(1-rho)Id.

The marked generator must be written unambiguously as

L_z f(x)=sum_(y,d) r(x,y,d)[exp(zd)f(y)-f(x)].             (2.1)

If written as a positive tilted sum minus q_x f(x), q_x includes ALL marked-event intensities, including nonzero-mark self events. Only after cancellation at z=0 does this reduce to the ordinary persistent jump generator. A one-state cell with opposite self marks already shows why subtracting only the persistent exit rate is wrong: it would not satisfy L_0 1=0.

## 3. Full explicit path proof of the open-cell gap

This closes the constant in C4. Let ell be the number of interior sites in a first-coordinate column of the cube; for source Lambda_L=(-L/2,L/2)^d intersect Z^d, ell<=L. Empty interior is trivial. Let

S_swap=sum_(internal first-coordinate edges)E_pi[(Delta_b f)^2],
S_flip=sum_(positive first-coordinate boundary sites)E_pi[(Delta_x f)^2].

The actual persistent Dirichlet form satisfies

E_G(f)>=S_swap/2+a S_flip/2,

because internal rates are >=1 and the boundary refresh flips an endpoint with conditional rate >=min(rho,1-rho)>=a.

Bernoulli variance tensorization gives Var_pi(f)<=chi sum_(x in I)E_pi[(Delta_x f)^2], chi=rho(1-rho). Implement a flip at x by swapping its bit along its first-coordinate column to the positive boundary, flipping that boundary bit, then reversing the swaps. At most 2ell steps are used, and the resulting transformation flips exactly x while restoring every other persistent bit.

Before the single flip, every accumulated permutation preserves the product law. Afterwards the pushed-forward density is at most 1/a relative to it: only one Bernoulli bit was toggled, whose likelihood ratio is at most max(rho/(1-rho),(1-rho)/rho)<=1/a. Telescoping and Cauchy–Schwarz therefore give a factor at most 2ell/a times the sum of the reference-law edge-square terms along that path. Across all origins in a column, an internal edge is used at most 2ell times, and the boundary flip at most ell times. Hence

Var_pi(f)<=chi[(4ell^2/a)S_swap+(2ell^2/a)S_flip].

Since chi<=1/4 and a<=1/2, comparison with the actual Dirichlet form gives

Var_pi(f)<=ell^2 a^(-2) E_G(f),

g_open>=a^2/ell^2>=a^2/L^2.                              (3.1)

The stated a^2/(12L^2) is consequently conservative. The proof uses the actual issued-edge boundary reservoir and no thermodynamic material gap. Ghost-to-ghost self marks do not affect this persistent-state gap.

## 4. Current variance, duration, noisy square and simulation costs

Marked reversal gives

E sum r[d+Delta f]^2=A-4<j,f>+2<f,Gf>.

Thus the corrector satisfies Gf=j on mean-zero interior functions, and v=A-2<j,G^(-1)j>. Differentiating the correctly defined tilted semigroup gives

E_pi J_t^2=At-2integral_0^t(t-s)<j,exp(-sG)j>ds.

The finite-duration excess is

0<=E J_t^2/t-v=(2/t)<j,G^(-2)(1-exp(-tG))j>
 <=A/(g_open t),                                         (4.1)

using 2<j,G^(-1)j><=A from nonnegative variational energy. No unproved current decorrelation constant is needed beyond (3.1). Dividing by V gives C6/C7, and dividing further by 2chi gives D10.

For marks d_l with known magnitudes and independent sign-noise contrast v, corrected scores Q=sum_l Y_l/v satisfy, conditional on the true path,

E[Q^2]=J^2+(v^(-2)-1)sum_l d_l^2.

The correct statistic is therefore

[Q^2-(v^(-2)-1)K_2]/(Vt),  K_2=sum_l d_l^2.              (4.2)

Only when every nonzero mark has magnitude one is K_2 its event count. For a single mark d=1/2 and v=1/2, weighted correction gives the true square 1/4; subtracting the event-count correction instead gives expectation -2. General matrix recovery must retain known bond orientations/magnitudes, or use directions whose nonzero marks all have unit magnitude and adjust the norm constants. The current repaired text uses K_2. Independent noises at distinct records are essential; a generic correlated detector is not covered.

A Poisson upper clock of rate lambda dV controls all computational proposals. The explicit cap/sample construction is polynomial and its factorial-moment tail estimates are valid. For a physical assay which records only nonzero current marks, cap the counted K rather than assuming an observable rejected-proposal clock; K is itself Poisson dominated and controls the same bounded statistic. Digital uniformization may cap its actual proposal count. Bias and confidence budgets must include aborted runs, finite-bit transition sampling, source/control bias and detector calibration. A fixed unknown systematic floor does not vanish by repetition.

The open simulator need only generate the finitely many fresh outside bits actually needed by the selected local bond; locality permits a lazy refresh implementation at O(2^O(r^d)) work per proposal. Refreshing the whole outside envelope is also polynomial, as stated, but wasteful. Neither implementation enumerates every persistent configuration.

The finite-cell Poisson-corrector query sampler is for a specified rate table. For acquired rates it directly computes the acquired table's own corrector. A true-corrector guarantee needs an extra resolvent perturbation budget, unlike the conductivity variational comparison. If tau_mix bounds the integrated infinity-norm mixing resolvent and R bounds |j| and total rate, a sufficient bound is

||fhat-f||_infinity<=eta R tau_mix_hat[1+2R tau_mix],

by Ghat(fhat-f)=Delta j-Delta G f. The logarithmic minimum-product-weight mixing bound makes this polynomial. The corrected constructor text acknowledges this; conductivity/PDE prediction does not need to pay for the entire pointwise corrector.

## 5. Dual cell: exact support, kernel, factor and gap

The dual operation in DUAL_ADAPTIVE_BRACKET.md matches the source's Proposition 4.1 and (4.1), (4.9)–(4.11). Its support and boundary conditions are materially different from the open primal cell:

- Every site of Gamma=Lambda^+ is persistent and evolves on the issued graph E.
- The finite outside environment zeta in N_r(Gamma) minus Gamma is drawn Bernoulli(rho) once per run and then FROZEN.
- Conditional on zeta and the count k in Gamma, the stationary law is the uniform k-particle shell. Product initialization automatically draws the right binomial count mixture; no rare shell is postselected.

Let G_c=-sum_E c_b pi_b, G_1=-sum_E pi_b and g=G_1 ell_q. In one dimension Lambda={0,...,L-1}, Gamma={0,...,L}, q=1 gives g=eta_L-eta_0. Its mean is zero on every count shell, including g=0 on the empty/full shells. Endpoint independence gives reversible symmetric rates on each shell, even after fixing zeta.

The source's dual objective is

(1/(2chi V))sup_u[2<g,u>-<u,G_cu>].

The maximizer on each mean-zero shell is u=G_c^(-1)g, with value <g,G_c^(-1)g>/(2chi V). Its inverse-diffusivity quadratic form is twice nu_*, hence in 1D

H_L=D_*^(-1)=E_(k,zeta)<g,G_c^(-1)g>/(chi V).             (5.1)

The factor in D6 is correct. The kernel is not a global mean-zero kernel alone: conserved particle count and frozen outside are separate invariant variables. The conditional centering of g handles all of them. Source Proposition 4.1(1) allows the conditional maximizers to depend on count and outside and paste into one local, rho-independent function; this is exactly the required admissible class.

The issued graph on Gamma is connected. Rates c>=1 imply conditional Dirichlet domination of unit-rate exclusion on that graph. Caputo–Liggett–Richthammer arXiv:0906.1238v3, Theorem 1.2 and Corollary 1.3/section 1.2.3, therefore supplies its random-walk gap. For any connected n-vertex graph, writing uniform variance as (2n^2)^(-1)sum_(x,y)(f(x)-f(y))^2, telescoping over paths of length <=n-1, and using edge congestion <=n^2 gives a gap at least 1/n^2. In the operational 1D case n=L+1; the exact path eigenvalue 2[1-cos(pi/n)] is also available. There is no unknown homogenization constant or inverse rare-shell probability in this bound.

A frozen-outside chain cannot be replaced by one which refreshes the outside at every proposal. The independent diagnostic below gives D_*=1.4763062 for a particular frozen-outside cell but 1.6302473 after this invalid replacement. It changes the operator and its inverse, not merely an implementation detail.

## 6. Dual estimation, density modulus and adaptive certification

Because each conditional chain is stationary and centered,

H_L=(1/(chi V))integral_0^infinity E[g(X_0)g(X_t)]dt.

The nonnegative missing tail at time tau is at most

||g||_infinity^2 exp(-gamma_c tau)/(chi V gamma_c).         (6.1)

This is a conditional spectral-theorem bound averaged over count/outside. No minimum configuration probability is needed. Choosing a uniform independent time S in [0,tau], the bounded score tau g(X_0)g(X_S)/(chi V) estimates the truncated integral. Hoeffding, the explicit gap and digital proposal bounds give a polynomial finite-sample confidence interval. Physical two-time scores additionally require unbiased, independently calibrated readouts and no backaction on the classical state; an arbitrary correlated detector is not covered. The digital version needs no large physical dual cell after local-rate acquisition.

The finite-scale order is justified, not guessed from apparent numerical convergence. On exactly tiled 3-adic cubes, Proposition 4.1(4) makes both the primal U_L=Dbar and the dual inverse H_L=D_*^(-1) nonincreasing. Proposition 5.1 makes their associated conductivities converge to the same limit, and Proposition 6.9 identifies that limit with the hydrodynamic coefficient. Thus at every such scale

1/H_L<=D_infinity<=U_L.                                  (6.2)

The quantity on the right is the same open primal cell already verified. A finite-duration current-square upper confidence endpoint is automatically a valid upper endpoint for U_L, because the finite-duration bias is nonnegative. The tail upper endpoint for H_L yields a lower endpoint 1/H_L^+. The known bounds 1<=D_*,Dbar,D<=lambda guarantee safe positive inversion. Exactly tiled cells avoid an unproved boundary substitution.

The density-uniform extension in D11 is also valid. The primal objectives are nonnegative, so product-likelihood comparison followed by infimum works. The dual signed objective cannot be compared that way. Instead use the nonnegative conditional optimum w(k,zeta)=<g,G_c^(-1)g>, independent of rho, or equivalently its nonnegative Dirichlet energy. Product averaging then gives the likelihood bound for chi H_L. Including both factors in chi yields

exp[-(m+2)|p-q|/a]Q(q)<=Q(p)<=exp[(m+2)|p-q|/a]Q(q),

for Q=U_L or H_L. A mesh of radius O(a epsilon/[lambda(m+2)]) is therefore a computable uniform cover. It is a modulus for the exact cell coefficient, not for individual signed Monte Carlo scores.

Rate-learning uncertainty is correctly inflated using variational monotonicity: if the positive acquired table has relative error eta, then (1-eta)D_true<=D_acquired<=(1+eta)D_true. An acquired-model interval [ell,u] gives a true-model interval [ell/(1+eta),u/(1-eta)]. The local table must preserve endpoint independence and bond consistency when clipped; arbitrary directed rounding need not preserve the required physical class.

The current adaptive algorithm allocates alpha_j proportional to 2^(-(j+1)^2), uses the explicit finite-scale intervals over the whole density grid, and stops only at observed width <=epsilon. It has a valid joint confidence event across stages and densities. Source algebraic convergence guarantees an eventual scale polynomial in inverse accuracy at fixed class parameters. The unknown numerical constants/exponent enter the complexity assurance, not the returned error interval. Squared-exponential failure allocation is enough for expected polynomial runtime: after the true convergence scale, reaching the next stage requires a failed statistical interval at the present stage, whose probability beats geometrically growing polynomial-in-L stage work. Fresh conditional concentration or this allocation must be retained; merely summable errors with no runtime-tail analysis are not automatically enough for an expected-cost claim.

Termination does not require the physical rate-learning event: every clipped acquired table still belongs to the same elliptic/range class. Correctness for the actual material does require that event. The algorithm provides effective observed coefficient stopping, while it does not provide a convenient numeric worst-case runtime constant. For a finite kinetic alphabet, certify and retain all those density tables once to cover later finite protocols. Fresh stochastic coefficient queries outside those retained tables need their own confidence allocations or a stated uniform control net; one local-rate event does not itself make infinitely many later Monte Carlo errors disappear.

## 7. One-dimensional PDE and numerical solver checks

The PDE comparison is for equal-mass solutions and weak readouts; the mass mode must be treated separately. Let A'=D and Ahat'=Dhat lie in [1,lambda], and let sup|A-Ahat|<=delta_D on the actual density interval. For w=u-uhat, inverse-Laplacian testing gives

(d/dt)||w||_(dot H^-1)^2
 <=-||w||_2^2+delta_D^2
 <=-lambda_1||w||_(dot H^-1)^2+delta_D^2,

with lambda_1=(2pi)^2 on the unit torus. This proves C12, including arbitrary finite coefficient switches. With ellipticity lower bound a_D, the floor is delta_D^2/(a_D^2 lambda_1). Matching primitive additive constants on the acquired density interval avoids an unknown integral through unacquired endpoint densities. A globally elliptic Lipschitz extension is needed because Galerkin approximations can leave the physical interval.

For the Fourier Galerkin solver, write r=(I-P_M)uhat, e=P_Muhat-w_M, z=uhat-w_M=e+r. Then

(1/2)(d/dt)||e||_(dot H^-1)^2
 =-<e,Ahat(uhat)-Ahat(w_M)>
 <=-(1/2)||z||_2^2+(lambda^2/2)||r||_2^2.

The exact PDE L2 energy law gives integral||partial_x uhat||_2^2<=||u0||_2^2/2. Fourier tail bounds control both the integrated L2 tail and the terminal H^-1 tail by O(1/M); their Fourier orthogonality closes C14 with an absolute constant. No derivative of D or unknown profile smoothness modulus is used in this numerical estimate.

On the fixed mean Fourier space, the ODE is the H^-1 gradient flow of the convex energy integral Fhat(w), Fhat'=Ahat. Its gradient has Lipschitz constant beta_M<=lambda(2pi M)^2. Convex-gradient cocoercivity makes explicit Euler nonexpansive for step <=1/beta_M. The stronger step <=1/[lambda^2(2pi M)^2] makes its L2 energy nonincrease, because

||P_M partial_xx Ahat(w)||_2<=2pi M lambda||partial_x w||_2.

For K constant-control pieces, normalize Ahat(0)=0, so 0<=Fhat(w)<=lambda w^2/2. Exact Galerkin energy dissipation summed over pieces gives integral||dot w||_(H^-1)^2<=Klambda||u0||_2^2/2. The one-step defect is <=beta_M Delta integral_step||dot w||; nonexpansive telescoping and Cauchy–Schwarz yield C15. Steps must align with switches. A continuously varying coefficient needs a separate energy-variation bound; C15 does not automatically ignore its variation.

Quadrature is constructive: a finite trigonometric w with known L2 bound has polynomially bounded sup norm and derivative sup norm in M; Ahat is explicitly Lipschitz. Thus uniform-grid quadrature has a known polynomial modulus for all required Fourier coefficients. Per-step arithmetic errors accumulate linearly under the nonexpansive maps. The initial profile still needs a computable representation/evaluation/integration contract; an arbitrary mathematical C-infinity function is not a finite free input. The text appropriately pays profile integration and actual input bits.

## 8. Entropy restart for a finite new kinetic protocol

At a switch the microscopic state is not a new product state; empirical-density convergence alone would not justify restart. The reference-measure argument supplies the missing operation.

For the same current smooth profile rho, write the corrected reference as product-profile density times exp(R_F)/Z_F. In dimension d,

R_F=N^(-1)sum_x grad logit(rho(x/N)).tau_x F.

The normalized sup log-density ratio of two references is at most

2||grad logit rho||_infinity (||F_old||_infinity+||F_new||_infinity)/N,

up to the fixed dimension norm convention; one factor comes from the exponents and one from normalizers. Hence

h_new(mu)<=h_old(mu)+O((||F_old||+||F_new||)/N).             (8.1)

Proposition 7.1 bounds ||F_N|| by O(n^2log n), so with the permitted n=N^s this is O(N^(2s-1)log N). Source section 7.3, especially (7.56), is affine in the initial normalized entropy before Gronwall. This permits the finite restart recursion. The source states D in C-infinity([0,1]) in (1.16), and its smooth interior-density initial hypothesis yields smooth parabolic profiles; each fixed finite restarted profile is therefore admissible. A finite kinetic alphabet permits taking the required maxima of its rate-class parameters.

This checks the structural proof of C17 for each fixed finite protocol, subject to the imported entropy/hydrodynamic estimate. Its actual constants depend on elapsed times, number of switches, intermediate profile bounds and source parameters. They have not been extracted. No conclusion of uniform accuracy over all growing K,T or an executable numeric finite-N confidence service follows merely from C17's existence of C_*,kappa_*.

Product site-probability error zeta gives normalized KL O(zeta^2) when densities stay in [a,1-a], and the corrector adds O(||F_N||/N). Correlated source TV error zeta_TV instead gives normalized entropy O_a(zeta_TV)+h(zeta_TV)/N by finite-alphabet entropy continuity and the product minimum-weight bound. Thus it enters a mean-square hydrodynamic estimate linearly in zeta_TV, not automatically quadratically. If using its square-root weak-error bound, allocate zeta_TV=O(zeta^2); alternatively use direct TV coupling for a bounded final readout, which adds O(zeta_TV) to that readout's expectation. Single-site means alone do not control correlated source entropy.

Theorem 1.4 uses sup_t E||error_t||^2, not E sup_t||error_t||^2. This gives uniform individual-time bounds, not a single realization's simultaneous continuous path guarantee. The current text preserves that distinction. Arbitrary external force changes the endpoint-independence/stationary structure and still needs a new driven hydrodynamic proof; a weak O(1/N) microscopic rate tilt over diffusive time is not a small full-path TV perturbation.

## 9. Remaining accounting and independent diagnostics

The local microscopic Markov architecture, finite known range, endpoint independence, spatial homogeneity, shared rate tables and same-law transfer across specimens/sizes are structural physical promises. Finite pattern experiments do not exclude every hidden-range or apparatus-context model. The short-time calibration argument is sound inside this architecture: relevant hazard changes occur through finitely many local updates, giving an O(h^2) bias; inverse-visibility scores and h=Theta(eta) give the stated elementary eta^(-4) count with actual preparation, timing and systematic-bias floors. Positive consistent clipping preserves the product-reversible class.

Digital cells use no later material specimens, but all proposals, random bits, probability precision, stationary product placements, finite envelopes, caps and Monte Carlo confidence counts are paid. A physical open/closed cell has stronger reservoir refresh or frozen-clamp/counter requirements; it is not a passive specimen automatically available from the material. The huge conservative polynomial sample construction is not evidence of practical advantage. Compare against an equally informed conventional rate-learner plus Green–Kubo/variational homogenization and kinetic/PDE solver.

Independent checks are in checks/check_dual_cell.py and check_dual_cell_result.json. Eighteen cells use Lambda lengths 3 and 5, nongradient c_x=1+a eta_(x-1)eta_(x+2), a=0,1,2, and rho=1/3,1/2,2/3. They construct the whole persistent Gamma, freeze the two required outside bits, solve only diagnostic finite Poisson equations on count-centered sectors, and check energy normalization, SSEP equality, and the explicit gap. Maximum Poisson/energy discrepancy is 6.7e-16. The wrong refreshed-outside variant differs by as much as 0.1539411 in D_* (L=3,a=2,rho=2/3), establishing a concrete boundary-contract sensitivity. A separate one-mark detector check gives the correct expected square .25 and the invalid count-subtraction value -2. These are finite diagnostics; none replaces the imported infinite-volume theorem or establishes novelty/hardware.

The source file inspected is constructor/sources/funaki_gu_wang_2404.12234v3.html, SHA256 18350f0690e9bb0bb58ce3068f3407b752edc6c98dafc84ccb16b7c5d53252d2. The older v2 is preserved separately and is not silently substituted. Numeric homogenization constants are unnecessary for the adaptive coefficient interval after the dual repair; effective hydrodynamic constants, arbitrary forces, actual apparatus performance, historical novelty and matched practical advantage remain separate open gates.

### Final version check

The final constructor follow-up checked for the resolved corrector-resolvent constant and coefficient-gap supersession is FOLLOWUP.md SHA256 9b8e0b1a2fdc8680938e57fc2b0802e117cce2bf3b406906130bd3c26d521497. Its full infinity-operator mixing bound now correctly uses [2+|I|log(1/a)]/g. The final dual note is DUAL_ADAPTIVE_BRACKET.md SHA256 03dc2358a50a224fb625389e2a81a0d9de7a57a0f0ae0db33d2e948207d9c7b1; the final version explicitly preserves the finite-N hydrodynamic gap and records an additional exact nonzero-primal-corrector stress test at L=7. The auditor did not execute the constructor's diagnostics as an independent hardware or infinite-volume validation; the separate auditor diagnostic and analytic checks above are the independent evidence supplied here.
