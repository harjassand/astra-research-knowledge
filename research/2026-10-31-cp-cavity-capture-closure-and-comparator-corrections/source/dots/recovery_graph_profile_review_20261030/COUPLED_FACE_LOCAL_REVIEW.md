# Independent coupled-face local challenge

30 October 2026. Reviewed frozen `COUPLED_FACE_TRACE_GREEN_AND_POOL.md`, SHA256 `7171cb36d0987df4e1478f94ad9250cec8dbdb7c32fa81f76842feaf2e744610`, copied into `coupled_sources/`. This is a new local review, not an application of the old independent-Q proof and not a global recurrence review.

## Verdict

**Accept the stated local interface with the explicit labeling/forcing and trace-cost details below.** I found no counterexample under the precise positive-rate reaction list. In particular, the old D=0 return norm remains non-small. What is acquired is a different, actual stopped module with true dormant boundary F={D=0,CE=0}, not a renamed estimate for the old boundary.

No whole-network conclusion follows from this review. The retained face labels and actual seed outputs must still be carried by any subsequent full connector transfer. I did not independently reassess the literature comparison or novelty.

## 1. Trace dynamics and protected pool

On every positive-D state, z=E+D-1>=0 and the pooled count a+C+z=n-1 is constant before terminal events. The beta/gamma moves leave these three counts unchanged. The conversion C->E consumes one C label and creates one z label; E->a and 2D->a+D consume one z label and create one a label. Their combined common-clock rate is

    r0=mu E+rho(D-1)>=min(mu,rho) z.

The a+D birth supplies additional z->a transitions when z>=1. At z=0 it instead exhausts the sole protected pool particle and exits F; it must not be continued as an illegal negative-z transition. A birth can also enter F when C=0,E>0,D=1 and z>0. That is simply an earlier true terminal event, so the pooled construction is stopped there too; z=0 is sufficient, not necessary, for such a birth exit.

The labels needed here are **abstract labels of pooled (a,C,z) particles**, not fixed physical E/D molecule identities. This distinction makes the construction precise. Give each z label an independent baseline c=min(mu,rho) clock. Their aggregate cz rate is at most r0. Split a baseline mark between the actual E->a and 2D->a+D reactions in proportions mu E and rho(D-1), and assign all residual rate r0-cz and a-born rate to adapted extra z->a moves. The aggregate physical reaction intensities are then exactly correct. Within the E+D pool labels may be reassigned, including the protected designation, because physical rates depend only on counts. This does not lose any pooled tag. The a and C baseline clocks similarly have the exact aggregate rates nu a and lambda C.

At a mixed-face hold, trace time is frozen. A reverse jump returns to positive D without changing the pooled state. A seed changes one or two a labels into z labels; it is a genuine seed mark, not an unpriced reverse event. Clearing and connectors terminate. Thus trace-time elimination introduces no hidden downward-a moves beyond a->C and seeds.

## 2. Adaptive extras do not destroy forcing concentration

Independent Q-chain paths would indeed be false here: z->a has adapted extra rate. The forcing construction avoids that assertion. For each label, suppress nu rings on the whole interval, require a lambda ring in its first third and a c ring in its second third. From any initial pooled type, this puts the label at a by the endpoint. Extra z->a moves cannot undo the event because the no-nu requirement then retains a. Rings at the wrong type are simply ignored. The event has probability at least c1 t^2 for 0<t<=1 and is independent across labels conditional on pre-interval history.

For an original-a cohort, at deterministic u<=1 the initial no-nu event gives a constant occupancy probability. At u>=1 apply the forcing event on [u-1,u], regardless of each label's adapted state at u-1. The independent forcing indicators give a binomial lower bound on the reference occupancy even though reference trajectories themselves are dependent. After a seed-deleted tag is continued fictitiously, its extra moves can be suppressed; the same forcing condition still works. Actual surviving tags differ by at most two deletions per seed.

The downward-crossing compensator needs only the marginal small-count bound and downward reference intensity <=nu times cohort size. It does not require independent positions at a random crossing. Reference seeds are not downward jumps because deleted tags are continued; their deletion count is charged separately by the geometric seed tail. A deterministic exponentially long common-clock horizon, paid by the polynomial moment bound, therefore gives the claimed polynomial-times-exp(-c a_in) depletion estimate. Mixed holds add no crossings except their actual seed endpoints.

## 3. Exact mixed holding costs

A beta entrance from D=1 produces outgoing e+1>=1. Its entrance rate times expected normalized hold is bounded by beta/[gamma(e+1)]<=beta/gamma. An a-born mixed entrance produces a+1; when its rate is nonzero, outgoing seed/clear intensity is at least c a(a+1), giving a uniform bound on kappa a times the mean hold. Connector stopping only decreases the hold.

Multiplying by any fixed power of 1+A changes these bounds by a fixed constant, since A changes by zero or one at entry. For physical time the ratio of common factors at entrance and hold is also bounded, so the same statement holds after division by `(A)_a0(b)_q`. Sum these actual entrance compensators under localization, condition at each entrance, and use the independently proved absorption moment to remove localization. This pays the total mixed occupation by positive-D occupation with the corresponding weight, regardless of how many mixed returns occur. It does not bound or assume a small count of returns.

For low-stage stops this argument remains valid with holds truncated at the actual seed, high-a hit, or terminal event. If the a-born entrance itself reaches the high cutoff, no subsequent hold is charged to the low stage. Initial mixed holding is a separate term, not omitted from this entrance sum.

## 4. Accessibility, absorption, and actual stopping

A mixed state can take its reverse edge first. At positive D, two type particles can be sent to a along paths of length at most two and then cleared. One type can be converted to a then used in an a-born birth; if this reaches F it already terminates the stage, otherwise clearing follows. With no types, the positive 2D channel supplies one. The finite path budget H=9 is sufficient. All required normalized rates have fixed positive lower bounds and totals are O(n^2).

Requiring every prescribed holding time to be <=1 gives a success probability c n^-2H in each deterministic H-unit operational block. Conditional block iteration earns all polynomial moments without independent blocks or prior recurrence. It also bounds the common clock by n times operational time. This establishes the moment prerequisite for both the tagged horizon and mixed-cost localization.

The only actual F entrances from positive D are a-born jumps from D=1 with CE=0. Beta entrances always have C>0 and outgoing E>=1, hence are mixed rather than true dormant. Reverse and seeds go to positive D. No omitted mixed-to-F fast edge exists. Clearing and connector outputs remain separately stopped, even if their output happens to lie in F.

## 5. Low arrival, resets, and return exponent

Before a seed, apply independent forcing indicators to the n-1 current labels. At t*=C sqrt(K/n) their mean forced-a count is at least 4K. Failure to hit K without an earlier stop is contained in the small forced-count event, not conditioned on surviving to the horizon. Seeds restart at their actual state; their total count before clearing has a geometric tail across both positive-D and mixed holds. Horizon failures have conditional probability exp(-cK). The same truncated chunk-count inequality as in the graph review therefore gives E u_low<=Ct*.

Positive-D operational time is at most common-clock time; the exact mixed Green pays the rest. Low clearing costs O(K^2 t*), connector stopping O(t*), and true dormant entry O(Kt*). High continuation uses the earned cohort and the actual clearing hazard, including during mixed holds. Ratios to that hazard pay high physical time K^-m/(b)_q and A-occupation K^(1-m)/(b)_q, rather than an unsupported upper bound on A. Bad-cohort continuation is paid by polynomial moments.

The reset balance is K^-s versus K^(5/2)n^-1/2, giving K=n^(1/(2s+5)) and exponent s/(2s+5). The high true-F terminal compensator costs C/K; with low cost K^(3/2)n^-1/2, K=n^(1/5) yields n^-1/5. Polynomial-times-exponential cohort error is negligible. These are estimates for the same stopped M-stage, not for the old D=0 hitting law.

For initial mixed states with a<K, ce>=c+e-1=n-a-1 gives the stated small initial hold and low terminal-event probability. Reverse/seed outputs have positive D and unchanged n, so their actual mixture inherits the uniform bounds. At high a, the holding cost has the clearing grade and bounded output shifts; alternatively the cohort starts before this frozen-clock hold. Thus no initial mixed occupation is missing.

Finally, the original logarithmic-input split transfers because all fixed moments, uniform resets, and cohort depletion bounds have now been earned for this exact M-stage. Predictable true-F jump compensators give V_p/[(b)_q U]<=C x^(a0-p) for p>=a0. The initial physical holding lower bound absorbs error relative to U. The proof obtains all fixed grades and same-episode ratios without manufacturing independence or importing the old small D=0 norm.

## Acceptance boundary

This is a substantive coupled-face local construction: exact mixed holding preconditioning, a pooled trace with independent forcing clocks despite adapted extras, and new true-boundary profiles. It validates neither the full signed-cycle operator with its two true dormant face labels nor a global deficiency-two recurrence conclusion. Those remain separate tasks.
