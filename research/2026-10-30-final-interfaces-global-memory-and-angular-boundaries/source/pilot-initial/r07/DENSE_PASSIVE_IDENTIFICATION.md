# Dense passive identification with clipped finite-level sensors

## Finding and scope

For an unknown linear **contractive scattering system**, thinning experimental
amplitude can replace thinning calendar activity. A fresh signed coordinate
probe in every window, read through a fixed-range 257-level stochastic ADC,
has a finite, relaxation-independent operator certificate. No reset, adjoint,
state estimate, or idle window is required. One operator confidence event also
certifies a family of future regularized inverse tasks selected after acquisition.

The estimator is ordinary instrumental-variable correlation, not a new
optimization algorithm. The result derived here is its explicit finite bound
combining passivity, conditional sign symmetry at a clipping boundary,
low-amplitude excitation, and a finite random-word ADC. External priority for
this combination is unestablished. The equally informed ordinary method is
identical and is executed as such.

This theorem requires a **pathwise scattering energy inequality** in warranted
input/output energy coordinates. That is a real restriction beyond the supplied
P1 account's conditional energy premise. It cannot be transferred silently to
arbitrary force/displacement sensors or a continuously powered bath. P1's
separately attached proof/program files were unavailable and are not claimed as
read or rerun. The present work is a fresh specified family, not a matched
improvement on P1's unavailable numerical fixture.

## Interface

The specimen obeys

\[
 z_{t+1}=Pz_t+Bx_t,\qquad y_t=Cz_t+Ax_t,
\]

where the unknown block operator
\(\mathcal S=\begin{pmatrix}P&B\\C&A\end{pmatrix}\) is a contraction.
The hidden state can be in a real Hilbert space; input/output dimensions are
d and m. The controller knows those dimensions and
\(\|z_1\|^2\le E_0\), but need not know A, P, B, C, internal dimension, or a
spectral gap. Dark invariant coordinates and arbitrarily slow visible modes
are allowed. In particular, \(\|A\|\le1\), and pathwise

\[
 \|z_{t+1}\|^2+\|y_t\|^2\le\|z_t\|^2+\|x_t\|^2. \tag{1}
\]

No continuing energy injection is omitted. Input/output amplitudes must have
an actual calibrated energy normalization.

Fix N divisible by d and put n=N/d. Cycle through coordinate indices j_t,
each n times. Draw a fresh independent Rademacher sign s_t immediately before
each window and drive \(x_t=Us_te_{j_t}\), with \(0<U<M\). Every window is
active and the specimen persists. The old field \(h_t=Cz_t\) is measurable
before the current sign.

The ADC clips each scalar output to [-M,M], then stochastically rounds its
magnitude to the adjacent members of the **uniform** grid
\(0,\Delta,\ldots,M\), where \(\Delta=M/K\), and restores its sign.
There are 2K+1 scalar reports. Each scalar read uses a fresh random word,
conditionally independent of the full pre-read history, current sign, command,
and analogue output. Saturated reports and flags are retained. Fixed sensor
loading is included in the plant; dither must not change its gain or inject
unaccounted specimen energy.

For ideal continuous dither the report mean equals the clipped input. The
executed version instead uses W equally likely centered words
\((r+1/2)/W\). Its round-up probability differs from the ideal probability
by at most \(\epsilon_p=1/(2W)\). The theorem explicitly charges this error.

## Conditional clipping mechanism

A crude first attempt treats clipping as arbitrary additive readout error and
divides it by U, giving a bias of order U. The stronger attack retains fresh
sign symmetry. For one output coordinate let a=(Ae_j)_k, h=(h_t)_k, and let
c_M denote clipping to [-M,M]. Conditional on all history before the sign,

\[
 \mu(h,a)=\frac{c_M(h+Ua)-c_M(h-Ua)}{2U}. \tag{2}
\]

Clipping is monotone and 1-Lipschitz, so mu lies between zero and a. It equals
a if \(|h|\le M-U|a|\). Thus, because \(|a|\le1\),

\[
 |\mu(h,a)-a|
 \le |a|\mathbf1\{|h|>M-U|a|\}
 \le\frac{h^2}{(M-U)^2}. \tag{3}
\]

Only old-field boundary encounters attenuate the incremental response. A large
raw clipping error does not automatically become a large gain bias divided by
U. This is a conditional calculation; marginally unbiased measurement error
would not suffice.

## Energy bounds and finite theorem

Let Q=NU^2 and V=E_0+Q. Telescoping (1) and applying Minkowski to the
concatenated time series h=y-Ax give, pathwise,

\[
 \sum_t\|y_t\|^2\le V,\qquad
 \sum_t\|h_t\|^2\le(\sqrt V+\sqrt Q)^2=:H. \tag{4}
\]

No relaxation time or final-warning time occurs in these bounds.

From the actual ADC reports q_t form

\[
 \widehat A_{:j}=\frac1{nU}\sum_{t:j_t=j}s_tq_t.
\]

For a declared failure probability delta define

\[
 T=V+\Delta(1+2\epsilon_p)\sqrt{mNV}
       +\epsilon_p Nm\Delta^2, \tag{5}
\]

\[
 r_A=\frac{\sqrt{T/\delta}}{nU}
       +\frac{H}{n(M-U)^2}
       +\frac{\sqrt{md}\epsilon_p\Delta}{U}. \tag{6}
\]

Then

\[
 \Pr\{\|\widehat A-A\|_F\le r_A\}\ge1-\delta. \tag{7}
\]

The radius uses only public interface constants. It does not use the true A,
hidden state, fitted dynamics, or population-model audit error. Its confidence
cost is conservative, proportional to delta^{-1/2}; no optimality claim is made.

### Proof

For a nonnegative clipped scalar z in a cell [l,l+Delta], ideal stochastic
rounding has variance
\((z-l)(l+\Delta-z)\le\Delta z\).
The finite centered word changes its second moment by at most
\(\epsilon_p\Delta(2z+\Delta)\). Therefore

\[
 \mathbb E[q_{tk}^2\mid y_t,s_t,\text{pre-read history}]
 \le y_{tk}^2+\Delta(1+2\epsilon_p)|y_{tk}|+\epsilon_p\Delta^2. \tag{8}
\]

Summing and using (4) and Cauchy-Schwarz bounds the total expected report
second moment by T.

Write \(\nu_t=\mathbb E[s_tq_t\mid\mathcal H_t]\), where H_t includes all
history before the current sign, including hidden state for the mathematical
filtration. Then
\(D_t=(s_tq_t-\nu_t)e_{j_t}^{\mathsf T}\) are martingale differences.
Their squared Frobenius moments sum to at most T, because subtracting a
conditional mean reduces a second moment. Orthogonality across times and
Markov's inequality imply, with probability at least 1-delta,

\[
 \left\|\frac1{nU}\sum_tD_t\right\|_F
 \le\frac{\sqrt{T/\delta}}{nU}. \tag{9}
\]

For ideal dither, (3), summed over coordinates, gives
\(\|\nu_t/U-Ae_{j_t}\|_2\le\|h_t\|^2/(M-U)^2\).
Triangle inequality and (4) bound accumulated clipping bias by
H/[n(M-U)^2]. The finite word changes each scalar conditional mean by at most
epsilon_p Delta; averaging in each column adds at most
\(\sqrt{md}\epsilon_p\Delta/U\) in Frobenius norm. Combine these two bias
bounds with (9).

## One acquisition, a family of inverse tasks

Let
\(u(A,b)=(A^{\mathsf T}A+\lambda I)^{-1}A^{\mathsf T}b\), lambda>0.
For arbitrary rectangular A and B,

\[
 \|u(A,b)-u(B,b)\|
 \le\frac{\|b\|}{\lambda}\|A-B\|. \tag{10}
\]

To prove this, define
\(L_A=\begin{pmatrix}\sqrt\lambda I&A^{\mathsf T}\\-A&\sqrt\lambda I\end{pmatrix}\).
Its skew part is skew-adjoint, so \(\|L_A^{-1}\|\le1/\sqrt\lambda\).
The first block of \(L_A^{-1}(0,b)\) is -u(A,b). The resolvent identity,
\(\|L_A-L_B\|=\|A-B\|\), and the same inverse bound prove (10).

On the single event (7), every b with norm at most B therefore has command
error at most Br_A/lambda. This is simultaneous, so b may be selected after
reading the acquired estimate. If the command ball contains radius
\(B/(2\sqrt\lambda)\), both ridge commands are feasible, using
\(\sup_{s\ge0}s/(s^2+\lambda)=1/(2\sqrt\lambda)\).
The acquired guarantee beats this zero-command guarantee simultaneously for
every nonzero b whenever lambda > 4 r_A^2 and the command ball is large enough.
For the executed radius, this covers all lambda greater than about 0.04718;
the theorem is not restricted to the one displayed target vector.

This concerns the **fixed incremental response** A. It does not certify raw
future warm output, remove old fields, or prepare a microscopic state. Receiving
experiments still need their own physical accounting.

## Rates and precision obligations

For ideal conditional-mean sensing, fixed d,m,E_0,M,Delta,delta, and the
finite-horizon choice U=c N^{-1/5}, (6) gives

\[
 r_A=O(N^{-2/5}),\qquad Q=O(N^{3/5}). \tag{11}
\]

The ADC contribution is order (NU)^{-1/2}, while clipping contributes order
U^2; their balance gives (11). This is a family of finite-horizon designs,
not an unproved anytime protocol.

With a **fixed finite random word**, the final term in (6) instead grows as
1/U. Unlimited convergence at fixed dither and calibration precision is not
established. One sufficient asymptotic choice is W=Omega(N^{3/5}), costing
O(log N) random bits per scalar read. The executed finite horizon uses W=65536
and charges its bias directly.

If actual conditional sensor means differ from the specified means by at most
eta_ADC per scalar, add sqrt(md) eta_ADC/U to r_A **provided the second-moment
bound (8) remains warranted**; otherwise also replace T by a warranted report
second-moment total. A mean contract alone cannot imply the low-amplitude
variance bound: symmetric reports of +/-M can have mean zero at zero input and
still have variance M^2. If each actual command
differs from its specified signed vector by norm at most eta_x, add
sqrt(d) eta_x/U and use a warranted bound on total actual input energy in
place of Q. Clipping is 1-Lipschitz, so the direct command error has this
bound; its subsequent state effects are already covered by actual input energy.
Fixed calibration errors impose a genuine accuracy limit.

Known independent zero-mean noise added after quantization can be charged in
T. Noise entering before clipping requires its own boundary-encounter energy
accounting as well; it cannot simply be added to T. An unknown mean error or
unknown continuous energy supply cannot be treated as free passive stored
energy. Apparatus power, time per window, heat, and detector work remain
unmeasured. No hardware calibration is established by the simulation.

## Earlier logarithmic representation: substantive failed attack

The first sensor attack was a logarithmic ladder spanning the maximum allowed
output amplitude. Rounding log(y) and decoding is biased: levels 1 and 4 with
y=2 give round-up probability 1/2 in log coordinates, hence decoded expectation
2.5. Repetition leaves the 0.5 bias. Correct amplitude-coordinate stochastic
rounding uses probability 1/3 and mean 2.

The repair is established technology, not a new discovery: NUQSGD treats
unbiased nonuniform ladders, and LUQ combines logarithmic levels with unbiased
amplitude rounding. A geometric ladder also buys range accuracy with small
absolute threshold gaps and associated threshold-control precision. Its finite
symbol count cannot be called free low-precision sensing. That resource failure
motivated the fixed uniform ADC and amplitude reduction above, which exposes
its own actuator and dither calibration costs explicitly.

## Executed result

`check_dense_passive_identification.py` chooses U by minimizing (6) from public
constants before generating any plant. It runs 256 synthetic specimens, each
for 65536 consecutive active windows. Each is a cascade of lossless scattering
cavities with orthogonal channel mixing, plus a permanently dark coordinate
holding nine energy units. Visible relaxation scales span roughly 10^2 to
10^12 windows; none is supplied to the controller. Initial total energy is 16.

The fixed ADC range is [-1,1], its 257 levels are uniformly spaced by 1/128,
and every scalar read uses a fresh centered 16-bit dither word. All saturated
reads are retained. The known task constants are B=.4, lambda=.5, command
radius .7, and failure probability .01. The receiving target is the dominant
left singular vector of the acquired operator estimate, scaled to norm .4;
it therefore depends on the acquired record.

| Quantity, per specimen | Executed value |
|---|---:|
| Physical and active windows | 65536 |
| Idle windows / resets / adjoint operations | 0 / 0 / 0 |
| Vector reads / scalar reads | 65536 / 131072 |
| Probe amplitude | 0.03638863513 |
| Incident energy | 86.77836499 normalized units |
| Scalar ADC report width | 9 fixed bits for 257 symbols |
| ADC random bits | 2097152 |
| Certified operator radius | 0.1085955872 |
| Certified inverse-task radius | 0.08687646979 |
| Zero-experiment task radius | 0.2828427125 |

Operator radius components were 0.09615462 (martingale noise), 0.01243769
(clipping), and 0.000003276 (finite-word bias). Across 256 runs, median/max
audited operator errors were 0.005950/0.015538; median/max inverse-task errors
were 0.001074/0.006833. These audited errors are not controller information.
There were no certificate violations in this finite test, which is not a proof
of coverage. Each run had 0 to 3 saturated scalar reads, all retained.

The largest numerical single-window energy-balance residual was 5.43e-15;
the incremental-response identity residual was 8.89e-16. The code also checks
the pathwise total-energy and old-field bounds and the actual conditional
clipping attenuation. The dark energy remains exactly nine.

The equally informed conventional forward-only instrumental-variable method
uses precisely the same sufficient statistic, signs, ADC reports, and low
amplitudes. The executable checks exact equality. Thus no algorithmic advantage
over the strongest ordinary method containing this construction is claimed.
Full signed-read correlation is also executed as a stronger sensing benchmark;
its median operator error is 0.005942. More structured identification could
exploit additional system knowledge, which this theorem does not assume.

These are normalized specimen-energy costs, not joules or total apparatus work.
The all-task guarantee is for regularized commands, not physical delivery of
all receiving outputs. The finite test supports the implementation at its
stated scope; the new derivation has not received an independent audit.

## Sources and remaining central obligation

The supplied FACTS.txt, P1_RECOVERY_FINAL_VISIBLE_DOM.txt, and
P1_RECOVERY_VISIBLE_ACTIVITY.txt govern the inherited theorem, failed bounded
comparison, and review scope. The unattached governing programs were not read.

The direct physical-adjoint predecessor is Aarnoudse and Oomen, *Model-Free
Learning for Massive MIMO Systems: Stochastic Approximation Adjoint Iterative
Learning Control*, IEEE Control Systems Letters (2021),
[TU/e primary PDF](https://pure.tue.nl/ws/files/193833656/Model_Free_Learning_for_Massive_MIMO_Systems_Stochastic_Approximation_Adjoint_Iterative_Learning_Control.pdf).
It already provides randomized model-free physical-adjoint learning; that
capability is not a new claim here.

Quantization precedents read were Ramezani-Kebrya et al.,
[*NUQSGD*](https://arxiv.org/html/1908.06077v2), Definition 3 and its variance
calculation, and Chmiel et al.,
[*Accurate Neural Training with 4-bit Matrix Multiplications at Standard
Formats*](https://arxiv.org/html/2112.10769v4), section 4 on LUQ. Neither
logarithmic levels nor unbiased stochastic rounding is claimed as new.

The unresolved physical obligation is an affordable, warranted scattering
energy normalization plus amplitude-compatible actuator and conditional ADC
calibration. Unknown relaxation alone need not force idle calendar windows in
the stated class. A new foundational capability, practical hardware advantage,
and external novelty remain unestablished.
