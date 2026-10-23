# Independent conditioning-volume check

Date: 2026-10-22. Verdict: **PASS within the declared evaluated ambient reaction model.** No previous scientific campaign was rerun. This is an independent mathematical/material-balance check, not new kinetic measurements or admission of a hardware design.

## Independent method and reproducibility

Run `python nitrogen_cycle7_20261022/conditioning_independent/independent_check.py`. It reads the frozen parent inputs and results but never imports or executes the parent's numerical algorithm. It reconstructs species concentrations and the NO chemical sink directly, then performs 70-decimal adaptive tanh-sinh quadrature in the original conversion coordinate X. This differs from the parent's exact-rational, 32-panel, u-transformed monotone endpoint sums. An oscillatory admissible dimer partition is checked additionally; universal validity follows from the pointwise proof below, not that example.

Input SHA256: `75de794a26ecaac2e8c4c938249bea1af08fa4fa7e563407962e9ecb58f10a34`.

The independent numerical integration is not a rigorous enclosure by itself. The parent's enclosure is rigorous conditional on its exact decimal inputs and mathematical model. Decimal values emitted to JSON are rounded numerical representations of the underlying rational bounds, not stored rational certificates.

## Species balance and derivative audit

Write F0 for the original dry-air molar feed and a for initial NO mole fraction after the declared all-NO reset. If only N2 + O2 → 2 NO generated that inlet, inlet N2/F0 = 0.79 − a/2 and O2/F0 = b = 0.21 − a/2. That formation reaction preserves the original total molar flow. Setting b = 0.21 instead would silently fail oxygen bookkeeping.

At conversion X with d = F_N2O4/F0:

- NO/F0 = a(1−X).
- O2/F0 = b−aX/2.
- NO2/F0 = aX−2d; N2O4/F0 = d; N2 is unchanged.
- Total flow ratio f = 1−aX/2−d, with 0 ≤ d ≤ aX/2.

Thus 1−aX ≤ f ≤ 1−aX/2. Oxidation and dimerization both contract the gas. Oxygen remains positive in all cases, with the smallest checked O2/F0 about 0.197851. Neither oxygen starvation nor a denominator sign change is present.

With C=P/(RT), the NO sink is 2 k [C a(1−X)/f]^2 [C(b−aX/2)/f]. The steady PFR balance is F0 a dX/dV = sink, not a fixed-volume batch concentration derivative. It yields precisely the parent's integrand and prefactor. The event-rate unit conversion k = 3.95e−38 NA²/10¹² = 0.014325140836635084 m⁶ mol⁻² s⁻¹ and F0 = 20/22.414/60 = 0.014871657594955534 mol/s check. Actual C is 40.359850685478534 mol/m³ at 298 K and 1 bar; standard flow is not used as the reacting concentration.

Since f³ increases monotonically with f, the all-dimer and no-dimer integrals pointwise enclose every admissible d(X), including a varying nonequilibrium partition. They are extreme mathematical partitions, not assertions that either is an equilibrium state at 298 K.

For u=1/(1−X), the integrand is g(X)=(1−saX)³/(b−aX/2), s=1 or 1/2. Its derivative has the sign of 1/2−3sb+saX after positive factors are removed. This sign is negative throughout each all-dimer range and positive throughout each no-dimer range. The exact endpoint rectangle sums therefore rigorously enclose each integral; combining the lower all-dimer sum with the upper no-dimer sum is valid. The parent's finer-grid assertion is consistent, but the derivative argument, not just that assertion, establishes the enclosure.

## Numerical results

Values below are independently integrated endpoint volumes, in litres. Every pair lies strictly inside its corresponding parent rational enclosure.

| Condition | Ordinary PFR | Split PFR |
|---|---:|---:|
| 95% NO conversion | 68.576957–69.511333 | 59.986254–60.925578 |
| 99% NO conversion | 357.097973–362.614211 | 312.341070–317.887385 |
| Robust NO ≤100 ppm | 384.106186–390.055987 | 386.387557–393.301308 |

The independently evaluated ideal CSTR balance agrees with every reported CSTR value to relative error below 1e−14. At robust ≤100 ppm its endpoint range is 41,279–41,942 L for ordinary and 47,700–48,582 L for split. Both have access to the same favorable ideal PFR control; a CSTR-only conventional comparator would be misleading. These are ideal steady gas-phase reactor volumes, not validated equipment dimensions.

## Matched-output interpretation

At fixed 99% conversion the higher-NO inlet gives a ~12.3–12.5% smaller ideal PFR when matching endpoint partition assumptions, but leaves more NO: worst-case residual is 107.49 ppm ordinary versus 123.47 ppm split. This is not equal outlet gas quality.

The robust fixed-conversion target X=(a−ε)/[a(1−ε)], ε=0.0001, solves the worst-contraction residual equation a(1−X)/(1−aX)=ε. It guarantees ≤100 ppm for every allowed outlet partition. It gives 99.06967% conversion ordinary and 99.19012% split. This calculation is a common robust gas-quality criterion, not a separate optimization of the minimum volume for every partition.

At this criterion the split/ordinary volume ratio is 1.005939 for all-dimer endpoints and 1.008320 for no-dimer endpoints. Under independently arbitrary partitions the ratio range spans 0.990595–1.023939, so the mathematical bounds do **not** establish a strict volume ranking for every possible pair of partitions. They do eliminate the claimed ~12% compactness advantage under the common quality criterion.

For a check on conservatism, impose exactly 100 ppm separately for the no-dimer endpoint. Then X=(a−ε)/[a(1−ε/2)] and volumes are 387.969885 L ordinary and 390.886888 L split. The same conclusion remains; using the robust target is not what creates the loss of the apparent advantage.

Equal residual NO does not mean equal useful product flow. The split point still carries more oxidized nitrogen. A system comparison must state which outcome is fixed and retain any resulting production-rate advantage separately from a conditioner compactness claim.

## Physical limitations and uncertainty

The evidence contract and dimer addendum in `oxidation_evidence/` correctly limit this to the IUPAC evaluated model. The current check accepts the independently established event-rate convention and the stated source admission; it does not independently retrieve the original Hisatsune experimental full text or establish simultaneous experimental coverage of the exact inlet mixture.

The 298 K, 1 bar, dry, all-NO inlet is a declared conditioning/reset state. It is not measured hot-reactor outlet speciation. Cooling, thermal duty, removal or decay of other plasma species, pressure loss, wall reactions, water chemistry, and any adjustment required to reach that state have not been identified by the volume calculation. An actual inlet containing NO2, N2O4, or other nitrogen/oxygen species needs different inlet inventories; simply applying the same a and b would not establish its balance.

The isothermal ideal-gas PFR and CSTR assumptions neglect transport and mixing limitations, pressure drop, heat transfer design, and other chemistry. NO disappearance establishes oxidized nitrogen flow NO2+2N2O4 within this model, not monomer NO2 yield, nitric acid, absorption performance, fertilizer yield, or an integrated plant result.

The IUPAC ±0.2 log10(k) band is an evaluator reliability sensitivity, not a confidence interval or a universal kinetic enclosure. All these volumes scale as 1/k. For a shared ambient model coefficient, that uncertainty is correlated across the two configurations and cancels from their volume ratio; independently pushing k to opposite extremes for each configuration would manufacture an unjustified ranking uncertainty. Composition-dependent model error or unequal actual conditions could break that cancellation and are not quantified here. No pressure extrapolation is admitted, and the independent check makes no compression/hardware/absorption claim.
