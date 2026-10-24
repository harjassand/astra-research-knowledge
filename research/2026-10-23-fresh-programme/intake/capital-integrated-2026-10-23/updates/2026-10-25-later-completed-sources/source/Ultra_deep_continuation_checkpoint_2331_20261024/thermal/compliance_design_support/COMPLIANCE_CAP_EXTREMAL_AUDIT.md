# Compliance-capped Bose design: exact moment, finite-order dual, and nonattainment

## Scope and conclusion

This note fixes a backbone mass \(m\), total mass \(M>m\), one intercell spring \(K\), and a cap \(C\le C_{\max}\) on the static compliance conjugate to the internal-centre-of-mass displacement relative to the backbone. It concerns the scalar rank-one harmonic model and ideal ballistic Bose functional only.

The compliance cap is exactly a third signed spectral moment, not a bound on total internal spring material. A regular three-moment dual has at most five positive roots; therefore its minimizing spectrum has at most three passbands and the Foster/Stieltjes construction realizes it with at most two side resonators. However, **global finite-star attainment is not universal**: I give an explicit valid resource family for which the infimum is approached by two-resonator stars whose final optical band escapes to infinite frequency, and no finite network attains the infimum. Thus a bounded active order for an approximating sequence does not guarantee a finite minimizing device.

## 1. Exact compliance moment

Use squared endpoint notation
\[
0=\alpha_0<\beta_0<\alpha_1<\beta_1<\cdots<\alpha_{n-1}<\beta_{n-1},
\]
so the bands in frequency are \([\sqrt{\alpha_j},\sqrt{\beta_j}]\). Put \(S=4K\), \(m_s=M-m\), \(\Omega^2=S/M\), and
\[
A=\sum_j(\beta_j-\alpha_j),\qquad
P=\frac{\prod_j\beta_j}{\prod_{j\ge1}\alpha_j}.
\]
For an admitted cell, \(A=S/m\) and \(P=S/M=\Omega^2\).

The internal-centre-of-mass relative coordinate is
\[
Y=\sum_j\frac{m_j}{m_s}x_j-x_b,
\]
with static compliance \(C\). Its spectral measure representation is
\[
q(t)=v^T(D_0+tI)^{-1}v
=\frac{1}{Mt}+\sum_\ell\frac{c_\ell}{t+r_\ell^2},\quad c_\ell>0,
\qquad \tau=\sum_\ell\frac{c_\ell}{r_\ell^2},
\qquad C=\left(\frac{M}{m_s}\right)^2\tau.
\]
The determinant ratio is
\[
\frac{\prod_j(t+\beta_j)}{\prod_j(t+\alpha_j)}=1+S q(t).
\]
Expanding at zero, the endpoint ratio is
\[
\frac{P}{t}\left[1+t\left(\sum_j\frac1{\beta_j}-\sum_{j\ge1}\frac1{\alpha_j}\right)+O(t^2)\right],
\]
while the resolvent form is \(S/(Mt)+1+S\tau+O(t)\). Equating coefficients gives
\[
\sum_j\frac1{\beta_j}-\sum_{j\ge1}\frac1{\alpha_j}
=\frac{M}{S}+M\tau
=\frac{M}{S}+\frac{m_s^2}{M}C.
\]
For \(\chi(\omega)=\sum_j\mathbf1_{[\sqrt{\alpha_j},\sqrt{\beta_j}]}(\omega)\), endpoint integration is therefore the exact moment identity
\[
D_3:=\int_0^\infty\frac{\mathbf1_{[0,\Omega]}(\omega)-\chi(\omega)}{\omega^3}\,d\omega
=\frac{m_s^2}{2M}C\ge0.
\]
Consequently \(C\le C_{\max}\) is equivalent to \(D_3\le D_{\max}:=m_s^2C_{\max}/(2M)\), in addition to the fixed trace and logarithmic moments. For a one-pendant cell, \(C=1/k\).

This moment is distinct from backbone incident stiffness. If
\[
E=\sum_j(\beta_j^2-\alpha_j^2),
\]
then the large-\(t\) expansion gives
\[
\sum_{j\text{ in Foster star}} k_j
=\frac{S(E-A^2)}{2A^2}.
\]
For any original network this quantity equals its backbone-diagonal internal stiffness \((H_0)_{bb}\); internal-to-internal springs can add more total spring material. The compliance bound instead fixes/bounds the small-frequency coefficient \(\tau\). One cannot exchange these costs.

## 2. Three-moment dual and bounded active order when a regular dual exists

Set \(x=\omega^2\), \(f(x)=\chi(\sqrt x)\), and \(f_0=\mathbf1_{[0,\Omega^2]}\). The three constraints and objective are
\[
T=\int_0^\infty f(x)\,dx=\frac{S}{m},
\quad L=\frac12\int_0^\infty\frac{f-f_0}{x}\,dx=0,
\quad D=\frac12\int_0^\infty\frac{f_0-f}{x^2}\,dx\le D_{\max},
\]
\[
J=\frac12\int_0^\infty\frac{g_\theta(\sqrt x)}{\sqrt x}f(x)\,dx.
\]
For Lagrange multipliers \(\lambda,\mu\) and a nonnegative cap multiplier \(\eta\), pointwise minimization over \(0\le f\le1\) selects \(f=1\) where
\[
\Phi(x)=H_\theta(x)+2\lambda x^2+\mu x-\eta<0,
\qquad H_\theta(x)=x^{3/2}g_\theta(\sqrt x).
\]

A finite root bound follows from a self-contained hyperbolic-series calculation. Scale \(z=\sqrt{x}/(2\theta)\), and let \(G(y)=y^{5/2}/\sinh^2\sqrt y\). Then \(H_\theta'''(x)\) has the sign of
\[
N(z)=\left(6z^2+\frac{15}{8}\right)\cosh4z
+\left(12z^2-\frac{15}{2}\right)\cosh2z-18z^2+\frac{45}{8}
-\left(z^3+\frac{33z}{4}\right)\sinh4z
+\left(-10z^3+\frac{33z}{2}\right)\sinh2z,
\]
with \(G'''(z^2)=N(z)/(8z\sinh^6z)\). Its even power series starts at \(z^4\). For \(n\ge2\), the coefficient of \(z^{2n}\) is
\[
\frac{4^{2n}}{(2n)!}\left[
-\frac{(2n)^3-27(2n)^2+158(2n)-120}{64}
-\frac{5(2n)^3-27(2n)^2-11(2n)+30}{4^{n+1}}
\right].
\]
The coefficients are negative for \(n=2,3\), positive for \(n=4,\ldots,9\), and negative for every \(n\ge10\) (both cubic numerators are positive for \(2n\ge20\)). Thus the coefficient sequence has three sign variations. The generalized Descartes rule for a convergent real power series bounds the number of positive zeros, counted with multiplicity, by three. Also \(N(z)<0\) near zero (leading coefficient \(-3z^4\)) and for large \(z\) (leading exponential term \(-z^3\sinh4z\)). The total positive-zero multiplicity is therefore even, so \(H_\theta'''\) has at most two positive zeros.

Rolle's theorem now shows \(\Phi\) has at most five distinct positive roots. When a finite-multiplier optimum exists, its selected set is consequently a union of at most three intervals. Strict three-band endpoint lists are actually realizable by the complete inverse construction: with at most three bands, the positive Foster star has at most two side masses/springs. This is a global certificate over the relaxed \(0\le f\le1\) class and an actual passive-network certificate for the resulting finite bands; it is stronger than merely optimizing unconstrained indicators.

The cap is feasible for every positive \(C_{\max}\): a one-pendant cell has \(C=1/k\), so any \(k>1/C_{\max}\) is strictly feasible. If the uncapped optimum already has \(C\le C_{\max}\), the existing one-resonator theorem remains the constrained global result. For active caps, the root bound supplies order \(\le2\) **conditional on an attained regular dual solution**. The next construction shows why that qualification matters.

## 3. An explicit nonattainment family

It suffices to use dimensionless \(\theta=1/2\), where
\[
G(x)=H_{1/2}(x)=\frac{x^{5/2}}{\sinh^2\sqrt x}.
\]
Let \(z=\sqrt x\). Direct differentiation gives
\[
G''(x)=\frac{z\,N_2(z)}{4\sinh^4z},
\quad N_2(z)=6z^2+4z^2\sinh^2z-18z\sinh z\cosh z+15\sinh^2z.
\]
The coefficient of \(z^2\) in \(N_2\) is 3. For \(n\ge2\), the coefficient of \(z^{2n}\) is
\[
\frac{2^{2n-1}}{(2n)!}(4n^2-20n+15).
\]
Its signs are negative at \(n=2,3,4\) and positive for \(n\ge5\). The series has two sign variations, so \(N_2\) has at most two positive zeros counting multiplicity. It is positive near zero and infinity, but
\[
N_2(1)=\frac{e^2+37e^{-2}-14}{4}<0
\]
(using \(7<e^2<8\), which makes \(e^2+37/e^2<14\)). Hence \(G''\) has exactly two positive simple zeros \(x_-<x_+\), with signs +,−,+.

Since \(G'(0+)=0\), \(G'(\infty)=0^-\), and \(x_+\) is the minimum of \(G'\), set
\[
b=-\frac12G'(x_+)>0.
\]
The function \(G'(x)+b\) has exactly two simple positive zeros \(u_1<u_2\): it is positive near zero and infinity and equals \(-b\) at \(x_+\); its derivative \(G''\) has only the two zeros already proved. Therefore \(F_0(x)=G(x)+bx\) has a strict local maximum at \(u_1\) and minimum at \(u_2\). Define
\[
v=\frac{F_0(u_1)+F_0(u_2)}{2}>0,\qquad \Phi_0(x)=G(x)+bx-v.
\]
The strict inequality \(v>0\) follows from \(F_0(u_2)=G(u_2)+bu_2>0\). The signs of \(\Phi_0\) are negative at zero, positive at its local maximum, negative at its local minimum, and positive at infinity. Since \(\Phi_0''=G''\) has exactly two positive zeros, Rolle's theorem excludes any additional roots; \(\Phi_0\) has exactly three simple positive roots \(0<a_1<a_2<a_3\), with sign pattern
\[
\Phi_0<0\text{ on }(0,a_1)\cup(a_2,a_3),\qquad
\Phi_0>0\text{ on }(a_1,a_2)\cup(a_3,\infty).
\]

Choose the reference rigid endpoint and the target moments by
\[
\Omega^2=\frac{a_1a_3}{a_2},\quad
A_*=a_1+a_3-a_2,\quad
D_*=\frac{(a_2-a_1)(a_3-a_2)}{2a_1a_2a_3}>0.
\]
The two-band indicator
\[
f_*(x)=\mathbf1_{[0,a_1]\cup[a_2,a_3]}(x)
\]
has exactly \(L=0\), \(D=D_*\), and trace \(A_*\). In particular,
\[
A_* -\Omega^2=\frac{(a_2-a_1)(a_3-a_2)}{a_2}>0.
\]
The logarithmic moment follows from \(a_1a_3/a_2=\Omega^2\); the compliance formula follows by integrating \(x^{-2}/2\) over the acoustic deficit and the second band.

Now fix any \(S>0\) and any \(A>A_*\), and define actual resources
\[
K=S/4,\quad m=S/A,\quad M=S/\Omega^2,
\quad C_{\max}=\frac{2M D_*}{(M-m)^2}.
\]
Because \(A>A_*>\Omega^2\), these have \(0<m<M\) and \(C_{\max}>0\). A one-pendant cell with sufficiently large finite spring is feasible under this cap.

Nevertheless the full fixed-\((m,M,K,C_{\max})\) infimum is not attained. First, \(f_*\) is a global lower-bound certificate even though it has the wrong trace. For any measurable \(0\le f\le1\) with \(L(f)=0\) and \(D(f)\le D_*\), the Lagrangian density
\[
A_0(x)=\frac{\Phi_0(x)}{2x^2}
=\frac{g_{1/2}(\sqrt x)}{2\sqrt x}+\frac{b}{2x}-\frac{v}{2x^2}
\]
selects exactly \(f_*\). Thus \(I:=\int A_0(f-f_*)\,dx\ge0\). Since \(I=J(f)-J(f_*)+b[L(f)-L(f_*)]+v[D(f)-D_*]\), every spectrum satisfying the full constraints obeys
\[
J(f)-J(f_*)=I-v[D(f)-D_*]\ge0.
\]
Equality forces \(f=f_*\) almost everywhere because \(\Phi_0\) has only three zero points. But a full-resource spectrum has trace \(A>A_*\), whereas \(f_*\) has trace \(A_*\). Hence no finite network attains this lower bound.

To show the lower bound is the actual infimum, let \(\delta=A-A_*>0\) and add a high squared-frequency band \([R,R+\delta]\). For each sufficiently large finite \(R\), adjust the three low endpoints to \(a_R,b_R,c_R\) near \(a_1,a_2,a_3\) so that
\[
a_R+c_R-b_R=A_*,
\]
\[
\frac12\left[\log a_R+\log(c_R/b_R)+\log((R+\delta)/R)-\log\Omega^2\right]=0,
\]
\[
\frac12\left[\frac1{a_R}-\frac1{\Omega^2}-\frac1{b_R}+\frac1{c_R}-\frac1R+\frac1{R+\delta}\right]=D_*.
\]
At \(R=\infty\), these equations reduce to the definitions of \(a_1,a_2,a_3\). The Jacobian of the low-endpoint trace, log and inverse-cube moments is
\[
\det\frac{\partial(T,L,D)}{\partial(a,b,c)}
=\frac{(a-b)(a-c)(b-c)}{4a^2b^2c^2}\ne0,
\]
so the implicit-function theorem supplies exact nearby endpoints for every sufficiently large finite \(R\). They remain strictly ordered below \(R\). The resulting three-band list
\[
0<a_R<b_R<c_R<R<R+\delta
\]
has trace \(A\), the fixed product \(S/M=\Omega^2\), and compliance moment \(D_*=m_s^2 C_{\max}/(2M)\). The complete Foster inverse realization therefore gives an actual positive star with two side masses/springs for each finite \(R\).

As \(R\to\infty\), the low endpoints converge to \(a_1,a_2,a_3\), while the Bose integral of the added high band vanishes exponentially. Hence \(J_R\to J(f_*)\). Combined with the dual lower bound, this proves the full finite-network infimum equals \(J(f_*)\) but is **not achieved**. A band of fixed squared-frequency width \(\delta\) escapes to infinite frequency. The sequence has bounded active order (two resonators), but unbounded frequency/stiffness resources.

For orientation, the exact implicit construction gives approximately
\[
a_1\simeq4.34159034,\quad a_2\simeq12.74304855,\quad a_3\simeq32.47705265,
\quad \Omega^2\simeq11.06501772,\quad A_*\simeq24.07559444,
\quad D_*\simeq0.04613612.
\]
Taking \(S=1\), \(A=A_*+1\) gives \(K=1/4\), \(m\simeq0.03987941\), \(M\simeq0.09037491\), and \(C_{\max}\simeq3.27049628\). The proof uses the implicit exact definitions above; these decimals only orient the scale.

## 4. Answer to the finite-star question

The complete Foster/Stieltjes comparator gets the same \(m,M,K,C_{\max}\) and is included in the proof. Compliance adds a real inverse-cube resource; it is not interchangeable with an internal spring-sum budget. In regular cases where the three-moment dual is attained with the trace equality represented by a finite spectrum, the root bound yields a global optimum with at most three passbands, realized by at most two side resonators. But the explicit family above shows that one cannot claim universal finite-star attainment: the constrained global infimum can require an optical band at infinity. The exact failure is nonattainment, not a failure of Foster realizability for any finite endpoint list.

No material, device, finite-contact conductance, or fabrication claim follows. The escaping sequence explicitly spends unbounded frequency/stiffness range; adding such a resource cap would define a different optimization problem.

General limitation: this counterexample disproves universal finite-star attainment, but does not classify when a general three-moment dual is attained, when trace escapes in a minimizing sequence, or whether a finite frequency/stiffness cap restores attainment. Those general compactness and cap-dependence questions remain open here.

## Append-only correction and nonattainment recheck

The coefficient signs quoted in Section 2 have **two** sign variations, not three: negative for `n=2,3`, positive for `n=4,...,9`, and negative for `n>=10`. The generalized Descartes bound gives at most two positive zeros of `N` directly (the endpoint signs also force even total multiplicity). Thus the conditional root conclusion is unchanged or strengthened: the third derivative of `H_theta` has at most two positive zeros, so a finite regular selector `H_theta + 2 lambda x^2 + mu x - eta` has at most five positive roots and at most three selected bands. Dual attainment and escape remain separate issues.

I rechecked the nonattainment argument independently. At `theta=1/2`, the objective density is `sqrt(x)/(2 sinh^2(sqrt(x)))`; multiplying the objective plus moment multipliers by `2x^2` gives `Phi0(x)=G(x)+b x-v`, where `G(x)=x^(5/2)/sinh^2(sqrt(x))`. The two-root sign pattern of `G''` gives three roots `a1<a2<a3` and negative set `(0,a1) union (a2,a3)`. For `f*=1_[0,a1] union [a2,a3]`, the dual integral `I` is nonnegative for every `0<=f<=1`, and for `L=0, D<=D*` it yields `J(f)-J(f*)=I-v(D-D*)>=0`. Equality forces `f=f*` almost everywhere; its trace is `A*`, so no spectrum with target trace `A>A*` attains the lower bound.

The upper sequence is exact at every finite `R`: append the squared-frequency band `[R,R+delta]`, where `delta=A-A*>0`, and solve the three low-endpoint equations in Section 3. The Jacobian is nonzero for strict `a1<a2<a3`; the implicit-function theorem preserves endpoint ordering and solves trace, log/product, and compliance moments exactly for sufficiently large `R`. Each list `0<a_R<b_R<c_R<R<R+delta` is strictly interlaced, so the complete Foster construction gives a positive two-side-resonator star with the same `m,M,K,Cmax`. Its objective converges to `J(f*)` because the low endpoints converge and the Bose weight of the added band tends to zero. This confirms a fixed-resource nonattainment counterexample, not merely a relaxed-indicator artifact. The general criterion for when this escape occurs is not established here.
