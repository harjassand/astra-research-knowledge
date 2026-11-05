# Recovery construction target and strongest existing comparisons

The [opening](README.md) proves necessity. The [independent fault-tolerance notes](package/independent/fault_tolerance/opening.md), [transfer audit](package/independent/transfer/burst_candidate_audit.md), [primary sources](package/SOURCES.json), and consolidated [report text](package/report_text.txt) identify the unproved positive operation.

## Isolated Toom repair is not a burst-recovery theorem

The two-dimensional north-east-center rule takes the majority of a site and its north/east neighbors. On an otherwise correct uniform background, errors in an a-by-b rectangle vanish within a+b-1 synchronous rounds and do not leave it. Monotonicity reduces this to the full erroneous rectangle, whose surviving sites satisfy `(a-1-x)+(b-1-y)>=t`. Thus an isolated radius-R corruption has an established O(R) repair mechanism.

But isolated regions cannot simply be superposed. Singleton errors at (1,0) and (0,1) each disappear in one round, while their union creates an error at the origin. A diagonal of m+1 such errors survives m+1 rounds. Independent per-fault recovery regions need not contain the interacting evolution.

Toom also erodes a finite island of the desired bit in an opposite blank background. Infinite prepared-phase stability does not construct the finite commissioned input, and mutable expansion/decoding metadata cannot be treated as fault-free. Preserving the input's meaning through interactions is the actual task.

## Exact large-burst scale and an unproved recurrence

For a spatial block `[-L,L]^d` over duration L/v, the expected number of radius>=L bursts intersecting it, including centers outside the device, is

```text
mu_L=(lambda 2^d alpha/v) L^(d+1-alpha)
      *sum_(j=0)^d binom(d,j)/(alpha-j).
```

Occurrence probability is at most mu_L. At geometric scales `L_(k+1)=B L_k`, the proposed construction must prove that a large bad block requires either a large physical burst or two sufficiently separated bad subblocks with a justified joint-probability bound. The desired recurrence is

```text
p_(k+1)<=C p_k^2+D lambda L_(k+1)^(d+1-alpha).
```

This is a target, not an established property of the current mechanism. The deterministic two-subblock implication, dependence control, finite-seed encoding, local recovery/transfer and finite readout remain missing.

If earned, the algebra can close with `p_k<=A lambda L_k^-beta`, beta=alpha-d-1>0. A fixed block's long-mission term would then scale as `lambda T L^(d-alpha)`, matching the fixed-device ceiling's exponent. Expanding through scales would accumulate a summable term proportional to `lambda r0^-beta/(1-B^-beta)`, matching the seed-extent exponent. Neither conditional deduction proves such a gadget exists.

## Existing machinery sets a strong comparison standard

Toom stability and contour methods already supply robust local memory under their noise hypotheses; polynomially likely large fault supports do not automatically satisfy the usual exponential support bounds. Gacs's reliable cellular automata, including the corrected 2024 work, already address repair of organization and evolving hierarchies. Self-maintenance in general is not an absent invention.

Poisson hail is the most important comparison. Existing workload-stability results already cover strict Pareto regimes compatible with alpha>d+1 when service time is proportional to radius. Another workload moment theorem alone would not earn the selected consequence. One must reduce a causal information-preserving local process to that workload construction, or find a stronger obstruction. A footprint-wide queueing maximum is not automatically a physically implementable decoder.

Vacant Boolean percolation has a close moment boundary in ambient dimension d+1, but an offline undirected vacant path is not an online recovery protocol. Disaster contact processes already show why catastrophe geometry matters; survival with reliable erasure flags does not supply recovery under unflagged data/control corruption. Recent local-memory rules and adversarial quantum fault-tolerance theorems are further strong ingredients with different assumptions about initial encoding, classical computation and waiting-time protection.

The source's targeted comparison leaves a substantive construction gap. It neither establishes priority nor proves no existing theorem can be translated to close it. The selection should be replaced if an existing method already supplies the same finite-seed, local-control and readout operation.

## Retained alternatives and their rejection reasons

The [continued-operation response opening](package/independent/transfer/response_opening_rejected.md) uses fresh private signs against predictable nuisance, with dissipation giving a physical nuisance-energy bound. It avoids equilibrium preparation under its stated contracts, but strong semiparametric identification already supplies the central regression mechanism. A delayed-return counterexample also prevents extrapolating finite acquired response to arbitrary future prediction/control.

The [first-principles alternative](package/independent/first_principles/assessed_opening.md) obtains private-reassignment support bounds; established private-code scrambling is the strong comparator. The [root screening](package/root_screening.txt) retains another rejected energy/locality-only opening. These are reusable scoped deductions rather than selected new capabilities. P2's accepted loaded-LTI/private-timing preparation remains intact; continuous energy influx, arbitrary horizons and spatial burst recovery have different premises.
