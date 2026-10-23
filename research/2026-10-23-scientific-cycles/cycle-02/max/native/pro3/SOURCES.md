# Primary sources and attribution boundary

The new universal arguments are fully written in PREFIX_THEOREM.md.
Numerical diagnostics supplement those proofs. The unchanged previous
owner archive and the accepted mixing trial source are included in sources/.
The exact input packet identity is recorded in INPUT_RECEIPT.json.

## Closest existing mathematical machinery

1. Alexey Kurennoy, Ramil Yarullin and Fergal Reid,
   *Metropolis–Hastings Dominates Importance Resampling for Policy
   Composition*, arXiv:2610.03480v1 (2 October 2026).
   https://arxiv.org/html/2610.03480v1
   Equation (21) gives the exact proposal-start IMH marginal density;
   the priority representation and finite-support convex-divergence
   comparison with ordinary SIR are established results. Theorem 6 is
   a related obstruction to certifying remaining error from a fixed
   proposal pool. It does not directly give this archive's certified-KL,
   post-prefix hybrid threshold. No new sampler or priority law is claimed.

2. Seiyun Shin, Juhyeong Pang and Kwang-Sung Jun,
   *Uniform Race: Parameter-Free Approximate Rejection Sampling*,
   arXiv:2609.34639v1 (28 September 2026).
   https://arxiv.org/abs/2609.34639v1
   The general-measure threshold-mixture representation is relevant to
   regularizing the initial law. Our first-high-candidate proof instead
   establishes the required tail bound directly for IMH, without an
   unspoken finite-support or disintegration assumption.

3. Adam Block and Yury Polyanskiy,
   *The Sample Complexity of Approximate Rejection Sampling with
   Applications to Smoothed Online Learning*, COLT 2023; corrected
   arXiv:2302.04658v3 (23 February 2024).
   https://arxiv.org/html/2302.04658v3
   The entropy-controlled exponential accuracy scale for selecting
   proposal samples is prior art. The old proceedings tail statement
   must not be used without its correction. This work proves the exact
   tail inequalities it needs and retains pure IMH as the comparator.

4. Christophe Andrieu, Anthony Lee, Sam Power and Andi Q. Wang,
   *Comparison of Markov chains via weak Poincare inequalities with
   application to pseudo-marginal MCMC*, arXiv:2112.05605v2;
   Annals of Statistics 50(6), 3592–3618 (2022).
   https://arxiv.org/abs/2112.05605v2
   Weak-Poincare and Dirichlet comparison techniques, including
   independence-MH examples, are established. The present analysis
   controls bounded observables and the initial low-weight mass; a
   stationary form comparison alone does not establish its result.

## What was actually checked

The principal reopened the four primary sources online, inspected the
exact marginal formula, the IMH/SIR theorem and the certification
obstruction, and read the literature contributor's source notes.
Preserved public PDF identities and the contributor's focused searches
are recorded in reviews/prefix_literature_sources.json and
reviews/prefix_literature.md. Full third-party PDFs are not required to
run any code or check the self-contained proof; their exact original URLs
and versions are provided.

The bounded search found no source stating precisely the new error-floor
formula or its prefix threshold. That is insufficient to establish
historical novelty. The result is described as an internally checked
sharp robustness theorem for composing standard samplers.

The already completed application and empirical decisions are inherited
unaltered from the exact original owner source, not reinterpreted as
adoption or computational benefit.
