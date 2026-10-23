# Conservative gas helper: explicitly modified thermochemical model

This is a small helper, not a finite-cycle solver. It keeps the original property kernel and cache unchanged, loads their pinned source, and uses a separately pinned cache. A new high-temperature NASA7 a6/a7 adjustment makes enthalpy and entropy continuous at1000K to floating coefficient precision, while leaving all cp polynomials, low-temperature branches, transport tables, forward reaction constants and stoichiometry unchanged. The variant changes equilibrium and reverse rates and MUST NOT be described as the unchanged original operator.

## API

Use `from helper import ThermoKernel; k=ThermoKernel()` with this directory on Python's module path.

- `k.evaluate(T,Y,P,strict=True,return_rates=True)`: property/kinetic batch. Species axis0, order N2,O2,N,O,NO,NO2. P may be scalar or a batch vector. Added `cv`, `Rmix`, `e_species`, `internal_energy` in SI mass units.
- `k.temperature_from_internal_energy(e,Y,T_guess=None,strict=True)`: e in J/kg, with chemical formation energy. Safeguarded Newton/bisection,200–3500K. Output T,Y,diagnostics. Does not need pressure for an ideal gas.
- `k.evaluate_ey(e,Y,P,...)`: inverse followed by kinetics/properties.
- `k.evaluate_rho_u(rho,U,Y,...)`: rho in kg/m3 of gas, U=rho*e in J/m3 of gas. Determines T and P, then properties. It does NOT multiply by bed porosity. Returns pressure, rho_input, internal_energy_density_input and conservative_energy_residual_J_m3.

Pressure domain is0.5–2atm. An explicit1e-10 P0 (0.0000101325Pa) numerical endpoint allowance covers inversion residual at a pressure boundary. Such inputs are snapped to the endpoint and pressure_original_Pa, pressure_effective_Pa and pressure_boundary_snap are reported. This is a disclosed numerical allowance, not exact-domain certification. Grossly out-of-range or nonfinite P rejects. Standard reference pressure P0 in Kc stays101325Pa.

Strict mode requires nonnegative unit-sum Y. Nonstrict mode clips and renormalizes Y exactly as the inherited source kernel, with diagnostics; never hide that change in an accepted conservative state. `trial_clamp=True` is opt-in, nonstrict only, for out-of-range energy during a solver's rejected trials. Original and effective residuals are returned. It is not admissible accepted-state clipping.

## Pressure physics

Concentrations are rebuilt as C_i=rho Y_i/W_i at actual P. Third-body concentrations and Lindemann reduced pressure are recomputed. At fixed T,Y, dissociation forward fluxes have P² while reverse recombination has P³; exchange reaction directions have P²; the NO+O(+M) channel has the exact P-dependent Lindemann fraction, multiplying P² forward and P reverse concentration products. Uniform P² scaling is wrong. pressure_scaling_check.py independently tests these formulas.

## Evidence and bounded changes

815 native corrected-Cantera comparisons, including0.5/0.8/1/1.2/2atm anchors and random states, passed. Maximum mass-source discrepancy is1.49e-13 of species gross reaction mass flux, not a misleading relative error on a near-zero net source. Internal-energy inversion reconstructs known T within6.65e-9K with≤5.85e-6J/kg original residual. Pressure reconstruction error≤7.15e-7Pa. Exact-rational Bernstein polynomial bounds establish cp/R−1≥1.4745 for each species on both declared branches; positive mixtures therefore have positive cv inside each branch.

Maximum species enthalpy change from the original NASA source is0.59165J/kg; entropy change≤0.00053568J/kg/K. The analytic absolute-log bound implies reverse-rate relative changes≤2.3441e-6 over300–3100K. This is a coefficient/rate bound, NOT a bound on a stiff integrated trajectory. Actual stored floating coefficients leave splice residuals recorded in pressure_scaling_check.json (not exact-real continuity). Default inverse tolerance exceeds those residuals; pathological exact-zero tolerances may fail and return no state.

Two initial failures are retained: an interpolated initial temperature exceeded the endpoint by floating roundoff (fixed by clipping the initial guess to its bracket); pressure reconstructed at an exact endpoint could slightly leave the domain (addressed by the explicit numerical boundary allowance, not silently discarded). Invalid pressure, negative density, nonfinite/impossible energy, strict negative composition, invalid tolerances, strict clamping and a loose-tolerance domain-bypass attempt reject.

Validation wall time is recorded in validation.json, with Linux RSS inKiB. No cycle/BVP, device validation, hardware, spending or universal numerical guarantee was performed. Dependencies are numpy plus Cantera for reference validation; inherited source uses no Cantera during helper evaluation.
