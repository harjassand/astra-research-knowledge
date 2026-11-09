# Mathematical review and source bindings

9 November 2026

This is a reader-facing summary of completed independent analytic reviews. It records what was checked and the limits of those checks. It is not a software validation, a benchmark, an exhaustive priority search or an independent reproof of every cited published theorem. The package's proof exports and cross-references were prepared afterward; their integrity is recorded separately in the manifest.

## 1. Original categorical factory

Reviewed mathematical source: `proofs/PROOF.md`.

SHA256: `851453442a734b44a033acb90079e1ad5e101718f9ed32dd15c7c25d483b7439`.

The review reconstructed the gambler's-ruin hitting probabilities, zero-atom and L=1 cases, shared-mass identity, complete joint kernel, residual-race normalization and exact expected query bill. It checked the fact that residual duration and acceptance may correlate: the first-step renewal equation, rather than an independence assumption, supplies the cost formula. Separate expected P/Q query counts and fair-bit charges were also checked.

The following qualifications are mandatory and are incorporated in the package's contract and cost discussion:

- Exact Q is marginal, not independence of Y from the observed X.
- An external conditional history is allowed only when the fixed-source/input and future-independence contract holds after conditioning.
- A retained response requires independence of fresh coupling randomness from that response conditional on X. Noninspection alone is insufficient.
- Exact work crossovers need actual conditional source means. Mere upper bounds give only appropriately formulated sufficient comparisons.

Underlying review binding: SHA256 `42d31c8879b86d29e5298d9ec41c43cb16750baba9a95c16bb26eb09de790d8b`.

## 2. Fixed allocations and hard caps

Reviewed mathematical source: `proofs/FIXED_ALLOCATION_COMPARISON.md`.

SHA256: `72dfb95629318508ef0df258e3d717c923e9c5876ac03e2c47783a39e1036a0e`.

The fourth-moment calculation, interpolation inequality, both regimes of kt, and exact integer consequence at d=16, eta=.01 were checked. The fixed-batch premise is inherited from N1691 and reproduced in `proofs/EMPIRICAL_BATCH_CONVERSE.md` for accessibility. That reproduction is an exposition of the reviewed premise, not a separate new theorem or a claim of new export-specific review.

The deterministic global-cap extension was derived independently: pre-generating M records from each source simulates any adaptive algorithm capped at M new calls, reducing it to a fixed per-source batch with r=M+1 and s=M. This gives the stated Omega(d/eta^2) cap requirement, not an expected-call lower bound.

Fixed-allocation review binding: SHA256 `653ed95c0df9938a3b3ec959b5d22eee2f654b17b7a51c9c91ca6fe820c39e9b`.

## 3. Preferred local-cap repair

Reviewed mathematical source: `proofs/LOCAL_CAP_EXTENSION.md`.

SHA256: `30beee05800d4d7abfd4e5f3973edfe92226b6cf59b580381506bb6d68c8a88a`.

The review checked all six main steps:

1. LOWER takes precedence if the Kth query hits that boundary; an interior timeout returns UPPER.
2. Every permitted LOWER path has one more down move than up move. Multiplying its weight by the initial p makes it symmetric in p,q, retaining an exact common submass in both factory orientations.
3. Lost common mass is bounded in both orientations by the original duration, giving the additional slack at most d(L-1)/K.
4. Local durations are truncated original durations. The complete residual normalization cancels in the mean bill, giving E N<=C.
5. The deterministic local cap supplies a distribution-uniform bound D on remaining expected calls from every internal state. Conditional Markov iteration gives the broad exponential tail.
6. Nonnegative summation of remaining expectations gives E[N(N+1)]/2<=D E N. This proves finite second moment rather than assuming it.

The fair-bit, counter-memory and integer-operation ledger was checked. The numerical formulas for d=16, eta=.01 were recounted analytically. No sampler or timing was run.

Disposition: the theorem passes at its stated exact-oracle scope. Its outer retries remain unbounded. The review does not give a mean-scale tail, a global hard cap, a wall-time guarantee for arbitrarily slow oracles, or a practical advantage.

Local-cap review binding: SHA256 `25e154477ee5a8778004419f4f29a5ba906e80592500ceb1bf7814e00122df9f`.

## 4. Binary second-moment obstruction

The independent argument is reproduced in `proofs/HARD_CAP_AND_MOMENT_LOWER_BOUNDS.md`.

For P=Bernoulli(1/2), Q_theta=Bernoulli(1/2+theta), exactness implies the stopped score identity 1=E(FS), with F=Y-X. An exponential moment justifies differentiation of stopped likelihoods. The fourth-moment bound E S^4<=2048 E N_Q^2 and Holder's inequality yield

    E N_Q^2 >= 1/(2048 eta^3).

This is a self-contained analytic argument, not an imported assertion of regularity for every finite-mean stopping rule. It applies to the preferred exponential-tail construction. The inverse-eta exponent matches for fixed d, but no optimal dimension factor, constant or complete tail distribution is established.

The same review checked the optional geometrically killed factory. It is not necessary for the preferred local-cap theorem.

Source review binding for these arguments: SHA256 `764f36db371d99dc3812201d798a2cdb9ecaab4a7bedab06d51b852d66ded837`.

## 5. Tolerant-testing expected-cost lower bound

Reviewed mathematical source: `proofs/TOLERANT_TESTING_LOWER_BOUND.md`.

SHA256: `f0ce8ff5efdfdeaec656c02508e18ce658c6f91d638997d1def9eae7ea43682a`.

The review directly checked the published Theorem 7 and Corollary 8 of Canonne, Jain, Kamath and Li (COLT 2022), and the corresponding arXiv statements. The formal norm is L1, so thresholds 2eta and 8eta are correct. No extra threshold-ratio restriction from the paper's upper-bound theorem is required for this lower-bound import.

It checked independent repetitions, both Chernoff exponents, the fresh-X +1 charge, conservative accounting of known-uniform source calls, and the Markov cap. The cap applies only to an approximate decision procedure, not to the exact sampler. No independence between runtime and disagreement outcomes is needed.

Disposition: the reduction passes with

    C(d,eta)+1 = Omega(d/[eta log d]+sqrt(d)/eta).

This is worst-case and asymptotic, for eta below an unspecified absolute constant. It permits adaptive allocation and unbounded stopping and assumes only a finite uniform mean. It is not a finite numerical bound at d=16, eta=.01, an equal-uniform instance bound, or a proof that the logarithmic gap is necessary.

Tolerant-testing review binding: SHA256 `977cc066b907acade3dba563e1b161462a6090c78d408616ace235a5208bb3d5`.

## 6. Prior and application scope

Primary checks support the access-model distinctions stated in the prior note: ordinary maximal coupling can evaluate probabilities; coupled rejection sampling uses dominating proposals and acceptance ratios; general dice enterprises do not by themselves supply the particular uniform cost cancellation; and exact black-box attribute alignment has a supplied target and a different retention objective.

These checks did not establish historical novelty. The operation is a quantitative extension assembled from established ingredients, not a new general sampling paradigm. No real application has been acquired or benchmarked. Known probabilities, common randomness, deterministic memoization, cheaper expectation-only estimators and direct categorical draws remain essential competitors.

A separate focused prior/application investigation checked the Jiang attribute-alignment interface and the Bernoulli-race particle-filter example. It found no inspected primary that directly supplies the complete retained-sample contract with these cost and latency bounds. It did not conclude that the result is historically first. Its recommendation was to preserve the restricted theory result while withholding practical-benefit claims. Source binding: SHA256 `d2341b5dbb3faa6f78df66af9fe28321407591d3b86e5a791dc1bbe8d0108e9d`.

## 7. What the package checks establish

The archive's manifest verifies the delivered bytes. The frozen mathematical source copies retain their reviewed SHA256 values. Exported proofs and summaries are identified in `PROVENANCE.json`. Hash validation is not proof verification. No empirical tests, software correctness claim, timing comparison or source-oracle certification is included.
