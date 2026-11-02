# Independent structural receipt: generic perturbations as full-time source columns

2026-11-02. **PASS for the corrected exact representation**, joined to the separately written mixed-gas analytic consumer. This earns a static perturbed-Gibbs weight interface for the specified calibrated native clock model with sufficiently weak fixed local imperfections. It is not an assertion of practical robustness or a complete loading/dynamics theorem.

Frozen source: `../EXACT_MIXED_SOURCE_ROD_FACTORIZATION.md`, SHA256 `d6c5c78066af317d3c3e75fcdff64c3a9f6d77446c348140c23cbc8702d8f238`.

Companion analytic results:
- `PINNED_SIGNED_GAS_RATIO_LEMMA.md`, SHA256 `2b0f8e0625469b0deaa240a8040726d7d5005130370ee6f8c54fea8a9cdc8741`.
- `MIXED_GAS_ANALYTIC_CONSUMER.md`, SHA256 `3077290b18531e15c9cf10ee4afe18c8e611db56cfe788c8a7a0e38a840c0654`.

## Exact issues checked

1. **Full-time rather than pointlike perturbation support.** A data Pauli can flip a check between two separated V events. A native winding rod entirely inside that interval sees the opposite flux although it meets neither insertion time. Thus a point-event overlap gas is false. The corrected construction owns the ENTIRE time circle of every affected check, including every check meeting the expanded data support. It also owns every explicitly acted-on clock. This removes the defect interval from the exterior rod gas exactly.

2. **Unique decomposition.** Sources are connected components of the set of DISTINCT USED elementary V labels, in the graph defined exactly by marked data/bath/clock overlap. Whole trajectories on owned columns belong to that source; exterior clock trajectories are ordinary/wrap rods. Disjoint marked supports are equivalent to absence of a cross overlap edge, so gluing cannot split a connected source or merge two allowed sources. Optional graph edges were removed after my audit: if they were retained without a matching compatibility rule, decomposition could overcount. Scalar identity labels are now removed and shared elementary labels explicitly conflict, eliminating the empty-mark corner case. This correction is material to exactness.

3. **Independent syndrome closure.** All check flips of a source lie in its marked columns, disjoint from other compatible sources. Therefore global return to the initial syndrome forces each source separately to return. Native hopping contains only check factors and changes no syndrome. Data supports and bath supports of different sources are disjoint. A native check factor inside one source cannot anticommute with another source's V Pauli: its check would then be marked in both sources. Consequently source data words can be regrouped without uncontrolled inter-source operators.

4. **Pair factors.** On an exterior clock, flux is constant and no V matrix entry acts. It has exactly the old signed rod measure. The controlled-prefix native signs are pairwise functions of clock trajectories. Grouping complete trajectories into sources produces source–source and source–rod scalar factors, still of modulus at most one, plus hard-core zeros. Arbitrary matrix-unit coefficients have no unmarked arguments. The pair factors are independent of the initial syndrome; dependence on syndrome lives in the single-source trajectory characters and the usual winding-rod characters.

5. **Small-source scalar reduction.** Each closed source has a fixed chronological data Pauli product, up to a scalar phase. Below code distance it is a stabilizer. Its chosen filling determines its initial-syndrome character, while internal closing hops contribute additional characters on the owned clock columns. Each trajectory is ONE monomial, not an arbitrary function requiring a truth-table expansion. Filling is used only to locate dependence; it does not increase the physical interaction support, source activity, or source charge. Large data words are retained as norm-one logical operators for the relative-remainder bound.

6. **All clock and bath states counted.** For fixed V event times, summing absolute internal clock paths after dropping nonnegative penalties is bounded by the trace/operator-norm estimate K^c exp(2 beta t c). Prescribed tensor matrix units have norm one; their number does not introduce a factor K per event. Bath energy shifts make onsite semigroups contractions; the corresponding bound is d_B^h, and division by the original bath product partition does not worsen it. This includes source paths that never visit zero and arbitrary real ancillary excitations.

7. **Repeated labels and interleavings.** For counts k_lambda≥1, summing chronological orders and integrating contributes beta^(sum k_lambda)/product k_lambda!. Summing counts gives product_lambda[exp(beta|c_lambda|)−1]. The resulting q^m estimate is uniform in volume and may be exponentially poor in beta t, but beta,t and local dimensions are fixed. Exact sorting of event times reconstructs interleavings once; there is no extra factorial or missing cyclic divisor.

## What the analytic join now supplies

The compound-source measure fits a two-species KP theorem with rod charges a0+b l and source charges A m. Choosing the actual perturbation threshold sufficiently small pays both directions of rod/source interaction, despite arbitrarily large fixed beta t. The pin-ratio lemma controls normalized signed background changes, not a bare extensive absolute partition estimate.

For local influence, the analytic consumer marks either a source whose OWNED-CLOCK/FILLING footprint contains the changed syndrome bit, or a winding rod on that bit in a cluster containing a source. The latter contribution must not be omitted: rod bridges can carry flux dependence away from source support. Fixed-majorant source scaling gives O(v) for both cases, and polynomial filling-anchor counting is absorbed in a spare exponential per-label charge.

A nonscalar exceptional source needs at least d/b distinct perturbation labels. Large memory-touching sources are anchored to O(n) native data OR clock labels, because clock-only native perturbations can acquire data Paulis under dressing. Bath-only scalar sources stay in the background at arbitrary size. The resulting relative matrix remainder is exp[O(n lambda^(d/b))]−1, uniformly in bath volume. Positivity of the ACTUAL projected Gibbs trace then gives positive syndrome-weight ratios; no positive-probability interpretation of the signed intermediate gas is required.

These steps establish the static interface needed by the earlier decoder-witness and thermal-logical-twirl construction. The actual reference Hamiltonian is the native clock Hamiltonian, not a commuting-spin Hamiltonian, but it is exactly identity on the decoded logical subsystem in the dressed frame. The perturbative analysis is on scalar projected traces and finite logical remainders, NOT on a uniform analytic operator logarithm. It therefore does not conflict with the earlier complex-pole counterexample.

## Scope and outstanding whole-model admission

The local coefficient decomposition, fixed-range bounded-density geometry, finite local dimensions, exact reference clock signs and penalties, fixed finite beta, and sufficiently weak fixed Hermitian V are required. The threshold may be extraordinarily small. The statement is not uniform as beta→infinity and says nothing about arbitrary nonthermal/time-dependent noise.

A whole physical-memory theorem must still apply the actual stable-syndrome witness, shrink stability for the dressed support of every perturbation component, verify the decoded logical commutator condition, specify interacting-equilibrium initialization and ideal endpoints, and charge the actual memory-touching perturbation norm density. These are identifiable transfer steps; they are not replaced by merely asserting geometric locality. Efficient equilibrium preparation, noisy loading/readout, and useful hardware parameters remain unearned.
