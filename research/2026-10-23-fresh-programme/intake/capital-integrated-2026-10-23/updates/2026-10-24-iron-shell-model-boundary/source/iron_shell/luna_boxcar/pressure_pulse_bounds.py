#!/usr/bin/env python3
"""Reproducible ideal-gas and inventory arithmetic for the iron-shell note.

These are scale checks, not a model of a particular TGA.  All outputs are
explicitly parameterized; in particular the suspended displacement volume,
hot volume, actual pressure ramp, and ore conversion rate must be measured.
"""

from math import isclose

R = 8.31446261815324  # J mol^-1 K^-1
M_H2 = 2.01588e-3     # kg mol^-1
M_H2O = 18.01528e-3   # kg mol^-1
M_FE2O3 = 159.687e-3  # kg mol^-1
M_FE = 55.845e-3      # kg mol^-1
M_O = 15.999e-3       # kg mol^-1
T_HOT = 1073.15        # K, illustrative 800 C
P_BASE = 100_000.0     # Pa
HOT_VOLUME = 100e-6    # m^3, illustrative 100 mL hot volume
MOLAR_VOLUME_STP = 22.414e-3  # m^3 mol^-1, illustrative 0 C / 1 atm


def mixture_molar_mass(x_h2o: float) -> float:
    return (1.0 - x_h2o) * M_H2 + x_h2o * M_H2O


def ideal_density(pressure_pa: float, temperature_k: float, x_h2o: float) -> float:
    return pressure_pa * mixture_molar_mass(x_h2o) / (R * temperature_k)


def sccm_to_mol_s(flow_sccm: float) -> float:
    return (flow_sccm * 1e-6 / 60.0) / MOLAR_VOLUME_STP


def pressure_step_min_s(volume_m3: float, delta_p_pa: float,
                        temperature_k: float, flow_sccm: float) -> float:
    """Ideal cell inventory / feed lower bound; excludes regulator and lines."""
    delta_n = volume_m3 * delta_p_pa / (R * temperature_k)
    return delta_n / sccm_to_mol_s(flow_sccm)


def mean_residence_s(volume_m3: float, pressure_pa: float,
                     temperature_k: float, flow_sccm: float) -> float:
    n_gas = pressure_pa * volume_m3 / (R * temperature_k)
    return n_gas / sccm_to_mol_s(flow_sccm)


def leak_pressure_drift_pa_s(volume_m3: float, temperature_k: float,
                             leak_sccm: float) -> float:
    """Unregulated isothermal pressure drift for a standard leak throughput."""
    return R * temperature_k / volume_m3 * sccm_to_mol_s(leak_sccm)


def leak_pressure_time_constant_s(volume_m3: float, pressure_pa: float,
                                  temperature_k: float, leak_sccm: float) -> float:
    """Inventory / leak-throughput time; leak is assumed constant in mol/s."""
    n_gas = pressure_pa * volume_m3 / (R * temperature_k)
    return n_gas / sccm_to_mol_s(leak_sccm)


def outlet_ratio_from_h2_depletion(inlet_ratio: float, h2_depletion: float) -> float:
    """For H2 + H2O/FeO reaction, chi = reacted H2 / inlet H2 molar flow."""
    return (inlet_ratio + h2_depletion) / (1.0 - h2_depletion)


def main() -> None:
    x_water = 0.10  # 10 mol% steam, so inlet H2O/H2 = 1/9
    ratio_in = x_water / (1.0 - x_water)
    rho_1bar = ideal_density(P_BASE, T_HOT, x_water)
    rho_2bar = ideal_density(2 * P_BASE, T_HOT, x_water)
    rho_10bar = ideal_density(10 * P_BASE, T_HOT, x_water)
    rho_50_50 = ideal_density(P_BASE, T_HOT, 0.50)

    print(f"T={T_HOT:.2f} K; x_H2O={x_water:.2f}; inlet H2O/H2={ratio_in:.6f}")
    print(f"mixture molar mass={mixture_molar_mass(x_water)*1e3:.6f} g/mol")
    print(f"rho(1 bar)={rho_1bar:.8f} kg/m^3")
    for pbar, rho in ((2, rho_2bar), (10, rho_10bar)):
        delta_ug_per_cm3 = (rho - rho_1bar) * 1e-6 * 1e9
        print(f"1->{pbar} bar buoyancy step={delta_ug_per_cm3:.3f} ug per cm^3 displaced")
    print(f"1 bar, 50:50 H2/H2O buoyancy scale={rho_50_50*1e-6*1e9:.3f} ug/cm^3")
    print(f"1 K temperature error at 1 bar={rho_1bar/T_HOT*1e-6*1e9:.4f} ug/cm^3/K")

    for flow in (10, 100, 200, 500):
        step = pressure_step_min_s(HOT_VOLUME, P_BASE, T_HOT, flow)
        tau = mean_residence_s(HOT_VOLUME, P_BASE, T_HOT, flow)
        tau_10bar = mean_residence_s(HOT_VOLUME, 10 * P_BASE, T_HOT, flow)
        print(f"flow={flow:3d} sccm: 1-bar inventory/step lower-bound={step:.2f} s; "
              f"tau@1bar={tau:.2f} s; tau@10bar={tau_10bar:.2f} s")

    leak = 1.0
    drift = leak_pressure_drift_pa_s(HOT_VOLUME, T_HOT, leak)
    tau_leak = leak_pressure_time_constant_s(HOT_VOLUME, P_BASE, T_HOT, leak)
    print(f"unregulated {leak:g} sccm leak: pressure drift={drift:.1f} Pa/s; "
          f"1-bar inventory/leak time={tau_leak/60:.1f} min")

    ratio_out = outlet_ratio_from_h2_depletion(ratio_in, 0.01)
    print(f"1% instantaneous H2 depletion: outlet ratio={ratio_out:.6f}; "
          f"relative ratio shift={(ratio_out/ratio_in-1)*100:.2f}%")

    # Ideal-gas scale for the 2--3.5 g pellets and 200--500 mL/min NTP flow
    # reported in the manufacturer application note.  The conversion is a
    # hypothetical complete Fe2O3 -> Fe balance over 120 min, not a claim that
    # each run had this exact loading/flow pairing.
    for sample_g in (2.0, 3.5):
        n_h2 = (sample_g / 1000.0) / M_FE2O3 * 3.0
        loss_g = n_h2 * M_O * 1000.0
        print(f"{sample_g:.1f} g Fe2O3 full-reduction stoich: H2={n_h2*1000:.3f} mmol; "
              f"oxygen loss={loss_g:.3f} g")
        for flow in (200, 500):
            n_feed_120 = sccm_to_mol_s(flow) * 120 * 60
            h2_used_fraction = n_h2 / n_feed_120
            outlet_r_pure_h2_average = n_h2 / (n_feed_120 - n_h2)
            print(f"  {flow} sccm for 120 min: H2 feed={n_feed_120:.3f} mol; "
                  f"integrated H2 use={100*h2_used_fraction:.2f}%; "
                  f"cumulative generated-H2O / residual-H2={outlet_r_pure_h2_average:.4f}")

    print(f"Fe -> FeO oxygen uptake per g Fe={M_O/M_FE:.6f} g O/g Fe "
          f"({100*M_O/M_FE:.2f}% mass gain relative to Fe)")
    print(f"FeO -> Fe oxygen removal per g FeO={M_O/(M_FE+M_O):.6f} g O/g FeO "
          f"({100*M_O/(M_FE+M_O):.2f}% mass loss relative to FeO)")

    # Separate fixed-total-pressure composition pulse: 10 -> 30 mol% steam.
    # Heat-capacity values are deliberately illustrative path-averaged values,
    # not a property-table claim or an instrument prediction.
    x_water_0, x_water_1 = 0.10, 0.30
    delta_molar_mass = mixture_molar_mass(x_water_1) - mixture_molar_mass(x_water_0)
    delta_rho = P_BASE * delta_molar_mass / (R * T_HOT)
    delta_buoy_ug_cm3 = delta_rho * 1e-6 * 1e9
    pellet_g, fe_mass_fraction, metallic_fraction, oxidized_fraction = 3.5, 0.678, 1.0, 0.001
    added_oxygen_g = (pellet_g * fe_mass_fraction * metallic_fraction *
                      oxidized_fraction * M_O / M_FE)
    cp_h2_mean, cp_h2o_mean = 29.0, 36.0  # J mol^-1 K^-1, illustrative path averages
    delta_cp_mixture = (x_water_1 - x_water_0) * (cp_h2o_mean - cp_h2_mean)
    delta_t_feed = T_HOT - 298.15
    print(f"fixed-P 10->30 mol% H2O: delta molar mass={delta_molar_mass*1e3:.4f} g/mol; "
          f"apparent mass step={-delta_buoy_ug_cm3:.2f} ug/cm^3 displaced at 1 bar")
    print(f"same composition step at 10 bar: apparent mass step={-10*delta_buoy_ug_cm3:.2f} ug/cm^3")
    print(f"3.5 g pellet, 67.8 wt% Fe, all Fe metallic, 0.1% oxidized: "
          f"ideal added O={added_oxygen_g*1e6:.1f} ug; "
          f"1 cm^3 buoyancy step is {100*delta_buoy_ug_cm3/(added_oxygen_g*1e6):.2f}% of it")
    print(f"at fixed total standard flow, illustrative composition-induced feed heat-load "
          f"change={delta_cp_mixture:.2f} J/mol/K; "
          f"{delta_cp_mixture*delta_t_feed*sccm_to_mol_s(200):.3f} W at 200 sccm and "
          f"{delta_cp_mixture*delta_t_feed*sccm_to_mol_s(500):.3f} W at 500 sccm")

    # Guard the core arithmetic against accidental edits.
    assert isclose(rho_2bar, 2 * rho_1bar, rel_tol=1e-12)
    assert isclose(rho_10bar, 10 * rho_1bar, rel_tol=1e-12)
    assert isclose(outlet_ratio_from_h2_depletion(1.0, 0.01), 1.01 / 0.99)
    assert isclose(100 * M_O / M_FE, 28.6476, rel_tol=2e-4)
    assert isclose(delta_molar_mass * 1e3, 3.19988, rel_tol=1e-6)


if __name__ == "__main__":
    main()
