# Productive-pool forcing despite an initially unbounded C/Y reset rate

30 October 2026. New local candidate. This is a resource-consuming pool mechanism, not an additional named chemical network or an integrated theorem.

There are n persistent labels divided into a source pool C and a working pool W, size Y=n-C. Working labels have ranks0,...,L, L>=1; rank0 is target. Source labels are not targets. Assume:

1. Source membership is irreversible during the episode. Each source label has a genuinely allocated entry subrate gamma>0 converting it to a working label of rank<=L. Extra conversions may help. Allocated physical rates are not double-counted.
2. Each working label has genuinely allocated rank-progress subrate q>0, with designated rank decreasing by at least1 and any collateral working changes safe.
3. Other working-rank changes are safe or adverse. Each adverse event touches at most k EXISTING working labels, and each working label's total adverse participation intensity is bounded by

       b0+b1 C/(1+Y).

   A source-entry event may also cause such an adverse batch; its actual participation is included in this bound. New labels from C are not part of a previously selected working cohort.
4. The exact process is nonexplosive and all generator allocations use the same clock. No births, deletions, or return from W to C occurs in this local statement.

Then there are constants c,K>0 such that for0<T<=1,

    P(A_T<c n T^(L+1))<=K exp[-c n T^(L+1)],         (P)

uniformly in the initial pool/rank configuration. In particular the initial adverse bound may be of order n when Y is small; no uniform initial per-label bound or small return norm is assumed.

## Proof

If initially Y>=n/2, select a working cohort of size floor(n/2). Monotonicity keeps Y>=n/2, so its adverse participation is bounded by b0+2b1 throughout. The root product theorem yields the stronger threshold/order n T^L. This implies (P) after adjusting constants, including small n.

Otherwise C>=n/2. Attach independent potential entry clocks of rate gamma to the initial source identities using the actual allocated subgenerators. Any identity whose first clock rings by T/2 must have entered W by then; an earlier extra conversion only helps. Consequently Y_(T/2) dominates Binomial(floor(n/2),1-exp(-gamma T/2)). Chernoff gives

    P(Y_(T/2)<c0 nT)<=exp(-c1 nT),

when nT is above a fixed constant. On its complement select M=floor(c0 nT) working labels measurably at time T/2. They remain working thereafter. Since Y cannot decrease, throughout the second half their adverse bound is at most

    b_T=b0+b1 n/(1+M)<=B/T,

where B is fixed. Apply the conditional root product theorem to this selected cohort for horizon T/2. Its exponential damping exp[-2^(k-1)b_T T/2] is bounded below by a positive CONSTANT; the progress Poisson factor is bounded below by c T^L. Thus the actual target count at T is at least c M T^L>=c' n T^(L+1), except with conditional probability exp[-c' n T^(L+1)]. Add the first-half failure. Small nT can be absorbed by the fixed prefactor K, since then nT^(L+1) is bounded.

The cohort is selected at a deterministic midpoint from past information only. No conditioning on future survival, restoration or successful ranks is used. The singular C/Y rate is paid by actual growth of its denominator, not declared bounded from the start.

## Scope and a warning about profiles

This is a deterministic-time target-forcing result. Its extra T factor records the necessary source-to-working preparation stage. It suggests a killing-time scale with effective depth L+1, but no such upgrade or incoming-profile preservation is asserted here.

In fact an A-only incoming inverse profile can FAIL to be preserved: productive growth can dilute a small existing target population before killing. The separate PRODUCTIVE_POOL_PROFILE_OBSTRUCTION.md gives an explicit example. Any whole Green/section integration may need a carried profile involving both A and Y, rather than simply reusing f_s(A). Returning working mass to C or allowing unbounded adverse batches also lies outside this theorem.
