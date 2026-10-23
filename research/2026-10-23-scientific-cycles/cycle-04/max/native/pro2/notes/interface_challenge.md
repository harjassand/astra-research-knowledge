# Interface challenge: local stability does not glue; aggregate-Gram amplification

Contributor: `/root/interface_challenge`, 22 October 2026 Australia/Brisbane.
Scope: one load-bearing interface obligation for the owner's five-query
fan-tree programme. This is a source-complete mathematical challenge and
review, not another complete programme, a historical-priority review, or a
replay of the original NIST/molecular calculations.

The root and this contributor independently reached the same covariance
dichotomy in messages that crossed. Root's first presentation used an inverse
constant inequality; the direct threshold version below is simpler. The
general treewidth-t specialization was proposed by root and algebraically
checked here. This is internal, full-context review, not a blind external
acceptance.

## 1. Exact model

For a known graph G, S_G is the real symmetric support space with every
diagonal free. X has q real columns and every row has total norm at most one.
The relevant inverse constant is

    C2(G,X) = sup_{0 != D in S_G} ||D||2 / ||DX||F,

with infinity for a nonzero kernel. Matrices may use only a subset of allowed
edges. The noise convention is absolute Frobenius norm of the whole action.
The counterexamples below concern this operator/Frobenius ratio, not merely
Frobenius output error.

## 2. Concrete failure of naive stable-block gluing

Take a root triangle fan with apex a and path vertices u,v. Set

    x_a=e3, x_u=e1, x_v=e2,

and pad with two zero coordinates to obtain five query columns. At u attach
N triangle fans, each with path rows e2,e3. At v attach N triangle fans, each
with path rows e1,e3. All new vertices are distinct. Every block has three
orthonormal query rows; each arises by an orthogonal rotation of the same
local template sending its apex row to the prescribed shared row.

For an isolated triangle whose apex diagonal belongs to its parent block,
the two nonapex action rows recover both nonapex diagonals, both spokes and
the path edge. These are isolated coordinate readings. Selecting one path-
edge reading gives Frobenius recovery error at most sqrt(2) times local
action error, even when the apex action row is discarded. Thus the proposed
local premise genuinely holds for every block.

Now define D by

* D_uv=D_vu=1;
* on the u-to-e2 spoke of every u-child, put -1/N;
* on the v-to-e1 spoke of every v-child, put -1/N;
* set every other allowed entry, including all diagonals, to zero.

The actions at a,u,v are exactly zero. Each of the 2N selected child path
rows has action of norm 1/N; every remaining row has action zero. Hence

    ||DX||F^2 = 2/N,        ||D||2 >= |D_uv| = 1,
    C2(G,X) >= sqrt(N/2).

There are 3+4N vertices and 3+6N edges. The instability already occurs with
one attachment level, so recursive depth is not required. It comes from
coherent cancellation at both endpoints of a core edge, with the necessary
residual spread over many child blocks.

This disproves the claimed implication from uniformly stable local blocks,
orthogonal frame matching and apex-row omission to a uniform global inverse.
It is only a bad gluing/design, not an all-design five-query impossibility.
The latter requires the additional argument below.

The exact script `checks/check_interface_challenge.py` checks the support,
orthonormal rows in every local block, action cancellation and rational ratio
for N=1,2,8,64,256. It is supplementary to the proof.

## 3. What would make a local-gluing proof valid

Assign every diagonal to the block where its vertex first appears. Edges
belong to unique blocks. Use coefficient coordinates with each off-diagonal
weighted by sqrt(2), so the coefficient Euclidean norm equals global matrix
Frobenius norm. Assign each measured row to the block where that vertex first
appears as a nonapex vertex (and include the root apex at the root).

The action map then has a block-triangular form

    y = B theta + C theta,

where B is block diagonal, and C sends a child's coefficients into the data
row of its apex in the parent block. If L=diag(L_b) is a uniformly bounded
local left inverse, LB=I, set T=LC. The natural exact decoder is

    theta_hat = (I+T)^(-1) L y.

The strictly triangular T is nilpotent for each finite graph, so exact
identification follows. It does not follow that the inverse norms are
uniform in depth or branching. Sufficient conditions include ||T||<=rho<1,
which gives ||(I+T)^(-1)L||<=||L||/(1-rho), or a corresponding uniform
summability bound on the powers T^k. Orthogonal annihilation of every child
port contribution by the selected parent functionals gives the especially
simple case T=0.

At a vertex with many children, a scalar selected parent functional ell sees
the aggregate sum_j ell C_j theta_j. Its norm on the orthogonal direct sum
of child coefficient spaces is exactly

    (sum_j ||ell C_j||^2)^(1/2).

Thus an individual interface norm bound is insufficient: multiplicity can
produce sqrt(number of children). This is a necessary condition for a
uniform norm bound on this proposed feedback operator, not a claim that
every conceivable global decoder must use a contracting triangular split.
The explicit family above shows that the risk can be a true operator
instability, rather than only an overly pessimistic Frobenius estimate.

## 4. General cone-port amplification lemma

This is the decisive all-design replacement for the bad-frame example.

### Hypotheses

Let H be a finite graph with a distinguished anchor h adjacent to EVERY
other vertex of H. Suppose every real r-column capped query on H admits a
supported symmetric D with ||D||2=1 and action norm at most a. Equivalently,
the all-design inverse constant on H is at least 1/a, with the usual zero-
action interpretation when a=0.

Let R be a root graph with its vertices partitioned into protected vertices
A and port vertices P. Fix q>=r and suppose

    dim S_R > q*|A| + (q-r)*|P|.                         (4.1)

At every port v attach N disjoint copies of H by identifying only h with v.
Write G for the resulting graph, n0=|V(R)|. All nonanchor vertices of the
copies are distinct. This is a one-vertex gluing, not an edge or clique sum.

Then for every capped q-column X and every L>0,

    C2(G,X) >= min{
        1/[a + sqrt((q-r+1)*L/N)], sqrt(L/n0)}.          (4.2)

The independent diagonal bound C2>=1 may also be included. The cone
hypothesis is essential to the proof: the cancellation below places spokes
from v to arbitrary nonanchor vertices of its attached copies.

### Low aggregate-rank case

At port v stack all nonanchor query rows from its N copies into W_v and put
A_v=W_v^T W_v. Let eigenvalues be in descending order. If some port satisfies
lambda_r(A_v)<=L, project onto the top r-1 eigenspace U. The sum of squared
residuals is

    tr((I-P_U)A_v) <= (q-r+1)L.

Consequently one child has nonanchor residual squared at most
(q-r+1)L/N. Project all rows of this child onto span(U,x_v). This span has
dimension at most r, contains its anchor query exactly, and orthogonal
projection preserves every row cap. It reduces, rather than increases, the
selected residual. Identify the span isometrically with at most r coordinates
and pad by zeros if necessary.

By the child hypothesis choose ||D_H||2=1 with projected action norm<=a.
For the original queries,

    ||D_H X_H||F
      <= ||D_H X_H_projected||F + ||D_H||2 ||X_H-X_H_projected||F
      <= a + sqrt((q-r+1)L/N).

Embedding D_H into G by setting all other coefficients to zero preserves its
operator norm and support; rows outside the child have zero action. The
shared anchor introduces no uncharged row because it is included in H.
This proves the first alternative in (4.2).

### High aggregate-rank case

Otherwise, at every port lambda_r(A_v)>L. Let U_v be its top r-dimensional
eigenspace. Choose a root-supported symmetric B subject to

    (B X_R)_a=0 for every a in A;
    (B X_R)_v belongs to U_v for every v in P.

There are at most q|A|+(q-r)|P| linear scalar constraints. Hypothesis (4.1)
gives a nonzero B. Normalize ||B||2=1. Set w_v=(B X_R)_v. Its action satisfies

    sum_{v in P} ||w_v||^2 = ||B X_R||F^2 <= ||X_R||F^2 <= n0.

For each v choose spoke coefficients beta_v satisfying

    W_v^T beta_v = -w_v.

The minimum-norm choice is beta_v=-W_v A_v^+ w_v, where A_v^+ is the
Moore-Penrose inverse. Since w_v belongs to U_v and eigenvalues there exceed
L,

    ||beta_v||^2 = w_v^T A_v^+ w_v <= ||w_v||^2/L.

Put these values on the v-to-nonanchor spokes and their symmetric entries,
leaving all other child entries zero. These are actual allowed graph edges
because every child is a cone at its anchor. The root action is now exactly
zero. At a nonanchor vertex i in a child at v, the only remaining action is
beta_i*x_v, so the total action squared is bounded by

    sum_v ||x_v||^2 ||beta_v||^2 <= sum_v ||beta_v||^2 <= n0/L.

The resulting D retains B as a principal block. Therefore ||D||2>=1 and
C2(G,X)>=sqrt(L/n0). This proves the second alternative and the lemma.

### Degeneracies and quantifiers checked

* X was arbitrary and the graph was fixed before X. No common palette or
  full-rank query-row assumption is made.
* If a global or child action kernel exists, the stated lower bounds are
  already satisfied. Compactness of the finite-dimensional supported
  operator-unit sphere justifies selecting a norm-one child witness from
  an inverse lower bound; no sup-attainment gap remains.
* Eigenvalue multiplicities cause no issue: choose any appropriate invariant
  eigenspace. The high branch has lambda_r>L>0 before pseudoinversion.
* Low-rank projections are exact real mathematical operations. A floating
  eigensolver success flag is not a certificate for a numerical execution.
* The support dimension counts include all free diagonals. Removing those
  freedoms could invalidate both the core count and the child hypothesis.
* Operator normalization and the full Frobenius query/action bridge are paid.
  No operator/Frobenius dimension conversion is silently omitted.

## 5. Application to the selected five-query fan-tree question

Use H=F_M, M>=4, anchored at its apex. The accepted all-design three-query
fan theorem gives

    r=3,     a=sqrt(3*pi)*M^(-1/4).

Its complete source, including singular cases and the capped-row argument,
was reread in the unchanged prior archive at
`incoming/tw2/arm_b/RESULT.txt`. The existing theorem is a dependency, not a
new numerical calculation in this task.

Use R=F_6. Its protected set is its one apex and its ports are its six path
vertices. There are seven vertices, eleven edges and eighteen free symmetric
coefficients. At q=5 the constraints number at most 5+2*6=17. Thus (4.1)
holds. The graph has two fan levels: a root fan and N child fans at each of
its six path vertices. It lies exactly in the owner's selected family.

For arbitrary N>=1, M>=4, L>0,

    C2(G,X) >= min{
       1/[sqrt(3*pi)*M^(-1/4)+sqrt(3L/N)], sqrt(L/7)}.

Set N=M=k and L=sqrt(k). Then every capped real five-column design has

    C2(G_k,X) >= k^(1/4)/(sqrt(3*pi)+sqrt(3)),
    |V(G_k)| = 7+6k^2.

The high-case constant 1/sqrt(7) is larger than the displayed common
constant, so no branch is discarded. Taking the maximum with one preserves
the elementary diagonal bound. The rate is not claimed sharp.

Hence five queries cannot have a uniform operator-error guarantee, even at
this bounded attachment depth. This lower result plus the established six-
query upper comparator settles the selected family's minimum at six. The
maximum degree grows; no bounded-degree five-query exclusion follows.

The first naive-gluing counterexample was insufficient for that conclusion.
The covariance dichotomy changes the quantifier to every dense graph-adapted
design and is the substantive new argument.

## 6. Review of root's treewidth-t generalization

Root proposed the following broader specialization of the same lemma. Let
t>=2, q=2t+1, r=t+1. Use the cone child

    H=K_(t-1) join P_M,

with one of its clique vertices as anchor. The inherited separator theorem
with s=t-1 gives

    a_t(M)=sqrt((2t-1)*pi)*M^(-1/4),   M>=2t.

Every nonanchor vertex is an actual anchor neighbor. The root graph has
the same form K_(t-1) join P_m0, with protected clique and port path, where

    m0=t(3t-1)/2+1,    n0=m0+t-1=t(3t+1)/2.

I checked the full dimension count:

    dim S_R = (t+1)m0 + t(t-1)/2 - 1;
    number of constraints <= (2t+1)(t-1) + t*m0;
    difference = m0 - t(3t-1)/2 = 1.

The low-case tail after the top t eigenspace has q-t=t+1 eigenvalues, giving
residual squared <=(t+1)L/N in the chosen child. The high-case action squared
is at most n0/L. Thus

    C2(G,X) >= min{
      1/[a_t(M)+sqrt((t+1)L/N)], sqrt(L/n0)}.

For N=M and L=sqrt(M), this diverges as M^(1/4), with a positive t-dependent
constant. The glued graph has treewidth exactly t: every component has bags
of size t+1, and joining bags containing each shared anchor yields a valid
width-t decomposition; the root already contains a clique of size t+1.

Therefore, conditional on the inherited separator theorem, the reviewed
argument gives a uniform stable query lower requirement of 2t+2 over all
treewidth-t supports. Only t=2 matches the stated six-query upper bound;
for t>=3 it is a lower bound, not a sharp query characterization.

### Why this cannot be iterated indiscriminately

The new two-level fan graph is NOT a cone at its root apex: the root apex is
not adjacent to child path vertices. It therefore cannot automatically be
used as a child H in another amplification round. The cancellation would
create forbidden edges. Likewise t=1 is excluded above because K_0 join P_M
has no universal clique anchor. Forgetting this hypothesis would falsely
contradict established forest or treewidth-two upper bounds.

## 7. Costs and acceptance scope

One exact supplementary checker invocation passed. Body timings are stored
in `results/interface_challenge_checks.json`:

* wall 0.010813078995852266 seconds;
* CPU 0.010811112000000001 seconds;
* peak RSS 10,878,976 bytes.

It checked five fixed-design counterexamples and the small root dimension
count. It did not numerically verify universal eigenvalue branches or the
old fan theorem, and no such claim is made. The universal conclusions are
analytic proofs above.

The prior finite-palette note and received fan proof were read locally. No
web search, package installation, optimization, precision sweep, new platform,
paid compute, original benchmark replay, or historical numerical simulation
occurred. Tool/service overhead, model inference, proof construction and
authoring are additional unmetered costs, not zero. This scoped investigation
ran concurrently with the root's work; its timing must not be added as a
serial wall-time claim.

Internal mathematical conclusion: the cone-port argument passes the checks
specified here, conditional on the inherited all-design child theorem.
Historical novelty is not assessed. Practical operator-acquisition or
spectral-computation advantage is not claimed.

## 8. Subsequent checked induction toward the sharp general treewidth budget

After the preceding note was communicated, root proposed a stronger induction.
This section records the distinct review obligation checked here: dimensions,
gluing/treewidth, quantifiers and graph-size parameters. Root assigned the
new coning lemma itself to another contributor. Thus the conclusion in this
section is conditional on that coning lemma as well as the established upper
bound; it does not pretend this section alone supplies all dependencies.

### The separately checked coning input

The proposed coning lemma says: if a graph H defeats every k-column capped
design with a norm-one supported witness having action at most delta, then
the graph consisting of k+1 disjoint copies of H and ONE new vertex universal
to all of them defeats every (k+1)-column capped design with action at most
sqrt(k+1)*delta after operator normalization. Its graph has treewidth at most
tw(H)+1 and is an actual cone.

Root's mechanism projects off the new apex query, chooses one bad witness
per copy, and uses k+1 coefficients to solve k apex-action constraints before
the support-preserving lift. This differs from falsely declaring the previous
vertex-sum graph to be a cone: the newly added universal edges really exist.

### Induction parameters checked

Put K_t=binom(t+2,2). Assume at treewidth t-1 there are arbitrarily bad
(K_(t-1)-1)-query graphs. Cone them by the lemma. This supplies bad h-query
cone children of treewidth at most t, where

    h=K_(t-1)=t(t+1)/2.

Set the target query count

    q=h+t=t(t+3)/2=K_t-1.

Use a root graph K_(t-1) join P_m with its clique protected and its path as
ports. Choose

    m=q(t-1)-t(t-1)/2+2=t(t-1)(t+2)/2+2,
    n0=m+t-1=1+t^2(t+1)/2.

The root support dimension is (t+1)m+t(t-1)/2-1. Its constraint count for
the cone-port lemma is at most q(t-1)+(q-h)m=q(t-1)+tm. Their difference is
exactly one. Therefore the core exists for every query design, even when
constraints are dependent. The low-case covariance tail has q-h+1=t+1
eigenvalues. No other dimension factor is hidden.

For desired sensitivity R>=1, take child action allowance at most 1/(2R),

    L=n0*R^2,       N>=4(t+1)*L*R^2.

The high branch has action <=sqrt(n0/L)=1/R. The low branch has action at
most 1/(2R)+sqrt((t+1)L/N)<=1/R. Both have a supported witness whose
operator norm is at least one before normalization. This gives an arbitrary
badness factor R at query count K_t-1.

The graph is selected BEFORE seeing X: first use the induction hypothesis
to select one child cone meeting the requested uniform action allowance,
then fix L,N and construct the root and its copies. The arbitrary X is
introduced only after this fixed graph exists. Thus no uniformity in X is
lost by the graph depending on R and t.

Coning adds the new apex to every bag of a width-(t-1) decomposition, giving
width at most t. Every later attachment is at one vertex; connecting a child
bag containing its anchor to a root bag containing that vertex gives a valid
width-t decomposition. The root clique on its protected vertices and two
adjacent path vertices has size t+1, so the resulting treewidth is exactly t.

Conditional on coning, this induction proves the lower requirement K_t.
The established K_t-color star construction gives a uniform direct decoder
with Frobenius (therefore operator) noise factor sqrt(2), so it would match
the stronger all-design operator lower bound. Exact identification only
needs t+1 columns by degeneracy peeling, with the matching clique lower
bound. No conditioning is asserted for that exact-algebra argument.

### A self-contained starting point is available

One need not invoke the quantitative fan lower theorem for this general
induction. At t=0 take a one-vertex graph, K_0=1, and zero query columns:
the diagonal matrix [1] has unit norm and exactly zero action. Coning with
k=0 produces an edge which has a nonzero kernel for every one-column query.
The t=1 root above is an edge (m=n0=2); attaching these edge children at both
ends gives a double star. The same cone-port dichotomy then supplies the
two-query forest lower bound. All later steps proceed as above.

This does not erase the received fan proof: that proof supplies the separate
quantitative obstruction on the specifically selected shallow fan-tree
family in Section 5. The general treewidth induction can have a different,
self-contained dependency chain.

### Explicit integer size parameters and cost limit

For integer R>=1, choose a preceding bad graph at sensitivity 2hR. The
coning allowance is then sqrt(h)/(2hR)<=1/(2R). Set the integer

    N=4(t+1)n0 R^4.

If n_t(R) denotes the number of vertices in this conservative recursive
family, then

    n_0(R)=1,
    n_t(R)=n0 + m*N*h*n_(t-1)(2hR).

Indeed each child cone has 1+h*n_(t-1)(2hR) vertices; its anchor is identified
with a root port, and there are m*N copies. For fixed t this gives
n_t(R)=O_t(R^(4t)), hence a corresponding positive t-dependent
n^(1/(4t)) lower scale along the constructed sequence. No sharp rate follows.

The constants are very large. These exact formulas already give
n_1(6)=41,474 and n_2(1)=62,708,695. This is a symbolic explicit graph family,
not a performed materialization or an efficient finite-size certificate.
No such large graph was constructed in this scoped task. A practical or
bit-complexity claim would require its own implementation and accounting.

Review status for this section: the algebra, graph support/decomposition,
quantifiers and size recurrence pass this contributor's checks. Acceptance
of the full sharp theorem still requires the separately assigned coning
lemma and exact statement of the classical star-color upper theorem.
No additional program was run for this section; its proof/review/authoring
cost remains unmetered additional work.

## 9. Final focused composition review of the owner's written PROOF.md

At root's request this contributor read the complete written proof, focusing
on the new self-contained base, final integer parameterization, structural
claims and adaptivity scope. The following checks supplement, rather than
repeat, the earlier local cone-port review.

### Checks that pass

1. **Zero-query base.** G_0(R) is one vertex. Its matrix [1] has operator
   norm one and zero action against the unique one-by-zero query block.
   The k=0 coning step has one coefficient and zero apex constraints; it
   is meaningful and produces the one-query edge kernel. The apex-row-zero
   case is separately handled. No earlier path lower theorem is required.

2. **Graph chosen before the query.** For integer R>=1, h,m,n0,L,N and the
   recursive argument 2hR are positive integers (L>0), all determined before
   X. The induction hypothesis selects a graph bad for every query, so using
   it as a child does not exchange an existential graph quantifier with the
   arbitrary-design quantifier. Covariance spaces and witnesses may then
   legitimately depend on the subsequently fixed X.

3. **Constants.** Coning h copies gives allowance sqrt(h)/(2hR)<=1/(2R).
   The covariance tail dimension is t+1. With L=n0 R^2 and
   N=4(t+1)n0 R^4, its low-branch residual is exactly 1/(2R), while the
   high-branch action bound is exactly 1/R. Operator normalization can only
   decrease these action bounds. The root dimension surplus is exactly one.

4. **Vertex recurrence.** A child cone has 1+h*n_(t-1)(2hR) vertices.
   Identifying its apex adds exactly h*n_(t-1)(2hR) new vertices. There are
   mN children, so the displayed recurrence counts every vertex once. It
   implies O_t(R^(4t)) at fixed t. The explicit n_1(1)=34 and
   n_2(1)=62,708,695 agree with that recurrence.

5. **Chordality.** Paths are chordal. Adding a universal vertex to a chordal
   graph cannot introduce an induced cycle of length at least four: a cycle
   containing the new vertex has chords, while one avoiding it was already
   present. A clique join is repeated universal addition. Disjoint unions
   preserve chordality, and a simple cycle cannot traverse two components of
   a one-vertex sum without revisiting the shared vertex. The induction's
   chordal claim therefore follows directly from its actual operations.

6. **Bounded diameter.** For t>=2 the root clique is nonempty, so any two
   root path ports are at distance at most two. Every added vertex, including
   vertices deep in a recursively specified copy, is adjacent to its NEW
   universal anchor at the root port. Thus any two added vertices have a
   route of length at most 1+2+1=4. Root protected vertices are no farther
   away. For t=1 the children are edges and the graph is a double star, of
   diameter at most three. Large degree is permitted and explicitly stated.

7. **Exact versus stable queries.** The exact t+1 argument uses degeneracy
   peeling and a row-full-spark block, while the matching lower count uses a
   clique of size t+1. It does not assume or prove conditioning. The stable
   lower count concerns operator output and the established upper decoder
   gives the stronger Frobenius bound, so these guarantees are matched.

8. **Deterministic adaptivity.** For a fixed graph and deterministic algorithm,
   the noiseless-zero transcript fixes X before selecting the adverse D.
   Running D with successive errors -Dx_j reproduces that transcript and
   hence the same queries. The combined error is -DX, with the same absolute
   Frobenius accounting; the row cap is the cap on the realized zero-transcript
   block. Noiseless exact recovery forces output zero there. This is valid
   for uniform adversarial-noise guarantees. The proof expressly avoids a
   fixed-input randomized claim or a full-entry-access restriction.

### Small written-contract clarifications requested

No theorem deletion, changed constant or substantive construction repair is
required. Four statement clarifications were sent to root before archiving:

* Lemma 2 should explicitly say q>=h>=1; h=0 is valid elsewhere but its
  lambda_h and top-(h-1) expressions are not defined in this lemma.
* Replace "Choose t+1 full-spark row directions" by a precise n-by-(t+1)
  block whose every at most t+1 rows are independent, then scale individual
  rows. Reusing only t+1 row labels would not support the peeling proof.
* Restrict the n^(1/(4t)) lower-rate sentence to t>=1; t=0 is the separate
  fixed one-vertex, zero-query kernel case.
* The construction is defined for integer R. State that real R>=1 in the
  opening theorem is handled by G_t(ceil R), or state the theorem's lower
  bullet for integer R. The existence conclusion already follows either way.

Verdict: the final composition passes the mathematical checks above, subject
to these small statement clarifications and the separately reviewed classical
upper theorem/coning proof. No new numerical checker was run because the
remaining obligations are symbolic and the needed operations were inspected
directly. Review and authoring cost are additional unmetered work.
