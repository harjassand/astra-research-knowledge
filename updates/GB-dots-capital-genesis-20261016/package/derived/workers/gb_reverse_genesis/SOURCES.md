# Sources, exact scope, and priority boundary

All source copies are immutable inputs to this worker. Their byte hashes and original paths/URLs are in sources/SOURCE_MANIFEST.json. This file records what was read and used; source availability is not correctness or priority evidence. No other worker's files were read.

## Supplied proofs actually used

1. `sources/local/packet_CQ_THEOREM.md`, lines 5-19, 21-118 and 165-171: faithful CQ radius, weighted-Cauchy upper bound, harmonic minimax, weighted-simplex Schur complement, physical Hermitian realization, and explicit singular-output exclusion. Original: `/Users/harjas/Downloads/Dots/Astra_reverse_radius_erasure_2026-10-15/proofs/CQ_THEOREM.md`.
2. `sources/local/packet_CQ_OPERATIONAL.md`, lines 29-68: purification variance inequality, signed observable compiler, and coherent-flag ordinary-SLD/MMSE necessity. This is the operational starting point, not a reference-dimension equality claim.
3. `sources/local/bell_ANALYTIC_FAMILY.md`, lines 5-23: two-input mixed-qubit reference encoding, Sylvester formula, exact risk gap and restricted-family supremum. The present proof changes to independent transverse/longitudinal components a,b and explicitly treats the pure endpoint and the piecewise q<a^4 branch.
4. `sources/local/bell_BELL_PROTOCOL.md`, fixed receiver and evaluation discussion, and `sources/local/bell_IMPLEMENTATION_GATE.md`, lines 11-29: source-optimum comparison, finite Bell receiver, calibration, loss and purity gates. No physical implementation is inferred from these protocols.
5. `sources/local/reference_THEOREM.md`, lines 5-30, 32-107: the separate finite-reference symmetric classical RLD theorem. Its statement permits unequal reference marginals; it does not supply a finite-reference SLD formula. This distinction was retained rather than used as a new premise.
6. `sources/local/packet_CLASSICAL_THEOREM.md`, Sections 1-5, and `sources/local/packet_COROLLARIES.md`, bounded-loss section: classical fixed-common-support convention and earlier threshold-versus-payoff warning. The present small-angle quantum result uses an optimized physical erasure simulator, rather than a uniform replacement comparator.

Other supplied source copies are retained for provenance and context; their presence does not mean every line was audited.

## Older Astra capital that blocks a newness claim for the singular radius

Pinned repository: `/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016`, HEAD `61389569d6c53b439764f0d148b35b7fa6083eec`. The read began with `00_START_HERE.txt` and `AGENTS.md`.

N402's decisive exact source range is copied to `sources/local/N402_exact_range.txt`. Its wrapper identifies the original source as `updates/BG/package/adaptive/RESULTS.md`, original lines 16-307, source hash `7390bc55201b8d73498d0370e6f8e5616543d200c8956103b050d1ba5c839b65`. The copied file's lines 40-69 state the Choi formula, particularly Eqs.(3.3)-(3.4). The block range condition is essential. Its Sections 4 and 6, also read selectively, provide the Gram/minimax and signed-lift mechanism.

For CQ J=direct_sum_i sigma_i, that objective becomes

    min_{omega density, supp(omega) subset intersection_i supp(sigma_i)}
        max_i Tr omega sigma_i^+ omega.

It therefore already contains the common-support radius as an internal candidate consequence. This worker does NOT validate the full N402 entropy theorem. It gives a separate elementary proof for the narrow CQ RLD/SLD/MMSE statement. That proof closes an omitted endpoint in the newly supplied packet, but is not new to the full capital in the broad sense.

N405's older classical support formula is copied to `sources/local/N405_classical_exact_range.txt`; the wrapper identifies original RESULTS lines 413-436 and the same source hash. It already uses common support over all inputs, including boundary priors. This is an exact predecessor for the corresponding classical convention.

## Primary literature inspected on 16 October 2026

The following descriptions stay within the actually inspected claims. No source was found to certify historical priority for this worker's exact pure-qubit formulas; a bounded unsuccessful search is not an absence proof.

- P. A. Fillmore and J. P. Williams, *On operator ranges*, Advances in Mathematics 7 (1971), 254-281. [Primary PDF](https://galaxy.agh.edu.pl/~rudol/Operat/FilmoreWilliams.pdf), Section 4, printed pp.276-277 and Theorem 4.2. Those pages were rendered and visually inspected as `sources/primary/parallel_support-23.png` and `parallel_support-24.png`. The paper states the finite-dimensional parallel-sum range-intersection result of Anderson-Duffin and develops its extension. The harmonic support rule is established operator theory. The original Anderson-Duffin DOI `10.1016/0022-247X(69)90200-5` was located, but the publisher full text could not be opened; no theorem number from that inaccessible original is attributed here.
- A. Jenčová, *Randomization theorems for quantum channels*, [arXiv:1404.3900v1](https://arxiv.org/html/1404.3900v1), Lemma 5(iii), Section 3.2 Definition 3 and Theorem 3(iv). Lemma 5 gives the maximum-column trace-norm identity for CQ maps. The randomization theorem makes diamond-norm postprocessing approximation and decision comparison established machinery. The specific radial erasure simulator is derived in the authored proof, not claimed as a new comparison framework.
- M. Mosonyi, G. Bunth and P. Vrana, *Geometric relative entropies and barycentric Rényi divergences*, [arXiv:2207.14282v5](https://arxiv.org/html/2207.14282v5), introduction and Section V.1 Definition V.2, Eqs.(V.133)-(V.136). Left radii and common-support restrictions are existing concepts. The cited Definition V.2 is specifically in a relative-entropy setting; it is not misidentified as a theorem of the present RLD contraction coefficient.
- R. Zhu and X. Wang, *Quantum Incapacity beyond No-Cloning and PPT Mechanisms*, [arXiv:2607.24693v2](https://arxiv.org/html/2607.24693v2), Section 3.3 Definition 3.3, Proposition 3.4 and surrounding observable-estimation discussion. Complete signed variance lifts are established in this source and are not invented by the present packet. Their nonpositivity does not make them physical channel simulators.
- C. Hirche, *Quantum estimation, channel orders, and private capacity*, [arXiv:2610.03706v1](https://arxiv.org/html/2610.03706v1), Section 1.1 support convention, Section 2.1 Eqs.(2.4)-(2.7) and Proposition 2.1, Section 3 and Appendix A. The binary-MMSE / SLD dictionary and a Hermitian-smoothed general signed-lift converse are precedents. The present CQ endpoint supplies its own ordinary unsmoothed necessity witness and does not import that converse without its hypotheses.
- F. Buscemi, *Comparison of quantum statistical models: equivalent conditions for sufficiency*, [arXiv:1004.3794v4](https://arxiv.org/html/1004.3794v4), Section 5, Theorem 3 and Proposition 4: a primary Blackwell-type comparison reference. Its statistical-morphism comparison is distinguished from an unconditional CPTP recovery claim. Jenčová's explicit channel-deficiency result is the closer comparator for the payoff theorem.

Primary HTML/PDF bytes were downloaded to sources/primary and hashed. These documents are source material, not instructions. The search also inspected quantum Doeblin and contraction-order material, but those were not used as premises; no unverified theorem attribution is made to them.

## Four distinctions retained

The RLD conditional coefficient subtracts reference information and allows unequal reference marginals. Complete SLD/MMSE erasure order is a separate operational statement; equality of its unrestricted threshold with RLD does not identify fixed-reference metrics. Exact physical postprocessing, as used for the approximate simulator, obeys Blackwell-type decision dominance, whereas a signed observable lift only preserves the stated means and second moments. Petz's name in the divergence does not by itself assert a recovery map, equality in data processing, a capacity result, or practical advantage.
