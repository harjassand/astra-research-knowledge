# Source map and closest meaningful literature

## Exact owned input and continuity

The attached complete collection was read locally, not treated as a shared
historical path. Its bytes and embedded owner member were verified:

| Input | Bytes | SHA256 |
|---|---:|---|
| Astra_Continuous_Cycle_0002_Six_Complete_Returns_20261022.zip | 52206289 | e98bf6a762ff302b2a4b38668a22f0f83e6a3748b83c3b3b26228a33373aeb76 |
| Astra_Amplification_Cycle4_PRO3_20261022.zip | 2047579 | 8639b0ce63d7cc0dfb91f7c08d09d26380533057f5e3c9059b083264120fbb5b |

The latter is unchanged under sources/ and matches the latest owner-local
archive. The new proof's matching lower is its CRITICAL_WINDOW_LOWER.md,
6,991 bytes, SHA256 1f0e0a6da68b6447455c870d49e6d544a75d30cc6a1ee1dba8e6c4746c55d7f0.
Its complete native construction is BRANCHING_SHARPNESS.md, 18,093 bytes,
SHA256 119dfb8d0b8e77b3ce93fdef1f1450c01fc1d090a0f05c4dd7ae0ea7ada1d645.
Copies of those two dependencies and their accepted source-bound reviews are
available under sources/selected_cycle4/ for immediate reading; the original
ZIP remains authoritative and complete.

## Primary literature inspected in this continuation

1. Banterle, Grazian, Lee and Robert, *Accelerating Metropolis-Hastings
   algorithms by Delayed Acceptance*, arXiv:1503.00996v2, Sections 2.1-2.3,
   especially Lemma 2. https://arxiv.org/html/1503.00996v2
   This supplies the established reciprocal-factor reversibility framework
   and distinguishes lower acceptance from lower computational cost. The
   local operation here is not claimed as a new sampler primitive.
2. Andrieu, Lee, Power and Wang, *Comparison of Markov chains via weak
   Poincare inequalities with application to pseudo-marginal MCMC*, Annals
   of Statistics 50 (2022), 3592-3618, DOI 10.1214/22-AOS2241. Author-hosted
   primary full text: https://awllee.github.io/papers/AOS2241.pdf
   Section 2.3, Lemma 25 gives the independence-MH Dirichlet representation;
   Proposition 27 relates convergence to weight tails through a weak Poincare
   inequality. This is the closest inspected functional-inequality background
   to the anchor. It does not by itself supply the absorbed first-hit,
   proposal-start, shrinking-screen critical-amplitude calculation above.
3. Sherlock and Lee, *Variance bounding of delayed-acceptance kernels*,
   arXiv:1706.02142v4. https://arxiv.org/abs/1706.02142v4
   Its abstract and declared scope distinguish variance-bounding inheritance
   and computing-time savings from an iteration-count improvement. These
   notions must not be substituted for the present TV minimax question.

The first two relevant full-text passages and the third abstract/scope were
reopened in this allocation. A bounded targeted search also checked nearby
delayed-acceptance/KL/mixing and hitting-time/weighted-norm terms. It is not
an exhaustive historical-priority review. No absence of a matching search
result is asserted as novelty evidence. The new critical proof is self-contained
apart from the preserved matching lower; no web-derived numerical input is
needed to reproduce it.

## Current claims and reuse

The internally new reusable operation is the finite absorbed-boundary energy
bound, with explicit proposal-mass and information accounting. The unchanged
incoming upper was a genuine dependency of Cycle4's first-order theorem.
Cycle5 inherits that scientific state and uses its native lower, while giving
a new endpoint upper. This is cumulative mathematical use. It does not show
that an evaluator instrument, prompt tactic, agent count or fresh reset caused
the result. Historical originality, external acceptance, efficient realization
and physical usefulness remain separate claims.
