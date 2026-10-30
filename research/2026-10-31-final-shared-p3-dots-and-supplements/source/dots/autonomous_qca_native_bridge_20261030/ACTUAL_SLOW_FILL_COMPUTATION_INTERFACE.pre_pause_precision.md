# Actual finite-rate interface for bounded-hop computation

Status: candidate composition of the exact bounded-hop lemma with the reviewed native service/cavity construction. No full purge/clock threshold or reliable flag is assumed.

## 1. Fresh physical mode and actual timer

Fix one finite quarantined domain H with frozen true boundary, feasible lift/range and hop cap D as in `BOUNDED_HOP_ENVELOPE_WITH_DIRTY_AUXILIARIES.md`. Every interior update is its own native small-write attempted channel, and full read/write ownership persists through the write. There are n=|H| such channels.

A supplied ACTUAL entry instrument puts a separate finite program register into CALCULATE and resets its timer. This is a physical local preparation, not an assumed clean prior timer. Use a separate onsite Lindblad jump

    J_fill=sqrt(mu) |FILL><CALCULATE|.              (1.1)

All other nominal terms commute with the CALCULATE/FILL label and do not change it. Their action may be controlled by that label. Consequently, after the actual entry reset, its first transition has the true exponential waiting law, independent of the current auxiliary/DATA input. The reset channel is a physical system-only onsite channel and is included in the generator; no nominal record is appended to an arbitrary perturbed process.

More elaborate finite Hamiltonian/reset clocks can replace (1.1), but then their fresh actual early/late bounds must replace the formulas below.

## 2. Correct computation event, not a trusted completion bit

Let T_s be a fixed native service window. For each local channel, the reviewed newly constructed two-SUCCESS witness bounds failure of two actual terminal completions in that window by p_s, uniformly over its full initial state, boundary/data inputs and retained bath. The first window is a burn-in: each owner's possible dirty first retirement is followed by a clean completion, after which all owners stay in the clean forest sector nominally. Their tuple registers may be arbitrary; that is allowed.

Set K=2D+2 and T_c=K T_s. In each of the following2D+1 windows require the actual two-SUCCESS event for every local update channel. These are correct fresh-snapshot updates, not observe–delay–commit records. There is at least one complete sweep per window, so the exact envelope has converged before T_c. Extra correct updates leave it fixed.

If the actual FILL transition occurs in [T_c,T_b], every subsequent clean fill transaction, after acquiring its full read footprint, sees the correct envelope. In-flight auxiliary prefixes are not read through: ownership waits for their completed current snapshot, and the virtual envelope is already a fixed point. The claim concerns this actual transactional read, not an arbitrary physical-time observation of partially written resource registers.

A union bound for the genuine nominal/cavity instrument gives

    p_bad ≤ n K p_s + mu T_c + exp[−mu(T_b−T_c)] . (2.1)

The early-transition term uses P(T_fill<T_c)≤mu T_c. The late term is a conservative exponential tail. No independent auxiliary initial state is needed, and no rare outcome branch is normalized.

Choose finite D/domain first, then T_s to make the service term small, then mu small for the early term, and finally T_b sufficiently large for the late term. All constants are physical fixed rates/durations independent of total computation size. Physical noise accumulated during T_b is not omitted: it enters the same marked-box norm budget and can force a much smaller final noise threshold.

## 3. Broad continuous-noise boundary

Under arbitrary bounded local HP generator perturbations with an actual joint CPTP propagator, the nominal service records in §2 need not exist as a subinstrument of the actual evolution. Apply the separately reviewed CP noise-cavity construction to the FULL finite physical domain and witness patches. In the cavity, the system-only onsite reset channels and timer are genuine, so §2 defines an actual compatible instrument. The mixed Boolean expansion then charges noise restoration and service/timing failure without fictitious actual records.

For simultaneous domains, joint exponential bounds require the corresponding packed service and timer witnesses; a one-domain union bound is not automatically an inclusive fault-path bound. The local statement (2.1) does not silently remove the existing cavity overlap exponent.

## 4. Scope

This supplies a finite-rate alternative to a perfect 'converged' flag for a fixed correct quarantine. A prematurely corrupted mode/timer is a real physical fault, not an innocent schedule choice. It does not validate the source domain, its frozen collar, boundary-source identities, overlapping purge epochs or the later quantum causal cut. Those remain separate construction obligations.
