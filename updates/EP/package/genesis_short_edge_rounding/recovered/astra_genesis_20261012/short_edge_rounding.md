# ASTRA Primitive Genesis: short edges and unbiased discrepancy rounding

**Research checkpoint:** 12 October 2026, Australia/Brisbane.

**Status:** A theorem and full argument derived in this research session. This is not independently reviewed, formally verified, or an established priority claim. The argument adapts the retained-row spectral method in recent Komlós work; it does not claim that method as an original invention. The new proposed contribution is its transfer to arbitrary short-edge 0/1 polytopes, including preservation of exact marginals, and the resulting geometric characterization. No polynomial-time construction is established here.

## 1. Main statement

Let P be a nonempty polytope whose vertices belong to {0,1}^n. For a nonsingleton P define

\[
 k(P)=\max\{\|u-v\|_1:[u,v]\text{ is an edge of }P\}.
\]

Thus k(P) is the largest number of coordinates changed by one polytope edge. Set k(P)=0 for a singleton.

For a real m-by-n matrix A with Euclidean column norms at most one, and x in P, write

\[
 G_C(P,A,x)=\{v\in\operatorname{vert}P:\|A(v-x)\|_\infty\le C\}.
\]

### Theorem 1: short-edge, exact-marginal rounding

For every nonsingleton P, every such A, and every x in P,

\[
 \boxed{x\in\operatorname{conv}G_{54k(P)}(P,A,x).}
\]

Equivalently, there is a probability distribution on vertices Z of P such that

\[
 \mathbb EZ=x,
 \qquad \|A(Z-x)\|_\infty\le54k(P)\quad\text{with probability one}.
\]

The law may depend on P, A, and x. This does NOT assert that one law works simultaneously for all matrices A. Its support can be chosen to contain at most n+1 vertices. This support bound is existential, not an efficient-construction assertion.

In particular, for every additional linear objective c there is a vertex v with

\[
 c^Tv\le c^Tx,
 \qquad \|A(v-x)\|_\infty\le54k(P).
\]

### Theorem 2: characterization of the universal radius

Define

\[
 \mathfrak b(P)=\sup_{m\ge1}\sup_{A:\max_j\|A_{\cdot j}\|_2\le1}
 \sup_{x\in P}
 \inf\{C\ge0:x\in\operatorname{conv}G_C(P,A,x)\}.
\]

Then

\[
 \boxed{\frac{k(P)}2\le\mathfrak b(P)\le54k(P).}
\]

For a singleton both sides are zero. Consequently, uniformly bounded edge Hamming length is necessary and sufficient for a family of 0/1 polytopes to admit uniformly bounded, exact-marginal discrepancy rounding. The constants are not optimized.

## 2. Immediate consequences

### Arbitrary matroid bases

Every edge of a matroid base polytope changes two coordinates. Hence, for every matroid M, every fractional basis x, and every real matrix A with Euclidean column norms at most one, there is a law on bases B satisfying

\[
 \mathbb E\mathbf1_B=x,
 \qquad \|A(\mathbf1_B-x)\|_\infty\le108
 \quad\text{almost surely}.
\]

This applies to arbitrary matroids, not only representable or strongly base-orderable matroids. In particular, one balanced basis has cost at most c^Tx for any prescribed linear cost c.

A quick proof of the edge fact uses symmetric basis exchange. If distinct bases B,C differ in more than one exchange, symmetric exchange gives B'=B-e+f and C'=C-f+e, both bases, with

\[
 \mathbf1_B+\mathbf1_C=\mathbf1_{B'}+\mathbf1_{C'}.
\]

If B,C were the endpoints of an exposed edge, the midpoint identity would put B',C' in that edge. They are different from B,C when |B\C|>1, a contradiction. Thus adjacent bases differ by one removal and one insertion. Symmetric exchange follows from the fundamental circuit of e relative to C and the fundamental cocircuit of e relative to B: their intersection cannot be {e}, because otherwise e would lie in the closure of B-e.

### Column-sparse constraints

If every column of a real matrix has at most t nonzeros and every entry has magnitude at most w, its column norms are at most w sqrt(t). Scaling therefore gives

\[
 \|A(\mathbf1_B-x)\|_\infty\le108w\sqrt t
\]

with exact marginals, and also a cost-nonincreasing choice of basis. Zero matrices are handled separately when w sqrt(t)=0.

### Spanning trees

For a connected graph, take its graphic matroid. A fractional spanning tree can be represented as a distribution over spanning trees with its exact edge marginals and with a deterministic bound 108 on every prescribed normalized linear measurement. If each edge belongs to at most t measurement categories, the corresponding unscaled category-count bound is 108 sqrt(t).

This is NOT a general cut-thin-tree theorem: listing all cuts can give a column norm that grows exponentially with the number of graph vertices. It is also not a spectral sparsification theorem, because the conclusion concerns the specified scalar matrix A, not an operator-norm constraint.

### Exact structural boundary

Two matroid constraints cannot be silently substituted for one. The perfect-matching polytope of an even cycle has only two vertices and an edge changing all cycle coordinates. Its maximum edge length grows with the cycle. Theorem 2 records precisely why a uniform exact-marginal rounding constant cannot hold there. The even-cycle obstruction itself is elementary and already appears in the matroid-discrepancy literature; it is not claimed as new.

## 3. Geometry: the face dimension is a proved consequence

For a face F of P let s(F) denote the number of coordinates that are not constant on F. If every edge of P changes at most k coordinates, then

\[
 \boxed{s(F)\le k\dim F.} \tag{3.1}
\]

Proof. Fix a vertex of F. Its incident edge directions span the direction space of F. Select dim(F) linearly independent such directions. Each is supported on at most k coordinates. Every coordinate that varies on F must occur in their union of supports. This proves (3.1).

At a point in the relative interior of a face of a 0/1 polytope, the varying coordinates are exactly the fractional coordinates. Indeed, a coordinate fixed on a face must have its common value at all of that face's 0/1 vertices, hence must be 0 or 1. Conversely, a coordinate at 0 or 1 at a relative-interior point must have that same value throughout the face.

The same facts hold after the change of variables y=2x-1, which maps P to a polytope Q with vertices in {−1,1}^n. Thus, if a point of Q has s unfrozen coordinates and all those coordinates are strictly between −1 and 1, the tangent space of its minimal face has dimension at least s/k.

This is not a new compatibility assumption. It is established from the local edge hypothesis, and an edge of maximum length attains the worst possible ratio s(F)/dim(F)=k.

## 4. Proof strategy and attribution

The proof works on Q=2P−1. We construct a good vertex of Q while allowing an arbitrarily small linear perturbation of a spectral potential. That perturbation gives cost preservation in a limit. Separation then produces exact marginals.

The retained coefficients, affine row tracking, concave row energy, nonnegative Gram potential, deletion budget, and diagonal normalization have antecedents in the recent constructive Komlós framework. In particular, the archive of Akbas and Sra contains these analytic ingredients and explicitly attributes the earlier spectral signing framework to Guo, Fang, and Lu and additional refinements to Li. This note gives the specific statements needed below with proofs, rather than importing an unproved extension to a new feasible set.

The proposed transfer has three substantive features:

1. The available dimension is the tangent dimension of the current polytope face, not the full cube dimension.
2. Diagonal normalization prevents the matrix used to hold large rows fixed from consuming that dimension reserve. Without it, a direct parameter choice gives an avoidable logarithmic loss in k.
3. Linear perturbations have zero Hessian. Consequently the same second-order contradiction can enforce every supporting linear objective and recover exact marginals at no extra discrepancy factor.

The existence proof uses global minimization over compact sets defined partly by concave sublevel inequalities. Those sets are generally nonconvex. No efficient optimization oracle for them is assumed as a computational primitive.

## 5. Parameters and retained-row state

Fix an upper bound k≥1 for the edge lengths and set

\[
 R=2\sqrt k,\quad
 \Delta=\frac1{16R^2}=\frac1{64k},\quad
 \beta=\frac1R,\quad
 a_0=4R^2,
\]
\[
 H=11R^2,\qquad b=6R,\qquad f(t)=2R(1-t^2),\quad -1\le t\le1.
\]

Then

\[
 0\le f\le2R,\quad f(\pm1)=0,\quad f'(t)=-4Rt,\quad f''(t)=-4R,
\]

and β(b−max f)=4.

Let y^0∈Q be the starting point. Let V be the currently unfrozen coordinates and s=|V|. Every frozen coordinate is held at its chosen value ±1 for all later steps. Row i has a retained subset T_i⊆V and an affine offset c_i. Put

\[
 b_{ij}=a_{ij}\mathbf1_{j\in T_i},\quad
 p_{ij}=b_{ij}^2,\quad q_i=\sum_{j\in V}p_{ij},
\]
\[
 d_i(y)=c_i+\sum_{j\in V}b_{ij}y_j,
 \qquad E_i(y)=\sum_{j\in V}p_{ij}f(y_j).
\]

Initially take V=[n], retain all coefficients, and set c_i=−(Ay^0)_i. Thus d_i(y^0)=0. Coordinates already on the cube boundary can immediately be frozen by the cleanup rules below.

The column normalization gives

\[
 \sum_iq_i\le s. \tag{5.1}
\]

A row is large if q_i>R², medium if 0<q_i≤R², and completed if q_i=0. Large rows are constrained by d_i=0. They undergo no deliberate deletion. On a medium row set r_i=√q_i.

Repeatedly delete any medium-row coefficient satisfying

\[
 p_{ij}>\Delta q_i. \tag{5.2}
\]

When a coefficient is deleted or frozen at the current point y, transfer b_ij y_j into c_i before removing it. This preserves d_i at the current point. A cleaned medium row satisfies

\[
 z_i:=p_i/r_i^2,\qquad \sum_jz_{ij}=1,\qquad 0\le z_{ij}\le\Delta. \tag{5.3}
\]

For each medium row and sign σ∈{−1,1}, define

\[
 u_{i\sigma}(y)=\frac{\sigma d_i(y)-H}{r_i}
                 +\frac{E_i(y)}{r_i^2}+b,
 \qquad a_{i\sigma}(y)=a_0 e^{\beta u_{i\sigma}(y)}.
\]

Require both barriers u_iσ≤0. They imply |d_i|≤H because E_i≥0 and b>0.

Choose η>0 with η≤1/(512kn). Define

\[
 W(y)=\sum_{i,\sigma}a_{i\sigma}(y)z_i z_i^T,
 \qquad B=\frac12\sum_{i\text{ large}}\operatorname{diag}(p_i),
\]
\[
 M(y)=W(y)+B+\eta\mathbf1\mathbf1^T,
 \qquad L(y)=\lambda_{\max}(M(y)). \tag{5.4}
\]

All matrices are on the active coordinates. Both W and B are positive semidefinite, M is entrywise strictly positive, and 0≤B≤I/2. The ridge makes L a simple eigenvalue. When no active coordinate remains, set L=0.

## 6. Initialization and cleanup

### 6.1 Covering a newly medium row

Such a row has d_i=0. At its entry scale r≤R,

\[
 u_{i\sigma}\le-H/r+2R+b=-11R^2/r+8R<0.
\]

Writing w_iσ=a_iσ/r⁴, the two row Gram terms are covered by the old diagonal deposit if

\[
 \frac{2a_0}{r^2}\exp(-11R/r+8)<\frac12. \tag{6.1}
\]

Set t=R/r≥1. The left side is 8t²e^(−11t+8). Its logarithmic derivative is 2/t−11<0. Therefore it is at most 8e^(−3)<1/2. An exact elementary certificate is

\[
 e^3>\sum_{j=0}^4\frac{3^j}{j!}=\frac{131}{8}>16.
\]

The matrix comparison uses p_i p_i^T≤q_i diag(p_i), which follows from weighted Cauchy–Schwarz. Initially the same calculation covers every initially medium row. Consequently

\[
 M(y^0)\preceq\frac12I+\eta\mathbf1\mathbf1^T,
 \qquad L(y^0)\le\frac12+\eta n<1. \tag{6.2}
\]

### 6.2 Deleting a coefficient

First hold r fixed. Removing a retained coefficient preserves d_i and decreases E_i, p_i, u_iσ, and w_iσ. The nonnegative row Gram matrix therefore decreases entrywise. For nonnegative symmetric matrices, entrywise decrease cannot increase the largest eigenvalue: use a nonnegative unit Perron eigenvector of the smaller matrix in its Rayleigh quotient.

Now decrease r to √q for the new retained mass, holding the new row data fixed. While u≤0 and E/r²≤2R,

\[
 r\partial_r u=b-u-E/r^2\ge4R,
\]
\[
 r\partial_r\log w=\beta(b-u-E/r^2)-4\ge0. \tag{6.3}
\]

Thus decreasing r preserves u≤0 and does not increase w. These conditions persist throughout the scale decrease: the new q is fixed, r² stays at least q, and the derivative at any possible first crossing u=0 has the sign excluding an upward crossing as r decreases.

### 6.3 Freezing coordinates

At y_j=±1, f(y_j)=0. Removing such a coordinate, before adjusting row scales or classes, simply takes a principal submatrix of M and preserves all tracked sums. Its top eigenvalue cannot increase. Subsequent scale updates are covered by §6.2, and a large row becoming medium is covered by §6.1. Completed rows have constant tracked sums of magnitude at most H, or zero if they completed directly from the large class.

All cleanup operations therefore preserve feasibility and do not increase L. They do not change y itself, its full n-coordinate squared norm, or any linear objective in y.

There are finitely many cleanup operations: a retained coefficient is removed only once, and each coordinate is frozen only once.

## 7. The deletion error does not accumulate with dimension

At a deliberate deletion, write a=|a_ij| and q for the row mass just before deletion. From a²>Δq,

\[
 \frac{a}{\sqrt q-\sqrt{q-a^2}}
 =\frac{\sqrt q+\sqrt{q-a^2}}a
 <\frac{1+\sqrt{1-\Delta}}{\sqrt\Delta}
 =:A_\Delta<8R. \tag{7.1}
\]

Summing decreases of √q from the row's first entry into the medium class gives

\[
 \sum_{j\text{ deliberately deleted in row }i}|a_{ij}|
 \le A_\Delta R<8R^2. \tag{7.2}
\]

Freezing only uses additional decreases of √q, so it does not invalidate the bound.

For every later point y agreeing on frozen coordinates, exact affine bookkeeping gives

\[
 [A(y-y^0)]_i-d_i(y)
 =\sum_{j\text{ deliberately deleted}}a_{ij}(y_j-y_j^{\mathrm{del}}). \tag{7.3}
\]

Both coordinate values lie in [−1,1], so the absolute difference in (7.3) is less than 16R². Hence every feasible endpoint obeys

\[
 \|A(y-y^0)\|_\infty< H+16R^2=27R^2=108k. \tag{7.4}
\]

The important fact is the telescoping row-mass bound, not a sum of per-round errors.

## 8. The normalized spectral curvature lemma

Work at a fixed cleaned state, differentiating only in y while holding retained sets, offsets, scales, and row classes fixed. Let v be the positive unit Perron vector of M.

For a row/sign pair write

\[
 g_{i\sigma}=\nabla u_{i\sigma}
 =\sigma b_i/r_i-4Rz_i\circ y.
\]

Since z_ij=(b_ij/r_i)²≤1/(16R²),

\[
 (g_{i\sigma})_j^2\le4z_{ij}. \tag{8.1}
\]

Define

\[
 U=\sum_{i,\sigma}a_{i\sigma}\beta^2(z_i^Tv)^2
                      g_{i\sigma}g_{i\sigma}^T,
\]
\[
 D=4R\beta\sum_{i,\sigma}a_{i\sigma}(z_i^Tv)^2\operatorname{diag}(z_i).
\]

Then

\[
 U_{jj}\le\frac1{R^2}D_{jj}. \tag{8.2}
\]

Let C have columns √a_iσ z_i, and let G have rows √a_iσ β(z_i^Tv)g_iσ^T. For a direction h,

\[
 M'[h]v=CGh,
 \quad U=G^TG,
 \quad v^TM''[h,h]v=h^T(U-D)h,
 \quad CC^T=W. \tag{8.3}
\]

### 8.1 Removing the diagonal deposit

Assume L>1. Set

\[
 D_L=LI-B,\qquad S=D_L^{-1/2},
 \qquad K=S(W+\eta\mathbf1\mathbf1^T)S. \tag{8.4}
\]

Because B≤I/2, D_L is positive definite. Further,

\[
 LI-M=D_L^{1/2}(I-K)D_L^{1/2}.
\]

Thus 0≤K≤I; its top eigenvalue is exactly one and is simple. A unit top eigenvector is proportional to D_L^(1/2)v.

For every q perpendicular to v,

\[
 \boxed{q^T(LI-M)^\dagger q=(Sq)^T(I-K)^\dagger(Sq).} \tag{8.5}
\]

Proof. Sq is perpendicular to D_L^(1/2)v. The vector

\[
 z=S(I-K)^\dagger Sq
\]

solves (LI−M)z=q. It differs from (LI−M)^†q only by a multiple of v, orthogonal to q. Taking the inner product with q gives (8.5). This proves a quadratic-form identity, NOT a general assertion that pseudoinverses commute with congruence.

The preconditioner S is an anchor-point device in this argument. We are not differentiating a variable-dependent K and ignoring derivatives of S.

### 8.2 Canceling high normalized modes

Let E_high be the span of eigenvectors of K with eigenvalue at least 1/5. Impose

\[
 P_{E_{\mathrm{high}}}SM'[h]v=0. \tag{8.6}
\]

This includes the top eigenvector and therefore gives L'[h]=0.

On the remaining eigenspaces let

\[
 T=(I-K)^\dagger P_{E_{\mathrm{high}}^\perp}.
\]

Since (SC)(SC)^T≤K,

\[
 (SC)^TT(SC)\preceq\frac14I. \tag{8.7}
\]

Indeed, its nonzero eigenvalues equal those of T^(1/2)(SC)(SC)^T T^(1/2), which is bounded above by T^(1/2)KT^(1/2). The latter has eigenvalues λ/(1−λ)<1/4 on the retained low spectrum.

The simple-eigenvalue second-derivative formula, (8.3), (8.5), and (8.7) now give

\[
 \boxed{L''[h,h]\le h^T\bigl(\tfrac32U-D\bigr)h.} \tag{8.8}
\]

### 8.3 Counting positive curvature directions

The number of positive eigenvalues of (3/2)U−D is at most

\[
 \frac{3s}{2R^2}=\frac{3s}{8k}. \tag{8.9}
\]

To see this, first discard zero diagonal entries of D. Equation (8.2) and positive semidefiniteness force the corresponding rows and columns of U to vanish. On the remaining coordinates, congruence by D^(−1/2) preserves inertia, and

\[
 \operatorname{tr}\bigl(\tfrac32D^{-1/2}UD^{-1/2}\bigr)
 \le\frac{3s}{2R^2}.
\]

Each eigenvalue greater than one uses more than one unit of this trace. The nonpositive spectral subspace therefore loses no more than the number of dimensions in (8.9).

## 9. A complete dimension budget

Suppose u_iσ≤0 and L≤9/8.

**Large rows.** By (5.1), there are fewer than s/R²=s/(4k) large-row equations.

**Binding barriers.** If u_iσ=0, then a_iσ=a_0=4R². Since Σ_j z_ij=1, every such pair contributes 4R² to 1^TW1. Also 1^TW1≤Ls. Thus the number of binding pairs is at most

\[
 \frac{Ls}{4R^2}\le\frac{9s}{128k}. \tag{9.1}
\]

**High normalized modes.** Diffuseness gives

\[
 \operatorname{tr}W\le\Delta\mathbf1^TW\mathbf1\le\Delta Ls.
\]

For L>1,

\[
 \operatorname{tr}K
 \le\frac{\operatorname{tr}W+\eta s}{L-1/2}
 \le2(\Delta+\eta)s.
\]

Consequently

\[
 \dim E_{\mathrm{high}}\le5\operatorname{tr}K
 \le\frac{5s}{32k}+10\eta s. \tag{9.2}
\]

Because η≤1/(512kn) and n≥1,

\[
 10\eta s\le\frac{5s}{256k}. \tag{9.3}
\]

**Positive curvature.** Equation (8.9) contributes at most 3s/(8k).

Adding all these codimension charges gives

\[
 \left(\frac14+\frac9{128}+\frac5{32}+\frac38+\frac5{256}\right)\frac{s}{k}
 =\frac{223}{256}\frac{s}{k}<\frac{s}{k}. \tag{9.4}
\]

The face tangent space has dimension at least s/k. Therefore, after imposing the large-row equations, gradients of binding barriers, the high-mode equations, and membership in the nonpositive subspace of (3/2)U−D, a nonzero feasible direction remains. Its residual dimension is at least

\[
 \frac{33s}{256k}>0. \tag{9.5}
\]

This argument counts codimensions in the ambient active coordinate space and then intersects with the actual face tangent space. It does not assume that the spectral or barrier directions align with the matroid or polytope geometry.

When L≤1, the high-mode and positive-curvature constraints are unnecessary; the large-row and binding-barrier charges alone are already smaller than s/k.

## 10. Variational rounding: every stage freezes a coordinate

Fix a linear objective c and a small τ>0. Set η=τ²/n, choosing τ small enough that

\[
 \eta\le\frac1{512kn},
 \qquad \eta n+2\tau\|c\|_1\le\frac1{512}. \tag{10.1}
\]

Consider

\[
 \Psi(y)=(L(y)-1)_+^3-\eta\|y\|_2^2+\tau c^T(y-y^0), \tag{10.2}
\]

where the squared norm includes frozen coordinates.

At each cleaned state, globally minimize Ψ over the following set: points of Q agreeing with all frozen coordinates, satisfying d_i=0 for every current large row, and satisfying u_iσ≤0 for every current medium row/sign pair. The set is compact, and contains the current point. Its minimum exists.

Initialization and cleanup imply that the value at every selected minimizer is at most Ψ(y^0)=−η||y^0||². Therefore

\[
 (L-1)_+^3\le\eta n+2\tau\|c\|_1\le\frac1{512},
 \qquad L\le\frac98. \tag{10.3}
\]

Suppose a minimizer has no new active coordinate at ±1. All s active coordinates are then fractional in the sign-cube sense. Let T be the tangent space of its minimal face in Q. By §3, dim(T)≥s/k.

For every binding barrier impose g_iσ^Th=0. Each u_iσ is concave in y, so

\[
 u_{i\sigma}(y+th)\le u_{i\sigma}(y)+t g_{i\sigma}^Th=0
\]

for both positive and negative sufficiently small t. Nonbinding barriers remain feasible by continuity. The large-row equations are preserved by their homogeneous direction constraints, and h∈T gives a two-sided feasible segment in Q because y is relatively interior to its minimal face.

If L≤1, choose a nonzero h after the large-row and binding-barrier constraints. The cubic positive part is twice differentiable even at L=1, with zero second derivative there. Consequently

\[
 \Psi''[h,h]=-2\eta\|h\|_2^2<0.
\]

If L>1, use all the constraints in §9. Then L'[h]=0 and L''[h,h]≤0, giving

\[
 \Psi''[h,h]
 =6(L-1)(L'[h])^2+3(L-1)^2L''[h,h]-2\eta\|h\|_2^2
 <0. \tag{10.4}
\]

The linear tilt has no second derivative. A twice differentiable function cannot have negative second derivative in a two-sided feasible direction at a local minimum. This is a contradiction.

Thus every minimization stage produces at least one new cube-boundary coordinate. Freeze all such coordinates, perform cleanup, and repeat. At most n minimization stages are required. Each stage can be a difficult nonconvex optimization problem; counting stages is not counting computational time.

At termination y is a vertex of Q. Indeed, a point of Q with all coordinates in {−1,1} cannot be a nontrivial convex combination of different sign vectors. Its discrepancy obeys (7.4).

## 11. Linear objectives and exact marginals

At termination ||y||²=n and the empty active matrix has L=0. Since Ψ never exceeded its initial value,

\[
 \tau c^T(y-y^0)
 \le\eta(n-\|y^0\|_2^2)\le\eta n=\tau^2.
\]

Thus

\[
 c^T(y-y^0)\le\tau. \tag{11.1}
\]

Let G be the finite set of all vertices of Q whose discrepancy about y^0 is less than 108k. For every sufficiently small τ, the preceding construction returns a point of G satisfying (11.1). Hence

\[
 \min_{v\in G}c^T(v-y^0)\le0. \tag{11.2}
\]

This holds for every c. If y^0 were outside conv(G), strict separation would supply c with c^T(v−y^0)>0 for every v∈G, contradicting (11.2). Therefore y^0∈conv(G).

Return to x=(y+1)/2. The matrix discrepancy is divided by two:

\[
 \|A(x-x^0)\|_\infty<54k.
\]

This proves Theorem 1 (with the stated non-strict bound). Carathéodory's theorem gives support size at most n+1. The expectation identity is exact; no limiting distribution or approximate marginal is left in the statement.

## 12. Proof of the lower bound

Choose an edge [u,v] of maximum Hamming length k, and let x=(u+v)/2. Any distribution on vertices of P with mean x is supported on {u,v}. To see this, choose a linear functional exposing that edge: its expectation is its maximum, so every support vertex must be in the exposed face. The mean condition then forces probability 1/2 on each endpoint.

Take the one-row matrix with coefficients a_j=u_j−v_j. Every column has norm at most one, and

\[
 a^T(u-x)=\frac12\sum_j(u_j-v_j)^2=\frac{k}{2},
 \qquad a^T(v-x)=-\frac{k}{2}.
\]

Thus every exact-marginal law for this instance has worst-case discrepancy k/2. Combined with Theorem 1, this proves Theorem 2.

## 13. What has and has not become computationally available

The proof establishes existence and a small verifiable certificate. It does not establish a polynomial-time sampler.

For rational A and x and a membership oracle for the feasible 0/1 vertices, a finite exhaustive construction is available: enumerate all 2^n binary vectors, retain feasible vertices satisfying the discrepancy bound, and solve the linear feasibility problem

\[
 \sum_vp_vv=x,\qquad\sum_vp_v=1,\qquad p_v\ge0.
\]

The theorem proves this LP feasible. Enumeration is exponential in n; LP time is polynomial in the enumerated instance, not the original implicit one. For a matroid, feasibility of a candidate basis is checkable using its independence oracle and rank.

A basic feasible solution has at most n+1 support vertices. Since the constraint columns consist of 0/1 vertices augmented by a 1, rational x admits rational probabilities of polynomial bit length (by Cramer's rule and a determinant bound). Once supplied, the certificate is checked by exact linear algebra, basis/membership checks, and evaluating all matrix discrepancies. This does not remove the cost of finding the certificate.

### The principal unresolved constructive task

For rational A, x, and a matroid independence oracle, give a procedure with time and bit complexity polynomial in the input size and inverse permitted additive accuracy that constructs the good basis or the exact-marginal law, without globally minimizing the nonconvex feasible sets in §10.

There is positive leverage toward this task, not a completed algorithm: every wholly fractional local minimum is excluded with a quantitative residual dimension, diagonal normalization avoids a supplied spectral gap, and a positive ridge bounds the simple-eigenvalue gap. A local descent implementation would still need a fully charged finite-precision analysis of changing matroid faces, near-active barriers, tiny coefficients, rational state restoration, and total progress. No such analysis is asserted in this note.

This constructive question is separate from the existence theorem; it is not a structural assumption on which Theorems 1–2 depend.

## 14. Validation record

The accompanying audit.py and audit_results.json record the following internal checks:

- Exact rational verification of the codimension sum 223/256 and remaining reserve 33/256.
- Exact rational verification of e³>131/8>16, sufficient for the entry-deposit inequality.
- 160 numerical tests of the normalized reduced-resolvent quadratic-form identity and the low-spectrum operator bound, including nonconstant diagonal deposits.
- 24 numerical tests of the diagonal curvature estimate, high-mode cancellation, second-derivative comparison, and negative potential curvature. Twelve use the tangent space of a partition-matroid face; the other twelve use the full cube tangent space.

Observed maximum relative error in the normalized quadratic-form identity was about 2.2×10^(−15). The maximum finite-difference absolute error in the curvature check was about 2.7×10^(−9). These are local analytic checks, not numerical verification of the theorem for large instances, an implemented rounding algorithm, independent review, or formal proof.

### Adversarial issues explicitly checked in the argument

The proof uses the minimal face of the actual polytope, not an assumed cube face. It checks barrier feasibility in both signs of the chosen direction. It proves a quadratic-form resolvent identity rather than a false pseudoinverse-congruence rule. It includes all coefficient-deletion error. It keeps the full norm when coordinates freeze. It uses the L≤1 branch separately. It obtains exact marginals by finite-set separation rather than assuming that an unbiased walk stays within the discrepancy set. It does not infer efficient access from the existence of a compact support.

## 15. Research selection and novelty boundary

The initial screen considered general polynomial identity testing, Fourier entropy–influence, and discrepancy with exact combinatorial feasibility. For identity testing, a cancellation-sensitive compression closed under circuit operations was the missing operation; no such closure was established. For Fourier entropy–influence, a coordinate restriction exposes a rare-coefficient logarithmic entropy charge, and no uniform way to discharge that charge was established.

The unconstrained Komlós existence-to-algorithm gap was not retained as an open target after current-source checks found the September 2026 deterministic algorithm. The selected question was instead whether exact structural feasibility could coexist with dimension-free balancing. An initial independent-pair-exchange approach would only cover restricted matroids; the face-dimensional argument above avoids assuming such exchanges can be made independently.

The result, if its proof and novelty survive independent review, is broader than an isolated matroid lemma: it characterizes an entire class of feasible polytopes by a local geometric parameter, up to universal constants. Nevertheless, its analytic machinery is closely descended from recent Komlós proofs. It should not be described as a new proof of the already addressed unconstrained conjecture, nor as an independently validated historic breakthrough.

The targeted source search did not locate this exact short-edge characterization. Search incompleteness, especially for very recent manuscripts, prevents a priority claim. Both proof review and a broader literature audit remain necessary before attributing an original result to Astra.

## 16. Sources inspected or used for context

The following are source references, not independent validation of this note.

1. Sankeerth Rao Karingula and Shachar Lovett, *An elementary proof of the Komlós conjecture*, arXiv:2609.20979, September 2026. https://arxiv.org/abs/2609.20979
2. Guo, Ethan X. Fang, and Junwei Lu, *Vector Balancing in Polynomial Time*, arXiv:2609.23540, submitted 20 September 2026. https://arxiv.org/abs/2609.23540
3. Emrullah Akbas and Suvrit Sra, *Tighter bounds on Komlós discrepancy: existence and algorithmic results*, arXiv:2609.27172. https://arxiv.org/abs/2609.27172
4. Companion proof source, *Constructive Komlós discrepancy below 67*, archive/komlos_constructive_below67.tex, file SHA fa04ee2359d3d16ed4546ae7ec9a8972908ddc18. https://github.com/suvrit/komlos/blob/main/archive/komlos_constructive_below67.tex
5. Companion proof source, *Constructive Komlós discrepancy below 37.54*, archive/komlos_constructive_final.tex, file SHA a3c0748ccecb4a4f3ecd98f01d9d699ccfc9c339. https://github.com/suvrit/komlos/blob/main/archive/komlos_constructive_final.tex
6. Kristóf Bérczi, Siyue Liu, Victor Reis, and Jakub Tarnawski, *Weighted Equitability and Matroid-Constrained Discrepancy*, arXiv:2608.13983, submitted 14 August 2026. https://arxiv.org/abs/2608.13983
7. Nikhil Bansal, *On a generalization of iterated and randomized rounding*, arXiv:1811.01597; STOC 2019. https://arxiv.org/abs/1811.01597
8. Emrullah Akbas and Suvrit Sra, *Boolean Small-Ball Inequalities for Discrepancy Theory*, arXiv:2609.20785, September 2026. Its stated scope explicitly excludes arbitrary matroid-constrained rounding. https://arxiv.org/abs/2609.20785
9. Xiao Han, *A new bound for the Fourier-Entropy-Influence conjecture*, arXiv:2312.08271. https://arxiv.org/abs/2312.08271
10. *Polynomial Identity Testing and Reconstruction for Depth-4 Powering Circuits of High Degree*, arXiv:2602.20832. https://arxiv.org/abs/2602.20832

The user-specified Astra and OpenAI mathematical repositories were selectively searched after independent opportunity screening. No result in them is being represented as independently validated evidence for this new statement.
