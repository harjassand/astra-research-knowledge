# Independent receiving review: certified quaternion oracle and finite FTPL
2026-10-29. Governing byte hashes are recorded in the accompanying receipt.

## Decision
Accepted at the following distinct scopes:
1. The six executed physical-bank global optimization intervals are exact rational certificates, with physical SU(2) orientation checked independently.
2. The rational SOS fast path plus exhaustive rational-grid fallback defines a complete finite additive optimization oracle. The SOS fast path alone does not.
3. The finite-bit, fresh-perturbation FTPL controller has the claimed actual-history fixed-comparator regret bound under the stated frame-independent probe, metadata privacy, neutral role scheduling and trusted control premises.

Not accepted or claimed: a generally fast SOS solver, polynomial-in-input-bit-length optimization, an online FTPL quantum execution, practical finite latency, acquired hardware rotation accuracy, a drifting/hindsight/policy-regret comparator, a full end-to-end recovery implementation, historical novelty, or advantage over an equally informed full-path controller. Fast certificates from six banks are not a runtime guarantee for future perturbed queries.

## Physical bank and global certificate
The 90 sufficient bank coefficients multiply nine linear and 81 quadratic rotation terms. Homogenizing with Q=||q||² gives precisely four times the signed cumulative estimator; the 35 homogeneous quartic coefficients are sufficient. I independently calculated R_ab=Tr(sigma_a V sigma_b V†)/2 for V=wI−i(xX+yY+zZ) at 30 exact rational quaternions and compared bank evaluation against stored quartic evaluation. All identities passed. This fixes the transpose/orientation ambiguity operationally.

For each supplied certificate, the exact identity f−lambda Q²=z2^T G z2 and positive rational LDL pivots imply a global lower bound on the unit sphere. The rational unit quaternion gives an exact upper bound. The finder may be numerically inaccurate or get stuck without harming soundness, provided its proposed certificate is checked and the requested rational interval width actually met. Replaying the separate SymPy verifier accepted all six intervals, with mean-objective gaps 8.66e-11 to 1.74e-10. I did not re-execute both 60k acquisition trajectories in this review; I inspected their capture insertion and checked the captured banks/certificates.

The non-SOS quartic's exact monomial argument is valid: zero fourth powers force associated PSD Gram rows to vanish; then absent squared mixed terms force xw,yw,zw rows to vanish, preventing any xyzw coefficient. A numerical weak lower certificate would not alone establish that limitation. Neither degeneracy nor a non-SOS gap is silently treated as oracle success.

## Complete fallback
For degree-four f with coefficient l1 norm A, ||gradient f||2≤4A on the unit ball, since every coordinate has magnitude≤1 and each exponent vector has l2 norm≤4. The stereographic chart covers the hemisphere by u in the unit ball. Nearest grid u=k/m has error at most sqrt(3)/(2m); stereographic chord distance is at most twice that. The quartic is even, so modulo-sign coverage suffices. Thus the author's more conservative interval `min_grid f−2L/m <= min_sphere f <= min_grid f`, L=4A, is valid. All evaluated q and values are rational. The finite grid includes all (2m+1)^3 points, not a heuristic local subset. Positive tolerance and zero polynomial are handled. A point-budget rejection is explicitly not a successful oracle and cannot be relabeled a neutral controller abort.

The full algorithm may put a deterministic finite cap on the optional numerical proposer, then use the complete grid. Its rational arithmetic and number of evaluations are finite. The cost is polynomial in coefficient magnitude/inverse tolerance and applicable numeric horizon/1/p parameters, not their input bit lengths. For p fixed or inverse polynomial, horizon-polynomial existence does not make the degree or constants practically acceptable; it can be far worse than the accepted expert-net learner.

## FTPL proof checked independently
Features x=(phi+1)/2 belong to [0,1]^35; the set need not be convex because all queries minimize linear functions over actual quaternion actions. The coefficient bounds are correct: each Q,R_ab has coefficient l1 norm at most4, so the signed, action-dependent one-shot quartic has l1 norm≤360; ghat has l1 norm≤720. Importance masking gives E||g_t||1≤720 and E||g_t||1²≤720²/p.

For Phi(w)=E_Z min_x(w+Z)·x with a fresh uniform cube perturbation, translating its density changes total variation by at most ||v||1/(2R). Bounded feature coordinates give the stated gradient Lipschitz bound. Concavity and integration give
`<gradient Phi(w),g> <= Phi(w+g)−Phi(w)+||g||1²/(4R)`.
The initial debit is at most dR/4 because min over a subset of [0,1]^d is no less than the sum of negative perturbation coordinates. Also Phi(G_T)≤G_T·x* for each fixed comparator. These establish the exact-optimizer regret after telescoping.

The decisive causal step is valid only because on a probe the actual input/settings and source map do not depend on the current freshly sampled perturbation/frame; on other roles the coefficient update is zero. Conditional on the actual past, current feedback is therefore independent of the chosen perturbation. Future losses may depend on past deployed frames and the actual retained quantum memory. The argument never replaces those histories by a comparator-induced environment and never permits a hindsight-selected comparator when passing from feedback to true physical loss.

For an epsilon-argmin, forward/backward coordinate difference quotients bound its selected coordinate. Averaging and integrating the gradient Lipschitz bound gives `epsilon/h+h/(4R)`. Optimizing h gives sqrt(epsilon/R), with no uniqueness assumption. This is not an assumed T epsilon loss debit. A finite midpoint perturbation differs from a coupled ideal uniform draw by ≤R/M per coordinate. Feature diameter is1, so its epsilon-argmin is an `(epsilon+dR/M)`-argmin for the coupled continuous objective. The continuous random variable exists only in the proof. Finite power-of-two midpoint sampling uses a fixed finite number of private bits.

With the specified rational R within a factor2 of the ideal scale, epsilon_oracle=R/(4T²) and M≥4dT², approximate/rounding debit≤720 and the conservative bound
`E sum delta(C_t) <= E sum delta(C*) +720 sqrt(35T/p)+720`
follows per star edge. No net approximation of the fixed comparator is needed. Actual returned candidates remain rational quaternions. The accepted full-memory operator transfer can consume this actual-history bound, but actual recovery/readiness execution and control precision remain separate obligations.

## Operational boundaries
A complete finite oracle must finish before every deployed query. Fresh candidate-dependent failures, timeouts, or visible computation times can reveal current metadata or alter an internal-clock source; they are not neutral aborts. The theorem correctly requires padding to a deterministic horizon/past-based bound or a genuinely isolated source-clock interface. This can erase any measured fast-path latency advantage. Only ideal requested rotations are supplied by the mathematical quaternion; gate synthesis, finite precision, routing, buffering, and noise are not acquired by the optimization certificate. Both the matching/orbit architecture and the strongest full-path baseline can use this same controller.

## Independent validation artifacts
- `check_orientation.py/.json`: 30 exact physical SU(2)/bank/quartic equalities.
- `replayed/check_certificates.py` and its JSON: all six exact global intervals replayed in a separate directory.
- `check_finite_bias.py/.json`: 100 exact scalar stability inequalities, 32 finite-midpoint cell boundary checks; a legal approximate oracle with expected bias 500 times epsilon shows why an epsilon-only debit is unjustified.
- `WORKING_REVIEW.md`: preliminary independent derivations and stronger fallback constant; superseded in decision/status by this review and receipt.

## Total-interface replay and one implementation correction
The author's subsequently supplied `certified_oracle.py` connects the capped numerical certificate finder to exact verification and the complete grid. I replayed its four declared branches in a copied audit tree: acquired-bank SOS success at 1e-7, exact zero polynomial, forced complete 4913-point grid, and non-SOS fine-target resource-cap failure. No cap failure was reported as a certified optimizer. The uncapped fine non-SOS fallback was not executed.

Review found an input-validation edge: malformed exponent tuples such as `(4,)` could be silently discarded when filling the canonical 35 monomials. The author was asked to reject anything outside four nonnegative integer exponents of total degree four. This does not affect the supplied valid banks or mathematical proof, but the final receipt must bind the corrected public wrapper, not silently certify its malformed-input behavior.

A separate useful resource distinction is persistent state: only 35 cumulative quartic coefficients per edge are needed, plus counters and current candidate. At fixed rational p these coefficients have logarithmic horizon bit length; the exhaustive grid may stream its points. This reduces the growing expert-weight array, not necessarily runtime or total circuit cost.

The wrapper input bug is now fixed in the receipt-bound version: it rejects wrong tuple lengths, non-integral/bool entries, negative exponents and wrong total degree before canonical monomial normalization. I independently replayed five adversarial malformed keys, all rejected, and replayed all four valid interface branches again after the fix. The correction changes no governing mathematical claims or supplied certificate values.
