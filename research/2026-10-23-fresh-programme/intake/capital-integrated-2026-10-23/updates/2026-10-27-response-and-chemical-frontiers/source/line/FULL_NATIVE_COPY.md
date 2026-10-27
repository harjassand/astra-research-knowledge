## Astra Pro3 — Research continuation, 27 October 2026

Research direction: Move beyond globally affine causal-interaction models toward certified discovery of nonlinear interventions.

The previous construction could learn sparse interactions efficiently, but a fourth-order interaction caused it to reject the model. That failure reveals a more fundamental question: can an agent discover and optimize useful nonlinear effects without knowing the maximum interaction order?

### 1. New mathematical construction

I derived a way to certify an optimum along a selected intervention family without assuming linearity, positivity, sparsity or a finite polynomial degree.

Let \\(f(x)\\) be the experimentally measured causal-interaction response as intervention dose \\(x\\) varies. Suppose an independent physical argument supplies just one regularity guarantee:

\\[ f''(x)\geq -M. \\]

For two measured settings \\(a\\) and \\(b\\), every intermediate response must satisfy

\\[ \boxed{ f(x)\leq \frac{b-x}{b-a}f(a) +\frac{x-a}{b-a}f(b) +\frac M2(x-a)(b-x). } \\]

This follows from the convexity of \\(f(x)+Mx^2/2\\).

The important distinction is that the response may contain arbitrarily high-order nonlinear effects, including signed interactions. Only its maximum downward curvature is constrained.

This produces a new experimental procedure: retain uncertainty intervals from physical measurements, calculate the highest response still compatible with the curvature bound, and choose the next experiment where that upper bound is greatest. Once the upper bound and the best measured lower bound are sufficiently close, the learner has a certified intervention choice.

This is a conditional theorem, not an acquired physical law. The curvature bound must be justified independently; successful measurements alone cannot establish it.

### 2. Stronger result: acquire the nonlinear response shape

The more promising construction needs no supplied bound on the size of the second derivative. Instead, it assumes

\\[ |f'''(x)|\le K. \\]

This limits how quickly curvature changes, while allowing an arbitrarily strong unknown quadratic interaction in the chosen intervention coordinates.

Three measured settings determine a quadratic interpolant \\(p_2\\). With bounded measurement uncertainty, every unseen response in an interval of width \\(h\\) has a certified error bounded by

\\[ |f(x)-p_2(x)| \leq \frac54\eta\_{\max} +\frac{Kh^3}{72\sqrt3}, \\]

where \\(\eta\_{\max}\\) is the largest measurement-interval half-width.

I executed this through a reconstructed four-port Schur-compatible source, including nonlinear background responses, continuum linear relaxation, affine instrument drift and adversarially bounded raw sensor errors.

Executed synthetic experiments

| Unknown nonlinear interaction               | Native reactions | Certified regret |
| ------------------------------------------- | ---------------- | ---------------- |
| Fourth-order + rational higher-order effect | 20               | 0.0008541        |
| Negative modifier coefficient               | 20               | 0.0008734        |
| Much stronger unknown interaction           | 20               | 0.0007731        |
| Unknown quadratic interaction               | 12               | 0.0001545        |

All bounds are in factorial-response units. These are synthetic calculations, not physical experiments or a reproduction of the unavailable original native script.

The learner also retained enough information to answer five previously unspecified intervention objectives, each with a different dose penalty. In the primary experiment, it generated previously unmeasured intervention settings with zero additional source readings and certified regret below 0.001375 for every objective.

This is a meaningful improvement in the scope of the acquired knowledge: a finite set of observations supports new continuous-dose decisions even when the causal response is not affine or polynomial.

### 3. Information-theoretic limits established

Two adversarial constructions clarify exactly what the learner has and has not achieved.

First, the interpolation precision is essentially optimal for the three-point observation interface. I constructed two source laws satisfying the same third-derivative bound and producing identical historical native reactions, yet differing by 0.0096225 in an unmeasured factorial response. This matches the theoretical three-point interpolation uncertainty almost exactly.

Second, the method cannot be extended to all 126 intervention positions merely by increasing its confidence. I constructed two sources with zero third derivatives everywhere, identical reactions across 20 axial measurements, and a difference of 3 in their response to an unmeasured mixed intervention. Discovering interactions between coordinates requires measurements that actually excite those interactions.

A separate lower-bound proof gives worst-case regret scaling at least as

\\[ \Omega\left(\frac{KB^3}{m^3}\right) \\]

for \\(m\\) exact adaptive measurements on the fixed one-dimensional family. The acquired interpolation method matches this exponent, though not necessarily the best constant.

An independent read-only verifier has also reconstructed all 92 native-reaction intervals and all 25 post-acquisition intervention certificates directly from the saved exact-rational traces.

### 4. Scientific assessment and remaining obstacle

The strongest outcome is a reusable, uncertainty-certified intervention procedure, not a new physical law or a civilisation-level breakthrough.

The mathematical ingredients have established precedents in polynomial interpolation and optimal recovery. An equally informed retaining algorithm could reproduce these guarantees, potentially improving their constants.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://eng.libretexts.org\&sz=32)

Engineering LibreTexts+1



The next important obstacle is to derive the regularity guarantee from actual physical dynamics and discover useful intervention subspaces rather than supplying them in advance. I also derived a route for obtaining the required third-derivative bound from a fifth mixed-derivative bound on the underlying reciprocal response. That physical contract remains unestablished for the original source.

### Preserved research

The complete mathematical arguments, exact-rational source traces, executable programmes, independent verifier and counterexamples are saved.

Full scientific proof and findings

Conditional theorems, actual results, information limits and next research obstacle.

Complete reproducible research archive

13 files, including code, exact observations, result records and verification. Isolated replay reproduced the saved results byte-for-byte.

The Astra GitHub repository was not modified.