# Independent kinetic information and certificate audit

## Verdict

The central finite-model certificate is internally consistent under its stated assumptions. I independently derived the reversible mass/conductance comparison, checked it on a rational 16-state model, replayed the acquisition equations for both 18-bit transcripts, and rebuilt the finite-response obstruction. These checks support the conditional mathematics; they do not validate the model class for a physical system.

The strongest practical boundary is that the advertised information economy is bought with structural promises and an expensive physical interface. The model supplies an exact pairwise energy law, a positive degree-at-most-two Boolean attempt-rate law, a specified single-site reaction, and preparations that preserve the original conditional clock. Those promises are not inferred from the finite observations. A cubic invisible-clock construction changes the mean by a factor of about 180,755 while preserving every degree-0/1/2 context query. A separate exact preparation-control example gives identical prepared downhill observations but different unprepared means.

The source packet reports A and B with the same equilibrium energy law but different context-dependent mobility: A's interval is about `[148838921.69,148841714.38]`, B's is about `[230236128.13,230236140.69]`, and the exact certificate ratio `B_lower/A_upper` exceeds `1.54685216`. My independent transcript reconstruction confirms that the clock inputs differ while the energy transcript matches; I did not independently solve the full 18-bit killed systems from scratch.

For the implemented comparison, the full-state preconditioned solver is better: on the same acquired model B and the same 1.05 enclosure target, its reported single-run time is 3.26 s versus 6.58 s for the tensor candidate, and its interval is tighter. The candidate uses a compressed representation, but no measured peak-memory or energy advantage follows. No laboratory measurements or physical context preparation were performed. The finite-error analysis itself estimates about 9.6e20 model-time units of expected dwell for its illustrative 1e-8 absolute-rate precision, before reset and clamping costs.

## Certificate reconstruction

Write the true stationary mass as `rho = rho0*w/Z`, where `rho0` is the normalized product of local block laws and `Z=<w,1>_{rho0}`. For the killed reversible generator, the weighted symmetric positive operator is `A = w(-Q+k)`, and the equilibrium-conditioned mean is

`tau = <w,A^{-1}w>_{rho0}/Z`.

The source comparison uses a reference `C` with local heat-bath conductances and the same reaction. On a flip edge with reference endpoint masses `m0x,m0y`, mass multiplier values `wx,wy`, and attempt multiplier `a/a0`, the conductance ratio is

`(a/a0) * ((m0x+m0y) wx wy)/(m0x wx + m0y wy)`.

If `1 <= w <= Rm` and `1 <= a/a0 <= Rk`, the middle factor lies in `[1,Rm]`: subtracting the denominator from its numerator gives nonnegative terms, and subtracting the numerator from `Rm` times the denominator also gives nonnegative terms. Thus every edge ratio lies in `[1,Rm Rk]`; the reaction ratio is `w`, in `[1,Rm]`. Summing edge and reaction quadratic forms gives `C <= A <= R C`, `R=Rm Rk`.

For any trial vector `v`, let `r=w-Av`. Completing the square gives

`<w,A^{-1}w> = 2<w,v>-<v,Av> + <r,A^{-1}r>`.

The variational term is therefore a lower bound. If `C >= alpha I`, then `A >= alpha I` and `0 <= <r,A^{-1}r> <= ||r||^2/alpha`; this gives the matching residual upper bound. The source also uses a two-source identity for point response. With `r_j=b_j-Av_j`, its correction is `<r1,A^{-1}r2>`. From `0<=A^{-1}<=alpha^-1 I`, the operator `2 alpha A^-1-I` is a contraction, so this cross correction is centered at `<r1,r2>/(2 alpha)` with radius `||r1|| ||r2||/(2 alpha)`. My exact rational checks include outward rational square-root bounds.

The independent 16-state fixture verified the three form inequalities `A-C >= 0`, `R C-A >= 0`, and `C-alpha I >= 0` by exact rational pivot tests. Its exact mean is `3.131386055948447...`; the equilibrium residual interval and a point-source two-solve interval both contain their exact rational answers. The checker separately recovers a degree-two clock law on all eight contexts from seven acquired contexts. Full values and fractions are in `independent_check_results.json`.

## Reverse-relaxation acquisition and costs

At context `y`, let `r=W(1,y)/W(0,y)`. The reversible heat-bath rates are `q01=a r/(1+r)` and `q10=a/(1+r)`. Preparing the less probable state and reading its downhill rate gives `d=a max(1,r)/(1+r)`, so `a=d(1+r)/max(1,r)` and `a/2 <= d <= a`. This removes the uphill Boltzmann suppression from the clock readout only if the prepared state has the original conditional microscopic law.

For a degree-two multilinear attempt law, values at the empty, singleton, and pair contexts determine all coefficients by Möbius differences. At `n=18`, this is `18*(1+17+choose(17,2))=2772` downhill queries; pairwise energy recovery adds `1+18+choose(18,2)=172` energy queries. I independently parsed the A and B transcripts, reconstructed the pairwise weights, recomputed all downhill rates and preparation bits, and checked all recovered coefficients. A's attempts range from `1/2` to `2`; B's range from `1/200` to `2`, with support sizes at most three in these fixtures. These are exact authored generator evaluations, not physical measurements.

The query count is polynomial only conditional on the known degree promise. Positivity and full support-table validation can still cost `2^s` for recovered support size `s`; the prototype rejects supports above ten. A degree-two polynomial may have dense support, and finite observations alone cannot prove that an unqueried higher-degree term is absent. The example's reported 21.49 `kBT` maximum unfavorable-state gap omits the costs of making and holding a full context. Work, heat, apparatus control, drift, and model error were not measured.

Under the pairwise energy promise, the empty/single/pair readings identify each interaction by `t_ij^2=W(e_i+e_j)W(0)/(W(e_i)W(e_j))`; single-coordinate readings then recover fields. The 172-query count is `1+n+choose(n,2)`, and each authored energy evaluation visits the explicit interaction law. The source separately includes an off-energy-graph clock dependency in a support-learning variant, showing that clock support need not be copied from the energy graph. Neither finite test establishes the global energy or clock degree promises for an unknown physical system.

In the 18-bit canonical partition, the source reports a separate mass contrast `Rm=9/4` and cross-block clock contrast `Rk=1`; the context-dependent clocks in B are handled inside the acquired local models. Thus the global comparison factor is `R=Rm Rk=9/4`, not a thermodynamic-only factor silently applied to unrelated rates. The `Z` denominator remains the global source normalization. In my independent 16-state fixture, I varied the two contrasts separately (`Rm=9/4`, `Rk=10/7`) and checked their product in `A <= R C`.

The deterministic error propagation uses assumed bounds `delta_E=1e-10`, `delta_q=1e-8`, and 0.2% reaction-clock relative uncertainty. It reports `eta ~= 0.0025476000024`, and robust intervals about `[148460674.87,149221900.49]` for A and `[229651025.25,230824232.43]` for B, leaving `B/A > 1.53899008`. Those are conditional error envelopes, not attained calibration accuracy. The stated repeated-dwell sufficient design costs about `9.6e20` model-time units before reset/preparation/clamping, and is explicitly not a necessary measurement lower bound.

## Countermodels to the acquisition promise

`countermodels.py` builds a four-bit rational system whose target attempt contains the cubic factor `1-(1-10^-15)y1*y2*y3`. All seven degree-0/1/2 clock contexts agree with the baseline, and the energy law is unchanged. The exact finite means have ratio `180755.4693599989`. This is deliberately outside the acquired degree-two class; it shows why the class promise is indispensable, not a refutation of the conditional theorem.

The preparation-control example has energy ratio `3/2` and reaction hazard one. In model 1 the free attempt is one and preparation doubles the clock; in model 2 the free attempt is two and preparation leaves it unchanged. Both yield the same prepared downhill rate `6/5`, while their unprepared equilibrium means are `7/3` and `2`. The original-potential protocol avoids this ambiguity only under its explicit assumption that preparation/readout preserves the intended conditional clock.

## Finite-response obstruction and a conditional completion

For a positive killed mixture, `F(s)=sum_j p_j/(lambda_j+s)` at any fixed finite set of positive shifts does not alone control `F(0)=sum_j p_j/lambda_j`. Given `k` distinct shifts, take `k+1` baseline rates and add a small fixed mass `delta` at `epsilon`. Adjust the old `k+1` weights using the square system consisting of normalization and the `k` response rows. Its Cauchy-type matrix is invertible. The right-hand side remains bounded as `epsilon -> 0`, so the old weight corrections are `O(delta)` and remain positive when `delta` is small enough. The sampled responses stay exact while the mean gains `delta/epsilon` plus a bounded term and diverges.

The independent exact four-rate example has rates `1,2,3,4`, equal masses, and shifts `1,2,4`. It preserves responses `77/240`, `19/80`, and `533/3360`; the mean grows from `25/48` to `0.617...`, `10.517...`, `100000.517...`, and `1000000000.517...` as the hidden rate decreases from `10^-2` to `10^-12`. This is an identifiability obstruction for finite regularized samples, not a theorem against fully identified finite-dimensional generator classes.

A positive conditional completion is available if a source-visible gap is known: if all rates satisfy `lambda >= g > 0`, then `F(s) <= F(0) <= (1+s/g)F(s)`. More generally, if the inverse-rate contribution from rates below `g` is independently bounded by `T`, then `F(0) <= T+(1+s/g)F(s)`. A mere bound on the mass below `g` is not enough; an inverse-rate tail or structural lower rate bound is needed. This completion is kept logically separate from the finite-sample obstruction and the source's residual certificate.

## Comparator and scale limits

The reported full-state and tensor methods use the same reverse-acquired heterogeneous model B, the same local reference factors, the same acquisition information, and an upper/lower target of 1.05. The tensor interval is approximately `[230236127.70,234586384.28]` (ratio `1.018895`, 5 PCG steps, 9,088 response coefficients, 6.58 s). The full-state interval is `[230236128.09,230402298.29]` (ratio `1.000722`, 6 steps, global 262,144-state vectors, 3.26 s). The full-state implementation is faster in this single run and returns a tighter interval. The tensor representation is smaller by the reported coefficient count, but coefficient count is not peak memory; full-state allocations and exact arithmetic differ. The timing is uncontrolled and does not include failed development or research. No energy-use advantage is measured.

The dense 18-bit, 153-edge stress case is a serious scale limit: at block cap six, at least 108 cross edges leave an exponential comparison factor of at least `2^108`, so the current compiler aborts. This is a failure of this reference/comparison construction, not a hardness theorem. The work also does not run matched WE, TAMMBER, or AIMMD comparisons.

## Relation to Astra capital

The four nearby capital results have different interfaces. N793's hidden-mobility lower bound concerns arbitrary unqueried local conductances with identical static information. N795 assumes an explicitly represented finite graph and independent conductance boxes; its stronger 37-query comparator wins within its supplied structural promise. N798 removes hidden-bath enumeration only when global source/form envelopes are supplied or acquired, and keeps severe-rarity failures open. N801 is specific to the supplied pairwise homogeneous zero-field Glauber cycle and its source/complement construction; its exact unseen-well and target-mobility countermodels preserve the model-validation gate. FI's heterogeneous modular, frustrated energy and separately acquired degree-two attempt law neither contradicts nor automatically inherits these results. In particular, N801's homogeneous cycle closure cannot be transferred to FI's frustrated law, and FI does not itself acquire N798's global continuous envelopes.

## Replay and provenance limits

Owned copies of four producer small fixtures passed their recorded checks. Transcript-only producer recertification matched all three lower endpoints. Upper endpoints differed because this host lacks SciPy and the bounded copy used NumPy to construct a local positive-vector `alpha` witness; the exact rational checker validated the new intervals, and their ratios remain equal to the stored ratios to roughly 1e-9 or better. This is a numerical-witness/library difference, not a demonstrated certificate defect. Numeric NPZ arrays were loaded only with `allow_pickle=False`; each inspected array had numeric `float64` dtype and no object dtype. No source or capital files were edited.

All conclusions here are internal finite-model checks and scoped source review. No external proof review, physical experiment, novelty determination, or physical capability claim was made.
