# Local fan ports: exact partial recovery and an all-frame obstruction

Contributor: `/root/fan_port_lemma`, 22 October 2026 Australia/Brisbane.
Scope: a local construction/challenge for the owner's five-query question.
This note does not claim a general five-query lower bound or a global solution.

## 1. Model and the natural recursive port design

A fan has one apex and a path of new vertices, every path vertex adjacent to
the apex. New fans attach by identifying only their apex with an existing
path vertex. A nonroot vertex belongs to exactly one parent fan as a path
vertex; it may be the apex of arbitrarily many child fans. Off-diagonal
coefficients are allowed on graph edges and all diagonals are free.

We consider q=5 query directions, with each query row a unit vector in R^5.
For a fan with apex a, write b for the apex of a's parent fan, if it exists.
The following candidate has an appealing exact separation property:

* x_a and x_b are orthogonal unit vectors.
* For each child fan of a, choose any orthonormal basis of
  W_a = span{x_a,x_b}^perp, a three-dimensional subspace.
* Assign the fan's path vertices the three basis vectors periodically.
* At the root use any auxiliary orthogonal unit vector in place of x_b.

The choices of basis may depend on the entire graph, differ between fans,
and have arbitrary dense real coordinates. The root query vector and its
auxiliary vector may also be selected freely. The arguments below do not
restrict them to a fixed coordinate palette.

All subsequent statements use exact real vectors and observed action
Y=DX+E with absolute Frobenius norm on E. Applied-direction error, if any,
belongs in E through D DeltaX; it is not included for free.

## 2. Positive local port lemma: diagonals and spokes are isolated

Call an edge vertical if it joins a fan apex to one of that fan's path
vertices, and horizontal if it lies along a fan's path. The vertical edges
form the attachment tree; horizontal paths connect groups of siblings.

**Lemma.** Under the recursive orthogonal port design above, every diagonal
and every vertical edge is recovered exactly without using any apex-row
action for that edge. With arbitrary noise E, the recovered partial matrix
containing only these coefficients obeys

    ||Dhat_vertical - D_vertical||_F <= sqrt(2) ||E||_F.

**Proof.** Let v be a path vertex in a fan with apex a. At row v, the two
parent-fan path neighbors have basis vectors different from x_v, and both
are orthogonal to x_a. Every child-fan query vector is in
span{x_v,x_a}^perp. Also x_v is orthogonal to x_a. Therefore

    <Y_v,x_v> = D_vv + <E_v,x_v>,
    <Y_v,x_a> = D_va + <E_v,x_a>.

No parent-fan apex-row action is used. At the root, all child query vectors
are orthogonal to the root vector, so its diagonal is equally isolated.
At each nonroot row the two selected functionals are orthonormal, hence the
sum of their squared errors is at most ||E_v||^2. Copying each vertical
coefficient to both symmetric positions costs a factor two in squared
Frobenius norm. Summing proves the claim. QED.

This is an exact partial-recovery lemma. It does not bound the remaining
horizontal coefficients. Subtracting estimated child spokes from an apex
row may add many errors coherently, and the next theorem shows that this is
an information failure of this whole design class, not merely an unfortunate
choice of elimination algorithm.

## 3. Every recursive orthogonal port design fails under replication

**Theorem.** For each N>=1 there is a two-level tree of fan blocks H_N such
that EVERY recursive orthogonal port design described above satisfies

    C_2(H_N,X) >= sqrt(N/2).

This includes all choices of local orthonormal frames, even graph-adapted,
dense frames varying from block to block.

**Graph.** Start with a fan whose apex is a and whose two path vertices are
u,v. Thus {a,u,v} is a triangle. Attach N child fans at u and N at v, each
with a three-vertex path. There are 3+6N vertices and 3+10N edges. This is
exactly within the owner's tree-of-fans family and has treewidth two.

**Proof.** The root-fan vectors x_a,x_u,x_v are orthonormal. Every attached
three-vertex path at u is an orthonormal basis p_(u,r,1),p_(u,r,2),p_(u,r,3)
of W_u=span{x_u,x_a}^perp. Since x_v belongs to W_u, write

    -x_v = sum_j beta_(u,r,j) p_(u,r,j),
    sum_j beta_(u,r,j)^2 = 1.

The expansions may differ with r. Likewise, in each child fan at v write
-x_u in its orthonormal path basis, with coefficients beta_(v,r,j) of
squared norm one.

Set D_uv=D_vu=1. For every child fan r at u, put coefficient
beta_(u,r,j)/N on the spoke joining u to its j-th path vertex. Use the
analogous coefficients on child spokes from v. Put all other entries,
including every diagonal and all child horizontal edges, equal to zero.

At u the action is x_v plus N copies of -x_v/N, so it is zero. At v it is
zero for the same reason. At a it is zero. Every child path vertex has
action beta_(u,r,j) x_u/N or beta_(v,r,j) x_v/N. Consequently

    ||DX||_F^2 = 2N/N^2 = 2/N.

On the other hand ||D||_2>=|e_u^T D e_v|=1. Thus the inverse quotient is at
least sqrt(N/2). QED.

The lower bound applies to every decoder using this X, including global
least squares or nonlinear reconstruction: the supported perturbation itself
has arbitrarily small action. Stable isolation of the vertical part in
Section2 is compatible with this theorem, because that part of the witness
has Frobenius norm only 2/sqrt(N), while the uncaptured horizontal edge is
order one. The theorem says nothing about other graph-adapted dense designs.

### General replication principle

The proof needs only that the opposite endpoint query vector have uniformly
bounded coefficient representations in each attached child's query rows.
If -x_v has coefficient vector beta_r in each replicated block at u, and
-x_u has gamma_r at v, splitting those coefficients by N gives

    ||DX||_F^2 = (||x_u||^2 sum_r ||beta_r||^2
                  + ||x_v||^2 sum_r ||gamma_r||^2) / N^2.

Thus a bounded mean representation cost permits the same cancellation.
Orthogonal bases make that cost exactly one. This is a local diagnostic for
future proposed interfaces: high branching can amplify a permitted span
overlap even when every block has perfect local conditioning.

## 4. Protecting three parent functionals leaves too little child rank

A different local repair would protect three independent parent-row
functionals from all child contributions, so that a diagonal, spoke and
selected horizontal coefficient could all be read directly.

**Proposition.** In R^5, any such exact protection rule is incompatible with
uniform stability on arbitrarily long child fans if it requires every child
path query vector to annihilate the same three independent functionals.

**Proof.** Their common kernel has dimension at most two. All path query
rows of an attached child fan lie in this kernel; adding its one apex row
gives a query block of row-span dimension at most three. An orthogonal right
coordinate change therefore compresses that child's full query block to
three columns without altering any row norm or Frobenius action norm.

The accepted all-design three-query fan theorem applies: on an m-vertex
path joined to its apex, the inverse factor is at least
max(1,m^(1/4)/sqrt(3 pi)), and the stronger sine bound is also available.
The child-supported matrix extends by zero to the whole graph, so the same
obstruction holds for the full observations. QED.

Dependency: the accepted incoming fan theorem is preserved in the prior
source at incoming/tw2/arm_b/RESULT.txt and assessed in INTAKE.md. This is a
receiving use of that established proof, not a replay or a new proof of it.

The proposition is restricted to exact annihilation of three independent
parent functionals. It does not exclude controlled nonzero interference,
joint decoding, or nonlinear graph-adapted constructions. With only two
protected functionals there is enough child rank for a single fan, but the
recursive orthogonal ansatz then suffers the replication failure of Section3.

## 5. Executable exact evidence and costs

The script checks/check_fan_ports.py constructs the coordinate-specialized
members with N=1,16,256. In this specialization x_a=e1, x_u=e2, x_v=e3;
child path bases at u are (e3,e4,e5), and at v are (e2,e4,e5). It forms the
full graph and exact sparse D, computes every action entry by Fraction
arithmetic, and verifies the support and squared action norm 2/N. A separate
fully populated rational supported input checks every diagonal and vertical
reading in Section2. The source uses no eigensolver and no producer imports.

Largest member: N=256, n=1539, graph edges2563, nonzero undirected
coefficients513, every row norm1, action norm squared1/128, operator norm
at least1, inverse quotient squared at least128. Canonical fixture SHA256:
0e601f66abbeb74c8115b0c49206edba9d770005528dfff434f999ee3d3a8d73.

All three exact checks passed in one execution. Body wall0.025995729s,
CPU0.025995013s, maximum RSS13,631,488bytes. The machine-readable receipt is
results/fan_port_checks.json. Per-case times were not separately measured.
One prior-proof file read and one source patch are additional tool/authoring
work. Mathematical development, model inference, interpretation, monetary
cost and energy are unmetered additional costs, not zero. There was no web
search, paid compute, original benchmark replay, or precision sweep in this
scoped contribution.

## 6. Recommendation to the owner

Retire the recursive design that protects only own and parent-apex directions
using full orthogonal child frames: arbitrary local frame rotations cannot
repair it. Do not infer failure of five directions in general. A surviving
five-direction construction must limit the replicated span overlap or use a
more global information allocation than perfect isolation of these two
coefficient types. The general replication formula can test such an allocation
before investing in a depth-dependent global decoder.
