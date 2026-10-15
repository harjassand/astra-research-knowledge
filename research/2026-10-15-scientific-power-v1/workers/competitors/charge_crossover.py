#!/usr/bin/env python3
"""Illustrative lithium charge/volume crossover for a slab conductance bound.

This is a parameterized scale check, not a measurement or candidate validation.
It assumes every coulomb counted as Q becomes metallic lithium and uses the
bulk 20 C resistivity reported by NIST. Change d_m, sigma_S_m, and target_R_ohm
to match a real interface before using the result.
"""

F_C_PER_MOL = 96485.33212
M_KG_PER_MOL = 6.94e-3
RHO_KG_PER_M3 = 534.0
SIGMA_LI_S_PER_M = 1.0 / (9.28e-8)  # NIST rho_e = 9.28e-8 ohm m at 293 K
D_M = 24e-6  # two 12 um separator layers in the 2014 third-terminal study
CELL_V = 4.0  # illustrative LIB voltage, not the Li/Li symmetric test voltage
J_A_PER_CM2 = 4e-3
AREA_CM2 = 1.0


def charge_to_rule_out(target_R_ohm: float, d_m: float, sigma_S_m: float):
    """Qcrit in C/Ah and Vcrit in m^3 for G < 1/R under G <= sigma*V/d^2."""
    gcrit_S = 1.0 / target_R_ohm
    vcrit_m3 = gcrit_S * d_m**2 / sigma_S_m
    qcrit_C = vcrit_m3 * F_C_PER_MOL * RHO_KG_PER_M3 / M_KG_PER_MOL
    qcrit_Ah = qcrit_C / 3600.0
    return gcrit_S, vcrit_m3, qcrit_C, qcrit_Ah


if __name__ == "__main__":
    current_A = J_A_PER_CM2 * AREA_CM2
    gross_alarm_mAh_cm2 = 4.0 * 3.5
    gross_control_short_mAh_cm2 = 4.0 * 6.5
    sputter_setpoint_energy_J = 150.0 * 5.0 * 60.0
    print(f"Li bulk sigma at 293 K: {SIGMA_LI_S_PER_M:.6g} S/m")
    print(f"illustrative slab gap: {D_M * 1e6:.3g} um; cell voltage: {CELL_V:.3g} V")
    print(f"nominal sputter setpoint energy: {sputter_setpoint_energy_J:.6g} J (not facility energy)")
    print(f"third-terminal alert gross throughput: {gross_alarm_mAh_cm2:.6g} mAh/cm^2")
    print(f"conventional control short gross throughput: {gross_control_short_mAh_cm2:.6g} mAh/cm^2")
    for target_R in (200.0, 1.0):
        g, v, q_c, q_ah = charge_to_rule_out(target_R, D_M, SIGMA_LI_S_PER_M)
        time_s = q_c / current_A
        i_short_A = CELL_V / target_R
        p_short_W = CELL_V**2 / target_R
        print(
            f"Rcrit={target_R:g} ohm: Gcrit={g:.6g} S, "
            f"Vmetal_crit={v:.6g} m^3, Qcrit={q_c:.6g} C "
            f"= {q_ah * 1e12:.6g} pAh; "
            f"at 4 mA/cm^2 over 1 cm^2, Qcrit/current={time_s:.6g} s; "
            f"at 4 V, Ishort={i_short_A:.6g} A, Pshort={p_short_W:.6g} W"
        )
