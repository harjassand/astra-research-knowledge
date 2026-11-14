# R200 streaming flow and thermal-core normalization

## Executed native large-instance work
Original theta4, phi.02, R200, L1600. The streaming implementation reproduces all previous R4–32 results. R200:

* Width1 deterministic growth log resistance: 6422.77191876298; 0.044s.
* Resistor-aware width2: 6422.34251116392; 42.742s.
* Width2 processes 214,294,799 triangular states, 427,307,200 edges, 1199 milestones.
* Peak transition array (1601*1602/2 doubles): 10,259,208 bytes; work vectors O(L).
* Maximum sink-mass error: 5.17e-14.

All numbers are floating evaluations, not outward certificates. Source contribution in these runs is 1 (kappa1). Source substitution below does not measurably change these logs but must be done in a certificate.

## Streaming recurrence
For strip states 0<=b<=a<=h, the backward suffix surrogate needs only the next a-row and current b+1 entry. Save p(a,b) in one triangular array. Forward propagation needs only the incoming a-row and previous b-entry, merging currents before squaring. No physical state bitmasks, path enumeration or separate edge array. O(L^3) real-arithmetic operations, O(L^2) peak memory for likelihood acquisition; the observed Python bottleneck was representational rather than intrinsic at R200.

Exact formulas define the transition likelihood. The implemented probabilities are finite precision. This is not an exact-random-bit sampler implementation.

## Physical source/target connectivity
The first strip begins at the empty plus set. Each DAG edge adds exactly one physical spin. Milestone end configurations are rectangles; each segment ends where the next starts. Intermediate area is strictly below majority until final area L²/2. This gives a valid unitflow from the reservoir edge attached to all-minus (which is in the original core) to B. No reflected chain, different heatbath clock or new source is substituted. Source resistance in units 1/wminus is kappa^-1. Extra source edges to other core configurations can carry zero current without violating conservation.

## Simple original-core normalization bound
The inherited r-box condition, even using the deliberately safe r+2 side convention from the older source, implies each augmented-adjacency plus component has at most49 sites at r5. Augmented graph degree is6. A canonically chosen DFS spanning tree encodes each rooted connected a-site set by a walk of length2(a-1), so at most36^(a-1) possibilities per root. Physical boundary satisfies P>=4sqrt(a) on a contractible lift. A component activity is exp(-8P+.04a). Components are physically nonadjacent, so activities multiply; dropping polymer exclusion gives

log(ZA/wminus) <= n sum_(a=1)^49 36^(a-1) exp(-32sqrt(a)+.04a).

This is a normalization bound, not a factorized physical Gibbs law. For a1 the exponent is -31.96 < -31. For 2<=a<=49, using log36<3.6 gives convex exponent bound 3.6(a-1)-32sqrt(a)+.04a. Its maximum on this interval is at an endpoint, both below -40 (sqrt2>1.4 suffices). Thus

log(ZA/wminus) <= n[exp(-31)+48 exp(-40)]
 < n[(2.7)^(-31)+48(2.7)^(-40)] < 10^-6.

The final strict comparison was checked exactly using Python Fraction (upper value1.09318e-7). This explicitly pays all core thermal configurations, not merely isolated defects or a fixed gas outside one path. It does not assert this bound is uniform in growing n at fixed temperature; the right side grows linearly with n.

## Consequence and limitations
If the numerical flow resistance is enclosed, Thomson plus the original clock bound kappa^-1<exp2593.6 yields

Ckappa/ZA >= exp(-10^-6) / (exp2593.6 + R_growth).

The R200 width2 numerical value suggests log inverse normalized lower about6422.342512. Compared with inherited exp(-6449), this is a useful tightening of one finite lower bound. Combining with the certified Wcut/ZA<=exp(-6215) still leaves W/C upper approximately exp207.343. This remains astronomically large; it is NOT a practical sampler, relative-time estimator, uniform polynomial guarantee or major breakthrough. The width2 refinement itself contributes only0.4294 to the exponent relative to the simple deterministic path; most of the26.7 improvement over6449 comes from evaluating a strong ordinary path more accurately.

Artifacts: resistor_stream.cpp, resistor_stream_results.jsonl. No certified floating enclosure has been supplied here. The explicit component normalization derivation is independently checkable and does not require a new literature claim.

## Added conservative directed certificate for width1
`certify_width1.py` now gives an independently reproducible positive-arithmetic enclosure for the simpler deterministic path, including full thermal normalization and original kappa. Each path energy is exactly an integer multiple of1/25. Resistance divided by exp6423 is a positive polynomial in q=exp(-1/25). Upper-bound q by the reciprocal of the 12th positive Taylor truncation for exp(1/25), then evaluate the polynomial in directed-upward 70-digit Decimal arithmetic. All exponents above5000 are lumped at5000, an explicit positive tail overcount. The reservoir term is also bounded by q^5000. The full-core multiplier exp(10^-6) is bounded by1/(1-10^-6).

The computed normalized resistance / exp6423 upper is <0.797, strictly below1. Therefore the derived conservative lower is **Ckappa/ZA > exp(-6423)**, conditional on the explicit geometry/core argument and the inherited original-clock kappa bound. This does not certify the stronger width2 numerical value. Combined with the retained marked upper exp(-6215), it tightens the conservative W/C bound from exp234 to exp208, still unusably large. This is a finite lower-bound refinement, not uniform polynomial progress. Source code and arithmetic receipt are saved; independent review remains appropriate before distribution.
