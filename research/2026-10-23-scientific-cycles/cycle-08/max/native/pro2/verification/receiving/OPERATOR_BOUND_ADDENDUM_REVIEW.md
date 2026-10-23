# Sharper operator bound: independent proof review

**Verdict: sound under the unchanged support, action, and noise contract.**
This is a source-informed mathematical review, not an additional numerical run.
The inherited Cycle2 `PROOF.md`, Section 2, was read in the preserved native
transport copy. Its forest mass-shifting argument uses only the absence of a
clique of order three. It therefore applies to every triangle-free support.
The following argument establishes the claimed transfer to the current
canonical least-squares operation.

## Exact hypotheses

Let `G` be a known finite simple triangle-free graph, with no restriction on
maximum degree. Let `c` be a supplied proper star coloring in `q` colors, and
let `X_i=e_{c(i)}`. Thus each row has total Euclidean norm one. The unknown
matrix `D` is arbitrary real symmetric with off-diagonal support contained in
`G` and arbitrary free diagonal. The full observation is `Y=DX+E`, with
arbitrary real noise measured in absolute Frobenius norm. All operators below
refer to this exact fixed graph and design.

## An isolated-cell left inverse

Every nontrivial bichromatic component is a star. For each edge choose its leaf
endpoint; for a one-edge component choose either endpoint deterministically.
Recover the edge coefficient from that endpoint's action cell in the other
endpoint's color. Read each diagonal from its own-color action cell, and output
zero at nonedges. Denote this linear map on the entire action space by `T`.

Each selected edge cell is isolated because the chosen leaf has exactly one
neighbor of that color. Selected edge cells are mutually distinct: two edges
could use the same vertex/color cell only if that vertex had two neighbors of
that color, contradicting the leaf condition. Properness also separates these
cells from every selected diagonal cell. Therefore `T(DX)=D` for every admitted
matrix, with no known coefficient or reduced-action assumption.

For any unit real vector `z`, set `w_i=z_i^2`. The squared Frobenius dual norm
of the scalar functional `E -> z^T T(E) z` is exactly

\[
 Q_G(w)=\sum_i w_i^2+4\sum_{\{i,j\}\in E(G)}w_iw_j,
 \qquad w_i\ge0,\quad\sum_iw_i=1.
\]

The coefficient four comes from copying one selected edge-cell error into both
symmetric matrix entries. Distinctness of all selected cells is essential to
this identity. Supremizing the scalar functional over `E` and `z` gives
`||T||_(F->op)^2 = max_w Q_G(w)`.

If two positive-weight vertices `u,v` are nonadjacent, keep `w_u+w_v` fixed and
move all other weights nowhere. As a function of `w_u`, the terms involving
these two weights have strictly positive quadratic coefficient: the two square
terms are convex and all edge interactions are linear, because `uv` is absent.
At least one endpoint of the allowed interval does not decrease `Q_G`. Move to
that endpoint, eliminating one positive weight. Repetition terminates after
finitely many steps with the positive support a clique. Since `G` is
triangle-free, this clique has at most two vertices. If its two masses are
`a,b`, with `a+b=1`, then

\[
 Q_G(w)=a^2+b^2+4ab=1+2ab\le\frac32.
\]

The one-vertex case gives one. Hence

\[
 \boxed{\|T(E)\|_{\rm op}\le\sqrt{3/2}\,\|E\|_F.}
\]

This direct-decoder norm is exactly `sqrt(3/2)` whenever `G` has an edge: equal
mass on the endpoints attains the quadratic maximum. That exactness statement
concerns `T`; it is not a sharpness claim for the least-squares inverse below.

## Transfer to the existing canonical least-squares inverse

Define the supported action map `A(D)=DX` and let `V=A(S_G)` be its range in the
full action space with its Frobenius inner product. Since `T A` is the identity,
`A` is injective. Let `Pi` be the Frobenius-orthogonal projection onto `V` and
let `R` be the canonical action least-squares inverse. For every action array
`Y`, `Pi Y` belongs to `V`, and its unique supported matrix preimage is both
`R(Y)` and `T(Pi Y)`. Therefore

\[
 R=T\Pi,\qquad
 \|R\|_{F\to\mathrm{op}}
 \le\|T\|_{F\to\mathrm{op}}\|\Pi\|_{F\to F}
 \le\sqrt{3/2}.
\]

In particular `R(DX+E)-D=R(E)`, so the already implemented canonical decoder
satisfies

\[
 \boxed{\|\widehat D-D\|_{\rm op}\le\sqrt{3/2}\,\|E\|_F.}
\]

Its separate Frobenius-output bound remains `sqrt(2)`. No changed decoding,
queries, action acquisition, noise model, or graph preparation is required.
The inequality for `R` can be strict; for a graph consisting of a single edge,
the least-squares inverse averages the two available edge readings and has a
smaller operator constant than the one-reading decoder. No optimality of the
new displayed least-squares bound is asserted for the current fixtures or class.

## Application and accounting

The current supplied grammar produces triangle-free graphs, and the checked
finite certificate supplies proper star-four colorings. Thus every admitted
grammar graph, including the three saved receiving inputs, satisfies the
hypotheses. The inherited three-query forest star coloring also satisfies them;
the sharper ordinary forest comparator must be retained. The Frobenius bound,
query count, and full original actions are unchanged.

The saved receiving JSON files still report the valid conservative operator
squared bound two. Their bytes, observed outputs, and recorded costs are not
modified by this proof strengthening. The new squared operator upper bound is
`3/2`, established by the argument above rather than another observed run.
There was no additional scientific execution, numerical test, timing trial,
or input change for this review. Mathematical reading, derivation, and authoring
costs are unknown and are not represented as zero.

The bound assumes exact `X` and exact stated observations. If actual query
assembly uses `X+deltaX`, its effect `D deltaX` must be included and bounded in
the action-error budget; the row cap alone does not pay that error. Any
approximate decoder or projection must also pay its numerical residual. This
addendum does not remove those existing obligations.

This is a transfer and extension of explicitly preserved mathematical capital,
with a receiving consequence for the current decoder. It does not establish
historical novelty, external acceptance, a four-query theorem for all
degree-four partial two-trees, or a practical speed advantage.
