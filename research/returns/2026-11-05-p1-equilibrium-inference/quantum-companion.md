# Scrambling collisions: source forgetting versus receiver acquisition

The separate [companion theorem](package/quantum_companion/theorem.md) supplies an exact finite-size coherent partial-SWAP law and an unrestricted decoder converse for a fully scrambling source. It extends established radiative random-circuit machinery and does not resolve the [earlier optimal joint receiver memory/processing problem](../2026-11-05-p1-joint-recovery/README.md). The main [equilibrium-inference programme](README.md) has a different model and target.

## Source control, tracial carriers and retained keys

An arbitrary unknown qubit, including its reference, starts at site 1 of an n-spin source; other source spins are tracial. Each cycle applies an independently uniform n-qubit Clifford, then parallel partial SWAPs `cos(theta)I+i sin(theta)SWAP` with n fresh tracial carriers. The receiver gets all outgoing carriers and every Clifford label. It cannot access the source, ancilla purifications or preparation labels, and carriers never return. Decoding may use arbitrary CPTP operations, initialized workspace and classical feedback.

This family pays for source-side Clifford control. Ensemble statements refer to the physical randomized channel retaining its full classical key, rather than to every fixed schedule. For `0<theta<pi/2`, define

```text
gamma_n=((1+3 sin(theta)^4)^n-1)/(4^n-1),
eta_n=((1+3 cos(theta)^2)^n-1)/(4^n-1),
q_t=(1-gamma_n)^t,     a_t=1-q_t.
```

The physical inverse reader initializes n tracial dummy spins and runs the stored layers backwards through inverse collisions and inverse Cliffords. Its averaged recovered qubit channel is `a_t id+(1-a_t)R_tau`, with **half-diamond** error `3 q_t/4`. Every decoder, including a global key-conditioned decoder, has half-diamond error at least

```text
(3/4) [1-sqrt(a_t)].
```

For `alpha=4 epsilon/3` in (0,1), optimal acquisition cycles therefore lie between

```text
ceil(log(1/(2alpha-alpha^2)) / -log(1-gamma_n))
and ceil(log(1/alpha) / -log(1-gamma_n)).
```

These match the leading coefficient of log(1/epsilon), without establishing minimum receiver memory or a faster decoder. The keyed final source's half-diamond distance from its keyed tracial replacer lies between `3 eta_n^t/4` and `min(3/4,3 eta_n^t/2)`. At fixed nontrivial angle, source forgetting can be exponentially fast in n while acquisition requires exponentially many cycles.

## Mechanism, fixed keys and local-circuit scope

Clifford transitivity and injective Pauli histories turn squared operator coefficients into an absorbing process whose per-cycle extinction probability is gamma_n. The tracial physical inverse is a Petz map; its Gram matrix yields the attained channel. Trace-norm contraction and Bell-fidelity testing give the converse for all decoders.

The obstruction is also typical below its exponential acquisition scale. For a fixed key, the probability of even admitting error <=epsilon is bounded by `a_t/(1-4epsilon/3)^2`; a separate Markov bound controls source forgetting. This supports simultaneous typical statements as n grows, not an obstruction for every key. The theorem keeps the keys rather than hiding them.

At n=1 and weak angle the acquisition scale reduces to the preserved quartic law. Without source scrambling, the first-qubit inverse reader instead has error `3(1-sin(theta)^4)^t/4`. A receiver forbidden to control the source cannot turn that comparison into an available control advantage.

The optional local brickwork Clifford mapping identifies ensemble second-moment support dynamics at effective death probability `p=sin(theta)^4`, not identical full output channels. The elementary rigorous region `p>3/8` gives survival at most `[8(1-p)/5]^t`. A numerical critical point inherited from prior work is not asserted as an exact proved threshold.

## Actual resources, evidence and attribution

Each cycle consumes n fresh tracial carriers and O(n^2) classical key bits. Source scrambling uses O(n^3) classical sampling/compilation and O(n^2) elementary Clifford gates, with a conservative nearest-neighbour routed implementation using O(n^3) bounded-strength gates. The cycle must last long enough for those gates.

The displayed inverse reader stores nt output qubits and n dummy spins, applies t inverse Clifford circuits and nt inverse collisions, and retains O(t n^2) classical key bits. A shifting-store implementation adds O(nt) routing cells, O(nt^2) swaps and O(nt^2) carrier-cycle storage volume. Other architectures may improve those costs; arbitrary-address memory is not free.

Preparation, gates, routing and storage defects compose by the half-diamond hybrid bound. A total defect nu adds at most nu to achieved error; a forward defect can weaken the converse by its own amount. Per-primitive error nu/G suffices for G primitives. No physical noise floor, fault-tolerance overhead or temperature robustness is invented without a hardware model. Ancillas are reset or discarded, with no catalytic reuse claim.

The supplied [finite verification record](package/quantum_companion/verification.json) contains actual dense-circuit and group checks. Capital did not rerun them. They are distinct from a large scalable device demonstration. Weinstein, Kelly, Marino and Altman's 2023 radiative random-circuit work already supplies the scrambling mechanism, inverse reader and survival connection; Koenig and Smolin supply Clifford sampling/synthesis machinery. Both are credited in the [primary source register](package/sources.json). The new scoped coherent-collision formulas and universal converse do not establish a newly discovered mechanism, a practical memory advantage or civilisation-changing capability.
