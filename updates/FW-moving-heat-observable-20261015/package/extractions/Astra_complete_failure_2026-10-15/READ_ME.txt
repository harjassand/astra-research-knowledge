ASTRA RESEARCH HANDOFF: COMPLETE FAILURE WITH HETEROGENEOUS LOAD SHARING
15 October 2026

RESULT
A reproducible, bounded-error calculation for a specified 400-component interacting model gives a conditional 95% probability interval
 [9.179222971065028e-51, 9.320102976605232e-51].
The relative half-width is below1%. The fixed production run used3,000,000 draws,147.04seconds of sampling/aggregation and30.66seconds of exact preparation in this environment. This is a model calculation, not an experimental material result. Coverage assumes the stated binary64 arithmetic semantics and independent fair random bits; the saved pseudorandom seed supplies reproducibility, not proof of that probabilistic assumption.

CAPABILITY AND OPERATION
All400 baseline rates are distinct: lambda_i=(399+2i)/798. An intact component fails at rate lambda_i*(400/(400-r))^2 after r failures. The target is COMPLETE failure by T=1/5, rather than20 initial failures.
An exact common-clock transformation represents the coupled failure time as the integral of squared empirical survival of independent exponential lifetimes. This makes a global convex-profile likelihood bound available. A compact geometric mixture of exponential lifetimes nearly matches the more elaborate variational profile and is simpler/faster, so this package uses it.
The representation and cap are proved in SURVIVAL_REPRESENTATION_AND_CAP.txt. Numerical implementation and its complete error ledger are in REPORT.md. The sampler does not use system logarithm/exponential routines; explicit polynomial kernels have all-input error bounds. Integer output statistics make the final confidence arithmetic independently reproducible.

EVIDENCE
- Exact change-of-clock and likelihood-cap derivations.
- Independent reconstruction of the cap, finite-mixture correction and numerical error budget.
- Small-state generator checks of the model and earlier proposal calculations.
- The final distinct-rate run, with explicit numerical/distributional bias <=7.2437543e-7 on the normalized scale.
- Exact rational reaggregation of the final interval from saved integer sufficient statistics.
These are internal scientific/computational checks, not external peer review, formal compiler verification or validation of a physical failure law.

WHAT COMPETITORS CHANGED
The original elaborate optimized profile was NOT the best practical construction for the two-rate test: a two-parameter geometric mixture achieved similar variance faster. A radial conditional-expectation extension further reduced measured variance, but its numerical quadrature has not been certified and is not used in the production result.
A naive exponential-rate tilt can miss extreme-survivor contributions and report a deceptively small probability. An analytic lower bound demonstrates its possible n-squared second-moment growth. This does not refute all established importance samplers.
The earlier two-rate example is exactly lumpable to40,401 count states and is only a validation/comparison case. The delivered preferred fixture has400 distinct rates; that particular count lumping is unavailable. This is not a proof that every competing deterministic method is expensive.

CLOSEST PRIOR AND UNRESOLVED COMPARISON
Common time changes, conditional Monte Carlo, exponential tilting, convex dominating-point methods, geometric mixtures and radial integration are established machinery. Historical novelty of this task-specific combination is unestablished.
Blanchet, Leder and Glynn's primary discussion of convex-set rare-event simulation is a relevant comparator:
https://web.stanford.edu/~glynn/papers/2009/BlanchetLederG09.html
A potentially decisive older method remains unresolved: Amari and Bergman (2008), DOI10.1109/RAMS.2008.4925836. Huang and Xu (2010) describe its reduction of load-sharing calculations to two-dimensional integrals:
https://www.cse.cuhk.edu.hk/~qxu/huang-tr10.pdf
The 2008 original equations were not obtained through the searched legitimate public routes. Its applicability, integrand cost and extreme-tail numerical precision have therefore NOT been verified. No claim of computational superiority over that method is made.

PHYSICAL CONSEQUENCE AND MISSING OPERATION
This supplies a practically reproducible calculation in a declared interacting model while paying numerical precision and complete-path costs. It does not establish the failure rates or load-sharing law of a real material. A recent carbon-fibre experiment inspected during this work actually reduces to a binomial model; its ordinary count law needs no new sampler, and an illustrative extreme tail changes by roughly25orders under a±1% fitted scale perturbation. Better model acquisition can matter far more than smaller Monte Carlo error.
The next decisive gates are a faithful comparison against the older load-sharing method, and a consequential physical system with measured interactions, an operational failure criterion and a quantified model-error budget. Do not translate the displayed model confidence interval into a physical safety claim.

REPRODUCE
Requirements: Python3 standard library and an existing C++17 compiler. No downloads or package installation are performed.
1. python verify_constants.py
2. python verify_results.py distinct_3000000_90273041.json
   These are quick deterministic checks of kernel constants and endpoint arithmetic.
3. g++ -O3 -std=c++17 -ffp-contract=off sampler.cpp -o sampler
4. python run.py distinct 3000000 90273041
   Replays the production-size calculation. Do not use fast-math, Python -O, or PYTHONOPTIMIZE. Compile-time/runtime arithmetic guards are part of the contract. A different platform is not automatically covered unless it satisfies the stated assumptions.
To rebuild exact preparation rather than use the supplied table, remove the local copies of distinct.in and distinct_prep.json and rerun step4. This modifies only extracted local files. Never change the arithmetic inputs without recomputing all bounds.

FILES
REPORT.md: complete numerical-error and confidence proof.
SURVIVAL_REPRESENTATION_AND_CAP.txt: mathematical operation and scope.
sampler.cpp / coefficients.h: compiled sampling kernel.
run.py / exact_intervals.py: exact preparation and aggregation.
verify_constants.py / verify_results.py: deterministic checks.
distinct.in / distinct_prep.json: reproducible prepared inputs.
distinct_3000000_90273041.json: exact sufficient statistics and endpoints.
BUILD.txt: original execution provenance. No binary is distributed.
SHA256.json: hashes for this source package.
