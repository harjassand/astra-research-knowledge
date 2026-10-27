# Challenge to retained-cloud compilation: physical gauge versus statistical precision

27 October 2026. This note checks the parent's retained Gaussian cloud construction and identifies the costs that cannot be omitted. It does not challenge its algebraic validity.

## 1. The positive construction is valid

Let Q=m+E, E~N(0,C), represent an old Gaussian cloud. A child uses center b+A Q and has seed-shift matrix H. Choose a square root P with

    P P^T=I-H A C A^T H^T > 0.

Draw fresh standard Gaussian Z. For analysis define the absorbed seed and refreshed old cloud by

    Z_child=P Z-H A E,
    Q_new=Q+C A^T H^T P^(-T) Z.

Their cross covariance is zero. Both are jointly Gaussian, Z_child is standard Gaussian, and Q_new has mean m and covariance

    C_new=(C^(-1)-A^T H^T H A)^(-1).

The child need not read E: runtime uses b+A Q and PZ, while its pathwise shift identity reduces that computation to the intended exact center and Z_child. Q_new itself is implementable from Q, Z and known matrices. This retains an independent noisier old cloud alongside the standalone child's actual output. The retained cloud and child output remain independent even when the child is merely approximately Gaussian: the child is a function of Z_child and independent private seeds, all independent of Q_new.

Thus the construction genuinely improves on a marginal-output receipt and does not assume a jointly Gaussian relation between an old sampler's output and its original seeds. It uses an old Gaussian error and NEW independent Gaussian seeds. Approximate old-cloud laws still require explicit error propagation, which is handled in the parent's theorem.

## 2. High-noise output reuse can exhaust precision

For one old mean with variance S1^2, child center coefficient a, and gauge norm D/r, feasibility requires

    a^2 S1^2 D^2/r^2 < 1.

After several children sharing this old mean, the exact cumulative condition is

    S1^(-2) > sum_j a_j^2 D_j^2/r_j^2.

In the frozen S1 mean circuit a typical a is a derivative-stencil weight times r_parent/S_parent. Reusing an output whose S1 is comparable to S_parent cancels the favorable small source Lipschitz/noise ratio from the precision condition. Derivative weights, radius cutoffs, and the number of children remain. Internal nodes may therefore require much smaller noise than final-output nodes. Their acquisition must be paid recursively.

Replacing the expression tree by a DAG removes duplicate center evaluations, but it does not by itself show that one global noise assignment is feasible with polylogarithmic total acquisition. A proof must display the assignment and bound every resulting child source/noise ratio and gauge.

## 3. A smaller statistical scale exists, but is not sufficient

Suppose an ideal positive channel, supplied only Q~N(m,C), returns independent Q_new~N(m,C_new) and Y~N(f(b+A m),S_child^2 I). Gaussian score calculus and Fisher-information data processing require

    C_new^(-1)+A^T Df^T Df A/S_child^2 <= C^(-1).

To prove this, the input score is C^(-1)(Q-m), and the output score is its conditional expectation given the outputs. Conditional Jensen bounds the output score covariance by C^(-1). Independence and the specified Gaussian output laws give the displayed left side. Gaussian-smoothed source means are differentiable, so the derivatives here exist analytically; no runtime derivative oracle is being supplied.

For ||Df||<=L, the local statistical scale is L^2/S_child^2. Pathwise gauge absorption instead charges D^2/r^2, potentially larger by order (S_child/(Lr))^2. The information inequality is only necessary. The companion Fourier obstruction proves that it is NOT sufficient: a nonlinear fixed-covariance Gaussian output family cannot be produced exactly from any finite-noise cloud, even when the local Fisher inequality is comfortably satisfied.

## 4. Why extra output noise does not automatically cheapen a pathwise gauge

For a routine whose first physical query is x+r times a unit Gaussian seed projection, preserving the physical query point under x->x+Delta imposes alpha.v=-1 for a unit alpha. Cauchy-Schwarz forces D=|v|>=1. An added final Gaussian output reserve cannot change this constraint on the first query point.

Therefore a high-noise routine can be statistically almost insensitive to its physical center while its query-preserving seed gauge still costs order 1/r^2. This is a restriction of the exact query-preserving interface, not of arbitrary samplers. A routine with a different query parametrization or a weaker law-level shift contract is not covered by this simple argument.

## 5. Consequential next instrument

Retain the valid cloud construction. Its first obligation is a fully charged feasible global precision assignment for the actual recursively acquired circuit. If that fails, a useful replacement is approximate center absorption at the level of the ACTUAL joint law, exploiting paid output smoothing rather than preserving every physical query point. This is a positive heat-deconvolution problem; the companion Fourier bound gives a real accuracy constraint for any such attempt. Another possibility is a source-dependent nonlinear seed transport, but its acquisition cannot be hidden in a conditional-law or derivative oracle.

No general polylogarithmic sampler or target lower bound is claimed here. The frozen fixed-exponent compiler remains an end-to-end competitor, and ordinary source-independent baseline methods retain their usual guarantees.
