# Actual seeded-D exit kernel for the dormant-face test
Status: personal regional derivation, unreviewed. It does NOT close the opposite large-D face or the full network.

Use the operational residual chain2A'<->A'+D<->C+D, with fixed positive rates and killing k_D(A')_2. Write a=A', d=D, n=a+c+d. Start with d=1; a may be arbitrary. Let J=floor(n^(1/8)), K=floor(n^(1/4)), and stop at clearing, d=0, or d>=J. All estimates below concern this ACTUAL stopped process. No post-exit return law is assumed.

The candidate bounds are:

    E sigma <=C n^-1/2,
    P(exit at d=0)<=C n^-1/8,
    P(exit at d>=J)<=C exp(-c n^(1/8)),
    P(clearing with a<K/2)<=C n^-1/4.

Thus the seed d=1 leads to a clearing with growing A reserve with probability1-o(1), while every exceptional outgoing face is retained explicitly.

## 1. A graph-earned geometric bound, not mixing
The D-creating edge2A'->A'+D and the clearing channel have exactly proportional propensities (a)_2. Mark the combined clock: each event is clearing with fixed probability p>0, independently of the preceding path. Hence the number of D-creating events before clearing is stochastically bounded by a geometric variable, even when stopped earlier at a face. This statement does not assume clearing is already known to occur. Starting d=1, reaching d>=J requires at least J-1 such creations, proving the exponential exit-mass bound.

The same observation bounds the number of A-decreasing2A' events before clearing and its tail. It is the resource control used below.

## 2. Low-A stage reaches K quickly or stops
While a<K and1<=d<J, c=n-a-d>=n/2 for large n. The A-increasing C+D channel has rate >=c_0 n d. The adverse A-decreasing channels have total rate <=C(a^2+ad). Since K^2+KJ=o(n), their drift is absorbed, giving Q a>=c_1 n (in fact order nd).

Stop this stage on a>=K or any of the three terminal outcomes. The bounded overshoot and optional stopping give expected stage time <=CK/n. One may use the finite-shell stopped generator with a terminal value in[0,K+O(1)] for the upper bound; killing only shortens the un-killed low-stage hitting argument. The probability of a D-loss event during this stage is bounded by its compensator:

    E int C a d dt <=C K J(K/n)=C J K^2/n.

This bounds exit at d=0, and more generally the chance of any D-loss in the stage. Clearing before a reaches K has probability <=CK^2(K/n)=CK^3/n.

## 3. High-A stage: clearing beats loss of the reserve
Start a high stage at a>=K (or at the initial a if already large) and stop at clearing, a<K/2, or either d-face exit. Before that stop, clearing intensity is at least cK^2, so its expected duration is <=CK^-2. The occupation compensator gives E int(a)_2 dt<=1/k_D. Therefore the expected number of A'D channel events is at most

    C E int a d dt <=C (J/K) E int(a)_2dt<=CJ/K.

In particular this bounds high-stage D-loss probability. To cross from a>=K to below K/2 requires at least K/2 bounded negative A jumps. The2A'->A'+D negative jumps have a geometric tail before clearing; all other negative A jumps are among the A'D events just bounded. Hence the probability of restarting a low stage is <=C J/K+C exp(-cK).

This estimate allows positive A jumps and arbitrary motion toward the A-dominant face; no assumption that C remains dominant in a high stage is needed. If a grows, its clearing hazard only increases, and d/a remains bounded by2J/K.

## 4. Earned restart and complete stopped bounds
The low/high stages alternate only on the just-bounded high-to-low restart. Its probability tends to0. Positive renewal iteration, first with finitely many stages and then monotonically, gives a uniformly bounded expected number of stages and finite actual sigma, without a pre-existing full-fiber mean. Summing the per-stage times yields

    E sigma<=C(K/n+K^-2)=O(n^-1/2).

Summing D-loss probabilities gives O(JK^2/n+J/K)=O(n^-1/8). Small-A clearing can occur only in a low stage (or after the rare high-to-low restart), and its per-stage compensator bound is CK^3/n=O(n^-1/4). The geometric D-creation count proves the d>=J exit bound independently of the restart analysis.

## Caveat requiring exact audit
The low-stage hitting-time proof must stop the underlying FAST chain at the d-boundaries and use an appropriate bounded terminal function, rather than incorrectly preserve the positive Q a drift after assigning cemetery a=0. A clean construction is to stop the fast chain at a>=K or d=0 or d>=J first; Qa>=cn on the interior and bounded terminal a<=K+O(1) imply its mean <=CK/n. Adding the independent clearing clock only shortens it. This is the intended proof.

## What this earns and what it does not
The dormant D=0 connector Green already supplies an outgoing seed with d=1 and exponentially integrable A,B phase cost. The present kernel controls its subsequent operational seeded excursion until clearing or explicitly recorded d-face exits. It provides an actual vanishing feedback probability to d=0 and an exponentially small probability of entering d>=J. Converting the latter into a globally integrable forcing still requires a real cost bound on the large-D/opposite face. No such bound is supplied or assumed here. Physical common-seed clock and connector competitors also require their own interface before this is used in the full chemical chain.
