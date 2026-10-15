# Directional tilt boundary and admissibility of finitely many tilts

This is an append-only consequence of PROOF.md, whose frozen bytes remain unchanged. Status: internally derived, not independently reviewed.

For the same separated-block tuple, every interior point \(g=(s,t)\) of any admissible scalar noise's Laplace domain must satisfy
\[
|s|<r_*
\quad\text{when }r_*<\infty.
\tag{A1}
\]
The transverse tilt \(t\) cannot evade the high-energy obstruction.

To prove this, use the moment-transfer and Schur-complement argument from Section 3 at the arbitrary tilt \((s,t)\). In one block put
\[
u=sa,\quad v=tb,\quad r=\sqrt{u^2+v^2},\quad
\alpha=u/r,\quad\beta=v/r,\quad f(r)=\sinh(r)/r.
\]
A real unitary change of Pauli basis makes the tilted exponent \(r\sigma_z\), while its derivative in the transverse coordinate becomes
\(b(\beta\sigma_z+\alpha\sigma_x)\), up to an irrelevant sign on the transverse Pauli matrix. At \(r>0\),
\[
H'=b[\beta H_0\sigma_z+\alpha f(r)\sigma_x],\qquad H_0=e^{r\sigma_z},
\]
\[
H''=b^2\left[
\beta^2H_0+\alpha^2\left(f(r)I+f'(r)\sigma_z\right)
+2\alpha\beta f'(r)\sigma_x\right].
\]
The cross term in \(H'H_0^{-1}H'\) vanishes because the Pauli matrices anticommute. Consequently the normalized Schur difference is
\[
H_0^{-1/2}(H'H_0^{-1}H'-H'')H_0^{-1/2}
=b^2\left[
\alpha^2d(r)\sigma_z-2\alpha\beta f'(r)\sigma_x
\right],
\quad
d(r)=\frac{\sinh(2r)-2r}{2r^2}.
\tag{A2}
\]
Its eigenvalues are opposite and the positive one is at least
\[
b^2\alpha^2d(r)=
\frac{b^2u^2}{2r^4}[\sinh(2r)-2r].
\tag{A3}
\]
For fixed \(s\ne0,t\), bounded \(b_n\) and \(a_n\to\infty\) give
\(r_n=|s|a_n+O(1/a_n)\), \(\alpha_n^2\to1\). Thus finiteness of the common tilted transverse variance again forces
\[
\sup_n |b_n|e^{|s|a_n}/a_n<\infty,\qquad r_*\ge|s|.
\]
If an interior point had \(|s|=r_*<\infty\), a nearby interior point would have larger \(|s|\), contradicting this bound. This proves (A1). If \(r_*=0\), no interior moment point at all is possible, since every open set contains a point with \(s\ne0\).

There is matching sufficiency for every bounded collection of requested interior tilts strictly inside the strip. For any \(\gamma>0\), apply the main theorem to the rescaled pair \((A,B/\gamma)\). A constant rescaling of \(b_n\) leaves \(r_*\) unchanged. Push the resulting common noise forward by
\[
(z_1,z_2)\longmapsto(z_1,\gamma z_2)
\]
and push the POVM forward by the same map. The exact Fourier identity for \((A,B)\) follows. Its full noise moment domain is the ellipse
\[
E_{R,\gamma}=
\{(s,t):s^2+\gamma^2t^2<R^2\},
\qquad R\le r_*.
\tag{A4}
\]
The law stays smooth, strictly positive and strictly log-concave.

Given a compact set \(K\) with
\(\max_{(s,t)\in K}|s|<r_*\), choose \(R\) strictly between this maximum and \(r_*\) (or any larger finite \(R\) if \(r_*=\infty\)), then choose \(\gamma>0\) small enough that \(K\subset E_{R,\gamma}\). This constructs one noise with moments on a neighborhood of all the requested tilts.

Hence, for any finite list of tilt points, admission as **interior finite moments** is possible exactly when the maximum absolute energy-coordinate tilt is strictly below \(r_*\). At \(r_*=\infty\), the main theorem already supplies every tilt at once. No one-law attainment of the whole infinite vertical strip is claimed for finite \(r_*\); covering it by a family of ellipses does not prove that assertion.

The rescaling is a mathematical domain construction. It does not establish reduced physical noise: its tail cutoffs and sufficient width depend on the enlarged coupling bound \(\sup|b_n|/\gamma\).
