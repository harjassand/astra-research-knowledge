# Review: control granularity and clock bandwidth

29 October 2026. Existing Astra P1 `record_geometry` role; no new agents or numerical checks.

Reviewed actual file: `CONTROL_GRANULARITY_AND_BANDWIDTH.md`  
SHA-256 `f4a62b3a6fd005200da94a38f01d2fffcbdadbd8d2c0c824cce7c9dd4e63770d`.

Exact snapshot: `CONTROL_GRANULARITY_AND_BANDWIDTH_REVIEWED_f4a62b3a6fd0.md`.

## Verdict

**Accepted.** For the stated grouped sign operation and bounded own-swap-invariant phase-independent amplitudes, `max_g n_g/gamma_g ->0` supplies both the volume-scale phase replacement and a fixed positive exchange-form constant. The rest of the already reviewed full density/current action proof therefore applies, including zero instantaneous native rates.

This is a sufficient program, not a universal lower bound or a proof of the order-`N` crossover. Its constructive common-clock regime does not conflict with the slower common-clock counterexample.

## 1. Exponential estimate

Write the centered source as `sum_g sigma_g v_g`, where `||v_g||<=C n_g`. Sign integration by parts and weighted Cauchy–Schwarz give

\[
|\langle H_N,|f|^2\rangle|
\le\left(2\sum_g\|v_g\|_\infty^2/\gamma_g\right)^{1/2}
\left(\sum_g\gamma_gD_g(f)\right)^{1/2}
\]

for normalized `f`. Completing the square against the macroscopic bath form `N^2 sum_g gamma_g D_g` at multiplier `bN` gives exactly the root's factor `b^2/2`. Thus the divided log moment is bounded by `C^2 b^2 T r_N/2`. Initial orientation/occupancy correlations cost at most `2^(N+#groups)`, which is at most `4^N`; the same Chernoff limit removes this fixed exponent.

The deterministic source bound is still `O(N)`, independent of group geometry. The integrated-residual time-grid argument remains valid. Weak comparison likelihoods only change native rates and keep their uniform upper bound, so their second-moment transfer is unaffected by arbitrarily large group-clock rates.

## 2. The repeated-group form factor is correct

For each native bond, use its entire group flip in the one-sign inequality. A group flip and the native exchange commute. Each group's form is counted once for every bond in that group, yielding

\[
D_{\rm ex}\le(4/s)D_{\rm native}+4\sum_g n_gD_g.
\]

Therefore the joint form dominates

\[
\min\{s/4,\min_g\gamma_g/(4n_g)\}\,D_{\rm ex}.
\]

No group has to be spatially contiguous for this argument. The `max` condition makes the coefficient eventually `s/4`. This is enough for the explicit occupation variational receiver and its weak-tilt transfer. Zero-rate transitions remain valid under multiplicative tilting because the zero set is unchanged.

The file correctly distinguishes the weaker averaged condition needed for the phase estimate alone from the stronger maximum condition used to supply exchange coercivity at closed gates. It does not silently apply the averaged condition to the full endpoint theorem.

## 3. Actual laws and resources

The complete conditional native-and-clock generator premise is explicit. Fresh group clocks alone would not justify conditional statements after a record reveals future native innovations. The proof also keeps mathematical weak tilts separate from supplied actuators.

The expected group-clock event count is `N^2 T sum_g gamma_g`, while the addressed-bond flip count is `N^2 T sum_g n_g gamma_g`. For equal group size `L` and `gamma=L h_N`, these are respectively `N^3 T h_N` and `N^3 T L h_N`, as stated. They are different physical quantities and neither alone specifies work or apparatus feasibility.

The one-common-clock sufficient regime `gamma_N/N -> infinity` is a valid constructive alternative. The parity counterexample shows failure when only `gamma_N -> infinity` is assumed and `gamma_N/N ->0`. The unproved finite-ratio crossover and necessity for particular models remain properly excluded.

## 4. A direct weaker sufficient corollary

The two reviewed estimates also give the full action under the separated conditions

\[
\frac1N\sum_g\frac{n_g^2}{\gamma_g}\longrightarrow0,
\qquad
\liminf_N\min_g\frac{\gamma_g}{n_g}>0.
\]

The first gives phase replacement; the second gives a uniform positive exchange-form coefficient, which need not equal `s/4`. For example, a fixed number of singleton groups can retain a fixed positive clock rate while the remaining singleton rates diverge. Their exceptional contribution to the first condition is `O(1/N)`. The root's maximum condition is a clean stronger sufficient condition, not an asserted necessity.

If native rates have a fixed positive lower bound, the second condition is unnecessary: native ellipticity already supplies occupation replacement. These are direct corollaries, not corrections or claims about a regime with vanishing coercivity.

