# Acquired input-output laws, retained information, and optimal new experiments

New construction in this continuation, 2026-10-25. The earlier operator-law,
metric, frame, defect-module, reaction-history and conditional-operation files
remain separate capital. No unavailable historical helper has been recreated.

## 1. What the construction obtains

The most useful outcome is an **acquired description of which scientific
operations are already determined, what remains unknown, and exactly how many
additional forward experiments a new linear response functional needs**.

The starting instrument supplies exact actions of a fixed linear map

\[
H:\mathbb Q^n\longrightarrow\mathbb Q^m,\qquad f\longmapsto y=Hf.
\]

It supplies no transpose. The learner searches for short equations among the
observable input/output coordinates and retains actual coefficients

\[
CH=D.
\]

The supports, coefficients, response rank and actuation incidence need not be
given. A fresh randomized all-input identity check follows discovery. A
complete presentation makes a transpose and new inverse-problem procedures
executable. An incomplete presentation remains useful. Crucially, the final
construction retains **every observed forcing-response pair**, including the
validation probes, rather than discarding observations after fitting laws.

Given these laws and observations, all remaining models can be parameterized
as

\[
H=H_0+NZT,\qquad Z\text{ arbitrary}.
\]

Here the columns of N span ker(C), the rows of T annihilate all previously
queried input directions, and H0 is an explicitly constructed consistent
completion. For a new task

\[
L_W(H)=\langle W,H\rangle_F,
\]

the exact marginal query complexity is

\[
\boxed{\operatorname{rank}(N^TWT^T)}.
\]

The code generates that many **full-vector forward queries**, obtains the
answer, and retains the new pairs. The matching lower bound is proved below
for deterministic exact algorithms over the full consistent-completion class.
It is not imported from a scalar oracle theorem. A retaining conventional
algorithm with the same laws and data can run this construction and tie it.

This is a scoped enabling framework, not an established historical novelty
claim or evidence of a superior general discovery agent. Kernel representations,
sparse identification, sparse updates, elimination, optimal recovery and
inexact-adjoint analysis have substantial antecedents. What is now executable
here is the acquisition-to-operation chain, including its missing-information
calculus, fresh tasks and exact limits.

## 2. Access contract and distinctions

The following are assumptions about the instrument, not conclusions of a few
experiments:

1. H is fixed and linear throughout acquisition and the uses of its certificate.
2. Inputs can be selected in the stated coordinate system; complete m-vector
   outputs are returned. Dimensions and units are known.
3. Executed answers are exact rationals. These are supplied software controls,
   not noisy physical observations or inferred biological kinetics.
4. Ideal independent draws from finite alphabets underlie probability bounds.
   The scripts use seeded PRNGs for reproducibility; a seed is not an
   adversarial-randomness guarantee.
5. New objectives, readouts, weights and regularizers are task specifications.
   Their scientific desirability is not learned by the evaluator.

Every native query returns m scalars. An experiment count independent of n is
therefore not an information bound for scalar measurements. Arithmetic, input
and output widths, rational bit lengths, failed search and construction costs
are reported separately. The initial discrete alphabet has 2^61 elements in a
bounded interval. The subsequent optimal-query compiler normalizes every
input coordinate to absolute value at most one, but exact precision remains a
substantive premise.

No claim is made that an arbitrary hidden physical environment has short
equations on its visible ports. Eliminating hidden variables can destroy that
property. Successful certification is about the observable response operation;
it does not identify a unique microscopic explanation or authorize a change
to the physical system based on a new interpretation of C and D.

## 3. Obtaining local relations without an inverse or a hidden coordinate promise

Let

\[
K=\begin{bmatrix}H\\I_n\end{bmatrix}.
\]

A relation on input/output coordinates is a row vector (c,-d) satisfying
(c,-d)K=0, equivalently cH=d. The relation space has dimension m. Its projection
onto the c coordinates is an isomorphism: c determines d=cH, and c=0 implies
d=0. Thus m independent true relations give an invertible output coefficient
matrix C. The rank of H itself is irrelevant.

### The local-rank acquisition statement

Fix H and a support budget s. Take q=s independent input vectors, with each
coordinate drawn uniformly from a set of M distinct rational values. For any
coordinate subset S of size k<=s, let r=rank(K_S). There is an r-by-r minor of
K_S applied to the first r random input vectors which is a nonzero polynomial
of degree r in the random coordinates. The polynomial is nonzero because r
independent row functionals admit inputs on which their evaluations are
independent. Therefore its probability of vanishing is at most r/M.

By a union bound, with failure probability at most

\[
\min\left(1,\frac1M\sum_{k=1}^s k{m+n\choose k}\right),
\]

all coordinate-subset ranks of size at most s are preserved by the observations.
For continuous generic inputs the failure probability is zero. This is a
fixed-source, nonuniform statement; it is not uniform recovery of every H
from one chosen set of s probes.

On that rank-preservation event, the kernel observed on each support is exactly
the true relation kernel on that support: true relations remain relations,
and equal ranks give equal nullities. Enumeration therefore acquires all local
linear circuits, meaning nonzero dependencies of minimal coordinate support.

Every relation is a sum of circuits contained in its support. To prove this,
take a nonzero relation r, choose a minimal dependency c within its support,
and cancel one nonzero coordinate by subtracting a scalar multiple of c.
Iterate on the reduced support. Thus, if there exists a complete presentation
whose rows each use at most s total input/output coordinates, the local
circuits span the complete relation space. Selecting m independent output
coefficient rows obtains an invertible C.

If the local circuits span only r<m output directions, the algorithm retains
that partial presentation instead. It does not invent the missing equations.

### What the executor does

`acquired_relational_semantics.py` enumerates supports in increasing size. A
nonzero square minor modulo a prime proves independence over the rationals and
rejects a support cheaply. Zero modular minors go to exact rational nullspace
computation. Supersets of already discovered minimal circuits need not be
searched again. The selected relations and actual observations are stored.

The search cost is combinatorial in s, up to a polynomial factor times
sum_{k<=s} binomial(m+n,k). This is not an efficient general sparse-identification
algorithm. Sparse regression and structured identification are legitimate
alternative proposal engines; they may use the same final certificate.

**Important modular detail.** A rationally nonzero minor remains a safe
rejection witness when it is nonzero modulo the chosen prime and all observed
denominators are invertible modulo that prime. A zero modular minor proves
nothing. Comparing modular support rank with modular augmented rank would be
unsafe: the equation p*c=1 has rational solution 1/p even though the coefficient
matrix vanishes modulo p. The executor uses a nonzero minor of the appropriate
full size, never that unsafe comparison. This failure has an executable control.

## 4. The global certificate and repeated use

Freeze any proposed matrices C,D, regardless of how they were obtained. For t
fresh vectors whose coordinates are independent uniforms from an alphabet of
size Mv, check

\[
CHf_j=Df_j.
\]

If R=CH-D is nonzero, some row is a nonzero linear functional. Conditional on
all but one relevant input coordinate, at most one value of the remaining
coordinate makes that row zero. A wrong frozen candidate passes all t probes
with probability at most Mv^{-t}. This proof does not assume sparsity, locality,
reciprocity, low rank or invertibility of H.

The implementation uses Mv=257 and t=5 for a first candidate. Its fixed-candidate
false acceptance bound is 1/257^5, approximately 8.9194e-13. If candidates are
adaptively revised, use fresh probes and t_j=5+j for attempts j=0,1,...; the
total bound is at most 257/(256*257^5), approximately 8.9542e-13. The inverse
and transfer executors charge their actual attempts, including failed checks.

The acquisition rank bound concerns **finding** the correct equations within
the search budget. The fresh identity bound concerns **accepting** wrong
equations. These are distinct events and must not be conflated.

On the event that the accepted equation is true, it is true for every input.
Any number of later adaptive readout queries, procedure candidates or exact
experiments may reuse it. There is no probability charge per downstream
candidate. Changing the source or the learned equation requires new
justification; loading a file does not certify a new external instrument.

These randomized statements do not establish linearity of an unknown
physical source. A nonlinear or time-varying source can agree on all tested
inputs and differ elsewhere. The exact linear instrument contract remains
substantive.

## 5. Complete and partial executable semantics

### Complete presentation

When C is square and nonsingular, CH=D implies

\[
H=C^{-1}D,\qquad H^T=D^TC^{-T}.
\]

An executable sparse elimination tape for C therefore supplies forward and
adjoint actions with no native source calls. The tape records its actual
pivots, row tails and elimination multipliers. Complete pivoting permits
zero-diagonal but nonsingular matrices. The transpose solve is the reverse
linear computation of the forward solve. Neither sparse elimination nor this
transposition principle is new.

The recovered C,D need not equal the equations used to construct the source.
Equivalent presentations can differ by invertible row operations. The
experiment below actually retains fewer D entries than the source description.
The claim is an exact response operation, not unique mechanistic identification.

### Partial presentation

Suppose C has full row rank r<m and CH=D has been certified. A new readout O is
obtained from these relations whenever exact linear solving gives O=L C. Then

\[
OH=L D=:G.
\]

G is a retained executable response for that readout. It supplies forward
predictions, adjoints and task gradients without reconstructing other outputs.
If a row of O lies outside rowspan(C), the relations alone do not determine its
response on every input. Choose z in ker(C) with Oz nonzero and a nonzero input
functional v^T. H and H+zv^T satisfy the same relations but differ under O.

That last statement is only about the relations. An equally informed method
also has the raw observations, which determine additional operations. The next
section incorporates all those observations instead of forcing a retainer to
forget them.

## 6. All retained observations and laws: the complete uncertainty object

Let U have independent columns spanning **all** previously queried inputs,
including training, validation and later task-directed queries. Let V=HU be
their corresponding responses. Retain the original pairs as well; U,V are a
computational basis, not a replacement that discards information.

Let C have independent rows, and suppose CV=DU. Choose:

- N, a full-column-rank basis of ker(C), of size m-by-(m-r);
- T, a full-row-rank matrix with ker(T)=range(U), of size (n-q)-by-n;
- any explicitly constructed H0 satisfying CH0=D and H0U=V.

Then the complete set of consistent linear responses is

\[
\mathcal H=\{H_0+NZT: Z\in\mathbb Q^{(m-r)\times(n-q)}\}.
\]

**Proof.** A difference Delta between two consistent responses satisfies
C Delta=0 and Delta U=0. Its columns lie in range(N), so Delta=N A. Since N is
injective, A U=0. Each row of A lies in the row space of T, so A=ZT. Conversely
every NZT satisfies both homogeneous constraints. The parameterization is
injective in Z because N is injective and T is surjective. Therefore the
remaining dimension is exactly (m-r)(n-q).

### Obtaining H0 without orthogonal projections or a dense response matrix

Row-reduce C and transform D by the same operations. This writes pivot output
coordinates as

\[
y_P=D'f-Ey_F.
\]

Choose input pivot coordinates I so the square submatrix U_I is invertible.
Define coefficients a(f)=U_I^{-1}f_I. Set the free output coordinates to
y_F=V_F a(f), then determine y_P by the equation above. This defines H0f and
agrees with every old observation. It needs a factor of U_I and retained
responses, not an explicit m-by-n matrix H0.

Standard nullspace construction gives N an identity on free output coordinates
and T an identity on free input coordinates. Therefore a desired vector b in
the T-input coordinates can be realized by an input supported on those free
coordinates, and the N-coordinates of a residual can be read from the free
output coordinates. These interfaces are constructed by elimination; they
are not supplied physical projections.

### Exactly determined linear functionals

For a task W of size m-by-n,

\[
L_W(H)=\langle W,H\rangle_F
=\langle W,H_0\rangle_F+\langle N^TWT^T,Z\rangle_F.
\]

Thus the functional is already determined iff N^TWT^T=0. This criterion uses
both the acquired laws and the full observation history. It allows
combinations of known output directions and known input directions.

For a scalar bilinear query o^T H f, with both remaining spaces nonzero, the
criterion reduces to: either o lies in rowspan(C), or f lies in range(U).
Queries outside both spaces need additional information. In particular, a
small output rank does not obtain an unknown input-facing adjoint functional.

## 7. Optimal additional full-vector experiments for a new functional

Put A=N^TWT^T and k=rank(A). Compute a rank factorization

\[
A=\sum_{j=1}^k a_j b_j^T.
\]

Construct f_j with T f_j=b_j using the free input coordinates. The response
residual y_j-H0f_j has N-coordinates Zb_j, which are obtained from its free
output coordinates. Hence

\[
L_W(H)=L_W(H_0)+\sum_{j=1}^k a_j^T Zb_j
\]

is obtained with exactly k additional native forward queries. The executor
rescales f_j when needed to enforce ||f_j||_infinity<=1 and compensates in the
contraction. This changes neither the query count nor the spanned directions.

The new pairs are appended **after** the old rank-factor calculation has been
executed. Updating H0 in the middle without changing the calculation would
double-count terms. Rebuilding the knowledge object then makes this functional
exactly determined and may reduce the cost of unrelated future tasks.

### Matching lower bound with the full vector API

Consider an arbitrary deterministic exact algorithm required to answer this
functional for every H in the completion class. Follow its adaptive execution
on the base completion H0. Suppose it makes t<k additional queries. Let S be the
span of their transformed input coordinates T f_i; dim(S)<=t.

Because rank(A)>t, some v orthogonal to S satisfies Av!=0. Let a=Av and choose
an alternative free matrix Z=a v^T. It changes every complete queried response
by N a(v^T T f_i)=0, so the entire adaptive transcript is unchanged. Yet it
changes the requested functional by

\[
\langle A,a v^T\rangle_F=a^TAv=\|Av\|^2>0.
\]

Two fixed sources in the allowed class therefore produce identical full-vector
transcripts but different required answers. The algorithm cannot be correct
on both. At least rank(A) queries are necessary in the worst case.

This proof explicitly allows a query to return all m output coordinates. It
does not reuse the earlier finite-field scalar-query lower bound. Its scope is
deterministic exact worst-case computation with rational inputs over the
unrestricted rational completion class. It does not exclude a randomized
bounded-error method, further structural promises, a supplied coefficient
bit-size bound enabling a different encoding strategy, access to a transpose,
source-code inspection, or a different approximate task. It is not a lower bound
for the publicly specified control example when its source formula is supplied
to the solver.

### Why this is reusable learning

The acquired laws determine N; actual past interactions determine T. A new W
was not needed during acquisition. Its missing coefficient A determines an
experimental procedure, not a remembered answer. Every executed experiment
then changes the retained knowledge and the requirements of future tasks.

The lower bound is relative to exactly the same retained information. An
ordinary retaining programme can use the same acquired N,T and generate the
same optimal strategy. The contribution under consideration is that these
objects and the procedure are obtainable from interactions, not architectural
exclusivity.

## 8. New inverse tasks and an acquired evaluator

For a complete presentation and a new readout O, data y and diagonal positive
penalty Gamma, consider

\[
\min_{u,f}\frac12\|Ou-y\|^2+\frac12 f^T\Gamma f,
\qquad Cu-Df=0.
\]

The compiler generates the first-order linear system

\[
\begin{bmatrix}
O^TO&0&C^T\\
0&\Gamma&-D^T\\
C&-D&0
\end{bmatrix}
\begin{bmatrix}u\\f\\p\end{bmatrix}
=\begin{bmatrix}O^Ty\\0\\0\end{bmatrix}.
\]

C invertible and Gamma positive imply a unique optimum even if H or D is rank
deficient. To check uniqueness of this KKT system, take a homogeneous solution
and combine its stationarity equations with its constraint. This gives
||Ou||^2+f^T Gamma f=0. Thus f=0, then Cu=0 implies u=0, and C^T p=0 implies p=0.

Generic complete-pivot elimination generates an executable instruction tape.
Checking the KKT residual and the acquired constraint certifies the operation
without a supplied correct answer. A standard state or observation Gram solve
gets exactly the same learned equations and is often arithmetically cheaper;
those alternatives were executed, not excluded.

The compiler uses supplied differentiation and elimination rules. This is a
learned semantic component for further procedure discovery, not a claim that
the system invented Gaussian elimination or an unprecedented optimization
algorithm. The desired objective remains supplied.

## 9. Approximate presentations and a relative adjoint certificate

For any frozen invertible C and any D, let

\[
R=CH-D.
\]

Then

\[
H^T=D^TC^{-T}+R^TC^{-T},
\qquad
\|H^Tz-D^TC^{-T}z\|\le\|R\|\,\|C^{-T}z\|.
\]

The square inverse case uses C=B,D=I. Writing d=B^{-T}z gives the particularly
useful relative bound

\[
\|H^Tz-d\|\le\epsilon\|d\|
\quad\text{if}\quad\|BH-I\|\le\epsilon.
\]

If epsilon<1, BH, B and H are invertible. No reciprocity, exact low rank or
exactly sparse inverse is required for this certificate. An approximate B can
come from any proposal engine or previously acquired model.

### Obtaining the operator bound using rational forward probes

Ball's cube-slicing theorem implies that, for uniform U on [-1,1]^n and every
unit vector v, the density of v^T U is at most 1/sqrt(2). Consequently
P(|v^T U|<=tau)<=sqrt(2)*tau. See Melbourne and Roberto, Theorem 1, cited below.

Round each U coordinate to one of M equal interval midpoints to obtain a
uniform finite-grid vector xi. The coupling error is at most sqrt(n)/M in
Euclidean norm, hence

\[
\Pr\{|v^T\xi|\le\tau\}
\le\sqrt2(\tau+\sqrt n/M).
\]

For a top right singular vector v of R,
||R xi||>=||R|| |v^T xi|. With t independent probes, m0=max_j||R xi_j||, this gives

\[
\Pr\{\|R\|>m_0/\tau\}
\le[\sqrt2(\tau+\sqrt n/M)]^t.
\]

The executor uses tau=1/4, M=65536 and t=16. It replaces sqrt(2) by 3/2 and
sqrt(n) by its integer ceiling to keep the reported probability arithmetic
exact. At n=32 the failure bound is about 1.5383e-7. It compares the exact
squared upper bound m0^2/tau^2 with one. This is a conservative norm estimator,
not a new concentration theorem or a dimension-independent approximation
ratio. It can reflect Frobenius scale and be loose for full-rank defects.

### An evaluator without a reference optimum or native adjoint

Let J(f)=ell(O H f-y)+r(f), with known differentiable convex ell and known
lambda-strongly-convex r. One actual forward action obtains the field Hf and
therefore z=O^T grad ell. Let

\[
v=C^{-T}z,\quad \widetilde g=D^Tv+\nabla r(f),
\quad e=\epsilon\|v\|.
\]

Then ||grad J(f)||<=||gtilde||+e, and strong convexity yields

\[
0\le J(f)-J(f_*)\le\frac{(\|\widetilde g\|+e)^2}{2\lambda},
\qquad
\|f-f_*\|\le\frac{\|\widetilde g\|+e}{\lambda}.
\]

The first inequality follows by minimizing the strong-convexity quadratic lower
bound at f. The distance bound follows from strong monotonicity of the gradient.
The executor uses exact upward rational square-root enclosures. The retained
operator event covers every later candidate and task, including candidates
chosen after inspecting earlier evaluations. It is not a guarantee that the
bound will be small.

The current numerical evaluator executes the square relative case. The
rectangular formula above is proved but not separately executed under noisy
or approximate rectangular data. Exact rectangular tasks are executed.

### Cancellation and the fallback operation

A relative error bound for one adjoint component does not automatically give
a descent direction after adding a regularizer or applying an arbitrary input
projection. The executed scalar counterexample is

\[
H=11/10,\quad B=1,\quad \lambda=1,\quad
f=99/100,\quad y=221/110.
\]

For J(f)=.5(Hf-y)^2+.5 f^2, the true gradient and the approximate total gradient
have opposite signs despite ||BH-I||=0.1. Their product is
-169949/110000000. Stepping along minus the approximate total gradient increases
the objective locally.

For any proposed direction d, one forward query Hd gives the exact directional
derivative. If it is positive, -d is a descent direction. Every line-search
field H(f-alpha d)=Hf-alpha Hd is then available without more native queries.
This is standard directional-derivative and line-search reasoning. Its useful
role here is to retain a verified task operation when a conservative global
certificate or a naive gradient-combination rule fails.

## 10. The inverse-equation specialization and transfer

For square invertible H with inverse rows of support at most s, the fixed
right-hand side D=I simplifies discovery. From forcing matrix F and response
matrix Y=HF, solve each sparse row equation

\[
b_i^T Y=F_{i,:}.
\]

For a fixed source, q=s+1 generic full-vector experiments reject every false
support of size at most s and identify the correct rows. A wrong support S
has coordinate response functionals e_j^T H, j in S, independent of the target
functional e_i^T. A nonzero (|S|+1)-minor excludes it. A correct support is
identified when its own evaluation matrix has full rank. The finite-alphabet
union bound used in the code is

\[
\min\left(1,\frac nM\sum_{k=1}^s(k+1){n\choose k}\right).
\]

This is a specialization of the joint relation construction: each inverse row
has at most s output terms plus one specified input term.

Once supports have been acquired, a new source with the same proposed supports
needs only new coefficient fits before fresh global validation. If the fit
fails, the failed observations identify equations needing repair. Searching
the old support plus at most t extra coordinates costs binomial(n-|S|,t)
extensions rather than rediscovering every coordinate. With q>=max_i |S_i|+t+1
generic experiments, the same minor argument separates false extensions.

The old support is a proposed search space, not an asserted invariant of the
new source. A dense change can exceed the repair budget. Sparse model recovery
after changes has direct precedent in abrupt-SINDy; no novelty is claimed for
retaining supports or favoring a small change by itself.

## 11. Executed constructions and failures

### Unknown nonreciprocal inverse equations

The supplied source is a strictly diagonally dominant, nonsymmetric,
permuted nearest-neighbor balance system of dimension 32. The learner does not
receive its ordering, coefficients, local operator action or transpose. H is
dense and full rank.

| Quantity | Executed result |
|---|---:|
| Training forward calls | 4 |
| Fresh identity checks | 5 |
| Returned scalars | 288 |
| Supports examined | 94,995 |
| Exact candidate fits | 32 |
| Modular inversions | 268,346 |
| Modular multiplications | 1,700,040 |
| Modular subtractions | 1,180,115 |
| Fraction arithmetic during acquisition | 5,116 |
| Learned equation entries / factor entries | 94 / 94 |
| Factor construction Fraction arithmetic | 93 |
| New adjoint Fraction arithmetic | 188 |
| Dense retained adjoint Fraction arithmetic | 1,984 |
| Maximum input / output rational bit lengths | 62 / 265 |

The full-source incumbent can obtain the equations without any learning
queries. The factorization and transpose routines are ordinary sparse linear
algebra. The learned model is advantageous as an acquired interface, not as an
exclusive solver architecture.

### Strong acquisition alternatives on the same API and history

Basis pursuit uses SciPy/HiGHS to propose supports, exact rational refitting,
and the same fresh global certificate. Its first four exact interactions are
identical to the exhaustive learner's. A second version additionally tries the
scientifically appropriate positive-diagonal/nonpositive-off-diagonal sign
hypothesis and still validates it globally.

| Method | Native forward calls | Additional local work |
|---|---:|---|
| Exhaustive support acquisition | 9 | About 3.15 million modular operations, plus 5,116 Fraction operations |
| Unconstrained basis pursuit proposal | 29 | 128 LPs, 1,836 reported HiGHS iterations, 22,020 Fraction operations |
| Sign-structured LP proposal | 17 | 78 LPs, 707 reported HiGHS iterations, 11,924 Fraction operations |
| Dense coordinate tomography | 32 | 4,992 Fraction operations for response acquisition; 1,024 stored H entries |
| Full source equations available | 0 learning calls | Direct ordinary sparse factorization |

The modular total counts inversions, multiplications and subtractions as
separate field operations; these have different bit costs. HiGHS does not expose
its total scalar FLOPs here, so dimensions, LP calls, iterations and local time
are reported instead. No matched-FLOP superiority is inferred.

For this inexpensive software source, exhaustive acquisition is slower locally
than either LP proposal or tomography. The executed profiled times were about
1.6 seconds for exhaustive discovery, 0.42 seconds for unconstrained LP, 0.18
seconds for sign-structured LP, and 0.015 seconds for tomography. These are
prototype observations, not portable benchmarks. A lifetime advantage requires
a workload where source actions or later repeated operations justify the
acquisition cost. All successful methods may retain the same model and use
the same later procedures.

### New kinetics and a new coupling

Fresh coefficients on the same unknown graph transferred in 8 calls, with
4,208 Fraction operations and no combinatorial support extensions. A changed
coefficient field plus an extra coupling, chosen by a fixed independent seed,
failed the old-support check, localized one changed row, and was repaired in
11 total calls with 13 support extensions and 9,053 Fraction operations. The
changed row was 17 and the new input coordinate 12; neither was supplied to
the learner. A dense perturbation exceeded the one-extra-coordinate repair
budget after 5 calls and 930 failed extensions.

Two genuinely new inverse tasks used different readouts, data and regularizers.
Their generic KKT compiler required 2,754 and 3,872 Fraction operations. Standard
state formulations used 1,706 and 2,455; standard observation formulations used
2,964 and 5,547. Answers were exactly equal. Construction/execution made zero
native source calls; separate native confirmations were charged separately.
The generic compiler did not beat the strongest state formulation.

### Complete rectangular, rank-deficient semantics

`acquired_relational_semantics.py` used a supplied response with 16 inputs,
12 outputs and rank 6. Its output balance and actuation incidence were withheld
from the learner. Five training calls plus five fresh checks obtained a complete
presentation. The search examined 79,379 supports, computed 50 exact nullspaces,
and selected 12 independent equations. It retained 38 C entries, 12 D entries,
and a 38-entry factor of C. Maximum output rational length was 181 bits.

Acquisition used 14,153 Fraction operations plus 289,433 modular inversions,
2,646,484 modular multiplications and 1,960,868 modular subtractions. A new
adjoint used 100 Fraction operations versus 288 for the dense response. A new
inverse task compiled in 1,301 Fraction operations; the equally informed
observation-space method used 984. Every input-basis forward action and every
output-basis adjoint action agreed exactly with a separate full-source
reference. This is a constructive extension beyond a square inverse, not a
runtime victory over structured algebra.

### Incomplete models and new experimental strategies

A rank-one source with dense unknown input functional yielded two true
output-null relations, but no nonzero input-facing operation. The compiler
returned UNKNOWN for the requested output response instead of mistaking output
rank for an acquired adjoint.

A different source with 19 input coordinates and 3 output coordinates yielded
one useful relation, y0=2 f3, while leaving the other outputs unmodeled. All
seven acquisition pairs were retained: two training experiments and five
validation probes. Their input span has dimension 7. The remaining response
class therefore has dimension (3-1)(19-7)=24.

Two new, dense, independently specified response weight matrices each required
rank(N^TWT^T)=2 new forward experiments. The generated answers matched exact
references. All new inputs had absolute coordinates at most one. After both
tasks, 16 independent response parameters remained undetermined: the framework
had not reconstructed the whole source. A third new weight matrix in the
acquired observable span required zero new experiments.

The respective nontrivial exact answers were
1392430267/232792560 and 304338447473/21416915520. Their numerical values are
method controls, not scientific discoveries. The result is the general
acquisition mechanism and the matching full-vector query bound.

With all the same raw history but without the acquired law, the missing-rank
calculation was 3 for each task. This is an information comparison, not a
handicapped incumbent: a retaining method given the same acquired law requires
the same 2 queries as this method. The executable contains both comparisons.

Initialization used 4,645 Fraction operations; the two acquisition plans used
14,913 and 18,147, including the new source actions and reconstruction of the
retained information. The generic zero-query task still used 16,129 Fraction
operations. That failure led to an actual procedure specialization: testing
whether W factors through C and, when it does, contracting directly with D.
The same new task then used 76 Fraction operations. Both executed versions and
their equal answers are retained. This contraction is a standard consequence
of the acquired law, not a claimed new algebraic identity. Zero native work
alone does not imply cheap local computation.
The four new inputs used at most 170-bit rational coefficients and returned
at most 200-bit rational outputs. Their conditional componentwise new-query
noise amplifiers were about 24.98 and 22.35. Those are not noisy learning
guarantees: the earlier laws and history were assumed exact in that calculation.

### Dense changes and the approximate evaluator

The previously acquired B was tested against preselected changes
H_eta=B^{-1}(I+eta*Cw), where Cw is a full-rank rational Walsh operator with
Cw^T Cw=I/32. The learner did not receive eta or Cw. Both changed inverse
matrices have all 1,024 entries nonzero.

| eta | Acquired residual-norm upper bound | True norm, control only | Outcome |
|---|---:|---:|---|
| 1/5 | 0.537919 | 0.0353553 | Useful relative adjoint certificate |
| 1 | 2.689593 | 0.176777 | Conservative global certificate does not pass epsilon<1 |

Each calibration used 16 forward calls and failure bound about 1.5383e-7.
The failed certificate does not prove that the larger change is unusable or
that a ranking reverses. A one-query directional check produced a verified
descent step for each preselected case.

For two new regularized inverse tasks under eta=1/5, a candidate compiled from
the retained model had true objective gaps about 7.76e-5 and 1.08e-4. The acquired
evaluator certified the larger bounds 0.03985 and 0.04533 using one forward
response per candidate. Zero and wrong-sign candidates were also evaluated;
their large bounds were retained rather than treated as successes. The desired
optima and exact true gradients appeared only in separate known-answer checks.

## 12. Comparators and where the construction stands

The comparison is not against independent marginals, forgotten trajectories,
or a programme forbidden from retaining the learned object.

- **Behavioral identification.** Kernel representations of manifest variables,
  latent-variable elimination and interconnection are established ideas.
  C y=D f is within that tradition, not a new philosophy of models.
- **SINDy-PI and SINDy-BVP.** Implicit sparse equations and inference of operators
  from forcing/response data have direct precedents. The present exact linear
  local-rank acquisition proof and all-input semantic use are a narrower
  construction; no claim is made to beat their noisy nonlinear identification.
- **Abrupt-SINDy.** Minimal changes to previously acquired models are an explicit
  antecedent of support transfer and repair. Retention itself is not the new
  claim.
- **Sparse recovery and forward-only operator learning.** Park/Nakatsukasa,
  Schafer/Owhadi, Boulle/Halikias/Otto/Townsend, and Gallmeier/Otto provide strong
  structured and adjoint-free approaches. In particular, the 2026 local-row-space
  method made the initial proposed route too close to established work. That
  route was not presented as a discovery. The present proposal searches the
  input-output relation structure instead of assuming prescribed response row
  subspaces; it pays combinatorial search and does not dominate those methods.
- **CoLA and structured solver libraries.** Given semantics or differentiable
  source code, they can exploit structure, transpose computations and select
  efficient procedures. CoLA explicitly obtains transposes using VJPs when the
  MVM code is differentiable. That interface should be used when available;
  a black-box experiment is a different access contract. The executed
  full-source and retained structured alternatives are allowed those rights.
- **Random identity testing.** A proposed global relation can be checked with
  fresh native actions without any special architecture. The useful object is
  the acquired relation plus its executable consequences, not the act of testing.
- **Inexact adjoints and optimal recovery.** Residual-based gradient guarantees,
  directional tolerances and information-based lower bounds have substantial
  antecedents. The exact marginal-rank result is proved for the particular
  acquired-information object; historical novelty of that linear-algebra result
  is not established here.
- **AlphaEvolve and other procedure search.** AlphaEvolve's primary description
  receives evaluation code from the user. This construction can obtain one
  missing source-dependent evaluator component before such a search begins.
  It has not executed an AlphaEvolve-scale search or invented a faster general
  algorithm. A search system given the same acquired object is an equally
  informed adopter, not an excluded competitor.

The result removes concrete restrictions of the preceding implementation:
nonreciprocal full-rank responses can yield adjoints; a square invertible
response is unnecessary; a full response model is unnecessary for useful
certified operations; and all retained observations contribute to an optimal
new experimental strategy. It does not remove combinatorial acquisition,
finite-precision/noise issues, unknown observation interfaces, or the need to
know what scientific question should be optimized.

## 13. Executable sources and exact run order

All files below are new work in this continuation. The core executors use only
the Python standard library. The LP comparison additionally uses NumPy/SciPy.
The JSON files contain actual retained matrices, factors, inputs, responses,
generated procedures, failed attempts and calculation results.

```text
python acquired_inverse_relations.py
python acquired_relative_adjoint.py
python acquired_balance_transfer.py
python acquired_operation_evaluator.py
python acquired_relational_semantics.py
python acquired_relational_controls.py
python acquired_query_acquisition.py
python acquired_inverse_alternatives.py  # NumPy/SciPy environment
```

Meaningful implementation controls include complete-pivot forward and transpose
solves on 18 nonsingular matrices with 81 basis right-hand sides, singular
rejection, the modular rank-drop counterexample, poorly exciting training,
new-coupling repair, dense failure, rank-deficient complete presentation,
incomplete input-facing information, and a nonzero completion witness that
preserves every prior observation and law but changes a new requested
functional. These tests supplement the proofs; they are not the proofs.

## 14. Primary sources actually consulted

1. Astra pinned governing entry, revision aa6e6a70aa35a337ef9e4cb714a2da2440d58733:
   https://raw.githubusercontent.com/harjassand/astra-research-knowledge/aa6e6a70aa35a337ef9e4cb714a2da2440d58733/00_START_HERE.txt
   Used for the exact information/cost/assumption and UNKNOWN conventions, not
   as evidence of a theorem in this file. Earlier local scientific files remain
   the actual continuation capital.
2. Gallmeier and Otto, *Efficient Approximation of Structured Linear Operators
   using Randomized One-Sided Queries*, 2026, v1:
   https://arxiv.org/html/2610.07513v1
3. Boulle, Halikias, Otto and Townsend, *Operator learning without the adjoint*,
   JMLR 25(364), 2024: https://jmlr.org/papers/v25/24-0162.html
4. Park and Nakatsukasa, *Approximating Sparse Matrices and their Functions using
   Matrix-vector products*, v3, 2026:
   https://arxiv.org/html/2310.05625v3
5. Schafer and Owhadi, *Sparse recovery of elliptic solvers from matrix-vector
   products*, v4: https://arxiv.org/abs/2110.05351
6. Trentelman and Willems, *The Behavioral Approach as a Paradigm for Modelling
   Interconnected Systems*, 2003, author-hosted text:
   https://homes.esat.kuleuven.be/~sistawww/smc/jwillems/Articles/JournalArticles/2003.3.pdf
7. Kaheman, Kutz and Brunton, *SINDy-PI*, 2020:
   https://arxiv.org/abs/2004.02322
   Primary abstract was accessible; the attempted PDF endpoint was blocked.
8. Shea, Brunton and Kutz, *SINDy-BVP*, 2021:
   https://arxiv.org/abs/2005.10756
9. Quade, Abel, Kutz and Brunton, *Sparse Identification of Nonlinear Dynamics
   for Rapid Model Recovery*, 2018, full paper:
   https://arxiv.org/pdf/1803.00894
10. Melbourne and Roberto, *Quantitative form of Ball's cube slicing in R^n
    and equality cases in the min-entropy power inequality*, Theorem 1:
    https://arxiv.org/pdf/2109.03946
    The original Ball DOI endpoint failed; the theorem and its precise
    all-hyperplane form were checked in this primary research article.
11. Macedo and Bueno, *Inexact Adjoint Gradients and Directional Tolerances for
    Full-Potential Airfoil Optimization*, 2026, v1:
    https://arxiv.org/html/2605.17599v1
12. Potapczynski, Finzi, Pleiss and Wilson, *CoLA*, 2023, v2:
    https://arxiv.org/html/2309.03060v2
13. Novikov et al., *AlphaEvolve*, 2025, section 2.1:
    https://arxiv.org/html/2506.13131v1
14. SciPy `linprog` documentation (the executed version is recorded in JSON):
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html

Access failures did not block the construction. No inaccessible historical
code is represented as recovered, and no physical evidence is inferred from
these software calculations.
