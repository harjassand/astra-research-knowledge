# A quantitative fast-neutral receipt: six reciprocal profiles pay the bare AE exponential cost

This is an exact internal-source inequality, not a global drift theorem. Keep
\(a=1/100,q=2\). Put

\[
P_{\rm rec}=\frac1{c+1}+\frac1{d+1},\qquad
D_c=\frac1{(c+1)(c+2)},\quad D_d=\frac1{(d+1)(d+2)}.
\]

Let \(t=\tau(x)\), and let \(t_1,t_2\) be the actual successor roots for
\(AE\to2A\) and \(AE\to CD\), respectively. At any state with \(AE>0\),

\[
\boxed{e^{t_1}+e^{t_2}-2e^t\le6(D_c+D_d).}             \tag{A1}
\]

The \(AE\)-source generator of \(P_{\rm rec}\) is exactly
\(-AE(D_c+D_d)\): \(AE\to2A\) increments both \(c,d\), while \(AE\to CD\) leaves them unchanged. Thus adding \(6r^N P_{\rm rec}\) pays the entire positive **bare** \(r^Ne^\tau\) AE contribution, with no adverse AB or CD term. The debt-weighted phase needs separate payment; (A1) is not a claim about that phase.

## 1. Nonpositivity already holds for t >= 4/5

Here \(c,d\ge A\ge1\). Write \(t_2=t+\delta\) and \(t_1=t-s\). As in the frozen finite-jump proof,

\[
\delta\le\frac1{2(c+t)(d+t)},\qquad 0<s<1,
\]

and

\[
\frac s\delta\ge
[2t(c+d+t+1)-(1-2a)]
\frac{(c+t)(d+t)}{(c+t+1)(d+t+1)}.
\]

For \(t\ge4/5,c,d\ge1\), the right side is at least

\[
[2t(t+3)-1]\left(\frac{t+1}{t+2}\right)^2
\ge\frac{10287}{4900}.
\]

Also \(\delta\le25/162\). Since \(e>8/3\), concavity gives
\(1-e^{-s}\ge(1-e^{-1})s>(5/8)s\). Meanwhile
\(e^\delta-1\le\delta/(1-\delta)\le(162/137)\delta\).
The exact rational comparison

\[
\frac58\frac{10287}{4900}>\frac{162}{137}
\]

therefore shows \(e^{-s}+e^\delta-2\le0\). This proves (A1) in this region with zero on the right instead of the stated positive allowance.

## 2. Uniform bound below 4/5, including H <= 0

For any current root \(0\le t<4/5\), the positive successor increments obey

\[
(t_2-t)_+\le\frac1{2cd},\qquad
(t_1-t)_+\le\frac1{2(c+1)(d+1)}.
\]

For \(H>0\), use the defining polynomial and its positive derivative. For \(H\le0\), the successor right sides are at most 1, respectively \(1-2a<1\), giving the same bounds directly. Thus no derivative is taken through the root kink.

The first bound is at most \(1/2\), the second at most \(1/8\). Convex chord bounds yield

\[
e^u-1\le\frac43u\quad(0\le u\le1/2),\qquad
e^v-1\le\frac87v\quad(0\le v\le1/8).
\]

For the first, \(e^{1/2}<5/3\) suffices; for the second use
\(e^v-1\le v/(1-v)\). Therefore

\[
e^{t_1}+e^{t_2}-2e^t
\le e^{4/5}\left[\frac2{3cd}+
\frac4{7(c+1)(d+1)}\right].                            \tag{A2}
\]

For positive integers \(c,d\),

\[
\frac1{cd}\le3(D_c+D_d),\qquad
\frac1{(c+1)(d+1)}\le\frac34(D_c+D_d).
\]

The first follows from \((c+1)(c+2)\le6c^2\) and the arithmetic-geometric mean inequality; the second follows by applying the same inequality to \(c+1,d+1\ge2\), using \((c+2)/(c+1)\le3/2\).

Finally \(e^{4/5}<9/4\), so (A2) is at most

\[
\frac94\left(2+\frac37\right)(D_c+D_d)
=\frac{153}{28}(D_c+D_d)<6(D_c+D_d).
\]

All elementary exponential constants can be checked by their power series. They have ample strict slack. This completes (A1).
