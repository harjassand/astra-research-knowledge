# A uniform randomized native entangler

This is a proof for the exact interface in `../../packet/CONTROL_TASK.md`. All
norms on channels below are diamond norms, without a factor of one half. The
proof is dimension independent. No norm bound on the bath Hamiltonian is used.

## The schedule and theorem

Put `F = Z_1 X_2`, with a bath identity understood. One cycle has ten pulses,
each of duration `d`, in the following **chronological** order:

| Pulse | Handle | Strength |
|---:|:---:|:---:|
| 1 | B | -s_B |
| 2 | C | -s_C |
| 3 | B | +s_B |
| 4 | C | +s_C |
| 5 | A | -s_A |
| 6 | C | -s_C |
| 7 | B | -s_B |
| 8 | C | +s_C |
| 9 | B | +s_B |
| 10 | A | +s_A |

Here `s_A,s_B` are independent fair private signs and `s_C=s_A s_B`.
Draw two **fresh independent signs in every cycle**. The cycle length `10d`
and every switching time are independent of the signs. There are no other
operations and no idle times.

**One-cycle theorem.** For `L=10d <= 1`, and any starting time, the averaged
joint data-memory channel in the bath interaction frame obeys

\[
\left\|\Phi-\operatorname{Ad}_{e^{-4id^3 F}\otimes e^G}\right\|_\diamond
\le \frac54 L^4. \tag{1}
\]

Here `G` is an anti-Hermitian bath-only operator depending on the unknown bath
trajectory in that cycle. The controller does not compute it. Its norm obeys
`||G|| <= L^3/6`.

**Full-gate theorem.** Choose an integer `N` and

\[
d=\left(\frac{\pi}{16N}\right)^{1/3},\qquad 10d\le1.
\]

Then, uniformly over all admitted piecewise-continuous bath Hamiltonians, all
finite spectator dimensions, and all correlated input states,

\[
\left\|\overline{\mathcal C}_{DM\to D}
-\operatorname{Ad}_{E}\circ\operatorname{tr}_M\right\|_\diamond
\le \frac{3125\pi}{4}\,d. \tag{2}
\]

The reference is already included by the diamond norm. This proves the
requested approximate randomized reachability.

## Removing only the irrelevant bath motion

Let `V_0(t)` solve `dV_0/dt=-i H_M(t)V_0`, and define

\[
S_j(t)=V_0(t)^\dagger\sigma_j V_0(t).
\]

For almost every time,

\[
\frac{d S_j}{dt}=iV_0(t)^\dagger[H_M(t),\sigma_j]V_0(t).
\]

Consequently each `S_j` is norm-one and 1-Lipschitz. The three `S_j(t)` obey
the simultaneous Pauli algebra at every time. These statements hold even if
`||H_M(t)||` is arbitrarily large. Piecewise continuity and finite dimension
justify the integral identity and hence the Lipschitz estimate across joins.

On a single cycle use a relative clock `t in [0,L]`. Write the signed pulse
profiles from the table as `f_j(t) in {0,+1,-1}`. At most one is nonzero,
`sum_j |f_j(t)|=1`, and `integral f_j(t)dt=0` for each handle. The
interaction-frame control Hamiltonian is

\[
K_s(t)=\sum_j s_j f_j(t)D_j\otimes S_j(t),
\quad D_A=X_1,\ D_B=X_2,\ D_C=Y_1.
\]

It has norm one. Freeze all three memory operators at the common midpoint
`m=L/2`, solely as a proof device, obtaining `K_s^0(t)`. Then

\[
\|K_s(t)-K_s^0(t)\|\le |t-m|. \tag{3}
\]

There is no physical freezing operation.

## The frozen cubic identity

Use generators `a=-iA`, `b=-iB`, `c=-iC`, with the simultaneous frozen memory
Paulis. In ordinary matrix order the chronological table equals

\[
W_s(d)=e^{d s_Aa}V_s(d)e^{-d s_Aa}V_s(d)^{-1},
\quad
V_s(d)=e^{d s_Bb}e^{d s_Cc}e^{-d s_Bb}e^{-d s_Cc}.
\]

Thus its constant, linear, quadratic and cubic Taylor coefficients are

\[
W_s(d)=I+d^3s_As_Bs_C[a,[b,c]]+O(d^4)
      =I-4id^3F+O(d^4). \tag{4}
\]

Indeed `[B,C]=2iY_1X_2 S_x` and `[A,[B,C]]=-4F`, so
`[a,[b,c]]=-4iF`. The product of the three private signs is exactly one.
The operator is bath independent because the common-conjugation Pauli
algebra is preserved. The vanishing linear and quadratic coefficients hold
for each of the four sign choices, not merely in expectation.

`exact_word_check.py` verifies these coefficients using only exact
Gaussian-integer arithmetic. The algebra above supplies the general
spectator-independent argument.

## The moving-medium channel estimate

Let `U_{n,s}` be the nth unitary Dyson term for `K_s`, with `U_{0,s}=I`, and
write

\[
Q_j=\int_0^L f_j(t)D_j\otimes S_j(t)\,dt.
\]

Zero pulse areas and midpoint freezing give

\[
U_{1,s}=-i\sum_j s_jQ_j,
\quad
\sum_j\|Q_j\|\le\int_0^L|t-m|dt=\frac{L^2}{4}. \tag{5}
\]

Since the sign means are zero and the pair correlations are
`E[s_j s_k]=delta_jk`,

\[
\mathbb E U_{1,s}=0,
\qquad
\mathbb E U_{2,s}=G-\frac12\sum_jQ_j^2, \tag{6}
\]

where

\[
G=-\frac12\sum_j\int_{t>u}f_j(t)f_j(u)
 I_D\otimes[S_j(t),S_j(u)]\,dt\,du. \tag{7}
\]

`G` is bath only and anti-Hermitian. The identity (6) follows by splitting
each ordered self-product into its commutator part and half the full-square
integral. The data part squares to the identity for every handle. Also,

\[
\|G\|\le\int_{t>u}(t-u)\,dt\,du=\frac{L^3}{6}. \tag{8}
\]

The bound uses `||[S_j(t),S_j(u)]|| <= 2|t-u|` and enlarges the handle
supports to the whole triangle.

It is essential to estimate the averaged **channel**. Averaging the unitary
alone would omit `E[U_{1,s}(.)U_{1,s}^dagger]`. From (5)-(6), the entire
second-degree part of that channel differs from `[G,(.)]` by at most

\[
\sum_j\|Q_j\|^2+\mathbb E\|U_{1,s}\|^2\le\frac{L^4}{8}. \tag{9}
\]

The moving quadratic unitary term itself is smaller than its generic Dyson
bound: its frozen counterpart is zero by (4), and (3) gives

\[
\|U_{2,s}\|\le
\int_{t>u}(|t-m|+|u-m|)\,dt\,du=\frac{L^3}{4}. \tag{10}
\]

Put `D=-4id^3F`. Comparing cubic products with their frozen counterparts
using (3)-(4) gives

\[
\|U_{3,s}-D\|\le
\int_{t_1>t_2>t_3}\sum_{k=1}^3|t_k-m|\,dt_1dt_2dt_3
=\frac{L^4}{8}. \tag{11}
\]

The integral is one sixth of its symmetric cube integral. The two cubic
left/right channel terms therefore differ from `[D,(.)]` by at most `L^4/4`.
The remaining degree-three cross terms have norm at most

\[
2\|U_{1,s}\|\|U_{2,s}\|\le\frac{L^5}{8}. \tag{12}
\]

For completeness, truncate the *channel* Dyson series at degree three. The
generator `-i[K_s(t),(.)]` has diamond norm at most two. Its exact fourth-order
integral remainder contains four such generators and one full intervening
unitary channel, whose diamond norm is one. Consequently that remainder is
at most `2^4 L^4/4! = 2L^4/3`. An exponential factor is unnecessary here.
This channel expansion has exactly the same degree-at-most-three terms as
the unitary Dyson products used in (9)-(12).

Combining these bounds,

\[
\|\Phi-(\mathrm{Id}+[G+D,(.)])\|_\diamond
\le\frac{L^4}{8}+\frac{L^4}{4}+\frac{L^5}{8}+\frac{2L^4}{3}
\le\frac76L^4. \tag{13}
\]

`G` and `D` commute. Their sum is anti-Hermitian and satisfies

\[
\|G+D\|\le\left(\frac16+\frac1{250}\right)L^3<\frac{L^3}{5}.
\]

The first-order Taylor remainder of its unitary conjugation is at most
`2||G+D||^2 <= 2L^6/25`; this follows from the integral Taylor formula and
the diamond norm one of unitary conjugations. Therefore, for `L<=1`,

\[
\|\Phi-\operatorname{Ad}_{e^{G+D}}\|_\diamond
\le\left(\frac76+\frac2{25}\right)L^4
=\frac{187}{150}L^4<\frac54L^4.
\]

This proves (1). Every multiplication-norm estimate also holds with an
arbitrary spectator/reference identity tensored on. No dimension factor is
hidden in it.

## Accumulation without resetting the medium

The bath interaction frame is fixed by `H_M(t)` alone. In particular it does
not depend on any private sign. Fresh independent signs make the averaged
joint channel for `N` cycles exactly `Phi_N ... Phi_1`, even though the memory
state can stay correlated with the data, the reference and past controls.
No memory Markov property is assumed.

Replace `Phi_k` by its comparison unitary channel from (1). Telescoping uses
diamond norm one of all the actual and comparison channels and gives error
at most `(5/4)N(10d)^4`. Their comparison product factorizes as

\[
\exp(-4iNd^3F)\otimes(e^{G_N}\cdots e^{G_1}).
\]

Restoring the laboratory frame only multiplies the bath factor by `V_0(T)`.
Partial trace discards it even on correlated inputs. With `4Nd^3=pi/4` the
remaining error is

\[
\frac54N(10d)^4
=\frac{3125\pi}{4}d,
\]

which proves (2). A bath allowed to react to the realized signs would destroy
the deterministic interaction frame and the exact conditional averaging
used here. That is outside the stated noise game.

## Explicit duration, count and finite precision

Let `e=min(epsilon,1)`, set `h=e/5000`, and choose

\[
N=\left\lceil\frac{\pi}{16h^3}\right\rceil,
\qquad d_N=\left(\frac{\pi}{16N}\right)^{1/3}.
\]

For exact common pulse duration `d_N`, error (2) is at most
`(5pi/32)e < 0.491e`. The resources are exactly

\[
\begin{aligned}
T&=10Nd_N=\frac{5\pi}{8}d_N^{-2},\\
\text{native segments}&=10N,\\
\text{interior switching boundaries}&=10N-1,\\
\text{private fair coin bits}&=2N.
\end{aligned}
\]

Hence duration is `O(epsilon^-2)` and segment/switch count is
`O(epsilon^-3)`. No extra control time or physical operation is hidden in
these counts. Computing the next two signs and the next event time is
ordinary finite classical computation.

An irrational duration is unnecessary. Use a positive rational `d` with

\[
|d/d_N-1|\le e/100.
\]

The comparison angle becomes `4Nd^3`. Its channel distance from the target is
at most

\[
\frac\pi2\left|\left(d/d_N\right)^3-1\right|
\le\frac\pi2(0.030301)e<0.048e.
\]

The accumulated cycle error is at most
`(5pi/32)(1.01)^4 e < 0.511e`. Thus the finite rational common duration still
gives total error below `0.559e`. Its absolute required accuracy is
`O(epsilon^2)` and its bit length is `O(log(1/epsilon))`.

If a clock implementation perturbs each switching event, including the
final turnoff, by absolute time at most `b`, while preserving event order,
a direct interaction-frame Duhamel bound adds at most `4(10N)b` to the
channel error. Compare both controls on the common horizon `T+b`, extending
each by free bath-only evolution after its final turnoff; that extension
has no effect on the returned data channel. The two control profiles differ only
on intervals whose total length is at most the sum of boundary shifts;
their Hamiltonian difference has norm at most two there. For example,

\[
b\le\frac{e}{160N}
\]

adds at most `e/4`; the overall bound stays below `0.809e < epsilon`.
Thus absolute event-time precision `O(epsilon^4)` suffices. Specifying event
times over the `O(epsilon^-2)` total horizon still uses
`O(log(1/epsilon))` bits per event. This clock tolerance is an explicit
implementation resource, not an assumption about the bath's derivatives.
The final turnoff occurs by time `10Nd+b`.

These constants are conservative. In the native rate-one units the
asymptotic sufficient duration is approximately
`4.91e7 epsilon^-2`; this is an existence theorem with a large cost, not a
practical speed claim.

## A sharp local noise check for this particular word

For the admitted constant qubit bath `H_M=Z_M/2`, exact Taylor expansion gives
in its interaction frame

\[
\begin{aligned}
U_s(d)&=I+id^2(5s_A X_1Y_M-4s_B X_2X_M)+O(d^3),\\
\mathbb E U_s(d)&=I+id^3(8Z_M-4F)-\frac{41}{2}d^4 I+O(d^5).
\end{aligned}
\]

Here the bath curvature in (7) is `G=8id^3Z_M+O(d^5)`. Consequently

\[
\Phi-\operatorname{Ad}_{e^{-4id^3F}\otimes e^G}
=d^4\{25(\operatorname{Ad}_{X_1Y_M}-\mathrm{Id})
       +16(\operatorname{Ad}_{X_2X_M}-\mathrm{Id})\}+O(d^5). \tag{14}
\]

The two nonidentity Paulis and the identity have mutually orthogonal
normalized Choi vectors. The normalized Choi trace norm of (14) is therefore
`82d^4+O(d^5)`, a lower bound on its diamond norm. The leading coefficient is
verified by `exact_moving_expansion.py` using exact Gaussian-integer
arithmetic after rescaling the Taylor parameter. This confirms that the
fourth-order **channel** fluctuation is real for this word; averaging the
unitary would miss it. It does not give an all-policy resource lower bound.

