# Spectral acquisition: exact finite-transcript ambiguity and a quantitative barrier

Date: 2026-10-10. Status: internally derived and independently AI-criticized; not externally certified, not a novelty claim, and not a historic breakthrough. Finite diagnostics support the implementation only. The primary objective remains unresolved.

## Stronger continuation result

The main result is now `FULL_LAW_BARRIER.md`: for every fixed a,b>0, explicit k-atom positive signals with noise b generate full probability laws exponentially close in total variation to a one-atom signal with noise a+b. The complete argument uses a continuous family of physical subordination solutions to control the correct quadratic branch uniformly down to the real axis. At a=b=1,k=100, the proved TV upper bound is 8.13e-13 and any estimator with at least 75% success on both models needs at least 8.53e11 independent exact real samples under the declared IID-law interface. This strengthens the earlier transform-oracle result; neither result is a lower bound for the joint eigenvalues of one finite Wigner matrix. Exact atom-count information versus an upper bound remains distinguished.

## Decision and source pin

Repository: `https://github.com/harjassand/astra-research-knowledge`, commit `8aed7fd74eb14622ed5a0a3635a799374296e32a`. Retrieval followed `AGENTS.md` and `00_START_HERE.txt`, read frontier notices before cards, and retrieved original arguments using `git show`; no checkout or research history was changed.

Inspected opportunity routes:

- N526: unknown semicircular noise from exact finite Cauchy-transform samples of an atomic signal. Original `updates/BQ/package/supplied/spectral_pick_boundary_result_2026-10-09/CANDIDATE_THEOREM.md` and `STABILITY_AND_FINITE_N.md` read completely. The supplied result assumes a known atom count/upper bound, and its finite-GOE budget is fixed-node/high-imaginary with conditioning dependence.
- N528: finite-time fragmentation inverse already covers noisy calibrated mass-tagged endpoint sampling with known rates. Independent child inspected the original and developed observation/acquisition obstructions and restricted remedies; see `fragmentation_blind.md`.
- N530: reviewed card and complete `FOCUSED_CHECK.md` read; original 887-line proof not reconstructed. An averaged marginal Gaussianity modulus is analytically interesting but does not itself acquire marginal divergences or reconstruct a distribution. No positive acquisition claim made here.

N526 is prioritized because it offers an exact simple target and makes the supplied-versus-acquired issue mathematically decisive. The strongest result achieved is a fully explicit obstruction: an extra atom can conceal a different noise level from any fixed finite transform transcript, and bounded-height noisy transforms can require exponentially many measurements even when an atom-count upper bound is supplied.

## Information interface and notation

For a probability measure lambda on R, write

`G_lambda(z) = integral 1/(z-x) lambda(dx)`, Im z > 0.

`SC_t` is the centered semicircle distribution of variance t; `SC_0=delta_0`. The observation law is `nu=mu free-additive-convolved SC_t`. Standard semicircular subordination gives

`G_nu(z)=G_mu(z-t G_nu(z))`.

The unknown target is the noise variance t, and the unknown signal mu is finitely atomic with positive weights. We distinguish:

1. Exact finite complex-transform queries at arbitrary upper-half-plane nodes.
2. Queries restricted to Im z >= eta with specified Gaussian measurement noise.
3. Full finite random matrices or all their eigenvalues. The theorems below **do not establish an information lower bound for this third interface**. Queries to a single finite spectrum have correlated, model-dependent errors; they are not independent Gaussian transform queries.

## Theorem A: every finite exact transcript has a lower-noise atomic alternative

Let mu be any compactly supported probability measure, t0>0, nu=mu free-convolved SC_t0. Fix distinct upper-half-plane nodes z_1,...,z_m and let g_i=G_nu(z_i). For every t in [0,t0), there exists a probability measure mu_t^Q on exactly m+1 distinct real atoms, with strictly positive weights, such that

`G_(mu_t^Q free-convolved SC_t)(z_i) = g_i`, for every i.

In particular this applies when the original mu is finitely atomic, including mu=delta_0.

### Proof

Set lambda=mu free-convolved SC_(t0-t). This has compact infinite support (positive-variance semicircular convolution is absolutely continuous). Associativity and subordination give

`w_i=z_i-t g_i in C+`, and `G_lambda(w_i)=g_i`.

The w_i are distinct: w_i=w_j implies g_i=g_j and then z_i=z_j. Define the strictly positive real polynomial

`Q(x)=product_(i=1)^m (w_i-x)(conj(w_i)-x)`

of degree 2m. The finite positive measure rho(dx)=lambda(dx)/Q(x) has compact infinite support. Its (m+1)-node Gaussian quadrature consists of distinct real nodes x_j and positive weights a_j and is exact for every polynomial of degree at most 2m+1. Put p_j=a_j Q(x_j)>0. Then

`sum_j p_j = sum_j a_j Q(x_j) = integral Q d rho = 1`,

and, since Q(x)/(w_i-x) is a polynomial of degree 2m-1,

`sum_j p_j/(w_i-x_j) = integral Q(x)/(w_i-x) rho(dx) = g_i`.

Thus mu_t^Q=sum p_j delta_xj is a probability measure with the required transformed samples. The equation h=G_(mu_t^Q)(z_i-t h) has a unique solution h in the lower half-plane, namely G_(mu_t^Q free-convolved SC_t)(z_i). Since g_i is such a solution, the samples match.

For completeness, uniqueness at a point does not need a high-imaginary contraction assumption. If h1,h2 are two lower-half-plane solutions and t>0, write w_j=z-t h_j and A_j=integral |w_j-x|^-2 dmu. The imaginary-part equation gives A_j=(-Im h_j)/(Im z+t(-Im h_j))<1/t. Subtracting the fixed-point equations and applying Cauchy-Schwarz would require 1<=t sqrt(A_1 A_2)<1 if h1 differs from h2. The case t=0 is immediate.

The quadrature fact itself has a short proof. The monic orthogonal polynomial P_(m+1) for rho has m+1 distinct roots in the interior of the convex hull of its support: multiplying its sign-changing factors would otherwise produce a polynomial of degree <=m whose product with P_(m+1) has constant sign, contradicting orthogonality. For a polynomial f of degree <=2m+1, divide f by P_(m+1); the quotient has degree <=m and integrates to zero after multiplication by P_(m+1). Interpolating the remainder at the roots gives exact quadrature. Applying this exactness to the squares of the degree-m Lagrange basis polynomials shows every weight is positive. This completes the proof.

### Consequence: deterministic adaptive queries do not remove the ambiguity

Suppose a deterministic algorithm, with no finite upper bound on the atom count, always identifies t exactly after finitely many adaptive exact-transform queries. Run it on nu=SC_t0 with signal delta_0. It stops after m distinct queries. The theorem constructs a different finite-atomic signal with noise t<t0 giving the identical answers at every queried point. The algorithm therefore follows the same transcript and returns the same value on two different variances, a contradiction.

This argument is deterministic. It must not be advertised as an impossibility for every randomized exact-real oracle algorithm: the adversarial alternative here depends on the realized query locations, and exact equality at a fresh continuously random node can have measure-zero behavior. Every realized finite transcript nevertheless admits the displayed alternative. The noisy theorem below handles randomized/adaptive policies directly.

The m+1 atom threshold explains why N526's m>=k requirement is substantive: a signal with one more unrestricted atom can exactly hide the variance change. It is not missing numerical ingenuity.

## Theorem B: explicit exponentially close positive-noise alternatives

Fix a>0, b>=0, eta>sqrt(b), and integer k>=1. Define

`x_j=2 sqrt(a) cos(j pi/(k+1))`,

`p_j=2 sin^2(j pi/(k+1))/(k+1)`, j=1,...,k,

and mu_k=sum p_j delta_xj. Compare two models:

- H0: signal delta_0 and noise a+b, with observation law nu0=SC_(a+b).
- H1: signal mu_k and noise b, with observation law nu1=mu_k free-convolved SC_b.

Both signals are positive finite atomic and supported in the fixed interval [-2sqrt(a),2sqrt(a)]. Their noise variances differ by the fixed amount a.

Set

`r=(sqrt(eta^2+4a)-eta)/(2sqrt(a))`, so 0<r<1,

`E_k = r^(2k+1)(1+r^2) / [sqrt(a)(1-r^(2k+2))(1-b/eta^2)]`.

Then uniformly for Im z>=eta,

`|G_nu1(z)-G_nu0(z)| <= E_k`.

### Proof

The k-point measure mu_k is the spectral measure at the first coordinate of the k-by-k tridiagonal matrix with zero diagonal and sqrt(a) on the two adjacent diagonals. Its normalized sine eigenvectors give exactly the displayed nodes and weights. Cofactor expansion therefore gives

`G_muk(z)=(1/sqrt(a)) U_(k-1)(z/(2sqrt(a)))/U_k(z/(2sqrt(a)))`,

where U_n is a second-kind Chebyshev polynomial. Let q=sqrt(a) G_SCa(z), choosing the branch |q|<1 with Im q<0. Then z=sqrt(a)(q+q^-1), and the elementary recurrence for U_n gives

`G_muk(z)=G_SCa(z) (1-q^(2k))/(1-q^(2k+2))`.

Consequently

`|G_muk-G_SCa| = |q^(2k+1)(1-q^2)/(sqrt(a)(1-q^(2k+2)))|`.

Write q=s exp(-i theta), 0<s<1 and sin theta>0. Then

`Im z=sqrt(a)(s^-1-s) sin theta <= sqrt(a)(s^-1-s)`.

For Im z>=eta this implies s<=r. The last exact identity is thus bounded by

`E0_k=r^(2k+1)(1+r^2)/(sqrt(a)(1-r^(2k+2)))`.

Now put h1=G_nu1(z), h0=G_nu0(z), and w_j=z-b h_j. Both w_j have imaginary part >=eta. Subordination and the elementary probability-transform Lipschitz bound

`|G_lambda(w1)-G_lambda(w0)| <= |w1-w0|/eta^2`

give `|h1-h0|<=E0_k+(b/eta^2)|h1-h0|`. Rearrangement proves the claim. All constants are explicit.

### Exact atom count does not restore uniform stability without separation

The pair above belongs to the class with supplied upper bound k. If the interface supplies the exact atom count k, replace H0's delta_0 signal by k distinct, equally weighted atoms in [-epsilon,epsilon]. In a free coupling, its self-adjoint signal operator X has norm <=epsilon. Resolvent identity for X+S versus S, where S is the same semicircular noise operator, gives

`|G_(mu_epsilon free-convolved SC_(a+b))(z)-G_SC_(a+b)(z)| <= epsilon/eta^2`.

Take epsilon=eta^2 E_k. Then both models have exactly k positive atoms and their observation transforms differ by at most 2E_k, with the same variance gap a. For all sufficiently large k, both supports lie within a common fixed compact interval. This version necessarily allows arbitrarily small atom separation; it makes no claim under a quantitative separation promise.

## Corollary: matched noisy-query lower bound

At each query z_j, assume Im z_j>=eta and observe

`Y_j=G_nu(z_j)+xi_j`,

where Re xi_j and Im xi_j are mutually independent N(0,sigma^2), independent across queries. Queries may depend on every previous observation and on model-independent randomization. Any estimator using at most M queries and satisfying

`P_i(|t_hat-t_i|<a/2)>=1-delta`, i=0,1,

for sigma>0 and 0<delta<1/2 must have

`M >= 4 sigma^2 (1-2delta)^2 / E_k^2`.

For the exactly-k variant, replace E_k by 2E_k.

Proof: conditional Gaussian KL per query is at most E_k^2/(2sigma^2). The chain rule gives KL(P0||P1)<=M E_k^2/(2sigma^2), including adaptive randomized policies. Thresholding t_hat at the midpoint creates a test whose two error probabilities sum to at most 2delta. Le Cam and Pinsker imply

`2delta >= 1-TV(P0,P1) >= 1-sqrt(M) E_k/(2sigma)`.

Rearrange. Because E_k is O(r^(2k)), the necessary query count grows at least as a constant times r^(-4k). This is an information lower bound applying equally to Pick feasibility, eigenmatrix inference, arbitrary optimization, or an unlimited-compute estimator under this exact oracle.

With adversarial deterministic transform error <=epsilon, the two models are indistinguishable at any number of restricted queries whenever epsilon>=E_k/2: their midpoint transform function is within epsilon of both. This is a statement about an error-bounded oracle, not about a physical probability spectrum requirement imposed on corrupted replies.

## Reproduction and resource ledger

Run `python3 work/spectral_acquisition/verify_spectral_barrier.py` (Python 3 and NumPy). It writes `spectral_diagnostics.json`. Current run used NumPy 2.5.3 and took approximately 0.052 seconds locally; timing is not a performance claim.

The exact-transcript example uses three nodes, nu=SC_1.25, alternative noise 0.2, and four positive alternative atoms. Its forward-sample mismatch was 5.98e-16 in floating point. A 4096-node reference semicircle quadrature and a four-step Lanczos construction approximate the rational quadrature in the proof. These numbers are diagnostic, not interval certificates.

The explicit hard-family test evaluates 12,003 nodes, checks the exact Chebyshev ratio against direct atomic summation, and computes both forward transforms by a contraction-certified fixed point. Largest formula discrepancy was 4.47e-16. The following are analytical lower bounds, not observed experimental sample requirements. Parameters: a=1, b=.25, eta=1, sigma=.01 per real coordinate, delta=.25.

| Atom upper bound k | Uniform transform gap bound E_k | Necessary independent noisy queries M |
|---:|---:|---:|
| 5 | 9.289e-3 | 1.16 |
| 10 | 7.528e-5 | 1.764e4 |
| 20 | 4.977e-9 | 4.038e12 |
| 30 | 3.290e-13 | 9.239e20 |

Constructing the k-atom hard family costs O(k) arithmetic and memory. Direct evaluation costs O(k) arithmetic per node; the ratio formula costs O(log k) arithmetic using repeated squaring, with finite precision charged separately. A Gaussian query costs one independent acquisition by definition; computing M such acquisitions cannot be replaced by counting algebraic iterations. Boundary realizations or optimized baselines receive the same nodes, noise level, atom-count information, and observations in the comparison.

No matrix diagonalization, physical detector, independently drawn eigenvalue model, or finite-N Wigner statistical comparison was implemented, because those would have different acquisition interfaces. The analytic exponentially small gap requires O(k) bits beyond fixed accuracy to resolve deterministically; reducing random uncertainty below that gap requires the exponential query budget just derived.

## Contemporary comparators and antecedents

- Lexing Ying, *Sparse free deconvolution under unknown noise level via eigenmatrix*, Applied and Computational Harmonic Analysis 79 (2025), 101802, [author manuscript](https://web.stanford.edu/~lexing/fdc1.pdf), [arXiv](https://arxiv.org/abs/2501.04599), [DOI](https://doi.org/10.1016/j.acha.2025.101802). The primary paper proposes a singular-value objective for unknown noise followed by sparse recovery. N526 already compares against it; our lower bound concerns the information interface shared by transform-based algorithms and cannot establish a speed advantage over it.
- Ying, *Blind free deconvolution over one-parameter sparse families via eigenmatrix*, [arXiv:2501.10660v2, 2025-07-10](https://arxiv.org/html/2501.10660v2). This author source explicitly states general blind free deconvolution is ill-posed, then restricts the input families and linearizes through R/S transforms. Our exactly finite-atomic transcript construction and quantitative oracle model are more specific obstructions; historical priority of these formulations was not established.
- Philippe Biane, *On the free convolution with a semi-circular distribution*, Indiana University Mathematics Journal 46(3), 705-718 (1997), [DOI](https://doi.org/10.1512/iumj.1997.46.1467). Standard semicircular subordination and regularity are imported here; the proof above independently supplies pointwise fixed-point uniqueness.
- Classical Gaussian quadrature, Chebyshev recurrences, rational interpolation, and two-point statistical testing are established tools. [NIST DLMF §3.5](https://dlmf.nist.gov/3.5) records the Gaussian quadrature framework; the required elementary argument is included above. We claim no new quadrature or statistical inequality.

The literature check is targeted, not exhaustive. These results should be stored as scoped internally reconstructed obstructions, not as a new historic theorem or a certified first discovery.

## Implications and strongest next gate

N526's computational advantage, if established, is useful inside a quantitatively identifiable sparse class. It cannot supply unknown model complexity or stable high-resolution information for free. Removing ordinary floating-point PSD uncertainty is worthwhile engineering, but cannot eliminate the displayed oracle ambiguity.

A physical change of interface can bypass the barrier. For example, observing two independent noisy matrices with the *same* unknown signal cancels the signal in their difference. If each GOE off-diagonal variance is t/N, then with n=N(N-1)/2 independent off-diagonal differences D_ij,

`t_hat=N/(2n) sum_(i<j) D_ij^2`, and `t_hat/t ~ chi_square_n/n`.

This has O(N^2) acquisition/arithmetic and an exact chi-square uncertainty law. It requires a second independently noisy matrix sharing the same signal, which is real added information; it is not available from two separately computed transforms of one observed spectrum. This familiar calibration mechanism is a baseline and an experimental-design direction, not a new invention.

The single consequential unresolved obstacle is **obtaining a quantitative, physically justified visibility or separation condition from the measurement process itself**. Sparse model promises, exact transforms, independent replicas, and visible near-boundary fragments must each be acquired or experimentally validated. Without that, improving inversion cannot establish a new practical capability.

Cross-branch handoff: Primitive Genesis can use these examples as exact tests against hidden supplied-oracle assumptions; Theoretical Pro can formalize the rational-quadrature ambiguity and oracle lower bound; Natural-Sciences Pro should seek physically realizable repeated observations or controlled interventions that produce the missing visibility, and benchmark their full preparation cost. No result here establishes new empirical physics or biology.
