# Independent receiving check of native data and reference bounds

22 October 2026. PASS on the requested numerical checks, with scope qualifications below. Script: check_native_receipt.py; deterministic output: native_receipt_check.json. No kinetic refits were performed.

## Native controls

Figure_4.csv has an EXACT row at 2700 s for all three series, so interpolation is unnecessary (although the parent's interpolation returns the same values):

- air: 795.605 mM
- 25 mM KSCN_air: 378.536 mM
- N2: 273.58 mM
- air/N2: 2.908125593976168
- KSCN_air/air: 0.47578383745702957

The source column labels and dataset_result.json agree. These are same-time descriptive series contrasts, not matched-replicate effect estimates or confidence intervals. Matrix equivalence across KSCN addition is an assumption if interpreting the ratio quantitatively as a chemical-yield reduction.

With 1 M original nitrite, valid Raman/tracer normalization and no nitrate background/import, air Y=.795605 gives max(0,8Y−6)=.36484 mol electron equivalents per initial mol N. The apparent/true overstatement factor that reaches Y=.75 is 1.0608066667, i.e. 6.08067% overstatement relative to corrected yield. Equivalently, this requires a 5.73212% downward correction relative to the apparent yield. A positive additive nitrate bias/background of 45.605 mM also reaches the ceiling. These percentage denominators should not be conflated.

Source qualification: the air series starts at 116.154 mM at t=0, falls to 27.1659 at 5 s and 7.79507 at 10 s. This does not support treating 116.154 mM as a constant genuine nitrate background, nor does the processed series alone certify zero initial nitrate. Do not subtract that isolated initial point mechanically; keep original-N provenance and baseline validity conditional.

## Calibration normalization

The five pairs in Figure_3.csv exactly match dataset_result.json. Using the supplied linear slope .0008021917919970197 and intercept −.020170585902323415 reproduces every saved residual. No refit is required to verify this. Largest absolute residual divided by slope is 45.6393229141748 mM, matching profile_result.json.

Physical normalization remains: standard nitrate concentration at a fixed nominal 1000 mM perchlorate represents 1000 times the nitrate/perchlorate mole ratio, subject to a valid relative optical response. Thus a reaction-droplet calibrated Ceff divided by Cfeed gives nitrate/input-N yield when the tracer and original feed ratio bind. The empirical intercept must be treated consistently in the inverse calibration. A new fit to five source points does not establish which processing/intercept was used for the already exported kinetic concentrations.

The descriptive 45.639 mM residual is numerically close to the 45.605 mM ceiling-erasing correction, but is NOT a confidence interval, a systematic-bias bound, or an independently measured cross-matrix error. It cannot establish that the physical redox inference failed. It shows that these five calibration pairs alone do not certify the small cross-matrix/baseline accuracy margin needed for an unconditional Y>.75 conclusion. The main result remains conditional tracer-inventory algebra plus native atmosphere/scavenger contrasts.

profile_result.json was inspected only for its calibration comparison and scope. Its kinetic profiles were not independently refitted; nothing here certifies asymptote identification or statistical uncertainty.

## Rayleigh reference check

For an isolated conducting spherical droplet in air/vacuum, classical Rayleigh charge limit is

    Q_R = 8π sqrt(ε0 γ r^3).

Taking the explicitly hypothetical reference r=5 μm, C0=1000 mol/m^3, γ=.072 N/m gives N0=(4πr^3/3)C0=5.23598775598×10^−13 mol. If all the .36484 electron-equivalent redox burden were instead uncompensated stored net charge, Q_need=F N0 .36484=1.84315715066×10^−8 C. The Rayleigh limit is 2.24354858782×10^−13 C, a ratio 82153.65429. Holding r fixed, required surface tension γ_req=γ(Q_need/Q_R)^2=4.85944049746×10^8 N/m. All agree with material_bounds.json to rounding/physical-constant precision.

This reference makes persistent uncompensated net charge storage an implausible sole sink under those assumptions. It is NOT a measurement of droplet charge, initial inventory, true surface tension, or stability. In particular:

- The nominal initial concentration and chosen radius jointly define a reference inventory, not a measured inventory after evaporation.
- Oxidation-state electron bookkeeping is not automatically net electrostatic droplet charge. Chemical reduction of oxygen or another species can balance nitrogen oxidation without storing this net charge.
- The argument does not rule out transient charge separation, internal opposing charges, continuous charge transport, chemical electron acceptance, oxygen involvement, or optical/energy flow.
- Conducting spherical isolated-drop Rayleigh theory is an assumed reference, not a validated model of every trapped, deforming, optically driven droplet.

No disjoint-route (3Y−1)/2 bound is used as a universal mechanistic claim.
