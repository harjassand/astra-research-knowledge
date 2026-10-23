# Source-pinned NumPy nitrogen kinetics and properties

This replaces repeated scalar property calls, not the mechanism or physical model.
It evaluates the unchanged six-species, seven-reaction `paper_model.gas_model()`
variant with the supplied NASA data from `sources/air.yaml`. No BVP, geometry
change, parameter sweep, physical-validity claim, or universal performance claim
is part of this package.

## Interface

```python
from kernel import Kernel
K = Kernel()  # Loads and SHA-256 checks cache once. Does not import Cantera/SciPy.
r = K.evaluate(T, Y)  # T: scalar or (N,); Y: (6,) or (6,N); P defaults to 101325 Pa.
```

Species order: N2, O2, N, O, NO, NO2. Outputs keep a length-one batch for scalar
inputs. `mass_production`: kg/m3/s, `rho`: kg/m3, `cp`: J/kg/K,
`h_species`: J/kg, `enthalpy`: J/kg, `viscosity`: Pa s, `conductivity`: W/m/K.
`T`, normalized `Y`, mole fractions `X`, and normalization diagnostics are also
returned. `return_rates=True` adds kmol/m3/s forward/reverse/net reaction progress,
log(Kc), species cp, h/RT, and s/R.

The enforced numerical domain is 200–3500 K and exactly 101325 Pa. NASA and pure
transport helpers enforce the same temperature domain. Nonfinite, empty,
malformed, and all-nonpositive compositions fail. As Cantera TPY does, the default
clips negative Y to zero and then normalizes; diagnostics report raw minima,
raw sums, negative entries, and normalization changes. This is for trial states,
not a license to accept an unphysical final solution. `strict=True` rejects any
negative input and any mass-sum deviation above 1e-12. Check final-state source
fractions and diagnostic flags; do not infer physical validity from solver success.

### Enthalpy-state interface

```python
inv = K.temperature_from_enthalpy(h, Y, T_guess=None)
r = K.evaluate_hpy(h, Y, T_guess=None)
```

HP inversion uses positive-cp safeguarded Newton/bisection on the two NASA
branches, with 200–3500 K endpoints. Default residual tolerance is
1e-6 + 2e-13*max(1,abs(h)) J/kg. Impossible enthalpies fail. Only explicit
`trial_clamp=True` in nonstrict mode permits clamping to the domain or nearest
NASA-splice endpoint, and returns original/effective targets and residuals,
`enthalpy_clamped`, and `NASA_splice_gap_input`. Never accept a clamped final state.
`strict=True, trial_clamp=True` is rejected.

The supplied NASA fits are not exactly enthalpy-continuous at 1000 K. Species
h(high)-h(low), in J/kg, is approximately [-0.1855573, -0.0021558, -0.5916484,
-0.0260586, -0.0825914, +0.0896419]. These are preserved, not smoothed. A negative
mixture jump can give two valid nearby roots: `NASA_splice_ambiguous` flags this,
`T_guess` selects its side, and absent a guess the low branch is selected. A
positive jump creates an enthalpy gap, which fails unless diagnostic trial
clamping was requested. Native Cantera can choose a different nearby root based
on its previous state. The known-input batch observed alternate roots differing
by up to 0.000399 K. Do not treat a source discontinuity as a globally smooth
constitutive law when interpreting collocation convergence.

## Construction and numerical scope

- NASA7 coefficients, molecular weights, stoichiometry, and elemental counts are
  exported as float64 from the actual source-built Cantera phase, with no new
  decimal rounding. At exactly 1000 K the low branch is used, matching Cantera.
- The seven explicit original rate expressions, including specified effective
  third bodies and Lindemann falloff, are implemented directly. Reverses use
  common NASA detailed balance: log Kc = -Delta(g/RT) + Delta(nu)*log(P0/RT).
- Net reaction progress uses a signed log-domain `expm1` difference. This avoids
  avoidable cancellation, but cannot make finite-precision equilibrium fluxes
  exact. Subnormal log-domain fluxes may survive when Cantera's intermediate
  concentration products underflow. Their absolute values are negligible, and
  no meaningful relative accuracy claim is made for such tiny rates.
- Pure-species viscosity and conductivity are sampled from the pinned Cantera
  phase at 661 temperatures, every 5 K from 200 to 3500 K. The actual samples and
  not-a-knot cubic coefficients in log(property) versus log(T) are in `cache.npz`.
  SciPy is used only to build the cache; runtime interpolation is NumPy.
- The Wilke viscosity rule and half arithmetic/half harmonic conductivity rule
  were checked using exact native pure properties, independently of interpolation;
  sampled agreement is within 4.45e-16 relative.
- Table interpolation is approximate: worst sampled off-grid pure-property error
  is 1.04e-8 viscosity and 1.11e-7 conductivity, concentrated near the lower
  boundary. Mixture errors in the 1085-state batch are 9.37e-9 and 1.01e-7.
- N2 NASA data formally start at 300 K; 200–300 K is inherited extrapolation.
  The mixture transport fit is also extrapolated below its 300 K phase minimum.
  R6's recommended source range ends at 2200 K. Agreement up to 3500 K validates
  numerical reproduction, not these physical extrapolations.

## Results and preserved failures

`validation.json` records 1085 deterministic diverse states: pure species,
zero/trace fractions down to 1e-280, Dirichlet and log-uniform mixtures, air,
native TP equilibrium, near-equilibrium perturbations, and clipped/nonunit trial
inputs. Separate off-grid transport checks cover 482 temperatures. Maximum cp
relative error is 6.59e-16; species h error is 1.50e-8 J/kg; mass-source error is
1.80e-13 of gross species mass flux. Maximum absolute mass-source discrepancy is
1.09e-5 kg/m3/s in very large-flux states, not an absolute bound for all states.
Scaled elemental/mass residuals are below 2e-16. Detailed-balance residuals of
native equilibrium states are reported for both methods, rather than dividing
by a nearly zero net rate. All declared T,Y validation gates pass.

`hpy_validation.json` compares the same 1085 states: unique-branch known-input
T reconstruction is within 2.53e-9 K, and kernel enthalpy residual is below
3.31e-6 J/kg. The original proposed comparison gate of 1e-5 K against native HPY
FAILED at 1.80e-5 K and is retained in
`hpy_validation_initial_overstrict_gate.json`. Investigation showed native HPY
itself missed the known TP-generated enthalpy by up to 0.0267 J/kg. The final
correctness gate uses known-input reconstruction and the actual enthalpy residual,
not a silently loosened native-comparison threshold. Native differences remain
reported. A deliberate pure-NO2 gap test rejects by default and explicitly flags
an opt-in clamp with 0.0448 J/kg residual against the original impossible target.

An initial validation-report JSON serialization failure is retained in
`validation_initial_serialization_failure.stderr`; it was a NumPy boolean
reporting issue, not a numerical result. The independent audit and follow-on
inversion audit preserve initial findings and final resolutions separately. The
independent audit found and preserved one HP tolerance-validation bug: infinite
rtol could bypass domain rejection. It is fixed and independently rechecked.
Tolerances must be finite/nonnegative; domain and splice-gap feasibility now use
a separate float64 roundoff allowance, so even a huge finite solver tolerance
cannot bypass feasibility. The final focused 10-case audit found no remaining issue
in its bounded scope.

## Workload-specific timings

`benchmark.json` includes raw seven-repeat timings, imports, construction, one
warmup, RSS, and checksums in separate fresh processes with one BLAS thread.
All requested properties are computed from identical saved T/Y or h/Y batches.
Batches are drawn from validation states, with splice-adjacent T moved to 1001 K
for throughput only. This is not an end-to-end BVP measurement.

| States | Mode | Native median | Vector median | Native/vector |
| --- | --- | --- | --- | --- |
| 1024 | TPY | 8.937 ms | 1.913 ms | 4.67 |
| 4096 | TPY | 40.002 ms | 8.153 ms | 4.91 |
| 1024 | HPY | 11.233 ms | 6.021 ms | 1.87 |
| 4096 | HPY | 40.180 ms | 15.873 ms | 2.53 |

At 4096 states, process maximum RSS was 42508/33276 KiB for native/vector TPY and
42568/34508 KiB for HPY. Runtime object construction, excluding imports and data
loading, was about 7.1–9.9 ms native and 7.4–9.3 ms vector. Imports were about
69–107 ms native and 48–60 ms vector. Cache construction separately cost 0.433 s
including imports, peak RSS 76044 KiB. The final rerun pins the final kernel hash; the earlier pre-guard benchmark is also
retained. This shared host was not CPU-isolated; variation between these runs is
visible and expected. No speedup is promised for other batch
sizes, CPUs, mechanisms, composition distributions, or integration workflows.

## Reproduce

Use Python 3.12, NumPy 2.3.5; rebuilding additionally uses SciPy 1.17.0 and the
existing source-local Cantera 3.2.0. No installation or network is required here.
From this directory:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python validate.py
python validate_hpy.py
python benchmark.py
python make_receipt.py --verify
# Only if intentionally regenerating the cache, then rerun all validations:
python build_cache.py
```

Regeneration can change timing values and archive hashes. The manifest pins the
original source hashes, species/reaction identity, actual cached data hash,
software versions, construction scope, and extrapolations. The receipt hashes
the delivered code/data/results and confirms the source files remain unchanged.
