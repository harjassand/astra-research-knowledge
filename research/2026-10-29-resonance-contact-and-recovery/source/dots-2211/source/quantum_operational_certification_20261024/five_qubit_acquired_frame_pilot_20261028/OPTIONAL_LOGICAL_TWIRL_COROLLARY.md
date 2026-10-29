# Optional reduced-channel deployment corollary: private logical Pauli randomization

28 October 2026. **Separate derived interface, independent review pending.** This was not physically executed or added to the frozen pilot, and it is not needed for that pilot's fidelity certificate.

Let L be the actual fixed one-qubit logical CPTP channel after the acquired frames, encoder, physical noise and known decoder have been fixed. Suppose its independently validated entanglement fidelity obeys F_e(L)>=1-epsilon. For each subsequent use choose P uniformly from {I,X,Y,Z}, independently of inputs, source and all other trials. Apply P before encoding and P after decoding; actually retire the private key after both operations. Keeping it available to a future controller under the name of a Pauli frame is not retirement. The effective reduced logical channel is

    L_tw(rho) = (1/4) sum_P P L(P rho P) P.

This requires two fresh private random bits and two trusted physical implementations of logical Pauli controls per transmitted qubit (identity choices may be omitted physically), plus communicating the key to the receiver through the existing trusted controller or an explicitly paid private control interface. It is not free if transmitter and receiver are separated. The source must implement the same fixed channel regardless of the private key; a key-responsive source is outside the assumption.

## Derivation

Write a Kraus operator as K_a=sum_Q k_(a,Q) Q in the Pauli basis, orthonormal for the normalized Hilbert–Schmidt inner product Tr(A^dagger B)/2, with k_(a,Q)=Tr(Q K_a)/2. Pauli conjugation multiplies each coefficient by its character. The uniform character average cancels every unequal pair Q != Q', giving

    L_tw(rho)=sum_Q p_Q Q rho Q,
    p_Q=sum_a |k_(a,Q)|^2 >=0,   sum_Q p_Q=1.

Trace preservation gives the normalization. Its identity probability is p_I=sum_a |Tr K_a|^2/4=F_e(L), so entanglement fidelity is unchanged. For a Pauli channel,

    (1/2)||L_tw-id||_diamond = 1-p_I.

The upper bound follows from the triangle inequality: the identity component cancels, and each nonidentity Pauli unitary channel differs from identity by diamond norm at most2. For the matching lower bound, apply the channel to half of a Bell state. The four Pauli images are mutually orthogonal Bell states, so the output trace distance from the original Bell state is exactly1-p_I. Therefore

    (1/2)||L_tw-id||_diamond <= epsilon.

Consequently, on the same simultaneous confidence event as the frozen pilot, a correctly implemented twirled deployment of its selected fixed stationary receiver has reduced logical half-diamond error <=0.001. This follows from the already-tested invariant F_e and does not require another noise-parameter fit. It is not an observed outcome of additional twirled trials, and it does not test the added controls or key distribution. If the added operations have a justified total half-diamond implementation error delta, triangle inequality changes the bound to epsilon+delta.

## Boundaries

The averaged reduced logical channel is the target. Its diamond-norm statement includes an arbitrary untouched reference entangled with the input payload, but not the source bath or a future memory process. The public training record may remain: on the simultaneous confidence event, fix that record and its selected receiver first, and average only the new private keys. This is not a branchwise claim conditional on P, nor a claim including a retained or publicly exposed classical key as output. It is not a comparison of joint physical-environment states. The original channel must be stationary at deployment, or a separate per-use guarantee must hold. Independent renewal is needed for the simple tensor-product multi-use interpretation; generic correlated memory does not follow from one stationary calibration or holdout. Under actual independent repeated uses, the elementary telescoping bound gives at most m epsilon after m twirled logical uses; this is not a scalable threshold or capacity theorem.

This is standard Pauli averaging with its elementary proof, not a claim of a new randomization technique. Its role here is to make explicit an optional, paid interface converting a validated complete-pipeline fidelity certificate into a worst-case reduced-channel error bound.
