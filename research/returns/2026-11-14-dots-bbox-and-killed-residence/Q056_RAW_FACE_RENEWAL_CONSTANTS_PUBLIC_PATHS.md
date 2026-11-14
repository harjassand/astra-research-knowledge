# Exact constants for the analytical box164 renewal reduction

The raw outer-face/hole injection is developed separately with the creative agent. It is an auxiliary COUNTING representation of closed unit squares, not the original fixed-diagonal filled-domain definition. Every originally allowed augmented-connected polymer is geometrically connected, so counting the larger class is safe. Rooted four-direction outer and hole walks may revisit vertices. The finite tests in geometric_face_count_tests.json check the corresponding perimeter and energy decomposition, including touching boundaries; tests are not the general topological proof.

For a polymer S with raw filled hull F and bounded geometric holes H_i,
E(S)=8P(F)−.04|F|+Σ_i[8P(H_i)+.04|H_i|].
For a b-wide bounding box, hole starts occupy at most(b+1)^2 dual vertices. Dropping compatibility and hole area weights yields a hole factor exp Γ_h(b), with
Γ_h(b)≤(b+1)^2(1/745)^4/(1−1/745),
because4exp(−8)<1/745. Use expΓ≤1/(1−Γ) throughout.

For core box164 hulls, area/P≤164/4 gives E(F)≥6.36P. For P≤40, area≤P²/16 improves this to7.9P. Handle P4/P6/P8 directly with shape counts1/2/9 and inherited rational activity bounds(10/27)^31, (10/27)^47, (10/27)^63. The remaining hull activity is bounded by
n[(1/674)^10/(1−1/674)+(1/144)^42/(1−1/144)],
where4e^-7.9<1/674 and4e^-6.36<1/144. This deliberately overcounts odd/invalid perimeters. Multiplying the total hull activity by1/(1−Γ_h(164)) gives polymer activity Γ<1.087e−7; therefore the hard-source numerator contribution inside the core beyond a is at most Γ/(1−Γ)<1.087e−7.

A first exit adds one gate joining old box164 components. The new component fits329×329, is contractible, and has at least one side165. Its raw filled hull therefore has physical outer perimeter≥332 and E(F)≥4.71P. Since4e^-4.71<1/27, the total component envelope is
T≤n(1/27)^332/(1−1/27)/(1−Γ_h(329)).
Pay329²=108241 possible gate sites. Native detailed balance bounds each outward edge by the post-component activity times the unaffected core configuration. Renewal occupation and h_a≤1 then give
p_exit≤[1/(1−Γ)]108241T(1+e^31.96)/n.

renewal_box164_raw_faces.py uses only exact Fractions for these comparisons, finite Taylor LOWER bounds for each exponential denominator, and the conservative e^31.96<3^32. It verifies p_exit<10^-450 and λ_a<10^-7. Its diagnostic logarithm of the exact rational p bound is−1047.43238998; the logarithm itself is ordinary float reporting, not the exact certificate.

If M bounds the full native mean hitting time of{a}∪B from every first-departure configuration, including all companion components, the outside occupation contribution is≤λ_a p_exit M. Thus M≤10^454 would suffice for outside contribution<10^-3. Using the killed-generator bound in KILLED_DURATION_CERTIFICATE.md, congestionρ≤10^446 would already suffice. Neither M norρ has been proved here. The raw-face topology premise and the subsequent path-congestion premise must not be conflated with these executed rational scalar inequalities.
