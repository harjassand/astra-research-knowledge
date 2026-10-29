# Independent audit: bounded-local-strength to bounded-incidence reduction

Date: 2026-10-29 UTC. Auditor: `challenge_thermal_counting_consequence`.

## Verdict

**PASS for the unconditional randomized sparsification reduction, and conditional PASS for its fixed-accuracy thermal/counting consequence.** No missing locality factor, tail-index error, sign restriction, or precision obstruction was found. The imported exact-counting algorithm is still a premise, not audited here. There is no novelty claim for the sampling/concentration method.

The physical class is fixed-k qubit Hamiltonians with bounded sum of local operator norms incident to each qubit. This is not merely a bound on the global norm of H or on the total interaction strength with arbitrarily concentrated hubs. Scalar/empty-support terms must be removed and restored as known shifts. Sampled occurrences are kept as separate local terms; merging duplicates is unnecessary.

## 1. Envelope and exact-input access

For a fixed d-by-d rational-complex Hermitian local matrix h, the rational quantity

`alpha=sum_ij (|Re h_ij|+|Im h_ij|)`

satisfies `||h||<=alpha<=2d^2||h||`. The lower bound follows through the Frobenius norm and entrywise absolute sum; each entry is bounded by the spectral norm for the upper bound. Thus genuine bounded local norm sums imply bounded, exactly computable envelope sums up to a fixed k-dependent factor. No unknown local norm oracle is needed. Define `g_v=sum_{e containing v}alpha_e`, `g=max_v g_v`, and `L=sum_e alpha_e<=ng`. Zero envelopes imply zero terms.

The branch `L<=epsilon n/4` returns the zero **Hamiltonian**: its ground-energy density is 0, but its free-energy density is `-ln2/beta`. Both restore any scalar shift. The perturbation guarantee in this branch is immediate from `||H||<=L`.

## 2. Sampling concentration, with the dimension factor included

In the nontrivial branch put `a=epsilon n/4<L`, `q=ceil(512L^2/(epsilon^2 n))`, and sample e with probability `p_e=alpha_e/L`. The Hermitian random matrix `Y=h_e/p_e` satisfies

```
E Y=H, ||Y||<=L, ||Y-H||<=2L,
E[(Y-H)^2]=E[Y^2]-H^2 <= L^2 I.
```

The last relation is valid for indefinite and complex Hermitian terms; positivity of the individual h_e is not assumed. Applying the two-sided self-adjoint matrix Bernstein bound to q independent centered samples in dimension `2^n` gives

`Pr(||Hhat-H||>a) <= 2^(n+1) exp[-q a^2/(2L^2+(4/3)La)]`.

Since a<L, the exponent is at least

`(3/10)q a^2/L^2 >= 9.6n`.

For every integer n>=1, the failure probability is below .00028. This is a simultaneous all-states operator-norm bound, not just an estimate of a few state energies. The exponential dimension is correctly absorbed by q=O(n), rather than omitted.

The invoked primary result is [Tropp, *User-Friendly Tail Bounds for Sums of Random Matrices*, Theorem 1.4](https://arxiv.org/pdf/1004.4389). Its one-sided bound applies to both X and -X to yield the displayed two-sided prefactor.

## 3. Constant incidence by trimming, without a union-bound logarithm

For every qubit v, `X_v~Bin(q,g_v/L)` and `mu_v=qg_v/L`. The ceiling in q contributes at most `g/L<4g/(epsilon n)`, so

`mu_v <= Lambda=512g^2/epsilon^2+4g/epsilon`.

Choose the integer

`D=ceil(9Lambda)+ceil(log2(max(2,200g/epsilon)))`.

The logarithm ceiling can be computed by rational/integer comparisons. Delete each sampled occurrence touching any v with `X_v>D`. If a vertex was bad it has no retained incident terms; otherwise it has at most D. Every occurrence has norm at most

`L/q <= epsilon^2 n/(512L) < epsilon/128`.

The exact tail identity is

`E[X 1{X>D}]=qp Pr(Bin(q-1,p)>=D)`.

The index D on the right is correct: the event on the left is X>=D+1. Applying the ordinary binomial tail bound with mean at most Lambda gives

`E[X_v 1{X_v>D}] <= mu_v (eLambda/D)^D <= mu_v e^(-D)`,

because `D>=9Lambda>e^2 Lambda`. This also holds when D>=q, since the left side is then zero.

Let Tdel count deleted **occurrences**, without double-counting an occurrence that touches two bad vertices. Then

`Tdel <=sum_v X_v 1{X_v>D}`.

Consequently the computable triangle-inequality deletion envelope U satisfies

```
||Hhat-Htilde|| <= U=(L/q)Tdel,
E U <= (L/q) sum_v mu_v e^(-D)
     = sum_v g_v e^(-D) <= ng e^(-D) <= epsilon n/200.
```

There is no additional factor k: the incidence sum is already bounded by ng. The chosen logarithm term ensures the final inequality both when `200g/epsilon>=2` and when it is smaller. Markov bounds `Pr(U>epsilon n/4)` by .02. A union bound with the sampling error gives success greater than .9797, hence the claimed .97. Correlations between different vertices' degrees do not matter because the proof sums expectations rather than assuming independent degree events.

The output always has incidence at most D and local strength at most epsilon/128, including bad sampling outcomes. The approximation bound is probabilistic. U is efficiently observable from the sampled indices; the original large-matrix sampling error is not claimed efficiently certifiable.

## 4. Random bits, preprocessing and transfer

All probabilities are rational. A common denominator converts the alpha_e to nonnegative integer weights whose bit lengths are polynomial in the original input length. Prefix sums and binary search allow exact sampling using a uniform integer below the total weight. Rejection from the next power-of-two range takes fewer than two trials in expectation. Hence q samples and all local rational rescalings cost expected polynomial bit work, with polynomial space, at fixed g,epsilon,k.

For a bounded-runtime Monte Carlo version, cap each draw at `t=ceil(log2(1000q))` rejection attempts. The union probability of any cap failure is at most .001. Charging that failure still leaves overall correctness above .9787, and therefore above .97. A capped failure must be flagged or counted as an algorithmic failure; it is not permission to silently regard a biased approximate draw as exact. No `2^n`-dimensional matrix is constructed during preprocessing.

For a scalar density target epsilon, use sparsification budget epsilon and backend accuracy epsilon/2: operator-norm perturbation contributes at most epsilon/2 to ground/free-energy density. For a low-energy-state target epsilon, use sparsifier parameter epsilon/2 and backend witness accuracy epsilon/2; the former contributes at most epsilon/2 after the norm error is paid twice. Exact measurement access remains exact for whichever rational witness was constructed; only its energy guarantee against the original H is probabilistic.

After sparsification, the earlier theorem applies with fixed incidence D and fixed local norm. Thus, conditional on the imported sparse exact-counting premise, the scalar result is a randomized `poly(input length,n) 2^{o(n)}` algorithm at fixed accuracy. The counting stage is deterministic once the sampled Hamiltonian is fixed. Exact measurement sampling additionally has its previously stated expected running time. Polynomial input-bit overhead must not be suppressed when discussing strict volume-subexponential time.

No logarithmically vanishing-error extension is certified here: D grows as epsilon decreases and the saved physical proof has very large dependence on D. Nor does this approximation preserve spectral gaps, ground spaces, global Gibbs states, or dynamics.

## 5. Existing sparsification comparators actually inspected

- [Anshu and Nirkhe, *Circuit Lower Bounds for Low-Energy States of Quantum Code Hamiltonians*, Theory of Computing 21(12), Appendix C, Lemma C.4 and its proof](https://toc.cs.uchicago.edu/articles/v021a012/v021a012.pdf) already sample local Hamiltonian terms and apply operator concentration. The displayed degree proof uses regularity and a union bound requiring sample count at least `n log n/ell`; for fixed ell its bound therefore retains logarithmic degree dependence. It is not a direct substitute for the present weighted, trimmed, constant-incidence guarantee. This comparison establishes prior sampling machinery, not novelty of our modification.

- [Basu, Brakensiek and Putterman, *Many Hamiltonians Are Sparsifiable*, arXiv:2605.02211v1 (May 2026), Theorem 1.1 and related results](https://arxiv.org/html/2605.02211v1) give near-linear-term multiplicative sparsifiers for shifted-Pauli and other broad PSD families. Their guarantee is stronger near low energies but their stated families and term-count output differ from arbitrary Hermitian additive-density approximation with bounded maximum incidence. Their result should be acknowledged rather than describing Hamiltonian sparsification as unexplored.

- [Aharonov and Zhou, *Hamiltonian Sparsification and Gap-Simulations*](https://arxiv.org/pdf/1804.11084) study preservation of low-energy eigenspaces/gaps and prove degree-reduction obstacles under that stronger simulation notion. Extensive additive norm error can destroy those features, so the present construction does not contradict their result.

Important dense/high-degree subclasses also have stronger polynomial-time mean-field/product-state approximation methods; this reduction is a general conditional algorithm, not a claim to beat those subclasses' algorithms or to invent a new sparsification principle.

## 6. Actual independent replay and additional branch tests

I read the root diagnostic source and results, copied the script to `independent_replay/`, executed it, and checked the JSON byte-for-byte against the root result. It matched. The 120 double-precision dense diagnostics at n=3,4,5 had reported errors below their budgets and correct normalization/degree/deletion bookkeeping. Their D exceeds q, so trimming cannot occur in those cases. These runs do not establish rare-tail probabilities or exact rational sampling.

I separately wrote and executed `independent_replay/check_sparsifier_exact_arithmetic.py`. It checks 1,500 binomial-tail identities using exact rational arithmetic, plus three forced rare sample sequences with valid theoretical parameters `n=64,g=1,epsilon=1/2,q=32768,D=18513`. The sequences exercise both-high-endpoint deletion, one-high-hub deletion, and surviving disjoint components. They verify occurrence counts, the potentially double-counted incidence upper bound, and the final degree cap. They deliberately include rare bad-approximation sample sequences; their purpose is trimming bookkeeping, not an empirical success-rate claim. All checks passed.

No full counting solver, physical preparation, integrated arbitrary-Hamiltonian backend or rare-tail statistical validation was executed in this audit.
