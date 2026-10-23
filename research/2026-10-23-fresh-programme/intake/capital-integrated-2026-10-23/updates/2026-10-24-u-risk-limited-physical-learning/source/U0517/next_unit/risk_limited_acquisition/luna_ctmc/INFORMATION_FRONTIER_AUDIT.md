# Time–hazard–information frontier: independent audit

24 October 2026. First bounded challenge, frozen after reading only `LEAD_OPENING_FROZEN.txt`. This derives the stated frontier, records censoring and finite-control limits, and makes no physical or comparative-advantage claim.

## Full stopped-law information bound

Let exposure (i) be attempted only while alive, with predictable amplitude (a_i\in(0,1]); if it survives, its readout is (Y_i=\theta a_i^r+\sigma Z_i). Write (M) for attempted exposures, including the failed exposure if one occurs, and

`E_att = sum_{i<=M} a_i^(2r)`, `H_att = kappa sum_{i<=M} a_i^s`.

Include actions, private randomization, live readouts, death, and the stopping decision in the transcript. At each step, the action/stopping kernel is identical under two parameter values conditional on the past. Conditional survival/death probabilities are also identical because the hazard law is theta-independent. A surviving Gaussian readout contributes exactly

`KL(N(theta a_i^r,sigma^2) || N(theta' a_i^r,sigma^2)) = (theta-theta')^2 a_i^(2r)/(2 sigma^2)`.

The stopped chain rule therefore gives the exact identity

`KL(P_theta || P_theta') = ((theta-theta')^2/(2 sigma^2)) E_theta[sum_{i<=M} 1{exposure i survives} a_i^(2r)]`

for a finite horizon, and by truncation when the expected information sum is finite. In particular it is bounded by `((theta-theta')^2/(2 sigma^2)) E_theta[E_att]`. A failed exposure is charged in `E_att` and `H_att` but yields no Gaussian information. The death symbol supplies no direct theta information; any indirect selection carried by adaptive actions is already accounted for by the past-readout likelihood terms. This avoids conditioning on the survivor-selected sample as though amplitudes and sample size had been fixed independently of the data.

## Pathwise and reference-expected frontier

Pathwise, `E_att <= M <= N`. If `s<=2r`, then `a^(2r)<=a^s`, so `E_att<=H_att/kappa<=h/kappa`. If `s>2r`, put `p=2r/s<1`; Holder gives

`E_att = sum (a_i^s)^p <= M^(1-p) (H_att/kappa)^p <= N^(1-p) (h/kappa)^p`.

Combining with `E_att<=N` gives the stated minimum. The same inequalities hold under a reference-world expected budget: use the measure on (path, attempted-step) pairs with mass `P_theta(dpath) 1{i<=M}`. Its total mass is `E_theta[M]`, its integral of `a^s` is `E_theta[H_att]/kappa`, and Holder yields the corresponding expected-information bound. A single reference world suffices for a one-direction KL testing lower bound; the resource expectation must be charged under that same law.

For a confidence interval of radius `epsilon` whose unconditional success probability is at least `1-alpha` under every theta, choose two interior parameters separated by `Delta>2 epsilon`. The interval induces a binary test with both errors at most `alpha` (death counts as failure). Data processing gives `KL >= kl(1-alpha || alpha)`. Consequently, under the reference law,

`E_theta[E_att] >= (2 sigma^2/Delta^2) kl(1-alpha || alpha)`.

Letting `Delta` approach `2 epsilon` gives the order `sigma^2 epsilon^-2 log(1/alpha)` for small `alpha` and `epsilon<1`. Combining with the frontier, fixed hazard cannot support arbitrarily small epsilon when `s<=2r`; when `s>2r`, a pathwise or reference-expected cap implies

`N >= (kappa/h)^(2r/(s-2r)) E0^(s/(s-2r))`

up to the testing constant, where `E0` is the required information exposure. The exponent is `2s/(s-2r)` in `epsilon^-1`.

## Censoring and hazard accounting

For a deterministic constant-amplitude plan of (N) attempts with (q=\exp(-\kappa a^s)), completion probability is exactly `q^N=exp(-H_plan)`, where `H_plan=kappa N a^s`. The expected number of observed Gaussian readouts is only `sum_{j=1}^N q^j`, so expected information in the stopped transcript is

`a^(2r) sum_{j=1}^N q^j`,

not the complete-data budget `N a^(2r)`. The latter is nevertheless valid on the event of full completion. This distinction is why an unconditional chance-of-completion factor belongs in the achievable guarantee.

A pathwise cap on the uncensored planned hazard gives `P(death)<=1-exp(-h)`. An expected cap on the *actual stopped* (H_{att}) only gives the union bound `P(death)<=E[H_att]` in general. For example, use constant per-exposure hazard increment `lambda` for up to `N` attempts and stop at first failure: `P(death)=1-exp(-lambda N)` but `E[H_att]=lambda(1-exp(-lambda N))/(1-exp(-lambda))`. At `lambda=0.1,N=10`, these are about `0.632` and `0.664`; `1-exp(-E H_att)` is only about `0.485`, so substituting the realized expected sum into the exponential pathwise formula is invalid. A bound on a separately defined uncensored cumulative hazard can support a different conversion; it must be stated as such.

## Constant-amplitude achievable policy and exact scaling

Let (E_0=N a^{2r}), set `a=(E0/N)^(1/(2r))`, and require (N\ge E_0) so (a\le1). On full completion, the weighted mean estimator has variance `sigma^2/E0` and an exact normal confidence radius `z_(1-alpha/2) sigma/sqrt(E0)`. Thus the exact normal choice

`E0 = sigma^2 z_(1-alpha/2)^2/epsilon^2`

has complete-data coverage `1-alpha`. The opening's simpler sufficient choice `E0=2 sigma^2 log(2/alpha)/epsilon^2` follows from the Gaussian tail bound and has the same order. Since fixed-amplitude survival is independent of the Gaussian readings, the joint event of full completion and valid interval has probability exactly `exp(-H_plan)(1-alpha)` for the exact-quantile choice, with

`H_plan = kappa E0^(s/(2r)) N^(1-s/(2r))`.

For `s>2r`, choosing

`N >= max{ E0, (kappa/h)^(2r/(s-2r)) E0^(s/(s-2r)) }`

makes `H_plan<=h`, matching the lower-bound exponent. If a desired total failure probability is `delta` for both death and interval error, one exact sufficient allocation is choose any `alpha<delta` and set `h=log((1-alpha)/(1-delta))`; then `exp(-h)(1-alpha)=1-delta`. For `s<=2r`, increasing (N) while holding hazard fixed cannot increase `E0` without bound. This is exponent matching, not proof of finite-sample optimality under all censoring-aware designs.

Substituting the opening's tail-bound exposure `E0=2 sigma^2 log(2/alpha)/epsilon^2` gives the explicit sufficient duration

`N >= max{ 2 sigma^2 log(2/alpha)/epsilon^2,
           (kappa/h)^(2r/(s-2r)) [2 sigma^2 log(2/alpha)/epsilon^2]^(s/(s-2r)) }`.

Thus the hazard-limited term scales as `h^(-2r/(s-2r)) epsilon^(-2s/(s-2r)) [log(2/alpha)]^(s/(s-2r))`; using the exact Gaussian quantile replaces `2 log(2/alpha)` by `z_(1-alpha/2)^2`.

## Physical control limits and conventional design boundary

If the smallest nonzero realizable amplitude is (a_*>0), then for `s>2r`

`E_att <= a_*^(2r-s) H_att/kappa = H_att/(kappa a_*^(s-2r))`.

Thus fixed hazard imposes a finite information ceiling even in the nominal weak-probe regime. For `s<=2r`, the existing `H/kappa` ceiling already applies. If each attempted exposure also has a hazard floor (\lambda_0>0), so total hazard includes `lambda_0 M`, then a pathwise cap gives `M<=h/lambda_0` and `E_att<=M`; under an expected cap, `E[M]<=h/lambda_0` and the same information ceiling holds in expectation. Finite amplitude resolution or a per-exposure risk floor therefore removes the arbitrary-weak-probe limit.

This matches the constrained-optimal-design boundary conceptually. Under pathwise `M<=N`, `H<=h`, for `s>2r` the map (x\mapsto x^{2r/s}) is concave, so equal (a_i^s) maximizes total Gaussian information at fixed count and hazard; the constant-amplitude policy reaches the Holder envelope. For `s<=2r`, information per hazard is maximized at the largest allowed amplitude. A likelihood-aware optimal design can still improve exact constants and confidence/death tradeoffs, especially with heterogeneous control costs; the derivation establishes the scaling frontier against arbitrary adaptive choices, not dominance over such a design.
