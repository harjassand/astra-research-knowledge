# Arbitrary-time-set marked-emission moment: independent proof receipt
2026-10-30. PASS. This strengthens the fixed-window estimate in AUTONOMOUS_LOCC_ARCHITECTURE_AUDIT.md and supplies a genuine joint spacetime moment bound.

## Statement

Let m(t) be a two-state continuous-time mark process starting at 0, with birth rate a and watchdog clearing rate mu. Independent commit attempts form a Poisson process of rate lambda. For any deterministic measurable finite-volume time set A contained in [0,T], let K(A) count commit attempts at times t in A for which m(t)=1. Set

    v=lambda(exp(theta)-1),     theta>=0.

If mu>v, then

    E_0 exp(theta K(A))
       <=exp[ a v |A|/(mu-v) ].                         (1)

The set A may be disconnected, widely separated, or consist of arbitrary selected spacetime windows. The bound depends on its TOTAL selected time, not on the full horizon T. It is uniform in how long the memory has previously run, provided the mark process was initialized at zero at the original time origin.

## Proof

Conditioning on the entire mark path gives the Poisson functional

    E[exp(theta K(A)) | m]=exp[v integral_A m(t)dt].     (2)

Let g_i(t) be the backward Feynman–Kac expectation from mark i at time t, with terminal values g_i(T)=1. Reverse time so the terminal condition becomes g_0(0)=g_1(0)=1, and write f(s)=1_A(T-s). The positive solutions satisfy

    g_0'=a(g_1-g_0),
    g_1'=mu(g_0-g_1)+v f g_1.                           (3)

Put x=g_1/g_0-1. The denominator is positive. Since x(0)=0 and the derivative at any x=0 is v f>=0, x remains nonnegative. Direct differentiation gives the EXACT equation

    x'=v f+(v f-mu-a)x-a x².

As 0<=f<=1,

    x'<=v f-(mu-v)x.

Therefore

    x(s)<=v integral_0^s exp[-(mu-v)(s-u)] f(u)du.

Integrate over s, interchange the nonnegative integrals, and use mu>v:

    integral_0^T x(s)ds <= v |A|/(mu-v).                 (4)

Meanwhile (3) gives (log g_0)'=a x, so (4) proves (1). Piecewise constant sets suffice first; standard nonnegative approximation gives the measurable-set version. No temporal independence of the marks is asserted or used.

The birth rate can be bounded above by a<=nu epsilon through a Poisson domination. The master watchdog clocks provide actual clearing events. Self-births while m=1 make no difference to this two-state process.

## Finite-overlap spatial composition

For each owner h, choose a deterministic selected time set A_h and count its marked commit attempts K_h(A_h). Its mark depends only on its watchdog clock and the primitive fault clocks in a fixed dependency patch. Color the overlap graph of these primitive-clock patches with chi colors. Within a color the entire exogenous clock families, and hence mark/attempt processes, are independent.

Holder over colors and (1), evaluated at chi theta, give

    log E exp[theta sum_h K_h(A_h)]
       <= [a_max v_chi/(chi(mu-v_chi))] sum_h |A_h|,
    v_chi=lambda(exp(chi theta)-1).                     (5)

Different fixed rates can be treated using their respective bounds or a common worst case. Bounded support weights per emission replace theta by c_support theta. Bounded patch incidence converts sum_h |A_h| to a constant times the selected DATA spacetime volume. Thus the logarithmic moment coefficient is O(epsilon), uniformly for arbitrary selected spacetime sets.

If this moment is combined with direct primitive-fault counts by another Holder/Cauchy–Schwarz step, that step increases the required theta again. ALL such factors must be included before fixing the physical watchdog rate. A sufficient final design inequality is

    mu > lambda [exp(c_Holder chi c_support theta)-1].  (6)

Choosing such a finite mu may make a complete transaction very unlikely between watchdogs, but its service probability remains a strictly positive N-independent constant. Choose the service window after these rates, and the primitive epsilon threshold afterwards. No practical numerical threshold follows.

## Scope and cautions

- The measure in (1) is a positive record of ACTUAL primitive fault/watchdog/attempt clocks. Pauli coefficient histories and retained-bath amplitudes are not sampled as faults.
- Shared bath memory does not destroy the exogenous clock independence used here. A state-dependent or otherwise non-Poisson fault process requires a separately established uniform domination.
- Starting all marks at zero is substantive. Initial corrupt controller/channel states must either be initialized through the actual reset/flush mechanism or charged by an initial support/mark distribution; they cannot be silently assigned zero marks. Raw Bell DATA errors with empty caches need not create stale-cache marks, but their relative-error support still needs its source bound.
- The condition mu>v is not an irrelevant technicality. For v>mu, the tilted two-state process can have an exponential growth rate that does not vanish linearly with a as a approaches zero, so an O(a)|A| exponent is not generally available in this form.

The parent derivation is therefore correct and closes the specific missing arbitrary-spacetime marked-emission moment. It does not by itself establish the deterministic GPT contraction or change the broader atomic-local-instrument primitive scope.
