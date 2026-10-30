# Completing service substitution for the classical snapshot/timer/commit hardware

2026-10-30. Independent derivation by `producer-workspace/challenge_live_busy_energy`. This is an actual all-state nominal service result, not a clean DATA-channel theorem or a Gács simulation.

## 1. Governing implementation, including dimension-sensitive choices

This supplement applies to the observe-delay-commit and two-SUCCESS latch files frozen in `reviewed_sources/`, and to the complete tick/opportunity implementation in the corrected central-box source. The author independently confirmed the following exact choices during review:

1. Every snapshot payload gate is controlled nondestructively by the physical counter c, is identity on the timer stage, and leaves c unchanged until its terminal SUCCESS. Implement the c<2/identity alternative by block-controlled unitaries, not by swapping the control into an unprotected computed register.
2. Persistent X, S, c and timer registers are NOT private native workspace erased by LOAD/abort/READY. Native reset formulas act as identity on these payload registers except for the explicitly declared snapshot, SUCCESS and COMMIT maps. Clean prefix ABORT reverses the actual snapshot Stinespring list before erasing private workspace.
3. Native finite monitors resolve the inherited native clock/tag labels, not the n+1 timer values. Their physical site count and alphabet are unchanged as n varies. All other terms are identity on monitor registers.
4. The timer and opportunity processes are complete onsite CPTP channels at fixed rates λ and κ. Group each complete family as one onsite generator when estimating norms. Their generator cb norms are at most 2λ and 2κ, and their summed no-count losses are λI and κI. Keeping individual resolved leaves for the physical instrument does not oblige one to sum n separate norm upper bounds.
5. The SUCCESS family has uniform complete source effect κ_SUCCESS P_CL, identity on the incoming persistent payload, even though its outputs increment/reset c and the stage. All workspace, counter and stage outcomes are retained when designating SUCCESS. No probability is conditioned on one timer-stage outcome.
6. The FREE-opportunity family is the ENTIRE family with tag FREE, comprising its nonready identity leaf and its enabled commit leaves. Its complete source effect is κ P_FREE. It does not require timer readiness.

These are actual finite-dimensional implementation choices, not imaginary Poisson marks added to an existing guarded process. All are compatible with onsite dissipators and the accepted two-site native alphabet. The resulting constants may be extremely small, but are uniform in timer length n for this family.

## 2. SNAP: fresh constants, not the old two-SUCCESS constants

Let k be the maximum observer resource footprint, L the length of its fixed snapshot payload gate list, d the resource owner incidence, and n_c<=1+k(d-1) the number of owner hubs in the finite conflict patch. None depends on n. The fixed snapshot circuit copies a fixed classical neighborhood; the n-stage timer is not implemented by an n-long coherent payload circuit.

Use the actual generic ClearOwner routine already audited: nonprefix watchdog/abort to Q0; for a prefix use its prefix watchdog, inverse B rail, and clean abort, or a distinct failed-test/dirty-abort branch; then remove own o/z tags, verify not-own predicates, and READY to I. It acquires nothing. A safe bound remains M_clear=L+3k+4. Arbitrary workspace, S, c and timer states do not block this path: the inverse/forward payload matrices are unitary on their ENTIRE input space, and the reset families have complete uniform source effects.

Clear the target and its direct competitors and park each cleared owner, INCLUDING the target until its own LOAD is selected. Retain the no-LOAD/no-watchdog part of their actual record, with its real losses. Run target LOAD, k acquisitions, native commitment reset, L forward gates and SUCCESS. A one-SUCCESS word length is at most

    m_1 = n_c M_clear + k + L + 3.

Suppress timer and commit-opportunity counts touching the finite patch throughout this fixed word and its finite monitor windows. This is a selected subset of the actual complete-count instrument, not physical control. Its extra survival cost is exp[-(N_tick λ+N_opp κ) T_path], with fixed finite site counts. Crucially it is independent of n. The payload source blocks remain unitary with the same lower edge amplitude. Complete SUCCESS/reset families remain uniformly trace-norm preserving on arbitrary stage/counter inputs up to their fixed scalar intensity.

Apply the accepted actual finite-monitor theorem with NEW B, m_1, site count, g_min and reset rates. B includes all boundary-crossing terms and the new scalar losses. Monitor windows are compared as complete recorded instruments; no sum over n stage outcomes and no inverse rare-outcome probability occurs. This yields fixed T_1,p_1>0 such that the actual one-SUCCESS event A_1 obeys

    A_1^*(I) >= p_1 I

on every physical state, retained bath and reference, uniformly in n. Nominal bath dynamics are bath-only under the governing service theorem; initial correlations are allowed.

Require one SUCCESS in each of two consecutive windows. Actual CP composition gives

    (A_1 compose A_1)^*(I) >= p_1^2 I.

This event is contained in two SUCCESSes by 2T_1, so T_2=2T_1 and p_2=p_1^2 are a fresh full-state two-SUCCESS bound. No independence or inherited numerical constant is used. A passive alive counter {0,1} counting these actual leaves gives the CP/TNI killed process for fewer than two. Its counter is separate from the physical three-state cycle latch.

## 3. FREE: service independent of timer readiness

For the local resource tag at x, include EVERY owner that can hold that tag and all their resources in a finite patch. There are at most its fixed incidence d_x owner hubs. Clear and park them by the same acquisition-free routine. The x tag is then FREE; no omitted owner can hold it because the tag alphabet/owner incidence is the actual finite one.

Keep unwanted loads and all interfering timer/opportunity counts suppressed during this finite selected path, then select the next FREE-opportunity family at x. Sum its nonready and enabled branches. The family has effect κP_FREE, so it succeeds with a fixed lower probability independent of c, timer stage, S, X and bath/reference correlations. One must not select only the enabled commit leaf here: readiness may require n ticks and would spoil this uniform path length.

A safe word length is d_x M_clear+1 plus any fixed bookkeeping/idle steps. Reapply the monitored-path estimate with its own new constants, obtaining T_F,p_F>0, uniform in n, for at least one actual FREE opportunity. This is not a guarantee of a commit before the timer is ready. Once ready, readiness persists and a FREE opportunity does commit, as separately proved by the physical cycle algebra.

## 4. Exponential tails and finite-support killed witnesses

Both resulting event complements are actual CP/TNI instruments. Full-state contraction at a fixed time iterates, giving

    ||N_a(t)||_diamond <= C_a exp(-r_a t)

for a in {SNAP,FREE}. The bound applies at deterministic boundaries after arbitrary incoming conditional states. It does not assign nominal records to a generic perturbed generator.

For the finite-support witness, apply the accepted anchored polynomial construction to EACH new killed generator. The only nonunital contribution is its local deleted event gain; its intensity is at most a fixed νI. The group norms/ranges of the nominal generator, the finite contraction time, and the positive contraction all have uniform-in-n bounds above. The construction therefore yields finite-support witnesses

    α_a I <= Z_a <= I,       K_a^* Z_a <= -r'_a Z_a,

with positive α_a,r'_a and support radius uniform in n. One uses local completely bounded norms of the grouped channels, not a Hilbert-space-dimension-dependent estimate. For the SNAP witness the alive counter has only two states. Taking the minima over the two test types yields the α,r used in the fixed-grid companion.

Actual numeric values are obtained by substitution into the existing explicit monitor/path and anchored-polynomial formulas; this supplement establishes their finite positive and n-uniform character. It does not import a previous machine's numerical coefficients. Any implementation that measures the timer as part of an n-growing monitor alphabet, resolves and postselects one stage outcome, allows extra active-stage resets, or synthesizes an n-long snapshot circuit falls outside this uniformity argument.

## 5. Consequence and limitation

With λ,κ and the snapshot circuit fixed, δ=n/(20λ) grows while α,r and the packing geometry may be held fixed. Hence both α^{-1}exp(-rδ) and 2exp(-n/24000) tend to zero. This removes the proposed parameter-order circularity for the stated physical implementation. After choosing one finite n and its hardware, choose the perturbation budget; no rate or dimension then varies with computation size.

This result supplies SERVICE and witness inputs to the deterministic-grid mixed norm calculation. It does not prove that an arbitrary dirty SUCCESS performs a valid classical table update, a physical Gács command, or a quantum logical operation. Those semantic claims require their separately stated clean/freshness argument.
