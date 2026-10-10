# Strong structured-constraint sampling

This package preserves one complete pasted research report as one unit. It is not split into separate frontier cards, and no claim-ledger status or existing mathematical result was changed.

## Reported result

For binary targets

`mu(x) proportional to nu_h(x) exp(0.5 x^T K x)`,

the report gives an entropy-contraction argument for a Gaussian auxiliary-variable sampler when the linearly tilted constrained base `nu_a` satisfies a uniform covariance bound. For the two described classes it claims `Cov_{nu_a}(X) <= 2 I`, yielding the sufficient condition `||K||_op < 1/2`, independently of the strength of constraints already absorbed into `nu`.

The two classes are (1) laminar families of log-concave count weights with interval support, including arbitrarily strong quadratic count penalties and feasible exact quotas, and (2) weighted matroid bases, including spanning trees, using primal and dual matroid covariance bounds. The source also describes a reduction for a weak residual negative quadratic penalty and provides an explicit initialization and finite-round total-variation bound for the ideal kernel.

The source reports implementation and finite-model diagnostics, including 256- and 1,024-variable nested constraints and an 8-by-8 grid spanning-tree case. These are source-reported results only. Benchmark comparisons are mixed; the source explicitly does not claim universal sampler superiority. The general matroid reduction is not reported as implemented. No historic-scale breakthrough, external correctness review, priority clearance, certified floating-point implementation, or uniform runtime guarantee for the numerical implementation is established.

## Evidence and provenance

- [`RESEARCH_REPORT.md`](RESEARCH_REPORT.md) is the exact 482-line pasted attachment, copied without editing.
- [`SOURCE_MANIFEST.json`](SOURCE_MANIFEST.json) records its original path, size, line count, SHA-256, and the status of the other referenced artifacts.
- The report points to `01_stronger_regimes_proof.md`, `02_evidence_and_limits.md`, and `astra_stronger_regimes_handoff_2026-10-11.zip` under `sandbox:/mnt/data/astra_quadratic_continuation/`. Those files were not present in the accessible Downloads, Codex workspace, attachment, or `/mnt/data` searches at intake. They have not been reconstructed or replaced. The preserved report itself contains the theorem statements, proof narrative, limitations, and benchmark summaries, but does not substitute for the separately linked full artifacts.
- No source code or benchmark scripts were included in the available attachment. No scientific computation or replay was run during this intake.

## Exact task interface and boundaries

The central target is a binary distribution tilted by a positive-semidefinite quadratic interaction `K=B^T B` over a tractable constrained base. The sampler alternates `Y | X=x ~ N(Bx,I)` with a full constrained-base sample `X' | Y=y ~ nu_{h+B^T y}`. The contraction premise must hold uniformly over every field used by this update. The stated `1/2` threshold is a sufficient condition for the specified covariance bound, not a lower bound for other algorithms or a claim about arbitrary overlapping hard constraints.

The source supplies these important limits and counterexamples:

- Arbitrary overlapping strong constraints are outside the laminar result; a three-variable overlapping example has covariance eigenvalue `3`, defeating the proposed uniform `2I` covariance mechanism.
- The Gaussian-convexity argument breaks at residual norm `1/2` in a hard-pair construction; this delimits the proof mechanism, not all samplers.
- The report's comparisons show the Gaussian/core sampler is useful under strong constraints but does not dominate the stronger constraint-preserving baselines in every regime.
- The matroid covariance argument imports established matroid log-concavity results; the generic matroid computation is a reduction, while the spanning-tree specialization is the reported implementation.
- Floating-point code is not certified to meet the ideal-kernel total-variation bound. Source-reported exhaustive checks and finite-kernel audits are not independent proof certification.

Read the report as source evidence. Its claims of complete internal derivations, benchmarks, and checks are not upgraded by this intake. Historical originality remains unresolved, including the precise distinction from the cited single-total-count-penalty result.
