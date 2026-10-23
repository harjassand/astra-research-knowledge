# Independent audit: exact-input full-spectrum comparator

Agent: `residual_challenge`  
Scope: check the ordinary complete-eigendecomposition comparator, not introduce another scientific programme.  
Status: **PASS**, with a stronger residual-only enclosure using the same main checked objects.

## 1. Inputs and guarantee

Let the intended target `A` and stored dyadic matrix `Abar` be real symmetric n by n matrices, with a proved bound

\[
\|A-\bar A\|_2\le\tau.
\]

Let `V` be a finite dyadic n by n matrix and `D` a real dyadic diagonal matrix. The diagonal entries of `D` need not initially be sorted. All checks below refer to these exact stored numbers; floating eigensolver termination is not part of the proof.

Write

\[
G=V^TV,\qquad R=\bar A V-VD.
\]

The supplied proposal assumes certified nonnegative bounds

\[
\|G-I\|_F\le\gamma<1,\quad
\|R\|_F\le r_0,\quad
\|\bar A\|_2\le M,\quad\|D\|_2\le K.
\]

In particular, `V` is invertible and

\[
\sigma_{\min}(V)\ge\sqrt{1-\gamma}>0.
\]

The resulting certificate bounds the complete empirical spectral CDF

\[
F_A(t)=\frac1n\#\{i:\lambda_i(A)\le t\}
\]

deterministically and simultaneously for every real threshold `t`.

## 2. The proposed polar theorem is correct

Set

\[
Q=VG^{-1/2},\qquad
d=\frac{\gamma}{1+\sqrt{1-\gamma}},\qquad
B=QDQ^T.
\]

Since `V` is square and invertible, `Q` is orthogonal. If its singular values are `sigma_j`, then

\[
\|Q-V\|_F^2
=\sum_j(\sigma_j-1)^2
=\sum_j\frac{(\sigma_j^2-1)^2}{(\sigma_j+1)^2}
\le d^2.
\]

The denominator bound uses `sigma_j >= sqrt(1-gamma)`, and the numerator sum is `||G-I||_F^2`.

Now

\[
(\bar A-B)Q=\bar A Q-QD
=R+\bar A(Q-V)-(Q-V)D.
\]

Orthogonal invariance and the norm inequalities give

\[
\|\bar A-B\|_2
\le \|\bar A Q-QD\|_F
\le r_0+(M+K)d=:r.
\]

Thus `||A-B||_2 <= tau+r`. The eigenvalues of `B` are precisely the diagonal entries of `D`, with multiplicities. Weyl's inequality proves the proposed sorted enclosures with radius `e=tau+r`. This proof requires no simple eigenvalues, eigengaps, total positivity, or matching of individually computed eigenvectors to exact eigenvectors.

The polar factor is a proof device: it need not be numerically formed or certified separately.

## 3. Stronger full-spectrum theorem: omit the polar-correction term

### Statement

For any real symmetric `Abar`, real diagonal `D`, and invertible square `V`, let

\[
m\le\sigma_{\min}(V),\qquad m>0,\qquad
\rho\ge\|\bar A V-VD\|_2.
\]

Then, with both eigenvalue lists sorted in nondecreasing order,

\[
\boxed{\max_i|\lambda_i(\bar A)-d_i|\le\rho/m.}
\]

In fact the same radius bounds the particular polar completion:

\[
\boxed{\|\bar A-QDQ^T\|_2\le\rho/m,\qquad Q=V(V^TV)^{-1/2}.}
\]

Thus the parent's `operator_error` field can retain its literal operator-norm meaning, even when the smaller residual-only radius is selected.

Consequently the same supplied bounds give the alternative radius

\[
\boxed{e=\tau+\frac{r_0}{\sqrt{1-\gamma}}.}
\]

Both radius formulas are sound; their minimum is also sound. No claim of historical novelty is made. This lemma is only a stronger way to certify the ordinary full-spectrum comparator.

### Short proof for the particular polar completion

Write `V=QH`, where `Q` is orthogonal and `H=(V^TV)^(1/2) >= m I`. Set

\[
C=Q^T\bar A Q,\qquad E=Q^TR=CH-HD,\qquad X=C-D.
\]

Both `C` and `D` are symmetric. Therefore

\[
E+E^T=CH-HD+HC-DH=XH+HX.
\]

Since `H>=mI>0`, the convergent Lyapunov integral gives

\[
X=\int_0^\infty e^{-tH}(E+E^T)e^{-tH}\,dt.
\]

Differentiating `e^{-tH}X e^{-tH}` and integrating verifies the identity. Consequently

\[
\|X\|_2\le\int_0^\infty e^{-2mt}\,2\|E\|_2\,dt
=\|E\|_2/m\le\rho/m.
\]

Because `Abar-QDQ^T=QXQ^T`, this is the claimed operator bound. Weyl immediately gives the sorted eigenvalue bound. The proof also works with the Frobenius norm, using its orthogonal invariance and the same integral estimate. No numerical formation of `H` or `Q` is required by the checker.

### Independent direct proof for sorted eigenvalues

Permute columns of `V` together with the entries of `D` so that `d_1 <= ... <= d_n`. This preserves every singular value and residual norm. Choose an orthogonal eigenbasis of `Abar`, ordered so that

\[
U^T\bar A U=\Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_n),
\quad\lambda_1\le\cdots\le\lambda_n.
\]

Let `W=U^TV` and `H=U^TR=Lambda W-WD`. Then `sigma_min(W)>=m` and `||H||_2<=rho`.

Fix an index `i` and first suppose `delta=lambda_i-d_i>0`. Let

\[
C=W_{\{i,\ldots,n\},\{1,\ldots,i\}},\qquad
T=H_{\{i,\ldots,n\},\{1,\ldots,i\}}.
\]

**Lower bound on the rectangular block.** The complementary block `W_{1:i-1,1:i}` has `i` columns and only `i-1` rows, so it has a unit vector `y` in its kernel. Extend `y` by zeros to an n-vector `x`. The first `i-1` coordinates of `Wx` vanish, and its remaining coordinates equal `Cy`. Hence

\[
\|C\|_2\ge\|Cy\|_2=\|Wx\|_2\ge m.
\]

This is the step that uses completeness and invertibility of the full square matrix `V`.

**Upper bound from separated spectral blocks.** Set

\[
L=\Lambda_{i:n,i:n}-d_iI\succeq\delta I,\qquad
S=D_{1:i,1:i}-d_iI\preceq0.
\]

The block residual equation is `LC-CS=T`. Its convergent integral solution is

\[
C=\int_0^\infty e^{-sL}T e^{sS}\,ds.
\]

To check the identity, differentiate `e^{-sL}C e^{sS}` and integrate; its value tends to zero at infinity because `L >= delta I` and `S <= 0`. Therefore

\[
\|C\|_2
\le\int_0^\infty e^{-s\delta}\|T\|_2\,ds
\le\rho/\delta.
\]

Combining the lower and upper bounds gives `lambda_i-d_i=delta<=rho/m`.

If `d_i-lambda_i>0`, take instead rows `1:i` and columns `i:n`. The complementary row block has one fewer row than the number of selected columns, so the identical kernel argument gives norm at least `m`. This time the selected `D` block lies entirely above the selected `Lambda` block; the same integral applied with the sides reversed gives `d_i-lambda_i<=rho/m`. A zero gap needs no argument.

This proves the claimed sorted enclosure. Applying Weyl once to `A` versus `Abar` adds `tau`.

### Scope and sharpness

The result concerns sorted eigenvalues and their multiplicities, not matching particular approximate eigenvectors. It does not require any spectral separation in the input: a positive putative sorted gap is used only inside the contradiction/bounding argument.

The factor `1/m` cannot be reduced universally: take dimension one, with `V=[v]`, `v!=0`. Then `||Abar V-VD||_2/sigma_min(V)=|Abar-D|` exactly. This is not a claim that the Frobenius residual bound is tight in higher dimensions.

The theorem cannot simply be applied to an incomplete rectangular Krylov basis. The full square invertibility premise is essential to the block lower bound. It supplies no alternate justification for the per-probe spectral-transfer step in the SLQ construction.

## 4. Cheaper exact norm accumulation using the same matrix products

A safe variant avoids squared-entry accumulation for both the Gram and residual norm budgets. Compute exact or outward-enclosed entries of `G` and `R`, and obtain

\[
\eta=\min_i\left(G_{ii}-\sum_{j\ne i}|G_{ij}|\right)>0,
\]

or any certified positive lower bound on that expression. Gershgorin gives `lambda_min(G)>=eta`, so `sigma_min(V)>=sqrt(eta)`. Next compute certified upper bounds

\[
p\ge\|R\|_1=\max_j\sum_i|R_{ij}|,\qquad
q\ge\|R\|_\infty=\max_i\sum_j|R_{ij}|.
\]

Then `||R||_2 <= sqrt(p q)` and

\[
\boxed{e=\tau+\sqrt{pq/\eta}}
\]

is sound. If an exact/outward bound `f >= ||R||_F^2` is already available, replace `pq` by `min(pq,f)`. If `gamma` is also checked, `eta` may be replaced by the larger of its certified lower bounds `eta` and `1-gamma`.

All these are scalar checks after the same main products `V^TV` and `Abar V`. Row/column absolute sums can reduce big-integer squaring and square-root bookkeeping, but they do **not** eliminate the dense Gram product. There is no demonstrated runtime saving until measured. A negative Gershgorin lower bound means this particular bound is inconclusive, not that `V` is singular.

For dense `V`, forming `G` remains cubic arithmetic and quadratic storage. With sparse `Abar`, the residual product has arithmetic proportional to `nnz(Abar)*n`, plus diagonal scaling/subtraction and accumulation. Exact bit complexity, numerical eigensolver time, original-input interval construction, rejected checks, and any independent replay remain chargeable by the parent experiment.

## 5. CDF endpoints, degeneracy, and exact evaluation

For any certified radius `e`, including either theorem above,

\[
d_i-e\le\lambda_i(A)\le d_i+e.
\]

Therefore the correct inclusive-CDF formulas are

\[
\boxed{\frac1n\#\{i:d_i+e\le t\}
\le F_A(t)\le
\frac1n\#\{i:d_i-e\le t\}.}
\]

For the lower bound, each `d_i+e<=t` forces `lambda_i(A)<=t`. For the upper bound, `lambda_i(A)<=t` forces `d_i-e<=t`. These implications remain true at equality and with repeated eigenvalues. Thus no strict-versus-nonstrict adjustment is required for this CDF convention. For a strict CDF defined with `<`, both displayed counting comparisons must instead use `<`.

The counts may use unsorted `D`; sorting is only needed to express the eigenvalue matching theorem and to evaluate many thresholds efficiently. No stochastic confidence allocation, probe-normalization correction, or simultaneous-threshold union bound is needed.

If a radius contains square roots, the checker may use a rational/dyadic outward upper enclosure `e_plus`. Then use exact comparison of stored `d_i +/- e_plus` with the intended threshold. A floating value of the radius rounded inward is not a certificate. The two staircase functions with outward endpoints specify the guarantee at every real threshold, not merely a grid of thresholds.

## 6. Exact generalized structural matrix boundary

For the parent's structural example, distinguish the stiffness matrix from a norm bound and write

\[
A=s\,M_{\rm mass}^{-1/2}K_{\rm stiff}M_{\rm mass}^{-1/2},
\qquad M_{\rm mass}=\operatorname{diag}(m_i),\quad m_i>0.
\]

The original public decimal coefficients, their symmetric interpretation, the diagonal mass coefficients, and the scale `s` define the target. The dyadic `Abar` must be related to that exact target by outward interval construction; merely certifying an eigendecomposition of `Abar` would be insufficient.

If the target and `Abar` are symmetric and certified numbers `aerr_ij` satisfy `|A_ij-Abar_ij|<=aerr_ij`, then

\[
\tau=\max_i\sum_j\mathrm{aerr}_{ij}
\]

is a valid operator-norm allowance. This follows from the maximum absolute row-sum bound for the eigenvalues of a symmetric error matrix. There is no additional factor two when `aerr_ij` already bounds the actual full-matrix entry error. Mass positivity and all errors from inverse square roots, coefficient conversion, symmetric assembly, and scale conversion belong in that construction.

The present result certifies eigenvalues of this stated finite matrix. Transforming them into physical frequencies requires the appropriate nonnegative spectral premise and the specified units/scaling; this lemma alone does not establish those additional claims.

## 7. Audit record

This is an independent mathematical audit and improvement of the proposed comparator error budget. It uses no new numerical sweep, no eigensolver run, and no claim of a faster achieved runtime. The proof above is the substantive result. Parent retains ownership of exact-integer implementation, public-input construction, actual cost accounting, and comparison with SLQ.
