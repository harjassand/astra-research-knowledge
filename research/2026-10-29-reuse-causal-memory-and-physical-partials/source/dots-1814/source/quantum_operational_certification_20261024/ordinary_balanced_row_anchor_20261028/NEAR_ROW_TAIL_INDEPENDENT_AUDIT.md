# Independent receiving: weighted approximate-row oracle penalty

28 October 2026. **PASS as the separate approximation-sensitive oracle theorem.**

Reviewed source: `WEIGHTED_NEAR_RANK_ONE_ROW_TAIL_EXTENSION.md`, SHA-256 `960c41787193e3ca53ba2b606eaabde8286797b7e108840956020646c85cc738`. The source and its author checks were read and left unchanged. No correction is required.

This review does not make the older tail theorem a dependency of the already received positive residual-validation construction. The tail theorem assumes a supplied balanced anchor for selected true leading row directions and allows an explicit unknown tail penalty; the validation theorem instead measures the residual of its actually learned directions. Those are different statements.

## 1. Actual compatible purification and model scope

The physical linear encoder and ordinary six-state preparation supply one common purification linear in the real selector. Source Kraus index and probe label can be placed in a shared environment, so row maps G_i exist and the actual diagonal effect is `B_i=Re(G_i^*G_i)`. This is not inferred from arbitrary positivity of a matrix polynomial, and no estimated positive completion is substituted.

For a real unit leading eigenvector u_i, the real PSD matrix `B_i-lambda_i u_i u_i^T` has trace tau_i. Since the input selector and u_i are real, the imaginary antisymmetric part of `G_i^*G_i` contributes zero to every displayed quadratic norm. Thus

`||G_i(I-u_i u_i^T)x||^2=x^T(I-u_i u_i^T)B_i(I-u_i u_i^T)x<=tau_i`.

Summing gives the manuscript's compatible purification residual. The leading-row factor obeys `Phi_x=R_x Phi_x0` exactly, and the supplied leading-direction anchor promise gives `||R_x||<=1/sqrt(kappa)`. Applying the same purification at x and x0 gives the stated `2sqrt(tau_row/kappa)` bound. It does not align unrelated purifications separately at each encoder and does not pinch the payload source.

For zero B_i the whole row map vanishes and its contribution is zero; arbitrary harmless direction conventions may be used. A degenerate leading eigenvalue is allowed if the promised selected leading vector is balanced. Such nonunique cases are necessarily tail-paid rather than well shaped. The learner need not discover which leading vector was selected in this promise.

Unlike the exact-row case, the observation that nonempty exact models require kappa<=1/4 need not be imposed here. The inherited parameter range 0<kappa<=1 suffices for all inequalities. Highly mixed effects can have a chosen leading vector perfectly aligned with the anchor, but their tail penalty may be large.

## 2. Conditional moments, observed certificates and realized counts

Write alpha_i=Tr B_i. The finite fourth design gives the exact conditional matrix

`M_i=(I_4+2B_i/alpha_i)/6`

at a nonzero row, with row probability alpha_i/4. For a well-shaped row, `tau_i<=lambda_i/4`, the second eigenvalue of B_i is at most tau_i. Therefore its conditional gap is

`(lambda_i-lambda_2(B_i))/(3alpha_i)>=1/5`.

No empirical classification of well-shaped rows is used in this argument. The class is a mathematical partition for the proof.

At actual count n>4096L, the same bounded matrix-moment event gives perturbation `t=sqrt(3L/n)<1/32`. The empirical top gap is therefore at least `1/5-2/32=11/80>1/12`, so the inherited observed-gap certificate accepts every high-count well-shaped row on this event. The eigenvector residual bound gives sine error at most `t/(1/5-t)`. The finite rational unit-vector approximation adds at most `sqrt(L/n)/100`. Even using the crude rational bound sqrt(3)<2, the resulting sine is below `12sqrt(L/n)`, giving squared error below `144L/n<1024L/n`. Thus the source's error constant and numerical certificate have slack.

The conditional variance of the rank-one observed projector xx^T is `M_i-M_i^2`, with norm at most 1/4, irrespective of row shape. At the displayed t the Bernstein exponent exceeds L comfortably. Conditioning on the actual label sequence makes the within-row records independent, so there is no extra union over all possible realized counts. The existing conservative L covers the finite row union and the count-tail event.

The lower-count event concerns alpha_i, not merely lambda_i. If `Nalpha_i/4>=8L`, then `alpha_i<=8n_i/N`. A low observed count therefore contributes at most `32768L/N`; a high well-shaped count contributes at most `8192L/N`. Rows of mean below 8L contribute less than `32L/N`. Since lambda_i<=alpha_i, the source's total `2^16 dL/N` bound is valid and includes missing nonzero rows. No minimum alpha_i or lambda_i is required.

## 3. Tail-paid bad rows and actual anchor weights

If a row is not well shaped, `tau_i>lambda_i/4`, hence `Tr B_i=lambda_i+tau_i<5tau_i`. Its estimated eigenvector can be inaccurate or its certificate can fail; only the uniform returned-ratio norm is used.

For a well-shaped row the actual anchor weight is

`w_i=lambda_i(u_i^T x0)^2+t_i0`, with `0<=t_i0<=tau_i`.

The received clipped-ratio argument pays the leading contribution by `32lambda_i e_i/kappa`, including failed anchor tests and low-count fallback. The true ratio vector has norm at most `1/sqrt(kappa)` and the returned vector at most `2/sqrt(kappa)`. The additional actual anchor weight thus contributes at most `9tau_i/kappa`. For a bad-shaped row the entire contribution is at most `9Tr B_i/kappa<=45tau_i/kappa`, regardless of its learned direction.

Summing gives the manuscript's `2^21 dL/(kappa N)+54tau_row/kappa` bound. In fact the well/bad tail partition allows a smaller aggregate tail constant, but no tightening is required. The use of actual w_i is essential: replacing it by the leading weight alone would omit source mass.

## 4. Full-decoder transfer, finite optimization and constants

The leading physical approximation, learned-row error on the same actual anchor, and fresh Bures bank give the three stated root-risk terms for the SAME positive loss operator `(3/2)C^T`, whose norm is at most 3. The total squared tail coefficient is exactly

`3*12+9*54=522`.

The prescribed source and Bures budgets put the statistical part below `gamma epsilon/8192`. Full-CPTP known-coefficient optimization uses the received bound `b=6/kappa` and the same finite feasible SDP repair. The predictor need not be normalized or a source Choi state; the returned decoder must remain CPTP on every record.

Let the selected root excess be `a=2delta+sqrt(nu_opt)`. Then `a^2<=8delta^2+2nu_opt`. Young's inequality at gamma/2, with gamma<=1, charges at most

`24delta^2/gamma+6nu_opt/gamma`.

The tail coefficient is `24*522=12528<2^14`, and the statistical contribution is below epsilon/256. The two statistical failure masses sum to epsilon/128 and cost at most one Bell loss because every fallback is physical. Their sum fits epsilon/64. This proves the displayed expected oracle inequality for nonzero as well as zero comparator loss. Private framing and one separately budgeted complete-process discrepancy give the factor-two tail term and actual unhalved bound. The tail term may be vacuous, as the source explicitly states.

The supplied anchor is fixed before the fresh actual Bures bank, and all state-rank, decoder and control contracts are the unchanged received imports. The source cap is deterministic, includes all rare or failed pilot outcomes, and has no stopping-time or success-probability division. The actual known physical output basis remains load-bearing; generic random frame reduction is not inserted.

## 5. Independent evidence

`near_row_tail_independent_checks.py/.json/.log` is new deterministic reviewer work. It checks:

- 80 exact weighted row inequalities, including 40 failed-anchor fallbacks, effects scaled down to 10^-20, and both well-shaped and tail-paid effects.
- 320 exact conditional finite-design matrix entries, plus 16 finite gap/certificate/count cases.
- 18 actual two-unitary-Kraus source models with 108 encoder probes, including 80 genuinely bad-shaped rows and 28 degenerate-leading-row cases. One physical six-state purification is retained across every encoder comparison.
- 48 exact source-budget and Young-inequality combinations.

All ten entries of the accepted base receipt were reverified. The maximum numerical physical residual is below 7e-16. There were no RNG draws, source calls, sampled trial outcomes, aggregate trial simulations, production SDP executions or quantum hardware runs in these independent checks. The author's own random-parameter physical fixtures are a separate source-disabled diagnostic class; this receipt does not pretend they tested count-pilot realizations or bad-shaped rows.

## Received conclusion and exclusions

The received result is the explicit approximation-sensitive oracle bound with additive `2^14 tau_row/(kappa gamma)` Bell-risk penalty and the corresponding private-framed complete-error penalty. It requires the actual known receiver basis, a supplied anchor balanced against selected true leading directions, stationary resets, the physical compatible lift and the accepted ordinary estimation/decoder controls. It does not certify tau_row from the transcript, establish automatic fast acceptance, acquire an unknown receiver basis, or prove a generic k^2 learner. It neither supports nor is required by the separately received residual holdout and automatic fast-path theorems. The strongest equally informed conventional protocol may use the identical construction.
