# A thermal visibility boundary for noisy learned computation

Date: 1 November 2026 (Australia/Brisbane)

## Status and purpose

This is a proved corollary and constructive failure developed in this investigation. It is not a claim of historical novelty or a positive breakthrough. It tests a tempting successor to Astra's exact algebra compiler: replacing exact closure by small normalized Hilbert--Schmidt error and promising later thermodynamic computations. That substitution fails at an explicit inverse-temperature scale.

The inherited information argument is credited to Astra N1543 at revision `51ce47ce39f976517d60e2f87bbe280b651f6056`, specifically:

`research/2026-10-31-native-quantum-bath-memory-interim/source/p1-noisy-W/members/Astra_Noisy_Computation_20261031/robust_solver/NOISY_OFFLINE_OBSTRUCTION.txt`.

The complete 431-line proof was read through the pinned GitHub connector. Its source/oracle is fixed before learner randomness. Its error model is a calibrated possibly nonlinear, query-dependent norm bound. It is not iid mean-zero measurement noise and not one fixed linear perturbation.

## 1. Intended consequence and the strongest ordinary attempt

Intended capability: learn a finite reusable representation from noisy vector actions, then compute equilibrium energy and partition functions for a broad later temperature range with no further source calls, even when the source has small generated algebra.

Ordinary stochastic Lanczos quadrature already retains a spectral measure that supports all later Lipschitz functions of ONE fixed matrix. Chen, Trogdon and Ubaru (ICML 2021) supply a Wasserstein spectral-distribution error analysis and posterior bounds: https://proceedings.mlr.press/v139/chen21s.html . This alone defeats any claim of a new reusable scalar spectral calculus.

General structured approximation is also a strong incumbent. Amsel et al., COLT 2026, establish nearly square-root logarithmic matvec query dependence for approximation from a finite matrix family, extending to approximately square-root dimension dependence for a linear family: https://proceedings.mlr.press/v336/amsel26a.html . Exact vector and transpose actions, approximation norm, enumeration/arithmetic and finite-family coverage must be kept separate from noisy action access and a genuinely acquired computational grammar.

Neither result as cited upgrades a small normalized Hilbert--Schmidt approximation into arbitrary low-temperature relative thermodynamics under the bounded-error interface below. The next calculation shows why that upgrade is false.

## 2. Source and exact thermodynamics

Fix N >= 3, a known real or complex unit vector e, an unknown unit vector u perpendicular to e, and an energy scale Delta > 0. Define

    H0 = 2 Delta I - Delta ee*,
    Hu = 2 Delta I - Delta (ee* + uu*).

Each source is positive definite, has condition number two, has exactly two eigenvalues {Delta, 2 Delta}, and generates a unital algebra of dimension two. Thus neither ill conditioning nor large exact algebra is responsible for the obstruction.

Their normalized Hilbert--Schmidt distance is

    ||Hu-H0||_F / sqrt(N) = Delta / sqrt(N).

At inverse temperature b >= 0, put x = exp(b Delta). Their partition functions are

    Z0 = exp(-2 b Delta) (N - 1 + x),
    Zu = exp(-2 b Delta) (N - 2 + 2x).

Their internal energies are

    U0 = 2 Delta - Delta x/(N - 1 + x),
    Uu = 2 Delta - 2 Delta x/(N - 2 + 2x).

Direct subtraction gives

    (Zu-Z0)/Z0 = (x-1)/(N-1+x),
    U0-Uu = Delta N x / [(N-1+x)(N-2+2x)].

These are exact formulas, with no asymptotic approximation.

## 3. Thermal visibility threshold

At b Delta = log N,

    (Zu-Z0)/Z0 = (N-1)/(2N-1) -> 1/2,
    U0-Uu = Delta N^2/[(2N-1)(3N-2)] > Delta/6.

Thus a perturbation whose normalized Hilbert--Schmidt size vanishes as N^(-1/2) causes an order-one change in the physical mean energy. A relative partition approximation with error epsilon < (N-1)/(5N-3) distinguishes the two sources. A mean-energy approximation of absolute error less than Delta/12 also distinguishes them.

By contrast, if b Delta = a log N with a < 1 fixed, both displayed differences are O(N^(a-1)) (for the energy, multiply by Delta), and simply returning the known baseline thermodynamics is asymptotically adequate at fixed tolerance. If a > 1, the relative partition difference tends to one, but the internal-energy difference tends to zero because both systems concentrate at their common lowest eigenvalue. Their degeneracies remain different. This difference between partition and energy tasks is essential; there is no universal scalar notion of thermal relevance.

## 4. Fixed noisy access and adaptive lower bound

Grant arbitrary chosen full vectors v and a reported action O(v) with

    ||O(v)-H v|| <= eta ||v||,    0 < eta < Delta.

For Hu, define the fixed continuous mask, with z = u* v,

    Ou(v) = H0 v - u (z/|z|) max(Delta |z| - eta ||v||, 0),

where the second term is zero when z = 0. Its error relative to Hu v has norm min(Delta |z|, eta ||v||), so the bound holds globally. It agrees with the exact H0 oracle whenever Delta |u* v| <= eta ||v||. It is chosen before all learner coins, continuous, and homogeneous (real or complex as appropriate).

For u uniform on the unit sphere in e-perp, every fixed v obeys the conservative common real/complex cap bound

    Pr[Delta |u* v| > eta ||v||]
       <= 2 exp(-(N-1) eta^2/(2 Delta^2)).

Fixing the learner coins and following its baseline transcript produces q queries independent of u. Until a cap is hit, all responses and future queries coincide. A union bound therefore gives

    Pr[the full transcripts differ]
       <= 2q exp(-(N-1) eta^2/(2 Delta^2)).

Whenever the desired answer intervals for the two sources are disjoint and each source must be answered correctly with probability at least 1-delta, delta < 1/2, this yields

    q >= (1-2delta)/2 * exp((N-1) eta^2/(2 Delta^2)).

At b Delta = log N this applies both to relative partition error epsilon < (N-1)/(5N-3) and to absolute energy error less than Delta/12. The source class is known in advance; the difficulty is not an unknown interpretation of the task.

The corresponding state and free-energy distinctions are also exact. At any b>0 the free-energy gap is log(Zu/Z0)/b. Thus the same lower bound applies to absolute free-energy tolerance less than half this gap, which at the crossover vanishes as Delta log(3/2)/(2 log N). It does NOT prove hardness of constant-accuracy free energy. The half trace distance between the two nested-projector Gibbs states is

    T_N(x) = x/(N-2+2x) - 1/(N-1+x).

At x=N this is 2(N-1)^2/[(3N-2)(2N-1)] -> 1/3. A Gibbs-state receiver with half-trace error less than T_N(N)/2 must also distinguish the two targets, so the same transcript-coupling lower bound applies. This is a target-output statement, not an assumption that a measurement revealing u is available.

This is an application of N1543's fixed-source masking argument to an ordinary thermodynamic consequence, rather than to a specially selected spectral projector query. It does not establish hardness for exact matvecs, iid unbiased noise, a fixed linear perturbation, physically supplied thermal samples, or an input supplying the hidden mode u.

## 5. A constructive precision remedy, with its bill

Suppose better action accuracy can be bought. Query independent random unit vectors in e-perp at eta = Delta/[4 sqrt(N-1)]. Declare a hidden mode if ||O(v)-H0v|| > eta. The null gives no false positives. The alternative forces detection whenever Delta |u*v| > 2eta. Paley--Zygmund gives success probability at least 1/12 per probe in either field, hence q = ceil(12 log(1/delta)) probes suffice against arbitrary admissible action errors.

The source class promises that detection determines both thermodynamic curves exactly; no reconstruction of u is needed. If precision work is eta^(-p), p > 0, the acquired detection therefore costs O((N/Delta^2)^(p/2) log(1/delta)), plus O(Nq) full-vector generation/readout/arithmetic and O(N) storage. The N1543 lower bound matches the N^(p/2) dependence at fixed confidence. This is a conventional random-probe detection construction credited to N1543, not a new algorithmic speedup.

## 6. Consequence for a future positive theory

A stable successor to exact algebra learning must specify the future operation and certify its relevant spectral mass or thermal occupation. Tiny unweighted closure residuals do not suffice. A useful positive advance would acquire a bounded-error representation for a whole NONCOMMUTING control family while paying the temperature-dependent discovery of rare modes. Uniform high-temperature scalar spectral sums alone already have strong conventional algorithms.

No new physical primitive or asymptotic superiority is claimed by this note. The retained output is a rigorous failure and a precise information/accuracy tradeoff that the stronger target must respect.
