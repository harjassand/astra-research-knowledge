# A finite raw-network trace/pool certificate finder

30 October 2026. New working method and soundness proof, NOT independently reviewed. This preserves all earlier reviewed examples. It is a terminating sufficient-certificate search for a restricted architecture, not a complete algorithm for arbitrary chemical recurrence.

## 1. Raw input and what is actually acquired

Input: a finite list of physical species, nonnegative integer source/product complexes, and rational nonnegative rates (zero-rate edges removed). Reaction IDs are unique. No pivot species, dormant face, pool, stationary law, population cutoff, or Lyapunov vector is supplied.

The implementation `acquire.py` searches the physical reaction list for a connector

    0 -> A+B -> mA+qB -> 0,   q>m>=4,

then sets a0=m-2. Every remaining edge must share the catalytic offset a0 A+qB on both ends. After subtracting it, each remaining residual source AND product must have total count2, and no residual B may remain. Clearing is kept as the kill k0(a)_2. This is an exact mass-action factorization, not a low-copy approximation.

A pivot D is selected from the common non-A support of all outgoing 2a seed products. Every such seed must produce positive D. The positive a+D->2a edge is required. The algorithm then acquires:

* the true dormant predicate F;
* the mixed-face first-event trace-cost certificate;
* the initial mixed-face population-clock certificate;
* a partition into pooled types, one protected D-pool particle, and a baseline graph;
* a path exponent L and explicit local decay exponents.

It also checks weak reversibility of the full physical graph before issuing a global-template certificate. Failure means only `NO_CERTIFICATE_IN_THIS_CLASS`.

## 2. Derive F from the raw restoring sources

For a candidate D, inspect every nonseed residual edge whose source has D-count0. Require that its source and product have a-count0 and its product has positive D. Call these restoring edges. At D=0, define

    F = {all restoring sources disabled},
    Bmix = {at least one restoring source enabled}.

The active module M consists of positive D and Bmix, on physical A>=a0,n>=2. F may contain many support/count faces. Its predicate depends only on hidden counts, not A, so its exact hidden state is frozen during the seed-free A,B connector law. At Bmix the next event is exactly one reverse/restoring jump, a seed, clearing, or connector. Restoring/seed outputs have positive D. There are no unpriced Bmix-to-Bmix transitions.

The finite source-enable signatures use hidden counts0,1,>=2. These may be retained as disjoint face types, but the ACTUAL hidden counts are metadata, not independently resampled labels. On F the marked A,B Green is the same previously earned dormant kernel for every frozen hidden state. Its operator norm is a supremum, not multiplied by the number of faces.

## 3. Exact finite algebra for the clocks and terminal boundary

Every D>0-to-D=0 ingress occurs at D=1 or2 because residual sources/products are binary. Partition all other input counts into cells

    0, 1, 2, 3, or 4+z_i with z_i>=0.

These cells fix source and output enablement under every possible jump shift (at most2). Evaluate falling-factorial rates exactly as polynomials in the remaining z_i.

On an ingress whose actual output is Bmix, let L_B be its restoring+seed+clear exit hazard. Require a rational coefficientwise certificate

    q_ingress(x) <= C_r L_B(x+nu_r).

All displayed polynomial coefficients must be nonnegative. Sum the per-reaction constants; an entrance compensator then pays total mixed operational occupation by C times positive-D operational occupation, regardless of return count. Fixed A-power rewards and physical factor restoration only change constants because entrance A shifts are bounded. Initial Bmix holding is not included in this sum and is checked separately.

For ingress whose actual output lies in F, require BOTH

    a_out>=2,
    q_ingress(x)<=C_r(1+a).

The first keeps a true-F entrance active and permits the fixed-b first-connector feedback. The second gives a low-cutoff return hazard O(K) and a high-A return hazard dominated by the clearing compensator. Sum, rather than maximize, the per-reaction constants. Every such output is terminal even if the protected pooled coordinate below is positive.

For initial Bmix states, require the additional coefficientwise bound

    1+n <= C_init L_B.

This is load-bearing. An enabled restoring edge with O(1) rate need not be fast when an uninvolved hidden species carries all large mass. The executable rejection test in Section8 detects exactly this failure. At low a<K the bound makes direct terminal probabilities O(K^2/n); at high a the seed/clear hazard pays the incoming inverse-power grade. Thus initially mixed inputs inherit uniform resets after their actual restoring/seed output enters positive D.

Each successful coefficient comparison is an exact nonnegative-polynomial identity over a continuous orthant, hence valid for every integer population in its cell. There is no finite-population extrapolation. This criterion may reject inequalities provable by another representation; completeness outside this explicit certificate cone is not claimed.

## 4. Acquire pools and a baseline graph without hand selection

Enumerate partitions of the residual species with a as a singleton. In the block containing D subtract one protected particle. Write

    Y_i=sum_{species in pool i} x_species - 1_{D is in pool i}.

For D>0 these counts are nonnegative and sum to n-1. Require every restoring edge to have zero pooled increment. Thus a mixed-face restoring jump is silent in Y. The implementation tries finer partitions first; there is no supplied E+D pool.

Divide the rates of nonsilent positive-D reactions by D. Every nonseed nonsilent pooled increment must be a unit transfer i->j. Since sources are binary and contain D, its divided rate is affine: k x_l for X_l+D, or k(D-1) for2D. Group rates by pooled transfer.

For j!=a, require the grouped rate to be EXACTLY q_ij Y_i. For j=a, extract a nonnegative baseline q_ia Y_i whose remaining affine coefficients are nonnegative after D=1+u_D; arbitrary nonnegative excess is permitted only toward a. Zero baseline edges can be omitted. Require every pooled type to have a directed baseline path to a. Full irreducibility is unnecessary: the protected D pool may feed a without being reachable back from a by the baseline graph.

These tests are rational coefficient identities/inequalities. A positive pooled rate from an empty non-D source pool is impossible by source enablement. An empty protected pool can have an extra a-producing jump only at D=1; its actual D=0 output has no particles in that pool. Pool neutrality of restoring edges then makes every restoring source disabled, so it is a true-F stop; the terminal guard in Section3 applies. The process is never continued with a negative pooled count.

To realize baseline clocks, split each grouped physical rate into the desired q_ij Y_i and its nonnegative remainder. Give each abstract pooled label independent q_ij clocks, choose the actual physical channel in proportion to its available rate, and assign/reassign internal physical labels within each pool. This preserves the observable generator. It does NOT assert independent physical-species paths. Only adapted extra transfers toward a remain.

## 5. Soundness of the local probabilistic certificate

Let L be the maximum shortest baseline distance to a (replace0 by1). For a label of any initial pooled type, prescribe its shortest path in successive subintervals of a small D-clock horizon t and suppress all other baseline rings, including departures from a. Extra transfers toward a can only shortcut the path; once at a, the suppressed departure clocks retain it. Conditional on the history at the start, these forcing events are independent across labels and have probabilities at least c t^L. No independence after survival conditioning is used.

Nonlinear seeds remove at most two original-a cohort labels per mark. Their total count before clearing has a geometric tail because all seeds and clearing share (a)_2. Restoring edges are pooled-silent and a-neutral. The deterministic-horizon/crossing argument therefore gives, for the ACTUAL M-stage stopped at F, clearing, or connector,

    P(inf a_t<c a_in) <= C n^M exp(-c a_in).

For long horizons use a last-unit prescribed path conditional on each label's current type; for short horizons use an initial-a no-departure event. Full baseline irreducibility is not needed.

Polynomial time moments are earned independently. From positive D choose a pooled label and follow its path to a, interleaving at most one restoring jump whenever a step reaches Bmix. The positive a+D->2a edge then supplies2a, unless an earlier true-F stop already occurred. Every true-F output has a>=2, so full fast clearing is available there too. An initial Bmix state first restores D. A fixed budget H=2L+5 suffices. Required operational propensities have positive lower bounds; totals are O(n^2). Requiring each prescribed holding time<=1 gives conditional H-unit block success c n^(-2H), hence all fixed polynomial moments without independent blocks.

For a<K, the n-1 labels and forcing events give a D-clock arrival horizon t*=C(K/n)^(1/L), with failure exp(-cK). Actual seed restarts have bounded geometric mean; horizon failures obey the usual conditional chunk-count inequality. Therefore E u_low<=C t*. The exact trace certificate restores all mixed physical/operational holding costs. Low clearing costs CK^2 t*, true-F return CK t*, and connector stopping Ct*. High continuation is paid by the cohort estimate and actual clearing hazard.

Consequently, for every fixed s>0,

    E f_s(A_out) <= C_s n^(-s/(Ls+2L+1)),
    P(enter F before clear/connector) <= C n^(-1/(2L+1)).

The latter balances K(K/n)^(1/L) with1/K. Positive-power uniform bounds for (b)_q T and (b)_q U follow from

    (b)_q T <= C[t*+K^-m+poly(n)exp(-cK)],
    (b)_q U <= C[K t*+K^(1-m)+poly(n)exp(-cK)].

Initial Bmix states use their separately certified growing exit hazard, not the ingress sum.

The logarithmic-input split then earns every fixed finite profile and m/(m-1) spending grade. On x>=C log^2(2+n), the same-episode ratios are

    T/U<=C/x,
    V_p/[(b)_q U]<=C_p x^(a0-p),  p>=a0.

The true-F rate bound and bounded output A shift give the last predictable compensator. Cauchy-Schwarz with the SAME terminal f_(2s) law supplies a true-F profile return O(n^(-1/(4L+2)))f_s.

## 6. Soundness of the full-template conclusion

All the local interface items required by the reviewed exponent-robust signed-cycle construction are now acquired. On F, hidden counts and their face signature are frozen until the actual seed, so the marked dormant Green is a direct sum of identical A,B kernels. Its sup norm is uniform in actual hidden counts. The return estimate controls the TOTAL output measure on F, not just diagonal face transitions. Thus arbitrary finite face signatures, and their carried hidden metadata, introduce no unpriced multiplicity.

The full fixed-b equations, tilted finite-grade processor, complete positive source CwT, genuine negative activation word, log-squared good set, and non-small dormant preconditioning use only these interfaces and the conserved N,B phase identities. They retain the actual seed phase and output face. The positive-D bad weight is replaced by w r^-eta for a sufficiently small acquired eta>0; actual-output domination by w f_m makes the cross-block product small.

Activity is also acquired, not assumed. For A>=a0,n>=2, positive D has an enabled baseline path or the required a-born edge; Bmix has a restoring edge; true F is active exactly at a>=2. Every true-F ingress was checked to leave a>=2. Seeds/restoring outputs have positive D. Hence fast moves preserve the exact active indicator. Inactive approaches and finite-head Z trials are therefore covered by the original actual-trial proof, with the finite clearing path above. The initial physical holding interval still gives U>=c r^-m at section B=q because all residual propensities remain degree2.

The two-direction physical-clock/Foster patch is unchanged once these hypotheses are proved. Conserved fast total count and high-degree connector clearing give independent nonexplosion. The explicitly checked weak reversibility makes communicating components closed. Subject to review of this generic soundness transfer, a returned certificate therefore supplies classwise positive recurrence and each requested total-count exponential invariant moment for its input network. No conclusion is returned for rejected inputs.

## 7. Costs and limits

The search is finite: finitely many connector candidates/pivots, at most a Bell number of set partitions, and O(5^(k-1)) boundary cells per ingress plus mixed-growth cells, where k is the residual species count. All proof-check arithmetic uses rational rates and coefficients. Coefficient bit lengths, forcing constants and final asymptotic cutoffs can be very large; no polynomial-time, well-conditioned or practical large-network guarantee is made.

The method requires conservative binary residual reactions, a common connector offset, one-hold a-neutral restoring faces, pooled unit transfers, and a baseline with only a-directed excess. It does not synthesize arbitrary weighted pools, multi-step internal face chains, adverse extra transfers, or arbitrary nonlinear forcing. `NO_CERTIFICATE_IN_THIS_CLASS` is not evidence of transience or null recurrence.

Ordinary ingredients remain essential: exact trace/censoring and entrance compensators, finite-chain path events, and stopped-time/Foster (including Filonov) inference. The new construction being tested is a finite finder/checker that chooses the decomposition and pools and exposes missing clock premises; it is not a historical novelty claim for those ingredients.

## 8. Actual exact-rational run and a necessary rejection

The raw coupled physical list is accepted without supplied D, F or pool. Output:

    D pivot; F={D=0 and CE=0}; pools {a},{C},{E,D};
    baseline a->C->pool->a; L=2;
    mixed ingress constants 1/7 and1, total8/7;
    return exponent1/5, weighted exponent1/10, f_m reset4/13 (m=4).

The raw unpaired conversion-cycle list is accepted with singleton physical pools, including protected D; its baseline is NOT irreducible, but every type reaches a. Removing the mixed reverse is rejected because a low-A true-face output is inactive.

A stronger test keeps the reverse and adds a hidden X connected by a+D<->X+D. Its baseline/trace structure would otherwise fit. At a=0,C=E=1,D=0,X=N, the mixed restoring rate is constant while total mass grows. The initial mixed-growth polynomial certificate fails, and the algorithm rejects it. This is a genuine missing-clock diagnostic, not a finite numerical failure or recurrence counterexample.

The implementation/results are exact certificate bookkeeping and must be reviewed separately from this mathematical soundness proof. No simulation is used as an infinite-state proof.
