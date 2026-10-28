# Independent receiving: native single-logical oracle and quadratic fit regret

28 October 2026. Reviewer: review_trace_class_synthesis. Status: PASS_SCOPED_SINGLE_LOGICAL_NATIVE_FIDELITY. Version bindings are in the accompanying JSON receipt. Original governing sources unchanged.

## Oracle corollary

Read the entire `positive_operator_single_logical_oracle_corollary_20261028.md` and its exact source-realization program. Starting from the normalized Bell expansion, C_j=N(sigma_j/2) gives Fe(RN)=(1+sum Tr[R†(sigma_j)C_j])/4. The unsigned output contributes exactly the constant because RN is trace preserving. The received convex dual therefore certifies the physical extraction Tr_G Ad_U† against every CPTP decoder on the SAME accessible output. No supplied strict gap is required for this optimum identity; learning does require excitation.

The common B family makes the extraction pointwise optimal across its conditional one-use channels, even against a decoder knowing their current coefficients. Initial logical/reference independence from source memory is necessary and is stated. The half-diamond comparison pays at most zeta in Bell probability because that probability is a bounded effect on the reference-extended output. This does not optimize complete environmental output, collective payload decoding, causal strategies or arbitrary later memory states outside the family.

Reran the author's exact SymPy fixture: Kraus trace preservation and all 64 channel-entry equalities, noncommuting spectator blocks, dual sum of squares and complementarity, 12 physical competing decoders, and forgetting boundary passed. Exact optimum is81/100, not inferred merely from sampled competitor agreement. The proof of optimum is the received dual. The fully forgetting channel's1/4 optimum is consistent with initial product input/memory and emphasizes lack of learning excitation.

## Quadratic fit certificate

Read entire `positive_fit_quadratic_recovery_regret_20261028.md`. Let Delta=C−Ctilde and any unital CP proposal have images P_j. With D²=sum||P_j−A_j||F², received fitted-model curvature gives

    F_C(P)−F_C(A)<=−kappa D²/2+<P−A,Delta>
                    <=−kappa D²/2+eD<=e²/(2kappa).

Dividing by4 gives e²/(8kappa). No physical realization of Ctilde or positivity of actual C is used. The exact finite fixture `positive_fit_quadratic_regret_independent_check_20261028.py` verifies SHARPNESS: identity fit S=I/2, actual rational real-unitary rotation, actual full-CPTP oracle1, extracted fidelity c², e²=4(1−c²), kappa1/2. Four exact instances saturate the claimed bound. This is a source-disabled mathematical check, not an acquisition simulation.

For the distinct future-family scope, the acquired common-B certificate gives D_AB<=2e/kappa. The exact physical-triple gap is (1/8)sum Tr[D_j T_jk D_k]. To justify its operator bound without accidentally commuting coefficients, define the row operator L=[D_X D_Y D_Z]. The positive expression is Tr(L T L†), bounded by Tr(T)||L||op². Since LL†=sum D_j², this is <=Tr(T)sum||D_j||op². Physicality and the oracle formula imply Tr(T)<=3. The result is3 D_AB²/8<=3e²/(2kappa²). Both upper bounds may be capped at1. No future knowledge of T is needed, but every future channel must actually share B and block positivity. The source says so.

## Conditions and limitations retained

- Full physical output is full only relative to the contrasts. A reduced local patch licenses only decoders on that patch.
- Simultaneous confidence permits data-dependent fit selection. An empirical residual without its uncertainty term is not e. Same-bank confidence describes its specified actual/averaged channel, not an unconstrained future source memory.
- Existing conditional acceptance, calibration, readout, source caps and gate implementation costs remain; exact nominal Pauli identities are not identities for noisy realized gates.
- Native scalar fidelity regret is not a complete-memory norm guarantee. The coherent flag counterexample remains relevant.
- These corollaries neither improve generic SDP complexity nor establish experimental benefit or historical novelty. The focused primary comparison identifies standard recovery-SDP objective and dual precedent.

No mathematical gap found at the stated scope. No receiving of broader unknown-noise recovery, capacity, hardware budgets or generic future-memory prediction.
