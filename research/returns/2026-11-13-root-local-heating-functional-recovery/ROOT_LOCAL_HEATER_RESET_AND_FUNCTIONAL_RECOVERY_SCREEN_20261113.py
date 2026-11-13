#!/usr/bin/env python3
"""Introduced lumped diagnostics; no measured material calibration or physical validation."""
from __future__ import annotations
import json, math
from pathlib import Path

def node_temperature(t, resistance, current=.5, capacitance=.25, conductance=.01, ambient=25.):
    return ambient + current**2 * resistance/conductance * (-math.expm1(-conductance*t/capacitance))

def crossing_time(target, resistance, current=.5, capacitance=.25, conductance=.01, ambient=25.):
    steady_rise=current**2*resistance/conductance
    rise=target-ambient
    if rise <= 0: return 0.
    if rise >= steady_rise: return None
    return -capacitance/conductance*math.log1p(-rise/steady_rise)

def massflow(p, area, ambient_pressure=100000., temperature=298.15, cd=.65):
    # Ideal-gas isentropic orifice surrogate; not an actual crack/valve flow map.
    gas_r=287.05; gamma=1.4
    if p <= ambient_pressure or area == 0: return 0.
    ratio=ambient_pressure/p
    critical=(2./(gamma+1.))**(gamma/(gamma-1.))
    if ratio <= critical:
        factor=math.sqrt(gamma)*(2./(gamma+1.))**((gamma+1.)/(2.*(gamma-1.)))
    else:
        factor=math.sqrt(2.*gamma/(gamma-1.)*(ratio**(2./gamma)-ratio**((gamma+1.)/gamma)))
    return cd*area*p/math.sqrt(gas_r*temperature)*factor

def leak_trace(radius, duration=5., step=.001, temperature_change=0., volume=1e-5, kappa=0.):
    # V(p)=V0*(1+kappa*(p-p0)); zero kappa is a rigid vessel.
    # Uniform externally specified temperature ramp. No polymer creep or pump is supplied.
    p0=150000.; t0=298.15; gas_r=287.05
    area=math.pi*radius**2
    def rhs(t,p):
        temp=t0+temperature_change*t/duration
        tempdot=temperature_change/duration
        v=volume*(1.+kappa*(p-p0))
        vp=volume*kappa
        return (-gas_r*temp*massflow(p,area,temperature=temp)+(p*v/temp)*tempdot)/(v+p*vp)
    p=p0; t=0.; n=round(duration/step)
    for i in range(n):
        dt=min(step,duration-t)
        k1=rhs(t,p); k2=rhs(t+dt/2.,p+dt*k1/2.)
        k3=rhs(t+dt/2.,p+dt*k2/2.); k4=rhs(t+dt,p+dt*k3)
        p += dt*(k1+2*k2+2*k3+k4)/6.; t += dt
    return {"radius_um":radius*1e6,"temperature_change_K":temperature_change,
            "volume_pressure_compliance_per_Pa":kappa,"final_pressure_Pa":p,
            "pressure_drop_Pa":p0-p}

def main():
    current=.5; r_hi=9.; r_lo=1.; ambient=25.; fuse=200.; melt=160.; rate=.5
    tf=crossing_time(fuse,r_hi,current=current)
    tm=crossing_time(melt,r_hi,current=current)
    assert tf is not None and tm is not None
    # Two series elements exchange physical roles. Their total resistance and terminal I,V
    # histories are identical, including opening when either high-resistance element fuses.
    cold_wait=.25/.01*math.log((fuse-ambient)/(50.-ambient))
    states=[]
    for name,wound_r,lead_r in [("wound_is_high_resistance",r_hi,r_lo),
                               ("lead_is_high_resistance",r_lo,r_hi)]:
        tw=node_temperature(tf,wound_r)
        tl=node_temperature(tf,lead_r)
        start=crossing_time(melt,wound_r)
        dwell=max(0.,tf-start) if start is not None else 0.
        extent=-math.expm1(-rate*dwell)
        states.append({"name":name,"wound_R_ohm":wound_r,"lead_R_ohm":lead_r,
                       "terminal_voltage_before_fuse_V":current*(wound_r+lead_r),
                       "terminal_current_before_fuse_A":current,"terminal_open_time_s":tf,
                       "wound_temperature_at_open_C":tw,"lead_temperature_at_open_C":tl,
                       "introduced_hot_closure_extent":extent,
                       "introduced_99pct_closure_test":extent >= .99})
    local_witness=[{"name":s["name"],"actual_local_voltage_V":current*s["wound_R_ohm"],
        "introduced_observed_voltage_interval_V":[current*s["wound_R_ohm"]-.05,current*s["wound_R_ohm"]+.05],
        "introduced_local_power_lower_bound_W":.49*(current*s["wound_R_ohm"]-.05)} for s in states]
    traces=[leak_trace(r*1e-6) for r in [0,1,2,5,10]]
    variations=[leak_trace(2e-6,temperature_change=d,kappa=k)
                for d in [-.1,0.,.1] for k in [0.,5e-6]]
    assert states[0]["terminal_open_time_s"]==states[1]["terminal_open_time_s"]
    assert states[0]["introduced_99pct_closure_test"] and not states[1]["introduced_99pct_closure_test"]
    assert abs(traces[0]["pressure_drop_Pa"]) < 1e-6
    warm_no_leak=leak_trace(0.,temperature_change=.1)
    assert abs(warm_no_leak["final_pressure_Pa"]-150000.*298.25/298.15)<1e-5
    result={
      "scope":"INTRODUCED model; not measured SEBS/LM/silicone properties, functional strength, hardware or novelty",
      "source_reference_scope":"Krings et al 2025 reports 0.5A local repair and separate reset; other model values are introduced, not fitted to that experiment",
      "series_electrothermal_indistinguishability":{
        "assumptions":{"constant_series_resistance_ohm":[r_hi,r_lo],
          "identical_node_capacitance_J_per_K":.25,"identical_node_conductance_W_per_K":.01,
          "ambient_C":ambient,"introduced_fuse_threshold_C":fuse,
          "introduced_closure_threshold_C":melt,"introduced_closure_rate_per_s":rate},
        "states":states,"energy_until_fuse_J":current**2*(r_hi+r_lo)*tf,
        "optional_local_voltage_witness":local_witness,
        "local_witness_limit":"Four-terminal/local taps with introduced +/-0.05V and current>=0.49A would distinguish the pair; real damage-site wiring, resistance evolution, thermal coefficients, closure kinetics and restored strength remain unconstructed/unqualified.",
        "cooldown_from_fuse_to_50C_s":cold_wait,
        "limitation":"Terminal-only electrical reset cannot distinguish these two locations under the declared model; actual thermal imaging or known lead constraints can distinguish them. No universal all-sensor obstruction."
      },
      "introduced_isolated_gas_proof":{
        "assumptions":{"initial_absolute_pressure_Pa":150000.,"ambient_pressure_Pa":100000.,
          "initial_temperature_K":298.15,"initial_volume_m3":1e-5,
          "duration_s":5.,"discharge_coefficient":.65,"gas_R_J_per_kgK":287.05,
          "gamma":1.4,"sensor_error_each_endpoint_Pa":50.},
        "rigid_isothermal_traces":traces,"temperature_and_compliance_variations":variations,
        "warm_no_leak":warm_no_leak,
        "limitation":"Pressure decay is affected by temperature, volume compliance and creep. Airtightness does not establish restored force, strength, fatigue, adhesion or material inventory."
      },
      "not_supplied":["actual thermal coefficients and resistance evolution","damage geometry and fuse location",
        "actual polymer closure and post-cooling strength","fixed-volume isolated pressure fixture",
        "sensor calibration","useful-load motion and fatigue","repeated renewal and chemical stocks",
        "whole-cycle energy/cost advantage","physical experimental validation"]
    }
    out=Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"states":states,"energy_until_fuse_J":result["series_electrothermal_indistinguishability"]["energy_until_fuse_J"],
      "cooldown_s":cold_wait,"rigid_isothermal":traces,"variations":variations,"output":str(out)},indent=2))
if __name__=="__main__":
    main()
