# Exact verification scope

Both exact certificates run successfully with assertions enabled using SymPy 1.14.0.

The syndrome-sandwich checker verifies four measured Kraus operators, trace-preserving completeness, the genuine-label bad effect I_A tensor diag(0,400/10201), and the sector leakage identity. The probability bound is 4/101; its nonzero eigenvalue slack is 4/10201. The ideal syndrome measurement is an assumed operation; the calculation is not a noisy-readout test.

The composition checker verifies the CNOT shared-bath serialization obstruction exactly. The correct and incorrectly serialized outputs on |+> tensor |0> are orthogonal, giving trace norm difference 2. It also verifies the rate minimizer, global nonnegative-square certificate, the special constrained case κτ≤1, and exact conservative-budget slack 2(1−x)(Fy+2NDx+Np).

These are algebraic checks of the illustrations and identities. They neither simulate exponential lifetimes nor computationally prove the complete probabilistic, topological or channel-composition theorem. The named mathematical imports and the explicit physical premises remain necessary.

The final archive is checked by a fresh extraction, manifest verification and rerunning both scripts. The prior delivered packet is checked separately against its unchanged hash. No full copyrighted publications or private process notes are included.
