# Scoped review: conditional live/absorbed sensor errors

## Verdict

Section 3 of `ABSORBING_BOUNDARY_EXTENSIONS.md` and `core/absorbing_sensor_robustness.py` are sound at the stated conditional-error scope. Temporal dependence of sensor errors, erroneous early stops and reuse of an exactly reported boundary state do not invalidate the construction. The probability argument needs the usual causal Markov experiment semantics, made explicit below. A merely marginal average error rate is insufficient.

The independent replay checked three representative saved cases, eta = 0, 10^-6 and 10^-4, with exact rational arithmetic. It verified three representative original confidence endpoints, recomputed the modified Schur and form bounds, checked the resulting global matrix domination by all principal minors, and reproduced the positive transport intervals exactly. All checks passed. **No trajectories were generated.** The accepted frozen main-compiler review was not repeated.

## Precise probabilistic premise

Let the history before a trial include all earlier physical actions, reports, stopping decisions and preparations. A genuine preparation at boundary j, or reuse after an exact report of that same boundary, must give the usual source path law from j conditional on this history. Reports are causal and nonintrusive. This is the ordinary controlled Markov-source interpretation; a sensor with advance information about future source randomness would need a stronger joint-law specification.

At each eligible nonboundary report, the conditional chance of confusing alive with absorbed is at most eta, uniformly over the available past. The bound applies after histories in which errors have already occurred. Boundary labels themselves are exact, and the observer takes at most H reports in a trial. Sensor errors may depend on the past, the action, and the current physical state subject to this uniform conditional bound. They need not be independent across time or trials.

## Coupling and early stopping

On the same underlying source trajectory, compare ideal reporting with the actual reporting-and-stopping rule. Up to the first wrong report the two protocols agree, including their stopping decisions. Therefore any disagreement in a saved trial indicator implies that some report among the first H was wrong. Conditioning on the history before the trial and using the conditional error bound at each reached report gives

\[
\Pr(\text{trial indicators disagree}\mid\text{prior history})
\le c=\min(1,H\eta).
\]

No independence between the stopping time and errors is used. The stopping rule must remain causal. If a false absorbed report stops a physically living excursion, the unexecuted continuation to H is a counterfactual path used in the coupling. It is not an extra experimental operation.

A false alive report after real absorption can prolong an observed trial or create an observed pending flag. A false absorbed report can truncate a trajectory that would later return. Both changes are covered by the same disagreement event. The ideal censored return-or-pending indicator still upper-bounds eventual return, as in the accepted main proof.

## Why the existing Chernoff endpoints can be shifted

For any one ideal finite-horizon event with fixed source probability p, let X_n be its observed indicator in trial n. Conditional on all previous trials,

\[
q_-\le \mathbb E[X_n\mid\mathcal F_{n-1}]\le q_+,
\qquad q_-=(p-c)_+,\quad q_+=\min(1,p+c).
\]

For positive lambda,

\[
\mathbb E[e^{\lambda X_n}\mid\mathcal F_{n-1}]
\le 1-q_++q_+e^\lambda.
\]

For negative lambda the same upper bound holds with q_- in place of q_+. Iteration gives the ordinary binomial Chernoff upper tail with mean q_+ and lower tail with mean q_-. No common fixed observed mean, independence, or stationarity of the sensor errors is required.

Consequently, if U and L are the accepted ordinary one-sided Chernoff endpoints computed from the observed count, then

\[
\Pr\{p>\min(1,U+c)\}\le e^{-\ell},
\qquad
\Pr\{p<\max(0,L-c)\}\le e^{-\ell}.
\]

The direction is essential: the upper bound on p uses the observed-count lower-tail domination at p−c, while its lower bound uses the upper-tail domination at p+c. The code applies precisely these shifts to the return, even-return and absorption quantities.

Initial boundary counts are unchanged because a live/dead error cannot create or erase a boundary identity. Their conditional source probabilities remain fixed. Thus kernel-entry, row-mass and structured model-noise bounds need no contamination increment. The 54 acquisition tails retain their original allocation; the four original direct-comparator tails are unaffected. The sensitivity cases do not constitute new data-dependent inference checkpoints: for any valid supplied warranty, the deterministic enlargement of the same confidence construction applies. A warranty stronger than the real instrument satisfies is not certified by this table.

## Why the conditional qualification matters

Consider a source that leaves the boundary and returns deterministically at step two. With probability eta, a latent sensor fault falsely reports absorbed at the first nonboundary observation on **every** trial; otherwise all reports are correct. Each report has marginal error probability eta, but after observing the fault its conditional error probability is one. On the fault event, every observed return indicator is zero although its ideal probability is one. For large N, adding H eta to the ordinary zero-count upper bound does not repair coverage. This counterexample is excluded by the stated uniform conditional warranty and shows why an average instrument error rate cannot be substituted for it.

## Known-boundary reuse and resources

An erroneous live/dead report never supplies a boundary label. A trial stopped by that report therefore receives a genuine preparation before the next trial. If a trial does end with the exact requested boundary label, the source really is at that state, and causal strong Markov reuse remains valid. The same exact preparation formula N minus the number of requested-boundary endpoints plus the final-endpoint bit still applies to receipts collected under this observer.

The saved sensitivity calculation does not produce noisy-source trajectories or a new noisy execution ledger. Its unchanged counts are a deterministic sensitivity exercise; the original instrument also satisfies every displayed upper error warranty because its error rate is zero. For an actual imperfect instrument, its own recorded durations and endpoints determine its resource ledger. The generic caps of H updates/reports and one preparation per trial remain available; the original run's exact costs are not asserted for all noisy runs.

## Executable checks

`replay_absorbing_sensor_review.py` independently accepts the saved cases using Fraction arithmetic and integer square-root enclosures. It does not invoke the source backend or the original sensitivity routine. The three checked uniform point-model bounds are 0.0399059846, 0.0451712088 and 0.3016404368. The transport order remains certified at eta = 10^-6 and is unresolved at eta = 10^-4, matching the saved result.

The reviewed sensitivity result SHA256 is:

`784fe6ab1cc82645fa7b0e07e0dc893f0b37676cf912d6c3f046d8c6919d900a`

The saved independent receipt is `ABSORBING_SENSOR_REVIEW_RESULTS.json`. Acquiring a uniform conditional sensor warranty remains an external calibration task; this proof charges such a warranty explicitly but does not establish it.
