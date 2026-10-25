# Acquiring a computational law together with its defect

New research construction, 25 October 2026. Earlier conditional-operation,
causal-controller, and reaction inference files remain unchanged. This work is
not a recovery of unavailable earlier code.

## Scientific operation and the change in representation

The learner interacts with linear computational primitives through exact
vector-action APIs and transpose-action APIs. It tries to acquire a reusable
calculus for comparing *new* programs built from those primitives. It is not
given a coordinate system, native matrices, a correct rewriting rule, a defect,
or a membership label. The first, specialized search grammar is explicit:

    A B = sigma B A + c I + R,   sigma in {+1,-1}, rank(R) <= r.

The later structural learner removes this proposed-law input: it searches all
linear combinations of I,A,B,A^2,AB,BA,B^2 for a rank-one residual. An observed
determinantal uniqueness gate and fresh native identity checks obtain a law.
Its BA coefficient can be any acquired rational q. A second acquired
representation, a faithful finite operator algebra, handles coexistence of
several exact identities. The two routes share one actual interaction record.
Their acquisition theorems and executed scope appear below.

The rank budget is a search budget, not an assertion that the source satisfies
it. FAILURE/UNKNOWN is an ordinary result. Linearity, exact arithmetic, and
access to transpose actions are substantive source assumptions.

The retained object is a learned relation, a factorization R=U V^T, and degree
filtered left/right defect modules. It supports an all-input correction to
ideal symbolic rewrites and the largest linear domain on which all bounded
degree uses of the ideal law are valid. It does not reconstruct the full native
algebra or predict an arbitrary new physical mechanism.

## Revealing control: finite differentiation

On coefficient vectors of polynomials of degree below n, let
D e_j=j e_{j-1}, X e_j=e_{j+1} for j<n-1, and X e_{n-1}=0. Then, over Q,

    D X - X D = I - n e_{n-1} e_{n-1}^T.

Low-degree test vectors miss the rank-one term. An exact finite-dimensional
identity [D,X]=I is impossible in characteristic zero because a commutator has
trace zero. Nor is the associative algebra small: its boundary projector,
successively multiplied by D and X, generates all matrix units. Thus its
dimension is n^2 even though the defective law has a short description.

This is a mathematical control, not physical data. A hidden similarity in the
executor will prevent the learner from simply reading off the familiar basis.

## Coefficient acquisition without a coefficient search

Let C=AB-sigma BA, assume n>2r, and choose k=2r+1. Query C on the k columns
of a random n-by-k matrix Omega, and form k-by-k matrices

    N=E Omega,  M=E C Omega,  H=N^{-1} M.

Here E is independently sampled; retry or return UNKNOWN if N is singular.
If C=cI+R and rank(R)<=r, then H=cI+N^{-1} E R Omega. Its characteristic
polynomial p has c as a root of multiplicity at least r+1. Every other root
has multiplicity at most r. Consequently

    gcd(p,p',...,p^(r)) = (z-c)^m,  m>=1,

up to a scalar. Recover c from the next-to-leading coefficient and check that
the gcd is this pure power. This uses rational polynomial arithmetic and no
factorization or enumeration of possible c values. A source outside the search
class can yield no candidate or a spurious candidate; neither is accepted
without the independent relation check below. If two scalars have rank-r
residuals, (c-c')I is a difference of rank-r matrices; n>2r implies c=c'.

The random compression does not by itself prove the native relation.

There is also an obtaining bound for this specialized route. If the true
residual has rank r'<=r, the square input-pencil determinant is a nonzero
polynomial of degree 2k in the sampled entries. With entries uniform in S,
its failure probability is at most 2k/|S|. A fixed nonzero r'-minor of the
first r' fresh residual-image probes gives a rank-finding failure bound
r'/|S|. Thus one attempt at the correct q succeeds with probability at least
1-(2k+r')/|S|, apart from earlier false acceptance already charged to its
independent identity checks. This is a loose sufficient bound; the extra
image probes improve practical obtaining but are not needed for that bound.
The charpoly/gcd computation is polynomial rational arithmetic in r; it does
not enumerate field elements or possible coefficient values.

## Obtaining a globally checked residual factorization

Sample columns of R to obtain a candidate image basis U. If its observed rank
exceeds r, reject the candidate. Select r' independent rows of U, with r' its
observed rank. Transpose queries obtain the same rows of R. Invert the small
row submatrix to obtain V^T such that the candidate residual is U V^T.

Fresh independent vectors z with coordinates uniform in a finite set S are
used to test (AB-sigma BA-cI-U V^T)z=0. For any fixed nonzero linear residual,
the chance of passing t such tests is at most |S|^{-t}; condition on all
adaptive discovery data before drawing these vectors. Union-bound over the
declared maximum number of accepted-candidate attempts. This is a randomized
*all-input identity certificate*, not a statement only about the tested input
distribution. It presumes exact answers and linear maps. Later exact algebra
uses the one acquired identity; it does not spend fresh statistical confidence
for each new program or each reuse.

## Defect modules and the maximal protected domain

For k>=0 define

    K_k = span{ w(A,B) U : |w|<=k },
    W_k = span{ V^T w(A,B) : |w|<=k }.

The learned relation gives the spanning sets

    K_k = span{ B^i A^j U : i+j<=k },
    W_k = span{ V^T B^i A^j : i+j<=k }.

To prove this, normal-order a word. A defect term is l U V^T r; when applied
to U its left word is shorter, and when preceded by V^T its right word is
shorter. Strong induction on degree, followed by the terminating normal-order
rewrites, proves both statements. Therefore each dimension is at most

    min(n, rank(R) * binom(k+2,2)).

For total context degree L>=2, set P_L=ker(W_{L-2}). This is exactly the
largest linear subspace on which

    l(A,B) (AB-sigma BA-cI) r(A,B) x = 0

for every pair of words with |l|+|r|<=L-2. Sufficiency follows from the row
module. For necessity choose l empty, and use that U has full column rank.
This maximality concerns every use of the acquired rule in the bounded degree
language; it does not assert that every particular program pair fails outside
P_L. Specific differences can cancel and have larger kernels.

For the finite differentiation control dim W_k=min(n,k+1), and P_L consists
of degree <= n-L polynomials for 2<=L<=n+1, transported through any unknown
similarity. Thus dim P_L=max(0,n-L+1). For unbounded degree this example has
no nonzero protected domain. Constant width is not claimed.

## A polynomial normalization mechanism

Use the ideal rewrite AB -> sigma BA+cI, with canonical monomials B^i A^j.
Its leading word has no nontrivial self-overlap; degree and inversion count
give termination and uniqueness of the ideal normal form.

To prepend A to a canonical monomial use the exact identity

    A B^i A^j = sigma^i B^i A^(j+1)
                 + c [i]_sigma B^(i-1) A^j
                 + sum_(t=0)^(i-1) sigma^t
                       (B^t U) (V^T B^(i-1-t) A^j),

where [i]_sigma=sum_(t=0)^(i-1) sigma^t. Prepending B requires no reorder.
Propagate already accumulated corrections by the learned left module action.
This avoids branching over all rewrite paths: every word yields an ideal
normal form plus a coefficient matrix between K_{L-2} and W_{L-2}.

After module acquisition to degree L-2, all these corrections use retained
arrays and rational arithmetic, with no native operator calls. Thus any two
new degree-L programs with identical ideal normal forms have a computable
all-input difference. A zero coefficient matrix, in independent module bases,
is an exact equality certificate conditional on the acquired native law.

General circuit multiplication can combine normal forms, left/right actions,
and the small pairing matrix W^T K. A circuit representation and explicit
degree cap are needed to prevent expanding a compact circuit into exponentially
many input words. The executable implementation and verified scope will be
recorded below; a theorem is not a claim that an unimplemented executor ran.

## Fair comparisons and current limits

* QuickSpec already discovers equations through examples and reuses their
  consequences. Testing, equation discovery, and pruning are not new here.
* Randomized range finding already acquires low-rank factors. Displacement
  structure already exploits low-rank operator identities. Neither ingredient
  is claimed as an invention.
* A rank-compressed block Krylov method gets the same source APIs, U,V, data,
  and retention rights. It can acquire the same defect modules and match that
  part of the native query count. The candidate contribution is the obtained
  relation-to-correction/domain calculus and its scope, not a false comparison
  against enumeration of all words.
* Dense tomography uses n action queries per primitive, retains O(n^2)
  entries, and subsequently answers every operator program without native
  calls. At small n it may be cheaper. Every vector-valued query here returns
  n field elements, and exact rational bit growth must also be charged.
* The proposed learner searches a declared law grammar. It does not discover
  arbitrary new syntax, obtain linearity from finite tests, acquire physical
  transpose access, or solve noise/conditioning by assuming exact rational
  answers. Extra native identities can exist, so ideal normal-form inequality
  is not a complete native inequality test.
* AlphaEvolve, DreamCoder, and Stitch get the same observations, source access,
  retained artifacts, and legitimate computation. They may adopt this compiler.
  No architecture-specific advantage or general intelligence is inferred.

## Primary sources consulted

* Novikov et al., AlphaEvolve (2025), https://arxiv.org/abs/2506.13131 .
  Automated evaluators and an initial program are supplied by the task author;
  evolutionary program search is a serious incumbent, not merely orchestration.
* Ellis et al., DreamCoder (PLDI 2021),
  https://people.csail.mit.edu/asolar/papers/EllisWNSMHCST21.pdf .
  Acquires reusable abstractions and a search policy from tasks.
* Bowers et al., Top-Down Synthesis for Library Learning (POPL 2023),
  https://arxiv.org/abs/2211.16605 .
  Stitch acquires program abstractions by corpus-guided synthesis.
* Claessen, Smallbone, Hughes, QuickSpec (2010),
  https://smallbone.se/papers/quickspec.pdf .
  Reads function APIs plus generators, tests equations, and prunes consequences.
* Halko, Martinsson, Tropp, Finding Structure with Randomness (2011),
  https://arxiv.org/abs/0909.4061 . Randomized low-rank range finding.
* Kailath, Kung, Morf, Displacement Ranks of Matrices and Linear Equations
  (1979), https://doi.org/10.1016/0022-247X(79)90124-0 .
  Displacement structure is a close antecedent. The abstract was retrieved;
  the AMS companion full-text route returned 403, so no unseen detail is used.

The unchanged supplied ACQUIRED_BASIS_INFORMATION_OPERATION.md was read.
Its paid structural acquisition and warm/cold distinction are retained. The
pinned Astra repository page was inaccessible through available retrieval
routes; Firecrawl returned insufficient credits. No missing text was invented.

## Structural acquisition without a proposed commutation law

### Theorem: a checked uniqueness gate obtains an unknown rank-one law

Let M_1,...,M_d be fixed rational linear maps available as compositions of
native primitives. They may be dependent. For projective coefficients theta,
write M(theta)=sum_j theta_j M_j. A finite complexity budget supplies the word
library, not a correct relation or source-family label. Choose right probes
Omega and a left projection E, obtaining H_j=E M_j Omega. Expand every
two-by-two minor of H(theta) in the d(d+1)/2 monomials theta_i theta_j, i<=j.
Let C be their exact coefficient matrix. Then:

1. Every native rank-at-most-one relation satisfies C v_2(theta)=0. This uses
   only rank(E M(theta) Omega)<=rank(M(theta)).
2. If C has full column rank, there is no nonzero rank-at-most-one relation
   in the library. This negative result is deterministic under the exact
   linear source contract, not failure to find a sampled candidate.
3. If ker C is one-dimensional, reshape its nonzero vector into a symmetric
   matrix Z. It must be projectively a rank-one symmetric square. If Z_ll is
   nonzero, recover theta_i/theta_l=Z_il/Z_ll and verify every entry against
   these ratios. No square-root choice is necessary.
4. If this succeeds, every possible native rank-at-most-one relation is
   proportional to the candidate. The observed gate proves uniqueness within
   the word library, conditional on existence; no generic-source promise is
   used for this conclusion.
5. Obtain and freshly check a native residual factorization. Conditional on
   that all-input identity event, the law exists and the uniqueness conclusion
   applies. The compressed candidate alone was not an existence certificate.

If ker C has higher dimension, this direct-linearization method returns
UNKNOWN, not a conclusion of no structure. If the unique candidate has syntax
outside the implemented normalizer, the code returns
LAW_CANDIDATE_OUTSIDE_EXECUTOR before native certification.

The actual library is (I,A,B,A^2,AB,BA,B^2): d=7 and the lifted dimension is
28. An eight-by-eight sketch supplies at most 784 minor equations. Retaining
subexpressions requires six primitive actions per right vector, or 48 actions
for acquisition, rather than recomputing all words from scratch. Elimination
uses at most 28 columns, independently of native dimension n. Every vector
query still returns n field elements, and bit lengths and arithmetic are
real costs. Random sketch failure is an obtaining failure, not silently
converted into a membership assumption; the gate is checked on actual data.

Successful executions gave coefficient rank 27 and acquired

    AB - BA = (7/3) I + R             (monomial and Chebyshev sources),
    AB - 2 BA = (7/3) I + R           (q-difference source),

with rank(R)=1. Neither the signs, coefficients, native coordinate basis, nor
source label was passed to the learner. Its word budget, rank-one search
budget, linear exact API, and transpose access were supplied.

This uses established MinRank minors modeling and direct linearization, not
a new general solution to MinRank. At residual rank r the analogous monomial
lift has dimension binom(d+r,r+1). A one-dimensional decomposable kernel gives
a corresponding conditional gate, but that general executor is not
implemented here. Arbitrary instances can require stronger algebraic solvers
and can be computationally hard. The actual uniqueness test is an obtained
condition rather than a hidden teacher supplying the right law.

### Recognition and scope of the acquired calculus

When the recovered AB coefficient is nonzero and only BA and I also occur,
normalizing it gives AB=q BA+cI+UV^T. All preceding module and normal-order
proofs work for arbitrary rational q, including zero, not only signs. Use
[j]_q=sum_(t=0)^(j-1) q^t without dividing by q-1. The q=1 case specializes to
ordinary differentiation. Unsupported law shapes are not relabelled as a
usable calculus. All executions use rational arithmetic; no finite-field
identity is extrapolated to characteristic zero.

## Synthesizing a new scientific computational procedure

For a new polynomial f(z)=sum_j f_j z^j, the acquired rule implies

    A f(B) - f(qB) A
      = c sum_(j>=1) [j]_q f_j B^(j-1) + E_f,

    E_f = sum_(j>=1) f_j sum_(t=0)^(j-1)
                    q^t B^t U V^T B^(j-1-t).

Induction using the exact insertion formula proves this identity. The
procedure learner computes E_f from retained module actions, factors its
small coefficient matrix, and emits actual left/right factors and Horner
coefficients. For degree(f)+1<=L, synthesis takes zero additional native
calls. Execution uses at most degree(f)-1 calls to B and the explicit
correction, with no A call. The target function is supplied after acquisition;
its answer is not in the retained training record.

Direct evaluation with two Horner chains and two A actions costs
2 degree(f)+2 primitive actions when A,B each count as one. This is a
per-execution comparison, not a lower bound against all informed retaining
methods. Dense tomography and structured methods may have better total cost.
Calls inside a derived primitive, such as K=[A,B], must be expanded.

With full-rank factors E_f=L_f R_f^T, ker(R_f^T) is the maximal input subspace
where this particular *uncorrected* procedure is valid. It can exceed the
common domain P_L of every bounded-degree rewrite. Including E_f gives
all-input correctness conditional on the one acquired native identity.

The executed unknown-q procedure used the new degree-five polynomial
f(z)=3-2z+5z^2-7z^4+4z^5. The learned q=2,c=7/3 produced normal coefficients
(-14/3,35,0,-245,868/3) and a rank-one correction. The generated procedure was
saved and reloaded. It matched native execution using four B actions versus
twelve direct actions. An independent exact check covered every one of the
32 source basis columns. These are mathematical/computational controls, not
physical measurements or an end-to-end performance comparison to AlphaEvolve.

## Repairing failure by acquiring a different representation

On a finite fermionic source, the isolated rank-one-law gate had coefficient
rank 10 and kernel dimension 18. Several exact quadratic identities coexist.
An isolated-law representation would discard useful information.

The alternate learner obtains an independent native operator basis from the
same word probes. It fits each generator acting on each basis element, then
checks all closure relations jointly on fresh random vectors. A nonzero
stacked residual is still a nonzero linear map of the input, so its
false-accept probability is at most |S|^-t, without a factor for the number
of fitted relations. Observed compressed basis independence proves native
independence deterministically.

### Theorem: checked closure gives a faithful all-program evaluator

Let native word operators M_0=I,M_1,...,M_(d-1) be observably independent.
Suppose the jointly checked identities are

    A_s M_j = sum_i T_s[i,j] M_i

for every primitive A_s and basis element M_j. Conditional on this identity
event, induction on word length puts every native word in the basis span.
Observed independence makes the representation faithful: different
coefficient vectors denote different native operators. Thus the retained
tables are sound and complete for equality of all finite polynomial programs
in these same primitives. There is no degree limit. Arithmetic work and
coefficient bit lengths can still grow with program size.

This is the conventional finite operator-algebra alternative, given the same
observations and retention rights. It is appropriate when native closure is
actually small. The fermionic control acquired dimension four, basis
(I,A,B,AB), and a three-dimensional complete zero-identity space within the
quadratic library. It now recognizes A^2=B^2=0, which the earlier one-law
evaluator correctly declined to infer. Ten new program graphs were checked
on every source basis vector without new native learning calls. Acquisition
used 96 actions versus 40 for dense tomography at n=20. This repairs
representation and scope; it is not a total-query win.

The same representation fails on truncated differentiation: writing
P=I-[D,X]=n e_top e_top^T, the operators
D^(n-1-i) P X^(n-1-j) are nonzero multiples of every matrix unit e_i e_j^T.
The full algebra therefore has dimension n^2, while its bounded-degree defect
calculus stays compact. Neither representation uniformly dominates.

The final learner uses one WordSketch object for both routes. It tries the
observed small algebra and checked closure; if that fails, it applies the
determinantal learner to the same already acquired matrices. It does not
read a source-family label or repeat failed quadratic probes. In new runs it
chose the defect calculus for the q-source (96 total actions including
degree-six modules), the finite algebra for the fermionic source (96 actions),
and neither for generic operators (48 probes). For the latter, coefficient
rank 28 deterministically excludes nonzero rank-at-most-one laws within the
quadratic library. It does not exclude higher-degree or higher-rank structure.

## General principle: finite defects without finite native closure

Consider a finite, terminating, degree-nonincreasing rewrite system with ideal
normal words N. Suppose each native rule residual is acquired as
R_j=U_j V_j^T, with total rank r=sum_j rank R_j. Let g(k) count normal words
of degree at most k. Then its left and right defect modules through degree k
have dimension at most min(n,r g(k)).

Proof: reduce a word acting on any seed U_j. Each rewrite gives ideal terms
and a residual term l U_t V_t^T r U_j. Its left context l has smaller degree
than the original word, so induction places its columns in the span of
normal-word seed columns. For row modules, use the shorter right context.
This needs no common reset, positivity, or independent hidden components.

This dimension statement alone does not guarantee efficient normalization.
An effective normalizer is required and its work must be charged; confluence,
polynomial growth, and the grammar itself are not obtained for free in the
general case. For the implemented two-generator q-law, the explicit insertion
recurrence supplies a polynomial algorithm and g(k)=binom(k+2,2).

The candidate principle is to acquire a law together with the operator
interface through which it fails. Propagating that interface can be governed
by the law's normal forms even when the full native algebra is huge. This
produces both procedures and validity domains. It is a source-to-operation
construction, not a claim that all its established algebraic ingredients, or
learning operator structure itself, are new.

## Circuit proof, queries, and retained width

Represent every program as P=N_P(A,B)+L K_P W^T, using independent retained
defect bases L,W. For M=W^T L,

    PQ = N_P N_Q + N_P L K_Q W^T + L K_P W^T N_Q
                       + L K_P M K_Q W^T.

Normal-order products of canonical monomials in the first term. Use retained
left/right module actions for the two mixed terms and the pairing M for the
last term. A syntactic degree bound ensures all actions are within the
filtered modules. Induction on a program DAG proves native correctness,
conditional on the acquired law. The implementation does not expand a DAG
into all its words. Normal coefficients number O(Lcap^2), and defect
dimensions are O(r Lcap^2). Arithmetic work is polynomial in Lcap, circuit
size, r, n, and the encountered rational bit lengths. It is not promised
polynomial in circuit size alone when that circuit encodes enormous degree.

For equal ideal normal forms, the difference of programs is
L(K_P-K_Q)W^T. Independence of L,W implies native rank exactly
rank(K_P-K_Q). Thus equality and the dimension of the exact zero-input
subspace are computed from the small matrix. Unequal normal forms give
UNKNOWN, since extra native identities such as A^n=0 can exist.

Module acquisition uses a degree-ordered independent-vector queue, querying
each primitive once per accepted basis vector below the frontier. At depth k
the two-generator native cost is

    2 dim(K_(k-1)) + 2 dim(W_(k-1)),

in addition to relation acquisition. Increasing the depth queries only new
frontier actions. An informed retained block Krylov method gets the same
count. Basis storage is O(n(d_left+d_right)) field elements; small action
tables and correction matrices add polynomial storage. Word caches are
bounded, so processing indefinitely many tasks need not retain their complete
history. Saved generated procedures are additional outputs with real costs.

## Source conditions and decisive failures

### A kinetic source requires a new primitive

The source primitives were A=(3/2)D^2,B=(2/3)X in hidden rational coordinates.
Direct scalar-plus-rank-two commutation failed. Within the explicitly declared
macro choices (A,B) and ([A,B],B), the second obtained
KB-BK=(4/3)I+R, K=[A,B], rank R=2. Every K query was charged as four original
actions. Failed search cost 40 actions, successful law acquisition brought
the total to 190, and degree-seven modules brought it to 250. At n=96,
tomography costs 192. A useful derivative operation was acquired, but this
trial did not show a better total acquisition budget. The macro language is
supplied; arbitrary new primitive syntax was not discovered.

### A different spectral projection changes the defect geometry

On coefficient-truncated Chebyshev polynomials, D differentiates and X
multiplies by x while dropping T_n. Standard recurrences imply

    DX-XD = I - (1/2) (T_n') e_top^T.

The derivative T_n' lies in the retained space. This X is not the nilpotent
monomial truncation, so the pair is not merely a simultaneous change of basis
of the first source. The same procedure mechanism worked after fresh native
acquisition. At n=40,Lcap=8 the left dimension profile was
(1,3,6,9,12,15,18), while the right profile was (1,2,3,4,5,6,7). Favorable
growth observed for the first source cannot simply be assumed on both sides
of a new source.

New polynomials of degrees 2,4,7 yielded exact corrected procedures taking
1,3,6 B actions per input, versus 6,10,16 direct actions. Both a mixed input
and the truncation-boundary input required nonzero corrections. Each generated
procedure was also checked on every source basis vector. Acquisition cost
86 actions versus 80 for tomography: again no universal total-cost win.

An interpretation obstruction remains. For coefficient projection P and
X=P x P,

    P x^2 P - X^2 = (1/4) e_top e_top^T.

The omitted intermediate T_n component returns to T_(n-1) on the next
multiplication. A procedure for f(X) does not automatically implement the
separately defined projected physical potential P f(x) P. Obtaining that
interface needs additional justified source information or interaction. The
code preserves this counterexample; no learned physical force law is claimed.

### Transpose access removes a genuine information barrier

Take B=diag(0,1,...,1), A=e_0 v^T with v_0=0. Then AB-BA=A has rank at most
one. A right query supplies one measurement v^T x. With fewer than n-1
independent measurements, different v can remain consistent with all answers,
even under adaptive deterministic querying. The entire residual cannot be
exactly recovered in the worst case; with at least two unresolved directions,
even its kernel can differ. A transpose query A^T e_0 returns v directly.
Thus the transpose API is substantive and is not free physical access learned
by this work.

### Source binding, exactness, and repeated use

The native maps and transpose semantics must remain fixed after acquisition.
Matching function names and dimensions do not make old factors valid for a
changed source. New discretizations above pay reacquisition. What transfers
across them is the procedure-learning mechanism, not the old native factors.

Probability bounds assume the maps are fixed before fresh independent
validation probes. Seeds make the synthetic executions reproducible; the
theorem concerns the specified random experiment, not an adversarial source
chosen after inspecting its seed. Independent exhaustive source checks
establish the executed finite identities exactly. Floating-point tolerance,
noisy responses, nonlinear maps, and drifting sources are not covered by the
rational identity theorem.

Linearity itself cannot be certified on an unrestricted oracle from finitely
many observations: a nonlinear map can agree on every queried input and
disagree on a new one. It must come from a justified computational interface
or additional source analysis. These experiments acquire algebraic semantics
*within* that linear interface; they do not infer its validity for an unknown
physical system.

All later deterministic symbolic uses share the one native identity event,
even for adaptively selected programs. No new confidence charge is needed per
program. Multiple candidate acquisitions or representation routes do require
an overall allocation. The final two-route learner uses the conservative
bound 2/257^4 when both checks could occur; the finite-algebra-first success
uses 1/257^4. This is not a deterministic proof of an arbitrary unknown native
implementation; it is a randomized all-input certificate under explicit
source assumptions.

## Executed cost evidence and fair comparison

All three scripts use the Python standard library. Source definitions and
reference computations are separate from the learner, which reads only the
linear action/transpose API. Reference answers do not enter acquisition.

The n=64 ordinary-law source cost 44 actions for its relation and 24 for
degree-eight modules, against 128 for tomography. The retained calculus had
1,254 rational array entries including duplicate seeds/factors, against
8,192 dense matrix entries. Maximum retained numerator/denominator lengths
were 60/9 bits. These figures exclude intermediate arithmetic and the
separately retained acquisition record; they are not whole-project storage
or time measurements.

Unlabelled quadratic-law discovery at n=32 cost 80 actions before modules and
then 16/26/16 more for monomial/Chebyshev/q sources. Tomography costs 64 there,
so all three lose on total native query count. Their demonstrated value is
obtained law form, validity, and reusable procedures. At fixed word library,
rank, confidence and degree, the action-count bound is independent of n,
while tomography scales with n. The width of each vector answer, arithmetic,
bit growth, memory, and native action cost must still be included in an actual
scientific application. No universal or minimax performance superiority is
claimed. Cross-source parameter discovery is paid, not called free transfer.

Strong established methods receive identical APIs, observations, prior tasks,
and retention rights. QuickSpec can discover equations and their consequences;
MinRank tools can recover the law; randomized range finding and block Krylov
can acquire the same factors and modules; displacement-structured methods can
exploit them. Ordinary software can adopt the entire construction. The
candidate contribution is the obtained chain from unknown native operations
to a learned rule, retained defect, scoped all-input evaluator, and new
procedures. Literature priority for that combination has not been established
by this bounded source review.

AlphaEvolve already searches whole programs and algorithms; its task API
receives an initial program and automatic evaluator. This construction could
supply one kind of acquired structural correctness evaluator or transformation
library to such a system. It is not a replacement or a claimed superior
inventor. DreamCoder and Stitch already acquire reusable program abstractions.
The target here is obtaining semantic laws and their validity interfaces from
primitive actions; procedure learning and retention themselves are antecedents.

## Additional primary sources

* Thomas, Gu, Dao, Rudra, Re, Learning Compressed Transforms with Low
  Displacement Rank (NeurIPS 2018):
  https://proceedings.neurips.cc/paper_files/paper/2018/file/8e621619d71d0ae5ef4e631ad586334f-Paper.pdf .
  Joint learning of displacement operators and residuals already exists.
* Bostan, Jeannerod, Mouilleron, Schost, On Matrices with Displacement
  Structure: Generalized Operators and Faster Algorithms (2017):
  https://arxiv.org/abs/1703.03734 . Retained structured generators are a strong
  computational alternative.
* Faugere, Safey El Din, Spaenlehauer, On the Complexity of the Generalized
  MinRank Problem (2013 version): https://arxiv.org/abs/1112.4411 .
  Determinantal modeling and algebraic low-rank-pencil solving are established.
* Bardet et al., Improvements of Algebraic Attacks for Solving the Rank
  Decoding and MinRank Problems:
  https://www.nist.gov/publications/improvements-algebraic-attacks-solving-rank-decoding-and-minrank-problems .
  Stronger algebraic linearization methods remain legitimate comparators.
* NIST DLMF section 18.9: https://dlmf.nist.gov/18.9 .
  Recurrences underlying the independently specified Chebyshev source; the
  defect and projection formulas here are deductions from those definitions,
  not DLMF empirical findings.

The earlier conditional-operation and causal-controller results remain
separate preserved capital. This new construction imports no unavailable
historical helpers and uses no physical measurements or external publication.
