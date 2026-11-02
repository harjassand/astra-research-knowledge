# Astra independent continuation: from passive spectral control to scalar-power nonlinear port laws

**Status (2 November 2026, Brisbane):** independently constructed exact-real mathematical certificates and executable synthetic experiments; not laboratory acquisition, formal machine verification, historical novelty, general physical advantage, or an AGI/civilisational breakthrough. This continuation has **not** consulted the other roles. Starting Astra input revision **`5489b118101275c81500d823361592c670ec77bb`**. The original previous-round proof and code remain frozen in `independent/gpt6-temporal-port-compression-20261102`; this continuation is a distinct file set.

## 1. Consequence diagnostic and strongest fixed-passive comparator

The prior question was finite noisy scalar acquisition of a collocated symmetric RC step response, followed by global optimization of a future rectangular input on the 24-port simplex. If the entire fixed passive model and experimental interface were perfectly qualified, the outcome would be certified linear system control, not a new operation beyond established positive spectral/moment methods. A conventional method with the SAME 1,956 scalar measurements was personally implemented and tested in `moment_baseline.py`.

Write the acquired normalized step response as

\[
R(t)=\int_{[0,\infty)}e^{-\lambda t}\,dM(\lambda),\qquad dM\succeq0.
\]

For the original RC generator this follows directly by integrating each positive spectral mode over its unit step: `(1-exp(-lambda*t))/(lambda*t) = integral_0^1 exp(-lambda*t*s) ds`. For distinct measured times `t_j`, the matrix Lagrange interpolation polynomial of degree `n-1` obeys

\[
\operatorname{sgn}\left((-1)^n\prod_j(t-t_j)\right)
 \left(R(t)-\sum_j\ell_j(t)R(t_j)\right)\succeq0.
\]

This is a matrix inequality against the **entire positive spectral class**, without a pole grid, an upper relaxation rate or hidden-state data. Each fitted r-by-r matrix has sensor operator error at most `2r*eta` in the original recorded experiment. We propagate the sum of absolute interpolation coefficients times this error, and retain the prior valid positive-spatial residual bound for the 20 unselected ports. Each future bilinear readout `w^T R(t)v` receives a source-valid interval using the PSD gap `U-L`:

\[
\left|w^T\left(R-(L+U)/2\right)v\right|
\le\tfrac12\sqrt{(w^T(U-L)w)(v^T(U-L)v)}.
\]

The future pulse objective is linear over every nonnegative fractional 24-port allocation, so a strictly better certified vertex lower bound dominates every mixture. The ordinary method, evaluated on precisely the same acquired 1,956 readings, chooses port 4 and reports rigorous-model-class gap `0.008618957622297`, better than the first-round certificate `0.008270`. Its proof inequalities hold in exact arithmetic; the executed NumPy matrix coefficient/eigenvalue work is floating diagnostic, not an interval-verified numerical implementation. Source regeneration and calculation used about 4.2–4.9 CPU seconds; no new physical measurements were made. This comparator is itself a feasible elementary dual to full moment-SDP optimization; a more expensive optimized SDP may improve it. **Selection outcome: bank the old linear mechanism.**

## 2. First replacement: physical-audit nonlinear local counterfactuals

### 2.1 Experiment and source contract

An arbitrary finite graph of maximum degree `d` has unknown, independently different edge laws `f_e(0)=0`, `mu <= f'_e(v) <= L`, and known positive grounding `kappa`; at each node the injection is `|g_i|<=G`. The equilibrium is

\[
\kappa x_i+\sum_{e=(i,j)} f_e(x_i-x_j)=g_i
\]

with consistent signs at endpoints. The local controller knows only a rooted graph ball `B_R` and its local injections. Each physically accessible edge can be voltage-clamped: one experiment at signed voltage `v` returns scalar `p_e(v)=v f_e(v)+noise`, absolute error `eta_p`. This does not supply arbitrary edge voltages or the edge law as inputs. For `v!=0`, it produces a current interval of radius `eta_p/|v|`; for tiny `|v|` the bound `|f_e(v)|<=L|v|` is used instead of pretending the power meter is infinitely accurate. The slope bound extends every past observed interval into an envelope for a new candidate voltage. Physical per-edge access, source invariance, settled measurements, ground and derivative caps remain required, not inferred.

### 2.2 The local theorem

Let `z` be **any** untrusted numerical candidate local equilibrium, and calculate an interval enclosure `[r_i^-,r_i^+]` of its local nonlinear residual from actual measured currents. Put `r=max_i max(|r_i^-|,|r_i^+|)`. Because the mean edge Jacobian is an M-matrix with row sum `kappa`, the complete local source family has the deterministic guarantee

\[
\|z-x_{B_R}^*\|_\infty\le r/\kappa.
\]

For any consistent completion outside the supplied rooted ball, the full solution obeys `||x_full||_inf<=G/kappa` by a discrete maximum principle. Missing boundary edges create a residual at most `2dLG/kappa`. The same mean Jacobian inverse has infinity norm at most `1/kappa`; at every interior homogeneous shell the off-diagonal recursion contracts by

\[
q=\frac{dL}{\kappa+dL}<1.
\]

The graph distance from the root to unobserved boundary forcing is `R`. Propagating the contraction across those R layers gives the all-completions theorem

\[
\boxed{\quad |x_o^{full}-z_o|\le \frac r\kappa+\frac{2dLG}{\kappa^2}q^R.\quad}
\]

No absent edge law, absent load, or full global graph needs to be supplied to execute the certificate. The local source graph and actually invoked edge-measurement budget are essential assumptions. All input-power commands, resets and settling times are extra physical costs.

### 2.3 Executed synthetic benchmark

`physical_audit.py` privately generates **12,100 nonlinear network nodes**, independently varying three families of smooth edge laws. Only the **841-node/1,600-edge rooted ball** and a per-edge scalar `power(edge,v)` operation are passed to the controller. It is not allowed access to the oracle's hidden material parameters, global graph, or actual equilibrium. An untrusted constant-conductance numerical model proposes candidates; accepted residuals derive solely from genuine source scalar reports. First 1,351 experiments, then 24 incremental experiments for a previously untested alternative, yield source-conditional scores:

- Center injection plus cost: `[0.0212582553, 0.0292098723]`.
- Neighbor injection: `[0.0070692425, 0.0172517788]`.

The winner is certified with margin **`0.0040064765788`** against every allowed exterior completion. A price of 0.15 makes this a nontrivial source-information task: uniform-slope alternatives satisfying exactly the same ex-ante contract favor **opposite** actions. Numerical held-out full solves agree, including changes to all exterior loads and cutting external graph edges. Total experiments 1,375; number of independently chosen local solve operations 8. Full physical charge per unit dwell is bounded by `0.7664297456` in normalized power×time units; actual equipment reset, isolation and noise calibration not acquired. The computed interval arithmetic used floating operations, not outward-rounded certified numerics.

Established nonlinear residual a posteriori error estimators and domain decomposition are formidable same-data incumbents. They can use the same M-matrix argument and local scalar interval evidence. Hence this is an operationally complete, *conditional* route, not an exclusive algorithmic advantage.

## 3. Without ground: exact conservation, small cycle space, and an information boundary

### 3.1 Tree result (known topology, no ground)

Let a finite tree have positive monotone edge laws `mu<=f'_e<=L`, no ground, and one balanced source/sink current `I,-I`. All branches outside the unique source-to-sink path have **identically zero current** by graph-cut conservation. Each path current is fixed by cuts, irrespective of the unmeasured constitutive functions. Invert each path law with signed scalar power queries and derivative-cone bracketing to obtain a rigorous interval on total source-sink voltage drop.

`gapless_tree.py`: 65,535 nodes, 30 relevant path edges, 65,504 completely unobserved branches, zero ground, 420 physically counted scalar queries at sensor error `1e-6`. Certified voltage drop `[35.8041965639,35.8068322316]` (withheld true `35.8057217339`). Summed bound per one-unit dwell: `549.995392` in the network's normalized power×time units. No current-from-infinity or undisclosed sources allowed. This is Kirchhoff's standard cut law expressed as a physically acquired certificate, not a newly discovered principle.

### 3.2 New core for known low-cycle-rank networks

Choose a spanning tree and `c` chords, let `C` be an `E × c` cycle-incidence matrix of full column rank, and let `I_0` be any known current that satisfies source/sink conservation. Every physical flow is `I=I_0+Cz`. For each independent edge, let `v_e(I)=f_e^{-1}(I)`; a one-dimensional monotone power-query bisection delivers an **interval** enclosing this inverse, without acquiring an explicit expression for the law. The true global potentials require `C^T v(I)=0` (zero cycle voltage sum). The strictly convex Thomson energy in cycle coordinates is

\[
\Psi(z)=\sum_e\int_0^{(I_0+Cz)_e} f_e^{-1}(s)\,ds,\quad
\nabla\Psi=C^Tv(I_0+Cz),\quad
\frac1L C^TC\preceq \nabla^2\Psi\preceq\frac1\mu C^TC.
\]

For any proposed flow `I`, measured inverse voltage midpoints `\hat v` and their certified per-edge halfwidths `\delta_e` give `rho=||C^T \hat v||_2+|| |C|^T\delta||_2`. With `sigma_min(C)>0` and target path readout `p^Tv`, monotonicity yields

\[
\boxed{\left|p^Tv(I^*)-p^T\hat v(I)\right|
\le \|p\|_1\max_{e\in supp p}\delta_e+
\frac L\mu\frac{\|p\|_2}{\sigma_{min}(C)}\,\rho.}
\]

The script uses the slightly sharper initial term `\sum |p_e|\delta_e`. Proof: strong monotonicity bounds `||C(z-z*)||_2<=L||\nabla\Psi(z)||_2/sigma_min(C)`. The inverse response is `1/mu`-Lipschitz; Cauchy-Schwarz yields the rest. No global ground or hidden state identification appears, but the **actual topology** and all chord observations must be supplied.

`gapless_cycles.py`: a 65,535-node tree with three documented chords has 65,537 edges but only 33 effective core edges. An actual source-certified voltage interval `[1.24201824,1.28025738]` is acquired using 1,918 scalar power queries (`eta_p=1e-7`) without querying the other 65,504 tree edges. A later `cycle_reuse.py` caches actual measured current/voltage intervals; tasks with injected currents `0.6,0.61,0.42` use respectively **1,028, 261 and 499 new readings**. The otherwise identical fresh-acquisition solver for `0.61` needs 1,034 new readings. These are pilot-specific acquisition reductions, not generally optimal rates. No unsupplied topology, flow, voltage or law is passed to the controller.

### 3.3 Exact obstruction with unknown remote topology

For any `R`, build two ungrounded two-terminal Ohmic circuits with exactly two labeled parallel branches A and B. Their path lengths are `(K,2K)` in world 1 and `(2K,K)` in world 2, where `K>2R`. Both worlds have `3K` components and vertices, the **same** rooted radius-R neighborhoods at both terminals, all identical local clamped component laws `p(v)=v²`, and the **same complete external terminal impedance** `2K/3`. Thus every number of allowed adaptive local component tests, every terminal current/voltage/power experiment and the full global size are indistinguishable. Yet under a source current of 1, the current through labeled A is `2/3` in one world and `1/3` in the other. A predictor of that branch current has worst-case absolute error at least `1/6`, and the safety decision whether it exceeds `1/2` is undecidable from this observational interface. A separately acquired in-situ branch-current observation or remote topology witness is required. `gapless_pair_boundary.py` provides exact rational checks with K=60, R=12. This is a source-access impossibility, **not** computational hardness.

## 4. Final selected mechanism: acquire a nonlinear terminal response from only *aggregate* power

This mechanism replaces individually accessible edges with a realistic, stronger-relevant operation: the ability to command a complete **m-dimensional terminal current vector** and measure **one total scalar terminal power**, `P(b)=b^T V(b)+noise`. **No individual terminal voltage is observed.** The network has a fixed but wholly unknown internal graph, independent arbitrary nonlinear edge laws, a physically warranted positive uniform ground `kappa`, maximum degree d, `mu<=f'_e<=L` and `|f''_e|<=M2`. No baseline source is present; the same source is allowed to settle/reset between commands; exact command amplitudes or calibrated actuation envelopes are required.

### 4.1 The scalar-to-vector completeness theorem

Let `D` be the hidden graph incidence operator and `B` select m distinct terminals. The actual internal energy (used only **as a proof object**, never supplied) is

\[
E(x)=\frac\kappa2\|x\|_2^2+\sum_e\int_0^{(Dx)_e} f_e(s)\,ds.
\]

With actual equilibrium `x(b)=argmin_x E(x)-b^TB^Tx`, define convex conjugate terminal potential `F(b)=sup_x[b^TB^Tx-E(x)]`. Standard envelope and implicit differentiation give

\[
V(b)=B^T x(b)=\nabla F(b),\qquad
\frac1{\kappa+2dL}I_m\preceq\nabla^2 F(b)\preceq\frac1\kappa I_m.
\]

The genuine measured scalar output is `P(b)=b^T V(b)=b^T\nabla F(b)`. The radial fundamental theorem of calculus therefore gives the **exact operational identification**

\[
\boxed{F(b)-F(0)=\int_0^1\frac{P(tb)}t\,dt.}
\]

Under `f_e(0)=0` and no baseline sources, `F(0)=0`. Thus if two *reciprocal gradient* sources have the same scalar P on every point of a star-shaped domain, **their entire terminal voltage maps are identical there**. This does **not** identify internal graph or edge laws, nor assert that the identity itself is mathematically novel. It establishes an operational quotient: scalar terminal power is information-complete for the gradient response within the qualified class.

### 4.2 Finite noisy power experiments: all error sources explicit

For target vector b, put `h_b(t)=P(tb)/t=b^T V(tb)` for t>0 and `h_b(0)=0`. The node sensitivity `x'(t)` obeys the positive M-matrix inverse bound `||x'(t)||_inf<=||b||_inf/kappa`. Differentiating a second time and using the independent physical bound `|f''_e|<=M2` gives

\[
\boxed{\sup_{t\in[0,1]}|h_b''(t)|
\le M_h(b):=\frac{4dM_2\|b\|_1\|b\|_\infty^2}{\kappa^3}.}
\]

With K equal radial subdivisions and exactly K **actual** scalar observations `\tilde P((j/K)b)`, `j=1,...,K`, the composite trapezoid

\[
\hat F(b)=\frac1K\left[\sum_{j=1}^{K-1}\frac{\tilde P(jb/K)}{j/K}+\frac{\tilde P(b)}2\right]
\]

has source-uniform absolute error

\[
\boxed{\epsilon_F(b)=\frac{M_h(b)}{12K^2}
+\eta_p\left(\sum_{j=1}^{K-1}\frac1j+\frac1{2K}\right).}
\]

The logarithmic harmonic term **pays** for absolute scalar power noise amplified by division by small current scale. If commanded current `b` has an independent error, the source output error must be enlarged; the formula does not grant ideal DAC calibration.

Using `2mK` scalar source measurements at `b±s e_i` and central differencing, the terminal gradient is certified coordinatewise:

\[
\boxed{\left|\hat V_i(b)-V_i(b)\right|
\le\frac{s}{2\kappa}+
\frac{\epsilon_F(b+s e_i)+\epsilon_F(b-s e_i)}{2s}.}
\]

For a requested terminal voltage target c, consider the legitimate convex injection-design objective `J(b)=F(b)-c^Tb` on a supplied compact domain `K_current` (or globally, if allowed). For any proposed feasible b, the **global** regret against the best feasible action is bounded by

\[
\boxed{J(b)-\min_{v\in K_{current}}J(v)\le
\frac{1}{2\alpha}
\left(\|\hat V(b)-c\|_2+\|\delta(b)\|_2\right)^2,
\quad\alpha=(\kappa+2dL)^{-1}.}
\]

The same vector norm bounds the actual terminal target mismatch. Numerical proposals may be arbitrary; the experimental certificate checks only acquired scalar data and independent source-class bounds. The established theory of convex conjugacy, finite differences and a posteriori optimization is the strongest equal-information conventional comparator. It can adopt this same construction. No exclusive solver advantage is claimed.

### 4.3 Complete executed synthetic scalar-power operation

`aggregate_port.py` generates a hidden 16×16 (**256 internal node**) network with 480 heterogeneous nonlinear edges and 6 selected terminals. **Only** `one_scalar_power(b)` is accessible to the controller; the material law, all voltages and the topology remain private. Guaranteed `kappa=1.5, d=4, mu=.25, L=.9, M2=.8`, raw absolute total-power error `eta_p=2e-8`. With K=96 radial queries and finite-difference step `s=.006`, it takes **2,304 physically distinct scalar power settings** to audit two untrusted gradient steps for a six-voltage target; 12 extra source readings belong solely to an isolated naïve-differentiation diagnostic and are not used in the certificate. The accepted current vector is in `aggregate_port_results.json`.

The executed source-conditional bounds are terminal-target Euclidean error `<=0.0262267567433` and global convex objective regret `<=0.0029921160464`. The withheld true six terminal voltages are inside every coordinate interval (largest numerical absolute error `2.92e-6`), and naïvely differencing raw `P` gives approximately **twice** the true terminal voltages in this fixture, rather than the desired port response. Source calculation costs `~2.65 s CPU` on this synthetic network, excluding laboratory voltage/current configuration, equilibration, readout and resets. Sum commanded terminal-current-square across all 2,304 experiments is `342.41937` in normalized units, yielding a conservative bound `228.27958` on summed *static* source power **if each setting lasts one unit of time**. Unknown actual dwell, switching, storage, sensing and setup costs are **not replaced by** this static bill.

### 4.4 A sharp necessary qualification: nonreciprocal sources

The theorem *cannot* be extended to all strictly passive port maps. Let S=diag(2,3) and A=[[0,.4],[-.4,0]], and define `V_±(b)=(S±A)b`. Both maps are strictly passive since `b^T V_±(b)=2b_1²+3b_2²`, but one has a lossless skew/gyrator component. **Every possible** source power experiment yields the same scalar answer for the two worlds; at current b=(1,0), the second output voltage is respectively `-.4` and `+.4`. Any source-power-only estimator has worst-case voltage error at least `.4`, even with infinite precision and calls. `nonreciprocity_obstruction.py` checks this exactly. A different cross-port measurement is essential to recover the antisymmetric component. This is a genuine observational impossibility and prevents silently treating passivity as reciprocity.

## 5. Strongest established alternatives, remaining obligations and research significance

**Strongest matched existing methods:** (i) positive Loewner/moment interpolation for the original fixed linear source, which demonstrably wins our equal-information test; (ii) classical a posteriori nonlinear elliptic residual estimators, domain decomposition, Thomson principles and network inverse schemes for the nonlinear local and cycle constructions; (iii) standard convex conjugate optimisation and gradient finite differences applied to the scalar aggregate-power data. Source contracts and physical query counts, not evocative method labels, decide whether any new capability exists. No claimed monopoly over standard machinery or priority.

**What is actually earned:** a complete source-conditioned scalar measurement to full nonlinear terminal-response *operation*, with a quantitative noisy finite-query implementation and downstream global convex regret; supplemental size-independent local nonlinear and known-low-cycle-rank routes; and two exact information boundaries (unknown remote topology without ground, nonreciprocal power indistinguishability). This is **not** a broad physical discovery or an enabling technology yet.

**Hardest unpaid scientific interface:** independently qualify reciprocity, source invariance, stationarity, ground/curvature or known cycle-topology as applicable and make the **2,304 accurate aggregate-current experiments** or **1,375 local clamp experiments** physically affordable. The first high-leverage next question is whether the scalar-potential programme survives *unknown, long-lived internal memory and nonreciprocal transport* when the additional measurements required to disambiguate them are themselves costly. A terminal scalar power oracle cannot solve that unsupplied problem; the explicit gyrator counterexample rules out any free extension. Another hard demand is simultaneous validity on families of changing/evolving networks with one retained calibration—unsupported here.

## 6. Primary source comparison and provenance

- David Jekel, *Nonlinear Discrete Laplace and Heat Equations for Electrical Networks* (2014): established monotone nonlinear Kirchhoff/convex energy machinery, https://sites.math.washington.edu/~reu/papers/2017/davidj/Nonlinear_Conductances.pdf.
- Allendes, Barrenechea and Rankin, *Fully Computable Error Estimation of a Nonlinear, Positivity-Preserving Discretization of the Convection-Diffusion-Reaction Equation*, SIAM J. Sci. Comput. 39 (2017), https://doi.org/10.1137/16M1092763: strong related a posteriori certificate comparator, not a claimant of the present scalar experiment model.
- Figotin and Vitebsky, *Spectra of Periodic Nonreciprocal Electric Circuits*, SIAM J. Appl. Math. 61 (2001), https://www.math.uci.edu/~afigotin/papers/Figotin_Vitebsky_siam_01.pdf: physical gyrator nonreciprocity and skew impedance, relevant to the obstruction.
- Frozen Astra `N1571` via exact `knowledge/current/packets/N1571.json` at starting SHA and governing `PASSIVE_NETWORK_BINDING.md`, `CONTROL_CONSUMER_PROOF.md`, `INTERVENTION_ORDER_LOWER_BOUND.md`, and the older independent artifact cited above. Sources from later trial workers were not read.

Reproducibility: each code file and output JSON is supplied beside this proof; all source data are synthetic and regenerated deterministically with the recorded seeds. Unit tests validate all numerical included truth checks but do not replace a formal proof or real measurements.