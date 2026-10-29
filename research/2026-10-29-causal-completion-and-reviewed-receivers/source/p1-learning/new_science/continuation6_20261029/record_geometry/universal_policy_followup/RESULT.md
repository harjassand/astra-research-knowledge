# Focused result: universal policy experiments and learning cost

Date: 2026-10-29. Existing Astra P1 / record_geometry. No new agents or transfers.

## Decision-relevant findings

The universal-coding to polynomial-horizon policy-evaluation bridge is a direct predecessor. Peshkin–Mukherjee COLT 2001 §5.2 explicitly supplies the chain; Peshkin's dissertation §6.5 states the constructive optimal-sampler qualification. Cover–Ordentlich 1996 already supplies the fixed-context Dirichlet-half bound. Ordentlich–Cover 1998 supplies the fixed-horizon domination optimum and its multinomial Fisher-volume asymptotic. See `PREDECESSOR_AUDIT.md` for inspected sources and qualifications.

The companion `ORDINARY_UNIFORM_POLICY_LEARNING.md` proves an explicit simultaneous confidence theorem for all row-simplex policies, including zero action probabilities. Its elementary floor/ceiling grid gives

\[
\sup_{q,j}|\widehat V_j(q)-V_j(q)|
\le3HA/M+2\left(\sqrt{2B\ell/N}+2B\ell/(3N)\right),
\]

when `HA/M <= 1/4`, with explicit grid entropy and `B = 2^S(1+H/S)^(S(A-1)/2)`. It assumes actual independent episodes with a common warranted deployment start. The data-selected near-maximizer loses at most twice this radius plus optimization error. This is a conventional constructive receiver, not a new generic mechanism.

Uniform episode mixing over deterministic fixed-context policies gives domination `A^S`, independent of horizon. A half-atomic/half-KT mixture keeps both this stronger deterministic comparator and continuous randomized coverage, each within a factor of two.

`PHYSICAL_INTERFACE_FAILURES.md` preserves exact failures for literal private keys, action-selection latency, frozen nominal repetition, arbitrary invented tasks, and overbroad interpretations of the geometric cost.

## Actual root-proof review

The core matching adaptive-learning lower bound passed review: count packing, `3/4` concentration, `5/8` identification, null-to-alternative KL, adaptive cancellation and all displayed constants are sound. Root corrected the two requested theorem quantifiers and the episode-count wording.

Accepted proof SHA256:

`6b69fb5008a9a4716cbe8cbb8ebbf6a5a1726986a696bf3a604d58a158cfe64e`.

The actual review, original snapshot, accepted snapshot and final receipt are preserved here. The receipt accepts Sections 3–7 at the stated physical-start, randomness, task and record interfaces. It does not certify the separately reported learner executable, which was outside the scoped review.

The learning lower bound is logically stronger than a domination lower bound because it permits arbitrary adaptive calibration and concerns a useful selected policy. Its historical priority remains unresolved. Fisher-volume domination and the finite-armed change-of-measure technique are established ingredients.

No new numerical fixture was needed for these analytical proofs and exact counterexamples. The completed LTI unit in the parent directory was left unchanged. No apparatus data, practical speedup or major-discovery claim is made.
