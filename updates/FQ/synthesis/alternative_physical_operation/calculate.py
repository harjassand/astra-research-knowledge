"""Reproduce conditional actuator/kinetic scales. No material performance inferred."""
from pathlib import Path
import csv
import json
import math

BASE = Path(__file__).resolve().parent
k_B = 1.380649e-23
q_e = 1.602176634e-19
eps0 = 8.8541878128e-12
d = 2.7e-12  # incoming room-temperature normalization, NOT hot measurement
shear = 1e8  # pure shear, NOT uniaxial stress
E = 1e6
h = 400e-9  # Barrett specimen film thickness; calculations are hypothetical controls
t = 600.0
C = 60e9  # declared normalization, NOT measured same-regime C44
epsilon = 13*eps0
T = 650+273.15
p_dc = 2*d*E*shear
p_ac = d*E*shear
frequency = 287.24e6  # room-temperature Rummel2023 platform
eta = 1.25e-4  # room-temperature fitted elastic loss normalization
b_ac = 2*math.pi*frequency*eta/C

table = []
for Sigma in [1e-8, 1e-5, 1e-2, 1, 100]:
    table.append({
        'conductivity_S_per_m_hypothetical': Sigma,
        'isolated_bulk_Maxwell_time_s': epsilon/Sigma,
        'DC_Joule_W_per_cm2': Sigma*E**2*h/1e4,
        'DC_Joule_J_per_cm2_600s': Sigma*E**2*h*t/1e4,
        'AC_Joule_W_per_cm2': Sigma*E**2*h/2e4,
        'AC_joint_loss_lower_bound_W_per_cm2_for_270Pa':
            p_ac*math.sqrt(Sigma*b_ac)/abs(d)*h/1e4,
    })

a0 = 0.5653e-9  # declared lattice-constant normalization
V_pair = a0**3/4
V_ten = k_B*T*math.log(10)/p_dc
step = a0/2
gamma = 28e-3*q_e/(1e-10)**2  # cold DFT normalization from Rubel family

results = {
    'status': 'CONDITIONAL_MODEL_ARITHMETIC_ONLY',
    'base_revision': '00631610750c708263d5cf6d812ebbb8edc77335',
    'normalizations': {'d_m_per_V':d, 'pure_shear_Pa':shear,
        'local_E_V_per_m':E, 'film_h_m':h, 'active_time_s':t,
        'elastic_C_Pa':C, 'relative_permittivity':13, 'temperature_K':T,
        'AC_frequency_Hz_ROOM_T':frequency,'AC_elastic_eta_ROOM_T':eta},
    'p_DC_Pa':p_dc,
    'p_AC_in_phase_Pa':p_ac,
    'p_DC_for_100MPa_uniaxial_110_Pa':p_dc/2,
    'electric_stored_J_per_cm2':epsilon*E**2*h/2e4,
    'elastic_shear_stored_J_per_cm2':shear**2*h/(2*C*1e4),
    'AC_local_mechanical_loss_W_per_cm2_normalization':b_ac*shear**2*h/2e4,
    'AC_local_mechanical_loss_J_per_cm2_600s_normalization':b_ac*shear**2*h*t/2e4,
    'Ohmic_conductivity_ceiling_for_1W_per_cm2_DC_S_per_m':1e4/(E**2*h),
    'atomic_pair_volume_m3_normalization':V_pair,
    'atomic_pair_event_odds_multiplier_at_540Pa':math.exp(p_dc*V_pair/(k_B*T)),
    'tenfold_event_odds_swept_step_volume_m3':V_ten,
    'tenfold_event_odds_patch_width_m_for_half_lattice_step':math.sqrt(V_ten/step),
    '1um3_domain_energy_split_eV_at_540Pa':p_dc*1e-18/q_e,
    'cold_DFT_gamma_J_per_m2_normalization':gamma,
    'cylindrical_curvature_pressure_Pa_for_R_1um_normalization':gamma/1e-6,
    'curve_pressure_over_DC_p_normalization':gamma/(1e-6*p_dc),
    'conditional_3p8eV_Arrhenius_rate_ratio_177C_to_650C':
        math.exp(-3.8*q_e/k_B*(1/(177+273.15)-1/T)),
    'overlap_ceiling_DC_Pa':{str(f):p_dc*f for f in [1,0.1,0.01]},
    'conductivity_table':table,
    'warning':'No conductivity, hot d, hot C/loss, directional wall mobility, pinning, damage threshold, or retained yield acquired. Cold normalizations are not combined into a claimed hot implementation.'
}

# Algebraic/model checks that can catch a sign/factor or bound error.
assert math.isclose(p_dc, 540)
assert math.isclose(p_ac, 270)
for a,b in [(1.0,2.0),(1e-8,b_ac),(100,b_ac)]:
    P = p_ac/abs(d)
    Ef = math.sqrt(P*math.sqrt(b/a))
    sf = math.sqrt(P*math.sqrt(a/b))
    q = (a*Ef**2+b*sf**2)/2
    assert math.isclose(Ef*sf,P,rel_tol=1e-12)
    assert math.isclose(q,P*math.sqrt(a*b),rel_tol=1e-12)

(BASE/'calculations.json').write_text(json.dumps(results,indent=2)+'\n')
with (BASE/'conductivity_thresholds.csv').open('w', newline='') as f:
    w=csv.DictWriter(f,fieldnames=table[0].keys())
    w.writeheader(); w.writerows(table)
print(json.dumps({k:v for k,v in results.items() if k not in
    ['normalizations','conductivity_table','warning']},indent=2))
