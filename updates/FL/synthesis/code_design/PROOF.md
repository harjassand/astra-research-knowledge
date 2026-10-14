# Finite-slew isotope-code result for the four-carbon E/O target

## Contract and notation

This proof concerns only the synthetic ancestry pair in the supplied FL temporal-ancestry note. Its four ages are

\[
A_j=C+j\tau+\tau X_j,\qquad j=0,1,2,3,
\]

where \(C\ge 0\) is a common delay and \(\tau>0\). Under model E, \(X\) is uniform on the eight even-parity bit strings; under model O it is uniform on the eight odd-parity strings. This is not a fitted catalytic model.

At the measured carbon-feed boundary let \(p(t)\in[p_{\rm low},p_{\rm high}]\) be the heavy-carbon probability. The worked contrast is \(p_{\rm low}=0.01\), \(p_{\rm high}=0.99\), so \(a=p_{\rm high}-p_{\rm low}=0.98\). Write

\[
p(t)=\frac{1+a u(t)}2,\qquad |u(t)|\le 1.
\]

The chemistry and product flux are assumed isotope-neutral, labels of distinct entering molecules are conditionally independent, and the five whole-product carbon-count bins \(K=0,1,2,3,4\) are observed with the calibrated response. These are the mathematical conditions used below, not validated experimental facts.

## Exact count-distribution identity

Fix output time \(t\) and common delay \(C\). Define the two possible feed probabilities for atom \(j\):

\[
p_j(0)=p(t-C-j\tau),\qquad p_j(1)=p(t-C-(j+1)\tau),\qquad d_j=p_j(0)-p_j(1).
\]

For a formal variable \(z\), the probability-generating polynomial of the isotope count conditional on \(X\) is

\[
G_X(z)=\prod_{j=0}^{3}\bigl(1-p_j(X_j)+p_j(X_j)z\bigr).
\]

Taking the even-minus-odd mixture cancels every term except the four-way interaction:

\[
G_E(z)-G_O(z)=\frac18\prod_{j=0}^3 d_j\,(1-z)^4.
\]

The sign of \((1-z)^4\) is immaterial here; the coefficient vector is \((1,-4,6,-4,1)\). Therefore the total-variation distance between the complete five-bin isotope-count laws is exactly

\[
\boxed{\operatorname{TV}(P_E^K,P_O^K)=\prod_{j=0}^3|d_j|.}
\]

No statistic of \(K\) can separate these two models more strongly per product. The even/odd parity means differ by \(2\prod_j d_j\), so parity attains the one-product optimal classification error \((1-\operatorname{TV})/2\) under equal prior probabilities.

This identity also makes the acquisition limit transparent: if any one of the four input contrasts is zero, the entire five-bin distributions coincide, even if the other three contrasts are maximal.

## Target-matched antiperiodic code

Consider a deterministic periodic waveform with

\[
u(t+\tau)=-u(t).
\]

Then the four adjacent feed differences for the ancestry grid have magnitudes \(a|u(t-C)|\) in heavy-probability units. Their product is \(a^4u(t-C)^4\). If output is collected across complete periods at constant flux, its phase is uniform over a period. This remains true for any fixed unknown \(C\), because translating a full-period integral does not change it. Define

\[
q=\frac{1}{2\tau}\int_0^{2\tau}u(s)^4\,ds.
\]

The pooled five-bin distance and parity gap are

\[
\boxed{\operatorname{TV}(P_E^K,P_O^K)=a^4q,\qquad
|\mathbb E_E(-1)^K-\mathbb E_O(-1)^K|=2a^4q.}
\]

For \(a=0.98\), \(a^4=0.92236816\). Thus finite transitions reduce the ideal binary-wave separation by exactly the fourth-power waveform factor \(q\); they do not require replacing the whole-count observation by an assumed independent code draw for each molecule.

## Theorem: maximum \(q\) at a measured slew limit

Assume \(u\) is absolutely continuous, \(|u|\le1\), \(|u'(t)|\le M\) almost everywhere, and \(u(t+\tau)=-u(t)\). Let \(z=M\tau\). Then

\[
\boxed{q\le q_{\max}(z)=
\begin{cases}
z^4/80,&0\le z\le2,\\[2mm]
1-8/(5z),&z\ge2.
\end{cases}}
\]

The bound is attained by a periodic maximum-slew ramp code. For \(z<2\), it is a triangle wave of amplitude \(z/2\), with no plateau. For \(z\ge2\), it has plateaus at \(\pm1\) and linear transitions of duration \(2/M\) at each sign change.

**Proof.** Let \(A=\|u\|_\infty\). Antiperiodicity and the slew bound give

\[
2|u(t)|=|u(t)-u(t+\tau)|\le M\tau,
\]

so \(A\le\min(1,z/2)\). A period of length \(2\tau\) contains a passage from \(-A\) to \(+A\) and one back. Each passage must traverse every level in \([-A,A]\) at speed at most \(M\). Relative to holding at \(|u|=A\), one passage loses at least

\[
\frac1M\int_{-A}^{A}(A^4-v^4)\,dv=\frac{8A^5}{5M}
\]

of the integral of \(u^4\). The two passages therefore imply

\[
q\le A^4-\frac{8A^5}{5M\tau}=A^4\left(1-\frac{8A}{5z}\right).
\]

For fixed \(z\), the right side has derivative \(4A^3(1-2A/z)\), so it increases throughout the allowed interval \(0\le A\le\min(1,z/2)\). Choosing its largest allowed amplitude gives the displayed piecewise bound. Maximum-slew ramps and endpoint plateaus attain the level-traversal bound, proving optimality within the phase-robust antiperiodic class. \(\square\)

The theorem is target-specific: it optimizes the exact E/O age grid with a known \(\tau\), under a measured slew limit. It does not prove that an antiperiodic code is globally optimal among every possible acquisition protocol or for a real catalyst.

## Matched single-tone frequency-response comparator

A sinusoidal isotope modulation at the target half-cycle,

\[
u_{\sin}(t)=A\cos(\pi t/\tau),\qquad A=\min(1,z/\pi),
\]

obeys the same slew limit, is also \(\tau\)-antiperiodic, and has

\[
q_{\sin}(z)=\frac38\min\left(1,(z/\pi)^4\right).
\]

At \(z=\pi\), the ramp code gives \(q=0.490704\), while the single tone gives \(q=0.375\). Their per-product total variation distances at the actual contrast are about \(0.45261\) and \(0.34589\), respectively. At equal independent-product count, the squared-signal parity estimator requires about \((0.490704/0.375)^2=1.71\) times as many products for the sine to match the ramp code's precision. At \(z=2\), the corresponding ratio is about \((0.2/0.06160)^2=10.54\).

This compares a target-tuned sinusoid, not an entire frequency-response program. A sweep or multisine can address several scales, but adds frequencies, time bins or nonlinear cross-frequency calibration; those costs require the actual reactor and detector. Isotopic frequency response itself is established prior art, and this calculation makes no priority claim for the underlying parity operation.

## Multiscale and minimax limit

For an arbitrary measured waveform with \(|u'|\le M\), each input difference across one grid gap is at most \(\min(M\tau,2)\). The exact count-law identity gives

\[
\boxed{\operatorname{TV}(P_E^K,P_O^K)\le
\frac{a^4}{16}\min(M\tau,2)^4.}
\]

If the physical feed isotope fraction itself has measured slew \(|p'|\le S\), the same statement in physical units is

\[
\boxed{\operatorname{TV}(P_E^K,P_O^K)\le\min(S\tau,a)^4.}
\]

For four unequal uncertain gaps \(\delta_j\), the exact per-phase distance is the product of the four actual feed-probability differences and hence is bounded by

\[
\operatorname{TV}\le\prod_{j=0}^3\min(S\delta_j,a).
\]

Consequently, no finite-slew waveform has a strictly positive uniform worst-case guarantee over a target class that permits any \(\tau\downarrow0\), or any one gap \(\delta_j\downarrow0\). For a periodic code of period \(P\), there is also an exact resonance null at \(\tau=P\): every adjacent input pair is equal. A multiscale guarantee therefore needs an explicit lower and upper scale range, a pilot/adaptive acquisition, or a separately charged frequency sweep. No uniformly superior code follows from the supplied contract, which does not specify those bounds.

The small-scale limit is not a theorem that useful codes fail on every bounded range. It is an exact statement that finite bandwidth and an unspecified minimum age gap prevent any promised positive minimax information.

## Product count and shared-campaign accounting

For the deterministic antiperiodic code, the per-product optimal equal-prior error is exactly

\[
e_1=\frac{1-a^4q}{2}.
\]

If \(N\) independent product histories are actually observed under the same deterministic campaign, a majority vote on \((-1)^K\) has error at most \(\exp[-N(a^4q)^2/2]\). Thus

\[
N\ge \frac{2\log 20}{a^8q^2}
\]

is a conservative sufficient count for at most 5% majority error, rounded up to an odd integer. At the ideal \(q=1\), a single product already has error \(0.038816\) at contrast \(0.98\); the Hoeffding count is intentionally more conservative. At \(M\tau=\pi\), the ramp code has \(q=0.490704\), one-product error \(0.273695\), and 31 products suffice by this bound. At \(M\tau=1\), \(q=0.0125\), one-product error is \(0.494235\), and the sufficient count rises to 45,073.

These are counts of independent, calibrated whole-product observations. Ion counts, repeated scans of the same products, or correlated catalytic outputs do not automatically equal \(N\). The deterministic code removes stochastic-code variance; it does not remove shared chemical, instrument, or calibration error. A phase or frequency randomized once per campaign is a single campaign-level variable, never an independent random draw for each product.
