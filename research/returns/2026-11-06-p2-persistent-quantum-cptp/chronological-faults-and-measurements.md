# Primitive chronology, exact quantum correction and sharp outputs

The [complete source response](P2_PERSISTENT_QUANTUM_CPTP_20261106_RETURN.txt) fixes a finite device and physical deadline. A primitive history contains ideal-attempt labels/times and burst times/physical supports. The actual attempt channels retain acceptance tests, clock changes, conditional gates, measurements and no-op branches. Fault values may change which operations execute. The proof does not select an ideal successful interleaving after observing them.

On each marked support, tensor Paulis or finite-dimensional Weyl operators form a unitary operator basis. The basis fault histories are deterministic support tests, **without a Pauli probability distribution, twirling or independent effective-noise replacement**. In common dilations an arbitrary fault on installed registers and a shared environment expands as `F_j=Σ_a P_(j,a)⊗B_(j,a)`. The chronological product is a coherent operator sum over the actual basis-history evolutions, retaining ordered environment operations. Clock, program, address and syndrome faults participate. Public measurement records can refine branches; the untouched reference is not exposed to the adversary.

For one fixed input/encoding and one common decoder, exact equality of every basis-history decoded channel to the same target isometry implies a dilation factorization `W_a V = U⊗|e_a⟩`, with environment independent of logical input. Substitution into the coherent sum proves the arbitrary-CPTP extension. This is exact error-correction machinery applied to the real attempted-update history. The device has not been shown to satisfy that premise, and neither its decoder nor a valid noncommuting gate history is supplied by the factorization.

For a fixed output instrument with dilated label projectors `Q_y`, the separate sharp-output condition is `V†W_a†Q_yW_aV=Π_y` for every basis history, with `Π_y` projectors on the **full logical input space being certified**. The identity `W†QW=Π ⇒ QW=WΠ` for an isometry and projectors makes the relation survive coherent combinations. Hence the actual measurement effects, including correlations with every untouched reference, equal the target projective measurement channel.

Projectivity is not inferred merely from a projective physical measurement on a larger system. Fixing workspace/ancillas and compressing them out can produce nonprojective logical POVM effects. The fixed output instrument also remains an operational obligation: if only an external decoder/observation is specified, the result remains a decoded guarantee. A zero target effect for a “not done” outcome transfers an already proved by-deadline certificate, without creating liveness or a safe first-done stopping rule.

## Exact counterexample for a general logical POVM

Let an ancilla `A` start in `|0⟩` and use joint projectors `F_0=(I+X_A⊗Z_Q)/2`, `F_1=(I−X_A⊗Z_Q)/2`. The induced logical effects on unknown qubit `Q` are both `I_Q/2`, an independent fair-bit measurement channel.

Every single ancilla Pauli `I,X,Y,Z` preserves those entire logical effects: the resulting computational-basis ancilla has zero `X` expectation. Yet an ancilla Hadamard produces `|+⟩`, changing the logical effects to `(I±Z_Q)/2`. For a Bell-entangled `QR`, the intended `YR` state is `I_Y/2⊗I_R/2`, while the Hadamard case is the equal mixture of `|00⟩` and `|11⟩`. Their trace distance is exactly `1/2`, although both output-bit marginals are uniform.

P2 reports verifying these identities with exact rational matrices. No code or check artifact has been collected or rerun here. This defeats the proposed individual-Pauli-to-general-measurement shortcut; it is not a no-go theorem for classical-output quantum computation or all POVMs. Stronger cross-term conditions may suffice. Exact projective and full-isometry criteria remain distinct positive interfaces.

## The actual-source probability step

Let `G` depend solely on primitive attempt/support geometry. One fixed input interface, target and output/decoder must meet an exact criterion for **every** history in `G`. If the original spatial Poisson source gives `Pr(Gᶜ)≤δ`, averaging exact agreement on `G` and worst-case half-diamond distance at most one outside it gives total half-diamond distance at most `δ`. Fault values can remain adaptive and correlated; no new iid law appears.

The source does not construct such a good event or establish its probability for the autonomous device. Approximate per-basis correction cannot be substituted without controlling coherent combinations; the response explicitly retains the extra spectral/cross-term conditions required by approximate error-set theory rather than assuming them.

[Open construction and costs](clock-routes-and-resource-status.md) · [Overview](README.md)
