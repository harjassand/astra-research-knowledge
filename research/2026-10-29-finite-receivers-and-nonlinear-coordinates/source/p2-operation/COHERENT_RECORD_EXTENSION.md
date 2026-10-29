# An exact larger complete-record error for the coherent-memory example

Author: `producer-workspace/recovery_challenge`. This is an additional authored result produced during independent challenge. It is not silently included in the review of root's pinned theorem, and its independent review is separate.

Use exactly the two-arrival operation in Section 5 of `MEMORY_FAULT_INTERFACE.md`: source bits x,z, environment branch

    V_xz=(X^x Z^z) tensor (X^x Z^z),

the complete Bell receiver, its prescribed source phase feedback, and coherent storage fault

    E=cI-isQ, Q=Z tensor I, c=4/5, s=3/5.

Write c=cos(theta), s=sin(theta), so 0<theta<pi/4. Root's input |+> on source x and common environment |00> gives distance 3/5, as stated there. That input-specific value is not the universal complete-record norm.

## Exact actual common-receiver reduction

Each V_xz is a Hermitian involution, and its Bell eigenvalue lambda_y(x,z) is the feedback phase. Consequently

    lambda_y(x,z) <Bell_y| E V_xz
      = <Bell_y| V_xz E V_xz
      = <Bell_y| exp[-i theta (-1)^x Q].

The corrected actual channel is therefore the common Bell-measurement channel after

    U_actual=exp[-i theta Z_x tensor Q].

The common noisy-receiver baseline is that same Bell channel after

    U_base=exp[-i theta I_source tensor Q].

These identities concern the actual Bell records and do not discard an outcome or introduce a new source control. They hold on arbitrary source/environment/reference inputs.

The relative unitary U_base* U_actual has spectrum contained in

    {1, exp(2i theta), exp(-2i theta)}.

For every normalized state, including purifications, the real part of its expectation of this relative unitary is at least cos(2theta)>0. The trace distance of the two pure unitary outputs is therefore at most sin(2theta). Convexity and the common Bell channel give the complete-instrument half-diamond upper bound

    epsilon_complete <= sin(2theta)=2cs=24/25.

## A purely record-based matching witness

Prepare the allowed source basis input x=1,z=0 and the common environment state

    |psi>=(|Phi+>+i|Phi->)/sqrt(2)
          =[(1+i)|00>+(1-i)|11>]/2.

Only the Phi records occur. The common noisy receiver gives

    P_base(Phi+)=(c+s)^2/2=49/50,
    P_base(Phi-)=(c-s)^2/2=1/50.

The corrected actual receiver gives the probabilities in the opposite order. Their total variation distance is 24/25. The source is the same basis state at both endpoints, so the entire distinguishability in this witness lies in the actual record.

The lower witness matches the all-input upper bound. Thus, for this operation and this coherent fault,

    actual universal complete-instrument half-diamond = 24/25.

By contrast, the falsely substituted classical Pauli channel with Z-fault probability s^2 has exact complete error 9/25 under the established classical-fault theorem. The original 3/5 source/full-record input witness remains correct. These are different quantities with different input scope.

`independent_fault_audit.py/json` directly computes all four actual record probabilities for the new witness in exact Gaussian-rational arithmetic. The upper bound is the analytic spectral argument above, not a numerical optimization.

This example isolates why the classical fault-path hypothesis has operational content. Coherence between Pauli terms can change the record law even on a source basis state. A deterministic known fault may be calibrated or corrected by an additional operation; no optimum over such added controls is claimed.
