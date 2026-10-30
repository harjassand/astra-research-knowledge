# A randomized weak nested cycle implements the required channel

All diamond norms below are full diamond norms, without a factor of one half.
Only the native controls and motion promise in the frozen `CONTROL_TASK.md`
are used. Memory includes its spectator throughout.

## Theorem

For every admitted fixed, coin-independent drift and every requested
`epsilon > 0`, a finite schedule of the allowed native evolutions has

\[
\left\|\operatorname{Tr}_M\circ\mathbb E\operatorname{Ad}_{U}
 -\operatorname{Ad}_{E}\circ\operatorname{Tr}_M\right\|_\diamond
 \leq\epsilon.
\]

The bound includes all initial data-memory-reference correlations. One
explicit family has total duration `O(epsilon^-2)`, at most
`O(epsilon^-3)` native segments, and `O(log(1/epsilon))` timing bits.
The constants given here are deliberately loose and extremely large.

For the exactly specified durations, the averaged *joint* channel is
close to a data gate tensor a
deterministic, instance-dependent bath unitary. This stronger statement is
only a comparison theorem; the bath unitary need not be known or controlled.

## 1. The interaction frame needs no drift-norm bound

Let `V(t)` be the propagator of `H_M(t)` alone and put

\[
S_j(t)=V(t)^\dagger\sigma_jV(t).
\]

These are Hermitian involutions, preserve the simultaneous Pauli algebra,
and satisfy

\[
\|S_j(t)-S_j(s)\|\leq |t-s|.
\tag{1}
\]

Indeed, their almost-everywhere derivative is
`i V(t)^dagger [H_M(t),sigma_j] V(t)`, of norm at most one.
Piecewise continuity gives the integral statement (1). No derivative of
`H_M`, its norm, or a spectator-dimension bound is invoked.

The controlled Hamiltonians in this frame are

\[
J_A(t)=X_1\otimes S_x(t),\quad
J_B(t)=X_2\otimes S_y(t),\quad
J_C(t)=Y_1\otimes S_z(t).
\]

They are fixed functions of absolute time, independently of the private
coins. All cycles below have the same duration for every coin outcome.

## 2. The actual ten-segment schedule

For each cycle, draw fresh independent fair signs `s_A,s_B` and set
`s_C=s_A s_B`. Use the following **chronological** segments, each of duration
`delta`, with the displayed native strength:

| Segment | Handle | Strength |
|---:|:---:|:---:|
| 1 | B | `-s_B` |
| 2 | C | `-s_C` |
| 3 | B | `+s_B` |
| 4 | C | `+s_C` |
| 5 | A | `-s_A` |
| 6 | C | `-s_C` |
| 7 | B | `-s_B` |
| 8 | C | `+s_C` |
| 9 | B | `+s_B` |
| 10 | A | `+s_A` |

At a common frozen time, write `a=-i s_A J_A`, and similarly `b,c`.
The product, with the rightmost factor acting first, is

\[
W=e^{\delta a}P e^{-\delta a}P^{-1},\qquad
P=e^{\delta b}e^{\delta c}e^{-\delta b}e^{-\delta c}.
\]

Its Taylor coefficients through degree three are

\[
W=I+\delta^3[a,[b,c]]+O(\delta^4)
  =I-4i\delta^3F+O(\delta^4),\qquad F=Z_1X_2\otimes I_M.
\tag{2}
\]

For clarity, `[J_B,J_C]=2iY_1X_2 tensor S_x` and
`[J_A,[J_B,J_C]]=-4F`; multiplying by `(-i)^3` gives `-4iF`.
The sign product is one. Every handle also has zero signed total duration.
The exact rational Pauli calculation in `check_construction.py` verifies
all four signed versions of (2), including the zero first and second
coefficients.

## 3. A uniform one-cycle channel estimate

Fix one cycle, translate its start to zero, and write `L=10 delta`.
Absolute bath times are understood. Assume `0 < delta <= 1/10`.
Let `f_j(t)` be the orientation `+1/-1` on the intervals occupied by handle
`j`, and zero elsewhere; the actual Hamiltonian is
`s_j f_j(t) J_j(t)` on those intervals.
Denote the cycle unitary by `U_s` and its Dyson terms by `D_k(s)`.

The norm-one Hamiltonian gives the completely uniform fourth-order tail

\[
\|R_4(s)\|\leq e^L L^4/24 <1133\delta^4.
\tag{3}
\]

### 3a. The second-order survivor is a bath operation

The signs have zero individual means and zero pairwise correlations.
Consequently `E D_1=0`, and

\[
\mathbb E D_2=I_D\otimes Q,
\quad
Q=-\sum_j\int_{t>s}f_j(t)f_j(s)S_j(t)S_j(s)\,ds\,dt.
\tag{4}
\]

Here the data Pauli squares to the identity whenever the same handle
occurs twice. Set

\[
G_j=\int_0^L f_j(t)S_j(t)\,dt,
\qquad K=(Q-Q^\dagger)/2.
\]

Each `G_j` is Hermitian. Splitting the integration square into its two
ordered halves gives the exact identity

\[
Q+Q^\dagger=-\sum_jG_j^2,
\quad Q=K-\tfrac12\sum_jG_j^2.
\tag{5}
\]

Because `integral f_j=0`, use the common midpoint `c=L/2` in (1). The
actual schedule has

\[
\|G_A\|\leq5\delta^2,\quad
\|G_B\|\leq12\delta^2,\quad
\|G_C\|\leq8\delta^2.
\]

Thus

\[
\|Q-K\|\leq\frac{233}{2}\delta^4.
\tag{6}
\]

Also

\[
K=-\tfrac12\sum_j\int_{t>s}f_j(t)f_j(s)
                 [S_j(t),S_j(s)]\,ds\,dt,
\]

so (1) implies

\[
\|K\|\leq\int_{0<s<t<L}(t-s)\,ds\,dt
          =L^3/6=(500/3)\delta^3.
\tag{7}
\]

`K` is anti-Hermitian and acts only on memory. It is not discarded as
zero, and it need not be small after all cycles are composed.

### 3b. The third-order survivor is the desired gate

Among third-degree sign monomials only those containing A, B, C once each
have nonzero expectation. Their expectation is one. Freeze all three
handles at the common midpoint. Equation (2) says their total is exactly
`-4i delta^3 F`. Replacing a product at times `t_1,t_2,t_3` by this frozen
product costs at most `sum_l |t_l-L/2|`. Therefore

\[
\left\|\mathbb E D_3+4i\delta^3F\right\|
 \leq\int_{0<t_3<t_2<t_1<L}\sum_{l=1}^3|t_l-L/2|\,d^3t
 =L^4/8=1250\delta^4.
\tag{8}
\]

The integral is one sixth of its integral over the cube, because the
integrand is symmetric. This step uses only Lipschitz motion.

### 3c. The mean unitary is insufficient: control its channel variance

Let

\[
X=I_D\otimes K-4i\delta^3F,\qquad V=e^X.
\]

It is a unitary of the form
`exp(-4i delta^3 Z_1 X_2) tensor exp(K)`. By (7),
`||X|| <171 delta^3`. For `delta<=1/10`,

\[
\|e^X-I-X\|\leq\tfrac12\|X\|^2 e^{\|X\|}
 <175\delta^4.
\]

Together with (3), (6), and (8), this proves

\[
\|\mathbb E U_s-V\|<2675\delta^4.
\tag{9}
\]

To control the fluctuation, Duhamel's inequality and midpoint freezing give

\[
\|U_s-U_s^{\rm frozen}\|
\leq\int_0^L|t-L/2|\,dt=25\delta^2.
\]

Equations (2), (3), and `||V-I||<=||X||` then give, for **every** sign
realization,

\[
\|U_s-V\|
\leq25\delta^2+175\delta^3+1133\delta^4<54\delta^2.
\tag{10}
\]

Writing `Delta_s=U_s-V`, expand the channel exactly:

\[
\mathbb E\operatorname{Ad}_{U_s}-\operatorname{Ad}_V
 =(\mathbb E\Delta_s)(\cdot)V^\dagger
   +V(\cdot)(\mathbb E\Delta_s)^\dagger
   +\mathbb E\bigl[\Delta_s(\cdot)\Delta_s^\dagger\bigr].
\]

The completely bounded trace norm of `rho -> L rho R` is at most
`||L|| ||R||`. Hence (9) and (10) prove

\[
\boxed{
\left\|\mathbb E\operatorname{Ad}_{U_s}
 -\operatorname{Ad}_{\exp(-4i\delta^3Z_1X_2)\otimes e^K}
 \right\|_\diamond
 \leq10000\delta^4.}
\tag{11}
\]

The sharper displayed intermediate constants give 8266 in place of
10000. The round constant is used below. In particular, averaging
unitaries has not been identified with averaging their channels.

## 4. Composition despite arbitrary retained correlations

Use fresh independent signs in each of `N` equal-duration cycles. For a
fixed drift their interaction-frame unitaries are functions of their own
cycle signs, so the averaged channel is the chronological composition of
the averaged cycle channels. This identity is linear and does not assume
fresh memory states or independent data-memory inputs.

Apply (11) in diamond norm, telescope the composition, and use
contractivity of channels. The comparison is the product of unitaries

\[
V_r=e^{-4i\delta^3Z_1X_2}\otimes e^{K_r}.
\]

The `K_r` need not commute with one another, but every one commutes with
the data gate. Their product therefore factorizes. Restoring the drift
frame merely left-multiplies the bath factor by `V(T)`. Thus for some bath
unitary `B_H`,

\[
\left\|\mathbb E\operatorname{Ad}_{U_{\rm physical}}
 -\operatorname{Ad}_{e^{-4iN\delta^3Z_1X_2}\otimes B_H}
 \right\|_\diamond
 \leq10000N\delta^4.
\tag{12}
\]

Discarding memory cannot increase this norm, and a bath-only unitary
does not change a partial trace, even on initially correlated states.

Coin independence is essential here. If the bath is allowed to react to
the realized signs, (4) and (8) need not hold.

## 5. Finite parameters, duration, switching, and timing tolerance

Put `e=min(epsilon,1)` and choose

\[
b=\lceil\log_2(4000/e)\rceil,\quad q=2^b,\quad\delta=1/q.
\]

Compute a dyadic `pi_hat` with `|pi_hat-pi|<=q^-3` and let `N` be the
nearest integer to `pi_hat q^3/16`. Only `3b+O(1)` bits of pi are needed;
the supplied generator uses an alternating-series certified Machin
formula. Then

\[
\left|N-\frac{\pi q^3}{16}\right|\leq\frac9{16},\quad
\left|\frac{4N}{q^3}-\frac\pi4\right|\leq\frac9{4q^3}.
\]

The extra full diamond error from the gate angle is at most `9/(2q^3)`.
By (12), the schedule with exactly specified durations consequently has

\[
\begin{split}
\text{error}&\leq\frac{10000N}{q^4}+\frac9{2q^3}\\
&\leq\frac{10000\pi}{16q}+\frac{5625}{q^4}+\frac9{2q^3}
 <\frac{2000}{q}\leq e/2.
\end{split}
\tag{13}
\]

The strict middle bound holds already for `q>=10`; here `q>=4096`.
There are exactly `m=10N` native segments, at most `m-1` switches, and

\[
T=10N/q\leq(5\pi/8)q^2+45/(8q),\qquad
m\leq(5\pi/8)q^3+45/8.
\tag{14}
\]

Since `4000/e<=q<8000/e`, these are the stated `O(e^-2)` duration and
`O(e^-3)` switching bounds. Two fresh random bits per cycle suffice.
Pulse strengths are exactly the legal signed strengths one.

For an explicit conservative precision tolerance, allow each actual
segment duration to differ from `1/q` by at most

\[
\eta=e/(4m^2).
\tag{15}
\]

The `k`th switching time can then move by at most `k eta`. Extend the
shorter schedule with uncontrolled drift so the two compared schedules
end at a common time. In the drift interaction frame the integrated
control-Hamiltonian difference is at most

\[
2\sum_{k=1}^{m-1}k\eta+m\eta=m^2\eta.
\]

This uses the norm-two bound on the change between adjacent native
Hamiltonians and a norm-one final turn-off. Duhamel and the unitary
channel bound cost at most `2m^2 eta=e/2` in diamond norm. The extension
changes only the discarded bath state. Combining with (13) proves the
theorem even with these independent duration errors. Total actual time
is at most `T+m eta`.

Absolute duration precision of
`ceil(log_2(4m^2/e))=7 log_2(1/e)+O(1)` binary places is sufficient.
This very conservative tolerance is optional for the ideal schedule but
makes the parameter-precision claim explicit. It never compares two
bath propagators using a bound on `||H_M||`.

## 6. Exact scope

This establishes the requested averaged-channel reachability statement
for arbitrary finite spectators and arbitrary admitted time dependence.
It does not establish an individual-coin guarantee, a short practical
gate, acquisition or hardware feasibility, or an optimum resource rate.
The deterministic exact obstruction in the packet remains consistent:
each finite approximate schedule has residual noise, and accuracy is
obtained by increasing both the word length and total duration.

The crucial structural feature is that the same-handle second-order
survivors are memory-only. They can be retained as actual bath evolution.
For native interactions whose same-label products act nontrivially on
data, this proof does not automatically extend.
