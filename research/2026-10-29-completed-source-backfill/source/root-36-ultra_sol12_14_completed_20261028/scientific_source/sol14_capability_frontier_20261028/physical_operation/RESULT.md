# Bounded physical-operation result

**No new feasible physical capability was acquired.** A continuously replenished liquid-Ga anode for aluminum-scrap upgrading was constructed as a transport model and challenged against directly renewed solid-anode electrorefining. The simple claim that a fast liquid host plus an anode potential below a visible Ga dissolution onset supplies pure, continuous Al production fails an explicit countermodel.

This changes the question from the old powder metrology branch. The desired enabling action was to turn compositionally contaminated scrap into useful Al without repeated exposure of a passivating solid anode or bulk remelting. A liquid intermediary could, in principle, separate solid-feed admission from the electrochemical interface. Sustained selective feed admission and purity are necessary parts of that operation.

## What was executed

The code solves a coupled Ga-leakage/Al-throughput calculation with:

- exact electron and atom counts, including Ga(I) leakage and four Al2Cl7 complexes per deposited Al;
- an exact finite-kinetics Nernst–Planck transport expression;
- an independent ordinary boundary-value solver at three drift values;
- both equal-film and the stronger species-dependent Levich hydrodynamic comparator;
- finite host inventory, impurity stream and production-area accounting;
- a conditional constant-potential versus pulsed-potential comparison.

The independent BVP flux agrees with the closed expression within 5e-13 relative error. This is an implementation control, not an acquired material law.

The numerical scenario deliberately exposes its missing inputs. Ga diffusion/formal-potential observations and Al-complex diffusion observations come from different ionic liquids and temperatures. Activities, interfacial rates, speciation, effective electric field, Ga support/wetting and dirty-feed admission are unqualified. The combined numbers are a countermodel to an inference, not a prediction of an actual Al–Ga cell.

## The discriminating result

At the supplied anode potential +0.20 V:

| Equally granted transport model | Al output, kg/m^2/h | Predicted Ga, ppm |
|---|---:|---:|
| Equal diffusion films | 0.0236763 | 5519.145 |
| Ordinary Levich species-dependent films | 0.0675167 | 1822.968 |

Both exceed the entire 1000 ppm impurity budget of 99.9% Al, despite +0.20 V being below a separately reported visible Ga dissolution onset near +0.325 V. The source regimes are not identified as equal.

For the stronger Levich model, the declared Ga gates permit maximum anode potentials of:

| Ga gate | Maximum model anode potential |
|---|---:|
| 1 ppm | +0.003812 V |
| 100 ppm | +0.124117 V |
| 1000 ppm | +0.184292 V |

The equal-film 1 ppm threshold was negative. The stronger ordinary comparator changes that conclusion and leaves a narrow positive window. No universal purity impossibility follows. Slow Ga kinetics, altered activity, selective barriers or a Ga-recovery stage could change the result; those are not supplied by a visible-onset measurement.

The surviving analytical result is a coupled flux/purity gate. Under the supplied fixed transport laws, increasing ordinary mixing scales productive Al and Ga leakage together; it does not by itself improve composition. Favorable metal-side transport has about 32 times the capacity of the stronger ionic-transport scenario, so faster motion inside Ga does not remove the modeled limiting step.

## Independent alternative and full costs

The retained alternative was direct solid-anode electrorefining with qualified surface renewal. A [2026 primary study](https://doi.org/10.1016/j.seppur.2026.137071) reports a laboratory ultrasonic regime giving 99.90 wt% Al at 343 K, 98.90% current efficiency and 0.65 V. It is a stronger starting point than granting the new host a free passivation remedy. Earlier primary low-temperature electrorefining and solid-state scrap-upgrading results were also screened.

The reported 1.958 kWh/kg is numerically consistent with cell-charge energy, calculated here as 1.95853 kWh/kg. That does not prove all auxiliaries were excluded, and no complete measured ultrasound/heat/bath/handling ledger was acquired. Neither route has an established full-cycle advantage in this work.

Even in the favorable host scenario, initial dissolved Al lasts only minutes. Product beyond preload requires continuing dirty-scrap admission, Ga recovery, residue management and repeated harvesting. A supplied 100 micrometre Ga layer would require about 8.89 t of host for 1 t/h at the stronger modeled throughput. This is a scenario extrapolation, not a universal resource lower bound; thinner supported layers and different transport would need their own qualification.

## Accepted scope and stopping decision

Root independently whole-read the model derivation and accepted its Nernst sign, Robin/drift flux, charge/atom counts, mass ratio, conditional scaling/Jensen control and inventory arithmetic at the stated supplied-model scope. Root required the Levich correction and did not validate the source-regime transfer or actual material laws.

The chosen architecture is **not advanced as an acquired feasible scrap upgrader**. The ordinary alternative is source-reported laboratory capability, not our invention or a demonstrated industrial solution. Generic transport theory, electrorefining and liquid-metal electrodes are established; novelty and practical superiority are UNKNOWN.

Proof: PROOF.md. All calculation code and outputs: code/redox_transport.py and results/REDOX_TRANSPORT.json. Source boundaries, costs and replay: COSTS_AND_REPLAY.md and sources/PRIMARY_INPUTS.json. Review scope: REVIEW_RECEIPT.md.
