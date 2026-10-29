# Conjugate local circuits and joint-state notation

28 October2026. Clarification to GOVERNING_BRIDGE_v1.md; original v1 and its manifest remain unchanged.

1. Bilateral stabilizer distillation uses conjugate A-side operations. If C_a=V†E_a maps B's syndrome-a sector into its logical qubit, Alice uses C_a* and Bob uses C_a E_c, where E_c corrects the measured syndrome difference. Thus A's stabilizer projectors are the complex conjugates (equivalently transposes for Hermitian projectors) of B's. The listed25-qubit stabilizer generators are real, but a compiled encoder/decoder with complex Clifford gates must use the conjugate A-side circuit, not blindly identical gates. The saved operation_checks_v1.py already implements Alice=C.conj() and Bob=C@corr.

2. In equation(2), omega_acc denotes the JOINT subnormalized accepted logical-pair plus retained-environment/public-record state. It does not denote the pair marginal alone. tau_acc is its environment/public-record marginal. The good accepted terms factor exactly as Phi+ tensor tau_good, while the bad accepted terms have trace at most beta; comparison with Phi+ tensor tau_bad gives the bound. Retired twirl keys remain excluded from this interface.

No numerical bound, source condition or recorded program changes. Independent reviewer identified these clarifications while reproducing the exact beta and globally checking the minimum-weight syndrome decoder.
