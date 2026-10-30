# An ordinary finite-cycle supplier for adaptive null sensing

30 October 2026. Constructive ordinary comparison using the three-qubit
correction resources in root's continuation-13 source. No new workers,
native-bath reset, microscopic copying or ideal intermediate gauge
replacement is used.

## 1. What the comparison establishes

A conventional periodic repair cycle can supply the same uniformly
positive unknown signal exposure needed by root's global conditional
bracket. The cycle alternates a finite ancilla-cooling hold with a finite
**damped excitation-transfer pulse**. Native errors, a persistent quantum
bath, the signal and the reset reservoir remain active throughout.

This alternative uses the same logical/gauge encoding, protected memory,
reset qubit and exchange coupling as root's always-on construction. It
also needs an actual **on/off command for that coupling**, plus calibrated
pulse timing. Those gates are not implied by a coordinate change or by
an always-on Hamiltonian. The comparison preserves that distinction.

All amplitudes, pulse precision and cycle frequency can remain fixed as
the final frequency tolerance tends to zero. The coherent logical
storage time and reference-field accuracy have exactly the same scaling
requirements as in root's receiver.

The result is a strong ordinary supplier, not a new inference algorithm
or a priority claim. The explicit conservative constants below are worse
than root's always-on sufficient constants. No total-work advantage is
established.

## 2. Actual controls and the persistent source

Use root's transformed coordinates: logical qubit \(L\), gauge qubit
\(q\), reset qubit \(r\), and arbitrary hidden system \(H\).
The physical encoding has
\[
Z_s=Z_LZ_q,\qquad X_s=X_q,\qquad
H_{\rm signal}=\delta Z_LZ_q/2,\quad \delta=\theta-u.
\]

Supply an actual gated exchange
\[
H_c(t)=g(t)(q_-r_++q_+r_-),\qquad g(t)\in\{0,R\},
\]
and the continuously active reservoir
\[
R\,\mathcal D[r_-]+\nu R\,\mathcal D[r_+],
\qquad 0\le\nu\le1/36 .
\]
In physical sensor coordinates the on coupling is exactly root's
\[
H_c=\frac R2(X_sX_r+Y_sZ_aY_r).
\]
Its two-/three-body structure remains a supplied physical resource.

Native jumps have operators \(X_q\otimes B_b(t)\), with
\[
\sum_b B_b(t)^\dagger B_b(t)\le\Lambda I_H.
\]
Also allow a transverse coherent coupling
\[
H_{\rm tr}(t)=X_q\otimes B_H(t),\quad
B_H(t)=B_H(t)^\dagger,\quad \|B_H(t)\|\le J.
\]
Hidden-only evolution can have arbitrary internal frequencies and need
not mix. The enlarged propagation must be well-defined. Every bound is
required after conditioning on the full preceding record and for both
actual coupling settings; installing a gate is not permission to keep an
unverified old noise envelope.

Write \(D=\Lambda+J\). At \(\delta=0\), every listed operation is exactly
the identity on \(L\). This is the protected resource. Incorrect physical
operators that introduce a logical term are not covered by good gauge
population measurements.

The cycle is:

1. **Cooling hold:** \(g=0\) for \(h=4/R\).
2. **Damped transfer:** \(g=R\) for a duration \(p\) specified below.
3. Repeat, without measuring or replacing the hidden state or gauge.

Only the reset reservoir remains continuously coupled to \(r\).
There is no initial pure-state assumption on \(q,r,H\), and they can be
entangled. Logical preparation is the actual conditional fresh-\(L\)
operation already required by root's inference interface.

## 3. A finite damped-swap identity

First omit native errors and the upward reservoir during the transfer
pulse. Let
\[
\mathcal C(\rho)=-i[R(q_-r_++q_+r_-),\rho]
                    +R\,\mathcal D[r_-](\rho).
\]
Starting with \(r=0\) and the single excitation on \(q\), the no-jump
amplitude remaining on \(q\) satisfies
\[
\ddot a+(R/2)\dot a+R^2a=0,\quad a(0)=1,\quad \dot a(0)=0.
\]
Therefore
\[
a(t)=e^{-Rt/4}
\left[\cos\!\left(\frac{\sqrt{15}Rt}{4}\right)
+\frac1{\sqrt{15}}\sin\!\left(\frac{\sqrt{15}Rt}{4}\right)\right].
                                                               \tag{1}
\]
Any reset jump from this single-excitation sector takes the state to
\(|00\rangle\), from which it cannot re-excite. Thus the total probability
of \(q=1\) is \(|a(t)|^2\).

At the first zero
\[
p_*=\frac{4\arccos(-1/4)}{\sqrt{15}\,R}
       =\frac{d_*}{R},\qquad d_*<2,                  \tag{2}
\]
an arbitrary input supported on \(r=0\) has zero output \(q\) excitation.
Let \(n_q=|1\rangle\langle1|_q\) and \(n_r=|1\rangle\langle1|_r\).
The output effect
\[
E_*=\exp(p_*\mathcal C^*)n_q
\]
is positive and at most \(I\). Its compression to the \(r=0\) subspace
is zero. Positivity implies that its cross block to that subspace is
also zero. Consequently the following **operator inequality** holds:
\[
0\le E_*\le n_r.                                   \tag{3}
\]

This is stronger than checking population transfer on a diagonal input.
It holds for every \(q,r\) state and after tensoring with an arbitrarily
entangled hidden system. No independent reset-state preparation was
used in deriving it.

The pulse is a finite ordinary exchange with damping still present.
It is not an instantaneous SWAP or a cold-state reset channel inserted
by hand.

## 4. Robust finite pulse rather than exact timing

The nominal first zero makes the proof transparent. The actual pulse
only needs a fixed effect tolerance
\[
\widetilde{\mathcal E}^{\,*}(n_q)\le n_r+\zeta I,
\qquad \zeta\le1/512,\qquad p\le2/R,                 \tag{4}
\]
where \(\widetilde{\mathcal E}\) includes the actual pulse waveform and
downward reservoir, but not the separately bounded native/upward terms.

This is available in an open neighborhood of the nominal finite pulse.
For example, Hermitian trace-norm Duhamel bounds control an effect
perturbation by the time integral of the actual generator perturbation.
A scalar exchange error contributes at most
\(2\int|\Delta g(t)|dt\), and a downward-rate error at most
\(2\int|\Delta\gamma(t)|dt\). A small pulse-duration change has a
corresponding bounded generator-times-duration contribution.

Square edges are only an ideal notation. Finite smooth ramps whose
integrated generator error obeys the same fixed \(\zeta\) budget give
(4). The nominal duration has a strict margin below \(2/R\), so fixed
finite ramps can be included. This requires an actual finite slew
capability and calibration. Their accuracy does not need to improve
with the final sensing tolerance.

The crucial qualification is algebraic: these errors must remain
gauge-only. A small wrong physical phase that introduces a logical
Hamiltonian or logical decoherence accumulates over the coherent
interrogation and belongs to root's \(O(\epsilon)\) logical error
budget. Equation (4) alone would not detect such an error.

There is also a within-pulse qualification. The waveform, ramps and
amplitude/timing errors used here retain the displayed
excitation-conserving exchange operator and a downward reset reservoir.
The population bound in (10) uses that conservation law. An arbitrary
gauge-only operation with the same terminal effect (4) could transiently
excite the clock, so (4) alone is not a certificate for such an operation.
Extra gauge disturbances require their own stated excitation-growth
bound, included in the native budget; they are not silently covered by
pulse endpoint calibration.

## 5. Uniform population bounds with the real bath still attached

All expectations in this section refer to the zero-residual comparison,
conditional on the complete history before the interrogation.
Its initial state on \(q,r,H\) is arbitrary.

During each cooling hold the reset population obeys the exact scalar
equation
\[
\frac d{dt}\langle n_r\rangle
=\nu R-(1+\nu)R\langle n_r\rangle.
\]
Native transverse terms act on \(q,H\) and therefore do not enter it.
At the end of any hold,
\[
\langle n_r\rangle
\le\frac{\nu}{1+\nu}+e^{-4(1+\nu)}
<\frac1{37}+\frac1{54}<\frac3{64}.                  \tag{5}
\]
This bound also holds on the first cycle, without a fresh reset input.

During a transfer pulse, the joint trace distance between the evolution
with and without the native/upward terms is at most
\[
(\Lambda+J+\nu R)p.
\]
Indeed, the native Lindblad sum has Hermitian trace-norm bound \(2\Lambda\),
the bounded coherent commutator has bound \(2J\), and the upward
dissipator has bound \(2\nu R\). Interleaved CPTP contraction gives the
bound; arbitrary hidden-only evolution can be retained in both
propagators.

Since \(0\le n_q\le I\), (4)--(5) give, after every pulse,
\[
\langle n_q\rangle
\le\frac3{64}+\zeta+2(D/R+\nu).                      \tag{6}
\]

Choose a single fixed rate
\[
R\ge512(D+W),                                       \tag{7}
\]
where \(W\) is the warranted initial frequency width.
Then (6), \(\nu\le1/36\), and \(\zeta\le1/512\) imply
\[
\langle n_q\rangle\le7/64.                           \tag{8}
\]

During a subsequent hold,
\[
\frac d{dt}\langle n_q\rangle\le\Lambda+J=D.
\]
The jump contribution is at most \(\Lambda\), while
\(\|i[X_q\otimes B_H,n_q]\|\le J\). Hence
\[
\langle n_q(t)\rangle\le7/64+4D/R\le15/128.           \tag{9}
\]

At the start of the next pulse, (5) and (9) give
\[
\langle n_q+n_r\rangle\le21/128.
\]
The exchange conserves \(n_q+n_r\), the downward reservoir decreases
it, and the remaining terms increase its expectation at rate at most
\(D+\nu R\). Throughout that pulse,
\[
\langle n_q\rangle
\le\langle n_q+n_r\rangle
\le21/128+2(D/R+\nu)<15/64.                          \tag{10}
\]

No classical jump-path representation of the clock was used. Coherent
transverse coupling to a warm quantum bath is included. The initial
state need not commute with any of the population operators.

## 6. All-time positive exposure

The first hold and pulse take
\[
\tau_0=h+p\le6/R.
\]
During that first warm interval we only use \(Z_q\ge-I\). At every
later time, (9)--(10) imply
\[
\langle Z_q\rangle=1-2\langle n_q\rangle\ge17/32.
\]
For any \(T\ge1/W\), not merely an integer number of cycles,
\[
\begin{aligned}
\int_0^T\langle Z_q(t)\rangle\,dt
&\ge\frac{17}{32}T-\frac{49}{32}\tau_0\\
&\ge\left(\frac{17}{32}-\frac{294}{32\cdot512}\right)T\\
&>\frac12T.                                        \tag{11}
\end{aligned}
\]

The source therefore meets root's conditional exposure premise with
\(v=1/2\), uniformly over all warm initial \(q,r,H\) states and all
permitted old records. Native rates, hidden couplings and hidden
frequencies are never estimated.

The physical signal continues during every hold, pulse and edge ramp.
Equation (11) is deliberately proved for the mathematical zero-residual
comparison. At the actual small residual, root's CPTP Duhamel/oddness
argument bounds the full signal backreaction. No signal-free correction
interval or hypothetical ability to switch off the unknown field is
assumed.

## 7. An equally informed ordinary estimator

Prepare the same logical \(|+\rangle\) conditionally on each retained
history. Run the fixed finite cycle for interrogation time \(T_j=1/w_j\),
measure logical \(Y\), and use root's same confidence bracket at the
known reference command \(u_j\).

Because the entire gated source is logical identity at the null and
\(\|Z_q\|=1\), its terminal mean satisfies
\[
|b(\delta)-\delta s_T|\le|\delta|^3T^3/6.
\]
For \(|\delta|T\le1/2\), (11) yields the same lower response slope
\(g_0=11/24\). The same conditional martingale concentration, central-
half update and confidence allocation therefore give total coherent
interrogation \(O(\epsilon^{-1}\log(1/\alpha))\), without an extra
logarithm of inverse precision in the interrogation sum.

This is an ordinary robust stochastic bracket around a protected
phase response. The inference procedure is not a new learning
algorithm. It does not identify the unknown exposure or divide by
a fitted finite-correction gain.

At an actual fixed nonzero residual, both this periodic operation and
the always-on operation generally have phase-scale bias and
decoherence. The adaptive range \(|\delta|T\le1/2\) is the consequential
receiving condition. An old finite-cycle QEC limitation calculated at a
fixed nonzero signal is not automatically a counterexample to that
different adaptive regime.

## 8. Exact resource comparison

| Resource | Root always-on supplier | This ordinary periodic supplier |
|---|---|---|
| Logical/gauge/reset qubits | Same three physical qubits | Same three physical qubits |
| Protected null coordinate | Exact logical identity | Same requirement |
| Reset reservoir | Always active, finite rates | Same type; never replaced by an exact reset |
| Exchange coupling | Continuously on | Same coupling with explicit gating |
| Native bath | Persistent, arbitrary warm state | Persistent, arbitrary warm state |
| Extra syndrome meter | None | None |
| Correction command clock | No periodic gate schedule required | Fixed finite on/off period |
| Sufficient balanced-rate bound | \(r\ge18(\Lambda+2J+W)\) in root's announced extension | Conservative \(R\ge512(\Lambda+J+W)\) |
| Pulse calibration | Actual gauge-only coupling required | Fixed finite transfer-effect budget |
| Reference-field accuracy | Order \(\epsilon\) | Same |
| Longest protected interrogation | Order \(1/\epsilon\) | Same |

The announced coherent extension in this table is distinguished from
the pinned earlier root input, which has only the jump envelope.
It is not accepted here as an unread source version.

The periodic result supplies the **same scaling at a fixed finite
correction bandwidth**. It does not match root's smaller sufficient
constant, and it does not have a lower complete apparatus cost.
One cannot claim an advantage under a fixed numerical maximum
coupling/reset rate by comparing different maxima.

The cycle consumes \(O(R\mathcal T)\) actual gate commands and reset
opportunities over total interrogation \(\mathcal T\). The protected
memory must remain coherent throughout each \(T_j\). Logical
preparation/readout counts, initial-range acquisition, reference
calibration, sensing and retained-record conditions are unchanged.

For the explicitly driven Hamiltonian \(g(t)H_{\rm ex}\), a specified
Hamiltonian-work convention includes
\[
W_c=\int\langle H_{\rm ex}\rangle\,dg,\qquad
\|H_{\rm ex}\|=1.
\]
Its magnitude is at most the actual total variation of \(g\): no more
than \(2R\) per ideal on/off cycle. Smooth ramps use their real
variation. This is a control-port bound, not a claim that each
cycle dissipates that amount or that it is the full drive/bath cost.
The reservoir energy scale and microscopic thermodynamic coupling must
be supplied before emission counts are called heat or total work.

A literal always-on source without a gating port cannot execute this
periodic sequence. An ordinary controller on those literal ports can
still use root's always-on operation and the same robust bracket,
with exactly the same resources as root. There is no computational or
statistical superiority over that equally supplied controller.

## 9. Close predecessors and the surviving distinction

Liu and Zhou, arXiv:2606.19628, primary PDF page 3, supply the exact
CNOT/gauge encoding and Bell input used here. Their gauge reset is
presented as an ideal intervening operation in a factorized discrete
query model. It directly preempts the basic encoding/reset architecture.
The finite damped exchange and uniform conditional exposure calculation
above are an ordinary explicit implementation comparison; priority is
not inferred from the difference in presentation.

Rojkov et al., PRL 128, 140503 (2022), directly establish that finite
correction delay changes the signal scale and can bias an estimator.
Their ordinary remedy includes calibrated postprocessing. A common-null
bracket is another ordinary receiving strategy when its conditional
sign source is actually available.

Shettell et al., arXiv:2101.02823, analyze finite error-correction
intervals, noisy ancillae and wrong syndromes. Their finite-interval
phase-variance terms explicitly depend on the signal strength; this
underscores the need to distinguish a fixed physical frequency from
the adaptively reduced residual. It does not remove their genuine
ancilla/logical noise obstruction.

No stronger null sensor is obtained merely by citing these papers.
The physical operator algebra, reset reservoir, conditional error
envelope, known cancellation port and real endpoint operations remain
the required source. The ordinary finite-cycle construction demonstrates
that the task is not exclusive to an autonomous constant coupling.

## 10. Verification scope

The accompanying code checks the damped-transfer effect inequality and
the minimum zero-residual integrated exposure over **all initial
states** in explicit finite joint gauge/reset/hidden models. It
includes noncommuting coherent hidden evolution. These are population
operator checks of the construction, not acquired device calibration,
not a sampled global learning experiment, and not a substitute for
the uniform analytic proof.
