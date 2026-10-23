# Independent challenge: new split-feed microwave operation

## Decision-relevant result

The same-total-feed experiments in Fig. 7 support a bounded **whole-apparatus outlet-concentration improvement** for this 26 mm quartz-tube, 2.45 GHz reactor at 1 bar: 10 SLM tangential feed plus 10 SLM cold-air impinging jets gives higher reported outlet NOx than 20 SLM tangential single-feed at each common reported 400, 500, 600 and 700 W point. Selecting this new operation as a prototype candidate does not require identifying every microscopic rate. The experimental comparison does not, by itself, establish net wall-plug energy superiority, sustained reset-compatible operation, or transplantation to any old heater.

The sensible admission is conditional: accept the new configuration as a demonstrated candidate at the reported operating points; retain explicit power, molar-output, and persistence conditions before promoting it to a net-energy or durable-process claim. Missing microscopic identification is not a reason to discard the measured whole-device comparison.

Source: Vashisth et al., Chemical Engineering Journal 543 (2026) 178575, https://doi.org/10.1016/j.cej.2026.178575. This challenge read the supplied complete paper and its original embedded figures. No broad search, operation, new experiment, or spending occurred.

## Independent Fig. 7 transcription

Original PDF page 9 (article page 8); original embedded JPEG images page9_image0.jpeg and page9_image1.jpeg. Black circles and black error-bar caps, not red simulated diamonds, were transcribed independently. Parent digitization files were not read.

| Reported W | Intrinsic 20 SLM center, NOx % | Forced 10+10 SLM center, NOx % | Forced/intrinsic center ratio | Implied P/output reduction* |
|---:|---:|---:|---:|---:|
|400|0.850|0.988|1.162|14.0%|
|500|1.061|1.217|1.147|12.8%|
|600|1.203|1.421|1.181|15.3%|
|700|1.343|1.625|1.211|17.4%|

*Assumes equal actual outlet molar flow and the same fixed-N definition; uses equal reported power. These are approximate plotted centers, not source numerical measurements. Do not claim four-decimal measurement accuracy from the CSV conversion.

| Reported W | Intrinsic visible-cap range, NOx % | Forced visible-cap range, NOx % | Conservative raster envelope I / F | Ratio envelope F/I |
|---:|---:|---:|---|---:|
|400|0.825–0.874|0.960–1.016|0.81–0.89 / 0.95–1.03|1.067–1.272|
|500|1.030–1.092|1.183–1.251|1.02–1.10 / 1.17–1.26|1.064–1.235|
|600|1.172–1.234|1.381–1.461|1.16–1.25 / 1.37–1.47|1.096–1.267|
|700|1.302–1.383|1.579–1.666|1.29–1.39 / 1.57–1.68|1.129–1.302|

The conservative raster envelope adds one pixel beyond each outer cap stroke and rounds outward to 0.01 percentage point. The ratio envelope divides the low forced endpoint by the high intrinsic endpoint and vice versa. This establishes separation of the plotted marks, **not a confidence interval, tolerance guarantee, or statistical significance test**. The main article does not identify what its experimental bars represent or give replicate count, covariance, drift, calibration uncertainty, or run order. A quoted numerical lower bound applies only to this visual construction, not to unknown true reactor performance.

The 500 W point is a useful transcription check: its center implies about 12.8–13% rather than 14% reduction. The article's broad “approximately 14–17%” summary should not overwrite the plotted data. Figure 8 is consistent with approximately 3.2 versus 2.8 MJ/mol-N at 500 W, again around 13%; it is not a separately established wall-plug measurement.

## What each inference requires

### 1. Whole-apparatus concentration capability

The relevant measured comparison is same total nominal dried, compressed air feed and same reported power setting, not identical core feed. The core-feed change is part of the chosen apparatus operation. At this level one does not need to hold every internal state or deposition profile identical; changing those can be a real whole-apparatus benefit.

The power convention must nevertheless be the same across the two experimental arms: generator command, forward microwave power, forward minus reflected power, deposited/absorbed power, and mains electricity are not interchangeable. Section 2 calls the operating range “plasma power” and the figures label “power input,” but the main article does not specify a forward/reflected calibration or a wall-plug accounting. Therefore label the evidence “same reported power,” not measured equal wall-plug or definitively equal absorbed power.

### 2. Fixed-N molar production rather than concentration

Let product output be Q = n_out times the nitrogen-equivalent product mole fraction. For NO + NO2, both molecules contain one fixed nitrogen atom. If other species enter the reported sum, their nitrogen stoichiometry must be stated; e.g. N2O4 counts twice on a mol-N basis. The main article reports continuous FTIR NOx downstream, holds its gas cell at 0.2 bar to avoid line broadening and N2O4 condensation, and defines energy cost per mol-N, but does not supply a full operational NOx sum/calibration in this text. The CFD chemistry has only N2, O2, NO, N and O, so its output is NO, not a separately resolved NO + NO2 prediction.

For a molar-yield ratio use r = (y_F/y_I)(n_out,F/n_out,I), with any needed species-basis correction included. Same 20 SLM dry air inlet makes equal outlet flow a reasonable leading approximation for mostly NO production, because N2 + O2 -> 2NO conserves total molecular count. It is not an outlet-flow measurement: NO2/dimerization, unaccounted losses, leaks, sampling biases, and non-steady accumulation can change the conversion. Do not accidentally compare a plasma-only sample with a combined post-quench sample. The reported downstream measurement is intended to be post-combination.

Eq. (13) mass-flux-weights a local mole fraction in CFD. Exact molar output requires integrating molar species flux (as done for NO in Eq. (15)); a mass-flux-weighted mole fraction equals the usual molar-flow-weighted quantity only when the relevant mean molecular weight is uniform or the difference is negligible. At a well-mixed cool outlet that approximation may be excellent, but it should not silently become an exact identity.

### 3. Confidence, repeatability, and persistence

The separated black bars visually support a consistent observed effect; their unspecified meaning cannot support a confidence statement. The ten-time-step averaging associated with Fig. 13 is a CFD temporal average, not ten independent experimental replicates. It does not close experimental variance, long-run drift, or paired-run covariance.

The microwave/quartz geometry avoids the specific electrode-consumption channel inherent to an electrode discharge, but it is not a wall-integrity or reset proof. The article's modeled wall-temperature discussion and claimed stable operation do not provide an endurance run, erosion/deposition mass accounting, startup/reset energy, retained-product inventory recovery, or repeated-cycle durability. These missing quantities do not erase the short-run concentration comparison; they block unqualified sustained-process or closed-cycle claims. A prototype admission should make persistence and no hidden material/inventory depletion explicit conditions, not invent a measured failure.

## What Fig. 13 does and does not establish

At 400 W the modeled forced configuration gives about 5.7% more outlet NO molar flow than the modeled 20 SLM intrinsic case and about 9.8% more than the modeled 10 SLM intrinsic case. These are NOT the roughly 16% experimental Fig. 7 gain at 400 W. The quoted 54.3% and 70% values are gap-closing quenching efficiencies under Eq. (14), not absolute nitrogen conversion or wall-plug efficiencies.

The 10 SLM model is a meaningful control for a simple bypass story: in a model that holds the imposed heat source and 10 SLM core feed fixed, merely adding an inert post-reactor 10 SLM bypass would dilute concentration but not increase the already produced NO molar flow. A higher cross-section-integrated NO molar flow in the jet case therefore cannot be explained by passive dilution alone within that model. It identifies a transport/thermal/reactive intervention in the modeled apparatus.

It is not an experimental 10 SLM comparator. It cannot independently show that the real discharge coupling, core extent, residence-time field, chemistry, or supply efficiency is unchanged when its feed or quench jets are altered. The CFD explicitly fixes source geometry and deposition profile, imposes equal volume-integrated input, omits electromagnetic feedback, and uses a five-species finite-rate model. Consequently the CFD supports a mechanism account conditional on those choices, while the experiment supports the whole-apparatus observation without uniquely identifying that account.

## Net energy admission inequality and counterexample

Use an explicit common boundary. Let S_I and S_F be total input power (or cycle-energy rates) including generator losses, air production/drying/compression, differential jet pressure work, cooling, and allocated startup/reset costs to the degree the chosen boundary includes them. Let r = Q_F/Q_I be actual fixed-N output ratio. Then

    SEC_F < SEC_I  iff  S_F < r S_I
                         iff  Delta S < (r - 1) S_I.

Writing S_i = a_i P_reported + A_i allows unknown supply losses and auxiliary loads. The comparison is admitted only if

    a_F P + A_F < r (a_I P + A_I).

At equal a and common baseline auxiliary load A_I, the incremental forced-operation budget is (r - 1)(aP + A_I), not automatically (r - 1)P. Same total gas feed does not establish equal compressor load because delivery pressures, restrictions, and jet momentum differ. The paper describes jets with about twenty times the main-inlet velocity. No measured differential supply cost is supplied in the main article.

Numerical counterexample, intentionally hypothetical: at reported 400 W, use the independently read r = 1.1624. Suppose the intrinsic configuration uses 550 W total wall-plug power and the forced configuration uses 650 W because of unreported incremental supply/jet losses. The reported concentration and nominal-power results are unchanged, but

    SEC_F / SEC_I = (650 / 550) / 1.1624 = 1.0167.

Thus the forced device is about 1.7% worse at this total-power boundary despite about 16.2% more output at the same indicated 400 W. An alternative split with 500 W versus 650 W totals reverses the ordering by about 11.8%. These are logically consistent countermodels, not estimates of actual apparatus loads.

Conversely, if differential power is known to fit below the admission threshold, the measured output improvement becomes a valid net-specific-energy advantage at that boundary even without a unique microscopic mechanism. The paper supports the numerator/output observation needed for this calculation; it does not fill in all unknown terms.

## Deliverables and audit trail

- independent_fig7_experiments.csv: centers, pixels, visible-cap bounds, and conservative raster envelopes.
- independent_ratios.json: center and visual-envelope ratios, plus conditional reported-power quantities.
- independent_receipt.json: source hashes, pixel calibrations, limitations, and independence statement.
- independent_fig7_read.py: repeatable coordinate-to-data calculations.
- fig7_panel_0_point_crops.png, fig7_panel_1_point_crops.png, fig7_intrinsic_500w_detail.png: visual audit crops.

Stopping condition reached: source inspected, Fig. 7 independently transcribed, method and Fig. 13 challenge completed, and a concrete opposite-wall-plug-ordering counterexample given. No operation or broader experiment is authorized or implied.
