# General transport angle and partial thermal refresh

**Status.** Independent constructive calculation for the root's new supplier attack. This is not an actual-version review of a root draft. It removes quarter-angle and full-refresh tuning at a compact, nondegenerate operation interface; it does not remove the paid fresh thermal coordinate or the actual force-conservation premise.

## 1. Exact correction and mobility

Put `c=cos(theta)`, `s=sin(theta)`, `r=cos(psi)`, and `z=(P,Y)`. The proposed period map and true displacement are

\[
z'=Mz+RdF+\sqrt R\,n\xi,\qquad
\Delta A=l^Tz+Rd_0F,
\]

\[
M=\begin{pmatrix}c&-s\\rs&rc\end{pmatrix},\quad
d=\begin{pmatrix}s/g+b\\r(1-c)/g\end{pmatrix},\quad
n=\begin{pmatrix}0\\\sin\psi\end{pmatrix},
\]

\[
l=\begin{pmatrix}s/g+bc\\-(1-c)/g-bs\end{pmatrix},\qquad
d_0=(1-c)/g^2+bs/g+b^2/2.
\]

I reconstructed these expressions by integrating the transport rotation and the subsequent free particle motion. In particular the force continues to act during the bath interval, and that motion is included in A. Omitting that force or displacement changes the supplier.

Since `det(I−M)=(1−c)(1+r)`, write `t=cot(theta/2)=s/(1−c)`. Direct inversion gives

\[
\boxed{k_P=
\frac{(1-r)s/g+b(c-r)}{(1-c)(1+r)},\qquad
k_Y=-\frac{2/g+bt}{1+r}.}
\tag{1}
\]

Here `k^T=l^T(I−M)^(−1)`. Therefore the actual current has the exact analytic correction

\[
\Delta A+k^T(z'-z)
=R\mu_{\rm cell}F+\sqrt R\,k^Tn\xi,
\tag{2}
\]

where substitution and `s²=1−c²` give

\[
\boxed{\mu_{\rm cell}=d_0+k^Td
=\frac{1-r}{2(1+r)}
\left(\frac2g+b\cot\frac\theta2\right)^2.}
\tag{3}
\]

The fluctuation relation follows with no sign ambiguity:

\[
\boxed{(k^Tn)^2
=k_Y^2(1-r^2)=2\mu_{\rm cell}.}
\tag{4}
\]

For `0<theta<pi`, `g>0`, `b>=0` and `|r|<1`, the square in (3) is strictly positive. On a fixed compact subdomain it is bounded above and below by positive constants. The physical mobility per unit time is `mu_cell/(theta/g+b)`.

## 2. An explicit uniform stability estimate

The thermal identity is

\[
MM^T+nn^T=I.
\tag{5}
\]

For any real or complex vector v, let `w=(s,c)`. The two-step dissipation identity is

\[
\|M^2v\|^2=\|v\|^2
-(1-r^2)\left(|wv|^2+|wMv|^2\right).
\tag{6}
\]

The two-row observation matrix with rows w and wM has determinant `−s`. Each row has norm at most one, so its smallest squared singular value is at least `s²/2`. Thus

\[
\boxed{\|M^2\|^2\leq1-(1-r^2)s^2/2<1.}
\tag{7}
\]

If `sin(theta)>=s_*>0` and `|r|<=r_*<1`, put
`q=sqrt(1−(1−r_*²)s_*²/2)<1`. Then

\[
\|M^j\|\leq q^{\lfloor j/2\rfloor},\qquad
\sum_{j\geq0}\|M^j\|\leq2/(1-q).
\tag{8}
\]

This explicit bound avoids any unproved inference from pointwise spectral stability to uniform nonnormal transients.

Prepare `z_0~N(0,RI)` and independent fresh standard-normal aggregate inputs xi. The zero-force recursion has covariance RI at every period by (5). For any adapted bounded force `|F_k|<=a`, decompose the actual state into that same Gaussian reference recursion plus the exact forced convolution. Bound (8) makes the latter at most `C Ra` pathwise, even though the actual state under feedback need not be Gaussian. A union bound gives

\[
\Pr\{\max_{k\leq K}\|z_k\|>x\}
\leq C(K+1)\exp[-(x-CRa)_+^2/(CR)].
\tag{9}
\]

The explicit within-period rotations and free motion have the same type of bound. Therefore the unobserved correction `k^T(z_k−z_0)` is superexponentially negligible at threshold epsilon N² under the dilute queue regime. No coefficient is learned or used by the sign controller: known compact parameter bounds supply uniform lower/upper capacity `R mu_cell a` and variance `2R mu_cell`.

The innovation in (2) is the fresh coordinate used at the **end** of this period. It must be independent of the information selecting the force. Unlike the earlier quarter-cell representation, it need not be regarded as an unread initial state coordinate: the full present state may be included in the mathematical filtration. The new future source remains unread before the fixed command is chosen.

## 3. Real boundaries and an exact failure outside the angle branch

Stability and thermal invariance alone do not guarantee nonzero winding mobility. Take

\[
\theta=3\pi/2,\quad g=1,\quad b=2,\quad r=0.
\]

Then `M=[[0,1],[0,0]]` is stable, but `k=(−1,0)` and `mu_cell=0`. The true cell is exactly `Delta A=Delta P`: current is a state boundary, with no sustained winding capacity. This is a concrete reason to retain the branch `0<theta<pi`, or explicitly warrant that `2/g+b cot(theta/2)` stays away from zero. It is not a counterexample inside the proposed compact branch.

For a literal finite-duration bounded-frequency refresh, also retain a positive lower bound on b and a bounded rotation angle/frequency. The algebraic b=0 limit with nontrivial refresh is not by itself a finite-duration implementation. Partial refresh retains old Y memory; it still consumes fresh thermal coordinates. The previous relative-energy bound for skewed local sensing survives, because the partial Y--xi rotation conserves their combined quadratic energy and can increase the retained relative energy by at most the incoming coordinate energy.

This calculation supports the stronger queue supplier without exact quarter rotation, full refresh, or coefficient identification. It does not extend the earlier actual force-work formula automatically; that formula must be rederived for the new state corrector and command filtration.

## 4. A useful work consequence that needs no new exact work identity

Rare arming still implies vanishing expected absolute **net force work**, without asserting the old nonnegative quadratic formula. Let K=O(N²), all forces be zero until the actual arming event G, and `|F_k|<=a` thereafter. True cell displacements and the uniform within-period solution imply

\[
|W|\leq C aK(\max_{k\leq K}\|z_k\|+Ra).
\]

The same bound holds for the integral of the absolute aggregate force power, since the actual instantaneous power is `F P`. By (9),

\[
E W^2\leq C a^2K^2[(Ra)^2+R\log(K+2)].
\]

Because W is zero when G does not occur, Cauchy--Schwarz gives

\[
E|W|\leq C aK[Ra+\sqrt{R\log(K+2)}]\Pr(G)^{1/2}.
\tag{10}
\]

Thus the supplied `Pr(G)<=C exp(−c log²N)` bound beats this polynomial prefactor and proves vanishing expected absolute net force work. The argument does not condition the Gaussian law on arming, and uses the pathwise forced-convolution bound under adapted commands. It leaves thermal preparation and the rest of the apparatus account untouched. It is not a sustained-current lower bound, nor a claim that all predictable partial-refresh feedback has nonnegative work.
