# High-drive acquisition of a weakly coupled nonlinear network

**Status: conditional mathematical candidate; no novelty or physical advantage claimed.** I independently analyzed whether large-amplitude interventions can evade the weak-coupling acquisition obstruction for a one-port cubic network. They do improve the number of scalar reads needed to distinguish one fixed pair of hidden rotations, from order \(\varepsilon^{-8}\) to order \(\varepsilon^{-6}\). Once input energy is charged, that gain disappears: for the full class of static equilibrium holds in this model, the information per unit input energy is at most order \(\varepsilon^8\), and a bounded bias attains that exponent. The candidate therefore identifies a measurement-count versus actuator-energy tradeoff, not a general recovery primitive.

My first thought was stationary-density intervention for a nonlinear diffusion, but the pinned Astra corpus already has the exact affine-tilt route N549, and it records active hidden-generator intervention routes N713/N718. Those are source-derived candidates with open independent-review gates, so I treated them as overlap signals and switched to a separate cubic ODE acquisition question.

This note uses only the permitted folder. The Astra entry point at revision `5fc72a144d77c31b400efc0768afd7833c702362` says to pin the exact interface and keep acquisition and physical costs explicit. Its N598 dossier and source report already contain a bounded-input hidden-rotation obstruction, a matched nonlinear grey-box baseline, and a local sensitivity sweep. The independent question here is whether an input scaled with the weak coupling changes that obstruction when the cubic law is trusted at arbitrarily large state amplitudes. The internal source record is `frontier/dossiers/N598.txt` and `updates/CL/package/astra_ultra_high_conviction_04_2026-10-10/reports/s45_realization.txt` in the pinned Astra tree; the relevant source-report passage is its Section 3, lines 93–146, and its excitation-cost discussion is lines 208–218. These records are candidates and diagnostics, not external validation.

## Interface and candidate operation

Consider the controlled ODE

\[
 \dot x=-K_\varepsilon x-\alpha x^{\circ 3}+e_1u,\qquad y=e_1^Tx,
 \quad \alpha>0,
 \qquad K_\varepsilon=
 \begin{pmatrix}a&\varepsilon b^T\\ \varepsilon b&B\end{pmatrix},
\]

where the hidden dimension is \(m\), \(B\succ0\), and \(K_\varepsilon\succ0\) for the small couplings under study. The vector cube is coordinatewise. The competitor is the hidden rotation

\[
 K_\varepsilon^Q=T_Q^TK_\varepsilon T_Q,
 \qquad T_Q=\operatorname{diag}(1,Q),\qquad Q\in O(m).
\]

The two linear one-port transfer functions agree exactly because

\[
 e_1^T(sI+K_\varepsilon)^{-1}e_1
 =\left(s+a-\varepsilon^2b^T(sI+B)^{-1}b\right)^{-1}
 =e_1^T(sI+K_\varepsilon^Q)^{-1}e_1.
\]

In a cubic network, this rotation is generally observable only through nonlinear terms. The proposed intervention is to hold a constant bias

\[
 u_\varepsilon(t)=\alpha t^3\varepsilon^{-3},\qquad t>0\text{ fixed},
\]

until the state is near its unique equilibrium, then read the port. It forces the port to scale as \(y\asymp t/\varepsilon\), so the hidden state reaches order one. This changes the small-signal \(\varepsilon^4\) output contrast into an \(\varepsilon^3\) contrast for a generic fixed rotation pair. The exact ODE is assumed valid all the way to \(|y|\asymp\varepsilon^{-1}\); this is a severe physical promise.

The intervention is pairwise. One high-drive point is one scalar of information about an unknown rotation. For \(m\ge3\), a generic level set of one such scalar on the rotation orbit still has positive dimension. Recovering an unknown full matrix would require a curve or a richer family of controls, a proof that the acquired responses identify the matrix modulo signed permutations, and a stable finite-noise inversion theorem. I do not establish those claims.

## Exact rescaling law

Write \(G_I(z)=z^{\circ3}\) and \(G_Q(z)=Q((Q^Tz)^{\circ3})\). In coordinates shared by the two models, their hidden equilibrium vectors \(z_I(s),z_Q(s)\) are the unique solutions of

\[
 Bz_r+\alpha G_r(z_r)=-bs,\qquad r\in\{I,Q\},
 \qquad h_r(s)=b^Tz_r(s).
\]

The uniqueness follows because each left side is the gradient of a strongly convex function. If the port equilibrium is \(y\), then \(s=\varepsilon y\), and its scalar equilibrium equation is

\[
 F_r(y)=ay+\alpha y^3+\varepsilon h_r(\varepsilon y)=u.
\]

Set \(q=\varepsilon y\). After multiplying the port equation by \(\varepsilon^3\), the equilibrium is exactly

\[
 \alpha q^3+a\varepsilon^2q+\varepsilon^4h_r(q)=\alpha t^3.
\]

At \(\varepsilon=0\) this has the positive root \(q=t\), and its derivative in \(q\) is \(3\alpha t^2>0\). The implicit-function theorem therefore gives

\[
 q_r=t+c\varepsilon^2+d_r\varepsilon^4+o(\varepsilon^4),
 \qquad y_r=t/\varepsilon+c\varepsilon+d_r\varepsilon^3+o(\varepsilon^3).
\]

Matching the \(\varepsilon^2\) coefficient gives the common \(c=-a/(3\alpha t)\). Matching the \(\varepsilon^4\) coefficient and subtracting the two models gives

\[
 d_I-d_Q=-\frac{h_I(t)-h_Q(t)}{3\alpha t^2}
 =-\frac{b^T(z_I(t)-z_Q(t))}{3\alpha t^2}.
\]

This proves

\[
 \lim_{\varepsilon\downarrow0}\varepsilon^{-3}
   (\bar y_I(u_\varepsilon(t))-\bar y_Q(u_\varepsilon(t)))
 =-\frac{b^T(z_I(t)-z_Q(t))}{3\alpha t^2}.
 \tag{1}
\]

Here \(\bar y_r(u)\) denotes the equilibrium port state. Equation (1) is an acquired input/output contrast, not a supplied-model computation: the hidden vectors appear only in the proof of what the port readout measures.

At small \(s\), put \(v=B^{-1}b\). The implicit equations give

\[
 z_r(s)=-sv+\alpha s^3B^{-1}G_r(v)+O(s^5),
 \qquad
 b^T(z_I(s)-z_Q(s))
 =\alpha s^3 b^TB^{-1}\!\left(v^{\circ3}-Q((Q^Tv)^{\circ3})\right)+O(s^5).
 \tag{2}
\]

The common linear term cancels because the two models have identical linear transfer. The cubic term is generically nonzero. Inserting (2) into (1) gives an order-\(\varepsilon^3\) port gap at fixed, sufficiently small \(t>0\).

### Concrete O(1)-separated pair

Set \(a=\alpha=1\),

\[
 B=\begin{pmatrix}1&0\\0&2\end{pmatrix},\qquad
 b=\begin{pmatrix}1\\1\end{pmatrix},\qquad
 Q=\frac1{\sqrt2}\begin{pmatrix}1&-1\\1&1\end{pmatrix}.
\]

Then \(B^{-1}b=(1,1/2)^T\),

\[
 Q^TBQ=\begin{pmatrix}3/2&1/2\\1/2&3/2\end{pmatrix},
 \qquad Q^Tb=(\sqrt2,0)^T,
\]

and

\[
 b^TB^{-1}\!\left(v^{\circ3}-Q((Q^Tv)^{\circ3})\right)=-\frac7{32}.
\]

Thus the two hidden blocks are separated by \(\|B-Q^TBQ\|_F=1\), remain separated as \(\varepsilon\to0\), and are not equivalent under hidden signed permutations. Their linear port transfer functions are exactly equal. At any fixed nonzero moderate bias with unrotated limiting port state \(y_0\),

\[
 \bar y_I-\bar y_Q
 =\frac7{32}\frac{y_0^3}{1+3y_0^2}\,\varepsilon^4+O(\varepsilon^6).
 \tag{3}
\]

At the scaled bias \(u_\varepsilon(t)=t^3\varepsilon^{-3}\), equations (1) and (2) instead give

\[
 \lim_{\varepsilon\downarrow0}\varepsilon^{-3}(\bar y_I-\bar y_Q)
 =\frac7{96}t+O(t^3)\quad(t\downarrow0).
 \tag{4}
\]

So for a sufficiently small fixed \(t>0\), a single settled high-drive output has a nonzero gap of order \(\varepsilon^3\), despite the same exact linear transfer and an O(1) hidden-block difference.

The numerical diagnostic `high_drive_pair_diagnostic.py` solves the exact equilibrium equations at 60 decimal digits. For fixed bias \(u=0.7\), the ratio \((\bar y_I-\bar y_Q)/\varepsilon^4\) converges to the coefficient in (3). For \(t=0.1\), the scaled-bias ratio \((\bar y_I-\bar y_Q)/\varepsilon^3\) converges to the limit in (4), 0.0072917. This checks the expansion on finite values; it does not validate a physical system or prove the generic statement.

## Acquisition cost and an energy lower bound

With independent scalar reads of variance \(\sigma^2\), the fixed high-drive setting has mean separation \(c_t\varepsilon^3+o(\varepsilon^3)\), so the two simple Gaussian hypotheses require and admit

\[
 N_{\rm high}=\Theta(\sigma^2\varepsilon^{-6})
\]

reads for fixed testing error. A fixed moderate bias with the nonzero coefficient in (3) instead uses \(N_{\rm moderate}=\Theta(\sigma^2\varepsilon^{-8})\). This is a real count-only gain under the stated independent-read model.

The input levels differ much more sharply. At high drive, \(u_\varepsilon^2\asymp\varepsilon^{-6}\) for fixed \(t\). If one unit of dwell at the chosen input is charged per read, high-drive input energy is order \(\sigma^2\varepsilon^{-12}\); moderate-drive input energy is order \(\sigma^2\varepsilon^{-8}\). The one-port sensor must also handle \(|y|\asymp\varepsilon^{-1}\), and the cubic equation must remain accurate at that amplitude.

There is also a global energy bound for all constant-equilibrium settings, including adaptive choices of the next bias based on earlier observations. Assume

\[
 0<\varepsilon\le\varepsilon_0,\qquad
 \mu:=a-\varepsilon_0^2\|b\|^2/\lambda_{\min}(B)>0.
\]

For this fixed pair \((B,b,Q)\), there is a constant \(C\), independent of \(u\) and \(\varepsilon\), such that

\[
 |\bar y_I(u)-\bar y_Q(u)|^2\le C\varepsilon^8 u^2
 \quad\text{for every real }u.
 \tag{5}
\]

The constant may depend on \(a,\alpha,B,b,Q\) and the chosen \(\varepsilon_0\). The proof is an all-amplitude case split:

1. Strong monotonicity gives \(F_r'(y)\ge\mu+3\alpha y^2\). The hidden equation implies \(|h_r(s)|\le(\|b\|^2/\beta)|s|\), with \(\beta=\lambda_{\min}(B)\), so the two equilibria at a common bias differ by at most \(O(\varepsilon^2|y|)\). Their port slopes along the segment are therefore comparable to \(1+y^2\).
2. The hidden maps share the same linear term \(-s b^TB^{-1}b\). Analytic expansion at zero yields \(|h_I(s)-h_Q(s)|\le C|s|^3\) for \(|s|\le1\). For \(|s|\ge1\), taking the inner product of the hidden equation with \(z\) and using \(\langle z,G_Q(z)\rangle=\|Q^Tz\|_4^4\ge\|z\|_2^4/m\) gives \(\|z_r(s)\|\le C|s|^{1/3}\), hence \(|h_I(s)-h_Q(s)|\le C|s|^{1/3}\).
3. The root gap first obeys \(|\bar y_I-\bar y_Q|\le C\varepsilon^2|y|\), so for small enough \(\varepsilon_0\) the two roots have comparable magnitudes. The mean-value theorem with \(F'_r\ge\mu+3\alpha y^2\) then gives

   \[
   |\bar y_I-\bar y_Q|\le
   \frac{C\varepsilon}{1+|y|^2}
   \begin{cases}
      (\varepsilon|y|)^3,&\varepsilon|y|\le1,\\
      (\varepsilon|y|)^{1/3},&\varepsilon|y|\ge1,
   \end{cases}
   \qquad y=\bar y_I(u).
   \]

   The common input obeys \(|u|\ge\mu|y|+\alpha|y|^3\). Writing \(r=|y|\), the resulting ratios are

   | State range | Output gap | Input lower bound | Squared gap / input power |
   |---|---:|---:|---:|
   | \(r\le1\) | \(C\varepsilon^4r^3\) | \(\mu r\) | \(C\varepsilon^8r^4\le C\varepsilon^8\) |
   | \(1\le r\le\varepsilon^{-1}\) | \(C\varepsilon^4r\) | \(\alpha r^3\) | \(C\varepsilon^8r^{-4}\le C\varepsilon^8\) |
   | \(r\ge\varepsilon^{-1}\) | \(C\varepsilon^{4/3}r^{-5/3}\) | \(\alpha r^3\) | \(C\varepsilon^{8/3}r^{-28/3}\le C\varepsilon^{12}\le C\varepsilon^8\) |

   This proves (5) uniformly across low drive, the hidden nonlinear crossover, and overdrive.

For a continuous white-noise readout \(dY=\bar y_r(u_t)dt+\sigma_c dW_t\) during equilibrium holds, Girsanov's formula and (5) give

\[
 D_{\rm KL}(P_I\|P_Q)
 =\frac1{2\sigma_c^2}\mathbb E_I\!\int
   |\bar y_I(u_t)-\bar y_Q(u_t)|^2dt
 \le\frac{C\varepsilon^8}{2\sigma_c^2}
   \mathbb E_I\!\int u_t^2dt.
 \tag{6}
\]

For a pathwise input-energy cap \(E=\int u_t^2dt\le E_{\max}\), Pinsker's inequality implies that fixed-success discrimination needs \(E_{\max}=\Omega(\sigma_c^2\varepsilon^{-8})\). The bound is sharp in exponent for this pair: hold any fixed moderate bias with the nonzero coefficient in (3) and observe for time \(\Theta(\sigma_c^2\varepsilon^{-8})\). Thus the scaled high-drive protocol lowers the number of independent reads but worsens information per actuator energy from order \(\varepsilon^8\) to order \(\varepsilon^{12}\) at fixed \(t\). Equation (6) is for the quasistatic equilibrium-read interface. It is not a theorem for arbitrary transients, arbitrary feedback within a trial, hidden-state resets, or sensor models in which variance changes with state.

The ODE is a gradient flow in a strongly convex potential for each constant input, so it converges exponentially to the unique equilibrium. Reaching equilibrium to output error \(O(\varepsilon^3)\) at high drive can be charged an additional \(O(\varepsilon^{-6}\log(1/\varepsilon))\) input energy for one setup interval, and reaching error \(O(\varepsilon^4)\) at moderate drive costs only \(O(\log(1/\varepsilon))\). Both are below the respective long-observation energies \(\Theta(\sigma_c^2\varepsilon^{-12})\) and \(\Theta(\sigma_c^2\varepsilon^{-8})\) for fixed noise level, as \(\varepsilon\to0\). This settling estimate uses the ideal exact ODE and a fixed contraction rate; reset hardware and actual sensor precision remain uncharged.

The lower bound allows the experiment designer to know \(\varepsilon\), \(B\), \(b\), and the competing rotation. That is an oracle-favorable two-hypothesis test. The high-bias prescription cannot be executed at its stated scale when \(\varepsilon\) is unknown without a calibration or amplitude-search phase; charging that search can only increase cost. The bound does not include reset time, input bandwidth, actuator heating, saturation, state-dependent sensor range, model mismatch, or energy stored and dissipated during settling.

## Counterexamples and unresolved gates

- If \(\alpha=0\), every hidden orthogonal rotation remains exactly invisible for every waveform and amplitude: the full input/output behavior is linear and the transfer functions coincide. The high-drive operation requires nonlinearity.
- If \(Q\) is a hidden signed permutation, then \(G_Q=G_I\) after relabeling; this is the accepted coordinate ambiguity and no output contrast exists.
- For an O(1)-separated generic pair, one scaled bias yields one scalar \(b^T(z_I(t)-z_Q(t))\), so it only separates that pair. It does not reconstruct a dense hidden block.
- At fixed amplitude \(|u|\le U\) independent of \(\varepsilon\), equation (3) recovers the order-\(\varepsilon^4\) contrast. The high-drive scaling is unavailable under this bound, consistent with the N598 acquisition obstruction.
- The input grows as \(\varepsilon^{-3}\), the port state as \(\varepsilon^{-1}\), and the cubic model must hold there. If saturation, clipping, state-dependent couplings, or measurement range intervene before that scale, equation (1) is not an operational prediction.
- A mixed nonlinear response curve could remove more of the hidden rotation ambiguity, but I have not proved global or stable identifiability of \((B,b)\) from that curve. Ordinary local identifiability would still leave finite-noise conditioning and full acquisition cost open.

The next decisive mathematical gate is to extend or refute (6) for the actual dynamical observation model, where high-drive transients are not instantaneous equilibria. A positive full-recovery gate would then require a constructive inversion of the whole acquired rescaled curve with noise and actuator limits, followed by a matched comparison with full nonlinear grey-box prediction-error fitting. Without those results, this is a narrow acquisition tradeoff and no general capability claim follows.

## Primary-method comparison

The strong adjacent results I checked establish different parts of the problem:

- Vanelli and Hendrickx, [*Local Identifiability of Networks with Nonlinear Node Dynamics*, v4 (31 Aug 2026)](https://arxiv.org/html/2412.08472v4), assume the graph topology and each node activation are known, with unknown edge weights. Their discrete-time node model has partial source excitation and sink measurement; they prove generic local identifiability for analytic activations crossing zero exactly when every source component is excited and every sink component is measured. This does not give a finite-noise acquisition rate, energy bound, or globally stable inverse. Its known-activation and generic-local scope differs from the unknown symmetric continuous-time generator here.
- Birpoutsoukis, Marconato, Lataire, and Schoukens, [*Regularized Nonparametric Volterra Kernel Estimation*](https://arxiv.org/html/1804.10435v1), estimate a finite discrete-time truncated Volterra model from input/output data with iid Gaussian output noise. Their regularizer encodes smoothness and exponential decay assumptions on higher-order kernels; the numerical example uses unit-power random-phase multisine excitation and compares validation output prediction. This is a direct nonlinear input/output alternative, but a finite Volterra truncation can fail when the proposed high-drive experiment leaves its small-signal range.
- Brunton, Proctor, and Kutz, [*Discovering governing equations from data by sparse identification of nonlinear dynamical systems*](https://doi.org/10.1073/pnas.1517384113), use sparse regression over a supplied candidate function library. It is a strong dynamics-discovery route when state trajectories and their derivatives (or derivative surrogates) are available. It does not solve this single-port hidden-state acquisition problem without additional state reconstruction and library assumptions.
- Rojas, Welsh, Goodwin, and Feuer, [*Robust optimal experiment design for system identification*](https://doi.org/10.1016/j.automatica.2006.12.013), formulate worst-case input design for linear systems under input energy or power bounds and a compact parameter set. This is the closest direct energy-design comparator I found; it is linear, whereas the rescaling calculation depends on the cubic state damping and nonlinear hidden response.
- The current [MathWorks nonlinear grey-box workflow](https://www.mathworks.com/help/ident/ug/estimating-nonlinear-grey-box-models.html) estimates an explicitly supplied nonlinear ODE structure from input/output data by prediction-error minimization. In the pinned N598 report, a full nonlinear ODE fit is the matched computational baseline and outperforms the tested cubic-kernel fit on its three-node finite dataset. My calculation changes the acquisition input and does not show that fitting or recovery becomes easier.

These are not priority-complete literature searches. The precise large-bias rescaling and its quasistatic energy inequality are candidate additions; priority remains unknown.
