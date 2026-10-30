# Unknown gains: a finite partial construction and a scalar-control barrier

All channel norms are full diamond norms. The physical model is exactly
`packet/CONTROL_TASK.md` with the modification in
`checkpoints/p01/CONTROL_NEXT_SCOPE.md`: static unknown gains
`g_A,g_B,g_C in [1,2]`, no calibration, and only first local motion. Write

\[
F=Z_1X_2,\qquad c=g_Ag_Bg_C\in[1,8].
\]

This document does **not** resolve arbitrary-accuracy reachability for all
native randomized programs. It establishes a constructive uniform error
below 0.84, and an accuracy obstruction for a precisely defined restricted
class that includes arbitrary compositions and classical mixtures of the
completed weak-cycle primitives. The obstruction is not asserted for every
native program.

## 1. Target and representation

The target is the same fixed channel `Ad_exp(-i*pi*F/4)` on data/reference,
after averaging private coins and discarding the retained memory. Neither
the target angle nor the output contract is weakened below.

The checkpoint retains one coherent clean generator, `c F`. Completing such
an operation before starting another one protects arbitrary retained-memory
inputs. It loses the coherent intermediate memory interactions needed by
the older polynomial gain-compensation compiler. Treating a completed
operation's bath factor as an inverse-able native coupling would be invalid.

The new organizing object is a probability law of accumulated logical
angles. It retains the full averaged channel, and therefore the
positive-definiteness constraints between responses at different gains.
This yields both a real constructive consequence and a real restriction.

## 2. A uniform unknown-angle primitive, including resources

For every prescribed `alpha >= 0` and accuracy `s > 0`, the checkpoint's
ten-segment cycle still implements a uniformly accurate unknown-angle
rotation `exp(-i alpha c F)`. It does not need to know `c`.

For completeness, the gain-dependent constants can be bounded directly.
Use the checkpoint's chronological ten-segment word, with fresh fair
`s_A,s_B` and `s_C=s_A*s_B`, every segment of duration `delta`. Let
`0 < delta <= 1/20`. Work in the exact bath interaction frame, so
`S_j(t)=V(t)^dagger sigma_j V(t)` has norm one and Lipschitz constant one.
Native norms are now at most two. The cycle's frozen third-order term is
`-4i c delta^3 F`.

The same-label second-order term is `I_D tensor Q`, with

\[
Q+Q^\dagger=-\sum_j g_j^2G_j^2,\quad
G_j=\int f_j(t)S_j(t)\,dt,\quad K=(Q-Q^\dagger)/2.
\]

The original moment bounds give

\[
\|Q-K\|\le466\delta^4,\qquad
\|K\|\le\frac{2000}{3}\delta^3.
\]

The fourth-order Dyson tail, using total integrated control norm at most
`20 delta`, is at most

\[
e(20\delta)^4/24<18123\delta^4.
\]

Only ABC third-order sign characters survive. Their moving-versus-frozen
error is at most `8*(10 delta)^4/8=10000 delta^4`.
For

\[
X=I_D\otimes K-4ic\delta^3F,\quad V=e^X,
\]

we have `||X||<699 delta^3`, and
`||exp(X)-I-X||<668 delta^4`. Thus

\[
\|\mathbb E U_s-V\|<29257\delta^4.
\]

For each sign realization, midpoint Duhamel freezing costs at most
`50 delta^2`; adding the frozen cubic term, tail, and `V-I` gives

\[
\|U_s-V\|<132\delta^2.
\]

The exact channel expansion around `V`, rather than averaging only
unitaries, consequently gives

\[
\boxed{\quad
\|\mathbb E_s\operatorname{Ad}_{U_s}
-\operatorname{Ad}_{e^{-4ic\delta^3F}\otimes e^K}\|_\diamond
\le C\delta^4,\qquad C=100000.
\quad}                                                    \tag{1}
\]

Indeed `2*29257+132^2=75938 < C`. No drift norm, higher derivative,
spectator dimension, or initial-state assumption enters these estimates.

With fresh signs in `N` cycles, the fixed coin-independent bath permits
channel telescoping, including arbitrary retained correlations. The bath
factors need not commute with one another. After discarding memory,

\[
\|\Phi_{N,\delta,c}-\operatorname{Ad}_{e^{-4iNc\delta^3F}}\|_\diamond
\le CN\delta^4.                                         \tag{2}
\]

For general `alpha`, choose a dyadic `delta <= min(1/20,
s/[C(alpha+1)])`, and take the nearest integer to `alpha/(4 delta^3)`.
The angle rounding costs at most `32 delta^3` in full diamond norm because
`c<=8`; (2) and rounding have total below `s/2`. There are `m=10N`
segments and duration `m delta`. The generous bound

\[
\eta\le s/(8m^2)                                        \tag{3}
\]

on every independent segment duration error costs at most `s/2` more.
To see this without comparing bath propagators, extend schedules by idle
drift to a common end time and compare their interaction-frame controls.
The difference between adjacent native Hamiltonians has norm at most four;
the integrated difference is at most `2m^2 eta`. Unitary-channel conversion
costs at most `4m^2 eta`.

For fixed `alpha`, duration is `O(s^-2)`, native segment count `O(s^-3)`,
and absolute timing precision `O(log(1/s))` bits. Two new fair private bits
per cycle suffice. This is an unknown-angle primitive, not gain compensation.

## 3. The exact retained object is a characteristic function

Define the **completed scalar class** as controllers with the following
comparison property. Conditional on some classical private variable `r`,
their returned-data channel is within `nu_r` of

\[
\operatorname{Ad}_{e^{-ic\Theta_r F}}\circ\operatorname{Tr}_M,
\]

where the law of the real number `Theta_r` is fixed by the program and
independent of the gains. Let `nu=E nu_r` uniformly on the gain box.
Arbitrary finite compositions, reversals of gate orientation, idles,
branch lengths, and classical mixtures of completed primitives satisfy
this definition with their errors added. It does not include arbitrary
interleavings with bare native couplings or unfinished memory interactions.

Let `P_+,P_-` be the two eigenspace projections of `F`. The exact scalar
mixture fixes the diagonal blocks of a data operator and multiplies
`P_+ rho P_-` by

\[
z(c)=\mathbb E e^{-2ic\Theta}.
\]

The target multiplies that block by `-i`. Exactly,

\[
\left\|\mathbb E\operatorname{Ad}_{e^{-ic\Theta F}}
-\operatorname{Ad}_{e^{-i\pi F/4}}\right\|_\diamond
=|z(c)+i|.                                               \tag{4}
\]

For the upper bound, the difference map is `|z+i|` times a unitary
conjugation of the off-diagonal projection
`(Id-Ad_F)/2`, whose diamond norm is one. A pure equal superposition of a
plus and a minus eigenvector attains that norm. Reference systems and
eigenspace degeneracy do not change the equality.

## 4. A quantitative obstruction for every scalar law

Suppose `sup_{1<=c<=8}|z(c)+i| <= d`. Let `z_k=z(k)`, `k=1,...,8`.
The nine-by-nine moment matrix

\[
T_{jk}=\mathbb E e^{-2i(j-k)\Theta},\qquad 0\le j,k\le8,
\]

is positive semidefinite: it is the average of the outer product of
`(1,e^{-2iTheta},...,e^{-16iTheta})` with its adjoint. Its diagonal is one.
If every desired moment equaled `-i`, its comparison matrix would be

\[
(T_*)_{jk}=\begin{cases}
1&j=k,\\ -i&j>k,\\ i&j<k.
\end{cases}
\]

For general size `n`, the vector `v_j=exp(i*j*pi/n)` is an eigenvector of
`T_*-I` with eigenvalue `-cot(pi/(2n))`. This follows by summing the two
finite geometric series, or subtracting neighboring eigenvalue equations.
For `n=9` this produces the negative eigenvalue
`1-cot(pi/18)`. Every off-diagonal entry of `T-T_*` is at most `d` in
absolute value; the Hermitian row-sum bound gives
`||T-T_*|| <= 8d`. Positivity therefore requires

\[
\boxed{\quad d\ge\beta:=\frac{\cot(\pi/18)-1}{8}
\simeq0.58391.\quad}                                    \tag{5}
\]

Every `c in [1,8]` used here is realized by an allowed gain triple, for
example `g_A=g_B=g_C=c^(1/3)`. Combining (4), (5), and the comparison
error proves that the worst-case error of any completed scalar controller
is at least `beta-nu`. In particular, making the native implementation
error tend to zero cannot turn arbitrary mixtures of these completed
rotations into an arbitrary-accuracy gain-independent entangler.

This applies to arbitrary probability laws, not merely a chosen finite
ansatz or a numerical search. It is a restricted representation barrier,
not a lower bound on all admitted native randomized policies.

## 5. A constructive consequence: a legal program with error below 0.84

The same object gives a nontrivial uniform positive guarantee. First take
an ideal exponentially distributed angle `Theta`, with mean `a=3/8`.
Its characteristic function is

\[
z_\infty(c)=\frac1{1+2iac}.
\]

Put `x=2ac=3c/4`. Then

\[
|z_\infty(c)+i|^2
=\frac{x^2-2x+2}{1+x^2}.
\]

The derivative has the sign of `x^2-x-1`, so the maximum on
`x in [3/4,6]` occurs at an endpoint. The two squared errors are `17/25`
and `26/37`, giving the uniform bound

\[
d_\infty=\sqrt{26/37}\simeq0.838274.                     \tag{6}
\]

This continuous law is now replaced by an exactly finite private-coin
program. Set

\[
M=8192=2^{13},\quad r=1-1/M,\quad
\Delta=3/(8M)=3/65536,\quad K=16M=131072.
\]

Count failures before the first success in independent trials of success
probability `1/M`, stopping at `K` failures. A trial reads thirteen fresh
fair bits and succeeds exactly when they are all zero. Let the capped count
be `G_K`, and set `Theta=Delta G_K`. It consumes at most `13K=1703936`
fair bits and produces a finite angle list `0,Delta,...,6` with an exactly
specified dyadic probability law.

Here is a uniform analytic discretization bound. For an uncapped geometric
`G`, couple it to `E~Exp(1)` by
`G=floor(E/b)`, where `b=-log r >= 1/M`. Thus
`Delta G <= a E` pointwise and

\[
\mathbb E(aE-\Delta G)=a-\Delta(M-1)=\Delta.
\]

Since `c<=8`, the characteristic-function change is at most
`16 Delta=6/M`. Capping changes it by at most
`2 Pr(G>=K)=2r^K <= 2e^-16`. Consequently

\[
\sup_{c\in[1,8]}|z_{K}(c)+i|
\le \sqrt{26/37}+6/8192+2e^{-16}.
                                                               \tag{7}
\]

Finally implement the sampled angle with Section 2, using the *same*
`q=2^30`, `delta=1/q` for every branch. For `G_K=k`, choose

\[
N_k=3k\,2^{72}.
\]

There is no rounding: `4N_k/q^3=3k/65536=Theta`. With
`s=1/2048`, the largest ideal implementation error is
`150000/2^30 < s/2`. Allow independent duration errors
`eta=s/(8m_max^2)`. Combining (2), (3), and (7) gives

\[
\boxed{\quad
\|\Phi-\operatorname{Ad}_{e^{-i\pi F/4}}\circ\operatorname{Tr}_M
\|_\diamond
\le \sqrt{26/37}+6/8192+2e^{-16}+1/2048
<0.84.
\quad}                                                     \tag{8}
\]

The last inequality has ample room for the displayed strict primitive bound.
It is uniform in all admitted moving baths, spectators, and initial DMR
correlations. The bath is never initialized, measured, reversed, or reset.
The angle-sampling coins and cycle signs are all private and independent
of the fixed bath. Appending a bath-only idle gives the same ideal finish
time on every angle branch if desired.

The explicit worst-case resources are

\[
N_{max}=3\,2^{89},\quad
m_{max}=15\,2^{90},\quad
T_{max}=15\,2^{60}.
\]

There are at most `m_max-1` changes between native segments, plus a final
turn-off/idle. At most `2N_max+1703936` fair bits are used. Pulse strengths
are exactly plus/minus one, and specified segment durations are `2^-30`.
The tolerance `eta=1/(225*2^194)` is met by 202 absolute binary places.
The actual active duration increases by at most `m_max eta`. These enormous
costs establish existence at the stated partial accuracy, with no practical
advantage claim.

More generally, choosing larger `M`, a larger geometric cap, and finer native
cycles gives error at most `sqrt(26/37)+zeta` for every `zeta>0`, by a finite
program of the same form.

## 6. A direct test of the tempting higher-order extension

Why does the older high-order polynomial construction not automatically
repair the gap? Even the original cycle has a genuine order-four channel
noise term under an entirely smooth, admitted bath. Set all gains to one
and take `H_M=sigma_y/2`, with no spectator. It satisfies the local motion
bound. At the start of a cycle,

\[
S_x'(0)=\sigma_z,\qquad S_y'(0)=0,\qquad S_z'(0)=-\sigma_x.
\]

The signed first time moments of the A, B, C pulses are respectively
`5 delta^2, 4 delta^2, 4 delta^2`. Their sign-dependent first Dyson term in
the interaction frame is therefore

\[
-i\delta^2\bigl(5s_A X_1\sigma_z-4s_CY_1\sigma_x\bigr)
+O(\delta^3).
\]

Both random coefficients have zero mean and zero covariance. With initial
memory `I/2`, the returned-data channel's entanglement fidelity with the
third-order target is

\[
F_e=1-(25+16)\delta^4+O(\delta^5)
=1-41\delta^4+O(\delta^5).                               \tag{9}
\]

The data Pauli errors are traceless, so their squared coefficients give
this leading loss. Coherent third-/fourth-order terms do not change that
leading infidelity. The exact rational expansion in `check.py` independently
checks the coefficient, including the actual physical forward bath drift.
Thus a claimed uniform `o(delta^4)` channel remainder for this unchanged
cycle is false, even for a constant qubit bath. Merely canceling its cubic
mean term to expose a fifth or ninth degree signal does not erase this
positive channel variance. This calculation is not a no-go for redesigned
native words, multiple scales, or coherent intermediate memory objects.

## 7. Remaining scientific question

The requested `epsilon`-arbitrary theorem for *all* allowed native programs
remains unproved here. Sections 4 and 6 specify what a successful next
construction must escape: either retain a coherent object beyond completed
scalar rotations, or suppress/organize its moving-bath variance while
generating nonlinear gain response. The stronger temporal regularity used
by the older flat polynomial compiler has not been reintroduced. The source
supplement already contains sign projection and polynomial gain compensation;
no claim of inventing either is made.
