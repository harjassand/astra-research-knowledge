# The constructed probability-rank learner does not yet cover logit rank

30 October 2026. Root's explicit transfer obstruction, not another claimed
learning theorem or a new benchmark. This keeps the discovery question attached
to its actual structural promise.

Primary source checked live: Golowich--Liu--Shetty, arXiv:2512.09892v1,
https://arxiv.org/html/2512.09892v1 , Definitions1.3--1.6/4.2--4.3,
Theorem5.14, Remarks5.8--5.9 and Problem6.2. That paper studies bounded approximate
LOGIT rank with logit-query access, and explicitly asks about conditional-sample
learning without exponential logit overhead. Its empirical/structural promise
is different from probability predictive rank. This primary read does not
establish that its open question remains globally unresolved in October2026.

## An explicit exponential separation

Let X,Y be independent uniform n-bit strings. The last bit Z has conditional
probability

    Pr(Z=1|X=x,Y=y)=sigma(b+lambda sum_i x_i y_i), lambda>0.

This process has a time-varying input-switched linear state of dimension n+2:
retain a constant coordinate, the n observed x_i, and an accumulator initially b.
At each x_i token store its bit using the constant coordinate. At each y_i token
add lambda*y_i*x_i to the accumulator. All first2n logits are zero; the last
token has binary log-odds equal to the accumulator. Thus its mean-centered logit
matrix at EACH FIXED CUT has rank at most n+2 by this explicit switched linear
representation. Combining differently timed cuts is not claimed to retain that
same rank without including a time coordinate.

At the cut after X, consider the matrix of last-bit-one future probabilities,

    A_xy = sigma(b+lambda x dot y), x,y in{0,1}^n.

Write epsilon=exp(b). As epsilon tends to0,

    epsilon^(-1) A_xy -> exp(lambda x dot y)
        = tensor_(i=1)^n [[1,1],[1,exp(lambda)]]_(x_i,y_i).

The two-by-two factor has determinant exp(lambda)-1>0. Its tensor power is
invertible, so continuity of determinant makes A invertible for every sufficiently
small positive epsilon. The predictive probability rank at that cut is therefore
2^n: future columns (y,Z=1) are 2^(-n)A and have full rank.

This separation uses very negative b; it does not assert a fixed practical
approximate-rank gap. Indeed Z=1 can be rare and negligible for a coarse TV task.
That fact is precisely why treating small probability rank as a proxy for useful
low logit rank would be misleading. The existing compiler cannot simply be
applied with r=n+2. Nor does the empirical teacher wrapper preserve low logit
rank merely because it preserves a KL interface to a low PROBABILITY-rank P.

The next substantial learning principle would need to exploit relevant logits
without demanding accurate estimation of every rare token or silently importing
an exponential probability rank. High-temperature access is an existing stronger
service in the cited source, and cannot be renamed ordinary conditional sampling.
This is a surviving capability boundary, not a solved extension.
