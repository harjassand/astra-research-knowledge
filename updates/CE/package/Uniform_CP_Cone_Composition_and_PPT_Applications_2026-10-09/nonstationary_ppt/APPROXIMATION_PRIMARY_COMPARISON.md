# Primary comparison for arbitrary-word approximation

Checked 9 October 2026. This is a targeted comparison, not an exhaustive novelty search or an independent proof review. No current-status claim about the PPT-square conjecture is inferred from an unofficial index.

## Precise candidate boundary

UNIFORM_APPROXIMATE_PPT_WORDS.md claims a deterministic, dimension-only diamond-norm approximation bound for every serial word of PPT channels, including arbitrary nonunital and nonstationary factors. It also preserves the exact input effect when extending the approximation to unnormalized CP words. It does not claim a common finite exact EB length for unrestricted words.

The tentative contribution is the quantitative synthesis: uniform determinant contraction, trace-nonincreasing low-rank Kraus truncation, backwards effect normalization without inverse-condition-number loss, and summing branch errors by their positive input effects before dimension induction. The determinant entanglement measure, its filtering law, and compression through low-rank Kraus operators are established ingredients.

## Closest inspected primary sources

1. **Kennedy, Manor and Paulsen**, *Compositions of PPT Maps*, arXiv:1710.08475v2, 7 December 2017; published as *Composition of PPT Maps*, Quantum Information and Computation 18 (2018), 472–480. Theorem 3.5 gives asymptotic EB for powers of one unital or trace-preserving PPT map. The proof uses the commuting limit idempotent of the cyclic semigroup. Its quantified statement is not uniform over arbitrary varying words. Primary full text: https://arxiv.org/html/1710.08475v2 .

2. **Tiersch, de Melo and Buchleitner**, *Entanglement evolution in finite dimensions*, arXiv:0804.0208v3, 25 October 2008; Physical Review Letters 101, 170502. Equations (5) and (6) give pure-input G-concurrence factorization and mixed-input upper bounds; the determinant filtering identity is explicit. The determinant Kraus weight in our Section 1 is the convex-roof ensemble expression for G-concurrence of the normalized Choi state. Vanishing G-concurrence alone detects a loss of maximal Schmidt number, not separability. Their Eq. (7) treats lower members of the concurrence hierarchy with an additional dimensional factor. We do not claim those ingredients as new. Primary full text: https://arxiv.org/html/0804.0208v3 .

3. **Christandl, Müller-Hermes and Wolf**, *When Do Composed Maps Become Entanglement Breaking?*, arXiv:1807.01266v2, 17 June 2019; Annales Henri Poincaré 20 (2019), 2295–2322. Theorem II.1 gives exact Schmidt-number iteration for arbitrary sequences of n-entanglement-breaking maps. Conjecture II.1 is precisely the assertion that every square PPT map has Choi Schmidt number at most d−1. Lemma II.2 compresses a PPT map between two low-rank Kraus maps, conditionally lowering Schmidt number if that conjecture holds. Corollary III.1 proves the arbitrary two-map qutrit result. These are close precursors to the separator step, but do not provide the present unconditional approximate replacement. Primary full text: https://arxiv.org/html/1807.01266v2 .

4. **Ekblad**, *A Multiplicative Ergodic Theorem for Bistochastic Ergodic Quantum Processes with Applications to Entanglement*, arXiv:2502.14997v2, 4 August 2025. Theorem 4 establishes almost-sure asymptotic EB under a positive probability of PPT factors in the bistochastic ergodic framework. Theorem 6 supplies a finite-time conclusion under additional hypotheses. This handles occasional PPT noise in a probabilistic setting, while our candidate requires every counted factor PPT and is deterministic, uniform, and nonunital. Neither assertion subsumes the other in full. Primary full text: https://arxiv.org/html/2502.14997v2 .

5. **Szczygielski and Chruściński**, *Eventually entanglement breaking divisible quantum dynamics*, arXiv:2407.16583v2, 16 November 2024. Theorems 2 and 8 impose commuting time-dependent generators, spectral decay, and a faithful stationary state. Theorem 9 concerns semigroups with a unique faithful stationary state. These continuous-time results do not supply a worst-case arbitrary discrete PPT-word bound. Primary full text: https://arxiv.org/html/2407.16583v2 .

## The exact rank-(d−1) question

The primary claim needed to replace approximation by exact rank loss is

 PPT(M_d) subset SP_(d−1)(M_d).

CMHW explicitly formulate it as Conjecture II.1. Targeted current primary searches did not locate a general resolution, so this investigation treats it as unavailable rather than assuming it. The known qutrit result and special partial-transpose-invariant classes are insufficient for arbitrary dimension.

**Johnston and Lovitz**, *PPT states of almost maximal Schmidt number*, arXiv:2609.11849v1, 10 September 2026, construct square PPT states of Schmidt number at least d−floor(sqrt(2d−1)); the rectangular construction reaches at least n−1 on n by (3n−4) systems. These are lower bounds, not the upper bound required here. They do not justify an exact singular-Kraus decomposition for every square PPT map. Primary full text: https://arxiv.org/html/2609.11849v1 .

**Park**, *Every PPT channel has finite entanglement breaking index*, arXiv:2608.13551v2, gives SP_(d−1) under an additional singular Perron support condition (Theorem 3.8). That conditional rank loss is different from an all-PPT inclusion. Primary full text: https://arxiv.org/html/2608.13551v2 .

## Search and certainty limits

Searches explicitly included asymptotic PPT-square results, arbitrary products/sequences, Schmidt-number iteration and G-concurrence contraction. The sources above were inspected at the identified statements, not inferred solely from snippets. No external contact or publication occurred. Failure to find a matching theorem is not a proof of originality; the new result remains an internally derived, unreviewed proof candidate.

## Stronger qubit-concurrence route

The subsequent EXPONENTIAL_APPROXIMATE_PPT_WORDS.md replaces dimension-recursive truncation by contraction of qubit-ancilla concurrence, a semialgebraic error bound to the 2-EB channel set, and the already-cited CMHW iteration theorem. It yields ordinary exponential approximation and applies even to CP channels that are 2-copositive. This broader scope concerns serial composition only.

An additional close structural precursor is **Li, Zhao, Fei, Fan and Liu**, *Mixed maximally entangled states*, arXiv:0906.5445v2, 26 February 2012; Quantum Information and Computation 12 (2012), 63–73. Theorem 1 and its subsequent discussion identify maximal-entanglement mixed states with a maximally entangled pair tensored with an output flag, up to a local isometry, and explicitly include convex-roof concurrence. The new derivation retains a short polarization proof of the needed special case. That range structure and the concurrence filtering law are not claimed as discoveries. Primary full text: https://arxiv.org/html/0906.5445v2 .

The tentative contribution in this stronger route is the uniform concurrence contraction for the entire PPT-output class, converted into a quantitative channel approximation through the compact semialgebraic 2-EB set. The targeted searches did not verify this complete arbitrary-word theorem in the inspected primary sources. This remains a limited comparison, not a priority certification.

## Preferred explicit rate

EXPLICIT_EB_NOISE_REPAIR.md is now the preferred quantitative route. It replaces the semialgebraic repair by an elementary rectangular separable ball and depolarizing admixture on the embedded Bell test states. GAUSSIAN_PPT_CONCURRENCE_GAP.md proves the explicit conservative deficit 1/(8d), with PAIR_ROTATION_CONCURRENCE_GAP.md preserving a separate 1/(4d^2) finite-ensemble argument. These use standard Pauli, reduction-map, ensemble and Gaussian moment identities. No sharpness or independent novelty claim is made for the numerical concurrence bound. The complete rate/repair synthesis remains the candidate research contribution under the limited primary comparison above.
