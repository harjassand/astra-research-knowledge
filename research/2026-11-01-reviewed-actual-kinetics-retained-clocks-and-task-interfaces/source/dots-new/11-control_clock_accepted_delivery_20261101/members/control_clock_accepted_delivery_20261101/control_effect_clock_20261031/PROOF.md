# Acquiring an action-response clock without a supplied mixing bound

**Status:** new, not independently reviewed. This is a finite-confidence composition of ordinary coupling/Poisson estimation, concentration, retained search, and the accepted canonical-control consumer. It is not a claim to invent coupled estimators or a practical advantage. The central positive statement is Theorems 1–4; Theorem 5 gives a task-level limitation. All observations and computations are classical.

## 1. Task and receiving interface

There are n named microscopic states, m actions including baseline 0, unknown row-stochastic matrices A_a, and an externally specified rational discount 0<gamma<1. A call prepares a requested named state i, applies action a, and returns its next microscopic label. Calls in different requested independent trajectories use independent source randomness. Preparation has an explicit cost; we do not assume a cheap physical reset, probability oracle, reverse transition, shared-noise simulator, or global mixing gap. If preparation is unavailable, this interface is unavailable: the theorem is not an offline-data coverage theorem.

The retained partition has indicators Z (n by r), and W averages uniformly within each block. Its labels/map, source family, action set, gamma and confidence are externally bound. The partition must be fixed independently of the validation bank below. It may have been acquired by the earlier refinement procedure, with all its work paid. Native reward features alone are also a legitimate starting partition. A partition selected using this bank requires fresh validation, or a separate uniform event over the possible partitions; merely reusing the same r-dimensional radius is invalid.

Future tasks specify an arbitrary block/action reward table g_a in [0,1]^r. The objective is normalized discounted value, (1-gamma) E sum gamma^t g_{a_t}(block(X_t)), and a stationary block policy with a pointwise regret certificate. Deployment requires microscopic label sensing and the retained partition lookup. No hidden-state/history controller or additional physical sensor is inferred.

Put H=(1-gamma)(I-gamma A_0)^(-1)Z and t=gamma/(1-gamma). The quantity needed by the accepted decision compiler is the *scaled* action response

    U_a = t(A_a-A_0)H
        = gamma sum_{s>=0} gamma^s (A_a-A_0) A_0^s Z.

Estimating the small difference (A_a-A_0)H to accuracy proportional to 1-gamma and then multiplying is unnecessary if U can be observed more directly. This does not make the physical response decay.

## 2. A capped paired-path observation

For each (i,a), a!=0, independently draw X_0~A_a(i,.) and Y_0~A_0(i,.). While their microscopic labels differ, take independent baseline transitions of both paths. Let tau be the first equal-label time (possibly infinity). At equality their future can be coupled identically and omitted: both marginal continuation laws are A_0. The construction uses only independent forward calls *before* equality, not a common-noise source oracle. Equal block labels alone are not a stopping rule.

At a predeclared integer cap K>=0 define

    Y_K = gamma sum_{s=0}^{K-1} gamma^s [Z(X_s)-Z(Y_s)],
    I_K = 1{tau>K}.

All summands after tau are zero. Simulate the terminal pair at time K unless already met. The exact call count is 2+2 min(tau,K), including the initial pair. For K=0 the prefix is zero but the initial pair is observed. Source-row, action, both intermediate microscopic labels, meeting time/censoring, and counts are retained. Ordinary competitors receive all of them.

**Theorem 1 (no-gap tail).** With mu_K=E Y_K and p_K=P(tau>K),

    ||U_a[i,:]-mu_K||_1 <= 2 gamma^(K+1) p_K/(1-gamma).

Indeed the summand at time s has the correct marginal expectation, norm at most 2, and is zero after meeting. Absolute convergence follows from discounting even if tau is infinite. Bounding P(tau>s)<=p_K for s>=K proves the result. A sharper survival-curve sum is possible but not needed here. No stationary distribution or gap appears.

This is a discounted, capped version of the ordinary coupled Poisson-difference estimator; see SOURCES_AND_COMPARISON.md. It is uniform over the retained block observables, not an optimal task-specific clock. It may be very pessimistic for observables that cancel before microscopic meeting.

## 3. Data-derived finite-confidence admission

Let F=n(m-1), and collect N>=2 iid capped paths per row/action. All designs are fixed before the paths, or belong to the uniform grid in Section 4. Define

    L_K=gamma(1-gamma^K)/(1-gamma) <= K.

Every subset sum of Y_K lies in [-L_K,L_K]; its coordinates sum to zero. Let the total fixed-design failure budget be delta, divided equally into delta_H, delta_E and delta_T. All logarithms below may be replaced by any **verified upper bound**, and square roots are rounded upward.

### Prefix

The subset-union Hoeffding radius is

    e_H = sqrt_up(8 L_K^2 ell_H/N),
    ell_H >= log(2^(r+1) F/delta_H).

For a zero-sum error x, ||x||_1=2 max_S sum_{j in S} x_j. Hoeffding and a union bound prove simultaneous row/action L1 coverage. The 2^r subsets are analysis only: their logarithm is O(r), no subset enumeration is required.

An ordinary empirical-Bernstein alternative is retained, not excluded. With unbiased coordinate sample variances V_j,

    e_E = sum_j [sqrt_up(2 V_j ell_E/N)
                         + 14 L_K ell_E/(3(N-1))],
    ell_E >= log(4 F r/delta_E).

Apply Maurer–Pontil Theorem 4 to each coordinate after mapping its range of length 2L_K to [0,1], apply the same bound to its negative, and union over F r. With both events paid, e_prefix=min(e_H,e_E) is valid. Realized maximum path length or empirical range CANNOT replace L_K. Unseen rare long trajectories are precisely the obstruction in Section 6.

### Tail

Let k be the number of nonmeetings at K, h=k/N, and ell_T>=log(2F/delta_T), b=ell_T/N. Use

    p_U = min(1,b)                                  if k=0,
    p_U = min(1,h+b+sqrt_up(2 h b+b^2))               otherwise.

For k=0, P(k=0)<=exp(-Np). For the other branch, the Bernoulli lower-tail Chernoff inequality gives h>=p-sqrt(2pb) except with probability exp(-ell_T); solving this quadratic gives the displayed bound. Two events per pair are paid, hence the factor 2F. The same paths supply the prefix and tail statistics; no independence between the confidence events is required.

The simultaneous response radius is

    e_ia=e_prefix + 2 gamma^(K+1) p_U/(1-gamma).

Write Uhat_a for empirical prefix rows, Uhat_0=0, and B_Uhat_a=W Uhat_a. A directly checked aggregate certificate is

    eta_U=max_{a,i} ||Uhat_a[i,:]-(Z B_Uhat_a)[i,:]||_1
                                      + max_{i,a!=0} e_ia.

Then, with probability >=1-delta,

    max_a ||U_a-Z B_Uhat_a||_(infinity->infinity) <= eta_U.       (1)

The maximum row error suffices; a finer row-dependent implementation may be cheaper. If exact response closure U_a=Z B_Ua holds and every row estimate has error <=e, then the measured within-block discrepancy is <=2e, so eta_U<=3e.

**Theorem 2 (all-goal control receiving).** Give the unchanged accepted direct-canonical compiler Bhat_a=B_Uhat_a/t and eta=eta_U/t. On event (1), any independently checked canonical witness X,delta_c with

    C_X=max_j X_jj/delta_c

admits every future action/block reward table with pointwise normalized policy regret at most

    2 eta_U C_X.

This is exactly the accepted residual theorem, since t Bhat=B_Uhat and t eta=eta_U. A reward-specific candidate with nominal residual rho has regret <=2(rho+eta_U ||w||_infinity). Core/source/map/goal/tolerance digests must be bound; the ordinary small LP and its checks are still paid. No empirical improvement is inferred from a unit-array witness. Full value features H are not sampled or stored by this frontend.

## 4. Retained search, rather than a supplied good cap

Use grid i>=1,j>=0, N_i=2^i, K_j=2^j-1, and budget

    delta_ij=delta_total 2^(-i-j-1).

The budgets sum to delta_total. For each row/action there is an analysis-only infinite iid bank of path pairs. The grid point uses its first N_i paths, capped at K_j. Generate only needed outcomes, retain paths, and extend previously censored paths when K increases. The bank is not a supplied common-random-number source: the actual forward calls are made when needed.

The union event over the predeclared grid permits arbitrary adaptive selection of the next grid point and stopping at a passing point. No independence between grid points is needed. It does NOT permit an outcome-dependent count/cap outside the grid with the fixed-design confidence unchanged. An adaptive acquired partition uses a fresh bank (or separately paid partition-uniform event).

One fully specified finite planner enumerates i+j=d for d=1,...,D_max, in fixed lexicographic order, running the response receiver and ordinary canonical proposal/check at each point. It reports UNKNOWN when its declared budget is exhausted. Failed probes, LPs, path extensions, storage, and all validation arithmetic are retained and paid. No optimal experimental-design oracle is assumed.

**Theorem 3 (oracle-grid overhead).** If a sufficient dyadic pair (N,K) has N(K+1)=2^d, all points through diagonal d cost at most O(F d 2^d) source calls even without path reuse. Each point costs <=2F N(K+1), there are d points on diagonal d, and sum_{k<=d} k 2^k=O(d 2^d). Actual retained-bank calls can be smaller. Confidence logarithms grow by O(d), not exponentially. The first passing point is data-dependent but covered by the same event.

The prototype implements retained banks and externally bound fixed grid-point receiving. The finite search driver pays every attempted point; its small executable budget is not a theorem that useful acquisition is cheap.

### Acquiring coordinates rather than supplying a useful partition

Start with equality classes of the native task feature rows, not an advised good operator basis. For a fixed current partition, use the preceding receiver. Connect rows within each block when their maximum action-response L1 difference is <=4e, where e is the simultaneous per-row radius, and take connected components. This is the already accepted response-refinement rule with C scaled by t; the prototype exposes `initial_partition` and `refine_received`.

The exact coarsest stable refinement exists because the singleton partition is stable. If a target stable partition refines the current one, Z_current=Z_target L, so H_current=H_target L and U_current=U_target L. Rows in a target block have identical current response signatures. On the confidence event they are always connected (estimated distance <=2e), so refinement does not split a true target block. If distinct exact current signatures have minimum distance Delta>0 and e<Delta/6, the connected components recover the exact next refinement, because distinct signatures have estimated distance >4e. At most n-r0 strict refinements are possible. A finite-precision stall is UNKNOWN, not proof of stability or no structure.

Each changed partition uses a fresh independent prefix bank. An outer round s=0,1,... receives confidence delta_total 2^(-s-1), split again over the cap/sample grid. All old paths remain usable for discovery/ordinary baselines, but they are not silently reused as independent r-dimensional validation. The microscopic meeting clock itself does not depend on the partition; the conditional fast-clock assumption in Section 5 therefore need not be postulated again for each coordinate system. A finite declared round/grid budget is a complete search procedure with possible refusal, not an efficient teacher. The prototype tests refinement receiving separately; it has not executed a successful multiround acquisition. Its actual observed small run retains the stated native partition and returns UNKNOWN.

## 5. Conditional success without assuming the clock as an input

Validity above requires no decay. To state a favorable performance regime, suppose the *actual* pair clocks satisfy p_K<=c exp(-K/kappa), uniformly over queried rows/actions. These unknown constants are NOT supplied to the algorithm and are not substituted into its certificate.

Fix desired per-row accuracy e in (0,1). Choose a dyadic K with

    c exp(-K/kappa) <= e(1-gamma)/64,

and N large enough for

    N >= 128 K^2 ell_H/e^2,
    N >= 96 ell/e(1-gamma),

where ell bounds both tail-confidence and a separate upper-count success logarithm. Choose upward-root precision with 2^(-bits)<=e(1-gamma)/64. This pays the amplification of the tail-probability rounding by 1/(1-gamma), not merely the prefix rounding. On an additional union event of prescribed probability, the upper Bernoulli count obeys h<=2p+2ell/N. The nonzero formula gives p_U<=2h+2ell/N+2^(-bits)<=4p+6ell/N+2^(-bits); the zero formula is smaller. Thus p_U<=9e(1-gamma)/64 and the tail radius is <=9e/32. The Hoeffding prefix radius is <=e/4 before rounding, hence e_ia<=e (with slack). The empirical-Bernstein alternative can improve this sufficient schedule but is not needed for this theorem.

Consequently K=O(kappa log(c/[e(1-gamma)])) and

    N=O(K^2 ell/e^2 + ell/[e(1-gamma)]).

All logarithms include F, confidence and grid-search overhead. The call bound from Theorem 3 is O(F NK log(N(K+1))), not gamma-independent. With fixed kappa,e and dimensions this is linear in (1-gamma)^(-1) up to logarithms. The earlier geometric-endpoint sufficient schedule with a constant canonical geometry had inverse-cubic discount scaling. This is a comparison of sufficient constructions, not a lower bound on an ordinary retaining learner; coupled-Poisson learners get this improvement too.

### A noncircular canonical success condition

Suppose true response closure holds and the exact small coefficients have a feasible canonical witness X0 with gap delta0>0, transformed diagonals <=1, and nonpositive transformed off-diagonals. No such witness is an input to acquisition; it is an analysis condition on the source family. Every coefficient column of A=[(I-B_Ua)^T]_a sums to 1.

Take lambda=delta0/[2(1+delta0)] and

    X1=(1-lambda)X0 - (lambda/r)11^T.

All transformed off-diagonals now have slack at least lambda/r; all column sums are >=delta0/2; transformed diagonals remain <=1. Let J=max_ij |(X1)_ij|. If the empirical small coefficient row errors are <=e, every transformed entry changes by <=Je and every column sum by <=rJe. For e<=min(lambda/(2rJ),delta0/(4rJ),1/J), this yields a perturbed positive witness with column sums >=delta0/4 and diagonals <=1+Je. Rescale by 1+Je. Its gap is >=delta0/8 and its C_X<=4/delta0. Therefore a correct exact maximum-gap LP obtains a gap at least delta0/8 and, since baseline columns bound its diagonal X by 1, C_X<=8/delta0. It follows that regret <=48e/delta0 after eta_U<=3e.

This establishes a neighborhood where ordinary LP acquisition succeeds, rather than assuming noisy fixed-point contraction. Standard rational polynomial-time LP is a theoretical consumer; the actual installed simplex backend supplies proposals only, may fail or exceed its budget, and its returned feasibility is checked exactly. No practical run or worst-case simplex guarantee is claimed. The earlier false assertion that every max-gap optimizer minimizes C_X is NOT used: only existence of a positive gap lower bound and the baseline diagonal bound are used.

### The stronger ordinary coupled-geometric baseline

The earlier independent-endpoint construction is not the strongest comparator. Independently draw T with P(T=s)=(1-gamma)gamma^s. Run the SAME paired paths only until min(tau,T), and output

    Xi=t [Z(X_T)-Z(Y_T)] 1{T<tau}.

It has mean U, costs 2+2 min(tau,T) calls, and uses no shared-randomness source oracle: only the internal stopping time is shared. If E tau<=kappa, each coordinate has variance <=t^2 P(T<tau)<=gamma^2 kappa/(1-gamma). The ordinary empirical-Bernstein learner with known range 2t and a uniform sample-count grid consequently also has inverse-linear discount sample scaling, rather than inverse-cubic. It retains all intermediate labels and can additionally run the capped receiver. It is a required strong comparator, not a method to exclude.

Conditional on a full meeting path, the expectation of Xi over T is the untruncated paired Poisson sum. The capped prefix is its partial Rao–Blackwellization plus an unresolved-tail certificate. Under bounded kappa, a sufficient coupled-geometric sample bill is O(r^2 kappa ell/[(1-gamma)e^2]+r ell/[(1-gamma)e]); the capped-prefix bill separates K^2 ell/e^2 from ell/[e(1-gamma)]. Thus it can remove an extra accuracy factor from the *rare-tail-dominated* sufficient bill, but not the information floor in Section 6. These are ordinary variance-reduction and confidence mechanisms, not proof of a new exclusive capability. Numerical/backend and all state-preparation costs remain.

## 6. A task-level rare persistent-effect obstruction

Let n=r=2, Z=I, and grant the learner the KNOWN baseline A0=I. The one unknown action is

    A1(p)=[[1-p,p],[0,1]].

Then H=I and U1=c[[-1,1],[0,0]], c=gamma p/(1-gamma). For epsilon in (0,1/16], gamma>=1/2, compare p0=0 and p1=8epsilon(1-gamma)/gamma. Their canonical witnesses X=I/(1+c) have gap 1/(1+c)>=2/3. Nevertheless the impulse response (A1-A0) A0^s Z is constant forever whenever p>0. Static canonical stability does not bound a physical response clock.

Use the SAME bounded action-reward task on both sources: at state 0 action 0 earns 2epsilon, action 1 earns 0; at state 1 both earn 1. A stationary randomized table uses action 1 at state 0 with probability theta. Its normalized state-0 value is

    V0(theta)=2epsilon(1-theta)                         on p0,
    V1(theta)=(2epsilon+6epsilon theta)/(1+8epsilon theta) on p1.

On p0 epsilon-optimality forces theta<=1/2. On p1, theta<=1/2 has regret at least

    epsilon(3-8epsilon)/[(1+8epsilon)(1+4epsilon)] > epsilon.

All queries except (state0,action1) are deterministic and identical across sources. For any learner making at most T forward calls, its entire p0 transcript has likelihood at least (1-p1)^T under p1, including arbitrary adaptive query choices and internal randomness. Thus confidence 1-delta epsilon-optimality on both sources requires

    delta >= (1-p1)^T(1-delta),
    T >= log((1-delta)/delta)/[-log(1-p1)].

Here p1<=1/2, so this is Omega(log(1/delta)/[epsilon(1-gamma)]). The obstruction also holds for expected acquisition on the instantly meeting null source, not just a fixed worst-case budget. Let G be the p0-good output event and N0 the random number of informative probes under p0. Change of measure and Jensen give

    P_p1(G) >= E_p0[(1-p1)^N0 1_G]
             >= (1-delta) exp(-[-log(1-p1)] E_p0[N0]/(1-delta)).

(The function q exp(-a M/q) increases with q, and E[N0 1_G]<=E[N0].) Thus E_p0[N0]>=(1-delta) log((1-delta)/delta)/[-log(1-p1)]. This applies to an almost-surely terminating randomized learner, with finite expected cost; infinite expected cost already satisfies the lower bound. This is an information obstruction for the stated stationary-table task and access language, not a general learning impossibility and not a lower bound for controllers granted uncharged deployment learning. Baseline probabilities and preparation have already been made easier for the learner.

On p0 every paired trial meets immediately. It is still expensive to certify absence of the rare persistent effect. Taking a huge K at no observed continuation cost cannot evade the bound: the prefix range L_K and its empirical-Bernstein range/N term grow, even when the empirical variance is zero. A verifier that uses the realized maximum meeting time as the range is unsound. The literal two-state source is efficiently handled by ordinary direct Bernoulli estimation; no clock-method superiority is claimed on this lower-bound fixture.

## 7. Failures and consequence

The acquired operation is a discounted, action-initialized response/error certificate usable by an ordinary reusable decision compiler. It need not acquire global mixing or a predictive aggregate Markov model. Reducible baselines can qualify if each action-initialized pair stays within a quickly coalescing component. Conversely, disjoint or periodic trajectories can fail microscopic meeting while all chosen observable effects vanish; the method then refuses or pays a large bill. Independent coupling is not the best available coupling in many sources. In fact, if A0 and every action are the identical uniform kernel on n states, all action responses vanish and baseline mixing takes one step, but independent-pair survival is (1-1/n)^(K+1) and E tau=n-1. The learned microscopic-meeting certificate can therefore have an ambient-n penalty even when the true control effect is zero. A known common-noise coupling or structural probability description could eliminate it; neither is granted by this interface. This is a method limitation, not a lower bound on every retaining learner. Strong ordinary coupling, Poisson, bias, successor-feature, direct row-estimation, and model-based methods retain all this data and may win.

No civilisation-level consequence, historical novelty, universal acquisition saving, or executed small-error all-goal success is asserted by the present prototype. The organizing result is the separation between (i) a learnable local response clock, (ii) the unavoidable price of excluding rare persistent effects, and (iii) the already acquired computational decision geometry. These are different resources.
