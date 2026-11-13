"""ROOT-owned introduced physical-operation models, 13 November 2026.
No producer code, measured material fit, apparatus, physical validation or
universal lower bound. All numeric parameters are introduced.
"""
import json, math, pathlib

def joint_temperature(h, ambient, heat_capacity, melt_temperature, latent):
    hs = heat_capacity * (melt_temperature - ambient)
    if h <= hs:
        return ambient + h / heat_capacity, 0.
    if h <= hs + latent:
        return melt_temperature, (h - hs) / latent
    return melt_temperature + (h - hs - latent) / heat_capacity, 1.

def thermal_rework(resistance, bridge_fraction=1., step=1e-5):
    # Assumed diffusive metallic conduction:
    # Q_e = n * L/(2R) * (T_hot_K**2 - T_cold_K**2).
    # This is a declared Lorenz-law model, not a law for every real contact.
    ambient, melt, neighbor_limit = 25., 140., 80.
    cj, cn, latent = 4e-5, 4e-5, 2e-3
    gj, gn, power, lorenz, contacts = 2e-4, 2e-4, .2, 2.44e-8, 4
    threshold = cj * (melt - ambient) + .95 * latent
    state = [0., ambient, 0., 0.]
    peak_j, peak_n, release_time, release_n = ambient, ambient, None, None
    initial_g = contacts * lorenz * (ambient + 273.15) / resistance
    time, active = 0., True

    def derivative(y, on):
        h, tn, ein, eout = y
        tj, _ = joint_temperature(h, ambient, cj, melt, latent)
        heat = contacts * lorenz * bridge_fraction / (2 * resistance) * (
            (tj + 273.15)**2 - (tn + 273.15)**2)
        pj, pn = gj * (tj - ambient), gn * (tn - ambient)
        pin = power if on else 0.
        return [pin - pj - heat, (heat - pn) / cn, pin, pj + pn]

    while time < 3.:
        if active and state[0] >= threshold:
            release_time, release_n, active = time, state[1], False
        if active and time >= 1.:
            active = False
        dt = min(step, 3. - time)
        k1 = derivative(state, active)
        k2 = derivative([a + .5*dt*b for a,b in zip(state,k1)], active)
        k3 = derivative([a + .5*dt*b for a,b in zip(state,k2)], active)
        k4 = derivative([a + dt*b for a,b in zip(state,k3)], active)
        state = [a + dt*(b+2*c+2*d+e)/6 for a,b,c,d,e in zip(state,k1,k2,k3,k4)]
        time += dt
        tj, _ = joint_temperature(state[0], ambient, cj, melt, latent)
        peak_j, peak_n = max(peak_j,tj), max(peak_n,state[1])
    residual = state[2] - state[3] - state[0] - cn*(state[1]-ambient)
    assert abs(residual) < 1e-9, residual
    return {
        "contact_resistance_ohm":resistance, "contacts":contacts,
        "bridge_conduction_fraction_during_rework":bridge_fraction,
        "ambient_thermal_conductance_before_isolation_W_K":initial_g,
        "drop_per_contact_at_introduced_0_1A_V":.1*resistance,
        "power_per_contact_at_0_1A_W":.01*resistance,
        "reached_95percent_melt":release_time is not None,
        "release_time_s":release_time, "neighbor_at_release_C":release_n,
        "whole_trajectory_neighbor_peak_C":peak_n,
        "introduced_neighbor_limit_C":neighbor_limit,
        "neighbor_within_introduced_limit":peak_n<=neighbor_limit,
        "joint_peak_C":peak_j, "input_energy_J":state[2],
        "energy_balance_residual_J":residual,
        "step_s":step,
        "limits":"thermal law, constant R, heat capacity, latent heat, ambient paths and release criterion are introduced; no stress, actual contact, oxide, selectivity or lifetime qualification",
    }

def repair_throat():
    # Best-case constant pressure, no extra downstream cavity resistance.
    width, length, h0, dp, viscosity, deposition = .002, .010, 20e-6, 20e3, .5, .2e-6
    cavity = .4e-9  # .4 microlitre
    prefactor = width*dp/(12*viscosity*length)
    initial_q = prefactor*h0**3
    close_time = h0/(2*deposition)
    delivered = prefactor*h0**4/(8*deposition)
    protected_fill_time = cavity/initial_q
    # Midpoint quadrature independently checks the integrated h(t)^3 flow.
    n=20000;dt=close_time/n
    numeric=sum(prefactor*max(0,h0-2*deposition*((i+.5)*dt))**3*dt for i in range(n))
    assert abs(numeric/delivered-1) < 2e-9
    events, deposit_per_event = 20, .1e-6
    remaining = max(0,h0-2*events*deposit_per_event)
    return {
        "width_m":width,"feed_length_m":length,"initial_aperture_m":h0,
        "pressure_Pa":dp,"viscosity_Pa_s":viscosity,
        "introduced_inward_cure_front_speed_each_wall_m_s":deposition,
        "damage_cavity_volume_uL":cavity*1e9,
        "initial_flow_nL_s":initial_q*1e12,"throat_closure_time_s":close_time,
        "optimistic_total_delivery_uL":delivered*1e9,
        "fraction_cavity_filled_before_feed_closure":delivered/cavity,
        "protected_uncured_feed_fill_time_s":protected_fill_time,
        "after_20_events_at_0_1um_deposit_each_wall_flow_fraction":(remaining/h0)**3,
        "max_deposit_each_wall_per_event_m_for_90percent_flow_after20":
            h0/(2*events)*(1-.9**(1/3)),
        "limits":"an upstream sealed throat can stop leakage before the downstream damage is filled. Separating delivery from cure would require real access, triggering, mixing, removal and closure, not an assigned reset.",
    }

def pressure_body():
    # Undeformed, homogeneous, isotropic thick cylinder with pressure p.
    # Inner hoop stress p*(b^2+a^2)/(b^2-a^2); not a hyperelastic actuator law.
    force, pressure, healed_strength, proof_factor = 20., 100e3, .34e6, 1.5
    a=math.sqrt(force/(math.pi*pressure))
    allowable=healed_strength/proof_factor
    assert allowable>pressure
    b=a*math.sqrt((allowable+pressure)/(allowable-pressure))
    rho,length=1200.,.1
    return {
        "introduced_force_N":force,"gauge_pressure_Pa":pressure,
        "inner_radius_for_piston_force_m":a,
        "hypothetical_healed_tensile_strength_Pa":healed_strength,
        "introduced_proof_factor":proof_factor,
        "minimum_outer_radius_in_Lame_screen_m":b,
        "minimum_wall_m":b-a,
        "body_mass_kg_at_introduced_density_1200kg_m3_length_0_1m":
            math.pi*(b*b-a*a)*length*rho,
        "limits":".34MPa is used as a hypothetical number in this geometry; no source property is transferred to a pressure vessel, large-strain actuation, defect, long-life or mixed-material body.",
    }

def main():
    results={
        "scope":"introduced independent ROOT models; physical mechanisms unconstructed; no source or producer artifact recovery",
        "microjoint_rework":[thermal_rework(.01),thermal_rework(.1),thermal_rework(.01,.01)],
        "repair_delivery_and_access":repair_throat(),
        "pressure_load_path":pressure_body(),
        "scientific_limits":"a cooler isolated case does not construct opening contacts or holding/exchanging a chip; a protected feed case does not construct cure selectivity, a mold, repaired strength, renewed transport or autonomous functional recovery",
    }
    # One halved-step calculation checks the conclusion is not a coarse thermal step artifact.
    refined=thermal_rework(.01,step=5e-6)
    assert abs(refined["whole_trajectory_neighbor_peak_C"]-results["microjoint_rework"][0]["whole_trajectory_neighbor_peak_C"]) < .02
    results["numerical_check"]={
        "coarse_fine_peak_difference_C":refined["whole_trajectory_neighbor_peak_C"]-results["microjoint_rework"][0]["whole_trajectory_neighbor_peak_C"],
        "energy_conservation_checked":True,"analytic_throat_integral_checked":True,
    }
    out=pathlib.Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(results,indent=2,ensure_ascii=True)+"\n")
    print(json.dumps(results,indent=2))

if __name__=="__main__":
    main()
