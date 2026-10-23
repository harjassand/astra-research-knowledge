# A sharp stable query budget for graphs with a forest separator

**Astra PRO 2, 22 October 2026.** The former three-query question on all
treewidth-two supports is closed: both incoming all-design obstructions are
accepted within their exact norm and row-energy contract. This checkpoint
then develops a separator-based recovery theorem, an executable decoder,
and exact rational instability witnesses. The structural-inference programme
continues; the original NIST and molecular stopping decisions are preserved.

## Main result

Suppose the known symmetric support graph comes with a set S of at most s
vertices whose removal leaves a forest. All diagonal coefficients are free.
Every query row has total squared energy at most one, and action noise is
measured by the absolute Frobenius norm of the whole query block.

**For each fixed s, exactly s+3 queries are necessary and sufficient for a
dimension-independent operator-error guarantee over this graph class.**

| Question | Established result | Scope |
|---|---|---|
| Exact identification | Worst-case minimum s+2 queries | Does not control numerical stability |
| Uniformly stable recovery | Minimum s+3 queries | All graphs with the supplied forest separator |
| Explicit direct decoder | Frobenius error <=sqrt(2) times action noise | Arbitrary correlated, nonsymmetric action noise |
| Same decoder, operator error | <=sqrt(5/3) times action noise when S is nonempty | Sharp for this specified decoder over the class |
| No separator | Operator factor <=sqrt(3/2), with three forest queries | Sharp for the specified decoder, not every possible decoder |

The positive mechanism is classical star-color composition: give separator
vertices distinct coordinates and use three depth-modulo-three coordinates
on the remaining forest. The new lower-bound argument shows why the smaller
exact-identification budget cannot give a uniform noise bound, even with
arbitrary real dense query rows. Historical novelty is not claimed.

## The all-design obstruction

For G=K_s joined to a path on m vertices, any row-capped X with s+2 columns,
and m>=2s+2, the proof establishes

\[
 \sup_{D\in S_G\setminus\{0\}}\frac{\|D\|_2}{\|DX\|_F}
 \ge\max\left\{1,
 [2\sqrt{m-1}\sin((2s+1)\pi/(2m))]^{-1/2}\right\}
 \ge\max\left\{1,\frac{m^{1/4}}{\sqrt{(2s+1)\pi}}\right\}.
\]

The proof projects the path rows off the s separator rows, leaving a
two-dimensional quotient. A path-flow perturbation is chosen from 2s+1 slow
modes so that all 2s separator-action constraints vanish. Lifting this matrix
preserves the clique/path/border support and leaves exactly the small path
action. A separate local rank-one witness pays for arbitrarily short projected
rows. Dependent separator rows or dependent neighboring projected rows give
exact supported kernels and are handled before division.

This is a direct receiving use of the incoming fan construction, generalized
from one apex to an arbitrary fixed separator. The theorem is uniform over X;
finite examples do not supply that quantifier. It also rules out deterministic
adaptive recovery with a uniform adversarial-noise guarantee by following the
noiseless zero transcript. It does not prove a fixed-input randomized lower
bound or restrict algorithms allowed to read all matrix entries.

## Actual executable evidence

The positive operation is `src/separator_forest.py`. It accepts the graph and
separator, validates the forest complement, constructs the query coloring,
and recovers a sparse symmetric matrix by isolated readings. It averages the
two readings for edges inside S. Seven exact fixtures cover forests, absent
border edges, separator edges, and empty parts; six invalid inputs are rejected.
An exact attaining-noise example checks the sqrt(5/3) operator constant.

The negative operation is `src/separator_witness.py`. It replaces sine modes
by disjoint integer tents so that rational input X produces rational witnesses
without a floating eigensolver or a precision parameter. With
`h=floor(m/(2(2s+1)))>=1`, it separately guarantees

\[
 C_2(G,X)^4\ge h^2/[3(m-1)].
\]

This executable bound is not presented as the stronger sine bound. Five flow
fixtures and two exact-kernel fixtures are frozen with their exact X, D, input
identities and receipts. A separate Fraction verifier imports no producer code
and checks every support position, row norm, projection, flow, lift, action,
ratio, and claimed rational bound. Four deliberate corruptions are rejected.

### Largest new fixture

For s=2, m=4010, n=4012 and four query columns, every query row has norm one.
The independent checker proves

\[
 \|DX\|_F^2=24651/4,\qquad
 \|D\|_2^2\ge1447209,
\]

hence

\[
 \boxed{\|D\|_2/\|DX\|_F\ge\sqrt{643204/2739}
       =15.324219079547102\ldots.}
\]

The lower numerator is a certified path-entry bound, not a floating eigenvalue.
Dividing D by1203 gives a perturbation with operator norm at least one and
action norm at most sqrt(2739/643204). The saved constraint matrix has rank
three; the proof only requires that its rank is at most four.

This number is a sensitivity certificate for this exact fixed design, not an
optimal four-query factor or a measured performance improvement over the old
NIST calculation. The family-wide necessity comes from the all-size proof.

## Two failed compression routes change the continuation

First, compressing an arbitrary c-color star seed into q<c dense coordinates
cannot preserve uniform stability. A fixed colored forest containing one
replicated star for each possible pivot color forces amplification at least
sqrt(N/(c-1)) for **every** capped compressed palette. Repeated small leaf
coefficients cancel a large hub diagonal exactly. Recoloring the graph remains
possible; this is not a lower bound for all designs on forests.

Second, the attempted repair—use a star coloring whose every closed neighborhood
has at most five colors—fails on a 41-vertex outerplanar graph from the classical
sharp star-color construction. Every star coloring of this graph, even with
unlimited total colors, has a closed neighborhood with at least six colors.
Thus five-query rowwise reconstruction of all color aggregates cannot be the
general treewidth-two solution. Joint dense decoding remains outside this
obstruction. Complete proofs and exact supplementary checks are preserved.

## Costs, comparisons and limitations

The seven exact witness constructions took **1.716356064 seconds** body wall
time. Their independent verifier took **1.530646674 seconds**. Including all
distinct new numerical/exact checker bodies, the subtotal is
**3.298460537 seconds**, with maximum recorded peak RSS **31,256,576 bytes**.
These are computational scopes, not total research cost: proof development,
authoring, source reading, service/inference time, packaging and delivery are
additional. The unsuccessful methods and superseded preliminary checker are
charged; unknown monetary and energy costs are not set to zero.

The decoder requires s+3 actual operator actions. Graph traversal/recovery is
linear in the support representation in the abstract algorithm; the supplied
Python implementation additionally sorts the edge list for canonical output.
Explicitly materializing or retaining the full action block costs O(n(s+3)).
The separator is supplied, and its discovery is not hidden in the timing.
Fraction arithmetic has input-dependent bit costs. Error in the operator,
approximate support and floating averaging must be added as stated in PROOF.md.

The original exact-decimal n1074 NIST calculation is unchanged: verified dense
proposal plus verification took1.675848413 seconds before shared conversion,
with width9/1074. The earlier common completion took39.019276241 seconds plus
independent verification and did not improve that incumbent. No original
benchmark, scalar-moment calculation, or retired molecular optimization was
rerun in this checkpoint.

## Decision and chosen continuation

The fixed-separator question is settled by the matching construction and lower
bound. The result makes the distinction between exact and robust identification
precise for a family with arbitrarily large local degree and a fixed number of
global couplings. It supplies a reusable exact cancellation operation for
transporting slow witnesses through a separator.

General treewidth two still has the established six-query upper comparator;
the four/five/six boundary is not settled here. A bounded forest separator is
a stronger assumption than bounded treewidth. The next chosen question is
whether five graph-adapted directions can recover arbitrarily deep trees of
fan blocks with a uniform global noise bound. These graphs retain small local
interfaces while their forest-separator size can grow. The decisive obligation
is a global inverse estimate across all repeated interfaces, rather than local
rank or local aggregate unmixing. See CONTINUATION.txt for the precise family
and stopped routes.

The archive preserves the prior owner source byte for byte, both accepted
incoming obstruction arms and their reviews/costs, all new source, proof,
fixtures, failures and receipts. Delivery to the existing private Page is a
source handoff, not a claim that Max has read or scientifically integrated it.
