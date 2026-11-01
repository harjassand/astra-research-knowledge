# Symmetry-Protected Green–Kubo Response: Full Construction and Proof

**Status (2026-11-01):** new source-independent derivation and executable conditional result; historical novelty not established. All spectral and numerical claims are restricted to the hypotheses below. This is a response theorem, **not** a bound on every pointwise time correlation, every kinetic model, or experimental uncertainty without acquired rate intervals.

## 1. Physical contract

A finite, connected continuous-time Markov chain with positive equilibrium law `pi` and reversible generator `L`. Let `K=-L` on `H=L²_0(pi)`. The target is the nonnegative Green–Kubo response

\[
\chi_f=\int_0^\infty \operatorname{Cov}_{\pi}(f(X_0),f(X_t))\,dt
=\langle f,K^{-1} f\rangle_\pi,
\]

for an actually supplied, centered observable `f` in a selected symmetry-invariant sector. Rates and energies are from the supplied microscopic law, not measured for free; `chi` concerns that model. The finite-state proof needs irreducibility. The same operation applies to the discounted response `chi_f(z)=<f,(K+zI)^-1 f>` for any `z>=0`.

## 2. Nonperturbative orbit theorem

Let a finite group `G` act as permutations of configurations, preserving `pi`; write `U_g` for its unitary action on `H`. Average the actual generator:

\[
K_0=|G|^{-1}\sum_{g\in G}U_g^{-1}KU_g.
\]

Then `K_0` is another reversible, positive Markov generator on `H` and commutes with the invariant-sector projection `P=|G|^-1 sum_g U_g`. Suppose a **proved** uniform energy-form comparison

\[
(1-\rho)K_0\preceq K\preceq(1+\rho)K_0,\quad 0\le\rho<1
\]

holds. Any `f=Pf` satisfies

\[
\boxed{\chi_{f,0}\le\chi_f\le\frac{\chi_{f,0}}{1-\rho^2}.}
\]

More generally, this is a positive-semidefinite matrix inequality for every finite family of invariant observables. It also holds separately for every `z>=0` with `K,K0` replaced by `K+zI,K0+zI`; a Laplace/Stieltjes response bound **does not automatically imply a pointwise time-domain covariance bound**.

### Proof (complete)

All inverses below are on `H`; `K0>0` because the finite graph remains connected. Put

\[
T=K_0^{-1/2}KK_0^{-1/2},\quad v=K_0^{-1/2}f/\sqrt{\chi_{f,0}}.
\]

`T` is self-adjoint and has spectrum in `[1-rho,1+rho]`; `||v||=1`. Since `K0` commutes with `P`, `v=Pv`. The group average gives `P(K-K0)P=0` **as a bilinear form**. Hence `<v,Tv>=1`. Let `mu_v` be the scalar spectral probability law of `T` with vector `v`. Then

\[
\chi_f/\chi_{f,0}=\int\lambda^{-1}\,d\mu_v(\lambda),\qquad
\int\lambda\,d\mu_v=1.
\]

The lower bound is Jensen's inequality for `1/x`. For each `lambda` in `[1-rho,1+rho]`,

\[
(\lambda-1)^2\le\rho^2\quad\Longrightarrow\quad
\lambda+\frac{1-\rho^2}{\lambda}\le2.
\]

Integrating and using `E(lambda)=1` yields `E(1/lambda)<=1/(1-rho²)`. Multiply by `chi0`. For discounted response, `K0+zI` still commutes with `P`, its compressions agree with those of `K+zI`, and the same form contrast holds because `zI>=0`. Repeat the argument. For the matrix extension, apply the scalar statement to each real linear combination of invariant observables. **QED.**

### Exact sharpness

Two independent spins with unbiased equilibrium, flip rates `nu1/2,nu2/2`, and `nu1=1-rho,nu2=1+rho` have invariant observable `f=sigma1+sigma2`. The original response is `1/nu1+1/nu2=2/(1-rho²)`. The group-averaged response is `2`. The upper bound is therefore attained and cannot be uniformly improved using only these premises.

### Monotone hierarchy (no enumeration of perturbation words)

Let `G0` contain `G1`, which contains `G2`, ... , and require `f` invariant under every group. Let `K_j` be the average of `K` under `G_j`. Since `K_j` is the group average of `K_{j+1}` over the larger group, operator convexity of the inverse (or the Schur variational argument) gives

\[
\chi_{f,0}\le\chi_{f,1}\le\chi_{f,2}\le\dots\le\chi_f.
\]

Each refinement retains *all* microscopic kinetics inside its residual groups via the quadratic bound. The best upper bound across levels is their minimum. These inequalities hold without perturbation series, weak coupling, a spectral-gap lower bound, or tensor compressibility. **State count** and arithmetic precision of each quotient still matter.

## 3. A materially broader physical input family

Partition `n` finite-state sites into `r` physical modules. For the binary case, each microscopic site has `eta_i∈{0,1}`. Let `k_g` be the number occupied in module `g`. Supply **any** integer potential `H(k1,...,kr)` and Gibbs weight per microscopic state

\[
\pi(\eta)\propto 2^{H(\boldsymbol k)}.
\]

No convexity, Gaussianity, field-free condition, or small interaction is imposed; `H` may contain arbitrary cooperative, antagonistic and multimodal couplings between modules. Each site `i` in module `g` has its own positive kinetic activity `nu_i`; multiplying both directions of a flip by `nu_i` preserves the common Gibbs equilibrium.

For a zero-to-one move `k -> k+e_g`, the native heat-bath factor is

\[
c^+_g(\boldsymbol k)=\frac{2^{H(\boldsymbol k+e_g)}}{2^{H(\boldsymbol k)}+2^{H(\boldsymbol k+e_g)}},
\quad c^-_g(\boldsymbol k+e_g)=1-c^+_g(\boldsymbol k).
\]

The actual microscopic flip rate is `nu_i c^+` or `nu_i c^-`. This is a positive finite physical generator satisfying exact detailed balance, not an assigned generator for the desired response.

Average `nu_i` inside each module to obtain `nu_bar_g`. The averaged process is **exactly lumpable** onto the count vector `k`; its rates are

\[
q(\boldsymbol k,\boldsymbol k+e_g)=(n_g-k_g)\bar\nu_g c^+_g(\boldsymbol k),\quad
q(\boldsymbol k,\boldsymbol k-e_g)=k_g\bar\nu_g c^-_g(\boldsymbol k),
\]

and its equilibrium count law is

\[
p(\boldsymbol k)\propto \left[\prod_g\binom{n_g}{k_g}\right]2^{H(\boldsymbol k)}.
\]

The site activities need **not** be constant in each physical module for the theorem: their residual variation is exactly what is enclosed. Indeed, with

\[
\rho=\max_g\max_{i\in g}|\nu_i/\bar\nu_g-1|<1,
\]

each microscopic edge conductance lies between `(1-rho)` and `(1+rho)` times its symmetrized conductance, proving the required *full-state* Dirichlet-form comparison without enumerating states.

The group quotient contains `D=prod_g(n_g+1)` states and at most `rD` undirected edges. General `q`-state modules similarly contain `D=prod_g binom(n_g+q-1,q-1)` counts for fixed `q`; the site-state transitions must be supplied with detailed balance and a shared local clock multiplier. The theorem itself is not specific to binary variables, or to count-energy systems: any reversible group-averaged chain with an acquired form contrast qualifies.

## 4. Constructive scalar solver with exact finite-bit output

In the one-module binary case, the quotient is birth-death: `k=0,...,n`. Let

\[
w_k=\binom nk 2^{H_k},\quad Z=\sum_k w_k,\quad
\mu=\frac1Z\sum_k w_k (2k-n),\quad f_k=2k-n-\mu,
\]

and `lambda_k=(n-k)nu_bar c^+(k)`. From the Poisson equation `K u=f`, the stationary current across edge `k->k+1` is

\[
F_k=\sum_{j=0}^k\frac{w_j}{Z}f_j.
\]

Detailed balance gives `p_k lambda_k(u_k-u_{k+1})=F_k`. The Dirichlet identity yields

\[
\boxed{\chi_{M,0}=\sum_{k=0}^{n-1}\frac{F_k^2}{p_k\lambda_k}.}
\]

This is a sum of nonnegative terms. For integer `H`, rational `nu_bar`, and integer `M_k`, define integer `B_k=sum_{j<=k}w_j[(2j-n)Z-\sum_l w_l(2l-n)]`. Then

\[
\chi_{M,0}=\sum_{k=0}^{n-1}
\frac{B_k^2}{Z^3 w_k\lambda_k}.
\]

Each numerator/denominator is rational. Multiply each nonnegative term by `10^p`, take the **exact integer floor** for the lower bound and ceiling for the upper bound, and sum. The enclosing interval width is at most `n*10^-p` in the stated time units. No eigensolver, unstable subtraction in the final response, floating normalization or long physical trajectory is needed. The code executes `n` binomial-weight terms, `n` current updates and `n` big-integer divisions. If energies and local rates have polynomial-length rational encodings, bit complexity is polynomial in `n`, input length and precision `p`; it is not a unit-cost arithmetic assertion.

A separate rational tridiagonal Thomas solver implements the discounted response `<f,(K+sI)^-1f>` at `s>0`, without numerically waiting for the collective process.

## 5. Certified multigroup finite-precision receiving

For the `D`-state group-count generator, a sparse numerical Poisson potential `v` can be converted to rational entries. Define the *exact rational* residual `r=f-K0 v`, Dirichlet energy `E(v,v)`, and dual value

\[
Q(v)=2\langle f,v\rangle_\pi-\mathcal E(v,v).
\]

The true response obeys

\[
Q(v)\le\chi_{f,0}\le Q(v)+B\|r\|_{L^2(\pi)}^2
\]

for any acquired Poincaré constant `Var_pi(u) <= B E(u,u)`. No unknown spectral gap is used as an oracle. Build a spanning tree of the **entire reduced count graph**, rooted at a state `o`; for each edge `e` let `T_e` be the branch separated from the root, `d(s)` the root-path edge count, and `c_e=p_x q_xy` its conductance. Then the explicit valid constant

\[
B=\max_e\frac{\sum_{s\in T_e}p_s d(s)}{c_e}
\]

follows by Cauchy–Schwarz along every root path and `Var(u)<=sum_s p_s(u_s-u_o)^2`. All quantities can be computed using rational weights and positive rates, including when `v` came from unreliable floating point. This finite-dimensional bound can be loose for deep metastability; it is not a uniformly fast solver for arbitrary `D`.

Combining the rational interval `[L0,U0]` with kinetic disorder gives `[L0,U0/(1-rho²)]` for the *full*, potentially exponentially larger microscopic chain.

## 6. Critical failure modes and limits

1. **Different energy landscapes per site**: permutation symmetry of `pi` fails. Two independent spins with variances 1 and 0.36 and respective rates 1.2 and 0.8 have collective Green-Kubo response `1/1.2+0.36/0.8=1.2833...`, smaller than the naive equal-clock reference `1.36`. The one-sided lower theorem does not apply.
2. **Noninvariant observable**: even with uniform equilibrium, observing only the faster of two independent spins gives lower response than its averaged-clock reference. The source must live in the selected invariant sector.
3. **No rate contrast**: if `rho>=1` or the rate support changes, the bound does not apply; an arbitrarily slow hidden site can control long times.
4. **Symmetry-poor geometry**: an arbitrary lattice with a small automorphism group can have exponentially many configuration orbits, so the exact quotient is not necessarily economical.
5. **Nonreversible dynamics**: positivity and self-adjoint spectral measure no longer follow. No extension is inferred from shared invariant distribution alone.
6. **Time-domain outputs**: the uniform Laplace-resolvent inequality does not establish all-time CDF, pointwise covariance, oscillatory response, frequency-resolved complex susceptibility or arbitrary observable sources.
7. **Physical input acquisition**: unknown site activity intervals and state energies must be measured or computed separately; the theorem cannot recognize an unmodelled slow state, chemical pathway or external forcing.
8. **Group count**: when the number of distinguishable populations grows with `n`, the quotient may again be exponentially large. `D^3` exact algebra and integer-bit growth are charged; the current sparse prototype is not a uniform near-linear solver for such quotients.

## 7. From clock uncertainty intervals to actual model bounds

If every site activity is admitted only through a positive rational interval `[nu_i^-,nu_i^+]`, compute

\[
\bar\nu_- =n^{-1}\sum_i\nu_i^-,\quad \bar\nu_+=n^{-1}\sum_i\nu_i^+,\quad
\rho_{\rm cert}=\max_i\{1-\nu_i^-/\bar\nu_+,\,\nu_i^+/\bar\nu_--1,0\}.
\]

If `rho_cert<1`, let `chi_unit` be the exact homogeneous response at rate 1. A uniform interval over all admitted independent site choices is

\[
\frac{\chi_{\rm unit}}{\bar\nu_+}
\le\chi_{\rm actual}\le
\frac{\chi_{\rm unit}}{\bar\nu_-(1-\rho_{\rm cert}^2)}.
\]

Averaging the physical clock rates is therefore not free. This is a conservative interface, not a statistical confidence interval derived from an experiment; physical calibration and model completeness remain separate.

## 8. Novelty and comparator boundary

Exact Markov lumpability, conditional expectation projection, Dirichlet comparisons, Kantorovich/operator-convex inequalities, and birth-death Poisson currents are established prior mathematics. The **newly constructed result in this record** is their fully specified response-and-cost interface for heterogeneous cooperative kinetics, including quadratic same-equilibrium error, all-resolvent extension, rational quotient solver, certified multigroup residuals, and fixed-input tests. Historical priority for the combined theorem/application has not been established. No new universal complexity class or practical materials speedup is claimed.
