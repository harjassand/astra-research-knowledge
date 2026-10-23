# Cycle4 result: stable coordinate information and two four-query operations

The full question on treewidth<=2, maximum degree<=4 remains **four versus
five**. This checkpoint resolves a meaningful subfamily, gives an operation
on a branching subfamily, and identifies the exact stability obligation for
the proper-coordinate route. All claims retain known symmetric support,
free diagonals, total probe-row norm<=1, absolute Frobenius action noise and
operator recovery error.

## Strongest structural result

For a specified proper coordinate design X_i=e_c(i), exact recovery is possible
exactly when every bichromatic component is a tree. For such a design let K
be the largest component size, Delta the maximum degree, and r the largest
number of distinct neighbor colors at a vertex. For Delta>=1,

    max(1,sqrt((K-1)/(2Delta))) <= sup_D ||D||2/||DX||F
                    <= sqrt(1+r(K-1)).

The upper bound is achieved as a guarantee by an explicit linear decoder;
the lower is an exact indistinguishability witness valid also for nonlinear
estimators. Thus, with bounded degree, uniformly stable coordinate recovery
is equivalent to uniformly bounded bichromatic tree size. At fixed degree
the dependence is Theta(sqrt(K)). A cycle gives an exact nonzero kernel.

This is a representation-specific characterization. It does not show that
every permitted graph possesses a suitable four-coloring and does not lower
bound arbitrary graph-adapted dense real designs. The proof, exact cut flow,
linear-time decoder and a posteriori residual allowance are in PROOF.md.

## Positive operations and strongest comparisons

| Known support class | Queries | Guaranteed error <= C ||E||F | Status |
|---|---:|---:|---|
| Supplied bandwidth-two ordering | 4 | C=sqrt(3+sqrt5), also in Frobenius norm | Period-nine coordinate seed, exact O(n) decoder |
| Same bandwidth-two class | 5 | C=1, also in Frobenius norm | Stronger ordinary five-query isometry comparator |
| Known subgraph of T Cartesian-product K2, T any forest | 4 | C=sqrt2, also in Frobenius norm | Depth-period-four star-color seed, O(n+m) decoder |
| All treewidth-two, maximum-degree-four supports | 5 | Fixed palette-dependent constant | Inherited 17-color square/full-spark upper remains |

The accepted all-design three-query squared-path obstruction is embedded in
the unchanged predecessor. Combined with the first row, it establishes the
worst-case stable minimum **exactly four for bandwidth-two supports**. No
three-query lower for forest prisms is claimed.

For a binary tree T, its prism has maximum degree four and treewidth two,
but unbounded bandwidth as depth increases. The prism operation therefore
extends the positive result to genuinely branching geometry. It does not
resolve every partial2tree of maximum degree four.

Four saves one action on the banded class while having a worse guaranteed
error constant than five. Acquiring actions, finding/validating a supplied
representation, arithmetic error and downstream work all count. No original
NIST runtime, energy, physical inference or molecular improvement follows.

## Actual error mechanism on the same input graph

The exact stored fixture is the254-vertex prism of the complete binary tree
on127 vertices. A naive proper four-color seed is acyclic but leaves one
127-vertex bichromatic tree in each layer. The cut-flow witness has a63/64
split, an edge coefficient of absolute value one, and

    ||D X_bad||F^2 = 127/4032,
    inverse lower >= sqrt(4032/127) = 5.6345391556... .

The new four-query prism seed on exactly the same support and matrix gives

    ||D X_good||F^2 = 3167639/451584,

and has the all-input upper constant sqrt2. This is a concrete failure and
repair of a design. It is deliberately not presented as a graph hard for
every design.

The root's exact experiment also saves a61-vertex full bandwidth-two input,
an edge-deleted subsupport, the five-query comparator, arbitrary deterministic
noise and decoded outputs, and an alternating C4 kernel. All inputs and
coefficients are in results/coordinate_operations.json; no external dataset
or optimizer is needed for these mathematical receiving tests.

## What changed the accepted calculation

The first signed period-six construction successfully proved stable q4 on
squared paths, with constant about5.0413. The focused literature contributor
then supplied a period-nine coordinate construction with constant about2.2883.
That stronger operation became the main banded decoder and comparator. The
signed representation is retained as a possible non-coordinate continuation,
not promoted as the best current operation on that family.

The structural contributor's counterexample to a bounded-bandwidth shortcut
was a forest prism. The owner constructed and tested the depth-based four-query
decoder on that very family. This is a concrete receiving use that changes
which graph geometries are positively covered. It is not archive indexing
or a successful rerun presented as research amplification.

The new operator criterion also explains why ordinary acyclic or linear
coloring alone does not establish this task's stability. Prior sparse-Hessian
recovery and roundoff analyses are established; historical priority of the
new quantitative formulation and periods remains unassessed.

## Proof and verification status

- Full all-size arguments are in PROOF.md and the focused contributor notes.
- A separate reviewer checked the cut-flow lower, supplied the sharper operator
  upper, and checked the arbitrary-input/nonlinear-estimator extension.
- Another reviewer checked the forest-prism coloring and global noise estimate.
- The independent exact checker did not read or import producer code. It
  reconstructed saved actions, solved tiny incidence systems by Fraction
  Gauss-Jordan, and verified saved outputs, exact witnesses and fixed-graph
  all-noise inequalities by rational PSD tests. First run passed.
- Finite checking does not replace the all-size proofs. Internal review does
  not establish historical originality or external scientific acceptance.

Producer coordinate experiment body:0.080766077s. Independent check body:
0.052666758s. Including the signed construction, finite local-completion
construction and period check, recorded computation bodies sum to about
0.353133485s. These tiny exact checks exclude substantial proof development,
reading, failed structural approaches, source authoring, service/inference,
integration and delivery; unknown totals are explicit in COSTS.md.

## Continuation decision

Keep the original full four-versus-five question active. The next precise
constructive obligation is a uniform bounded-component acyclic four-coloring
for all degree-four partial2trees, starting with the composition of triangle
and square pieces across supplied size-two separators. A valid finite-state
composition invariant must bound component size through arbitrary depth.

If an obstruction rules out every such coloring on a family, it closes only
the coordinate representation. Return to the retained local-nullspace scalar
operator for arbitrary real rows; do not infer a universal q4 lower from a
palette failure. No precision sweep, larger fixture, q5-to-q6 relaxation or
change of the scientific target is selected by default.

The closed molecular, GUIDE and other historical operations stay preserved
inside the unchanged native source. Other programme ownership is unchanged.
