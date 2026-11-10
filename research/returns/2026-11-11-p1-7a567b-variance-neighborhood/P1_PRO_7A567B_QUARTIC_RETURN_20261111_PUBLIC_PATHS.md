# P1 completed return 7a567bd0-9d2c-52c4-971c-670283a92c84

Chat: https://chatgpt.com/c/6af2bc39-2f58-83ec-b26b-3a99e1d2c0f2
User turn: 4cebd067-0a5e-4818-aa03-b11517fad039. Prompt reference: work/astra-renewed-pro-programmes-20261103/P1_FULL_ORIGINAL_QUARTIC_AFTER_THREE_SHEAR_AND_CONTACT_PRO_20261111.txt, SHA-256 159c220950091264341a5fd44d28252a164e11e0d1e36dd140c399bbde5f4766. UI previously showed Pro. Native final returned in full without a truncation flag; this does not assert literal database-byte identity.

The Mac is locked; current activity and helper panels cannot be inspected through the UI. The excerpt following the final was visible at the prior review and is incomplete. No current ZIP has been inspected or collected; its availability and identity are unknown. Existing holds apply.

## Complete native-returned final

**I have not resolved the full all-\(k\) inequality, and I have not found an admissible negative.** This continuation does produce a stronger compatible estimate from the supplied Burkholder theorem. It gives an explicit positive neighborhood in **total Jacobian variance** for the original density, for every affine mean and every \(k>1\).

The complete proofs, independent audits, actual potentials, exact rational certificates, and finite-work receipts are in:

- :chatgpt-content-reference{index="3"}[VARIANCE_COMPANION_CONTINUATION_RESULTS.txt](sandbox:/workspace/scratch/21b466b728a1/quartic_research_packet/VARIANCE_COMPANION_CONTINUATION_RESULTS.txt)
- [:chatgpt-content-reference{index="2"}](https://chatgpt.com/library?file_id=libfile_6d1aa4e4e9f08191bc79875c2b2752c0&account_id=personal)

The accepted large-\(k\) proof is preserved unchanged.

## 1. The new estimate for the original density

Write
\[
G=D\phi,\qquad
\Delta_k(A,G)=\int_{\mathbb T^2}J_k(A+G)-J_k(A),
\]
and define the total Jacobian variance
\[
V_j=\int_{\mathbb T^2}
\bigl(\det(A+G)-\det A\bigr)^2.
\]

For every real \(k>1\), every real \(A\), and every periodic \(W^{1,4}\) vector potential, the new bound is
\[
\boxed{
\Delta_k(A,G)
\ge
\frac{3\ell}{640nk^2}\int_{\mathbb T^2}|G|^4
-\frac{n}{2(k-1)}V_j.
}
\tag{1}
\]
Here \(|G|\) is the Frobenius norm. **If \(\det A\ge0\), the factor \(k^2\) in the first denominator can be removed.**

Consequently, the desired original inequality holds whenever
\[
\boxed{
V_j\le
\frac{3\ell(k-1)}{320n^2k^2}\int|G|^4.
}
\tag{2}
\]
At half this threshold there is an explicit positive margin:
\[
\boxed{
V_j\le
\frac{3\ell(k-1)}{640n^2k^2}\int|G|^4
\quad\Longrightarrow\quad
\Delta_k(A,G)\ge
\frac{3\ell}{1280nk^2}\int|G|^4.
}
\tag{3}
\]
For \(\det A\ge0\), remove \(k^2\) from these denominators as well.

These statements impose no frequency, concentration, amplitude, or output-direction restriction. Their restriction is the displayed bound on the **total** Jacobian variance. They do not cover arbitrary determinant fluctuations.

The proof uses the supplied companion once. The main new ingredient is the following estimate.

## 2. Four affine means give a stronger compatible fourth-power bound

Let
\[
R=\begin{pmatrix}0&-1\\1&0\end{pmatrix},
\qquad
W(F)=F_{\mathrm{col}1}+RF_{\mathrm{col}2}.
\]
For every affine mean \(A\) and every compatible periodic \(G=D\phi\),
\[
\boxed{
\int|W(A+G)|^4-|W(A)|^4
\ge \frac3{80}\int|G|^4.
}
\tag{4}
\]

The coefficient \(3/80\) is proved here; I am not asserting that it is optimal. If \(W(A)=0\), it improves to \(1/25\).

### Compatibility and the four choices of mean

Identify the target \(\mathbb R^2\) with \(\mathbb C\). Write the complex columns of \(G\) as
\[
G_1=p+h,\qquad G_2=i(p-h),
\qquad p=\mathcal B h.
\]
This is the original-torus compatible gradient relation. In particular,
\[
\int h=\int p=0,\qquad
\int|p|^2=\int|h|^2,\qquad W(G)=2h.
\]
Put \(W(A)=2q_0\), and define
\[
\begin{aligned}
D&=\int|q_0+h|^4-|q_0|^4,\\
C&=\int|h|^4,\qquad P=\int|p|^4,\\
a_0&=|q_0|^2\int|h|^2,\\
b_0&=\int\bigl[\operatorname{Re}(\overline q_0h)\bigr]^2.
\end{aligned}
\]

The supplied full Burkholder theorem applies at every affine mean on the original unit torus. In its \(p=4\) normalization, the quasiconvex density is
\[
(3|q|-|p|)(|p|+|q|)^3.
\]
I checked this normalization and scope directly in Corollary 2 of the supplied primary paper. :chatgpt-content-reference{index="0"}

Multiply that density by \(27/16\), calling the result \(\mathscr U\). The exact scalar identity
\[
\boxed{
81|q|^4-|p|^4-\mathscr U(p,q)
=
\frac{(|p|-3|q|)^2
\bigl(11|p|^2+66|p||q|+135|q|^2\bigr)}{16}
\ge0
}
\tag{5}
\]
provides a majorant.

Apply quasiconvexity to the **same periodic potential** at the four affine means
\[
(p_0,q_0),\qquad
p_0\in\{3q_0,\;3iq_0,\;-3q_0,\;-3iq_0\}.
\]
Every pair defines an ordinary constant real matrix, and
\(\mathscr U(p_0,q_0)=0\). Thus
\[
\int|p+p_0|^4\le81\int|h+q_0|^4
\]
for each choice.

The four-point average is exact:
\[
\frac14\sum_{p_0}|p+p_0|^4
=
|p|^4+36|q_0|^2|p|^2+81|q_0|^4.
\]
Using the \(L^2\) equality between \(p\) and \(h\) gives the stronger retained inequality
\[
\boxed{P+36a_0\le81D.}
\tag{6}
\]

This step has exactly four applications of an accepted theorem. It uses no sampled phase average, numerical integration, or new operator oracle.

### Extracting the coefficient \(3/80\)

Expansion and Cauchy–Schwarz give
\[
\begin{aligned}
D
&=C+4\int |h|^2\operatorname{Re}(\overline q_0h)
       +2a_0+4b_0\\
&\ge(\sqrt C-2\sqrt{b_0})^2+2a_0,
\end{aligned}
\tag{7}
\]
with \(a_0\ge b_0\).

Combining (6) with nine times (7),
\[
P+9(\sqrt C-2\sqrt{b_0})^2+54b_0\le90D.
\]
Weighted Cauchy–Schwarz then yields
\[
\begin{aligned}
(\sqrt P+\sqrt C)^2
&\le
\left(1+\frac19+\frac4{54}\right)
\left[P+9(\sqrt C-2\sqrt{b_0})^2+54b_0\right]\\
&\le\frac{320}{3}D.
\end{aligned}
\tag{8}
\]
The intermediate scalar \(\sqrt C-2\sqrt{b_0}\) can have either sign; no sign assumption enters this calculation.

Finally,
\[
\int|G|^4
=4\int(|p|^2+|h|^2)^2
\le4(\sqrt P+\sqrt C)^2
\le\frac{1280}{3}D,
\]
while
\[
\int|W(A+G)|^4-|W(A)|^4=16D.
\]
This proves (4).

When \(q_0=0\), equation (6) instead gives \(P\le81C\) directly, hence
\[
\int|W(G)|^4\ge\frac1{25}\int|G|^4.
\]
The detailed proof includes a compact radial Lipschitz construction showing that this **unshifted** constant \(25\) is sharp. Its annular logarithmic contribution and its bounded core and outer errors are explicit. That sharpness statement does not establish optimality of \(3/80\).

Smooth periodic approximation and fourth-order growth extend all these inequalities to the stated \(W^{1,4}\) class.

## 3. How this enters the original \(J_k\)

Set
\[
\kappa=\frac{\ell}{8n},\qquad
\sigma=\frac{n}{2(k-1)},
\]
and, for \(F=A+G\), use
\[
du=u-u_0,\quad dv=v-v_0,\quad dj=j-d,\quad d=\det A,
\qquad S_i=\int|G_i|^2.
\]

Orthogonalizing the two supplied feature squares gives the exact identity
\[
\boxed{
\begin{aligned}
\Delta_k(A,G)+\sigma V_j
={}&\kappa\,\Delta|W|^4
+\gamma_A S_1\\
&+\kappa(k^2-1)
\int\left(du+\frac{2dj}{k-1}\right)^2,
\end{aligned}}
\tag{9}
\]
where
\[
\gamma_A=\frac{\ell}{4}\bigl((k-1)u_0+2d\bigr).
\]
Thus \(\gamma_A\ge0\) whenever \(d\ge0\).

For the other determinant sign, put
\[
U(F)=kF_1-RF_2.
\]
A complementary exact reallocation is
\[
\boxed{
\begin{aligned}
\Delta_k(A,G)+\sigma V_j
={}&\frac{\kappa}{k^2}\Delta|U|^4
+\frac{\widetilde\gamma_A}{k^2}S_2\\
&+\frac{\kappa(k^2-1)}{k^2}
\int\left(dv-\frac{2k\,dj}{k-1}\right)^2,
\end{aligned}}
\tag{10}
\]
where
\[
\widetilde\gamma_A
=\frac{\ell}{4}\bigl((k-1)v_0-2kd\bigr).
\]
Here \(\widetilde\gamma_A\ge0\) whenever \(d\le0\).

These are two reorganizations of the same companion identity. Their reserves are not added together.

### The anisotropic estimate preserves the torus contract

The required counterpart of (4) is
\[
\boxed{
\Delta|U|^4
\ge\frac3{80}
\int\bigl(k^2|G_1|^2+|G_2|^2\bigr)^2.
}
\tag{11}
\]

For rational \(k=r/s>0\), take the actual periodic potential
\[
\psi(x)=\frac1s\phi\bigl(\operatorname{diag}(r,s)x\bigr)
\]
and then conjugate the complex target, using
\(\mathsf C=\operatorname{diag}(1,-1)\).
Its gradient is
\[
D(\mathsf C\psi)(x)
=\mathsf C\,G\bigl(\operatorname{diag}(r,s)x\bigr)
             \operatorname{diag}(k,1).
\]
Because \(R\mathsf C=-\mathsf CR\), its \(W\)-feature is the conjugate of \(U\). Applying (4) and averaging the finite \(rs\)-fold torus covering proves (11).

For real \(k\), the resulting integrals involve the same original \(F,G\) and polynomial expressions in \(k\). Rational approximation passes to the limit with an error bounded by
\[
C|k-k'|
\left(\int|F|^4+|A|^4+\int|G|^4\right)
\]
on bounded parameter intervals. Convergence of the covering potentials is unnecessary.

Substituting (4) into (9), or (11) into (10), gives (1), retaining two additional nonnegative terms in the applicable determinant-sign branch. Since \(k>1\),
\[
\bigl(k^2|G_1|^2+|G_2|^2\bigr)^2\ge|G|^4,
\]
which gives the displayed common coefficient for every mean.

The full extra affine term in (6) also remains available. It can be used as an alternative bound or through a convex combination with (4). It has not yielded a payment of the entire \(\sigma V_j\) term.

### A quantitative constant-Jacobian consequence at \(k=1\)

If the **total** determinant is constant, then \(V_j=0\) identically. Taking \(k\downarrow1\) in (1), for this fixed field, proves
\[
\boxed{
\det(A+G)=\det A\ \text{a.e.}
\quad\Longrightarrow\quad
\Delta_1(A,G)\ge\frac3{640}\int|G|^4.
}
\tag{12}
\]
The divergence of \(\sigma\) causes no problem in this passage because its multiplier is identically zero. This does not extend the unrestricted variance estimate through \(k=1\).

## 4. A random operation that preserves actual compatible gradients

The stochastic branch also produced an exact operation on arbitrary compatible gradients, with its approximation and covariance accounting completed.

Let \(P_t=e^{t\Delta}\) be the torus heat semigroup. For finite Fourier data, define
\[
\mathcal V_T(x)
=-\sqrt2\int_0^T
(\partial_2P_tG,-\partial_1P_tG)
       (x+\sqrt2B_t)\cdot dB_t,
\tag{13}
\]
componentwise in the matrix entries.

Differentiation in \(x\) commutes with this stochastic integral. Thus \(\mathcal V_T\) is the gradient of the corresponding integral applied to \(\phi\), and is an actual periodic compatible gradient with zero spatial mean for almost every sample.

The proved bounds are
\[
\mathbb E\|\mathcal V_T\|_4^4\le12\|G\|_4^4
\]
and, for \(S>T\),
\[
\boxed{
\mathbb E\|\mathcal V_S-\mathcal V_T\|_4^4
\le12\|P_TG\|_4^4.
}
\tag{14}
\]
The note gives an explicit exponential Fourier bound for the last term. These estimates provide an \(L^4\) limit \(\mathcal V_\infty\). Compatible Fourier approximation and the periodic Poincaré inequality preserve \(W^{1,4}\) potentials almost surely. No stochastic simulation or nonlinear PDE solver is used.

For
\[
G_\theta=\cos\theta\,G+\sin\theta\,\mathcal V_\infty,
\]
and the original quartic moments \(c_G,b_G,H_G\), the averaged identities are
\[
\boxed{
\begin{aligned}
\mathbb E H_{G_\theta}&=H_G,\\
\mathbb E b_{G_\theta}&=\cos\theta\,b_G,\\
\mathbb E c_{G_\theta}
&=\cos^2\theta\,c_G+\sin^2\theta\,c_V,
\end{aligned}}
\tag{15}
\]
where
\[
c_V=\mathbb E\int J_k(\mathcal V_\infty)\ge0.
\]

The finite-horizon formulas retain all three heat corrections. The vanishing fourth-order odd cross term is proved using the imaginary holomorphic quartic identity; it is not discarded merely from a zero third moment.

### Why this does not establish the original inequality

Optimizing the expected gap over **one common affine mean** gives exactly
\[
\boxed{
\inf_A\mathbb E\,\Delta_k(A,G_\theta)
=
\cos^2\theta
\left(c_G-\frac12b_G^TH_G^\dagger b_G\right)
+\sin^2\theta\,c_V.
}
\tag{16}
\]
The operation contracts the averaged cubic moment, but also changes the quartic cost. Positivity of \(c_V\) does not force positivity of the original parenthesis. Nor may the common-mean minimum in (16) be exchanged with an expectation of samplewise minima.

There is also an exact covariance result. For the hidden martingale \(V\), with matrix bracket \(\mathcal A=[V]\), and symmetric matrices \(C,D\),
\[
\begin{aligned}
\mathbb E[(V_T^TCV_T)(V_T^TDV_T)]
={}&\mathbb E[
\operatorname{tr}(C\mathcal A_T)
\operatorname{tr}(D\mathcal A_T)]\\
&+2\mathbb E\operatorname{tr}
(C\mathcal A_TD\mathcal A_T).
\end{aligned}
\tag{17}
\]
This is an integrated fourth-moment identity, without an assumption of Gaussianity or independence.

Replacing an ordinary bracket channel by its hidden terminal quadratic adds the **same covariance** to total variance and conditional variance. Their difference—the conditional-projection norm—does not improve. Consequently, that contribution supplies no second reserve toward \(18c_G\). The required joint endpoint/area estimate remains unpaid.

## 5. The compatible fourth-shear search was completed and stopped

The search used three new rational piecewise-linear maps
\[
f_3=S_h\circ T_g\circ S_l
\]
and a fourth vertical shear:
\[
f_4=f_3\circ T_m,\qquad
\phi=f_4-\mathrm{id}.
\]
The derivative \(m'\) was constant on 32 equal intervals, with its mean constrained to be exactly zero. Every nomination therefore defines an actual periodic Lipschitz potential.

A measure-preserving source change removes the values of \(m\) from the integral and leaves exact conditional slice weights. Those weights were computed by rational polygon clipping. This evaluates the distribution of an actual gradient; it does not replace compatibility by an arbitrary matrix measure.

The declared budget was six deterministic starts, at most 120 iterations and 800 evaluations per start, with a separate 180-second cap. It was not expanded.

| Stage | Recorded finite work | Recorded elapsed time |
|---|---:|---:|
| Exact geometry | 321 base polygons; 3,961 sliced pieces; 3,073 slice atoms; 4,741 clipping attempts | 0.5842 s |
| Exploratory optimization | 708 evaluations; 621 iterations | 1.1528 s |
| Exact certification | Six rational mean minimizations, six direct original-gap comparisons, six parameter tests; 5,948 atoms | 5.9782 s |

The largest recorded exact fraction had 6,999 bits. Floating outputs only nominated data. Each nominated slope and parameter was rounded to a rational with denominator \(2^{24}\); the slopes were then recentered exactly. All signs were recomputed using rational arithmetic.

For every one of the six nominations:

- **At its selected parameter**, the exact minimum over all independent affine means is positive.
- **At its resulting fixed rational minimizing mean**, the complete parameter polynomial is positive for every \(k>1/3\).

Those statements do not combine into a joint all-mean/all-parameter theorem. They also do not prove positivity over all choices of the fourth profile.

All six have positive total Jacobian variance and negative lower-endpoint deficit \(a\). No original negative was found. The smallest floating normalized gap was about \(0.010438\), and its rational nomination remained strictly positive under exact certification.

## 6. An exact lower-endpoint reserve calculation

A simple admissible field also makes the small positive ratios near \(k=1/3\) precise.

Take two periodic triangular profiles with derivatives \(a,d\in\{-1,1\}\), each on half a period, and
\[
f=S_h\circ T_g,\qquad A=I.
\]
After the genuine measure-preserving coordinate change, the four sign pairs have equal weight and
\[
Df=\begin{pmatrix}1+ad&a\\ d&1\end{pmatrix},
\qquad
G=Df-I=\begin{pmatrix}ad&a\\ d&0\end{pmatrix}.
\]
Direct evaluation of the original density gives
\[
\Delta_k(I,G)
=\frac{\ell(12k^2+8k+9)}{8n},
\qquad
\int J_k(G)
=1+\frac{\ell(4k^2+9)}{8n}.
\]
Therefore the optimal universal reserve satisfies the upper bound
\[
\boxed{
R(k)\le
\frac{\ell(12k^2+8k+9)}
{\ell(4k^2+9)+8n}
=
\frac{117}{32}\left(k-\frac13\right)
+O\!\left((k-\tfrac13)^2\right).
}
\tag{18}
\]

Both displayed energies are positive for every admissible \(k\). This proves that any universal positive reserve must degenerate near the lower endpoint. It establishes neither nonnegativity of \(R(k)\) nor the limit \(R(k)\to0\).

## 7. The remaining full question

The new original-density result is the variance-restricted bound (1)–(3), together with its stronger retained terms and the constant-total-Jacobian consequence (12). The stochastic operation is compatible and exact, but has no proved comparison that forces the original optimized gap to be nonnegative. The finite fourth-shear investigation produced no negative.

For unrestricted compatible \(G\), the target remains
\[
\boxed{b_G^TH_G^\dagger b_G\le2c_G.}
\]
This continuation does not establish that inequality throughout the remaining parameter range. In particular, arbitrary determinant fluctuations remain unresolved outside the new sufficient conditions, and the full interval \(1/3<k<1\) is not closed by these arguments.

The accepted unrestricted large-\(k\) tail remains valid at its stated analytic threshold. **Neither a full affirmative proof nor an admissible negative for the original question is contained in this return.**

## Previously visible activity excerpt (prior review; incomplete)

I’ll continue toward the unrestricted original inequality. I’ll use the new Jacobian-variance identity as one route to the missing sharp estimate, while also checking for a different integral argument or a rigorously certifiable compatible negative. The accepted tail and three-shear theorem remain available at their stated scopes.

Analyzed the Jacobian variance companion. Explored F-gradient rigidity and checked elliptic constraints. Checked corrected-feature kernel. Verified rotation rigidity. Tested nonlinear Korn bounds. Checked positive feature coefficients. Checked affine reduction and computed rotation averages. Checked weighted-minor control. Read Theorem 1 proof and considered unbounded convex K. Prepared scale integration and tested polygonal K. Explored a quadratic rowblock and analyzed the ellipse formula. Checked B's Lipschitz bounds. Tested matched-block J and checked branch symmetry. Checked bi-SO2 invariance. Checked rank-one curvature and derived Hessian conditions. Rearranged the Hessian.
