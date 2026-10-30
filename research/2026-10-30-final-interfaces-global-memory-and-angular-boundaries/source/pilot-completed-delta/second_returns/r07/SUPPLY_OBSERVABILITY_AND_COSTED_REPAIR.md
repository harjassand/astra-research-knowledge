# Supply-driven saturation: a sharp obstruction and a costed range repair

## What this continuation establishes

The first tranche showed that low-amplitude dense probing can replace waiting
for a finite-energy contractive passive specimen. Its essential limitation was
the absence of a replenished energy source. The natural extension fails for an
information-theoretic reason, not just because its energy bound is loose.

There are two explicitly given reciprocal, lossless passive devices, with
opposite optimal commands, whose fixed-range ADC transcripts are identical
under **every** adaptive bounded forward/adjoint experiment. A known,
zero-mean, finite-power external input replenishes the background. Returning
zero is exactly minimax optimal on this pair, attaining the first tranche's
zero-experiment radius. Arbitrarily many experiments and all digital processing
do not help within the stated operation set.

There is also a finite-energy version entirely inside the original no-supply
class: a preloaded delay reservoir hides the gain for T windows whenever its
initial energy can pay for those T masked outputs. This supplies an explicit
energy-versus-deadline lower bound with actual indistinguishable instances.

A calibrated attenuation operation **before** clipping breaks the obstruction.
A second theorem gives a finite-horizon, finite-word certificate for an unknown
contractive specimen with a warranted total external-supply budget. Its range,
lost signal, supply energy, finite-word bias and calibration sensitivity are
explicit. This is a sufficient construction, not an optimal algorithm. On the
known two-device family, an ordinary consistency decoder with an appropriate
gain identifies the member in one read. No general or practical advantage over
equally informed ordinary methods is claimed.

The first tranche's files remain unchanged. This continuation uses only those
retained local results and new local mathematics/computation. No new external
source or partner result is used.

## 1. Why amplitude reduction cannot remove a replenished background

Extend the passive input/output energy inequality to an uncontrolled port w_t:

\[
 \|z_{t+1}\|^2+\|y_t\|^2
 \le\|z_t\|^2+\|x_t\|^2+\|w_t\|^2. \tag{1}
\]

Assume a warranted pathwise supply budget \(\sum_t\|w_t\|^2\le J_N\).
For fresh coordinate probes of amplitude U, let Q=NU^2 and V=E_0+Q+J_N.
The first proof's old-field estimate becomes

\[
 \sum_t\|h_t\|^2\le(\sqrt V+\sqrt Q)^2. \tag{2}
\]

If J_N=NP with P>0, its clipping-bias term does not vanish as U approaches
zero. At fixed large N, its limiting scale is dP/M^2. Merely adding bath power
to a variance term while retaining a vanishing clipping term is invalid.
The following physical pair shows that this is a real observability failure.

## 2. Explicit indistinguishable physical instances

Take 0<lambda<1, b>0 and a command bound R at least
\(r=b/(2\sqrt\lambda)\). Let

\[
 a_\pm=\pm\sqrt\lambda,\qquad c=\sqrt{1-\lambda},\qquad
 S_\pm=\begin{pmatrix}a_\pm&c\\c&-a_\pm\end{pmatrix}. \tag{3}
\]

Each S is real, symmetric and orthogonal. It is a reciprocal lossless two-port
scattering device; its adjoint is the same physical operation. The controlled
input is x_t at the first port. The second input is
\(w_t=W_bv_t\), with v_t independent equiprobable signs drawn before the current
controlled-input randomization. The controller does not control this port.
Its law, amplitude and even its realized sign may be revealed without changing
the obstruction. It has zero mean and exact energy W_b^2 in every window.

The first output, available to the controller only through the ADC, is

\[
 y_t=a_\pm x_t+cW_bv_t. \tag{4}
\]

The other output \(cx_t-a_\pm W_bv_t\) is inaccessible and exports the remaining
energy. It is not ignored in the physical energy balance. One may append a
dark coordinate z'=z carrying nine energy units forever; the same specimen
then retains genuine persistent hidden memory without affecting the example.

The allowed measurement operation clips to [-M,M] and then applies the first
tranche's finite uniform stochastic ADC. If

\[
 cW_b\ge M+\sqrt\lambda R, \tag{5}
\]

then for every permitted x in [-R,R], the clipped report is exactly M v_t in
both instances. Subsequent rounding is deterministic at the rail. Thus every
transcript is independent of the choice of a_+ or a_-.

Condition (5) follows if

\[
 P=W_b^2\ge\frac{(M+\sqrt\lambda R)^2}{1-\lambda}. \tag{6}
\]

This is the threshold for both analogue branches to lie beyond the hard rails
in this construction, not a claimed universal threshold for identifiability.
For bounded analogue dither before clipping, enlarge M in (5) by its maximum
amplitude. The numerical example also has more than one ADC step of margin.

### The operation set is material

The conclusion permits arbitrary adaptive bounded commands, forward or adjoint
queries, zero-input waiting windows, fresh signs, the specified fresh dither,
unlimited digital computation, and knowledge of the complete two-instance
family and supply law. In the SISO case forward and adjoint are the same gain.
Couple the two instances with the same supply signs and controller random seed.
Induction on the transcript gives identical commands and reports forever.

The operation set excludes pre-ADC analogue subtraction, analogue lock-in
integration, programmable measurement gain/offset, access to the second port,
and commands beyond R. These are genuine ways to change the information, not
counterexamples within the stated operation set. The claim is not a theorem
about an equilibrium Gaussian thermal bath: the continuing input here is an
explicit bounded binary-phase source. It does establish failure for the broader
class that admits such a zero-mean source, even when its statistics are known.

## 3. Sharp minimax consequence

The desired fixed incremental-response task is

\[
 F_\pm(u)=\tfrac12(a_\pm u-b)^2+\tfrac\lambda2u^2.
\]

Its optima are

\[
 u_\pm^*=\frac{a_\pm b}{a_\pm^2+\lambda}=\pm r,
 \qquad r=\frac b{2\sqrt\lambda}. \tag{7}
\]

Any terminating policy sees the same transcript distribution under the pair,
so it returns a common random variable Uhat. Therefore

\[
 \frac12\mathbb E[(\widehat U-r)^2+(\widehat U+r)^2]
   =\mathbb E[\widehat U^2]+r^2\ge r^2. \tag{8}
\]

At least one instance has expected squared command error at least r^2.
Returning zero attains exactly r^2 on both. Its worst absolute error is also
exactly r. For epsilon<r the two success intervals are disjoint, so the sum of
the two success probabilities is at most one. No policy always returning a
radius below r can have uniform confidence greater than 1/2. More experiments
cannot establish a 99% radius below r.

Since \(F_\pm(u)-F_\pm(u_\pm^*)=\lambda(u-u_\pm^*)^2\), minimax expected
excess objective is exactly b^2/4, again attained by zero. This is an exact
ordinary-comparator boundary, not a failed learning run being promoted to a
general impossibility claim.

### Executed constants

M=1, R=.7, lambda=.5, b=.4, W_b=2.2 give

\[
 a_\pm=\pm0.70710678,\quad cW_b=1.55563492,\quad P=4.84.
\]

The minimum rail margin is 0.06066017, exceeding the ADC spacing 1/128.
The hard-rail power threshold in (6) is 4.46989899. The optimal commands are
+/-0.2828427125, minimax squared command error is .08, and minimax expected
excess objective is .04. The universal zero-experiment radius from the first
tranche is sharp on these physical instances.

## 4. Finite stored energy already implies a deadline lower bound

Replace the continuing supply by a finite reservoir state z in R^T. Let

\[
 z'=(z_2,\ldots,z_T,0),\quad
 y=a_\pm x+cz_1,\quad p=cx-a_\pm z_1. \tag{9}
\]

Here p is an inaccessible exported wave, not a free disappearance of energy.
For every z,x, not merely the chosen initial state,

\[
 \|z'\|^2+y^2+p^2=\|z\|^2+x^2. \tag{10}
\]

Thus the measured state/input-to-state/output colligation is contractive.
It is a shift-delay wave reservoir feeding the same lossless coupling. There
is no input-to-state injection in this realization; unused controlled and
reservoir energy leaves at the accounted export port. Its incremental scalar
response remains a_+ or a_- in every window, and each scalar adjoint is the
same scalar operation.

Initialize each component of z to W_b v_j, with arbitrary signs chosen before
the controller's future randomization. Its initial energy is E_0=TW_b^2. Until
the reservoir empties, condition (5) gives the same ADC report M v_j under
both gain signs, for **every** bounded adaptive command policy. Therefore
no policy terminating by window T can beat radius r with uniform confidence
greater than one half, despite there being no continuing supply.

For any integer T and E_0 at least
\(T(M+\sqrt\lambda R)^2/(1-\lambda)\), such a pair exists. This is a
sufficient adversarial construction and a worst-case deadline lower bound,
not a universal necessary energy threshold for all devices. It explicitly
charges T state coordinates and their preparation energy; it does not assert
that a large preloaded specimen is easy or free to construct.

`check_finite_reservoir.py` executes T=4096, W_b=2.2, using initial energy
19824.64 and zero continuing-supply energy. An adaptive bounded input policy
produces exactly identical prefixes; the first different ADC reports occur
at window 4097 after the reservoir is empty. A small explicit colligation has
operator norm one. The local energy-identity numerical residual is at most
7.28e-12 and the terminal reservoir energy is zero. The implementation computes
remaining state norms directly, rather than accumulating energy-subtraction
roundoff.

At the first tranche's warranted E_0=16, this particular W_b permits only three
fully masked windows. Consequently this lower bound does **not** defeat its
65536-window guarantee. It instead identifies a parameter that no uniform
finite-service claim can omit: the initial stored-energy budget relative to
sensor range and actuator headroom. Unknown spectral gap is not the only
notion of memory duration; this shift is nilpotent but can have arbitrarily
long finite delay as its dimension grows.

## 5. A costed pre-ADC range operation restores information

For the positive statement, the unknown fixed specimen is any contractive
linear state/control/supply colligation satisfying (1). Its incremental
controlled response is A. The uncontrolled current input is predictable before
the current fresh sign, or independent of that sign conditional on the past.
It must not implement an unknown contemporaneous feedback that changes A.
The controller has a warranted **pathwise** bound J_N, not just an unspecified
average bath power.

Use N=dn signed coordinate inputs of amplitude U. From (1),
\(\sum_t\|y_t\|^2\le V=E_0+NU^2+J_N\), hence every scalar amplitude is
at most sqrt(V). Supply a calibrated, impedance-matched attenuation operation
after the output port and before clipping:

\[
 g=M/\sqrt V. \tag{11}
\]

The attenuator must preserve plant loading and gain A. Its loss ports/heat and
the external supply are actual resources. This is an additional physical
measurement operation; it was absent from the obstruction's operation set.
There is no hidden full signed readout, analogue sample replay or extra ADC
call. The attenuated signal fits the original range in one read per window.

Let q_t be the 2K+1-level stochastic report of gy_t, using the same W centered
random words as before, and digitally reconstruct r_t=q_t/g. In original units
the grid spacing is

\[
 D=\frac{\sqrt V}{K},\qquad\epsilon_p=\frac1{2W}. \tag{12}
\]

There is no clipping bias. Define

\[
 T_R=V+D(1+2\epsilon_p)\sqrt{mNV}+\epsilon_p NmD^2. \tag{13}
\]

For \(\widehat A_{:j}=(nU)^{-1}\sum_{t:j_t=j}s_tr_t\),

\[
 \Pr\left\{\|\widehat A-A\|_F\le
 \frac{\sqrt{T_R/\delta}}{nU}
 +\frac{\sqrt{md}\epsilon_pD}{U}\right\}\ge1-\delta. \tag{14}
\]

### Proof of the repair

Exactly as in the retained first proof, stochastic rounding in a cell has
variance at most D times the scalar magnitude, and a finite centered word
changes its second moment by at most epsilon_p D(2|y|+D). Thus the total
expected reconstructed second moment is at most T_R. Fresh signs cancel the
pre-sign field, including the current external-supply contribution. The
centered matrix report sum is a martingale with squared Frobenius moment at
most T_R. Markov's inequality yields the first term in (14). Finite-word
conditional mean errors are at most epsilon_p D per scalar, giving the second
term. No relaxation or system order is used.

The first tranche's resolvent proof supplies, on this one event, simultaneous
inverse-command radii \(B r_A/\lambda\) for every \(\|b\|\le B\), including
targets chosen from the acquired record. As before, this is a statement about
the fixed incremental response, not physical delivery of warm raw outputs.

## 6. What the repair costs and still assumes

For J_N=NP, fixed nonzero U, ideal conditional-mean sensing and fixed K, the
sufficient bound (14) is O(N^{-1/4}); global worst-case range grows as sqrt(N).
An ordinary full signed-read correlation estimate has an O(N^{-1/2}) bound
under this energy budget. Their information and precision costs differ.

With finite W, the bias term is order sqrt(N)/W. Retaining the ideal rate
requires W=Omega(N^{3/4}), or O(log N) random bits per scalar read. A fixed
16-bit word is charged at the executed finite horizon; unlimited convergence
at fixed precision is not established.

If the ADC's conditional mean in attenuated units has additional error at most
eta, the operator radius needs at least sqrt(md) eta/(gU), provided the report
second-moment contract remains warranted. A mean guarantee alone is insufficient.
To retain the ideal N^{-1/4} rate this sufficient scheme requires eta of order
N^{-3/4}. A warranted relative gain error also has to be charged, and gain
headroom must prevent actual clipping. The exact-gain calculation below is
mathematical; no device tolerances are qualified.

For example, independent post-quantizer readout noise of variance sigma_q^2 in
attenuated ADC units adds, in SISO, the exact correlation-variance contribution

\[
 \frac{\sigma_q^2}{Ng^2U^2}
 =\frac{\sigma_q^2V}{NM^2U^2}
 \longrightarrow\frac{\sigma_q^2(U^2+P)}{M^2U^2}. \tag{15}
\]

This is a nonzero floor for this scheme, not an impossibility theorem for all
other readout architectures. Noise before clipping also changes the necessary
boundary/range accounting. Thus the gain operation restores mathematical
observability but does not make physical low-noise sensing free.

The attenuator exports or dissipates
\((1-g^2)\sum_t\|y_t\|^2\) energy. Its heat handling, gain control, detector
power, and source apparatus work are not included in a normalized wave-energy
number. All source energy is explicitly charged; the supply is not called
passive stored energy.

## 7. Executed discrimination and strongest ordinary comparisons

Run `python3 check_supply_observability.py`. It makes 256 coupled path pairs
for each interface, 65536 windows per specimen. The coupling is a numerical
counterfactual comparison; different sensor interfaces are not free simultaneous
physical reads. No first-tranche file is overwritten.

The program checks both scattering matrices, the per-window full two-port
energy identity, every controlled amplitude in a 10001-point grid, and all
fixed-ADC transcripts. Matrix and energy residuals are at most 2.23e-16 and
8.89e-16. Fixed-range transcript disagreements are exactly zero; every primary
read saturates. Fresh signs and dither do not recover the hidden gain sign.

It also embeds the pair as A=diag(+/-sqrt(lambda),1) and deliberately tries the
first-tranche 2D protocol at its retained amplitude 0.03638863513, without
admitting the continuing supply. Every acquired operator estimate violates the
inapplicably reused 0.1085956 radius, and 97.65625% of the task errors violate
the inapplicable task radius. This is the substantive failed extension, **not
a counterexample to the first theorem**, whose no-supply premise is violated.

For the generic SISO repair, E_0=16, U=.7, P=4.84, M=1, K=128, W=65536,
delta=.01 give:

| Per specimen | Executed value |
|---|---:|
| Active windows / scalar reads | 65536 / 65536 |
| Idle windows / resets / adjoint operations | 0 / 0 / 0 |
| Calibrated pre-ADC gain | 0.001691945945 |
| Warranted original-unit range | 591.0354304 |
| Reconstructed grid spacing | 4.617464300 |
| Controlled input energy | 32112.64 |
| External supply energy | 317194.24 |
| Mean attenuator loss energy | 174652.94 |
| Mean energy delivered to ADC | 0.4999771 |
| ADC random bits / fixed report bits | 1048576 / 589824 |
| 99% operator radius | 0.22320223 |
| Simultaneous task radius, B=.4 and lambda=.5 | 0.17856178 |
| Zero-experiment radius | 0.28284271 |

The attenuated interfaces had no saturations and 3596427 paired transcript
differences. Median/max audited operator errors were .009864/.044266; these
are not controller information. No certificate violations occurred in this
finite test; this is not a substitute for the proof. Tiny audited task errors
at a=+/-sqrt(lambda) reflect the flat ridge solution map at those extremal
points and are not evidence of general hardware performance.

Ordinary least squares on the exact same reconstructed observations equals
the proposed estimate to 1.12e-16. For the known pair, the ordinary exact
consistency decoder using the same generic gain identifies the member in a
median of seven reads, maximum 69, on these paths. There are no unresolved
members. This decoder uses the explicitly supplied pair model, which the
generic unknown-colligation theorem does not assume.

More strongly, if both competitors are granted the known pair, use the
calibrated gain \(g_{pair}=M/(cW_b+\sqrt\lambda R)\), about 0.48766.
The four possible signed outputs from the two instances occupy disjoint ADC
code sets. An ordinary consistency decoder then identifies the member in
**one read**, which is optimal because zero reads leave the pair unresolved.
The code exhausts every 16-bit dither word and both command signs to verify
zero ambiguities. The 65536-window generic bound is therefore not a claimed
necessary cost on this simple family. The exact obstruction under the old
operation set survives even this full pair knowledge.

## Remaining obligation and actual consequence

The sharp result is that a replenished zero-mean input can make a bounded ADC
erase all gain information, even in a reciprocal lossless system and even with
forward/adjoint access. It explains exactly why amplitude thinning alone does
not extend the first result. At least some accessible information or operation
must change on this pair.

The positive construction makes one such change explicit and supplies a
finite certificate with its real energy and precision costs. It does not
establish a useful full-apparatus advantage, known thermal-bath performance,
external novelty, or hardware qualification. The strongest unresolved
obligation is a physically affordable way to retain incremental signal
information before hard saturation while warranting the measurement mean and
variance. The mathematical derivations and executions have not received an
independent audit.
