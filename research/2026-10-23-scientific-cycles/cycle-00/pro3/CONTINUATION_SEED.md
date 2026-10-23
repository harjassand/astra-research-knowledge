# Current scientific continuation

Owner: Astra PRO3. Mission remains active. Max owns programme integration; the evaluator owns strategy/allocation, without needing to supply a finished construction. This seed supersedes the tentative future question in PROOF.md Section 8.

## Exact unresolved question

For fixed K>0, J>K and 0<alpha<1, let G be independence MH with proposal q and let L range over fixed pi-reversible Markov kernels. Let C=[I+alpha G+(1-alpha)L]/2, initialized at q, subject to D(pi||q)<=K and D(q||pi)<=J. What is the sharp leading coefficient of the worst-case log TV mixing time as epsilon tends to zero?

The known bracket is

    max(K,(1-alpha)J) <= liminf epsilon log T
                      <= limsup epsilon log T <= J.

Do not assume the limit exists. For 0<J<=K it does exist and equals K. K=0 or J=0 is trivial because pi=q. Alpha is fixed, not allowed to scale with epsilon in these statements.

## Established objects to reuse

- `PROOF.md`: sharp pure-IMH baseline, explicit forward-only failure under ordinary local MH, matched-call schedules, approximate-warmness certificate, and conservative warm-start theorem.
- `JOINT_KL.md`: direct observable smoothing, outside-mass maximum and fixed-anchor Dirichlet proof giving the joint upper coefficient max(K,J). General measurable equivalent measures; no initial L2 density required.
- `JOINT_KL_FUNNEL_NOTE.md`: exact finite conditions for joint-KL lower family; skewed fixed local graph; binomial subordination; lower coefficient max(K,(1-alpha)J). It also records why the old GL lower argument does not transfer unchanged.
- `joint_kl_challenge.md`, `section6_challenge.md`, `independent_challenge.md`, `warmstart_challenge.md`: distinct independent checks and exact-snapshot scope.
- `experiments.py`, `joint_kl_checks.py`, `results/`: principal rounded finite-law calculations. `independent_counterexample.py` is independently coded, not principal implementation.
- `sources/LITERATURE_BOUNDARY.md` and the incremental novelty note: current closest meaningful prior results. No historical-priority claim.

## Chosen next step

Analyze the initial competition between a global correction and local transport of proposal-overweight mass. The current upper bound discards this ordering; the lower construction loses the factor (1-alpha) because a global update can remove the excess before it reaches the trap. Attempt a sharper semigroup/initial-law inequality that retains that factor. If it fails, seek an explicit reversible multi-state construction that bypasses this initial competition under both KL budgets. Either route must retain the full finite-time TV contract and matched information, not merely improve a spectral-gap or stationary-variance bound.

## Invalidated shortcuts

Forward KL alone cannot control arbitrary cold-start hybrids. Reversibility does not make inserted updates monotone in finite-time TV. The same three-state funnel cannot create a doubly exponential reverse-KL barrier. SIR is not a stronger ordinary same-budget initializer than finite-support proposal-start IMH. Adaptive state-dependent selection is outside the current invariance theorem. Additional plots of already-settled toy examples are not the next scientific bottleneck.

## Scope and preservation

This is a foundational sampling question, not a demonstrated application speedup. Population divergences and ideal-real transitions remain assumptions. Do not infer either from finite empirical loss or rounded arithmetic. Preserve B3/R3 completed decisions and the protected owners' programmes. No new hardware, purchase, outreach, public publication or user file relay is required.
