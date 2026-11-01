# Narrow automata / semigroup / kernel-operator extension

1 November 2026. Extends FINDINGS.md; no change to its limited novelty status.

## Result

No actual dominator was located in this narrower primary-source pass. In particular, polynomial-query automata titles must not be read as polynomial, gap-free noisy Gram-query results. The exact-to-noisy gap is material. This is a useful negative result, not exhaustive priority clearance.

## Quantum finite automata: exact full amplitude oracle

Daowen Qiu, *Learning Quantum Finite Automata with Queries*, arXiv:2111.14041v2, November 12, 2023 (journal MSCS 34(2), 2024). Section 3 defines AD as returning **all amplitudes** of the state after a word, and supplies Q and its accepting/rejecting partition. Its basis-expansion algorithm learns an equivalent MO-1QFA; the MM-1QFA counterpart also uses exact amplitude vectors. Proposition 7 gives O(n^5 |Sigma|) computational complexity for the latter. Section 5 leaves polynomial learning from a weaker oracle open. These are not scalar overlap experiments and do not establish the candidate's finite-noise no-gap claim. Conversely, the candidate does not solve exact QFA identification: finite-horizon approximate readouts and task-fed service are weaker output contracts.

Primary full version: https://arxiv.org/html/2111.14041v2 , sections 3–5; especially lines 197–216, 541–560.

## Weighted automata: exact membership plus equivalence; local noisy sensitivity

Balle and Mohri, *Learning Weighted Automata*, CAI 2015, author-hosted full manuscript. Section 4.1 learns a rank-n weighted automaton using exact value membership queries and an equivalence oracle returning counterexample strings. Counterexamples enlarge a Hankel basis. Section 3.6's noisy reconstruction, Theorem 5, gives parameter error O(epsilon) as epsilon tends to zero for a fixed complete basis and correct rank. Its formula uses inverse retained singular values. The statement is not a uniform polynomial tolerance guarantee independent of the Hankel gap. Thus neither its exact query learner nor its noisy reconstruction already proves the candidate's contract.

https://cs.nyu.edu/~mohri/pub/cai.pdf , sections 3.6 and 4.1, pp. 10–14.

## Probabilistic automata: distinguishability is a charged parameter

Balle, Castro, Gavaldà, *Learning Probabilistic Automata: A Study in State Distinguishability*, author-hosted manuscript dated October 20, 2011; published TCS 473 (2013), 46–60. The paper studies PDFA distribution learning and statistical/L-infinity queries. It establishes a distinguishability-dependent obstruction for its query class and develops an adaptive learner with the corresponding complexity dependence. It is not a Gram-return lower bound or a no-gap Gram-return compiler. Its negative result must not be transferred to the stronger pair-return interface, and its positive learner must not be treated as rank-only complexity.

https://borjaballe.github.io/papers/tcs13.pdf , abstract and sections 2–3.

Tzeng's 1992 state-distribution learning is described in Qiu's primary text as returning state distributions. The original Tzeng paper was not fetched in this pass; no original-theorem inspection is claimed. A state-distribution oracle is not S0.

## Kernel operators: sharp finite-sample rates still have source/regularity/gap conditions

Kostić, Lounici, Novelli, Pontil, *Sharp Spectral Rates for Koopman Operator Learning*, NeurIPS 2023, proceedings PDF. Theorem 2 requires singular-value separation at the truncation rank, regularity RC and spectral decay SD, for observed transition-pair data in a chosen RKHS. Page 6 explicitly identifies separation-dependent constants in sample complexity. Theorem 3 adds compact self-adjoint structure for spectra. This is genuine strong operator-learning theory, not a hidden scalar-return feature-discovery theorem. Its finite-rank minimax statements should not be paraphrased as uniform no-Gram-gap operation acquisition from S0.

https://papers.nips.cc/paper/2023/file/663bce02a0050c4a11f1eb8a7f1429d3-Paper-Conference.pdf , sections 2 and 5, Theorems 2–3.

## Own mathematical comparison: what S0 changes

For self-adjoint primitives, Gamma(u,v) equals a terminal seed-return value on an appropriate chronological reversed/concatenated word. Therefore S0 is not intrinsically unrelated to membership-style queries: the crucial distinction is the known adjoint/contraction structure and positive Gram geometry, not merely the name of the oracle. General terminal-output membership does not supply this structure, nor does a squared overlap reveal a signed real overlap.

With exact Gram entries and exact arithmetic, ordinary closure/BFS can discover an invariant word span, solve action coordinates, and stop after at most rank-many independent features. This is conventional realization machinery and already acknowledged by N1515's exact baseline. Its finite-noise implementation can inherit arbitrarily poor conditioning. Candidate credit, if earned, belongs to the robust approximate finite-horizon stability/acquisition join, NOT to existence of a small exact operator representation or exact rank discovery.

Known-core spectral learning can already predict unseen words without fresh source calls. Online kernel prediction can already avoid explicit hidden coordinates. Neither statement separately yields the combined guarantee. A fair prior extension may combine them, but it must prove the same noisy geometry and pay the same scalar experiments rather than assume precisely the desired representation.

## Decision and stopping boundary

Current evidence supports continuing the finite-noise theorem audit rather than parking based on an identified prior theorem. It does not support a priority claim or civilization-changing claim. Retain the distinction between online finite lifetime acquisition and an upfront finished compiler. Finish construction, then assess a consequential source whose preparation and shot costs make the theorem enabling; polynomial notation alone remains inadequate.

## Access ledger

All four primary full-text targets listed above opened successfully. No new access failure occurred in this extension. No denied IEEE, Binev, Laurence–Robert, or prior stopped arXiv work was retried or retrieved elsewhere. Search snippets not promoted to uninspected theorem evidence. No benchmark, external mutation, or outreach performed.
