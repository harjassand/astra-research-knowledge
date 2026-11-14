# Reconstructed R200 full dilute-core Poisson sampler

This reconstructs the previously reported algorithm from its mathematical interface because the current workspace did not contain the last implementation. It is not represented as recovered byte-identical code. Source: delivered four-corner archive's `sources/original_math_source_return.txt`, especially the original core interface.

## Exact scope and unresolved convention
L=1600, theta=4, phi=.02; nearest-neighbor perimeter P; plus activity exp(-8P+.04a). Augmented adjacency uses fixed NE/SW diagonal (degree six). Every core component is a contractible lift inside the original r by r rectangle, r=5. The source excerpt does not resolve whether this means five lattice sites or coordinate span five. The implementation EXPLICITLY accepts `core_sites=5` or `6` and refuses other values. Neither convention is silently declared to be the original. Both have <=49 sites; the common envelope is valid for both. Integration must select the original convention from governing source.

## Mark envelope
Each a-site augmented-connected polymer has a UNIQUE encoding: its lexicographically minimum torus vertex and the deterministic direction-ordered DFS tree traversal, length 2(a-1), in six directions. The reverse directions are paired. Every code is decoded and checked for closure, exactly a distinct sites, consistent contractible lift, box inclusion, canonical root and canonical DFS. Failed codes are nulls.

There are at most n*36^(a-1) codes. Use rational per-code bounds
b_1=(10/27)^31;
b_a=(10/27)^40/36^(a-1), 2<=a<=49.
For a sites, square-lattice perimeter is at least 2 ceil(2 sqrt(a)). `tests()` verifies exp(-8Pmin+a/25)<=b_a using exact rational alternating Taylor bounds and squaring, for every a=1..49. Thus total mark intensity
Γ=n[(10/27)^31+48(10/27)^40]=1.0931717844...e-7.

Draw Poisson(Γ) marks; sizes, roots, and six-letter codes according to their rational envelope weights. Valid codes are thinned with probability exp(-8P+a/25)/b_a. Independent Poisson thinning leaves one independent Poisson variable of intensity z(S) for each valid polymer S.

Reject the entire draw if any accepted polymers overlap or touch in augmented adjacency. For a compatible unordered family, the Poisson probability is exp(-Σz) Πz(S): duplicates are incompatible; no factorial multiplicity remains. On conditioning compatibility, this is exactly the Gibbs law on the chosen core because distinct augmented components have no physical nearest-neighbor bonds, so energy adds. The empty family guarantees acceptance >=exp(-Γ). No finite perimeter/polymer truncation is used beyond the defining finite core.

## Arithmetic and acquisition costs
Poisson inversion uses exact rational lower/upper bounds on exp(-Γ) multiplied by rational cumulative sums. Bernoulli exponential thinning uses range-reduced alternating Taylor bounds, exact squaring, and an expanding dyadic random-uniform interval. No fixed precision cap, floating decision, numerical logarithm or fixed seed supplies the law. `secrets` is the ideal random-bit interface assumption; the Python runtime/entropy source is not a formal cryptographic proof.

Expected proposal restarts <=exp(Γ)<1.00000011. An envelope mark has <=96 symbols and validates at <=49 sites. Translation/root sampling costs O(log n) random bits. Exact exponent comparisons terminate almost surely and have finite expected work for fixed rational exponents and scales; no uniform polynomial-in-general-parameter proof is supplied here. This finite R200 algorithm is not a uniform-temperature/full-r theorem.

## Executed evidence and limitation
`receipt.json`: 10,000 unconditional source draws, all empty. This is expected at the extremely dilute setting and is NOT an empirical test of rare polymer probabilities. `forced.json` separately exercises singleton, physical-pair, diagonal-pair exponential branches, with exact bounds checked before draws; forced tests are not unconditional source samples. Tests cover wrapped contractible lifts and distinguish five-site/six-site cores.

This solves only source sampling for the explicitly selected convention. It does NOT sample the source-flux/capacity tilted law efficiently; a direct source-decision success probability C/(κZA) can remain exponentially small. It does not provide Nκ, residence-time bounds, whole-cut energy acquisition, or a practical transition-time estimator. Existing source interface already asserts a polynomial TV sampler; exact finite implementation is constructive machinery, not claimed novel theorem or North Star result.
