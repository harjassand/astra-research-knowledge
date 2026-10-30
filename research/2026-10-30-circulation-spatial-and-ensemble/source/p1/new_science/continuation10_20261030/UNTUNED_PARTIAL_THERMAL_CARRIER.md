# Finite-response carrier transport without exact pulse tuning or full thermal reset

30 October 2026. Root's next construction after the circulation-history and
force-limit results. The existing record-geometry role independently checked
the algebra and found the zero-response phase counterexample below. This is
a stronger supplier for the same physical operation, not the unfinished
round9 nonlinear apparatus.

## 1. The missing operation addressed

The original mechanical supplier used exact quarter transport and full
thermal exchange. Here both angles may be fixed unknown values in warranted
intervals. Neutral memory is partially retained. The controller obtains an
inward true-current response without learning angles, mobility, hidden
relative interactions or the proof's analytic corrector.

Parameters are common to identical carriers within one lane and fixed during
deployment. Different lanes may differ. Arbitrary per-carrier mismatch or
time-dependent pulse jitter is not covered. Uniform bounds on the implemented
operations remain actual premises.

## 2. Physical cycle and true displacement

R unit charges on a lane of circumference N have positions X_l, velocities
V_l and neutral coordinates Y_l. The unknown smooth relative potential U is
translation-invariant, so sum_l partial_l U=0. Well-posedness and the separate
readout energy envelope are retained. During transport for duration h,

\[
\dot X_l=V_l,\quad \dot V_l=-\partial_lU-gY_l+F,
\quad \dot Y_l=gV_l.                                  \tag{1}
\]

During a bath interval b>0 disconnect only V--Y. Particles keep moving under
dot X=V, dot V=-partial U+F. Rotate Y with a fresh unread standard Gaussian
xi through angle psi at finite frequency psi/b. Thus

\[
Y_l^{\rm next}=rY_l^{\rm transport}+u\xi_l,
\quad r=\cos\psi,\quad u=\sin\psi.                   \tag{2}
\]

The retired coordinate is the other component of the physical rotation. It
contains old memory and cannot be reused as a fresh source without preparation.
F is held for a cycle and chosen before its new xi is exposed. All movement
in both stages contributes to the measured current.

Require fixed compact bounds

\[
0<g_-\le g\le g_+,\quad 0<b_-\le b\le b_+,
\quad 0<\theta_-\le\theta=gh\le\theta_+<\pi,
\quad |r|\le r_*<1.                                  \tag{3}
\]

Choose psi in [acos(r_*),pi-acos(r_*)], giving bounded thermal rotation
frequency. There is no exactly prescribed angle. Common coupling, switching,
timing and force uniformity within the lane remain operations.

Set c=cos(theta), s=sin(theta), P=sum_l V_l, Y=sum_l Y_l, z=(P,Y)^T.
Summing the real equations cancels every unknown relative force. The cell is

\[
z_{k+1}=Mz_k+RdF_k+\sqrt R\,n\zeta_k,
\quad M=\begin{pmatrix}c&-s\\rs&rc\end{pmatrix},
\quad d=\binom{s/g+b}{r(1-c)/g},\quad n=\binom0u,       \tag{4}
\]

with fresh standard Gaussian zeta_k. True displacement is

\[
\Delta A_k=\ell^Tz_k+Rd_0F_k,
\quad \ell=\binom{s/g+bc}{-(1-c)/g-bs},
\quad d_0=(1-c)/g^2+bs/g+b^2/2.                       \tag{5}
\]

Incoming noise acts on the next cell, not directly on (5). This event order
is necessary for the decision filtration and work calculation.

## 3. A current relation whose unknown coefficients need not be learned

Since det(I-M)=(1-c)(1+r)>0, define only for analysis

\[
k^T=\ell^T(I-M)^{-1}.                                \tag{6}
\]

Direct inversion gives

\[
\beta=2/g+b\cot(\theta/2),\quad k_Y=-\beta/(1+r),
\quad k_P=\frac{(1-r)s/g+b(c-r)}{(1-c)(1+r)}.           \tag{7}
\]

Combining (4)--(6) cancels the previous center-of-mass state:

\[
\boxed{\Delta A_k+k^T(z_{k+1}-z_k)
=R\mu F_k+\sqrt R\,\sigma\zeta_k,}
\quad \mu=d_0+k^Td,\quad\sigma=k^Tn.                  \tag{8}
\]

Its coefficients obey

\[
\boxed{\mu=\frac{1-r}{2(1+r)}
\left(2/g+b\cot(\theta/2)\right)^2>0,\qquad
\sigma^2=2\mu.}                                      \tag{9}
\]

All coefficients and 1/mu have uniform bounds on (3). A force
F=-a_N sign(delayed error) therefore supplies corrected-current inward drift
at least c R_Na_N without estimating g,h,b,r,mu or k. The detector reads A;
the unknown endpoint correction is bounded below rather than implemented.

Equation (9) follows from the displayed operations, not from knowledge of
their invariant law alone. At zero force each conservative segment preserves
energy and volume, and partial thermal rotation preserves the joint Gaussian
law, so the full conservative model preserves its Gibbs law. This implies
neither preparation nor mixing of its unknown relative positions.

## 4. Memory is uniformly controlled while being retained

M is uniformly stable on (3). For w=(s,c), one step loses
(1-r^2)(w z)^2 of squared norm. The two-row matrix with rows w and wM has
determinant -s and row norms at most one. Its least squared singular value
is at least s^2/2. Consequently

\[
\|M^2\|^2\le1-(1-r^2)s^2/2<1,
\qquad \|M^j\|\le C\kappa^j,\quad\kappa<1             \tag{10}
\]

uniformly on the compact parameter class.

The covariance identity M M^T+n n^T=I is exact. Supply z_0~N(0,R I),
independent of unread future sources; independent initial Gaussian velocities
and Y_l suffice without preparing relative positions. For arbitrary adapted
|F_k|<=a_N, the actual recursion decomposes pathwise as

\[
z_k=z_k^0+R\sum_{j<k}M^{k-1-j}dF_j,
\qquad |z_k-z_k^0|\le C R a_N,                       \tag{11}
\]

where each z_k^0~N(0,R I), with temporal correlations retained. A union bound
and the explicit within-period solution give

\[
\Pr\{\sup_{s\le N^2T}|z(s)|>x+C R a_N\}
\le C(N^2+1)e^{-x^2/(CR)}.                           \tag{12}
\]

The same estimate bounds displacement inside one cell. The noise zeta_k in
(8) is fresh in the actual decision filtration. Hence the scalar delayed
queue applies to A-Z+k^T(z-z_0); the actual E=A-Z differs by (12). The
controller never computes k. Uniform bounds suffice for the proof.

For R_N=o(N), R_Na_N->infinity and R_Na_N d_N=o(N^2), this supplies the full
nonlinear circulation operation. Local pickup retains the separate relative
energy envelope. An integrated rare-arming example is R_N=ceil(N^(1/3)),
a_N=N^(-1/6), d_N=O(N log N): its O(R_NN) conservative detector error is below
N^(3/2)log N, and Gaussian endpoint errors are smaller with superexponential
probability. The physical period h+b is bounded above and below, so this
remains a physical-time result.

## 5. Actual work on rarely armed histories

The unforced corrected current is a Gaussian martingale of variance
O(R_NN^2), plus endpoint (12). With an unforced native aggregate martingale,
the trigger b_N=N^(3/2)log N has probability
p_arm<=C exp(-c log^2 N), adding actual sensor failures.

Actual drive work is

\[
W=\int_0^{N^2T}F(s)P(s)\,ds,                         \tag{13}
\]

not force times corrected current. Because force is zero before arming,
(11)--(12) and Cauchy--Schwarz give

\[
\mathbb E|W|\le C_Ta_NN^2
\left[R_Na_N p_{\rm arm}
+\sqrt{R_N\log(2+N)}\sqrt{p_{\rm arm}}\right].         \tag{14}
\]

This vanishes faster than every inverse polynomial. Every momentum/force
correlation is retained. Thermal preparations, pickup, communication and
field-switch hardware work are outside (13); they continue while force is
off. Under a sustained load arming need not be rare, so (14) yields no low
work promise. The physical-mechanism role's separate delayed-block derivation
supplies the loaded comparison, including an exponentially small old-state
correlation remainder. There is no assertion of exact finite-block work
nonnegativity for arbitrary feedback.

## 6. Failed stronger claim: stable memory is insufficient

Outside the response interval in (3), take

\[
\theta=3\pi/2,\quad g=1,\quad b=2,\quad r=0.          \tag{15}
\]

M is nilpotent and thermal memory is stable, but beta=mu=0. The real cell
obeys Delta A=Delta P, so corrected winding is identically zero. Repetition
does not create a force-to-flow response. Invariance, stable auxiliary memory
and finite bandwidth do not supply useful transport capacity. The positive
response range in (3) is an actual requirement.

## 7. Scientific and resource scope

Exact quarter transport, full thermal replacement and knowledge of kinetic
coefficients have been removed. Positive-response bounds, common carrier
coupling, fresh independent thermal coordinates, finite local sensing and
an actual force port remain. Partial memory is physically retained. All
charges and every displacement are counted.

This strengthens the supplier for the nonlinear full-path operation. It does
not certify a built sensor network, arbitrary pulse-jitter robustness, total
energetic efficiency or historical priority over repeated-interaction thermal
models. Earlier accepted results and their interfaces remain unchanged.
