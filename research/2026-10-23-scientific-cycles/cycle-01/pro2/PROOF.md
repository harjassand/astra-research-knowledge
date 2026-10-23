# Shared-operator information, exact sparse identification, and stable recovery

Owner: Astra PRO 2. Checkpoint: 21 October 2026.

Computational file paths in this proof are relative to `research/` in the
archive; `sources/` refers to the archive root.

All mathematical statements below concern exact real matrices. Numerical
claims have separate exact-input certificates. Historical priority is not
claimed for completion theory, sparse peeling, coloring, or incidence spectra.
The new work is the source-bound calculation on the owned input, its sharp
identification threshold, an explicit conditioning witness, and the proved
stability comparison with its stated normalization.

## 1. What is retained from the preceding checkpoint

The original owner archive is preserved byte for byte under `sources/`:
`Astra_Restore_PRO2_20261021.zip`, 6,330,093 bytes, SHA-256
`f58b4f09eb259f0ac2d3962b955abd0fc7d603a7960a038257b72b1f00624115`.

Its sharp finite-precision completion estimate remains

\[
 \|A-B\|\le\tau+\frac{z+2\sqrt{z^2+3r^2}}3.
\]

The exact starting-vector moments agree with `e1^T J^j e1` through degree
`2k-1`. Its isospectral counterexample, eigenvector leakage, source conversion
allowance, and actual cost defeat are unchanged. In particular, moving the
horizontal threshold alone does not transfer a **probe-weighted** spectral CDF.

The incoming canonical-quadrature construction resolves the previous exact
single-probe question. For ell=0 its inclusive-CDF range is
`(0.22602940932374105045..., 0.56618106297375683022...]`; for ell=7 it is
`(0.11993665622255536217..., 0.61097287812379343815...]`. These use moments
through degree127, threshold `12983/536870912`, and support
`[-(M+tau+e_ell), M+tau+e_ell]`. The infima are not attained and the maxima are.
The supplied witnesses, polynomial duals, verifier, separate source-binding
program and receiving receipts are included under `incoming/`. We accepted
the source-bound construction and its independent review without repeating
the resolved numerical calculation. Eight individual measures do not by
themselves supply one common original operator.

## 2. Exact common-operator completion theorem

Let `X` be a real n-by-d matrix of full column rank, `Y` a prescribed action,
and `L<U`. Write

\[
 G=X^TX,\qquad T=X^TY=T^T,\qquad H=Y^TY.
\]

Assume `T-LG` and `UG-T` are positive definite. Consider

\[
 \mathcal C=\{B=B^T:BX=Y,\quad LI\preceq B\preceq UI\}.
\]

Define the explicit operators

\[
 B_L=LI+(Y-LX)(T-LG)^{-1}(Y-LX)^T,
\]
\[
 B_U=UI-(UX-Y)(UG-T)^{-1}(UX-Y)^T.
\]

**Theorem 1.** The class is nonempty if and only if

\[
 (L+U)T-LUG-H\succeq0.
\]

When nonempty, it is exactly the Loewner interval `[B_L,B_U]`. Both endpoints
satisfy the original action and support constraints. No basis of the omitted
complement is needed to construct or apply them.

### Proof

Put `Z_L=Y-LX` and `H_L=T-LG`. Then `Z_L^T X=H_L`, so `B_L X=Y`.
The corresponding identity gives `B_U X=Y`.

For any feasible B, let `C=B-LI>=0`, `W=C^(1/2)X`. Then `W^TW=H_L>0`
and `W(W^TW)^(-1)W^T` is an orthogonal projection. Consequently

\[
 Z_LH_L^{-1}Z_L^T
 =C^{1/2}W(W^TW)^{-1}W^TC^{1/2}\preceq C.
\]

Thus `B_L<=B`. Applying the same argument to `UI-B` gives `B<=B_U`.
Conversely, if `B_L<=B_U`, both endpoints lie in `[LI,UI]` and have action Y.
Their difference D is PSD and `DX=0`. If `0<=B-B_L<=D`, then
`X^T(B-B_L)X=0`; positivity implies `(B-B_L)X=0`. Every point of the order
interval is therefore feasible.

To derive compatibility, only for this proof choose `Q=X G^(-1/2)` and
complete Q to an orthogonal basis. In these coordinates all completions are

\[
 \begin{pmatrix}J&R^T\\R&C\end{pmatrix},\quad
 J=G^{-1/2}TG^{-1/2},\quad
 R^TR=G^{-1/2}HG^{-1/2}-J^2.
\]

Their allowable complement blocks are bounded by

\[
 C_L=LI+R(J-LI)^{-1}R^T,\quad
 C_U=UI-R(UI-J)^{-1}R^T.
\]

The functions of J commute, giving

\[
 C_U-C_L=(U-L)\{I-R[(J-LI)(UI-J)]^{-1}R^T\}.
\]

The condition `I-VV^T>=0` is equivalent to `I-V^TV>=0`. Therefore the
last display is PSD exactly when
`R^TR<=(J-LI)(UI-J)`. Substitute the expression for `R^TR`, cancel `J^2`,
and conjugate by `G^(1/2)` to obtain the stated criterion. This proves all
assertions. If some actual A satisfies `LI<A<UI` and `AX=Y`, compatibility
is strict because `X^T(A-LI)(UI-A)X>0`.

These are finite-dimensional instances of classical extremal self-adjoint
extension theory; see Tarcsay and Sebestyén, Theorem2.2 [R1].

## 3. Exact attained unweighted CDF extrema

Let `N_B(t)` count eigenvalues of B **less than or equal to** t, with algebraic
multiplicity. Loewner monotonicity of ordered eigenvalues proves

\[
 \min_{B\in\mathcal C}N_B(t)=N_{B_U}(t),\qquad
 \max_{B\in\mathcal C}N_B(t)=N_{B_L}(t).
\]

The same two matrices attain the extrema at every threshold. This is about
unweighted counts; it does not use the invalid weighted-CDF transfer.

For `L<=t<U`, define d-by-d symmetric pencils

\[
 P_L(t)=H-(t+L)T+LtG,\qquad
 P_U(t)=H-(t+U)T+UtG.
\]

**Theorem 2.** With `n_-`, `n_0`, `n_+` denoting exact inertia,

\[
 N_{B_L}(t)=n-d+n_-(P_L(t))+n_0(P_L(t)),
\]
\[
 N_{B_U}(t)=n_+(P_U(t))+n_0(P_U(t)).
\]

For t<L both counts are zero; for t>=U both are n.

### Proof

`Z_L` has rank d since `X^TZ_L` is invertible. The d nonzero eigenvalues of
`Z_L H_L^(-1) Z_L^T` are those of
`H_L^(-1/2) Z_L^TZ_L H_L^(-1/2)>0`. Its comparison to `(t-L)I`, by
congruence, has the inertia of `Z_L^TZ_L-(t-L)H_L=P_L(t)`. The remaining
n-d eigenvalues of `B_L` equal L. The upper endpoint works identically with
`Z_U=UX-Y`: its d nontrivial eigenvalues are U minus positive eigenvalues,
so the relevant inertia is **nonnegative**, giving the second formula.
Zeros are included exactly as the inclusive convention requires.

**Theorem 3.** Put `r=rank(B_U-B_L)`. The maximum over all thresholds of
the empirical-CDF ambiguity is exactly `r/n`, attained at t=L. If the class
contains a strictly interior A, then `r=n-d`. Pointwise, for `L<=t<U`, the
gap is at least `max(0,n-2d)/n`.

### Proof

A PSD update of rank r moves at most r eigenvalues across any threshold:
restrict the min-max subspaces to its kernel, losing at most r dimensions.
At L, `B_L` has n-d eigenvalues. In the block representation above, the
Schur complement of `B_U-LI` is `C_U-C_L`, of rank r. Hence
`nullity(B_U-LI)=n-d-r`, and the difference of counts at L is r. Strict
interiority gives `B_U>=A>LI`, so that nullity is zero. The pointwise bound
uses `N_BL>=n-d` and `N_BU<=d`, together with monotonicity.

Strictness cannot be dropped: `A=diag(-1,1)`, `X=(1,1)^T`, L=-1,U=1
has positive compressed endpoint forms but `B_L=B_U=A`; r=0 while n-d=1.
The exact rational fixtures include this counterexample.

The possible counts are integers. The endpoints determine the exact interval
hull of possible CDF values, not every real value inside it.

## 4. Binding the calculation to the original exact-decimal input

The actual target is the exact real matrix

\[
 A=M_{\rm mass}^{-1/2}K M_{\rm mass}^{-1/2}/33554432,
 \qquad n=1074.
\]

K and the diagonal mass matrix use their original decimal Matrix Market
values, interpreted as rationals. Positive mass square roots are enclosed by
the unchanged owner loader. It constructs the exact dyadic `Abar` with
denominator `2^32` and proves

\[
 \|A-\bar A\|\le\tau,
 \quad M=2340600979/4294967296,
 \quad\tau=11685898332914907/604462909807314587353088.
\]

Set `S=M+tau`, `L=-S`, `U=S`. This support is for the **original A**, not
the incoming individual completed Jacobi operators; their supports include
their additional completion errors.

X concatenates all eight stored k64 bases, exactly as their integers divided
by `2^29`, giving 512 columns. The joint mathematical transcript is `Y=AX`.
The calculation pays for joint action information; separate J matrices alone
do not supply it. It does not generate probes or additional Krylov steps.

### Strict support

For every connected component of the nonzero graph of `|Abar|`, the exact
maximum absolute row sum is at most M and at least one row is strictly less
than M. Suppose an eigenvalue had modulus M. At a component of an eigenvector
of maximum modulus, triangle equality forces all neighboring eigenvector
moduli to equal that maximum, and the row sum must equal M. Connectedness
propagates this to a deficient row, a contradiction. Thus `||Abar||<M` and
`||A||<M+tau=S`. The checker finds the 1071-vertex component and three
isolated vertices and checks the strict deficiency in each.

### Exact rank despite nearly dependent stored columns

A floating SVD diagnosed condition about `4.0e8`; its output is only a
proposal. Store an exact dyadic preconditioner `C=Cint/2^32`, and form
`Z=XC` by guarded integer products. The exact denominator of Z is `2^61`.
Round it to `W=Wint/2^40`, with an exactly bounded
`delta=||Z-W||F <=1.9459816485648737e-10`. The exact Gram calculation gives
`||W^TW-I|| <=gamma <=2.6866965145035974e-6`.
Consequently `sigma_min(W)>=sqrt(1-gamma)>delta`. Z has full rank, which
also proves that X and C have rank512. This is not a floating rank decision.

### Original-input and coordinate-error bridge for the pencils

For b=L or U and fixed t, let `f_b(A)=A^2-(b+t)A+btI`. Then the exact
congruence-transformed pencil is `Z^T f_b(A)Z`.

Write `w>=||W||`, `z=w+delta>=||Z||`, `||Abar||<=M`, `||A-Abar||<=tau`.
For `E=A-Abar`, the noncommuting identity
`A^2-Abar^2=Abar E+E Abar+E^2` gives

\[
 \|f_b(A)-f_b(\bar A)\|
 \le\tau(2M+\tau+|b+t|).
\]

Expanding the coordinate perturbation separately therefore proves

\[
 \|Z^Tf_b(A)Z-W^Tf_b(\bar A)W\|
 \le z^2\tau(2M+\tau+|b+t|)
 +\delta(2w+\delta)(M+|b|)(M+|t|).
\]

The last product bounds `||f_b(Abar)||` because both factors are polynomials
in the same matrix. Exact integer products compute `W^TW`, `W^TAbar W`,
and `(Abar W)^T(Abar W)`. Quantization of the resulting pencil contributes
its own exact Frobenius allowance. A rounded eigendecomposition supplies a
proposal; the original complete-basis residual verifier certifies its sorted
eigenvalue intervals including **all** these allowances. No solver status is
used as a certificate.

At `t=12983/536870912`, the verified original-input inertias are

| Pencil | Negative | Zero | Positive | Minimum certified distance from zero |
|---|---:|---:|---:|---:|
| P_L | 47 | 0 | 465 | >2.4395208701e-7 |
| P_U | 465 | 0 | 47 | >2.6544178872e-7 |

The total pencil allowances before complete-basis eigenverification are
`6.622379304625443e-8` and `6.621934506265824e-8`; final eigenvalue radii
are `8.177798345891796e-8` and `7.239547521508489e-8`. All exact rational
values are in `results/common_action_producer.json`.

It follows that the exact attained CDF extrema for this joint information
class are `47/1074` and `609/1074`. Their gap is

\[
 \boxed{562/1074=281/537=0.5232774674115456\ldots}.
\]

This is also the exact maximum ambiguity over thresholds by Theorem3.

## 5. Restoring the known symmetric support changes identifiability

The original K has 7,017 independent lower-triangular nonzero coefficients,
including all diagonal entries, and 12,960 expanded nonzeros. Positive mass
scaling does not change the pattern. A graph degeneracy order has at most
eight still-present off-diagonal neighbors per vertex.

**Peeling lemma.** Let `S_i` be vertex i and its still-present neighbors in
an elimination order. If each `X[S_i,:]` has full row rank, the map
`D -> DX` is injective on symmetric matrices supported on that pattern.

**Proof.** In the first row of `DX=0`, all permitted coefficients multiply
linearly independent rows of X, so those coefficients vanish. Symmetry
removes the corresponding column. Apply the same argument inductively to
the next remaining row. Every coefficient vanishes.

This is the symmetric specialization of established exact support-peeling
mechanisms; Musco and Ramesh, Lemma10 and Algorithm1 [R2], is a particularly
close current comparator. No general novelty is claimed for the lemma.

For this input take X9 to be the eight saved starting columns followed by
the second saved column of probe0. Each entry is an exact integer divided by
`2^29`. All1074 local rank obligations pass using nonzero selected minors
modulo the proved prime `2147483647`. A nonzero modular minor proves the
corresponding integer, and hence real, determinant is nonzero. Modular
multiplication and subtraction have explicit int64 bounds. Verification
replays the selected minors rather than searching for a new rank witness.

Thus nine **existing** directions identify every symmetric matrix on the
known pattern from its exact action. This is a uniqueness certificate, not
an implemented numerical reconstruction or a spectral speedup.

### Sharp necessity of nine directions on the actual pattern

The exact 8-core has m=84 vertices, 573 undirected off-diagonal edges and
84 diagonal positions, hence a 657-dimensional space of allowed symmetric
perturbations supported inside the core. The core is independently rebuilt
from the original nonzero decimal data.

For an arbitrary m-by-q query block of rank r, the map from all symmetric
m-by-m matrices to their actions has rank

\[
 mr-r(r-1)/2.
\]

To prove this, rotate the column space of X onto the first r coordinates
and apply an invertible change of query coordinates. The action determines
a symmetric r-by-r leading block and an arbitrary `(m-r)`-by-r block,
giving `r(r+1)/2+(m-r)r` independent parameters.

For any q<=8 the rank is at most `84*8-8*7/2=644`. Its restriction to the
657-dimensional supported subspace therefore has a kernel of dimension
at least13. Extending such a nonzero D by zeros outside the core gives
`DX=0` for the full matrix and preserves the original pattern.

Consequently **no eight exact query directions identify this symmetric
pattern**, while the certified nine directions do. The exact minimum is9.
For a deterministic adaptive sequence, the same kernel argument can be
applied to its realized query transcript: sufficiently small supported
perturbations give identical outputs at every preceding step by induction.
If a norm enclosure is imposed about a strictly interior A, small enough
perturbations remain inside it.

This proves matrix nonidentifiability, not a nonzero CDF gap at the chosen
threshold. Nor is it a distributional lower bound for a fixed A chosen
before randomized queries. The full input is already stored; an algorithm
allowed to read every coefficient is not restricted to this query class.

The initially attempted 9-clique necessity argument failed: an exact graph
check found no such clique. The dimension obstruction above replaces that
failed sufficient criterion; the failure record is retained.

## 6. An explicit sensitivity witness on the actual nine directions

Exact identification is not a finite-precision error certificate. The stored
`witnesses/sparse_noise_direction.npz` defines an exact symmetric D with
denominator `2^40`, supported on the original nonzero positions in the
84-vertex core. A stored dyadic vector of denominator `2^29` provides a
Rayleigh quotient. Exact integer and independent Fraction arithmetic prove

\[
 \|DX_9\|_F\le0.0001201874138736621,
 \qquad\|D\|_2\ge0.9600116062328917,
\]

and, using the exact unrounded ratio in the receipt,

\[
 \boxed{\|D\|_2/\|DX_9\|_F>7987.62179.}
\]

The SVD that proposed D is not part of the acceptance argument. The
independent checker reconstructs every action entry from the pinned saved
columns, verifies every allowed support position against the original
decimal matrix, and recomputes the rational Rayleigh quotient and norms.

Any bound `||D||2 <= C ||DX9||F` valid on this support class must have
`C>7987.62179`. This is an absolute inverse-sensitivity lower bound. It is
neither an inverse upper bound nor exact invisibility nor a proof that the
threshold CDF changes. Query normalization and error norms are part of it.

## 7. A sharp distinction between exact and stable recovery on paths

Let `T_n` be the real symmetric tridiagonal matrices including their
diagonals, n>=2. For an n-by-q query block define

\[
 C_F(X)=\sup_{0\ne D\in\mathcal T_n}\frac{\|D\|_F}{\|DX\|_F},
 \qquad
 C_2(X)=\sup_{0\ne D\in\mathcal T_n}\frac{\|D\|_2}{\|DX\|_F}.
\]

Set the constants to infinity when the map is noninjective. Noise is
absolute Frobenius error in the entire action block. Initially require
**every row of X to have Euclidean norm1**; this fixes the per-row energy
and gives total query energy n for either two or three columns.

**Theorem 4 (sharp two-query Frobenius constant).**

\[
 \boxed{\inf_{X\in\mathbb R^{n\times2},\ \|x_i\|=1} C_F(X)
       =\frac1{\sqrt2\sin(\pi/(2n))}.}
\]

The infimum is attained by alternating rows e1,e2. It grows as
`sqrt(2)*n/pi`, although two columns suffice for exact identification.
Three periodic coordinate-color rows give `C_F=C_2=1`.

### Universal lower bound by an explicit flow

If adjacent rows are dependent, a nonzero vector w on those two vertices
annihilates the restricted X; `ww^T` is a supported invisible perturbation.
Otherwise write `delta_i=det(x_i,x_(i+1)) !=0`. Take real c_i with c_0=c_n=0,
and set

\[
 b_i=c_i/\delta_i,\qquad
 a_i=-b_{i-1}\langle x_i,x_{i-1}\rangle
     -b_i\langle x_i,x_{i+1}\rangle.
\]

Omit missing endpoint terms. Let D have diagonal a and off-diagonal b.
With `J=[[0,-1],[1,0]]`, decompose every neighboring unit vector into its
parallel and perpendicular components relative to x_i. The parallel terms
cancel, and the left determinant is `-delta_(i-1)`, so

\[
 (DX)_{i,:}^T=(c_i-c_{i-1})Jx_i.
\]

Hence `||DX||F^2=sum(c_i-c_(i-1))^2`, whereas
`||D||F^2=sum a_i^2+2sum b_i^2>=2sum c_i^2`, since `|delta_i|<=1`.
Choose `c_i=sin(pi*i/n)`. The discrete Dirichlet eigenvector identity gives

\[
 \sum_{i=1}^n(c_i-c_{i-1})^2
 =4\sin^2(\pi/(2n))\sum_{i=1}^{n-1}c_i^2.
\]

It follows either by summation by parts or by multiplying
`2c_i-c_(i-1)-c_(i+1)=2(1-cos(pi/n))c_i` by c_i and summing. This proves
the universal lower bound against **all** dense unit-row two-query blocks.

### Attainment and the three-query operation

For alternating e1,e2 rows, diagonal and off-diagonal outputs occupy
different coordinates. Let T be the unsigned n-by-(n-1) path incidence
matrix. Then `||DX||F^2=||a||^2+||Tb||^2`, while
`||D||F^2=||a||^2+2||b||^2`. The Gram matrix `T^TT` has diagonal2 and
off-diagonal1. Its sine eigenvectors give eigenvalues
`2+2cos(j*pi/n)`, j=1,...,n-1, whose minimum is `4sin^2(pi/(2n))`.
The optimal ratio is therefore exactly the displayed constant (at least1
for n>=2). An alternating-sign sine b, with a=0, attains it.

For three rows cycling e1,e2,e3, a vertex and its two neighbors always have
different colors. Every coefficient occupies a separate action coordinate,
so `||DX3||F^2=sum a_i^2+2sum b_i^2=||D||F^2`. A single diagonal
coefficient gives the matching inverse lower bound1. At n=2 two queries
already give1; three is the uniformly stable budget for the growing family.

Choosing instead `c_i=min(i,n-i)` in the universal flow, and putting
`m=floor(n/2)`, gives `||DX||F^2=2m`, `||D||2>=max|b_i|>=m`. Therefore
`C_2(X)>=max(1,sqrt(m/2))`. Even the operator-norm inverse constants of
unit-row two-query schemes cannot be bounded independently of n.

Halikias and Townsend [R3] already give the alternating two-query exact
recovery and periodic coordinate design. The positive coloring mechanism
is classical. The bounded primary search did not establish historical
novelty of the minimax conditioning formula; no priority claim is made.

## 8. Row-cap extension, its failed sharp conjecture, and forests

The sharp formula above does **not** remain true if the requirement is only
`||x_i||<=1`. For n=4 choose rows `(4/5,0),(0,1),(1,0),(0,4/5)`.
The off-diagonal action Gram has diagonal `(41/25,2,41/25)` and
off-diagonal `4/5`. Its smallest eigenvalue is
`(91-sqrt(3281))/50`. Therefore

\[
 C_F(X)^2=(91+\sqrt{3281})/50<2+\sqrt2,
\]

strictly smaller than the unit-row optimum squared. The diagonal recovery
constant squared is25/16 and does not dominate. This exact counterexample
retires the attempted monotone row-scaling argument.

A weaker universal instability result survives. If no row is zero, write
`X=R U`, with `r_i=||x_i||`, `r_min=min r_i` and U having unit rows.
For any supported D' let `D=R^(-1)D'R^(-1)`. Then
`DX=R^(-1)D'U`, and `||DX||F<=||D'U||F/r_min`. Since all r_i<=1,
`||D||F>=||D'||F`; also `D'=RDR` gives `||D||2>=||D'||2`.
A single diagonal entry separately gives both inverse constants at least
`1/r_min`. It follows that

\[
 C_F(X)\ge\max\{1/r_{\min},\ r_{\min}/[\sqrt2\sin(\pi/(2n))]\}
 \ge [\sqrt2\sin(\pi/(2n))]^{-1/2},
\]

\[
 C_2(X)\ge\max\{1,\,[\lfloor n/2\rfloor/2]^{1/4}\}.
\]

Zero rows or dependent adjacent rows give noninjectivity. Thus no two-query
scheme with per-row energy at most1 has a dimension-independent inverse
constant on all paths. These row-cap bounds are not claimed sharp, and
a mere total-energy constraint without a row cap is a different problem.

**Theorem 5 (forest operation).** For any known forest, root each component
and choose `X3[v,:]=e_(depth(v) mod3)`. For every symmetric matrix D on its
edges and diagonal, writing `b_v=D[v,parent(v)]` for nonroots,

\[
 \|DX_3\|_F^2
 =\sum_v D_{vv}^2+\sum_{v\ne root} b_v^2
   +\sum_v\left(\sum_{w:parent(w)=v}b_w\right)^2.
\]

In particular `||D||F<=sqrt(2)||DX3||F`. Each diagonal is read from its
own-color coordinate, and each edge is read from the child's parent-color
coordinate. Parent, self, and child colors are distinct, proving the
identity and the direct recovery rule. The constant sqrt2 is sharp for
this design at a vertex with two children: opposite edge coefficients
cancel the child sum. On an endpoint-rooted path each vertex has at most
one child and the identity is an isometry.

For measured action `DX3+E`, this actual direct-read algorithm produces
`Dhat` with `||Dhat-D||F<=sqrt2||E||F`, hence the same operator bound.
Indeed its error energy is a sum of selected squared entries of E, with
weights1 on diagonals and2 on edges. The executable operation is
`src/forest_recovery.py`. Forest construction and recovery require O(n)
work and storage, plus the cost of **three actual matrix actions**. It
does not hide their acquisition, input uncertainty, or downstream spectrum
computation. No new actions or target benchmarks were run for this theorem.

Together with the path lower bound, three is the minimum fixed number of
queries permitting uniformly stable recovery for all forests under the
per-row energy cap and these absolute error norms. Two suffice for exact
identification of nontrivial forests with a suitable generic block.
This contrasts exact identification with stability; it does not assert
an automatic advantage on the fully stored NIST problem.

The forest seed is a star coloring, an established direct-recovery mechanism.
Gebremedhin et al. [R4], especially section3.3, also analyze error propagation
in the different acyclic/tree-substitution method. Their result and the
query-optimality references prevent attributing the positive constructions
to this checkpoint as historical inventions.

## 9. Scientific and computational scope

1. The joint completion result concerns the defined action-and-support
   class, which omits exact sparsity, trace and other possible information.
   It is not an impossibility result about the fully specified original A.
2. The nine-query theorem retains known symmetric support. It establishes
   exact identification, without claiming finite-precision reconstruction.
3. The actual perturbation gives a lower sensitivity bound under fixed
   query scaling and norms. It supplies no CDF crossing or inverse upper bound.
4. The path and forest theorems use an explicit action-error norm and energy
   constraint. They are structural mathematics, not a substituted performance
   benchmark and not a proof about the actual matrix's query conditioning.
5. Exact integer/Fraction acceptance, complete-basis residuals and source
   hashes are the certificate layer. Floating SVD/eigh results are proposals.
6. All numerical attempts and independent checks are charged in `COSTS.md`.
   The old verified dense computation remains the practical incumbent.

## Primary references

[R1] Z. Tarcsay and Z. Sebestyén, *Reduction of positive self-adjoint
extensions*, Opuscula Mathematica44(3),425-438 (2024), Theorem2.2.
DOI: https://doi.org/10.7494/OpMath.2024.44.3.425.
Primary manuscript: https://real.mtak.hu/175242/1/Opuscula-1(1).pdf.

[R2] C. Musco and I. Ramesh, *Nearly Instance Optimal Sparse Matrix
Approximation from Matrix-Vector Products*, ESA2026, LIPIcs388,85:1-14,
Lemma10, Algorithm1 and its approximation caveat.
https://doi.org/10.4230/LIPIcs.ESA.2026.85.

[R3] D. Halikias and A. Townsend, *Structured matrix recovery from
matrix-vector products*, Numerical Linear Algebra with Applications31(1),
e2531 (2024), section2.1.3.
https://arxiv.org/abs/2212.09841; https://arxiv.org/pdf/2212.09841.

[R4] A. H. Gebremedhin, A. Tarafdar, A. Pothen and A. Walther,
*Efficient Computation of Sparse Hessians Using Coloring and Automatic
Differentiation*, INFORMS Journal on Computing21(2),209-223 (2009).
https://doi.org/10.1287/ijoc.1080.0286.
Primary manuscript: https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf.

[R5] X. Sun, D. P. Woodruff, G. Yang and J. Zhang, *Querying a Matrix
through Matrix-Vector Products*, ICALP2019. Used only to distinguish
deterministic transcript obstructions from randomized fixed-input claims.
https://doi.org/10.4230/LIPIcs.ICALP.2019.94.

[R6] M. O. Albertson, G. G. Chappell, H. A. Kierstead, A. Kündgen and
R. Ramamurthi, *Coloring with no 2-colored P4's*, Electronic Journal of
Combinatorics11 (2004), R26, Theorems6.1 and6.3. The former, attributed
there to Fertin, Raspaud and Reed, gives binomial(t+2,2) star colors for
treewidth t; the latter proves this star-coloring bound sharp.
https://www.combinatorics.org/ojs/index.php/eljc/article/viewFile/v11i1r26/pdf/.
For treewidth2 it gives six query colors. Each coefficient is isolated in
a distinct action coordinate at one end of its bichromatic star, so the
direct recovery error is at most sqrt2 times Frobenius action error.
This already settles existence of a size-independent stable query budget;
the chosen continuation concerns whether three arbitrary dense queries
can suffice. Star-coloring lower bounds do not settle that stronger class.

Further source access, failed retrievals and the bounded novelty search are
recorded in `notes/*literature*.md`. The proofs above are complete without
assuming that a numerical solver returned success or that a search's failure
to find an earlier theorem establishes novelty.
