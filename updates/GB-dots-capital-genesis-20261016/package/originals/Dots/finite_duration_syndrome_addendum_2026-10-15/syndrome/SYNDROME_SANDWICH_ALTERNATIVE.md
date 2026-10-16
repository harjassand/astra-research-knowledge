# Genuine syndrome-sandwich alternative to private-frame randomization

Date: 2026-10-15.
Status: bounded constructed interface lemma. The algebra below gives a sound alternative under ideal added measurements and the stated uniform post-error norm bound. It does not establish fault tolerance of those measurements or of a general controller. It is an application of the established syndrome-projection principle, not a claim of new QEC or new noise tailoring.

This note is separate from, and does not modify, the finalized twirl theorem in ../../coherent_memory_packet_2026-10-15/bridge/BATH_MARKED_PROPOSAL_THEOREM.md.

## 1. Result and model distinction

A genuine local check measurement immediately before a completed correction, followed by the same measurement immediately after a bounded coherent joint post-error, supplies real good/bad labels with conditional bad probability at most delta^2. This removes the private-frame, frame-erasure, and frame-independent-error premises of the twirl construction.

The replacement cost is substantive: both additional check measurements must actually be implemented, their outcomes must be correctly retained/interpreted, and the ideal correction branch must be known. Their imperfections, resets, support, and finite latency are not covered automatically. The ideal mathematical composite event has the stated order at one proposal time; a finite-duration overlapping physical implementation requires a separate model.

The added measurements change the full-input channel. They preserve every ideal definite-full-syndrome Pauli orbit and the corresponding classical correction transitions. No claim is made that the unmeasured physical channel was already this syndrome-sandwiched channel.

## 2. Exact instrument

Fix a bounded post-error patch A. Let G be a bounded-support subgroup of code stabilizers that detects the full stabilizer syndrome of all Paulis supported in A. Require no local logical Pauli on A: every patch Pauli commuting with G is a code stabilizer up to phase.

Choose commuting generators g_1,...,g_m for G and let R_s denote their nonzero joint spectral projectors. They are actual measured projectors, not a reinterpretation of the aggregate inactive correction projector.

At a proposal execute:

1. Measure {R_s}, retaining its label s.
2. Execute the completed sweep correction with recorded branch j, Kraus K_j=Q_j Pi_j, including K_0=Pi_0.
3. Compute the predicted outgoing label s'=s xor syndrome_G(Q_j).
4. Apply the actual joint unitary U_{s,j} on A tensor B.
5. Measure the same {R_t}, retaining t. Declare bad exactly when t differs from s'.

Choices of U may depend on these genuine already-observed labels and other genuine causal records. For every admissible record assume a bath unitary V_{s,j} with

    ||U_{s,j}-I_A tensor V_{s,j}||<=delta.

No randomization is used. The bound must hold after conditioning on actual labels; a premeasurement or ensemble-average estimate is insufficient.

All Pi_j are functions of code stabilizers, so [Pi_j,R_s]=0. Because Q_j is Pauli,

    Q_j R_s = R_{s'} Q_j,
    L_{s,j}=Q_j Pi_j R_s = R_{s'} L_{s,j}.

Zero branches are omitted. The full joint Kraus operators are

    B_{s,j,t}=(R_t tensor I_B) U_{s,j} (L_{s,j} tensor I_B).       (1)

Their adjoint products sum to I, even with label-dependent U_{s,j}. Thus this is a complete CPTP instrument on ALL inputs, including arbitrary initial joint memory-bath correlations.

## 3. Uniform conditioned mismatch effect

Fix any feasible s,j and set P=R_{s'} tensor I_B, U=U_{s,j}, and D=U-I tensor V_{s,j}. The current normalized state is supported in P, regardless of its prior coherences or entanglement. Bath-only I tensor V commutes with P, so

    (I-P)UP=(I-P)DP.

It follows that

    P U^dagger(I-P)U P
      =P D^dagger(I-P)D P
      <=delta^2 P.                                          (2)

This is exactly the bad effect after conditioning on the actual measured prelabel and correction branch. It proves Pr(t!=s' | s,j,past)<=delta^2 for every normalized joint state supported in P.

The complete all-input instrument also has the global inequality

    sum_{s,j,t!=s'} B_{s,j,t}^dagger B_{s,j,t}
      <=delta^2 sum_{s,j} (L_{s,j}^dagger L_{s,j} tensor I_B)
      =delta^2 I.                                           (3)

No assumption that a good branch is globally identity/bath-only is used. Its action can depend on unmeasured stabilizer sectors, and it can be trace-decreasing.

## 4. Encoded Pauli histories and the role of local detectability

Decompose U into its G-character blocks U_chi. On an input sector R_{s'}, the final projector R_t selects only the character chi=t xor s':

    R_t U R_{s'}=U_{t xor s'} R_{s'}.

Detection completeness and no local logical imply

    U_chi=(P_chi tensor I_B) sum_M M tensor A_{chi,M},

where P_chi is a representative Pauli supported on A and every M is a code stabilizer supported on A. The bath coefficients need not commute. For any full-code Pauli orbit EV_code,

    U_chi(EV_code tensor I_B)
        =P_chi E V_code tensor A_{chi,E}.                    (4)

Each added R_s either kills that orbit or preserves it, as does each original Pi_j before its prescribed Pauli correction. Hence every complete record (including the real pre/post syndrome labels) follows one encoded Pauli orbit. For t=s', take P_0=I: the good branch preserves the orbit with a syndrome-dependent bath filter. For t!=s', the only added error is the bounded-patch representative P_chi.

The absence of a local logical is essential. Otherwise a logical rotation could commute with every measured check, produce no mismatch, and still rotate the encoded information. Detection completeness is likewise essential: omitting a needed check can misclassify a detectable physical error as a no-change outcome.

The measurement group G need not measure every local stabilizer that appears inside the zero-character polynomial. Those stabilizers are already scalar on each definite FULL-syndrome encoded Pauli orbit. On a general state within one measured G sector they need not be scalar, which is why this orbit statement is not a full-input ideal-channel CP minorant.

## 5. Channel comparison and trajectory preservation

With no post-error, U=I tensor V, only t=s' survives. The memory channel is C D_G, where D_G(X)=sum_s R_s X R_s. This differs from C on general syndrome coherences. On every orbit density E V_code rho V_code^dagger E^dagger, D_G is identity, so the original ideal Pauli correction transitions are unchanged.

For fixed label-independent U, the syndrome sandwich is also algebraically equal to

    D_G Ad_U C D_G = T_U C D_G,

where T_U is the ideal mathematical G twirl. This is an equality of the implemented measured channel; it does not require applying any random frames. For genuinely label-dependent U, equation (1), not a single unconditional U formula, is the correct description.

All outcomes must be summed to obtain the complete channel. Postselecting successful syndrome checks is neither requested nor used. A good record has a subnormalized Kraus map, not a normalized CPTP map.

## 6. Same-attempt probability and memory transfer

The proof ingredients required by the already checked classical module are present:

- all exogenous rate-kappa corrections still occur;
- each actual measurement mismatch has conditional probability <=p=delta^2;
- no mismatch adds no Pauli support on an encoded orbit;
- mismatch adds bounded patch support after that correction;
- the event order is correction then possible birth, with the ideal measurements preserving every orbit.

The genuine labels may be causally used by later operations, unlike fictitious character labels in a purely mathematical unravelling. Any such feedback must keep the clocks exogenous, remain within fixed patch enclosures, and preserve the same uniform conditional norm hypothesis. Arbitrary label-driven memory control is not authorized by this result.

The verified classical interface

    ../../coherent_memory_packet_2026-10-15/classical/SAME_ATTEMPT_LABEL_COMPARISON.md

then dominates the actual mismatch field by independent Bernoulli(delta^2) reference marks on the SAME original Poisson clocks. The new guarded-birth budget is kappa delta^2 N_guard Delta; the ideal correction rate is not thinned. The reference must preserve clock/birth correlation. The measurement operations add no ideal error support, but physical measurement faults would require additional charged births or another analysis.

The common-decoder good Kraus factorization and the TNI-good-map completion of

    ../../coherent_memory_packet_2026-10-15/bridge/BATH_QUANTUM_AUDIT.md

apply verbatim after substituting the real syndrome records. Thus, under the other hypotheses of ../../coherent_memory_packet_2026-10-15/bridge/BATH_MARKED_PROPOSAL_THEOREM.md, the same existence of positive coherent-strength/external-noise thresholds and the same bound A L^4(1+kappa T)exp(-cL) follow. This corollary replaces that theorem's ideal joint-twirl premise with the ideal measured sandwich of this note. It does not inherit an unproved physical measurement implementation.

## 7. Exact rational joint-bath example

Let the memory consist of a stabilized ancilla A with stabilizer Z_A and an untouched logical subsystem L. The completed correction resets A to |0>, with K_0=|0><0| and K_1=X|1><1|. Measure Z_A before correction; its predicted outgoing value is always +1. The patch A contains no local logical.

Let B be a bath qubit, c=99/101, s=20/101, and

    U=I_A tensor |0><0|_B
       +(c I_A-i s X_A) tensor |1><1|_B.

Measure Z_A after U. For either feasible prelabel/correction record, the two postmeasurement Kraus factors are exactly

    good: L_{s,j} tensor diag(1,c),
    bad:  X_A L_{s,j} tensor diag(0,-i s).

The summed global bad effect is

    I_A tensor diag(0,400/10201) <= (4/101) I_AB,

and ||U-I||^2=4/101. Completeness is exact because diag(1,c)^dagger diag(1,c)+diag(0,-i s)^dagger diag(0,-i s)=I_B. The good outcome is a bath filter, so this example still need not admit any independent ideal/bath-channel CPTP mixture. The spectator logical subsystem is preserved for every initially correlated logical-bath state after summing outcomes.

Exact symbolic checker, using installed SymPy and no floating point:

    ../checks/check_syndrome_sandwich_exact.py

It verifies all four nonzero measured Kraus operators, CPTP completeness, the exact real-label bad effect, and the sector identity behind (2). It passes. This is an algebraic example, not an empirical memory test.

## 8. Physical and originality boundary

This alternative trades random-frame privacy and error-frame independence for ideal extra syndrome measurements and truthful records. It requires actual measurement backaction, not a classical annotation or a reinterpretation of Pi_0. Measurement ancilla noise, readout errors, resets, noncommuting measurement circuitry, coherent disturbances during checks, and finite-duration clock overlap remain outside the displayed model until separately justified.

The result uses the standard QEC syndrome-projection mechanism. Its role here is a tailored interface into the completed-sweep same-attempt probability theorem with a persistent bath and a full joint-input bound. No novelty is asserted for syndrome projection, no hardware feasibility is established, and no general faulty-controller or arbitrary continuous-coupling theorem is claimed.
