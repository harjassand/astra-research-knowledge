# Retain the projective defect; change the move

Status: restricted operations proved; general strongly polynomial LP algorithm **not obtained**.
Date: 2026-10-13. No commit or publication. No novelty or priority claim.

## 1. Target and primary-source baseline

The target is a rational LP algorithm using poly(m,n) arithmetic operations and comparisons independently of coefficient magnitudes, with every intermediate rational of encoding length polynomial in the input. A coefficient-dependent number of exact, cheap steps fails this target.

Targeted primary-source checks on 2026-10-13:

* Dadush–Huiberts–Natura–Végh, [A scaling-invariant algorithm for linear programming whose running time depends only on the constraint matrix](https://arxiv.org/abs/1912.06252): nearly optimal diagonal scaling can itself be computed with polynomially many operations, but the optimized condition parameter survives in the LP iteration bound. Asking for a better scaling is an occupied and incomplete route.
* Dadush–Koh–Natura–Végh, [On circuit diameter bounds via circuit imbalances](https://arxiv.org/abs/2111.07913): the augmentation bound still involves log(n+kappa_A). A short, computably acquired walk independent of that parameter is the relevant missing feature.
* Dadush–Koh–Natura–Olver–Végh, [A strongly polynomial algorithm for linear programs with at most two nonzero entries per row or column](https://bentonatura.com/assets/pdf/genflow.pdf), Theorem 1.1 and Sections 1.1/1.3: exact 2VPI and minimum-cost generalized-flow optimization is strongly polynomial. The manuscript states that general LP remains open and distinguishes arithmetic-operation bounds from rational bit size. Its discussion notes that three entries per inequality already suffice to represent general LP.
* Black, [Exponential Lower Bounds for Many Pivot Rules for the Simplex Method](https://arxiv.org/abs/2403.04886): shadow and norm-based steepest-edge variants have broad worst-case lower bounds. Renaming an edge norm or projection supplies no progress argument.

These establish the comparison used here, not an exhaustive literature search.

## 2. Operation A: normalize a projective frame

Choose an independent column basis B of a homogeneous configuration A, replace A by B^{-1}A, then positively scale each nonzero column to have coordinate 1-norm one. This takes polynomially many exact operations. In a standard-form LP, row transformations and positive column scaling have the usual exact transformations of b,c,x.

The hypothesis that frame changes remove small-angle geometry fails on four rays:

~~~
            [1  0  1  1]
A_epsilon = [0  1  1  e],       0 < e <= 1/4.
~~~

Its four circuits, up to overall sign, are

~~~
g123 = (-1, -1, 1, 0),
g124 = (-1, -e, 0, 1),
g134 = (e-1, 0, -e, 1),
g234 = (0, e-1, 1, -1).
~~~

Let kappa(A) be the maximum absolute ratio of nonzero coordinates of a circuit. Positive column scaling D sends g to D^{-1}g; invertible row transformations leave the kernel unchanged.

**Proposition 1.** For every invertible U and positive diagonal D,

~~~
kappa(U A_epsilon D) >= e^(-1/2).
~~~

For e<=1/4, D=diag(1,sqrt(e),sqrt(e),1) attains equality.

Proof. In circuits 123 and 124, the ratios of coordinate 2 to coordinate 1 after scaling are r=d1/d2 and er. If every ratio is between 1/K and K, then r<=K and er>=1/K, so K²>=1/e. With the displayed D, the four circuit magnitudes are

~~~
(1,1/sqrt(e),1/sqrt(e)),
(1,sqrt(e),1),
(1-e,sqrt(e),1),
((1-e)/sqrt(e),1/sqrt(e),1).
~~~

Each ratio is at most 1/sqrt(e) for e<=1/4. The square root only describes the optimum; the rational test uses e=2^(-2L).

For Delta_ij=det(a_i,a_j), the invariant is

~~~
(Delta_13 Delta_24)/(Delta_14 Delta_23) = 1/e.
~~~

All six minors are nonzero, with fixed signs throughout 0<e<1. A fixed realizable oriented matroid therefore contains arbitrarily large projective defects. This obstructs conditioning the defect away, **not** a strongly polynomial oriented-matroid algorithm. Rank two is easy to solve exactly.

## 3. Operation B: exact two dimensional fan jump

Given a feasible rational x for P={x:Hx<=h}, choose an input-defined rational two-column frame V. For equality-form LP, its columns must lie in the equality kernel. Solve the entire slice

~~~
maximize   c^T V u
subject to (H V)u <= h-Hx,    u in R².
~~~

This macro operation can cross arbitrarily many candidate bases inside its slice. An exact O(N³)-operation implementation for N inequalities is:

1. Include u=0.
2. For every nonzero row a_i, include the rational projection (b_i/(a_i^T a_i))a_i onto its boundary line.
3. Solve every independent pair of boundary equations.
4. Test all candidates against all inequalities; select the best feasible candidate.
5. Test improving recession directions among both signs of every perpendicular row vector and both signed coordinate axes. A successful direction certifies full-LP unboundedness.

A bounded optimum has a vertex unless all normals are parallel. Pair intersections cover vertices; single-line candidates cover the parallel case. Lower-dimensional degeneracy is included. No square root, tolerance, or circuit oracle occurs.

For input-defined frames, a selected update is an affine rational map of the previous point with input-defined coefficients. Common-denominator accounting grows encoding length additively by poly(input) per update. Polynomially many jumps would therefore have polynomial bit size. Inverse matrices depending nonlinearly on the current point need a separate global bit-growth argument.

This bypasses the four-ray scale exactly, but its proposed global progress fails.

## 4. Lower bound for every bounded coordinate block

For d>=3, define

~~~
P_alpha = { z>=0 : z_i <= alpha sum_{j!=i}z_j for every i,
                        sum_i z_i <= 1 }.
~~~

Maximize sum_i z_i. Set alpha=1/(d-1)+delta, delta>0, and z^0=eta 1 with 0<d eta<1. This point is strictly feasible. The optimum is exactly one, attained at z*=1/d 1.

A block jump optimizes all selected k<d coordinates, fixing the rest. Let S be the sum of selected coordinates and T the sum outside. Summing selected constraints gives, for alpha(k-1)<1,

~~~
S <= alpha((k-1)S+kT),
S <= alpha k T/[1-alpha(k-1)].                         (1)
~~~

If equality is feasible and the cap is not reached, the unique block optimum is

~~~
z_i^+ = alpha T/[1-alpha(k-1)]   for selected i.        (2)
~~~

The universal growth bound does not presume (2) is feasible. For *every feasible update*, each selected inequality and (1) imply

~~~
(1+alpha)z_i^+ <= alpha(S+T)
                 <= alpha(1+alpha)T/[1-alpha(k-1)].
~~~

Writing M=max_i z_i, this yields

~~~
M^+ <= R M,
R = alpha(d-k)/[1-alpha(k-1)]
  = 1+delta(d-1)^2/[d-k-delta(d-1)(k-1)].             (3)
~~~

An optimum has M>=1/d. Thus *every sequence*, regardless of block selection, needs

~~~
T_steps >= log(1/(d eta))/log R.                       (4)
~~~

For fixed d,k<d this is Omega(1/delta). Taking delta=2^(-L) forces exponentially many exact macro steps in a coefficient's encoding length. This lower bound is for coordinate blocks, not arbitrary adaptively rotated subspaces.

**Fully executable d=3 instance.** Take k=2, eta=1/12, 0<delta<=1/4. Before the cap, the exact pair optimum is

~~~
z_i^+ = z_j^+ = r z_k,
r = alpha/(1-alpha) = 1+4delta/(1-2delta).
~~~

The outside constraint holds because 2 alpha r>=1, equivalent to (2alpha-1)(alpha+1)>=0. Hence M^+<=rM. Since log r<=r-1<=8delta,

~~~
T_steps >= log(4)/(8delta) > 1/(8delta).
~~~

The weaker last bound needs no logarithm: if 8delta T<=1, the binomial expansion gives (1+8delta)^T<3<4.

At delta=0, the sum of all row slacks is zero, forcing z=t1. Every proper coordinate slice is a singleton, though increasing all coordinates together reaches the optimum. This is exact degeneracy, not roundoff.

**Standard form.** Add nonnegative slacks s_i=alpha sum_{j!=i}z_j-z_i and t=1-sum z. The equalities are

~~~
s_i+z_i-alpha sum_{j!=i}z_j=0,
t+sum_j z_j=1.
~~~

The natural basis consists of the s_i and t. Its fundamental directions are exactly the z-coordinate directions with induced slack changes. Thus this is a failure for fully acquired fundamental-direction pair slices.

## 5. Mutation: keep the full cluster and resolve its direction

The narrow-cluster normal matrix is

~~~
M_alpha=(1+alpha)I-alpha 11^T,
M_alpha 1=[1-alpha(d-1)]1=-theta 1,
theta=alpha(d-1)-1=(d-1)delta.
~~~

An exact solve gives

~~~
v=-M_alpha^{-1}1=(1/theta)1.
~~~

Normalize by its first nonzero coordinate to get v=1. One exact ratio test against the cap reaches z*=1/d 1 from eta 1. Dividing by tiny theta costs one permitted rational arithmetic operation. For delta=0, rational nullspace computation produces the same diagonal. For delta<0, summing constraints proves the only feasible point is zero.

The augmented normal configuration retains the defect in the exact relation

~~~
sum_i row_i(M_alpha)+theta 1^T=0.
~~~

Erasing theta changes the LP. The mutation keeps the relation intact and constructs a collective direction rather than repeatedly optimizing small coordinate pieces.

**General checkable primitive.** Given feasible x, a k-column rational frame V, k selected inequality rows S, and positive rational q, set

~~~
R=H_S V,
beta=-R^{-1}q,
v=V beta.                                            (5)
~~~

If R is singular, compute a rational nullspace instead; presume no favorable sign. Explicitly verify

~~~
c^T v>0,
H_i v<=0 for every currently tight row i.             (6)
~~~

When (6) holds, take the exact ratio step

~~~
tau=min_{i:H_i v>0}(h_i-H_i x)/(H_i v).                (7)
~~~

An empty denominator set gives an unboundedness certificate. Otherwise x+tau v is feasible and improves. This is polynomial arithmetic for any acquired block, however ill-conditioned it is. Fraction-free elimination bounds one invocation's rational encoding length polynomially in its supplied data. It solves the whole lower-bound family in one move with V=I, S the narrow-cluster rows, q=1.

This uses classical linear algebra as a candidate scheduling operation. The inverse is not claimed as a new theorem.

## 6. Remaining gates are substantive

**Uniform q fails.** For 0<e<1, let

~~~
H=[-1 -e]
  [-e  1].

-H^{-1}1=((1+e)/(1+e²),(e-1)/(1+e²)).
~~~

The second coordinate is negative, yet v=(1,e/2)>0 satisfies Hv<0. Failed signs do not certify infeasibility. The algebraic-exchange cell independently supplied positive-pivot Z-matrix elimination finding an appropriate nonnegative ray for its sign-restricted setting; unrestricted acquisition remains separate.

**Generic feasible-q acquisition encodes general LP.** Given arbitrary rational Fz<=g with z free, at the origin use u=(z^+,z^-,t)>=0 and

~~~
F(z^+-z^-)-g t<=0.
~~~

Choose R=-I from the nonnegativity rows, so (5) gives v=q. Finding positive q satisfying all remaining tight inequalities and improving objective t>0 is equivalent to the original LP being feasible. One direction divides z^+-z^- by t. Conversely take t=1 and add a large common positive vector to a signed splitting of any feasible z. Adding sum u<=1 bounds the move without changing equivalence. A generic sign-feasible-q oracle is therefore an LP oracle.

**New tight rows are not permanent.** Consider

~~~
0<=z1,z2<=1,  0<=z3<=1,
z1+2z3<=2,    z2+2z3<=2,
maximize z1+z2+5z3.
~~~

From (1/10,1/10,1/10), the exact slice fixing z3 returns (1,1,1/10). Both newly tight rows z1<=1 and z2<=1 are slack at the unique global optimum (0,0,1). Freezing either selected facet can exclude the optimum. Macro jumps supply no permanent rank progress.

## 7. Surviving operation and exact next gates

The surviving primitive is **collective solve (5), sign checks (6), ratio jump (7)**, with exact nullspace and sign verification at singular blocks. It skips arbitrary projective scales on an acquired cluster and has a polynomial arithmetic and bit-size implementation per invocation.

Disproved claims: all defects can be normalized away; bounded-size exact coordinate fan jumps have a strongly polynomial total count.

Unresolved:

1. Acquire suitable unrestricted signed clusters from the input in poly(m,n) operations, without a hidden LP or supplied circuit oracle.
2. Prove each accepted jump gives a final certificate or permanent progress in a polynomially bounded state. A new tight row is insufficient.
3. Bound total invocations independently of all cross ratios and coefficient magnitudes.
4. Bound global rational encoding length for the actual adaptive representation.

The executable decisive_tests.py checks the formulas, degeneracy, rational cross-ratio family, pair-jump recurrence, full-cluster escape, and invalid progress inferences.
