# Primary machinery connection: arXiv:2610.22548v1

2026-11-02. Primary source: [Balasubramanian–Davydova–Lin–Thorngren, A thermally and perturbatively stable classical spin model in two dimensions](https://arxiv.org/html/2610.22548v1). Selectively read §§2.4.2–2.4.5, 3.1–3.2, 3.4–3.5, 4.2, and Outlook. Coordinated with the explicit quantum-family constructor, who continues actual gluing rather than duplicating this audit.

## Source facts (compact)

The classical construction uses odd ell≥7. Reduced comparison maps preserve H¹; higher transferred differentials are retained unless shown absent. Section4.2 separately proves a terminal-flip budget: local correction cost t_b is at most internal syndrome weight, giving 2|sigma_coarse|≤|sigma_fine| in Rep; Par has nonincrease. Theorem4 controls gauge-averaged classical potentials with arbitrarily small decay loss. Its expansion uses commuting Boltzmann factors. Outlook leaves quantum-perturbation proof elsewhere. The lifetime consumer is classical thermal dynamics, not the native83 joint-unitary interface.

## Derived consequence for the ACTUAL ell=8 quantum collar

The material transferable idea is a **terminal-cost certificate**, not importing the classical cochain map or its contraction statement. Our collar already demonstrates why these differ: its algebraic relative quotient contains unmatched U,V,W; knowing that a comparison map preserves logical cohomology does not erase those classes or control their representative weights.

For each actual patch P, specify disjoint interior syndrome coordinates I_P, boundary coordinates J_P, correction variables f_P, and matrices

    A_P f_P = interior change,
    B_P f_P = exported boundary change.

Retain all relative trace labels q_P, including correlated T charges. For each locally extendible (s_P,q_P), compute a table of allowed output carries q'_P and minimum exported cost, subject to the exact reduced-chain identity. The intended analogue of a terminal budget is not necessarily |B_P f_P|≤|s_P| for every isolated relative trace. That can fail when a legitimate incoming charge must pass through an empty patch. Instead seek a *potential-adjusted* inequality

    outgoing cost + Phi(q'_P) - Phi(q_P) <= owned interior syndrome cost.

Here Phi must live on the actual shared ports and cancel when patches glue; each physical syndrome bit must be owned once. This is a finite optimization/dual-certificate target after incidence completeness is established. Closed components may then telescope the potentials; boundary components must retain explicitly charged terminals. A single a+ defect producing two correlated quotient charges must be charged as one packet, not two independent ports.

This is a proposed proof architecture, not a theorem. It gives a decisive falsifier: an actually admissible closed collection of patch transitions with positive total exported cost and zero/insufficient owned syndrome budget cannot be repaired by any telescoping potential of this type. A failed local inequality for an arbitrary nonextendible trace, by contrast, is not a global counterexample.

Two necessary contracts remain independent:

1. **Algebra:** residual=F² sigma_coarse and sigma_coarse is an actual valid coarse syndrome, with logical reference preserved.
2. **Metric:** the disjoint terminal/carry accounting yields the needed contraction.

An H¹ isomorphism establishes neither (2) nor validity of an arbitrary relative trace. For our mapping-cylinder span, the two actual rib inclusions have shifted preimages; replacing them by an identical-copy inclusion would assume the key step. The reduced complex must keep its induced/higher differential until calculation proves that no term remains. The classical construction's simpler ladder partition is not evidence that our extra T charges disappear.

## Derived consequence for robust native83

The new primary paper is a strong nearby prior for hierarchical gauge averaging and finite-temperature perturbative stability. It cannot simply remove the native full-column factor exp(2 beta t b_c).

The exact abstract twirl DOES generalize: for a finite unitary group and any invariant observable B,

    Tr[B E_G(exp(-beta H))] = Tr[B exp(-beta H)].

The partition function is preserved as well. Since the twirled positive operator is strictly positive in finite dimension, defining H_eff=-(1/beta)log E_G(exp(-beta H)) preserves those Gibbs event probabilities exactly. This statement is valid without commutativity and includes real ancilla excitations. Thus 'quantum twirling fails' would be the wrong diagnosis.

The missing step is locality/strength control of this operator logarithm relative to the native clock reference. For noncommuting V_X one cannot replace exp(-beta sum V_X) by product_X exp(-beta V_X). Likewise a gauge-invariant operator A need not commute with a residual U, so exp[-beta(A+U)] cannot be pulled apart as exp(-beta A) exp(-beta U). Group invariance and mutual commutativity are different conditions. Nor does invariance under code gauges remove the noncommuting ancillary coefficients.

A legitimate improvement would therefore require normalized, connected imaginary-time cumulants for the actual clock/bath Gibbs reference (or a different proved operator-valued conditional-expectation expansion), with bounds independent of the entire owned-column absolute history weight. Establishing that estimate might materially enlarge the certified v region. The scalar gauge-averaging theorem alone supplies no such estimate, and replacing native83's source majorant by its classical norm bound is invalid.

Finally, neither this twirl identity nor an improved equilibrium expansion supplies a physical quotient thermalizer or handles noisy native-output release. Those interface costs remain separate from perturbative retention. The prior strengthens attribution and offers a useful carry-budget design principle; it does not currently replace the actual ell8 gluing proof, native thermal expansion, or write–store–read endpoint theorem.
