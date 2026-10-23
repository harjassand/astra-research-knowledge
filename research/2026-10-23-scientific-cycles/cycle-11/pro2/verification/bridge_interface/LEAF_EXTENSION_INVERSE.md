# Uniform inverse for pendant extensions of stable tree cores

Independent bounded proof contribution, Pro2 Cycle11, 23 October 2026.
This argument concerns the actual bichromatic trees supplied by the module
quotient lemma. It uses the ordinary unweighted Euclidean norm and the full
original actions. No probability or normalization of the action error is used.

## 1. The extension lemma

Let T be a finite connected tree with at least two vertices. Suppose

    sum_v (x_v - mean_T(x))^2 <= beta sum_uv in E(T) (x_u-x_v)^2

for all real x, with beta>=1. Form T+ by attaching at most a>=0 new pendant
vertices to each ORIGINAL vertex of T. Attachments to new vertices are not
allowed in this lemma. Then T+ has Poincare constant at most

    L = ((a+1)beta + 1
         + sqrt(((a+1)beta-1)^2 + 4a beta))/2.

This holds uniformly in the order of T and in the actual number of leaves.
It does not follow merely from a bound on the diameter.

### Proof

Fix any real values on T+. Let c be the unweighted mean of the values on T.
For each original vertex v write delta_v=x_v-c. If leaf ell is attached
at v, write eta_ell=y_ell-x_v. Put

    U = sum_uv in E(T) (x_u-x_v)^2,
    V = sum_new_leaves eta_ell^2,
    a_v = number of new leaves at v <= a.

The mean on T+ minimizes squared distance to constants. Evaluation at c
therefore gives

    Var_(T+)(x,y)
       <= sum_v delta_v^2 + sum_ell (delta_parent(ell)+eta_ell)^2
        = sum_v (1+a_v)delta_v^2
          + 2 sum_ell delta_parent(ell) eta_ell + V.

The core Poincare hypothesis and Cauchy--Schwarz imply

    sum_v (1+a_v)delta_v^2 <= (a+1)beta U,
    |sum_ell delta_parent(ell) eta_ell|
       <= sqrt(sum_v a_v delta_v^2) sqrt(V)
       <= sqrt(a beta U V).

Consequently

    Var_(T+)(x,y) <= (a+1)beta U + 2 sqrt(a beta U V) + V.

The right side is the quadratic form of

    Q = [[(a+1)beta, sqrt(a beta)],
         [sqrt(a beta), 1]]

at (sqrt(U),sqrt(V)). Its larger eigenvalue is the displayed L. Thus the
right side is at most L(U+V), which is exactly the required original plus
pendant edge energy. This also covers a=0, with a conservative value beta
when beta>=1. There is no division by the number of vertices. QED.

If the core is a singleton, evaluate at its value: the total variance is at
most the sum of pendant edge energies directly. This is the star case and
has Poincare constant at most one. A component with no edge needs no edge
inverse. These cases avoid assigning a nonexistent positive spectral gap
to a one-vertex core.

## 2. Exact clean constant for Cycle11

For the inherited arm-at-most-two spider core, use

    beta = (3+sqrt(5))/2.

In the bridge-deleted module construction, every original module vertex has
internal degree at least two. Since its original full degree is at most
four, at most a=2 pendant bridges attach to it. This is a bound on original
degree, not a fictitious action on the module alone.

For these values, the matrix Q is strictly smaller than 9I in the Loewner
order. Indeed

    9-3beta > 0,
    det(9I-Q) = 8(9-3beta)-2beta
              = 72-26beta = 33-13sqrt(5) > 0.

The first inequality follows from beta<3. The final inequality is exact:
33^2=1089 > 845=13^2*5 and both sides compared are positive. The 2-by-2
Sylvester criterion gives Q<9I. Therefore every full bichromatic tree in
this operation has Poincare constant less than nine, including bridge-only
stars by the singleton-core case. The resulting convenient uniform
reconstruction bound uses nine; no floating eigenvalue is its proof.

If desired, the exact stronger expression is

    2L = 3beta+1 + sqrt((3beta-1)^2+8beta).

No claim is made that this upper bound is the optimal full-graph inverse.
The stricter Cycle10 constant remains applicable when no bridges are present.

## 3. Canonical full-action least squares

For a proper coordinate coloring, the measurements at a vertex in the
columns of its neighboring colors decompose into unsigned tree-incidence
problems, one per bichromatic component. Multiplying vertex observations
by the bipartition sign conjugates unsigned incidence to oriented incidence.
The nonzero squared singular values are the positive Laplacian eigenvalues.
The mean-zero projection and subtree-sum inverse are the canonical least
squares solution. A Poincare constant at most L gives

    ||edge_coefficient_error||_2^2 <= L ||component_action_noise||_2^2.

Distinct color-pair problems occupy disjoint entries of the original n-by-q
action matrix. Arbitrary diagonal coefficients are read from the vertex's
own-color entry, also disjoint from those problems. In the symmetric output,
each offdiagonal coefficient appears twice in the Frobenius norm. Therefore

    ||Dhat-D||_F^2
       <= ||diagonal_noise||_2^2
          + 2L sum_component ||component_action_noise||_2^2
       <= max(1,2L)||E||_F^2.

With the exact upper L<=9 from Section 2, this yields

    ||Dhat-D||_op <= ||Dhat-D||_F <= 3sqrt(2) ||E||_F.

Unused action entries can be discarded orthogonally. This does not grant a
reduced-action oracle: all original actions are acquired, and noise in every
entry remains part of the original absolute Frobenius budget. Exact noiseless
recovery follows from injectivity of tree incidence on edge coefficients and
the proper-color separation of diagonals.

This is an exact-real-arithmetic theorem. Any finite-precision implementation
must add a bound for its acquisition/design/assembly error and certified
decoder residual. Those quantities are not included for free in the proof.

## 4. Scope and observed work

The combinatorial module hypotheses are proved in BRIDGE_INTERFACE_LEMMA.md,
conditional there on the new rooted atom guarantee. Their critical restriction
is that every bridge child endpoint is a leaf in its own bridge color pair.
If bridges can continue through their child endpoint, the new leaf-extension
lemma does not apply; the saved triangle-chain example demonstrates failure.

The argument was derived and checked symbolically. There was no numerical
eigenvalue experiment for this bound. Reading, inference, proof authoring and
review costs are unknown. The separate exact triangle-chain diagnostic has
its own recorded execution costs and is not charged as this proof's discovery
cost. No historical novelty, application performance, or all-real query lower
bound is asserted.
