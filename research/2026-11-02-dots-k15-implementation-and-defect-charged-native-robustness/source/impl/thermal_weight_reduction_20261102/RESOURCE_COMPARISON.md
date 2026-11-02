> Superseding concrete result: RESULT.md and UNTOUCHED_K15_AND_NATIVE_DICTIONARY.md establish original-source K≤15/D≤196. All K180-based cone numbers below are historical conservative-stage comparisons, not the strongest current baseline. Optional K13 is only a modest additional exact-Gibbs re-encoding.

# Same-resource comparator and quantitative ledger

## Established alternatives before new machinery

- **Hastings, On Quantum Weight Reduction, arXiv:2102.10030v3 (corrected 2021 construction).** General CSS copying/gauging/thickening/coning gives weight ≤5 for LDPC inputs with constant overhead and constant distance loss. This is already a decisive comparator to a weight-180 implementation. Its code-parameter conclusion is not full Gibbs equivalence. https://arxiv.org/abs/2102.10030
- **Hsieh–Li–Lin, arXiv:2510.09601v2 (Oct 2026).** Symmetric local cones give weight ≤5, qubit degree ≤6, O(n w² log w) qubits and an amplified distance with uniformization/expanderization. Its vanilla Theorem 4.6 suffices for fixed-w local replacement; the three-stratum presentation permits the explicit finite contraction used here. Use corrected v2, not v1. https://arxiv.org/html/2510.09601v2
- **Sabo et al., PRX Quantum 5, 040302 (2024).** Classical-input reduction yields weight ≤6 for hypergraph/lifted-product codes and can use much less overhead than general Hastings reduction. The declared sheaf family is not supplied as such a product, so this cannot simply replace its Hamiltonian. https://arxiv.org/abs/2402.05228
- **Subsystem/circuit constructions.** Bacon–Flammia–Harrow–Shi provide sparse subsystem codes from Clifford circuits. Gauge generators are not commuting stabilizer energies; a Hamiltonian made of their sum need not have the Gibbs syndrome law used here. Measurement-based gauge fixing, protected symmetries, and noiseless subsystems change the resource/noise contract. https://arxiv.org/abs/1411.3334
- **Local Clifford/subdivision.** Exact conjugation U(H+H_aux)U† preserves the full spectrum and Gibbs state, but replacing conjugated high-weight generators by another low-weight generating set generally changes the Hamiltonian and Gibbs law. Ordinary cell subdivision can have the exact disjoint-parity property; simultaneous quantum cone reduction requires checking both endpoint maps.

## Source parameters actually justified

The source root admits wX≤180, wZ≤15; every edge has at most four incident faces, hence qZ≤4. A vertex stalk is a subspace of F2^(incident faces), of dimension at most 30. An edge qubit meets two endpoint vertex stalks, so qX≤60 for an arbitrary chosen basis. Thus total source incidence ≤64 and w=max(check weight, total qubit degree)≤180 is safe. These are conservative bounds, not measured requirements.

CSS orthogonality implies every intersecting nontrivial X/Z pair shares at least two qubits. Hence an X check can neighbor at most wX qZ/2≤360 distinct Z checks; a Z check can neighbor at most wZ qX/2≤450 X checks. This statement counts actual generator coordinates, including repetitions.

For the HLL three-stratum HPL maps, with maximum block coordinate count M and **only original-Tanner x→q→z attachments (p^{xz}=0)**:

| projection | maximum column support c | maximum row support r |
|---|---:|---:|
| P0 (fine Z syndromes → source Z syndromes) | max(1,qZ,wX qZ/2) ≤360 | (1+wZ+wZ qX/2)M ≤466M |
| I2ᵀ (fine X syndromes → source X syndromes) | max(1,qX,wZ qX/2) ≤450 | (1+wX+wX qZ/2)M ≤541M |

These follow from at most two strictly ordered attachment steps; no column can reach arbitrarily many distant old checks just because its finite block is large. Block sizes remain in row norms and entropy. The generic thermal sufficient bound is consequently B_new≥450[B_old+log(541M)]. This is a bound, not a necessity and not the logarithmic parity-fiber theorem.

## Native clock ledger

After the reduction, check weight ≤5 and total qubit degree ≤6 imply that one check shares data with at most 5(6−1)=25 other checks. Thus the clock overlap count including itself obeys **D_new≤26**. Each native clock needs K_a=max(3,w_a)≤5 levels, and its direct Pauli prefix touches at most five reduced-code qubits. These are real physical reductions in local device complexity.

For the admitted resonant uniform compiler, write x=Dbar eta², J the effective coefficient of −J S, and K the maximum length. **The violation energy in the thermal theorem is J_violation=2J, so B=2 beta J.** Peak internal coefficient is

 t_max = J K³/(2 eta²) = J K³ Dbar/(2x).

At fixed effective J and identical x, the K-only factor changes by (5/180)³=1/46656. Using conservative overlap certificates, old D≤1+180(64−1)=11341 versus new D≤26 yields a further certificate-level change. These are NOT comparisons of proven minimal physical requirements.

To maintain the same physical temperature, J_new/J_old must also account for changed cold threshold. The multi-rod event margin may force smaller x roughly inversely in beta J, so peak-energy cost can be quadratic in the cold threshold rather than linear. New trace entropy, filling/adjoint growth and source-contact constants can change x and the admitted generic perturbation strength again. No numerical operating point is earned from K alone.

The full native sufficient activity remains, in the new geometry,

 q_native = Kmax^(b_c) dB^(b_B) exp(beta delta_max b_c) [exp(beta v_dict)−1].

Replacing Kmax by5 reduces one factor. The constants b_c, C_dict, q_*, the source-contact graph, exceptional-source threshold, and the decoder/filling constants must be recomputed for the new actual code and noise range. Some are controlled by short native prefixes; others see the coarse prepass and can depend on M. Quoting the old v tolerance unchanged would be invalid.

## Geometry, count and comparison stopping condition

Let A be the actual number of new sites/checks per old local neighborhood. Fixed-w theory gives A=O(w² log w) at the code level, with implementation-dependent constants. A bounded-density three-dimensional embedding can be retained at increased density A times the old density, or after a fixed spatial dilation and charged volume/range increase. Native size counts every new data qubit and every clock site. No fixed-density or fixed-volume free lunch is asserted.

A net physical improvement requires either (i) an actual sparse endpoint/fiber certificate and numerical trace/native constants, or (ii) a stronger directly analyzed correlated-fiber thermal decoder. The existing root does not include the full finite star-incidence generator or the HLL cone implementation needed to measure these. Therefore the present package stops at a proved transfer principle, an exact logarithmic-overhead subclass, and an explicit obstruction/test for the general family. It does not substitute a ground-space theorem for a full-temperature one.
