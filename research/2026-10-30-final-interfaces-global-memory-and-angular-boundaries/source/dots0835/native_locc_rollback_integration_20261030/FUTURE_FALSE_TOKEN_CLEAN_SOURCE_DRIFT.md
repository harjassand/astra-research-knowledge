# Exact phase-controlled false-token bookkeeping and clean-source drift
2026-10-30. Non-governing future-operator note requested by parent. This is not a continuous-noise threshold, complete full-Hilbert energy inequality, or useful-service CP-credit proof.

## 1. Actual program occupation needs no new validity bit

Use the existing native engine phase to define Bob program occupation:

- occupied in A_i, C_t, B_(j0,l), and R_(p,j) with parent p of type A/C/B;
- empty in I, Q_i, and R_(p,j) with parent p of type I/Q.

This is the correct definition even when the outer master is malformed, e.g. C_t+READ_WAIT or C_t+WANT. Do not use outer BUSY alone, and do not compare the default idle P=0 to Alice's current syndrome.

Every actual Hamiltonian edge preserves this occupation: acquisition stays A; gates stay C; rollback stays B; verification stays Q; abort leaves inherit the parent; cleanup does not change the clock. The prefix watchdog C_t->B_(t,t) also preserves occupation. There is no coherent I/A, A/C or C/Q edge.

## 2. False tokens, not independent per-slot monotonicity

For each occupied DATA reply/held/cache/program token with value a, use the projector that a differs from the CURRENT relevant commuting Alice stabilizer vector. Let F_tot be the sum over all physical tokens (not OR flags). ACK, request, empty and unoccupied-program slots contribute zero. The operator family commutes in the forest frame, together with mechanical history projectors.

Check the actual transitions:

| Transition | Token action |
|---|---|
| reply hop | move value, empty source; false count unchanged |
| Alice HOLD enqueue, only at I | move value to return FIFO, worker IDLE |
| Bob response -> WANT in READ_WAIT | move value from FIFO to cache |
| unconditional discard in other master phase | delete response token |
| Bob LOAD I+WANT(a) -> A0+BUSY, P=a | consume cache token, create identical program token |
| Bob PREFIX watchdog C->B | preserve program token and value |
| Bob T -> Q0+FLUSH_SEND(0) | delete active program and any malformed simultaneous cache token |
| Bob READY/refresh | no new token; program is unoccupied in Q/I |
| Alice clean read SUCCESS | overwrite worker with a TRUE value |
| Alice abort/rollback/cleanup | preserve worker; REQUEST is not a syndrome token |

LOAD really sends WANT->BUSY in the explicit onsite instrument, so it does not copy-and-keep a false cache. If a malformed active C engine also has READ_WAIT, receiving DATA creates WANT but simultaneously consumes its FIFO source; the preexisting active P remains a separate token. No cloning occurs. Alice C+HOLD cannot enqueue before I, and its terminal overwrite can delete an old token while creating its one output.

Bob never changes Alice DATA. Thus nominal Bob changes cannot turn other true Alice-value tokens false. A mechanically clean Alice terminal preserves Alice stabilizers and writes their actual measured value; it cannot create a false token. Every clean Hamiltonian/FIFO transport is therefore false-count conserving or decreasing in the stated source ranges.

## 3. Exact clean Bob source inequality

Let U be the imported integer raw syndrome energy. Let K_U bound its increase under any one allowed bounded Bob correction mask. Let F_P be the false-program projector in a committed C_L source. Compress to the mechanically good source G_h (full owned read/write footprint and correct forest workspace):

- on F_P=0, the terminal is the ordinary GPT instrument, so U is nonincreasing;
- on F_P=1, its bounded mask raises U by at most K_U;
- Alice comparisons and all other carried values are unchanged;
- the program token is deleted by actual terminal reset.

Consequently, for the normalized clean terminal channel Phi_h and any R_token>=K_U,

    G_h [Phi_h^*(U+R_token F_tot)-(U+R_token F_tot)] G_h
        <= -(R_token-K_U) G_h F_P.

Any simultaneous malformed WANT token cleared by terminal only strengthens this inequality. This is an operator inequality within the commuting stabilizer/program blocks on the mechanically clean source; it does not assign stochastic Pauli probabilities. Its rate-weighted jump form follows by multiplying the actual terminal rate. Clean rollback has DATA identity and deletes the active token, so its corresponding compressed difference is <=-R_token F_P.

This observation means semantic useful-service credit is not needed merely to pay a wrong Bob correction's bounded raw-energy increase: its consumed false program supplies immediate payment. False tokens still need an actual transport/healing analysis for the full drift/barrier construction and initialization comparison.

## 4. Dirty Alice hierarchy and remaining obstruction

A mechanically dirty Alice retirement may change only boundedly many Alice stabilizers and its held reply; only boundedly many extant physical tokens compare to those stabilizers. Let n_spawn bound this number, including the new held token. A triangular spectral weight with Alice mechanical defect weight larger than its raw-energy cost plus n_spawn R_token is therefore the natural candidate. Mechanical Bob defects require their own raw-energy payment but cannot create new Alice-value false tokens.

What is NOT proved by this note:

- domination of all good/dirty source cross terms for the full reset adjoint;
- a full-Hilbert multiplicative spectral envelope for U and transported token projectors;
- locality/commutation of the CP energy credits when false tokens are moving;
- the required actual bad-resolvent useful-service construction and noise transfer;
- any positive continuous-noise threshold or arbitrary-controller initialization.

The stochastic-native governing theorem uses classical root/retirement records and does not depend on this future operator route.
