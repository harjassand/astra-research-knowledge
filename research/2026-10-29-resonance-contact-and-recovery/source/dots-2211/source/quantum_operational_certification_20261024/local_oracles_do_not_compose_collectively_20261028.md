# Strict local positive-block oracles do not imply a collective oracle

28 October 2026. Exact boundary construction; independent review pending. This protects the scope of the single-logical native-oracle corollary.

Consider two logical qubits, no emitted gauge and the identity encoding. The native Pauli channel has probabilities

    p_II=1/10,
    p_XI=p_ZI=p_IX=p_IZ=9/40,

and zero for every other Pauli. These probabilities are nonnegative and sum to one. Each one-qubit marginal, when the other input is averaged maximally mixed and the other output is ignored, has p_I=11/20 and p_X=p_Z=9/40. Its Bloch contractions in X,Y,Z order are

    (11/20, 1/10, 11/20),

all strictly positive. Thus exact extraction is the one-qubit full-CPTP entanglement-fidelity oracle, with fidelity11/20, for either marginal.

The stronger full-output local signed contrast statement also holds. Averaging the other input, C_(i,j)=lambda_j B_(i,j)/4, so the local operator-block T is diagonal with entries lambda_j I4/4 and has strict floor1/40. Both local triples arise from the SAME global identity unitary and commute. There is no weak-gap, inconsistent-embedding or omitted-output excuse for the following failure.

The collective two-qubit identity decoder has entanglement fidelity p_II=1/10. Applying the known unitary correction XI before returning both qubits instead has fidelity p_XI=9/40. This is already strictly larger, so the collective identity/extraction operation is NOT the full-CPTP collective oracle despite both strict local positive-block promises.

The collective benchmark uses a four-dimensional logical/reference maximally entangled input, not the product of independently optimized marginal fidelities. Correlated native errors carry information that one-qubit contrasts do not retain. Local complete-operator inverse closeness can still be composed as an operation guarantee; local NATIVE ORACLE optimality cannot be promoted to collective optimality without a new joint theorem.

This does not contradict the received one-logical full-output theorem: that theorem has one logical input, with other factors treated as emitted gauge whose state is independent of the unknown logical input. Here the second input is an independent unknown logical payload/reference, and the objective rewards joint preservation. No capacity or asymptotic coding conclusion follows from this counterexample.
