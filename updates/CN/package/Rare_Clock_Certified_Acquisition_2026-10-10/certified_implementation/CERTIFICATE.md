# Certified finite-bit first-hit acquisition: bounded implementation gate

Date: 2026-10-10. This is an internal implementation and mathematical certificate, not an external software audit, historical novelty certification, or a claim about arbitrary initial CTMC states.

## Outcome and exact scope

A working finite-bit implementation is provided for stationary independent binary CTMC components with dyadic target probabilities and positive rational relaxation rates. All decisions, logarithm enclosures, rate calculations, and output sums use Python integers and exact fractions. There is no floating-point sampling or transcendental oracle. Floating-point values in result files are display-only approximations or wall-clock measurements. A display value outside binary64 range is null. Exact rational encodings use decimal numerator/denominator text normally, and explicit 0x hexadecimal numerator/denominator text beyond 10,000 bits; exact_fraction parses either form without disabling Python's decimal-conversion protection.

The original construction and finite-bit specification are unchanged. This implementation uses the same Brown/Cox law and a separately accounted, less conservative finite-bit variant. It uses certified exponential arrival cells instead of a bounded Poisson probability table. Exact input Bernoulli draws are bounded because this gate requires dyadic probabilities; non-dyadic probabilities are explicitly rejected.

Under independent unbiased input bits, the algorithm always returns a nonnegative rational Hhat and admits a coupling with the exact stationary first-hit time H satisfying

    P(|Hhat - H| > epsilon H) <= D < delta.

For the delivered moderate instance epsilon = 1/4, delta = 1/20, and the explicit conservative failure bound is

    D = 59429 / 5242880 < 0.011336.

This is a multiplicative coupling guarantee. It is not a relative error guarantee for small tail probabilities, an exact path sampler, or unquantized total-variation approximation. The CDF consequence from the companion construction is

    sup_t |F_Hhat(t) - F_H(t)| <= D - log(1-epsilon)/e.

For epsilon=1/4 this is approximately 0.1172; a simple all-rational bound is D+1/8 < 0.136336, using -log(3/4)<=1/3 and 1/e<3/8. This CDF statement is deliberately weaker than the tape-specific observed error.

## Random-bit assumption versus executable evidence

The public acquire(..., tape_bank=...) API accepts BitCallbackBank: a caller supplies an independent getbits(k) callback per stream. Each callback must return an integer in [0,2^k), with independent unbiased bits across calls and streams. The adapter checks type and range. Statistical independence cannot be certified by a finite test.

The initial reproducible validation runs use explicitly labeled, deterministic SHA256 counter fixtures. They prove the arithmetic, bounded execution, and tape-specific enclosure claims recorded below. They are NOT, by themselves, random samples whose law is proved IID. The probability theorem applies to the identical executable algorithm with the stated independent-bit source contract. No pseudorandom seed is silently treated as information-theoretic randomness.

A separate, single OS-backed moderate acquisition uses os.urandom through OSRecordedBank. Its generated bit blocks are preserved and replayed exactly by PrefixReplayBank; no reselection or additional reference run was performed. OS entropy is a practical implementation of the bit-source interface, not a mathematical proof of physical independence. The requested probability guarantee retains the same explicit bit-source assumption.

An injected source must supply a matching replay bank to request a same-tape reference. The production algorithm itself never needs a reference. No continuous random input is used by the executable.

## Exact input and operation budget, recorded before running

Moderate instance:

- n = 4
- p = (1/8, 1/16, 1/32, 1/16)
- lambda = (1, 2, 4, 8)
- target->other rate for component i: (1-p_i)lambda_i
- other->target rate: p_i lambda_i
- initial law: independent stationary product law
- q = 1/65536
- epsilon = 1/4; delta = 1/20

Preflight constants:

- h = epsilon/(2+2epsilon) = 1/10
- kappa = (1, 23/16, 27/16, 117/64)
- L = 8
- R = M = (4800, 6900, 8100, 8775)
- K = (115214, 165614, 194414, 210614)
- J = 1,400,288 maximum main-algorithm exponential cells
- eta = 1/292608000
- a = 1/1792368640
- b = 94 uniform bits per exponential cell
- P = 126 fixed-point fractional bits; N = 45 series terms
- conservative expected exponential-cell count <= 142,884

The input-dependent physical time is not simulated. A 1,000-cell preflight microcheck took about 0.03 seconds. No worst-case tape or probability table is preallocated. The literal constants in the companion specification would require roughly 1.90 million compressed sample marks for this same moderate instance, before small-stratum count work; this tighter-budget variant avoids that unnecessary acquisition cost.

The machine-readable PREFLIGHT_BUDGET.json also includes deterministic bit-request bounds. These bound calls to getbits(k); a source that fetches whole bytes may use extra padding bits.

## Algorithm

Sort rates together with their corresponding probabilities. Compute q, maximum-activated-rate stratum weights w_i, and kappa_i exactly as in the companion construction. Choose the following values by integer/rational comparisons:

    h = epsilon/(2+2epsilon)
    L = smallest integer with 4n(3/8)^L <= delta/4
    R_i = M_i = ceil(6 kappa_i L / h^2)
    capell = smallest integer with n 2^-capell <= delta/64
    K_i = 24 R_i + capell + 1
    J = 1 + sum_i (R_i + 2K_i)
    eta = min(epsilon/100, delta/(512 sum_i R_i))
    a = delta/(64J)
    2^-b <= eta a^2/16.

The constructor verifies the final relative-error inequalities exactly. The theorem concerns inputs accepted by these checks.

For one b-bit integer k, the ideal uniform extension lies in [k/2^b,(k+1)/2^b]. Reject to fallback output zero if this entire cell is not contained in [a,1-a]. Otherwise construct a rational interval [Elo,Ehi] enclosing -log(U) for every ideal extension, with Ehi-Elo<=eta Elo. A point Epoint in this interval is the finite exponential output.

Draw the W cell from one exponential cell divided by q. For stratum i, let [rlo,rhi] and rpoint be w_i times the corresponding W interval and point.

- If rpoint >= 2R_i, assert rlo>=R_i and compress. Generate exactly M_i independent stratum marks and return rpoint times their point-value mean.
- Otherwise generate certified exponential arrival cells, summing their lower and upper endpoints. Accept the next arrival if its upper sum is <=rlo. Stop if its lower sum is >rhi. If neither comparison is certified, return fallback zero. If K_i arrivals have all been accepted, also return fallback zero.
- After a successfully determined small count, generate that many stratum marks, using exact dyadic Bernoullis and exponential cells. Return their sum.

A stratum mark is E / (lambda_i + sum_{j<i} lambda_j B_j), with P(B_j=1)=1-p_j. Grouping point and interval sums by observed exact rates reduces denominator growth. Only observed groups are stored; the sampler never constructs the product-state generator. The n=4 reference tests do construct a small killed generator, solely for independent verification.

Each main failure returns rational zero and records its reason. A runtime failure of an asserted mathematical enclosure is an implementation error, not a silently accepted certificate; the proved width bounds ensure it cannot occur for accepted cells in exact Python arithmetic.

## Integer logarithm enclosure

For v in [1,2], write z=(v-1)/(v+1), so 0<=z<=1/3. Use

    log(v) = 2 sum_{j>=0} z^(2j+1)/(2j+1).

At fixed-point scale F=2^P, propagate lower powers by floor division and upper powers by ceiling division using the exact rational z^2. Sum each term with outward rounding. The omitted tail is bounded by

    3 * 3^-(2N+1).

The code chooses N so this tail is at most one fixed-point unit. At each power recurrence the interval width is at most three units; hence the full log interval width is at most 10N+2 units, conservatively.

For midpoint U_b=(2k+1)/2^(b+1), use binary range reduction and a cached outward interval for log(2). The midpoint log interval has width at most (b+2)(10N+2) units. For every U in the cell, the mean-value theorem gives

    |log(U)-log(U_b)| <= 1/(2k).

Expand both sides by ceil(F/(2k)) units. For an accepted cell k/2^b>=a, total enclosure width is bounded by

    2^-b/a + C 2^-P,   C=(b+2)(10N+2)+2.

The constructor chooses P and N so C 2^-P<=eta a/16. Combined with the b-bit bound, the width is <=eta a/8. Since the true exponential is >=-log(1-a)>=a, the interval lower endpoint is positive and its width is <=eta times that lower endpoint. This proves the per-cell assertion. The point and every ideal extension therefore differ by a multiplicative factor at most 1+eta, in either direction.

## Failure budget and coupling proof

1. Endpoint cells. For one uniform, rejection has probability at most 2a+2*2^-b<=4a. Expose up to J input uniforms, even for adaptive draws. The union charge is <=4aJ=delta/16. Exponentials used only by the optional reference are not part of this main-algorithm budget.

2. Branch slack. Every accepted W cell has multiplicative width at most 1+eta. A compressed stratum satisfies true r>=2R/(1+eta)>=R. A small stratum satisfies true r<(1+eta)2R<=9R/4<3R. Branch selection depends only on the W cell, so conditional independence of arrivals and marks is retained.

3. Small-branch ambiguity. Arrival sums inherit the same multiplicative interval-width bound. If an arrival sum interval intersects the W intensity interval without a certified decision, its ideal arrival time lies in

       [ r/(1+eta)^2, (1+eta)^2 r ].

   For eta<=1/8 this band has length <=5eta r. Conditional on W, the probability that a unit-rate Poisson process has any arrival in this band is at most its length. Summing small branches and using r<3R gives a charge <=15eta sum_i R_i. No unstable comparison is guessed.

4. Count cap. Reaching K accepted arrivals implies Poisson(r)>=K. In a small branch r<4R and K>=24R. The classical Chernoff bound and e<3 give

       P(Poisson(r)>=K) <= (e r/K)^K < 2^-K.

   Thus all count caps cost at most n 2^-capell<=delta/64.

5. Compressed strata. Apply the companion centered-mark and compound-Poisson concentration bounds at h, with true r>=R and M=R. The two failures per stratum sum to at most 4 exp(-L). Since e>8/3, total charge over all n strata is at most 4n(3/8)^L<=delta/4. True compound-Poisson marks and the compressed sample-mean marks are conditionally independent given W, as supplied by separate source streams.

On the complement of these failures, small-stratum counts are exactly the same as the ideal Poisson process at true r, and each output mark approximates its coupled ideal mark by factor at most 1+eta. For a large stratum, concentration and two finite-cell factors give

    (1-h)/(1+h)/(1+eta)^2 <= Hhat_i/H_i
                                      <= (1+h)/(1-h)*(1+eta)^2.

The constructor checks these are within [1-epsilon,1+epsilon] using exact rational arithmetic. Summing nonnegative strata preserves relative error, including the zero atom. The ideal sum has the stationary CTMC hitting-time law by the companion Brown/Cox reduction.

The total implemented bound is

    D = delta/16 + 15eta sum_i R_i
        + n 2^-capell + 4n(3/8)^L < delta.

No measured frequency is used in this proof.

## Bounded work

A small branch uses at most K_i arrival cells and K_i-1 mark cells. A large branch uses exactly R_i mark cells. The deliberately loose J bounds the main execution. The count loop never depends on the huge global Cox count. Conditional on an accepted W cell, a small branch uses at most 2N(r)+1 exponential cells before completion or charged abort; its expected count is <=2r+1<=9R/2+1<5R+2. This proves the preflight expected-cell bound 1+sum_i(5R_i+2), independent of q and numerical rate ratios.

Each mark needs at most n-1 exact dyadic Bernoulli draws and O(n) rational operations. Arithmetic bit lengths include the supplied rate and probability sizes and the number of bounded operations. The small n=4 implementation deliberately does not make a production-performance claim for large n or arbitrary rational Bernoulli denominators.

## Reproducible evidence

REPLAY_RESULTS.json records the complete exact rational output, exact intensity and H intervals, bit-stream hashes, and counts. Fixture seed: rare-clock-certified-20261010-v1.

- Moderate instance: three small strata with counts (6,106,3423), one compressed stratum with 8775 marks
- Main execution: 15,849 exponential cells and 1,619,385 requested bits
- Certified full same-W reference: 55,468 ideal marks enclosed using 110,941 exponential cells
- Same finite tapes are reused for all small-stratum arrivals and marks; exact stream hashes are tested
- The rational reference interval proves the output is within 0.001653 relative error for every extension of these finite cells
- Typical recorded runtime: about 0.5 seconds main, about 3.5 seconds including reference

This is one controlled tape, not a Monte Carlo statistical claim. The exact continuous H itself is represented by an enclosure, not falsely reported as an exactly computed real number.

An additional scale check uses p_i=2^-50 for all four components, the same rates, q=2^-200, and the same requested accuracy. All four strata compress, with mark counts (4800,7200,8400,9000). It uses 29,401 exponential cells in about 0.9 seconds and returns an exact rational time approximately 2.13e59. No exact Cox reference is generated for this enormous-count case. Its role is to verify finite representation and bounded operation count; it supplies no new statistical validation.

The final 17-test suite also verifies q=2^-2000 display overflow and q=2^-20000 exact serialization, plus deliberate reference-fingerprint mismatch rejection, OS-prefix exact replay, prefix-corruption rejection, and replay exhaustion rejection. Tests include independent exact-Fraction log endpoint enclosures, exact rational killed-generator resolvent comparisons at s=(1/16,1,16), zero-atom preservation, forced endpoint/ambiguity/cap failures, bad-source rejection, invalid and floating input rejection, deterministic replay, and small-stream identity. Test results and the separate audit are included. No full-state floating-point CDF comparison is used as a certificate.

## One OS-backed acquisition, no reselection

OS_ACQUISITION_RESULTS.json records the one fresh OS-backed draw. It had no acquisition failure and used 14,769 exponential cells, 1,514,177 requested bits, small counts (2,90,2903), and one compressed stratum of 8,775 marks. It returned an exact rational approximately 3600.61881067 in about 0.50 seconds. OS_PREFIX contains 189,440 bytes of generated blocks (including a few unused padding bits) plus the source/stream manifest.

OS_REPLAY_RESULTS.json records exact prefix replay. The rational output, branches, counts, consumed-bit counts, and all stream fingerprints match. No new random bits are fetched by replay, and a changed or insufficient prefix is rejected. No full Cox reference was generated for this fresh draw. It is an actual OS-source acquisition under the stated source assumption; its tape-specific relative error was not measured.

## Reproduction

From this folder:

    python certified_clock.py --budget-only
    python certified_clock.py --reference
    python -m unittest -v test_certified_clock.py
    python certified_clock.py --replay-recorded OS_PREFIX

The extreme-rarity result has its own exact input and preflight JSON. PROVENANCE.json identifies companion proof hashes, the Python/platform environment, and fixture labels. SHA256SUMS covers the delivered files. No original proof or prototype file was modified.
