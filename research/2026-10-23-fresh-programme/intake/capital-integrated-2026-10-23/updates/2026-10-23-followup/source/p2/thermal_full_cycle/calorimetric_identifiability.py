"""Two explicit models with identical normalized thermal relaxation.

This is a synthetic identifiability counterexample, not a fit to any experiment.
Positive q means pump-induced net removal from the observed specimen.
No experimental waveform or acquired temperature measurement is used.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp


def main():
    out=Path(__file__).resolve().parent
    C=1.0                         # J/K, synthetic
    G=1.0                         # W/K, synthetic passive conductance
    bath=290.0                    # K, synthetic independent calorimeter anchor
    target=300.0                  # K
    slope=.6                      # W/K pump-induced differential conductance
    offsets=[.2,-.2]              # W at target: opposite signs of net removal
    heater=10.0                   # W before a small calibrated step
    delta_heater=.1
    ts=np.linspace(0,4,801)
    rows=[]; traces=[]
    for q_at_target in offsets:
        # C*Tdot = Pe - G*(T-bath) - [slope*(T-target)+q_at_target].
        steady=(heater+G*bath+slope*target-q_at_target)/(G+slope)
        final=steady+delta_heater/(G+slope)
        def rhs(t,y):
            return [(heater+delta_heater-G*(y[0]-bath)
                     -slope*(y[0]-target)-q_at_target)/C]
        sol=solve_ivp(rhs,[ts[0],ts[-1]],[steady],t_eval=ts,
                      rtol=1e-11,atol=1e-12,max_step=.01)
        normalized=(sol.y[0]-steady)/(final-steady)
        traces.append(normalized)
        clamp_heater=G*(target-bath)+q_at_target
        rows.append(dict(net_removal_at_300K_W=q_at_target,
            unclamped_initial_temperature_K=steady,
            unclamped_final_temperature_K=final,
            normalized_relaxation_time_s=C/(G+slope),
            heater_needed_to_clamp_300K_W=clamp_heater,
            heater_change_relative_to_pump_off_W=clamp_heater-G*(target-bath)))
    err=float(np.max(abs(traces[0]-traces[1])))
    assert err<1e-9
    result=dict(status='SYNTHETIC_IDENTIFIABILITY_COUNTEREXAMPLE',
        no_experimental_data_used=True,models=rows,
        maximum_normalized_trace_difference=err,
        pure_radiation_heating_only_example=dict(
            tau_off_over_tau_on=1.67,
            temperature_ratio_needed=1.67**(1/3),
            T_off_K=300.,T_on_K=300*1.67**(1/3),
            assumption='radiation dominates differential conductance; constant heat capacity'),
        interpretation='Relaxation identifies a derivative, not the sign of the absolute net heat. Electrical substitution at fixed true temperature identifies the signed increment if other heat paths are held fixed.')
    (out/'calorimetric_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
