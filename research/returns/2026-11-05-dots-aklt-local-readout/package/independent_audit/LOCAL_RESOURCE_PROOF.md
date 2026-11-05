# Independent resource bound for the query-local sampler

## Result

For any finite vertex query K, on the infinite square lattice or in an open finite box, the implemented local engine satisfies

- E(total length of retained clan cylinders) < 34.481635 |K|;
- E(number of retained clan cylinders) < 6.539013 |K|;
- E(number of calls to the local birth oracle, including every null seed and parent proposal) < 14.120548 |K|.

The pair/history scans have finite moments, uniformly in the surrounding physical volume. Their crude second-moment bound grows at most quadratically in |K|. This is not a bound on expected exact-real bit complexity, a latency guarantee, or a speed comparison with another sampler.

The exact arithmetic is reproduced by certify_local_resources.py and recorded in its JSON output. The upstream full tilted type-kernel certificate is assumed here; it was separately audited.

## 1. Root mass and type weights

Let K(i,j)=w_j[1-delta(i,j)]. The full spatial sums range over actual placed loops, not just shape types. Set a_i=L_i v_type for short loops and a_i=L_i for long loops. The upstream rational certificate gives

sum_j K(i,j) exp(mu L_j) a_j <= q a_i,

where q=.907806, mu=log(1000001/1000000), .711122124 L_i <= a_i <= L_i, and a_i >=3.749901596.

At a fixed vertex, the total tilted loop-length mass is the sum of the degree-two straight, degree-two turning and degree-four contributions. Thus

B = S2 + T2 + M4 < 2.260657078927

bounds sum_{i containing vertex0} w_i L_i exp(mu L_i). There is no extra factor two at a degree-four vertex here: M4 already counts each loop once, whereas a cyclic-visit density would count it twice. A union bound gives local seed root-length mass at most B|K|.

## 2. The discovery forest, rather than the full ancestor DAG

Assign each newly retained cylinder to the first queried child that discovers it. Existing known cylinders may add parent edges, but never add another node to the queue. Before old-region exclusions, a queried type-i cylinder generates a fresh independent PPP of candidate parent types with intensity K(i,j): the local birth proposal is exactly thinned by its independent conflict mark with that child.

Excluding old exposed regions only deletes candidates. Complete the missing candidates with phantom offspring, and independently continue their offspring as well. This couples the implementation's discovery forest below an ordinary multitype Poisson branching forest with offspring intensity K. It does not assume independence of the actual ancestor DAG, does not redraw known ancestors, and does not invoke any all-order connected-derivative or witness-tree formula.

The roots are the true PPP of loop cylinders alive at0 and meeting K. Consequently the expected total a-weight is at most B|K|/(1-q). Dividing respectively by v_min or a_min gives the length and node bounds above.

## 3. Charge every proposal

Write lambda=66455976045001/166988328468480, the exact local proposal rate per queried vertex. Initial proposal count has mean lambda|K|. Conditional on each queried cylinder i, its fresh parent proposal count has mean lambda|V_i| <=lambda L_i. By predictable conditional expectation and the total-length bound,

E P <= lambda |K| + lambda E sum_i L_i <14.120548 |K|.

Nulls and proposals rejected for old-region overlap are included. This bound is not just a count of accepted physical loops or discovered ancestors.

## 4. Joint MGF and finite scan moments

The branching completion can retain all pre-thinning proposals as cost marks. Let A be total retained a-weight and P count every oracle proposal. For one root type i, let F_i be the MGF of its completed descendant tree, including its own a-weight and all proposals generated while processing its descendants. Marking every parent proposal by exp(t), and true parent offspring by their descendant MGF, gives the positive recursion

F_i = exp[s a_i + lambda_i(exp(t)-1) + exp(t) sum_j K(i,j)(F_j-1)],

where lambda_i=lambda|V_i| <=lambda a_i/v_min. It suffices to use F_i<=exp(c a_i). For 0<c<=mu,

sum_j K(i,j)(exp(c a_j)-1)
<=c sum_j K(i,j) a_j exp(mu L_j)
<=c q a_i.

Take c=9/10000000 and s=t=1/100000000. Since log(1+x)>=x/(1+x), c<mu. The exact rational checker verifies

s + (lambda/v_min)t/(1-t) + c q/(1-t) < c.

Because exp(t)<=1/(1-t), this is a strict supersolution. Generation truncation and monotone convergence justify the MGF without assuming its existence first.

The seed proposal PPP also includes null proposals. Its compound-Poisson MGF is bounded by

E exp(s A+t P) <= exp(H |K|),
H = [lambda t + c B]/(1-t) < .000002039.

Here the seed uses exp(c a)-1<=c L exp(mu L). All retained nodes and all proposal counts therefore have finite joint moments. Scaling (c,s,t) by any beta in(0,1] preserves the supersolution. Taking beta=1/max(1,|K|) yields a bound on E[(A+P)^m] of order |K|^m for every fixed m, with very loose but finite constants.

Let M be retained clan size. The code tests at most M(M-1) known pairs and at most MP previous-region memberships. Each cover test uses at most two exact comparisons, and the seed-region test adds at most P. Since M<=A/a_min, these counts have finite expectation and all fixed moments. Enumerating set intersections and sorting candidate IDs introduces additional polynomial factors; this still does not establish the expected arithmetic cost of the exact-real comparisons.

## 5. Oracle cost and remaining bit-cost issue

The finite-memory torus bridge has a geometric survival bound from the memory-6 Collatz certificate, so each local oracle call has all fixed path-length moments uniformly over K and physical box. The constructor is separately certifying its sharper exact constants. Combined with E P this bounds the total expected walk-transition and canonicalization cost, with due accounting for query sorting and the history scans above.

Almost-sure termination of lazy-real comparisons is independently proved by exact rational log enclosures and continuity. The companion LAZY_TIME_COST_PROOF.md now supplies a qualitative finite-expected-arithmetic argument using sequential timestamp anti-concentration and this joint proposal-count MGF. It gives no useful numerical bit-cost constant or linear query-size guarantee. A detailed implementation-level cost audit of the Poisson primitive remains separate from the exact first-moment certificates above.
