# A source-resolved cold conditioning operation, not a new high-temperature closure

## Owner-selected contract and why it matters

The next useful product is not simply a hotter or more concentrated NO signal. A dry downstream oxidation step can convert poorly absorbable NO to oxidized nitrogen using oxygen already in the feed. This is an ordinary operation, not a novel reaction or a finished fertilizer process. It is selected because its evaluated ambient kinetic law is available, unlike the parked state-resolved high-temperature package.

The calculation has a NEW, explicit inlet contract: all inlet counted NOx is NO, N2/O2/NO ideal gas at298K and1bar, total original feed20SLM with the DECLARED standard molar volume22.414L/mol, initially79/21 N2/O2 before NO formation. At the two published500W center concentrations use a=0.010635658914728683 (ordinary) or0.012198142414860683 (split), b=0.21-a/2 oxygen, N2=0.79-a/2. This is a calibration scenario conditioned on all-NO speciation, NOT a measured inlet analysis. The same original feed is counted in both arms; no new oxygen stream is supplied. Humidity, wall loss, absorption and leaks are excluded. These restrictions must be qualified for a real device.

IUPAC NOx23 supplies the evaluated reaction-event law r=k cNO^2 cO2, k298=3.95e-38cm6 molecule^-2 s^-1. Its guide fixes the stoichiometric convention: the NO sink is2r, notr. Evaluator reliability is +-0.2 in log10 k at298K, not a statistical confidence interval, a universal enclosure of experiments or a wall/surface uncertainty bound. The original Hisatsune paper was not recovered. Its evaluated concentration ranges support a conditional interpolation inference, not an independently verified exact experiment at these combined conditions.

## Dimerization is bounded, not silently omitted

Let F0 denote initial molar flow, X the fraction of initial NO consumed, and D the molar flow of N2O4. In the restricted chemistry:
FNO=F0 a(1-X), FO2=F0(b-aX/2), FNO2=F0 aX-2D.
0<=D<=F0 aX/2; Ft=F0(1-aX/2)-D.
Consequently1-aX<=Ft/F0<=1-aX/2. This remains valid for any dynamically varying dimer partition, without inventing an equilibrium constant or treating monomerNO2 as the entire product. Oxidized nitrogen is FNO2+2FN2O4=F0 aX. The IUPAC evaluation reports no product-inhibition term and tests with addedNO2/N2O4; unmodeled pathways remain outside the construction.

With c=P/(RT), steady plug flow obeys
 dX/dV=2k c^3 a(1-X)^2(b-aX/2) / [F0 (Ft/F0)^3].
Thus the volume is bracketed by replacing Ft/F0 by1-aX and1-aX/2 in
 V=F0/(2k c^3 a) integral_0^X (Ft/F0)^3/[(1-X)^2(b-aX/2)] dX.
The variable-flow correction is retained. A fixed-volume batch concentration derivative is not substituted into this flow balance.

## Numerical enclosure, rather than an uncontrolled ODE trajectory

Use u=1/(1-X): dX/(1-X)^2=du. For s=1 or1/2 the smooth transformed integrand is f_s=(1-saX)^3/(b-aX/2). Its derivative sign is the sign of1/2-3sb+saX, which is constant on every selected interval. Exact Fraction arithmetic bounds each of32 equal-u panels by its endpoint extrema. The64-panel result lies inside the32-panel result. Inputs include exact decimal SI R, Avogadro constant and the pinned source-readout decimals. Final displayed decimals round exact-rational mathematical bounds; they are not thermophysical certificates. No kinetics solver or old flow calculation runs.

## The matched-quality comparator changes the decision

At a common99% fractional conversion, the evaluated-k volume brackets are approximately:
- Ordinary:357.08–362.65L.
- Split:312.32–317.93L.
This approximately13% apparent compactness benefit uses UNEQUAL residual NO fractions: ordinary~107ppm, split~123ppm. It is not a matched gas-quality result.

Instead prescribe the same internal-conditioning criterion yNO,out<=epsilon=100ppm. This is NOT an emission/safety standard; the gas remains highly NO2/N2O4-rich and requires capture. The conservative common target that covers every allowed dimer partition is X=(a-epsilon)/(a(1-epsilon)). It gives:
- Ordinary X=.9906967373, volume384.09–390.09L.
- Split X=.9919012206, volume386.37–393.34L.
The volume intervals overlap; no strict ordering follows if dimer partitions differ. For either common limiting partition, split is slightly larger, not13% smaller. The IUPAC reliability sensitivity expands the absolute brackets to about242–618L and244–623L, respectively; a common k uncertainty rescales both and must not be assigned opposite signs to manufacture a relative advantage.

Why: in the dilute constant-O2/constant-flow limit,
 V approximately F0/(2k c^3 b) [1/epsilon-1/a].
For epsilon much smaller than a, the tail target controls volume, not the initial NO concentration. Exact variable-flow bounds verify that this ordinary tail mechanism survives the admitted contractions. The original plasma production gain is NOT erased: more fixed nitrogen is produced and conditioned by split flow. What fails is an additional claimed polishing-volume saving inferred from percentage conversion alone.

The strong conventional control is also plug flow. A single CSTR at the same target holds the entire inventory at the slow outlet rate; the corresponding exact model requires roughly41–42m3 ordinary and48–49m3 split. Comparing a split PFR only with an ordinary CSTR would manufacture an architectural gain. Neither ideal reactor is a qualified residence-time distribution or materials design.

## Full resource and state boundary

Isothermal298K operation is imposed, not free equipment. In the restricted species model its reaction heat rejection is exactly
 Q=F0 aX[hNO(298)+0.5hO2(298)-hNO2(298)] + D[2hNO2(298)-hN2O4(298)],
plus any feed sensible, kinetic and pressure/shaft-work terms. Standard298.15K NIST formation values (NO90.29, NO2~33.10,N2O4~9.08kJ/mol) show an exothermic scale, but are NOT silently substituted as an exact298K thermal closure; no finite cooling area or measured outlet-temperature claim is made. Upstream plasma heat removal remains separately required. Gas dimerization stores/exports chemical energy; it is not missing nitrogen.

The apparatus inventory PV/(RT), startup filling, off-spec startup gas and complete shutdown/flush must be charged. A steady PFR model has no growing inventory, but does not establish the time or energy needed to reach it. At approximately0.4m3 and20SLM the transit scale is many minutes, not the microwave papers' unrelated sampling-settling criterion. No commercial vessel/material/pressure-drop design is admitted.

At constant k,T a pressure change gives V proportional P^-3 and a transit-time scale proportional P^-2. This scaling is a model consequence, NOT a validated high-pressure extrapolation of the ambient evaluated law. Reversible isothermal compression of the whole cooled20SLM stream from1 to2bar costs at least25.54W before any separately justified work recovery; actual demand is greater. Tenbar would cost84.84W in that same reference. These are not measured jet costs and must not be charged only to split flow: both comparators receive the same compression/recovery options. The old shared-feed jet-pressure budget and old arc ballast are different boundaries. No net-SEC ranking follows from this lower bound alone.

## Decision

Keep the real electrodeless production result. Do not add a free internal-preheat gain or a13% matched-quality polishing-volume gain to it. A conventional atmospheric oxidative holding section is a source-resolved next component to evaluate, with a finite conditional volume envelope and explicit cooling/inventory duties. Do not choose pressure solely to obtain a visually compact component without a whole-train energy/volume requirement. The next useful experiment/evidence is actual cooled outlet NO/NO2/N2O4/flow and paired capture performance, including hydraulic/power/heat and startup/reset, not another arbitrary high-temperature trajectory. Complete absorption, matched captured product, fertilizer SEC, material persistence and wall-plug superiority remain unestablished.

The reference standard-volume convention is not the article's verified metrology. Replacing22.414 with24.466L/mol rescales all volumes, rates and compression reference powers by22.414/24.466; dimensionless ratios and matched-quality conclusions are unchanged within the model. The500K heat ledger elsewhere uses a different four-molecular-species endpoint; it is not silently reused after N2O4 is admitted here. A coupled heat certificate requires its own correct species-resolved enthalpies and capacities.
