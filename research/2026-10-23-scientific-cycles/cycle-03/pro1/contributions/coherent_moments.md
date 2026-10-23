# Exact insertion hierarchy and bounded depth corrector

Contributor: /root/coherent_moments  
Date: 22 October 2026 (Brisbane)  
Status: complete analytic contribution with supplementary exact algebra checks. The root owns the positive-observable tilt, exponential escape proof and communication consequence. This is internal proof work, not external certification or a historical-priority claim.

## 1. Source, operator model and hypotheses

Actual source read: Cycle2 COHERENT_CAPACITY_FLOOR.tex (entire-bath representation and bounded depth algebra), SUPPLEMENTARY_RESULTS.tex (coherent drift and normal-form algebra), and reviews/COHERENT_DRIFT_CHECK.md. No earlier capacity proof was rerun.

The bath is the exact two-seed Fock space \(E=\mathbb C^2\otimes\mathcal F(\mathbb C^2)\). Creation operators prepend colors, \(S_a|j,w\rangle=|j,aw\rangle\). The vacuum exchange is \(R\), with
\[
S_a^*S_b=\delta_{ab}I,\quad \sum_aS_aS_a^*=I-P_0,\quad
R=R^*,\quad R^2=P_0,\quad RS_a=S_a^*R=0.
\]
The depth is \(L|j,w\rangle=|w||j,w\rangle\). Both seeds and their exchange remain present. The device is
\[
U=\begin{pmatrix}R&S_1&S_2\\S_1^*&0&0\\S_2^*&0&0\end{pmatrix},
\qquad V=\alpha U+i\beta I,\qquad
\alpha>0,\quad \alpha^2+\beta^2=1.
\]
The initial derivation uses
\[
\rho=\begin{pmatrix}q&ig&0\\-ig&a&0\\0&0&a\end{pmatrix},
\quad 0<q<1/2,\quad a=(1-q)/2,\quad g\in\mathbb R,\quad g^2\le qa.
\tag{1}
\]
These are the exact density positivity conditions. Put \(\Phi(\tau)=\operatorname{Tr}_{\rm port}V(\rho\otimes\tau)V^*\) and \(T=\Phi^*\). No physical initializer is changed. The selected operation begins at the actual
\[
\tau_\pi=\frac{I_2}{2}\otimes\frac23\sum_w6^{-|w|}|w\rangle\langle w|.
\]

## 2. Exact reduced channel and first creation moment

Let \(S=S_1\), \(D=S^*-S\), and \(A=qR+igD\). The Schrödinger channel is
\[
\begin{aligned}
\Phi(\tau)={}&\beta^2\tau+\alpha^2\left[
q\left(R\tau R+\sum_aS_a^*\tau S_a\right)
+a\sum_aS_a\tau S_a^*
+igR\tau S^*-igS\tau R\right]\\
&+i\alpha\beta(\tau A-A\tau).
\end{aligned}
\tag{2}
\]
The normal unital dual therefore obeys, for every bounded \(X\),
\[
\begin{aligned}
T(X)={}&\beta^2X+\alpha^2\left[
q\left(RXR+\sum_aS_aXS_a^*\right)
+a\sum_aS_a^*XS_a
+igS^*XR-igRXS\right]\\
&+i\alpha\beta[A,X].
\end{aligned}
\tag{3}
\]
Write \(C(X)=\sum_a S_aXS_a^*\). Direct substitution yields
\[
\boxed{T(S)=(\beta^2+\alpha^2a)S+\alpha^2qC(S)
+i\alpha^2gR-i\alpha\beta qSR
-\alpha\beta g(I-SS^*).}
\tag{4}
\]
In the actual diagonal initializer the expectations of \(S,C(S),R,SR\) vanish and \(\operatorname{Tr}\tau_\pi SS^*=1/6\). Hence
\[
\boxed{\operatorname{Tr}[\Phi(\tau_\pi)S]=-\frac56\alpha\beta g.}
\tag{5}
\]
For the selected positive \(\beta,g\), this has the opposite sign from the positive real coherence needed to cancel outward depth drift. This one-step finding alone does not establish long-time failure.

A scalar recursion for \(\operatorname{Tr}(\tau S)\) is not closed: deeper insertion and root coherences occur in (4). One cannot iterate only the coefficient multiplying \(S\).

## 3. The entire creation-word insertion hierarchy

For a nonempty word \(w\), set \(F_{k,w}=C^k(S_w)\), \(k\ge0\). This operator inserts \(w\) after the existing prefix of length \(k\). Since \(C^k\) is an isometric *-homomorphism into the corner of depth at least \(k\), \(\|F_{k,w}\|=1\).

For \(k\ge1\), all root terms vanish, and
\[
S^*F_{k,w}=F_{k-1,w}S^*,\qquad F_{k,w}S=SF_{k-1,w}.
\]
Consequently,
\[
\boxed{\begin{aligned}
T(F_{k,w})={}&\beta^2F_{k,w}
+\alpha^2[qF_{k+1,w}+(1-q)F_{k-1,w}]\\
&-\alpha\beta g[(F_{k-1,w}-F_{k,w})S^*
+S(F_{k-1,w}-F_{k,w})],\quad k\ge1 .
\end{aligned}}
\tag{6}
\]
No boundary is imposed at large \(k\).

Let \(\operatorname{rot}(w)\) move the first letter of \(w\) to its end, and let \(\operatorname{tail}(w)\) delete that first letter. The empty tail has creation operator \(I\). At \(k=0\),
\[
\begin{aligned}
T(S_w)={}&\beta^2S_w+\alpha^2[qC(S_w)+aS_{\operatorname{rot}(w)}
+ig\,1_{\{w_1=1\}}S_{\operatorname{tail}(w)}R]\\
&-i\alpha\beta qS_wR-\alpha\beta g[D,S_w].
\end{aligned}
\tag{7}
\]
This includes every exceptional-root contribution.

## 4. Norm-convergent Poisson corrector and telescoping commutator

Because \(q<1/2\),
\[
r=\frac q{1-q}\in(0,1),\qquad
B_w=\sum_{k=0}^{\infty}r^kF_{k,w}
\tag{8}
\]
converges in operator norm, with \(\|B_w\|\le1/(1-r)\). For \(w=1\), the norm bound is exact: on the word \(1^N\), all allowed insertions have the same output and total coefficient \((1-r^{N+1})/(1-r)\).

The channel and commutator maps are bounded, so the geometric series may be substituted and summed in norm. The bulk cancellation uses \(r-q-(1-q)r^2=0\), giving
\[
\begin{aligned}
(I-T)B_w={}&\alpha^2a(2S_w-S_{\operatorname{rot}(w)})
+i\alpha\beta qS_wR\\
&-i\alpha^2g\,1_{\{w_1=1\}}S_{\operatorname{tail}(w)}R
+\alpha\beta g[D,B_w].
\end{aligned}
\tag{9}
\]
For \(w=1\), write \(B=B_1\). Then
\[
\boxed{(I-T)B=\alpha^2aS+i\alpha\beta qSR-i\alpha^2gR
+\alpha\beta g[D,B].}
\tag{10}
\]

A crude bound \(2\|D\|\|B\|\) is unnecessarily singular at \(q=1/2\). Instead,
\[
\sum_{k\ge1}r^k(F_{k-1,w}-F_{k,w})
=S_w-(1-r)B_w
\]
gives the exact commutator identity
\[
\boxed{
[D,B_w]=S^*S_w+S_wS-(1-r)(B_wS^*+SB_w),\qquad
\|[D,B_w]\|\le4.}
\tag{11}
\]
In particular,
\[
[D,B]=I+S^2-(1-r)(BS^*+SB).
\tag{12}
\]
The norm bound is uniform as \(q\uparrow1/2\), even though \(B\) itself is not uniformly bounded.

For a finite exact algebra check, define \(B_N=\sum_{k=0}^Nr^kF_{k,1}\). The exact remainder formulas are
\[
\begin{aligned}
(I-T)B_N={}&\alpha^2aS+i\alpha\beta qSR-i\alpha^2gR
+\alpha\beta g[D,B_N]
+\alpha^2qr^N(F_{N,1}-F_{N+1,1}),\\
[D,B_N]={}&I+S^2-(1-r)(B_NS^*+SB_N)
-r^{N+1}(F_{N,1}S^*+SF_{N,1}).
\end{aligned}
\tag{13}
\]
Both remainders vanish in norm. These identities do not refer to a finite bath.

## 5. Corrected depth and root square completion

Write \(\operatorname{Re}X=(X+X^*)/2\). The inherited bounded depth increment is
\[
\Delta L:=T(L)-L
=\alpha^2(1-2q)I+\alpha^2qP_0-2\alpha\beta g\operatorname{Re}S.
\tag{14}
\]
It is first an equality on \(\operatorname{Dom}L\), whose right side is the bounded extension. Set
\[
c=\frac{2\beta g}{\alpha a},\qquad
H=L-c\operatorname{Re}B,\qquad
\|c\operatorname{Re}B\|\le
\frac{4|\beta g|}{\alpha(1-2q)}=:C_0 .
\tag{15}
\]
Each \(F_{k,1}\) raises depth by one. Norm convergence of \(B_N\) and \([L,B_N]=B_N\), plus closedness of \(L\), shows that \(B\) preserves \(\operatorname{Dom}L\) and \([L,B]=B\). Its adjoint has the corresponding property. Thus \(H\) is self-adjoint on \(\operatorname{Dom}L\), a bounded perturbation of depth.

Taking real parts in (10) removes only the anti-Hermitian term \(-i\alpha^2gR\). The remaining root term must be retained. Combining (10) and (14),
\[
\boxed{
\Delta H=\mu I+A_0P_0+\kappa\operatorname{Re}(iSR)
+\frac{2\beta^2g^2}{a}\operatorname{Re}[D,B],}
\tag{16}
\]
where
\[
\mu=\alpha^2(1-2q),\qquad A_0=\alpha^2q>0,\qquad
\kappa=\frac{2\beta^2gq}{a}.
\]

Put \(J=SR\). Then \(J^*J=P_0\), \(JJ^*=SP_0S^*=:Q_1\), and \(P_0Q_1=0\). For every vector \(x\),
\[
|\langle x,\operatorname{Re}(iJ)x\rangle|
\le\|P_0x\|\|Q_1x\|.
\]
Scalar square completion therefore gives the operator inequality
\[
A_0P_0+\kappa\operatorname{Re}(iJ)
\ge-\frac{\kappa^2}{4A_0}Q_1
\ge-\frac{\kappa^2}{4A_0}I.
\tag{17}
\]
Together with (11),
\[
\boxed{
\Delta H\ge\nu I,\qquad
\nu=\alpha^2(1-2q)
-\frac{8\beta^2g^2}{a}
-\frac{\beta^4g^2q}{\alpha^2a^2}.}
\tag{18}
\]
This is valid for both signs of real \(g\). Its consequences below require \(\nu>0\). If the numerical lower bound is nonpositive, the exact identities still hold but this estimate proves no positive drift.

## 6. Strict positivity for the selected seed

For \(q=1/2-3\beta^2/32\), \(g=\beta/8\),
\[
C_0=\frac8{3\alpha}.
\tag{19}
\]
Using \(a\ge1/4\), \(q\le1/2\), \(\alpha^2\ge1/2\),
\[
\nu\ge\beta^2
\left(\frac3{16}-\frac{11}{16}\beta^2-\frac14\beta^4\right)
>\frac{\beta^2}{8}>0
\tag{20}
\]
throughout \(0<\beta\le1/512\). The present scientific operation fixes \(\beta=1/512\), rather than varying it with the horizon. At that fixed value, the expression (18) is exactly
\[
\nu=
\frac{3626718083480614861275163}
{5070590311629645407074262188032}
=7.152457328612333\ldots\times10^{-7},
\tag{21}
\]
and \(\nu/\beta^2=0.18749737739517514\ldots\).

## 7. No normal invariant state, including infinite-mean states

Assume \(\nu>0\). There is no normal invariant bath density.

To avoid subtracting infinite means, put \(L_M=\min(L,M)\) and \(H_M=L_M-c\operatorname{Re}B\). Every \(H_M\) is bounded. The established whole-device bounded-increment argument shows that \(T(L_M)-L_M\) is uniformly bounded and converges strongly to (14). This also follows directly from (3), since every shift changes depth by at most one. Hence \(T(H_M)-H_M\) converges strongly, with a uniform norm bound, to (16).

If a normal invariant density \(\sigma\) existed, then
\[
\operatorname{Tr}\sigma[T(H_M)-H_M]=0
\]
for every \(M\). Normal trace-class pairing permits the limit and gives
\[
0=\operatorname{Tr}(\sigma\Delta H)\ge\nu,
\]
a contradiction. The argument assumes neither finite entropy nor finite mean depth, and does not require a diagonal or faithful invariant state.

No orbit of a normal initializer is uniformly tight in finite vertex-coordinate projections. Otherwise its Cesaro averages would also be tight. The gentle compression estimate and finite-dimensional compactness yield a trace-norm convergent subsequence of those averages. Since
\[
\left\|
\Phi\!\left(\frac1N\sum_{n=0}^{N-1}\Phi^n(\tau)\right)
-\frac1N\sum_{n=0}^{N-1}\Phi^n(\tau)
\right\|_1\le2/N,
\]
the normal limit would be invariant. This contradicts the preceding conclusion.

No-invariant-state and failure of uniform tightness are weaker than exponential escape from low depth. A quantum drift inequality cannot simply be called a classical concentration theorem. The root's positive weighted-observable argument supplies that separate obligation.

For an initializer of finite mean depth, all iterated means are finite because the physical depth bandwidth is one. Then the ordinary expectation version is legitimate:
\[
\operatorname{Tr}[\Phi^n(\tau)L]
\ge\operatorname{Tr}(\tau L)+\nu n-2C_0.
\tag{22}
\]
In particular \(\operatorname{Tr}\tau_\pi L=1/2\). Equation (22) is not asserted as an ordinary difference for an infinite-mean initializer.

## 8. Anisotropic two-color addendum

The root proposed extending the mechanism beyond equal color weights. The following verifies that extension algebraically.

Let
\[
\rho=
\begin{pmatrix}
q&ig_1&ig_2\\
-ig_1&a_1&0\\
-ig_2&0&a_2
\end{pmatrix},\qquad
a_1,a_2>0,\quad a_1+a_2=1-q,\quad g_1,g_2\in\mathbb R,
\]
with \(\rho\) a density and \(0<q<1/2\). Write \(S_v=\sum_jv_jS_j\), \(A_c=\operatorname{diag}(a_1,a_2)\), and \(D_g=S_g^*-S_g\). Choose
\[
f_1=g_1/a_2,\qquad f_2=g_2/a_1,\qquad
B_f=\sum_{k\ge0}r^kC^k(S_f).
\tag{23}
\]
The sole changed diagonal-color term for \(k=0\) is \(S_{A_cf}\). For \(k\ge1\), summing color weights still gives \(1-q\), so the same geometric cancellation applies. In general the undriven boundary coefficient is
\[
\alpha^2S_{((1-q)I-A_c)f}.
\]
The choice (23) makes it exactly \(\alpha^2S_g\). The coherent root coefficient is \(S_g^*S_f=g\cdot f\). Thus
\[
\boxed{
(I-T)B_f=\alpha^2S_g+i\alpha\beta qS_fR
-i\alpha^2(g\cdot f)R+\alpha\beta[D_g,B_f].}
\tag{24}
\]
The commutator telescopes to
\[
\boxed{
[D_g,B_f]=(g\cdot f)I+S_fS_g
-(1-r)(B_fS_g^*+S_gB_f),\qquad
\|[D_g,B_f]\|\le4\|g\|_2\|f\|_2.}
\tag{25}
\]
Indeed \(\|S_f\|=\|f\|_2\) and \(\|B_f\|\le\|f\|_2/(1-r)\). Real coefficients make \(g\cdot f\) real, so its anti-Hermitian root term again drops only upon taking real parts.

Now let
\[
H_f=L-\frac{2\beta}{\alpha}\operatorname{Re}B_f .
\]
The \(S_g\) term cancels the physical coherent depth drift exactly. For \(J_f=S_fR\), \(J_f^*J_f=\|f\|_2^2P_0\); its range is orthogonal to \(P_0E\). Repeating (17) with the scalar coefficient \(2\beta^2q\) gives
\[
\boxed{
T(H_f)-H_f
\ge\left[
\alpha^2(1-2q)
-8\beta^2\|g\|_2\|f\|_2
-\frac{\beta^4q}{\alpha^2}\|f\|_2^2
\right]I.}
\tag{26}
\]
The bounded corrector norm is at most
\[
\frac{2|\beta|}{\alpha}\,
\frac{\|f\|_2}{1-r}.
\]
All signs and factors of two agree with the root's proposed formula. The root and the separate stability helper own the entropy inequalities that might make (26) positive for a larger input class. No such entropy conclusion is presumed here.

## 9. Failures and a load-bearing counterexample

- The first moment (4) is not a closed scalar recursion. Its apparent single coefficient is not a proven iteration contraction.
- The initial negative response (5) points in the wrong direction for the seed but does not replace the long-time proof.
- Crude control of \([D,B]\) would lose a factor \(1/(1-2q)\). The exact telescoping identity, not a finite experiment, removes it.
- The surviving \(SR\) term cannot be dropped. The root square completion is required.
- At \(q=1/2\), the series (8) is not norm convergent. At \(g=0\) the known critical depth process is diffusive; a strictly positive linear-escape assertion there would be false.
- Dropping the parameter condition also has a direct invariant-state counterexample: for \(q=3/4\), \(g=0\), the original \(\tau_\pi\) is normal stationary for every allowed mixing angle. No general claim of absence of normal invariant baths is justified.
- Failure of this product-input compression mechanism is not a quantum-capacity converse. It does not retire the broader fixed-angle gain question or change the proved capacity floor.

## 10. Receiving use, replay and measured costs

The reusable interface is the exact bounded corrector, its norm and depth bandwidth, and the positive drift bound retaining both seeds. These are analytic observables: no bath measurement, filter, reset, initializer substitution or extra device call is performed.

The script coherent_moments_replay.py imports the unchanged Cycle2 exact normal-form module. At two rational parameter points with opposite signs of \(g\), it verifies (4), (5), the hierarchy for \(k=1,\ldots,5\), and the exact finite-series remainder formulas (13) for \(N=0,\ldots,4\). It verifies (21) and \(\nu>\beta^2/8\) using exact rational arithmetic. These are finite checks in the exact infinite-bath algebra, not finite-bath approximations or proofs by check count. The norm limit and invariant-state argument above supply the all-length obligations.

Observed replay resources: wall time 0.10727014099393273 seconds; CPU time 0.107271178 seconds; maximum resident set 12160 KiB; Python 3.12.14. These measure that process, not discovery cost. Total inference, reading, proof discovery, energy and monetary costs were not independently metered. No purchase, external execution service, outreach or dependency installation was used.

The distinct anisotropic extension was subsequently checked by coherent_anisotropic_replay.py at unequal color weights and two nonzero coherences of opposite sign. It verifies unitality, the insertion hierarchy for four depths, and the exact finite-series resolvent and commutator remainders for five truncation orders, still in the infinite-bath operator algebra. Observed process resources: wall time 0.1368274670021492 seconds; CPU time 0.136777629 seconds; maximum resident set 12416 KiB; Python 3.12.14. These are supplementary finite identity checks, not the proof of the all-parameter addendum.

Replay from the workspace:

    python work/cycle3/contributions/coherent_moments_replay.py --representation work/cycle2/representation/exact_representation.py --output work/cycle3/contributions/coherent_moments_reproduced.json

After relocating the source, pass the actual preserved normal-form file via the representation argument. No shared local path is presumed across receiving agents.

