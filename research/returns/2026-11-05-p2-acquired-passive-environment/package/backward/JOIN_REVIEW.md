# Review of the new acquired-passive-memory join

## Verdict

The scalar mathematical join is sound under its stated calibrated source, actuator, readout, initial-energy, and potential assumptions. No sign error, hidden reset, missing filtered-kernel correction, or exact-model/numerical-velocity substitution remains in the completed compiler join.

The executed digital trajectory has a conditional uniform error bound **0.0102648972208**. This differs from the floating BDF diagnostic, whose looser exact-model bound omits a numerical solver budget. The physical acquisition witness uses numerical ODE/quadrature sufficient statistics; it is not an interval-validated laboratory experiment or a materialized execution of every raw meter box.

Reviewed files: `../bridge/acquired_passive_bridge.py`, `../bridge/physical_bridge_results.json`, `../forward/passive_FULL_PROOF.md`, `../independent/passive_execution_compiler.py`, and `../independent/passive_compiler_results.json`. This review checks their new interfaces rather than revalidating accepted warm results.

## 1. Interface checks

### Force sign: correct

The physical convention is

\[
 x'+V'(x)+m=f,\qquad m=\int(x-y_\lambda)d\nu.
\]

`report()` evaluates the triangular average of \(f-V'(u)-x'\), so it estimates the **resisting** memory force \(m\), up to paid tracking/potential terms. The bath force is its negative. The code correctly sets

\[
 c=-R_{\rm final\ guard},\qquad q'+V'(q)+\widehat K*q'=f+c.
\]

The compiler correctly verifies \(\rho=q'+V'(q)+\widehat K*q'-f-c\).

### The old-state envelope survives the entire experiment

In this fixture \(x(0)=0\), \(V'(0)=0\), and the initial stiffness ramp is nonnegative. The initial excursion is bounded by \(X_0=G_0/\mu\), where \(G_0=\sqrt{2BE_0}\). Subsequent tracking gives \(|x|\le A+\delta\). Thus

\[
 X_{\rm history}=\max\{X_0,A+\delta\},\qquad
 \int|y_\lambda(t)|d\nu\le G_0+B X_{\rm history}=:G
\]

throughout preparation, calibration, return, and the final guard. This follows from the positive exponential averaging formula for \(y_\lambda\), without accumulation proportional to probe count.

At a probe start with \(|x|\le\delta\), the derivative-memory state \(z=x-y\) has envelope \(G+B\delta\). The code's tracking numerator includes it. The final guard instead uses the \(y\)-relative-to-reference envelope \(G\), as required by the 3Bδ initialization proof. These envelopes are not being conflated.

### The acquired and unfiltered targets are distinguished

The ramp and positive triangular readout acquire

\[
 K_*(t)=\int e^{-\lambda t}c_h(\lambda)d_w(\lambda)d\nu,
\]

another positive mixture of mass at most \(B\), whose effective delay has mean \(h/2+w\). Hence \(\|K-K_*\|_1\le B(h/2+w)\). The fitter's exact certificate applies to \(K_*\); root adds the smoothing allowance to obtain the original-kernel certificate. Frozen modes have both filter factors equal to one. The demonstration's total certificate is approximately \(0.02124183485\), including \(0.006\) smoothing allowance.

### Final initialization is correctly separate

The apparatus returns through a finite ramp and remains retained for the final guard. Its triangular readout has support of length \(2w_i\). The guard uses the conservative denominator \(H_i-2w_i\) and separation \(T+2w_i\). Its forecast error includes

\[
 G(T+2w_i)/(e(H_i-2w_i))+3B\delta,
\]

plus final force-bin approximation, meter bias, position-average bias/noise, known-potential tracking error, and readout noise. Clipping \(c\) to \([-G-2B\delta,G+2B\delta]\) cannot worsen its error to the true bath-force average.

The model starts at reference zero with zero derivative-memory state. The physical coordinate's displacement is paid by \(\delta\). Starting a model at the actual physical coordinate while leaving its memory zero would require the extra \(B\delta\) allowance or replay. The implementation does not make that substitution.

### The actual finite trajectory is the certified object

The compiler imports the learned six-mode rational model and measured bias. It emits 1,024 piecewise-linear segments for exact rational DC force \(7/20\). Fresh-file verification gives

\[
 D_{\rm decoded}=0.398790660435239,\qquad
 \|\rho\|_\infty\le0.000786240803546772.
\]

The bias's 40-bit encoding error is explicitly added. The final bound is

\[
 \max\left\{\delta,
 (\zeta D_{\rm decoded}+\gamma_{\rm encoded}+\|\rho\|_\infty)/\mu\right\}
 =0.0102648972207608.
\]

No BDF velocity, exact-model velocity, microscopic state, or unverified exponential is substituted into this digital certificate. Piecewise-linear derivative jumps are harmless: the path is absolutely continuous and the residual uses an essential supremum.

## 2. Scope details to retain

1. **The compiler adapter is fixture-specific.** Its `main()` fixes \(\mu=1\), \(V'(x)=x+3x^3/20\), and imports normalized fit poles/weights without rescaling. Correct here because \(B=T=1\). Add assertions for those normalizations, or divide poles by \(T\), multiply weights by \(B\), and scale the kernel certificate by \(BT\) before accepting arbitrary source JSON. The parameterized compiler functions are broader than this adapter.
2. **Physical receipts are analytically derived, not machine-verified interval outputs.** ODE propagation, readout quadrature, and physical-budget arithmetic in the witness are floating calculations. Exact fitting and exact trajectory verification remain conditional on supplied physical receipts. Formal verification of every physical-budget bit would require outward evaluation of those receipts too.
3. **Every raw box is costed but not materialized.** The witness represents 79,356,088 force averages by sufficient statistics. A fixed finite ADC range must include the forward theorem's overflow event in the confidence allocation. Do not describe the saved record as an executed finite-ADC capture of all raw boxes.
4. **Preparation capabilities differ slightly.** The witness uses a finite initial stiffness ramp; the forward theorem supplies fixed-stiffness preparation and treats ramping as optional. Label the extra witness capability. Its centering exponent uses \(k+\mu+B\); the universally safe generic argument uses \(k+\mu\), unless true mass is known. This fixture has true mass \(B\), with additional conservative stiffness slack, so this is not a failed fixture certificate.
5. **The witness uses a quintic ramp; the final forward proof presents a septic ramp.** Both are monotone symmetric smoothsteps with the same mean-delay argument. The quintic feedforward center is \(C^{1,1}\), with bounded piecewise acceleration; the septic construction gives a \(C^2\) center. Keep the appropriate constants and regularity with each.
6. **Forcing must match the certified query.** The compiled witness uses exact DC force, so no sinusoid approximation is hidden. Other queries must include force-encoding discrepancy in the residual. The four BDF alternatives are simulated counterfactual branches, not four physical repeat experiments.
7. **Confidence is not multiplied by query count.** One kernel/old-force event supports all admitted common force histories. Arbitrary separately simulated discontinuous feedback laws do not follow. The stated Lipschitz/small-gain extension is the available deterministic feedback result.

## 3. Sound isotropic vector corollary

Assume \(x,y_\lambda\in\mathbb R^d\), known \(\mu\)-strongly convex \(V\), and the **same scalar** positive measure in every direction:

\[
 \dot x=-\nabla V(x)-\int(x-y_\lambda)d\nu+f,
 \qquad \dot y_\lambda=\lambda(x-y_\lambda).
\tag{V1}
\]

Use Euclidean norms and \(E_0=\tfrac12\int\|y_\lambda(0)-x(0)\|^2d\nu\). Then \(G_0\le\sqrt{2BE_0}\), the bounded-history envelope, derivative aging bound, 3Bδ allowance, and positive filtering construction hold unchanged.

### One commanded direction suffices within this assumed class

Choose a unit vector \(a\) and command \(x_r+u(t)a\). Use a full isotropic trap with known vector feedforward

\[
 q_{\rm trap}=x_r+ua+[u'a+\nabla V(x_r)]/k.
\]

Radial tracking uses strong convexity and a bound on \(\|\nabla V(x_r+ua)-\nabla V(x_r)\|\). Project the finite residual measurement onto \(a\). Its ramp signal is \(AK_*\), because \(a^Ta=1\); old-force and tracking errors obey the scalar bounds. One axial experiment therefore estimates the common scalar kernel. This requires full trapping of transverse coordinates. It does not claim that a single uncontrolled port identifies a generic coupled vector system.

The final old force is a vector. Read all \(d\) force/position channels and form \(c\in\mathbb R^d\). For coordinate error budgets \(\eta_i\), use \(\eta=(\sum_i\eta_i^2)^{1/2}\), with e.g. confidence \(\alpha_g/d\) per channel. Sensor effort and precision can depend on \(d\). Shared kernel structure alone does not make the physical cost dimension independent.

### Vector trajectory comparison

Let \(e=x-q\), \(J=-K'\), and \(u=\|e\|\). The isotropic memory gives almost everywhere

\[
 \dot u\le-(\mu+K(0))u+J*u+\|r\|,
\]

because \(e^T[\nabla V(x)-\nabla V(q)]\ge\mu\|e\|^2\) and
\(e^T(J*e)/\|e\|\le J*\|e\|\). The same positive Volterra comparison proves

\[
 \boxed{\sup_t\|x(t)-q(t)\|
 \le\max\{\delta,
 (\zeta\|\dot q\|_\infty+\gamma+\|\rho\|_\infty)/\mu\}.}
\tag{V2}
\]

The model potential \(W=V-c^Tx\) stays strongly convex. Observed and auxiliary states remain in the Euclidean ball of radius
\(D=\max\{\|\nabla V(x_r)-c\|/\mu,F/\mu\}\)
around \(\arg\min W\). A local gradient Lipschitz bound gives \(\|\dot q\|_\infty\le F+(L+2B)D\).

With \(m\) learned poles, this model stores **O(dm)** auxiliary scalar entries and costs O(dm) per modal update, plus the separately paid gradient-evaluation cost. The scalar rational-bisection compiler has not been extended to a vector solver; (V2) certifies any vector path with a sound residual. Do not advertise an implemented vector compiler.

This is a corollary for assumed isotropy, not an empirical test of isotropy. For general matrix-valued memory, the radial convolution inequality need not hold. No general matrix-kernel maximum principle is claimed; the accepted L2 result remains the appropriate broader statement.

## 4. Scientific and practical judgment

The completed join is finite-control acquisition of an unfiltered positive memory kernel, a measured retained slow bias, and an executed nonlinear trajectory with a residual certificate. It does not establish priority for Prony realization, kernel learning, no-reset acquisition, or comparison arguments. The strongest ordinary alternatives remain the primary model-reduction and generalized-Langevin methods cited elsewhere in the programme.

The resource bill is severe: roughly 15,028 physical time units for a one-unit deployment horizon; 79.4 million fine force averages; stiffness about 3.27 million in normalized units; demanding readout precision; and a 266,242-pole fitting dictionary before reduction to six modes. These costs are finite but establish no practical superiority. The constitutive law, energy bound, calibration, and known strongly convex potential remain supplied. No laboratory validation, broad physics discovery, or civilisation-changing consequence has been demonstrated.
