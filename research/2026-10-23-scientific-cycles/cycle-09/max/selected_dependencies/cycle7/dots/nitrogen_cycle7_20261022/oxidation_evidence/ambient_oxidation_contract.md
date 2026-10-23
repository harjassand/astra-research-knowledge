# Ambient NO oxidation evidence contract

Prepared 2026-10-22. Scope: gas-phase conditioning, approximately 1% NO in air at 298–300 K and 1 bar. Not absorption, fertilizer production, hardware authorization, or measured reactor-outlet speciation.

## Decision

A source-admitted **evaluated-model calculation** is possible using the IUPAC recommendation, with explicitly conditional applicability. A stronger claim of independently verified original experimental coverage of the exact simultaneous 1% NO / air / 1 bar mixture is **not established**: the Hisatsune–Zafonte original full text was unavailable. If the acceptance rule requires that exact primary experimental evidence rather than the evaluating authority's documented coverage, the premise fails and that path must stop.

Do not describe different published coefficients as a statistical confidence interval. In particular do not transplant the Neyrolles high-pressure coefficient into ambient air, or use the Greig–Hall low-NO coefficient as an experimentally established 1% result.

## [1] IUPAC evaluated model and coverage

IUPAC NOx23, evaluated November 2017, preferred-value change May 2014:
https://iupac-aeris.ipsl.fr/datasheets/pdf/NOx23.pdf

Preferred k298=3.95e-38 cm6 molecule−2 s−1; temperature fit k=4.25e-39 exp(663.5/T), 270–340 K. Assigned reliability is Δlog10(k)=±0.2 at 298 K, not a stated frequentist confidence interval. The evaluation explicitly reports an unexplained factor-two disagreement with Olbregts.

Comment(g) records Hisatsune maximum NO/O2 partial pressures 320/640 mbar, concentrations varied over two orders, NO2≤18.7 mbar, with NO2-dimerization correction. Comment(k) and discussion warn that dimerization matters above approximately 1 mbar NO2. The evaluation supports third-order kinetics and discusses buffer-gas, water, and added-NO2 tests, while warning about wall chemistry.

Inference: 10 mbar NO and about 210 mbar O2 lie inside inferred individual concentration spans, but simultaneous tested conditions are not demonstrated. This is supportive evaluated coverage, not a verified individual experiment.

## [2] Rate convention

IUPAC Guide to Gas-Phase Datasheets, October 2017, §2.2:
https://iupac-aeris.ipsl.fr/guides/Guide_to_Gas-Phase_Datasheets_Final_Oct_2017.pdf

Search-indexed official text explicitly defines the coefficient of A+A as −(1/2)d[A]/dt=k[A]^2. Direct retrieval currently returned404; the official indexed section was available and checked twice.

Applied to [1], event/source rate r=k[NO]^2[O2]; chemical NO sink=2r and chemical O2 sink=r. For fixed-volume batch, −d[NO]/dt=2r. For variable-volume flow, use dF_NO/dV=−2r; do not replace the complete material derivative of concentration with the chemical sink without the dilution/contraction term.

This convention admission belongs to the IUPAC evaluated model. The original Hisatsune paper's own differential equation was not retrieved. A NIST reaction listing alone is not proof of the original author convention.

## [3] NIST Hisatsune–Zafonte record

https://kinetics.nist.gov/kinetics/Detail?id=1969HIS%2FZAF2980-2989%3A2
Original DOI https://doi.org/10.1021/j100843a034

Official indexed record: J. Phys. Chem.73(1969),2980–2989;277–329K;0.98bar;N2 bath;IR absorption; absolute measurement. k=2.09e-38 exp(1546/RT); tabulated k300=3.89e-38. Full page fetch cache-missed, but exact official search entry was retrieved. The rendered activation-energy uncertainty is anomalous (±133863 J/mol) and must not be used to build an uncertainty envelope. Publisher full text requires purchase; no purchase attempted.

## [4] Greig–Hall is separate low-NO evidence

https://pubs.rsc.org/en/content/articlelanding/1967/tf/tf9676300655
https://kinetics.nist.gov/kinetics/Detail?id=1967GRE%2FHAL655-661%3A0
DOI10.1039/TF9676300655;Trans.Faraday Soc.63(1967),655–661.

Primary abstract: approximately50ppm NO in O2/N2 mixtures;293–372K. At293K,O2=0.5–175mmHg,total≈630mmHg. Reported orders2 in NO,1 in O2 and pressure independence; rate coefficient about35% above accepted higher-NO results. Thus describing the study simply as an O2-only bath is inaccurate. NIST fit1.06e-38 exp(3999/RT) gives about5.26e-38 at300K. Not admitted as a1%NO-specific coefficient.

## [5] Neyrolles is separate high-pressure evidence

https://kinetics.nist.gov/kinetics/Detail?id=2020NEY%2FLAR329-340%3A1
https://doi.org/10.1002/kin.21353
International Journal of Chemical Kinetics52(2020),329–340.

NIST directly retrieved:288–323K,9.70–19.90bar,k300=1.76e-38;fit2.23e-39exp(5155/RT). Publisher abstract concerns pressurized CO2-containing fumes and reports oxygen-fraction dependence. It is not ambient1bar validation. Full publisher view redirected to abstract; repository HAL04571594 returned access denied. No bypass attempted.

## [6] Independent convention caution

Šolc,Nature209(1966),706;https://doi.org/10.1038/209706a0.
Official indexed abstract explicitly defines k_exp=(d[NO2]/dt)/([NO]^2[O2]) and reports composition-dependent limiting values0.80e4 and1.48e4 L²mol−2s−1 at25°C,partial pressures1–50mmHg. Those are product-formation/NO-loss coefficients, not event coefficients. This establishes why numeric comparisons without convention normalization are unsafe; not adopted as an air1bar model.

## Derived implementation numbers and limits

Using [1] fit, k298=3.938673364e-38 and k300=3.880641817e-38 cm6 molecule−2s−1. Convert to L²mol−2s−1 by multiplying NA²/1e6:14284.06346 and14073.60520. Chemical NO-loss coefficient is twice these values.

At300K,1bar: total number density2.414323505e19cm−3;1%NO gives2.414323505e17cm−3. Ideal-gas concentration substitution must use actual mixture pressure and temperature, not nominal standard flow concentration.

At298K,[1]'s separate tabulated preferred3.95e-38 and ±0.2 log reliability imply2.492e-38 to6.260e-38. Label as evaluator reliability bounds at298K, not a confidence range or proof that all alternative experiments lie inside it. No unqualified bound at300K was separately assigned here.

A single-reaction2NO+O2→2NO2 PFR is exact only within that restricted species model. Actual NO2/N2O4 equilibrium changes monomer yield and total molar flow; a useful total oxidized-N measure is F_NO2+2F_N2O4. Merely equating NO disappearance to measured monomerNO2 overstates what this model establishes. Water/wall pathways and any initial mixed NOx remain separate unresolved physical conditions.
