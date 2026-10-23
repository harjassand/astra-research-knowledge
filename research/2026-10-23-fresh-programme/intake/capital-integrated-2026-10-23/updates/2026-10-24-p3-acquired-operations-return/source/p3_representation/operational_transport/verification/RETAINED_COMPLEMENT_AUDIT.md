# Retained observations and exact finite-support audits

Date: 23 October 2026. Bounded native follow-up by
/root/verification_primitive.

## Verdict

The proposed retained-data audit is sound, including when the final candidate
is selected adaptively using all old observations. Its sample size is exactly
minimax-optimal for a cap on additional queries under the unrestricted
point-query completion model and one-sided completeness: a source equal to
the candidate must be accepted with probability one.

The minimal integer sample size is not quite the minimum *expected* query
count if the audit may randomize its budget. The exact expected optimum is a
linear interpolation of two adjacent sample counts, saving less than one
clean-source query. This distinction does not invalidate the proposed
deterministic-budget implementation.

## 1. Conditional setup and the audit

Let S be an explicit finite set with N elements. The application's N=2^r is
a special case; the theorem holds for any finite N.

Condition on all old information H. This fixes:

- The support and its exact encoder.
- The final candidate P on S.
- A retained set D of k distinct addresses in S and their exact source
  values F(x).
- The error tolerance epsilon in [0,1] and false-warrant budget delta in [0,1).

The fixed deterministic source F may be arbitrary. The candidate may have
been fitted, refitted, or chosen using H; it must be frozen before the new
audit draws. Verify P(x)=F(x) for every x in D. Reject if any check fails.
Repeated addresses count only once toward k. Old observations outside S do
not count toward its coverage. Inconsistent repeated source values violate
the fixed exact-source contract.

Write

\[
 U=N-k,\qquad K=\lfloor\epsilon N\rfloor+1.
\]

If U<K, accept with a deterministic warrant. Otherwise choose the smallest
integer m in {0,...,U} such that

\[
 R_m(U,K):=\frac{\binom{U-K}{m}}{\binom Um}\le\delta,       \tag{1}
\]

where a binomial coefficient is zero when its lower index exceeds its
nonnegative upper index. Draw m distinct addresses uniformly without
replacement from S minus D. Reject at the first mismatch; accept if all
sampled values agree.

All of P, S, epsilon, delta, and the initial cache are fixed before these
fresh random choices. The samples may be generated sequentially and recorded
in the cache, but P cannot be refitted during this audit.

## 2. Conditional false-warrant theorem

Define the total error mass under the uniform law on S:

\[
 e=\frac{|\{x\in S:F(x)\ne P(x)\}|}{N}.
\]

If the retained checks pass and e>epsilon, the number J of mismatches is an
integer satisfying J>=K, and all J mismatches lie in S minus D.

If U<K, no such bad completion exists: e<=U/N<=epsilon. This is an exact
deterministic certificate, with no statistical query required.

Otherwise a fresh uniform m-subset misses a fixed J-element error set with
probability

\[
 \frac{\binom{U-J}{m}}{\binom Um}
 \le \frac{\binom{U-K}{m}}{\binom Um}=R_m(U,K).            \tag{2}
\]

The inequality is monotonicity in J. Thus, conditional on every admissible
old history H,

\[
 \Pr(\mathrm{PASS}\ \text{and}\ e>\epsilon\mid H)
 \le\delta.                                               \tag{3}
\]

If a retained mismatch is found, PASS has probability zero and (3) still
holds. Averaging over H proves the unconditional false-warrant guarantee.

This argument imposes no source-class promise and no independence between
the final candidate and old observations. It needs independence of the new
uniform audit randomness from H, conditional on the stated sampling space.
In particular, post-fitting all old samples is allowed; post-fitting the
fresh audit samples while retaining their original warrant is not.

Equation (3) is a frequentist bound on issuing a false warrant. It is not a
posterior probability statement about a fixed candidate after acceptance.
As before, adaptively issuing many warrants requires an appropriate common
confidence budget. One final fresh audit is valid after arbitrary old
training and candidate selection.

The algorithm has no tolerant completeness claim: it rejects on any known
or newly observed mismatch even if the candidate's total error is below
epsilon.

## 3. Exact finite-support minimax lower bound

Fix a retained transcript with all its addresses matching the final
candidate. Suppose all arbitrary completions on the U unqueried addresses
are allowed. There must be at least one alternative output at each address;
this holds for the present arbitrary full-state source model whenever the
raw output space has at least two states.

Consider any possibly randomized adaptive verifier which:

1. Accepts the clean source F=P on S with probability one.
2. Makes at most m additional source queries on every clean-source run.
3. Must control acceptance for every completion having at least K errors.

Query repetitions and queries outside the unqueried portion cannot improve
the following lower bound. Let Q(omega) be the set of distinct unqueried
addresses visited by the verifier on the clean source with random tape omega.
Its cardinality q(omega) is at most m.

Choose an error set B uniformly among all K-subsets of the U addresses.
Define F_B to agree with the clean source outside B and have a different
output at each address in B. These sources are consistent with the retained
point transcript.

Run the verifier against F_B with the same random tape as its clean run.
If B is disjoint from Q(omega), the entire transcript and decision remain
the clean ones, so the verifier accepts. Therefore

\[
 \begin{aligned}
 \mathbb E_B\Pr_{F_B}(\mathrm{accept})
 &\ge
 \mathbb E_\omega\frac{\binom{U-q(\omega)}K}{\binom UK}\\
 &\ge \frac{\binom{U-m}K}{\binom UK}\\
 &=\frac{\binom{U-K}m}{\binom Um}=R_m(U,K).               \tag{4}
 \end{aligned}
\]

The identity uses either counting disjoint subsets in two orders or
factorial cancellation. Thus some admissible bad completion is accepted
with probability at least R_m(U,K). Adaptive choice of query addresses and
full successor-state readout cannot improve this bound before a mismatch
is encountered.

Uniformly sampling an m-subset and accepting exactly when it misses the
error set achieves R_m(U,K) for every completion with exactly K errors,
and no more for completions with additional errors. Hence

\[
 \inf_{\text{one-sided verifiers, query cap }m}
 \sup_{F:\ e>\epsilon}
 \Pr_F(\mathrm{accept})=R_m(U,K).                         \tag{5}
\]

The proposed smallest m is therefore exact minimax for this query-cap
contract. Its early rejection does not change the cap or acceptance event.

The lower bound is conditional on this unrestricted completion model.
Additional independently established structural information about the true
source may rule out some error sets and permit a better audit. In particular,
it would be incorrect to reuse (5) unchanged under a promise that every true
source is a permutation of S: a single-input defect may then be impossible.
No such true-source promise is used by the present construction.

Clean-source completeness is essential to a query lower bound. Without
some acceptance requirement, a verifier which always rejects needs zero
queries.

## 4. Exact expected query cost and its optimum

For the proposed fixed m and a source with J unseen mismatches, sampling
stops on the first mismatch or after m draws. Its expected additional
source calls are

\[
 \mathbb E_J Q
 =\sum_{t=0}^{m-1}\frac{\binom{U-J}{t}}{\binom Ut}.        \tag{6}
\]

The t=0 term is one when m>0. This follows by summing the probability that
at least t+1 draws are made, which is exactly the probability of no mismatch
among the first t samples. The clean source J=0 costs exactly m; other
sources cost no more. This is a source-query count, not a full computation
cost.

For an expected-query formulation, define R_j for j=0,...,U. The alternative
expression

\[
 R_j=\frac{\binom{U-j}K}{\binom UK}
\]

gives

\[
 R_j-R_{j+1}
 =\frac{\binom{U-j-1}{K-1}}{\binom UK}.                   \tag{7}
\]

The differences are nonnegative and nonincreasing in j. Thus R_j is
decreasing and convex, including its zero tail. Let R_bar be its
piecewise-linear interpolation.

For any one-sided verifier, the first line of (4) gives average bad-source
acceptance at least E[R_q]. Convexity gives

\[
 \sup_{|B|=K}\Pr_{F_B}(\mathrm{accept})
 \ge \overline R(\mathbb E_{\rm clean}q).                 \tag{8}
\]

Distinct queried addresses are no more numerous than total calls.
Consequently, if m_star is the smallest integer with R_(m_star)<=delta,
the minimum possible worst-case expected number of additional calls is

\[
 q_\star=m_\star-1+
 \frac{R_{m_\star-1}-\delta}
      {R_{m_\star-1}-R_{m_\star}},                        \tag{9}
\]

when 0<=delta<1 and U>=K. Randomly choose m_star-1 or m_star draws with
the corresponding mixing weights; conditional on that choice sample a
uniform subset and reject at the first mismatch. Its bad-source acceptance
is at most delta, its clean expected cost is q_star, and every other
source costs no more. Hence (9) is attained.

This saves less than one query relative to the fixed budget m_star.
At delta=0 the saving is zero. It is unnecessary for the proposed practical
implementation unless expected-query optimality itself is claimed.

Example: U=5, K=2 gives

\[
 (R_0,R_1,R_2,R_3,R_4,R_5)=(1,3/5,3/10,1/10,0,0).
\]

At delta=1/5, the smallest fixed cap is three queries. An equal mixture of
two and three queries has exact worst-case false-pass probability 1/5 and
clean expected cost 5/2.

## 5. Endpoint and arithmetic conditions

- K must use the exact floor of epsilon*N. A floating-point error near an
  integer can make K too large and invalidate the bound. Rational epsilon
  and integer arithmetic avoid that issue.
- When epsilon=1, K=N+1 and the warrant is trivially valid.
- When epsilon=0, K=1 and the audit controls exact agreement probabilistically.
  At delta=0 it must query all U unobserved addresses.
- When U>=K, R_0=1 and R_m becomes zero at m=U-K+1. Thus a qualifying m
  always exists, including for delta=0.
- If U=0, the retained data already constitute a census and give an exact
  deterministic warrant.
- Reject invalid epsilon or delta parameters rather than silently clipping
  them. A delta of one permits a vacuous zero-query warrant; it is excluded
  from the substantive confidence contract here.

The exact recurrence

\[
 R_0=1,\qquad
 R_{m+1}=R_m\frac{U-K-m}{U-m}
\]

is valid through the first zero. It avoids computing factorials. Exact
integer products or reduced rational arithmetic can compare it with rational
delta. Their bit costs and the search for the smallest m are preprocessing
costs and must be charged; the formula does not justify free arbitrary
precision.

## 6. Uniform sampling by rank/select on the complement

Let the explicit support encoder use integer addresses 0,...,N-1.
Keep the k known addresses sorted. Let

\[
 A(x)=x+1-|\{d\in D:d\le x\}|
\]

be the number of unqueried addresses through x. For rank j in
{0,...,U-1}, the j-th unqueried address is the smallest x satisfying
A(x)>=j+1. This x lies between j and j+k, hence never exceeds N-1.

The function A is nondecreasing. At a retained address its value does not
increase, so the first point reaching the threshold is necessarily
unqueried. This proves the rank/select formula without enumerating S.

Draw j uniformly from the remaining rank range, select x, and insert x
into the excluded-address data structure. Repeating this operation produces
each ordered m-tuple of distinct initially unqueried addresses with
probability

\[
 1/[U(U-1)\cdots(U-m+1)].
\]

The resulting unordered subset is therefore uniform, as required by (2).
An alternative is to sample distinct ranks without replacement in the
original U-address complement and use a static selector.

Exact uniform integer generation requires unbiased random bits with rejection
or another proved unbiased method. Taking a random machine word modulo U
without correcting the remainder generally introduces bias.

A sorted-array implementation can binary-search A using exact prefix counts;
an order-statistic tree can support dynamic selection and insertion.
Their storage, comparisons, big-integer operations, inverse-chart calls,
and source preparations are distinct from the number m of new source calls.

## 7. Bounded executable checks planned before execution

The follow-up checker will use no root implementation or sealed values.
The disclosed finite scope is:

1. For every U=1,...,8, K=1,...,U, and m=0,...,U, enumerate all m-subsets
   against one fixed K-error set. Check the exact binomial miss probability,
   its alternative expression, recurrence, monotonicity, convexity, and
   minimal sample count for delta in {0,1/20,1/5,1/2}.
2. For N in {1,2,4,8}, enumerate every retained-address subset and every
   valid complement rank. Check binary-search rank/select against the
   directly enumerated small complement.
3. Verify the displayed U=5,K=2 mixture example exactly.

All cases are exposed here before execution; they are algebra and
implementation checks, not independent evidence for practical superiority.
There will be one run, no external source calls, no random simulation, and
no new workers. Any failure will be preserved. The earlier operational
transport source, results, and manifest remain unchanged.

Exact serving-model, token, and monetary usage are not exposed to this
agent and remain UNKNOWN. Follow-up process costs and hashes will be
recorded separately.
