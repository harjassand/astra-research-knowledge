# Independent receiving review: acquired hidden-response cancellation

29 October 2026. Actual complementary review within Astra P1. The reviewer
developed the separate physical phase-scrambling construction before seeing
this root mechanism. This is an ordinary mathematical review with exact
independent algebra, not formal verification, external peer review, a physical
experiment or a priority judgment.

Reviewed source:

    ACQUIRED_HIDDEN_RESPONSE_CANCELLATION.md
    sha256 17507118b24da8848620b3d5c753b93d56846bc6f9e7bb8e8e3752619f667bcd

An unchanged snapshot is retained in
reviewed_versions/ACQUIRED_HIDDEN_RESPONSE_CANCELLATION_17507118b24d.md.

## Verdict

The main acquisition, cancellation, retained-history, preparation and
two-source statements in Sections 1--5 and 7--9 are correct at the declared
interface. I found no counterexample to those scoped results. Two small
clarifications below should be adopted: positive semidefiniteness in the
injectivity boundary, and the common-null-set justification if the allowed
compiled-action family is uncountable. Neither requires altering the central
construction. The standard finite-menu interpretation already avoids the
second issue.

I independently checked the weighted identity on two distinct reversible
weights in a four-state rational source. The unweighted identity fails there,
whereas the stated endpoint-weight orientation is exactly correct. I also
checked all listed root mixture constants, separation, witness and Hankel
determinants at five sizes. Results and executable code are preserved.

## 1. Chronological weighted loop identity

For T_i reversible in w_i mu, its adjoint in L2(mu) is

    T_i* = M_wi T_i M_(1/wi).

Consequently, for a fixed b,

    <T_i 1_b, E_a T_j 1_b>_mu
      = <1_b, M_wi T_i M_(1/wi) E_a T_j 1_b>_mu
      = [w_i(b)/w_i(a)] <1_b, T_i E_a T_j 1_b>_mu.

The right side is exactly the chronological i-then-j loop in Section 2.
There is no conditional hidden restart. Only the first call's adjoint is used;
the weight is therefore w_i, not w_j. The identity is symmetric in i,j only
after applying the appropriate weight to each orientation. The random
variables themselves need not be symmetric.

In the independent rational check all eight ordered (a,i,j) identities hold.
For example, a=0,i=0,j=1 would have unweighted error -1547/2700000; applying
the specified visible endpoint weight makes its error exactly zero. This is
a meaningful test of the weighted orientation rather than a common-equilibrium
fixture in which a wrong weight would remain invisible.

The matrix H is a Gram of true conditional means, so it is PSD. One stochastic
future's square is not this statistic. The one/two-call acquisition count is
correct for finitely many raw calls, with confidence events paid over all
reported rows and entries.

## 2. Null sets and arbitrary retained records

If mu(A)=0, equivalence of mu_j and mu and invariance of mu_j imply
T_j(x,A)=0 for mu-almost every x. Under a history-dependent selector, the
unnormalized input measure assigned to any one j is dominated by the whole
current input measure. Absolute continuity therefore propagates through every
finite call, even when the selector is correlated with the hidden state
through the retained history.

The claimed arbitrary old Z is sound. Conditional laws X|Z can be singular
(Z=X0 is the extreme case). One must not condition the absolute-continuity
premise separately on each value of Z. Instead, avoid the common exceptional
set under the unconditional marginal, then use conditional expectation for
the next-label row. That proves the equality jointly with Z.

Suggested clarification for an uncountable compiled-action family: for each
a, choose a finite basis of ker H^a. Every basis residual vanishes mu-a.e.;
outside the union of finitely many such null sets every vector in ker H^a
has zero residual. Thus ALL exactly cancelling simplex vectors share one
exceptional set. This directly covers history-selected p in that nullspace.
For a declared finite or countable compiled menu, the usual union already
suffices. The source currently leaves menu cardinality implicit.

With fresh independent index selection, endpoint-only service, fresh/current
labels, and withheld keys and timing side records, ordinary induction gives
the complete finite record law. Cylinder consistency supplies the countable
infinite record. This does not include raw intermediate paths, exposed random
indices or new unacquired operations.

## 3. Synthesis, exclusion and preparation

The simplex quadratic objective is convex for true H. Useful-transition and
cost constraints correctly exclude the interpretation that any zero residual
constitutes a useful control. The separating witness follows from

    <sum_j p_j r_j, sum_i z_i r_i> >= c,
    ||sum_i z_i r_i||^2 = v2,

and Cauchy--Schwarz. Lower confidence bounds on c and an upper confidence
bound on v2 are the correct directions for a robust exclusion certificate.

The Dobrushin preparation argument is valid jointly with Z. Once the actual
visible process is exactly controlled Markov, the initial visible law
conditioned on Z contracts by theta^m toward pi_R, and every subsequent
compiled service is a channel from that prepared label. Arbitrary future
record length cannot enlarge TV. The original physical reference at mu is
warranted only in the shared-mu, label-independent mixture case described
in the second paragraph of Section 4.

For the binary B action, the sharper exact worst-case preparation error is
indeed (1/2)(2/5)^8=0.00032768. This is a statement about the compiled record
language. It is not decay of hidden H, and it does not prepare raw operations.

## 4. Finite-data boundary

On simultaneous entry confidence |H-Hhat|<=d, any simplex p obeys
|p^T(H-Hhat)p|<=d because sum_(ij)p_i p_j=1. The stated bound is correct.
For known mu_a, clipped [0,1] conditional means each erring by eta/mu_a,
the loop-frequency contribution eta/mu_a plus 2k such product contributions
gives d_a=(1+2k)eta/mu_a. Weighted-loop confidence must additionally use the
actual bounded report range; no range-free weighted sampling claim is licensed.

The document properly refuses exact-zero claims from finite samples and
correctly notes the generic N^(-1/4) norm behavior of an N^(-1/2) squared-defect
bound. L1 selection-probability error zeta gives kernel TV <=zeta/2, so the
n-stage hybrid cost is correct. The sampling/padding/actuation costs remain
real.

I also inspected Section 6 as context, although it was not the primary review
request. Its fixed finite compiled-menu, static-H proof is the usual KL chain
rule with a pointwise sum over nonnegative row divergences, followed by the
initial marginal density bound and Pinsker. Its stated reason for failure
when feedback changes H is correct. An uncountable data-selected menu would
need a uniform row envelope rather than a literal finite sum; this should not
be silently generalized.

## 5. Infinite rank and useful exact compilation

The raw probabilities lie in [1/20,9/20], and the stated symmetric jump-rate
realization has the stated ceiling log(10)/(2t). The source needs independently
prepared H across baseline trials; no time average on one frozen specimen
provides nu. This cost is explicitly retained.

The autocorrelation sequence has moments of lambda=4/5-h/10 on a continuous
interval. Every finite Hankel matrix is a Gram of distinct polynomial powers
under a full-support law and is therefore positive definite. This proves
unbounded rank, not merely numerical high rank. A finite linear observable
representation would impose a finite Hankel rank, so it cannot reproduce all
raw records.

The cancelling mixtures have slopes zero and flip probabilities 3/20 and
3/10 exactly. Their distinction is operationally nontrivial even though a
competent conventional two-state controller solves their planning problem.

## 6. Isolated-operation separation and exposed keys

For each raw j separately, changing v_j to -v_j is exactly the transformation
h -> -h of the initial uniform hidden law. Since the entire fixed-generator
path conditional on h is transformed with it, equality holds for complete
one-operation baseline path laws, including adaptively selected observation
times under that same generator. This does not equate experiments that switch
between differently registered raw operations on one retained H; those are the
cross-information being acquired.

In the all-positive-slope source every simplex slope is >=1/20. The squared
row residual is therefore >=1/600. The supplied z=e_0 witness reaches this
bound. The 0-then-1 return probabilities are 131/200 and 133/200, a separation
of exactly 1/100. The actual cross experiment is essential; the result is not
an advantage over a comparator supplied the same cross information.

Retaining J for action A gives the stated two-hidden-point TV 3/20. Those
point inputs are used as an explicit key-exposure illustration, not as inputs
to the mu-absolutely-continuous theorem. Analogous nonzero failures can be
obtained from narrow positive-width hidden intervals if desired. Repeated keys
and timing leakage likewise change the instrument. My separate physical
scrambling fixture independently has retained-key and reused-key failures.

## 7. Required wording clarification in the injectivity boundary

The sentence 'A positive mixture of positive injective self-adjoint kernels
remains injective' is correct when 'positive' means positive semidefinite as
an L2 operator. It is false if it means only positivity preserving or positive
transition entries, as Markov-kernel terminology sometimes suggests.

Counterexample to the latter reading:

    T_plus = [[3/4,1/4],[1/4,3/4]],
    T_minus= [[1/4,3/4],[3/4,1/4]].

Both are strictly positive stochastic, self-adjoint and injective. Their equal
mixture has identical rows and is not injective. T_minus has a negative
eigenvalue. Please state 'positive semidefinite, injective self-adjoint
operators in a common L2 space' explicitly. Positive-time reversible
semigroups satisfy that stronger premise, so the intended boundary survives.

## 8. Novelty and predecessor assessment

The document's cautious scope is appropriate. Strong lumpability, convex
mixture design, covariance, positive state models and randomized error
tailoring are established. The candidate addition is the observable weighted
cross-loop acquisition of unknown relative hidden responses, followed by a
useful-control cancellation/exclusion problem with an infinite-rank and
isolated-characterization separation example.

Winick et al., arXiv:2212.07500, Theorem 3 and Eq.(2), retain environment-
dependent stochastic Pauli weights. Their results must not be described as
already guaranteeing a memoryless whole record; they also explicitly warn
about random-key leakage. Choi--Lim--Wang, arXiv:2512.13067, provide strong
group-averaging/GPG precedents. Cardelli et al., QEST 2021, Sec.3.4, already
use randomized extremal controls to produce convex rates. Detailed source
comparisons are saved in PRIMARY_COMPARISON_AND_FAILURES.md. The root's
referenced SOURCES_AND_PREDECESSORS.md had not yet been created when inspected.

Neither this review nor the exact fixture establishes historical novelty,
affordable physical acquisition, laboratory feasibility, practical speedup or
a civilisation-scale discovery. It does establish that the reviewed scoped
construction has coherent mathematical content beyond simply fitting a
low-rank predictor to the original operations.
