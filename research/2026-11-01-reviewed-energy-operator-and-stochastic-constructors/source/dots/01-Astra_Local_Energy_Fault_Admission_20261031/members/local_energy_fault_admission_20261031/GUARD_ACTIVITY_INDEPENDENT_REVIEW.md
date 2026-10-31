# Separate guard-activity review

31 October 2026. Mathematical PASS after full read of `GUARD_BANDWIDTH_AND_ACTIVITY_NOTE.md`, 3,818 bytes, SHA-256 `671f8b8ae6baa138839ab6052ad51a617f1af0d6e1a18810b7e3264f779840ba`.

The count is exactly the sum of the specified canonical guard loss and injection jump counts. It excludes spectator/environment events, intended control operations and any other unraveling. All real allowed Hamiltonians commute with total guard occupation N: each hopping term raises one guard and lowers another even when its coefficient acts on the spectator; density-controlled terms and guard-independent terms also commute. System-only instruments preserve its expectation.

For qubit guards, the adjoint acts on N as -sum lambda_i n_i+sum a_i(1-n_i). Integrating and using the jump compensators gives the stated exact mean balance, E J_loss=E N0-E NT+E J_inj, and E(J_loss+J_inj)<=E N0+2anT. It does not posit a classical occupation path in between quantum jumps. Unequal loss rates cancel through the same integrated identity.

For u>=0 and W=exp(uN), L_loss^dagger W L_loss=lambda_i exp(-u)n_i W. Counting that jump with exp(u) exactly cancels its ordinary anticommutator term. Injection instead contributes a_i(exp(2u)-1)(1-n_i)W, bounded above by a_i(exp(2u)-1)W. Thus the positive tilted evolution and W>=I give

E exp[u(J_loss+J_inj)] <= Tr[exp(uN)rho_G(0)] exp[anT(exp(2u)-1)].

No normalization/Jensen argument for tilted states is used. The operator inequality remains valid with arbitrary finite source/system/spectator/reference correlations under the initialized Markov-field premise and the spectator domain qualifications already reviewed. The initial weighted factor is real and cannot be replaced by one without a cold-input certificate. System-only instruments leave W unchanged. If injection rates vary deterministically with time, replacing anT by their summed integral is valid.

This exact displayed balance is for the declared qubit loss/injection channels. Additional jump operators, counted spectator events, guard-creating controls, or alternative unravelings require their own contributions. In the illustrative mixed-sector qutrit, injection availability would be its actual input projector rather than automatically 1-Q; a corresponding upper bound may be proved separately, but is not silently substituted into this exact qubit identity.

The conclusion separates activity from bandwidth: fixed physical a permits a lambda-independent emission-count bound. It does not establish that increasing lambda while holding a fixed is physically available. If a scales with lambda, the benefit can disappear. Occupation N is not an acquired thermodynamic Hamiltonian, and these equations are neither heat/power nor entropy-production bounds. A jump-count estimate alone is not a simulation-cost theorem. No hardware mechanism, practical regime, or new threshold result is earned.
