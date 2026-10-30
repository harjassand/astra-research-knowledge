# Independent collective incoming-grade completion review

30 October 2026. Frozen source SHA256 b89aa2a25a144cf8ed9afc51d4b41828d873eee07b50be6079c2091d4a5370e4, copied to `token_sources/COLLECTIVE_INCOMING_GRADE_COMPLETION.md`. Dependencies are the separately reviewed collective forcing and killed-Green contracts.

**Verdict: accept equations (1)-(4) as local fixed-population sufficient estimates, with the pre-terminal stopping clarification below.** No physical-clock or global signed-cycle import is accepted.

## Generator and Green estimate

For f_s(A)=(1+A)^(-s), only adverse events that touch an existing target can increase f_s. If such an event lowers A by d, then d is at most the number of target labels it touches. For A>=2k the mean-value estimate is bounded by C d f_s(A)/(1+A), and summed touched-target intensity is at most bA. For A<2k, the rate of events touching any target is at most bA, their positive increments are bounded, and f_s is uniformly bounded below on this finite range. At A=0 no event can lower A. This proves the positive-drift bound uniformly, without bounding the arbitrarily fast safe component.

The grade-2s deterministic-time estimate and unconditioned Cauchy-Schwarz give exactly the stated integrand bound. On block j, its geometric factor is 2^(-j/2) and its exponential growth factor is at most exp(C_(2s)(j+1)t_n/2). For sufficiently large n depending on the fixed grade, their product is summable with a uniform ratio less than one. The integral is therefore at most C_s t_n f_s(A_0). Neither a survival-conditioned rank law nor independence of killing and the actual state is assumed.

## Pre-terminal stopping clarification (binding)

For the displayed independent Cox mark, there is no simultaneous underlying label jump, so direct optional stopping gives the claimed pre-jump observable. If another terminal mark is itself an underlying label jump, ordinary optional stopping of the unchanged process gives its POST-jump value, not its pre-jump value. The source's sentence about using the pre-jump state needs the following precise construction.

Freeze an auxiliary observable at the pre-terminal value: follow the original A until the first terminal mark, suppress that mark's label update for this observable only, and hold its value thereafter. This is a stopped marked-process construction, not a change to the physical output. Recompute its generator bound: suppressing terminal safe/progress jumps does not introduce positive increments, and all remaining positive increments still satisfy the same adverse touched-target bound. Thus its discounted f_(2s) process is a nonnegative supermartingale with the same constant. Optional stopping now legitimately bounds exp(-C_(2s)tau) f_(2s)(A_(tau-)). Physical output updates remain separate and are never silently suppressed in the terminal kernel.

Geometric block survival implies E exp(C_(2s)tau)<=C_s for sufficiently large n, since exp(C_(2s)t_n)/2<1. Cauchy-Schwarz then yields the pre-terminal incoming-profile bound. The displayed kill has A>=m and removes at most m targets, so its actual output satisfies f_s(A_out)<=(m+1)^s f_s(A_(tau-)). Consequently the marked output expectation obeys (3). No analogous output statement is granted to unbounded-loss exits.

## Stronger-output reset

On the low-input displayed-kill event, f_(s+p)(A_out)<=f_s(A_out). Apply Cauchy-Schwarz to that event using the already earned grade-2s OUTPUT preservation and the actual low-input kill probability C K^m n^-delta. The result is C f_s(A_0) K^(m/2)n^(-delta/2). On high input, bounded target loss gives f_p(A_out)<=C K^-p, and grade-s output preservation pays the remaining factor. Balancing these terms with K=n^[delta/(2p+m)] proves (4), for sufficiently large n so K>=2m. All constants and the finite threshold may depend on the finite requested grade list.

This is stronger output grade s+p versus incoming grade s. It does not claim an extra population-small factor for equal grades. The distinction is necessary for initially large target populations. Time-weighted profiles, changing n, immigration/seed accounting, activation credit, exact physical-clock conversion and the full section/Foster construction remain separate obligations.
