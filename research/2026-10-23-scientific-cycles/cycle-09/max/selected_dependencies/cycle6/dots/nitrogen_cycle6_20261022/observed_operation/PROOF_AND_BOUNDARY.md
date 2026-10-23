# A measured operation can be selected without inventing its microscopic closure

## New contract and observed comparison
This checkpoint changes the physical construction, not the old equations. We use the actual2026 microwave reactor's two configurations:20SLM dried compressed air through the plasma, or10SLM through plasma plus10SLM opposed cold jets. Reactor pressure1bar; same reported400–700W settings; measured downstream FTIR observable labelledNOx. This is not the saved2700K,79/21,300K heater contract. It does not inherit its product yield,1.407MJ/kg export number or ideal SEC.

The whole apparatus comparison is admissible as published experimental evidence. The primary-flow change is part of the operation. It need not preserve every microscopic rate, every core parcel or the same source deposition to show a whole-device change. It cannot, however, identify isolated quench causality. SourceFig13 includes a10SLM ordinary CFD comparator and an actual molar-flux calculation, not a measured late-dilution control.

Parent digitize.py extracts black experimental errorbar caps from the exact embedded figureJPEGs. Its two-pixel reading allowance and one-pixel axis allowance are declared graphical conventions. Independent manual center/cap transcription agrees within those envelopes. No raw samples, calibration covariance, bar interpretation or replicate count was recovered. The intervals below are therefore mathematical consequences of the graphical construction, not confidence statements about true device performance.

## Unknown NO2 split need not prevent a bounded original-feed comparison
Assume reactive N/O species are only N2,O2,NO,NO2, allowing any unchanged inert gas in the dry feed and outlet, no leakage/storage/other nitrogen product, and reportedx=xNO+xNO2. Letz=xNO2. Atom balance gives Fout=Fin/(1+z/2), so the useful counted product per inlet mole is h=x/(1+z/2). Since0<=z<=x,
  x/(1+x/2) <= h <= x.
Unchanged Ar or another conserved inert cancels from the molecular-flow balance; it need not be absent. Both endpoints increase withx. Given graphicx∈[l,u], h∈[l/(1+l/2),u]. For forced andbaseline at equal originalFin, a conservative ratio is
  Gmin = [lF/(1+lF/2)]/uB,
  Gmax = uF/[lB/(1+lB/2)].
This is exact inventory algebra in the declared four-species class. N2O4 or other sample losses, reactive trace-species effects outside the assumed net balance, wall inventory and an incorrectly definedNOx observable require explicit correction. PureNO-to-NO2 conversion does not itself destroy the counted nitrogen. Never divide split-feed product by only10SLM.

With the parent's graphical allowance the ratio minima at400/500/600/700W are1.04899,1.04810,1.08494,1.11398. Centers indicate roughly13–18% reported-power-per-NOx reduction. The minimum is not a physically certified margin: a differential systematic calibration error remains unidentified. Equal opposite relative biases can erase these conservative positive ratios at about2.35–5.39%. A common multiplicative calibration cancels, but composition-dependent or time-varying error need not.

## Matching output rather than comparing two different yields
For a corrected targeth*, define lower/upperh envelopes Lc(P),Uc(P) for configurationc. At a shared measured powerP*, if
  max[UB(P*),UF(400)] < h* < min[LF(P*),LB(700)],
then two data-consistent continuous, nondecreasing corrected-output response curves must attain that exact target with
  PF(h*) < P* < PB(h*).
Proof: forced is below target at400 and above it atP*; ordinary is below target atP* and above it at700. Continuity gives crossings in the respective open intervals; monotonicity supplies ordered minimum required settings. No source power interpolation is silently fitted.

For the parent envelope the nonempty target windows are:
- separator500W:0.0111007752<h*<0.0116347071mol countedN per original inletmol;
- separator600W:0.0125271318<h*<0.0128165629.
This is a conditional matched-product-count result at the same20SLM throughput. It does not match NO:NO2 ratio, thermal state, pressure loss or complete capture/product quality. Plasma hysteresis/discontinuities or nonmonotonic response can invalidate the interpolation premise. No actual matched-target run was performed.

A uniform positive watt saving does NOT follow. ordering_proof.py constructs continuous nondecreasing piecewise-linear curves through all central observations, whose target-power gap approaches zero as unresolved slope grows near500W. The100W measurement spacing is not a100W saving certificate. Source central values may suggest such a scale, but only a measured response/slope constraint can certify it.

## Complete input-power condition
At equal reportedP, let Ec=P/eta_c+Ac be actual input power under a common whole-system boundary. eta includes the indicated-power-to-electric conversion convention, not an assumed measured device efficiency; Ac counts actual relevant auxiliaries consistently. For positive usefulproduct ratioG=NF/NB,
  EF/NF < EB/NB iff AF-G AB < P(G/etaB-1/etaF).
IfetaF=etaB=1 andAB=0, the conservative graphic-derived extra-power allowances are19.59,24.05,50.97,79.78W. These are conditional thresholds, not measured compressor or electrical losses. Equal lower conversion efficiency increases the absolute watt allowance, while a sufficiently worse forced conversion can reverse the comparison. With noaux, etaF/etaB must exceed1/G. A same-indicated500W counterexample withetaB=.8,etaF=.6 reverses SEC despite the center yield gain; it is not an assertion about the experiment.

At exactly matched usefuloutput the powers generally differ andG=1. The relevant condition is instead
  AF(PF)-AB(PB) < PB/etaB(PB)-PF/etaF(PF).
Do not carry the same-P yield headroom directly into a measured matched-output saving claim.

For an illustrative pressure screen only, extra isothermal compression of the EXISTING10SLM quench share costs nRT ln(r)/etaC at300K. r is the additional pressure ratio relative to baseline pressure already charged to that share; it is not automatically compression from ambient. The total original feed remains20SLM. Common compressed-air/drying costs must not be charged twice. Under the unity common power-conversion reference andetaC=.5, the conservative allowed incremental ratio is about1.70 at400W,1.91 at500W,3.95 at600W,8.59 at700W using22.414L/mol as a declared standard-volume convention. Neither the actual jet pressure nor compressor efficiency/SLM reference was recovered. Alternative24.466L/mol convention is also tabulated. The calculation does not admit any of those operating pressures.

## Physical decision and remaining load
Select this experimentally operating electrodeless split-feed architecture over the melted arc-attached divider for further physical investigation. No finite-area/mode simulator is needed to acknowledge the observed whole-device gain. Do not promote that observation into intact long-duration geometry, actual total electrical savings, a complete300K/1atm endpoint or useful heat recovery. Cold-jet mixing transfers energy between streams; sustained heat ultimately must leave or be recovered. Actual wall hot spots, thermal persistence, outlet enthalpy, measured supply/jet powers and product closure are the next coupled evidence boundary. The old25kOhm ballast belongs to a different experiment and is not charged to this solid-state microwave apparatus.
