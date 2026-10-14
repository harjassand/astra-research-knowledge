"""Reproduce illustrative S04 arithmetic; constants are assumptions, not measurements."""

from math import log, pi, sqrt

V0 = 1.0             # V, assumed test drive
V_threshold = 0.2    # V, assumed effective growth threshold
I_max = 100e-6       # A, assumed safe forming limit
length = 100e-9      # m, hypothetical gap length
width = 100e-9       # m, hypothetical desired square bridge width
rho_e = 1.68e-8      # ohm m, bulk Cu; inappropriate at atomic scale
rho_mass = 8960.0    # kg/m3, Cu
molar_mass = 0.063546  # kg/mol, Cu
F = 96485.33212      # C/mol

R_series = V0 / I_max
R_stop = V_threshold * R_series / (V0 - V_threshold)
A_equivalent = rho_e * length / R_stop
r_equivalent = sqrt(A_equivalent / pi)
A_target = width**2
R_target = rho_e * length / A_target
I_threshold_target = V_threshold / R_target
R_series_target = R_target * (V0 / V_threshold - 1)
Q_target = 2 * F * rho_mass * length * A_target / molar_mass
p_false_max = 1 - 0.9 ** (1 / 1_000_000)
p_repair_min = 0.9 ** (1 / 10)
N_zero_false_95 = log(0.05) / log(1 - p_false_max)

for label, value in (
    ("R_series_min_ohm", R_series),
    ("R_stop_min_ohm", R_stop),
    ("bulk_cylinder_equivalent_radius_nm", r_equivalent * 1e9),
    ("bulk_R_target_ohm", R_target),
    ("current_at_0.2V_target_A", I_threshold_target),
    ("R_series_for_target_ohm", R_series_target),
    ("ideal_Cu_charge_C", Q_target),
    ("p_false_max", p_false_max),
    ("p_repair_min", p_repair_min),
    ("zero_failure_trials_95pct", N_zero_false_95),
):
    print(f"{label}: {value:.9g}")
