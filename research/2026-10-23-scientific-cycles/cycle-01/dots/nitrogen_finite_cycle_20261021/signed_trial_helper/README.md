# Signed Newton-trial continuation

Decision: bounded synthetic checks support using this helper as a candidate numerical continuation for Newton iterations. This is not evidence that a trajectory is accurate, that negative states are physically admissible, or that the cycle improves performance. Root retains cycle/acceptance ownership. No cycle was run here.

`from helper import SignedTrialKernel`; `evaluate_rho_u(rho,U,Y,T_guess=None,strict=False,trial_clamp=False,return_rates=False)` matches the prior interface. U is J/m³, rho is kg/m³, concentrations are kmol/m³, species order N2/O2/N/O/NO/NO2. `evaluate` is inherited for physical initialization. `strict=True` rejects every negative Y. Nonstrict trial states permit at most 0.001 total negative mass fraction, require unit signed mass sum within 1e-12, positive density, positive mixture gas constant, positive cv throughout the temperature range, 200–3500 K, and 0.5–2 atm. No signed composition is normalized.

Thermochemistry is linear in signed Y. Conservative energy is rho sum(Y_i u_i(T)). Safeguarded Newton/bisection uses the unchanged continuous-NASA coefficients. Whole-range cv extrema are computed from polynomial stationary points on each NASA branch; this is a float64 numerical guard, not a formally rounded proof. Branch h/s continuity is inherited up to the documented stored-coefficient roundoff. Original/effective energy and pressure diagnostics are preserved. Explicit trial_clamp retains the old opt-in energy clamp and reports its original/effective residual; this does not authorize acceptance.

Chemistry uses the exact integer mass-action monomial structure with signed concentrations. Signed logarithmic magnitudes are an evaluation strategy, not a fractional-power or absolute-concentration model: monomial signs are retained. Same-sign opposing fluxes use expm1 to preserve stable cancellation; opposite-sign fluxes add algebraically. Third-body concentrations use signed concentration sums; Lindemann reduction uses that actual signed sum. Nonpositive third-body sums reject the trial. Stoichiometry remains unchanged and exactly atom balanced even off-domain.

Only viscosity/conductivity use a clipped-normalized positive-mixture trial extension. All EOS, thermo, composition, density and rate fields returned by evaluate_rho_u are overwritten consistently from raw signed Y. Diagnostics explicitly disclose transport_clipped_mixture and transport_composition_max_change. `evaluate` remains the inherited physical initializer and is not the signed path.

Run the synthetic test:
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=$PWD/nitrogen_quench_recovery_20261021/deps python nitrogen_finite_cycle_20261021/signed_trial_helper/validate.py

Validation includes positive-state agreement against the pinned continuous-NASA evaluator; signed energy/EOS inversion; integer element balance and floating mass/element residual; direct independent all-seven polynomial mass action including falloff; left/right fixed-T fixed-other-concentration N=0 restoration against an independent complex-step polynomial derivative; and explicit rejection checks. Complex step differentiates the independent analytic polynomial implementation, not the signed-log implementation. No native Cantera derivative was required, and no solver-convergence inference is drawn.

Dependencies and original/cache files are referenced in manifest.json, not changed or copied. No failed test attempts occurred. Performance receipts describe this synthetic test only and exclude development/tool overhead.
