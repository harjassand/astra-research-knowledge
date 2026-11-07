# N33 spatial continuation checkpoint — 2026-10-21

**Status:** additive research on draft PR #111, not canonical claim or gate status. All original N33/N54/N142/N173 records and their reviews remain unmodified. Formal Lean checks, external peer review, physical lab validation and historical originality for new statements are **not** claimed. The original theorem is externally overlapped by Mislan's 2026-10-09 registered proof; do not re-claim it as a fresh broad breakthrough.

## Inputs and pinned proof dependencies

Astra main source head at branch creation: 65633ec33f253deb1e8e01dd47fa91803c1916ac.
N33 original at web/pages/d-326696af15b5e02b.html (reported hash bbecea61cd373a787920bb4484494114b7d616d5f20ee096cae3831487707e9c): strict active-slope weighted drift lines 396–518; compact positive plateau lines 519–571; a.e. invariance/absorption 573–737; deterministic common scalar diffusion 858–918; conditional molecular exponential-martingale appendix 1159–1310. Original source149 pinned adc7f1241b42e322a6451854ab7e4b4c146bf78a. Independent registered comparator mmislan/palomar-endotactic-permanence pinned c72c945264565397ecc3eee779e6bd5f3f3a061d, 9 Oct 2026.

## New scope and completed findings

- S1: explicit all-compartment first-exit bound for six-channel ordinary-endotactic synthetic reaction system (network and deterministic operating region **attributed to Mislan**), real integer-complex falling-factorial molecular propensity, per-channel predictable rates in [1/2,2], and completely distinct predictable specieswise balanced directed migration graphs with in/out budget <=1/4 per species/site, any finite n, V>=100:
  P(exit Q^n by T) <= 6n exp(-V/20) + (2205/44)n V T exp(-V/480), where Q=[2/5,5/2]^3, initial per-site counts=(V,V,V).
  The exact inequality is based on six local face exponentials, rational lower generator margins 57/55000, 125127/440000 and 67976607/88000000, exp(1/12)<=12/11 and local affected-hazard budget 735/8. Detailed analytic proof in SPATIAL_STOCHASTIC_EXTENSION.md. At n=100,V=30000,T=exp(V/960): probability <=4.030645587585597e-6; dimensionless time.
- S2: conditional on N33's original all-dimensional permanence theorem, its **full-span** integer-complex plateau provides uniform strict inward facet collars; if species migration is balanced and compatible with each facet normal (species appearing in a given normal share coefficients), a product polytope has exponential-in-V predictable-control safety uniform in n except multiplicative n. No finite-bit polynomial synthesis is claimed.
- S3: for two-site diffusion-only and **every** independently selected diagonal diffusion matrix, invariance of a full-dimensional bounded convex polytope Q×Q is equivalent to Q being an axis-aligned box. The proof uses opposite tangent perturbations at each facet. This substantiates why generic N33 oblique plateaux cannot automatically transfer to arbitrary unequal diffusion. A concrete two-species oblique-facet counterexample is recorded.
- Conditional finite bounded-graph perturbation: small total species mobility mismatch is absorbed by strict reaction drift, with threshold proportional to facet margin divided by sum |normal|*coordinate width. No PDE/mesh-uniform result due diffusion row budgets increasing under refinement.
- Applied caveat: no measured chemical rate box, microscopic physical parameterization, feed/energy balance or device advantage. Stochastic confinement for a stopped process is NOT stochastic recurrence or global stationary behavior.

## New independent research artifacts

- SPATIAL_STOCHASTIC_EXTENSION.md (proof text, assumptions, comparator/attribution, failure cases).
- verify_spatial_safety.py (Python standard-library Fraction assertions of the six-reaction stoichiometry, all generator margins, hazard and numerical example).
- spatial_reproduction.json (saved sufficient inequality values).
Earlier REPORT.md, CHECKPOINT.md and verify_metastability.py remain untouched.

## Reproduce now

Run \`python3 research/2026-10-21-n33-controlled-metastability/verify_spatial_safety.py\`. The printed exact rational values should match spatial_reproduction.json. Python arithmetic checks are *not* a formal proof of the stopped compensator, distinct from the handwritten analytic derivation. Verification read depth: original N33 full named proof sections and reviews; Mislan paper/Lean top-level statements; primary literature on reaction-diffusion invariant regions and jump large deviations; no full historical prior-art exhaustivity, no independent Lean replay.

## Precise next mathematical step

Independently prove and mechanize the S1 stopped compensator on the full simultaneous two-compartment jumps under **adapted predictable** coefficients, paying special attention to exit overshoot and local-vs-global total hazard. A falsifier would be one allowed initial configuration/rate/migration rule where any of the six rational collar inequalities fails or an exit event violates Phi(exit)>=1. Then audit S2 with an actual non-rectangular full-span N33 polytope and a non-scalar facet-compatible migration to see if the hypothesis is nontrivial. Finally compare S1 against best known stochastic spatial Lyapunov/large-deviation results under the same control and graph parameters; seek a credible real biochemical reaction/transport model and account for maintaining minimum rates for the enormous nominal horizon.

No ongoing asynchronous research or completion is implied. No old proof, checkpoint, claim, gate or branch is overwritten.
