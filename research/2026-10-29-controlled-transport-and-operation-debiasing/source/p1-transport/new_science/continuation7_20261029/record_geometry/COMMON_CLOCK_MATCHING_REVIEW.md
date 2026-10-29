# Review: matching common-clock scalar transport law

29 October 2026. Existing Astra P1 `record_geometry` role. Mathematical review only; no new agents or numerical fixtures.

Reviewed actual input:

`COMMON_CLOCK_MATCHING_RARE_TRANSPORT.md`  
SHA-256 `c48892b0024a573b3257889106c4da196a970da19d8a1d855618ef6843f67f90`.

Exact snapshot: `COMMON_CLOCK_MATCHING_RARE_TRANSPORT_REVIEWED_c48892b0024a.md`.

## Verdict

**Accepted.** The corrected-current tilt has the stated `O(1)` adjoint source; its entropy bound closes the canonical-initial activity limit and the matching scalar lower bound. Together with the already reviewed upper and moment estimates, it gives the exact common-clock scalar LDP and SCGF. The stationary closed-gate zero SCGF is also supported. The file explicitly keeps the full common-clock spatial action and a matching deterministic-initial lower bound unproved.

No load-bearing correction was found. In particular, the explicit initial relative-entropy condition prevents the retained-record scope from silently reverting to that of the more permissive upper-bound theorem.

## 1. Adjoint cancellation

On an active transition, native exchange flips both `delta_i` and `u`, hence `d_i(eta^i,sigma)=-d_i(eta,sigma)`. The base rate is unchanged under this exchange. Detailed balance of the canonical reference therefore gives the displayed adjoint source

\[
(L_N^\lambda)^*1=-2N^2\sum_{i\,\mathrm{active}}r_i\sinh(\lambda d_i/N).
\]

The exact identity `sum r_i d_i=0` cancels the linear term. Since the total active rate is `c A<=cN` and `|d_i|<=2`, one possible bound is

\[
\|(L_N^\lambda)^*1\|_\infty
\le(8/3)c|\lambda|^3e^{2|\lambda|}.
\]

The unmodified common-clock generator has zero adjoint source. Neither the clock rate nor a native mixing rate enters this bound. Setting `d_i=0` on inactive bonds is essential to the active-event likelihood convention; the actual file does so.

## 2. Entropy and activity

For the positive comparison density `f_t`,

\[
\frac d{dt}H(f_t\mu_N\mid\mu_N)
=\langle f_t,L_N^\lambda\log f_t\rangle
\le\langle f_t,(L_N^\lambda)^*1\rangle.
\]

The inequality follows directly from `log y-log x<=y/x-1`; stationarity of the tilted law is unnecessary. This gives `H_t<=H_0+C_lambda T`.

The canonical variance `Var(A/N)=O(1/N)` then suffices. For a fixed activity tolerance, its reference bad-event probability is `O(1/N)`, and the binary entropy inequality divides `H_t+log2` by a denominator of order `log N`. The comparison bad-event probability tends to zero uniformly in time when `H_0=o(log N)`. Boundedness of activity gives its integrated convergence in probability. No spectral-gap argument or common-clock hydrodynamic theorem is needed for this scalar step.

The main canonical-times-fair initializer has `H_0=0`. A recorded fixed common sign has `H_0=log2` when the visible initial marginal is canonical. More generally, any conditional sign law above that same canonical visible marginal costs at most `log2`. Conversely, a retained record revealing the full initial occupancy usually creates entropy of order `N`; freshness of future dynamics alone would not justify the lower bound after that conditioning. The actual theorem states the necessary initial-law/entropy condition at the conditional level.

## 3. Typical corrected current and the lower likelihood

Under the tilted law, the base additive current `M` is no longer a martingale. Its new drift has expansion

\[
\sum_i r_i e^{\lambda d_i/N}d_i
=\lambda c(1-\alpha^2)A/N+O_\lambda(N^{-1}).
\]

The scaled martingale remainder has bracket `O(1/N)`. Thus the canonical activity result gives limit `s chi(m)(1-alpha^2)lambda T` for `M/N^2`. The exact path correction to physical circulation remains negligible: its already proved superexponential event transfers under the bounded predictable weak tilt by the likelihood second-moment estimate.

The likelihood uses `lambda M/N`, while its compensator has a vanishing linear part. Its normalized quadratic term is `s chi(m)(1-alpha^2)T lambda^2/2`. These factors agree with the drift and bracket conventions. Choosing the fixed multiplier `lambda=q/[s chi(m)(1-alpha^2)T]` gives the desired typical target and inverse-likelihood lower bound. This choice is valid for the stated fixed `alpha<1`; it is not silently made with a diverging `lambda_N` as `alpha_N` approaches one.

The existing local upper bound applies at the canonical initializer as well. Exponential tightness supplies the closed-set extension. This proves the asserted full scalar LDP, not a full spatial action.

## 4. Moments and endpoint

At every fixed multiplier the native martingale has an `O(N)` log-moment bound, while the common-clock correction terms cost `O(gamma_N)` under the stated stationary reference. Holder's inequality does not require their independence. These envelopes and exponential tightness give the needed exponential-integrability tail bound, so the SCGF follows from the LDP with a justified moment passage.

For `alpha_N ->1`, the reduced native bracket makes its divided log moment vanish. The remaining divided costs are `O(gamma_N/N)` and `O(1/N)`. The stationary mean current is zero, so Jensen supplies the matching zero lower SCGF. The file correctly limits that concluding argument to its stated stationary initialization; the arbitrary-initial superexponential probability bound is a separate result.

## Scope retained

The result is at fixed macroscopic time, even ring size, fixed interior density, and the stated common-clock scaling. The canonical initializer remains a paid/warranted premise. The `o(log N)` entropy extension uses only the actually supplied variance estimate; a larger entropy class would need an explicit stronger concentration estimate. The separate `NEXT_ATTACK_NONLOCAL_CURRENT_MOBILITY.md` is not certified by this receipt and remains a conjectural next connection.

