# Useful memory interfaces: result and scope map
2026-10-30. Files in this directory distinguish ordinary constructions, reviewed transfers, and actual remaining hardware obligations.

## Actual autonomous LOCC bridge: now proved in a broader primitive model
**AUTONOMOUS_LOCC_GLOBAL_ENERGY_THEOREM.md has an independent scoped PASS.** A finite-state autonomous machine uses local atomic quantum instruments, measured finite-capacity FIFO channels, actual stochastic clocks and watchdogs. The G+1 SYNC purge prevents stale-packet reuse without growing tags; unconditional response draining prevents full-queue deadlock. Bob reads his current syndrome at commit and Alice never nominally changes her syndrome, so this atomic-instrument version needs no distributed locks.

Arbitrary initial finite controller/channel states are allowed: mark all initially, and bound early bad commits by the reset/commit rate ratio. The proved moment and first-exit argument gives known-Bell target error at most source error plus C(1+t) exp(-cN), with all controller/message faults charged. There is no global correction schedule or reliable classical record assumption.

The scoped PASS is AUTONOMOUS_LOCC_GLOBAL_THEOREM_AUDIT.md, bound to theorem SHA-256 02d6535fc45b5b4187b575b0dc37aba088f4c2c3e5d8ba7d51773a2ca40c5146. Its qualifications include the combined CSS recovery radius, nominal-LOCC versus shared-entangled-bath noise, and the explicitly granted stochastic FIFO channel primitives. Supporting files:
- AUTONOMOUS_LOCC_ARCHITECTURE_AUDIT.md: exact finite machine and stale-message proof.
- FIFO_PROTOCOL_CLARIFICATION_AND_WORD_PROOF.md: unconditional dequeue, deadlock counterexample without it, and a uniform finite service word.
- MARKED_EMISSION_SPACETIME_MGF_AUDIT.md: independent arbitrary-time-set Feynman–Kac bound and all exponent/coloring factors.
- check_fifo_flush.py / .json: exhaustive asynchronous finite-state checks for five capacity pairs.

**This is not the native two-site-Hamiltonian/onsite-reset compiler.** Its atomic local read/table/correction instruments are an explicitly stronger quantum primitive. LOCAL_QUANTUM_ROLLBACK_COMPILER_CANDIDATE.md now gives a concrete next mechanism: an onsite watchdog transfers a live local quantum prefix to an inverse-prefix rollback corridor, retaining locks/program until a zero-prefix reset. Clean aborts are DATA identity, and Alice's terminal syndrome can be exported as a measured classical pointer. LOCAL_ROLLBACK_INSTRUMENT_AUDIT.md independently passes the clean inverse-prefix cancellation, coarse-grained identity abort and positive integrated reset-window bound; five operator regressions pass in check_local_rollback.json. The full malformed-state no-creation, retirement-tail, semantic-taint and good-service composition remains a separate compiler proof.

## Strongest useful recipient interface
**Known distributed Bell resources can avoid both a high-energy preparation-frame decoder and an immutable measured-syndrome baseline.** Raw physical Bell pairs already belong to the coherent shared-syndrome Bell-target span. Measure checks on each side, compare DIFFERENCES, and correct relative errors. The common syndrome is harmless to this known target. A concrete scheduled implementation uses fixed-iteration Tanner decoding, noisy bounded-depth classical processors, physical corrections, and fresh per-round records. The full raw physical Bell byproduct also permits direct switching between two such signed-sector links without converting them to the zero-syndrome code. More usefully, the same resource teleports an UNKNOWN already-encoded input into the standard zero-syndrome recipient code, preserving arbitrary logical/reference entanglement.

This is a constructive ordinary purification/buffering/switching path, NOT a novel entanglement-purification identity. It consumes N physical Bell pairs, ongoing two-sided check extraction, O(N) classical communication per round and fixed physical propagation times. Arbitrary unknown-state loading and reliable bare-output extraction remain separate.

**The reviewed native coherent controller is not yet a distributed LOCC controller.** A joint coherent Stinespring payload touching both parties can supply quantum communication during unfinished prefixes. The broader-model theorem above is a real autonomous alternative, but an audited local quantum-module/message composition is still needed to inherit the ORIGINAL native hardware theorem. Merely observing that a completed local-GPT channel is LOCC does not close that gap.

Core files:
- BILATERAL_BELL_BUFFER.md: scheduled construction, contraction/resource accounting.
- BILATERAL_BELL_ALGEBRA_AUDIT.md: independent exact target/gauge instrument, raw-pair initialization, common-error and decoder scope.
- BILATERAL_SCHEDULED_CPTP_ADDENDUM.md: frozen common-record/coherent-gauge proof closing the scheduled retained-bath step; target error at most twice the uniform bad-record mass, not arbitrary-joint-logical identity.
- SIGNED_SECTOR_BELL_SWITCH.md: exact full-physical-mask switching; fixed-latency controller seam explicitly charged. Independent receipt: SIGNED_PHYSICAL_BELL_SWAP_AUDIT.md.
- SIGNED_BELL_ENCODED_TELEPORTATION.md: exact unknown encoded-input transfer through a signed resource into the standard recipient code convention. Independent receipt: SIGNED_BELL_TELEPORTATION_AUDIT.md. Tests cover 4096 exact input-operator cases, 8192 input/resource error cases, and an additional 20480 dense matrix checks.
- TANNER_CLASSICAL_DEPENDENCY_AUDIT.md: independent check that the actual parallel decoder has bounded depth/fanout for fixed iteration count, including invalid-local-syndrome defaults and deterministic ties.
- check_signed_bell_swap.py / .json: all 4160 syndrome/outcome cases for two small CSS codes pass, with gauge-instrument completeness.
- NOISY_CLASSICAL_ORDINARY_COMPARATOR.md: constructive adaptation removing ideal classical gates from fixed-iteration scheduled memory cycles under the same bounded-incidence local-stochastic location model. Constant depth/fanout is checked against the actual Tanner algorithm. Does not remove an external schedule or solve growing-depth final decoding.

## Independently reviewed persistent-baseline bridge
For general pending-frame preparations, one can instead protect an unknown fixed syndrome coset using one SHARED noisy baseline. A fixed sparse baseline error creates a biased GPT energy with a static O(|D|) floor. It need not itself be a valid global syndrome.

- PERSISTENT_BASELINE_GPT_ANALYSIS.md: unconditional finite work, active-hub density/window/rooted contraction with static defects charged once. Frozen SHA-256 74a81ece8148f2b8b81f6b30869050a53ff7ae1c65062e3383d018a7cff04b17.
- PERSISTENT_BASELINE_GLOBAL_ENERGY.md: simpler linear-cutoff total-energy first-exit proof and exponentially long native stochastic-noise buffer. Frozen SHA-256 342558fa4a3430a21f8b5884615323ac0b0fbaffac2520df11a0049ec12ccbd1.
- Independent PASS receipts are in producer-workspace/INDEPENDENT_REVIEW.md and GLOBAL_ENERGY_REVIEW.md.

Load-bearing qualifications: component restrictions also restrict eta to the selected defective views; one fixed common baseline per view is required; the initial bad-event tail must be uniform as a positive preparation/record-instrument bound for a diamond claim; output is in the full forest-dressed DATA frame. The proof supplies globally small reduced residual weight, not a local-stochastic residual distribution. Stable shared baseline WRITE/storage/access remains real hardware, and independently drifting hub copies can destroy the common energy. The two-owner oscillation counterexample is explicit.

PENDING_FRAME_HANDOFF.md is a separate controlled F_new P F_old† seam candidate, not an accepted noisy physical compiler or factory feedforward theorem.

## Earlier useful workload and exact ordinary boundaries
1. **Zero-syndrome encoded Bell switch:** ENCODED_BELL_SWITCH.md reuses the already reviewed controlled destructive CSS readout and adds a transversal CNOT. Matched column grouping makes the Clifford operation onsite and preserves the support certificate. BELL_INTERFACE_AUDIT.md is an independent scoped PASS. All incompatible controller motion and whole-forest frame inversion must be handled; no free quantum tail or mode switch is assumed.
2. **Fixed bare-port error floor:** BARE_PORT_NO_GO.md gives an N-independent first/last-depolarization-event floor for unknown bare-state loading/retrieval through a fixed-dimensional bounded-rate port. Ordinary limitation, not new physics.
3. **Delayed-basis task:** DELAYED_BASIS_GAME.md proves the exact optimal measure-first/classical-storage success (1+2^(-k/2))/2, including an explicit optimal collective POVM; quantum encoded waiting plus the established readout can approach one.
4. **Subthreshold-access boundary:** SUBTHRESHOLD_ACCESS_BOUNDARY.md applies information-disturbance: any recipient disjoint from the retained decoder registers is nearly input-independent if its coupling lies inside the storage theorem's correctable perturbation class. It cannot quietly become a useful output/control port.
5. **Rare-link synchronization:** WAITING_RESOURCE_CALCULATION.md gives mean arrival-time improvement p^(-2) to O(p^(-1)); for p=exp(-alpha N), alpha<c, a memory with error C poly(N)(1+t)exp(-cN) retains an exponential reliability margin. The SAME advantage is available to a conventional quantum buffer with equal resources.
6. AUXILIARY_AUDIT.md independently passes the bare-port, delayed-basis and subthreshold-access ordinary arguments.

## Primary preparation comparison and initializer transfer
- PREPARATION_BASELINE_2411.md: Bergamaschi–Liu supplies genuine physical residual-error envelopes for encoded Bell/GHZ preparation. Exponential factory reliability at linear distance uses O(N²) resources. Its instantaneous feedforward assumption and general Pauli versus retained-bath CPTP scope must not be silently imported. Its good-event LS bound is used subnormally, not after rare postselection.
- PREPARATION_2609_BOUNDARY.md: the newer confinement-only theorem's matched ideal final recovery does NOT by itself supply a native-basin initializer; its stronger soundness branch has a physical LS-residual guarantee under its stated model.
- INITIAL_SEED_SLAB.md: an actual LS physical residual at clean controller initialization can be paid as an initial witness layer, with no ideal cleanup and with subnormalized successful-factory events.
- CONTINUOUS_INITIALIZER_HANDOFF_AUDIT.md independently passes root's complementary LS-support-to-animal-moment/gentle-basin transfer, conditional on the reviewed continuous-noise Tanner simple-compiler theorem. It does not solve factory runtime feedforward.

## Honest comparison and next exact action
The ordinary competitor gets the same Bell sources, graph connectivity, message channels, finite control stages and noisy local gates. Fixed-iteration single-shot Tanner recovery is already a strong constructive competitor and need not have perfectly reliable classical gate circuitry. No numerical/practical hardware advantage has been established.

Next action for the ORIGINAL native Bell-resource claim: instantiate the local rollback/syndrome-export module with its complete label/claim table; prove malformed-state no-creation and actual retirement; compose semantic taint with FIFO purge and local locks; recompute dressed noise/service constants; then audit the full-mask endpoint with live frames. The broader atomic-local-instrument autonomous theorem is already established in its declared model and should neither be understated as merely scheduled nor overstated as the native compiler.
