# Root check of the complementary Z trial ledger
30 October 2026. Independent constructive check of Section8 of the full closure candidate, conditional on its stated uniform local clearing/occupation kernels. This does not validate the r-cycle correction.

Write Z=B-N-h I, h=q-m>0, and stop at its first strict change. While Z=z is fixed, B=z+N+hI>=z. The only upward move is active activation (+h). Immigration is neutral or lowers Z by h upon first enabling activity; clearing is neutral or lowers Z by h if activity survives. Fast reactions preserve Z.

## Large N: an actual bounded-stage trial
Choose the fixed N_* large enough for the existing uniform positive-D first-connector estimates, including a fixed probability of clearing with active output. Changes of N by the fixed number of preparation events can be absorbed in N_*.

1. Inactive A=0: wait for the compulsory immigration. No activation, clearing or fast event is enabled. Mean wait is 1/i. It is neutral unless it enables activity (then the trial ends down).
2. Inactive A>=1: wait for the first immigration or activation. An immigration is a neutral trial failure or a down exit. Prescribed activation has probability bounded below for large z and makes activity true without changing Z. The wait has mean <=1/i.
3. Active positive D: run the ACTUAL complete first-connector episode. Terminate the trial there. Clearing with active output has probability >=c>0 for N>=N_*, and is a down exit. Active activation has probability k_T B U <=C B^(1-q) from the uniform local U bound. Other outcomes end neutrally. Physical mean duration is bounded uniformly.
4. Active D=0: its enabled source has A>=m. Stop at the first seed, clearing or connector birth. The seed-to-clearing ratio is fixed because both have common (A)_m(B)_q factor. Its seed probability is bounded below uniformly for large z. If a seed occurs, use stage3; otherwise end at that actual event. Active activation before the seed has probability <=C B^(1-q), and stage3 adds the same bound. Direct clearing may itself be down and otherwise ends neutrally.

This trial contains only a bounded number of stopping stages, not a bounded number of fast jumps. Its down probability is >=c, up probability <=C z^(1-q), and mean physical duration <=C, uniformly in all sufficiently large hidden N. Conditional local kernels are applied to the actual seed output, not an independently sampled reset.

## Bounded N: an actual finite-stage favorable path
Fix N<=N_* (or a slightly larger finite head needed at the regime interface). While inactive and A>=1, prescribe activation followed by the next actual clearing. Activation is neutral and adds m-1 to N; clearing either exits down or destroys activity and removes m. In the neutral case net N decreases by exactly1 and net B decreases by1. The finite active fast graph has an absorption probability bounded below into clearing and uniformly finite B-scaled mean over this bounded N range. This is the existing finite-shell path/value argument, not an assumed stationary law.

Any unexpected immigration ends the trial neutrally (or down if it enables activity); an active activation ends it up. Thus no failed branch is silently recycled inside the favorable finite word. After at most a fixed number of successful neutral pairs, either down occurs or A=0. From A=0 prescribe consecutive immigrations until activity is enabled. At most m immigrations suffice. The first is compulsory. Every later inactive A is bounded by m-1, and B=z+O(1), so each required immigration wins its race with probability >=c/z. If activity appears earlier, it is already a down-Z event. Therefore this finite trial has down probability >=c z^(-(m-1)).

Every active subepisode in this bounded construction has up probability <=C B^(1-q), by its finite-source rate/path bound. There are only a fixed number of them, so total up probability <=C z^(-(q-1)). The total mean trial duration is bounded: inactive waits have the immigration-rate floor and active finite-shell waits have the established bounded mean. Constants can depend on N_* and fixed reaction rates.

## Conditional renewal, without independence
At the beginning of every new neutral trial choose its regime from the actual current N. Both regimes satisfy

 p_down>=c z^(-(m-1)), p_up<=C z^(-(q-1)), E[duration|past]<=C.

Hence the expected number of trials before a strict Z exit is <=C z^(m-1). Summing conditional upward probabilities over these trials bounds the eventual up-exit probability by C z^(-(q-m)). Summing their conditional mean durations gives E[t_exit]<=C z^(m-1). No independence of trial outcomes or holding times is required.

Since every exit changes Z by exactly +/-h, a sufficiently large fixed z0 makes any prescribed exponential-level weight contract on the embedded Z exits. A polynomial factor pays the level holding time. The actual stopped potential for running cost exp(theta_Z Z) is therefore finite and bounded by a polynomial in Z times exp(theta_Z Z), UNIFORMLY in hidden N.

Define that stopped potential as0 below z0. Only active activation can re-enter its domain from the exterior threshold strip, with rate k_T AB and destination Z in a fixed bounded interval. Its positive generator leakage is consequently <=C AB. This is the precise form needed by the global two-potential comparison; it is not a bounded constant on that unbounded strip.

Review obligations remain: use the exact active predicate of the actual graph, verify its preservation by fast reactions, and ensure the cited finite-shell absorption constants and large-N local kernel bounds cover every seed output. These are concrete table/kernel checks. The ledger does not settle Sections2–6 of the r-side proof.
