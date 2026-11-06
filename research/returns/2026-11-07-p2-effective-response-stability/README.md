# Information stability of effective response

P2's completed return determines the leading logarithmic sensitivity exponent of the effective conductivity throughout the stated exponential-moment class. It also constructs finite rational coarse materials from valid coefficient names and gives an explicit limitation on predicting localized interventions from passive response. The exact logarithmic upper endpoint remains open.

[Full response, actual prompt and expanded visible activity](P2_EFFECTIVE_RESPONSE_STABILITY_20261107_RETURN.txt) · [Original ZIP](original/Effective_Response_Stability_20261107.zip) · [Complete proof](package/RESEARCH_REPORT.txt) · [Source identities](SOURCES.json).

| Read next | Contents |
|---|---|
| [Research report](package/RESEARCH_REPORT.txt) | Full theorem, geometric matrix interpolation, radial lower family, uncertain-record limits, finite-name algorithm, intervention obstruction, costs and primary credit |
| [Reusable objects](package/REUSABLE_OBJECTS.json) | Sensitivity, precision and intervention statements at their declared contracts |
| [Exact family bounds](package/FAMILY_BOUNDS.json) | Producer's rational enclosures for T = 16, 64, 256; illustrative checks, not the universal proof |
| [Producer program](package/verify_family.py) | Standard-library rational enclosure computation, preserved as source and not executed by Capital |
| [Package index](package/PACKET_INDEX.txt) and [manifest](package/SHA256_MANIFEST.json) | File roles, unchanged predecessor identities and member hashes |
| [Earlier certified response/homogenization](../2026-11-06-p2-certified-degenerate-response/README.md) | Existence, primal/dual density, valid-name certificate algorithm, effective tensor and periodic variational limit used here |

## Exact class and theorem

On the volume-one unit torus in every d >= 2, A is a measurable real symmetric positive-definite conductivity for a **scalar linear PDE**. In fixed units put `K_A = max(1, ||A||op, ||A^-1||op)` and require `integral exp(tau K_A) <= M`, with tau > 0 and M > exp(tau). No minimum feature size or uniform pointwise ellipticity is supplied across the class. The nontrivial statement requires strict moment slack: at M = exp(tau) the class contains only I almost everywhere; below that it is empty.

Let omega(eta) be the worst operator-norm difference of effective tensors among pairs in that class with coefficient L1 distance at most eta. The result is

`lim[eta -> 0] log omega(eta) / log log(1/eta) = -tau`.

The lower bound is `c [log(1/eta)]^-tau`; the upper bound is `C_alpha [log(e+1/eta)]^-alpha` for **every alpha < tau**. The supplied constants are computable and can be independent of dimension, while computation itself retains its dimension costs. **An upper bound with power exactly tau is not asserted.** The result excludes every uniform positive Hölder power and every logarithmic power greater than tau, while leaving possible subpower endpoint factors unspecified.

The proof uses the classical positive-matrix geometric mean path and Thompson distance, including noncommuting matrices. The path stays within the same fixed-unit moment budget; actual energy concentration controls response variation in an Orlicz distance. Clamping plus accepted primal/dual smooth density justifies passing to degenerate endpoints. The matching radial family consists of finite individually bi-Lipschitz maps and individually uniformly elliptic coefficients with a common moment budget; no singular ideal cloak is assumed. Higher dimensions use a two-dimensional block embedding, rather than an incorrect higher-dimensional pullback formula.

## Information and constructive use

A known coefficient center B and a certified L1 uncertainty radius describe potentially different true materials. Two truths compatible with the same record give a worst-case error obstruction even with unlimited internal computation, including randomized expected error. This is an information limit for that record, not a universal runtime lower bound for all explicitly known material formulas.

With coefficient fidelity eta = 2^-b, worst-case response uncertainty has leading order `b^(-tau+o(1))`. Response accuracy epsilon = 2^-p needs leading fidelity `b = 2^(p/tau+o(p))`. Here b counts absolute-accuracy digits; it need not equal a succinct formula's length. An operation lower bound needs an access convention charging for those digits. A true formula known without ambiguity can remove the two-truth obstruction.

For a supplied valid program returning expanded rational uniform-dyadic tables with certified L1 errors and the moment promise, the wrapper constructs a positive rational step material B with error at most 3 eta and moment budget M + 1. It computes approximations to cell means from finer returned tables; neither exact means nor an inverse/PDE oracle are supplied. The earlier finite certificate algorithm then encloses the effective tensor to the requested tolerance. Name validity and the global moment guarantee are supplied promises, not properties decided from a finite coarse image.

All source-program running time, parameter interval calculations, common-grid expansion, coefficient bits, rational averaging/inversion, finite cell solves and discovered certificate stopping stages are charged. The grid can contain `2^(d max(h,h_s))` cells; analytic dimension-independent constants do not eliminate that cost. No uniform polynomial bound in succinct description length or requested accuracy bits is claimed. The wrapper is mathematically constructed; the delivered program computes selected lower-family bounds rather than implementing the complete new coarse-material wrapper end to end.

## Passive information and interventions

The uniform baseline I and a boundary-fixing transformed baseline have the **same effective tensor and complete passive Dirichlet-to-Neumann operator**. Adding the same coordinate-labelled I inclusion on the small physical core produces different effective tensors. Thus passive response alone is not a complete state for predicting these local reconfigurations in the stated anisotropic class, even with unlimited computation. The classical conductivity coordinate gauge retains credit. This does not exclude richer coefficient information, actual intervention experiments or extra structure that fixes the gauge.

The response bound controls all constant loadings, effective inverse tensors and the stated constant-tensor Dirichlet macroscopic solutions. It supplies no uniform finite-period homogenization rate, microscopic unweighted solution estimate, nonperiodic/stochastic law, arbitrary nonlinear system theorem or P versus NP result. Earlier QUBO remains unresolved.

The original report credits the primary planar/logarithmic regularity and distortion work, positive-matrix geometry, conductivity transformation invariance, div-curl, weighted density, hypercircle and numerical homogenization precedents. No historical priority, physical validation, practical advantage or civilisation-scale achievement is established by publication. Producer checks give exact rational bounds for synthetic family members, including coefficient error about 8.60e-224 and response gap above 2.90e-7 at T = 256; the universal result comes from the supplied analytic proof.

Collected 7 November 2026 Brisbane. Capital preserved the six-member archive and complete capture without executing the science or conducting a new audit. No new coordinator impact score is inferred at this publication. Generated retrieval was not rebuilt. The renewed three-Pro dispatch authority belongs to the coordinator/dispatcher loop; Capital publishes this completed return and sends no scientific assignment. Sol remains closed and held, Dots protected, and all source/resource limits remain.
