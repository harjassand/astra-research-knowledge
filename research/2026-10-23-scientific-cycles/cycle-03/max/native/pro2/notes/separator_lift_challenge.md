# Focused challenge of the root's clique-separator/path lift

Reviewer: `/root/tw2_local_design`; 22 October 2026 Australia/Brisbane.
Scope: analytic check of the root's proposed `K_s join P_m` extension of the
incoming fan obstruction. This is not an independent whole construction,
external review, or historical novelty assessment. No numerical test is a
premise of this note.

## Reviewed statement

For an integer `s>=1`, `m>=2s+2`, graph `G=K_s join P_m`, and arbitrary real
`X` of shape `(s+m) by (s+2)` with every row norm at most one, define

`C_2(G,X)=sup_{0!=D in S_G} ||D||_2 / ||DX||_F`,

with infinity when the map has a supported nonzero kernel. The proposed bound

`C_2 >= max(1, [2 sqrt(m-1) sin((2s+1) pi/(2m))]^(-1/2))`

passes the load-bearing algebra and quantifier checks below. It implies the
weaker explicit bound `max(1,m^(1/4)/sqrt((2s+1) pi))`.

The conclusion is for each fixed `s` as `m` grows. It need not diverge when
`s` grows together with `m`; no such quantifier is claimed.

## 1. Exhaustive reductions

The apex rows form an `s by (s+2)` matrix. If they have row rank less than
`s`, a nonzero dependence vector `w` supported on the apex has `w^T X=0`.
Its rank-one matrix `ww^T` is supported entirely on the apex clique and
its diagonals, so the inverse constant is infinity. Thus no favorable
apex rank assumption is smuggled in.

Otherwise apply an orthogonal transformation in query-coordinate space,
which preserves all row norms and the measured Frobenius norm. Write

`X = [[0_(s by 2), T], [Z, U]]`,

where `T` is invertible `s by s`, `Z` has two columns and `U` has `s`
columns. Every quotient row `z_i` satisfies `||z_i||<=1`.

If adjacent rows `z_i,z_(i+1)` are dependent, the `s+2` rows consisting of
all apex rows and those two leaf rows are dependent. These vertices induce
a clique, so the same rank-one kernel construction is supported. Since
`m>=2`, this also handles zero quotient rows. It is therefore valid to
assume all adjacent determinants are nonzero and `delta=min_i||z_i||>0`.

## 2. Small-row witness is independent of apex conditioning

Fix leaf `i` and let `w` have that leaf entry one, all other leaf entries
zero, and apex row vector `-u_i^T T^(-1)`. Then

`w^T X=[z_i^T,0]`, `||w||>=1`.

The support of `ww^T` lies in the clique consisting of the apex plus leaf
`i`. Hence its inverse ratio is exactly `||w||/||z_i||>=1/||z_i||` and
`C_2>=1/delta`. No upper bound on `||T^(-1)||` is required. An ill-conditioned
apex block can only enlarge this particular ratio.

## 3. Path-flow representation and independent constraints

Let `c_0=c_m=0`. With the same orientation of the 90-degree rotation as in
the incoming fan argument, define the tridiagonal matrix `B(c)` by

`b_i=c_i/det(z_i,z_(i+1))`,

`a_i=-(b_(i-1)<z_i,z_(i-1)>+b_i<z_i,z_(i+1)>)/||z_i||^2`.

Then exactly

`(BZ)_i=(c_i-c_(i-1)) J z_i / ||z_i||^2`.

Thus `||BZ||_F<=delta^(-1)||Delta c||_2`, while
`||B||_2>=max_i |b_i|>=||c||_2/sqrt(m-1)`.
The determinant upper bound uses both projected row caps, not unit norms.
The target remains operator norm, with the `sqrt(m-1)` loss paid explicitly.

Choose the space of the first `2s+1` sine modes of the length-`m` Dirichlet
path. It has dimension `2s+1` because `m-1>=2s+1`, and every vector in it
satisfies

`||Delta c||_2<=2 sin((2s+1) pi/(2m)) ||c||_2`.

The map `c -> U^T B(c) Z` has `2s` real scalar output coordinates and is
linear in `c`. Rank-nullity therefore provides a nonzero vector satisfying
all these constraints exactly. No rank assumption on that constraint map
is needed, and no finite sampled set of designs replaces an all-X claim.

## 4. The cancellation is exact; no hidden lift factor

Set

`C=-T^(-T) U^T`, `L=[C;I_m]`, `D=L B(c) L^T`.

Then `L^T X=[Z,0]` and

`DX = [C BZ; BZ,0] = [0; BZ,0]`,

because `U^T BZ=0`. In particular `||DX||_F=||BZ||_F` exactly. A bound
involving `||L||`, `||U||` or `||T^(-1)||` would be both unnecessary and
potentially destructive; the construction avoids it by equality.

The leaf principal block of `D` is the tridiagonal `B`, so its leaf support
is the path. All introduced apex-leaf entries and apex-apex entries are
allowed because this is the complete join with an apex clique. Therefore
`D` is supported and `||D||_2>=||B||_2`. The nonzero flow cannot have zero
path derivative under the two endpoint conditions, so its action and its
matrix are both nonzero in the nondegenerate case.

This proves `C_2>=delta Q`, with
`Q=[2 sqrt(m-1) sin((2s+1)pi/(2m))]^(-1)`. Combining with `1/delta` gives
`C_2>=sqrt(Q)`. Since `delta<=1`, one also has `C_2>=1`.

## 5. Support/decoder/upper scope

Consecutive bags consisting of the `s` apex vertices and leaf pairs give
width `s+1`; an apex-plus-adjacent-pair clique gives equality. The graph has
`binom(s,2)+sm+(m-1)` edges, plus all allowed diagonals.

The simple upper uses `s+3` queries: give the apex distinct coordinate
rows, and give path vertices three periodic coordinate rows in disjoint
coordinates. Select one distinct action cell for every diagonal/edge;
apex-leaf edges are selected from leaf rows, leaf-path edges from either
isolated endpoint, and apex-apex edges from one endpoint. For arbitrary
unstructured action noise, copying symmetric off-diagonal coefficients
costs at most `sqrt(2)` in Frobenius norm, hence also in operator norm.
The upper extends to `K_s join F` for any forest `F` by the previously
proved depth-modulo-three seed. Construction/readout is
`O(s^2+sm+m)` for this family, in addition to `s+3` actual actions.

The lower rules out a smaller *fixed uniform* query budget on the family:
any budget at most `s+2` can be padded with zero columns without changing
row caps. It does not claim that every individual small graph needs `s+3`
for exact recovery. Generic full-spark rows plus endpoint peeling give
exact identification with `s+2`; fewer cannot identify the induced clique
of size `s+2`. This identifies the exact-versus-uniformly-stable separation.

## 6. Qualifications and cost

No defect was found in the proposed all-design lower statement. It is an
extension of the supplied fan proof, and should be described as reuse plus
a general separator constraint count, not as unrelated rediscovery.
The construction uses exact real arithmetic and trigonometric modes. A
stable bit-complexity bound for forming witnesses is not established by
this proof. Arbitrarily small determinants and a badly conditioned apex
block must not be hidden in an implementation claim.

No further tool calls, numerical experiments, or sources were needed for
this focused analytic challenge. Authoring/inference/energy/monetary costs
were not separately metered; they are not zero. The separate local-color
obstruction note contains its own measured source/check costs.
