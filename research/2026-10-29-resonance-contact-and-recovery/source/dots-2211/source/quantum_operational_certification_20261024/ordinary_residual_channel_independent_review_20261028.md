# Independent receiving: same-record residual-channel acquisition and finite code-library evaluation

28 October 2026. **PASS at the exact corrected source version bound in the companion receipt.** This review is separate from the positive-Bloch acquisition review. It receives a finite local residual-model interface and supplied-library comparison, not generic unknown-code invention or a complete environmental model.

## Governing scope

The source restricts to the stationary product-qubit reduced-channel family with the received canonical positive-Bloch target. Its R has trace one, unlike the earlier general positive-contrast contract. That distinction is necessary for recovering the contraction magnitude, not merely its axes. The residual channel is a one-use reduced physical channel; continuing environmental outputs, future coherent feedback and arbitrary correlated multi-use processes are not described by this product model. Complete receiver-to-fixed-inverse comparison remains a separate theorem.

## Derivation checks

- Exact whitening gives F_j=B_j R/sqrt(c), c=Tr R². Positivity and Tr R=1 yield l=Tr|F_j|=1/sqrt(c), independently of j. Therefore l sqrt(G)=S. For the common mixed input, Tr(B_j rho_J) equals the residual Bloch translation. Neither equality uses an environment inverse or a supplied exact noise model.
- Signed and unsigned estimates can use the same outcomes. Allocating their simultaneous finite-bank confidence event makes every subsequent inequality deterministic on that event. Learned B and the selected code may depend on the data: no unjustified independence or postselection confidence is used.
- Trace-norm Lipschitz continuity gives the displayed e_l=dE+v_l. The contraction estimate is split as (lhat-l)sqrt(Ghat)+l(sqrt(Ghat)-sqrt(G))+lhat Ghat(W0-Ghat^-1/2). The three operator bounds are exactly the displayed D_S. Because the received W0 is a real rational polynomial in Ghat, H0=Ghat W0 really is rational symmetric; multiplying an arbitrary noncommuting inverse-root approximation would require a correction not needed here.
- The affine estimate uses exact physical reflection matrices. Its error is bounded by d a0 from the unsigned operator error plus delta from the operator certificate, uniformly even though both were fitted from the same bank.
- For the normalized qubit Choi convention, the coefficient bound is e>=3 tau+3 sqrt(3) D_S. A 3-by-3 spectral error has entrywise l1 norm at most 3 sqrt(3) times its spectral norm. Each tensor Pauli has operator norm one and trace norm four, yielding Choi operator error <=e/4 and trace-norm error <=e.
- On the confidence event, shifting by (e/4)I and dividing by 1+e gives an exactly TP positive matrix. Its normalized-Choi trace-distance error is at most (e+(3/2)e)/(1+e). The normalized-Choi/input-dimension-two comparison makes this also an upper bound on channel half-diamond error. The numerical coefficient 5/2 and the min-with-one clipping are correct.
- Product-channel hybrid comparison gives Eta<=sum_i eta_i. Uniform channel distance controls every supplied CPTP encoder/decoder score simultaneously, without a union over the library. Two model-to-true replacements, two additive evaluation tolerances and the approximate selection tolerance produce exactly 2 Eta+2 v_eval+v_sel. Learned inverse implementation adds its own uniform zeta once. This is a regret bound against the same supplied library, not an optimal-code oracle.

## A physicality correction required before receipt

The original confidence-radius Choi shift was guaranteed positive only on the confidence event. A bad record could produce a nonpositive matrix while the algorithm called it a physical channel. The author preserved that earlier version and added a mandatory exact all-15-principal-minor PSD check on the 4-by-4 rational Hermitian candidate before output or use. Failure returns ABSTAIN or a fixed depolarizing fallback explicitly carrying no accuracy promise. This makes the procedure defined and physical on every record; on the joint good event the check always passes, so the claimed successful-record bounds are unchanged.

The author also made library descriptions finite rational/algebraic, or certified computable approximations with their precision/error charged. Thus score evaluation is a finite acquired-description calculation rather than an implicit free real-number or channel oracle. Exponential computation in block size/library size remains allowed and explicit; no scalable code optimizer is claimed.

## Independent executable evidence

`ordinary_residual_channel_independent_check_20261028.py/.json` uses an unknown-axis amplitude-damping residual and a nonuniform spectator whose common factor has c=25/64, so whitening normalization l=8/5 is exact rational. It verifies all three normalization and translation identities, two conservative finite contraction/translation certificates, exact TP and all principal-minor positivity tests for repaired channels, and four-candidate selection in each case. It independently exhibits a bad-record affine estimate with t_z=10 for which the unguarded small-radius shift is still nonpositive. The newly required PSD check rejects that case.

Exact algebra establishes identities, matrix positivity and candidate comparisons. Floating norm diagnostics merely illustrate the bound; they are not a substitute for the proof. There are zero acquired source outcomes and zero RNG draws. The author's separate known-matrix tests are bound separately. No generic learner, hardware, full circuit compiler or code search was executed.

## What is added and what is not

The acquired residual model removes a free-exact-noise-model assumption for a supplied finite library. All measurements can be drawn from the same whitening records, but extra unsigned confidence accounting, all-three-axis matrix descriptions, trace-norm arithmetic and every candidate evaluation are paid. The code's useful performance still depends on actual native residual noise and implementation. This source does not learn arbitrary non-product noise, infer hidden memory behavior, certify the structural class from finite data, establish fault tolerance or outperform an equally informed conventional learner. Those remain separate scientific obligations.
