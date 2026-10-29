# Independent receiving review: signed continuation control theorem

29 October 2026. Reviewer: the existing Astra P1 physical-mechanism role.
No additional branch or worker was created. Root's manuscript was not edited.

## Reviewed input and disposition

Input: `../SIGNED_CONTINUATION_CONTROL_THEOREM.md`.

SHA-256: `f05c28e6c516510179ef2e68b51ed2b3594e6471d7d7ee15c8e8fe2912d69a15`.

The 23,026-byte input is preserved verbatim at
`reviewed_versions/SIGNED_CONTINUATION_CONTROL_THEOREM_f05c28e6c516.md`.

**The bounded-time and heralded signed-continuation theorems in Sections 2--7
are accepted under their stated physical interface.** I found no mathematical
counterexample to the stopped-likelihood lemma, its analyticity, or the sign
contradiction. The finite-data qualifications and ordinary alternatives are
substantive and necessary. The ring algebra in Section 10 is also correct.
Two presentation/interface clarifications should precede an unqualified
apparatus interpretation: account explicitly for state evolution during
controller latency, and describe the exposed-clock conclusion as an
h-dependent JOINT law rather than necessarily an h-dependent conditional
output-given-clock relation. Details and concrete checks follow.

## 1. Stopped likelihood and analytic continuation

The reference chain on the union of allowed directed edges has a finite
intensity ceiling R. The controller and stopping rule are fixed measurable
functionals on that canonical path space with an h-independent external seed.
The action at a jump is its predictable pre-jump action. These details are
needed: allowing the rule itself to know h would make the continued integrand
a different function and would invalidate the theorem.

On each compact K of the analytic domain, the displayed envelope

    exp[(R+(|X|-1)Q)T] max(1,Q/rho)^(N_T)

is integrable by Poisson domination. Thus a stopped event probability is
holomorphic, including arbitrary bounded stopping, event-dependent switching,
and an unbounded number of switches. Finite menu selection causes no hidden
analytic difficulty: for a fixed reference path, its occupation times in the
finitely many state/action pairs are coefficients in the integrated rate.
Disabled edges contribute identically zero at physical and witness parameters.

At the real witness the holding exponential is positive, each enabled jump
factor is negative, and every actual allowed jump changes the two-color label.
Therefore all paths in an opposite-color event have one sign, and all paths
in a same-color event have the other sign. A positive physical probability
implies a positive reference-measure set of paths with nonzero witness
likelihood. This proves the strict sign assertion required for heralding,
not merely nonpositivity.

For a physically almost surely bounded stopping rule one may use min(tau,T)
on the reference space without changing any physical law. This removes any
irrelevant issue about how an algorithm is extended to zero-likelihood
reference paths. For an unbounded rule, min(tau,T) with success {tau<=T}
justifies the exposed-clock corollary exactly as stated.

An actual zero-rate hold does not repair the obstruction. Reference paths
jumping during that hold have weight zero everywhere; all remaining paths
retain the sign argument. No negative rate has been interpreted as an actual
control. The existence of an analytic witness remains a structural model
premise, not an inference licensed by a finite set of trials.

## 2. Exact source-B and quantitative checks

For the specified four source-B modes, the common domain Re(z)<4/3 and witness
h_*=-4 are correct. The four endpoint flips at the witness are
(-1/10,-3/10,-3/20,-1/20); their logarithmic rates are all negative. The
physical rate ceiling log(10)/(2t0) is correct. Hence the source-B conclusion
allows continuous observation and arbitrary predictable switching, not just
fixed endpoint words.

The finite-call highest-degree proof is independently valid. For an odd
terminal path of length d, the leading sign is (-1)^(d-1); for an even path
it is (-1)^d. In the heralded identity (1-c)F-cE, all accepted paths of maximum
degree have the same leading sign. Varying termination depth and randomized
policy weights do not permit cancellation.

At h=-7/2 all flip factors are nonpositive, including p3=0. Therefore f at
that witness is nonpositive, which is sufficient for

    sup_(h in [-1,1]) |f(h)-c| >= c/T_L(7/2).

The Chebyshev alternation proof and its use with a degree at most L polynomial
are correct. This is a conservative uniform norm lower bound; it does not
supply a lower bound against the same-specimen confidence guarantee averaged
over actual calibration data.

`check_signed_feedback_obstruction.py` was written independently before
reading root's checker. Exact rational enumeration covers all 40,805 complete
adaptive endpoint trees with at most three calls, including early stopping.
All 40,804 nonidentity trees have nonconstant flip probability, the claimed
top coefficient sign, and strictly negative value at h_*=-4. All 1,298
heralded trees of depth at most two were checked; the 1,197 with positive
completion fail every tested nondegenerate target identity at the witness.
Thirty-two positive mixtures of sixteen complete trees preserve the sign.
The source-A opposite-slope mixture correctly returns the exact constant
3/20, showing that the checker does not incorrectly exclude that case.
Continuous-time entries in the check file are labelled numerical sanity
checks, not a numerical proof of the infinite-path theorem.

## 3. The exact exposed-clock conclusion and one wording correction

Section 5.3 correctly rules out a fixed nondegenerate endpoint distribution
independent of the full completion clock throughout the uncertain family.
The theorem in fact also implies that no nontrivial operation can have a
parameter-independent joint law of (actual endpoint,completion time). If it
did, for some finite T the positive event {opposite endpoint,completion<=T}
would have constant probability in h, contradicting the signed continuation.
This argument does not require independence of bit and clock.

However, the Section 6 phrase "parameter-dependent output-clock relation"
should mean this JOINT law. It should not mean that the conditional relation
P(output|clock) must depend on h. A concrete counterexample to that stronger
reading is the ordinary controller: draw R~Bernoulli(c), stop immediately
when R=0, and wait for the first observed flip when R=1. Conditional on clock
zero the output is unchanged, and conditional on positive clock it is flipped,
for every h. That conditional relation is identical across h; the positive
completion-time distribution depends on h. Suggested replacement:

    Its joint output-and-clock law must retain dependence on h.

This is a wording correction; the formal statements in Sections 5.1--5.3
survive it.

## 4. Calibration and old-information scope

After a finite endpoint calibration record D, all source-B parameters have
positive likelihood, and conditioning on a fixed D selects one future rule
that still does not know h. An exact pointwise-in-h future row cannot be
obtained from that retained record. This does not rule out posterior-averaged
balancing or finite-confidence per-device control.

For full continuous calibration records, individual records have probability
zero. The stated equivalent-likelihood qualification is appropriate. A fully
explicit almost-everywhere argument can choose a countable dense set of
physical h, intersect the calibration-record full-measure sets using their
mutual absolute continuity, then extend each selected future event identity
by analyticity. This avoids an uncountable-intersection mistake.

The phrase about arbitrary further old information must not be read as
supplying the controller exact h or parameter-revealing data with disjoint
supports. The manuscript already excludes that interface at the start of
Section 8. The robust target is pointwise in h, and arbitrary old records may
be protected by that target; the no-go controller itself retains the stated
common-rule/full-support-information premise.

## 5. Ring consumer: algebra accepted; latency must be physically covered

The three probabilities 27/160,9/40,9/32 and selector probabilities
1/8,1/2,7/8 are correct. The 32 five-bit keys give primitive counts

    (21,7,2,2), (12,4,8,8), (3,1,14,14).

Their source-A hidden slopes cancel exactly. The resulting local transition
is (11/20)I+(9/20)heat-bath. The Ising value beta J=(1/4)log(5/3) produces
conditional probabilities 3/8,1/2,5/8. Correlated frozen H_i do not affect
the pointwise cancellation. The full record statement remains valid only at
the declared compiled interface with fresh internal selectors unavailable.

An independent integer-state implementation checks all 64 four-site local
contexts and all 32 keys per context, then the full 16-state random-scan
transition matrix and all 256 detailed-balance equalities. Its stationary
probabilities are 25/248 for zero domain walls, 15/248 for two, and 9/248 for
four. The random-scan address choice costs two additional bits for four sites;
the local five-bit count is not the total addressing/readout cost.

**Required apparatus clarification:** a fixed controller latency alone does
not preserve the bit while neighbour labels are read and the table is
computed. If an unprotected native mode acts during that delay, the declared
kernel changes. For example an extra mode-3 source-A call before a compiled
flip-c gate gives flip probability c+(1-2c)p3(h). For c=3/20 it is 93/200 at
h=-1 and 13/40 at h=+1; for c=3/10 it is 12/25 and 2/5. Exact cancellation
has been lost. These are exact rational counterexamples to treating physical
controller time as a harmless scalar overhead.

The network construction can state that its added isolation controls hold
ALL sites unchanged during sensing/computation and actuation latency, or
that those intervals are included in each actual acquired primitive kernel.
Alternatively its input epoch can be defined after independent selector bits
are prepared, with an explicitly instantaneous ideal read-and-switch
interface. The existing addressability/isolation premise may intend this;
it should say so. No claim is made that such holding follows from invariance.
The discrete kernel algebra is accepted independently of this implementation
clarification.

## 6. Strong ordinary comparison and source discipline

The complementary note now includes the cheap waiting route. Mode-3 waiting
has multiplier lambda in [1/10,1/2]. With an ACTUAL identity branch, choose
P3^L with probability 2c; its positive marked reference uses Pi or I with the
same branch key and duration. Native interiors are excluded. The n-record
bounds are

    min(1,n c_max 2^(-L),sqrt[n c_max d(2^(-L))]),
    d(x)=[(1+x)log(1+x)+(1-x)log(1-x)]/2.

For 100 macros, c_max=3/10 and L=9, the entropy bound is 0.007564423002729038,
with at most 540 expected raw calls and 900 worst-case calls. The simple
hybrid uses L=12 for bound 0.00732421875. This is much cheaper than the
conservative million-call per-device confidence calculation. Neither route
contradicts an EXACT bounded-time obstruction.

Preparation alone needs no identity branch: L mode-3 calls have joint
(H,Z,Y) error <=2^(-L-1) against the reference carrying the same (H,Z) and an
independent uniform Y. It transfers to ANY common later actual channel by
data processing, including feedback and clocks. It does not prepare H or
provide an H-independent model, and preparation outcomes are not retained.
The exact stopping and calibrated fully marked alternatives also remain
valid at their documented scopes and costs.

The closest primary algebraic predecessor read in this review is Goyal--Sigman,
*On Simulating a Class of Bernstein Polynomials*, TOMACS22(2), 2012:
https://www.columbia.edu/~vg2277/simulate_bernstein.pdf ;
https://doi.org/10.1145/2133390.2133396 . Its Proposition2.2 and Theorem2.3
already use nonnegative weighted finite transcript polynomials for bounded
Bernoulli factories. The terminal physical parity/sign restriction is the
additional mechanism here.

Crank--Fill, *Interruptible Exact Sampling in the Passive Case*, Theorem5.1
and its polynomial identity proof, were read at
https://www.ams.jhu.edu/~fill/papers/passive.pdf . Unknown-chain interruptible
sampling impossibility is established; their target may be an unknown
stationary law and their returned sample need not equal the physical terminal
state. The controlled analytic physical-state statement should be compared
with that predecessor, not labelled the first exposed-clock no-go.

The strong/ordinary stationary-time distinction is already explicit in
Aldous--Fill Chapter9.1:
https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch9.S1.html . Nacu--Peres'
analytic Bernoulli factories (https://arxiv.org/pdf/math/0309222) generate
classical output with random input count; they do not by themselves reset the
actual device or its clock record. No exhaustive novelty claim is accepted.

## Acceptance scope

Accepted: the analytic stopped-likelihood proof, bounded-time opposite-color
and nondegenerate-heralding impossibilities, exposed-clock obstruction,
source-B witness, finite-call Chebyshev bound, and ideal addressed-ring
transition algebra. The observed A/B capability separation is a valid
structural population-model consequence. It is not a finite-sample
identification theorem, physical implementation, practical speedup, or
large-scale computational advantage.

The clock wording and controller-latency clarification above are the only
requested changes before extending acceptance to the corresponding prose
and apparatus interpretation. No predecessor file was modified.
