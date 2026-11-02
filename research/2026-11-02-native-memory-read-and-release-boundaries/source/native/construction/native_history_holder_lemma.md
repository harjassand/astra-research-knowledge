# Native extension: exact history bound and marked-rod route

Read after the independent decoder-boundary framework was reported. The supplied exact-spin-environment/twirl construction already earns the dynamic consumer; this note does not claim it anew.

## An exact bound that survives the noncommuting auxiliary reference

Write the dressed native reference as direct_sum_s I_L tensor H_a(s). Include an onsite bath Hamiltonian in H_a(s) if desired. Put Z_a(s)=Tr exp(-beta H_a(s)). The audited rod result implies a uniform flux-change bound

 |log Z_a(s)-log Z_a(s')| <= C_beta |s-s'|,
 C_beta <= 2 beta J0(1+epsilon_rod)

(up to the convention counting ±1 syndrome changes). This follows by flipping one formal flux at a time using the proven local Fourier norm. Formal flux sectors are useful even when intermediate syndrome labels are constrained physically.

Expand each dressed local perturbation into a finite sum of data Paulis times ancillary/bath operators; diagonal syndrome coefficients can be expanded into finitely many stabilizer Paulis as well. The constant-depth circuit guarantees a volume-independent coefficient-norm overhead. Consider one Dyson history with m insertions, data Pauli labels E_j, ordered time gaps a_j beta, a_j>=0, sum a_j=1. Let s_j be the syndrome in the j-th gap and B_j the corresponding ancillary/bath insertion. Starting in s=s_0, every s_j differs from s on at most b m check bits for a fixed b.

Generalized Schatten Hölder gives the EXACT finite-volume inequality

 |Tr_a [exp(-beta a_0 H_a(s_0)) B_1 exp(-beta a_1 H_a(s_1)) ... B_m exp(-beta a_m H_a(s_m))]|
 <= [product_j Z_a(s_j)^(a_j)] product_j ||B_j||
 <= Z_a(s) exp(C_beta b m) product_j ||B_j||.

Proof: use Schatten p_j=1/a_j for each exponential, infinity norm for each B_j. Then ||exp(-beta a_j H_a(s_j))||_(1/a_j)=Z_a(s_j)^(a_j). Zero gaps are handled by the limit/infinity norm. This uses no commutation between H_a(s_j), no ground-band truncation, no imaginary-time conjugation locality, no operator monotonicity of exp, and no bound proportional to auxiliary or bath volume.

Consequently individual perturbative histories admit an activity scale beta epsilon C_local exp(C_beta b), after their time simplex and local Pauli-decomposition overhead. This bound holds even with beta t very large. It is substantially preferable to bounding exp(beta H_a) B exp(-beta H_a) in operator norm.

## What this DOES NOT prove

The history inequality alone does not turn the Dyson expansion into a convergent spatial polymer gas. Summing all histories gives an extensive exp(O(N beta epsilon)) bound. Nor do spatially separated V supports factor: the reference H_a(s) is interacting, and its rods can bridge those supports. Subtracting disconnected contributions/cumulants is mandatory. The already-earned commuting-reference polymer identification cannot simply be copied.

## Concrete two-species construction

1. Keep the exact native temporal rods as the first species; their signed pair factors and full-spectrum wrap rods are retained.
2. Introduce each generic V insertion as a local defect vertex with a finite data Pauli and ancillary matrix-unit label. Matrix units cut/pin clock trajectories. Pauli errors change the syndrome flux seen by later closing hops, making local imaginary-time seams.
3. Define connected components using overlap of pinned clock paths, rod interactions, and affected data checks. The last condition prevents different components from canceling a nonzero syndrome secretly.
4. Resum all rod-only components into the already-proven Z_a(s). Components with one or more V vertices are the only new polymers. A valid rooted estimate must charge all connecting background rods and all time seams to their marked V vertices, with constants uniform in volume. Spare KP charge from the audited rod inequalities should pay the connectors. The Hölder lemma above controls potentially adverse time ordering/flux excursions without full-spectrum operator-norm propagation.
5. A closed memory Pauli product from a small new component is a stabilizer by distance; use the existing polynomial filling theorem for its syndrome-dependence neighborhood. Large components touching memory are anchored at O(n), not bath volume. This supplies the same structure required by the existing finite polymer-ratio theorem and logical twirl consumer.

The exact missing estimate is a summed connected insertion bound, for a marked local V support x:

 sum_(connected marked clusters C containing x, |V(C)|>=1) |activity(C)| exp[a |V(C)| + mu spatial_extent(C)] <= K_beta epsilon,

plus a version controlling dependence on a flipped syndrome bit by the polynomial-filling neighborhood. Spatial_extent may need polynomial rather than linear charging to match the existing filling theorem. K_beta may be enormous but must be finite at fixed beta, native t/Delta, and local bath parameters, independent of volume. This is the actual new theorem; asserting it from scalar free-energy analyticity alone is invalid because off-diagonal insertions probe noncommutative correlations.

## A possible fallback construction, not a completed theorem

Choose a strictly interior rod-KP point, then choose a fixed epsilon so small that beta epsilon C_local exp(C_beta b) fits the remaining charge. This supplies an open parameter region if the pinned-rod cumulant estimate closes. All physical resources stay fixed: K-level ancillary spins, the same two-body native Hamiltonian, generic small two-body imperfections, and a bounded-spin 3D weakly coupled environment. No local dimension, interaction strength, resolution time, or penalty scale grows with n.

This is stronger than conventional perturbative simulation only if the connected estimate is actually proved. The present result is the exact history bound and a targeted proof architecture, not an already-earned robust-native-memory theorem.
