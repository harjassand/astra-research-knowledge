# A matched physical-execution lower bound for adaptive scalar experiments

28 October 2026. The short-echo obstruction can be strengthened to cover
arbitrary adaptive choices of experiment length under a specified stochastic
receiver. It then has an equally informed existing strategy matching its
cost order. This is an application of standard information inequalities to
the present source family, not a new general statistics principle.

## Source, receiver and task

Let 0<e<=1/4, b=e_1, A_e=[[1-e,e],[e,1-e]], B_e=(1-e)I. Both are positive
contractions, and

    f_A(k)=[1+(1-2e)^k]/2,  f_B(k)=(1-e)^k.

The unknown source is one of this known pair. A query chooses any finite
integer k, applies the unknown operation k times to a fresh reset, and
returns one independent binary observation of mean q(k)=1/4+f(k)/2.
Its charged physical cost is k primitive applications. Charging resets,
readout and computational work as well can only increase the cost.
No coherent superposition of queries or change of evolution speed is supplied.

The algorithm may adapt k to all previous observations, use private
source-independent randomness, and stop at an unbounded, almost surely
finite stopping time. It must distinguish the two sources with error at
most 1/3 under each. An all-word amplitude predictor with error at most
1/5 and success probability at least 2/3 would also do this for the target
word below, since the two target intervals are disjoint.

## Information available per unit of physical execution

For d_k=f_A(k)-f_B(k), convexity and a second-derivative bound give

    0<=d_k<=e^2 k(k-1)/2.

Also (1-2e)^k<=(1-e)^(2k), so

    d_k<=[1-(1-e)^k]^2/2<=1/2.

For any Bernoulli probabilities p,q, KL(p||q)<=(p-q)^2/[q(1-q)]. Since
both receiver probabilities are in [1/4,3/4], each conditional query obeys

    KL(q_A(k)||q_B(k)) <= (4/3)d_k^2
      <= (1/3) min{(ek)^4,1} <= ek/3.

The last step uses min{x^4,1}<=x for nonnegative x. Thus using many precise
short observations, a few long observations, or an adaptive mixture cannot
buy more than e/3 nats per charged primitive application in this bound.

## Adaptive lower bound

The conditional KL chain rule, followed by truncation and monotone limits,
gives for the stopped transcript

    KL(P_A||P_B) <= (e/3) E_A[total primitive applications].

If the expected cost is infinite, the desired lower bound is automatic.
Otherwise the same bound holds after arbitrary internal randomization and
data processing into the final answer. Testing error at most 1/3 under both
sources requires total variation at least 1/3. Pinsker's inequality then
requires KL>=2/9. Consequently

    E_A[total primitive applications] >= 2/(3e).

This is an all-design lower bound for the specified receiver and pair. It
does not assert that every scalar instrument obeys the same observation law,
or that coherent control obeys this classical transcript bound.

## Matching order with direct execution

Take e=1/m, m>=4, and the future word length H=5m. Then

    f_A(H)-f_B(H) >= 1/2-exp(-5) > 49/100.

Query this long word 64 times. The receiver-probability separation is at
least 49/200. Comparing the empirical mean with the known midpoint has,
under either source, Hoeffding error at most

    exp[-64 (49/100)^2/8] < 1/3.

The physical cost is 64H=320/e. Thus the optimal expected primitive cost
is Theta(1/e), or Theta(H), up to constants. Direct execution is a strong
equally informed comparator and matches the lower bound's order. Its
64 terminal samples do not make the intervening evolution cost disappear.

## Meaning for reusable learned operations

Even a known two-dimensional family, a binary alphabet of hypotheses and
constant desired accuracy cannot guarantee a bounded acquisition cost
independent of the slow time scale. A compiler may amortize that cost over
many later tasks; it cannot avoid paying for the first information that
distinguishes this pair. The result complements, rather than replaces,
the fixed-short-design precision lower bounds.

`core/adaptive_cost_obstruction.py` checks 57 exact finite-length instances
of all algebraic envelopes, six target separations, and the elementary
exponential constants. The adaptive proof above covers all finite lengths
and stopping rules; exhaustive finite checks are not substituted for it.
