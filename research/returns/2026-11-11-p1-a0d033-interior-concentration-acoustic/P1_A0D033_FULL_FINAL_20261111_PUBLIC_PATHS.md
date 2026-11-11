# P1 completed return — a0d03311

Same Pro chat: https://chatgpt.com/c/6af2bc39-2f58-83ec-b26b-3a99e1d2c0f2
Prompt: P1_FULL_ORIGINAL_QUARTIC_AFTER_CONCENTRATION_REMOVAL_PRO_20261111.txt, SHA-256 733cdb90e9b9b2fbc69a6aa40bb801bc56506d71930eb408c3df2e271d0391a2. Native final returned in full (12,562 characters, no truncation flag); UI ending was observed. Current expanded activity and helper panels were not captured; a visible ZIP is not collected because its identity/hold status is not established. No individual file, held library or archive was accessed. No literal database-byte identity is claimed.

**I have not resolved the full original inequality.** This continuation gives neither a proof for every \(k>1/3\) nor an actual compatible field with a negative original gap. It also does not enlarge the accepted unrestricted large-\(k\) range.

The strongest result obtained here is a **conditional concentration theorem at an interior quasiconvex parameter**. I also obtained an exact two-square factorization of the lower-endpoint constrained acoustic Hessian. The subsequent calculations retain terms whose sign or sharp bound is still unpaid.

The complete proofs, independent audits, symbolic code and execution receipt are saved in:

- :chatgpt-content-reference{index="1"}[SHARP_COMPARISON_AND_BOUNDARY_RESULTS.txt](sandbox:/workspace/scratch/21b466b728a1/SHARP_COMPARISON_AND_BOUNDARY_RESULTS.txt)
- [:chatgpt-content-reference{index="0"}](https://chatgpt.com/library?file_id=libfile_6d1aa4e4e9f08191bc79875c2b2752c0&account_id=personal)

## 1. A proved consequence at an interior quasiconvex parameter

Write
\[
\mathcal E_k(A,\phi)
=\int_{\mathbb T^2}J_k(A+D\phi)-J_k(A).
\]

The following statement applies to the **original density**.

### Theorem

Let \(K\Subset(1/3,\infty)\) be a compact parameter interval. Suppose \(k_j\in K\), and suppose \(J_{k_j}\) is quasiconvex for every index used. If
\[
F_j=A_j+D\phi_j,\qquad \sup_j|A_j|<\infty,
\]
and
\[
\mathcal E_{k_j}(A_j,\phi_j)\longrightarrow0,
\]
then the fourth powers \(\{|F_j|^4\}\) are equiintegrable.

In particular, this holds at any fixed parameter \(k_*>1/3\) where quasiconvexity of \(J_{k_*}\) is already known.

The quasiconvexity hypothesis is essential to the proof. This theorem does not assert it at an unproved parameter.

### Proof

There are explicit original-density bounds
\[
\mu_k|F|^4\le J_k(F)\le\nu_k|F|^4,
\]
where one possible choice is
\[
\mu_k=
\frac{(3k-1)\min(k^2,1)}{16(k+2)}
\]
and
\[
\nu_k=
\frac{(3k-1)(\max(k,1)+1)^2}{8(k+1)}
+\frac{3k-1}{16}+\frac14.
\]

For the lower bound, put \(w=ku-v+2j\). Since \(j^2\le uv\),
\[
\begin{aligned}
(ku+v)^2
&=(ku-v)^2+4kuv\\
&\le2w^2+4(k+2)uv\\
&\le16(k+2)Q_k(F).
\end{aligned}
\]
Also
\[
ku+v\ge\min(k,1)(u+v).
\]
Multiplying by \(3k-1\) gives the stated coercivity. The upper bound follows from
\[
|ku-v+2j|
\le(\max(k,1)+1)|F|^2,
\qquad
uv,\ j^2\le\frac{|F|^4}{4}.
\]

Consequently, on \(K\) there are uniform constants
\[
0<\mu_K\le\mu_k,\qquad \nu_k\le\nu_K<\infty.
\]
The bounded means and vanishing gaps therefore give a uniform \(L^4\) bound.

Suppose the fourth powers were not equiintegrable. Apply the accepted **actual compatible concentration removal**. Along a subsequence it supplies fields
\[
\widetilde F_m=A_{j_m}+D\widetilde\phi_m
\]
with exactly the same affine means, equal to \(F_{j_m}\) outside sets \(E_m\), such that
\[
\int_{E_m}|\widetilde F_m|^4\longrightarrow0,
\qquad
\liminf_m\int_{E_m}|F_{j_m}|^4\ge\kappa>0.
\]

The original-density bounds then give
\[
\begin{aligned}
\mathcal E_{k_{j_m}}(A_{j_m},\widetilde\phi_m)
\le{}&
\mathcal E_{k_{j_m}}(A_{j_m},\phi_{j_m})\\
&-\mu_K\int_{E_m}|F_{j_m}|^4
+\nu_K\int_{E_m}|\widetilde F_m|^4.
\end{aligned}
\]
The upper limit is at most \(-\mu_K\kappa<0\), contradicting quasiconvexity at the **same parameter** \(k_{j_m}\). This proves equiintegrability.

Unlike the lower-endpoint retuning argument, this proof does not need to preserve a determinant-variance error relative to a vanishing \(\ell\). Original quartic coercivity pays for the removed mass directly.

### Consequence for a possible interior boundary

Suppose
\[
k_j\longrightarrow k_*>1/3,
\]
\(J_{k_*}\) is quasiconvex, and actual tests with bounded means satisfy
\[
\mathcal E_{k_j}(A_j,\phi_j)<0.
\]
Then their fourth powers must be equiintegrable.

Indeed, on a compact interval containing these parameters, direct differentiation of the coefficients gives
\[
|J_k(F)-J_{k'}(F)|
\le L_K|k-k'||F|^4.
\]
Negativity and coercivity give
\[
\int|F_j|^4
<\frac{\nu_K}{\mu_K}|A_j|^4.
\]
Hence
\[
\begin{aligned}
0
&\le \mathcal E_{k_*}(A_j,\phi_j)\\
&\le L_K|k_j-k_*|
\left(\int|F_j|^4+|A_j|^4\right)
\longrightarrow0.
\end{aligned}
\]
The fixed-parameter theorem applies.

This removes fourth-power concentration from bounded-mean negative sequences approaching an **interior quasiconvex parameter**. It does not reach \(k_*=1/3\), where the original density becomes \(j^2\) and the coercivity constant above vanishes.

## 2. Why this does not propagate the affirmative tail

The remaining compactness issue includes a concrete spatial dilution mechanism.

Take a compactly supported potential \(\phi\), place its support inside a torus cell, and define
\[
\phi_\rho(x)=\rho\,\phi\!\left(\frac{x-x_0}{\rho}\right).
\]
Then
\[
\int J_k(D\phi_\rho)
=\rho^2\int J_k(D\phi),
\]
and, at the same affine mean,
\[
\mathcal E_k(A,\phi_\rho)
=\rho^2\mathcal E_k(A,\phi).
\]
Thus the ratio
\[
\frac{\mathcal E_k(A,\phi_\rho)}
{\int J_k(D\phi_\rho)}
\]
is unchanged, while
\[
D\phi_\rho\longrightarrow0
\quad\text{strongly in }L^4.
\]

Therefore bounded-mean normalization can produce a trivial limiting field even when a relative reserve is approaching zero. Conversely, normalizing
\[
\int J_k(D\phi)=1
\]
can make the affine means unbounded.

The concentration theorem does not supply compactness modulo this dilution, or rigidity of a nontrivial zero-Jensen gradient law.

For an **actual** zero-gap field at an already quasiconvex parameter, the valid stationarity identities are stronger than the single energy equality. With \(F=A+D\phi\) and \(P=DJ_k\), they include
\[
\int P(F)=P(A),
\qquad
\int P(F):D\eta=0,
\]
and
\[
\int P(F)F^T=P(A)A^T,
\qquad
\int F^TP(F)=A^TP(A).
\]
The source variation in the last identity was justified on its actual changed lattice, followed by the compact-support transfer. These identities still leave the signed constitutive work
\[
\int[\lambda(F)-\lambda(A)]\,\operatorname{cof}F:D\phi
\]
uncontrolled. Strict monotonicity of the companion \(T\) does not remove that term.

## 3. Exact lower-endpoint acoustic factorization

There is a useful exact identity for \(Q_0=Q_{1/3}\).

Let
\[
u=|F_1|^2,\quad v=|F_2|^2,\quad
w=F_1\cdot F_2,\quad d=\det F,
\]
let
\[
R=\begin{pmatrix}0&-1\\1&0\end{pmatrix},
\qquad \rho=(p,t)^T,
\]
and set
\[
E=(FR\rho)\otimes\rho.
\]
The entire line \(F+sE\) has determinant \(d\), because
\[
F+sE=F(I+sR\rho\otimes\rho),
\qquad
\det(I+sR\rho\otimes\rho)=1.
\]
This argument also covers singular \(F\).

The identity is
\[
\boxed{
\begin{aligned}
24D^2Q_0(F)[E,E]
={}&\big[(d+3v)p^2-3(u-d)t^2\big]^2\\
&+3\big[w(p^2-3t^2)+(3v-u-2d)pt\big]^2.
\end{aligned}}
\]

A direct derivation starts from the fixed-determinant expression
\[
Q_0(F)
=\frac3{32}(u+v-2d)^2+\frac d2u-\frac1{12}u^2.
\]
Writing
\[
z=|FR\rho|^2=ut^2-2wpt+vp^2,
\]
the variations along \(E\) are
\[
u'=2p(-tu+pw),\qquad
v'=2t(-tw+pv),
\]
\[
u''=2p^2z,\qquad v''=2t^2z.
\]
Substitution and expansion show that the difference between the two sides of the boxed identity is
\[
(uv-w^2-d^2)(p^4+18p^2t^2+9t^4),
\]
which vanishes by the Gram determinant identity.

### What happens in the generating chart

For
\[
M=\begin{pmatrix}a&c\\c&b\end{pmatrix},
\qquad q=1+c>0,
\qquad
K(M)=qQ_0(L(M)),
\]
this factorization yields an exact decomposition
\[
D^2K(M)[H,H]
=
\frac{(\ell_1(M):H)^2+3(\ell_2(M):H)^2}{24q^3}
+\Lambda(M)\det H.
\]
The complete covectors and rational coefficient \(\Lambda\) are in the report.

The canonical two-form that would cancel the determinant terms in scalar Hessian heat evolution is
\[
-\Lambda\,(da\wedge dc+dc\wedge db).
\]
Its exterior derivative is
\[
-(\Lambda_a+\Lambda_b)\,da\wedge dc\wedge db.
\]
It is not closed: at
\[
(a,q,b)=(1,1,0),
\qquad
\Lambda_a+\Lambda_b=\frac{11}{4}.
\]

Thus the two positive squares do **not** yet give a zero-integral correction or the required generating-Hessian Jensen inequality. This calculation neither excludes every other correction nor produces a negative compatible field.

## 4. The rank-one martingale construction retains an explicit unpaid term

The stochastic route can be written without losing the affine mean or the residual.

Let \(g_s=P_sG\), where \(G=D\phi\), and let \(X_t\) be stationary Brownian motion with generator \(\Delta\). For a finite horizon \(T\), put
\[
M_t=g_{T-t}(X_t),
\]
and define
\[
dV_t=\sqrt2\left(
\partial_1g_{T-t}(X_t)\,dW_t^2
-\partial_2g_{T-t}(X_t)\,dW_t^1
\right).
\]
Then
\[
N_t=A+M_t-V_tR
\]
has rank-one noise:
\[
dN_t
=\sqrt2\,\Delta P_{T-t}\phi(X_t)\otimes dW_t.
\]

Rank-one convexity therefore applies to this martingale. Retaining the exact start and using the accepted conditional covariance identities gives
\[
\boxed{
\mathbb E J_k(N_T)
=
\int J_k(A+G)+\mathcal R_T(A,G)+\mathcal G_T(G),
}
\]
where
\[
\mathcal R_T(A,G)=
\int_0^T\!\int
\sum_{i=1}^2
D^2J_k(A+g_s)
[(\partial_i g_s)R,(\partial_i g_s)R]\,dx\,ds.
\]
The additional term \(\mathcal G_T\) has an explicit nonnegative double-heat representation, with
\[
0\le\mathcal G_T(G)\le104\nu_k\int|G|^4.
\]

The rotated-Hessian integral is absolutely convergent as \(T\to\infty\). For a coefficient bound satisfying
\[
|D^2J_k(F)[E,E]|\le C_k|F|^2|E|^2,
\]
one obtains
\[
|\mathcal R_\infty-\mathcal R_T|
\le C_k\left(
|A|^2\|P_TG\|_2^2+\frac12\|P_TG\|_4^4
\right).
\]
The finite-horizon identities extend by strong \(W^{1,4}\) approximation.

The resulting statement is
\[
\mathcal E_k(A,\phi)
+\mathcal R_\infty(A,G)+\mathcal G_\infty(G)\ge0.
\]
The comparison needed to remove the **complete additional term** is missing.

This issue is visible even on a simple compatible shear. At \(k=1,A=I\), take
\[
G=\varepsilon e_1\otimes e_2\,g(x_2),
\qquad \int g=0.
\]
Its actual original gap is
\[
\mathcal E_1(I,\phi)
=\frac{\varepsilon^4}{8}\int g^4.
\]
The martingale terminal energy contains an additional positive quadratic term
\[
4\varepsilon^2
\left(\int g^2-\int(P_Tg)^2\right).
\]
Therefore this operation does not give the sharp original budget merely from its rank-one increments. Its terminal field is generally not a compatible gradient, and no conditional Jensen inequality for \(J_k\) has been assumed.

## 5. A relaxed negative was explicitly kept separate from the original question

For an actual smooth determinant-one map \(F=D\Psi\) with mean \(I\), its conductivity
\[
\sigma=F^{-1}F^{-T}
\]
has determinant one and effective conductivity \(I\). The corresponding expression for the endpoint energy is
\[
Q_0(F)
=
\Phi(\sigma)
=
\frac3{32}(\operatorname{tr}\sigma-2)^2
+\frac12\sigma_{22}
-\frac1{12}\sigma_{22}^2.
\]

Retaining only \(\det\sigma=1\) and its effective conductivity loses necessary information. For example, let \(u(x_1)=1+\varepsilon\) and \(1-\varepsilon\) on equal half-periods, and set
\[
\sigma=\operatorname{diag}(1/u,u).
\]
Its effective conductivity is \(I\), and
\[
\int\Phi(\sigma)-\frac5{12}
=
\frac{\varepsilon^2(-8+25\varepsilon^2+\varepsilon^4)}
{96(1-\varepsilon^2)^2}.
\]
At \(\varepsilon=1/2\), this equals
\[
-\frac1{128}.
\]

But its actual harmonic-coordinate corrector has gradient
\[
\operatorname{diag}(u,1),
\]
whose determinant is \(u\). The determinant-one square-root field associated with the metric is not that compatible corrector. **This is a negative for the stated relaxation, not a negative for the original variational problem.**

## 6. Computation and the exact remaining question

Only one new mathematical computation was executed in this continuation: a bounded exact symbolic check of the acoustic factorization and generating-chart Hessian identity. It verified the factorization residual and all nine Hessian residual entries exactly, and computed the nonzero closure coefficient. It used rational polynomial arithmetic, completed in approximately \(0.86\) seconds of reported process wall time, and stayed within its declared \(60\)-second cap. The code and exact receipt are included.

The other results above were proved analytically. No numerical optimizer, numerical energy integration, stochastic simulation or PDE solver supplied an outcome. The previous bounded searches remained closed. All inherited source and resource restrictions were retained.

For arbitrary compatible \(G=D\phi\), the full unresolved comparison remains
\[
\boxed{\,b_G^T H_G^\dagger b_G\le2c_G\,}.
\]
The compatible range condition is accepted, so proving this inequality for every \(G\) would settle every affine mean. Alternatively, one actual compatible field violating it, together with a rigorously certified original gap, would settle the question negatively.

**Neither of those two conclusions has been obtained here.**
