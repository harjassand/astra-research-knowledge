# Rank-monotone excess: robust independent forcing clocks for pooled labels
30 October 2026. Root construction candidate; independent review pending. This strengthens the former 'all adapted excess goes directly to a' sufficient interface. It is not a whole-network recurrence theorem by itself.

## 1. Actual labeled-generator contract
There are finitely many pooled types I with distinguished target a, and M labeled particles. In the chosen operational clock, each label has fixed baseline transfers i->j at rates q_ij>=0, plus adapted transfers with nonnegative state/history-dependent rates. Other allowed events may remove a bounded number of cohort labels; their count is paid separately by the existing seed/clear law. Pool-neutral internal face dynamics pauses the operational clock and does not change label types. The physical-to-label realization must preserve the actual count generator.

Suppose an acquired integer rank r has r(a)=0, r(i)>=1 for i!=a, and:

- For every i!=a, some baseline edge i->j(i) has r(j(i))<r(i) and q_i,j(i)>=q_min>0.
- Every possible adapted excess edge i->j has r(j)<=r(i).

In particular excess cannot leave a. Equal-rank transfers and arbitrarily correlated excess histories are allowed. Rates must define a nonexplosive stopped process; in the intended conservative binary module, fixed total population gives a finite state space and bounded rates, which supplies this condition. No uniform upper bound on excess rates is used in the following forcing probability.

## 2. Split actual baseline rates into two independent potential clocks
For every label introduce independent Poisson clocks:

- a progress clock of rate q_min, taking i!=a to the selected lower-rank j(i), and acting as a no-op at a;
- a residual baseline clock of rate Q_max>=max_i sum_j q_ij. At type i, select the remaining baseline edges with their actual rates divided by Q_max, otherwise make a no-op.

At i!=a subtract q_min from the selected baseline edge; all residual rates remain nonnegative. At a subtract nothing. Thus this realizes exactly the baseline generator. The clocks are independent across labels and of the potential clocks used to realize adapted excess; destinations depend on the current type. State-dependent channel selection and physical label reassignment within a pool must retain the given observable rate splitting.

Let L=max_i r(i). On the event that a label has at least L progress rings and zero residual rings during a clock interval of length t, its rank reaches0 by the endpoint. Excess cannot increase the rank, cannot delay a progress ring, and cannot remove a label from a once it arrives. Its success event has probability

 p(t)=exp(-Q_max t) Pr(Pois(q_min t)>=L)
 >=exp(-(Q_max+q_min)t) (q_min t)^L/L!.

For 0<t<=1, p(t)>=c t^L with explicit c>0. These forcing events are independent across labels before any episode-survival conditioning, even though the physical label histories need not be independent. This is stronger than following one fixed path that an adapted excess transition might disrupt.

For a cohort initially at a, zero residual rings alone retains each member at a until a seed removes it. On short intervals the retained fraction is therefore binomially concentrated near exp(-Q_max t). For a later unit interval, apply the progress event to every surviving label from its actual current type. It has the same uniform lower bound regardless of that type.

## 3. The stopping/seed argument stays a containment, not conditional independence
On a trajectory surviving below a target a-count K until deterministic clock time t, the number of successful forcing events cannot exceed K plus the number of removed cohort labels. If each seed removes at most b labels, this is K+b N_seed. Bound seed counts using the actual geometric seed-versus-clearing comparison, then apply the ordinary independent Bernoulli concentration bound to the forcing events. Never condition those events on survival and call them independent.

Taking t=C(K/M)^(1/L) gives expected successes of order K. The usual large enough C and small t regime yield exponentially small failure in K, with the separately bounded seed-count event added. The initial-a cohort and last-unit version give the same high-a protection used by the prior stopped-module proof. Thus the local reset/time/cohort estimates depending ONLY on these forcing interfaces receive rank-monotone excess with the acquired exponent L. Other clock, boundary, activity and global phase hypotheses are unchanged.

## 4. A finite complete finder FOR THIS rank criterion
Input two directed graphs: positive baseline edges Q and possible nonnegative excess edges E. This is not a synthesis of the rate decomposition itself. First reject if E has an edge from a to a different type.

Start A={a}, r(a)=0. At each round:

1. Let C be unranked types with at least one Q edge into A.
2. Repeatedly remove i from C if E has an edge i->j with j outside A union C.
3. If C is empty while unranked types remain, return NO_RANK_CERTIFICATE. Otherwise assign every i in C the next rank and add C to A.

The process terminates after at most |I|-1 successful rounds. Every added type has a lower-rank baseline edge; all its excess successors are either already ranked or in the same round. Therefore the returned ranks satisfy the contract.

It is also complete for the stated rank criterion. Suppose a valid rank exists. Among currently unranked types, all types in its lowest remaining rank have a baseline edge to an already processed smaller rank (or have already been included earlier); their excess successors are already processed or in that same minimum-rank set. More formally, induct on the number of rounds against successive layers of any valid ranking: all types of valid rank at most k are included by the end of round k. They cannot be pruned since their excess successors of rank<=k remain inside the same candidate set or A. Hence a valid ranking cannot coexist with a terminal empty C. This is a finite graph argument, not a claim of completeness for all stable controlled chains.

Straightforward repeated scanning is polynomial in the number of types and edges. Rational q_min and Q_max are read from the actual acquired baseline rates. The possible excess graph must include every transfer with nonzero allowed remainder, not merely edges observed at small populations.

## 5. Raw reaction interface and limits
In the conservative pooled chemical setting, first establish exact nonnegative rate splitting for every unit transfer. Previously a non-a target required its rate to equal the baseline exactly. Under this lemma a nonzero remainder is also allowed when its acquired rank is nonincreasing. Uphill transfers still require exact baseline equality. The old all-excess-to-a case is recovered with the baseline shortest-distance ranks.

An empty protected pool transition must be stopped or otherwise received by the actual boundary rule; this lemma never creates a label from a negative pool count. The existing actual-output terminal guards, face-potential entrance compensation, seed/clearing law, and weak-reversibility check remain required for the whole recurrence transfer. A rank certificate does not supply them.

This is a robust finite-type forcing mechanism and its finder, not an asserted new solution of general weak reversibility or a practical algorithm for arbitrary chemical networks. Poisson thinning, graph ranks and adversarial monotonicity are ordinary ingredients. Historical novelty is not claimed.
