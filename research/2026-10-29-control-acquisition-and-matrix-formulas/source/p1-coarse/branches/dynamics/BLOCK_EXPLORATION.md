# Acquiring contracting operation blocks: what works and what cannot

28 October 2026. Follow-on challenge to the reciprocal scalar-word compiler.
The main finding is that, for positive reciprocal primitives, exponentially
searching the space of words is often the wrong problem. One full cycle can
supply the block structure. The real barriers are a quantitative gap,
physical execution length, observable access to that gap, and the restriction
of the future operation language.

## 1. Exact conservation subtraction uses the same scalar receiver

Let A_i be self-adjoint contractions on a real Hilbert space, and let C be
the orthogonal projection onto a known common fixed subspace: A_i C=C.
Self-adjointness implies C A_i=C, so C-perp is invariant for every primitive
and every word. For the same reset vector b and receiver b*,

\[
f(w)=\langle b,A_wb\rangle
=\|Cb\|^2+\langle b_\perp,A_wb_\perp\rangle,
\quad b_\perp=(I-C)b.
\]

If the baseline c=||Cb||^2 is warranted, centered observations f_c(w)=f(w)-c
therefore are genuine inner products in the same source Hilbert space. No
new receiver and no physical preparation of the signed vector b_perp are
required. In particular,

\[
\langle A_vb_\perp,A_wb_\perp\rangle
=f(\mathrm{rev}(v)w)-c
\]

with the chosen consistent word convention. Blocks need not be self-adjoint:
their physically reversed primitive words implement their adjoints. Thus
all primal/dual block Grams remain obtainable by the same scalar operations.

The conserved-subspace and baseline claims are premises. Knowing that some
conservation law exists does not identify C or ||Cb||^2. A finite fit does
not establish stationarity, the invariant subspace, or receiver matching.

### Quantum dephasing specialization

For a unital trace-preserving quantum channel acting on Hilbert-Schmidt
operators, I/d is fixed and the traceless subspace is invariant. Prepare a
known pure rho_b and use the two-outcome effect rho_b as the receiver. Then

\[
p(w)=\operatorname{tr}[\rho_b\Phi_w(\rho_b)]
=1/d+\langle \rho_b-I/d,\Phi_w(\rho_b-I/d)\rangle_{HS}.
\]

For a qubit with rho_b=(I+b.sigma)/2 and ||b||=1, dephasing along n acts on
Bloch vectors by P_n=n n^T. The centered scalar is

\[
f_c(w)=2p(w)-1=b^T P_wb.
\]

A probability reading error eta_p becomes centered error 2eta_p. Unitality
is essential; trace preservation alone does not warrant subtracting I/d.
This is the same physical survival receiver throughout. The current result
is conditional on known preparations, fixed dephasing channels and calibrated
terminal probabilities; it is not a laboratory demonstration.

## 2. Two dephasings: explicit non-self-adjoint blocks

Let n0,n1 be unit axes, c=n0.n1 with |c|<1, and P_j=n_j n_j^T. Define

\[
B=P_1P_0=c\,n_1n_0^T,\qquad B^*=P_0P_1=c\,n_0n_1^T.
\]

Both primitive projectors have norm one. Both two-pulse blocks have norm
|c|<1 on the entire traceless Bloch space. Every admissible program consisting
of H complete B/B* blocks has norm at most |c|^H. The physical reverse of
the block supplies the adjoint used by the general compiler.

This statement covers exactly the block language. It does not transfer to
arbitrary primitive programs, such as long repetitions of P0, which preserve
its axis and have norm one. No irreversible dephasing is inverted.

If the original reset direction is b=n0, the same centered receiver gives
f_c(01)=c^2. Thus an acquired upper bound u<1 immediately gives |c|<=sqrt(u).
The angle's sign is irrelevant to the contraction norm. For a general reset
b, sandwiching by P0 gives

\[
f_c(0\,w\,0)=(b.n_0)^2\,n_0^TP_wn_0.
\]

Normalization by f_c(0)=(b.n0)^2 requires a certified positive denominator;
small preparation overlap amplifies error. If both relevant overlaps are
dark, these modes are not excited by the source port, and a global block-norm
claim should not be manufactured from that missing signal.

## 3. One deterministic cycle often replaces word search

For positive self-adjoint contractions 0<=A_i<=I, set
C=intersection_i ker(I-A_i), and work on C-perp. In finite dimension, if
C has been completely removed, the single product B=A_m...A_1 satisfies

\[
\|B\|<1.
\]

Proof: if a unit x attained ||Bx||=1, every intermediate contractive step
would preserve its norm. For a positive contraction, ||A_i y||=||y|| forces
A_i y=y. Hence every intermediate vector would remain x and x would be a
common fixed vector, a contradiction. Compactness of the unit sphere turns
pointwise strictness into a norm gap. Any ordering containing every primitive
once works; its reverse is an equally contracting physical adjoint.

This is an existence result with no need to search exponentially many words.
It does not acquire the size of the gap.

### Elementary quantitative bound

Suppose the genuinely global gap

\[
\sum_{i=1}^m(I-A_i)^2\succeq\alpha I\quad\text{on }C^\perp
\]

is warranted. Then

\[
\boxed{\|A_m\cdots A_1\|^2\le1-\frac{2\alpha}{m(m+1)}}.
\]

For unit x, set x_i=A_i x_(i-1) and d_i=||x_i-x_(i-1)||. Positivity gives
d_i^2<=||x_(i-1)||^2-||x_i||^2. Also
||(I-A_i)x||<=sum_(j<=i)d_j. Therefore

sum_i||(I-A_i)x||^2 <= [m(m+1)/2]sum_j d_j^2
<= [m(m+1)/2](1-||Bx||^2), proving the bound.

For projections this is a simple, conservative alternating-projections gap
estimate. Stronger local versions are classical detectability-lemma results;
they are not a new theorem of this programme. A positive gap measured only
on the finite acquired dictionary does not become a global gap automatically.
The compiler's separately acquired defects are what can qualify reuse beyond
the dictionary.

If arbitrary proposed macros U_j may be padded with the full cycle, then
B U_j (or B U_j B*) is contracting with a known bound. Padding changes the
physical operation and its scientific meaning. It cannot silently validate
the unpadded programs or a language that disallows the cycle.

## 4. Adaptive same-receiver construction with full execution costs

The qubit example admits a concrete adaptive construction. Assume b=n0,
c in (0,1), and centered scalar error at most eta<1/8. Query

\[
f_c(B^k)=c^{2k},\qquad k=1,2,4,8,\ldots
\]

using one prepared sequence of 2k primitive dephasings per query. Form a
valid upper endpoint U_k from the scalar error interval. Stop only when
U_k<=1/4. For the selected macro D=B^k,

\[
\|D\|=c^{2k-1}
=[c^{2k}]^{(2k-1)/(2k)}\le\sqrt{U_k}\le1/2.
\]

Its reverse implements D*. The procedure terminates for every fixed c<1
under the stated constant error contract. It uses O(log k) readouts but
O(k) primitive operations and elapsed primitive durations. Long-word source
stability and calibration remain actual requirements.

### Exact rational family with exponentially long execution

Let Q=4^n and take rational axes

\[
n_0=(1,0,0),\quad
n_1=\left(\frac{Q-1}{Q+1},\frac{2^{n+1}}{Q+1},0\right),
\qquad c_n=\frac{Q-1}{Q+1}.
\]

The projectors have rational entries with O(n) description bits, and their
only common fixed operator in qubit space is the identity. Nevertheless,
any nonempty primitive word of length L has norm c_n^s, where s is its number
of changes between the two axes. Since s<=L-1,

\[
\|P_w\|\ge c_n^{L-1}.
\]

Thus any macro with norm <=1/2 needs
L>=1+ceil(log(1/2)/log(c_n))=Omega(4^n) primitive operations. No clever ordering
or search avoids this physical cost; alternation maximizes s and is optimal.

For eta=1/1000, even under worst-case upward center error, the doubling scheme
above stops exactly at k=Q/2. Indeed c_n^Q lies below exp(-2)<1/4-2eta,
whereas c_n^(Q/2) is at least exp(-16/15)>1/4. These inequalities follow from
log(c_n)=-2 atanh(1/Q) and Q>=4. The complete acquisition cost is therefore

\[
\text{readouts}=2n,\quad
\text{primitive applications}=2(1+2+\cdots+Q/2)=2Q-2,
\quad\text{selected macro length}=Q.
\]

This is logarithmic readout count with unavoidable exponential execution in
parameter bit length. It is not an exponential combinatorial search lower
bound. A standard equally informed doubling/alternating-projections method
can perform the same experiment and tie these costs.

Fixed bounded noise also prevents resolving arbitrarily small angle changes
from unlimited short experiments. Starting and ending on n0, every scalar
word response is c^r for r<=L+1. Thus |f_c(w)-f_d(w)|<= (L+1)|c-d|. Two
different nonparallel small-angle sources can have overlapping error
intervals for every such word. Repeated adversarial bounded errors do not
remove this overlap.

## 5. Infinite-dimensional obstruction: no contracting finite block exists

Let the Hilbert space be the orthogonal direct sum of two-dimensional planes.
On plane n, let P0 project onto e_(n,0) and P1 onto
c_n e_(n,0)+sqrt(1-c_n^2)e_(n,1), where c_n in (0,1) increases to one.
Both primitives are positive orthogonal projections. Their common fixed
space is {0}, yet every finite nonempty word has operator norm one:
on plane n its norm is c_n^s for a fixed finite switching count s, whose
supremum over n is one.

This is not merely a forever-dark-sector objection. Choose reset
b=sqrt(3)sum_(n>=1)2^(-n)e_(n,0). The vectors P0(P1P0)^k b carry the moment
coordinates c_n^(2k). Polynomial density on the compact spectral interval
shows that their closed span contains every e_(n,0); applying P1 then supplies
every e_(n,1). Hence the cyclic reachable closure is the whole Hilbert space.
There is no strictly contracting finite block even on that relevant closure.

For each fixed state the alternating product still decays strongly, by
dominated convergence. Strong decay is not uniform operator contraction.
Consequently a weak promise of no exact extra conservation law cannot
guarantee that adaptive block discovery will ever succeed. A quantified
angle/gap, finite-dimensionality plus instance-dependent cost, or a narrower
task-relative certificate is necessary.

This obstruction concerns contraction of the actual hidden block operator.
It does not invalidate the parent's uniform source-output certificate:
stable reduced coefficient maps can yield a finite double-defect sum even
when the hidden middle products are bounded only by one. Small source
weight in a slow sector can make that certificate useful without proving
a global hidden contraction gap. The fixed-rank example in Section 8
instead rules out a uniform acquisition cost across unrestricted slow
scales when the later scalar difference is itself large.

## 6. Strong baseline and scientific meaning

Once a contraction bound rho for every legal block has been acquired, the
conserved-baseline predictor already satisfies

\[
|f(w)-\|Cb\|^2|\le\|b_\perp\|^2\rho^H
\]

after H blocks. For qubit survival this is |p(w)-1/2|<=rho^H/2. Long-horizon
absolute accuracy by itself is therefore weak evidence of useful learned
science: passive mixing can make every answer approach the same baseline.
The reduced compiler must earn its value on informative transient tasks,
task-dependent outputs, or reuse before this trivial tail bound becomes
adequate. Relative errors or dividing by rho^H reintroduce a precision cost.

The block restriction is a real changed operation language. It can be a
useful lawful physical capability, but it does not solve arbitrary quantum
control or preserve information that the inserted dephasings destroy.

## 7. Acquiring the reachable dictionary also need not enumerate words

Here q denotes reachable dimension, and m denotes the number of allowed
macros, including whichever reversals are themselves future operations.
Assume that the scalar echo operations needed for inner products are
available for acquisition, that the centering baseline is warranted, and
that exact scalar reads are supplied. No entrywise hidden-state access is
assumed. Let

\[
\mathcal R=\operatorname{span}\{B_w b_\perp:w\text{ an allowed macro word}\},
\qquad \dim\mathcal R=q<\infty.
\]

Start the dictionary with b_perp, unless it is zero. Maintain linearly
independent word vectors v_1,...,v_r and their exact Gram G. Each appended
vector puts its m one-step extensions on a queue. For candidate x=B_i v_j,
acquire h_k=<v_k,x> and z=<x,x> by scalar echoes. Its exact squared distance
to the current span is

\[
s=z-h^T G^{-1}h.
\]

If s>0, append x and its already acquired Gram column. If s=0, discard x.
A discarded candidate remains in the span after later appends, so it never
needs retesting. There are at most q appends and exactly m q candidate
extensions by termination. Every B_i then maps every basis vector into the
final span. That span is invariant, contains b_perp, and is therefore the
whole reachable space. Coordinates of each accepted or discarded extension
give exact reduced operators and predict every subsequent word.

This is ordinary reachable-subspace construction with acquired inner
products. It is not a new finite-rank realization algorithm. Its relevance
is that reciprocity makes all required inner products physically scalar.
There is no exponential enumeration of all length-q words:

\[
\begin{array}{ll}
\text{scalar readings} & \le 1+m q(q+1),\\
\text{longest dictionary word} & \le q-1\text{ macros},\\
\text{longest acquisition echo} & \le 2q\text{ macros},\\
\text{primitive applications} & O(m q^3\ell_{\max}),
\end{array}
\]

where ell_max is the maximum primitive length of an allowed macro.
The reading bound is deliberately conservative; repeated echoes can be
cached. It counts exact values, not the precision or number of physical
shots needed to obtain them. Finite-dimensional arithmetic and coefficient
bit growth also require payment. The promise q need not be known in advance
for exact termination; it remains an assumption behind the finite cost.

With bounded errors, a residual interval containing zero does not decide
whether s is zero. Certified positive lower bounds can justify an append.
Certified upper bounds can justify an approximate defect certificate.
Neither outcome supplies exact closure unless the evidence warrants it.
An arbitrary proposed T and the parent's defect-corrected compiler avoid
using an unjustified inverse, but do not make a small, well-conditioned
dictionary or informative error bound appear for free.

Already for the qubit source with v_1=n0 and x=P1 n0,

\[
G=1,\quad h=c^2,\quad z=c^2,\quad
s=c^2(1-c^2).
\]

The reachable rank is exactly two for every c in (0,1), while the novelty
test can be arbitrarily close to zero. Thus fixed reachable rank does not
give a uniform finite precision requirement for this exact construction.

## 8. Fixed rank still permits an acquisition-cost impossibility

The preceding difficulty is not solely numerical inversion. Consider two
sources from the rational family, with parameters Q and 4Q. Both have the
same reset n0, the same scalar receiver, the same two primitive labels,
reachable rank two, and the identity as their complete common conserved
quantum subspace. For any primitive word of length at most L, its centered
response is c^r with r<=L+1. Therefore

\[
|f_Q(w)-f_{4Q}(w)|
\le (L+1)(c_{4Q}-c_Q)
= (L+1)\frac{6Q}{(Q+1)(4Q+1)}
<\frac{3(L+1)}{2Q}.
\]

Choose Q sufficiently large that this is at most 2eta. A common midpoint
transcript is then consistent with both sources under the same bounded
centered-reading error eta. This remains true for adaptive query choices:
identical previous transcripts lead to identical next choices. Arbitrarily
many repetitions of short histories do not distinguish the sources under
an adversarial bounded-error contract.

But the legal future word B^(Q/2), of primitive length Q, has scalar values
c_Q^Q and c_(4Q)^Q. The first is less than exp(-2)<1/7, while Bernoulli's
inequality gives the second greater than 1/2. Their future centered outputs
therefore differ by more than 5/14, or more than 5/28 in actual survival
probability. Both sources obey all the rank, conservation and reciprocity
promises just listed.

Consequently there is no acquisition-cost bound depending only on fixed
reachable dimension, alphabet size and constant receiver error that
guarantees accurate arbitrary-horizon reuse. For any fixed budget of
primitive applications, one can choose Q beyond that budget's short-history
distinguishing power. A slow-mode scale, an allowed horizon, a sharper
precision contract, or a quantitative gap must enter the complete cost.
Independent stochastic shots could reduce their statistical error; those
shots and the required precision would then be part of the acquisition,
not an exception to this bounded-error statement.

This lower bound does not assert that word ordering is hard. In this family
alternation is optimal, the right experiment is known, and the obstruction
is physical duration or precision. It therefore survives comparison with
an equally informed existing route.

## Executed checks

The independent checker check_block_geometry.py uses exact rational
arithmetic for the rational qubit axes with n=1,...,5. It checks every
primitive word up to length six, every B/B* word up to four blocks, the
one-step dictionary novelty formula, adaptive doubling with worst-case
bounded measurement error, and exact minimal length needed for norm at most
one half. It also checks the fixed-rank indistinguishability and later
separation inequalities for the paired Q and 4Q sources. Its output is
BLOCK_GEOMETRY_RESULTS.json. These checks exercise the small exact physical
geometry; they do not implement or duplicate the parent's noisy compiler.

## Primary antecedents checked

- Anshu, Arad and Vidick, *A simple proof of the detectability lemma and
  spectral gap amplification*, Phys. Rev. B 93, 205142 (2016):
  https://arxiv.org/abs/1602.01210 . Products of local projections approximate
  the common ground-space projector with contraction controlled by a gap;
  the proof permits arbitrary ordering.
- Badea, Grivaux and Muller, *The rate of convergence in the method of
  alternating projections*, St. Petersburg Math. J. 23 (2012), 413–434:
  https://doi.org/10.1090/S1061-0022-2012-01202-1 . The paper studies the
  distinction between uniform convergence and arbitrarily slow convergence
  using generalized Friedrichs angles.
- Petreczky, Bako and van Schuppen, *Realization theory of discrete-time
  linear switched systems*, Automatica (2013):
  https://arxiv.org/abs/1103.1343 and
  https://doi.org/10.1016/j.automatica.2013.07.022 . Finite generalized
  Hankel rank, reachable and observable realizations, and construction
  of state-space representations from noncommutative input-output data
  are established antecedents. The queue construction in Section 7 is
  ordinary linear reachability, with physical echoes providing its Gram.

These sources establish that the broad projection/gap mechanism is existing
mathematics. The candidate contribution is its carefully acquired scalar
operation interface and its use inside the noisy source-valid compiler.
