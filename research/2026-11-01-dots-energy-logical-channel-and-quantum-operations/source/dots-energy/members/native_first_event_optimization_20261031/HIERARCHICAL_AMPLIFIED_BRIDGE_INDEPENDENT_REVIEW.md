# Independent review: stable hierarchical bridge and constant-degree preparation

31 October 2026. PASS for these two acquired inner-source improvements and their stated error receiving. They do not silently replace the frozen sharp assembly, its ledger, or a complete kernel-cost analysis.

## Source binding

I read both complete sources and verified their hashes:

- `STABLE_HIERARCHICAL_BRIDGE_BINDING.md`: `63c817ed2b571c1aaa7995cb13a3f56e92bf2b054e475ad5de0687d5de4f80c5`.
- `CONSTANT_AMPLIFIED_BRIDGE_PREPARATION.md`: `c58d3e1e99128ddc3de8c3442d0d6e8666be3a491f86333a259fa356df524061`.

They receive the separately checked elementary bridge law and sharp complete-isometry assembly. This review checks the new actual preparation, hierarchical ordering and finite-error claims rather than inferring them from those earlier results.

## 1. Unified proposal and shared-uniform stability

For t>1/v, the stated lower and upper weights equal the integrals of their envelope pieces after multiplication by the common scalar exp(a t)/v. The lower envelope is v x exp(a/v) on [0,1/v]; the upper is exp(a x) on [1/v,t]. Dividing the target exp(a x)(1-exp(-v x)) by those envelopes gives exactly the stated acceptances. For t<=1/v only the square-root proposal is used, and its direct density calculation gives the same target after acceptance. The common-scalar interpretation of the two weights is needed only at/above the split; the lower-only normalization below the split is irrelevant to its conditional proposal law.

R(z)=(1-exp(-z))/min(1,z) is continuous, bounded below by 1-exp(-1), and globally 1/2-Lipschitz. In the lower proposal a*x0<=1. Thus all pointwise acceptances exceed 1/5, and the two-component formula joins continuously at t=1/v. The stable H=v*Delta*exprel(-a*Delta) avoids subtracting rounded nearly equal quantities or evaluating a large positive exponential.

The quantile of a truncated exponential is nondecreasing and 1-Lipschitz in its truncation endpoint. The proposed remaining-time maps, including both opposite-endpoint mixture branches, therefore have derivative in [0,1]. This property concerns remaining times, not a separately rounded elapsed-time reconstruction.

The exact no-event atom derivative is bounded by a. The opposite-endpoint mixture weight is a probability under the exponential family on [0,1]; its derivative is a bounded-variable covariance and hence has magnitude at most v/4. The lower-component probability above the split has derivative at most 2v and joins the constant value one below it. Acceptance changes along coupled proposals are bounded by the stated constant times v|dt|. Consequently the capped shared-uniform mismatch bound (1+6Rcap)v|dt| is valid, while matching accepted-index outputs differ in remaining time by at most |dt|. This removes the inverse-duration/endpoint powers from this particular source stability argument without asserting a generic conditioning principle.

## 2. Zero durations and hierarchical ordering

The t=0 extension is a limit of the conditional word law: no event for identical endpoints, one required zero-time flip for opposite endpoints. It is not a positive-probability zero-time jump of the unconditioned chain. Retaining the associated zero intervals is correct because the exact source contraction satisfies F(0)=Q/2, and its scalar factor two has already been priced.

Rounding returned remaining times into the current interval yields O(jh) error after j matching transitions. It does not double the error at each recursion. Summed discrete mismatches are therefore O((Rcap+1)vK^2h). QQ counts in matched residences have mean perturbation O(cKh); monotone Poisson quantile coupling bounds count mismatch by the absolute mean difference. Their summed contribution is O(cK^2h).

With matching counts, common relative uniforms and within-residence sorting preserve maximum coordinate errors. All QQ insertions use the same QKQ operator and phase. Their hierarchical residence ordering, with the bordering crossing operators retained even at coincident rounded times, prevents numerical movement across a sector boundary. Swapping labels of two identical QQ insertions has no additional operator meaning. Exact source/H0 interval derivatives then give the stated O((Hs+mu(alpha_H+1))(K+1)^2h) word error.

This is why the anti-tie and inner endpoint floors can be removed here. The argument does not apply to independently colored noncommuting event streams, where changing their relative order would change the operator word. It also does not remove the outer physical-time comparison or its actual continuation costs.

## 3. Closed scalar acceptance and exact coherent amplification

Direct integration gives Zbar=v exp(-at) integral_0^t exp(ax)(1-exp(-vx))dx, which is the displayed difference of nonpositive-exponential expressions. Below the split, proposal normalization gives P=2 Zbar/(v^2t^2); above it, P=Zbar/(L+H). Both branches agree at vt=1, and P tends to one as t tends to zero. The earlier pointwise acceptance bound gives P>=1/5. On the upper branch L+H>=1/2. On the lower branch cancellation is handled by its explicit guard-bit or Taylor budget, not by an acceptance-estimation oracle.

As a diagnostic only, I independently evaluated 100 rate/time instances and compared this formula with direct integration of the two proposal acceptances. The maximum discrepancy was below 8e-13 in ordinary floating arithmetic. The analytic integral and uniform lower bound are load-bearing; these checks do not certify an implemented reversible arithmetic circuit.

For each retained time/rate parameter, the proposal isometry has a good vector with norm sqrt(P). Attenuating by sin(pi/10)/sqrt(P) is a valid contraction and makes this amplitude independent of the parameter. Two ordinary amplitude-amplification iterations yield sin(5*pi/10)=1, requiring five calls to the attenuated proposal or its inverse. The success and clean-input reflections leave the parameter register unchanged. Thus this works uniformly on its coherent superpositions; it is not an argument that first measures time and then normalizes a classical outcome.

A fixed conventional overall sign is chosen so that the final accepted amplitude is positive. No unknown or time-dependent phase can be omitted. The probability is computed from its explicit scalar formula, not by amplitude estimation. The finite implementation costs that arithmetic, the controlled attenuation and the reflections. Constant proposal-call count is not constant reversible gate cost.

## 4. Finite grid, selected means and actual unitary errors

The distinction between source-vector error and selected-word mean error is correct. Removing proposal mass delta_s does not make the coherent preparation vector delta_s-close in norm. Instead, after normalization by P>=1/5, its pushforward word law changes by O(delta_s), together with the coupled error in continuous time. Continuous and discrete time distributions are not being compared in total variation merely because their times are close.

For the actual finite proposal, P_disc differs from the ideal scalar by the charged amount. The same constant-degree rotation calculation gives O(delta_s) coherent preparation failure and 1-O(delta_s^2) accepted amplitude in its finite accepted direction. SELECT assigns zero to this failure flag. PREP-dagger SELECT PREP therefore weights words by the actual finite success probabilities; it does not postselect the physical state. All earlier seeds and flags are retained through the sequential source computation, and their conditional word-law errors add over the cap. Separate actual gate-synthesis errors telescope in operator norm through the implemented PREP/SELECT/PREP-dagger circuit.

The exact accepted conditional law can be analyzed with an infinite classical rejection coupling without implementing that rejection loop quantumly. Before agreement or mismatch, its continuation probability is at most 4/5, and its per-attempt mismatch bound is at most 5v|dt|. Summing gives 25v|dt|, with the stated 64v|dt| allowance covering the atom and opposite-endpoint branches. On matching accepted indices the remaining-time map is nonexpansive. This justifies the improved recursive precision budget while actual execution still uses five proposal calls.

The displayed delta_s, h, strip widths, h_prop and uniform grid budgets account for the O(K) amplified stages. Away from the charged endpoint strips the inverse-exponential and square-root maps have the stated derivative bound. Fresh uniforms price comparison ambiguities; tiny component weights receive squared probability tolerances for amplitude preparation. Small acceptance amplitudes do not cause an inverse-probability cost because the pointwise acceptance itself is bounded below. Finite Poisson scans and zero-overflow behavior remain separately charged. Actual elementary operation counts, not K alone, determine final synthesis tolerances.

The stable capped-rejection routine and the constant-amplification replacement are both valid at their stated costs. The latter removes Rcap from quantum proposal-call count, not from every conceptual proof or from required scalar arithmetic. It supplies a different explicit finite circuit, not an expected-runtime shortcut.

## 5. Receiving boundary

The new source errors fit the existing inner mean-block budget when the specified subdivisions are applied. They do not change the exact positive endpoint weights, physical jump output, aggregate word cutoff, physical count/window cap or outer common-uniform private-clock proof. The actual source is never reset by these routines.

No load-bearing correction is required to either source. Their use in a revised full assembly and resource ledger must explicitly bind these operations and their finite costs. A proposal-call proxy such as 10 S d_A K is not a gate count and does not include Gaussian/LCHS kernels, source encodings or consumer costs. Neither local result establishes a practical crossover, novelty or a new physical capability.
