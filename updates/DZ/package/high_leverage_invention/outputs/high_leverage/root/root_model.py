"""Conditional calculations; no physical simulation or feasibility claim.

Run beside this file. Standard library only; writes root_model_results.json.
The geometric-control entries are rigorous analytic upper bounds evaluated
in floating arithmetic, not computed physical leakage rates.
"""
import json
import math
from pathlib import Path

KB = 1.380649e-23
E_CHARGE = 1.602176634e-19
NA = 6.02214076e23
R_GAS = 8.31446261815324
M_FE = 0.055845


def control_bound(a, t):
    epsilon = math.pi ** (t + 1) / math.factorial(t + 1)
    delta = 1 / (2 * (t + 1) ** 2)
    omega_over_kappa = a / (math.pi * math.sqrt(2) * (t + 1) * (t + 2))
    bound = min(1.0, 4 * epsilon**2 + 1 / (1 + omega_over_kappa**2))
    return dict(a=a, t=t, delta=delta, peak_over_rms=1 / math.sqrt(delta),
                omega_over_kappa_lower=omega_over_kappa,
                ideal_rate_ratio_upper=bound,
                static_isotropic_rate_ratio=math.atan(a) / a,
                bandwidth_over_kappa_sufficient=a * omega_over_kappa)


def main():
    control = []
    for a in [10, 100, 1000, 10000, 100000, 1000000, 10000000]:
        rows = [control_bound(a, t) for t in range(3, 32)]
        control.append(min(rows, key=lambda row: row['ideal_rate_ratio_upper']))

    temp, radius, length = 1163.0, 30e-9, 30e-9
    open_fraction, thickness = 0.2, 3e-9
    atoms_surface, conductivity, effective_charge = 2.5e19, 1e6, 10.0
    ds = 10 * math.exp(-228000 / (R_GAS * temp))
    conducting_fraction = open_fraction * ((1 + thickness / radius)**2 - 1)
    surface_per_area = 2 * open_fraction / radius
    mass_flux = 10 / 3600  # kg / m^2 / s
    atom_flux = mass_flux * NA / M_FE
    field = atom_flux * KB * temp / (surface_per_area * ds * atoms_surface * effective_charge * E_CHARGE)
    current = conductivity * conducting_fraction * field
    voltage = field * length
    power = current * voltage
    contact_allowance = (0.6 * 3.6e6 * mass_flux - power) / current**2
    iron = dict(
        assumptions=dict(T_K=temp, radius_m=radius, length_m=length,
                         open_fraction=open_fraction, shell_thickness_m=thickness,
                         surface_density_atoms_m2=atoms_surface,
                         conductivity_S_m=conductivity, effective_charge=effective_charge),
        source_law='Ds=10 exp[-228000/(RT)] m2/s; clean alpha-Fe, dry H2; not ore/CNT measurement',
        Ds_m2_s=ds, conducting_fraction=conducting_fraction,
        target_kg_m2_h=10, field_V_m=field, active_voltage_V=voltage,
        current_A_m2=current, local_power_W_m2=power,
        local_electricity_MWh_t=power / mass_flux / 3.6e6,
        mass_per_charge_kg_C=mass_flux / current,
        charge_per_kg_C=current / mass_flux,
        FeIII_stoichiometric_charge_C_kg=3 * E_CHARGE * NA / M_FE,
        max_extra_contact_RA_ohm_m2_for_total_0p6_MWh_t=contact_allowance,
        Onsager_coupling_squared_if_same_reciprocal_bulk_model=(
            ds * atoms_surface / (thickness * KB * temp) *
            (effective_charge * E_CHARGE)**2 / conductivity),
    )
    architecture = []
    # Every serial interconnect spans the stated distance, all have the same
    # conductivity, and extra heat is <= eta times the ideal active-layer heat.
    for h in [10e-6, 30e-6, 100e-6, 200e-6]:
        for sigma_wire in [1e6, 1e7]:
            eta = 0.1
            volume_per_area = current * h*h / (sigma_wire * eta * voltage)
            architecture.append(dict(
                minimum_span_m=h, conductor_sigma_S_m=sigma_wire,
                allowed_extra_power_fraction=eta,
                minimum_conductor_volume_m3_per_m2=volume_per_area,
            ))
    # Exact covariance integral checked against its short- and long-time limits.
    ou = []
    for x in [1e-4, .01, .1, 1, 10, 100]:
        value = x + math.expm1(-x)
        assert value > 0
        ou.append(dict(s_over_tau=x, minus_log_C_over_sigma2tau2=value))
    result = dict(
        status='conditional arithmetic and analytic bound evaluation only; no experiment or device simulation',
        geometric_control=control, iron_export=iron,
        serial_interconnect_volume_lower_bounds=architecture,
        OU_phase_correlation=ou,
        flat_band_white_noise_D_over_W_for_tenfold=1 / math.tan(math.pi / 20),
    )
    Path(__file__).with_name('root_model_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status=result['status'], control_cases=len(control),
                          iron_local_MWh_t=iron['local_electricity_MWh_t'],
                          current_MA_m2=current/1e6, architecture_cases=len(architecture)), indent=2))


if __name__ == '__main__':
    main()
