# Unknown encoded-input teleportation through a signed Bell resource
2026-10-30. Independent exact ordinary instrument audit. PASS, with a fixed input syndrome sector and the stated finite-latency physical correction seam.

## Exact convention and channel

Use the real CSS projectors Pi_s of rank K=2^k in dimension D=2^n, and real unitary Pauli representatives P=X^x Z^z. Set

    Omega_s=vec(Pi_s)/sqrt(K),
    beta_P=vec(P)/sqrt(D).

An unknown input lives at Q; the signed resource is Omega_s on A,B. Bell-measure Q,A in the beta_P basis. Direct contraction gives the input-to-B Kraus map

    K_(P,s)=Pi_s P†/sqrt(KD).                            (1)

Applying the PHYSICAL Pauli P on B yields

    P K_(P,s)=Pi_(s+sigma(P))/sqrt(KD).                  (2)

Therefore, on an arbitrary unknown input vector in the fixed syndrome-t sector,

    P K_(P,s)|psi_t>
       =1[s+sigma(P)=t] |psi_t>/sqrt(KD).               (3)

The same identity holds tensored with an arbitrary reference. Every compatible mask has probability 1/(KD), there are KD compatible masks, and all incompatible masks have zero probability. Thus the sum of corrected branches is EXACTLY the identity channel on the entire K-dimensional signed sector. No logical measurement, global syndrome decoder, or choice of syndrome preimage is required.

For t=0, the output is the same unknown state in the ordinary zero-syndrome code. The resource's unknown common syndrome is removed automatically by the physical Bell mask. This is a useful interface to an ordinary encoded recipient, rather than only to another signed Bell buffer.

If the alternative convention beta_P=(I tensor P)Phi_D is used, the Kraus contains P* and the correction is P^T. Since Pauli transpose changes only a global phase, the actual mask bits are equivalent. One must keep one convention consistent in the written contraction.

## Coherent resource gauge

Let W|s>=Omega_s. On the fixed input sector t, the corrected outcome-P operation is

    (KD)^(-1/2) I_(C_t) tensor <t+sigma(P)|_G.          (4)

It acts identically on the unknown encoded input and measures only the consumed resource's gauge label. Equation (4) holds for arbitrary coherent resource-gauge/bath states. If the resource gauge is correlated with the input/reference, the unconditional channel, after discarding that consumed gauge and the outcome record, still preserves the input/reference marginal: summing all P gives the identity on the input tensored with trace on G. Keeping the outcome can of course reveal pre-existing correlations with G; no secrecy claim against such initial correlations is made.

For a resource gauge density matrix tau, outcome P has probability

    <t+sigma(P)|tau|t+sigma(P)>/(KD).

There is no assumption that a common syndrome was sampled classically before the protocol. Conversely, a coherent UNKNOWN INPUT superposition across distinct syndrome sectors is not covered by the fixed-sector identity. A resource containing only k usable encoded ebits cannot be assumed to teleport all n physical input qubits, including arbitrary syndrome quantum information.

## Correctable errors and noisy terminal stage

Put the resource relative error E_B on B, and an input Pauli E_in on |psi_t>. The corrected Kraus is

    P E_B Pi_s P† E_in/sqrt(KD)
       =phase · E_B Pi_(s+sigma(P)) E_in/sqrt(KD).

The compatible condition is s+sigma(P)=t+sigma(E_in). On it, the output is

    phase · E_B E_in |psi_t>/sqrt(KD).                 (5)

Thus the output stabilizer-reduced error weight is at most the sum of the input and resource residual weights. Errors on the resource's A half can first be transferred to B with a common-gauge change. Faults in the bounded-depth physical Bell circuit, raw-mask transmission, temporary classical storage and local Pauli application add only a bounded common support enlargement per actual fault. A wrong mask bit creates a same-column output Pauli.

For coherent retained-bath errors, expand on the common positive actual fault record. Equation (5) applies coefficientwise; final relative/ordinary recovery of the summed small output-error span preserves the arbitrary unknown logical/reference state. This is stronger than the Bell-target-only identity once an ALREADY ENCODED input is supplied, but it does not initialize an arbitrary bare unknown state.

The entire Bell measurement, physical message latency and applied mask must be treated as one charged stage, with incompatible recipient correction dynamics paused or otherwise explicitly managed. Before mask application the recipient generally has an extensive byproduct. Arbitrarily delayed classical messages and an unproved autonomous controller handoff are not granted.

## Conclusion

This closes a real encoded-recipient interface: a signed Bell resource prepared and maintained without a global preparation frame can teleport an unknown encoded state into the recipient's original code convention. Ordinary active implementations have the same constructive interface. Bare-input loading, bare-output accuracy, asynchronous source acquisition, and the autonomous LOCC/mode-switch compiler remain separate obligations.
