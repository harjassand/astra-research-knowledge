## ASTRA — Correcting quantum key leakage instead of assuming perfect isolation

A stronger physical interface has survived the mathematical and computational checks: Astra's two coherent control bits can be encoded so that an arbitrary interaction between the apparatus and one physical flag spin does not destroy the exact quantum-memory fault representation.

The construction uses the established `[[4,2,2]]` stabilizer code. Four physical qubits encode both control bits, with stabilizers

\\[ S_X=XXXX,\qquad S_Z=ZZZZ. \\]

Its key property is

\\[ P\sigma_jP=0 \\]

for every nonidentity single-qubit Pauli \\(\sigma_j\\), where \\(P\\) projects onto the encoded space.

This permits two operating modes:

- Unknown exposed spin: check the stabilizers and reject if an error is detected. Every accepted branch retains the correct encoded control state.
- Known exposed spin: measure the syndrome, correct the indicated Pauli error and continue without rejection.

The second mode is stronger. Even an arbitrarily large, coherent interaction between that physical spin, the data qubit and a never-reset quantum bath is exactly correctable, provided its support remains confined to that one known flag spin.

### Full-memory verification

# 40

Independent arbitrary-interaction checks across both modes

# 5.91 × 10⁻¹⁶

Maximum corrected syndrome/test-instrument residual

# 3.04 × 10⁻¹⁶

Maximum accepted positive-channel residual

# 0

Bath dimension or mixing-time assumptions

The error syndrome can remain available for later adaptive control. The actual private Pauli key must still be retired.

This is an application of established quantum error-detection and erasure-correction theory, including the previously demonstrated four-qubit code, not a new quantum-code discovery.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://doi.org\&sz=32)

Science Advances

+1



### Stronger consequence: second-order protection with a fast bath

When the unwanted one-spin coupling is bounded but the bath Hamiltonian is arbitrarily fast, syndrome correction provides a uniform quantitative improvement.

Write

\\[ H(t)=I_F\otimes H\_{DM}(t)+V(t),\qquad \operatorname{Tr}\_{F_j}V(t)=0, \\]

with \\(V\\) supported on one known physical flag spin, the data and the bath. Define

\\[ \varepsilon=\int_0^T\\|V(t)\\|\\,dt. \\]

After exact flag recovery, the complete data–bath channel differs from the channel without \\(V\\) by

\\[ \boxed{\frac12\\|\mathcal N\_{\mathrm{recovered}}-\mathcal U_0\\|\_\diamond \le \min(1,\varepsilon^2).} \\]

The result requires no bound on the bath's own Hamiltonian norm. The key idea is that the error's first-order term lies outside the correctable logical sector; the residual effect on the recovered channel starts at second order.

Sixteen controlled reference calculations tested bath-Hamiltonian norms up to 150 and correlated quantum reference inputs. Every tested distance respected the derived bound.

### Exact limit: sequential access defeats the code

A bath that touches flag spin 1 and then flag spin 2 can copy their parity, which is an encoded private key bit. Each contact is local, but together they implement an undetectable logical operation.

The executed counterexample had:

- Stabilizer acceptance probability: 100%.
- An encoded control bit copied into the bath.
- A completed logical output differing from the falsely assumed randomized channel by trace distance 0.35355.

This establishes a critical hardware requirement: the total flag region accessible to the uncontrolled apparatus across one complete call must be correctable. Restricting the number of simultaneous interactions is insufficient.

### Further result: the exposed spin carries no private-key information

The code provides a stronger property than error detection. For any encoded two-bit control state, even one entangled with the data, hidden bath and an untouched reference,

\\[ \boxed{ \rho\_{F_j,DMR}=\frac{I\_{F_j}}2\otimes\rho\_{DMR}. } \\]

Thus a single exposed flag spin is maximally mixed and completely uncorrelated with the rest of the accessible system. The bath can still infer information indirectly from the data, but direct access to this flag spin supplies no additional key information.

I verified the identity on 100 randomly generated correlated logical–data–bath–reference states. The largest residual was \\(1.28\times10^{-16}\\).

### Extension to non-Clifford gates

The shield also preserves Astra's positive fault accounting for a completed \\(T\\) gate. After syndrome recovery and private frame correction, the logical fault branches are \\(T\\), \\(TX\\), \\(TY\\) and \\(TZ\\).

Eighty full-memory, syndrome-conditioned reference checks passed, with maximum complete-channel residual \\(6.49\times10^{-16}\\).

The construction additionally passed a two-round calculation with syndrome-dependent feedback and a reused bath. This confirms that retaining the correction syndrome does not itself invalidate the positive fault representation.

### Physical cost and scientific decision

The reference implementation requires 15 two-qubit gates per call, excluding terminal measurements and corrections. That is substantially more expensive than a conventional controller with genuinely isolated classical random keys.

The meaningful tradeoff is different: exact quantum-control-key isolation can be replaced by an independently justified restriction on which physical flag spins the apparatus can access. This is useful only when that access geometry is easier to guarantee than the original isolation assumption.

The quantum coding mechanism is established science. The new result is its explicit integration into Astra's complete-memory, non-Clifford fault-certification interface—not a demonstrated new device or independently established foundational theorem.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://journals.aps.org\&sz=32)

Phys. Rev. A

+2



### Preserved work

All nine executable validation studies passed a clean consolidated rerun. The source files, numerical outputs, complete derivation, counterexamples and checksums are saved.

Complete technical derivation

Full-memory correction theorem, second-order bound, unknown-location detection, physical compiler and no-go cases

Reproducible research archive

Nine Python studies, executed results, validation log, environment details and verified SHA-256 checksums

Next decisive experiment: implement the encoded control register with a retained spectator-memory qubit, deliberately expose one versus two flag spins, and measure the complete subsequent quantum instrument. The key question is whether real hardware can enforce the correctable-access boundary throughout the gate and syndrome-extraction sequence.

That physical boundary remains unverified.