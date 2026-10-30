# Independent sharp robust-forcing exponent review

30 October 2026. Abstract controlled finite-type theorem, not a stronger raw-network recurrence claim.

## Verdict and scope

**Accept the sharp exponent theorem and the separately frozen no-deletion population-scale corollary**, under the previously reviewed freely selectable, unbounded excess-rate contract. Fixed baseline rates and support are held constant. The rank finder succeeds, a non-target type exists, and L is its least-rank maximum. Then the infimum terminal probability over all initial types and admissible controls is Theta(t^L) for0<t<=1.

Sources are frozen in `sharp_rank_sources/` and recorded in `SHARP_RANK_SOURCE_SHA256.txt`. Main theorem SHA:54b9d18ad0529b3ed0d7137b9b1013da2d8d25aa86d1025f65bc634d59eec358. The optional population corollary is reviewed explicitly, not silently included as a stronger chemical statement.

## 1. Least rank and lower bound

The prior completeness induction implies that all vertices of any valid rank at most k are processed by round k. Therefore the greedy rank is no larger at each vertex than any other valid integer ranking. It is itself valid, hence componentwise least and minimax for its maximum. No rate optimization or claim about different pool partitions is involved.

The independent progress/no-residual event supplies

    F(t)>=exp(-(Qmax+qmin)t)(qmin t)^L/L!.

For0<t<=1 this yields a fixed positive multiple of t^L, uniformly over actual starting types and adapted excess histories. The constants may depend on the fixed rates and graphs.

## 2. The intermediate-parent issue is resolved

A dangerous final-rank-k vertex has a baseline edge into S_(k-2). It was therefore initially eligible at round k-1. Since its final rank is k, it was pruned in that round, not merely ineligible. Its recorded parent points to an earlier-pruned vertex or an initially ineligible vertex; it never points to a survivor of that round or an already processed vertex.

Every vertex on this parent chain consequently lies outside S_(k-1), so its final rank is at least k. Every chosen edge belongs to the allowed excess graph and the final rank is valid, so ranks along the chain cannot increase from the starting value k. These two inequalities force equality throughout the chain. This argument includes intermediate parents, not just the terminal safe node.

An intermediate parent that was itself pruned was initially eligible in the SAME historical round. Having final rank k, it is itself dangerous, and its globally selected parent and distance are taken from that same record. A terminal initially ineligible parent has no baseline edge into S_(k-2), is safe at rank k, and has distance zero. Thus the global distance assignment is consistent and every chosen edge decreases it by exactly one. Distinct rank layers cannot create a cross-layer distance conflict.

Safe rank-k vertices have no baseline decrease of two or more. Rank0 and rank1 vertices are automatically safe. Parent paths are acyclic by deletion order and have length at most the finite number of types.

## 3. Finite-rate skip suppression and sharp upper bound

The chosen control assigns K to each dangerous parent edge and zero to other extras. All chosen moves preserve rank exactly. The bounded global distance satisfies

    Ld<=-K 1_D+n Qmax.

Finite-chain Dynkin and nonnegativity of the terminal distance give the stated occupation bound. The compensator for baseline jumps decreasing rank by at least two has hazard at most Qmax on D and zero elsewhere, yielding the actual probability bound O((1+t)/K). This is a probability estimate, not an inference from large mean hitting times.

On no-skip paths, reaching rank zero from rank L needs at least L baseline jumps: each baseline decrease is at most one, baseline increases only add work, and selected excess moves preserve rank. A rate-Qmax uniformization clock dominates the baseline jump count, even if a baseline and controlled channel share the same physical edge; the colored clock realization has the correct summed generator. Endpoint occupancy implies a previous hit, so the count argument bounds endpoint probability as well.

Taking the infimum over admissible finite-K controls and then K to infinity gives the Poisson-tail upper bound. The factorial-moment inequality P(N>=L)<=E[(N)_L]/L!=(Qmax t)^L/L! is valid. No infinite-rate process or exchange of a path-law limit with expectation is needed. The maximizing-rank initial type may be fixed independently of K.

Together with the lower bound this proves exact power order. It does not claim existence or optimality of a limiting leading coefficient, nor an exponent for one fixed excess law.

## 4. Checks specifically exercising long parent chains

The frozen graph checker was rerun and its JSON matched exactly. Independent test `test_sharp_rank_challenge.py` includes a five-type example with rank2 parents2->3->4, where both2 and3 are dangerous and4 is safe. The computed global distances are2,1,0, directly exercising the requested intermediate-parent issue.

I also tested5,000 independently seeded random graphs with3–10 types. Of these,1,469 accepted policies passed exact rational generator inequalities at every state with finite K=13. There were173 policies with multiple-edge parent chains, with maximum checked distance4. These tests supplement, not replace, the all-size parent/rank argument.

## 5. Optional population-scale corollary

Interpret the threshold as an integer1<=K<=n, with no label deletions. The independent potential forcing events imply that the actual target count at time t dominates their binomial count even under correlated excess histories. H_K>t implies the target count at t is below K; this gives the stated exponential upper tail when t=C(K/n)^(1/L)<=1 and C is sufficiently large. That condition restricts the claimed regime when K is a substantial fraction of n; it is not a bound for arbitrary K near n at a fixed small time.

For the converse, the same finite-K reset policy actually bounds FIRST hitting, not merely the endpoint: a first hit still requires L baseline rings unless a skip occurred. Starting all labels at a maximal-rank type and applying the finite-rate policy to each gives the stated bound on each ever-hit indicator. Reaching K simultaneously implies at least K distinct ever-hit labels, so Markov's inequality needs no label independence. Choosing finite reset speeds for each n makes both terms vanish whenever n t_n^L/K_n tends to zero. With1<=K_n<=n this is automatically an eventual small-time regime.

Thus (K/n)^(1/L) is sharp for a guarantee uniform over the abstract freely scalable control class. It is not an expectation claim for H_K, an optimal chemical reset exponent, or a fixed-network rate lower bound.

## Final boundary

The sharpness policy relies on turning some excess channels off and scaling others arbitrarily. Fixed raw reaction intensities may not realize it. The result sharpens the abstract forcing interface only; it neither supplies a chemical recurrence necessity condition nor optimizes the later Lyapunov powers. All raw face, pool, boundary, activity and global transfer guards remain separate and unchanged.
