# What the comparison learner does not acquire

13 October 2026. Independently derived in this intake, with an internal critic.
This is a finite oracle theorem, not a scientific-priority or application claim.

## Exact recognition requires exponential access without an additional promise

Let \(n\ge3\), \(1\le d\le n-2\), and \(N=2^n\). The input is an arbitrary
strict comparison oracle of a permutation of \(\mathbb F_2^n\). A membership
recognizer must distinguish the hidden-affine triangular degree-at-most-\(d\)
class of the submitted theorem from its complement. The identity rank belongs
to that class.

**Theorem.** Every deterministic exact recognizer makes at least \(N/2\)
comparisons on the identity oracle. A randomized recognizer which accepts the
identity with probability at least \(1-\alpha\), and accepts each nonmember
with probability at most \(\beta\), has expected number of comparisons on the
identity at least
\[
  \max(0,1-\alpha-\beta)\,2^{n-1}.
\]
The expectation includes its internal randomness. If it can fail to halt, the
bound applies to the number of queries in the full run, possibly infinite;
completeness means an actual acceptance event, not eventual intention.

**Proof.** Use most-significant-first raw coordinates \(x=(z,b)\), with
\(z\in\mathbb F_2^{n-1}\). For each \(a\), define the rank permutation
\[
 Q^{(a)}(z,b)=(z,b+\mathbf1[z=a]).
\]
It swaps exactly the two adjacent identity ranks \((a,0)\) and \((a,1)\).
Every comparison other than their mutual comparison is unchanged, including
comparisons that use one of those points and a third point.

The last coordinate has Boolean algebraic normal form
\[
 b+\prod_{i=1}^{n-1}(1+z_i+a_i),
\]
and therefore exact degree \(n-1>d\). Invertible affine substitutions preserve
Boolean algebraic degree: substitution cannot increase degree, and applying the
inverse substitution gives the reverse inequality. Every actual rank coordinate
in the promised class has degree at most \(d\) in raw inputs. Thus each
\(Q^{(a)}\) is a nonmember, independently of any alternative hidden input basis.

For a deterministic recognizer, an unqueried special pair leaves the identity
transcript identical to the corresponding nonmember's transcript. Correct
acceptance on identity and rejection on that nonmember are then impossible.
The \(N/2\) pairs are distinct, proving the deterministic assertion.

For a randomized recognizer couple both runs using the same complete random
tape. Until the special pair is queried their histories coincide. Let \(E_a\)
be the event that the identity run queries that unordered pair. The acceptance
indicators can differ only on \(E_a\), so
\[
  1-\alpha-\beta
  \le \Pr[\text{accept identity}]-\Pr[\text{accept }Q^{(a)}]
  \le \Pr(E_a).
\]
Summing over \(a\), the expected number of distinct queried special pairs is
at least \((1-\alpha-\beta)N/2\), and it cannot exceed the expected total query
count. This proves the claim. Reversed orientations of the same special pair
count once; repeating them cannot improve the lower bound. □

**Consequence.** The polynomial decoder acquisition theorem cannot be converted
to an exact end-to-end arbitrary-oracle class recognizer by a polynomial-query
verification wrapper. Even the identity target incurs this obstruction. This
does not refute promised acquisition, learning a useful approximation, tests
against inputs a fixed distance from the class, or certification by an additional
supplied structural model. The nonmembers here are extremely close in comparison
distance: one unordered pair among \(\binom N2\). Their distance is essential.
For \(d\ge n-1\) this witness is inside the degree bound and proves no such
membership obstruction. No lower bound for that regime is asserted.

This closes one precise missing recognition transfer negatively. An actual
application now needs either a trusted model establishing the class promise,
a meaningful distance/tolerance criterion, or substantially different access.

## Conditional noisy-access compilation

This second statement is a standard repetition construction, recorded to make
the new operation's noise assumption and cost explicit; novelty is not claimed.

Put \(P=\binom n2\), \(D=\sum_{j=0}^{d}\binom n{j+1}\), and choose a tournament
failure allocation \(\beta_t\in(0,1)\). Set
\[
 T=\lceil\log_2(P/\beta_t)\rceil,
 \qquad B=D+(2T+2)P.
\]
Implement the submitted learner with a global logical-query cap \(B\), and abort
with UNKNOWN on any malformed algebraic state, failed invariant, or exceeded
cap. The explicit global cap is required because the structural promise does
not control a transcript containing incorrect comparison answers.

Assume the underlying true comparator satisfies the submitted class promise.
For every repeated physical answer, its conditional probability of error given
the entire preceding history, including previous repeats, is at most
\(1/2-\rho\), with a supplied calibrated \(0<\rho\le1/2\). Independent errors at that
rate are a sufficient special case. A marginal error rate by itself is
insufficient.

Replace every logical comparison by an odd number \(r\) of repeats and return
their majority, where \(r\) is the least positive odd integer satisfying
\[
 r\ge\frac{\log(B/\beta_n)}{2\rho^2},\qquad \beta_n\in(0,1).
\]
The conditional Hoeffding supermartingale argument bounds the majority error
by \(e^{-2r\rho^2}\). For completeness, if \(E_s\) denotes an error indicator,
then conditional Hoeffding's lemma gives
\(\mathbb E[e^{\lambda(E_s-\mathbb E[E_s\mid\mathcal F_{s-1}])}
\mid\mathcal F_{s-1}]\le e^{\lambda^2/8}\). Iteration and Chernoff optimization
show \(\Pr[\sum E_s\ge r/2]\le e^{-2r\rho^2}\). A union bound over at most
\(B\) adaptively chosen logical comparisons gives error probability at most
\(\beta_n\). Couple the learner to an exact-comparator run on the same internal
random tape. Outside the majority-error event, the transcripts coincide, and
the source tournament fails with probability at most \(\beta_t\). Hence
\[
 \Pr[\text{an exact decoder is returned}]\ge1-\beta_t-\beta_n.
\]
The physical comparison budget is at most \(rB\), input transmission at most
\(2nrB\) bits, and returned comparison bits at most \(rB\), before physical
reset, settling and calibration costs. The source's zero semantic error on
completion no longer holds: an erroneous completed model is possible on the
noise event. A finite confidence statement does not certify an acquired gap,
freshness of the errors, legal repeated inputs, or a physical target.

**Correlated-repeat counterexample.** Draw one global Bernoulli error bit of
probability \(1/4\), and flip every repeated answer iff it is one. Each individual
answer has marginal error \(1/4\), but every odd majority also has error
\(1/4\), for arbitrarily large \(r\). After one observation of that error the
conditional contract fails. Thus the conditional or suitable independence
assumption cannot be replaced by a marginal accuracy claim.

## Relationship to cumulative Astra capital

N580's dual-kernel sampler assumes explicit bilinear matrices and a certified
collective-rank bound; this comparison learner acquires a different restricted
triangular representation. Neither supplies the other's input contract. The
common-radical quadratic sampler in this submission assumes complete quadratic
coefficients. Acquired complete triangular coordinates do supply such
coefficients, but the common-radical rank condition need not hold, and its
one-shot correction is unnecessary for the already acquired prefix sampler.
There is no claimed generic quadratic-system solver or closure of N580's gate.

An exact strict separation within the acquired class is useful. Take
\(Q(x_1,x_2,x_3,x_4)=(x_1,x_2,x_3+x_1x_2,x_4)\) and condition on the first
three output bits. This is a complete triangular quadratic permutation, so
the acquired decoder samples each two-point prefix fiber with one random suffix
bit. The common polar radical of its first three coordinates is
\(\operatorname{span}(e_3,e_4)\), whose output translation image is only
\(\operatorname{span}(0,0,1)\). Its rank is one, below the required three for
the source common-radical right-inverse sampler. The conditional triangular
correction therefore handles this example despite failure of that sufficient
one-shot certificate. This is a compatibility/separation observation proved
directly from the acquired representation, not a new general joint-fiber
sampler or evidence against the common-radical theorem.

The robust-tracking source also separates supplied structural block promises
from generic selector closure. That is an interface discipline shared with
this theorem, not a mathematical implication between the two constructions.
No existing control or thermal-learning theorem discharges exact decoder class
membership. No generic architecture change is needed for this obstruction.
