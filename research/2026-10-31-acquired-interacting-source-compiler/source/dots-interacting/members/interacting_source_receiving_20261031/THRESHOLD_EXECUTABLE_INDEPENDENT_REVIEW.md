# Independent executable review: rational threshold-source acquisition

31 October 2026. Verdict: PASS for exact classical circuit-specification acquisition and canonical record verification in the declared positive-rational open-chain domain. No source edit was required. This is not an implemented quantum state-preparation or retained-simulator backend.

## Exact source bindings

- `acquire_threshold_source.py`: 9,263 bytes, SHA-256 `1b79b249475c1cae8e240a1898c3413a4d8f29608f8365e07ae132d28bbd94be`.
- `test_threshold_acquisition.py`: SHA-256 `1675bed798d8cad401695f76e8fd2bb196bc268a1d5af4e62a37a827760b294a`.
- Independent added tests `test_threshold_independent.py`: SHA-256 `9e759cbc4cc3fd7ada839ba9a50bf447e984adb62c84c1f0a83ef158025f0ad6`.
- Independent results `threshold_independent_checks.json`: SHA-256 `a68b1820b063cd883248389a22ba39edeafaa44f41061785342a438db1cf26d3`.

Both supplied files were read in full, and the supplied ten unittest groups were independently executed successfully. The source remained unchanged throughout this audit.

## 1. Raw input and exact local law

The constructor accepts a nonempty list of two-entry positive rational onsite factors and exactly n-1 positive rational 2-by-2 nearest-neighbor factors. Integers, rational strings and Fraction objects are accepted; booleans, floats, zero/nonpositive factors and malformed shapes are rejected. Labels and sites reject booleans and nonintegers, not only out-of-range values.

`ratio_flip` correctly cancels every unchanged Gibbs factor, including the left/right orientation of nonsymmetric edge-factor matrices. The derived heat-bath rate is ratio/(1+ratio). All contexts contain only the existing one or two chain neighbors. Exact sorting and duplicate removal yield strictly positive interval widths, and `map` uses the interval upper endpoint with >=, which is constant throughout the represented threshold interval. The complementary-rate property proves the asserted n<=R<=2n bound.

`column(x)` enumerates exactly two slots per color: y=x and y=x flipped at that color's site. It tests f(y)=x and assigns the correct weight Delta/R times pi_y/pi_x. There is no hidden inversion subroutine or enumeration over the full configuration space. The exact normalization assertion is justified by reversibility; independent tests checked equality to the forward random-map transition law and the actual reversible erasure relation.

## 2. Gibbs messages, means, and numerical description length

Suffix sum messages acquire the exact partition sum and first/conditional probabilities. The separate minimum-product suffix recursion computes the actual minimum unnormalized configuration weight, not a surrogate sum. Thus `pi_min` is exact for this open chain. Conditional denominators are positive suffix sums, and multiplying the stored conditional probabilities reconstructs pi(x).

`parity_mean` inserts the correct (-1) bit factors during the transfer recurrence. It therefore returns exact source Z-string expectations, including the identity string. Sparse masks are deduplicated; work is proportional to the supplied mask list rather than all possible strings.

For finite rational input length, these recurrences have polynomial rational bit complexity: a product of the supplied local denominators provides a polynomial-bit common denominator, and the sum over configurations adds only polynomially many bits to its numerator bound. A very small probability is not processed by a numerical reciprocal-sized loop. The test with 1001-bit factors exercises this distinction but is not the proof of polynomial complexity.

## 3. Influence certificate and dyadic rounding

For each ordered neighboring pair (i,j), the code maximizes the absolute change of the site-i bit-1 conditional probability over all other local contexts. It adds this value to column j. Thus kappa=1-max(column) uses the appropriate column-sum influence certificate, even for asymmetric supplied factor matrices.

If kappa<=0, the valid source specification remains available but return_m is None and return_admitted is False. Failure of this sufficient contraction certificate is not a declaration of instability or nonexistence of a faster quantum realization.

For kappa>0, ell is the exact smallest integer with 2^ell>=16n/pi_min. Its bit-length estimate and correction loops are valid at exact dyadic boundaries and on both sides. The code chooses m=ceil(R ell/kappa), so

(1-kappa/R)^m <= exp(-kappa m/R) <= exp(-ell) <= 2^(-ell) <= pi_min/(16n).

This is a conservative safe replacement for the natural-log return horizon. It uses no floating-point transcendental comparison. The code stores the horizon as an integer; its acquisition runtime does not iterate m times. A large horizon still remains a real downstream resource cost.

## 4. Canonical verifier and limitations

`verify_spec` reconstructs all acquired data from the record's raw factors and requested mean-mask keys, then compares canonical JSON exactly with nonfinite numeric values disallowed. It explicitly rejects nonmapping inputs and noninteger/bool version markers. Reconstruction plus exact JSON comparison rejects altered colors, probabilities, means, dimensions, scope, return flags and numerical types such as n=3.0. Extra or noncanonical keys do not silently become trusted claims.

This verifies the algebraic record for the factors contained in it. It is not an authenticity check against some independently stored raw input, experimental model truth, a caller's external requested-mask manifest, or an implemented quantum circuit. In particular:

- A truthful unadmitted source record still verifies; callers must separately inspect return_admitted before invoking the contraction-based compiler.
- Removing all optional requested parity means yields a different but valid record. The verifier does not promise that an external caller's requested output list has been fulfilled.
- Changing the raw factors and recomputing a correct full record is not forgery of the inference algebra; external input binding must be handled by the consumer.

The independent adversarial harness initially expected an empty parity-means table to be rejected. That expectation was corrected because means are explicitly optional; no source defect or weakened false-value test was hidden by that correction.

## 5. Executed evidence

The supplied ten test groups passed, including 32 random small rational-chain classical-law checks, selected dense W-isometry/dark-state checks, exact means/messages, malformed input/record tests, dyadic rounding and symbolic n=64 acquisition.

The independent harness additionally passed:

- 80 random rational open chains through five spins, 992 exact source columns, all their Z-string expectations and conditional-message products;
- 142 malformed or noncanonical specification checks;
- 1,245 exact dyadic-boundary checks through 249-bit scales;
- a positive-rational extreme-factor case with 1001-bit numerical input;
- a valid nonadmitted strong-interaction record;
- symbolic n=128 acquisition, with 764 colors, return_m=22,910 and a 558-bit minimum-probability denominator.

The symbolic case builds no 2^128 source-state table. Dense calculations occur only in explicit small test code, not in the acquisition module. These tests support the full code review but are not a universal theorem or quantum circuit implementation.

## 6. Receiving boundary

The output is an exact classical specification for the separately reviewed paper W/psi/c construction, plus a sufficient return certificate and optional diagonal means. Actual square-root rotations, reversible arithmetic gates, quantum reference reflections, complete simulator assembly and hardware execution are not implemented in this module. Their costs and finite-error budgets remain the paper receiving theorem's explicit obligations. Known rational model input is not an unknown-source learner. No novelty or practical advantage is inferred.
