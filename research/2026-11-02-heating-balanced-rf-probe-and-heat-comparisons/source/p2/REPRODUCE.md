# Reproduce and inspect

Requires Python 3 with NumPy, SciPy and Matplotlib, no external network calls.

From this folder:

```
python wave_force_transfer.py
python control_rank_test.py
python rotating_gramian.py
python mhw_counterfactual.py
python response_probe.py
python temporal_reachability_probe.py
python temporal_validate.py
python matched_controller_comparison.py
python plots.py
python test_interfaces.py
```

The mHW fixed-step RK4 N40 run uses dt=.01 for explicit hyperdiffusion stability. An earlier dt=.025 run overflowed and is NOT a successful result. The prepared N40 `mhw_counterfactual_results.json` uses burn35,T45, seed19. `response_probe_results.json` uses N32 burn80,T5, seeds19,22,27, dt=.01. Temporal positive/negative probes use the same numerically generated state per seed. All 3 temporal validation results use desired phase .001 rad, not larger extrapolations. The sample numeric results are exploratory floating point. Interval bounds not produced for nonlinear PDE time stepping.

`wave_force_transfer.py` checks independent Maxwell Poynting/Drude loss expressions. `energy_conserving_ray` is downstream arithmetic from *supplied test damping rates* and is **not** a BORAY run. The `.tar` Gkeyll archives were not downloaded.

For extended precision/physical source validation one would need full magnetic geometry, antenna fields, species-resolved hot dielectric, actual ray/full-wave damping, dressing momentum from the Hermitian susceptibility, a nonlinear gyrokinetic intervention dataset and time-resolved heat flux. The current repository supplies none of these as established physical output.

`test_interfaces.py` checks the exact scheme-level source power balance, wave ±ky parity, ray power conservation, projected mHW forcing channel, complex amplitude/phase identity and rotating Gramian identity. It does not constitute independent scientific validation of the reduced model.

## Extended physical-model and heat tests

Run these from the same folder (NumPy/SciPy/Matplotlib):

```bash
python isoheating_rank_audit.py
python dressed_momentum_test.py
python energy_budget_audit.py
python heat_response_convergence.py
python heat_vs_phase_matched.py
python analyse_results.py
```

`mhw_heat_transport_results.json` is retained from the finite N32, dt=.0125, burn=60, horizon=18, five-seed run:

```bash
python mhw_heat_transport.py --N 32 --dt .0125 --burn 60 --horizon 18 --eps .003 --seeds 19 22 27 31 37
```

That full run takes substantially longer than the diagnostic checks. Re-running `mhw_heat_transport.py` without these flags would run its *different* default experiment and overwrite the recorded file. The deliberately retained `heat_run.log` records the rejected coarse-step divergent run; `heat_run2.log` records the accepted parameter run. `heat_response_convergence.py` checks three short-horizon steps, not convergence of stationary transport. `heat_vs_phase_matched.py` uses three **offline** branch rollouts for each of three states and has explicit cost/information caveats. All archived JSON outputs are floating-point diagnostics or descriptive intervals, not validated numerical-interval bounds for the nonlinear PDE.
