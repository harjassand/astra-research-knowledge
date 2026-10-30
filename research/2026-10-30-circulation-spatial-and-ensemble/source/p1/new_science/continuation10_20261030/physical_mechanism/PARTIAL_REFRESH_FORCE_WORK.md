# Partial thermal refresh: delayed physical work and the sustained-load bound

30 October 2026. Constructive challenge to root's improved carrier supplier. This calculation uses the period map sent by root and the independently saved algebra in `record_geometry/PARTIAL_REFRESH_CELL_CONSTRUCTIVE_CHECK.md`, SHA256 `3d918f42ce3db48c24376b7905930de583bb2378cc577a15929e2dc3c830ba80`. It is not an actual-version receiving review of a root draft which was still being written. All previous files and reviews are preserved.

## 1. Outcome

The sustained-load work bound survives general transport angles and partial thermal refresh. The exact quarter-cell work identity does not survive unchanged: a small old-state correlation remains. Under the actual one-block delay and uniformly stable period map, that correlation is exponentially small in the held block length `L`.

For forces held over `L` cells, `L` of order `N`, define `S=sum_m E F_m^2`. At the supplied fixed-parameter port,

\[
\boxed{\mathbb E W=R\mu L S+O(RS)+\varepsilon_N,\qquad
|\varepsilon_N|\le \operatorname{poly}(N)e^{-cL}.}
\tag{1}
\]

The constants are uniform on a warranted compact parameter set. Consequently a mean actual counter-displacement of order `N^2` on the physical `N^2` horizon requires mean force work `Omega(N^2/R)`. A constant force attains the leading mobility/work relation.

Rare arming retains a different conclusion. Stable state bounds and the actual work `F Delta A` show that its expected **absolute aggregate force work** tends to zero under the superpolynomial arming estimate. Neither conclusion prices continuing neutral-source preparation, sensing, communication, synchronization or field generation.

Do not replace (1) by exact nonnegative finite-`L` work without another argument. A partial-refresh system retains an exponentially small old-state correlation which an informed controller can in principle exploit. The exponentially small remainder is a real qualification, not an algebraic inconvenience to discard.

## 2. Actual cell and uniform scope

Let `z=(P,Y)` be the aggregate charged momentum and neutral coordinate. Root's actual period is

\[
z_{j+1}=Mz_j+RdF_j+\sqrt R\,n\xi_j,
\qquad
\Delta A_j=\ell z_j+Rd_0F_j,
\tag{2}
\]

where each end-of-period `xi_j` is a fresh standard Gaussian, independent of the information selecting `F_j`. Actual carrier displacement during both transport and bath stages is included. With `c=cos(theta)`, `s=sin(theta)`,

\[
M=\begin{pmatrix}c&-s\\rs&rc\end{pmatrix},\quad
d=\binom{s/g+b}{r(1-c)/g},\quad n=\binom0{\sqrt{1-r^2}},
\]

\[
\ell=(s/g+bc,\;-(1-c)/g-bs),\qquad
d_0=(1-c)/g^2+bs/g+b^2/2.
\tag{3}
\]

For the row vector `k=ell(I-M)^(-1)`, the supplied algebra gives

\[
\mu=d_0+kd
=\frac{1-r}{2(1+r)}
\left(\frac2g+b\cot\frac\theta2\right)^2>0,
\qquad (kn)^2=2\mu,
\tag{4}
\]

and the exact current identity is

\[
\Delta A_j+k(z_{j+1}-z_j)
=R\mu F_j+\sqrt R\,kn\xi_j.
\tag{5}
\]

The physical period length is `p=theta/g+b`; `mu/p` is the mobility per unit physical time. The detector and force source still use true `A`, not the corrected current in (5).

For statements uniform over unknown fixed parameters or hidden classes, retain actual compact bounds

\[
\sin\theta\ge s_*>0,\quad 0<\theta<\pi,\quad
|r|\le r_*<1,
\quad 0<g_*\le g\le g^*,
\tag{6}
\]

and finite duration bounds for the bath. These imply positive lower/upper mobility and bounded `k,d,ell`. The sibling's direct two-step dissipation proof supplies

\[
\|M^j\|\le C\rho^j,\qquad \rho<1,
\tag{7}
\]

uniformly, without inferring a uniform nonnormal bound merely from individual spectral radii.

The parameters are fixed during deployment and common to the aggregate mechanical coupling. Arbitrary distinct pulse angles on interacting particles do not supply this two-dimensional cell: their weighted interaction forces need not cancel. No such heterogeneity is introduced here. If `r` approaches one with `N` without a warranted margin, mobility and the memory-decay rate can both vanish; the uniform work and queue constants cannot be retained for free. Pointwise asymptotics at one fixed `r<1` and a uniform hidden-class theorem are different statements.

## 3. Block recursion and the correct command filtration

Hold `F_m` over the complete cells `mL,...,(m+1)L-1`. Use `B` complete control blocks; the physical horizon in this calculation is `T_*=BLp`. Let `Z_m=z_(mL)` and set

\[
Q=M^L,\qquad v=\sum_{j=0}^{L-1}M^j d,
\qquad w=k(I-Q).
\tag{8}
\]

Then

\[
Z_{m+1}=QZ_m+RvF_m+\Xi_m,
\tag{9}
\]

where `Xi_m` is the block innovation, independent of all information available at block start. The thermal identity `MM^T+nn^T=I` gives its covariance `R(I-QQ^T)`.

The actual delay is

\[
F_m\text{ is measurable with respect to the record at the start of block }m-1.
\tag{10}
\]

It may depend arbitrarily on that older record and on native current history. It may not depend on the last block's new innovation. This is a full-block-old command, not a command chosen from the just-completed momentum. Set `F_0=0`; this matches initially unarmed control and removes an initial work term. Prepare `z_0` with the supplied centered Gaussian covariance `RI`, independently of future sources.

Equation (10) implies

\[
\mathbb E[F_m\Xi_{m-1}]=0.
\tag{11}
\]

It does **not** imply `E[F_m Q Z_(m-1)]=0`: the old state is part of, or correlated with, the old record. That surviving term is the main difference from exact fresh-quarter renewal.

## 4. Exact expected-work identity

The physical work is

\[
W=\sum_m F_m\sum_{j=mL}^{(m+1)L-1}\Delta A_j.
\tag{12}
\]

Summing (5) within a block and using the fresh-source mean gives

\[
\mathbb EW
=R\mu L\sum_m\mathbb EF_m^2
-\sum_m\mathbb E[F_m k(Z_{m+1}-Z_m)].
\tag{13}
\]

Substitute (9), then substitute the preceding block recursion in the remaining `F_m w Z_m` term. Equation (11) gives the exact formula

\[
\boxed{
\begin{aligned}
\mathbb EW
={}&R(\mu L-kv)\sum_m\mathbb EF_m^2\\
&+Rwv\sum_m\mathbb E(F_mF_{m-1})\\
&+\sum_{m\ge1}\mathbb E[F_m wQ Z_{m-1}],
\end{aligned}}
\tag{14}
\]

where `F_(-1)=0`. The `m=0` term vanishes because `F_0=0`. The final sum is not omitted and has no asserted sign.

Uniform stability bounds `|kv|+|wv|` by a fixed constant, and

\[
\left|\sum_m\mathbb E(F_mF_{m-1})\right|
\le\sum_m\mathbb EF_m^2=S.
\tag{15}
\]

Thus all displayed quadratic corrections in (14) are bounded by `C R S`.

## 5. The remaining memory term is exponentially small

For an adapted force cap `|F_m|<=a<=1`, decompose the actual state into the same unforced Gaussian recursion plus its bounded forced convolution:

\[
z_j=G_j+R\sum_{i<j}M^{j-1-i}dF_i,
\qquad \|z_j-G_j\|\le C R a.
\tag{16}
\]

Here `G_j` has centered Gaussian marginal with covariance `RI` at every cell. It need not be independent of the feedback, and no such independence is used. In particular

\[
\mathbb E\|z_j\|\le C(\sqrt R+Ra).
\tag{17}
\]

The last line of (14) consequently obeys the simple absolute bound

\[
\left|\sum_{m\ge1}\mathbb E[F_m wQ Z_{m-1}]\right|
\le C B a\rho^L(\sqrt R+Ra).
\tag{18}
\]

For `L` of order `N`, `B=O(N)`, `R=o(N)` and bounded `a`, this is a polynomial prefactor times `exp(-cN)`. Combining (14)–(18) proves (1), including the two-sided bound

\[
R(\mu L-C)S-\varepsilon_N
\le\mathbb EW
\le R(\mu L+C)S+\varepsilon_N,
\quad
\varepsilon_N=C B a\rho^L(\sqrt R+Ra).
\tag{19}
\]

This is an absolute exponentially small remainder. A version using Cauchy–Schwarz and Young can absorb an additional `C R S` and make the remainder quadratic in `rho^L`; neither refinement is required for the sustained-load conclusion.

Exact positivity is not a consequence of (19). For example, if an old state component is actually measured, its residual correlation `wQZ` can be used by a force of exponentially small size to extract an exponentially small amount of thermal energy. Whether that measurement port is supplied is a separate issue; (14) shows why the mathematical term cannot simply be assigned a favorable sign.

## 6. Sustained actual transport lower bound

Summing (5) over all blocks gives exactly

\[
J_*:=\mathbb E A(T_*)
=R\mu L\sum_m\mathbb EF_m
-k(\mathbb E Z_B-\mathbb E Z_0).
\tag{20}
\]

Under the centered preparation and bounded force, the endpoint mean in (20) is `O(Ra)`. It is negligible beside a sustained actual displacement `J_*=vT_*+o(T_*)`, `v!=0`, on `T_*=Theta(N^2)`.

Cauchy–Schwarz gives

\[
S\ge\frac1B\left(\sum_m\mathbb EF_m\right)^2
=\frac{[J_*+k(\mathbb E Z_B-\mathbb E Z_0)]^2}
{B R^2\mu^2L^2}.
\tag{21}
\]

For large `L`, (19) and (21) imply

\[
\boxed{
\mathbb EW\ge
\left(1-O(L^{-1})\right)
\frac{J_*^2}{R(\mu/p)T_*}-o(1)
=\Omega(N^2/R).}
\tag{22}
\]

The displayed coefficient is for a fixed device with fixed `mu`. For a mixture of unknown fixed classes with uniform positive/finite mobility bounds, apply the conditional version, or use those two bounds in (21); the same order lower bound survives, but one must not replace the random conditional mobility by an unexplained averaged coefficient.

A constant force after the initial zero block has only bounded state transients and attains the leading mobility and work relation in (22). Better knowledge of the fixed pulse angles cannot remove this sustained-mean bill at the same port. It can change controller tuning or constants.

The calculation uses complete blocks. A horizon sequence of complete blocks with `T_*/N^2 ->T` suffices for this scaling statement. Any remaining short physical interval must retain its actual motion and work in the complete receiver; it is not a free hold. One may set the force to zero on that terminal interval, and its `O(N)` duration has negligible macroscopic current error under the supplied bounds.

## 7. Rare arming still gives vanishing expected absolute force work

Let `H=O(N^2)` be the number of complete cells. The Gaussian reference in (16) obeys

\[
\mathbb E\max_{j\le H}\|G_j\|^2
\le C R\log(H+2).
\tag{23}
\]

The force is zero before arming. From the actual displacement in (2),

\[
|W|\le\sum_j|F_j\Delta A_j|
\le C aH\left[Ra+\max_{j\le H}\|G_j\|\right]
\mathbf1_{\{\mathrm{arm}\}}.
\tag{24}
\]

No current corrector has been substituted for physical work. Cauchy–Schwarz therefore gives, with `p_arm=Pr(arm)`,

\[
\boxed{
\mathbb E|W|
\le C aN^2\left[
Ra\,p_{\rm arm}
+\sqrt{R\log(2+N)}\sqrt{p_{\rm arm}}\right].}
\tag{25}
\]

For `p_arm<=C exp(-c log^2 N)+p_N`, superexponential `p_N`, `R<N` and `a<=1`, every prefactor is polynomial. The expectation tends to zero faster than every inverse power. This estimate needs neither the sign nor the small-memory refinement of the mean work in (19). It remains valid for any causal bounded force policy satisfying the same rare-arming contract and stable cell supplier.

The work here is the aggregate force source's actual work. It does not bound the sum of every local actuator's unrecovered losses, neutral-source retirement work, or synchronization/detection expenditure. The source is continuously prepared even on the overwhelmingly probable unarmed histories.

## 8. Predecessor and physical scope

Partial Gaussian refresh is conventional machinery. Kennedy, Edwards, Mino and Pendleton, *Tuning the generalized Hybrid Monte Carlo algorithm*, explicitly combine Hamiltonian evolution with Gaussian momentum/noise rotation and arbitrary refresh angle in Section 1.2; the actual primary text was read: <https://arxiv.org/pdf/hep-lat/9509043>. It identifies Horowitz's generalized scheme as an earlier instance. Horowitz's primary publisher abstract was also read, DOI <https://doi.org/10.1016/0370-2693(91)90812-5>; the attempted full-text repository read was blocked, so no claim here depends on having read that full article.

The present physical supplier must earn its consequence through true charged displacement during both stages, a force-conserving interacting lane, the finite-period mobility/corrector, compact stability margins, and actual fresh-source preparation. Gaussian rotation or partial momentum refresh itself is not a new operation. The work calculation establishes the sustained-load resource bound and the separate rare-arming estimate for that supplied interface; it does not certify a manufactured apparatus or eliminate phase uniformity, isolation or pulse-error requirements.
