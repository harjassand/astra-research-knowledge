# Independent robust-forcing converse review

30 October 2026. Abstract controlled finite-type result only; no additional chemical-network conclusion.

## Verdict and domain

**Accept the converse and resulting equivalence**, under the stated contract: fixed finite baseline rates, a finite allowed excess support, and freely selectable nonnegative nonanticipative excess intensities yielding a nonexplosive process. For each fixed t>0, a uniform positive lower bound on terminal target probability over ALL initial types and ALL such controls exists exactly when the rank criterion succeeds.

Frozen main source: `ROBUST_FORCING_CONVERSE.md`, SHA c30994c1efdb66d9c75645b52d9e696c8b81b56900847e66e207d4824b98d3a9. The graph checker and output are frozen in `robust_converse_sources/`; exact hashes are in `ROBUST_CONVERSE_SOURCE_SHA256.txt`. The previously reviewed rank forcing lemma supplies sufficiency.

The infimum is over an unbounded control class. There is no fixed common upper rate bound K. Each counterexample control is finite-rate and time-homogeneous; only the sequence of its probabilities is taken to a limit. This is essential to the statement and correctly distinguished from fixed raw chemical intensities.

## 1. Sufficiency at every fixed positive time

For 0<t<=1 the independent progress/no-residual event gives the explicit uniform positive bound from the prior receipt. For t>1, apply the unit-interval forcing event on [t-1,t] conditional on the actual history at t-1. The same bound works from every current type and for every admissible continuation of the adapted control. Thus the statement is genuinely for every fixed t>0, not only small times.

Rates are understood as usual nonanticipative/predictable intensities. No claim is made for a controller that changes the fixed baseline generator or is given an inconsistent anticipatory filtration. The nonexplosion condition permits the stopped clock realization used in sufficiency.

## 2. Excess departure from the target

With one chosen a->j excess set to K and all others zero, incoming baseline flow to a is at most Qmax. Baseline outgoing flow is nonnegative and only helps the upper estimate, so

    p'(t)<=Qmax-Kp(t),
    p(t)<=exp(-Kt)p(0)+(Qmax/K)(1-exp(-Kt)).

The stated weaker bound follows and tends to zero for each fixed t>0. It works even from initial a. This is an endpoint/retention obstruction, not a first-hitting obstruction. Qmax=0 is also covered.

## 3. Failed pruning creates an actual finite-rate reset control

At the failed round, let S be the processed set and E0 the remaining vertices with a baseline edge into S. If E0 is empty, turning all extras off makes S inaccessible from every remaining initial state.

Otherwise, each deleted candidate has an excess edge to a vertex outside the current processed-or-eligible union. In the batch implementation this means a previous deletion or Z=R\E0, not another vertex in the same current batch. Its parent distance is therefore already defined. Parent chains are acyclic and terminate in Z, with length at most |I|. If Z were empty initially, no candidate could be deleted at all; hence the claimed nonempty safe set is justified.

Give each chosen parent edge rate K and every other excess edge zero. These selected edges stay in R. The path potential d decreases by exactly one on each chosen excess; every baseline jump can increase it by at most k. Extending d=0 on S gives

    Ld<=-K 1_E0+k Qmax

on R. For the finite stopped chain, Dynkin yields

    K E integral_0^(t wedge sigma)1_E0 ds
       <=d(i)-E d(X_(t wedge sigma))+k Qmax t
       <=k(1+Qmax t).

Nonnegative stopped d is the required sign; no assumed stationary occupation is used.

Only baseline edges out of E0 can first enter S. The first-entry compensator is consequently bounded by Qmax times this SAME stopped occupation. This proves the source's bound (C). After entry the chain may leave S again, but X_t=a still implies a first entry by t, so the endpoint upper bound remains valid. Every initial i in the fixed nonempty R works, independently of K.

For each K the state space and all rates are finite. Thus no explosive limiting chain, infinite-rate action or future-dependent policy is used. The limit only establishes that the infimum of finite-K endpoint probabilities is zero. The proof handles sparse/disconnected baseline graphs and zero Qmax without a reachability assumption.

The unit-rate 2->1->a example has mean absorption times K+2 and K+1 as stated. More importantly, the occupation/compensator estimate supplies the fixed-time conclusion; divergent means alone would not establish it.

## 4. Checker and independent tests

The checker records the correct parent graph during simultaneous pruning; each recorded parent is already outside the current candidate set. Its certificate verification checks the partition, absent baseline entry from Z, actual allowed parent edges, strict distance decrement and bounded d. Its root is0 in the executable test, consistently with its verifier.

I reran a copy of the frozen checker: all4,096 three-type graph pairs verified and its output matched exactly (384 rank,640 reset,3,072 departure). This is graph evidence, not a substitute for the analytic finite-K proof.

`test_robust_converse.py` additionally checks1,000 seeded random graphs with4–8 types, suppressing target departures to exercise the more substantive reset branch. It found934 reset certificates and66 ranks. For each reset certificate it assigned positive rational baseline rates and checked the generator drift inequality exactly at every unprocessed state with K=11. All passed. Results are recorded separately; sources were not modified.

## Final scope

This proves necessity and sufficiency for uniform fixed-time TERMINAL forcing against every freely chosen excess control with the given support. It is stronger than completeness merely for the syntax of integer ranks, but it is not necessity for a fixed physical rate law. The adversary may turn off and independently accelerate channels that a raw reaction network cannot control. Therefore rank rejection still says nothing by itself about that network's recurrence, transience, actual hitting probabilities or realizability of the reset policy. The source makes this distinction correctly.
