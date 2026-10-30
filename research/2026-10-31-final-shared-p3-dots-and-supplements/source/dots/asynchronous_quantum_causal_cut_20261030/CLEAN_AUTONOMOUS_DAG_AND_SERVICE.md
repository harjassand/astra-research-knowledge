# Exact nominal autonomous DAG, with actual finite service

2026-10-30. New derivation; no noise threshold asserted.

## 1. Local programmed channel

Fix a bounded-degree finite circuit DAG. Each module g owns one finite classical flag b_g in {WAIT,DONE}, and a permanently assigned output bank. Sources are supplied as ready; the unknown encoded or unencoded input itself is supplied, not prepared by this construction. The initially unused output banks and auxiliary controls have the native compiler's stated initialization.

Let the full read/write footprint of g contain its input/output quantum banks, its flag, and every predecessor's flag. Define a finite CPTP channel Psi_g:

* Measure only these classical flag registers in their designated basis.
* If b_g=WAIT and all predecessor flags are DONE, perform the destructive-transfer channel T_g and set b_g=DONE.
* Otherwise act identically on the quantum DATA.
* Return a classical acceptance bit equal to one exactly in the first case.

The same measured control convention applies to initially off-diagonal flag inputs; clean initialized histories are classical. There is no measurement or copying of the unknown quantum input. The native compiler locks the entire footprint, including read-only flags. Competing terminal updates therefore admit a serial order. Atomic means the exact completed channel semantics of this native compiler, not an infinitesimal generator identity.

## 2. Accepted-only physical parking

Compile Psi_g using the exact finite Stinespring construction. Route the resolved terminal/cleanup branch according to the classical acceptance bit. An accepted branch cleans the workspace, releases all ownership tags, and then enters a physical absorbing DONE mode with no DATA drive. A no-acceptance branch cleans and retries normally. This is different from parking after every SUCCESS: a successful identity attempt with an unsatisfied guard must not park the module.

All additions are finite local classical registers, onsite resolved terminal/reset leaves, and the existing two-site edges. The acceptance bit is carried in hub workspace from the finite channel circuit to the terminal; it is not supplied by an external scheduler. Any malformed/dirty route remains an arbitrary local fault in a noisy analysis, not a clean erase of unknown DATA.

## 3. Exact nominal circuit semantics

On clean native histories, predecessor flags are monotone. A module accepts at most once. Acceptance requires that every producer has already completed, and the transfer resets its consumed banks. By induction in the terminal order, the completed modules form an order ideal of the circuit DAG and their live banks carry exactly the intended circuit state, with all references retained. The native forest frame describes partial transactions between completed terminals. No clock repair, phase modulo, quantum snapshot, or rollback of a completed logical operation is used.

Once all modules park, their quantum output is the intended circuit output. Cleanup/parking time is part of completion; one must not read a controller-coherent partial output early.

## 4. Why two actual SUCCESS events suffice after readiness

Let tau_g be the first time all predecessor modules have completed their physical accepted handoff (or the supplied readiness time for a source). In a clean history these predecessor flags never revert. At tau_g, g may have one transaction already in flight, which read a stale false predicate. There cannot be two such transactions at its single hub. The first subsequent successful terminal might therefore be a stale identity attempt; any later loaded successful attempt sees a true predicate, unless g has already accepted. Thus by the second genuine successful terminal after tau_g, g has accepted.

The generic native two-SUCCESS all-state witness cannot literally hold after parking, since no more successes occur then. Use instead the killed unfinished process, deleting the accepted parking gain while retaining its loss. Before acceptance this process agrees with an unparked comparison implementation. Re-run the finite clearing-word proof for the new alphabet: a competing parked owner already has all tags free and requires no clearing; every unparked owner has the existing finite clear route; target LOAD remains unconditional until acceptance. Add the finite cleanup path to the accepted endpoint. The finite monitored-instrument argument then supplies new constants C,r>0 (and a finite reference-stable effect bound), not numerical constants copied from the old hardware:

    P[ g unfinished at tau_g+t | complete past ] <= C exp(-r t).

This statement is nominal. Under generic generator calibration it must not be interpreted as an actual nominal-SUCCESS record. A noisy version requires the inclusive cavity argument and a new semantic controller theorem.

## 5. Finite-circuit progress

Let L be the number of modules and D the longest module count on a directed path. Set W_g equal to g's completion delay after all predecessors complete. The conditional all-state service estimate implies

    P[ exists g: W_g > t ] <= L C exp(-r t).

On its complement, the maximum completion time is at most D t, by the elementary DAG recurrence. Independence of service times is not assumed. Thus nominal autonomous completion by

    (D/r) log(LC/delta)

has failure probability at most delta, up to the finite choice of a nonnegative service window and constants. This is a safe global upper bound, not a claim of optimal speed.

The circuit's quantum error under fixed continuous noise is NOT controlled by this bound alone. It also does not bound a particular live wire's exposure independently of D. Gács-type repaired control is sought precisely to replace that missing local robustness, not to justify it by naming a reliable classical computer.
