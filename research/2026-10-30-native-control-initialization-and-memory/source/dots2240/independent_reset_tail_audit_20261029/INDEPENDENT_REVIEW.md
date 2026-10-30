# Independent audit: actual transactional reset tails

Audit date: 2026-10-29 UTC. Inputs are pinned by `SOURCE_SHA256.txt`; copies of the four principal source files and both original regression programs are retained here. Original sources were not edited. This review is independent of the source documents' acceptance language.

## Finding and acceptance boundary

No mathematical obstruction was found to the two tail statements **as conditional theorems for the stated monitored, noiseless, local generator**. The event definition, full-alphabet repair paths, CP killed-effect iteration, finite-time local polynomial construction, and buffered product argument are compatible with the reset-first transactional variant. This is not implementation certification and not a data threshold. The finite fixture contains no workspace matrices, Hamiltonian amplitudes, or monitor implementation, so it cannot certify their operator hypotheses. No acceptance is given to those absent implementation checks.

### 1. Actual event and changed architecture

The source generator has distinct A and C phases, an irreversible complete A_k→C_0 commitment instrument, and no coherent A–C edge. Its claims predicate disables coherent cleanup in every R label. The terminal/abort event, and only that event, is an exit to Q_0 with complete workspace overwrite. Commit, ready, workspace refresh, cleanup, and monitor emissions are not designated events.

Deleting actual designated gains while retaining their losses produces a CP trace-nonincreasing killed instrument. Its effect is exactly the no-designated-event probability operator; the CP diamond norm equals its effect norm. Thus a full-state lower bound p on an actual event by T implies N_h(T)^*(I)≤(1-p)I and permits iteration after arbitrary preceding no-event records. No structural bad-projector estimate is substituted here.

### 2. Full-alphabet paths

ClearOwner handles arbitrary inconsistent A/Q/C by a specific failed-test abort and reset; all R labels reset directly. Consistent C runs forward to terminal, never back into acquisition. Consistent Q removes its own unverified tags and verifies; consistent A reverses its acquired prefix. These operations never acquire new resources while clearing competitors. Including every owner incident to a target resource excludes omitted target blockers. Including all their resources makes every selected operation patch-supported. Boundary-crossing interactions must remain in B, as the document requires.

The per-owner M=L+3k+4 and total m bounds are conservative. The short C/R_C invariant-sector argument is correctly distinguished from the one-window bound for arbitrary R: R_A can coherently return to A and R_Q to Q. An explicit R_A→A counterexample was independently checked; it is not a defect in the current text, which expressly excludes unrestricted short-bound iteration.

### 3. Finite monitored paths to the CP contraction

The probability proof requires complete physical sites in the patch; a unique eligible gU block acting unitarily on the entire dirty workspace/data sector; clock-diagonal complete no-jump losses; and bounded incident norms including every crossing term. Under these assumptions the outside-only CPTP evolution commutes with a selected patch operation. The second-order Hamiltonian contribution is g²δ², with a bounded local Dyson remainder, uniformly on arbitrary outside/reference states. Bundled reset completeness is essential to the reset-step lower bound: coherent summation of workspace Kraus channels would invalidate the premise.

The finite reset-monitor model has total loss identity on clock/data/workspace and hence autonomous monitor timing. Its F_u is strictly positive by the two-level observability argument. A resolved reset at each monitor flushes arbitrary initial monitor entanglement; after conditioning on timing, subsequent clock instruments can be compared with simultaneous label projections without dividing by the rare-window probability. The approximation must concern the complete recorded instrument, not individual label outcomes. The documents explicitly make this requirement. An absorbing analysis flag can count designated events during flush/measurement windows; it must not label commit as success or introduce a physical reset. These conditions justify the stated positive finite p and T, not any claim for an unmonitored generator.

### 4. Arbitrary finite T local polynomial

The anchor is necessary: K_h^*I=-A_h is not zero, so an empty-support/unital expansion would fail. With h retained in every tracked support, the connected term expansion yields C^q(s)_q uniformly in volume. Small-step Taylor tails with δC≤1/4 are valid; subdividing arbitrary finite T and increasing K_j as the tracked support grows avoids extrapolating one short-time Taylor disk to large T.

O_j and F_j are polynomials in the same fixed K_h^*, so K_h^*F_j=O_j-I holds exactly. Endpoint error ≤η controls drift without applying an extensive generator norm to a state-approximation error. Contractivity bounds accumulated O_j errors; integrating them plus local integral errors gives the stated conservative (T+δ)η bound. Since a≤T, the displayed bounds imply (a/2)I≤F_h≤(3T/2)I and drift ≤-(p/2)I. Normalization gives αI≤Z_h≤I and K_h^*Z_h≤-rZ_h with the claimed conservative constants. The support radius can be enormous but is finite and volume-independent under fixed geometry and rates.

### 5. Joint product and exterior

The required separation is not just disjoint initial resource sets: no generator term may touch two witness supports. Under this buffered separation, each ordinary local adjoint factors through all untouched positive factors and annihilates the product if it touches none. Each deleted actual gain is local at its own anchor. This proves the exact K_S^* product identity even with an interacting exterior. The complementary factors commute with every drift contribution, so multiplication preserves order. CP comparison then gives the spatially extensive killed-instrument bound. Packing a bounded-degree graph gives the stated weaker arbitrary-set exponent; no statistical independence or future exterior-record postselection is needed.

### 6. Actual versus nominal reset caveat

The optional perturbation argument is conditional on retaining the same actual separately recorded reset channels in the physical perturbed generator. Merely knowing L+N is CPTP does not ensure that subtraction of the old nominal gains remains a CP killed instrument. The text correctly states this restriction. Under it, local identity-annihilating perturbations and their incidence budget give the displayed α^(-b) drift cost. This certifies record tails only, not reset-output correctness, quantum serialization, or bounded data faults.

## Fresh evidence

Executed only copies in this new audit directory:

* `python check_transactional_flags.py`: PASS, 29,160 states, 143,676 transitions, 98,172 computation-owned-lock continuation checks.
* `python check_reset_paths.py`: PASS, 58,320 full-alphabet constructed paths, maximum 25≤46; 44,550 C/R paths, maximum 4.
* `python independent_graph_checks.py`: PASS. Independently built reverse graph distances to **owner-specific terminal/abort** events; every state reaches each owner's actual event, maximum shortest distance 17 for both owners. Checked 2,295 commit edge typings and 80,447 owned-tag preservation instances in R. Confirmed R_A can escape to A without a designated event, preventing an unsupported all-R short-sector iteration.

The supplied path checker continues beyond an early target event and records target h in its local `seq` entries even while clearing j; only lengths are read, so this does not undermine its eligibility/length receipt. It is not an event-flag implementation test. The independent reachability check explicitly distinguishes the event's owner and type.

## Remaining unestablished items / blocked actions

No tool or permission block occurred. No empirical quantum implementation was supplied to check unique amplitudes, complete reset losses, or monitor records; these remain stated operator hypotheses rather than verified implementation facts. No numeric trajectory test can replace that missing specification. Data-instrument factorization, schedule independence, completed-update-index fault bounds, and a data threshold remain outside this audit and unproved by these files. No source failure was repaired or hidden.
