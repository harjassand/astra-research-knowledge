# Independent audit: quartic path indistinguishability

15 October 2026. **Audit verdict: the scalar inequality is correct under its stated finite-parameter, common-policy, exact-reset model.** The unstable-side moment estimate is uniform in time, and a direct exponential-Lyapunov argument closes the unbounded Girsanov step. The bounded-feedback extension also holds for policies with a well-defined unique nonexplosive law that do not depend on the unknown label. I found no counterexample inside that contract. The result is a conditional mathematical testing lower bound, not a new material capability or a hardware validation.

This is an independent proof check of §6 in `workers/native_computation/REPORT.md`; no Capital files were changed. The exact quartic specialization's historical priority remains unknown.

## Model and scalar moment theorem

Take fixed \(b,\gamma,\mu,\beta>0\), exact \(Y_0=0\), and grant the investigator exact knowledge of these parameters; only the sign label is hidden.

\[
 U_s(y)=\tfrac b4y^4+\tfrac\gamma2y^2,\qquad
 U_u(y)=\tfrac b4y^4-\tfrac\gamma2y^2.
\]

Their curvatures at the reset point are \(U_s''(0)=+\gamma\) and \(U_u''(0)=-\gamma\), a difference of \(2\gamma\).

Allow one common causal policy, independent of the hidden model label, with predictable controls \(g_t\) and \(f_t\) satisfying \(|g_t|\le G\) and \(|f_t|\le F\) for fixed finite constants. Require that the controlled SDE has a unique nonexplosive law. With \(\theta=-1\) for \(U_s\), \(\theta=+1\) for \(U_u\), and \(\sigma=\sqrt{2\mu/\beta}\),

\[
 dY_t=\mu[(g_t+\theta\gamma)Y_t-bY_t^3+f_t]dt+\sigma dW_t.
\]

For \(s(t)=\mathbb E Y_t^2\), Itô's formula gives

\[
 s'(t)=2\mu\mathbb E[(g_t+\theta\gamma)Y_t^2-bY_t^4+f_tY_t]+2\mu/\beta.
\]

Since \(\mathbb E Y^4\ge s^2\), the bound on controls and Young's inequality give, for any \(\eta>0\),

\[
 s'(t)\le 2\mu[-bs(t)^2+Cs(t)+H],\quad
 C=G+\gamma+\eta/2,\quad H=1/\beta+F^2/(2\eta).
\]

The positive root of \(-bs^2+Cs+H=0\) is

\[
 s_* = \frac{C+\sqrt{C^2+4bH}}{2b}.
\]

Scalar comparison from \(s(0)=0\) implies \(s(t)\le s_*\) for every \(t\ge0\), under either model and uniformly over all such policies. Nonexplosion and the moment passage can be justified by stopping at \(|Y|=R\): the generator applied to \(1+y^2\) and to \(1+y^4\) is bounded above by a constant times the corresponding Lyapunov function, because the negative quartic drift dominates the bounded force/gain terms. Standard stopped-Itô and Fatou arguments then supply finite second and fourth moments and the displayed inequality.

With no controls, omit Young's inequality and set \(G=F=0\). The sharper bound is exactly

\[
 q_b=\frac{\gamma+\sqrt{\gamma^2+4b/\beta}}{2b}.
\]

It is the positive equilibrium of \(\dot q=2\mu(\gamma q-bq^2+1/\beta)\). This proves the proposed moment bound with no stationarity assumption and uniformly over every finite or infinite observation horizon.

The reported controlled \(s_*(\eta)\) is valid. A slightly sharper closed comparison can retain the force term: \(s(t)\le s_F\), where \(s_F\) is the unique positive root of

\[
 b s_F^2-(G+\gamma)s_F-F\sqrt{s_F}-1/\beta=0.
\]

Indeed, before Young's inequality the differential bound is \(s'\le2\mu[-bs^2+(G+\gamma)s+F\sqrt s+1/\beta]\); its right-hand side changes sign once from positive to negative as \(s\) increases. This alternative is not needed for the stated theorem. At fixed \(G,F,\gamma,\beta,\eta\), both bounds are \(\Theta(b^{-1/2})\). More precisely, \(s_*(\eta)\sim\sqrt{H/b}\), where \(H=1/\beta+F^2/(2\eta)\), while the sharper retained-force root satisfies \(s_F\sim(\beta b)^{-1/2}\).

## Girsanov step, including Novikov

For a fixed realization of the investigator's independent random seed, the control rule is the same path functional under both labels. On the stable law \(P_s\), the drift difference needed to obtain the unstable drift is \(2\mu\gamma Y_t\). The normalized change is

\[
 \vartheta_t=\frac{2\mu\gamma Y_t}{\sigma}
 =\sqrt{2\mu\beta}\,\gamma Y_t,
 \qquad \tfrac12\vartheta_t^2=\mu\beta\gamma^2Y_t^2.
\]

Here is a direct proof of Novikov rather than an unproved integrability assertion. Under the stable controlled law, for \(a>0\) put \(V(y)=e^{ay^2}\). Its time-dependent controlled generator satisfies

\[
 \frac{L_tV(y)}{V(y)}
 =-2a\mu b y^4
 +[2a\mu(g_t-\gamma)+4a^2\mu/\beta]y^2
 +2a\mu f_ty+2a\mu/\beta.
\]

For every finite \(\lambda>0\), the quartic leading term implies \((L_t+\lambda y^2)V\le K_\lambda V\) for a finite constant uniform in the bounded controls, time, and seed. Stop at \(\tau_R=\inf\{t:|Y_t|\ge R\}\). The stopped Itô formula makes

\[
 e^{-K_\lambda(t\wedge\tau_R)+\lambda\int_0^{t\wedge\tau_R}Y_r^2dr}
 V(Y_{t\wedge\tau_R})
\]

a supermartingale. Since \(V\ge1\), its expectation bounds the exponential integral; nonexplosion and Fatou yield

\[
 \mathbb E_s\exp\!\left(\lambda\int_0^T Y_r^2dr\right)\le e^{K_\lambda T}V(0)<\infty.
\]

Choosing \(\lambda=\mu\beta\gamma^2\) proves Novikov. Girsanov therefore changes \(P_s\) into a law whose coordinate has the unstable drift and the same feedback functional. The assumed uniqueness in law identifies that law with \(P_u\). Under \(P_u\), square integrability of \(\int\vartheta^2dt\) follows from the moment bound, so the stochastic integral in the log likelihood has mean zero. Consequently,

\[
 D(P_u\|P_s)=\tfrac12\mathbb E_u\int_0^T\vartheta_t^2dt
 =\mu\beta\gamma^2\int_0^T\mathbb E_uY_t^2dt
 \le \mu\beta\gamma^2T s_*.
\]

This identity is conditional on the independent policy seed. Because the seed distribution is the same under both hypotheses, the joint seed/path KL is the average of conditional KLs and is bounded by the same constant. Marginalizing the seed can only decrease KL. This handles randomized feedback as well as deterministic feedback.

The native report's alternative localization is also sound if formulated as the two path laws stopped and frozen using the same exit functional: their KL is bounded by the original, unstopped moment integral up to the exit, and the frozen records converge weakly to the full records under nonexplosion; lower semicontinuity then bounds the full KL. It must not rely on claiming that the moment of a frozen process obeys the original killed-process inequality. The direct Novikov proof above avoids that bookkeeping.

For no controls, this gives both orientations by swapping the numerator law, since the same moment bound holds under stable and unstable dynamics. In the notation where \(P_-=P_s\) and \(P_+=P_u\),

\[
 D(P_-\|P_+)\le\mu\beta\gamma^2Tq_b,
 \qquad
 D(P_+\|P_-)\le\mu\beta\gamma^2Tq_b.
\]

The KL is generally below this upper bound; it is not asserted equal to the root-based expression.

## Testing consequence and precise limits

For equal priors, the optimal one-record error is \((1-\mathrm{TV}(P_u,P_s))/2\). Pinsker gives

\[
 P_e^*\ge \max\!\left\{0,\frac{1-\sqrt{\mu\beta\gamma^2Ts_*/2}}2\right\}.
\]

If both type-I and type-II errors are at most \(\delta<1/2\), mapping the path to the decision bit and applying binary data processing instead gives

\[
 D(P_u\|P_s)\ge (1-2\delta)\log\frac{1-\delta}{\delta}.
\]

Thus any such test must satisfy

\[
 T\ge \frac{(1-2\delta)\log((1-\delta)/\delta)}{\mu\beta\gamma^2s_*}.
\]

For fixed positive \(\mu,\beta,\gamma\), fixed finite \(G,F\), fixed finite \(\eta>0\), and fixed dimension, \(s_*=\Theta(b^{-1/2})\). Hence \(T=o(\sqrt b)\) forces the KL upper bound to zero and the equal-prior error to \(1/2\); a fixed target error requires interrogation time at least order \(\sqrt b\). If \(T=\Theta(\sqrt b)\), the bound is only order one and proves no impossibility at that scale. It is a necessary sample-time lower bound, not a sufficient strategy or a lower bound on reset, energy, or fabrication costs.

For finitely many exact-reset trials with deterministic horizons or deterministic caps summing to \(T_{\rm total}\), conditional application per trial and the KL chain rule give the same result with \(T_{\rm total}\), even when later bounded policies depend on earlier records. The per-trial bound is uniform over each common policy. No claim follows here for an unqualified expected stopping time; stopping correlated with the path needs its own argument.

The fixed-parameter limit matters. At fixed \(\gamma\), the unstable minima are \(\pm\sqrt{\gamma/b}\) and the barrier from \(0\) is \(\Delta U=\gamma^2/(4b)\), so the minima coalesce and the barrier vanishes as \(b\to\infty\). The thermally sampled scale from the quartic term is \((\beta b)^{-1/4}\), making the drift difference \(2\mu\gamma Y\) small along typical paths. This is not a high-barrier Kramers limit. If \(\gamma\) grows like \(\sqrt b\) to keep the barrier fixed, the KL upper bound need not vanish. Likewise, if dimension grows with \(b\), the scalar asymptotic does not automatically hold.

The reset assumption is used in the uniform-in-time comparison: with initial second moment \(s(0)=s_0\), the immediate bound is \(s(t)\le\max(s_0,s_*)\), which need not decay with \(b\) for fixed \(s_0>0\). That does not disprove a refined initial-layer result, but the exact-reset proof cannot be carried over as written. Identical nonzero diffusion coefficients are also essential for this path-KL argument: if the noise amplitudes differ, full continuous records have different quadratic variation and can be mutually singular.

The conclusion covers only full observation of the noisy coordinate with the same known \(\mu\) and \(\beta\), exact reset, fixed \(b,\gamma\), and common bounded gain/force feedback. It does not cover an unbounded gain/force, a nonzero hard displacement clamp with force readout, direct observation of the force law, changed temperature/mobility/noise, or a different physical readout. Those are new information or intervention contracts and must be costed separately. Infinite sampling of the stated path and any postprocessing cannot beat data processing.

## Dimension check

The theorem proved above is scalar. A corresponding radial extension in fixed \(d\) dimensions is straightforward but has a dimension-dependent bound. For

\[
 U_{s/u}(x)=\tfrac b4|x|^4\pm\tfrac\gamma2|x|^2,
 \quad dX=\mu[(g_t+\theta\gamma I)X-b|X|^2X+f_t]dt
 +\sqrt{2\mu/\beta}\,dW_d,
\]

with \(\|g_t\|_{op}\le G\), \(\|f_t\|\le F\) and \(X_0=0\), Itô/Jensen gives

\[
 s'(t)\le2\mu[-bs^2+(G+\gamma+\eta/2)s+d/\beta+F^2/(2\eta)],
 \quad s=\mathbb E|X|^2.
\]

Its positive root replaces \(s_*\), and the normalized drift difference again gives KL at most \(\mu\beta\gamma^2T s_*\). Without controls the root is

\[
 q_{b,d}=\frac{\gamma+\sqrt{\gamma^2+4bd/\beta}}{2b}
 =\Theta\!\left(\sqrt{\frac d{\beta b}}\right)
\]

for fixed \(d\). The claim is therefore not dimension-free; if \(d/b\) does not tend to zero, this displayed upper bound does not force the path KL to vanish. This radial \(d\)-dimensional statement is a derived extension, not part of the scalar candidate's exact constant.

## Prior-art boundary

The change-of-measure step is standard. Girsanov's original paper establishes absolute continuity for diffusion processes with identical diffusion matrices and changed drift under its integrability conditions ([Girsanov 1960, DOI 10.1137/1105027](https://doi.org/10.1137/1105027)). Opper treats relative-entropy rates for SDE path measures and explicitly derives the path-measure likelihood with Girsanov ([Opper 2017, DOI 10.1016/j.jcp.2016.11.021](https://doi.org/10.1016/j.jcp.2016.11.021)). These sources support the method, not the quartic moment calculation.

Adaptive experimental design for nonlinear diffusions is also prior art. Hooker, Lin, and Rogers formulate feedback from continuously observed state to maximize expected Fisher information. Their bistable example uses \(V(x)=x^4-2x^2+A e^{-(x/w)^2/2}\) and a finite control alphabet \(u\in\{0,\pm2,\ldots,\pm10\}\); their simulations report more frequent barrier crossing and improved estimates of \(A\) ([arXiv:1210.3739v3](https://arxiv.org/pdf/1210.3739v3), §§2 and 4). This establishes adaptive control and bounded-force probing as incumbent methods. It does not use the present opposite-curvature sign pair or prove a uniform KL upper bound over all such policies.

Potential-barrier crossing for Brownian motion is a classical physical model ([Kramers 1940, DOI 10.1016/S0031-8914(40)90098-2](https://doi.org/10.1016/S0031-8914(40)90098-2)). The explicit stationary points and barrier of this quartic follow by differentiation. Since this construction sends the barrier to zero at fixed \(\gamma\) while increasing \(b\), it should not be sold as new high-barrier metastability or as a new physical material mechanism. A targeted search here did not establish whether the exact pair-specific controlled inequality has appeared before; historical priority remains **UNKNOWN**. The testing inequalities and continuous-path change of measure are standard ingredients. The report's defensible mathematical capital is their audited combination for this explicit opposite-curvature pair under the stated model contract.

## Audit disposition

No counterexample was found within the theorem's scope. The main proof gap one might suspect—the unbounded linear drift difference in Girsanov—is closed by the exponential Lyapunov estimate above; localization is not being treated as a substitute for Novikov without an argument. The moment bound, KL coefficient, Pinsker constant, binary-error threshold, and deterministic multi-trial chain rule are consistent. The necessary time scale is \(\Omega(\sqrt b)\) at fixed parameters. None of this establishes a device, measured physical parameters, practical advantage, or novelty clearance.
