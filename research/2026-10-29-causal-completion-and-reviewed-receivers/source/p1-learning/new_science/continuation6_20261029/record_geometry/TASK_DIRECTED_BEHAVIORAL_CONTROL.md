# Useful untested control from one actual input–output trajectory

**Status.** A deliberately strong conventional comparator, with a constructive finite-precision receiving certificate and an exact synthetic example. The behavioral mechanism is established by Willems and successors, not claimed as a new physical principle. The new work in this folder is the explicit interface accounting, derivation, fixture and adversarial boundary used to guide the Astra P1 choice. No apparatus data, practical advantage, or global stability claim is supplied.

## 1. The consequence and the interface

A physical port has an unknown but warranted linear, time-invariant input–output behavior. An actual input waveform and its visible output are recorded on one persistent specimen. Those data suffice to compute a different, previously unexecuted waveform, and to certify that its actual finite-horizon task cost improves over a stated baseline. The hidden initial state need not be known or reset. The relevant object is the finite-horizon response at the port, not a microscopic realization.

The following are premises, rather than discoveries inferred merely from a good fit:

1. On the specified operating range and throughout calibration and execution, the port has a deterministic LTI realization
   \[
   x_{t+1}=Ax_t+Bu_t,\qquad y_t=Cx_t+D_0u_t.                 \tag{1}
   \]
   The dimension of the minimal input–output realization is bounded. A visible-past length \(\ell\) at least its observability index is warranted.
2. The input values and timing are actual controlled quantities. The same affine actuator law applies to the newly designed waveform. Calibration at a few settings does not establish the kinetics of an arbitrary new actuator.
3. Outputs are noninvasively measured, and their metrological errors have a stated simultaneous bound or a warranted tail contract. The simple theorem below does not include unknown process disturbances.
4. All coefficients remain fixed on this specimen during the experiment. They may depend on an arbitrary frozen device parameter, provided the premises hold uniformly and calibration and use refer to that same parameter.

The microscopic system can contain arbitrarily many additional variables, including frozen ones. What matters is that their influence on the declared port is exhausted by (1). This is a strong physical model-class premise. Calling the port model a representation instead of a model does not remove it.

If linearity is warranted only inside a local microscopic operating region, a separate invariant-region or execution warrant is required. Bounds on the visible output alone do not establish that an unobserved state remains inside such a region. The exact fixture uses the declared global linear port law.

For the concrete receiver, take a two-temperature linear port: heat or cool one accessible component, read only its temperature, and allow a second component to remain hidden. The scientific question is how to choose a short future heating waveform with useful tracking and low actuation cost. No equilibrium initializer or conditional preparation theorem is required.

## 2. Exact synthesis from actual trajectory segments

Let a calibration record contain \(N\) input–output pairs. Choose a past length \(\ell\) and a task horizon \(T\). Each length-\(\ell+T\) window is an actual trajectory segment of the same system. Arrange the windows into the usual Hankel blocks
\[
\begin{pmatrix}U_p\\U_f\end{pmatrix}=H_{\ell+T}(u^d),\qquad
\begin{pmatrix}Y_p\\Y_f\end{pmatrix}=H_{\ell+T}(y^d).       \tag{2}
\]
The superscript \(d\) denotes the calibration data, not a distinct specimen. Let \((u_p,y_p)\) be the actual most recent \(\ell\) inputs and outputs at deployment.

**Proposition 1: a behavioral synthesis certificate.** For every vector \(g\) satisfying
\[
U_pg=u_p,\qquad Y_pg=y_p,                                \tag{3}
\]
the physically executed future input
\[
u=U_fg                                                     \tag{4}
\]
produces the future output
\[
y=Y_fg.                                                    \tag{5}
\]
This statement holds for every feasible \(g\); the data need not span every possible control program.

**Proof.** Let \(x_j\) be the hidden state at the beginning of calibration window \(j\). Linearity makes the weighted sum of window trajectories a trajectory from \(\sum_jg_jx_j\), with input and output equal to the corresponding matrix products in (2). Compare its past with the specimen's current past. Both have the same past input, so their output difference over that past equals the observability matrix \(\mathcal O_\ell\) applied to their initial-state difference. Equation (3) makes this zero. Since \(\ell\) is at least the observability index, the two minimal states agree, and hence their states at the end of the past agree. Their future input is (4), so their future outputs agree. ∎

The computation can use negative entries of \(g\). These are representation coefficients justified by the actual linear input law; no copying or signed probability experiment is performed. Only the one feasible input waveform (4) is executed. Its amplitude, slew, timing and energy constraints must be imposed on \(U_fg\), rather than on the arbitrary representation vector.

Consequently, solve
\[
\min_g J(Y_fg,U_fg)
\quad\text{subject to (3), } U_fg\in\mathcal U,\;Y_fg\in\mathcal Y. \tag{6}
\]
Any feasible solution is a true physical task trajectory. It can combine calibration segments into an input never present in the data. If only a restricted collection of programs is represented, (6) optimizes over that collection. It makes no optimality claim over omitted directions.

**Task-only weakening.** If the task observes a linear functional \(Qy\), full state observability can be weakened to
\[
\ker\mathcal O_\ell\subseteq\ker(Q\mathcal O_{\mathrm{future}}A^\ell).
                                                               \tag{7}
\]
Here \(\mathcal O_{\mathrm{future}}\) starts at the future boundary. The same proof establishes only \(Qy=QY_fg\). This can be useful when hidden directions persist but cannot affect the particular task. Condition (7) still needs an independent physical or model-class warrant; a finite set of observed windows does not establish its quantification over every hidden direction.

## 3. When one actual experiment covers all programs

For a controllable minimal realization of dimension \(n\), an input persistently exciting of order \(\ell+T+n\) makes the columns of the length-\(\ell+T\) joint input–output Hankel matrix span all such trajectories. This is the fundamental lemma of Willems, Rapisarda, Markovsky and De Moor. Thus (6) becomes the usual exact finite-horizon optimal-control problem, expressed through data. The current past supplies its hidden initial condition implicitly. The deterministic LTI equivalence with model predictive control is established by Coulson, Lygeros and Dörfler.

For \(m\) input channels, persistent excitation of order \(L\) means
\[
\operatorname{rank} H_L(u^d)=mL.                           \tag{8}
\]
It requires at least \((m+1)L-1\) samples. This is an actual algebraic condition on the executed inputs; an independent random input is only one way of producing it. Actuation and sample costs remain real.

There is no necessity to reconstruct \(A,B,C,D_0\). Indeed, unknown similarity transformations of the hidden realization do not affect the answer. Nevertheless, under the full persistent-excitation hypotheses the data are also sufficient for ordinary system identification within the declared model class. Avoiding an explicit realization is a computational or representational choice, not evidence that the data lack model information. Data informativity theory separately shows that some control tasks need genuinely less information than unique identification; stabilization and exact LQR do not have identical requirements.

## 4. A finite sensor-error certificate with a measured conditioning cost

This section specializes to a scalar input and output, with minimal order \(n\) and \(\ell=n\). An upper bound alone can be treated with rank-revealing coordinates, but the square construction below assumes the exact order. The fixture has \(n=2\).

There is a linear predictor
\[
y_f=M z,\qquad z=\operatorname{col}(u_p,y_p,u_f),\qquad
d=\dim z=2n+T.                                             \tag{9}
\]
The existence follows by inverting the \(n\)-step scalar-output observability matrix. It is independent of calibration. Let
\[
D=\operatorname{col}(U_p,Y_p,U_f),\qquad F=Y_f.
\]
Then \(F=MD\). Select \(d\) columns, giving square \(D_J\) and corresponding \(F_J\). A complete experiment provides invertible choices. The selection can depend on the observed data.

Suppose every distinct actual sensor reading used in the calibration matrix and current past has error at most \(\epsilon\). Inputs are exact. Put hats on observed matrices and define
\[
\widehat M=\widehat F_J\widehat D_J^{-1},\quad
k=\|\widehat D_J^{-1}\|_\infty,\quad
q=d\epsilon k.                                            \tag{10}
\]
Matrix infinity norm means maximum absolute row sum. If \(q<1\), then the true selected matrix is invertible and
\[
\boxed{\|M-\widehat M\|_\infty\le
\Delta:=\frac{d\epsilon(1+\|\widehat M\|_\infty)k}{1-q}.} \tag{11}
\]

**Proof.** Write \(\widehat D_J=D_J+E_D\), \(\widehat F_J=F_J+E_F\). Each row has \(d\) entries, so both perturbation norms are at most \(d\epsilon\), even though inputs have no error. The Neumann bound gives
\[
\|D_J^{-1}\|_\infty\le k/(1-q).
\]
Using the defining identity for \(\widehat M\),
\[
M-\widehat M=(-E_F+\widehat M E_D)D_J^{-1},
\]
which proves (11). ∎

The many appearances of the same raw reading in a Hankel matrix are correlated. This proof never assumes independence between matrix entries. The single simultaneous reading bound also protects a data-selected column subset and a data-selected future control. Choosing a well-conditioned subset lowers an actual measurable amplification factor; it does not make the unobserved lag premise disappear.

Let \(\widehat z=\operatorname{col}(u_p,\widehat y_p,u_f)\). For any chosen feasible future waveform,
\[
\boxed{\|y_f-\widehat M\widehat z\|_\infty
\le \xi(u_f):=\Delta\|\widehat z\|_\infty
 +(\|\widehat M\|_\infty+\Delta)\epsilon.}                \tag{12}
\]
This follows by adding \((M-\widehat M)\widehat z\) and \(M(z-\widehat z)\). A control constraint \(\|u_f\|_\infty\le U\) permits a common \(\xi\) using
\[
Z=\max\{\|u_p\|_\infty,\|\widehat y_p\|_\infty,U\}.
\]

For a task reading only a row \(Qy_f\), the same argument applied to \(QF\) gives a task-specific predictor radius
\[
\Delta_Q\le
\frac{d\epsilon(\|Q\|_1+\|\widehat M_Q\|_1)k}{1-q},
\quad\widehat M_Q=Q\widehat F_J\widehat D_J^{-1}.          \tag{13}
\]
Thus the required precision can be set by the queried output functional. Uniform recovery of all microscopic quantities is not an intermediate requirement.

## 5. Converting the response interval into a useful decision

Consider the physical cost
\[
J(u)=\sum_{j=1}^T(y_j-r_j)^2+\lambda\sum_{j=1}^T u_j^2,
\qquad\lambda>0.                                          \tag{14}
\]
For the predicted \(\widehat y=\widehat M\widehat z\), (12) implies the fully computable bound
\[
|J(u)-\widehat J(u)|\le E_J(u):=
2\xi(u)\|\widehat y-r\|_1+T\xi(u)^2.                     \tag{15}
\]
Therefore a sufficient actual improvement certificate over a particular baseline \(u_b\) is
\[
\widehat J(u_b)-E_J(u_b)
  >\widehat J(u_*)+E_J(u_*).                              \tag{16}
\]
There is no need to certify every possible controller before (16) can establish useful new control. It compares actual physical costs, not signed projected laws.

Output constraints are handled by tightening each predicted constraint by its certified error. For example, \(|\widehat y_j|+\xi\le Y_{\max}\) implies the true bound. Optimizing the fitted quadratic over an input box is a conventional convex program. Any rounded, digitally executable candidate can instead be inserted into (12)–(16), with its actual input values; exact execution of a real-valued mathematical minimizer is unnecessary.

If a uniform cost radius \(E\) holds over the input domain, the fitted minimizer has true excess cost at most \(2E\). If an implementation incurs fitted optimization error \(\delta_{\mathrm{opt}}\), this becomes \(2E+\delta_{\mathrm{opt}}\). A finite-horizon certificate by itself does not prove recursive feasibility or all-time stability. Stronger established robust MPC results address those separate questions under their additional hypotheses.

## 6. Confidence, retained records and costs

The preceding conclusions are pathwise on the metrology event. If \(Q_0\) distinct sensor readings each have a warranted two-sided sub-Gaussian tail with parameter \(\sigma\), a union bound yields
\[
\epsilon=\sigma\sqrt{2\log(2Q_0/\beta)}                  \tag{17}
\]
with failure probability at most \(\beta\). Independence among overlapping windows is neither needed nor available. Equation (17) is a possible sensor supplier, not an experimentally established property of the fixture.

One may condition the tail premise uniformly on a persistent device parameter and preceding experiment history. The resulting event still protects any subsequently chosen column subset and control because the inequalities are simultaneous deterministic statements. This gives a valid joint high-probability statement with arbitrary retained old information. It does not assert that a confidence probability remains \(1-\beta\) after conditioning on every possible observed calibration transcript.

There are no costs for hidden-state copies because no such operation is requested. The experiment pays for all \(N\) actual input calls, visible readings, elapsed call time, actuation energy, and the subsequent \(T\) calls. Noninvasive readout precision, allowed actuator resolution, persistence of the linear regime, and any protection needed to keep the coefficients fixed are premises or costs. If sensor averaging requires a physical hold, that hold must be supplied; it is not silently inserted. The example uses a specified one-reading error budget instead.

Small coordinate error is the service objective. For deterministic continuous outputs, even nearby distinct outcomes can have total variation distance one. No full-record TV claim is made.

## 7. Executed exact synthetic construction

The unknown-to-the-designer plant used for verification is
\[
A=\begin{pmatrix}3/4&1/8\\1/8&1/2\end{pmatrix},\quad
B=\begin{pmatrix}1/4\\0\end{pmatrix},\quad
\text{readout after each call }y=x_1.                      \tag{18}
\]
This is a stable symmetric positive two-temperature port model with a hidden second temperature. A post-call readout is an LTI output of form (1), with \(C'=CA\), \(D_0=CB\). The simulator begins at \((1/3,-1/4)\); the designer receives neither this state nor the matrices.

The actual synthetic calibration is one 40-call input record with amplitudes in \(\{-1,+1\}\). Every readout and its deliberately imposed bounded sensor error is saved exactly as a rational number. No state reset occurs. Use \(n=\ell=2\), \(T=6\), target \(r_j=2/5\), \(\lambda=1/20\), and \(\epsilon=10^{-6}\). Exact rational elimination verifies input persistent excitation of order 10 and behavioral predictor rank 10. Floating-point pivoted QR is used only to select measured columns; all identities and receiving inequalities are then checked with exact rational arithmetic.

The fitted minimizer is rounded to the declared actuator grid \(2^{-16}\mathbb Z\). The executed six inputs are
\[
(0.5750885009765625,\ 0.42352294921875,\ 0.369171142578125,
\ 0.3425445556640625,\ 0.31353759765625,\ 0.2413787841796875).
\]
Every amplitude is absent from the calibration data and lies strictly inside its amplitude range. Applying these inputs to the same continuing specimen yields the independent verification results:

| Quantity | Result |
|---|---:|
| Measured selected inverse infinity norm | 125.22217084199136 |
| Neumann radius \(q\) | 0.0012522217084199136 |
| Certified predictor infinity error \(\Delta\) | 0.004070197599429853 |
| Actual predictor infinity error | 0.00025861709864435835 |
| Certified maximum future output error \(\xi\) | 0.004072447980390399 |
| Actual maximum future output error | 0.0000016430909407106985 |
| Zero-input baseline true cost | 0.48063305378713406 |
| New waveform true cost | 0.053130256879652005 |
| Certified true cost reduction | 0.4121036470381547 |
| Actual true cost reduction | 0.42750279690748205 |

The fixture demonstrates a complete finite-data calculation, not a statistical or apparatus experiment. In particular, \(10^{-6}\) metrological accuracy is imposed and explicitly charged as a premise. The conditioner has an appreciable inverse norm, which the certificate retains. No claim that 40 noisy physical samples at unspecified resolution suffice is justified.

Artifacts: `check_behavioral_control.py`, `BEHAVIORAL_CONTROL_SYNTHETIC_READOUTS.json`, and `BEHAVIORAL_CONTROL_CHECKS.json`. The designer routine takes only the visible data, lag, task and metrological budget. Hidden matrices occur only in the simulator and independent check.

## 8. A passive hidden-delay obstruction to learning the missing premise

For any finite calibration budget \(N\), choose an integer delay \(L>N\), a gain \(0<\rho\le1\), and two systems
\[
S_+: y_t=\rho u_{t-L},\qquad
S_-: y_t=-\rho u_{t-L},\qquad u_t=0\ (t<0).                \tag{19}
\]
They have nilpotent shift-register state realizations, so both are stable LTI systems. They are passive in the scattering-energy sense:
\[
\sum_{t=0}^K y_t^2\le\rho^2\sum_{t=0}^K u_t^2
\le\sum_{t=0}^K u_t^2.                                    \tag{20}
\]
A passive delay line with opposite terminal reflection signs is an appropriate port interpretation; this is not a claim about positive-real impedance passivity.

For every adaptive or randomized experiment of at most \(N\) calls, their entire calibration records are identical: all outputs are zero, and hence a controller with the same random seed selects the same inputs. One also cannot distinguish either from a zero-transfer port during that time. The fact that the observed response has low rank therefore does not certify a short hidden lag or the absence of a delayed mode.

There is a sharp control consequence. Immediately after calibration choose a new input \(u_N\), with \(|u_N|\le1\), and require the future output at time \(N+L\) to equal a target \(a\in(0,\rho]\). For a controller which knew the sign, \(u_N=\pm a/\rho\) achieves zero error. Any controller based on the indistinguishable calibration record must choose the same distribution of \(u_N\) on both systems, and
\[
\frac12\mathbb E[(\rho u_N-a)^2+(-\rho u_N-a)^2]
=\rho^2\mathbb E[u_N^2]+a^2\ge a^2.                       \tag{21}
\]
Thus at least one compatible system has expected squared task error at least \(a^2\). Later feedback cannot change this particular output, which depends on the already fixed \(u_N\). The task horizon here includes the hidden delay; this is not an impossibility claim for every fixed short task with an independently controlled initial state.

The obstruction survives perfect noiseless sensing, arbitrary input amplitudes during calibration, and ordinary stability and energy-passivity warrants. It is resolved by a warranted order/lag, a finite task-relevant memory/tail bound, another physically informative observation channel, or sufficiently long experiments. A nonparametric label alone does not resolve it.

## 9. Implication for the next central mechanism

Ordinary behavioral control already joins an actual intervention record to a useful untested physical waveform, with hidden-state continuation and finite-precision accounting. The valuable new question is therefore not merely whether some predictive information can guide a control.

A stronger physical contribution would have to supply a missing premise more economically or in a wider class: for example a physically certified task-relevant memory bound for nonlinear hidden dynamics, a control algebra which makes an otherwise unknowable response direction observable, or an intervention structure that guarantees useful performance despite unresolved hidden alternatives. An exact finite behavioral closure assumed at the port is already a powerful comparator; presenting it again as a new representation would not clear that comparator.

Primary comparisons, precise source-reading scope, and qualifications are recorded in `PRIMARY_PREDECESSORS.md`.
