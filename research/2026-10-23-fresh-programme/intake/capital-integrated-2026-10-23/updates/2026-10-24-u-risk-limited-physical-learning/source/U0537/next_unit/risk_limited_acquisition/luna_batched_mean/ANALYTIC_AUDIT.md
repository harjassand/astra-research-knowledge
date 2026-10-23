# Stopped-law and reuse-gate audit

This audit follows the frozen opening in this folder. It does not inspect or rely on another worker's derivation.

## 1. Full stopped-law KL includes adaptive actions, censoring, and stopping

Write \(\Delta=\theta-\theta'\). At a live history \(h\), the policy's action kernel is the same under both parameter values. Given the selected \(a\), let \(q(a)=e^{-\kappa a^s}\). The next observed symbol is death with probability \(1-q(a)\), or survival followed by a Gaussian readout with mean \(\theta a^r\) and variance \(\sigma^2\). The death probabilities agree under \(\theta,\theta'\); the conditional readout KL is \(\Delta^2a^{2r}/(2\sigma^2)\). Hence the one-step observed-symbol KL is
\[
q(a)\,\frac{\Delta^2a^{2r}}{2\sigma^2}.
\]
Applying chain rule to the complete action/readout/death/stopping transcript (policy kernels contribute zero conditional KL) gives, for bounded horizons,
\[
D_{\rm KL}(P_\theta\Vert P_{\theta'})
=\frac{\Delta^2}{2\sigma^2}\,\mathbb E_\theta\!\left[\sum_{t\le M}q(a_t)a_t^{2r}\right]
\le \frac{\Delta^2}{2\sigma^2}\,\mathbb E_\theta\!\left[\sum_{t\le M}a_t^{2r}\right].
\]
Here \(M\) counts attempted exposures, including the attempt that dies; actions after death are absent. The equality follows by summing conditional KL over pre-exposure histories. For an unbounded stopping time it extends by truncation when the reference expected attempt count/information sum is finite. Crucially, it is the *unconditioned full stopped law*: conditioning on completion can create the selection bias in the frozen counterexample.

This also clarifies the notation in the opening: the resource \(E\) should be the predictable attempted-exposure sum \(\sum_{t\le M}a_t^{2r}\), with expectation under the same reference law as the KL. The exact KL uses the smaller survival-weighted sum.

## 2. Hazard/information inequalities

Set \(A=\sum_{t\le M}a_t^{2r}\), \(G=\sum_{t\le M}a_t^s=H/\kappa\).

- If \(s\le 2r\), then \(a^{2r}\le a^s\) for \(0<a\le1\), so \(A\le G\) pathwise.
- If \(s>2r\), put \(q=2r/s\in(0,1)\). For each path, concavity gives \(A=\sum(a_t^s)^q\le M^{1-q}G^q\). Thus pathwise caps \(M\le N,H\le h\) imply \(A\le N^{1-q}(h/\kappa)^q\), and also \(A\le N\).
- Under reference-world *expected* caps, put counting measure \(\mu(B)=\mathbb E_\theta\sum_{t\le M}\mathbf1\{a_t\in B\}\). Its mass is \(\mathbb E_\theta M\), and \(\int a^s d\mu=\mathbb E_\theta G\). Jensen for the concave power \(q\) gives \(\mathbb E_\theta A\le (\mathbb E_\theta M)^{1-q}(\mathbb E_\theta G)^q\), also at most \(\mathbb E_\theta M\). Therefore the displayed minimum in the lead is valid with expected caps evaluated under that same reference world. If caps are pathwise, the pathwise bound is stronger and does not need Jensen.

The event of at least one death is bounded by \(1-e^{-h}\) under a pathwise total-hazard cap: couple the hazard coins along each potential alive history, whose total survival probability is \(e^{-H}\ge e^{-h}\). Under expected hazard \(\mathbb E H\le h\), the elementary per-attempt union bound gives \(P(\text{death})\le\mathbb E H\le h\); it does not give the exponential pathwise guarantee.

## 3. What precision lower bound is actually licensed

For \(\epsilon\le1/3\), compare \(\theta_0=0\) and \(\theta_1=3\epsilon\). An estimate within \(\epsilon\) yields a test by thresholding at \(3\epsilon/2\). If the entire stopped procedure outputs a \(\epsilon\)-accurate estimate with probability at least \(1-\alpha\) in both worlds, its test errors are at most \(\alpha\), so data processing gives
\[
D_{\rm KL}(P_{\theta_0}\Vert P_{\theta_1})\ge d_{\rm Ber}(1-\alpha,\alpha)
=(1-2\alpha)\log\frac{1-\alpha}{\alpha},\quad 0<\alpha<1/2.
\]
Combining with the stopped-law upper bound yields
\[
\mathbb E_{\theta_0}A\ge \frac{2\sigma^2}{9\epsilon^2}
 d_{\rm Ber}(1-\alpha,\alpha),
\]
which has the claimed \(\epsilon^{-2}\log(1/\alpha)\) scale. A death/no-result run must count as failure for this unconditional statement.

If precision \(1-\alpha\) is promised only *conditional on a returned result* \(C\), the same test is accurate conditionally. The KL chain rule gives \(D(P_0\Vert P_1)\ge P_0(C)D(P_0(\cdot|C)\Vert P_1(\cdot|C))\). Thus a lower bound with the confidence factor is still available when \(P_{\theta_0}(C)\ge p>0\), but it carries factor \(p\). A pathwise hazard cap gives survival probability at least \(e^{-h}\) along a planned path; it implies \(p\ge e^{-h}\) only when the source has a finite/a.s.-terminating no-death plan and returns an output whenever that plan survives. An expected cap \(h<1\) similarly gives survival at least \(1-h\), and gives that completion bound only with the same termination/output condition. Hazard control alone cannot force a controller to terminate or return an estimate. Without a lower bound on returned-result probability, conditional accuracy alone does not force unconditional information expenditure. This distinction should be explicit when stating the lower bound.

## 4. Fixed-design upper bound and exponent match

For fixed \(a\) and \(N\) attempted exposures, define \(E_0=2\sigma^2\log(2/\alpha)/\epsilon^2\) and select \(a=(E_0/N)^{1/(2r)}\), requiring \(N\ge E_0\) so \(a\le1\). On completion, \(\bar Y/a^r\) has standard deviation \(\sigma/\sqrt{Na^{2r}}\); the Gaussian tail inequality gives radius \(\epsilon\) with error at most \(\alpha\). Since the amplitude schedule is fixed, completion is independent of every Gaussian noise, with probability \(e^{-H}\), \(H=\kappa N a^s\). Therefore conditional-on-completion coverage is at least \(1-\alpha\), and joint completion/accuracy is at least \(e^{-H}(1-\alpha)\).

For \(s>2r\), \(H=\kappa E_0^{s/(2r)}N^{-(s-2r)/(2r)}\). Solving \(H\le h\) gives exactly the lead's stated exponent
\[
N\ge (\kappa/h)^{2r/(s-2r)}E_0^{s/(s-2r)}.
\]
This matches the Holder information lower bound up to confidence constants when the completion probability stays bounded below. For \(s\le2r\), every path with hazard cap \(h\) has \(A\le h/\kappa\), so arbitrary precision cannot be obtained at fixed hazard by lowering amplitude; increasing duration alone does not defeat the obstruction.

The fixed-design upper claim is sound under the declared Gaussian and hazard premises. It must not be generalized to an arbitrary predictable amplitude or a data-dependent stopping time by simply reusing the fixed-\(N\) z interval.

## 5. Optional stopping is a separate failure mode

Even without hazard, a nominal fixed-sample Gaussian interval is not generally valid at a data-dependent sample size. At \(\theta=0,\sigma=1\), take iid \(Z_1,Z_2\sim N(0,1)\), stop after one observation if \(Z_1>2\), otherwise take two, and use the usual two-sided 95% z interval at the selected sample size. With \(z=1.95996\ldots\), the one-observation stop branch never covers. Write \(W=(Z_1+Z_2)/\sqrt2\); \(Z_1|W=w\sim N(w/\sqrt2,1/2)\). Coverage is exactly
\[
\int_{-z}^{z}\!\varphi(w)\,\Phi(2\sqrt2-w)\,dw\approx0.9352<0.95.
\]
The integral expression is exact; the decimal is numerical quadrature. With the lead's positive per-exposure hazard and fixed amplitude \(a=1\), condition on completing the chosen one- or two-exposure schedule; its survival weight depends on the selected stopping time. As \(\kappa\downarrow0\), conditional coverage tends continuously to the value above, so the miscoverage persists for all sufficiently small positive \(\kappa\). Fixed horizon avoids this issue; otherwise a sequentially valid confidence sequence or explicit stopping-aware likelihood is needed.

## 6. Reuse gate, adaptive targets, and scope

Let \(C\) denote a returned source result and let \(I\) be its interval. Require either conditional coverage \(P(\theta\in I\mid C)\ge1-\alpha\), or state a joint guarantee \(P(C\cap\{\theta\in I\})\ge g\). Choose later controls \(u_t\) as predictable functions of \(I\), source data, and subsequent observed histories. If a trusted envelope \(h_t(\theta,u_t)\) is valid for every candidate \(\theta\in I\), and the gate ensures \(\sum_t\sup_{\vartheta\in I}h_t(\vartheta,u_t)\le b\) on every live path, then on event \(\theta\in I\) the true additive hazard is at most \(b\). Conditional later survival is at least \(e^{-b}\). Under conditional coverage this gives
\[
P(\theta\in I\text{ and later survival}\mid C)\ge (1-\alpha)e^{-b}.
\]
Under only the joint guarantee, the valid conclusion is the unconditional bound \(P(C\cap\{\theta\in I\}\cap\{\text{later survival}\})\ge g e^{-b}\); it is not a conditional-on-completion bound. If an anytime procedure has unconditional miscoverage at most \(\alpha\) and \(P(C)\ge c\), then \(P(C\cap\{\theta\in I\})\ge c-\alpha\), giving total later-valid survival at least \(\max(0,c-\alpha)e^{-b}\). For the fixed-amplitude, fixed-\(N\) source, completion is independent of the Gaussian noises, so conditional coverage is at least \(1-\alpha\), completion probability is \(e^{-H}\), and the total source-and-later guarantee is at least \(e^{-H}(1-\alpha)e^{-b}\).

Selection of one target from the same fixed interval costs no extra multiplicity factor because the hazard bound is uniform over \(I\) at the selected target. Replacing the interval with repeated optional-stopped intervals requires a confidence sequence or an explicit simultaneous bound. Estimating the envelope from the source also requires its uncertainty to be included. The gate is conditional on the physical response/hazard and envelope promises; source survival and a narrow interval do not validate those premises.

## Conclusion

The full stopped-law KL and dose/information frontier survive the audit with the resource sum defined over attempted exposures and reference-law expectations made explicit. The fixed-amplitude/fixed-horizon upper procedure is valid. The key qualification is the confidence event used in the lower bound: unconditional success needs no completion factor; conditional-on-completion success needs a positive returned-result lower bound; a hazard cap supplies a survival lower bound only for a terminating plan that returns an output when it survives. Adaptive survival selection and optional stopping each invalidate a naive fixed-sample survivor interval. A single valid source interval can safely license adaptively chosen later controls under a genuinely uniform, separately trusted risk envelope and predictable cumulative budget.


## Correction note

This file was clarified after adversarial review: hazard caps imply survival bounds, while a returned-result lower bound also assumes the planned source terminates and returns an output on completion. The reuse probability statement now distinguishes conditional interval coverage from a joint completion-and-coverage guarantee; it does not promote the latter to a conditional guarantee. No experiment or numerical result changed.
