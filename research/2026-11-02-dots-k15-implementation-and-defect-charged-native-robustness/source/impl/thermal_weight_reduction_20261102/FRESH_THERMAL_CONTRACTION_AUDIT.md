# Independent thermal-contraction audit

2026-11-02. **PASS for the abstract full-thermal transfer and parity-fiber theorem; HOLD for a net hardware advantage of the actual sheaf instance.** This is an internal mathematical review, not external peer review or a compiled HLL/sheaf gadget certificate.

## Material checked

- THERMAL_CONTRACTION_THEOREM.md
- EXACT_PARITY_FIBERS_AND_OBSTRUCTION.md
- RESOURCE_COMPARISON.md
- The saved HLL v2 primary text, particularly the local-block framework and vanilla Theorem 4.6.

## Findings

1. **Finite contraction is correctly typed.** Block contractions can be chosen with p d0=0, d0 i=0, pi=1, h²=hi=ph=0. The strict three-stratum filtration makes (hδ)^3=(δh)^3=0. The displayed finite HPL formulas satisfy P I=1, P D=d P, D I=I d, and D H+H D=1+I P. Higher transferred differentials vanish by the mismatch of retained homology degrees, not by an unproved geometric cancellation. The statement uses actual local blocks, not a global growing inverse.

2. **Full Gibbs, not ground-space substitution.** At the endpoint S'=P0^(-1)(S) follows for every vector from the contraction. Consequently independent fine thermal defects conditioned on P0 b∈S give the exact entire finite-temperature syndrome law, and pushing them forward gives the stated correlated parity marginal. The CSS sector factorization is legitimate for commuting all-positive CSS stabilizer Hamiltonians. The document explicitly does not assert that this general marginal equals the old Gibbs law.

3. **Duality and decoder are correct.** The opposite-sector projection is I2ᵀ, with inclusion Pᵀ and homotopy Hᵀ. R'(s')=I1R(P0s')+H0s' corrects all valid fine syndromes and preserves logical jumps under mapped faults. The degree-one chain/cochain pairing is also preserved. The finite-temperature argument retains the ideal endpoint assumptions of the source theorem.

4. **Exact parity-fiber theorem passes.** For disjoint nonempty fibers the even/odd sums and tanh formulas are exact, including source metachecks. The inequality q_eff=tanh(Σ atanh q_j)≤Σq_j proves the stated exact sufficient B_new≥B_old+log r, with violation-energy convention. It requires both endpoint maps for a quantum conclusion.

5. **The no-free-lunch result is valid and useful.** The duplicate-generator example refutes a universal singleton-column projection at bounded fine-qubit degree. More strongly, a fine single-qubit fault mapping to the nonzero source error translates the two coarse fibers bijectively with energy cost ≤d_f J_new. Thus Z_exc/Z_ground≥exp(−βd_fJ_new), independently of auxiliary entropy, and retaining source suppression exp(−βrJ_old) requires J_new≥rJ_old/d_f. This is not asserted to describe a particular sheaf star.

6. **The incidence bounds are valid under the declared source and HLL attachment graph.** qZ≤4 and qX≤60 follow from the actual sheaf face/vertex-stalk bounds. CSS even overlap gives at most 360 opposite neighbors of an X check and 450 of a Z check. With attachments only on original Tanner incidences and no extra x→z edges (as in HLL), the endpoint columns are bounded by 360/450, and rows by 466M/541M respectively. An arbitrary additional shortcut attachment would require revising those numerical counts, even though the abstract HPL theorem survives.

7. **Resource claim is appropriately limited.** K≤5 and unperturbed clock-overlap D≤26 are earned at the code-theorem level. They are not a proof of net reduction in peak energies, physical volume, or admitted perturbation tolerance. The changed prepass/trace entropy and native contact/dictionary/filling/adjoint constants remain charged and uncompiled. The native compiler coefficient J_Pauli in −J_Pauli S corresponds to violation energy 2J_Pauli; retain that convention when numerically comparing cold conditions.

## Independent calculations

`audit_hpl_regression.py` constructs 40 nontrivial randomized filtered complexes by lower-stratum conjugation of a source complex plus local contractible pairs. It verifies 280 HPL/side identities and exhaustively verifies 1,536 endpoint-preimage cases. It independently checks 48 parity/log-overhead parameter cases, maximum floating-point error 2.22e−16. Results are in `audit_hpl_regression.json`.

These are generic algebra regressions, not evidence that the actual HLL cones or explicit sheaf basis have disjoint parity fibers. No such certificate is present. The full-trace/native transfer is an in-principle application of the previously admitted input-seeded cancellation-aware trace machinery after changing its constants, not a new numerical operating-point certificate.

## Outcome

The package supplies a reusable all-spectrum thermal-transfer principle, a stronger exact logarithmic-overhead subclass, and a rigorous obstruction to treating the latter as universal. It does not close the implementation obstacle for the concrete memory. The next decisive certificate is both actual endpoint maps (or an equivalent correlated-fiber decoder analysis) together with their full native resource constants.

## Explicit endpoint-homology gate

The equality S'=P0^(-1)(S) is valid only because the hypotheses give the **entire** degree-0/1/2 contraction. H1 equivalence alone would not suffice: additional fine H0 relations could shrink S' inside P0^(-1)(S), and additional fine H2 relations would spoil the transposed endpoint argument.

This stronger input is expressly present in HLL v2 §4.1.2, which lists all three homology degrees of every x/q/z block, and §5.2, which derives them from contractible check cones and the dual-tree × tree qubit block. Their induced adjacent maps reproduce the original check matrices. Consequently the vanilla Theorem 4.6 is sufficient for the present fixed-w claim without invoking distance amplification.

The §4.1.3 dummy-face variant declares the same cellular block complexes and identity-on-interface maps; dummy expander edges remain within check-cone boundaries, and the text separately verifies the altered chain-map relation. It therefore retains the same full-contraction structure when implemented as specified. Nevertheless the present audit does not turn either variant into an actual finite-coordinate implementation certificate. Any custom cone, omitted boundary cell, nonstandard dummy-face attachment, or optimization must recheck all block homology and interface maps before using the exact thermal marginal.

The subsequently added general fiber-translation inequality also passes: translation by a valid fine syndrome τ gives a bijection of coarse fibers over s and s+Pτ, with pointwise energy change bounded by E_τ. Therefore exact source-Gibbs matching requires |E_source(s+Pτ)−E_source(s)|≤E_τ. This necessary condition does not constrain a different correlated marginal that merely supports a logically successful decoder; the package correctly distinguishes those cases.
