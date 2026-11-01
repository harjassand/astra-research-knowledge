# Strengthening: cutoff 2, a common small tilt, and retained reverse-arm reserve

This is a supplement to the frozen `FULL_GENERATOR_STOPPED_DRIFT.md`; that file's bytes and its original cutoff-100 theorem are unchanged. All notation and the exact twelve-reaction table are inherited from it. The only parameter changes are allowing **every** \(1<r\le101/100\), and lowering the proved charging cutoff from 100 to 2. Constants \(a=1/100,q=2,K=1,\epsilon=20\) remain unchanged.

## Strengthened theorem

For every integer state with \(t=\tau(x)\ge2\),

\[
\boxed{
\frac{LV(x)}{V(x)}\le-
\left\{\frac3{20}+10A^2+
\frac t4\left[\frac{AC}{d+t+1}+\frac{AD}{c+t+1}\right]\right\}.
}                                                        \tag{S1}
\]

The inequality is uniform in \(1<r\le101/100\), all ratios of \(C,D\), and every integer state in the indicated region. No global receiving interface or stability conclusion is included.

### 1. All finite-jump prerequisites remain valid

On \(t\ge2\), \(H\ge2t^3/3\ge16/3>1\). Thus every actual one-step neighbor remains in the positive-root domain. All pointwise finite-jump facts from Sections 1–2 of the original proof remain valid, including the exact \(AE\) grouping: its proof explicitly used only \(t\ge2\).

The useful uniform phase bound becomes

\[
1\le h\le1+\frac{20}{198\cdot2}=\frac{104}{99}.         \tag{S2}
\]

### 2. Uniformity in the common tilt

Every positive immigration bound used only \(r\le101/100\). Every port-death bound used \(r^{-1}\le1\), not equality to \(100/101\). All other reactions conserve \(N\). Consequently decreasing \(r\) to any number above 1 changes no asserted upper bound. The same estimates also hold at \(r=1\), although the small positive tilt is the intended application.

### 3. The \(A\ge1\) constants at cutoff 2

The base estimate, **before** adding the strictly negative reverse-arm terms, is still

\[
h\{(r-1)+(e-1)A+3(e-1)A(A-1)\}
\le\frac{104}{99}\Big(\frac1{100}+6\Big)A^2<7A^2.
\]

Here only \(e<3\) was used. Define

\[
\theta(t,r)=\frac{16}{198t}+\frac2{99}+\frac{9r}{198t^3}.
\]

The exact phase-correction budget from the original proof is

\[
-20A(2A-1)+20\theta(t,r)A.                             \tag{S3}
\]

The coarser bound \(-20A^2+20\theta A\) is sufficient. Since

\[
\theta(t,r)\le\frac{16}{396}+\frac2{99}
 +\frac{9\cdot101}{100\cdot198\cdot8}
 =\frac{10509}{158400}<\frac1{15},
\]

this coarser correction is at most \(-56A^2/3\). Therefore, retaining all unused nonpositive base terms,

\[
\frac{LV}{r^Ne^t}< -\frac{35}{3}A^2
-h\{AC(1-e^{-s_C})+AD(1-e^{-s_D})\},                  \tag{S4}
\]

where \(s_C\) and \(s_D\) are the actual debt decreases of \(AC\to2A\) and \(AD\to2A\), respectively. The positive correction costs of those arms have **already** been paid inside (S3); (S4) does not omit them.

Dividing by (S2), the quadratic reserve is greater than

\[
\frac{35}{3}\frac{99}{104}A^2=\frac{1155}{104}A^2
>\left(10A^2+\frac3{20}\right),\qquad A\ge1.           \tag{S5}
\]

The sharper unrelaxed expression (S3), rather than just the \(10A^2\) reserve in (S1), remains available for a future gluing calculation.

### 4. Quantitative reverse-arm reserve

For \(AC\to2A\), the mean-value theorem gives

\[
s_C\ge
\frac{t(c+t/2)+a/q}{(c+t)(d+t+1)}
\ge\frac{t}{2(d+t+1)}.
\]

For \(AD\to2A\), symmetrically,

\[
s_D\ge\frac{t}{2(c+t+1)}.
\]

Both decreases are less than 1: at \(t-1\), compare the one-coordinate-shifted polynomial with the two-coordinate-shifted identity (2) of the original proof and use \(qP(c,d,1)>a\). Thus concavity of \(1-e^{-s}\), together with \(e>2\), yields

\[
1-e^{-s_C}\ge\tfrac12s_C\ge\frac{t}{4(d+t+1)},\qquad
1-e^{-s_D}\ge\frac{t}{4(c+t+1)}.                       \tag{S6}
\]

Equations (S4)–(S6) prove (S1) on \(A\ge1\). In particular the reserve is order \(C\) when \(A,d,t\) stay fixed and \(C\to\infty\); the adverse ray for a naive profile sum is not an obstruction merely because a weakened debt estimate discarded this reserve.

### 5. The \(A=0\) constants at cutoff 2

The original convex endpoint bound still applies with

\[
\rho\ge4/9,\qquad \eta\ge15/16.
\]

Using the purely rational estimate

\[
e^{4/9}>1+4/9+(4/9)^2/2=125/81,
\]

the larger endpoint is bounded by

\[
\max\{r-1-\eta,\,r e^{-\rho}-1\}
\le -\frac{4319}{12500}.
\]

The phase error is at most

\[
\frac{20}{198}\left(\frac32+\frac{3\cdot101}{100\cdot8}\right)
=\frac{501}{2640}.
\]

Their sum is strictly less than \(-3/20\): numerically it is approximately \(-0.15574727\), with the exact rational comparison decisive. When \(A=0\), both reverse-arm reserves vanish. This completes (S1).

## Stopped receiving consequence

The same Poisson localization justification in the original proof now gives, for
\(\sigma_2=\inf\{s\ge0:\tau(X_s)<2\}\),

\[
\mathbb E_x\left[e^{3(T\wedge\sigma_2)/20}
V(X_{T\wedge\sigma_2})\right]\le V(x),
\qquad \mathbb E_xe^{3\sigma_2/20}\le V(x).
\]

This is a complete charging-episode statement in the actual process. It does not receive the lower-debt region or authorize independent resetting of continuing episodes. At the root kink \(H=0\), jump effects must be evaluated directly; neither differentiability nor the grouped \(AE\) estimate is asserted there.
