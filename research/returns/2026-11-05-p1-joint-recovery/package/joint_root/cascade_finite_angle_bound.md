# An explicit finite-angle lift of the matched-cascade limit

5 November 2026. This is a uniform finite-dimensional estimate for the specified
physical matched cascade, not an unrestricted optimal receiver law. It replaces
the previously unspecified fixed-width remainder constants by explicit ones.

## Statement

There are n=k+1 spins: inaccessible source first, followed by k retained receiver
qubits. The carrier meets them in order at the same angle theta and is discarded.
Let T=T_{n,theta} be the resulting source-plus-memory channel. Let P be collective
SU(2) twirling and let

\[
G(X)=-\frac1{32}\sum_{a=1}^3[Y_a,[Y_a,X]]+\frac i8[C_n,X],
\]

as proved in `joint_channel/slow_generator_derivation.md`. Put d=2^n and

\[
R_p(n,\theta)=e^{2n\theta}\frac{(2n\theta)^p}{p!},\qquad
\Gamma_n=\frac38 n^2(n-1)^2+\frac14n(n-1)(n-2),
\]

\[
\eta_n(\theta)=1-\theta^2+R_3(n,\theta),\qquad
E_n(\theta)=R_5(n,\theta)+\frac{\theta^8\Gamma_n^2}{2}e^{\theta^4\Gamma_n}.
\]

Here \Gamma_n is an explicit upper bound on the generator's diamond norm.
Assume 0<theta<=1,

\[
\theta^2\left(1+\frac{n(n+1)}2\right)\le2,\qquad \eta_n(\theta)<1.
\]

Then for every integer N>=1,

\[
\boxed{\frac12\|T^N-e^{N\theta^4G}P\|_\diamond
\le\frac12\left[N E_n(\theta)+2^n\eta_n(\theta)^N\right].}
\tag{1}
\]

The upper bound can always be replaced by its minimum with 1. For comparison
with a chosen slow time t, add

\[
\frac12\Gamma_n|t-N\theta^4|
\tag{2}
\]

to the right side. These bounds hold after arbitrary receiver initialization,
tracing the actual source, and applying any physical final decoder, including
with an inaccessible logical reference. They are conservative: the sufficient
small-angle regime from eta<1 scales at worst as theta=O(n^{-3}); the scalar
error at fixed t has leading bound O(t n^5 theta). Neither is asserted sharp.

## Proof

Each conjugation by exp(i theta SWAP) is exp(theta A_j), where A_j is a
commutator superoperator of diamond and Hilbert--Schmidt operator norms at most
2. The chronological product of n such maps has Taylor coefficients bounded
in either norm by (2n)^r/r!, by the multinomial theorem. Injection of I_E/2 and
partial trace are contractions in diamond norm. In Hilbert--Schmidt norm their
norms are respectively 1/sqrt(2) and sqrt(2), which cancel. Thus a remainder
starting at degree p is bounded by R_p(n,theta) in the relevant norm.

On the invariant algebra the exact first through third coefficients vanish and
the fourth coefficient is G. Composing on the right with P therefore gives

\[
\|(T-I-\theta^4G)P\|_\diamond\le R_5(n,\theta).
\]

For each component, ||Y_a||<=n(n-1): each ordered-pair cross product has norm
at most 2. Also ||C_n||<=6 binom(n,3)=n(n-1)(n-2). The commutator and
double-commutator estimates give ||G||_diamond<=\Gamma_n. Consequently

\[
\|(e^{\theta^4G}-I-\theta^4G)P\|_\diamond
\le\tfrac12\theta^8\Gamma_n^2e^{\theta^4\Gamma_n}.
\]

Both T and exp(theta^4 G) are CPTP, preserve the invariant algebra, and commute
with P. A telescoping sum gives

\[
\|(T^N-e^{N\theta^4G})P\|_\diamond\le N E_n(\theta).
\]

On the complementary operator-spin sectors, the full second-order Taylor
coefficient of T is -D, where

\[
D=\frac18\sum_a\operatorname{ad}(J_a)^2.
\]

It has eigenvalues l(l+1)/2 for l=1,...,n, independent of multiplicities.
The angle condition ensures ||I-theta^2 D|| on this complement is at most
1-theta^2. The third-order remainder yields
||T(I-P)||_{2->2}<=eta_n(theta). Exact SU(2) covariance makes the complement
invariant, hence ||T^N(I-P)||_{2->2}<=eta_n(theta)^N. For a map on d-dimensional
matrices, ||Lambda||_diamond<=d||Lambda||_{2->2}; this follows by stabilization
with a d-dimensional ancilla and the Schatten-norm inequality on dimension
d^2. Therefore ||T^N(I-P)||_diamond<=2^n eta_n(theta)^N. Combining the two
sectors proves (1). Finally the CPTP semigroup contraction and integration of
its generator give ||exp(tG)-exp(uG)||_diamond<=\Gamma_n|t-u|, proving (2).

## Physical resources and finite control

The operation uses k retained qubits and one incoming carrier, kN two-qubit
partial-SWAP encounters, plus the stated initialization and final decoder.
A generic entangled state and decoder on k qubits have exponential-in-k
synthesis costs; the theorem does not remove those costs. With one carrier at
a time and a per-gate service duration tau_g, each encounter requires at least
k tau_g before discard in this implementation. An arrival interval Delta below
the achieved service time requires additional coherent buffering or parallel
resources, all counted. The retained register is protected over the entire
actual acquisition time N Delta and any additional waiting/readout time.

If G_phys elementary gates (including preparation and readout) are implemented
with individual half-diamond error at most zeta, their worst-case added error
is at most G_phys zeta. Thus a claimed error margin delta_control requires
zeta<=delta_control/G_phys. For an angle error |dtheta| in a partial SWAP the
half-diamond gate error is at most |dtheta|, so |dtheta|<=delta_control/(kN)
is a sufficient worst-case uniform receiver-angle precision budget. This is
an explicit control requirement, not an assumed noise-protection cost model.
Without a hardware noise model, no universal number of physical error-correcting
qubits or joules can be inferred from an ideal CPTP gate count.

The separately saved k=9 frame/readout has numerically replayed limiting Bell
fidelity 0.510258885281022, with a margin above 1/2 much larger than the measured
numerical residuals. The matrices and exact positive-part/marginal-normalization
prescription define a physical decoder. The floating-point replay is **not** an
interval-certified fidelity proof. Equation (1) supplies the analytic angle
quantifiers for any separately certified limiting fidelity; it does not turn an
uncertified numerical value into a theorem or provide high-accuracy scaling.
