# Independent all-size proof of the asynchronous enumeration

29 October2026. Analytic review/clarification, not a finite-graph extrapolation.
No new graph/model/trajectory or scalar fixture is executed. The input is the
literal independent occurrence-flag model of root_coherent_admission/PROOF.md.

## 1. Filtration that survives overlapping scans

Write O_v for independent virtual Bernoulli(theta) occupations, except a
FIXED prescribed root set S, all of which is occupied from the outset.
These auxiliary variables are independent of every exogenous read flag
Z_(a,k), with P(Z=1)>=1/2 independently for every check a/block k.
The roots are fixed BEFORE these variables are drawn. The later polymer
enumeration fixes S and filters eligible sets inside the expectation; it
does not condition on S having been selected by a realized graph.

Start a FIFO queue with all roots. Mark them discovered/queued. Process each
discovered vertex once. At an occupied vertex v=(j,k), for each check touched
by j, first expose every still-unknown occupation in that check's row k.
Enqueue new occupied vertices immediately. Then scan in either direction
from the adjacent block to the first read flag1 inclusive or the time boundary.
At every visited row expose all its unknown occupations BEFORE revealing a
previously unknown flag. Cache both. Previously discovered occupied vertices,
including queued roots, are never new children.

The invariant is:

    Every REVEALED read flag has a COMPLETELY exposed occupation row.

It holds initially and is maintained by the prescribed order. A known zero
flag can therefore be crossed without producing new children. A known flag1
ends the scan and also has no hidden children. An own-block exposure may
leave its read flag unrevealed; a later scan can reveal that flag, but its
occupation row is already complete. Partial exposures caused by another
check only reduce the number of new Bernoulli variables in the row.

All previously unexposed occupations remain independent Bernoulli(theta)
under this adaptive filtration; all unexposed flags remain independent with
success probability at least1/2. The proof must not condition on the full
already-realized read graph while asserting this deferred-decision property.

## 2. Conditional scan moment, not independent cluster sizes

Let a=(1+3theta)^K. Any own-row exposure contributes new-child fourth moment
at most a, because it reveals at most K fresh Bernoulli variables. For one
directional scan, skip complete known-zero rows. A complete known-one row
or boundary terminates it. Otherwise each new read trial has probability
at least1/2 of termination after its row is exposed; that row contributes
conditional moment at most a. The flags are independent of its newly drawn
occupations. Thus the whole scan contributes at most

    sum_(m>=1) (1/2)^m a^m = a/(2-a),                  (1)

provided a<2. Earlier termination only improves the bound. Equivalently use
the geometric upper process; it is not necessary to claim the actual scan
outcomes or final components are independent.

Apply (1) sequentially with the tower property at the CURRENT exploration
filtration. This pays all overlaps, adaptive queue choices and forced roots:

    E[4^Y | past] <= a^b[a/(2-a)]^(2b)
                    =a^(3b)(2-a)^(-2b).              (2)

Every conditional scan bound is valid after all earlier scans. Whole-row
caching is load-bearing: a scheme that learns a long failure run but leaves
candidate occupancies inside it hidden would not justify (1).

For theta=1/(64bK), let u=3/(64b). Binomial expansion gives
a<=(1-u)^-1 and therefore

    a^(3b)(2-a)^(-2b)
      <=(1-u)^(-b)(1-2u)^(-2b)
      <=(64/61)(16/13)=1024/793<2.                    (3)

The last step is the elementary integer Bernoulli inequality applied to
(1-u)^b and (1-2u)^(2b). All denominators are strictly positive. No floating
branching-process estimate or native numerical case is being used.

If P vertices are processed and Q remain queued, 2^P4^Q is a nonnegative
supermartingale, since processing one vertex multiplies its conditional
expectation by E4^Y/2<=512/793<1. On a finite graph the stopping time is
bounded by N. Its final value is 2^|C(S)|, with C(S) the union of occupied
components of all forced roots. Hence

    E_(Z,O) 2^|C(S)| <=4^|S|.                         (4)

No branching independence is needed. Root mergers only remove duplicate
work; each of the r forced roots was counted exactly once initially.

## 3. The multi-polymer step that avoids Jensen

For the component bad event b(M), the Boolean Mobius coefficient a_R is zero
if even one component of H[R] is smaller than d. Indeed g=1-b factorizes
over the components of H[R]. A small component gives the zero nonempty
Mobius coefficient of the constant function1. For R nonempty,
a_R(b)=-a_R(g). Also a_empty=0 and |a_R|<=2^|R|. Thus an inclusive
epsilon-bound majorizes the bad-map norm by

    Z_large(H,x)=sum_(nonempty R: all H[R] components>=d) x^|R|,
    x=2epsilon.                                      (5)

For a particular R with r components, pick each component's least-labelled
vertex. This gives a unique root set S with |S|=r. Conversely for fixed S
only count R whose components each contain EXACTLY one prescribed root,
with the least-label rule. For each such R, all R minus S being virtually
occupied is equivalent to R being contained in C(S). Its conditional
probability is theta^(|R|-r), for every fixed graph.

Therefore its weight may be rewritten exactly as

    x^|R|=theta^r E_O[(x/theta)^|R| 1_(R subset C(S))].

For x<=theta and |R|>=rd, summing eligible R gives

    sum_eligible R x^|R|
       <=theta^r(x/theta)^(rd) E_O 2^|C(S)|.

The reason there is no extra partition factor is that R determines its
connected components in H[R]; the fixed roots identify them uniquely.
Take the joint expectation over flags and occupations and apply (4), then
sum over all root sets of size r. This proves

    E_Z Z_large(H_Z,x)
       <=sum_(r>=1) binom(N,r)[4theta(x/theta)^d]^r
       <=exp[4Ntheta(x/theta)^d]-1.                    (6)

The use of (4) for MULTIPLE forced roots is essential. Bounding the average
single-polymer activity and then writing E exp(activity)<=exp(E activity)
would have the wrong Jensen direction. The above proof does not do that.

## 4. Quantum conditioning contract

For each FIXED exogenous read schedule (including its timestamps), the
inclusive complete strategy-norm bound must hold uniformly. Only then may
one apply (5) and average over that schedule. The read flags mean independent
Poisson occurrences, not correct noisy measurements. All Born-outcome/Kraus
records remain unnormalized and are handled in the common quantum process.
Conditioning on a normalized rare Born record would destroy the stated
uniform-noise inference and is not justified by this calculation.

The exact Pauli-word/coherence-component correctness hypothesis is separate
from this enumeration. Neither minimum-weight decoding nor memory persistence
is a consequence of the mere component event in(5).
