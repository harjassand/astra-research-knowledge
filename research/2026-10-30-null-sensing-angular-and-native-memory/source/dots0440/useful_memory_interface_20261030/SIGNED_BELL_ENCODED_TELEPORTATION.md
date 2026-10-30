# Unknown encoded-input teleportation through a signed-sector Bell resource
2026-10-30. Exact ordinary teleportation interface; the quantum input remains encoded. No bare-state loading, noiseless control, or completed autonomous controller handoff is assumed.

## Useful result
A Bell resource with an UNKNOWN extensive common syndrome can transfer an UNKNOWN already-encoded quantum state, including its external-reference entanglement, without computing that syndrome's Pauli frame. Perform a full physical Bell measurement, communicate all raw outcome bits, and apply their physical Pauli mask to the recipient. If the input used the ordinary zero-syndrome code, the corrected recipient uses the SAME zero-syndrome code.

This is more than testing known Bell correlations: it supplies an encoded-to-encoded quantum recipient. Combined with the bilateral buffer, it avoids an arbitrary encoded-Bell factory for this teleportation resource. The missing native autonomous LOCC compiler and finite-duration live-controller seam are still explicit obligations. The algebra is standard teleportation, not a novelty claim.

## 1. Exact reference-preserving instrument
Let Pi_s be the real CSS-code syndrome projectors, each of rank K=2^k, on physical dimension D=2^N. The resource on A,B is

    |Omega_s>_(A,B)=vec(Pi_s)/sqrt(K).

Q is the input block. For a physical Pauli P, use the Bell outcome convention

    |beta_P>_(Q,A)=(P_Q tensor I_A)|Phi_D>.

Vectorization gives the unnormalized transfer operator from Q to B,

    T_(s,P)=Pi_s P†/sqrt(KD).                       (1)

The recipient applies P, so the corrected operator is

    P T_(s,P)=P Pi_s P†/sqrt(KD)
               =Pi_(s+sigma(P))/sqrt(KD).            (2)

If the input lies in ANY fixed syndrome sector t, then the corrected branch is

    (P T_(s,P)) Pi_t
       =1[s+sigma(P)=t] Pi_t/sqrt(KD).               (3)

Every compatible outcome has probability 1/(KD), independent of the logical state and any reference entangled with it. There are KD compatible masks. Summing their branches yields the identity channel on the entire t-sector. In particular, an unknown input Enc(rho_LR) in sector zero is transferred exactly to the SAME encoding at B, with reference R untouched. Neither party needs to know s.

For a general physical input not restricted to one sector, the corrected average channel is syndrome dephasing,

    rho -> sum_t Pi_t rho Pi_t.                     (4)

It is not the identity on all N input qubits. This prevents a false claim that only k encoded ebits teleport N arbitrary unknown qubits. The intended workload has k unknown logical qubits and no protected quantum information in the syndrome coordinate.

## 2. Coherent resource gauge and retained environment
Write W|s>=Omega_s. For a coherent resource sum_s gamma_s Omega_s, the corrected outcome operator on an input in fixed sector t is

    (KD)^(-1/2) gamma_(t+sigma(P)) I_t.              (5)

If gamma_s is a bath/reference vector or an operator-valued coefficient, the same equation holds with that coefficient retained. Thus every branch acts as identity on the logical input and only changes the resource gauge/bath. Summing outcomes is trace preserving on the gauge, so arbitrary correlations with a retained reference are treated correctly. No classical sampling of the initial common syndrome is required.

Raw physical Bell pairs lie in W|+>^(N-k), and the bilateral-buffer theorem preserves this Bell-target span up to a small relative-correctable error. The teleportation identity therefore does not insert an unproved known-syndrome encoded initializer.

## 3. Residual and endpoint errors remain local
Choose the resource relative error F on the recipient half B, absorbing common errors into the gauge. Let E be an input error on the encoded source. Before correction, the transfer operator is F Pi_s P† E/sqrt(KD). Applying the reported physical mask P gives, up to a Pauli phase,

    F Pi_(s+sigma(P)) E/sqrt(KD).

On a zero-syndrome encoded input, only s+sigma(P)=sigma(E) survives, and the output is F E times the original encoded state. Therefore, for stabilizer-reduced representative radii r_resource and r_input,

    r_output <= r_resource+r_input+c K_endpoint.    (6)

K_endpoint includes bounded-support faults during the ENTIRE finite-duration stage: any required data-frame extraction, local physical Bell gates, terminal measurements, classical messages and records, recipient waits, and raw-mask application. The ideal Bell circuit and per-qubit physical-mask controls have bounded matched-column light cones. The same support envelope holds for every Pauli coefficient of arbitrary CPTP faults on a common actual record; no twirl is used.

Choose the two incoming radii and endpoint budget so (6) lies inside the recipient memory's correctable/initialization radius. A common ideal recipient recovery then preserves the unknown logical/reference state on every good path. This is an encoded-output guarantee, not a physically noiseless bare-state guarantee.

The full raw mask is O(N) bits and may have extensive Hamming weight. That is harmless when it is APPLIED locally in parallel: gate count O(N), depth O(1), and local faults have local effect. By contrast, leaving that mask unprocessed under an ordinary zero-syndrome controller is not harmless. It must be applied before that controller resumes in its declared frame.

## 4. Controller and latency interface
For a scheduled implementation, complete a recovery round, pause incompatible nominal correction actions, execute the full finite-latency teleportation sequence, apply the raw mask, and begin the recipient's ordinary single-block recovery. Every quantum wait and classical bit location is counted. No global decoder runs during this step; only local Bell measurement, bit transmission, and measured local Pauli control are needed.

For live autonomous controllers, the controlled terminal stage must address ALL incompatible nominal dynamics and any unfinished data/controller frame. Starting a new single-block controller on the output also requires a physical initialization/reset/frame seam with its faults charged. The previously reviewed destructive CSS terminal stage supplies a related building block, but it is not automatically a proof of this receiver handoff. A coherent cross-party Stinespring realization cannot be substituted for a genuinely classical channel.

The mask transmission time is a physical resource. The protection boundary cannot be crossed while an extensive uncommunicated byproduct remains. Fixed latency can be included in a fixed-duration endpoint; growing or unpredictable latency requires an additional protected pending-frame mechanism. No claim that classical network latency disappears is made.

## 5. Strong ordinary comparator and scope
An ordinary scheduled noisy Tanner implementation with the same physical Bell sources, local extraction/control circuits, graph connectivity and classical channels performs this exact teleportation. Its fixed-iteration decoder can use noisy bounded-degree classical circuitry as shown in NOISY_CLASSICAL_ORDINARY_COMPARATOR.md. Hence this interface does not establish an autonomous asymptotic advantage; it makes the actual useful recipient and the remaining autonomous service/handoff obligation explicit.

It does not prepare an arbitrary unknown logical input from a bare port, supply magic states, provide general reliable logical gates, or remove the known bare-port error floor. It does show that the common syndrome of a KNOWN Bell resource is not itself an obstruction to transporting an already-encoded unknown state into the standard recipient code convention.
