# A tail-reward lift of coercive carried-target episodes

## Status and governing source

The carried-target augmentation, exact residual log-factorial identity, bounded target-following episodes, scalar propagation, and bimolecular single-linkage availability lemma are PRIOR operations in Alec Kriebel, *Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible Stochastic Reaction Networks*, Version 1.2.4, 22 August 2026, an unrefereed primary preprint. Its complete proof and public source package have been read; exact bytes are preserved under `sources/`. Its source has no received independent expert peer-review status. The present work is the same history-exposed principal, not an independent audit.

This file develops an author-derived tail-reward operation on that prior mechanism. Historical priority for the lift is not established. The conclusion below concerns a whole arbitrary-dimensional class with several coupled, unpinned inventories, rather than a pinned controller or an assumed stationary fiber. It does NOT settle the full weak-reversibility recurrence conjecture.

## Complete consequence

For every finite weakly reversible stochastic mass-action network with ONE linkage class and maximum complex molecularity TWO, every fixed positive rate vector, and every actual communicating class C, its stationary probability pi_C has

    sum_(x in C) pi_C(x) exp(r |x|_1) < infinity       for EVERY r>0.       (1)

Finite classes and absorbing singletons satisfy (1) immediately. For infinite classes the proof combines the primary source's coercive episode lemma with the new reward lift proved below. It provides existence of all stationary exponential moments; it supplies no numerical moment value, universal tail constant, spectral gap, or efficient enumeration of the finite exceptional head.

More generally, the lift applies to ANY finite reaction list for which a finite family of the specified target-following episodes has proved coercive negative mean residual entropy. That general criterion is not presumed for arbitrary weakly reversible lists.

## 1. The exact supplied-and-verified episode structure

Delete physically null reactions, combine exact parallel channels if desired, and write a_y for the sum of rate constants leaving complex y. Let m be the number of complexes, R=max_y a_y/min_y a_y, and D the maximum complex molecularity (D=2 in (1)). At a marked physical state (x,t), the actual preceding target t is present. Put z=x−t>=0 and

    V(x,t)=E(z)=sum_i log(z_i!),     N=|z|_1.

If the next actual source is s, with product u, the new residual is z+t−s, so the exact increment is

    Y=log[(x)_t/(x)_s].                                             (2)

Every target-following reaction has Y=0. Fix one directed path from each t to each terminal c in the linkage. Follow that path only while its designated channels fire, stopping on the first other channel; if the terminal is reached, take one final ordinary jump. An episode has between 1 and m jumps. Its ENTIRE total reward is the increment on its one final jump. All other increments are zero, even though every inventory and every actual propensity evolves.

The source's finite-family argument proves the stronger coercivity statement

    J(x,t):=min_c E_(x,t)[V(Z_tau_c)−V(x,t)] -> −infinity             (3)

as (x,t) leaves every finite subset of one fixed infinite class. The displayed source uses threshold −1, but its contradiction proof applies to every fixed negative threshold: along any escaping sequence its availability lemma and scalar recursion produce a fixed terminal whose episode reward tends to −infinity. Thus (3), rather than mere negative drift at one threshold, is actually earned by its proof. A minimizing terminal can be selected before the episode starts from the finite acquired path library.

The exact source-probability calculation is short. If p_x(s)=a_s(x)_s/q(x), then for 0<gamma<1, (2) gives

    E exp(gamma Y)
      = (p_x(t)/a_t)^gamma sum_s a_s^gamma p_x(s)^(1−gamma)
      <= (m R)^gamma.                                             (4)

Disabled sources have p=0 and are omitted. This derivation uses the actual competing channel law; it changes no rate or physical clock.

## 2. Uniform positive-reward control for the WHOLE episode

An episode may terminate at any of at most m phases. Its probability of reaching a phase is at most one, and all earlier designated increments vanish. Therefore, with Y now the TOTAL episode reward,

    E exp(gamma Y_+) <= B_gamma:=1+m(mR)^gamma.                     (5)

In particular there are explicit network constants C1,C2 such that

    E Y_+ <= C1,
    E[Y_+^2 exp(lambda Y_+)] <= C2       whenever 0<=lambda<=gamma/2. (6)

For example choose gamma=1/2, C1=B_gamma/gamma and C2=16 B_gamma/gamma^2. These intentionally loose constants follow directly from (5).

The finite molecularity gives a different, deterministic bound on the negative part. Every episode endpoint has residual z+c−s, where |c|,|s|<=D. Hence

    |Y| <= 2D log(N+D+1).                                         (7)

This is a bound on the true episode endpoint. It does not replace elapsed physical time by jump count.

## 3. Convert entropy drift into a true exponential count reward

For any theta>0 define the increasing concave function and its exponential

    g_theta(v)=theta integral_0^v du/log(e+u),
    W_theta(x,t)=exp(g_theta(V(x,t))),
    lambda(V)=g_theta'(V)=theta/log(e+V).

Concavity gives, for EVERY possible endpoint including negative Y,

    W_theta(Z_tau)/W_theta(x,t) <= exp(lambda(V) Y).                (8)

For fixed dimension d, the elementary factorial bounds give

    N log(N/d)−N <= V <= N log N.

Consequently V/(N log N)->1 uniformly over count compositions, and

    g_theta(V)/N -> theta.                                        (9)

The integral asymptotic g_theta(v)~theta v/log v follows by differentiating numerator and denominator. Equation (9) is uniform over the whole class, including faces.

For all sufficiently large N, (7) implies lambda(V)Y_-<=4D theta. Set b_theta=exp(−4D theta)>0. For Y<0,

    exp(lambda Y)−1 <= −lambda b_theta Y_-.

For Y>=0, Taylor's integral bound and (6) give

    E[(exp(lambda Y)−1) 1_(Y>=0)]
       <= lambda C1 + lambda^2 C2/2,

once lambda<=gamma/2. Therefore

    E[exp(lambda Y)−1]
       <= lambda[C1−b_theta E Y_-]+lambda^2 C2/2.                 (10)

By (3), E Y_- >= −E Y >= −J(x,t) tends to infinity for the selected episode. For any fixed theta, outside a finite classwise head it exceeds exp(4D theta)(C1+3), and lambda C2/2<=1. Equations (8) and (10) then give

    E[W_theta(Z_tau)−W_theta(x,t)] <= −lambda(V) W_theta(x,t).      (11)

This step is why a generic assertion that positive recurrence implies moment bounds would be wrong, and why the actual reward distribution matters. Uniform exponential control of Y_+ and the logarithmic bound on Y_- together preserve negative drift under a transform whose growth is genuinely exponential in N. No Gaussian or stationary approximation is used.

## 4. Keep the physical occupation reward and close the whole return cycle

Fix the desired count reward F_r(x)=exp(r|x|_1), and choose theta>r. During one selected episode there are at most m genuine physical jumps, and every state has count at most N+2D. Thus its total jump-count reward is at most

    m exp(r(N+2D)).                                               (12)

By (9), lambda W_theta divided by the right side of (12) tends to infinity. After enlarging the finite head, (11) therefore pays the ENTIRE reward in (12), not merely one endpoint reward. The sampled-chain supermartingale, stopped at that head, gives finite expected sum of F_r over all original jumps until the head is reached. From the finite head, one ordinary jump has finitely many successors and finite reward; each successor has the proved return-reward bound. The finite irreducible trace chain on the head has geometrically bounded return count, so a complete regenerative return to one marked state has finite expected sum of F_r over ALL its jumps.

For completeness, attach the actual CTMC holding times after this embedded construction. Every state in a nonabsorbing class enables a genuine reaction, and positive integer falling factorials give

    q(x)>=kappa_min>0.

The holding time at x has its actual mean 1/q(x), independently of the next channel given x. Hence the expected physical occupation reward in that same regenerative cycle is at most kappa_min^(−1) times its already bounded jump reward. Infinite repeated returns include independent positive holding times at the fixed return state; their sum diverges almost surely, proving nonexplosion. The physical return cycle has positive finite mean length. Its normalized occupation formula now proves (1).

All phases, outputs, changing inventories and holding times lie in the SAME original model. There is no infinite-rate homogenization, frozen conditional equilibrium, assumed mixing gap or neighboring-profile law.

## 5. Exact scope of what was acquired

The operation acquired is a general transformation from COERCIVE carried-target entropy episodes to finite exponential occupation rewards at every prescribed count tilt. For single-linkage bimolecular networks the governing coercivity lemma is actually proved by the read primary source, so (1) is a completed author-derived consequence at that scope. A finite directed path library and all constants in (4)–(11) are acquired from the raw graph and rates. The finite head is proved to exist by the source's analytic compactness; its numerical extent and a numerical moment bound have NOT been acquired.

For arbitrary coupled weakly reversible networks, the missing operation is still coercive actual episode drift across linkage/activation layers. A scalar target-following path stays in its linkage, and higher-order source activation can require additional residual particles. Neither the banked bulk receiver nor (1) proves that operation. This tail lift should be preserved as an intermediate asset which will carry the required rewards if a valid broader episode construction is found.
