# P1 completed return

Source: https://chatgpt.com/c/6af2bc39-2f58-83ec-b26b-3a99e1d2c0f2  
Model: Pro (visible UI)  
Prompt: `work/astra-renewed-pro-programmes-20261103/P1_FULL_ORIGINAL_QUARTIC_AFTER_GLOBAL_TAIL_PRO_20261111.txt`; latest human continuation: `Please cpmtomie from wher eyou left off`  
Final: `f66146f9-8c45-5e78-8527-0b742f5120aa`. Native final is complete as returned; UI activity history was virtualized, so the following are only visible excerpts. The original ZIP for this new return was not identified with certainty; no archive is included.

## Visible activity excerpts

From the visible current-turn screen before completion:

> The Fourier lift is now fully audited: it satisfies the exact lift equation for every compatible L4 gradient at k = 1, and its continuity bound is proved by a finite-horizon martingale argument. The available general norm estimate is still far above 18cG. The endpoint work likewise has a stronger exact negative-gap test, but no field satisfying it. Both gaps remain substantive.

> Checked all-k lift feasibility; Checked uniform coercivity and pointwise lift failure; Audited the C2 obstruction proof; Checked the coefficient bound; Verified the positivity bound; Checked first-column control; Derived the cubic inequality; Checked sharp endpoint inequality.

## Complete final as returned

I continued from the accepted large-\(k\) theorem. **I have not proved the full inequality for every \(k>1/3\), and I have not constructed a compatible negative witness.** The affirmative tail remains
\[
k\ge K_*=780(41+12C_0)^2
\quad\Longrightarrow\quad
\int_{\mathbb T^2}J_k(A+D\phi)-J_k(A)
\ge \frac19\int_{\mathbb T^2}J_k(D\phi).
\]
The work below does not establish a new unrestricted positive parameter interval.

This continuation produced an exact stronger certificate for a negative **original** gap, an exact variance decomposition, a general compatible bilinear lift at \(k=1\), and an all-parameter obstruction to the pointwise heat/two-form method. The construction search produced actual compatible fields, but none met the negative certificate.

The proofs, coefficient tables, code, and verification receipts are saved in the updated [:chatgpt-content-reference{index="3"}](https://chatgpt.com/library?file_id=libfile_6d1aa4e4e9f08191bc79875c2b2752c0&account_id=personal). The current account is :chatgpt-content-reference{index="4"}[LOWER_ENDPOINT_AND_BILINEAR_CONTINUATION_RESULTS.txt](sandbox:/workspace/scratch/21b466b728a1/LOWER_ENDPOINT_AND_BILINEAR_CONTINUATION_RESULTS.txt).

## 1. An exact stronger certificate for a negative original gap

Let \(F=A+G\), where \(G=D\phi\) is an **actual compatible periodic gradient**, and write
\[
\Delta H=\int_{\mathbb T^2}H(F)-H(A).
\]
Define
\[
X=\Delta u^2,\qquad
D=\Delta(u+v-2j)^2,\qquad
V=\Delta j^2
  =\int_{\mathbb T^2}(j-\det A)^2,
\]
and
\[
a=-\Delta Q_0,\qquad
Q_0=Q_{1/3},\qquad
J_k=j^2+(3k-1)Q_k.
\]

The useful identity is the exact division
\[
\boxed{
Q_k(F)
=\frac18\left[
(k-1)u^2+4uj+\frac{(u+v-2j)^2}{k+1}
\right].
}
\tag{1}
\]

It gives, for **every \(h>0\)**,
\[
\boxed{
\Delta J_{1/3+h}
=
V-3ha+
\frac{3h^2}{8}
\left[
X-\frac{D}{(4/3)(4/3+h)}
\right].
}
\tag{2}
\]
There is no Taylor remainder or small-\(h\) restriction.

Both \(X\) and \(D\) are nonnegative convex Jensen gaps. More strongly,
\[
G\ne0\quad\Longrightarrow\quad D>0.
\tag{3}
\]
To see the strictness, let \(R\) be the positive quarter-turn and set
\[
W(F)=F_{\cdot1}+RF_{\cdot2}.
\]
Then
\[
|W(F)|^2=u+v-2j.
\]
Equality in the strictly convex Jensen inequality for \(|W(F)|^4\) would force \(W(G)=0\) almost everywhere. Compatibility gives
\[
\int|W(G)|^2
=\int|G|^2-2\int\det G
=\int|G|^2,
\]
so equality forces \(G=0\).

Also, \(a>0\) forces \(X>0\). Indeed, \(X=0\) makes the first total column constant, hence \(\Delta(uj)=0\), and (1) gives
\[
\Delta Q_0=\frac{3D}{32}\ge0.
\]

We can therefore choose the explicit admissible parameter
\[
\boxed{k=\frac13+\frac{4a}{X}}
\tag{4}
\]
whenever \(a>0\). Substituting it into (2) gives the exact original gap
\[
\boxed{
\Delta J_k
=
V-\frac{6a^2}{X}
-\frac{6a^2D}
 {X^2(4/3)(4/3+4a/X)}.
}
\tag{5}
\]

Consequently,
\[
\boxed{
a>0,\qquad VX\le6a^2
\quad\Longrightarrow\quad
\Delta J_{\,1/3+4a/X}<0.
}
\tag{6}
\]
Even equality \(VX=6a^2\) yields a strict negative because the last term in (5) is strictly negative.

This strengthens the earlier \(VE<3a^2/4\) sufficient condition in two ways: it uses the specific column Jensen gap \(X\), and it retains an additional favorable exact term. The full expression (5) can certify fields beyond the convenient sufficient condition (6).

For rational polygonal potentials and rational means, all quantities in (4)–(5) are rational. Thus a qualifying field would immediately give an exact compatible witness, parameter, and negative margin. Spatial dilution of a compactly supported test scales \(X,D,V,a\) by the same area fraction, preserving both the selected parameter and the sign criterion.

**No field satisfying this certificate has been obtained.** Its derivation does not supply the required gradient.

The proof and independent review are in :chatgpt-content-reference{index="5"}[EXACT_ENDPOINT_DEFECTS_AND_LIMITS.md](sandbox:/workspace/scratch/21b466b728a1/lower_endpoint_continuation/EXACT_ENDPOINT_DEFECTS_AND_LIMITS.md) and :chatgpt-content-reference{index="6"}[CONSTRUCTION_INDEPENDENT_ENDPOINT_REVIEW.md](sandbox:/workspace/scratch/21b466b728a1/lower_endpoint_continuation/CONSTRUCTION_INDEPENDENT_ENDPOINT_REVIEW.md).

## 2. An exact variance decomposition of the original density

There is also a direct positive comparison that retains determinant fluctuations.

Put
\[
\alpha=\frac{4\ell}{3n},\qquad
\beta=\frac{\ell^2}{24n},\qquad
\kappa=k+\frac13.
\]
The exact pointwise decomposition is
\[
J_k(F)=\alpha Q_0(F)+g(F_{\cdot1},j),
\]
where
\[
g(x,j)=j^2+4\beta |x|^2j+\beta\kappa |x|^4.
\tag{7}
\]

Define
\[
\sigma_* =1-\frac{\ell^2}{2nm},\qquad
q=j+\frac{\kappa}{2}u,\qquad
q_A=\det A+\frac{\kappa}{2}u_A,
\]
and
\[
S=\int u-u_A=\int|G_{\cdot1}|^2.
\]
Completing the square in (7), then integrating, yields
\[
\boxed{
\begin{aligned}
\Delta J_k
={}&\alpha\,\Delta Q_0+\sigma_*V
+\frac{4\beta}{\kappa}\operatorname{Var}(q)\\
&+4\beta q_AS+\beta\kappa S^2.
\end{aligned}}
\tag{8}
\]

This is an identity for the original energy. In particular, if
\[
\det A\ge0,
\qquad
\frac13<k\le\frac{7+2\sqrt{13}}3,
\tag{9}
\]
every remainder term after \(\alpha\Delta Q_0\) is nonnegative. Thus, throughout this parameter range,
\[
\Delta Q_0\ge0
\quad\Longrightarrow\quad
\Delta J_k\ge0.
\tag{10}
\]
The **total Jacobian may change sign** in this statement.

A possible negative in this range must therefore have \(a>0\) and overcome the complete variance and column reserve in (8). What is missing is a bound on that endpoint deficit for every compatible field.

There is a related comparison for every \(k>1/3\), under the stronger hypothesis \(j(F)\ge0\) almost everywhere. Set
\[
\sigma=\frac{2(9k+1)}{3nm}>0.
\]
The function \(g(x,j)-\sigma j^2\) is convex on \(j\ge0\), by an explicit Hessian completion. It gives
\[
\boxed{
\Delta J_k
\ge
\alpha\,\Delta Q_0+\sigma V
+\frac{8\beta}{3}(\det A)S.
}
\tag{11}
\]
Equations (8) and (11) are two allocations of the **same** remainder \(g\). Their reserves cannot be added.

### The mean-orientation reduction preserves compatibility

For the existence of a strict negative, restricting to nonnegative mean determinant is legitimate.

At rational \(k=p/q>1/3\), take
\[
M=qB_k=
\begin{pmatrix}0&p\\q&0\end{pmatrix}.
\]
Since \(M\) has integer entries,
\[
\phi_M(x)=\phi(Mx)
\]
is periodic, and
\[
AM+D\phi_M(x)=F(Mx)M.
\]
The integer torus covering preserves normalized integration. Direct substitution gives
\[
J_k(ZM)=p^2q^2J_k(Z),
\qquad
\det(AM)=-pq\,\det A.
\]
Hence a strict negative with negative mean determinant becomes a strict negative with positive mean determinant. An irrational strict-negative parameter first admits a nearby rational parameter by continuity for the same fixed field.

This uses an actual source transformation and compatible potential.

## 3. The constant-total-Jacobian problem is now an explicit sharp inequality

Suppose
\[
j(F)=\det A=d\ge0
\quad\text{almost everywhere}.
\]
Then \(V=0\) and \(\Delta(uj)=dS\). Formula (1) gives
\[
\boxed{
\Delta Q_0=-\frac{X}{12}+\frac{dS}{2}+\frac{3D}{32}.
}
\tag{12}
\]
Thus positivity of the endpoint energy on this class is exactly
\[
\boxed{
X\le6dS+\frac98D.
}
\tag{13}
\]

A compatible violation would give a negative original gap through (4)–(5). Conversely, for a fixed constant-determinant field, (13) implies positivity of its original gap for every \(k>1/3\): multiplying its \(Q_k\)-gap by \(8(k+1)\) gives
\[
(k^2-1)X+4(k+1)dS+D,
\]
which is increasing for \(k>0\).

**I have not proved (13) for every compatible constant-determinant field.** Even proving it on that class would leave the general determinant-fluctuation problem.

### Exact formulation on the original Beurling graph

The final analytic reduction retains the determinant constraint pointwise.

Identify the output plane with \(\mathbb C\), and write the matrix columns as
\[
p+q,\qquad i(p-q).
\]
For the affine mean use \(p_0,q_0\). Every compatible perturbation is represented by a mean-zero \(h\in L^4\):
\[
p=p_0+\mathcal Bh,\qquad q=q_0+h,
\]
where \(\mathcal B\) is the Beurling multiplier on the original torus.

Constant **total** determinant is exactly
\[
\boxed{
2\operatorname{Re}
\bigl(\overline{p_0}\mathcal Bh-\overline{q_0}h\bigr)
+|\mathcal Bh|^2-|h|^2=0
\quad\text{a.e.}
}
\tag{14}
\]
The representation has a compatible converse; it imposes no global inverse-map or twist assumption.

At \(A=I\), put \(z=(\mathcal B+I)h\). Then (13) becomes
\[
\boxed{
\|z\|_4^4
+4\int\operatorname{Re}(z)|z|^2
\le
18\|h\|_4^4+4\|\operatorname{Im}z\|_2^2,
}
\tag{15}
\]
subject to
\[
2\operatorname{Re}(\mathcal Bh)
+|\mathcal Bh|^2-|h|^2=0.
\tag{16}
\]

The sharp Beurling theorem supplied in the premises does not directly give (15): combining \(\|\mathcal B\|_4\le3\) with the triangle inequality yields only
\[
\|(\mathcal B+I)h\|_4^4\le256\|h\|_4^4,
\]
and does not control the signed cubic term. The known Burkholder/Beurling result remains available, but this use of it is insufficient. :chatgpt-content-reference{index="0"}

The all-mean formulation, converse, and approximation limitations are recorded in :chatgpt-content-reference{index="7"}[CONSTRAINED_BEURLING_ENDPOINT.md](sandbox:/workspace/scratch/21b466b728a1/lower_endpoint_continuation/CONSTRAINED_BEURLING_ENDPOINT.md). In particular, the note does **not** assert that Fourier truncation preserves the nonlinear constraint (14).

## 4. A general two-input compatible lift at \(k=1\)

The earlier exclusion of output-frequency multipliers left general two-input symbols available. That larger construction now produces an exact lift.

Using the inherited strain notation, a \(20\)-parameter family of bilinear corrections gives
\[
z_\theta(G)
=
\Pi_0\!\left[
S(G,G)+W^{-1/2}\mathcal Z_\theta(G,G)
\right],
\]
with
\[
\boxed{K_G^*z_\theta(G)=3b_G}
\tag{17}
\]
for **every compatible \(G\in L^4\)** at \(k=1\). Here
\[
W=\operatorname{diag}\!\left(\frac18,\frac3{32},\frac38,\frac18\right).
\]

The symbol retains both input frequencies and uses the denominator
\[
Q(\eta,\zeta)
=|\eta|^2+|\zeta|^2+|\eta+\zeta|^2.
\]
The numerators have degree four in potential frequencies, with positive degree in each input. The cyclic identity was solved as an exact rational system with

- \(1{,}408\) equations and \(100\) unknowns;
- \(13{,}824\) nonzero entries;
- rank \(80\), leaving \(20\) free parameters.

The polynomial identity holds for all frequencies and amplitudes. The passage from finite Fourier fields to \(L^4\) is also paid: a finite-horizon heat/martingale argument proves the required bilinear \(L^4\times L^4\to L^2\) bounds directly on the torus.

What remains missing is the sharp norm estimate. A universal choice of \(\theta\) satisfying
\[
\boxed{\|z_\theta(G)\|_2^2\le18c_G}
\tag{18}
\]
would suffice to prove the original inequality at \(k=1\). I have not proved (18).

The explicit general bound obtained for the correction is
\[
\|W^{-1/2}\mathcal Z(G,G)\|_2
\le
\sqrt{\frac{4122408}{625}}\,
\|G\|_4^2,
\]
which is far too large for the required conclusion. A sharper bound for the displayed lift on fixed-output one-direction fields also does not establish (18) for arbitrary vector gradients.

The complete coefficients, analytic extension proof, and precise remaining functional are in :chatgpt-content-reference{index="8"}[TWO_INPUT_BILINEAR_LIFT.md](sandbox:/workspace/scratch/21b466b728a1/projection_sharp_continuation/TWO_INPUT_BILINEAR_LIFT.md). Failure of a particular member of this lift family would itself be only a failure of that sufficient certificate.

## 5. The pointwise heat/two-form certificate is excluded for every \(k>1/3\)

This branch reached a complete conclusion about the proposed method.

For every \(k>1/3\), there is **no closed \(C^2\) two-form**, even defined only near \(F=0\), and no constant positive definite spatial diffusion matrix \(C\), such that
\[
\sum_{i,j}C_{ij}D^2J_k(F)[B_i,B_j]
+\omega_F(B_1,B_2)\ge0
\tag{19}
\]
for all nearby \(F\) and all compatible second jets
\[
B_1=
\begin{pmatrix}a&b\\d&e\end{pmatrix},
\qquad
B_2=
\begin{pmatrix}b&c\\e&f\end{pmatrix}.
\]

This exclusion does **not** assume completeness of sums of squares.

The proof normalizes with \(\rho=\sqrt{k}\):
\[
f_\rho(F)=J_k\!\left(F\operatorname{diag}(\rho^{-1},1)\right),
\qquad
\mathscr J=8kn\,f_\rho.
\]
Symmetry averaging reduces a hypothetical homogeneous quadratic closed form to a complete eight-dimensional space. Acoustic zeros and stationarity impose a \(32\times8\) system of rank seven. The checked rank minor is
\[
-4096\rho^6(\rho^2+1)^4(3\rho^2+1),
\]
so no positive parameter is lost through an exceptional pivot.

For every form in the resulting necessary family, the compatible jet
\[
B_1=
\begin{pmatrix}0&2\rho\\0&0\end{pmatrix},
\qquad
B_2=
\begin{pmatrix}2\rho&0\\0&-m\end{pmatrix}
\]
and background \(F=\operatorname{diag}(p,s)\) force the certificate to equal
\[
\boxed{-4\ell m^2(p-\rho s)^2.}
\tag{20}
\]
This is negative whenever \(p\ne\rho s\).

For a general closed \(C^2\) form near zero, positivity first forces its constant and linear Taylor coefficients to vanish. Rescaling then produces a forbidden homogeneous quadratic closed-form certificate. Genuine source/jet transformations and reflection/swap averaging extend the contradiction to every constant positive definite spatial diffusion.

The proof and independent audit are saved in :chatgpt-content-reference{index="9"}[ALL_PARAMETER_POINTWISE_HEAT_OBSTRUCTION.md](sandbox:/workspace/scratch/21b466b728a1/heat_certificate_continuation/ALL_PARAMETER_POINTWISE_HEAT_OBSTRUCTION.md).

**Equation (20) is a pointwise certificate contradiction, not an original quasiconvexity counterexample.** No periodic field with a negative original gap follows from those jets. Indeed, this obstruction coexists with the accepted affirmative large-\(k\) tail, so this family itself demonstrates that the certificate condition is stronger than quasiconvexity.

## 6. The compatible construction search and its finite costs

The new construction branch used compact square-annulus twists and overlapping compositions of at most four twists. Each branch is a rational affine map of determinant one; the pieces match continuously, and the opposite-sign twist is the inverse. These are actual periodic Lipschitz maps.

For an outer matrix \(A\), their fields have the form
\[
AB=A+D(A\psi),
\]
with constant total determinant. Compatibility and the determinant constraint are therefore built into the construction.

The declared finite search was completed:

| Item | Actual work |
|---|---:|
| Compatible fields | \(12\) |
| Final polygons across all fields | \(640\) |
| Maximum polygons in one field | \(124\) |
| Branch tests | \(2{,}677\) |
| Candidate outer-mean solves | \(48\) |
| Scalar bisections | \(3{,}960\) |
| Exact endpoint checks | \(12\) |
| Exact original-density checks | \(36\) |

All twelve evaluated endpoint deficits had \(a<0\), while \(V=0\) exactly. All evaluated original gaps at \(k=17/50,1/2,1\) were positive. Floating calculations proposed means; the reported signs at the rounded rational means were recomputed exactly.

These checks prove the signs of those evaluated fields and means. They supply neither an all-mean certificate for each map nor a universal theorem.

The other finite algebraic work is recorded with its actual receipts:

| Calculation | Exact result | Recorded internal time |
|---|---|---:|
| Endpoint identity verifier | Ten identities reduce to zero | \(0.5514\) s |
| Bilinear coefficient solve | Rank \(80\), twenty free parameters | \(11.0017\) s |
| Same solve exporting the complete kernel | Exact rational kernel | \(10.8995\) s |
| All-parameter heat system | Rank seven, complete necessary family | \(3.4107\) s |
| Independent all-parameter audit | All residuals, fixed minor, negative evaluations verified | \(4.3798\) s |
| Twelve-field twist search | Completed declared budget | \(0.7442\) s |

The packet also records the independent verifiers, bounded numerical candidate search, corrected preprocessing failures, bit sizes, and execution caps. No numerical optimization failure is used as an impossibility proof.

I also checked the primary incompressible-elasticity theorem of Ghiba–Martin–Neff. Its rank-one-convexity-to-polyconvexity conclusion assumes objective **and isotropic** planar incompressible energies; those symmetry hypotheses do not cover this anisotropic density. No full-family theorem was imported from it. :chatgpt-content-reference{index="1"}

## What remains unresolved

For every compatible \(G\), the full original question still requires
\[
\boxed{
b_G^{\mathsf T}H_G^\dagger b_G\le2c_G.
}
\]

The continuation has identified more exact structure around that inequality:

- A qualifying compatible field in (6) would give an explicit rationally certifiable negative.
- The variance identity (8) records positive original-density terms that such a field must overcome.
- The lift (17) pays compatibility and the \(L^4\) domain, but its sharp norm estimate remains unproved.
- The all-parameter heat obstruction closes that pointwise certificate route without deciding the original inequality.

**None of these results resolves the remaining unrestricted parameter range, and no negative original-energy witness is claimed.**

