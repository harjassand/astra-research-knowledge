# Binding compliance: an all-frequency two-band certificate

This result is for the supplied scalar, rank-one, ideal-contact harmonic model. It uses the full-band trace, logarithmic and compliance identities supplied in sources F and C. It does not establish a material device or historical priority.

## Exact candidate and resources

Take backbone mass 1, side mass 1, intercell spring 1, and internal spring 4. The two endpoint matrices are

\[
D_0=\begin{pmatrix}4&-4\\-4&4\end{pmatrix},\qquad
D_\pi=\begin{pmatrix}8&-4\\-4&4\end{pmatrix}.
\]

Thus its full bands are \([0,p]\cup[r,s]\), where

\[
p=\sqrt5-1,\qquad r=2\sqrt2,\qquad s=\sqrt5+1.
\]

In particular \(p^2+s^2-r^2=4\), \(ps/r=\sqrt2\), and
\(p^{-2}+s^{-2}-r^{-2}=5/8\). The supplied third moment gives

\[
D(\chi):=\int_0^\infty
\frac{1_{[0,\sqrt2]}-\chi}{w^3}\,dw
=C_{\rm CM}/4.
\]

The candidate has \(D_*=1/16\), equivalently \(C_{\rm CM}=1/4\). This agrees with the direct static compliance \(1/k=1/4\).

## The exact dual is defined by interpolation

Here \(g(w)=(w/\sinh w)^2\). Define the real numbers \(\lambda,\mu,\eta\) uniquely by

\[
F(w)=w^3g(w)+\lambda w^2+2\mu w^4-\eta,
\qquad F(p)=F(r)=F(s)=0.
\]

Uniqueness follows from interpolation at the three distinct squared nodes \(p^2,r^2,s^2\). The standard-library exact-rational interval program `certify_dual.py` proves

\[
-0.591137020902620<\lambda<-0.591137020902619,
\]
\[
0.0197894500757470<\mu<0.0197894500757471,
\qquad
0.351276884506192<\eta<0.351276884506193.
\]

The program's more precise rational intervals are in `CERTIFIED_MULTIPLIERS.txt`. It brackets square roots with integer `isqrt` and decimal-grid rational endpoints. For positive \(w<4\), it brackets \(\sinh w\) by 80 positive Taylor terms and a geometric bound for the remaining positive tail. It then evaluates the exact quadratic Lagrange interpolation formula with rational interval operations. No sampled frequency signs are used by the proof.

## A finite-sign-variation lemma for convergent power series

Let \(f(x)=\sum_j a_jx^{e_j}\), with strictly increasing integer exponents bounded below, converging with its termwise derivatives uniformly on every compact subinterval of \((0,\infty)\). Discard zero coefficients. If the coefficient signs have a finite number \(V\) of variations, then \(f\) has at most \(V\) positive zeros counted with multiplicity.

Proof: induct on \(V\). With no variation, every nonzero term has one sign and so does their convergent sum. Otherwise let \(k\) be the exponent of the first coefficient whose sign differs from the initial coefficient sign. In
\[
h(x)=\frac{d}{dx}\bigl[x^{-k}f(x)\bigr]
=\sum_j a_j(e_j-k)x^{e_j-k-1},
\]
every earlier coefficient changes sign, the coefficient at exponent \(k\) disappears, and every later sign is preserved. Consequently the first sign variation is removed, with at most \(V-1\) remaining. By induction, \(h\) has at most \(V-1\) positive zeros. Multiplication by \(x^{-k}\) preserves positive zeros and multiplicities; Rolle's theorem, including repeated roots, would give at least \(V\) zeros of \(h\) if \(f\) had at least \(V+1\). Contradiction. This argument also rules out infinitely many positive zeros by selecting any finite number of them.

## All-frequency root count

Multiply \(F\) by the positive factor \(\sinh^2w/w^2\) for \(w>0\). The resulting entire function is

\[
Q(w)=w^3+\lambda\sinh^2w+2\mu w^2\sinh^2w
-\eta\frac{\sinh^2w}{w^2}.
\]

Let \(a_n=2^{2n-1}/(2n)!>0\), so \(\sinh^2w=\sum_{n\ge1}a_nw^{2n}\). The constant coefficient of \(Q\) is \(-\eta\), its sole odd coefficient is the positive coefficient of \(w^3\), and the even coefficients are \(a_nB_n\), with

\[
B_1=\lambda-\eta/3,
\qquad
B_n=\lambda+\mu n(2n-1)
-\frac{4\eta}{(2n+2)(2n+1)}\quad(n\ge2).
\]

Since \(\mu>0\) and \(\eta>0\), \(B_2-B_1=6\mu+\eta/5>0\), and \(B_n\) strictly increases thereafter, tending to positive infinity. Therefore the even coefficients have at most one change from negative to positive. Adding the one positive odd coefficient at degree three gives at most three coefficient sign variations in all. In fact the exact interval program verifies \(B_1,B_2,B_3,B_4<0<B_5\), so the variations are exactly three.

The lemma shows that \(Q\), and hence \(F\), has at most three positive roots counted with multiplicity. Its known distinct roots \(p,r,s\) exhaust that bound and are all simple. Also \(F(0)=-\eta<0\) and \(F(w)>0\) for all sufficiently large \(w\), since \(2\mu w^4\) dominates. The entire frequency axis therefore has the signs

\[
F<0\text{ on }(0,p)\cup(r,s),\qquad
F>0\text{ on }(p,r)\cup(s,\infty).
\]

## Global comparison over every legal finite internal network

Set
\[
R(w)=F(w)/w^3
=g(w)+\lambda/w+2\mu w-\eta/w^3.
\]
The candidate indicator equals one exactly where \(R<0\). For every other admitted finite network, \(0\le\chi\le1\), so pointwise
\(R(\chi-\chi_*)\ge0\). The trace and logarithmic moments agree at the fixed masses and intercell spring. Hence

\[
\int_0^\infty R(\chi-\chi_*)\,dw
=J(\chi)-J_*+\eta[D(\chi)-D_*].
\]

The compliance cap gives \(D(\chi)\le D_*\), so

\[
J(\chi)-J_*
=\int R(\chi-\chi_*)\,dw-\eta[D(\chi)-D_*]\ge0.
\]

All integrals of differences are well defined: both connected finite spectra equal one on a nonzero interval next to zero and vanish beyond finite frequencies. The dual's apparent singularities introduce no extra limiting assumption.

Thus no finite positive internal mass/spring graph in the declared fixed-resource model improves on the spring-4 one-pendant design. Equality forces the same complete active spectrum almost everywhere and, because \(\eta>0\), saturation of the compliance cap. Equivalent isospectral networks or additional dark modes are not excluded.

## Conditional frontier beyond the supplied point

The root-count argument is not confined to the displayed numerical resource point. At any positive temperature, scale \(x=w/(2\theta)\), \(\bar\lambda=\lambda/(2\theta)\), \(\bar\mu=2\theta\mu\), and \(\bar\eta=\eta/(2\theta)^3\). The same series and coefficient monotonicity hold with barred multipliers. Therefore any actual one-pendant spectrum whose three-edge interpolated dual has \(\mu>0\) and \(\eta>0\) is globally optimal at its fixed masses and binding compliance cap. The limiting case \(\mu=0\), \(\lambda>0\), \(\eta>0\) also works: the even brackets increase to the positive number \(\bar\lambda\), and the positive tail comes from \(\lambda w^2\).

A numerical continuation finds \(\mu<0\) for the fixed-mass one-pendant design by \(k=16\). Its dual is then negative at sufficiently high frequency, so this finite two-band negative-set certificate cannot remain valid. That observation alone is not a proof of a better legal network. It motivates an actual two-pendant construction with one very stiff branch, which the parent is independently executing. At a \(\mu=0\) effective-backbone design, the trace term drops out, so the same dual can furnish an all-network lower bound even if some trace resource is placed at frequencies tending to infinity. Finite positive networks, their actual costs and full bands must still be supplied to establish attainability or nonattainment of such a bound.
