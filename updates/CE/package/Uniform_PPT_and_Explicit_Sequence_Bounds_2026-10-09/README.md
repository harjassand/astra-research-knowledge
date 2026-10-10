# Exact PPT powers and explicit nonstationary approximation

9 October 2026. Consolidated research edition. The earlier focused-reviewed core is preserved unchanged; the new sequence and operational results are later internally derived proof candidates. No external certification, formal verification or priority claim is made.

## Preferred new result

Fix d>=2. An arbitrary length-n serial word T of CP, 2-copositive maps on M_d admits EB CP maps E and F with

 E=q_n T+F,   E*(I)=T*(I),   F*(I)=(1−q_n)T*(I),

where, for n>=d−1,

 m=floor(n/(d−1)),
 q_n=[1+4sqrt(2)d^2(1−1/(8d))^m]^(-(d−1)).

PPT maps are included. The factors may be nonunital, non-trace-preserving, independently varying and nonstationary. For every reference and positive joint input X, the trace-norm error is at most 2(1−q_n) times that input's output trace. Conditioning therefore has no inverse-success-probability penalty. The same E works for all inputs and references.

For trace-preserving words E is an EB channel. A sufficient length for diamond error, or the stated conditioned-state error, at most eta in (0,2) is

 n >= (d−1) ceil[8d log(8sqrt(2)(d−1)d^2/eta)].

This is a conservative explicit O(d^2 log(d/eta)) guarantee, not an optimal engineering threshold. The channel-level repair is explicit; an efficient measure-and-prepare decomposition is not asserted.

Finite branch instruments retain all classical-record probabilities exactly under the EB replacement. This requires fixed transmitted dimension, no retained noiseless quantum memory bypassing the noise, and CP/2-copositivity of every counted branch factor. A map that is PPT only after averaging outcomes need not satisfy the branch condition. No general quantum-network, tensor-power or distillability conclusion is claimed.

## Reading order for the new result

1. nonstationary_ppt/EXPLICIT_EB_NOISE_REPAIR.md gives the preferred positive repair, explicit rate and conditional-state conclusion.
2. GAUSSIAN_PPT_CONCURRENCE_GAP.md proves c_d<=1−1/(8d). PAIR_ROTATION_CONCURRENCE_GAP.md preserves an independent finite-ensemble bound.
3. POSTSELECTION_ROBUST_EB_APPROXIMATION.md gives exact backwards normalization, including an explicit singular-support completion, and the instrument assumptions.
4. EXPONENTIAL_APPROXIMATE_PPT_WORDS.md preserves the earlier concurrence/semialgebraic proof. UNIFORM_APPROXIMATE_PPT_WORDS.md preserves the still-earlier determinant/dimension-induction proof. The preferred proof no longer needs their non-numerical rate constants.
5. APPROXIMATION_PRIMARY_COMPARISON.md and NONSTATIONARY_SOURCE_PROVENANCE.md identify the inspected prior mechanisms. Concurrence filtering, Bell-flag structure and CMHW's 2-EB iteration are credited; the general PPT rank-(d−1) Kraus conjecture is not used.

## Exact results preserved from preceding editions

- A common finite EB power N(d) for all PPT CP maps, including non-TP maps. More generally, a closed convex semialgebraic CP mapping cone whose members are all eventually EB has a common exponent.
- A finite invariant-corner criterion for such cones.
- An exact finite real-algebraic criterion for eventual EB of any algebraic CP map: after the L=lcm(1,...,d) power, every proper invariant corner has nilpotent cross-transfer. A negative certificate gives one fixed pure qubit-ancilla input remaining NPT at every serial time. Its entanglement may become arbitrarily weak.
- A complete candidate of uniform exact EB length for arbitrary bistochastic PPT words. Both unitality and trace preservation are required in that theorem.

The full reviewed core and its original reports are under filter_closed_uniformity and general_cp_eventual_eb. The fixed-pure-input supplement and bistochastic sequence proof were developed after those reviews. No prior report is represented as covering later work.

## Exact boundary still unresolved

Exponential approximation, even the positive separable-noise repair, does not prove finite exact membership for unrestricted nonunital words. FILTER_UNIFORM_APPROXIMATION_EXACTNESS_BARRIER.md supplies explicit bistochastic PPT nonEB qutrit maps with arbitrarily tight CP-order comparisons, uniform local-filter approximation and EB depolarizing repairs. It does not give arbitrarily long PPT factorizations, so it is an output-only obstruction rather than a counterexample to the exact word conjecture.

STRICTLY_POSITIVE_FILTERED_WORD_THEOREM.md proves a uniform exact length for compact strictly output-positive CP families with arbitrary CP filters. FAITHFUL_TRAJECTORY_CONDITIONAL_THEOREM.md proves an exact nonunital extension under a uniformly faithful trajectory, assuming the unrestricted lower-dimensional exact bound; it is unconditional through d=4. EXACT_UNRESTRICTED_GATE_REDUCTIONS.md and INTERMEDIATE_CONCENTRATION_BARRIERS.md preserve the remaining factor-sensitive concentration issue.

## Reproduction and integrity

Run the Python scripts in their folders; NumPy and SymPy are the only dependencies used by the bounded new checks. PACKAGE_VALIDATION.json pairs every rerun script with its result file. In particular the 66-case concurrence interface script and the 100-case peel/lift script now have distinct names and outputs. The checks include 1,625 weighted pair-rotation ensembles, deterministic six-permutation Wick calculations, two exact Wick cases, singular effect normalization, and 189 local-filter barrier examples. No stochastic Gaussian job is needed. These computations check examples and algebraic identities; the universal claims rest on the written proofs.

MANIFEST.json records byte counts and SHA-256 hashes for every other bundled file. The reviewed arbitrary-map core remains 1437f7755136344d1261ee7768b6ede48670dd744c9890e27b1c619f3007ae78. The delivered bistochastic proof remains 4752fca42fe48f6637671c91c31518816ed6b9a7562c96fca9b1f3735053d011. Reviewed cores and reports are byte-identical to the prior delivered edition. No third-party full texts are included.
