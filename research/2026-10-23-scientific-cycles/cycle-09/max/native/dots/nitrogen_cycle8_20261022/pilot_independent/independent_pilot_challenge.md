# Independent challenge to two projected improvements in the integrated pilot

Scope: McKinney et al., Nitrogen 2025, 6(3), 51, DOI https://doi.org/10.3390/nitrogen6030051. This is a challenge to extrapolations from the demonstrated nitrogen-fixation pilot, not a reopening of a general heat-engine programme. Line references below are to `capture_evidence/pilot.txt` supplied by the parent. No new apparatus parameters are asserted.

## Bottom line

1. The claimed 25% heat-to-electric conversion is not thermodynamically compatible with the demonstrated approximately 60°C recovered-water port rejecting heat to a 25°C environment. It can only be defended as a different recovery design operating on higher-grade heat, or under a materially different cold-sink assumption. The paper does contain hotter upstream heat; the 60°C ceiling must not be applied to that different port.
2. Raising single-pass column capture from 65% to 90% does not establish a 30% reduction in closed-loop plant SEC. At fixed fresh nitrogen fixation and power, complete survival of returned fixed nitrogen is an explicit counterexample: recovery per pass improves and inventory falls, but steady acid production is unchanged. This is a counterexample to inference, not evidence that the actual plant has complete survival.
3. The measured batch remains a demonstrated result. The main text explicitly limits its approximately 5.3 MJ/mol SEC to power delivered to plasma. Generator input alone implies approximately 6.38 MJ/mol before auxiliaries, heating/cooling services, startup/shutdown and reset accounting.

## A. Heat grade: apply the bound at the correct port

### What the primary text says

- Line 169: 50 kW absorbed plasma power requires 60.5 kW microwave-generator input, corresponding to 82.6% grid-to-plasma efficiency.
- Line 245: gas leaving plasma is at bulk 1500–3000°C, depending on input power.
- Line 246: HEX #1 circulates approximately 100 L/min of water and recovers approximately 60% of plasma energy into a 7500 L tank at 60°C. The forced-air-cooled conical diffuser is at 300–450°C and is **not** part of the recovered-water system. HEX #2 cools approximately 100°C loop gas to room temperature to protect blowers.
- Line 4047 says recovered heat maintains the tank at 60°C, simulating a digestate ammonia stripper.
- Line 4049 proposes increasing recovery by collecting diffuser heat and then separately assumes 25% conversion of heat recovered by HEX #1 into electricity, reducing the projected 3.7 MJ/mol to 3.15 MJ/mol.

### Bound and hydraulic qualification

For heat supplied at 60°C and rejected to an assumed 25°C environment:

eta_C = 1 - 298.15 / 333.15 = 0.10506.

Thus 30 kW recovered heat (60% of 50 kW) has at most 3.15 kW reversible work potential when supplied isothermally at 60°C. The paper's arithmetic credits 7.5 kW, or 15% of plasma power, so 3.7 × 0.85 = 3.145 MJ/mol. This arithmetic is transparent; the unsupported element is the conversion efficiency at the demonstrated recovery port.

Water-side temperature rise also matters. Using a transparent approximate water property assumption, density 1 kg/L and heat capacity 4.18 kJ/(kg K):

30 kW / [(100/60 kg/s) × 4.18 kJ/(kg K)] = 4.31 K.

If, conditionally, HEX #1 receives well-mixed 60°C tank water, it could return water at approximately 64.31°C. This is NOT a measured inlet/outlet pair in the supplied text. The largest source-temperature Carnot bound then becomes 11.65%, still much less than 25%. Reversible recovery of the *incremental 30 kW* as this stream cools from 64.31°C back to 60°C would be:

W_rev = m_dot cp [(T_hot - T_cold) - T0 ln(T_hot/T_cold)] = 3.32 kW.

Do not count the exergy of cooling the entire recirculating water stream to ambient as though that were free extra heat recovered from the same 30 kW input. That would change the tank boundary and its steady operating condition.

At a 25°C sink, 25% ideal efficiency requires a source temperature of at least 124.38°C; any real engine requires a higher effective source temperature. Conversely, a 60°C source would need a sink no warmer than approximately -23.3°C even for ideal 25% conversion. Neither cold sink is a reported pilot service.

These are recovery-port limits, not bounds on a proposed engine installed upstream of HEX #1 on 1500–3000°C gas, nor on recovered 300–450°C diffuser heat. A different heat path must establish its own hot/cold temperature profiles, heat duty, NO survival during quench, corrosion constraints, pressure drop, heat-exchanger approach temperatures, auxiliary loads, and net electricity. The present heat utilization as a simulated ammonia-stripper supply cannot simultaneously be credited in full after the same heat has been diverted to electricity generation.

For illustration only, if the unproven 3.7 MJ/mol capture projection were retained, the isothermal-60°C reversible heat credit would give 3.7 × [1 - 0.6 × 0.10506] = approximately 3.47 MJ/mol on the plasma-power basis, before engine parasitics. This is not a corrected full-plant forecast.

## B. Closed-loop capture: distinguish improved per-pass capture from new production

Define a minimal steady pass model on a fixed-nitrogen basis:

- S: newly fixed nitrogen added per circulation pass, excluding already-fixed nitrogen returned to the torch.
- A: fixed-nitrogen flow arriving at the absorber.
- epsilon: fraction of that fixed-nitrogen flow captured as the defined recoverable product per pass.
- s: fraction of uncaptured fixed nitrogen surviving the rest of the loop and returning, after purge/leak losses, reconversion to N2, and other irreversible losses.

All quantities must be on a consistent nitrogen-atom basis; NO oxidation to NO2 or regeneration of NO during absorption is not creation/destruction of fixed nitrogen.

At steady state, with S and s invariant:

A = S + s(1 - epsilon)A = S / [1 - s(1 - epsilon)],

P = epsilon A = epsilon S / [1 - s(1 - epsilon)].

At equal power, the SEC ratio for epsilon .65 to .90 is:

SEC_90 / SEC_65 = (.65/.90) × (1 - .10s)/(1 - .35s).

| Return survival s | SEC ratio | Result from 5.3 MJ/mol |
|---|---:|---:|
| 0 | 0.7222 | 3.83 MJ/mol |
| 0.5 | 0.8316 | 4.41 MJ/mol |
| 0.8 | 0.9228 | 4.89 MJ/mol |
| 0.9 | 0.9594 | 5.09 MJ/mol |
| 1 | 1.0000 | 5.30 MJ/mol |

These are mathematical examples, not parameter estimates for this plant. The possible capture-only saving in this model ranges from 27.8% when uncaptured material is entirely lost to zero when it all survives. The paper's rounded 30% and 3.7 MJ/mol are not falsified by comparing them to 27.8% and 3.83. The material objection is that the large saving assumes a particular loss/source response not established by the quoted per-pass efficiency.

For the exact counterexample s = 1: A_65 = S/.65, A_90 = S/.90, but both product rates equal S. Improved capture lowers circulating fixed-N inventory and residence before capture; it does not increase steady new fixation. Any observed temporary production jump after changing columns can be release of held-up fixed nitrogen rather than permanent productivity gain.

### Why the actual loop needs measurements

- Line 247 ties quench/bypass choice, loop flow, residence time and capture efficiency together. They cannot automatically be held fixed when replacing columns.
- Lines 268 and 273 identify two real purge paths: a process-gas leak near blowers and analyzer exhaust. Their fixed-N flow rates are not quantified in the supplied passages.
- Line 269 describes entrained liquid/acid vapor, condensation and automatic return, so final absorber-liquid samples alone do not inventory the entire loop.
- Line 275 identifies approximately 5 psi column pressure drop and 7 psi torch pressure drop at full flow; changing packing/capture can change electrical blower duty and torch flow.
- Line 249 states that the approximately 65% observation corresponds to acid below 5%, with decreasing absorption as acid concentration rises. Lines 4025 and 4048 report acid-concentration dependence; the model predicts 66% down to 57% over the batch. One constant epsilon is therefore a deliberately simplified counterexample, not a batch reconstruction.
- Line 4003 reports composition dependence; line 4047 reports power/flow dependence. Fresh fixation S may change when the returning NO/NO2 mixture, O2 fraction, flow, pressure or thermal history changes. A simple epsilon multiplier cannot decide that coupled response.

### Exact missing discrimination and a sufficient ranking experiment

For the minimal capture-only model, the missing scalar is the effective survival fraction s of *already-fixed* nitrogen between absorber exit and its next absorber entry, measured at each operating condition. Total NOx concentration alone cannot distinguish surviving return from fresh plasma fixation. A suitably resolved tracer/perturbation balance that separates returning fixed nitrogen from newly fixed nitrogen, with measured molar flows and NO/NO2 speciation, would identify s and the fresh source S. A tracer is one possible identification method, not an asserted pilot instrument or a requirement to undertake a particular hazardous test.

For actual column/plant ranking, this scalar alone is insufficient. The decisive experiment is matched old/new-column operation at the same specified delivered acid concentration and product basis, recording:

1. Integrated whole-plant electrical input at the grid boundary, including generator, blowers, air compressor, PSA, liquid circulation, cooling/exhaust services and restart/reset requirements; separately metered recovered net electricity, if any.
2. Net recovered HNO3 nitrogen, including initial and final fixed-N inventories in gas, columns, condensate/demister, piping and collected liquid. Count dissolved NOx/nitrite separately from specified nitric-acid product rather than assuming all titratable acidity is the same product.
3. Time-resolved purge/leak/analyzer flows and their fixed-N composition; escaped/removed acid or liquid; NO/NO2 molar flows on both sides of the absorber and torch; enough identification to separate fresh generation from destruction/survival of return.
4. Actual pressure drops, torch and loop flows, O2/Ar composition, acid concentration trajectory, heat duties and inlet/outlet temperatures. These reveal whether the proposed capture gain is purchased with more compression, altered fresh fixation, changed quench or a lower-grade heat output.

Integrate across startup, production, shutdown and a comparable reset, or prove identical initial/final inventories and equivalent stored thermal/pressure states. The finite-interval fixed-N balance is:

fresh fixed nitrogen generated = recoverable product nitrogen + fixed nitrogen lost or destroyed + change in held-up fixed nitrogen.

Where acid is retained in the columns until extraction, classify that acid either as product or as inventory, never both. A lower terminal gas inventory may raise apparent batch acid yield once without giving the same recurring steady production advantage. Conversely, faster capture may reduce future destruction or purge loss, which is a genuine benefit once measured. Regenerated NO that remains fixed nitrogen stays in the circulating balance; it must not be counted as fresh S on each pass.

## C. Baseline energy boundary retained

Lines 4005 and 4046 report 30.9 operating hours, 198.9 L at 28.6 wt%, and 66.5 kg HNO3 on a 100% basis. The reported 1545 kWh = 50 kW × 30.9 h and approximately 5.3 MJ/mol are explicitly plasma-delivered quantities (line 4046). Using the reported 60.5 kW generator input gives 1869.45 kWh and approximately 6.38 MJ/mol for approximately 1055.35 mol acid. This is a lower-bound electrical boundary before unreported auxiliaries, not a measured all-in SEC. The 30.9 hours are operating hours, approximately 40% of the testing-period working hours (line 4005); elapsed campaign duty and intervening resets are not established by multiplying continuous operation alone.

No claim above negates the reported acid batch. It restricts what the measurements establish about the two projected improvements and identifies the experiment needed to rank actual integrated alternatives.

## D. Review of the parent's two additional conditional checks

### Oxidation-vessel residence time

Line 248 reports diameter 0.9 m, height 1.5 m, approximately 1 m3 volume, approximately 45 s residence, and 13.5 psig pressure. The geometric volume is approximately 0.9543 m3. Dividing that volume by 1300 standard L/min gives approximately 44.0 s, consistent with the quoted nominal residence but without converting standard volume to actual chamber volume.

If 1300 SLPM actually passes through that chamber, its reference is 273.15 K and 1 atm, chamber gas is 298.15 K, atmospheric pressure is 14.696 psi, and the entire geometric volume is effective gas volume, ideal-gas conversion gives approximately 0.01233 m3/s actual flow and approximately 77.4 s space time. The reference conditions, actual branch flow, effective gas volume and temperature are not established by these passages; thus 77.4 s is a conditional calculation, not a corrected measured residence time. State the inconsistency as a request to reconcile pressure, standard-flow basis and residence definition. It does not invalidate measured acid output, and real residence-time distributions need not equal geometric space time.

### Thermal storage versus sustained useful heat

At 30 kW over 30.9 operating hours, recovered heat would integrate to 3.337 GJ. A 7500 L water inventory heated from an *assumed*, not reported, initial 25°C to 60°C stores approximately 1.097 GJ using 1 kg/L and 4.18 kJ/(kg K). In an otherwise adiabatic continuous idealization, it reaches 60°C after approximately 10.16 hours. Thus approximately 2.24 GJ needs a removal/rejection path if 30 kW truly is sustained over the entire batch and these initial/final states apply.

This is not evidence that the authors omitted a real operating load. “Maintain” at 60°C (line 4047) is compatible with heat rejection, intentional demand, or losses; 30.9 hours were intermittent operating hours, so heat loss between periods is also possible. The stated 60% recovery may be an operating-point result rather than a time-integrated batch recovery. Record tank temperatures over calendar time and heat delivered to an actual load separately from heat stored and rejected. Only measured useful output on the chosen system boundary supports a coproduct credit; gross heat delivered to the tank and a separate engine credit cannot both spend the same energy twice.
