# Acquiring reset and finite grades from the raw graph

30 October 2026. Unreviewed construction following GRAPH_TAGGED_COHORT_OCCUPATION_INTERFACE.md. The additional assumption here is a positive `2D -> a+D` rate. This supplies an accessible source when almost the entire residual mass is D. No full-network recurrence assertion is made.

Use the same physical first-episode stop sigma, n, a0, m=a0+2, b>=q. Write f_s(A)=(1+A)^(-s). The preceding note supplies polynomial absorption moments and an initial-a cohort depletion probability C n^M exp(-c a_in). Its proof and actual stop conventions are prerequisites, not assumptions of recurrence.

## 1. A uniform low-a arrival clock

Take K=n^alpha with 0<alpha<1/(2L+1), rounded and with small n handled separately. Stop a low stage on reaching a>=K, clearing, D=0, or a connector event. Seeds restart the arrival calculation at their actual output. Use u=integral D dt_op.

Before the next seed, D is nonincreasing. Thus a phase with D>n/2 can be followed by a phase with D<=n/2, but cannot recur before that seed. In the former phase, below a=K, the `2D -> a+D` channel increases a at D-clock rate at least cn. A-consuming conversions have rate at most CK; the seed loss rate is at most CK^2/n. Hence the stopped a drift is at least cn/2 for large n. Dynkin's formula (freeze a at its pre-jump value at terminal clearing/connector stops) gives expected D-clock duration at most CK/n, since the stopped value is bounded by K plus a fixed jump size. Other D-consuming births increase a. A seed or reaching D<=n/2 ends this subphase and uses its actual output.

In the latter phase there are at least n/2 type particles. Up to the next seed, retain them as independent reference Q-chains, with births adding particles. Prescribed paths give P_i(X_u=a)>=c u^L for u<=u0. At

    t_*=C(K/n)^(1/L)

the reference a-occupancy has mean at least 4K. The chance a has not reached K and no earlier stop has occurred is at most exp(-cK), by pathwise containment in a Poisson-binomial lower-tail event. No conditional independence after survival is claimed. Horizon failures restart at the actual state; since D cannot increase without a seed they stay in this second regime.

Seed interruptions have a bounded geometric total before clearing. Each actual restart again has one of these two regimes. Horizon-only failures have conditional probability exp(-cK). Conditional positive iteration therefore yields

    E u_low <= C[(K/n) + (K/n)^(1/L)] <= C t_*.

This remains valid when connector/dormant stops intervene, since they only terminate the stage.

## 2. Low terminal costs and high continuation

Below a=K the clearing D-clock rate is k0(a)_2/D<=CK^2. Thus clearing before reaching K costs at most CK^2 t_*. Dormant entry costs at most CK t_*, because it can occur only at D=1. Connector immigration and activation D-clock rates are bounded by a constant uniformly in b>=q:

    i/[(b)_q (A)_a0 D] <= C,
    tAb/[(b)_q (A)_a0 D] <= C,

using a0>=2 and b/(b)_q bounded. Thus the probability of ANY terminal event before reaching K is at most CK^2 t_*.

At the first a>=K, apply the tagged-cohort result with that actual input. Except on probability C n^M exp(-cK), a stays above cK until sigma. Any terminal connector/clear output changes A by at most a fixed constant; a dormant birth increases it by one. Therefore, for every fixed s>0,

    E f_s(A_sigma) <= C[K^(-s) + K^2(K/n)^(1/L)
                           + n^M exp(-cK)].

This includes the actual output on all four terminal types, not merely clearing conditioned on success. Set alpha=1/(Ls+2L+1) to obtain the explicit reset

    E f_s(A_sigma) <= C_s n^(-eta_s),
    eta_s=s/(Ls+2L+1)>0.

For time, low-stage physical duration is at most C u_low/(b)_q and low occupation is at most C K u_low/(b)_q. Before high-cohort failure, clearing hazard is at least c(b)_q K^m, and its compensator gives high time <=C K^(-m)/(b)_q and high A-occupation <=C K^(1-m)/(b)_q. After failure, the independent polynomial moment bound pays C n^M exp(-cK)/(b)_q. Hence

    (b)_q T <= C[t_* + K^(-m) + n^M exp(-cK)],
    (b)_q U <= C[K t_* + K^(1-m) + n^M exp(-cK)].

Choosing, for example, alpha=1/(4L+2) gives some explicitly positive power decay n^(-eta) for BOTH T and U, uniformly over every active positive-D input. No false O(1/n) rate is asserted.

## 3. Recover all fixed finite inverse-power grades

For any fixed s>=0, the following bounds follow:

    E f_s(A_sigma) <= C_s f_s(A_in),
    (b)_q E integral_0^sigma f_s(A_t) dt
        <= C_s f_(m+s)(A_in),
    (b)_q E integral_0^sigma A_t f_s(A_t+m-1) dt
        <= C_s f_(m+s-1)(A_in).

The first is trivial at s=0. Here is the actual acquisition argument, rather than an assumption of profile stability.

Put x=1+a_in and split at x=C_s log(2+n), with C_s chosen after the finite polynomial moment constants. Below this logarithmic threshold, the uniform polynomial resets of Section 2 dominate every required inverse logarithmic power: the output reset proves the first bound, the uniform T reset proves the second, and the uniform U reset proves the third.

Above the threshold, stop at the first cohort depletion a<c x. Before that stop, the clearing compensator and A>=c x give respectively

    f_s(A_output) <= C_s x^(-s),
    f_s(A)/(A)_m <= C_s x^(-(m+s)),
    A f_s(A+m-1)/(A)_m <= C_s x^(-(m+s-1)).

At high A, the physical clearing intensity is exactly a fixed constant times (b)_q(A)_m, up to the fixed offset convention, so these pointwise inequalities pay the stopped occupation integrals. After depletion, the probability C n^M exp(-c x) times coarse polynomial moment bounds pays all continuation costs. Increasing C_s makes this error smaller than the desired incoming inverse power. The terminal output changes A by bounded amounts, so the same argument covers its profile. Only finitely many requested s are needed; no uniformity as s tends to infinity is asserted.

The different thresholds are deliberate. A logarithmic threshold suffices to prove each fixed graded bound because its constant can depend on s. The common log-squared good set in the previous note dominates every fixed polynomial error simultaneously for the finite collection used by a closure.

## 4. Scope and consequence

Shortest paths, finite jump bounds, and a tagged-cohort concentration construction now acquire: a uniform polynomial reset, all fixed finite power-spending grades, and the SAME-episode good-input occupation ratios. The two-edge arrival obstruction is preserved: the acquired reset exponent depends on graph distance, and nowhere is an O(1/n) direct-source clock imported.

The tools are conventional finite-state/branching concentration and stopped compensators; the constructive choice is to trade a tailored rational resolvent for logarithmic good sets and coarse polynomial absorption costs. This is an acquisition mechanism for this raw module class, not a universal algorithm for arbitrary weakly reversible networks.

The exact off-section dormant Green, phase-weighted signed source, correction, complementary strip, and clock/Foster patch still have to be transferred with these altered exponents and thresholds before any broader full recurrence result. In particular the positive-D bad-source scale would be n^(-eta), not the old 1/n; the correction weights must change accordingly. The completed frozen four-species theorem is not enlarged by this note.
