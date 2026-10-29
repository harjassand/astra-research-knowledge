# Model-free finite guard around an acquired quantum-program decoder

2026-10-29. Root transfer, receiving review pending. This composes the earlier received full-memory guard with the new physically defined quantum-training decoder. It does not turn IID learning completeness into arbitrary-memory availability.

## Complete port, not a known classical decoder assumption
Before each fresh private role coin, prepare the candidate's finite quantum training registers, references and known controller state. All preparation source calls, rejected training attempts, classical calculations and timing happen BEFORE that coin and may depend on past permitted records. Use public finite caps. A failed preparation either aborts the entire finite guard, or selects a fully specified CPTP fallback port before the coin; it cannot silently omit an already-loaded service payload.

The current complete port consists of one encoded-payload source use followed by the known joint-compression/tomography/recovery ALGORITHM using those training registers. All outputs are returned in the same fixed logical dimension k. Invalid support guesses and infeasible learned matrices have the already specified total CPTP defaults. The algorithm is fixed before role choice; its internal outcomes may be correlated with the current payload, source memory and quantum training state. They are included in the full joint map and are not assumed to identify an independent classical channel.

Bundle the quantum training/program registers, source bath and allowed controller history into memory M. Their state may be arbitrarily correlated. The entire fixed algorithm/current source step is a CPTP map L tensor M -> L tensor M'. The source must not receive extra current-role, current-test-setting or pad-key information through controls/timing/routing. Known trusted controls/storage and private endpoint operations remain supplied; uncontrolled noise during those operations requires its own budget.

## Actual positive test and exact memory effects
On TEST prepare a fresh uniformly selected logical pure-state2-design, run the full port, and perform its matching survival measurement. For k=2 the six Pauli eigenstates and corresponding single-qubit readout suffice. For every current memory density sigma, the actual failure probability q(sigma) and logical Bell loss e(sigma) satisfy
 e(sigma)=(k+1)q(sigma)/k.
This is the standard average-fidelity/entanglement-fidelity identity applied to the actual logical reduced channel. Since it holds for every sigma, it is also an equality of the corresponding memory effects; it is not an estimate on a stationary average source.

On SERVICE apply a fresh uniform logical Pauli key before the port, undo it after the logical decoder, and permanently retire it. Averaging this key gives the exact full joint CP instrument
 sum_P Ad_P tensor B_P.
The aggregate nonidentity Pauli effect has probability e(sigma). Quantum data-dependent tomography/decoder outcomes do not invalidate this algebra: they are part of the CPTP port's Kraus expansion. The full port must be executed on tests too; a cheaper test of only its raw source output is not substituted.

## Finite hazard transfer
Take SERVICE probability s and TEST probability a=1-s. At every allowed refined past history (including virtual service Paulis, excluding retired keys),
 Pr(bad service|h)<=R Pr(test failure|h), R=[(k+1)/k]s/a.
Training before the next fresh role is merely another memory-only operation and preserves the required branch factorization. The same received negative-binomial comparison therefore bounds obtaining t+1 bad services before b+1 failed tests by
 epsilon_NB=sum_(j=0)^b binom(t+j,j) [R/(1+R)]^(t+1)[1/(1+R)]^j.
Abort at b+1 test failures or a fixed cap, accept after J services, and use an actual total Clifford/Pauli outer decoder correcting every pattern of<=t service faults. The earlier aggregate-effect argument then gives
 (1/2)||A_acc-id_payload tensor B_acc||diamond<=epsilon_NB,
including arbitrary initial payload-memory-reference correlations at the received memory-filter scope. B_acc is a memory/transcript CP filter, generally not a scalar acceptance probability. Normalized accepted error can require division by the actual acceptance probability; no availability or per-transcript posterior guarantee is supplied against arbitrary memory.

An explicit small outer choice is the already checked five-qubit code (J=5,t=1), with syndrome-only Pauli correction and a defined action for all1024 error patterns. Thus this transfer does not assume an unavailable length-J field code for one-qubit service symbols. Larger received binary/GRS constructions may be substituted only with their actual correction and typing conditions.

## Resource and comparison scope
Count EVERY training/filter/decoder source call as well as the current service/test source call. If the per-trial preparation cap is Q and the guard cap is L, source calls are at mostL(Q+1), plus any separately declared acquisition/calibration. If physical time passes under the source during decoding, its entire common idle interaction must be included in the port or separately bounded. Protected outer buffers, quantum training storage, known control synthesis, randomness and readout are not protected for free by the guard.

For IID low-support or the stated depolarized mixed-encoding family, the new learner may supply low Bell-loss ports and hence a completeness/yield analysis. For arbitrary causal retained memory the SAME algorithm remains only a candidate: the guard's accepted-operation soundness survives, but its learned-model fidelity and readiness theorem do not. The source could prevent useful acceptance forever. A quantum training block is consumed; its old estimated latent frame cannot be reused on unrelated future original-D payloads.

This is an application of existing authentication-style/private-pad/positive-test machinery to a new acquired-program port, not a new authentication theorem or practical advantage over an equally informed conventional controller.

## Governing sources actually read
Earlier retained source: sequential_singlet_guard_20261029/GOVERNING_v1.md, GENERIC_TWO_DESIGN_CONTROLLER_v7.md, CORRELATED_INPUT_MEMORY_FILTER_v3.md and independent_audit/REVIEW_CORRELATED_v3.md with its receipt. The fresh six-state effect identity and the quantum-program-as-memory substitution are proved above. The received new five-qubit outer syndrome implementation is in noisy_frame_recovery_architecture_20261029 with its separate audit; only its algebraic every-pattern decoder is imported, not its IID error tail. Main low-support decoder and complete fixed-capped defaults remain governed by their own received packets.
