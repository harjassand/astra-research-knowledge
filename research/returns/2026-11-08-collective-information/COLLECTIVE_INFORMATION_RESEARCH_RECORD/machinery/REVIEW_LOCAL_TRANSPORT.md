# Independent source and applicability review: acquired local transport

7 November 2026. Reviewed constructor `FOLLOWUP.md` at SHA256 `a021718b23d28aba61faea5c4e39453f2d77b41be6516a959eeb56578193f508`. Principal requested an additional dual-cell constructive check during review. This file preserves both the review and that additional derivation. No further agents were spawned.

## 1. Verdict

The ghost-current construction matches the actual Funaki–Gu–Wang finite-volume coefficient, including the issued-bond convention, outermost excluded layer and marks on persistent-state self events. It is a deliberately constructed reservoir cell, not a native closed subvolume of the material.

The finite-alphabet kinetic restart is mathematically justified **for each fixed finite protocol** by changing the second-order reference measure at each switch and using the affine initial-entropy term in source equation (7.56). It is not a uniform theorem for unrestricted protocol length/horizon, arbitrary external force, arbitrary writer correlations or unknown source profiles. Numeric hydrodynamic constants remain unextracted.

There is a further constructive improvement: an exactly matched **closed dual cell** gives a computable lower bound on diffusivity. In one dimension a derived polynomial canonical gap controls its correlation tail. Combining it with the primal upper bound yields an adaptive confidence-interval stopping rule for the constitutive law that does **not** need numeric homogenization constants or exponents. Those constants enter only the proof of polynomial stopping scale. This does not remove the separate finite-N hydrodynamic constants gap.

All relevant mechanisms have strong predecessors: Green–Kubo/current fluctuations, finite-cell homogenization, canonical exclusion gaps, kinetic Monte Carlo and entropy hydrodynamic limits. Historical novelty of the synthesis remains **UNKNOWN**; full-cost advantage and hardware implementation are **NOT ESTABLISHED**.

## 2. Exact source pin and imports

Primary: Funaki–Gu–Wang, *Quantitative homogenization and hydrodynamic limit of non-gradient exclusion process*, [arXiv:2404.12234v3](https://arxiv.org/html/2404.12234v3), 14 January 2026. Independently retrieved HTML SHA256:

`18350f0690e9bb0bb58ce3068f3407b752edc6c98dafc84ccb16b7c5d53252d2`.

Cache: `source/2404.12234v3.{html,txt}`. Checked theorem statements and the indicated load-bearing sections; the entire 109-page proof was not independently reconstructed.

| Source | Exact applicable scope |
|---|---|
| Hypothesis 1.1 | Translation-invariant finite-range bond rates, 1<=c_b<=lambda, independent of both exchanged occupancies |
| Theorem 1.3 | Density-free local correctors with density-uniform error O(L^-gamma) |
| Theorem 1.4 | Smooth profile in (0,1), normalized entropy O(N^-kappa0) relative to its corrected reference; sup_t E||rho_N-rho||_(H^-alpha)^2<=C N^-kappa for alpha>d/2, fixed T |
| Theorem 1.5 | Algebraic grand-canonical and canonical finite-cell convergence; constants depend on d,lambda,range |
| Proposition 7.1 | r(Phi_n)<=n, ||Phi_n||_infinity<=C n² log n, density-uniform conductivity residual <=C n^-gamma |
| Section 7.3, (7.56) | Entropy bound affine in initial entropy before the fixed-time Gronwall factor |

In particular, Theorem 1.4 controls **supremum of expectations**, not expectation of the path supremum. H^-1 is permissible for the constructor's d=1 specialization; it is not the theorem's stated norm for d>=2.

## 3. Primal geometry and marked-current matching

For a source cube Lambda, let I=Lambda minus its boundary and

\[
 E=\{\{x,x+e_i\}:x\in\Lambda,\ i=1,\ldots,d\},\qquad |E|=d|\Lambda|.
\]

These are exactly source (1.40)–(1.42). The affine function is understood through its increments

\[
 \pi_b\ell_\xi=(\xi\cdot e_i)(\eta_x-\eta_{x+e_i}).
\]

For a persistent interior configuration, refresh all remaining needed bits independently from Ber(rho) at each proposal. Pair an accepted marked move with its reverse by exchanging the ghost bits too. Product weight is preserved; endpoint-independent c_b is unchanged; the mark reverses. For every f depending only on I, full interior/ghost expectation therefore gives

\[
 \inf_f E\sum_{b\in E}c_b[\pi_b\ell_\xi+\pi_b f]^2
   =|\Lambda|\,\xi\cdot\bar c(\rho,\Lambda)\xi.
\]

This is source (1.25), using (1.27) to remove the factor 1/2 on each side. A function of the interior may be arbitrary on its finite configuration space, so there is no missing restriction in the infimum. Events that alter only ghosts still carry affine current and must be included. An ordinary periodic conductivity, a closed-cell displacement, or a process dropping these marks would generally estimate a different finite-volume object.

There is a simple explicit primal gap bound in d=1. Let n=|I|. Product heat-bath resampling at each interior site has gap one. Realize a resampling at site i by moving its bit to the left boundary through nearest-neighbor swaps, resampling there from Ber(rho), and reversing the swaps. Every intermediate law remains product. The path has length at most 2n and each edge occurs in at most 2n such paths. Telescoping and Cauchy–Schwarz give E_heatbath<=4n² E_open, hence gap_open>=1/(4n²). The actual averaged c>=1 form dominates this rate-one open form. Tiny or empty interiors can be handled directly. No inverse density factor is necessary for this sufficient bound.

The constructor's scalar noisy-current subtraction needs one repair: if marks have magnitudes other than one, subtract

\[
 (v^{-2}-1)\sum_{\text{events}}|d_b|^2
\]

rather than (v^-2-1) times their count. This matters for normalized off-diagonal polarization directions. Alternatively choose componentwise unit marks and enlarge norm-dependent constants. The auditor was separately notified.

## 4. Restart proof for new homogeneous kinetic sequences

Take a fixed finite alphabet of source-admissible rates, fixed K, fixed switching times and a smooth initial profile staying in [a,1-a]. Each scalar unforced diffusion equation preserves that range. Its solution is spatially smooth on every piece, and the profile is continuous at switches; time derivatives need not match across a switch because the source estimate is applied separately.

Let psi_j^- and psi_j^+ be the old/new corrected references at a switch, using the **same current profile** and correctors F_N^- and F_N^+. Their product parts agree. If lambda=logit(rho), normalization of the two exponentials gives, for every microscopic law f,

\[
 |h_N(f|\psi_j^+)-h_N(f|\psi_j^-)|
 \le \frac{2\|\nabla\lambda\|_\infty}{N}
 (\|F_N^-\|_\infty+\|F_N^+\|_\infty)
 =O(N^{2s-1}\log N).\tag{R1}
\]

Choose the corrector scale s sufficiently small for every alphabet member; source constants/exponents depend only on the common finite-range/ellipticity parameters, and taking finite maxima/minima is legitimate. Equation (7.56), rather than empirical-density convergence alone, gives on piece j

\[
 \sup h_j\le B_j h_j(0)+E_jN^{-\kappa_j},\qquad B_j<\infty.\tag{R2}
\]

Iterating (R1)–(R2), with logs absorbed into a slightly smaller exponent, yields

\[
 \sup_{t\le T}h_N(t)\le C_{protocol}
 (h_N(0)+N^{-\kappa_{protocol}}).
\]

The entropy-to-weak-observable argument in source Lemma 7.4, followed by its Sobolev summation, then yields C17 in d=1. An independent product writer with per-site probability error <=zeta gives initial entropy <=C_a zeta²+O(N^{2s-1}log N), so the extra zeta² term follows directly from the affine inequality even when the literal vanishing-entropy hypothesis is not used.

This proof requires actual bounds on intermediate profile derivatives, the fixed density cutoff, corrector constants and error scales. Their existence is enough for a fixed-protocol theorem. It does not establish a computable N threshold today, a polynomial bound uniform in growing K, controls oscillating with N, E sup_t error, or arbitrary correlated writer noise. A new source is permitted only through its stated profile/entropy interface.

## 5. Exact dual cell and its polynomial sampler

### 5.1 The outside must be frozen, not refreshed

Let A=Lambda^+ and S include every site needed by c_b for b in E. Condition on the total count k in A **and on the outer configuration zeta in S minus A**. Keep zeta fixed for an entire run. Let nu_k be uniform on k-occupancy configurations of A and

\[
 L_{c;k,\zeta}f=\sum_{b\in E}c_b(\eta_A,\zeta)\pi_b f,
 \qquad G_{c;k,\zeta}=-L_{c;k,\zeta}.
\]

This is a closed, count-conserving process. It is reversible in nu_k because c_b does not depend on the exchanged endpoints. Define L_0=sum_(b in E) pi_b and g=-L_0 ell_q. Then E_(nu_k)g=0 for every k,zeta. Integration by parts gives the source dual objective, conditional on k,zeta, as

\[
 \sup_f\{2\langle g,f\rangle_{\nu_k}
              -\langle f,G_cf\rangle_{\nu_k}\}
 =\langle g,G_c^{-1}g\rangle_{\nu_k}.
\]

Consequently source (4.1) satisfies exactly

\[
 \bar\nu_*(\rho,\Lambda,q)
 =\frac{E_{k,\zeta}\langle g,G_{c;k,\zeta}^{-1}g\rangle_{\nu_k}}
        {2\chi(\rho)|\Lambda|}.\tag{D1}
\]

The mixing weights for k,zeta are those induced by independent Ber(rho) bits on S. Source Proposition 4.1(1) / Remark 4.2 explicitly justify pasting the solutions for fixed count and exterior; the optimizer is independent of rho. Refreshing the outer bits every event would average generators before inversion and generally give a different number.

### 5.2 Explicit canonical gap in one dimension

For a one-dimensional interval Lambda of V sites, A is a path of n=V+1 sites, E contains its V edges, and q=1 gives

\[
 g(\eta)=\eta_{right}-\eta_{left},\qquad |g|\le1.
\]

Since c_b>=1, its Dirichlet form dominates rate-one simple exclusion on that path in every count sector. Caputo–Liggett–Richthammer gives its gap equal to the rate-one path random-walk gap,

\[
 g_0=2[1-\cos(\pi/n)]\ge4/n^2.\tag{D2}
\]

The empty/full sectors have g=0. No assumption about a gap for the full thermodynamic-volume process is used.

**Version correction:** the actual [0906.1238v3 PDF](https://arxiv.org/pdf/0906.1238v3), dated 26 June 2009, is titled *A recursive proof of Aldous' spectral gap conjecture*. Its main statement is Theorem 1.2; **Corollary 1.3** explicitly gives exclusion gap = random-walk gap. Section 1.2.3 explains the exclusion contraction. It does not have the earlier-cited Theorem 1.1 / Section 4.1.1 numbering. PDF SHA256 `64f1f657dd2935c86f27fc25d202d8b6249d2f915d551f2d14a9ecf3a2c8fb71`, cached as `source/0906.1238v3.pdf`.

### 5.3 Finite correlation time, confidence and costs

Start A and its frozen outer bits from fresh independent Ber(rho), so conditional on k,zeta the run is stationary. Set

\[
 F_T=E\left[g(\eta_0)\int_0^Tg(\eta_t)dt\right],\quad
 F_\infty=E_{k,\zeta}\langle g,G_c^{-1}g\rangle.
\]

Spectral positivity in each sector yields

\[
 0\le F_\infty-F_T\le e^{-g_0T}/g_0.\tag{D3}
\]

Each run's statistic lies in [-T,T], so ordinary Hoeffding bounds provide absolute precision epsilon_F for F_T with O(T² epsilon_F^-2 log(1/delta)) fresh runs. The integral is evaluated exactly between digital event times or by an explicitly charged arithmetic tolerance. Rates are bounded by lambda, so the expected updates per run are <=lambda V T; hard Poisson caps give a finite-work failure budget. The state and fixed outer environment use O(V+range) bits. Choosing T=g_0^-1 log(max(exp(1),1/[g_0 chi V epsilon_R])) controls normalized inverse-diffusivity tail by epsilon_R and is polynomial in V, a^-1 and log(epsilon_R^-1). Since R_infinity>=1/lambda, take epsilon_R=O(epsilon_D/lambda²) for an absolute diffusivity tolerance epsilon_D.

No sample of the exponentially large configuration array is required. An equally simple estimator draws U uniformly in [0,T] and uses T g(eta_0)g(eta_U).

In d=1 the scalar inverse dual diffusivity is

\[
 R_\infty=2\bar\nu_*(\rho,\Lambda,1)
 =F_\infty/[\chi(\rho)V]=\bar D_*(\rho,\Lambda)^{-1}.
\]

An **upper** confidence bound on F_T plus the positive tail in (D3), divided by chi V and inverted, gives a certified **lower** bound on bar D_*. Inverting the truncated correlation without adding its tail goes in the wrong direction.

## 6. Adaptive primal–dual stopping removes constitutive constant extraction

Use source triadic cubes so exact tilings apply. Proposition 4.1(4) makes primal bar D_m decrease with m. It makes bar nu_*,m decrease, hence bar D_*,m increase. Proposition 5.1 gives their common limit, and Lemma 6.8 identifies it with D. Thus

\[
 \bar D_{*,m}(\rho)\le D(\rho)\le\bar D_m(\rho).\tag{D4}
\]

Lemma 4.6 alone only compares the two finite-volume values; the monotonicity/common-limit identification is needed for (D4).

For a learned admissible rate table, estimate primal bar D_m from the constructor's ghost-current variance and dual bar D_*,m from (D1)–(D3). The primal finite-exposure variance is biased **upward** relative to its infinite-exposure limit, so an upper statistical interval is safe; its known gap controls how long to run to make it tight. The dual uses the inverse of an upper correlation/tail interval. Clip using the source's known 1<=D,D_m,D_*,m<=lambda.

At stage m assign failure probability delta_m proportional to delta/(m+1)², include its finite density grid in the union bound, and stop only when every grid interval is narrower than the target tolerance after density interpolation and local-table error are charged. This is an executable stopping criterion with no unknown C_h or gamma_h.

Uniform density coverage is also effective. For the primal nonnegative objective use the constructor's product-likelihood comparison. For the dual, the fixed-sector solution u=G_c^-1g is independent of rho (source Proposition 4.1(1)); its energy is a nonnegative local function. For p,q in [a,1-a], on S of size m_S,

\[
 e^{-\theta}\frac{\chi(q)}{\chi(p)}R_\infty(q)
 \le R_\infty(p)\le
 e^\theta\frac{\chi(q)}{\chi(p)}R_\infty(q),\quad
 \theta=m_S|p-q|/a.
\]

Inversion gives an explicit analogous modulus for D_*. A mesh O(a epsilon/[lambda(m_S+2)]) suffices, after harmless constants. No unknown smoothness modulus of D is used. The learned/true rate comparison expands learned diffusivity intervals by the known factors 1/(1+eta),1/(1-eta).

On the joint confidence event the interval always contains the true D, and source uniform convergence guarantees eventual stopping. The theorem's algebraic convergence gives a polynomial bound in inverse accuracy for the required cell size and consequently for the total sampling work, at fixed class parameters. Failed stages and the density-grid growth are included. Numeric convergence constants/exponents are needed to predict this worst-case work **in advance**, but are unnecessary to run the stopping algorithm or certify its returned constitutive interval.

This closes the operational constitutive-law constants gap. It leaves intact the need for effective finite-N switched-hydrodynamic constants if an actual specimen-size error certificate is requested, and the absent arbitrary-force hydrodynamic theorem.

## 7. Prior-art and capability judgement

The strongest exact mathematical predecessor here is Funaki–Gu–Wang itself: the non-gradient homogenization, density-free corrector, quantitative hydrodynamic limit, primal/dual finite-cell structures and convergence are theirs. The current identities are finite-state Green–Kubo/Poisson-equation consequences; kinetic Monte Carlo replaces explicit state enumeration. These operations should be credited as implementations and quantitative composition, not new physical principles.

A concrete earlier operational comparator is Embacher–Dirr–Zimmer–Reina, [*Computing diffusivities from particle models out of equilibrium*](https://pmc.ncbi.nlm.nih.gov/articles/PMC5938669/), Proc. R. Soc. A 474 (2018), 20170694, DOI 10.1098/rspa.2017.0694. Its full primary text was inspected: it extracts nonlinear diffusivity from particle fluctuations, uses lattice kinetic Monte Carlo, and tests random walkers, zero range, exclusion and a Kawasaki-type example. Its local-equilibrium/Gaussian fluctuation premise and formal SPDE differ from the present finite-cell confidence route. It already defeats any novelty claim based merely on learning a constitutive diffusivity from particle fluctuations or then using a continuum solver.

Green–Kubo and variational conductivity are also explicit prior machinery in the governing source, including its reference to Spohn's 1991 book and Sasada's 2018 paper. No detailed theorem from those books/papers is imported here without a separate full-source check. Strongest fair numerical comparisons include acquired-rate kinetic Monte Carlo, standard finite-cell Green–Kubo, primal/dual stochastic homogenization estimators and ordinary nonlinear diffusion solvers, all with the same local-rate information.

What has become concrete is a finitely acquired local constitutive operation, reusable under new smooth profiles and fixed finite homogeneous kinetic protocols in the specified product-reversible class. What remains unearned is generic material applicability, arbitrary external drives, rare-event/macroscopic fluctuation prediction, a numeric finite-N certificate at today's constants, hardware implementation and favorable full cost. The new adaptive dual-cell synthesis needs independent mathematical checking and a priority search before any novelty claim; status **candidate with proofs supplied / novelty UNKNOWN**.

## 8. Independent finite diagnostic

`check_primal_dual_cell.py` constructs exactly the source primal and dual geometries for V=3 and V=9 and rate c_b=1+strength eta_(x-1)eta_(x+2). It checks SSEP normalization, frozen-exterior canonical gaps, primal/dual ordering and triadic monotonicity at densities .2,.5,.8. The rho=.5,strength=1 brackets shrink from [1.15596330,1.25] to [1.18780078,1.24000491]. Both SSEP estimates equal one to <3e-14. Outputs are in `PRIMAL_DUAL_CELL_CHECK.json`. Enumeration verifies only these small algebraic cases; the proposed algorithm above uses trajectories and polynomial tails, not this enumeration.
