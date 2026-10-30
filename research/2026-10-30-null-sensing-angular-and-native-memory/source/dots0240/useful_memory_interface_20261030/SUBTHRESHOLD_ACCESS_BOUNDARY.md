# The storage guarantee also forbids useful subthreshold logical access
2026-10-30. An ordinary information-disturbance consequence, not a claimed new theorem in quantum information.

## Precise boundary
Let M_T be the physical initialized memory channel and D_T its prescribed mathematical decoder. Suppose

    ||D_T M_T-id_L||_diamond <= delta_N(T).

Include any proposed recipient, its ancillas, collected reset radiation, and common retained bath in the physical environment E, initially in one fixed state independent of the logical input. The recipient/environment must be DISJOINT from the output registers on which D_T acts; one cannot count a live controller needed by the forest decoder both as retained memory and as leaked output. If all recipient-to-memory couplings stay within the exact noise class covered by the memory theorem, the same bound still holds: calling a term a useful 'control signal' does not remove it from the quantified perturbations.

Then there exists one environment state sigma_E, independent of the logical input, such that

    ||M_T^E - [rho -> Tr(rho) sigma_E]||_diamond
       <= 2 sqrt(delta_N(T)).                       (1)

Any accessible recipient subsystem satisfies the same bound by CPTP contraction. In particular, for two equiprobable candidate logical input states, its optimal discrimination probability is at most 1/2+sqrt(delta_N(T)). The result includes arbitrary entangled side references in its channel formulation; it is not merely a statement that local expectation values happen to be small.

## Proof and primary source
Append a Stinespring dilation of D_T to a physical dilation of M_T. Its complementary output includes the actual environment and the discarded decoding workspace. The dimension-independent continuity theorem for Stinespring dilations gives a common enlarged dilation within sqrt(delta_N) in operator norm of a dilation of the identity. The latter is |psi> -> |psi> tensor |eta>. Tracing the logical output and using the elementary channel-distance bound <=2 times the isometry distance proves (1); discarding decoder workspace gives the physical-environment assertion.

Primary theorem inspected: Kretschmann, Schlingemann and Werner, *The Information-Disturbance Tradeoff and the Continuity of Stinespring's Representation*, Theorem 1 and Theorem 3, https://arxiv.org/pdf/quant-ph/0605009 (published IEEE TIT 54, 1708–1717, 2008). The dilation space may be enlarged; no problematic fixed-minimal-environment unitary assertion is required.

## Consequences for this proposed memory
If delta_N(T)<=C N^a(1+T)e^{-cN}, the recipient leakage norm is <=2sqrt(C)N^{a/2}sqrt(1+T)e^{-cN/2}. It remains exponentially small throughout any T<=exp(alpha N) with alpha<c, up to polynomial factors. Thus a weakly coupled spectroscopy/readout probe cannot use the same protected logical degrees of freedom as an order-one signal channel while claiming to remain inside this guarantee. This is a storage-versus-access boundary, not a claim that physical syndrome or temperature signals disappear.

Likewise suppose a desired logical gate V has Delta=||V-id_L||_diamond>0. An implementation inside the same protected perturbation class cannot be within epsilon of V unless

    epsilon >= Delta-delta_N(T).

The inequality is simply the triangle inequality, using the FIXED original decoder. It does not forbid changing a classical Pauli-frame label; it forbids a physical nonidentity logical channel under that decoder. Nontrivial computation requires an intentional change of code/generator/operating mode, a coupling outside the protected perturbation budget, a time outside the certified lifetime, or a change in the declared logical reference frame whose physical implementation is separately charged.

For the native physical memory, this statement applies to allowed local CPTP Poisson couplings. It does NOT promote its physical finite-duration controller to arbitrary weak continuous-Hamiltonian robustness. For the ideal atomic continuous-noise theorem, it also applies to the declared bounded continuous data-bath couplings. These are distinct scopes.

This observation is useful as a design filter: no proposed quantum recipient can extract order-one logical information merely by adding an interaction that the accepted theorem has already proved correctable for the entire access duration. Encoded Bell switching escapes by an explicit terminal operating-mode change and a code-preserving logical operation; it does not claim an invisible extraction while the original logical identity theorem remains applicable.

It also yields a limited quantum-escrow interpretation: under the stated local-access restrictions, stored quantum information is approximately private from the allowed environment. This is not cryptography against an unrestricted custodian who can switch off, dismantle, strongly couple, or globally decode the device. Scheduled fault-tolerant memories with the same diamond-norm correctness enjoy the same privacy consequence.
