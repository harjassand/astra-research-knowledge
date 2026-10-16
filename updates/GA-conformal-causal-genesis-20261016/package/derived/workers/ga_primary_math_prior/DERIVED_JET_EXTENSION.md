# Weighted jets for the conformal defect

Date: 16 October 2026. Authored in this audit; internal mathematical derivation. Historical originality and external correctness remain UNKNOWN.

This note extends the packet's finite-constant selection theorem. It does not prove the unchanged sharp quasiconvexity bound. All torus integrals and norms below use normalized measure. Write

\[
D\phi=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
q=\sigma a+d,\qquad T_\sigma\phi=(q,c),\qquad \sigma>0.
\]

## 1. The analytic input and its fractional consequences

For finite \(1<p,s<\infty\), let \(1/t=(1/p+1/s)/2\). The packet's classical mixed-derivative interpolation and periodic Hodge argument give

\[
\|a\|_t^2\le C_{\sigma,p,s}\|T_\sigma\phi\|_p\|D\phi\|_s. \tag{J1}
\]

For completeness, take
\((\sigma f,g)=\nabla\chi+(\psi_y,-\psi_x)\), with \(\Delta\chi=q\).
Then \(\sigma a=\chi_{xx}+\psi_{xy}\),
\(\sigma b=\chi_{xy}+\psi_{yy}\), and
\(c=\chi_{xy}-\psi_{xx}\).
Second-order Riesz bounds control \(\chi_{xx}\) in both \(L^p,L^s\), while
\(\|\psi_{xx}\|_p\le C\|T_\sigma\phi\|_p\) and
\(\|\psi_{yy}\|_s\le C_\sigma\|D\phi\|_s\).
Apply
\[
\|\psi_{xy}\|_t^2\le C_{p,s}\|\psi_{xx}\|_p\|\psi_{yy}\|_s
\]
and ordinary interpolation to \(\chi_{xx}\).
The mixed derivative inequality follows by an analytic strip family of coordinate imaginary powers after deleting axis modes; finite \(L^p\) multiplier bounds and the three-lines argument are the classical input. No endpoint assertion is needed.

Put \(E=\|T_\sigma\phi\|_p\) and \(M=\|D\phi\|_s\).
Interpolating (J1) with \(\|a\|_s\le M\) gives, for \(0\le\alpha\le1/2\),
\[
\|a\|_{u_\alpha}\le C E^\alpha M^{1-\alpha},
\qquad \frac1{u_\alpha}=\frac\alpha p+\frac{1-\alpha}s. \tag{J2}
\]
For \(Z=q,c\), the same conclusion holds for \(0\le\alpha\le1\):
interpolate \(\|Z\|_p\le E\) with \(\|Z\|_s\le C_\sigma M\).
For \(b\) only the choice \(\alpha=0\) is used.

Consequently a monomial \(a^i b^j c^k q^\ell\) of degree \(m\) admits
\[
\|a^i b^j c^k q^\ell\|_1
\le C E^\theta M^{m-\theta} \tag{J3}
\]
whenever
\[
0\le\theta\le i/2+k+\ell,\qquad
\frac\theta p+\frac{m-\theta}s=1.
\]
To prove this, allocate exponents \(\alpha\) to its individual factors with capacities \(1/2,0,1,1\), respectively, so that their sum is \(\theta\), and apply Hölder to (J2). The Hölder reciprocals sum exactly to one. This is a sufficient weighted monomial criterion; for \(\theta>1\), no general signed-absolute equivalence or necessity is asserted.

## 2. Exact polynomial selection for all degrees

Let \(m\ge2\), \(0<\theta\le1\), and finite \(1<p,s<\infty\) satisfy
\[
\frac\theta p+\frac{m-\theta}s=1.
\]
For a real homogeneous polynomial \(P\) of degree \(m\), the following are equivalent:

1. A finite constant bounds
   \(\left|\langle P(D\phi)\rangle\right|
   \le K\|T_\sigma\phi\|_p^\theta\|D\phi\|_s^{m-\theta}\)
   for every smooth periodic compatible map.
2. The same estimate, with possibly different constant, bounds
   \(\|P(D\phi)\|_1\).
3. The restriction \(P(a,b,0,-\sigma a)\) is divisible by
   \(a^{\lceil2\theta\rceil}\).

Thus the required vanishing is one transverse jet for \(0<\theta\le1/2\), and two for \(1/2<\theta\le1\).

**Sufficiency.** Change variables from \((a,b,c,d)\) to \((a,b,c,q)\).
Write
\[
P=qP_{m-1}+cR_{m-1}+a^{h}S_{m-h}(a,b),
\qquad h=\lceil2\theta\rceil.
\]
Every monomial containing \(q\) or \(c\) has defect capacity at least one, and every remaining monomial has capacity at least \(h/2\ge\theta\). Apply (J3), then sum. The absolute estimate implies the signed one.

**Necessity, including explicit compatible fields.** Let
\[
h_0(z)=\cos z+\cos2z,\qquad
\eta(z)=-\cos z-\tfrac14\cos2z.
\]
Then \(\eta''=h_0\), \(\langle h_0\rangle=0\), and
\(\mu_m=\langle h_0^m\rangle>0\) for every integer \(m\ge2\).
Indeed, all four nonzero Fourier coefficients of \(h_0\) are positive. A zero-sum list of length \(m\) exists: use pairs \((1,-1)\) for even \(m\), and \((1,1,-2)\) followed by pairs for odd \(m\ge3\).

The exact kernel field \(\phi=(\eta'(y),0)\) has
\((a,b,c,d)=(0,h_0(y),0,0)\).
Its nonzero \(m\)-th moment excludes the coefficient of \(b^m\).

For each positive integer \(N\), use the one-phase periodic map
\[
\phi_N(x,y)=
\left(N^{-1}\eta'(x+Ny),-\sigma N^{-2}\eta'(x+Ny)\right).
\]
It is genuinely compatible and
\[
(a_N,b_N,c_N,d_N)
 =h_0(x+Ny)(N^{-1},1,-\sigma N^{-2},-\sigma N^{-1}),
\qquad q_N=0. \tag{J4}
\]
Hence \(E_N=\sigma N^{-2}\|h_0\|_p\) and \(M_N\) stays bounded above and below.
After the \(b^m\) coefficient vanishes, a nonzero coefficient \(\beta\) of
\(ab^{m-1}\) gives
\[
\langle P(D\phi_N)\rangle=\beta\mu_m/N+O(N^{-2}).
\]
This contradicts a bound of order \(N^{-2\theta}\) precisely when \(\theta>1/2\).
No further exclusion is needed for \(0<\theta\le1/2\).
This proves the equivalence.

The packet's cubic theorem is \(m=3,\theta=1,p=2,s=4\).
For \(\theta=1\), the admissible space has dimension
\[
\binom{m+3}{3}-2;
\]
the cubic value is 18, the quadratic value 8, and the quartic value 33.
In the coordinates \((a,b,c,q)\), this is membership in the homogeneous part of the ideal \((q,c,a^2)\).
For \(0<\theta\le1/2\), its dimension is \(\binom{m+3}{3}-1\).
These are elementary consequences of the same classical interpolation input, not independent evidence of historical novelty.

## 3. A sharp Hilbert-space normalization

For \(p=s=2\), the missing derivative estimate has the explicit sharp constant
\[
\boxed{\|a\|_2^2\le
\sigma^{-1}\|T_\sigma\phi\|_2\|D\phi\|_2.} \tag{J5}
\]
Since the mean determinant vanishes,
\[
\sigma\langle a^2\rangle
=\langle aq-bc\rangle.
\]
Cauchy-Schwarz in the product space gives
\[
\sigma\|a\|_2^2
\le\|(a,b)\|_2\|(q,c)\|_2
\le\|D\phi\|_2\|T_\sigma\phi\|_2.
\]
For (J4), the ratio of the left side \(\|a_N\|_2^2\) to
\(\|T_\sigma\phi_N\|_2\|D\phi_N\|_2\) equals
\[
\frac1{\sigma\sqrt{1+(1+\sigma^2)N^{-2}+\sigma^2N^{-4}}},
\]
which tends to \(1/\sigma\).
This normalization is not the missing mixed \(L^2\)-\(L^4\) sharp constant for the quartic target.

## 4. Explicit higher-integrability decay for the target cubic

Retain \(\sigma=r+1\) and \(\kappa=r(r+2)/3\). In the linear defect coordinates the unchanged target cubic is
\[
\mathcal C_r
=2aq^2-(r+2)a^2q+rc^2q-2bcq-\kappa a^3-\kappa ac^2. \tag{J6}
\]
Assign weights \(1,0,2,2\) to \(a,b,c,q\). Every displayed monomial has weight at least three; equivalently, its defect capacity is at least \(3/2\).

For \(4<s\le6\), set
\[
\theta_s=\frac{2(s-3)}{s-2}\in(1,3/2].
\]
The relation \(\theta_s/2+(3-\theta_s)/s=1\) holds, so (J3) yields
\[
\|\mathcal C_r(D\phi)\|_1
\le K_{r,s}\|T_\sigma\phi\|_2^{\theta_s}
                 \|D\phi\|_s^{3-\theta_s}. \tag{J7}
\]
Since \(Q_r=\langle q^2+\kappa c^2\rangle\), its square root is equivalent to
\(\|T_\sigma\phi\|_2\) for fixed \(r>0\).
Consequently, whenever \(Q_r>0\),
\[
\frac{|C_r(\phi)|}{\sqrt{Q_r(\phi)}}
\le K'_{r,s}\,
 Q_r(\phi)^{(s-4)/(2(s-2))}
 \|D\phi\|_s^{s/(s-2)}. \tag{J8}
\]
In particular,
\[
\boxed{\frac{|C_r|}{\sqrt{Q_r}}
\le K_r Q_r^{1/4}\|D\phi\|_6^{3/2}.} \tag{J9}
\]
This gives an explicit rate on a uniformly \(L^6\)-bounded family. The packet's uniform-integrability consequence applies to a larger class and supplies no such universal rate.

The exponent \(3/2\) of the defect in (J7) at \(s=6\) cannot be increased in a bound with a uniformly bounded gradient norm: on (J4),
\[
C_r(\phi_N)
=-\kappa\mu_3N^{-3}(1+\sigma^2N^{-2}),\qquad
\mu_3=3/4,
\]
while \(\|T_\sigma\phi_N\|_2\) is order \(N^{-2}\), and every finite
\(\|D\phi_N\|_s\) stays bounded and nonzero.

**Concentration boundary.** For the packet's critical concentration
\(\phi_\varepsilon(x)=\varepsilon^{1/2}\phi((x-x_0)/\varepsilon)\),
\(Q_r\) scales as \(\varepsilon\), and
\(\|D\phi_\varepsilon\|_s\) scales as
\(\varepsilon^{2/s-1/2}\).
The two factors on the right of (J8) therefore have exactly opposite powers of \(\varepsilon\).
At \(s=6\), they are \(\varepsilon^{1/4}\) and
\((\varepsilon^{-1/6})^{3/2}=\varepsilon^{-1/4}\).
The estimate retains the original concentration obstruction and gives no all-\(W^{1,4}\) sharp conclusion.

Smooth approximation extends the stated estimates to the corresponding periodic Sobolev/intersection classes. Zero extension followed by periodic placement gives the zero-boundary forms, with the exponent balance ensuring the same homogeneous scaling.

No analytic statement in this note has been machine formalized. The separate exact receipt checks carrier moments, coefficient bookkeeping, and the symbolic exponent/scaling balances only.
