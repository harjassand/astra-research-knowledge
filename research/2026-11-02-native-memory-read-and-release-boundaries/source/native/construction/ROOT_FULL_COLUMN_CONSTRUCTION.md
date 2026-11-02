# Root full-column construction for generic native perturbations

2026-11-02. Candidate proof mechanism, pending independent verification. This is not yet a robust-memory theorem.

## 1. Finite local decomposition
Conjugate native V by the exact bounded-depth U. Expand each local term into data Paulis times clock/bath matrix units. The coefficient l1 overhead is a fixed constant from bounded support and dimension. For each original perturbation label x choose one fixed expanded column set R_x containing all clock and bath sites in those coefficients, every clock whose stabilizer meets the data support (over-inclusive is safe), and enough bounded neighbors that physically overlapping data supports imply overlapping column sets. The actual code has no isolated data qubits. |R_x|<=c and column-overlap degree is fixed. This set is independent of chosen Pauli component and repeated-event count.

## 2. Exact worldline partition candidate
For a Duhamel history, take the set of V labels used at least once. Its connected components under R_x overlap are source animals C. Define R_C=union R_x. Include the ENTIRE imaginary-time trajectory of every clock in R_C inside that source, not merely the segments cut by V events. No ordinary background rod is allowed on those clocks. All exterior clocks split into the already-proved ordinary/wrapping rods. Bath sites in source supports are likewise included for the whole time circle, while untouched onsite bath traces factor and normalize.

This should be a unique partition: the used-label set determines C and R_C, and each clock is either in one source or in the exterior. All internal clock paths and V event orderings remain as source labels. Integrating over their labels comes later. Sources sharing a column are forbidden because they would have been one animal.

## 3. Why data operators factor
An exterior stabilizer S_h commutes with every data Pauli in every source: otherwise its clock h would have been included in the source's R_x. Thus exterior closing-edge data labels can be moved past all source words without a data phase. Source words in distinct animals also commute: their data supports cannot overlap incompatibly, and a source clock stabilizer that flips another source's data Pauli would be in both column sets. A nonzero net data syndrome cannot cancel between different source animals, because all affected checks belong to their disjoint R_C. Projection onto a fixed input syndrome therefore forces each source data word separately into the centralizer.

Inside a source, closing hops contribute stabilizers S_h and V contributes a Pauli word E_C. The logical class of the total word equals that of E_C. Its data support is contained in the union of the m DISTINCT perturbation supports, hence weight<=b*m even when labels repeat arbitrarily. If b*m<distance, every closed E_C is a stabilizer. The source is then scalar on the logical qubit, with syndrome dependence localized by the earned polynomial filling theorem plus its own clock set. Large sources are treated as matrix remainders, not falsely scalarized. Pure clock rods never create a logical class.

## 4. Mixed pair interactions
Internal gauge hopping signs factor over clock pairs. For a source and an exterior rod, multiply all pair signs between that rod and the internal clock trajectories. This is a factor +/-1; it can differ from one only near R_C, and the source occupies the entire time circle. Source-source interactions across neighboring but disjoint clock sets have the same pairwise sign factor, again modulus one. Same-column overlap is hard core. Ancillary matrix-unit factors of V involve only R_C by construction and are part of the source measure, not new interactions with distant rods. Data scalar stabilizer signs are also part of that measure. Therefore the proposed exact representation is a two-species complex-measure gas with pair factors of modulus<=1, not an asserted generic off-diagonal cumulant theorem.

## 5. Activity and KP target
A source with m distinct V labels has at most c*m unrestricted clocks/bath sites. Sum internal absolute hopping paths and V events. A conservative bound is

 |activity(C)| <= [exp(beta*C_local*v)-1]^m * exp[C_beta*m],

where C_beta includes local dimension, onsite bath normalization and unrestricted clock hopping costs; C_beta may be enormous but is independent of volume. One may safely use C_beta=O(beta*(Delta+t+B0)+log d) per expanded support. Positive clock penalties may improve this to a bound involving t rather than Delta, but this improvement is unnecessary.

A source sees all neighboring background rod starts throughout beta, contributing O(|R_C|*beta*t^2/Delta) plus charged wrapping activities. Give source charge proportional to m+|R_C|*(a0+b*beta), with additional space/filling counting slack. A background rod sees source fugacity only on bounded-neighbor columns; making v sufficiently small fits its spare endpoint charge, uniformly in the rod duration. Source-source animal counting is bounded-degree. Thus an open v interval is plausible without beta*t small or any volume-dependent resource.

The unresolved work is to make the exact activity definition, time-ordering combinatorics and the matrix remainder ratio fully explicit, and to prove the syndrome-influence sum after polynomial filling. A raw absolute partition bound exp(C*n*v) is not acceptable. Remote rod-only clusters must cancel by the mixed-gas logarithm or a finite polymer-ratio theorem.

## 6. Bath-volume and decoder interface
Bath-only sources can remain scalar regardless of their size. Logical exceptional sources must contain enough memory-touching labels and can be anchored at O(n) memory locations, not total bath volume. Bounded-density onsite bath dimensions and local V remain explicit. Once the actual Gibbs witness bound is established, the already-earned exact-H logical-twirl/equilibrium-overwrite consumer applies; there is no need to invoke a fully secular Davies approximation.
