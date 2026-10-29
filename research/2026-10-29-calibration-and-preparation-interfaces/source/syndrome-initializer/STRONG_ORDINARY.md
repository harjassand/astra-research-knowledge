# Stronger ordinary sampler: expected polynomial cost at exponential accuracy

29 October 2026. This is an admitted/reconstructed ordinary polymer algorithm,
not a new sampling invention. Its family-specific computability premises are
paid by PROOF.md and literal_history.py. It improves the precision dependence
of the executed finite-list receiver; that slower receiver remains valid.

## 1. Controlling primary result

Chen--Galanis--Goldberg--Perkins--Stewart--Vigoda,
[1901.06653v6](https://arxiv.org/html/1901.06653), Definitions3--4,
Theorems2/5, and Sections2.2--2.3, requires computable allowed polymers and
exponential decay stronger than merely KP. For a binary model its sampling
condition is tau>=5+3ln Delta. Here tau=beta/4=ln B0. One fixed
B0>=Abar^4 satisfies this (Abar=4max(1,Delta_bar)); increase it further if
the primary memory temperature criterion requires it. The primary supplies
a stronger same-information algorithm and must not be hidden behind our
slower finite-list benchmark.

Theorem 5 states a bounded runtime guarantee in its algorithmic model. Our
literal fair-bit implementation below is admitted only with the independently
proved EXPECTED bit-work contract. We do not turn its expected update cost
into that stronger statement by restarting conditioned on finishing quickly.

Here is a completely specified rational expected-time version of its rooted
proposal, so no enumeration or real-coin oracle is free. We use fixed-count
Markov updates and do not condition the output on a favourable runtime.

## 2. Exact rooted proposal and finite input costs

Let A=4max(1,Delta), R=A², and choose root v. Draw an integer K with

    Pr(K>=s)=R^(-s), 1<=s<=N.

This is the number of consecutive successes of a rational 1/R coin, capped
at N. Capping retains all required tails since no polymer has size>N.
Enumerate EVERY connected allowed support gamma containing v of size<=K,
using the local predicates of PROOF.md. Output gamma with mutually exclusive
probability w_gamma R^|gamma|; otherwise output empty. This is valid because

    sum_(gamma contains v) w_gamma R^|gamma|
       <= (R/B0)/(1-AR/B0)<=1/(3A)<1.                    (S1)

For each particular polymer, the exact output probability is

    Pr(K>=|gamma|) w_gamma R^|gamma|=w_gamma.              (S2)

All weights are rational. For a finite enumerated list with maximum top
energy Emax, use common denominator B0^(4Emax); gamma's integer numerator
is R^|gamma| B0^[4(Emax-Egamma)]. Add the remaining numerator to the empty
outcome. Thus one exact uniform integer with O(K log B0) bits suffices for
categorical selection. Standard fair-bit integer rejection has finite
expectation; no tiny-probability acceptance loop of cost 1/w_gamma occurs.

The enumeration cost conditioned on K is bounded by
C_rule poly(K,Delta,log B0) A^K in a local-array implementation. Since R=A²,

    expected work <=C_rule sum_(K>=0) poly(K)(A/R)^K<infinity,    (S3)

uniformly in N. For an explicit polynomial k^r one can use
sum_(k>=1) k^r x^k <=r! x/(1-x)^(r+1), x=1/A<=1/4.
Local address bits and exact integer arithmetic give additional polynomial
logarithmic factors. Literal Python global bitsets pay an extra polynomial
N-bit arithmetic factor; no unit-cost large-integer claim is made.

## 3. Full dynamics and expected-time/accuracy contract

Use the primary's vertex chain. Choose v uniformly. With probability 1/2
remove its occupied polymer (if any); otherwise use the exact proposal above
and add it if compatible. Detailed balance has birth/death ratio w_gamma.
For completeness, couple two configurations differing by gamma using the
same root, removal coin and proposal. A removal at any vertex of gamma
eliminates the discrepancy, with probability |gamma|/(2N). A proposal eta
which is incompatible with gamma can create one additional discrepancy with
probability |eta|w_eta/(2N). Therefore polymer-count distance has conditional
expectation at most

    1+[-|gamma|+sum_(eta incompatible gamma)|eta|w_eta]/(2N)
        <=1-(1-c)|gamma|/(2N)<=1-(1-c)/(2N).

The path metric has diameter <=2N: remove the first configuration's polymers
and add the second's. Thus path coupling contracts at least
(1-c)/(2N)>=1/(4N), with c from PROOF.md. Hence

    T=4N ceil(log2(8N/epsilon))

fixed updates suffice for TV error <=epsilon/4. Every update terminates
almost surely; (S3) gives expected operation count polynomial in N and
log(1/epsilon), including qualified rule and bit costs. This statement needs
no truncated-polymer approximation and no finite-list normalizer.

If a deterministic runtime cap is required, run ONE copy, cap total charged
work at 4E_work/epsilon, and return empty on timeout. Markov's inequality
adds at most epsilon/4 in TV. This retains the ordinary polynomial-in-
1/epsilon worst-case guarantee. Restarting until a fast run finishes could
condition the output law on runtime; that argument is not used here.

Taking epsilon=2^(-L) with L=O(2^k) now has EXPECTED polynomial cost in
n_k, since the accepted distance bound implies 2^k<=n_k/d_seed. Thus the
nominal encoder can match the exponentially small logical-error scale in
expected polynomial ideal computation time, under this stronger ordinary
algorithm. The bounded worst-case runtime for that same accuracy has not
been improved here. Neither statement includes noisy physical encoding.

The implemented rooted_sampler.py is this exact expected-time engine. Its
seeded run is only an implementation/resource diagnostic. Ideal independent
fair bits are the theorem's computational randomness contract.
