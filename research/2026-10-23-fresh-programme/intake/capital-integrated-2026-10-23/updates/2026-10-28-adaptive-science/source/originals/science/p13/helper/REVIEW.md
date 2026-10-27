# Critical review of integrated owner proof

Reviewed the full owner `PROOF.md`, with particular attention to Sections 3–5, the interval implementation, and both new certificate scripts. I reran `certify_finite_network.py` and `certify_envelope.py`; both passed with the retained numerical enclosures reproduced. I found no substantive sign, normalization, attainability, or leading-asymptotic error in the claims actually made.

## Checks that carry the conclusions

1. For total side mass one, the actual star compliance is exactly `sum m_i^2/k_i`. The rational Section 3 cell saturates `C=1/20` and uses total spring constant `2300/99<24`. Its displayed quadratic/cubic coefficients agree with the exact general star trace, second coefficient, and determinant. All three passbands enter the integral. The one-pendant comparison uses the actual optimum `k=20` in `[20,24]`, not a mistuned comparator. The interval gain is strictly positive.

2. In Section 4, `r^2=(A-2)/C` is correctly normalized for the effective backbone `4/A`: the effective side mass is `2-4/A`, and its compliance moment in the *original fixed-mass normalization* is `D=C/4`. The fitted zero-trace-multiplier dual therefore compares to every actual fixed-m=1 network even though the limiting two-band cell itself has a different trace. The missing trace term vanishes because `mu=0`; it is not silently discarded. Equality would force the limiting active spectrum, which contradicts the actual trace 4. Dark modes do not repair this contradiction. The finite-H stars charge both compliance terms and converge to the effective response, while the third band escapes to infinity. Thus the nonattainment and exact infimum arguments are consistent.

3. In Section 5, differentiating `w^3*g(w)` gives `lambda(r)=r*g(r)*(r*coth(r)-5/2)`, with the stated sign. The supporting dual has one root at `sqrt2` and at least a double root at `r0`; the three-zero multiplicity bound makes these exactly the complete positive root list. Its pointwise sign therefore gives the all-network coefficient `eta0/4`, including the correct factor of four from compliance. Eliminating lambda between the two root equations gives precisely the displayed constructive slope.

4. I independently checked the potentially delicate finite-star asymptotics. Write `R=r0^2`. The specified sequence has

   `b=C*R+O(C^2)`, `h=1-C*R+O(C^2)`, `H=C^-2`, and `k/b=R+C*(R-R^2/2)+O(C^2)`.

   After multiplying the exact characteristic polynomials by `C^2`, their finite roots are simple at the limit. Direct perturbation gives

   `alpha_low = R+C*R+O(C^2)`,

   `beta_acoustic = 2-C*2*R/(R-2)+O(C^2)`,

   `beta_low_optical = R+C*2*R*(R-1)/(R-2)+O(C^2)`.

   Taking square roots yields exactly the proof's acoustic-edge and optical-width coefficients. The high-frequency edge is of order `1/C`, so the omitted Bose tail is smaller than every power of C. The resulting `O(C^2)` objective remainder is justified.

## Certificate implementation

The integral formula is correct: `integral_a^infinity g = sum_(n>=1) exp(-2*n*a)*(2*a^2+2*a/n+1/n^2)`. The positive remainder bound uses decreasing positive coefficients and a geometric exponential tail. The total integral is `pi^2/6` at theta=1/2. The Machin arctangent and exponential Taylor remainders have the correct signs, and interval rounding is outward. Polynomial root brackets isolate all roots because their counts exhaust the characteristic polynomial degrees and strict interlacing is checked.

The root sign brackets prove existence without a separate uniqueness proof. This is sufficient: choosing any exact root within each certified bracket with the enclosed multiplier signs establishes the bound/construction. A full global phase diagram is correctly left unproved. The finite spring-cap optimum at 24 is also correctly left open, and the sharp small-C sequence openly spends unbounded stiffness. No stronger physical, novelty, or conventional-method advantage is supported by this review.
