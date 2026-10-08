"""Evaluate the conditional binary-electrolyte ionic heat-flux decomposition.

Inputs are signed molar fluxes along one axis and constant species heats of
transport. The model omits solvent advection, electrode heat and Fourier heat.
"""

from math import log

FARADAY_C_PER_MOL = 96485.33212
GAS_CONSTANT_J_PER_MOL_K = 8.31446261815324


def decompose(j_plus, j_minus, q_plus, q_minus):
    """Return current, neutral-salt flux, and two ionic heat-flux terms."""
    current = FARADAY_C_PER_MOL * (j_plus - j_minus)
    salt_flux = (j_plus + j_minus) / 2
    zero_salt_peltier = (q_plus - q_minus) / (2 * FARADAY_C_PER_MOL)
    ionic_heat_flux = q_plus * j_plus + q_minus * j_minus
    current_term = zero_salt_peltier * current
    salt_term = (q_plus + q_minus) * salt_flux
    return {
        "current_A_per_m2": current,
        "salt_flux_mol_per_m2_s": salt_flux,
        "zero_salt_peltier_V": zero_salt_peltier,
        "ionic_heat_flux_W_per_m2": ionic_heat_flux,
        "current_term_W_per_m2": current_term,
        "salt_term_W_per_m2": salt_term,
    }


def source_parameter_example():
    q_na, q_cl = 3500.0, 500.0  # J/mol, values reported by Tsutsui et al. (2025)
    current_density = 1.0  # A/m^2; ratios below do not depend on pore area
    j_na_only = current_density / FARADAY_C_PER_MOL
    j_zero_salt = current_density / (2 * FARADAY_C_PER_MOL)

    na_only = decompose(j_na_only, 0.0, q_na, q_cl)
    zero_salt = decompose(j_zero_salt, -j_zero_salt, q_na, q_cl)
    r = 1e4
    temperature_k = 293.0

    return {
        "current_density_A_per_m2": current_density,
        "na_only_heat_flux_W_per_m2": na_only["ionic_heat_flux_W_per_m2"],
        "na_only_heat_per_current_V": q_na / FARADAY_C_PER_MOL,
        "zero_salt_heat_per_current_V": zero_salt["zero_salt_peltier_V"],
        "same_current_heat_difference_per_A_W_per_A": (q_na + q_cl)
        / (2 * FARADAY_C_PER_MOL),
        "same_current_heat_difference_for_1uA_W": (q_na + q_cl)
        * 1e-6
        / (2 * FARADAY_C_PER_MOL),
        "ideal_monovalent_nernst_voltage_V": (
            GAS_CONSTANT_J_PER_MOL_K * temperature_k / FARADAY_C_PER_MOL
        )
        * log(r),
        "ideal_neutral_salt_delta_mu_J_per_mol": (
            2
            * GAS_CONSTANT_J_PER_MOL_K
            * temperature_k
            * log(r)
        ),
    }


if __name__ == "__main__":
    for key, value in source_parameter_example().items():
        print(f"{key}: {value:.12g}")
