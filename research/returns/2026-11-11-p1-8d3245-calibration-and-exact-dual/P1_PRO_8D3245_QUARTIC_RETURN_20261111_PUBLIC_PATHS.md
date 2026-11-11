# P1 complete available return

Chat: https://chatgpt.com/c/6af2bc39-2f58-83ec-b26b-3a99e1d2c0f2  
Model visible: Pro. User turn: 799ffb69-23fa-43e9-8c08-828ed43903e7; final: 8d3245e5-a766-5266-b9cd-0a0a48a382d2.

Actual prompt: `P1_FULL_ORIGINAL_QUARTIC_AFTER_VARIANCE_NEIGHBORHOOD_PRO_20261111.txt` (SHA-256 78265d7d8ab98d4b8934ba4d86ff3ef4097eca5ada00c74255865d02a067b413).

Full final copied using current UI, UTF-8 17238 bytes, SHA-256 f2626f25b2958cfc607de5cb5e4401459af504bbbd8a6c76ef57b55d5d0d86cd. UI-copy capture is not a database-byte claim. Expanded current visible activity and three available current helper final panels follow; accessibility-rendered mathematics can fragment or repeat. The linked ZIP uses the known held prior library identity libfile_6d1aa4e4e9f08191bc79875c2b2752c0 and was not collected. All source and transfer holds remain.

## Complete UI-copied final

**I have not resolved the full universal inequality.** This continuation produces neither an affirmative for every \(k,A,\phi\) nor an actual compatible negative example. The accepted unrestricted large-\(k\) theorem remains unchanged.

The main completed advance is a **calibration that permits every final shear profile**, together with explicit classes of preceding maps for which that calibration holds. These results prove the inequality for the **original** \(J_k\) throughout \(k>1/3\) on new classes of actual compatible gradients. I also obtained stronger mixed-moment information from the unaveraged Burkholder theorem and completed a nonlinear-core projection construction. Their remaining gaps are stated below.

The complete proofs, exact constants, finite-work records and independent audits are saved in:

- :chatgpt-content-reference{index="3"}[COMPATIBLE_CALIBRATION_CONTINUATION_RESULTS.txt](sandbox:/workspace/scratch/21b466b728a1/COMPATIBLE_CALIBRATION_CONTINUATION_RESULTS.txt)
- [quartic_global_quasiconvexity_research_packet_2026-11-10.zip](https://chatgpt.com/library?file_id=libfile_6d1aa4e4e9f08191bc79875c2b2752c0&account_id=personal)

## 1. A proved original-density inequality with an arbitrary final shear

Write
\[
S_h(x,y)=(x+h(y),y),\qquad
T_g(x,y)=(x,y+g(x)).
\]

Here is one completed theorem.

**Theorem.** Fix a nonconstant real periodic
\[
h\in W^{2,\infty}(\mathbb T).
\]
There are explicit constants
\[
\varepsilon_h>0,\qquad \delta_h>0
\]
depending only on \(h\), such that every real periodic mean-zero
\[
g\in W^{1,\infty}(\mathbb T),
\qquad \|g'\|_\infty\le\varepsilon_h,
\]
and every real periodic
\[
r\in W^{1,4}(\mathbb T)
\]
give an actual map
\[
f=S_h\circ T_g\circ S_{-h}\circ T_r
\]
satisfying, for **every real \(k>1/3\)**,
\[
\boxed{
\int_{\mathbb T^2}J_k(Df)-J_k(I)
\ge
\frac{4\ell}{3n}
\left[
\frac{\delta_h}{6}\|g'\|_2^2
+\frac1{288}\|r'\|_4^4
\right].
}
\tag{1}
\]

The final profile \(r\) has **no amplitude or frequency restriction**. The smallness condition on \(g'\) is independent of its frequency and concentration.

This theorem has a matched mean \(A=I\) and constant total determinant. It does not establish arbitrary independent means or arbitrary-size middle profiles.

### The compatible potential is explicit

For clarity, set
\[
Y=y+r(x),\qquad X=x-h(Y),\qquad Z=Y+g(X).
\]
Then
\[
f(x,y)=\bigl(X+h(Z),Z\bigr),
\]
so the periodic perturbation is
\[
\phi(x,y)=f(x,y)-(x,y)
=\bigl(h(Z)-h(Y),\,r(x)+g(X)\bigr).
\tag{2}
\]

Thus the theorem concerns \(I+D\phi\), with an actual periodic
\(\phi\in W^{1,4}\). Each shear preserves area, and the composition gives
\[
\det Df=1\quad\text{a.e.},\qquad \int_{\mathbb T^2}Df=I.
\]

The \(W^{1,4}\) assertion does not require the last shear to be Lipschitz. The preceding three-shear map is Lipschitz; \(T_r\) has the explicit inverse
\[
(x,y)\longmapsto(x,y-r(x)),
\]
and its preservation of measure follows directly from Fubini. This also pays the exceptional-set issue in composing its derivative with the preceding map.

## 2. The calibration that pays every final profile

The central estimate applies to a general actual base map.

Let
\[
f_3=\mathrm{id}+\psi
\]
be Lipschitz and affine-periodic, with
\[
M=Df_3,\qquad \det M=1.
\]
For its columns, put
\[
u=|Me_1|^2,\qquad v=|Me_2|^2,\qquad w=Me_1\cdot Me_2.
\]
Define
\[
E=\int_{\mathbb T^2}Q_0(M)-Q_0(I)
\]
and the scalar function
\[
B(x)=\frac1{24}\int_0^1 w(u+9v+6)\,dy.
\tag{3}
\]

Then, for every periodic \(r\in W^{1,4}\),
\[
\boxed{
\int_{\mathbb T^2}Q_0\!\left(D(f_3\circ T_r)\right)-Q_0(I)
\ge
E-\frac34\operatorname{Var}(B)
+\frac1{288}\|r'\|_4^4.
}
\tag{4}
\]

Consequently,
\[
E\ge\frac34\operatorname{Var}(B)
\tag{5}
\]
is an explicit sufficient condition paying **all** final profiles simultaneously.

No minimizer of the fourth-profile problem is supplied by an oracle here. The estimate follows from a finite quartic completion.

### Proof of the calibration

Put \(p(x)=r'(x)\). The actual source change \(y\mapsto y+r(x)\) gives
\[
\int Q_0\!\left(D(f_3\circ T_r)\right)
=
\int Q_0\!\left(M(x,y)
\begin{pmatrix}1&0\\p(x)&1\end{pmatrix}\right)\,dx\,dy.
\tag{6}
\]

For fixed \(x\), denote the \(y\)-average by brackets. The conditional energy is a convex quartic:
\[
K_x(p)=K_x(0)+B(x)p+c_xp^2+b_xp^3+a_xp^4,
\]
where
\[
a_x=\frac{\langle v^2\rangle}{96},\qquad
b_x=\frac{\langle vw\rangle}{24},\qquad
c_x=\frac{\langle6w^2+2(3v+1)^2\rangle}{96}.
\tag{7}
\]

The exact identity
\[
ap^4+bp^3+cp^2
=
\frac a3p^4+
\left(c-\frac{3b^2}{8a}\right)p^2
+\frac{2a}{3}p^2
\left(p+\frac{3b}{4a}\right)^2
\tag{8}
\]
retains both a quartic term and a quadratic term from one allocation.

Cauchy–Schwarz gives
\[
c_x-\frac{3b_x^2}{8a_x}
\ge \frac{\langle(3v+1)^2\rangle}{48}.
\]
The actual slice identity
\[
\int_0^1Me_2\,dy=e_2
\]
implies
\[
\langle v\rangle\ge1,\qquad
\langle v^2\rangle\ge1,
\]
and therefore
\[
K_x(p)\ge K_x(0)+B(x)p+\frac13p^2+\frac1{288}p^4.
\tag{9}
\]

Since \(\int p=0\), the linear term pairs with \(B-\overline B\). Completing the remaining quadratic square yields
\[
\frac13p^2+(B-\overline B)p
\ge-\frac34(B-\overline B)^2.
\]
Integration proves (4).

The quadratic and quartic reserves in (9) are distinct terms of the single identity (8). They are not two uses of the same reserve.

There is also a matched-mean version at a constant \(C\) with \(\det C\ge0\), recorded in the proof note. Neither version asserts that condition (5) holds for every base map.

## 3. Why the cancelling-horizontal class satisfies the calibration

For
\[
f_3=S_h\circ T_g\circ S_{-h},
\]
the positive baseline at \(g=0\) vanishes. A separate compatible averaging argument supplies the needed margin.

### An explicit contraction from actual source translations

Define
\[
\mathcal T_hq(x)=\int_0^1q(x-h(y))\,dy.
\tag{10}
\]

Let
\[
H=\|h'\|_\infty>0,\qquad L=\|h''\|_\infty.
\]
Choose a closed interval on which \(h'\) has one sign and is bounded away from zero. Choose an image subinterval of length
\[
0<d_0\le\frac12.
\]
The pushforward of Lebesgue measure by \(h\), modulo one, dominates \(H^{-1}\) times Lebesgue measure on that image interval.

It follows that every nonzero integer Fourier multiplier of \(\mathcal T_h\) is bounded by
\[
\rho_h
=
1-\frac{d_0}{H}
\left(
1-\frac{\sin(\pi d_0)}{\pi d_0}
\right)
<1.
\tag{11}
\]
Indeed,
\[
\left|\frac{\sin(\pi n d_0)}{\pi n d_0}\right|
\le \frac{\sin(\pi d_0)}{\pi d_0}
\qquad(n\in\mathbb Z\setminus\{0\}),
\]
using \(|\sin(nt)|\le |n||\sin t|\).

Thus, on the **original torus**, for every mean-zero \(q\in L^2\),
\[
\|\mathcal T_hq\|_2\le\rho_h\|q\|_2.
\tag{12}
\]
Set
\[
\delta_h=1-\rho_h^2>0.
\]

This controls all integer frequencies at once. No spectral sampling or uncomputed maximum over frequencies is used.

### The constrained cubic cancellation

For any compatible
\[
G=\begin{pmatrix}a&b\\c&d\end{pmatrix},
\qquad \det(I+G)=1,
\]
there is the exact integrated identity
\[
\boxed{
\int Q_0(I+G)-Q_0(I)
=
\int
\left[
Q_0(G)+\frac13c^2+
\frac16(a+3d)(a^2+c^2)
\right].
}
\tag{13}
\]

In particular, the cubic term contains no \(b^2\) contribution.

For the conjugate base, let
\[
\xi=x-h(y),\quad s=g'(\xi),\quad
a_0=h'(y),\quad b_0=h'(y+g(\xi)).
\]
Its actual perturbation gradient is
\[
G_3=
\begin{pmatrix}
b_0s&b_0-a_0-a_0b_0s\\
s&-a_0s
\end{pmatrix}.
\tag{14}
\]

Because \(Q_0(G_3)\ge0\), identity (13) gives
\[
E\ge
\left(\frac13-C_E\varepsilon\right)\|g'\|_2^2,
\qquad
\varepsilon=\|g'\|_\infty,
\qquad
C_E=\frac23H(1+H^2).
\tag{15}
\]

For the stress in (3), the actual slice identity
\[
\int_0^1(G_3)_{12}\,dy=0
\]
removes its linear horizontal contribution. A Taylor expansion with a paid remainder gives
\[
B=\frac23\mathcal T_hg'+R,
\qquad
\|R\|_2\le C_B\varepsilon\|g'\|_2.
\tag{16}
\]

Explicit valid constants are
\[
C_G=L+(H+1)^2,\qquad
C_B=\frac{41}{4}C_G^2.
\]
The estimate uses \(\varepsilon\le1/C_G\), so that \(\|G_3\|_\infty\le1\). On the resulting matrix ball, the Hessian of the stress polynomial is bounded by \(41/2\).

Combining (12), (15) and (16),
\[
E-\frac34\operatorname{Var}(B)
\ge
\left[
\frac{\delta_h}{3}
-(C_E+\rho_hC_B)\varepsilon
-\frac34C_B^2\varepsilon^2
\right]\|g'\|_2^2.
\tag{17}
\]

Therefore the explicit choice
\[
\boxed{
\varepsilon_h=
\min\left\{
\frac1{C_G},
\frac{\delta_h}{12(C_E+C_B)},
\frac{\sqrt{\delta_h}}{3C_B}
\right\}
}
\tag{18}
\]
gives
\[
E-\frac34\operatorname{Var}(B)
\ge\frac{\delta_h}{6}\|g'\|_2^2.
\tag{19}
\]

The linear and quadratic error terms each consume at most \(\delta_h/12\). Substitution into (4) proves
\[
\int Q_0(Df)-Q_0(I)
\ge
\frac{\delta_h}{6}\|g'\|_2^2
+\frac1{288}\|r'\|_4^4.
\tag{20}
\]

### Transfer to every original parameter

For any actual field \(F=I+G\) with constant total determinant one, put
\[
X=\int u(F)^2-u(I)^2\ge0,\qquad
S=\int u(F)-u(I)=\int|G_1|^2\ge0.
\]
The supplied division of \(Q_k\) gives the exact identity
\[
\boxed{
\Delta J_k
=
\frac{4\ell}{3n}\Delta Q_0
+
\frac{\ell}{8n}
\left[
\left(k^2-\frac19\right)X
+4\left(k-\frac13\right)S
\right].
}
\tag{21}
\]
Every additional term is nonnegative for \(k>1/3\). Combining (20) and (21) proves the original-density theorem (1).

### A fully rational nonempty instance

The constants need not be selected through numerical optimization. For example, periodically extend
\[
h(y)=y^2(1-y)^2,\qquad 0\le y\le1.
\]
Use the rational bounds \(H=1,L=2\), and take \(d_0=1/128\). A weaker rational form of the multiplier estimate permits
\[
\rho=1-\frac1{20971520},\qquad
\delta=1-\rho^2,\qquad
\varepsilon=\frac{\delta}{4444}.
\]
Then
\[
g(x)=\varepsilon\left(h(x)-\frac1{30}\right)
\]
is mean zero and satisfies the required smallness condition.

Since
\[
\int_0^1|h'|^2=\frac2{105},
\]
every periodic \(r\in W^{1,4}\) gives
\[
\int J_k(Df)-J_k(I)
\ge
\frac{4\ell}{3n}
\left[
\frac{\delta\varepsilon^2}{315}
+\frac1{288}\|r'\|_4^4
\right]>0.
\tag{22}
\]

This is a concrete positive family. It is not a negative witness or a substitute for the universal assertion.

## 4. Nearby independent means and determinant fluctuations

Each strict field above has an explicit positive neighborhood allowing determinant fluctuations.

Define
\[
\nu_k=
\frac{\ell(\max\{k,1\}+1)^2}{8n}
+\frac{\ell}{16}+\frac14.
\]
Direct differentiation of the original density gives
\[
|DJ_k(F)|\le4\nu_k|F|^3.
\tag{23}
\]

Suppose a proved field \(F_0=I+G_0\) has original gap at least \(\Gamma>0\), and put
\[
N_0=\|I+G_0\|_4,\qquad
d=|A-I|+\|G-G_0\|_4.
\]
For every compatible \(G\),
\[
\begin{aligned}
&\left|
\bigl[\int J_k(A+G)-J_k(A)\bigr]
-\bigl[\int J_k(I+G_0)-J_k(I)\bigr]
\right|\\
&\qquad\le
4\nu_k\bigl[(N_0+d)^3+(\sqrt2+d)^3\bigr]d.
\end{aligned}
\tag{24}
\]

Hence
\[
d\le
\min\left\{
1,\,
\frac{\Gamma}
{8\nu_k[(N_0+1)^3+(\sqrt2+1)^3]}
\right\}
\tag{25}
\]
implies an original gap of at least \(\Gamma/2\).

There is no determinant constraint on these nearby fields. The radius depends on the fixed positive base field and parameter; it does not pay arbitrary total-Jacobian variance.

## 5. Stronger joint cubic information from unaveraged Burkholder inequalities

I also pursued the full moment criterion directly.

Write a compatible complex derivative pair as
\[
G_1=p+z,\qquad G_2=i(p-z),\qquad p=\mathcal Bz,
\]
with zero means. The arbitrary-mean periodic Burkholder inequality used here is precisely the supplied Corollary 2 of Agazzi et al.; it is treated as established capital. [arxiv.org](https://arxiv.org/html/2609.28311v2?utm_source=chatgpt.com)

Set
\[
\mathcal U(p,z)=(3|z|-|p|)(|p|+|z|)^3,
\]
\[
T=\int p(3|z|^2-|p|^2),\qquad
C_{\mathcal U}=\int\mathcal U(p,z),\qquad
Q_\theta=\int[\operatorname{Im}(e^{-i\theta}p)]^2.
\]

Applying the theorem at the artificial conformal mean
\((te^{i\theta},0)\) gives the exact constraint
\[
\boxed{
\begin{aligned}
0\le\Phi_\theta(t)
={}&4Q_\theta t^2
+4t\operatorname{Re}(e^{-i\theta}T)
+C_{\mathcal U}\\
&+8\int
\bigl(|t+e^{-i\theta}p|-|p|\bigr)|z|^3,
\qquad t\in\mathbb R.
\end{aligned}
}
\tag{26}
\]

The function \(\Phi_\theta\) is convex. Retaining its modulus term preserves mixed information discarded by the phase-averaged majorant. One consequence is
\[
\boxed{
|\operatorname{Re}(e^{-i\theta}T)|
\le
2\int|z|^3+\sqrt{Q_\theta C_{\mathcal U}},
}
\tag{27}
\]
including the case \(Q_\theta=0\).

More substantially, **every component of the original**
\[
b_G=\int DJ_k(G)
\]
can be reconstructed exactly from \(T\) evaluated on twelve actual compatible fields:

| Potentials | Number |
|---|---:|
| \(\phi,\overline\phi\) | 2 |
| \(\phi+\beta_j\overline\phi\) and \(\overline\phi+\beta_j\phi\), \(\beta_j=i^j/2\) | 8 |
| \(\frac12\phi(3x_1,x_2)\), \(\frac12\phi(x_1,3x_2)\) | 2 |

The last two are genuine degree-three integer coverings of the original torus. Their normalized integrals are accounted for exactly.

These transformations recover the six complex moments
\[
\int p|p|^2,\quad
\int p|z|^2,\quad
\int z|p|^2,\quad
\int z|z|^2,\quad
\int p\,\Re(p\bar z),\quad
\int z\,\Re(p\bar z),
\]
which determine \(b_G\) for every \(k\).

**The remaining step is still the sharp shared estimate**
\[
|b_G:A|^2\le2c_GH_G[A,A].
\tag{28}
\]
The twelve transformed inequalities do not presently provide that comparison. Their Burkholder energies cannot be counted as twelve independent pieces of the original \(c_G\).

A separate exact construction shows that the averaged all-radius inequalities alone are insufficient, even with the null determinant moment and \(H>0\). It uses an abstract three-state matrix measure. No compatible realization is supplied, so its negative matrix Jensen gap is not a counterexample to the original question.

## 6. A completed nonlinear-core extension, with its global requirement still unpaid

The projection branch produced a valid extension operation.

Let \(\mathcal K\) be an affine operator ball covered by the accepted contact theorem, and let \(f_0\) be continuous and quasiconvex under the full gradient constraint \(Dw\in\mathcal K\). For positive-definite constant weights \(M,N\), define
\[
E(F)=\sup_{Z\in\partial\mathcal K}
\{f_0(Z)+(MZN):(F-Z)\}.
\]
Then
\[
\mathcal E f_0(F)=
\begin{cases}
\max\{E(F),f_0(F)\},&F\in\mathcal K,\\
E(F),&F\notin\mathcal K
\end{cases}
\tag{29}
\]
is globally quasiconvex.

The proof projects **potentials in \(L^2_M\)**. It uses contact and the translation pairing
\[
\int(MDwN):(Dv-Dw)\ge0.
\]
The convex-envelope lower bound and the constrained-core lower bound are combined by a maximum.

There is also an admissible source of nonlinear cores. From a known quasiconvex density \(q\), put
\[
E=F-A_0,\qquad
f_0(F)=\det(I+BE)\,
q\!\left(F_*+LE(I+BE)^{-1}\right).
\tag{30}
\]
On a compact constraint satisfying
\[
\sup_{F\in\mathcal K}\|B(F-A_0)\|_{\rm op}<1,
\tag{31}
\]
this is constrained quasiconvex.

The actual source map is
\[
\eta(x)=x+B\bigl(u(x)-A_0x\bigr).
\]
Condition (31) makes it globally bi-Lipschitz. Its transformed lattice, affine mean and nonconstant Jacobian weight are retained. The transfer to that lattice is justified by a cutoff argument with normalized boundary error \(O(1/N)\).

A large-parameter original \(J_K\), whose full quasiconvexity is accepted, can serve as \(q\). The graph change has a genuine adjustable fourth-order coefficient at the critical kernel. It therefore supplies a different possible calibration mechanism.

What is missing is global domination by the target density. With a fixed polyaffine normalization \(\pi\) and \(\widehat J=J_k-\pi\), one must still prove
\[
f_0(F)\le\widehat J(F)\qquad(F\in\mathcal K)
\]
and
\[
\boxed{
f_0(Z)+(MZN):(F-Z)\le\widehat J(F)
\quad
\text{for every }Z\in\partial\mathcal K
\text{ and every real }F,
}
\tag{32}
\]
together with touching at the desired affine mean.

No data satisfying these conditions for the full requested family have been constructed. Local adjustment of a kernel coefficient does not establish (32) or propagate the large-\(K\) theorem to smaller parameters.

## 7. Verification and the remaining full question

The completed results above use analytic estimates and exact algebra. There was **no new numerical candidate search or optimizer invocation**. Seven predetermined polynomial identities were independently checked with exact rational symbolic arithmetic. The shear realization, spectral estimate, reserve allocation, original all-\(k\) transfer, moment reconstruction, projection hypotheses and graph-change formulas received independent analytic audits.

The conclusions now established in this continuation are:

- A condition on an actual base map that pays every final vertical shear.
- Explicit classes satisfying that condition, including cancelling horizontal profiles, with an original-density inequality for every \(k>1/3\).
- Quantified nearby compatible fields allowing independent mean perturbations and determinant fluctuations.
- Unaveraged constraints that recover all original cubic components through twelve compatible transformations.
- A nonlinear-core extension and an admissible graph-change construction, with the global touching conditions explicitly identified.

The demanded unrestricted assertion still requires either
\[
b_G^TH_G^\dagger b_G\le2c_G
\quad\text{for every compatible }G,
\]
or an actual compatible field violating it. **Neither has been obtained.**

## Current expanded visible activity (accessibility snapshot)

Worked for 69m 10s
    - paragraph: I’ll continue with the unrestricted original inequality. I’ll check whether the new free-radius defect can control the Jacobian variance, while the other existing principals pursue a different integral argument and a compatible negative construction. I’ll retain each supplied result at its stated scope.
    - region "Subagent activity":
      - button "Principal moment"
      - text: ","
      - button "Principal projection"
      - text: and
      - button "Principal construction"
      - text: updated
    - paragraph: Derived radius bound and expanded moment coefficients
    - paragraph: Expanded J coefficients and analyzed all-k Hopf positivity
    - paragraph: Checked source-mix control and tested source-hyperbolic cone
    - paragraph: Checked Burkholder curvature
    - paragraph: Examined hidden bilinear covariance and tested MCV cancellation
    - paragraph: Tested endpoint cancellation coefficients and read the old coefficient table
    - paragraph: Tested full 18c SOS and checked the defect term
    - paragraph: Checked cross-block H positivity and derived covariance-based H
    - paragraph: Checked covariance constraints and tested CP-map interpretation
    - paragraph: Prepared quasiconvexity search
    - paragraph: Derived the Shield transform
    - paragraph: Tested rotated Shield equivalence and checked transformed degree
    - region "Subagent activity":
      - button "Principal projection"
      - text: updated
    - generic: Searched 15 websites
    - paragraph: Reviewed notes for gaps
    - button "Read files, searched the web"
    - generic: Read files, searched the web
    - paragraph: Explored quartic Bellman smoothing, monotone stress, and boundary rigidity
    - paragraph: Checked minimizer existence and Burkholder Hessian
    - paragraph: Checked Hessian alignment and computed components
    - paragraph: Checked translated Hessian and chose residual α
    - paragraph: Computed B4 Hessian
    - paragraph: Checked transformed parameter match and third B4 increment
    - paragraph: Checked cubic behavior
    - paragraph: "The translated Burkholder inequality retains mixed information that the four-phase average discards, so I’m testing it directly. The main issue is contact at the affine mean: a useful lower bound must match both the zero quadratic shear curvature and the cubic terms of the original density. The construction work is also checking whether the fourth-shear remainder admits an all-profile estimate."
    - region "Subagent activity":
      - button "Principal moment"
      - text: updated
    - paragraph: Analyzed critical-gap behavior and checked quartic coercivity
    - paragraph: Derived bounds on X from D
    - paragraph: Checked inverse-map compatibility and analyzed inverse B4 control
    - paragraph: Tested pointwise bounds and martingale interpolation
    - paragraph: Checked gradient geometry and rank-one noise combinations
    - paragraph: Checked martingale increments and noise-averaging inequality
    - paragraph: Derived joint fourth-moment and quartic covariance identities
    - paragraph: Tested holomorphic recovery and checked complex martingale structure
    - region "Subagent activity":
      - button "Principal projection"
      - text: updated
    - paragraph: Analyzed quartic moments and tested angular anisotropy
    - paragraph: Formulated a Bellman function and P(M,V) terms
    - paragraph: Assessed Bellman-extension obstruction and bounded the ΔQ gap
    - paragraph: Derived the companion bound and bounded moments via B4
    - paragraph: Tested the E22 case
    - paragraph: Computed the b:I derivative
    - paragraph: Explored trilinear bounds and checked quartic SOS finiteness
    - paragraph: Pursued localized shear insertion and checked Q0 monotonicity
    - paragraph: Explored symplectic generating functions and energy transformations
    - region "Subagent activity":
      - button "Principal construction"
      - text: updated
    - button "Searched the web"
    - generic: Searched the web
    - paragraph: Checked jet-matching algebra and derived transformed B4
    - paragraph: Checked cubic cancellation and translated cubic gap
    - region "Subagent activity":
      - button "Principal projection"
      - text: updated
    - paragraph: Checked Fourier compatibility constraints
    - paragraph: Analyzed limiting functional
    - paragraph: Checked the modulation ansatz
    - paragraph:
      - text: "The cubic calculation exposes a problem with the simplest translated Burkholder supports: their quadratic contact can match, but their cubic term along the remaining null direction cannot match"
      - math:
        - generic: J
        - generic: k
      - text: J
      - generic: k
      - text: . I’m checking whether a nonlinear change of variables avoids that obstruction. Separately, the integral approach still has room to use the unaveraged Burkholder inequalities; the pointwise obstruction does not rule that out.
    - paragraph: Derived J(G) and b and checked the cubic identity
    - paragraph: Checked cubic integral and computed Hessian scaling
    - generic: Ran command
    - region "Subagent activity":
      - button "Principal moment"
      - text: updated
    - paragraph: Tested coercivity and checked integration-by-parts bounds
    - paragraph: Derived trigonometric moments and computed the exact Fourier gap
    - paragraph: Derived translated moment constraints and examined singular-scale escape
    - paragraph: Checked kernel quartic sign
    - generic: Searched 7 websites
    - paragraph: Tested B4–V control and checked B4 along E12
    - paragraph: Analyzed quartic moment cones and bounded unaveraged cubics
    - paragraph: Formalized the cubic bound
    - paragraph: Checked cubic bounds and selected positive coefficient weights
    - paragraph: Tested cubic compatibility identities
    - region "Subagent activity":
      - button "Principal projection"
      - text: and
      - button "Principal construction"
      - text: updated
    - paragraph: Checked cubic kernel bounds
    - paragraph: Refined moment bounds and tested mixed-moment positivity
    - paragraph: Checked cubic integral identities and formed a test triad
    - generic: Searched for Listed continuation files and read shear calibration and Jacobian identity documentation
    - paragraph: Calculated the k=1 bound
    - paragraph: Tested F21⁴ witness and checked objectivity
    - paragraph: Tested transposition and checked the full-inversion image
    - paragraph: Checked projective parameter matching and J_K alignment
    - region "Subagent activity":
      - button "Principal construction"
      - text: and
      - button "Principal projection"
      - text: updated
    - paragraph: Derived shifted Hessian bounds
    - paragraph: Balanced core scaling and tested core B_K
    - paragraph: Analyzed F monotonicity
    - paragraph: Derived core shear constraints
    - region "Subagent activity":
      - button "Principal projection"
      - text: updated
    - paragraph: Checked quartic lower bound
    - paragraph: Checked derivative bounds
    - generic: Read files
    - paragraph:
      - text: There is a new positive result for actual compatible maps. An explicit condition on a determinant-one base map controls every subsequent vertical shear, including arbitrary
      - math:
        - generic: W
        - generic: "1"
        - generic: ","
        - generic: "4"
      - text: W
      - generic: 1,4
      - text: profiles. I’ve checked the square completion and the composition formula. This gives a nonempty four-shear class throughout
      - math:
        - generic: k
        - generic: ">"
        - generic: "1"
        - generic: /
        - generic: "3"
      - generic: k >
      - generic: 1/3
      - text: ", but it still imposes a condition on the base map and uses its matched affine mean."
    - generic: Ran command
    - region "Subagent activity":
      - button "Principal construction"
      - text: updated
    - paragraph: Tested weighted dual completion
    - paragraph: Tested a three-matrix realization
    - region "Subagent activity":
      - button "Principal moment"
      - text: updated
    - generic: Read files
    - region "Subagent activity":
      - button "Principal projection"
      - text: updated
    - paragraph: Derived a quartic reserve
    - paragraph: Tested uniform L4 control and H0 coercivity
    - paragraph: Checked mixed trilinear bounds
    - paragraph: "The new calibration now has an explicit class where its hypothesis is satisfied: fix two horizontal profiles with nonzero combined derivative, take the intervening vertical profile sufficiently small by a stated bound, and allow the final vertical profile to be arbitrary. The separate Burkholder calculation also recovers every cubic coefficient of the original density from twelve compatible transformations. What remains unproved there is the sharp comparison with the single original energy and Hessian budget."
    - generic: Searched for Inspected continuation files, packet receipt, and research README
    - paragraph: Audited the new proof
    - paragraph: Derived the F formula
    - paragraph: Checked coefficient formulas
    - paragraph: Derived graph-shear QC preservation
    - paragraph: Tested weighted support and set f0 from conjugates
    - paragraph: Audited attenuation constants
    - region "Subagent activity":
      - button "Principal construction"
      - text: and
      - button "Principal projection"
      - text: updated
    - paragraph: Checked the spectral-gap constant
    - paragraph: Bounded the nonlinear remainder
    - region "Subagent activity":
      - button "Principal construction"
      - text: updated
    - paragraph: Audited proof notes
    - button "Read files, searched the web"
    - generic: Read files, searched the web
    - paragraph: Tested iterative profile calibration
    - paragraph: Tested shear decomposition and checked conjugation convexity
    - generic: Read files
    - paragraph: Tested graph-shear QC
    - paragraph: Checked global QC extension status
    - region "Subagent activity":
      - button "Principal moment"
      - text: updated
    - paragraph: Checked the free-radius premise
    - paragraph: Bounded J variation
    - paragraph: Prepared quantified-neighborhood proof
    - button "Edited a file"
    - generic: Edited a file
    - paragraph: Derived the four-shear map and verified periodicity and regularity
    - paragraph: Audited the QC definition
    - generic: Read files
    - region "Subagent activity":
      - button "Principal moment"
      - text: and
      - button "Principal construction"
      - text: updated
    - paragraph: Documented root audit
    - paragraph: The calibration also works when the two horizontal profiles cancel. Averaging translations by a fixed nonconstant horizontal profile gives an explicit contraction on every nonzero integer frequency. That contraction pays the error from a small middle profile, uniformly over its frequencies, while still allowing an arbitrary final shear. The proof uses no sampled profiles. It remains restricted to the matched mean; it does not settle the full all-mean question.
    - generic: Searched for Applied patches and reviewed continuation project files and constraint analysis
    - region "Subagent activity":
      - button "Principal projection"
      - text: and
      - button "Principal construction"
      - text: updated
    - paragraph: Reviewed Section 5 formulas
    - paragraph: Chose a periodic polynomial
    - paragraph: Defined the rational perturbation
    - paragraph: Verified explicit h data
    - button "Edited a file"
    - generic: Edited a file
    - paragraph: Checked covariance derivation
    - paragraph: Verified numerical bounds
    - region "Subagent activity":
      - button "Principal moment"
      - text: updated
    - generic: Read files
    - region "Subagent activity":
      - button "Principal projection"
      - text: and
      - button "Principal moment"
      - text: updated
    - paragraph:
      - text: The completed proofs and their limits are now being consolidated. Each strict positive four-shear field also has an explicit
      - math:
        - generic: L
        - generic: "4"
      - text: L
      - generic: "4"
      - text: neighborhood that allows nearby independent means and determinant fluctuations, with the integral error bounded quantitatively. These neighborhoods do not cover arbitrary fields, and the sharp global moment inequality remains unproved.
    - generic: Searched for Updated projection continuation files using nonlinear core and graph shear documentation
    - region "Subagent activity":
      - button "Principal moment"
      - text: finished
    - paragraph: Prepared archive script
    - paragraph: Proved constrained cutoff transfer and verified cutoff approximation
    - paragraph: Established η’s global invertibility and checked the 2×2 identity
    - generic: Read files
    - paragraph: Developed projection proof
    - region "Subagent activity":
      - button "Principal projection"
      - text: updated
    - paragraph: Collected report notes
    - generic: Read files
    - paragraph: Drafted the core extension
    - paragraph: Checked projection extension
    - paragraph: Validated the projection construction
    - generic: Read files
    - paragraph: Checked projection invariance and summed inequality
    - paragraph: Verified projection construction
    - region "Subagent activity":
      - button "Principal projection"
      - text: updated
    - button "Edited a file"
    - generic: Edited a file
    - paragraph: Assessed conjugate-bound redundancy
    - generic: Read files
    - region "Subagent activity":
      - button "Principal projection"
      - text: updated
    - paragraph: Verified quartic coefficients
    - region "Subagent activity":
      - button "Principal construction"
      - text: updated
    - paragraph: Prepared and applied file metadata
    - generic: Read files
    - region "Subagent activity":
      - button "Principal projection"
      - text: updated
    - paragraph: Waited for audit completion
    - generic: Read files
    - paragraph:
      - text: The projection extension and graph-change formulas are also checked. They retain the source-map inverse, the Jacobian weight and the transformed period lattice. They still need a global minorant touching
      - math:
        - generic: J
        - generic: k
      - text: J
      - generic: k
      - text: ", which I have not constructed. I’m finishing the proof record with that gap, the new calibrated classes and the unresolved full statement clearly separated."
    - paragraph: Gathered report source files and verified archive manifest
    - paragraph: Audited projection block
    - region "Subagent activity":
      - button "Principal construction"
      - text: and
      - button "Principal projection"
      - text: finished
    - paragraph: Built and wrote an assembly script
    - paragraph: The final independent audits are complete. They confirm the calibrated four-shear theorems, the moment identities and the nonlinear-core extension. A missing plus sign in the graph-change tangent formula was corrected and rechecked. I’m saving the proofs and audit receipts now. I still have neither the full all-parameter proof nor a compatible negative example.
    - generic: Ran command
    - paragraph: Prepared attribute application with limited error output
    - button "Used Library integration, ran a command"
    - generic: Used Library integration, ran a command
    - paragraph: Finalized proof notation
    - paragraph: Checked explicit constants
    - paragraph: Checked the quartic bound
    - paragraph: Derived conjugate-map bounds
    - paragraph: Refined quartic variation formula
    - 

## Current available helper final panels (accessibility snapshots)

  - complementary:
    - heading "Subagents" [level=2]
    - button "Enter full view":
    - button "Close panel":
    - tabpanel "Subagents" [active]:
      - button "Back to subagents":
      - generic: Principal moment
      - heading "Status" [level=2]
      - generic: Done
      - heading "Final response" [level=2]
      - paragraph:
        - text: Completed this branch.
        - strong: The sharp original all-gradient inequality remains unproved
        - text: ", and no compatible negative witness was obtained."
      - heading "New integrated moment results" [level=3]
      - paragraph: The exact unaveraged Burkholder constraint is
      - math:
        - generic: "0"
        - generic: ≤
        - generic: Φ
        - generic: θ
        - generic: (
        - generic: t
        - generic: )
        - generic: =
        - generic: "4"
        - generic: Q
        - generic: θ
        - generic: t
        - generic: "2"
        - generic: +
        - generic: "4"
        - generic: t
        - generic: ℜ
        - generic: (
        - generic: e
        - generic: −
        - generic: i
        - generic: θ
        - generic: T
        - generic: )
        - generic: +
        - generic: C
        - generic: U
        - generic: +
        - generic: "8"
        - generic: ∫
        - generic: (
        - generic: ∣
        - generic: t
        - generic: +
        - generic: e
        - generic: −
        - generic: i
        - generic: θ
        - generic: p
        - generic: ∣
        - generic: −
        - generic: ∣
        - generic: p
        - generic: ∣
        - generic: )
        - generic: ∣
        - generic: h
        - generic: ∣
        - generic: "3"
        - generic: ","
      - text: 0 ≤
      - text: Φ
      - generic: θ
      - text: (t) =
      - text: "4"
      - text: Q
      - generic: θ
      - text: t
      - generic: "2"
      - text: + 4t ℜ(
      - text: e
      - generic: −iθ
      - text: T) +
      - text: C
      - generic: U
      - text: + 8 ∫
      - generic: (
      - text: ∣t +
      - text: e
      - generic: −iθ
      - text: p∣ − ∣p∣
      - generic: )
      - text: ∣h
      - text: ∣
      - generic: "3"
      - text: ","
      - paragraph: where
      - math:
        - generic: T
        - generic: =
        - generic: ∫
        - generic: p
        - generic: (
        - generic: "3"
        - generic: ∣
        - generic: h
        - generic: ∣
        - generic: "2"
        - generic: −
        - generic: ∣
        - generic: p
        - generic: ∣
        - generic: "2"
        - generic: )
        - generic: ","
        - generic: Q
        - generic: θ
        - generic: =
        - generic: ∫
        - generic: "["
        - generic: ℑ
        - generic: (
        - generic: e
        - generic: −
        - generic: i
        - generic: θ
        - generic: p
        - generic: )
        - generic: "]"
        - generic: "2"
        - generic: ","
        - generic: C
        - generic: U
        - generic: =
        - generic: ∫
        - generic: U
        - generic: (
        - generic: p
        - generic: ","
        - generic: h
        - generic: )
        - generic: .
      - generic: T =
      - text: ∫ p(3∣h
      - text: ∣
      - generic: "2"
      - text: −
      - text: ∣p
      - text: ∣
      - generic: "2"
      - text: ),
      - text: Q
      - generic: θ
      - text: =
      - text: ∫[ℑ(
      - text: e
      - generic: −iθ
      - text: p)
      - text: "]"
      - generic: "2"
      - text: ","
      - text: C
      - generic: U
      - text: =
      - generic: ∫ U(p, h).
      - paragraph: Its retained modulus term gives information lost by phase averaging. The elementary consequence
      - math:
        - generic: ∣
        - generic: ℜ
        - generic: (
        - generic: e
        - generic: −
        - generic: i
        - generic: θ
        - generic: T
        - generic: )
        - generic: ∣
        - generic: ≤
        - generic: "2"
        - generic: ∫
        - generic: ∣
        - generic: h
        - generic: ∣
        - generic: "3"
        - generic: +
        - generic: Q
        - generic: θ
        - generic: C
        - generic: U
      - text: ∣ℜ(
      - text: e
      - generic: −iθ
      - text: T)∣ ≤
      - text: 2 ∫ ∣h
      - text: ∣
      - generic: "3"
      - text: +
      - text: Q
      - generic: θ
      - text: C
      - generic: U
      - paragraph:
        - text: is valid, including
        - math:
          - generic: Q
          - generic: θ
          - generic: =
          - generic: "0"
        - text: Q
        - generic: θ
        - text: =
        - generic: "0"
        - text: .
      - paragraph: I also recorded the distinct convex artificial-mean constraint
      - math:
        - generic: ∫
        - generic: ∣
        - generic: p
        - generic: ∣
        - generic: "4"
        - generic: ≤
        - generic: "6"
        - generic: ∫
        - generic: ∣
        - generic: p
        - generic: ∣
        - generic: "2"
        - generic: ∣
        - generic: q
        - generic: +
        - generic: h
        - generic: ∣
        - generic: "2"
        - generic: +
        - generic: "8"
        - generic: ∫
        - generic: ∣
        - generic: p
        - generic: ∣
        - generic: ∣
        - generic: q
        - generic: +
        - generic: h
        - generic: ∣
        - generic: "3"
        - generic: +
        - generic: "3"
        - generic: (
        - generic: ∫
        - generic: ∣
        - generic: q
        - generic: +
        - generic: h
        - generic: ∣
        - generic: "4"
        - generic: −
        - generic: ∣
        - generic: q
        - generic: ∣
        - generic: "4"
        - generic: )
        - generic: (
        - generic: q
        - generic: ∈
        - generic: C
        - generic: )
        - generic: .
      - text: ∫ ∣p
      - text: ∣
      - generic: "4"
      - text: ≤
      - text: 6 ∫ ∣p
      - text: ∣
      - generic: "2"
      - text: ∣q +
      - text: h
      - text: ∣
      - generic: "2"
      - text: +
      - generic: 8 ∫ ∣p∣∣q +
      - text: h
      - text: ∣
      - generic: "3"
      - text: +
      - text: "3"
      - generic: (
      - text: ∫ ∣q + h
      - text: ∣
      - generic: "4"
      - text: − ∣q
      - text: ∣
      - generic: "4"
      - generic: )
      - text: (q ∈
      - generic: C).
      - paragraph:
        - text: For a nonzero field, its right side is coercive and strongly convex in the two real coordinates of
        - math:
          - generic: q
        - generic: q
        - text: . No optimizer was invoked.
      - paragraph:
        - text: Most substantially,
        - strong:
          - text: twelve explicit compatible potential transformations recover all six complex cubic moments needed for every component of the original
          - math:
            - generic: b
            - generic: G
          - text: b
          - generic: G
        - text: ":"
      - list:
        - listitem: The original potential and its conjugate.
        - listitem: Four constant target transformations of each.
        - listitem: Two degree-three integer source coverings.
      - paragraph: All phase averages are finite and exact; all source operations preserve the original torus and its normalized integrals. Root and construction independently checked the formulas, including the real pairing convention with no additional factor of two.
      - paragraph:
        - text: The missing step is still a coupled estimate of these twelve transformed constraints by the
        - strong: single original
        - math:
          - generic: c
          - generic: G
          - generic: ","
          - generic: H
          - generic: G
        - text: c
        - generic: G
        - text: ","
        - text: H
        - generic: G
        - text: ", with the sharp constant"
      - math:
        - generic: ∣
        - generic: b
        - generic: G
        - generic: ":"
        - generic: A
        - generic: ∣
        - generic: "2"
        - generic: ≤
        - generic: "2"
        - generic: c
        - generic: G
        - generic: H
        - generic: G
        - generic: "["
        - generic: A
        - generic: ","
        - generic: A
        - generic: "]"
        - generic: .
      - text: ∣
      - text: b
      - generic: G
      - text: ":"
      - text: A
      - text: ∣
      - generic: "2"
      - text: ≤
      - text: "2"
      - text: c
      - generic: G
      - text: H
      - generic: G
      - text: "[A, A]."
      - paragraph: No transformed Burkholder budget has been counted as a free original reserve.
      - heading "Exact separation of the averaged conditions" [level=3]
      - paragraph:
        - text: A separate note constructs, for every
        - math:
          - generic: k
          - generic: ">"
          - generic: "1"
          - generic: /
          - generic: "3"
        - generic: k >
        - generic: 1/3
        - text: ", an abstract three-state matrix measure satisfying:"
      - list:
        - listitem: Zero mean and zero determinant moment.
        - text: Positive-definite
        - math:
          - generic: H
        - generic: H
        - text: .
        - listitem: Every supplied averaged inequality for all radii and all artificial means.
        - text: Failure of
        - math:
          - generic: b
          - generic: T
          - generic: H
          - generic: −
          - generic: "1"
          - generic: b
          - generic: ≤
          - generic: "2"
          - generic: c
        - text: b
        - generic: T
        - text: H
        - generic: −1
        - text: b ≤
        - generic: 2c
        - text: .
      - paragraph:
        - text: The proof has explicit finite error constants and an entirely rational
        - math:
          - generic: k
          - generic: =
          - generic: "1"
        - generic: k =
        - generic: "1"
        - text: instance. Root independently checked all identities and bounds.
      - paragraph:
        - strong: No gradient realization is supplied.
        - text: This is an insufficiency result for the listed averaged moment conditions, not a counterexample to quasiconvexity. It leaves the stronger unaveraged compatible constraints open.
      - heading "Independent audits" [level=3]
      - paragraph: "Both construction calibration notes pass the analytic audit, including:"
      - list:
        - text: The actual
        - math:
          - generic: W
          - generic: "1"
          - generic: ","
          - generic: "4"
        - text: W
        - generic: 1,4
        - text: last-shear composition.
        - listitem: The separate quadratic and quartic terms of the single exact completion.
        - text: The matched-mean transfer to every
        - math:
          - generic: k
          - generic: ">"
          - generic: "1"
          - generic: /
          - generic: "3"
        - generic: k >
        - generic: 1/3
        - text: .
        - listitem: The actual translation spectral gap.
        - text: The two separately paid
        - math:
          - generic: δ
          - generic: h
          - generic: /
          - generic: "12"
        - text: δ
        - generic: h
        - text: /12
        - text: errors in the cancellation case.
      - paragraph:
        - text: The rational-profile corollary and explicit
        - math:
          - generic: L
          - generic: "4"
        - text: L
        - generic: "4"
        - text: neighborhood corollary also check. Their conclusions concern their stated structured classes and neighborhoods, including nearby determinant fluctuations; they do not establish a global variance estimate.
      - heading "Completed files" [level=3]
      - list:
        - button "UNAVERAGED_BURKHOLDER_JOINT_MOMENTS.md":
          - text: UNAVERAGED_BURKHOLDER_JOINT_MOMENTS.md
        - button "AVERAGED_CONSTRAINTS_SEPARATION.md":
          - text: AVERAGED_CONSTRAINTS_SEPARATION.md
        - button "FOURTH_SHEAR_CALIBRATION_AUDIT.md":
          - text: FOURTH_SHEAR_CALIBRATION_AUDIT.md
        - button "ROOT_COROLLARIES_SCOPE_AUDIT.md":
          - text: ROOT_COROLLARIES_SCOPE_AUDIT.md
      - paragraph:
        - strong: "Costs:"
        - text: analytic derivations and local file reads/writes only. No computational search, numerical certification, symbolic solver, new source access, or additional resource was used.

---

  - complementary:
    - heading "Subagents" [level=2]
    - button "Enter full view":
    - button "Close panel":
    - tabpanel "Subagents" [active]:
      - button "Back to subagents":
      - generic: Principal projection
      - heading "Status" [level=2]
      - generic: Done
      - heading "Final response" [level=2]
      - paragraph:
        - strong:
          - text: The projection continuation is complete, independently audited, and file-stable. It proves the nonlinear-core extension and an admissible graph-shear transfer, but it does not yet provide a minorant touching the original
          - math:
            - generic: J
            - generic: k
          - text: J
          - generic: k
          - text: .
      - paragraph: "Files:"
      - list:
        - button "NONLINEAR_CORE_EXTENSION.md":
          - text: NONLINEAR_CORE_EXTENSION.md
        - button "GRAPH_SHEAR_INTERFACE.md":
          - text: GRAPH_SHEAR_INTERFACE.md
        - button "CONSTRUCTION_CORE_GRAPH_AUDIT.md":
          - text: CONSTRUCTION_CORE_GRAPH_AUDIT.md
      - heading "Proved extension" [level=3]
      - paragraph:
        - text: Let
        - math:
          - generic: K
        - generic: K
        - text: be an operator-ball constraint covered by the accepted contact theorem, including its compatible invertible left/right transforms. Let
        - math:
          - generic: f
          - generic: "0"
        - text: f
        - generic: "0"
        - text: be continuous and quasiconvex under the full gradient constraint
        - math:
          - generic: D
          - generic: w
          - generic: ∈
          - generic: K
        - generic: Dw ∈
        - generic: K
        - text: . With constant positive-definite target and source weights
        - math:
          - generic: M
          - generic: ","
          - generic: "N"
        - generic: M, N
        - text: ", define"
      - math:
        - generic: E
        - generic: (
        - generic: F
        - generic: )
        - generic: =
        - generic: sup
        - generic: ⁡
        - generic: Z
        - generic: ∈
        - generic: ∂
        - generic: K
        - generic: "{"
        - generic: f
        - generic: "0"
        - generic: (
        - generic: Z
        - generic: )
        - generic: +
        - generic: (
        - generic: M
        - generic: Z
        - generic: "N"
        - generic: )
        - generic: ":"
        - generic: (
        - generic: F
        - generic: −
        - generic: Z
        - generic: )
        - generic: "}"
        - generic: .
      - generic: E(F) =
      - generic: Z∈∂K
      - generic: sup
      - text: "{"
      - text: f
      - generic: "0"
      - text: (Z) +
      - generic: "(MZN) :"
      - generic: (F −
      - generic: "Z)}."
      - paragraph: Then
      - math:
        - generic: E
        - generic: f
        - generic: "0"
        - generic: (
        - generic: F
        - generic: )
        - generic: =
        - generic: "{"
        - generic: max
        - generic: ⁡
        - generic: "{"
        - generic: E
        - generic: (
        - generic: F
        - generic: )
        - generic: ","
        - generic: f
        - generic: "0"
        - generic: (
        - generic: F
        - generic: )
        - generic: "}"
        - generic: ","
        - generic: F
        - generic: ∈
        - generic: K
        - generic: ","
        - generic: E
        - generic: (
        - generic: F
        - generic: )
        - generic: ","
        - generic: F
        - generic: ∉
        - generic: K
      - text: E
      - text: f
      - generic: "0"
      - text: (F) =
      - generic: "{"
      - text: "max{E(F),"
      - text: f
      - generic: "0"
      - text: "(F)},"
      - generic: E(F),
      - generic: F ∈ K,
      - text: F
      - generic: ∈
      - generic: /
      - text: K
      - paragraph: is globally quasiconvex.
      - paragraph:
        - text: The proof projects
        - strong:
          - text: potentials in
          - math:
            - generic: L
            - generic: M
            - generic: "2"
          - text: L
          - generic: M
          - generic: "2"
        - text: . It uses the accepted contact property and weighted translation pairing, then applies the actual constrained quasiconvexity of the nonlinear interior core. The metric and transformed-lattice hypotheses are recorded explicitly.
      - heading "Proved graph-shear transfer" [level=3]
      - paragraph:
        - text: For a known quasiconvex core
        - math:
          - generic: q
        - generic: q
        - text: ", set"
        - math:
          - generic: E
          - generic: =
          - generic: F
          - generic: −
          - generic: A
          - generic: "0"
        - generic: E =
        - generic: F −
        - text: A
        - generic: "0"
        - text: and
      - math:
        - generic: f
        - generic: "0"
        - generic: (
        - generic: F
        - generic: )
        - generic: =
        - generic: det
        - generic: ⁡
        - generic: (
        - generic: I
        - generic: +
        - generic: B
        - generic: E
        - generic: )
        - generic: q
        - generic: ⁣
        - generic: (
        - generic: F
        - generic: ∗
        - generic: +
        - generic: L
        - generic: E
        - generic: (
        - generic: I
        - generic: +
        - generic: B
        - generic: E
        - generic: )
        - generic: −
        - generic: "1"
        - generic: )
        - generic: .
      - text: f
      - generic: "0"
      - text: (F) =
      - generic: det(I +
      - text: BE) q
      - generic: (
      - text: F
      - generic: ∗
      - text: + LE(I + BE
      - text: )
      - generic: −1
      - generic: )
      - text: .
      - paragraph: On a compact constraint satisfying
      - math:
        - generic: sup
        - generic: ⁡
        - generic: F
        - generic: ∈
        - generic: K
        - generic: ∥
        - generic: B
        - generic: (
        - generic: F
        - generic: −
        - generic: A
        - generic: "0"
        - generic: )
        - generic: ∥
        - generic: o
        - generic: p
        - generic: <
        - generic: "1"
        - generic: ","
      - generic: F∈K
      - generic: sup
      - text: ∥B(F −
      - text: A
      - generic: "0"
      - text: )
      - text: ∥
      - generic: op
      - text: <
      - generic: 1,
      - paragraph: this function is constrained quasiconvex.
      - paragraph: The proof uses the genuine bi-Lipschitz source map
      - math:
        - generic: η
        - generic: (
        - generic: x
        - generic: )
        - generic: =
        - generic: x
        - generic: +
        - generic: B
        - generic: (
        - generic: u
        - generic: (
        - generic: x
        - generic: )
        - generic: −
        - generic: A
        - generic: "0"
        - generic: x
        - generic: )
        - generic: .
      - generic: η(x) =
      - generic: x +
      - text: B
      - generic: (
      - text: u(x) −
      - text: A
      - generic: "0"
      - text: x
      - generic: )
      - text: .
      - paragraph:
        - text: For affine mean
        - math:
          - generic: A
        - generic: A
        - text: ", its transformed lattice is"
      - math:
        - generic: (
        - generic: I
        - generic: +
        - generic: B
        - generic: (
        - generic: A
        - generic: −
        - generic: A
        - generic: "0"
        - generic: )
        - generic: )
        - generic: Λ
        - generic: .
      - generic: (
      - text: I +
      - generic: B(A −
      - text: A
      - generic: "0"
      - text: )
      - generic: )
      - text: Λ.
      - paragraph:
        - text: The Jacobian weight remains in the integral. The passage from unit-torus quasiconvexity to that lattice is paid by an ordinary cutoff argument with normalized error
        - math:
          - generic: O
          - generic: (
          - generic: "1"
          - generic: /
          - generic: "N"
          - generic: )
        - generic: O(1/N)
        - text: .
      - heading "Exact freedom supplied by a large- original core" [level=3]:
        - text: Exact freedom supplied by a large-
        - math:
          - generic: K
        - generic: K
        - text: original core
      - paragraph: For
      - math:
        - generic: D
        - generic: K
        - generic: =
        - generic: diag
        - generic: ⁡
        - generic: (
        - generic: "2"
        - generic: ","
        - generic: −
        - generic: m
        - generic: K
        - generic: )
        - generic: ","
        - generic: B
        - generic: =
        - generic: γ
        - generic: D
        - generic: K
        - generic: −
        - generic: "1"
        - generic: ","
      - text: D
      - generic: K
      - text: =
      - generic: diag
      - text: (2, −
      - text: m
      - generic: K
      - text: ), B =
      - text: γ
      - text: D
      - generic: K
      - generic: −1
      - text: ","
      - paragraph: the critical kernel transforms exactly as
      - math:
        - generic: t
        - generic: D
        - generic: K
        - generic: +
        - generic: b
        - generic: E
        - generic: "12"
        - generic: ⟼
        - generic: t
        - generic: "1"
        - generic: +
        - generic: γ
        - generic: t
        - generic: D
        - generic: K
        - generic: +
        - generic: b
        - generic: (
        - generic: "1"
        - generic: +
        - generic: γ
        - generic: t
        - generic: )
        - generic: "2"
        - generic: E
        - generic: "12"
        - generic: ","
      - text: t
      - text: D
      - generic: K
      - text: +
      - text: b
      - text: E
      - generic: "12"
      - text: ⟼
      - generic: 1 + γt
      - generic: t
      - text: D
      - generic: K
      - text: +
      - text: (1 + γt
      - text: )
      - generic: "2"
      - generic: b
      - text: E
      - generic: "12"
      - text: ","
      - paragraph:
        - text: with Jacobian weight
        - math:
          - generic: (
          - generic: "1"
          - generic: +
          - generic: γ
          - generic: t
          - generic: )
          - generic: "2"
        - generic: (1 +
        - text: γt
        - text: )
        - generic: "2"
        - text: .
      - paragraph: After subtracting the correctly transformed polyaffine tangent, its cubic kernel term remains
      - math:
        - generic: −
        - generic: "2"
        - generic: ℓ
        - generic: K
        - generic: "n"
        - generic: K
        - generic: t
        - generic: "3"
        - generic: ","
      - text: −2
      - text: ℓ
      - generic: K
      - text: "n"
      - generic: K
      - text: t
      - generic: "3"
      - text: ","
      - paragraph:
        - text: while the fourth-order coefficient of
        - math:
          - generic: t
          - generic: "4"
        - text: t
        - generic: "4"
        - text: changes from
        - math:
          - generic: J
          - generic: K
          - generic: (
          - generic: D
          - generic: K
          - generic: )
        - text: J
        - generic: K
        - text: (
        - text: D
        - generic: K
        - text: )
        - text: to
      - math:
        - generic: J
        - generic: K
        - generic: (
        - generic: D
        - generic: K
        - generic: )
        - generic: +
        - generic: "2"
        - generic: ℓ
        - generic: K
        - generic: "n"
        - generic: K
        - generic: γ
        - generic: .
      - text: J
      - generic: K
      - text: (
      - text: D
      - generic: K
      - text: ) +
      - text: "2"
      - text: ℓ
      - generic: K
      - text: "n"
      - generic: K
      - text: γ.
      - paragraph:
        - text: The pure
        - math:
          - generic: E
          - generic: "12"
        - text: E
        - generic: "12"
        - text: quartic coefficient remains unchanged. The note gives the full exact rational formula, not only this expansion. This supplies local flexibility beyond the affine diagonal-core calculation; its use also changes the admissible constraint size.
      - heading "Exact remaining gap" [level=3]
      - paragraph:
        - text: Writing
        - math:
          - generic: J
          - generic: ^
          - generic: =
          - generic: J
          - generic: k
          - generic: −
          - generic: π
        - generic: J
        - text: =
        - text: J
        - generic: k
        - text: −
        - generic: π
        - text: for a fixed polyaffine normalization, a touching minorant still requires
      - math:
        - generic: f
        - generic: "0"
        - generic: (
        - generic: F
        - generic: )
        - generic: ≤
        - generic: J
        - generic: ^
        - generic: (
        - generic: F
        - generic: )
        - generic: (
        - generic: F
        - generic: ∈
        - generic: K
        - generic: )
        - generic: ","
      - text: f
      - generic: "0"
      - text: (F) ≤
      - generic: J
      - text: (F) (F ∈
      - generic: K),
      - paragraph: and, crucially,
      - math:
        - generic: f
        - generic: "0"
        - generic: (
        - generic: Z
        - generic: )
        - generic: +
        - generic: (
        - generic: M
        - generic: Z
        - generic: "N"
        - generic: )
        - generic: ":"
        - generic: (
        - generic: F
        - generic: −
        - generic: Z
        - generic: )
        - generic: ≤
        - generic: J
        - generic: ^
        - generic: (
        - generic: F
        - generic: )
        - generic: for every
        - generic: Z
        - generic: ∈
        - generic: ∂
        - generic: K
        - generic: and every real
        - generic: F
        - generic: .
      - text: f
      - generic: "0"
      - text: (Z) +
      - generic: "(MZN) :"
      - generic: (F −
      - generic: Z) ≤
      - generic: J
      - text: (F)
      - generic: for every
      - text: Z ∈
      - text: ∂K
      - generic: and every real
      - text: F.
      - paragraph: The latter is equivalently
      - math:
        - generic: f
        - generic: "0"
        - generic: (
        - generic: Z
        - generic: )
        - generic: ≤
        - generic: (
        - generic: M
        - generic: Z
        - generic: "N"
        - generic: )
        - generic: ":"
        - generic: Z
        - generic: −
        - generic: J
        - generic: ^
        - generic: ∗
        - generic: (
        - generic: M
        - generic: Z
        - generic: "N"
        - generic: )
        - generic: .
      - text: f
      - generic: "0"
      - text: (Z) ≤
      - generic: "(MZN) :"
      - generic: Z −
      - generic: J
      - generic: ∗
      - text: (MZN).
      - paragraph:
        - text: Touching also requires
        - math:
          - generic: f
          - generic: "0"
          - generic: (
          - generic: A
          - generic: ∗
          - generic: )
          - generic: =
          - generic: J
          - generic: ^
          - generic: (
          - generic: A
          - generic: ∗
          - generic: )
        - text: f
        - generic: "0"
        - text: (
        - text: A
        - generic: ∗
        - text: ) =
        - generic: J
        - text: (
        - text: A
        - generic: ∗
        - text: )
        - text: at the target mean.
      - paragraph:
        - strong: No data satisfying these global conditions for the requested original family have been obtained.
        - text: Local jet adjustment does not pay the boundary-plane inequalities or propagate the large-
        - math:
          - generic: K
        - generic: K
        - text: theorem to smaller parameters.
      - paragraph: Root and construction both checked the completed proofs. The missing plus sign in the transformed tangent was corrected; construction’s final audit found no substantive remaining error. No numerical optimization, symbolic search, new source retrieval, or additional resource was used.

---

  - complementary:
    - heading "Subagents" [level=2]
    - button "Enter full view":
    - button "Close panel":
    - tabpanel "Subagents" [active]:
      - button "Back to subagents":
      - generic: Principal construction
      - heading "Status" [level=2]
      - generic: Done
      - heading "Final response" [level=2]
      - paragraph:
        - strong: Final independent audit passed.
        - text: The completed notes prove the nonlinear-core extension, admissible graph-shear transfer, and displayed kernel identities under their stated hypotheses.
      - paragraph: "I checked:"
      - list:
        - text: The projection acts on affine-periodic
        - strong: potentials
        - text: ", with the required operator-ball constraint and positive-definite metrics."
        - text: Contact and translation pairing justify the nonlinear extension for periodic
        - math:
          - generic: W
          - generic: "1"
          - generic: ","
          - generic: "2"
        - text: W
        - generic: 1,2
        - text: perturbations. Its two lower bounds are combined by a maximum, without double-counting a reserve.
        - listitem: The graph source map is globally bi-Lipschitz under the explicit contraction hypothesis. Its transformed lattice, affine mean, nonconstant Jacobian weight, and normalized integral factor are correct.
        - text: The passage to an arbitrary fixed lattice has the stated controlled
        - math:
          - generic: O
          - generic: (
          - generic: "1"
          - generic: /
          - generic: "N"
          - generic: )
        - generic: O(1/N)
        - text: boundary error.
        - text: The critical-kernel inversion, polyaffine tangent, rational denominators, and quartic coefficient adjustment are correct. The missing “
        - math:
          - generic: +
        - generic: +
        - text: ” in equation (11) has been corrected and verified.
        - text: The global interior domination, boundary-plane inequalities, and touching equality for the target
        - math:
          - generic: J
          - generic: k
        - text: J
        - generic: k
        - text: remain explicitly unpaid. Neither note claims that these operations settle the original universal question.
      - paragraph:
        - text: The audit is saved in
        - button "CONSTRUCTION_CORE_GRAPH_AUDIT.md":
          - text: CONSTRUCTION_CORE_GRAPH_AUDIT.md
        - text: .
      - paragraph:
        - strong: No substantive correction remains pending. No computation, numerical search, source retrieval, or additional worker was used.
