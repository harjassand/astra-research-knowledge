# Reading and reproduction guide

Start with HANDOFF.md for the capability, evidence, prior work, missing implementation, consequences, and next test.

Full proofs:
- proofs/CLASSICAL_THEOREM.md: arbitrary finite classical channels, exact small SDP, zero support, physical sharpness.
- proofs/CLASSICAL_OPERATIONAL.md: ordinary unsmoothed complete SLD/MMSE order, signed observable compiler, finite witnesses.
- proofs/CQ_THEOREM.md: faithful quantum-output reverse radius, matrix-harmonic dual, exact benchmarks.
- proofs/CQ_OPERATIONAL.md: complete quantum-output variance inequality and ordinary SLD/MMSE erasure threshold.
- proofs/PAULI_ORDINARY_AND_FINITE.md: distinct reference-free SLD/RLD coefficients and a faithful finite quantum-output decision witness.
- proofs/CONDITIONED_CQ_FIXTURE.md: exact finite gap and conditioning certificate for a separate quantum-output binary experiment.
- proofs/COROLLARIES.md: exclusion thresholds, product composition, and bounded-loss obstruction.

PRIOR_ART.md credits established ingredients. AUDIT_SUMMARY.md describes independent reconstruction and its limits. checks/ contains exact executable tests and result fixtures. examples/ contains the rational cyclic input and primal/dual certificate.

To verify all certificates, install Python 3 and SymPy, then run verify_all.py by its full path from any directory. It reads files relative to its own location and does not modify them. SHA256SUMS covers every file except itself.

Optional solver usage, with NumPy and SciPy additionally available:

python /path/to/archive/solver.py /path/to/archive/examples/cyclic_channel.json

The numerical proposal is followed by exact rational interval verification. This optional solver is separate from the network-free exact-check suite.

## Metric conventions

For faithful normalized states, standard Petz Q2(rho||sigma)=Tr(rho² sigma^-1) and D2=log Q2. For Hermitian tangents, the RLD quadratic form is Tr(H R^-1 H). The conditional form subtracts the corresponding untouched-reference term. If rho=sigma+tH with Tr H=0, Q2=1+t² Tr(H sigma^-1 H) exactly; this identity explains the Petz erasure ordering, rather than a multiplicative contraction inequality for log D2.

For SLD, L_B(X)=(BX+XB)/2 and g_B(H)=Tr[H L_B^-1(H)]. In a balanced binary experiment B±tH with labels ±1, optimal mean squared error is exactly 1-t²g_B(H), after the stated trace normalization. General POVM estimation is reduced to Hermitian observables by the second-moment inequality. Both metric names and their different ordinary coefficients are kept distinct throughout.
