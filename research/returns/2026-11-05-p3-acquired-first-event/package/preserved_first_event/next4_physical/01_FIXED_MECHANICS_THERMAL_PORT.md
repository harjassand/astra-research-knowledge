# Fixed mechanics, hidden heat: an exact thermal-port equivalence

## Status and purpose

This is a completed, independently checked physical specialization of an obstruction **already present in the Astra corpus**. It should not be promoted as a new scientific destination or as a new useful engine.

The current Astra return “Active mechanical ports do not identify thermodynamic cost” already proves exact indistinguishability under arbitrary adaptive force protocols, including minimal controllable and observable realizations with different entropy production. Its isothermal construction changes mobility and native force law. The construction below instead fixes the entire reciprocal spring system, unit mobility, bath directions, force port, and observation port, and changes only two reservoir temperatures. It needs just two even coordinates. The distinction comes from the different physical model class, not a contradiction or a stronger general theorem. [A1–A2]

The consequential fact is therefore sharply scoped:

> In an explicitly specified two-reservoir harmonic system, a mechanical port can have exactly the equilibrium position process, equilibrium response, and equilibrium cyclic-work statistics while a positive heat current crosses the system. No amount of observation or admissible adaptive forcing at that port distinguishes the conductor from its equilibrium twin.

The result is a boundary on thermodynamic inference and intervention from an incomplete physical interface. It is not an implementation of useful work extraction, a new acquisition algorithm, or an assertion that maintaining the reservoirs is free.

All equations below use dimensionless units with Boltzmann's constant and each coordinate's friction set to one. Every coordinate is even under time reversal.

## 1. Choose the physical consequence before the algebra

A proposed response-based thermodynamic instrument ought to answer more than whether a fitted transfer function is stable. It should distinguish a device at equilibrium from one carrying heat, and it should determine whether that heat is accessible through its permitted actuators.

Here the instrument is unusually generous. It sees an ideal continuous position record, can apply a bounded mechanical force conjugate to that position, can implement arbitrary well-posed causal feedback, and may retain unlimited classical memory. It is allowed arbitrarily long experiments and arbitrarily precise computation. The device itself has fixed rates 1 and 3; there is no closing gap.

Nevertheless, the entire resulting experimental transcript is identical for an equilibrium device and a heat-conducting device. This obstruction survives all finite-band or noisy versions of the same measurement interface because those are conditional postprocessings of the ideal transcript.

Brownian gyrators provide a primary physical antecedent for two orthogonal thermal baths acting through a reciprocal harmonic potential. They can power suitable loads when the required mechanical access is supplied. Our claim concerns the specifically restricted port defined below, not all loads or all ports. [P1]

## 2. A fixed, minimal, two-dimensional model

Set
\[
 A=\begin{pmatrix}1&0\\0&3\end{pmatrix},\qquad
 c=\frac1{\sqrt2}\binom11,\qquad
 v=\frac1{\sqrt2}\binom1{-1}.
\]
For
\[
 0\le s<s_*:=4+2\sqrt5
\]
define
\[
 \Sigma_s=A^{-1}+s vv^\top
 =\begin{pmatrix}
 1+s/2&-s/2\\-s/2&1/3+s/2
 \end{pmatrix}
\]
and
\[
 D_s=\frac{A\Sigma_s+\Sigma_s A}{2}
 =\begin{pmatrix}
 1+s/2&-s\\-s&1+3s/2
 \end{pmatrix}.
\]
The physical process and the measured coordinate are
\[
 dX_t=(-AX_t+c\,u_t)\,dt+\sqrt{2D_s}\,dW_t,\qquad
 Y_t=c^\top X_t. \tag{1}
\]
The native initial condition is
\[
 X_0\sim\mathcal N(0,\Sigma_s),
\]
independent of future bath noise and controller randomness.

The potential energy is \(H(x)=x^\top Ax/2\). Mobility is the identity for every member. Adding the potential \(-u_t c^\top x\) therefore produces exactly the force term \(c u_t\) in (1). This is an actual conjugate mechanical force, not an arbitrary source term renamed a force.

The covariance is positive definite. Also
\[
 \det D_s=1+2s-\frac{s^2}{4}>0
\]
on the stated range, and its first diagonal entry is positive. Thus (1) is a nondegenerate stationary Ornstein–Uhlenbeck diffusion when \(u=0\), with the displayed covariance.

There is no dynamically detached extra coordinate. In fact
\[
 \det[c,Ac]=1,\qquad
 \det\binom{c^\top}{c^\top A}=1.
\]
The deterministic system is both controllable and observable. Its drift eigenvalues are always 1 and 3. Deterministic observability does not identify an unknown process-noise covariance from a partial stationary stochastic record.

## 3. Only reservoir temperatures change

Write
\[
 D_s=I+sM,\qquad
 M=\begin{pmatrix}1/2&-1\\-1&3/2\end{pmatrix}.
\]
The eigenvectors of \(M\), and hence the bath directions, do not depend on \(s\).

Choose \(0<\theta<\pi/4\) with
\[
 \cos(2\theta)=1/\sqrt5,\qquad \sin(2\theta)=2/\sqrt5,
\]
and let
\[
 R=\begin{pmatrix}\cos\theta&-\sin\theta\\
 \sin\theta&\cos\theta\end{pmatrix},\quad q=R^\top X,\quad b=R^\top c.
\]
Then (1) becomes
\[
 dq_t=(-Kq_t+b u_t)\,dt+
 \sqrt{2\,\operatorname{diag}(T_c,T_h)}\,dW_t,
 \qquad Y_t=b^\top q_t,
\]
where the **fixed** reciprocal spring matrix is
\[
 K=R^\top A R
 =\begin{pmatrix}
 2-1/\sqrt5&2/\sqrt5\\
 2/\sqrt5&2+1/\sqrt5
 \end{pmatrix},
\]
the **fixed** port is
\[
 b=\frac1{\sqrt2}
 \binom{\cos\theta+\sin\theta}{\cos\theta-\sin\theta},
\]
and only
\[
 T_c(s)=1+s(1-\sqrt5/2),\qquad
 T_h(s)=1+s(1+\sqrt5/2) \tag{2}
\]
change.

At \(s=0\), both reservoirs have temperature 1. At \(s=4\),
\[
 T_c=5-2\sqrt5\approx0.527864,\qquad
 T_h=5+2\sqrt5\approx9.472136.
\]
Consequently, the equilibrium/conductor ambiguity already occurs with strictly positive temperatures in a bounded interval and with bounded, identical mechanical components.

The ideal white reservoirs are an explicit Markovian modeling assumption. A finite microscopic reservoir implementation, its replenishment apparatus, or its ultraviolet cutoff is not constructed here. Such an implementation would require its own analysis; it is not needed for this exact model-class identifiability theorem.

## 4. Full mechanical transcript equivalence

Since \(v^\top c=0\),
\[
 \Sigma_s c=A^{-1}c.
\]
The native scalar process is centered Gaussian with covariance
\[
 C(t)=\mathbb E[Y_tY_0]
 =\frac12\left(e^{-|t|}+\frac13 e^{-3|t|}\right), \tag{3}
\]
independent of \(s\). The causal mechanical impulse-response kernel is likewise fixed:
\[
 g(t)=c^\top e^{-At}c
 =\frac12(e^{-t}+e^{-3t}),\qquad t\ge0. \tag{4}
\]
The word “impulse-response” names the mathematical kernel; no impulsive experiment is assumed or required.

Duhamel's identity gives the actual path equation
\[
 Y_t=Y_t^{\,0}+\int_0^t g(t-r)u_r\,dr, \tag{5}
\]
where \(Y^0\) has the common stationary law (3). This identity remains valid when \(u\) is chosen from past measurements.

**Theorem 1 — adaptive mechanical-port equivalence.**
Consider any causal controller whose commands are measurable functions of its independent random seed, previous measurements, and retained memory. Suppose the coupled system is well posed, with a unique input/output solution. The controller may impose force and slew limits, stop adaptively, digitize observations, add conditionally specified detector noise, and keep a record of its commands and computations. If its only plant coupling is the conjugate force in (1), its entire transcript has the same law for every \(s\).

**Proof.** Couple the experiments by giving them one common realization of \(Y^0\), one common controller seed, and the same conditional measurement-noise construction. Equation (5), together with the same causal controller, is the same Volterra equation in every experiment. Uniqueness makes the observed record and commands coincide pathwise. Every recorded or stopping-time output is then the same measurable function of the coupled common record. ∎

The result allows nonlinear feedback. It does not grant unmodeled access through thermometer readings, reservoir manipulation, direct observation of another coordinate, or a reset of the hidden physical state. A controller's digital memory reset does not reset that state.

The quadratic variation is also identical:
\[
 [Y]_t=2(c^\top D_s c)t=2t.
\]
Thus arbitrarily fine ideal sampling does not expose an overlooked diffusion coefficient.

## 5. Exact hidden heat and entropy production

For an all-even overdamped diffusion with constant diffusion matrix \(D\), the stationary entropy-production rate is
\[
 \sigma=\int \frac{j(x)^\top D^{-1}j(x)}{p(x)}\,dx.
\]
This is the irreversible probability-current expression appropriate to the stated parity and reservoir model. The treatment of odd variables would differ; none are being hidden in this construction. [P2]

Here
\[
 Q_s:=\frac{A\Sigma_s-\Sigma_s A}{2}
 =\begin{pmatrix}0&s/2\\-s/2&0\end{pmatrix},
 \qquad
 \frac{j_s(x)}{p_s(x)}=-Q_s\Sigma_s^{-1}x.
\]
Therefore
\[
 \sigma_s=\operatorname{tr}
  (\Sigma_s^{-1}Q_s^\top D_s^{-1}Q_s)
 =\boxed{\frac{s^2}{1+2s-s^2/4}}. \tag{6}
\]

For completeness, let \(Q_s=(s/2)J\) with \(J_{12}=1,J_{21}=-1\).
For symmetric \(2\times2\) matrices,
\(J^\top D^{-1}J=D/\det D\).
The Lyapunov identity also gives
\(\operatorname{tr}(\Sigma^{-1}D)=\operatorname{tr}A=4\).
These identities yield (6) immediately.

The heat interpretation can be checked independently. For fixed
\[
 K=\begin{pmatrix}\alpha&k\\k&\beta\end{pmatrix}
\]
with two independent unit-friction baths, stationarity implies
\(KS+SK=2\operatorname{diag}(T_c,T_h)\).
The mean heat entering the system from coordinate \(i\)'s bath is
\[
 J_i=T_i K_{ii}-(KSK)_{ii}.
\]
Solving the two-dimensional Lyapunov relation gives
\[
 J_h=-J_c=\frac{k^2(T_h-T_c)}{\alpha+\beta}.
\]
In our model,
\[
 \boxed{J_s=\frac{s}{\sqrt5}},\qquad
 \sigma_s=J_s\left(\frac1{T_c(s)}-\frac1{T_h(s)}\right).
 \tag{7}
\]
At \(s=4\), the hidden conductor carries
\[
 J_4=4/\sqrt5\approx1.788854,\qquad \sigma_4=16/5=3.2,
\]
although every allowed mechanical transcript is exactly that of \(s=0\).

As \(s\uparrow s_*\), entropy production diverges. This is not unbounded heat power: \(J_s\) tends to \(2+4/\sqrt5\), while the cold-bath temperature tends to zero. A claim of uniform bounded-temperature hardware with arbitrarily large entropy production would therefore be false. The bounded-temperature pair \(s=0,4\) already proves the substantive identifiability failure.

## 6. A finite-force, finite-slew work experiment

Equations (3)–(4) obey
\[
 g(t)=-C'(t),\qquad t>0,
\]
the scalar equilibrium fluctuation-response relation at temperature 1, at every frequency and time scale. This gives more than passive reversibility.

Take any deterministic absolutely continuous force with
\(u(0)=u(T)=0\). Work done on the system over the cyclic potential change is
\[
 W=-\int_0^T \dot u(t)Y_t\,dt
   =\int_0^T u(t)\circ dY_t.
\]
It is Gaussian under (1), and its law is independent of \(s\).

An explicitly admissible probe is
\[
 u(t)=F\sin^2(\pi t/T).
\]
It has peak force \(F\), maximum slew \(F\pi/T\), and zero force and endpoint slope. For a prescribed slew limit \(L\), choose \(T\ge F\pi/L\). No sudden switching or ideal impulse is needed.

For \(\lambda\in\{1,3\}\), let
\[
 z_\lambda'=-\lambda z_\lambda+u,\qquad z_\lambda(0)=0.
\]
The mean work contribution of that mode is
\[
 m_\lambda=-\frac12\int_0^T \dot u\,z_\lambda\,dt
 =\frac12\int_0^T (z_\lambda')^2dt+
   \frac{\lambda}{4}z_\lambda(T)^2\ge0.
\]
Since the covariance contribution is \(e^{-\lambda|t-r|}/(2\lambda)\),
integration by parts gives
\[
 \operatorname{Var}(W_\lambda)=2m_\lambda.
\]
The diagonal equilibrium realization has independent modes, hence
\[
 \boxed{W\sim\mathcal N(m,2m),\quad
 m=m_1+m_3\ge0,\quad \mathbb E[e^{-W}]=1.} \tag{8}
\]
Because of transcript equivalence, the same law holds in every conductor.

Thus this entire class of open-loop cyclic force experiments fails to extract positive mean work from the hidden heat current at this port. Arbitrary feedback has the same transcript and work statistics as the corresponding equilibrium feedback experiment, but may extract work using acquired information. Equation (8) is **not** asserted for arbitrary feedback; treating it as such would erase the controller's information resource.

Timescale-separated examples can exhibit a detectable fluctuation-response violation caused by hidden dissipation. The relevant primary work establishes that phenomenon in its specified regimes. Our exact zero-violation construction shows why that diagnostic cannot be elevated to a universal completeness guarantee. [P3]

## 7. What extra operation breaks the equivalence?

### A trusted full-state reset

Suppose an extra operation prepares the entire two-dimensional state at the known value \(X_0=0\), with zero applied force and the chosen reservoirs active afterward. This changes the experiment's initial information. Then
\[
 \operatorname{Var}_s Y_t=
 \frac12\left[(1-e^{-2t})+\frac{1-e^{-6t}}3\right]
 -\frac{s}{4}(e^{-t}-e^{-3t})^2. \tag{9}
\]
At \(t=(\log3)/2\),
\[
 \operatorname{Var}_sY_t=\frac{40}{81}-\frac{s}{27}.
\]
The \(s=0\) and \(s=4\) variances differ by \(4/27\), so repeated truly reset trials distinguish them.

This observation does not construct the reset. Resetting a controller, preparing a known mean, or applying a deterministic force is insufficient. The operation has to control or know the covariance of the full physical state. The deterministic controllability rank calculation does not supply a noise-free reset under ongoing thermal forcing. A proposal that uses (9) must specify and pay for its clamping, cooling, conditional preparation, or extra actuator, including precision, duration, measurement noise, reservoir disturbance, and memory erasure.

### An extra coordinate measurement

Observing \(Z=v^\top X\) gives
\[
 \operatorname{Var}Z=\frac23+s,
\]
which immediately resolves the family given sufficient calibrated samples. That is extra physical sensing, not more numerical processing of \(Y\).

### A thermal intervention

Calibrated changes to the diffusion law can also expose the hidden covariance. Astra already has an explicit finite-slew common thermal-pulse identification construction, including its reachability, calibration, and cost qualifications. It is prior machinery, not an operation newly solved here. [A3]

The hardest missing operation for converting this branch into a positive universal thermodynamic instrument is therefore **additional certified physical access**: a trustworthy full-state preparation or a calibrated thermal/extra-sensor intervention. Under the present port alone, the missing operation is impossible rather than merely expensive.

## 8. Statistical consequences and the exact covariance freedom

A test \(\varphi\in[0,1]\) based on any admissible transcript satisfies
\[
 \mathbb E_0\varphi=\mathbb E_4\varphi.
\]
Its power against the conductor equals its size against equilibrium, even with unlimited acquisition time. The obstruction is exact nonidentifiability, not a slow-mixing lower bound.

If an upper confidence bound \(U\) is uniformly valid at level \(1-\alpha\) over the full family,
\[
 \Pr_s\{U\ge\sigma_s\}\ge1-\alpha\quad\text{for all }s<s_*,
\]
then, since all transcript laws are the same and \(\sigma_s\) is unbounded,
\[
 \Pr\{U=+\infty\}\ge1-\alpha.
\]
This unbounded-confidence conclusion uses the approach to a zero-temperature reservoir. With specified positive temperature bounds, the equilibrium/conductor testing impossibility survives, but the numerical upper bound need not be infinite.

The same mechanism has a useful algebraic statement. Let \(A=A^\top>0\) be known, let \(B\) be a fixed mechanical port matrix, and consider
\[
 dX=(-AX+Bu)dt+\sqrt{2D}\,dW,\qquad Y=B^\top X.
\]
With stationary covariance \(\Sigma\), every symmetric \(S\) satisfying
\[
 SB=0,\qquad
 \Sigma+S>0,\qquad
 D'=\frac{A(\Sigma+S)+(\Sigma+S)A}{2}>0 \tag{10}
\]
produces the same native output covariance and the same forced transcript.

Conversely, if \((B^\top,A)\) is observable and two such stationary output laws agree, then their covariance difference satisfies \(SB=0\). Indeed equality of all positive-lag covariances implies
\(B^\top e^{-At}SB=0\), hence
\(B^\top A^k SB=0\) for every \(k\). Observability forces every column of \(SB\) to vanish.

This is the exact covariance ambiguity for known reciprocal mechanics and fixed ports. It is not a general identification theorem for unknown drift, unknown parity, or unknown bath memory.

## 9. Acquisition, initialization, memory, and execution cost ledger

| Component | What is explicitly supplied | What the result does and does not claim |
|---|---|---|
| Physical interaction | Reciprocal quadratic potential, unit mobility, fixed two-bath directions, conjugate scalar force | A legitimate two-temperature overdamped model; no changing nonconservative native force |
| Native initialization | Exact stationary Gaussian state for each model | Granted explicitly to strengthen the no-go; no claim of cheap preparation |
| Acquisition | Full continuous scalar position record and all commanded forces | Even this ideal record is insufficient; finite resolution cannot repair it |
| Force and slew | Arbitrary well-posed bounded protocols; explicit smooth sine-squared example | No impulse or infinitely sharp switch is used |
| Noise | Independent white thermal baths in a fixed coordinate basis | Non-Markovian microscopic bath implementation remains outside this theorem |
| Memory | Unlimited causal controller memory and private randomness | More retained data cannot break equal transcript laws |
| Execution | Any time horizon, stopping rule, number of retained-state trials, or computation | No finite or infinite computational budget identifies \(s\) from this interface |
| Reservoir supply | Heat maintenance implicit in fixed bath temperatures | Native heat power is real; its apparatus and replenishment are not free or costed |
| Additional preparation | Full-state reset would make transient variance informative | Reset is a new physical capability requiring a separate construction and cost |
| Useful output | Certified inference boundary and restricted-port work equivalence | No useful engine or new universal thermodynamic acquisition capability is delivered |

The paper-level endpoint is complete within its explicit model. The engineering endpoint is not: adding or pricing a suitable extra physical operation remains a separate task. This is why the branch should not replace a more consequential constructive destination that actually closes its acquisition and initialization costs.

## 10. Prior-art comparison and selection recommendation

The corpus comparison was performed at main revision
`fef3640a8b1dc5475674a006de417f652f3baf3c`.

| Result | What was already established | Increment here |
|---|---|---|
| Active-port nonidentifiability [A1–A2] | Exact adaptive forcing equivalence; observable/controllable minimal examples; entropy-production variation and unbounded upper certificates; work-law equivalence | Fixed unit mobility, fixed reciprocal conservative mechanics, fixed bath basis and port; two dimensions; explicit finite positive-temperature pair and heat-current calculation |
| Thermal pulse identification [A3] | Finite-slew common diffusion intervention can identify a finite-order observable OU model under stated physical reachability and calibration assumptions | A transparent explanation of why mechanical and thermal access are distinct; no new pulse algorithm |
| Brownian gyrator [P1] | Two-bath reciprocal harmonic systems and accessible mechanical engines | A particular mechanical port that is exactly equilibrium-equivalent for the full admissible transcript |
| Linear Langevin entropy production [P2] | Covariance/current formulas, including parity-sensitive cases | An exact auditable substitution, not a new entropy-production formula |
| Hidden-dissipation response [P3] | Observable response violations under specified separated-timescale conditions | A fixed-rate, zero-violation counterexample to universal extrapolation |

**Recommendation to the parent:** retain this as a useful assumption audit or a physical companion result. The broad endpoint was already closed in Astra, and the narrowed construction does not establish independent novelty against the wider literature. Do not select it as the next main destination in preference to a genuinely new completed physical or sampling capability.

## Sources

### Current Astra primary project artifacts

[A1] “Active mechanical ports do not identify thermodynamic cost.”
https://github.com/harjassand/astra-research-knowledge/blob/fef3640a8b1dc5475674a006de417f652f3baf3c/research/returns/2026-11-05-p2-tracial-acquisition/active-port-nonidentifiability.md

[A2] Proof companion, active port nonidentifiability.
https://github.com/harjassand/astra-research-knowledge/blob/fef3640a8b1dc5475674a006de417f652f3baf3c/research/returns/2026-11-05-p2-tracial-acquisition/package/companions/active_port_nonidentifiability.txt

[A3] “Thermal pulse identification.”
https://github.com/harjassand/astra-research-knowledge/blob/fef3640a8b1dc5475674a006de417f652f3baf3c/research/returns/2026-11-05-p2-causal-payload-memory/thermal-pulse-identification.md

### Primary published research

[P1] R. Filliger and P. Reimann, “Brownian Gyrator: A Minimal Heat Engine on the Nanoscale,” Physical Review Letters 99, 230602 (2007).
https://doi.org/10.1103/PhysRevLett.99.230602

[P2] G. T. Landi, T. Tomé, and M. J. de Oliveira, “Entropy production in linear Langevin systems,” Journal of Physics A 46, 395001 (2013).
https://doi.org/10.1088/1751-8113/46/39/395001
Primary author-hosted manuscript:
https://www.fmt.if.usp.br/~gtlandi/2012_12---entropy-circuit.pdf

[P3] S.-W. Wang, K. Kawaguchi, S.-i. Sasa, and L.-H. Tang, “Entropy production of nano systems with timescale separation,” Physical Review Letters 117, 070601 (2016).
https://doi.org/10.1103/PhysRevLett.117.070601
https://arxiv.org/abs/1601.04463

### Secondary cross-check, not a novelty basis

D. Lucente et al., “Conceptual and practical approaches for investigating irreversible processes,” New Journal of Physics 27, 041201 (2025).
https://doi.org/10.1088/1367-2630/adc6ab
https://arxiv.org/html/2410.15925v1
Sections 3.3–3.3.1 discuss the scalar Gaussian observation obstruction and the Brownian gyrator context.

## Verification artifact

`audit.py` checks the covariance and positivity identities symbolically, independently verifies heat and current formulas numerically, and evaluates a smooth bounded-force/bounded-slew cyclic work experiment using two independent mean-work expressions and the covariance integral. `audit_results.json` contains the actual output. These checks validate the mathematics, not a laboratory implementation.
