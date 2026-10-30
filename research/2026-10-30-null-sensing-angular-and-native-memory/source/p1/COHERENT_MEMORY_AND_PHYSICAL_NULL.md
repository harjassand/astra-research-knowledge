# Coherent hidden memory and the necessity of a physical null

30 October 2026. Root next attack after the finite auxiliary and global receiver were constructed. This extends their physical scope to a coherent persistent bath and proves a distinction between cancelling the actual signal and subtracting a phase afterward. It does not claim a new encoding, a new generic phase-estimation algorithm, or a manufactured apparatus.

## 1. A coherent environment need not be characterized or reset

Keep the sensing qubit s, memory a and reset qubit r from FINITE_AUXILIARY_CORRECTION_AND_OCCUPATION.md. In addition to the permitted native jumps, let the actual sensing qubit have a transverse Hamiltonian coupling

\[
H_{\rm int}(t)=X_s\otimes B_H(t),\qquad
B_H(t)=B_H(t)^\dagger,\qquad \|B_H(t)\|\le J.          \tag{1}
\]

The environment's internal Hamiltonian H_H(t) can be arbitrary, and its initial state can be entangled with the clock and reset qubit. It is never refreshed. The exact enlarged propagation must be well-defined; finite baths suffice, and an infinite bath needs the usual domain/propagator justification. A bound on the bath's total energy, internal frequencies, dimension or mixing time does not enter the estimate.

The physical coordinate change sends X_s to X_q tensor I_L. Thus (1), however strongly it entangles q with the bath during a trial, acts as logical identity at the null. The storage operator V still acts only on q,r. Its Hamiltonian disturbance obeys

\[
i[H_{\rm int},V]\le 2Jc I,
\qquad c=\|V\|=2/\gamma+\gamma/(4g^2).               \tag{2}
\]

The bath's internal Hamiltonian commutes with V and contributes zero, even when it is fast. Combining the native activity bound Lambda, finite-temperature upward reset and the warm-state boundary yields

\[
s_T\ge[1-2c\Lambda-4cJ-4c\gamma_\uparrow]T-2c.       \tag{3}
\]

Take g = gamma = r, gamma_up = nu r. The fixed finite choice

\[
r\ge18(\Lambda+2J+W),\qquad \nu\le1/36               \tag{4}
\]

gives s_T/T >= 1/2 for every T >= 1/W. The global conditional receiver and its O(epsilon^{-1} log(alpha^{-1})) total interrogation bound follow unchanged. This is a statement about a genuinely coherent memory, not a classical random-rate approximation.

The same argument permits any bounded clock/environment Hamiltonian H_int with norm at most J, and the more general jump class already stated in the supplier proof, provided those operations remain logical identity. The special form X_s tensor B_H makes the physical error algebra explicit. A signal-parallel coupling Z_s tensor B_H fails that algebra and is not covered.

This extension explains which information replaces full microscopic identification: the physical error-operator algebra and an interaction/activity envelope. Those may be warranted by an engineered model or acquired by a separate procedure with its own confidence and costs. The construction does not acquire them from a few terminal outcomes or infer them from equilibrium weights. Finite-data absence of observed logical errors does not establish exact null protection for unlimited future time.

## 2. The quantum bath is persistent through the actual measurement instrument

For a numerical realization, include one hidden qubit h with H_H = Omega Z_h/2 and H_int = J_actual X_q X_h. Evolve the full L,q,r,h Lindblad equation, keeping the finite q--r exchange. A trial prepares only the logical factor, interrogates, measures logical Y with a stated readout confusion channel, and then retains the resulting *conditional joint q,r,h state* for the next trial.

For outcome y, let M_y be the trace-decreasing completely positive map on q,r,h induced by that entire trial. The actual continuation is

\[
\tau_{i+1}=\frac{\mathcal M_{y_i}(\tau_i)}
 {\operatorname{tr}\mathcal M_{y_i}(\tau_i)}.          \tag{5}
\]

This updates the bath's quantum correlations and posterior state. Replacing it by a fresh stationary bath, an independent hidden label, or an unconditional averaged clock state would be a different experiment. Conditional preparation/readout errors and complete records are budgeted as in the main theorem.

The population checker check_coherent_memory_sensor.py implements (5). It does not demonstrate a bath reset or an experimental source. Its idealized endpoint operation still requires the actual finite-time preparation/readout error supplier stated in the main proof.

## 3. A physical cancellation is stronger than terminal phase subtraction

Here is an exact distinction within the finite auxiliary model, not a classical-clock approximation. Use constant g > 0, native flip rate lambda > 0, downward reset gamma > 0 and upward reset gamma_up > 0. Omit the extra bath in this subsection. Let the real residual be a fixed delta != 0.

**Claim.** Every logical off-diagonal component of the full L,q,r state decays exponentially at long time. In contrast, at delta = 0 the logical state is preserved exactly. Consequently a terminal phase rotation or subtraction from a classical phase estimate cannot reproduce the protected dynamics of an actual physical reference u that makes delta small.

**Proof.** The full jump operators are proportional to I_L X_q, I_L r_- and I_L r_+. In each fixed Z_L sector, the clock semigroup has a faithful stationary state. To see faithfulness without assuming it, the support of a stationary state is invariant under both r_- and r_+, hence has the form a q subspace tensor the full r space. Invariance under X_q and the exchange Hamiltonian then forces invariance under the q Pauli algebra, so a nonzero support is the full q,r space. The block-diagonal mixture of the two sector stationary states is a faithful stationary state rho_* of the full semigroup.

Suppose O is an adjoint eigenoperator with purely imaginary eigenvalue i omega. The Lindblad dissipation identity gives

\[
\mathcal L^*(O^\dagger O)
 -(\mathcal L^*O^\dagger)O-O^\dagger\mathcal L^*O
 =\sum_b[J_b,O]^\dagger[J_b,O].                      \tag{6}
\]

Taking its rho_* expectation makes the left side zero. Faithfulness implies that O commutes with all three jump operators. In the logical off-diagonal sector it must therefore have the form

\[
O=|0\rangle\langle1|_L\otimes(aI_q+bX_q)\otimes I_r. \tag{7}
\]

The commutator with H_c produces a term proportional to b Z_q Y_r, which cannot be proportional to (7) or cancelled by the signal term. Thus b = 0. The signal commutator then produces a term proportional to delta a Z_q, which also cannot be proportional to (7). Since delta != 0, a = 0. There is no nonzero imaginary-axis eigenoperator in a logical off-diagonal block. The conjugate block has the same property.

Finite-dimensional CPTP propagation has spectrum in the closed left half-plane; the strict absence of peripheral off-diagonal eigenvalues gives exponential decay of that entire block (a possible polynomial Jordan factor can be absorbed by a smaller positive decay exponent). At delta = 0, every logical operator tensor I_clock commutes with the generator, so logical coherence is preserved exactly. This proves the claim.

If f_delta(T) is the terminal logical coherence, applying exp(+iuTZ_L/2) at the end only multiplies it by a phase. It leaves |f_delta(T)| unchanged. The same holds for merely subtracting uT in data analysis. The actual physical field -uZ_s/2 changes the entire coupled generator to one with residual delta = theta-u; it can therefore keep the operation close to its protected null during the whole interrogation.

This comparison uses an unobserved reset bath and terminal access to the supplied sensor. Monitoring the environment, changing the correction cycle, or adding a different physical sensor is an additional operation and can change the task. The claim does not exclude those constructive alternatives.

## 4. The noncommuting limits are operationally consequential

For each fixed nonzero delta, Section 3 gives vanishing late-time logical coherence. Nevertheless the signed-response theorem gives, for any fixed 0 < c_0 <= 1/2 and all allowed T,

\[
\operatorname{sign}(\delta)E[Y_L]
 \ge (1/2-1/24)c_0,
\qquad \delta=\pm c_0/T.                            \tag{8}
\]

Thus fixed-field coherence loss and inverse-time sensing are compatible at the same finite correction rate. The adaptive program follows a shrinking residual through a sequence of actual physical interventions. A calculation that first fixes a nonzero field and sends T to infinity addresses a different experiment.

This is an explanatory consequence rather than a claim of an unknown general metrology principle. Adaptive cancellation and finite-strength bias already have strong predecessors. The uniform conditional proof supplies the declared nonmixing memory scope and finite physical correction mechanism; an ordinary equally informed controller can use them.

## 5. A quantitative failure when null protection leaks

An uncorrected logical dephasing term gamma_L D[Z_L], gamma_L > 0, commutes with the stated signal/noise propagation and multiplies every logical coherence by eta_T = exp(-2 gamma_L T). It therefore destroys the nonvanishing response in (8) for sufficiently long T. Better occupation of q cannot repair this logical error.

A restricted but explicit information lower bound shows that this is more than a loose certificate. Consider the simpler allowed sensor with a perfect clock S=I, no hidden parameter-bearing side channel, fresh logical |+> per trial, arbitrary physical reference u, and a terminal binary logical quadrature measurement. A trial of duration T has

\[
p_\theta={1+\eta_T\sin[(\theta-u)T+\phi]\over2}.        \tag{9}
\]

The readout phase phi may be selected from history. For two parameter values separated by Delta,

\[
|p_\theta-p_{\theta+\Delta}|\le\eta_T|\Delta|T/2,
\quad p_{\theta+\Delta}(1-p_{\theta+\Delta})
 \ge(1-\eta_T^2)/4.
\]

The elementary Bernoulli KL upper bound gives

\[
D_{\rm KL}(p_\theta\Vert p_{\theta+\Delta})
\le {\Delta^2 T^2\over e^{4\gamma_LT}-1}
\le {\Delta^2 T\over4\gamma_L}.                      \tag{10}
\]

Commands, durations and readout phases may be selected causally from the full earlier record. Conditional KL adds, so a program of deterministic total interrogation at most mathcal T satisfies the same upper bound with T replaced by mathcal T. For 0 < alpha < 1/2, achieving error at most alpha under each hypothesis therefore requires

\[
\mathcal T\ge {4\gamma_L\over\Delta^2}
 (1-2\alpha)\log{1-\alpha\over\alpha}.               \tag{11}
\]

The same constant holds for equal-prior average error at most alpha by using the KL upper bound in both directions and the symmetric binary testing inequality. The restriction alpha < 1/2 is essential. For alpha >= 1/2 random guessing already suffices, and no positive time lower bound follows; the earlier unqualified wording was corrected after the receiving review.

This lower bound is for the declared terminal-quadrature family, with common initialization and no free informative old calibration. It is not a universal no-go theorem against stronger quantum codes, bath monitoring, nonterminal measurements or added initializers. It shows that a fixed logical leakage rate changes the precision exponent for this supplied service, even with a perfect internal clock and an equally informed adaptive controller.

The main construction therefore earns inverse-time sensing from an actual algebraic null and positive signal exposure. It does not earn it from a small finite calibration sample, a scalar rate fit, arbitrary passive memory, or an unpriced perfectly stable reference.
