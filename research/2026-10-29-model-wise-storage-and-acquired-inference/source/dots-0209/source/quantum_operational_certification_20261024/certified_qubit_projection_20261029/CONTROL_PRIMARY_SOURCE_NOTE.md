# Conventional control machinery: primary-source attribution

Checked2026-10-29. Barenco et al., *Elementary gates for quantum computation*, Physical Review A52,3457 (1995), [arXiv:quant-ph/9503016](https://arxiv.org/abs/quant-ph/9503016), [DOI10.1103/PhysRevA.52.3457](https://doi.org/10.1103/PhysRevA.52.3457).

Relevant governing source locations: Lemma5.1 and Corollary5.3 for single-controlled one-qubit gates; Lemma6.1 for a doubly controlled gate via a square root V; Section6.1 for simplifying the resulting local circuit. The paper also emphasizes that gate universality does not solve physical coherence/error-correction requirements.

Our circuit programs execute this conventional decomposition, with rational-unitary rounding and exact instance-specific residual checks. They do not originate those decompositions. The quoted894-gate thin circuit is not an optimized synthesis bound: merging adjacent single-qubit factors and other standard simplifications can reduce it. Counts are for the actually emitted circuit, not a claimed fundamental lower bound or a comparison establishing a new advantage.
