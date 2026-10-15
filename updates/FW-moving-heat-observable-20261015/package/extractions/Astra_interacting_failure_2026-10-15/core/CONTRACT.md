# Finite-error conditional path sampler

This closes the time/likelihood numerical gap for the explicitly pinned **synthetic rational fixture**, not for the original NumPy samples or a calibrated physical system. It does not establish a general-purpose production sampler for every parameter regime. Standard assumptions are correct Python integer/Fraction operations and independent fair random bits. Seeded `random.Random` is used only to reproduce the demonstration, and does not prove the random-bit premise. The kernel is auditable, not formally verified.

## Model and implementation

The SHA256 and exact decimal-rational parameter convention are those of `../conditional_precision/model_pin.json`. T=1/200, n=400, k=20, beta=2. The fixture hash and exact lambda-list consistency are checked on every run. Optimized Python (-O) is rejected so certificate assertions cannot be disabled. Explicit guards check max(lambda)*T<=1/2 and M*T<=1, plus the stronger fixture-specific .0075 and .3 bounds below. Each W entry is the rational represented by the stored binary64 scalar's Python repr, rather than that binary64 scalar itself. All model arithmetic after that decoding is exact integer/rational. The resulting h0 is approximately 5.10418718710409704415e-14; this slight difference from the earlier binary64-pinned model is intentional.

`sampler.py` constructs a 256-bit outward suffix-tail DP. Conditional label probabilities are replaced by their computed lower dyadic endpoints, and are sampled by comparing fresh 256-bit integers. The sum over stages of the largest reachable conditional interval width bounds the sequential-label total variation distance; there is no extra coin-rounding error because each chosen endpoint already is exactly a 256-bit probability. Forced labels remain forced.

Each selected label receives a fresh 64-bit integer R and u=(2R+1)/2^65. A floating inverse-CDF calculation supplies only a candidate rational c. Integer Taylor brackets verify that the exact inverse CDF at u is within DELTA=T*10^-12 of c. Floating arithmetic never decides a label, ordering certificate, likelihood, or confidence endpoint. All returned candidate times lie in [0,T]. If the candidate fails, exact rational bisection supplies a verified replacement. The implementation never drops an inconvenient sample.

Likelihood jump factors, weighted excess hazards and holding exponents are rational. Weighted full-column sums are precomputed once. Thereafter the exact excess-hazard update uses only prior failed labels, so dense-model preparation is O(n²) and each likelihood needs O(k²) integer arithmetic rather than a fresh O(nk) scan. This optimization is valid because the input is the fixed additive pair-interaction model.

## Elementary exponential kernel and finite termination

For rational 0<=x<=1, the code propagates lower/upper integer endpoints of each x^j/j! on scale S=2^256, forms alternating sums through even degree 40, and subtracts an upper endpoint for the degree-41 remainder from the lower sum. Alternating-series monotonicity proves the resulting enclosure of exp(-x). Rounding is by integer floor/ceil, with no transcendental library trusted.

For the inverse CDF, lambda*T<.0075. The kernel endpoint width is at most 200/S + (.0075)^41/41!, well below 2^-240. The p=1-exp(-lambda*T) uncertainty has the same bound. At an ambiguous bisection comparison, the discrepancy between the true CDF numerator at c and u*p is at most twice this bound. The derivative of that numerator is lambda*exp(-lambda*t)>= (1/2)*(1-.0075)>0.49. Thus an ambiguous midpoint is far closer than DELTA to the inverse, and the c±DELTA endpoint test succeeds. At a nonambiguous comparison the retained half interval contains the true root. After 40 such bisections its width is below DELTA; at worst one more midpoint and its endpoint check succeeds. The code permits 64 iterations, and treats a violated bound as an error rather than silently returning a path.

On every path, H<=M*T, where M=2(k-1)sum(lambda)/n<57, so H<.285<.3. The same kernel's likelihood-width bound is at most C[200/S + (.3)^41/41!]<2^-200. (The code also checks the computed interval width.) Return the midpoint after clipping the interval into [0,C], where C=product_(s=0..19)(1+2s/400). Clipping preserves its enclosure of the true candidate-path weight. Numerical weight error is therefore at most zeta=2^-200, a deliberately conservative budget.

These are finite fixed precision constructions. All loop lengths and all rational denominator sizes are bounded for this fixed fixture. Arbitrary changes in n, rates or T require rechecking the constants and bounds; the script is not advertised as a uniform bit-complexity theorem over all models.

## Coupling proof

Couple the ideal conditional labels and dyadic labels sequentially. Their mismatch probability is at most eta_label, the sum of worst reachable probability-interval widths. For matched labels use independent continuous uniforms U, with R=floor(2^64 U). The ideal truncated exponential inverse has derivative

    p exp(lambda*t)/lambda <= T exp(lambda*T) < 2T.

Thus its ideal time and the verified candidate time differ by at most

    epsilon = DELTA + T*2^-64.

This is a functional coupling. The finite time grid is not close in total variation to the continuous-time law.

Conditional on any chosen set, ideal times are independent, and each has density at most lambda/p <= (1+lambda*T)/T < 2/T. For each pair, probability of separation at most 2*epsilon is at most 8*epsilon/T. A union bound over at most n(n-1)/2 pairs gives

    eta_order <= min(1, 4*n*(n-1)*epsilon/T).

Outside that event the entire order, hence first k labels and rational jump product J, agree. For successive waiting times the difference is at most 2*epsilon. Excess hazards on all pre-threshold states are between 0 and M, so |H-H'|<=2k M epsilon. Since both exponents are nonnegative, exp(-x) is 1-Lipschitz there. Consequently

    |J exp(-H) - J exp(-H')| <= C*2k*M*epsilon.

Label/order mismatch costs at most C because both weights lie in [0,C]. Therefore for the implemented rational output Z and exact ideal L,

    |E Z - E L| <= B_num
      = zeta + C*(eta_label + eta_order + 2k*M*epsilon).

For this fixture B_num < 0.000001602827. This is a bias bound at the conditioned scale and does not contain 1/p. No independence between the mismatch event and weights is needed. Label coupling can be selected independently of the time uniforms; the conditional density bound is uniform over every label set.

## Confidence calculation

Fix N before sampling. Under independent unbiased random bits, returned Z values are iid in [0,C]. Use their own exact rational mean and unbiased sample variance, not latent ideal weights. The two-sided empirical Bernstein radius is

    R = sqrt(2 S² log(80)/N) + 7 C log(80)/(3(N-1)).

This is the fixed-sample 95% bound obtained from Maurer–Pontil (2009), Theorem 4, applied to Z/C and 1-Z/C with a union bound; original source: https://www.cs.mcgill.ca/~colt2009/papers/012.pdf . The present implementation conservatively substitutes 4.383 for log80 and proves exp(4.383)>80 by an exact finite positive Taylor sum. Square root is rounded upward on a 2^-128 grid using integer isqrt. h0 DP endpoints are rational, too.

Let h_-<=h0<=h_+. A 95% interval conditional on the iid-bit premise is

    [h_- max(1, mean-R-B_num), h_+ min(C, mean+R+B_num)].

The constraints 1<=E L<=C follow from the attractive-model coupling and likelihood bound. This is fixed-N inference, not an optional-stopping confidence sequence. Samples were not taken until a desired interval happened to appear.

## Executed demonstration

Command: `python core/sampler.py 3000 722`.

Fresh confirmatory run, seed 722, N fixed to 3000 before this run, distinct from the seed-721 runtime-only 10-sample benchmark. The prior seed-721 3,000-sample output is preserved as `exploratory_results_3000_seed721.json`; it reused the pilot prefix and is superseded for the reported interval. Distinct deterministic seeds are not a proof of statistical independence. It is distinct from the earlier NumPy run. The benchmark was not used to select a sample mean or variance threshold. Total runtime approximately 5.6 seconds, including 0.91 seconds preparation. No inverse fallback was needed in this particular run; maximum selected count 23. Results are in `results_3000.json`.

- Mean returned likelihood: 1.5278820340757162
- Sample variance: 0.0009477379765270790
- Label TV upper bound: 2.373e-32
- Order-mismatch upper bound: 6.384001e-7
- Total normalized numerical bias: 1.602827e-6
- Empirical Bernstein radius: 0.0102258202236833
- Conditional 95% p interval: [7.74639322004729e-14, 7.85079858342434e-14]
- Half-width divided by lower endpoint: below 0.006739, hence below 1%

The run supplies a reproducible arithmetic certificate and the theorem supplies coverage under its stated randomness model. Neither a deterministic PRNG seed nor the numerical experiment verifies physical truth or independently proves the probabilistic assumptions.
