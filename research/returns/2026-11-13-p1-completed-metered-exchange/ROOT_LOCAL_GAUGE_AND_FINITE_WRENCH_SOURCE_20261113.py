"""ROOT introduced local-gauge and finite force-source models, 13 November 2026.
No material, cylinder, sensor, machine or actual service is qualified by these calculations.
Python standard library only; no producer artifact imported or executed.
"""
import itertools
import json
import math
from pathlib import Path

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]

def transpose(a):
    return [list(x) for x in zip(*a)]

def mul(a, b):
    return [[dot(row, col) for col in transpose(b)] for row in a]

def mv(a, x):
    return [dot(row, x) for row in a]

def inverse(a):
    n = len(a)
    t = [list(row) + [float(i == j) for j in range(n)] for i, row in enumerate(a)]
    for i in range(n):
        p = max(range(i, n), key=lambda j: abs(t[j][i]))
        if abs(t[p][i]) < 1e-14:
            raise ValueError("Singular")
        t[i], t[p] = t[p], t[i]
        pivot = t[i][i]
        t[i] = [x/pivot for x in t[i]]
        for j in range(n):
            if j != i:
                q = t[j][i]
                t[j] = [x-q*y for x, y in zip(t[j], t[i])]
    return [row[n:] for row in t]

def norm(x):
    return math.sqrt(dot(x, x))

def eigen_symmetric(a):
    a = [list(row) for row in a]
    n = len(a)
    for _ in range(1000):
        i, j = max(((i, j) for i in range(n) for j in range(i+1, n)),
                   key=lambda ij: abs(a[ij[0]][ij[1]]))
        if abs(a[i][j]) < 1e-10:
            break
        phi = 0.5*math.atan2(2*a[i][j], a[j][j]-a[i][i])
        c, s = math.cos(phi), math.sin(phi)
        ai, aj, aij = a[i][i], a[j][j], a[i][j]
        for k in range(n):
            if k != i and k != j:
                aki, akj = a[k][i], a[k][j]
                a[k][i] = a[i][k] = c*aki-s*akj
                a[k][j] = a[j][k] = s*aki+c*akj
        a[i][i] = c*c*ai-2*c*s*aij+s*s*aj
        a[j][j] = s*s*ai+2*c*s*aij+c*c*aj
        a[i][j] = a[j][i] = 0.0
    return sorted(a[i][i] for i in range(n))

positions = [[.55,.15,-.20],[.55,-.15,-.20],[.15,0,-.26],
             [.15,.26,0],[.55,.26,0],[.80,0,.09]]
directions = [[0,0,1],[0,0,1],[0,0,1],[0,1,0],[0,1,0],[1,0,0]]
J = [n+cross(r,n) for r,n in zip(positions,directions)]
W = transpose(J)
Winv = inverse(W)
identity_residual = max(abs(v-float(i==j)) for i,row in enumerate(mul(W,Winv))
                        for j,v in enumerate(row))
assert identity_residual < 1e-12
member_bounds = [1000*norm(row[:3])+250*norm(row[3:]) for row in Winv]
L = .3
Jn = [row[:3]+[x/L for x in row[3:]] for row in J]
G = mul(transpose(Jn), Jn)
eigsG = eigen_symmetric(G)
assert min(eigsG) > 0 and abs(sum(eigsG)-sum(G[i][i] for i in range(6))) < 1e-8

# A simultaneous opposed gauge pair can reference actual pad lands while the old
# joint still retains the workpiece. The datum moves if their probe forces differ.
# This is a declared normalized diagonal old-joint stiffness, not the P1 CAD matrix.
gauge_cases = []
for Kold in [1e6, 5e6]:
    for head_force_error in [.1, .5, 1.0]:
        eps = 2*head_force_error
        maxima = [0.0]*6
        max_pose = [0.0]*6
        for signs in itertools.product([-1,1], repeat=6):
            p = [eps*s for s in signs]
            q = [x/Kold for x in mv(transpose(Jn),p)]
            contact_motion = mv(Jn,q)
            maxima = [max(a,abs(b)) for a,b in zip(maxima,contact_motion)]
            max_pose = [max(a,abs(b)) for a,b in zip(max_pose,q)]
        gauge_cases.append({"Kold_normalized_N_per_m":Kold,
            "each_head_probe_error_N":head_force_error,
            "paired_residual_max_N":eps,
            "pad_datum_relaxation_max_um":[x*1e6 for x in maxima],
            "pose_component_max_um":[x*1e6 for x in max_pose]})
# Introduced sufficient land coverage and setting budgets. A three-point plane
# does not constrain arbitrary roughness between the points; that is explicit.
selected = gauge_cases[0]
fixed_budget_um = {"gauge_certificate":2.0, "unseen_land_figure":5.0,
                   "positive_lock_shift":5.0, "thermal_change":3.0,
                   "local_elastic_recovery_at_1N_1MNm":1.0,
                   "tilt_over_entire_land":3.0, "wear_contamination":2.0}
total_gauge_budget = sum(fixed_budget_um.values())+max(selected["pad_datum_relaxation_max_um"])
gauge_gap_um = [60-total_gauge_budget,60+total_gauge_budget]
gauge_trip_example = {"declared_gap_um":60,"fixed_error_terms_um":fixed_budget_um,
    "worst_opposed_probe_datum_shift_um":max(selected["pad_datum_relaxation_max_um"]),
    "conditional_gap_interval_um":gauge_gap_um,
    "actual_installed_result":"UNQUALIFIED",
    "global_target_correction":"Not used in this different local comparison operation",
    "unconstructed_operations":["access and withdrawal of every gauge",
        "low-force simultaneous opposing probing","actual local and old-joint compliance",
        "positive lock shift","full pad figure, tilt, temperature and contamination",
        "sensors and interlocks","capture dynamics under the resulting intervals"]}

# Twelve tensile force ports, paired at each of six lines.
# Sums of opposing tensions cancel in ideal equilibrium but add inertia, geometric
# stiffness and local stresses. No free low-stiffness load source is supplied.
g = 9.80665
T0, A, pa, gamma, T_kelvin = 1500.0,.004,1e5,1.4,293.15
p_abs = pa+T0/A
mass_pair = 2*T0/g
Mnorm = [[mass_pair*x for x in row] for row in G]
mass_eigs = eigen_symmetric(Mnorm)
chambers = []
for V in [.002,.020]:
    kgas = gamma*A*A*(2*p_abs)/V
    Kgas = [[kgas*x for x in row] for row in G]
    eigs = eigen_symmetric(Kgas)
    # Exact scalar displacement of +/-1mm about each of that line's worst
    # coherent load. Both initial chambers have volume V in this introduced model.
    nonlinear=[]
    for bound in member_bounds:
        tp, tm = T0+bound/2,T0-bound/2
        pp, pm = pa+tp/A,pa+tm/A
        forces=[]
        for x in [-.001,0,.001]:
            fp = A*(pp*(V/(V+A*x))**gamma-pa)
            fm = A*(pm*(V/(V-A*x))**gamma-pa)
            forces.append({"x_m":x,"net_N":fp-fm,
                           "error_from_command_N":fp-fm-bound})
        nonlinear.append({"command_N":bound,"tensions_N":[tp,tm],"displacement":forces})
    # Reversible isothermal maximum work relative to ambient for the initial,
    # balanced chamber state. Not a real vessel rating or full pneumatic energy.
    initial_exergy = 12*V*(p_abs*math.log(p_abs/pa)-p_abs+pa)
    chambers.append({"each_chamber_volume_L":V*1000,"total_12_chamber_volume_L":12*V*1000,
        "pair_scalar_tangent_stiffness_N_per_m":kgas,
        "normalized_eigen_stiffness_N_per_m":eigs,
        "source_to_1MNm_declared_frame_spectral_ratio":max(eigs)/1e6,
        "source_to_5MNm_declared_frame_spectral_ratio":max(eigs)/5e6,
        "balanced_initial_ideal_isothermal_exergy_J":initial_exergy,
        "one_mm_exact_gas_law_cases":nonlinear})

source_errors=[]
for eps in [.5,1,5]:
    maxF=maxM=0
    for signs in itertools.product([-1,1], repeat=6):
        dw=mv(W,[2*eps*s for s in signs])
        maxF=max(maxF,norm(dw[:3]))
        maxM=max(maxM,norm(dw[3:]))
    source_errors.append({"each_port_force_error_N":eps,
                         "max_force_norm_error_N":maxF,"max_moment_norm_error_Nm":maxM})
# A common 1K chamber temperature drift changes each opposing preload equally:
# it ideally cancels, but differential +/-1K errors do not.
temperature_pair_error=2*A*p_abs/T_kelvin
# Direct cable geometry adds transverse restoring forces ~2T0 / distance per pair.
cable_distance=1.0
geometric_scalar=2*T0/cable_distance

# A hanging mass source changes a scalar machine mode to
# (m_machine + m_source)*xdd + k*x = commanded gravity force.
inertia_examples=[]
for meff in [100.0,300.0]:
    msource=mass_pair
    inertia_examples.append({"machine_mass_kg":meff,"source_pair_kg":msource,
        "initial_measured_force_fraction_of_gravity_command":meff/(meff+msource),
        "frequency_ratio_to_massless_source":math.sqrt(meff/(meff+msource))})
human={"candidate_h_year":61.93,"strong_assisted_h_year":476.4,
       "tenfold_budget_h":47.64,"missing_h":61.93-47.64,
       "listed_intervention_reset_h":15,
       "if_all_15_physically_eliminated_h":61.93-15,
       "if_all_15_physically_eliminated_factor":476.4/(61.93-15),
       "fraction_of_15_to_remove":(61.93-47.64)/15,
       "accounting_only_USD_per_exchange":(61.93-47.64)*40/5000,
       "operation_achieved":False}
output={"status":"INTRODUCED_BOUNDED_MODELS_NOT_HARDWARE",
    "coordinates":{"J_physical":J,"length_for_rotation_normalization_m":L,
                   "W_inverse_residual":identity_residual,
                   "coherent_1000N_250Nm_member_bounds_N":member_bounds,
                   "G_eigenvalues":eigsG},
    "local_gauging":{"cases":gauge_cases,"selected_conditional_budget":gauge_trip_example},
    "finite_load_source":{"T0_N":T0,"each_piston_area_m2":A,
       "piston_diameter_m":math.sqrt(4*A/math.pi),"balanced_absolute_pressure_Pa":p_abs,
       "all_hanging_mass_kg":12*T0/g,
       "normalized_hanging_mass_eigenvalues_kg":mass_eigs,
       "hanging_mass_scalar_transients":inertia_examples,
       "gas_chambers":chambers,"force_error_corners":source_errors,
       "differential_plus_minus_1K_pair_error_N":temperature_pair_error,
       "one_metre_cable_geometric_pair_stiffness_N_per_m":geometric_scalar,
       "actual_source":"NOT_CONSTRUCTED_OR_QUALIFIED",
       "omitted_not_free":["diaphragm force-area and hysteresis",
        "moving piston, bearing and cable inertia","all cable/guide geometry",
        "pressure vessel and hose proof, compliance, energy and heat",
        "friction, temperature gradients, leaks and power outage",
        "individual load-cell or pressure-area metrology",
        "anchor routes and frame backreactions","manufacture, preparation, life and cost"]},
    "human_operation_budget":human}
out=Path(__file__).with_suffix(".json")
out.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"output":str(out),"member_bounds_N":member_bounds,
 "gauge_gap_um":gauge_gap_um,"hanging_mass_kg":12*T0/g,
 "gas_cases":[{k:c[k] for k in ["each_chamber_volume_L",
 "pair_scalar_tangent_stiffness_N_per_m","normalized_eigen_stiffness_N_per_m",
 "balanced_initial_ideal_isothermal_exergy_J"]} for c in chambers],
 "source_errors":source_errors,"human":human},indent=2))

