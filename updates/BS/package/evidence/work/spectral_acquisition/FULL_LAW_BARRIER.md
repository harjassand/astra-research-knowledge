# Exponentially close spectral laws with distinct positive noise variances

2026-10-10. Internal proof reconstruction plus independent AI criticism; no external certification or historical novelty claim. This strengthens the transform-oracle theorem in `RESULT.md` to the entire probability density. It does **not** establish a lower bound for a finite Wigner matrix or its correlated joint eigenvalue distribution.

## Exact observation contract

The unknown pair is `(mu,t)`, where mu has at most k distinct real atoms, all weights positive, and is supported in a supplied compact interval. One observes independent exact real draws from `nu=mu free-convolved SC_t`. The noise variance t is unknown. Independent draws from a limiting spectral law are a mathematical observation model; a single matrix's N eigenvalues are not such draws.

No supplied model count beyond the upper bound k, no exact limiting transform oracle, and no physical preparation assumption is hidden. The resulting lower bound is information-theoretic: unlimited computation and any estimator are allowed.

## Theorem

Let a,b>0 and c=a+b. For integer k>=1, set

`mu_k = sum_(j=1)^k p_j delta_(x_j)`,

`x_j=2sqrt(a) cos(j pi/(k+1))`,

`p_j=2sin²(j pi/(k+1))/(k+1)`.

Define `nu_0=SC_c` and `nu_1=mu_k free-convolved SC_b`. Their respective signal/noise pairs are `(delta_0,c)` and `(mu_k,b)`. The variance gap is a, and both signals belong to the class with at most k atoms supported in [-2sqrt(a),2sqrt(a)].

Let `rho=sqrt(a/c)` and choose any `rho<r<1`. Put

`E_k(r)= r^(2k+1)(1+r²) / [sqrt(a)(1-r^(2k+2))]`,

`D_k(r)= (b/c) r^(2k+2)(1+r²) / (1-r^(2k+2))`,

`H_k(r)=3sqrt(D_k(r))/sqrt(a)+E_k(r)`.

If the explicit gate `rho+3sqrt(D_k(r))<r` holds, then

`sup_(Im z>0) |G_nu1(z)-G_nu0(z)| <= H_k(r)`.

The laws nu_0 and nu_1 have bounded densities, supported in [-R,R] for `R=2sqrt(a)+2sqrt(b)`, and

`TV(nu_0,nu_1) <= min(1, R H_k(r)/pi)`.

For each fixed a,b>0 and fixed rho<r<1, the gate holds for all sufficiently large k, while H_k(r)=O(r^k). Thus the full laws are exponentially close despite a fixed positive variance difference.

### Proof 1: rational quadrature identity

The k-by-k symmetric tridiagonal matrix with sqrt(a) on adjacent diagonals has eigenvalues x_j and squared first-coordinate eigenvector magnitudes p_j. Its resolvent's first diagonal entry, by determinant recurrence, is

`G_muk(w)=(1/sqrt(a)) U_(k-1)(w/(2sqrt(a)))/U_k(w/(2sqrt(a)))`.

For w in the upper half-plane let `q=sqrt(a)G_SCa(w)`. Then |q|<1, Im q<0 and `w=sqrt(a)(q+q^-1)`. The Chebyshev recurrence gives

`G_muk(w)= (q/sqrt(a)) (1-q^(2k))/(1-q^(2k+2))`.

Write

`e_k(q)=G_muk(w)-G_SCa(w)= -q^(2k+1)(1-q²)/[sqrt(a)(1-q^(2k+2))]`.

For |q|<=r, `|e_k(q)|<=E_k(r)`.

### Proof 2: continue the physical subordination solution

For s in [0,1], define the *signal* mixture

`lambda_s=(1-s)SC_a+s mu_k`, and `nu_s=lambda_s free-convolved SC_b`.

The intermediate lambda_s need not be atomic. It is used solely as a proof path; the two endpoint models have the required atomic signals. For any fixed z in the upper half-plane, put

`h_s=G_nus(z)`, `w_s=z-b h_s`, `q_s=sqrt(a)G_SCa(w_s)`.

Subordination ensures Im w_s>0 and

`h_s=q_s/sqrt(a)+s e_k(q_s)`.

Because w_s=sqrt(a)(q_s+q_s^-1), the equation z=w_s+b h_s becomes

`(c/sqrt(a))q_s²-z q_s+sqrt(a)+b s q_s e_k(q_s)=0`. (1)

At s=0 the two roots of the unperturbed quadratic are

`u=sqrt(a)G_SCc(z)`, and `v=a/(c u)`.

For finite z in the upper half-plane, u is nonzero, |u|<rho, and the physical initial solution is q_0=u. No value at infinity is used. Factoring the quadratic in (1) gives

`(q_s-u)(q_s-v)=-(b sqrt(a)/c) s q_s e_k(q_s)`. (2)

While |q_s|<=r, equation (2) implies

`|(q_s-u)(q_s-v)|<=D_k(r)`.

Consequently q_s lies in the union of the two closed disks of radius sqrt(D_k) around u and v. If these disks are disjoint, any continuous path starting at u stays in the disk about u. If they meet, their union lies within distance 3sqrt(D_k) of u. Hence, along either type of path,

`|q_s-u|<=3sqrt(D_k)`.

The q_s are continuous in s. One direct justification uses fixed-point uniqueness: h_s are bounded by 1/Im z; from any s_n -> s, every subsequential limit satisfies the subordination equation for lambda_s, because its finite mixture transform is continuous and Im(z-bh)>=Im z. The solution in the lower half-plane is unique. A limit cannot lie on the real axis, since the transform on the right has strictly negative imaginary part. Thus the entire sequence converges.

For completeness, uniqueness follows by subtracting two solutions h1,h2. If `A_j=integral |z-bh_j-x|^-2 lambda_s(dx)`, imaginary parts give `A_j=(-Im h_j)/(Im z+b(-Im h_j))<1/b`. Distinct solutions would imply `1<=b sqrt(A_1 A_2)<1`, a contradiction.

Now suppose q_s first exits the open radius-r disk. Up to that time the previous bound applies, and at the exit time it yields

`|q_s|<=|u|+3sqrt(D_k)<rho+3sqrt(D_k)<r`,

a contradiction. Therefore the disk bound holds throughout s in [0,1], uniformly in the choice of z. At s=1,

`|h_1-h_0| <= |q_1-u|/sqrt(a)+|e_k(q_1)| <= H_k(r)`.

This proves the uniform whole-upper-half-plane transform bound. It does not use high-imaginary contraction, exclude spectral edges, assume root separation, or choose an unphysical quadratic branch.

### Proof 3: densities, support, and total variation

For any probability signal lambda, let h=G_(lambda free-convolved SC_b)(z), y=-Im h>0, eta=Im z>0, and v=Im(z-bh)=eta+b y. Taking imaginary parts of subordination gives

`y=v I`, where `I=integral |z-bh-x|^-2 lambda(dx)`.

Therefore I=y/(eta+b y)<1/b. By Cauchy-Schwarz, `|h|²<=I<1/b`. In particular the Poisson-smoothed densities `-Im h(x+i eta)/pi` are uniformly bounded by 1/(pi sqrt(b)). Weak convergence as eta decreases to zero implies the law has an essentially bounded density with this same bound. Almost-everywhere convergence of Poisson convolutions to an L-infinity density then turns the uniform transform difference into

`|f_1(x)-f_0(x)|<=H_k(r)/pi` almost everywhere.

For compact support, represent the free convolution as the spectral law of bounded free self-adjoint variables X+S. Here ||X||<=2sqrt(a), ||S||=2sqrt(b), so ||X+S||<=R. The same bound contains SC_c since sqrt(c)<=sqrt(a)+sqrt(b). This standard spectral realization of free convolution is the sole support argument; no matrix ensemble or large-N limit is assumed. Integrating over [-R,R],

`TV=(1/2) integral |f_1-f_0| <=R H_k(r)/pi`.

## Corollary: independent sample lower bound

Let an arbitrary estimator, from M independent exact real draws, estimate the noise variance within strictly less than a/2 with probability at least 1-delta under each endpoint model, where 0<delta<1/2. Then

`M >= (1-2delta) pi / [R H_k(r)]`.

Proof: threshold the estimated variance at the midpoint of b and c. The resulting test has sum of error probabilities <=2delta. Yet the two-point testing inequality gives sum >=1-TV(nu_0^M,nu_1^M), and independent-product coupling gives

`TV(nu_0^M,nu_1^M)<=M TV(nu_0,nu_1)<=M R H_k/pi`.

Rearrange. A sharper version, writing epsilon=R H_k/pi<1, uses maximal product coupling to obtain `TV(nu_0^M,nu_1^M)<=1-(1-epsilon)^M`, and therefore `M>=log(1/(2delta))/[-log(1-epsilon)]`. Randomization of the estimator does not help because the same randomness can be coupled under both models. As H_k=O(r^k), the necessary number of independent samples grows exponentially with k.

The estimator may know a,b, k, the compact support, and even that the unknown pair is one of these two explicit models. The lower bound thus survives any matched algorithmic baseline. It does not cover an oracle supplying the *exact* atom count because the two signals have counts 1 and k; the declared interface supplies an upper bound k. The earlier transform-oracle note has an exactly-k perturbation extension, but that extension has not been transferred to this density theorem.

## Reproducible constants and finite replay

For a=b=1, choose r=3/4 and delta=1/4. The variance gap is 1 and the supplied signal atom upper bound is k. All gates below hold.

| k | Analytical TV upper bound | Necessary IID samples (product-coupling bound) |
|---:|---:|---:|
| 20 | 8.045e-3 | 85.8 |
| 50 | 1.434e-6 | 4.834e5 |
| 100 | 8.121e-13 | 8.535e11 |
| 200 | 2.605e-25 | 2.661e24 |

These are analytical lower bounds, not extrapolated finite experiments. `verify_spectral_barrier.py` evaluates the constants. Its k=20 finite replay uses 9,001 points at imaginary height 1e-4, follows the physical polynomial branch by Newton iteration, and independently checks the atomic subordination residual. The maximum residual was 4.97e-16 and the observed transform gap 4.46e-6, below the proven uniform bound 6.32e-3. The full script ran in approximately 0.054 seconds with NumPy 2.5.3. These floating-grid diagnostics are not a numerical certificate of TV or an empirical validation.

## Proven repair and honest remaining boundary

The theorem holds for every fixed positive b. Simply lowering the transform query height does not recover a uniform polynomial sample guarantee in this class: the entire laws are exponentially close.

If the lower-noise member has b=0, there is a real change. For a=1, querying `z=i/(k+1)` gives the exact transform gap

`r_k^(2k+1)(1+r_k²) / |1-(-1)^(k+1)r_k^(2k+2)|`,

where `r_k=exp(-asinh(1/[2(k+1)]))`. Since asinh(x)<=x, the numerator is at least e^-1 and denominator at most 2; the gap exceeds 1/(2e). Therefore the pair can be distinguished with constant order fixed-variance Gaussian transform queries, or O(k² log(1/delta)) independent samples used to estimate that near-axis transform. However, for this known b=0 pair one exact sample already distinguishes the discrete support from the continuous law. This is an oracle-interface illustration, not a new optimal learning method or a repair for positive b.

Another true repair changes the experiment: two independent noisy GOE matrices sharing the same unknown signal yield a difference with independent centered Gaussian entries, and the chi-square variance estimator in `RESULT.md` has parametric accuracy. The added independent repeated measurement is essential, and the calibration is classical.

No novel transformative positive capability was established. The full-density theorem isolates a central obstacle: high-complexity atomic signals can absorb a fixed amount of apparent free-Gaussian noise into exponentially small changes in the entire measured spectral law. Any positive invention must supply verifiable structure, controlled repeated information, or a demonstrably different observation interface.

## Provenance and status

This theorem uses the explicit Gaussian quadrature family and exact transform identity developed from N526's acquisition question. Original source pin and contemporary baseline links are in `source_manifest.json` and `RESULT.md`. N526 does not state the present full-density lower bound. That distinction is not a historical novelty claim: truncated moment matching, quadrature approximation, smoothing-based deconvolution difficulty, and two-point testing are established techniques. A targeted prior-art search cannot certify priority.

Independent critic: `spectral_critic.md`. Executable finite checks: `verify_spectral_barrier.py`, with results in `spectral_diagnostics.json`. The proof is analytic; a finite grid cannot certify a uniform density or total-variation bound.

## Targeted prior-art comparison

Maida, Nguyen, Pham Ngoc, Rivoirard and Tran, *Statistical deconvolution of the free Fokker-Planck equation at fixed time*, Bernoulli 28(2), 771–802 (2022), [primary paper](https://www.ceremade.dauphine.fr/~rivoirar/21-BEJ1366.pdf), develops known-time free deconvolution from Dyson matrix observations through subordination and a Cauchy deconvolution step. It already obtains logarithmic rates for Sobolev initial densities. Our exponential construction must therefore not be described as the first discovery of severe free-deconvolution ill-posedness. The differences are unknown semicircular variance, finite positive atomic signals with a supplied count upper bound, an explicit full-law pair, and a declared independent-law-sampling interface.

Catherine Matias, *Semiparametric deconvolution with unknown noise variance*, ESAIM: Probability and Statistics 6 (2002), 271–292, [primary article](https://www.numdam.org/item/PS_2002__6__271_0/), establishes logarithmic minimax difficulty in a classical Gaussian-convolution model. This is a methodological antecedent, not a direct proof of the free-convolution statement here. Together with classical quadrature and moment-matching lower bounds, these precedents make a historic or sweeping conceptual-novelty claim inappropriate. Exact priority of the displayed free atomic construction remains UNKNOWN.
