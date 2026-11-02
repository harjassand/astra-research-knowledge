# Result first: full-thermal weight reduction, and its resource gate

Status: the abstract transfer, exact parity theorem and resource obstruction passed independent internal mathematical audit (FRESH_THERMAL_CONTRACTION_AUDIT.md). This is not external peer review. It closes an all-syndrome/Gibbs/decoder gap in local weight reduction, but does **not yet certify a net practical hardware improvement** for the explicit sheaf memory.

1. The strongest verified comparator is Hsieh–Li–Lin **arXiv:2510.09601v2, 5 Oct 2026**, not v1 (v2 fixes gadget errors). Its cone construction has check weight at most 5 and total check incidence per qubit at most 6. The vanilla version already gives bounded local blocks; the full distance-amplifying variant has O(n w² log w) size. Hastings arXiv:2102.10030v3 already establishes weight 5 for LDPC inputs; the newer symmetric construction gives a cleaner explicit block framework. None of these quoted code theorems supplies the needed thermal memory statement.

2. For any three-stratum local cone replacement with the stated block homology, an explicitly finite homological-perturbation contraction gives maps P,I,H in the **whole syndrome space**, not merely a ground-code isomorphism. Both Pauli-sector decoders transfer exactly. The new stabilizer Hamiltonian's **entire** finite-temperature syndrome marginal is the pushforward of independent fine-check defects, conditioned on validity in the source syndrome space. It need not be a product Gibbs law on old checks.

3. If the endpoint projection has disjoint parity fibers, exact summation gives tanh(beta J_eff/2)=product tanh(beta J_j/2), using violation energies J_j. Then the cold-energy cost for a fiber of size r is asymptotically log r in beta J, and all fine thermal excitations are retained. This is a genuine reusable thermodynamic subdivision principle.

4. Generic quantum cone reduction does **not** automatically have disjoint endpoint fibers. A short redundancy counterexample rules out such a universal claim at bounded fine-qubit degree. For the actual sheaf source, finite HPL has a sharper column bound than gadget volume: at most 360 in one sector and 450 in the other, using wX<=180, wZ<=15, qZ<=4, qX<=60. This gives a rigorous but possibly costly threshold B_new >= 450[B_old+log(541 M)], with M the actual maximum local-cone coordinate count. Constants in full traces and generic perturbation admission must also be charged.

5. K<=5 and overlap D<=26 remove the old large local clock dimension and improve the **clock-only** coefficient. However M, the contraction norms, new contour entropy, and native source/character constants are not numerically compiled. Therefore the result is a full-thermal **transfer theorem plus exact resource obstruction/test**, not a declaration that K5 automatically beats the old device. The decisive unclosed test is whether the explicit sheaf incidence/basis permits low-congestion endpoint projections (ideally disjoint fibers), or a directly analyzed correlated-fiber decoder with comparable entropy.

Files: THERMAL_CONTRACTION_THEOREM.md; EXACT_PARITY_FIBERS_AND_OBSTRUCTION.md; RESOURCE_COMPARISON.md; thermal_reduction_regression.py/json; INDEPENDENT_MECHANISM_PRECOMMIT.md.

Primary sources:
- https://arxiv.org/html/2510.09601v2 (Theorem 4.6; Sections 2.4, 4.1.2, 5.2)
- https://arxiv.org/abs/2102.10030 (corrected 2021 work, v3 2023)
- https://arxiv.org/abs/2402.05228 (product-code alternative, not a theorem about arbitrary sheaf inputs)
- https://arxiv.org/abs/1411.3334 (subsystem circuit construction, not full Gibbs equivalence)

## Exact unclosed implementation action

- Action: compile both actual endpoint maps P0 and I2^T, minimize/measure their column patterns, then instantiate changed trace/native constants.
- Target: the declared scale-eight sheaf physical bases composed with corrected HLL v2 vanilla cones.
- Reason still open: the source package has no complete executable finite star-incidence generator, and this work proves the generic contraction instead of inventing missing concrete matrices. No access or permission bypass was attempted; this is a missing mathematical/implementation certificate, not a denied-read blocker.
- Status: exact full-temperature principle and logarithmic-overhead subclass proved/audited; particular low-congestion/net-resource conclusion HOLD. Generic K5 qualitative thermal memory transfer is available with explicitly changed, potentially prohibitive fixed constants.

Regression evidence: constructor checks 5,120 decoder syndromes, five complete thermal enumerations, and 30 parity cases; independent audit checks 280 HPL identities, 1,536 endpoint-preimage cases, and 48 parity cases. These test abstract formulas, not the absent concrete sheaf/HLL fiber matrices.
