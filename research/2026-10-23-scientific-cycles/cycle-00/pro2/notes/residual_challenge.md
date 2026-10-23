# Independent challenge of the residual completion

Date: 21 October 2026. Scope: the finite dimensional algebraic link from a stored, imperfect Krylov basis and a tridiagonal matrix to an exact Gaussian quadrature problem. This is a local proof review and strengthening, not a separate spectral programme or a historical novelty claim.

## Conclusion

The proposed completion is valid. The original bound

\[
\|B-\bar A\|\le \sqrt{2r^2+z^2}+r
\]

is conservative because it allocates the same first-column residual separately to two orthogonal components. A Pythagorean argument immediately removes the final `+r`. A sharper, optimal bound using only the two stated scalar budgets is

\[
\boxed{\|B-\bar A\|\le \mathcal E(r,z)
       :=\frac{z+2\sqrt{z^2+3r^2}}{3}.}
\]

Here `r` bounds the Frobenius norm of the recurrence residual in the first `k-1` columns after orthonormalisation, and `z` bounds the last diagonal mismatch. The same explicit completion attains this sharp worst-case bound already in dimension two. This does not establish that the resulting bound is the minimum possible backward error for a particular input: it is sharp for the chosen completion given only these two budgets.

## 1. Hypotheses and quantities that must actually be bounded

Let \(\bar A\in\mathbb R^{n\times n}\) be symmetric and let \(V\in\mathbb R^{n\times k}\), with \(1\le k\le n\), have full column rank. Let \(J\in\mathbb R^{k\times k}\) be symmetric tridiagonal. For the Gaussian-quadrature conclusion with exactly `k` distinct nodes, assume every subdiagonal entry of `J` is nonzero. The condition is vacuous for `k=1`.

Suppose the reported numbers are valid mathematical upper bounds:

\[
\|\bar A\|_2\le M,\quad \|J\|_2\le K,\quad
\|V^T V-I\|_F\le\gamma<1.
\]

Put

\[
G=V^T V,\quad Q=VG^{-1/2},\quad
P=I-e_ke_k^T,\quad
d=\frac{\gamma}{1+\sqrt{1-\gamma}}.
\]

For `v_k=Ve_k`, assume

\[
r_0\ge\|(\bar A V-VJ)P\|_F,
\qquad \xi\ge|J_{kk}-v_k^T\bar A v_k|.
\]

Define

\[
r=r_0+(M+K)d,\qquad
z=\xi+Md(1+\sqrt{1+\gamma}).
\]

For `k=1`, use `r=0` directly: `P=0`, so there is no first-column recurrence residual to bound. The displayed generic formula remains safe but needlessly loose in that case.

All square roots and scalar operations in a numerical checker need outward enclosures. A floating value of a norm, a factorisation's success status, or a nearby-looking recurrence does not itself establish these hypotheses.

## 2. Polar correction

Write the singular values of `V` as \(\sigma_i\). Since
\(\|G-I\|_2\le\|G-I\|_F\le\gamma\),

\[
\sqrt{1-\gamma}\le\sigma_i\le\sqrt{1+\gamma}.
\]

The polar factor `Q` has orthonormal columns. Its Frobenius distance from `V` satisfies

\[
\begin{aligned}
\|Q-V\|_F^2
 &=\sum_i(1-\sigma_i)^2\\
 &=\sum_i\frac{(1-\sigma_i^2)^2}{(1+\sigma_i)^2}\\
 &\le\frac{\|G-I\|_F^2}{(1+\sqrt{1-\gamma})^2}
 \le d^2.
\end{aligned}
\]

Thus both the Frobenius and operator norms of `Q-V` are bounded by `d`. This is valid for arbitrary full-rank `V`, without a random-matrix or regular spectral-density assumption.

## 3. Recurrence and last-diagonal budgets after polar correction

Let

\[
Y=\bar A Q-QJ.
\]

Then

\[
YP=(\bar A V-VJ)P+
     (\bar A(Q-V)-(Q-V)J)P,
\]

so \(\|YP\|_F\le r\).

For `q_k=Qe_k`, use \(\|q_k\|=1\),
\(\|v_k\|\le\sqrt{1+\gamma}\), and
\(\|q_k-v_k\|\le d\) to obtain

\[
\begin{aligned}
|J_{kk}-q_k^T\bar A q_k|
&\le \xi+
 |v_k^T\bar A v_k-q_k^T\bar A q_k|\\
&\le \xi+M\|v_k-q_k\|(\|v_k\|+\|q_k\|)
\le z.
\end{aligned}
\]

These are the only two budgets needed for the sharp completion bound below.

## 4. The explicit self-adjoint completion

Set

\[
D=J-Q^T\bar A Q,\qquad
R=(I-QQ^T)\bar A QP,
\]

and

\[
E=QDQ^T-RQ^T-QR^T,\qquad B=\bar A+E.
\]

`D` is symmetric, `Q^T R=0`, and `Re_k=0`. Consequently `E` and `B` are symmetric. Direct multiplication, using `R^T Q=0`, gives

\[
\begin{aligned}
BQ
 &=\bar A Q+QD-R\\
 &=QJ+(I-QQ^T)\bar A Q-R\\
 &=QJ+r_*e_k^T,
\qquad r_*=(I-QQ^T)\bar A q_k.
\end{aligned}
\]

The remaining last-column vector satisfies `Q^T r_*=0`. Its norm does not enter the backward error, because a Lanczos recurrence is allowed to have an arbitrary coupling from its last retained vector into the omitted complement. This is exactly the distinction between an allowed truncation residual and errors in the earlier recurrence columns.

### A simple improvement by orthogonal residual splitting

The components of `YP` in `range(Q)` and its orthogonal complement are `-QDP` and `R`, respectively. Hence

\[
\|YP\|_F^2=\|DP\|_F^2+\|R\|_F^2\le r^2.
\]

In a basis extending `Q`, the completion has block form

\[
E\simeq\begin{pmatrix}D&-R_\perp^T\\-R_\perp&0\end{pmatrix}.
\]

Writing `D_11` for the leading `(k-1)`-square block, symmetry gives

\[
\begin{aligned}
\|E\|_F^2
 &=\|D\|_F^2+2\|R\|_F^2\\
 &=2\|DP\|_F^2+D_{kk}^2-\|D_{11}\|_F^2+2\|R\|_F^2\\
 &\le 2r^2+z^2.
\end{aligned}
\]

Thus \(\|E\|_2\le\sqrt{2r^2+z^2}\), already stronger than the originally proposed triangle bound.

## 5. Sharp two-budget operator bound

Decompose the ambient space as

\[
S=\operatorname{span}\{Qe_1,\ldots,Qe_{k-1}\},\qquad S^\perp.
\]

Because `Re_k=0`, the completion has the form

\[
E=\begin{pmatrix}D_{11}&C^T\\C&D_{kk}qq^T\end{pmatrix},
\]

where `q` is the coordinate vector of `q_k` in `S^perp`. The off-diagonal block `C` combines the last row of `DP` and the complement residual. The previous Pythagorean identity says

\[
\|D_{11}\|_F^2+\|C\|_F^2=\|YP\|_F^2\le r^2.
\]

For any unit vector \(x=(u,v)\), let \(s=\|u\|^2\); then \(\|v\|^2=1-s\). Frobenius Cauchy–Schwarz applied jointly to `D_11` and `C` yields

\[
\begin{aligned}
|x^TEx|
 &\le |u^TD_{11}u+2v^TCu|+z\|v\|^2\\
 &\le r\sqrt{\|uu^T\|_F^2+4\|vu^T\|_F^2}+z(1-s)\\
 &=r\sqrt{4s-3s^2}+z(1-s).
\end{aligned}
\]

If \(y=s-2/3\), the final expression is

\[
z/3-zy+r\sqrt{4/3-3y^2}.
\]

Its maximum over `0<=s<=1` is

\[
\mathcal E(r,z)=\frac{z+2\sqrt{z^2+3r^2}}{3}.
\]

For `r>0`, it occurs at

\[
s_*=\frac23-\frac{2z}{3\sqrt{z^2+3r^2}},
\]

which lies in `(0,2/3]`. The `r=0` case gives `e=z` directly. Taking the supremum of `|x^T E x|` proves the operator-norm bound.

### Sharpness

For `r>0`, put \(f=\sqrt{4s_*-3s_*^2}\) and define

\[
a=rs_*/f,\qquad b=2r\sqrt{s_*(1-s_*)}/f,
\qquad E_* =\begin{pmatrix}a&b\\b&z\end{pmatrix}.
\]

Then `a^2+b^2=r^2`, and the unit vector
\((\sqrt{s_*},\sqrt{1-s_*})\) has Rayleigh quotient
\(\mathcal E(r,z)\). The bound already proved shows that this is the operator norm. To realise this example within the completion theorem, take `n=k=2`, `V=Q=I`, choose any irreducible symmetric tridiagonal `J`, and set `Abar=J-E_*`. Then the first-column residual has norm `r`, the last-diagonal mismatch is `z`, and the explicit completion equals `E_*`.

In particular, at `z=r` one can take

\[
E_*=r\begin{pmatrix}1/3&2\sqrt2/3\\2\sqrt2/3&1\end{pmatrix},
\qquad \|E_*\|=5r/3.
\]

At `z=0`, the sharp bound is `2r/sqrt(3)`; at `r=0`, it is `z`. These are useful tests against inadvertently dropping too much of the error budget.

## 6. Why the exact recurrence gives Gaussian quadrature

Let `q_1=Qe_1`. Tridiagonality implies
\(e_k^T J^j e_1=0\) for `0<=j<k-1`. Induction in the exact recurrence therefore gives

\[
B^j q_1=QJ^j e_1,\qquad 0\le j\le k-1.
\]

For every integer `0<=ell<=2k-2`, choose `a,b<=k-1` with `a+b=ell` and use self-adjointness:

\[
q_1^T B^\ell q_1
 =(B^a q_1)^T(B^b q_1)
 =e_1^T J^\ell e_1.
\]

For the final degree, since `Q^T BQ=J`,

\[
q_1^T B^{2k-1}q_1
 =(B^{k-1}q_1)^T B(B^{k-1}q_1)
 =e_1^T J^{2k-1}e_1.
\]

Thus the spectral measures `(B,q_1)` and `(J,e_1)` agree on all polynomials of degree at most `2k-1`. An irreducible real symmetric tridiagonal matrix has `k` distinct real eigenvalues and nonzero first component in every eigenvector: if a first component were zero, the eigenvector recurrence would force all components to vanish. Its spectral weights at `e_1` are therefore positive and sum to one. These nodes and weights give the `k`-node Gaussian quadrature rule for the spectral measure of `(B,q_1)`.

This argument includes happy breakdown `r_*=0`, when the retained subspace is invariant and the quadrature measure is the exact full probe measure. It also includes `k=1`, where moments zero and one match, and `k=n`, where the omitted complement is zero. No artificial nonzero last residual is required.

## 7. Target matrix and intended probe

If the intended exact target `A` obeys \(\|A-\bar A\|\le\tau\), then

\[
\|A-B\|\le\tau+\mathcal E(r,z).
\]

The matrix `B` may depend arbitrarily on the observed probe and numerical proposal. This deterministic assertion does not make `B` independent of the random probe. Any stochastic concentration theorem must still be applied to the fixed original `A`.

Let `u` be the intended **unit** probe. For any orthogonal projector `T`,

\[
|u^T T u-q_1^T Tq_1|
\le \sqrt{1-|u^Tq_1|^2}
\le\|u-q_1\|
\le\|u-Ve_1\|+d.
\]

The first inequality follows by diagonalising the trace-zero rank-two operator
`uu^T-q_1 q_1^T`, whose nonzero eigenvalues are plus and minus
`sqrt(1-|u^T q_1|^2)`. It applies to any effect `0<=T<=I`, including each CDF spectral projector. The constant one relies on unit-normalised probes and the effect/projector condition; for a general signed operator of norm one, the corresponding trace-duality bound has a factor two. Clip the bound at one if desired.

## 8. Evidence and limits

`checks/check_residual_construction.py` contains three exact rational checks of the `z=r` sharpness identities, the zero-diagonal limiting identities, and 396 bounded floating matrix examples. The examples cover `k=1`, `k=n`, nonorthogonal stored bases, recurrence reconstruction, moments through degree `2k-1`, and intended-probe errors.

The observed largest exact-parameter operator-bound discrepancy in floating arithmetic was `1.6653345369377348e-16`; the largest recurrence residual was `2.029501450266695e-15`; the largest moment discrepancy was `1.9984014443252818e-15`. The inflated reported budgets had a strictly negative maximum excess. These diagnostics support the algebraic implementation and are not substitutes for the proof.

Recorded checker body: 0.13952912700005982 seconds wall, 0.677869994 seconds CPU. Peak native RSS was 24560 KiB on Linux, or 25149440 bytes, including imported runtime state. Tool startup, analytical reasoning and file-writing costs are outside that process-body receipt.

The note does not establish the correctness of a particular numerical `gamma`, `r_0`, `xi`, `M`, `K` or `tau`; those must be checked by the parent implementation. It does not validate a Gaussian generator, certify a practical speedup, or establish historical priority. Its positive result is the explicit exact completion and the sharp error bound under the stated checked hypotheses.
