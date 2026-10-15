# End-to-end integer certificate for the boundary-DP mean

This is an independent implementation, not execution of the author's repository. The four fixtures use the exact rational values of binary64 outputs of NumPy RandomState(0).rand(n), sorted decreasing. Loads and temperatures are exact rationals: moderate F=7n/40,T=3/20; author-style F=n/8,T=1/20. The input JSON records the exact strengths; input text contains exact mechanics and outward-rounded exponent arguments.

## Reproduction

Compile `large_certificate.cpp` with `g++ -O3 -std=c++17 -o large_certificate large_certificate.cpp`, then run `python run_large_certificate.py 100 moderate` (or 400, or author). The only probabilistic-fixture dependency is installed NumPy; no external code is downloaded or executed. `validate_large.py` performs additional non-proof numerical cross-checks.

## What is certified

Let each independent operational-time clock have rate lambda_i=exp(-sigma_i/T), and let K(u) be the terminal avalanche size obtained from clocks surviving operational time u. The mean physical lifetime is the integral of E[psi(K(u))] du, psi(0)=0 and psi(k)=exp(-F/(kT)). The expectation is nonincreasing in u. This operational-time identity and the exact boundary recursion are derived in DERIVATION.md. This code certifies its integral for each fixed strength fixture. It does not certify the physical adequacy of that stochastic model or a disorder-averaged mean.

## Exact mechanics and fixed-point arithmetic

M=2^60. The Python input builder uses Fraction arithmetic to compare sigma_i*m with F, determine strict eligibility counts j_m, and construct the weak backward gate sigma_i*m<=F. Thus binary64 near-equality cannot silently change the mechanical convention. Every exponential argument is bounded outward at denominator M.

For fixed dyadic probability inputs, both forward prefix and backward gate recursions are convex weighted sums with weights p and 1-p. Integer evaluation floors after each sum. Their errors are nonnegative and bounded respectively by j/M and (n-j)/M, since gates and convex combinations are nonexpansive in maximum norm. The product yielding a PMF component adds one further unit, so each computed component is below its exact value by at most (n+1)/M. Multiplying by a dyadic psi and flooring adds at most another unit per component. The sum over positive sizes is therefore low by at most n(n+2)/M. The implementation adds the conservative n(n+3)/M for its upper expectation.

The exact terminal survivor count is coordinatewise nondecreasing in the clock-survival bits, and psi is nondecreasing in count. Consequently, evaluating all lower probability bounds and lower psi bounds gives an expectation lower bound; upper inputs plus the error allowance gives an upper bound. This avoids invalid componentwise monotonicity assumptions about individual PMF entries.

All recurrence multiplication and addition uses unsigned 128-bit integers, with factors at most M and two products per convex combination, well below 2^128. The prescribed n<=400 and U<=10^11 keep integral numerators below range limits. A guard prevents overflow of the tail-bound product for unsupported input extremes. The demonstrated endpoint probabilities have one-unit upper bounds, so this guard passes trivially.

## Exponential enclosure without a trusted floating exp

For exact nonnegative fixed-point X/M, arguments >=64 give [0,1/M]. This follows from e>2 and 2^-64<2^-60. Otherwise reduce by an exact power of two until the argument y is <=1/2, bound y outward at denominator M, and evaluate the degree-24 alternating Taylor polynomial of exp(-y). The recurrence for each term y^k/k! uses integer floor/ceiling to bound it, and additions/subtractions use the appropriate interval endpoints. The alternating remainder is less than (1/2)^25/25! < 1/M; expanding both ends by one unit safely includes it. Repeated interval squaring returns exp(-X/M). For an input interval, monotonicity reverses its endpoints. All arithmetic used for the certificate, including exponentials, is integer arithmetic.

## Integral and tail

Operational-time endpoints are exact integer microticks (denominator D=10^6). Start at zero then one microtick; each following positive endpoint is ceil(1005*ticks/1000), capped at U*D. Left-upper/right-lower rectangles bound the entire finite integral, including the initial cell. Their accumulated integer numerator has common exact denominator M*D.

For the infinite tail, E[psi(K)] <= P(any clock survives) <= sum_i exp(-lambda_i*u). Therefore the tail above U is <= sum_i exp(-lambda_i*U)/lambda_i. Replacing lambda_i by its certified lower bound increases each term. The numerator exponential is bounded outward, and each division is rounded up into the common integral denominator. No floating-point value contributes to the claimed enclosure. Decimal endpoints and relative gaps in JSON are convenience displays; the integer numerator and denominator define the certificate exactly.

## Results

| n | F | T | certified lower (display) | certified upper (display) | relative gap | kernel seconds |
|---|---|---|---|---|---|---|
|100|17.5|0.15|3.273490843336511|3.2898583979281053|0.5000031%|0.323|
|400|70|0.15|3.942459356110544|3.9621717744506357|0.5000031%|3.860|
|100|12.5|0.05|515.050919196308|517.6270671983951|0.5001735%|0.487|
|400|50|0.05|858.3703837983501|862.676217625171|0.5016289%|6.280|

Moderate fixtures use U=100000 and 4133 evaluations; author-style fixtures use U=10^11 and 6903 evaluations. Wall-time measurements are illustrative, not a performance guarantee. The author-style n400 upper bound includes roughly 0.014 of deliberately conservative fixed-point error integrated over a very long interval. This can be reduced simply by shortening the already-negligible tail cutoff, but is unnecessary to achieve <1%.

The certificate is deterministic conditional on its saved fixture. Exact output is in `large_result_{n}_{kind}.json`; independently inspectable input is in matching `large_input_*` text. The numerical validation report is separate, because comparisons with high-precision or adaptive floating quadrature are useful implementation checks but do not provide the rounding proof.

### Storage qualification

The rolling forward/backward probability recurrence uses O(n) working storage. This prototype precomputes an n-by-(n+1) Boolean mechanics-gate table for transparent inspection, so the implementation's total mechanics storage is O(n^2), not O(n). Each row is a contiguous true-prefix and can be represented by a single integer cutoff floor(F/sigma_j), reducing total kernel storage to O(n), without changing any arithmetic or result. The saved input format also explicitly lists the gate table.
