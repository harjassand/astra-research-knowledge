# Independent review: complete robust entropy witnesses from tree compatibility

29 October 2026. Scoped review of root's proposed entropy bridge. This does not re-audit the full tree-representation theorem or launch a new synthetic example.

## Verdict and necessary qualifications

The proposed path-KL identity and bound are correct:

    D(P_Q[0,T] || P_A[0,T]) <= T sigma(Q)/4,
    A = (Q+Q*)/2.

For a finite-word statistic F with range length L, universal equilibrium expectation at least zero, and target mean -gamma<0, the resulting certificate is

    sigma(Q) >= 8 gamma^2/(T L^2).

The statement applies uniformly to every finite stationary all-even CTMC completion of the observed law. No hidden cardinality, rate, mass, or irreducibility bound is needed.

Two qualifications should remain in the main theorem.

1. Inside equilibrium closure there is no robust positive bound from a finite rational-cylinder neighborhood. This does not prove that the infimum of entropy over EXACT finite completions of the entire law is zero. Closure and exact realization are distinct.
2. Existence of a finite separating linear statistic follows abstractly from closed convexity. The tree construction's contribution is an explicit complete family of finite linear feasibility problems and algebraically certified dual witnesses. Reversibilization, divergence contraction, Pinsker, concentration, and linear separation are established ingredients.

With the standard averaged Jensen–Shannon convention, the relevant classical inequality is JS <= Jeffreys/8. The unaveraged bracket for ONE unordered flux pair is at most one quarter of that pair's entropy-production term. Stating the scalar formula avoids a factor-of-two convention error.

## 1. Model, support, and entropy convention

Let Q be a generator on a finite state space, pi a stationary probability distribution, and remove states with pi_i=0. Stationarity implies that positive-pi states have no outgoing rate to a zero-pi state, so this restriction preserves the stationary path law.

Use row-generator conventions. For i!=j, put

    f_ij = pi_i q_ij,
    q*_ij = pi_j q_ji/pi_i.

The diagonal of Q* equals that of Q. Indeed stationarity gives

    sum_{j!=i} pi_j q_ji = -pi_i q_ii.

Define ordinary stationary entropy production in nats per unit model time by

    sigma(Q)
      = sum_{i!=j} f_ij log(f_ij/f_ji)
      = sum_{i<j} (f_ij-f_ji) log(f_ij/f_ji).          (1)

Terms with both fluxes zero contribute zero. A one-way positive stationary flux gives infinite sigma. Physical interpretation as ordinary time-reversal entropy requires that the hidden variables are physically even. This note supplies no separate heat, work, bath, or parity identification.

No irreducibility assumption is used. In particular, pi may distribute mass among several closed communicating classes.

## 2. Exact comparison with additive reversibilization

Set A=(Q+Q*)/2. It has the same escape rates and stationary law as Q. Moreover

    pi_i a_ij = (f_ij+f_ji)/2

is symmetric, so A is reversible.

On a finite path window, Q and A have the same initial pi density and the same integrated holding factors. A_ij >= q_ij/2 whenever q_ij>0, so Q's finite-window path law is absolutely continuous with respect to A's even when Q has one-way edges.

The path log likelihood ratio is therefore the sum over jumps of log(q_ij/a_ij). Stationarity gives mean jump count T pi_i q_ij. Hence

    D(P_Q || P_A)
      = T sum_{i!=j} f_ij log[2f_ij/(f_ij+f_ji)]
      = T sum_{i<j} J(f_ij,f_ji),                    (2)

where

    J(f,g) = f log[2f/(f+g)] + g log[2g/(f+g)].       (3)

There is no omitted escape-rate compensator or initial-distribution KL term. Both vanish under the stated stationary comparison.

### Scalar bound with the exact constant

For f,g>0 write m=(f+g)/2 and u=(f-g)/(f+g). By symmetry take 0<=u<1. Let

    ell(u)=log[(1+u)/(1-u)].

Then

    J(f,g)/m
      = (1+u)log(1+u)+(1-u)log(1-u)
      = integral_0^u ell(v) dv.

Since ell(0)=0 and ell is convex on [0,1), its graph lies below the chord from zero to u. Therefore

    integral_0^u ell(v)dv <= u ell(u)/2.

But

    (f-g)log(f/g) = 2m u ell(u).

Consequently

    J(f,g) <= (f-g)log(f/g)/4.                       (4)

The zero-flux endpoints follow by limits, with an infinite right-hand side when just one flux is positive. Summing (4) in (2) proves

    D(P_Q[0,T] || P_A[0,T]) <= T sigma(Q)/4.          (5)

The local ratio approaches 1/4 as f/g approaches one. Thus the quarter constant in this scalar comparison cannot be uniformly reduced.

In standard probability notation JS(p,q) averages its two KL terms, whereas Jeffreys(p,q)=D(p||q)+D(q||p). The corresponding standard bound is JS<=Jeffreys/8. Crooks and Sivak explicitly print that convention and inequality in their 2011 primary paper, equation (14); see the source receipt below.

## 3. A bounded observed witness gives a completion-independent entropy floor

Let the deterministic memoryless observation take values in a finite alphabet. The same observation map is used for Q and A. Let F depend on a finite set of times inside [0,T], have known range in [m_F,M_F], and write L=M_F-m_F>0.

Suppose

    E_R F >= 0 for every equilibrium closure law R,
    E_Q F = -gamma < 0.

A's observed law is one of those equilibrium laws. Hence

    gamma
      <= E_A F-E_Q F
      <= L TV(P_Q^obs,P_A^obs)
      <= L TV(P_Q,P_A)
      <= L sqrt[D(P_Q||P_A)/2]
      <= L sqrt[T sigma(Q)/8].

Thus

    sigma(Q) >= 8 gamma^2/(T L^2).                   (6)

This uses the convention TV=(1/2)||P-Q||_1. Using an L1 distance instead without changing constants would be an error.

Any safe upper bound on the range length may replace the exact L. An additive constant in F has no effect on L but must remain in the equilibrium inequality and target mean.

If T=0, a strict universal separation is impossible: every one-time finite-alphabet distribution has an equilibrium realization. A nontrivial certificate therefore has T>0.

The argument is conditional on a finite all-even CTMC completion existing. It does not establish such a completion for an arbitrary supplied probability law. For every completion that does exist, the same observed gamma,L,T apply.

## 4. Optional improvement for time-symmetric observed alternatives

The universal Pinsker transfer does not require F to be symmetric under time reversal. If the target observed law IS reversible, any separating F can be replaced by its pointwise reversal average after enlarging the observation grid to include its reflection:

    F_even = (F+F composed with reversal)/2.

Equilibrium expectations are unchanged. The target mean is unchanged, and the range length does not increase.

This makes the already available path-affinity argument stronger than (6). Let p,q,a be the stationary hidden path densities of Q,Q*,A on [0,T], and put

    r=sqrt(pq),  m=(p+q)/2,  affinity=integral r.

Their initial and holding factors agree. Edgewise arithmetic-geometric mean gives a>=r, while m>=r. Since a and m both have mass one,

    TV(m,a) <= 1-affinity.                            (7)

The stationary reversal involution implies D(p||q)=D(q||p)=T sigma. The elementary scalar inequality

    (x-y)log(x/y) >= 4(sqrt(x)-sqrt(y))^2

then gives

    2T sigma >= 8(1-affinity),
    1-affinity <= T sigma/4.                         (8)

For a pointwise reversal-even F, its expectation under m equals its expectation under Q. Equations (7)-(8) therefore imply

    sigma(Q) >= 4 gamma/(T L).                       (9)

This is an application of the previously reviewed symmetric-KL/Hellinger mechanism, not a new underlying divergence inequality. The nonlinear affinity bound from Jensen is also available, but no optimization of response curves is needed for the completeness claim.

For nonsymmetric observed alternatives, simply symmetrizing a witness can destroy its gap; (6) remains the complete universal transfer.

## 5. From finite LP duals to one observed grid statistic

Assume the metric-tree completeness theorem at its reviewed scope. At a finite level, all unknown tree probabilities lie in a finite product of simplices. Structural constraints have rational coefficients. The feasible observed path tables form a rational polytope after projection.

If a finite level excludes the target table, finite-dimensional linear separation supplies

    c_0 + sum_{k=1}^r c_k p(E_k) >= 0               (10)

for all feasible equilibrium tables, with strict negativity at the target. The coefficients can be rational: the finite system is rational, and a strict separator can be selected from its rational dual certificate cone. Equivalently one can enumerate rational exactly verified dual certificates.

Every E_k is an observed cylinder on a finite rational time set. Translate the times of each cylinder so its earliest time is zero. Stationarity preserves all its probabilities. Let S be the union of the resulting time sets and T=max S. Define

    F(y_S) = c_0 + sum_k c_k 1_{E_k}(y_S).           (11)

Then (10) is precisely E F>=0. No independence between the different E_k in one record is assumed or needed. All their indicators are evaluated on the SAME word on grid S.

The mixed original horizons therefore present no obstruction. A simple safe range bound is

    L <= sum_k |c_k|;

an exact finite-alphabet range can be computed by evaluating (11) on all words when worthwhile. This conversion uses passive stationary time-cylinder data. If different terms come from different controlled protocols, they are not automatically one passive path statistic; that would require a separate protocol formulation.

## 6. Completeness and the actual addition

Let E be the rational-cylinder closure of finite stationary reversible CTMC observation laws with the given finite alphabet and deterministic state observations.

E is closed by definition. It is convex: realize a finite convex mixture by the block-diagonal direct sum of the generators and a stationary distribution carrying the desired mass on each block. Taking closure preserves convexity.

Closed convexity alone implies that every p outside E has a finite-coordinate continuous affine separator. In the countable product of cylinder probabilities, every continuous linear functional uses finitely many coordinates. This abstract statement is not itself a new consequence of tree representation.

The tree hierarchy supplies more: a specified sequence of FINITE LPs whose feasible extension tables characterize E, so their duals give an explicit complete certificate family without choosing a hidden dimension or rate cap. A target outside E violates one of these certified finite statistics. Equation (6) then gives a positive entropy floor for every finite all-even completion.

For targets in E, every bounded finite-cylinder functional nonnegative on equilibrium laws remains nonnegative by continuity. Therefore no such finite witness exists.

This is completeness for robust separation from equilibrium, not completeness for computing the exact entropy optimum or distinguishing every positive-entropy hidden model from every zero-entropy model by its observations.

## 7. What inside-closure impossibility does and does not say

If p belongs to E, then every neighborhood specified by finitely many rational cylinder probabilities and positive tolerances contains a finite reversible CTMC observation law. Such a neighbor has sigma=0. Consequently no strictly positive entropy lower bound can be uniformly valid over that neighborhood.

This statement also has a direct statistical version. Fix a finite observation grid and N independent stationary records on that grid. The finite alphabet makes cylinder convergence equivalent to total-variation convergence of the one-record law, and the N-record product laws then converge in total variation. Any test whose rejection probability is at most alpha under all finite equilibrium models must have rejection probability at most alpha at p.

The same conclusion applies to finite collections of grids and fixed finite sample sizes. It does not require the target itself to have a zero-entropy exact finite realization.

In particular, none of the following stronger claims has been proved:

- every p in E has an exact finite reversible realization;
- the minimum or infimum of sigma over EXACT finite completions of p is zero;
- a source supplying infinite records, continuous-path information, or unbounded precision is captured by one finite-cylinder experiment;
- additional known structure, hidden dimension bounds, clocks, intervention access, or a physical parity restriction cannot change the inference problem.

The absence of a robust finite-cylinder entropy floor is the correct conclusion.

## 8. Sound acquisition of an enumerated witness family

Enumerate a countable family F_j of exact universally valid rational dual certificates. Each has a finite grid S_j, horizon T_j, and certified range length L_j. The enumeration and validity checks need not use the target samples.

The acquisition premise is independent stationary preparations of the observed record on each required grid. Independence, stationarity, timing, and the sensor interface must be supplied or separately calibrated. One long trajectory does not automatically provide independent stationary replicas, especially for a nonergodic model or a model with unknown slow mixing.

For witness j, let N_m=2^m and let hat_mu_{j,m} be its empirical mean from N_m independent records. Set, for j,m>=1,

    alpha_{j,m} = alpha 2^{-j}/[m(m+1)],
    r_{j,m} = L_j sqrt[log(1/alpha_{j,m})/(2N_m)].

The failure budgets sum to alpha. One-sided Hoeffding gives

    Pr(mu_j > hat_mu_{j,m}+r_{j,m}) <= alpha_{j,m}.

A union bound supplies one event of probability at least 1-alpha on which every upper confidence bound

    U_{j,m}=hat_mu_{j,m}+r_{j,m}

is simultaneously valid. Dependence between different tests or reuse of the same records across fixed witnesses does not invalidate this union bound; independence within the records used for each Hoeffding statement remains necessary.

Whenever U_{j,m}<0, put gamma_cert=-U_{j,m}. On the simultaneous event,

    sigma >= 8 gamma_cert^2/(T_j L_j^2).

The maximum of all reported valid lower bounds is still valid. No extra multiplicity correction is needed beyond the already assigned budget.

Dovetail the enumeration so every fixed j receives arbitrarily large sample levels. If p is outside E, some enumerated F_j has a strictly negative mean. For that fixed j the radius tends to zero and the strong law makes the empirical mean converge; that witness eventually detects the alternative almost surely under the acquisition premise. This is pointwise eventual detection, not a uniform bound on which level, how many records, how long, or how much arithmetic will be required.

A witness selected by optimizing the SAME data cannot simply be inserted into a fixed-witness Hoeffding formula. Either use the predefined simultaneous family, or validate a selected exact certificate on independent held-out data with a valid budget over rounds.

If acquired one-record laws differ from the ideal stationary grid law by certified TV at most nu_j, then the score error is at most L_j nu_j. Replace U_{j,m} by U_{j,m}+L_j nu_j before testing. The calibration itself is not supplied by the theorem.

Record cost remains visible: each record has duration T_j and |S_j| observation times, and the source must deliver stationary independent preparations at the claimed accuracy. Finite-state execution, mixing, preparation and instrument precision do not follow from the finite number of queried table entries.

## 9. Irreducible zero-entropy approximants

Let R be any finite reversible generator with stationary pi positive on its retained state support. Define the stationary refresh matrix Pi=1 pi and

    R_epsilon = R + epsilon(Pi-I),  epsilon>0.        (12)

Its added off-diagonal rate is epsilon pi_j. Thus every off-diagonal entry becomes positive, R_epsilon is irreducible, and

    pi_i (R_epsilon)_ij
       = pi_i R_ij + epsilon pi_i pi_j

is symmetric. It remains exactly reversible and has entropy production zero. The escape-rate increase is at most epsilon.

Since R Pi=Pi R=0,

    exp(t R_epsilon)
       = exp(-epsilon t)exp(t R)
          +(1-exp(-epsilon t))Pi.                    (13)

A stronger finite-window statement follows from coupling: run R and the refreshed process together until an independent rate-epsilon Poisson refresh. They agree before that event. Therefore

    TV(P_R[0,T],P_R_epsilon[0,T])
       <= 1-exp(-epsilon T) <= epsilon T.            (14)

The same bound holds after the deterministic observation. This includes reducible mixtures. If a state space has only one retained state, it is already irreducible in the usual convention.

Thus restricting finite equilibrium approximants to irreducible ones leaves the rational-cylinder closure unchanged. Choose epsilon sufficiently small for each finite horizon in a diagonal approximation.

No infinite-horizon path-TV approximation is asserted. The required mixing or independent-preparation cost can diverge as epsilon tends to zero. If a fixed exact rate ceiling were part of the comparison class, the additional refresh would need an explicit cap-preserving modification; no fixed ceiling is imposed here.

## 10. Prior comparisons and receipt

The direct flux proof above independently verifies the constants. Its ingredients are conventional: additive reversibilization, the finite CTMC path likelihood, the scalar Jensen–Shannon/Jeffreys comparison, data processing, Pinsker, Farkas separation, and Hoeffding concentration.

Primary source for the divergence convention:

Gavin E. Crooks and David A. Sivak, “Measures of trajectory ensemble disparity in nonequilibrium statistical dynamics,” Journal of Statistical Mechanics (2011), P06003, DOI 10.1088/1742-5468/2011/06/P06003.

https://threeplusone.com/pubs/Crooks2011a.pdf

Sections 3–4 and equation (14) were read directly in the author-hosted paper. It defines Jeffreys as the sum of the two KL divergences and Jensen–Shannon as their equally weighted comparison to the mixture, then states JS<=Jeffreys/8. It does not establish the new tree-hierarchy completeness assertion.

Existing Astra N507's preserved v1–v3 proof already uses additive reversibilization, a finite observed inequality, and the path-affinity transfer. Its current source scope and exact retrieval are recorded in SOURCE_AND_SCOPE_RECEIPT.md. This review extends that bridge to the proposed complete certificate family; it does not relabel the old mechanism as new.

No numerical fixture was constructed or run for this review. The result is an ordinary proof and scope correction. Its dependency on the tree hierarchy is explicit and remains subject to the separate representation review.

## 11. Addendum: the projected convex information distance

Root subsequently added Section 5 of COMPLETE_EQUILIBRIUM_INFORMATION.md. Its new population bound is correct under the following explicit construction.

Fix a finite observation grid G in [0,T], with T>0. Let K_m be nested finite subsystems of the universal tree-consistency constraints. Include the probability table on G as a variable r. Leave ALL other path tables and tree extension tables variable, subject only to the universal constraints and to their marginalization relations with r. Let C_m(G) be the projection onto r.

It is essential not to freeze other path tables to additional target statistics while still claiming a bound from p_G alone. The additive reversibilization need not match those other target statistics; such a restriction could remove the required equilibrium comparator.

With the free-variable definition, the observed grid law r_A of the additive reversibilization belongs to every C_m(G). Therefore

    d_m(p_G) := min_{r in C_m(G)} D(p_G||r)
              <= D(p_G||r_A)
              <= D(P_Q[0,T]||P_A[0,T])
              <= T sigma/4.

Thus

    sigma >= (4/T) d_m(p_G).                          (15)

Each C_m(G) is a compact rational polytope and is convex. It is nonempty and contains a full-support equilibrium grid law: use a finite reversible complete-graph chain with one state per observed letter and strictly positive stationary masses. At distinct ordered times, every observed word then has positive probability. Hence the displayed minima are finite and attained. The usual convention handles a grid with repeated times by first removing duplicate time coordinates.

### Why intersections commute with projection here

Work in the compact product of all finite tree probability simplices. A finite subsystem defines a closed subset K_m of that product, and the K_m are nested. If r belongs to every C_m(G), then

    K_m intersect {the G table equals r}

is a nested sequence of nonempty compact sets. Their intersection is nonempty. It supplies a full compatible extension with G marginal r. Consequently

    intersection_m C_m(G) = E_G,

where E_G is the projection of the full equilibrium closure E onto G. This would not follow merely from arbitrary noncompact projections; the compact fibers are doing real work.

### Convergence of the KL minima

The values d_m increase because C_m decreases. They are bounded above by

    d_infinity = min_{r in E_G} D(p_G||r).

Take minimizers r_m and a convergent subsequence with limit r_*. For every fixed k, its tail lies in the closed set C_k(G), so r_* belongs to E_G. Lower semicontinuity of KL gives

    d_infinity <= D(p_G||r_*) <= liminf_m d_m <= d_infinity.

All inequalities are equalities. Thus d_m converges monotonically to the information distance from E_G. No continuity of KL at zero entries is needed.

Because D(p||r)=0 only when p=r, compactness also gives

    d_m(p_G)>0 if and only if p_G is not in C_m(G).

If p is outside E, some finite grid has p_G outside E_G; otherwise compactness of the compatible finite-grid fibers would give a global law in E matching every cylinder of p. The decreasing compact hierarchy then excludes that grid table at a finite level. This proves completeness for positive detection when grids and levels are both allowed to increase.

Equation (15) is a certified lower bound, not a formula for minimum hidden entropy. It compares to the equilibrium class through a particular reversibilization and classical KL contraction.

## 12. Addendum: written acquisition scope and adaptive optimization

Root's acquisition section correctly separates the exact probability-law theorem from independent stationary record preparation, finite precision, dependence, and reuse.

For the new information-distance bound, let P_N(G) be a confidence region containing the TRUE ideal grid law p_G with probability at least 1-alpha. Then

    sigma >= (4/T)
        min_{p in P_N(G), r in C_m(G)} D(p||r)         (16)

on that event. The joint optimization is convex when P_N(G) is convex. Joint convexity of KL by itself does not make an arbitrary nonconvex confidence region a convex feasible set. Linear multinomial intervals, a suitable convex likelihood region, or a convex outer approximation retain the stated form. Calibration uncertainty must be included in the region for the ideal law, or separately accounted for.

One valid confidence event for a fixed grid covers ALL hierarchy levels m at once, because the true p_G remains in P_N(G) and r_A remains in every C_m(G). Choosing the level after seeing the data therefore needs no additional multiplicity penalty across those levels. Selection across grids, repeated confidence-region updates, or an unbudgeted stopping rule still needs simultaneous coverage or independent validation.

The plug-in value min_r D(hat_p_G||r) without a valid confidence region is not a certified population lower bound.

Finally, the linear bound (9) requires pointwise reversal symmetry of the STATISTIC. That property can be imposed exactly when constructing F_even, then its own mean can be validated. It does not require finite data to prove that the whole observed source law is reversible. Full target reversibility is used only in the existence argument that symmetrizing an already separating witness preserves its population gap.

No new fixture was required for these checks. They are convexity, compactness, lower-semicontinuity, and confidence-interface arguments.
