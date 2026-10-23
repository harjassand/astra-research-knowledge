# Independent challenge opening: survival selection and reuse gate

**Frozen:** 2026-10-24, after reading only the lead opening and before reading other worker files or sources.  
**Scope:** exact analytical audit; no implementation, parameter sweep, or downstream benchmark.

## Counterexample to arbitrary adaptive survivor-conditioned confidence

Take the lead model with \(r=1,s=2,\theta=0\), \(a_1=1\), and \(Y_1=\sigma Z\), \(Z\sim N(0,1)\). Choose the second amplitude predictably as
\[
a_2=\begin{cases}\delta,&Y_1/\sigma\le -1,\\1,&Y_1/\sigma>-1,\end{cases}\qquad 0<\delta<1.
\]
Condition on surviving exposure 1 (which is independent of \(Y_1\), since \(a_1\) was fixed) and then on surviving exposure 2. Let \(q_\ell=e^{-\kappa\delta^2}\), \(q_h=e^{-\kappa}\), and \(z_{.975}=1.95996\ldots\). The usual single-observation Gaussian interval \([Y_1-z_{.975}\sigma,Y_1+z_{.975}\sigma]\), valid with 95% coverage before survivor selection, has conditional coverage
\[
\frac{q_\ell[\Phi(-1)-\Phi(-z_{.975})]+q_h[\Phi(z_{.975})-\Phi(-1)]}
{q_\ell\Phi(-1)+q_h[1-\Phi(-1)]}.
\]
Along any joint limit with \(\delta\downarrow0\), \(\kappa\to\infty\), and \(\kappa\delta^2\to0\), survivors are selected almost entirely from \(Z\le-1\), and this coverage tends to
\[
\frac{\Phi(-1)-\Phi(-z_{.975})}{\Phi(-1)}\approx 0.8425,
\]
not 0.95. For example, \(\kappa=3,\delta=0.1\) gives approximately 0.870. (The displayed formula gives the exact finite-parameter value.) The high-amplitude second exposure is more hazardous precisely on histories with less-negative first readout; conditioning on completion therefore selects the first readout. This is a two-exposure counterexample, not a challenge to valid inference that models the selection or uses a fixed design.

## Fixed-design condition that restores the stated guarantee

For fixed \(a\) and exactly \(N\) attempted exposures, continue until death or completion. The survival coins are independent of the Gaussian noises; the all-\(N\)-survive event has probability \(e^{-\kappa Na^s}\) and is independent of the counterfactual vector \((Z_1,\ldots,Z_N)\). Conditional on completion, the observed Gaussian sample mean thus has its ordinary distribution and its predeclared Gaussian interval retains coverage \(1-\alpha\). Joint completion-and-coverage is at least \(e^{-\kappa Na^s}(1-\alpha)\). The fixed amplitude and fixed horizon, rather than generic “survivor confidence,” do the work.

## Initial reuse-gate challenge

If a completed source yields a single interval \(I\) with coverage \(1-\alpha\) under the actual declared source law, a later control \(u=g(I,\text{source data})\) may be selected adaptively without a new multiple-comparisons penalty, provided a separately justified envelope holds uniformly over every \(\theta\in I\) and selected control: \(h_e(\theta,u)\le \sup_{\vartheta\in I}h_e(\vartheta,u)\). A predictable pathwise sum of these envelope bounds no larger than remaining budget \(b\) then bounds later hazard on the same coverage event. If the interval is repeatedly updated or optional-stopped using later outcomes, use a simultaneous confidence sequence; if the envelope is learned/selected from the same data, its uncertainty also needs uniform coverage. The gate transfers a valid interval; it does not validate the physical response, hazard, or envelope premises.

This opening targets the lead's analytical claims, not the estimator's novelty. I will check the full-history stopped-law KL and reference-budget Holder bounds independently after this freeze.
