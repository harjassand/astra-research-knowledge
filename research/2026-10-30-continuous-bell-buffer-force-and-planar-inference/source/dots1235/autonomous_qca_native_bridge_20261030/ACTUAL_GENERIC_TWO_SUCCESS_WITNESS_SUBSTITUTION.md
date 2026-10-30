# Actual two-SUCCESS witness for the generic local-channel compiler
2026-10-30. New hardware substitution proof. Separate from the frozen abstract cavity/norm candidate.

## 1. Exact generator choices — no LOCC pipe

Fix finitely many attempted-update CPTP channels Phi_h on bounded full read/write footprints R_h. Synthesize their exact finite Stinespring hub/resource gate lists as in EXACT_NATIVE_ATTEMPT_COMPILER.md. Use the verified rollback alphabet and transitions with these substitutions:

* NO Alice/Bob lab split, FIFO, classical intersite transport, request controller, pending reply or external program capture is present.
* Each hub has one fixed payload type; its attempted guard and all variable control fields belong to the locked QCA payload. There is no private variable P that is read externally during a prefix.
* LOAD is an unconditional fixed positive-rate complete onsite reset from ready I to A0, W=0. It does not require an algorithmic guard or neighboring readiness predicate.
* COMMIT, SUCCESS, clean/dirty abort, nonprefix watchdog, READY, refresh and resource z->free resets are separately resolved ONSITE instruments, identity on the retained external bath. Prefix watchdog C_t->B_(t,t) is also onsite and is identity on W. All workspace erasures resolve every basis label with equal rates.
* Clock/tag monitors are the actual finite onsite Hamiltonian-plus-reset monitor registers of the inherited construction. They resolve clock/tag labels only, not workspace or QCA payload.
* Every Hamiltonian is the stated finite hub/resource edge (or an onsite grouped operation). No multisite dissipative transport is imported.

All rates/amplitudes are strictly positive fixed finite constants. A weak LOAD is allowed, but its actual chosen value enters the new constants. No numerical witness coefficient from the LOCC source is reused.

## 2. Finite full-Hilbert path to two genuine SUCCESS events

Let k=max|R_h|, L=max gate-list length and d=max resource owner incidence. For target h, let Gamma contain h, every owner incident to R_h, and all resources of those owners. There are at most n_c=1+k(d-1) owner hubs and n_c k resources. Boundary-crossing Hamiltonians and all local reset losses touching the proof patch are included in its norm budget.

For any owner g in this patch, ClearOwner(g) needs no acquisition:

1. In I/A/Q/R, take its actual complete nonprefix watchdog/abort to Q0.
2. In C, take the actual prefix watchdog to its B rail. If the rail is consistent, traverse at most L inverse edges and take the clean abort at B0; if inconsistent, use a distinct enabled failed-test leaf and its complete dirty abort. An initial B uses the same latter alternatives.
3. At Q0, release all own o/z tags using o->z->free, pass the local Q verification chain, and take READY to I. Other owners' tags do not obstruct the Q 'not-own' tests.

The conservative selected-step bound is M_clear=L+3k+4. This covers arbitrary malformed phases, ownership masks, workspace states and entanglement. Inverse/forward payload blocks are unitary on the entire workspace+DATA space, so the probability path does not assume good history.

First ClearOwner for h and each of its n_c-1 direct competitors. Park the competitors in I by selecting the no-LOAD/no-I-watchdog part of their actual local record during the remaining finite word; anticommutator losses and all coherent background terms remain in the norm budget. Parking is a selected event, not physical feedback.

All R_h tags are now free: every owner that could own one is among these competitors. From I run LOAD, k acquisition edges, COMMIT, L forward edges and SUCCESS. This takes at most k+L+3 selected steps and is always available; Phi_h's internal marching guard is NOT an acquisition/LOAD precondition. Clear h again and repeat. Thus

    m_2 <= (n_c+1) M_clear + 2(k+L+3)                  (2.1)

selected transitions suffice for two genuine C_L->Q0 SUCCESS events. Early successful terminals can only help a passive count; no particular DATA/measurement outcome is selected. All resolved workspace outcomes are retained.

## 3. Finite monitored instrument effect, not a classical path probability

Apply the exact projected-step/finite-monitor estimate of

    transactional_regeneration_20261029/ACTUAL_RESET_INSTRUMENT_TAIL.md

with this NEW path length m_2, NEW finite physical/monitor count, NEW incident no-jump budget B, NEW positive minimum Hamiltonian amplitude and reset rate, and the actual new clock alphabet. Every hypothesis is checked structurally:

* selected edges have unique nonzero blocks gU, with U unitary on their entire payload space;
* failed tests have distinct leaves, so no selected block cancels another;
* complete erasure losses are scalar on W, and all ordinary losses are clock/control diagonal;
* all main terms are identity on the finite monitor registers;
* all required reset intensities are positive, including LOAD, COMMIT, SUCCESS, cleanup and READY;
* malformed B sectors have a failed-test route, not an assumed connection to the zero endpoint;
* all competing owners are cleared without acquisition, so no recursively expanding blocking patch is assumed.

The monitor proof supplies actual finite flush/read windows and a strictly positive full-instrument lower effect. It does not replace them by instantaneous measurement or independent classical attempts. Substituting the new quantities in its explicit formulas gives finite T_2 and p_2>0, depending on this fixed hardware but not N, such that two genuine SUCCESS events occur by T_2 with effect at least p_2 I on every physical/input/reference state. The outside retained bath is nominally uncoupled from the apparatus and may evolve arbitrarily under its bath-only channel; its initial correlations are retained by the reference-stable estimate.

## 4. Actual killed counter and finite-support witness

Attach a passive classical counter c in {0,1}: the first SUCCESS changes 0->1; further successes leave 1. Delete the SUCCESS gain from source c=1 while retaining its loss. The resulting K_(h,2) is the genuine nominal CP/TNI instrument for fewer than two successes. The alive counter space is {0,1}; no absorbing completed sector is included in the Lyapunov inequality. Starting in counter 1 requires only one more success and is covered by the same conservative path.

The preceding effect gives

    exp(T_2 K_(h,2)^*) I <= (1-p_2)I.                  (4.1)

Apply the anchored finite-support polynomial construction in

    transactional_regeneration_20261029/JOINT_LOCAL_LYAPUNOV_TAIL.md

to THIS new killed generator. Its sole nonunital term remains the local deleted second-SUCCESS gain at h. Nominal finite-range terms annihilate identity away from their tracked support, and the counter is a local analysis factor. Consequently the construction yields new finite-support Z_h and explicit positive constants

    alpha I <= Z_h <= I,
    K_(h,2)^* Z_h <= -r Z_h.                           (4.2)

The polynomial degrees/support radii and alpha,r can be astronomically poor but are finite functions of the supplied fixed channel circuits and physical rates. They are not independent of a LOAD rate later sent to zero. The actual apparatus is chosen before the service window and noise strength.

For buffered separated owners the same exact local product identity yields the joint killed drift. Enlarge the cavity to include each witness, its full owner good-history/forest/read-write footprint, all monitor positions and the relevant generator-range buffer. This proves the service contract needed by the abstract cavity theorem, subject to an independent audit of this substitution rather than a transplanted old witness.

## 5. What is not certified

This establishes fresh attempted-channel service, not marching-guard ACCEPTANCE or the recursive QCA's logical progress. The physical state need not be encoded or correct for the service probability theorem. Good-channel semantics require the separate forest/leading-rectangle arguments. No encoded initialization, externally supplied schedule, data-energy drift, full universal threshold or practical rate claim is inferred.
