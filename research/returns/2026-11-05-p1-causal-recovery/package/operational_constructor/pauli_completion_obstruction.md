# The Pauli-completed rotated tensor loses information on the first tick

This is an obstruction to one concrete receiver mechanism, not to the full class of instruments.

Let `c=cos(theta)`, `s=sin(theta)`, `Phi=|Bell><Bell|`, and `V_AE=c I-2i s Phi_AE`. The four Kraus operators

    K_k = (1/2) V_AE (P_k^A tensor I_E)

form a trace-preserving instrument: `V^dagger V=c^2 I+4s^2 Phi` and the four Paulis twirl Phi to identity. Initialize receiver qubits R,A in a Bell pair. On the first tick, move the input P_k on A across that Bell pair and correct its transpose on R. All four corrected branches are identical, each with probability 1/4 for every source input.

Suppose the processed carrier E is discarded. The normalized corrected first-step map is

    G(rho) = Tr_E[V_AE U_SE
        (rho_S tensor Phi_RA tensor I_E/2)
        U_SE^dagger V_AE^dagger].

This is a physical trace-preserving map from S to SRA on the specified input subspace. The outcome record is input-independent and cannot repair its lost distinguishability.

## Exact distinguishability

Set `x=s^2` and `Delta=G(sigma_z/2)`. Its characteristic polynomial is

    (8lambda-x)^2 (8lambda+x)^2
      * [64lambda^2 - 32(1-x)^2 lambda - x(4-3x)]
      * [64lambda^2 + 32(1-x)^2 lambda - x(4-3x)] / 2^24.

Define `R_x=sqrt(4(1-x)^4+4x-3x^2)`. The eigenvalues are `+/- x/8`, each twice, and

    +/-(R_x+2(1-x)^2)/8,
    +/-(R_x-2(1-x)^2)/8.

Thus the trace distance between the full SRA states from orthogonal inputs |0> and |1> is

    D_1 = ||Delta||_1 = (x+R_x)/2.

For 0<x<1 this is strictly less than one, because

    (2-x)^2-R_x^2 = 4x(1-x)^2(2-x) > 0.

Every subsequent physical operation, including future source collisions, is a CPTP map on SRA and independent fresh systems. The full classical record supplies no extra input information after the first step. Therefore final output trace distance cannot exceed D_1, even if the decoder is granted S and arbitrarily large memory from this point onward.

Half-diamond error at most epsilon from identity requires output trace distance at least `1-2epsilon` for these orthogonal inputs. Hence

    epsilon >= (1-D_1)/2
            = x(1-x)^2(2-x)/(2-x+R_x)
            = theta^2/2 - 11theta^4/12 + O(theta^6).

The bound vanishes at x=0 and x=1 and is positive at every intermediate angle. Future Pauli frames or the entire classical history cannot remove it.

## Scope of the discard

If E is retained, the first step is an isometry from E into RAE: `|psi>_E -> V_AE(|Bell>_RA tensor |psi>_E)` preserves inner products. The loss above comes from discarding E. Retaining E invalidates this particular obstruction but retains the arriving quantum information; it does not itself compress the stream.
