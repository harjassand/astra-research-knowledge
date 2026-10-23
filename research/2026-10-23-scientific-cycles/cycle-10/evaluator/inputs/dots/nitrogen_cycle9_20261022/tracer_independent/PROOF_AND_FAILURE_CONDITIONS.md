# Evaporation-invariant nitrogen-oxidation challenge

Independent mathematical audit, 22 October 2026. No dataset fits, no assumed confidence intervals. Numeric fixtures are supplied apparent yields, not newly fitted measurements. Author-source facts are taken from the locally available primary-paper excerpt and data metadata; derivations below are this audit's, not claims attributed to the authors.

## 1. What the internal standard does establish, conditionally

Let S0 be co-aerosolized perchlorate moles and N0 initial nitrite-N moles. Feed ratio R=Cfeed/(1000 mM) gives N0/S0=R if both salts enter the droplet in their feed ratio. Suppose calibrated Raman ratio reports r=n(NO3)/n(ClO4), with equal effective sampling volume and matrix-valid relative Raman response. The reported nominal-perchlorate 'concentration' is Ceff=(1000 mM)r. If perchlorate moles are conserved, then

    y=Ceff/Cfeed=r/R=n(NO3)/N0.

Common water loss cancels exactly: n/V divided by S/V is n/S. Ceff need not equal actual physical nitrate molarity after evaporation. Thus an evaporation-only objection cannot invalidate this conditional mole-yield inference. Calibration standards undergoing the same kind of water loss likewise retain their known analyte/tracer ratios.

This y certifies at least y of the original N remains as measured droplet nitrate, if that nitrate originates in original nitrite. It does not certify full retention, final complete conversion, no gas production, exclusive oxygen oxidation, or process-scale capture. Net original-N loss cannot exceed 1−y at that instant; gross gas generation/recycling is not bounded by this simple net-loss statement.

## 2. Exact correction and falsification boundaries

Define p=(N0/S0)/R (initial relative nitrite enrichment), t=Sfinal/S0 (tracer survival), g=relative Raman ratio sensitivity in reaction droplets divided by calibration sensitivity, and h=additive apparent-ratio bias divided by R. Let b0 be nitrate background/import not derived from initial nitrite, expressed as fraction of N0. If a is apparent yield, the corrected product yield is

    Y = [t/(g p)](a−h)−b0 = K a−b,
    K=t/(g p), b=K h+b0.

For any stoichiometric ceiling T, exclusion requires strictly K a−b>T. Equality no longer excludes that model. With no additive error/background, boundary K=T/a, or apparent/true overstatement F=1/K=a/T. With ideal multiplicative calibration, background boundary is b=a−T. With g=p=1 and no additive bias, tracer loss boundary is 1−T/a. These are alternative single-error explanations, NOT tolerances that can all be used simultaneously. Combined biases must satisfy the full equation. Signed calibration offsets can increase or decrease Y. No probability or confidence level follows from a deterministic boundary.

Loss of nitrite alone before trapping, while S0 and the original feed-linked N inventory remain known, decreases nitrate obtainable and cannot create a false high yield. Nitrite enrichment relative to tracer during aerosolization (p>1), tracer loss (t<1), positive response enhancement (g>1), positive spectral offset, and imported/initial nitrate can. A changed denominator must be named explicitly: yield relative to surviving nitrite is not yield relative to original feed-associated N.

## 3. Specified disproportionation ceiling and two-route bound

For 3 HNO2 → HNO3 + 2 NO + H2O, a closed initial N inventory produces at most N0/3 nitrate if NO is not subsequently converted to nitrate. Unreacted nitrite, nitrate loss, and nitrite loss only lower retained nitrate. Therefore Y>1/3 excludes that reaction as the sole net nitrate source.

For DISJOINT initial-N pools, let d be nitrate formed by this reaction, o nitrate formed by a separate one-N-to-one-nitrate route, all normalized to N0. Then 3d+o≤1 and d+o=Y. Eliminating d gives

    o≥max(0,(3Y−1)/2).

This is not an oxygen-specific bound. It assumes mutually exclusive nitrogen accounting, not an arbitrary reaction network. In particular it cannot be applied unchanged to sequential disproportionation followed by NO reoxidation: at Y=1 that sequence produces 1/3 nitrate first and 2/3 by reoxidation, yet the disjoint-route formula would claim o≥1. With such NO recycling allowed, additional nitrate above one-pass disproportionation is at least max(0,Y−1/3), not necessarily (3Y−1)/2. This distinction prevents turning a valid conditional two-route model into an overstrong mechanistic claim.

## 4. Stronger universal nitrogen redox bound

Excluding nitrate+NO disproportionation is not excluding ALL nitrogen disproportionation. Nitrogen coproduct at oxidation state z permits nitrate fraction at most (3−z)/(5−z) without net nitrogen oxidation. Examples: NO (+2) gives 1/3; N2O mean (+1) gives 1/2; N2 (0) gives 3/5; NH3/NH4+ (−3) gives 3/4.

Allow every unobserved original nitrogen atom, retained or emitted, to reach the lowest conventional oxidation state −3. Retained nitrate contributes 5Y to the final oxidation-state sum, and all other N contributes at least −3(1−Y). Initial nitrite contributes 3. Therefore net nitrogen oxidation/electron export obeys

    Δe/N0 ≥ 5Y−3(1−Y)−3 = 8Y−6.

For Y>3/4 the initial nitrogen pool cannot balance its own redox chemistry by disproportionation alone. Some non-nitrogen electron sink or charge export is needed. The positive lower bound is max(0,8Y−6) mol electron equivalents per mol original N. This includes all remaining/escaped N in the bookkeeping and needs no assumption that it stayed in the droplet. It does require original-N provenance and an exhaustive N pool; imported nitrogen invalidates the calculation. It does NOT identify O2 as the sink: reduction of another species, hydrogen generation, photochemical or electrical charge export, etc. are logically distinct possibilities. This is an electron-balance statement, not an oxygen-atom-source statement.

At Y=.843/.834, the bound is .744/.672 mol e− per mol initial N. Unlike the 1/3 exclusion, this stronger conclusion is relatively sensitive to calibration: only apparent/true factors 1.124/1.112, or background fractions .093/.084, bring the yields to .75. These are hypotheses to test, not measured biases.

## 5. Numeric fixtures

| Apparent Y | Disjoint-route o lower bound | Extra nitrate above NO-only 1/3 | F needed to reach 1/3 | Background N0 fraction to reach 1/3 | Net N e− export lower bound |
|---:|---:|---:|---:|---:|---:|
| .843 | .7645 | .509667 | 2.529 | .509667 | .744 |
| .834 | .7510 | .500667 | 2.502 | .500667 | .672 |
| .357 | .0355 | .023667 | 1.071 | .023667 | 0 |
| .283 | 0 | 0 | already below | 0 | 0 |
| .290 | 0 | 0 | already below | 0 | 0 |
| .722 (361/500) | .5830 | .388667 | 2.166 | .388667 | 0 |
| .560 (printed ratio) | .3400 | .226667 | 1.680 | .226667 | 0 |

For .843/.834/.357, tracer loss alone would have to reach 60.46%/60.03%/6.63% respectively to reach 1/3. For the 3.5 μm row, 361/500=.722 conflicts with the printed .56; retain both fixtures rather than silently choosing. Neither exceeds .75. Rounded fixtures .834/.357/.283 are deliberately the requested ones; actual 730/875, 268/750, 177/625 differ slightly. Parent's native-data work can resolve input estimates separately. All full-precision values and both thresholds appear in bounds.csv/json.

## 6. Evidence supports a bounded positive claim, not dismissal

The primary Meroni paper describes 1050/932 cm−1 nitrate/perchlorate band integration; standards span 200–1000 mM nitrate at 1 M perchlorate; perchlorate is described as nonvolatile/stable/nonreacting. Those facts positively support the ratio-inventory interpretation. They do not independently measure tracer survival or prove equal relative Raman response across changing ionic strength, nitrite/nitrate mixtures, spatial profiles, focusing, droplet size, and optical resonances. Water loss can matter indirectly through such response changes, even though common-volume dilution cancels algebraically.

Air versus N2 gives approximately threefold nitrate difference at 45 min; nitrate is suppressed, not eliminated, under N2. KSCN decreases product about 50%; matched bulk controls are negative. These observations support atmosphere-dependent droplet chemistry and are consistent with oxygen involvement. They do not uniquely distinguish direct O2 oxidation, radical intermediates, NO/NO2 recycling, effects on gas partitioning, residual O2, or matrix/optical changes. Bulk controls cannot alone assign the elementary reaction mechanism.

Validation priorities: preserve the actual ratio calibration and intercept; calibrate nitrite/nitrate/perchlorate reaction matrices across evaporation states; independently recover tracer and initial droplet feed ratio; measure initial nitrate and exogenous N uptake; measure nitrite/nitrate and emitted N species. A proper N balance would convert conditional stoichiometric evidence into a much stronger mechanistic/process result. No statistical confidence bound is invented here.

## Sources and files

- Meroni et al., GRL (2026), DOI https://doi.org/10.1029/2025GL120957; primary excerpt at ../nitrite_finishing/meroni2026_web_excerpt.json, especially lines 173–174, 192–193, 202–214, and 241–246.
- Dataset metadata https://doi.org/10.5281/zenodo.17965118, local ../nitrite_finishing/zenodo_metadata.json; native Figure_3 calibration and Figure_6B plateau data are available to the parent analyst. This audit does not refit them.
- calculate_bounds.py reproduces the deterministic bounds.csv and bounds.json fixtures.
