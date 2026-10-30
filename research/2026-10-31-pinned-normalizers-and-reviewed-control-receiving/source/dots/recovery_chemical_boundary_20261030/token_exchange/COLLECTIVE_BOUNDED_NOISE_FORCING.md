# Collective bounded-noise forcing without independent realized labels

30 October 2026. New abstract local theorem. No raw compiler/global transfer is asserted.

## Contract

There are n persistent labels, each with integer rank R_l in {0,...,L}, L>=1. Rank0 is the target. The nonexplosive (or localized) process has these exact generator components, possibly adapted to additional retained state:

1. Each label has a progress clock of rate q>0. If its rank is positive, its progress event reduces rank by at least1; at rank0 it does nothing. A progress event changes only that label.
2. Arbitrary safe events only decrease ranks. Their rates and the number of affected labels need not be uniformly bounded.
3. An adverse event changes at most k labels, where k is fixed. For EACH label, the sum of rates of adverse events involving that label is at most b, uniformly in the actual state/history. Adverse events may be collective, correlated and state dependent, and may choose arbitrary new ranks.

All clocks/rates refer to the SAME actual trace or physical clock. No frozen fiber, independence of realized label trajectories, or small return is assumed. The label count is fixed; deletions and births require separate accounting. The progress component must actually exist in the generator, not just in an averaged law.

Let A_t count rank-zero labels. There are constants c,C>0 depending only on q,b,k,L such that, for 0<T<=1,

    P(A_T < c n T^L) <= exp[-c n T^(2L-1)].             (1)

## Time-dependent test and exact drift

Set g_r(u)=P(Pois(q u)>=r), g_0=1, and phi_r(u)=exp(-b u)g_r(u). Then phi is nonincreasing in r and, for r>=1,

    d_u phi_r=q(phi_(r-1)-phi_r)-b phi_r,

while d_u phi_0=-b phi_0. For a fixed terminal T define

    S_s=sum_l phi_(R_l(s))(T-s),  0<=s<=T.

At time T, S_T=A_T. The time derivative plus the progress generator is at least b S_s: progress drops by more than1 only help. An adverse event can lose at most the sum of current phi values of the labels it touches. Summing its intensity and using the per-label participation bound gives adverse drift >=-b S_s. Hence

    (partial_s + L_progress + L_adverse) S_s >=0.

Safe events have nonnegative increments in S_s. Importantly, they need not be included in a quadratic-variation bound.

## Lower-tail estimate without an independence claim

For F_s=exp(-xi S_s), the contribution of a safe event is <=0. For progress/adverse events use

    exp(-xi Delta)-1 <= -xi Delta + (xi^2/2)exp(xi k)Delta^2,

with 0<=xi<=1/k (enlarge k to max(k,1)). Progress increments have magnitude<=1 and total rate<=qn. For adverse events, Delta^2<=k times the number of touched labels, so the summed quadratic term is <=kbn. Consequently, for a fixed C0 depending only on q,b,k,

    (partial_s+L) F_s <= C0 xi^2 n F_s.

Localized Dynkin/Gronwall and boundedness of F yield

    E exp(-xi A_T) <= exp[-xi S_0+C0 xi^2 n T].

This does not require a bound on safe-event intensity: its exact contribution has the favorable sign. Almost-sure nonexplosion, or an independently justified localization limit for the stated process, is still required.

Let d(T)=exp(-bT)P(Pois(qT)>=L). Initially S_0>=n d(T), whatever the rank configuration. For T<=1,

    c0 T^L <= d(T) <= qT.

Choose xi=d(T)/(4 C1 T), where C1>=C0 is enlarged so xi<=1/k. Exponential Markov at threshold n d(T)/2 gives

    P(A_T<=n d(T)/2)
       <=exp[-n d(T)^2/(16 C1 T)],

which implies (1). All constants are population independent.

## Retention and a weaker but positive reset scale

If a specified cohort starts at rank0, the same proof has S_0=n exp(-bT). Choose a fixed small T0 with exp(-bT0)>=3/4 and a fixed sufficiently small xi. For T<=T0 this gives P(A_T<n/2)<=exp(-c n). The argument applies to the cohort in the presence of other labels if the same per-label participation bound holds.

For arbitrary starting ranks, take T=n^-delta with 0<delta<1/(2L-1). Then

    P(A_T<c n^(1-L delta))
       <=exp[-c n^(1-(2L-1)delta)].

Consequently every fixed inverse grade obeys

    E(1+A_T)^(-s)
      <= C_s n^(-s(1-L delta))
         + exp[-c n^(1-(2L-1)delta)].

This is a positive polynomial reset scale, not the sharp independent-clock threshold. For L>1 the lower-tail exponent is weaker than n T^L; it does NOT preserve previously advertised reset exponents automatically. A signed-cycle application must redo its finite-grade ordering, occupation/time estimates, and all actual terminal/birth/deletion costs.

## Relevance and limitation

A traced face kernel that changes several ordinary labels can fit this contract even when it cannot be represented by single-label independent residual clocks. One must acquire both a bounded batch size and bounded per-label participation intensity for its adverse part. A holding-time/ingress certificate alone supplies neither. A common reset of all n labels violates the fixed-k hypothesis, and the theorem does not conceal that obstruction.

This provides an actual alternative local concentration mechanism for collective face motion. It is not a theorem that arbitrary hidden face kernels satisfy the contract, nor a recurrence result by itself.
