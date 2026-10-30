# Two obstructions to extending the first-motion gate to unknown gains

This file retains the full trace-norm/diamond-norm convention of the task,
without a factor of one half. The complete unknown-gain question remains
open here. The results below rule out two precise construction classes;
neither is an all-policy impossibility theorem.

The predecessor supplement already contains native sign projection,
order raising and odd-chirality polynomial compensation. Those constructions
are not claimed as new. Their stronger static or finite-jet regularity is
essential to the comparison below.

## 1. What the first-motion primitive does supply with unknown gains

Write `c=g_A g_B g_C in [1,8]`, and `F=Z_1X_2`. Use the first-tranche
ten-pulse schedule, but with native strengths `+/-1/2`. Its normalized
coupling coefficients are `g_j/2 in [1/2,1]`. Their norm and first-motion
bound are at most one, so every estimate in the preserved first-tranche
derivation applies uniformly. The frozen cubic term is now

\[
-4i d^3\frac{c}{8}F=-\frac i2 c d^3F.
\]

Consequently one cycle, with fresh private parity signs, satisfies

\[
\|\Phi-\operatorname{Ad}_{e^{-icd^3F/2}\otimes e^G}\|_\diamond
\le\frac54(10d)^4,
\qquad 10d\le1,
\]

for a bath-only anti-Hermitian `G`. It follows that for any prescribed real
`alpha`, the uncertain rotation

\[
R_c(\alpha)=e^{-i\alpha cF}
\]

is a qualified completed operation, after final bath discard, to any finite
uniform accuracy `eta>0`. For `alpha>0`, choose

\[
Nd^3=2\alpha,
\quad
\text{error}\le25000\alpha d,
\quad
T=20\alpha d^{-2},
\quad
\text{segments}=20\alpha d^{-3}.
\]

Choose an integer `N` large enough to meet the displayed bound, then compute
`d=(2alpha/N)^(1/3)`. For negative `alpha`, flip the C convention. The zero
case is idle. This is a uniform product comparison on the retained complete
memory, so completed calls compose on arbitrary correlated inputs. Finite
rational common durations and event-time tolerances follow exactly as in
the first tranche, with the additional target-angle Lipschitz factor bounded
using `c<=8`. For fixed `alpha`, duration and count remain `O(eta^-2)` and
`O(eta^-3)`, with logarithmic scalar-description bit length.

This gives an unknown-coefficient logical rotation, not a uniform target
angle. The distinction cannot be removed by randomizing its duration.

## 2. A sharp barrier for every commuting-macro policy

Consider any finite open-loop policy built exclusively from completed
operations `R_c(alpha)` above, with arbitrary private randomness in the
number, order, signs and sizes of the coefficients. For each realized
program all logical factors commute, so its ideal logical action is

\[
e^{-ic A F}
\]

for a real random variable `A` independent of the gain. The different
bath factors can depend on gains and coins; after discarding the bath they
do not change this statement, including on correlated inputs.

Choose vectors from the `F=+1` and `F=-1` eigenspaces. The off-diagonal
coherence between them is multiplied by

\[
m(c)=\mathbb E e^{-2icA}.
\]

The desired entangler has multiplier `z=-i`. Gains `(1,1,1)` and `(2,1,1)`
are both allowed, so put

\[
Z=e^{-2iA},\qquad m_1=\mathbb EZ,\quad m_2=\mathbb EZ^2.
\]

The moment Toeplitz matrix

\[
T=\begin{pmatrix}
1&\overline m_1&\overline m_2\\
m_1&1&\overline m_1\\
m_2&m_1&1
\end{pmatrix}
\]

is positive semidefinite. Its hypothetical exact-target version is

\[
T_0=\begin{pmatrix}1&i&i\\-i&1&i\\-i&-i&1\end{pmatrix}.
\]

For

\[
v=\frac1{\sqrt3}(1,e^{i\pi/3},e^{2i\pi/3})^T,
\qquad T_0v=(1-\sqrt3)v.
\]

If both `|m_j+i|<=r`, each of the three off-diagonal pairs contributes at
most `2r/3` to `v^dagger(T-T_0)v`. Positivity therefore requires

\[
0\le v^\dagger Tv\le1-\sqrt3+2r,
\quad\text{so}\quad
r\ge r_*:=\frac{\sqrt3-1}{2}\approx0.3660254. \tag{1}
\]

For these two-sector phase channels, their diamond distance is precisely
the absolute difference of their coherence multipliers. One lower-bound
input is an equal superposition of an `F=+1` and an `F=-1` vector. For the
upper bound, factor the off-diagonal difference map into a phase unitary,
the scalar magnitude, and the map `(Id-Ad_F)/2`, whose diamond norm is one.
Thus (1) is a diamond-error floor for this policy class, not just a bound on
one arbitrary numerical surrogate.

The two-point bound is sharp. Let

\[
\Pr(Z=-1)=p=\frac{1-1/\sqrt3}{2},
\qquad
\Pr(Z=e^{-i\pi/3})=1-p.
\]

Then both `|m_1+i|` and `|m_2+i|` equal `r_*`. The corresponding coefficient
choices are `A=pi/2` and `A=pi/6`. Sharpness is only for these two gain
values; no optimality claim is made over the full gain box.

If a physical macro implementation has total uniform synthesis error
`delta`, the triangle inequality gives

\[
\epsilon+\delta\ge r_*.
\]

In particular, arbitrarily accurate implementation of the commuting
unknown-c library does not make uniform gain compensation possible.
This barrier permits arbitrarily long finite programs and arbitrary
probability distributions of their scalar angles. It does **not** cover
native interactions interleaved inside uncompleted macros.

## 3. A first-motion adversary against fixed higher-degree weak words

The other natural bridge is the predecessor's higher odd-chirality Lie
words. The following theorem shows why substituting only a Lipschitz bath
estimate into that strategy fails.

Let a fixed finite native profile on normalized time `x in [0,ell]` be
`f_A(x),f_B(x),f_C(x)`, with at most one active, magnitudes at most one and
each profile having zero area. Apply fresh fair parity signs
`s_A,s_B,s_C=s_As_B` to the whole profile in every repetition. Physical time
is `t=t_k+tau*x`. Assume that at unit gains and zero bath drift its whole
unitary obeys

\[
W_s(\tau)=I+O(\tau^5) \tag{2}
\]

for every sign choice. Assume A is used nontrivially. In particular, a fixed
word whose first useful clean Lie term has degree `k>=5` satisfies (2).

**Theorem.** If the number of repetitions obeys

\[
N(\tau)\gg\tau^{-4}\log(1/\tau),
\]

then this program has worst admitted-bath output trace-norm error at least
`1-o(1)` against **any** data unitary as `tau->0`. In particular it cannot
implement a higher-degree finite-angle primitive by choosing
`N beta tau^k=theta!=0` with `k>4`.

Only the qubit memory and the unit gain point are needed for this
counterexample. Hence enlarging the source class to the unknown gain box
does not help this construction class.

### The allowed bath

Set

\[
F_A(x)=\int_0^x f_A(y)dy,\quad
\overline F_A=\ell^{-1}\int_0^\ell F_A(x)dx,\quad
M_A=\max_x|F_A(x)-\overline F_A|>0,
\]

and choose the public profile

\[
h(x)=\frac{F_A(x)-\overline F_A}{2M_A}.
\]

It has zero mean and `|h|<=1/2`. On cycle `k`, let

\[
H_M(t)=\eta_k h((t-t_k)/\tau) Z_M,
\]

where the signs `eta_k` are independently pre-drawn, independently of every
private controller sign and the initial input. This is a probability
distribution over **fixed** admitted bath trajectories. It is used only
to prove a worst-bath lower bound; it supplies no new controller operation.
Every realization has `||[H_M,sigma_j]||<=1`. It may know the public shape
and clock, and never reacts to the realized private signs. Free bath
evolution over every cycle is exactly the identity because `integral h=0`.

The rapid dependence on `t/tau` is allowed by the first-motion promise.
The higher temporal regularity constants required by the predecessor do
not stay uniformly bounded along this adversary family.

### The exact leading averaged channel

For `j=A,B` put `F_j(x)=integral_0^x f_j`, and define

\[
a_A=2\int_0^\ell F_Ah\,dx
 =\frac{\int_0^\ell(F_A-\overline F_A)^2dx}{M_A}>0,
\qquad
a_B=-2\int_0^\ell F_Bh\,dx.
\]

Let `P_A=X_1Y_M` and `P_B=X_2X_M`. The second unitary Taylor term of the
actual moving-bath cycle is

\[
U_{2,s,\eta}
=-i\eta\tau^2(s_Aa_AP_A+s_Ba_BP_B). \tag{3}
\]

For example, in the bath frame
`sigma_x(t)=X_M-2eta tau(integral_0^x h)Y_M+O(tau^2)`.
Integrating against `f_A` and integrating by parts gives (3). The frozen
quadratic term vanishes by (2); `sigma_z` commutes with the chosen drift.

Average over both controller signs and the independent bath sign. At
degrees one through three all coefficients vanish. A surviving control
sign monomial has count parity 000 or 111, and a surviving drift count is
even. Thus a cubic survivor would be a pure-control term, which vanishes
by (2). The free bath itself returns exactly.

At degree four, the zero-drift terms again vanish by (2). Terms with three
controls and one drift have odd `eta` and vanish. Terms with two controls
and two drifts must contain the same control twice. Their data part is the
identity and their memory Pauli product, containing two identical native
Paulis and two Zs, is also a scalar identity. Hence the mean fourth
unitary coefficient is scalar. Unitarity fixes its Hermitian part to
`-(a_A^2+a_B^2)I/2`. There is no imaginary scalar part: the Hamiltonian is
traceless, so `trace log U=0`, while the lower second-order square has real
trace. This accounts for the whole fourth coefficient.

Writing `S=a_A^2+a_B^2>0`, the combined averaged channel is therefore

\[
\Psi_\tau=\mathrm{Id}+\tau^4\mathcal D+\mathcal R_\tau,
\quad
\mathcal D=a_A^2(\operatorname{Ad}_{P_A}-\mathrm{Id})
           +a_B^2(\operatorname{Ad}_{P_B}-\mathrm{Id}), \tag{4}
\]

with an explicit bound

\[
\|\mathcal R_\tau\|_\diamond
\le K_5\tau^5,
\qquad K_5=\frac{(3\ell)^5}{120}. \tag{5}
\]

Indeed the full instantaneous Hamiltonian has norm at most `3/2`, so its
channel generator has norm at most three. Rescaling to normalized time
makes this an ordinary bounded Dyson series in `tau`. Its fifth-order
integral remainder is bounded by `(3ell tau)^5/5!`, using the norm one of
the full channel in that remainder. No derivatives of the bath are used.

### Loss before the higher-degree signal can accumulate

Let `Q=Z_1Z_2 tensor I_M` and prepare the two orthogonal inputs

\[
\rho_\pm=\frac{I_D\pm Z_1Z_2}{4}\otimes\frac{I_M}{2},
\quad
\Delta=\rho_+-\rho_-=Q/4,
\quad\|\Delta\|_1=2.
\]

Both `P_A` and `P_B` anticommute with `Q`. Hence
`D(Delta)=-2S Delta`. Put `lambda=1-2S tau^4` and take `tau` small enough
that `0<=lambda<=1`. From (4)-(5) and trace-norm contractivity,

\[
\|\Psi_\tau^m(\Delta)\|_1
\le2\lambda^m+2mK_5\tau^5. \tag{6}
\]

Use the random-sign bath for only the first `m` cycles, and zero drift
thereafter. The remaining controller is a joint CPTP map and cannot restore
the lost distinguishability; final bath discard also cannot restore it.
The ideal images of these two data inputs under any data unitary have
trace-norm distance two. Thus any uniform full-program error must satisfy

\[
\epsilon\ge1-\lambda^m-mK_5\tau^5,
\qquad m\le N. \tag{7}
\]

Although (7) is derived using a mixture of predetermined bath trajectories,
the supremum over fixed trajectories is at least its averaged-channel
lower bound. This is just convexity and preserves the private-coin noise
game in the question.

Choose

\[
m=\left\lceil\frac{\log(1/\tau)}{2S\tau^4}\right\rceil.
\]

Then (7) gives the quantitative asymptotic bound

\[
\epsilon\ge
1-\tau-\frac{K_5}{2S}\tau\log(1/\tau)-K_5\tau^5
\longrightarrow1. \tag{8}
\]

The assumed repetition count guarantees `m<=N` eventually. This proves
the theorem. Its conservative remainder constant need not be useful at
moderate `tau`; the asymptotic obstruction is rigorous.

The cubic first-tranche primitive has `N=O(tau^-3)`, so the destructive
`tau^-4` time scale arrives after that gate has finished. There is no
contradiction with the earned positive theorem. A fifth- or ninth-degree
primitive repeated to a finite angle crosses that time scale first.

## 4. An exact inherited-word instance

Use the predecessor's raw word for `L_5=ad_a^2[c,[a,b]]`. With the usual
chronological commutator recursion its length is 46. At unit gains,

\[
W_s(\tau)=I-16i\tau^5F+O(\tau^6)
\]

for all four parity choices. The exact program checks all coefficients
through degree five.

For a rational finite bath, take the piecewise-constant midpoint version
of the profile above: on segment j put

\[
h_j=\frac{F_A(j-1/2)-\text{mean of those midpoints}}
 {2\max_j|F_A(j-1/2)-\text{mean}|}.
\]

The midpoint rule is exact for the integral of `F_A` on a unit segment.
Thus this also has zero mean, `max |h_j|=1/2`, and positive `a_A`. The exact
values computed in `high_order_barrier.py` are

\[
a_A=188/11,\quad a_B=-128/77,\quad S=1748240/5929.
\]

The code verifies the entire combined-mean unitary series through degree
four, including its scalar coefficient `-874120/5929`, using Gaussian
integers after a common rational rescaling. Thus the leading channel noise
is exactly

\[
\tau^4\left\{\frac{35344}{121}(\operatorname{Ad}_{X_1Y_M}-\mathrm{Id})
 +\frac{16384}{5929}(\operatorname{Ad}_{X_2X_M}-\mathrm{Id})\right\}.
\]

This is a failure under an admitted moving bath of an attempted extension
of that word. It does not invalidate its predecessor's stronger qualified
regularity theorem. The earlier native sign projection and polynomial
compensation remain attributed to those supplied originals.

## 5. Exact remaining frontier

The commuting-macro theorem applies to arbitrary scalar-angle policies,
while the higher-degree theorem applies to repetitions of a **fixed**
small-word shape with fresh whole-word parity signs and pure-control
order at least five. These are distinct restrictions. They do not jointly
exhaust the original native interface.

In particular, this work does not exclude epsilon-dependent changing word
shapes, nonperturbative protocols, private waveform randomization beyond
the displayed sign construction, or another invariant mechanism. It does
not prove that every native approximate target operation factors through
the commuting unknown-c library. Establishing such a reduction would be
a genuinely additional all-policy theorem, and has not been done here.

Therefore the full uniform unknown-gain, arbitrary first-motion question
is **not resolved by this tranche**. What is established is a sharp
black-box composition barrier and a quantitative adversarial failure of
the straightforward high-degree extension, with an actual first-motion
noise mechanism rather than an absent remainder estimate alone.
