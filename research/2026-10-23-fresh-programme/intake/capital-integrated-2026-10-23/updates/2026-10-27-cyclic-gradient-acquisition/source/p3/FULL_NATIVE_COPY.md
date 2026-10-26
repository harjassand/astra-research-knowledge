## ASTRA Pro3 — A joint consistency test for scientific response laws

The new construction exposes an information failure that simpler response-family methods miss: every pair of observations can be consistent with a smooth, strongly convex energy law, while the entire set is incompatible with any such law.

For a stable energy \\(E\\) with

\\[ I\preceq\nabla^2E\preceq3I, \\]

I constructed three exact position–force observations. All three pairwise smooth-convex interpolation tests pass. However, one directed three-observation cycle violates the necessary energy-consistency inequality by exactly

\\[ \boxed{\frac{11}{75}}. \\]

This is a decisive finite-data rejection of the proposed conservative-source contract, not merely a failed numerical fit.

The underlying interpolation mathematics is established.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://arxiv.org\&sz=32)

arxiv.org

&#x20;The consequential acquisition principle is that a scientific learner must retain joint compatibility, not just individual response intervals or pairwise admissibility.



### New capability: unforeseen symmetric feedback controllers

I extended the compiler to matrix-valued feedback controllers chosen after acquisition.

Suppose the unknown energy satisfies

\\[ \mu I\preceq\nabla^2E\preceq LI \\]

and a future task specifies a symmetric matrix \\(K\\) with \\(K\prec\mu I\\). The requested equilibrium solves

\\[ \nabla E(x)-Kx=p. \\]

By passing to the convex conjugate of \\(E(x)-\tfrac12x^\top Kx\\), I obtained an exact finite interpolation test using the historical gradient readings. It retains a single compatible source across all future loads handled under that fixed controller.

The key technical improvement is an anisotropic interpolation metric: the test uses the full matrices \\((\mu I-K)^{-1}\\) and \\((LI-K)^{-1}\\), instead of replacing them with loose scalar curvature bounds.

I executed six previously unspecified controller/load combinations, including controllers with off-diagonal couplings, using three previously acquired two-dimensional gradient readings and zero additional learner source calls. All passed exact rational source-consistency and equilibrium-enclosure checks.

The conditional transfer is exact for each fixed symmetric controller. Joint optimization across different controllers remains a separate, generally harder problem.

### Further result: four-way evidence can invalidate every three-way explanation

A second counterconstruction shows that pairwise and three-way consistency are not sufficient for larger scientific records.

For four controlled native measurements, every one of the four possible three-measurement subsets admits a globally smooth, strongly convex source. Nevertheless, the entire record has a four-cycle violation of exactly \\(14/75\\).

Even with adversarial force-report error up to \\(10^{-3}\\) per coordinate, the certified incompatibility margin remains approximately 0.181059. This establishes why a scientific agent needs a complete joint-evidence test rather than a catalogue of locally plausible explanations.

### Another transferred capability: energy differences from gradients alone

The same acquisition record can answer questions about differences in force-controlled energy, without measuring energy directly.

| Native gradient calls | Sharp energy-difference interval | Width |
| --------------------- | -------------------------------- | ----- |
| 2                     | [0.303333, 0.363333]             | 0.060 |
| 3                     | [0.318333, 0.348333]             | 0.030 |
| 5                     | [0.325833, 0.340833]             | 0.015 |

The later task was unspecified during acquisition. Additional experimental positions were selected from previously known controlled positions, without access to a native inverse oracle.

The bounds are sharp over the declared source class. An independent source-aware calculation gives the true answer \\(1/3\\), inside every interval. Absolute energy remains undetermined without an energy calibration.

### Computational correction

The original exact-rational future-equilibrium optimizer suffered coefficient explosion. I replaced it with outward-rounded, certified tangent cuts.

Twelve rational cuts now produce a bracket on the sharp minimum equilibrium coordinate:

\\[ -0.161629954214\le u\_{\min}\le-0.161628. \\]

The width is approximately \\(1.95\times10^{-6}\\), with cut coefficients requiring at most 24 bits. Both the outer bound and the compatible-source witness were independently checked.

The remaining limitation is substantial: separately compatible controllers need not admit a single common physical source. The work includes an exact counterexample. A complete, efficiently solvable joint representation across arbitrary different feedback controllers remains unresolved.

### Preserved results

Complete proofs and scientific findings

Gradient-only interpolation, cycle falsification, sharp inverse bounds, anisotropic feedback, executable certificates and limitations.

Reproducible research archive

17 files, including executable scripts, six research result sets, independent verifier, governing proofs and SHA-256 manifest.

All six investigations passed clean-directory execution with byte-identical results. Archive integrity and hashes were verified.

Scientific assessment: The strongest development is a joint experimental-knowledge representation that can both generate new certified operations and decisively reject some false scientific assumptions. It remains conditional mathematical and synthetic-source research. The core interpolation mathematics is established, and an equally informed retaining method can reproduce the results.

The work is saved locally. The Astra GitHub repository was not modified.