# Stopped-transcript KL and survival-only audit

Scope: derive the acquisition opening's statistical claims under its stated hazard/readout model. The audit treats any death or missing output as failure for a uniform accuracy guarantee. No numerical fixture, source survey, or application claim is included.

## 1. Full stopped-law KL for adaptive amplitudes and stopping

Write \(q(a)=\exp(-\kappa a^s)\) for survival probability at one attempted exposure. Let \(I_t\) indicate that the experiment is alive and has not stopped before step \(t\); if \(I_t=1\), the policy draws \(A_t\in(0,1]\) from a kernel depending on the complete past and its private randomness, attempts the exposure, observes death if it fails, and otherwise observes \(Y_t\). The policy, stopping rule, and private-randomness law are the same under \(\theta\) and \(\theta'\); they cannot use the unknown parameter directly. Let \(M=\sum_t I_t\) count attempted exposures, including the failed one if death occurs. The full transcript includes actions, survival/death symbols, live readouts, stop, and the policy's random seed if exposed.

At a fixed pre-action history and chosen \(a\), the conditional kernel under parameter \(\theta\) is
\[
D\sim\mathrm{Bernoulli}(q(a)),\qquad
Y\mid(D=1,a)\sim N(\theta a^r,\sigma^2),
\]
where \(D=1\) denotes survival. The action-selection kernel has zero KL because it is common. The survival/death symbol also has zero KL because \(q(a)\) is parameter-independent. Conditional on survival, the two Gaussian laws have KL \((\theta-\theta')^2a^{2r}/(2\sigma^2)\). Applying the chain rule to the complete killed/stopped transcript therefore gives, when the sums are integrable,
\[
D_{\rm KL}(P_\theta^{\rm stop}\Vert P_{\theta'}^{\rm stop})
=\frac{(\theta-\theta')^2}{2\sigma^2}
\mathbb E_\theta\!\left[\sum_{t:I_t=1}q(A_t)A_t^{2r}\right]
=\frac{(\theta-\theta')^2}{2\sigma^2}
\mathbb E_\theta\!\left[\sum_{t:I_t=1,\,D_t=1}A_t^{2r}\right]
\le\frac{(\theta-\theta')^2}{2\sigma^2}
\mathbb E_\theta\!\left[\sum_{t=1}^{M}A_t^{2r}\right].
\]
The second equality is the compensator identity for the survival indicator. If the stopping time is unbounded, apply the chain rule to the transcript truncated after \(T\) attempts, then take \(T\to\infty\) using monotone convergence for the nonnegative information sum (or state a finite expected information budget). Stopping decisions are functions/kernels of the observed history and add no separate conditional KL; their information is already in the joint transcript. The death symbol is included, not censored away.

The expectation on the right is under the **same reference law** \(P_\theta\) that orients the KL. Thus a reference-world expected cap \(\mathbb E_{\theta_0}M\le N\), \(\mathbb E_{\theta_0}H\le h\) controls \(D_{\rm KL}(P_{\theta_0}\Vert P_{\theta_1})\); a cap only under \(\theta_1\) does not automatically control this orientation. For a symmetric testing guarantee one may reverse the KL and use a cap under \(\theta_1\), or assume uniform caps. Do not substitute survivor-conditional expectations for these reference-law expectations.

## 2. Reference-world energy bounds

Set \(E=\sum_{t\le M}A_t^{2r}\) and \(H=\kappa\sum_{t\le M}A_t^s\), with both sums over attempted exposures. For \(s\le 2r\) and \(A_t\le1\), \(A_t^{2r}\le A_t^s\), hence \(E\le H/\kappa\) pathwise.

For \(s>2r\), set \(\rho=2r/s\in(0,1)\). With deterministic pathwise caps \(M\le N,H\le h\), Holder and \(A_t^{2r}\le1\) give
\[
E\le \min\left\{N,\;N^{1-\rho}(h/\kappa)^\rho\right\}.
\]
The same inequalities hold for **reference-law expected caps**: use the measure \(d\mu(\omega,t)=\mathbf 1\{t\le M(\omega)\}dP_{\theta_0}(\omega)\) on path-step pairs. Then \(\int1\,d\mu=\mathbb E_{\theta_0}M\), \(\int A^s d\mu=\mathbb E_{\theta_0}H/\kappa\), and \(\int A^{2r}d\mu=\mathbb E_{\theta_0}E\). Holder yields
\[
\mathbb E_{\theta_0}E\le
\min\left\{N,\;N^{1-\rho}(h/\kappa)^\rho\right\}
\]
for \(\mathbb E_{\theta_0}M\le N,\mathbb E_{\theta_0}H\le h\). For \(s\le2r\), \(\mathbb E_{\theta_0}E\le h/\kappa\). This is exactly the budget placement needed by the forward-KL testing argument.

## 3. Binary-confidence precision bound (with death as failure)

Assume a procedure returns an estimate/interval of radius at most \(\epsilon\) only on alive completion and has **unconditional** success probability at least \(1-\alpha\) for every \(\theta\in[-1,1]\); death, noncompletion, or inaccurate output counts as failure. Let \(0<\epsilon<1\) and choose \(\eta>0\) with \(\epsilon+\eta\le1\). Test the two hypotheses
\[
\theta_0=-(\epsilon+\eta),\qquad \theta_1=+(\epsilon+\eta)
\]
by the sign of the returned estimate (assign any fixed decision on death). On a successful estimate the sign is correct with margin \(\eta\), so both type errors are at most \(\alpha\). Data processing to the decision bit gives
\[
D_{\rm KL}(P_{\theta_0}^{\rm stop}\Vert P_{\theta_1}^{\rm stop})
\ge \operatorname{kl}(1-\alpha\Vert\alpha),
\quad 0<\alpha<1/2.
\]
Combining with the full stopped-law bound, with \(\Delta=2(\epsilon+\eta)\), forces under the reference world \(\theta_0\)
\[
\mathbb E_{\theta_0}E\ge
\frac{2\sigma^2}{\Delta^2}\operatorname{kl}(1-\alpha\Vert\alpha)
=\frac{\sigma^2}{2(\epsilon+\eta)^2}\operatorname{kl}(1-\alpha\Vert\alpha).
\]
Taking \(\eta\downarrow0\) gives the necessary energy
\[
E_0=\frac{\sigma^2}{2\epsilon^2}\operatorname{kl}(1-\alpha\Vert\alpha)
=\Theta\!\left(\frac{\sigma^2}{\epsilon^2}\log\frac1\alpha\right)
\]
for small \(\alpha\). If success is only guaranteed **conditional on survival/completion**, with no lower bound on completion probability, this binary reduction does not apply: an arbitrarily rare selected survivor population can have high conditional accuracy while almost all trials die. If alive completion is at least \(1-\beta\) and conditional precision failure is at most \(\alpha_c\), the unconditional success guarantee is at least \((1-\beta)(1-\alpha_c)\), which can be substituted as the total success level.

Combining \(\mathbb E E\ge E_0\) with the preceding energy bounds yields the claimed duration obstruction. For \(s\le2r\), fixed reference expected hazard \(h\) requires \(h/\kappa\ge E_0\), so fixed \(h\) cannot support arbitrarily fine precision. For \(s>2r\), expected caps require both \(N\ge E_0\) and
\[
N\ge (\kappa/h)^{2r/(s-2r)}E_0^{s/(s-2r)}.
\]
Thus at fixed positive \(h\), the duration order is \(\epsilon^{-2s/(s-2r)}\) times the corresponding confidence factor \([\operatorname{kl}(1-\alpha\Vert\alpha)]^{s/(s-2r)}\). These are necessary conditions under the stated Gaussian/hazard model, not an all-model acquisition theorem.

## 4. Expected hazard is not a pathwise survival guarantee

A pathwise cap \(H^*=\kappa\sum A_t^s\le h\) on the full no-death continuation (including the counterfactual continuation after a would-be death) gives a clean risk bound: conditional on that continuation and its readouts/actions, survival through its planned exposures has probability \(e^{-H^*}\), so actual source death probability is \(\mathbb E[1-e^{-H^*}]\le1-e^{-h}\).

An expected cap on the **actual stopped** hazard \(H\) instead directly gives the compensator/union bound
\[
P(\mathrm{death})=\mathbb E\sum_{t\le M}\mathbf 1\{\text{alive before }t\}(1-e^{-\kappa A_t^s})
\le \mathbb E H.
\]
It does not in general justify replacing this by \(1-e^{-\mathbb E H}\). For a deterministic two-attempt schedule with dose \(d>0\) at each attempt, stopping at death or after attempt two, \(P(\mathrm{death})=1-e^{-2d}\) while \(\mathbb E H=d(1+e^{-d})<2d\). Hence \(1-e^{-\mathbb E H}<1-e^{-2d}=P(\mathrm{death})\), although the union bound \(P(\mathrm{death})\le\mathbb E H\) holds. An expected cap is also law-specific: if it is only under a reference parameter, it bounds death under that reference, not automatically under every alternative.

## 5. Live-evidence versus destructive-evidence decomposition

For a more general comparison between worlds \(0,1\), let \(q_i(a)\) be conditional survival probability and \(G_i(\cdot\mid a)\) the live-readout law. At one attempted exposure the complete observation is either death or (survival, readout). Its conditional KL is exactly
\[
\operatorname{kl}(q_0(a)\Vert q_1(a))
+q_0(a)D_{\rm KL}(G_0(\cdot\mid a)\Vert G_1(\cdot\mid a)).
\]
Therefore for the full predictable, stopped policy,
\[
D_{\rm KL}(P_0^{\rm stop}\Vert P_1^{\rm stop})
=\mathbb E_0\sum_{t\le M}\left[
\operatorname{kl}(q_0(A_t)\Vert q_1(A_t))
+q_0(A_t)D_{\rm KL}(G_0(\cdot\mid A_t)\Vert G_1(\cdot\mid A_t))\right],
\]
when integrable. The first term is hazard-symbol evidence; the second is live-readout evidence, weighted by the probability the readout is actually observed. For the opening's Gaussian model, \(q_0=q_1=e^{-\kappa a^s}\), so the hazard term is zero and the live term gives the exact KL in §1. This chain-rule split is for the **joint killed/stopped law**; it does not license an analysis conditional only on eventual survival.

Indeed, under adaptive amplitudes, conditioning on survival to completion generally reweights live histories by their survival likelihood. Along a live path with actions \(a_1(y_{<1}),a_2(y_{<2}),\ldots\), the chance of surviving its exposures is \(\exp[-\kappa\sum_t a_t(y_{<t})^s]\); this depends on earlier readouts whenever later amplitudes depend on them. Thus the survivor-only readout law is a selected, generally non-Gaussian mixture even though each one-step live observation conditional on its action is Gaussian. The full-transcript chain rule above is the valid route.

## 6. Survival-only permission bound

Assume a safe and unsafe world have identical live-output laws and the same policy/randomization, while for every action the unsafe world is weakly more hazardous: \(q_u(a)\le q_s(a)\). Couple their live outputs and policy randomness identically, and use a common uniform survival draw at each attempted exposure, so every exposure survived in the unsafe world is also survived in the safe world. Let \(A_s\) be the event permission is issued alive in the safe world, \(A_u\) the corresponding unsafe event, and \(D_u\) unsafe source death. If \(A_s\) occurs and the unsafe process has not died before that permission time, both histories coincide through the decision and the unsafe policy also grants permission. Pathwise under this coupling,
\[
A_s\subseteq D_u\cup A_u.
\]
Consequently, if \(P_s(A_s)\ge1-\beta\) but \(P_u(A_u)\le\alpha\), then
\[
P_u(D_u)\ge 1-\beta-\alpha.
\]
Use \([1-\beta-\alpha]_+\) when the right side is nonpositive. Monotone hazard ordering is needed for this nested-survival coupling; without it, the stated death lower bound does not follow merely from “hazards differ.” This isolates why survival-only evidence cannot give a strong low-risk permission rule. If live laws differ, the decomposition in §5 identifies a non-destructive evidence channel; it can support a license, but only together with an unconditional completion/confidence guarantee and a separately validated later-risk envelope.
