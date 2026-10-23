# What the ordinary dark experiment actually identifies

We use the independently measured nitrite and nitrate channels of Yang et al. (2025), DOI 10.1038/s41467-025-60696-3, and the exact deposited Source Data workbook (10.6084/m9.figshare.28210994). This is reanalysis of published measurements, not a new laboratory experiment or a novel accounting theorem.

## Query and scope

The selected query is net aqueous nitrate nitrogen per nominal initially dosed peroxide in the measured dilute dark batch. It is not nitrate per absorbed photon, total energy efficiency, fertilizer output or new nitrogen fixation. Nitrite already contains fixed nitrogen. We distinguish a source-supported point reconstruction from a metrologically certified uncertainty enclosure.

The reported recipe supplies 100 mL, initially nominal 0.5 mM nitrite and 1 mM peroxide, pH3, 298K and darkness. Ion chromatography measures nitrite and nitrate separately. Initial nitrate is nonzero. The peroxide dose is a reported nominal charge; an independently standardized stock assay and its uncertainty were not identified in the inspected source. Hence a dose-normalized point value is useful but not a certified yield interval.

## Exact inventory identity with sampling

Let V0 be the initial liquid volume, c0 the initial nitrate concentration, ct the final concentration before the last analytical draw. Prior draws have volumes vi and nitrate concentrations ci; no liquid is replaced, the solution is well mixed, and no liquid feed is added. Then Vt=V0-sum(vi). Nitrate in the final liquid plus withdrawn samples is

P_gross = Vt ct + sum(vi ci).

Subtracting the whole initial nitrate inventory gives

P_net = V0(ct-c0) - sum[vi(ct-ci)].

A final draw merely partitions final inventory and changes neither side. Counting each draw and still assigning V0 to final liquid is double counting. The analogous net nitrite loss is

L = V0 n0 - Vt nt - sum(vi ni).

The quantity P_net/L is formation per nitrite lost, P_net/(V0 n0) is net formation per initial nitrite, and P_net/Q is product per initial reagent charge Q. These are distinct. None requires knowing the chemical identity of every gas if the numerator and its nitrogen provenance are independently established. The gas would matter to an emissions claim, not to this scalar inventory identity.

If some original nitrate is destroyed, subtracting all initial nitrate is conservative for new nitrate, not necessarily an equality for nitrate newly created from original nitrite. Exact attribution also needs exclusion or a bound on other nitrate/nitrogen inputs. Here the stated reagents other than nitrite do not intentionally supply nitrogen; initial nitrate is explicitly measured and subtracted. No isotope-derived proof or complete contaminant budget is claimed.

Analytical aliquots are exports in this accounting, not isolated usable fertilizer. Their NaOH quench and IC processing are not free product recovery. A remaining-liquid-only query needs a different numerator and cannot be substituted silently.

## Applied source means

At 0 and 40 minutes the H2O2 arm gives nitrite 0.475 and 0.0018468468468468466 mM; nitrate 0.007089102950030104 and 0.4718554459645774 mM. Therefore concentration-based nitrite conversion is 99.61119%, net nitrate / initial nitrite is 97.84555%, and net nitrate / nitrite lost is 98.22746%. Their near-agreement with reported ~98.3% is not exact reproduction of a replicate-wise statistic: source replicate arrays and covariance are not supplied.

The main methods say approximately 1mL aliquots. Taking exactly four 1mL prior samples at 0,10,20,30 minutes is a declared reconstruction, not a measured sampling log. It gives 45.889148 micromol net nitrate in remaining plus sampled liquid, 96.60873% of initial nitrite, and 0.458891 mol nitrate per nominal mol peroxide. Peroxide charge / product is 2.179164, not the balanced-reaction stoichiometric value 1. The difference may include excess unconsumed reagent; no peroxide-depletion assay proves actual consumption or recoverability.

The 0 and 2mL equal-draw cases are sensitivities, not error bounds. They delimit 0.464766 and 0.453017 mol net nitrate per nominal mol peroxide for this chosen sampling family. A certified interval cannot be obtained by calling '~1mL' an exact ±1mL tolerance.

## Uncertainty and blank controls

Reported error bars are replicate standard deviations. They do not bound systematic calibration, dose preparation, aliquot volume or matrix effects. Our one-SD rectangular calculation is only a perturbation sensitivity, not a 68%,95% or guaranteed interval. Covariance is not inferred from aggregate SD columns.

With validated product bounds [P-,P+] and delivered reagent bounds [Q-,Q+], Q->0, the quotient interval is [max(0,P-)/Q+, P+/Q-]. We do not supply unmeasured Q bounds. A common volume scale may cancel for an unsampled same-stock concentration ratio; differential ion calibration, peroxide stock error and unknown sampling do not all cancel.

The ordinary no-peroxide source arm shows slow nitrite decay, not exact invariance: initial0.467717mM and0.436512mM at120min. No matched blank nitrate channel is supplied. Thus this ledger gives the nitrate output of the peroxide-containing process, not a separately quantified peroxide-caused nitrate increment. The large treatment/control nitrite contrast is real but is a different observable.

## Comparator fairness

The 532nm droplet model's initiation coefficient cannot be converted into measured nitrate yield to fabricate a direct energy comparison. The ordinary dark peroxide experiment demonstrates dilute nitrate formation at its own stated pH and reagent charge. It establishes a real conventional comparator that a proposed alternative must match, not a measured winner against a different apparatus.

Organic-peroxide source arms have different endpoints (40 versus120min), initial measured nitrite values, molecular peroxide structures and unmeasured downstream product quality. Their ratios can be reconstructed but do not provide a same-time/same-quality process ranking. In particular a molecule of 2-butanone peroxide is not automatically equivalent to one molecule of H2O2 in oxidizing equivalents.

Heater, stirring, cooling, acidification, peroxide manufacture/delivery, excess-peroxide cleanup, salt inventory, recovery and reuse remain outside the scalar reagent ledger. No practical plant claim or historical novelty is made.
