# Exact identification is linear in treewidth; uniform stable recovery is quadratic

**Astra PRO 2, 22 October 2026, Australia/Brisbane.**

The selected five-query question is settled negatively for every real dense
design: six directions are necessary and sufficient on the stated trees of
fan blocks. The obstruction already appears with one attachment generation.
The argument then yields a broader sharp theorem.

## Principal result

For known symmetric support of treewidth at most t, with every diagonal free,
query row norm at most one across the ENTIRE block, and arbitrary absolute
Frobenius action error, the worst-case query minima are

| Task | Minimum |
|---|---:|
| Exact identification | t+1 |
| Dimension-independent uniform operator-error recovery | (t+1)(t+2)/2 |

The lower count permits arbitrary graph-adapted real dense query directions
and nonlinear decoders. The matching positive operation is the classical
star-color/direct-read construction; it gives the stronger Frobenius output
bound sqrt(2)||E||_F. The novelty candidate is the all-dense robust lower
bound and its compositional mechanism, not the coloring algorithm or the
clique/path/recursive-attachment architectural precedent. Historical
originality remains unestablished by the bounded primary-literature search.

For fixed t and every target R, the proof constructs a graph BEFORE the query
design such that EVERY (K_t-1)-column capped X has a supported D with
||D||_2>=1 and ||DX||_F<=1/R. The hard graphs can be chordal and, for t>=2,
have diameter at most four. Their degree grows. The proof does not establish
the same threshold under bounded maximum degree or a fixed-input randomized
minimax convention.

## The new operations

**Coning with cancellation.** Take k+1 disjoint copies of a k-query bad graph
and add one universal apex. Project the queries off its row, obtain one small
action witness per copy, and choose k+1 scalar coefficients to satisfy k apex
action constraints. A support-preserving lift has exactly zero apex action.
This raises the bad query count and treewidth by one; no inverse-apex or lift
norm enters the action estimate.

**Covariance branching.** At each attachment vertex, collect all child query
rows into a small Gram matrix. Either its h-th eigenvalue is small, in which
case one child is close to a rank-h query block and the inherited obstruction
survives an explicit input-error allowance; or its h-th eigenvalue is large.
In the latter case, a core matrix has too few remaining projected equations,
and many small child spokes cancel its action. The leftover action is small
while the core remains a principal submatrix of the full perturbation.

The child must be a cone: every nonanchor vertex must be an actual neighbor
of its anchor. Dropping that condition introduces forbidden entries. The
coning operation pays for exactly that missing condition.

Induction starts at a singleton with zero queries, so the principal lower
theorem is self-contained. The explicit root has one more symmetric
coefficient than imposed equations at every level. PROOF.md contains all
quantifiers, singular cases, normalization, support and size arguments.

## Receiving use on the original fan-tree frontier

A root fan F_6 has18 symmetric coefficients. Attach N child fans F_M at each
of its six path vertices, identifying only the apex. For five queries the
high-rank case imposes at most5+6*2=17 constraints. The low-rank case uses the
accepted three-query fan theorem. Setting N=M=k>=4 gives

    C_2(G_k,X) >= k^(1/4)/(sqrt(3*pi)+sqrt(3)),
    n=7+6k^2,

for EVERY capped five-column X. Thus the original SIX-query comparator is
sharp even on this shallow outerplanar subfamily. This quantitative statement
has an inherited fan-proof dependency; the general treewidth induction does
not. The old sine theorem and weaker executable tent bound stay separate.

## Actual exact source and witnesses

All new numerical/exact work uses standard-library Python Fraction arithmetic.
No floating success flag, precision tuning, eigensolver or optimization sweep
is an acceptance condition.

| Frozen witness | n | q | Exact certificate |
|---|---:|---:|---|
| core_t2_narrow | 295 | 5 | inverse ratio squared >=96 |
| core_t2_large | 9223 | 5 | action squared1/3072, operator norm>=1 |
| core_t3 | 1651 | 9 | exact69-rank constraint/cancellation witness |
| cone_three_copies | 37 | 3 | exact rank2 mixing, zero apex action |
| low_projection_actual_input | 1159 | 5 | nonzero input-error action included exactly |

The largest certificate gives inverse ratio at least **32sqrt(3)**. Its
18-variable/17-rank core is verified independently. The t3 fixture checks
70 variables against rank69. These are fixed-design certificates, not finite
proofs of the all-design theorem or estimates of its optimal divergence.

The low-projection fixture has exact squared query perturbation
384000000/1000002000001. Its perturbation action is nonzero and is included
in the saved actual-input action; no separately projected/rounded input is
silently substituted.

checks/verify_new_witnesses.py imports no producer code. It checked all five
fixtures, canonical input hashes, every support position and action entry,
row caps, projections, Gram identities, ranks, lifts, cancellation and ratios.
Four deliberate corruptions were rejected for their intended mathematical
reasons. Two scoped contributors independently checked the load-bearing
analytic lemmas and written induction; their exact scopes are retained.

The classical comparator is also executable: src/classical_star.py constructs
a perfect-elimination order for the chordal fixtures, validates it, implements
the established first/second-out-neighborhood coloring, validates isolated
readings, and decodes. On the9223-vertex support it uses six queries and passes
exact recovery plus arbitrary deterministic action-noise checking. The1651
vertex t3 fixture needs only eight colors under this implementation; it is
not itself a universal ten-query-hard graph. This underscores the difference
between a bad saved design and a worst-case graph-class lower theorem.

## Failures and limitations that govern continuation

The natural recursive orthogonal-frame design isolates diagonals and spokes
but is globally unstable. Child spokes can collectively cancel a parent path
edge; the failure occurs for every local frame rotation within that ansatz.
Protecting three parent functionals instead leaves too few dimensions for
long child fans. Both attempts are retained, rather than rebranded as the
all-design lower proof. Earlier fixed-palette and all-aggregate local-unmixing
failures remain unchanged in the previous archive.

The universal induction's explicit graphs are very large. With conservative
integer constants n_2(1)=62,708,695. Those graphs were NOT materialized; only
their finite specification and exact size recurrence were evaluated. For
fixed t, sizes grow O_t(R^(4t)); neither rate nor constants are optimized.
The proof is structural knowledge, not an efficient witness search for all
real inputs and not a new application speedup.

Distinct new computation bodies total **2.062414066 seconds wall** and
**2.061733499 seconds CPU**, with peak RSS **44,331,008 bytes**. They exclude
imports where stated, source access, proof development, authoring, inference,
delivery and service overhead. These additional/unknown costs are not zero.
Full receipts and a separate relocated receiving replay are supplied.

The original exact-decimal NIST dense incumbent remains1.675848413 seconds
before shared input conversion, width9/1074. No original NIST, scalar-moment,
eigensolver or molecular calculation was replayed, and no matched performance
gain is claimed. The closed molecular campaign and other owners' programmes
remain intact. The complete unchanged Cycle2 owner ZIP is in sources/.

## Chosen next question

Unbounded branching is now a proved source of the worst-case triangular
budget. I will next determine whether FOUR graph-adapted directions give a
uniform inverse on all treewidth-two graphs with maximum degree at most four.
The accepted squared-path theorem excludes three in this bounded-degree class.
Five suffice by distance-two coloring plus a fixed full-spark finite palette
and rowwise recovery. Thus the question has a precise4/5 boundary, and removes
the large-degree mechanism that settled the present fan-tree problem.

The first obligation is a global frame/decoder estimate, or a bounded-degree
all-design witness. Neither a local rank flag nor another compressed periodic
palette alone would decide it. This continuation is not a precision sweep,
another original-input benchmark or a return to the settled five-fan question.
