# Independent controls review: growing-selector active effect acquisition

28 October 2026. **PASS.** Bound source: `ordinary_growing_selector_active_effect_acquisition_20261028.md`, SHA256 `136c4f8a83c81ad28f097f3f35adaf1299b0113d4435e860be119ca0668ed202`.

This narrow source-specific review follows the independent construction in `growing_selector_effect_tomography_controls_20261028.md`. No source calls, sampling, new simulations, or changes to received files. The first read source was `f09356012c56536d8d44a9ea6bf57530313606c16785eb9fff29c4af3df53c27`; final precision edits explicitly identify the new m-anchor marginal and separate primitive random bits from the complete decoder's additional samplers. Final refinements also fix the largest allowed dyadic grid (so the bit cap is explicit) and distinguish a perfect scalar-visible encoder from general visibility lambda_best/m. No statistical algorithm or risk constant changed.

## Actual experiment and finite sampler

The unknown object is the actual frozen-receiver PSD effect of a real selector, not an expectation oracle or general circuit landscape. The basis/sign mixture has the required even fourth moments. The source correctly calls it an even/projective design; no unused odd-moment assertion is needed. The mixture is sampled by uniform integers and fair signs, without enumerating its exponential support.

At most two integer draws occur per primitive query. Each capped rejection sampler has failure at most `2^-R`, and `R=ceil log2(2T_max/nu_rng)` bounds their total exhaustion probability. Safe abort is charged, not postselection. The displayed primitive bit cap is correct; the final source separately pays all m-anchor, logical-probe and Clifford randomness in the complete process.

## Rational C, moments and reconstruction

The canonical finite binomial series is exactly rational and commutes with B. Its geometric tail is at most 1/16, and `B^(-1/2)>=I/2` implies `C>=(7/8)B^(-1/2)`, hence `CBC>=(49/64)I` and `C^(-2)<2B`. No unknown source/gauge eigenvalue is inverted.

The experiment prepares the actual normalized Cz and weights its observed y by the exact rational `||Cz||^2`. Thus the moment is exactly unbiased for F=CAC, not for a fictitious ideal inverse-root query. The kernel has squared Frobenius norm `L_m=m^3(m+3)/4`; on good prior histories F<=I, giving the stated variance `L_m/tau`.

The source's tighter batch size 2304, compared with the standalone note's optional conservative 9216, is valid: at radius c/12 it gives failure at most 1/16. A strict-majority cluster selected with exact squared rational distances has error at most c/4. Independence is fresh conditional independence within a fixed stage. The `2^-b` majority tail and union over J are valid.

Exact congruence reconstruction gives error bounded by cB/2. Dyadic rounding contributes at most cB/4, proving the total `3cB/4` bound. The lower and upper PSD guards therefore always pass on statistical good histories. Rational PSD elimination is exact and polynomial; failed histories use a physical default encoder. There is no unproved Loewner-preserving spectral clipping or numerical-failure probability.

## Invariant, finite arithmetic and source cap

The induction `A+tau_j I<=B_j<=aA+2tau_j I`, with `a=1/(1-2c)`, is correct from B0=2I. The upper scalar recurrence closes because `8c+1<=2`. Good envelopes remain below 4I. Final gap-free Rayleigh slack tau_J/2 gives `p(x)<=a lambda_min(A)+(3/2)tau_J`, and `a<=1+gamma/7` is valid.

The geometric sum of `1/tau_(j-1)` and `2^J<16/epsilon` gives exactly the displayed `36864 L_m/(c^2 epsilon)` training cap, equivalent to `9437184 L_m/(gamma^2 epsilon)`. Payload remains additional.

Dyadic update rounding resets envelope bit length. A common grid with `b>=ceil log2[2m/(c tau_min)]` suffices. A degree-K binomial preconditioner has denominator dividing `2^[1+K(b+4)]`; determinant/cofactor bounds give polynomial-bit exact inverse entries. Within a batch, common denominators limit accumulation growth to logarithmic dependence on batch size. Thus exact moments, congruences, comparisons and PSD decisions have finite polynomial arithmetic caps. No eigengap is required for the final known-matrix Rayleigh witness.

## Physical state preparation and complete composition

An m-dimensional selector uses ceil(log2 m) qubits after padding, but arbitrary known amplitudes require O(m) two-level rotations before native compilation, routing and precision overhead. It is not a polylog(m) input oracle. The entire sequence of actual selector preparations, q-logical Clifford inputs, frozen D uses, inverse Cliffords, readouts and final selected-input preparation is covered by one preallocated operational discrepancy. Finite gate approximation compares the full actual adaptive process with the exact rational reference experiment; the latter's moment law is not falsely assigned to imperfect gates.

The count/bit cap includes aborted histories and no refunded calls. Statistical failures, sampler exhaustion and physical compilation discrepancies are separately identified and jointly budgeted. A final physical loss is bounded by one, so exceptional histories do not acquire the large importance-weight norm as a risk multiplier.

## Growing-selector transfer

The new anchor marginal is explicitly the m-anchor Gbar and its resulting rho. Both weighted proxy tails and operator margins must hold for this new rho. State-independent unitary locality tails imply this; a previous four-anchor weighted statement alone would not.

Positive quadratic domination changes the oracle-transfer factor to m. The source substitutes this factor into eta and the approximation floor, preserves kappa as a separately justified operator margin, and retains a counterexample to inferring it from a single perfect encoder with varying gauges. The m-factor witness is valid. The actual global-test-to-Bell conversion, fresh frozen-receiver encoder stage, updated confidence allocation and replacement of—not addition to—the old scalar learner are consistent.

Every literal source call consumes q logical inputs plus ceil(log2 m) selector inputs and n physical outputs. The full m-anchor/global-Clifford random-bit ledger is additional to the primitive's bit formula, explicitly in the same operational budget. Finite-time tails must shrink with m q A_geom and retain their width cost. Same-information conventional learners get the identical method. No generic circuit optimization, family-membership certification or uncharged protected reference is claimed.

No correction remains within this controls/finite-arithmetic/composition scope. This binding closes the current review; it does not initiate further enhancements or sampling.

Binding history: a first receipt command checked the prior source hash and stopped before writing because the final grid/visibility refinements had arrived. This was a version guard, not a mathematical or permission failure. The current receipt is the first successful source-specific binding and uses the final hash above.
