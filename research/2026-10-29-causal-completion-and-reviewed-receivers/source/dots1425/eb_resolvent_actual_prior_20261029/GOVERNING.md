# Constant-weight EB resolvent removes the actual-prior penalty
2026-10-29. Analytic candidate; receiving review pending.

Suppose Φ=αB+(1−α)C, 0<α≤1, with B an EB CPTP channel and C CPTP. For any faithful actual prior σ, let R be its universal averaged rotated-Petz recovery for Φ. Then Ψ=RΦ fixesσ and decomposes as αE+(1−α)D, with E=RB EB CPTP and D=RC CPTP.

Define F=αΣ_(k≥0)(1−α)^k D^k E. Each term is EB, and its scalar weight isα(1−α)^k; the weights sum1. Therefore F is CPTP and EB. Let Q=(1−α)D. The series converges in diamond norm and ||(id−Q)^−1||diamond≤1/α. Exact composition algebra gives
id−F=(id−Q)^−1(id−Ψ).
Consequently, for anyρ and arbitrary quantum reference,
T(ρ,Fρ)≤α^−1T(ρ,Ψρ).
Universal recovery gives T(ρ,Ψρ)≤√ℓσ,Φ(ρ). Averaging an ensemble of actual meanσ yields
**e_avg(F)≤√δ/α**, δ=χ(ensemble)−χ(Φ ensemble), with NO barycenter penalty and NO stationarity requirement. The complete formulation requires product meanσ⊗ω_R, so the recovery factors. F⊗id_R is EB on A only.

## Uniform unital self-compatible qubits
The independently accepted Pauli-pairing construction in ../qubit_entropy_comparator_20261029/GOVERNING.md supplies such a decomposition with
α=1−s2≥1−1/√2
for every full-domain self-compatible UNITAL qubit channel, in its canonical unitary gauges. Its EB branch may be a convex combination of output-unitary conjugates of the same input dephasing, which is still EB. Thus
**e_avg(F)≤(2+√2)√δ**
for EVERY actual qubit prior, including coherent and nonstationary means, and the product-barycenter complete extension. This improves the prior-transfer scope of the original fixed-dephasing entropy proof. It does not preserve that fixed comparator; F is prior-adapted.

## Constructiveness and limits
The resolvent defines a convergent EB channel. At finite depthm, use the firstm terms and assign remaining probability(1−α)^m to any specified EB replacement channel; diamond error from F is at most2(1−α)^m, hence state trace error at most(1−α)^m. This is a mathematical finite-comparator approximation. Actual acquisition/preparation of R is not supplied; no cheap implementation or source-oracle inversion is asserted.

No arbitrary nonunital-channel, arbitrary correlated-barycenter, or many-noisy-qubit tensorization claim follows. Generalized universal recovery, EB closure under composition/mixture, and geometric resolvents are prior machinery; no historical novelty assertion is made. This is an explicit actual-prior transfer using the accepted compatibility coefficient.

Dependencies: Junge et al., arXiv:1509.07127v3 universal recovery; accepted qubit Pauli pairing packet and its receiving receipt. The TNI extension suggested during exploration is NOT accepted: see TNI_ORDERING_OBSTRUCTION.md.
