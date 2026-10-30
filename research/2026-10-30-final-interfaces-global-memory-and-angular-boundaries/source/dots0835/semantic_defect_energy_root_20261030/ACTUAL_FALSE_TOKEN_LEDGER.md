# Actual false-value token ledger for the native LOCC machine
2026-10-30. Root candidate following inspection of EXTENDED_MACHINE_AND_OPERATOR_PROOF.md and DELAYED_ALICE_TAINT_AND_SERVICE.md. This is NOT the governing stochastic theorem and is NOT an accepted continuous-noise extension.

## Why a token sum is better than a per-link OR
A Bob wrong-program terminal can change DATA while some other stale packet remains in the FIFO. A per-link OR may therefore stay1 and cannot pay that terminal's DATA cost immediately. Count the actual value-bearing tokens instead. The specified machine moves/consumes packets rather than cloning them, and a successful Bob terminal consumes its private program.

For a private Alice-to-Bob communication patch h, compare each value a against the CURRENT commuting Alice stabilizers requested by h. Count a false token at:
- Alice HOLD(DATA(a));
- every occupied DATA(a) response-FIFO slot;
- Bob outer WANT(a) (its cache);
- Bob private active program a, using the phase-controlled validity below.
ACK, SYNC, READ, empty slots and REQUEST carry no syndrome-value token. Include every actual finite value-bearing location, rather than only the Bob cache. All of these predicates are diagonal in physical classical registers and Alice stabilizer projectors in the forest frame; they commute each other and the DATA-independent mechanical history projectors.

## Private program validity without an unmodeled extra bit
The existing separate ready phase I is essential. Declare a program token present in A_i, C_t, B_(j0,l), and R_(p,j) whose parent p is A/C/B. Declare it absent in I,Q_i and R leaves whose parent is I/Q. A failed-test Hamiltonian connects p to a leaf with the SAME validity; forward/rollback/acquisition Hamiltonians also preserve it. COMMIT preserves the program. LOAD I→A0 creates the program token while changing WANT(a) to BUSY, consuming that cache token. Complete T retirement goes to Q0 and deletes the program token. This definition is independent of outer master coherence/malformation, so a malformed C+READ_WAIT still has its actually used program counted.

Counting P=0 as a token in every idle I state would create an artificial extensive defect population whenever Alice's syndrome differs from0. Counting validity only through Bob's outer BUSY bit would miss malformed active engines. Both alternatives are rejected. The current phase-origin R labels appear sufficient; verify against every actual reset before accepting the ledger.

## Proposed exact nominal accounting
- Clean Alice terminal writes a true token and overwrites any older HOLD; it cannot increase false-token count.
- Enqueue/HOLD clearing, FIFO hops and response acceptance transfer the same token; unwanted replies are discarded.
- LOAD moves WANT to private P, so does not duplicate a false token.
- Prefix watchdog retains the program/validity; clean rollback/retirement deletes it.
- Clean Bob SUCCESS with true program performs the ordinary relative-syndrome GPT move, lowering U or leaving it unchanged.
- Clean Bob SUCCESS with false program has bounded local U increase K_B but deletes at least that false token. Choosing R_token>K_B makes U+R_token D_false nonincreasing on this source.
- A dirty Bob retirement heals its own mechanical flag, changes only bounded Bob DATA, and can discard its program/cache; it cannot create Alice-value false tokens elsewhere because Alice is unchanged.
- A dirty Alice retirement can alter bounded Alice checks and overwrite one local held reply. It can thereby make a bounded number of stored tokens false in neighboring private patches. A larger Alice-history weight pays this finite fanout and the bounded raw U increase.

In the forest frame every nominal Hamiltonian is DATA identity and preserves immutable programs, phase validity and packet values. Thus it should commute U+D_false+mechanical-history energy. Classical packet transitions are basis-resolved; complete quantum reset envelopes must still be proved for nonmonomial dirty DATA action. The bounded-local-spectral-range argument in TRIANGULAR_RESET_ENERGY.md is available, but does not replace the actual source/target checks.

## Remaining decisive obligations
The token accounting may yield a genuine nonincreasing raw exponential potential, rather than an imaginary history of faults. It does NOT yet give a uniform negative drift: false packets can wait, useful correctors can be delayed, and quantum engines can be busy. One needs actual full-purge service/finite local credits and useful-operation density, with all shared masks and controller correlations retained. A final T event need not clear every in-flight false token. Existing stochastic ancestry/count results do not automatically supply this continuous operator credit.

Any extra nominal packet copying, a LOAD that retains an independently reusable WANT value, or a phase/reset that changes program validity without the matching token source would break the proposed monotonicity. Such a finding must change the real machine or the potential, not be absorbed into an unearned assumption.
