# Single lower-level damage island to bounded quantum command holes

2026-10-30. Conditional deterministic interface lemma. It uses the primary classical robust-medium contract and separately charged native service failures. It is not the full native trajectory or quantum threshold theorem.

## 1. Chosen setting and initialization

Use fixed aligned colonies C(x) with bases spaced QB, initialized with the source encoding of a nonvacant classical control computation. Each observer is permanently attached to one distinct unrolled quantum module; it never retargets a later quantum bank. Do not invoke homogeneous self-organization to obtain this alignment for free.

A fully explicit target control program is a serial phase wave along the one-dimensional chain of module indices: module 0 starts ARM, and module g starts ARM only after observing module g-1 in AFTER. Each phase is held for a fixed finite counter length. The sequence is

    BEFORE -> ARM -> RUN -> DRAIN -> AFTER.

AFTER is permanent in the intended virtual computation (a separate time-marking field continues to change). This controls an arbitrary finite sequential gate circuit with permanently assigned wire banks. The phase program is classical and has no input from an unprotected quantum DONE or measurement record. A parallel DAG version requires an explicitly routed classical parent-flag program; it is not assumed here. The serial program does not solve scalable quantum waiting protection.

## 2. Wrong-snapshot wake lemma

For observer base x, let I_x be the inspection interval used in Gács Definition 19.5, of width (3Q+2.2)B. Let one lower-level damage island occupy spatial interval A and time interval [u0,u1]. Suppose there is no higher-level damage and, outside this island, the relevant lower-level trajectory satisfies the source robust rules.

For a snapshot at time t after

    u1 + split_t + T_upper,

assume the current colony passes the actual full structural/package Safe test and is live. The latest switching time t' of the colony lies in (t-T_upper,t], by the lower-level dwell upper bound. Since t' >= u1+split_t, its preceding split_t inspection interval is damage-free. The current colony configuration is unchanged since t'. Its full Safe test verifies the same-work-period domain and the accepted-package condition at t'. Thus t' is the latest admissible time in Definition 19.5 and the physical current package decoding equals the source's decoded macrocell.

This proves soundness outside the island's bounded forward wake. It does not posit a physical detector for the absence of damage. Safe may be wrong during the wake; such observations are charged to the island.

Normal work-period boundary intervals can fail Safe without being faulty. Their effect is NO COMMAND/delay, not an arbitrary accepted command. To guarantee a subsequent successful safe read, use the source's middle-age-band progress bound and the actual fresh two-success observer service. A service miss is charged separately. The resulting correction of a stale command record includes the wait to the next safe band and the finite observer service window; it is not instantaneous at the end of the wake.

## 3. Spatial incidence is independent of codeblock size

An island of width at most beta B (beta=15 in Definition 10.3) intersects I_x for only a bounded number of aligned observer bases. A conservative bound is

    C_obs <= 5 + ceil((beta+2.2)/Q),

hence C_obs <= 6 for Q>=18 (using 8 is a harmless conservative choice). The observer native read footprint may be physically large, but it does not write the read-only source labels. It may change only its own command register and quantum module footprint.

Therefore, apart from separately marked native/timing defects, a single lower-level island can issue wrong accepted commands to only C_obs permanently assigned quantum modules. It cannot acquire a new module identity each time it replays. No descendant DATA are recursively erased.

## 4. Actual module channel and phase serialization

Use ONE full-footprint attempted CPTP channel per module, reading its actual command register C_g and local latch under the same ownership transaction. It performs:

* ARM: initialize the local one-use latch, without erasing incoming DATA;
* RUN with ARMED latch: destructive transfer T_g, then set DONE;
* RUN with DONE, DRAIN, AFTER, BEFORE, or NO COMMAND: identity on DATA.

All DATA-moving elementary edges are controlled on a hub predicate initialized to zero and computed from the locked command/latch snapshot before any DATA motion. Controller refresh and cleanup keep running even in the false-guard cases. Observer writes to C_g also respect its owner tag. A cached ARM command outside this full-footprint transaction is not allowed: it could arrive after a successful RUN and rearm the gate incorrectly.

This common ownership makes phase effects serializable. In a clean history, an ARM transaction whose read was genuinely before RUN cannot complete after a RUN transaction that read the later command: the held command/latch footprint prevents that race. RUN is accepted at most once between legitimate ARM events.

## 5. Phase windows and actual service

Choose the fixed phase counter lengths so each ARM/RUN/DRAIN phase contains a source-certified safe observation band and a sufficiently long native service window. The quantities are chosen from the actual source T_low*, T_upper* and actual observer/module service constants. A failed observation, failed arm refresh, no accepted RUN, or incomplete cleanup is an explicitly charged bad service event. The two-SUCCESS argument removes a possible stale first attempt. Neither acceptance nor cleanup is supplied by a clock label alone.

If the observer and module service events are good, an undamaged module completes its correct transfer before its virtual AFTER state. Hence, along every edge between two undamaged modules, the producer's actual transfer precedes the consumer's transfer. This remains true even when a neighboring damaged module skipped, replayed or falsely completed: the classical virtual phase wave does not depend on its raw native completion bit.

The known clean nominal service proof is in CLEAN_AUTONOMOUS_DAG_AND_SERVICE.md. Applying it inside repaired source windows requires the source-compatible full-footprint construction and the common marked-record/inclusive service analysis; numerical constants are not transplanted.

## 6. Resulting open circuit

Let F consist of the C_obs modules whose observers can be affected by the island, plus every module touched by separately marked native faults or service failures, including neighboring native partial transactions whose full footprints were compromised. Every other module has the intended quantum tensor once, in good-good causal order. The destructive-transfer reset removes pre-production and post-consumption bank contacts, so the physical process is the designated good open circuit contracted with an arbitrary retained boundary comb on the bounded ports of F.

This is the exact receiving premise needed by OPEN_TENSOR_CORRECTNESS_V1.md. It does not turn the comb into an ordinary causal gate fault. Provided the actual fault-tolerant rectangle tolerates all these marked ports with the common full-amplitude decoder identity, its correctness survives the contraction.

## 7. What this lemma does NOT yet establish

1. The observe-delay-commit implementation plus all observers is a strong native trajectory of the Gács primitive medium under the broad continuous joint-bath perturbation model. That is a remaining physical proof.
2. The one-island argument extends to every overlapping/healing hierarchy configuration without enlarging a quantum fault to an entire codeblock. The fixed alignment and full Safe test are part of the stated local case.
3. A time-local norm estimate for each quantum circuit location. A module can wait a long time before or during its live input interval. Old inactive-bank contents are overwritten, but live exposure and control errors persisting into activation still need finite-window charging/protected handoff.
4. A fault-tolerant encoded quantum gadget has been implemented merely because the open-tensor receiver exists.

Thus this is a concrete single-island command/cut bridge, with genuine quantum no-copying and bounded module identity, but not the completed autonomous computation construction.
