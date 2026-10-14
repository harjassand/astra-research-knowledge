# Proof closure: finite-slew antiperiodic optimum and pooled TV

This supplement closes two proof details in the frozen PROOF.md and REPORT.md. It does not change their scope: the optimization is only over absolutely continuous, \(\tau\)-antiperiodic codes for the stated four-gap E/O target, with a measured normalized slew bound. It is not a global acquisition-protocol optimum or external validation.

## Complete upper bound, allowing arbitrary turning points

Let \(u:\mathbb R\to[-1,1]\) be \(2\tau\)-periodic and absolutely continuous, with

\[
u(t+\tau)=-u(t),\qquad |u'(t)|\le M\quad\text{a.e.},\qquad
A=\max_t|u(t)|.
\]

We prove the bound without assuming that a half-period is monotone, has one zero, or has symmetric extrema. The cases \(A=0\) or \(M=0\) are immediate. For \(A>0\), antiperiodicity gives both a \(+A\) point and a \(-A\) point on the period circle. Also

\[
2A=|u(t)-u(t+\tau)|\le M\tau,
\quad\text{so}\quad A\le \min(1,M\tau/2).
\]

Set \(D(v)=A^4-v^4\ge0\) for \(|v|\le A\), and define the increasing primitive

\[
\Phi(v)=\int_{-A}^{v}D(r)\,dr.
\]

The chain rule for absolutely continuous functions gives

\[
\int_0^{2\tau}D(u(t))|u'(t)|\,dt
=\int_0^{2\tau}|(\Phi\circ u)'(t)|\,dt.
\]

On the period circle, choose one \(+A\) point and one \(-A\) point. The two arcs joining them are disjoint except at their endpoints. Along each arc, the total variation of \(\Phi\circ u\) is at least the absolute difference of its endpoint values. Summing the two arcs therefore yields

\[
\int_0^{2\tau}D(u)|u'|\,dt
\ge 2\bigl(\Phi(A)-\Phi(-A)\bigr)
=2\int_{-A}^{A}(A^4-v^4)\,dv
=\frac{16A^5}{5}.
\]

This variation argument includes extra extrema, repeated or flat zero crossings, unequal rising and falling profiles, and all other backtracking: those can only increase the total variation. Since \(D(u)\ge0\) and \(|u'|\le M\),

\[
\int_0^{2\tau}D(u(t))\,dt
\ge \frac1M\int_0^{2\tau}D(u(t))|u'(t)|\,dt
\ge \frac{16A^5}{5M}.
\]

Consequently, for \(q=(2\tau)^{-1}\int_0^{2\tau}u(t)^4\,dt\),

\[
q=A^4-\frac1{2\tau}\int_0^{2\tau}D(u(t))\,dt
\le A^4-\frac{8A^5}{5M\tau}.
\]

Writing \(z=M\tau>0\), the right-hand side \(F_z(A)=A^4-8A^5/(5z)\) has derivative

\[
F_z'(A)=4A^3(1-2A/z)\ge0
\quad\text{for }0\le A\le\min(1,z/2).
\]

It is therefore maximized at \(A=\min(1,z/2)\), giving

\[
q\le\begin{cases}z^4/80,&0<z\le2,\\[1mm]1-8/(5z),&z\ge2.\end{cases}
\]

For \(z\le2\), a triangle wave of amplitude \(z/2\), with slope magnitude \(M\) throughout, attains equality. For \(z\ge2\), a waveform that ramps between \(-1\) and \(+1\) at slope magnitude \(M\) for duration \(2/M\) and holds the endpoint value for the remaining \(\tau\)-half-cycle attains equality; the second half-cycle is its negative. Thus the upper bound is attained in both regimes. This proves the stated optimum over the full antiperiodic Lipschitz class, including codes with arbitrary additional extrema.

## Phase-pooled count-law TV equality

At a fixed output phase let \(s=t-C\), and use the frozen proof's convention

\[
d_j=p(s-j\tau)-p(s-(j+1)\tau),\qquad j=0,1,2,3,
\quad p(s)=\tfrac12(1+a u(s)).
\]

Antiperiodicity implies \(u(s-j\tau)=(-1)^j u(s)\), hence

\[
d_j=(-1)^j a u(s),\qquad \prod_{j=0}^3d_j=a^4u(s)^4\ge0.
\]

The fixed-phase signed five-bin difference vector is

\[
P_E^K-P_O^K=\frac{\prod_jd_j}{8}(1,-4,6,-4,1).
\]

Let phase pooling mean averaging over complete code periods with constant product flux, so the phase measure is uniform; a fixed unknown \(C\) only translates that measure. Since the scalar \(\prod_jd_j\) is nonnegative at every phase, averaging preserves the same signed coefficient vector:

\[
P_{E,\mathrm{pool}}^K-P_{O,\mathrm{pool}}^K
=\frac{a^4q}{8}(1,-4,6,-4,1).
\]

The coefficient vector has \(\ell^1\) norm \(16\), so pooled TV is \(\tfrac12(a^4q/8)16=a^4q\). At each phase, pointwise TV is \(\prod_j|d_j|=a^4u(s)^4\), whose phase average is also \(a^4q\). Therefore

\[
\operatorname{TV}(P_{E,\mathrm{pool}}^K,P_{O,\mathrm{pool}}^K)
=\mathbb E_{\rm phase}\!\left[\operatorname{TV}(P_E^K(\cdot\mid\rm phase),P_O^K(\cdot\mid\rm phase))\right]
=a^4q.
\]

The equality uses the nonnegative product sign forced by the four factors and exact antiperiodicity. In general, total variation is convex under pooling and only the inequality “pooled TV \(\le\) average pointwise TV” follows; equality need not hold if the signed phasewise scalar changes sign. The phase-pooling claim also retains the model condition of uniform phase exposure (for example, constant output flux over complete periods).

## Scope note

This closes the stated mathematical upper-bound and pooling steps only. It does not expand the code class, establish an optimum over arbitrary non-antiperiodic/adaptive protocols, resolve unknown-scale minimax design, or validate feed purity, slew, flux, isotope neutrality, or detector calibration in a physical system. The finite product counts and acquisition/calibration costs remain as scoped in the frozen packet.
