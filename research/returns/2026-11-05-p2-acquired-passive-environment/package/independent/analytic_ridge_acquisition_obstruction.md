# Analytic low-dimensional response does not imply affordable design acquisition

Independent construction, 5 November 2026. Parent task: choose a fundamentally different, fully earned scientific capability. This branch supplies a complete obstruction and a contrasting constructive operation. It does **not** establish the requested transformative positive endpoint, and makes no novelty claim.

## 1. Operational question and answer

Suppose a controllable d-coordinate system has a scalar response that depends on only one hidden linear coordinate. Does this reduce the experiments needed to find a useful control to polynomial cost?

Not without quantitative information about accessible signal contrast. A response may be entire analytic, bounded, and one-dimensional, with every fixed derivative order bounded by a polynomial in d, yet require exponential total sensing time. This remains true with adaptive controls and unlimited computation. Conversely, an explicit axis-contrast premise permits acquisition of a signed latent direction, realization of every latent control value, and global optimization with a stated finite sensing budget.

This is a transfer of adaptive-experiment indistinguishability to representation learning and inverse design. It distinguishes the complexity of a representation from the cost of learning and using that representation.

## 2. Negative theorem: an analytic hidden direction

Let d>=1 and gamma>0. There are M=2^d possible hidden sign vectors a in {-1,+1}^d. The available control is x in [-1,1]^d, and the response is

\[
f_a(x)=\exp[-\gamma(d-a^\top x)].
\]

Each response is entire analytic, lies in [exp(-2 gamma d),1], and has maximum 1 at x=a. It is a ridge function of the normalized latent coordinate a^T x/d:

\[
f_a(x)=g_d(a^\top x/d),\qquad
g_d(t)=\exp[\gamma d(t-1)].
\]

The experimental primitive is a scalar Gaussian exposure. At call j, choose x_j and duration tau_j>0 using all preceding observations and internal randomness, then obtain

\[
Y_j=f_a(x_j)+\xi_j,\qquad
\xi_j\mid\mathcal H_{j-1}\sim N(0,\sigma^2/\tau_j).
\]

Errors are conditionally independent. Sigma squared has response-squared times time units. The policy uses finitely many calls and obeys the hard budget sum_j tau_j<=T on every possible transcript. Computation, memory, control precision and resets are free in this lower bound, making it favorable to the learner. Adding their physical costs cannot improve the bound.

Fix c with exp(-gamma)<c<1. Success means outputting xhat with f_a(xhat)>=c. Define

\[
q_\gamma=\frac{1+e^{-4\gamma}}2.
\]

For a uniformly random hidden sign vector, every such policy satisfies

\[
\Pr\{\text{success}\}\le 2^{-d}
+\sqrt{\frac{Tq_\gamma^d}{4\sigma^2}}.
\]

If its average success probability is at least 1-delta, where 1-delta>2^-d, then the sharper bound is

\[
\boxed{
T\ge 2\sigma^2q_\gamma^{-d}\,
  \operatorname{kl}(2^{-d}\Vert1-\delta)
}
\]

with binary relative entropy kl(p||q)=p log(p/q)+(1-p)log((1-p)/(1-q)). In particular, the bound applies to uniform success over all a.

### Proof, step 1: useful controls identify the hidden direction

If a and b differ in k>=1 coordinates, then for every control

\[
f_a(x)f_b(x)
=\exp[-2\gamma d+\gamma(a+b)^\top x]
\le e^{-2\gamma k}
\le e^{-2\gamma}<c^2.
\]

Consequently no x can be c-useful for both a and b. The M success regions are disjoint. It is not enough to predict an average response: useful design identifies one of M alternatives.

### Proof, step 2: no control has large average squared signal

Average over all independent signs a_i:

\[
\begin{aligned}
\frac1M\sum_a f_a(x)^2
&=e^{-2\gamma d}\prod_{i=1}^d\cosh(2\gamma x_i)\\
&\le e^{-2\gamma d}\cosh(2\gamma)^d
=q_\gamma^d.
\end{aligned}
\]

The maximum is attained at cube corners. Thus even choosing a point that is excellent for one alternative yields exponentially small average squared response.

### Proof, step 3: price every adaptive observation

Let P_a be the law of the complete transcript, including the policy's internal random seed and final output. Let P_0 be the law under a formal zero-response source. The zero source need not belong to the promised class; it is a reference probability measure.

Conditioned on a fixed preceding transcript, the same policy chooses the same x_j and tau_j under P_0 and P_a. The Gaussian relative entropy for this observation, in the direction P_0||P_a, is tau_j f_a(x_j)^2/(2 sigma^2). The chain rule gives

\[
D(P_0\Vert P_a)
=E_0\sum_j\frac{\tau_j f_a(x_j)^2}{2\sigma^2}.
\]

Average over a before taking the P_0 expectation. Under P_0 the policy is independent of a, so the preceding squared-signal inequality and the hard exposure budget imply

\[
\frac1M\sum_aD(P_0\Vert P_a)
\le \frac{Tq_\gamma^d}{2\sigma^2}.
\]

This is the step that makes the proof apply to arbitrary adaptive control and adaptive exposure allocation. Applying a pointwise nonadaptive argument to the true source's adaptive controls would not justify the same conclusion.

### Proof, step 4: convert information into success

Let E_a be the event that the final output is c-useful for a. Disjointness implies

\[
\bar p=\frac1M\sum_a P_0(E_a)\le1/M.
\]

Let \(\bar s=M^{-1}\sum_aP_a(E_a)\). Data processing and joint convexity of binary relative entropy give

\[
\frac1M\sum_aD(P_0\Vert P_a)
\ge\frac1M\sum_a\operatorname{kl}(P_0(E_a)\Vert P_a(E_a))
\ge \operatorname{kl}(\bar p\Vert\bar s).
\]

When bar s>=1-delta>1/M, monotonicity on that rectangle bounds the right side below by kl(1/M||1-delta). This proves the boxed lower bound. Alternatively Pinsker followed by Cauchy-Schwarz yields the stated success upper bound.

## 3. Exponential cost despite polynomial fixed-order smoothness

Take d>=17, gamma=(log d)/4 and c=1/2. Then exp(-gamma)=d^-1/4<1/2, and

\[
q_\gamma^d=2^{-d}(1+1/d)^d\le e\,2^{-d}.
\]

Therefore

\[
T\ge (2\sigma^2/e)2^d\operatorname{kl}(2^{-d}\Vert1-\delta).
\]

For each fixed derivative order k,

\[
\nabla^k f_a(x)=\gamma^k f_a(x)a^{\otimes k},\qquad
\|\nabla^k f_a(x)\|\le(\gamma\sqrt d)^k.
\]

Thus every fixed-order ambient derivative bound grows only polynomially, with logarithmic factors, while required exposure grows exponentially. This does not claim a dimension-independent bound on the normalized profile slope; its slope is gamma d.

For delta=.05 the computed exact lower bounds on T/sigma^2 are approximately 2.97e5 at d=17, 9.61e9 at d=32, 4.10e19 at d=64, and 7.53e38 at d=128.

### Matching exhaustive operation

Measure each of M corners for

\[
\tau=32\sigma^2\log(2M/\delta).
\]

A Gaussian tail and union bound ensure every measured response is within 1/4 of its true value with probability >=1-delta. Return the corner with the largest estimate. Its true response is at least 1-2(1/4)=1/2.

Total exposure is 32 sigma^2 M log(2M/delta), within a logarithmic factor of the exponential lower bound for fixed delta. A streaming implementation retains only the current best d-bit corner and estimate: O(d) working memory, O(dM) control-writing work, and M reset/setup operations. Physical reset time must be added if applicable. Finite control and digitization errors must be priced as actual response biases; the statement does not silently equate exact real input with finite hardware.

## 4. Which richer interfaces evade or retain the obstruction?

**Exact gradient.** At every x, sign(partial_i f)=a_i. One exact full gradient immediately identifies the hidden direction. The obstruction is about finite absolute sensing noise, not computational difficulty or exact derivative access.

**Noisy fixed-order derivatives.** Suppose an even more generous sensor simultaneously returns all tensor derivatives from order 0 through K, with independent isotropic Gaussian absolute noise sigma^2/tau on every coordinate, in dimensionless normalized units. The squared mean norm is

\[
f_a(x)^2 S_K,\qquad
S_K=\sum_{k=0}^K(\gamma^2d)^k.
\]

Repeating the identical proof gives

\[
T\ge\frac{2\sigma^2q_\gamma^{-d}}{S_K}
\,\operatorname{kl}(2^{-d}\Vert1-\delta).
\]

Fixed K supplies only a polynomial improvement. This grants simultaneous operation of 1+d+...+d^K channels; a channel-time accounting costs more, not less. Derivatives with unequal units/noise require their own calibrated weights.

**Direct log-response.** A genuinely available primitive that measures log f_a with fixed absolute noise has mean -gamma d+gamma a^T x and admits polynomial direction acquisition from axis contrasts. Computing a logarithm after the original noisy f measurement does not manufacture that primitive: uncertainty is amplified by 1/f.

**Active-subspace covariance.** Under uniformly random corners,

\[
C=E[\nabla f_a\nabla f_a^\top]
=\gamma^2q_\gamma^d aa^\top.
\]

Its nonzero eigenvalue is d gamma^2 q_gamma^d, while the supremum squared gradient is d gamma^2. The ratio is q_gamma^-d. This explains why certain sufficient concentration bounds become exponential. It is not itself a necessary direction-recovery bound; the exact gradient example proves that distinction. The sensor-level KL argument is the actual necessity proof.

## 5. Positive theorem with an explicit accessible-contrast premise

Consider the restricted class

\[
f(x)=g(a^\top x/d),\quad a\in\{-1,+1\}^d,
\]

where g is L-Lipschitz on [-1,1]. The same Gaussian exposure primitive is available. Assume an actual known contrast bound

\[
|g(1/d)-g(-1/d)|\ge\Delta_0>0.
\]

This premise is part of the source/instrument contract. It is not inferred from “one latent variable” or from a finite run with favorable outcomes.

### Acquire the latent direction

Measure both +e_i and -e_i for every coordinate, with exposure

\[
\tau_A=\frac{4\sigma^2}{\Delta_0^2}
\log(2d/\delta)
\]

per reading. Their true difference equals a_i D, where D=g(1/d)-g(-1/d) is common to all coordinates. The measured difference has variance 2 sigma^2/tau_A. Its sign is wrong with probability at most exp(-Delta_0^2 tau_A/(4 sigma^2))=delta/(2d). Hence all signs recover b=s a, with one common unknown sign s, with probability at least 1-delta/2.

Total axis exposure is

\[
T_A=\frac{8\sigma^2d}{\Delta_0^2}\log(2d/\delta).
\]

If the contrast contract is Delta_0=2 kappa/d, this becomes 2 sigma^2 d^3 kappa^-2 log(2d/delta). Since g is L-Lipschitz, Delta_0 cannot exceed 2L/d. The statement does not assume a dimension-independent contrast while also holding L fixed.

### Earn the inverse control interface

The learned vector b is itself an available cube control direction. For every t in [-1,1], set x=t b. Then

\[
f(tb)=g(st).
\]

As t runs over the interval, this accesses every possible latent value of the original cube. The common unknown sign causes no loss. The latent representation is therefore actionable; it is not merely a statistical embedding.

### Globally optimize and account for uncertainty

Use K=ceil(4L/epsilon)+1 equally spaced t values in [-1,1]. The nearest grid point to a true maximizer loses at most epsilon/4. Measure each point for

\[
\tau_G=\frac{32\sigma^2}{\epsilon^2}\log(4K/\delta).
\]

All grid measurements have error at most epsilon/4 simultaneously with probability at least 1-delta/2. Choosing the largest estimate loses at most another epsilon/2, so total regret is at most 3 epsilon/4, in particular epsilon, with probability >=1-delta.

The closed operation costs T_A+K tau_G sensing time, 2d+K setup/reset calls, O(d) working memory with streaming comparison, and O(Kd) control-writing arithmetic. If setup consumes t_set per call, add (2d+K)t_set. No claim about actuator energy or readout precision is implicit in this model.

### Finite actuator and digitization accuracy

If every applied coordinate differs from its commanded value by at most eta, the latent coordinate changes by at most eta and the response bias by at most L eta. Axis differences can shift by 2L eta. Under eta<=Delta_0/(8L), conservatively replace Delta_0 by Delta_0/2 in the axis exposure, multiplying that exposure by four.

For grid evaluation and final actuation, the extra regret is at most 2L eta. Requiring eta<=epsilon/(8L) fits the unused epsilon/4 slack. Known digitization bias can be added to the same error budgets, reducing permitted margins as needed. The required number of actuator bits is logarithmic in the inverse tolerances for bounded fixed-point controls, while calibration and setting time remain actual hardware costs.

This is a sufficient operation on the stated signed-direction class. It is not a characterization of all easily learnable ridge functions, nor a claim that axis contrast is necessary. For the hard analytic family, its axis contrast 2 exp(-gamma d)sinh(gamma) is exponentially small, and this axis method can be worse than exhaustive search.

## 6. Numerical checks and limits of verification

The accompanying verify_ridge_acquisition.py verifies the squared-signal identity by exhaustive sign enumeration for d=1,...,12 and checks disjoint-cap products on random distinct directions. Its independent positive simulation uses d=24, sigma=.1, epsilon=.1, delta=.05 and g(t)=sin(2t)+.25t, with L=2.25.

In 300 trials, all hidden signed directions were recovered up to common sign, every trial met the epsilon regret target, and maximum observed regret was .01429. Total prescribed sensing exposure was about 26271.88. These checks corroborate arithmetic and the implementation; the proof supplies the guarantee. They are not physical measurements or an empirical optimality claim.

The script and verification.json preserve exact choices, formulas, random seeds and outputs.

## 7. Strongest prior alternatives and novelty assessment

- Doerr and Mayer, *The recovery of ridge functions on the hypercube suffers from the curse of dimensionality*, establish closely related generic impossibility for uniform ridge-function recovery, including randomized methods. Our optimization target, entire-analytic family and explicit exposure primitive differ, but this is strong prior art against a broad novelty claim. https://arxiv.org/abs/1903.10223
- Fornasier, Schnass and Vybíral, *Learning Functions of Few Arbitrary Linear Parameters in High Dimensions*, give polynomial randomized recovery under additional smoothness/variation and geometric assumptions. This is the positive alternative: low dimension becomes useful through quantitative observability assumptions, not dimension alone. https://arxiv.org/abs/1008.3043
- Holodnak, Ipsen and Smith, *A Probabilistic Subspace Bound with Application to Active Subspaces*, SIAM J. Matrix Analysis and Applications 39(3), 1208–1220 (2018), provide sufficient subspace-sampling bounds involving variation and spectral information. Those bounds must not be restated as necessary sample lower bounds. https://ipsen.math.ncsu.edu/ps/SIMAX114150.pdf
- Jun, Jain, Mason and Nassif, *Improved Confidence Bounds for the Linear Logistic Model and Applications to Bandits*, ICML 2021, address small local variation and associated identification costs in a different response family. This is relevant contemporary prior for the information-cost mechanism. https://proceedings.mlr.press/v139/jun21a.html

The negative proof uses standard KL chain rule, data processing and a carefully chosen analytic packing. The constructive contrast operation uses elementary axis differences and Lipschitz gridding. Neither currently supports a historical novelty claim. Its useful contribution to the parent task is a decisive selection rule: a new scientific theory or capability must earn informative measurements, the usable representation and inverse actuation together. Relabeling a low-dimensional representation cannot supply the missing signal.
