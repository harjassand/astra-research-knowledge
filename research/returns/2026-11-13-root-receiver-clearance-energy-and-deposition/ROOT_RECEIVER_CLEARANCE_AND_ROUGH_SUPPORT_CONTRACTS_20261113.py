"""ROOT-owned introduced physical screens, not a manufactured gripper.

No producer code is executed. Source-reported quantities remain source-scoped.
The continuous-wrench certificate is conditional on introduced contact cones,
geometry, paired preload balance, engaged-tip count and load-sharing bounds.
It supplies no sensor, asperity strength, creep, body stiffness or field life.
"""
import json
import math
from pathlib import Path


def inverse3(matrix):
    a = [list(row) + [float(i == j) for j in range(3)]
         for i, row in enumerate(matrix)]
    for j in range(3):
        pivot = max(range(j, 3), key=lambda i: abs(a[i][j]))
        a[j], a[pivot] = a[pivot], a[j]
        z = a[j][j]
        if abs(z) < 1e-18:
            raise ValueError('singular normal wrench map')
        a[j] = [x / z for x in a[j]]
        for i in range(3):
            if i != j:
                z = a[i][j]
                a[i] = [x - z*y for x, y in zip(a[i], a[j])]
    return [row[3:] for row in a]


def clearance_screen(c, station_radius=0.01591, face_halfwidth=0.0245):
    """Exact diameter of linearized corner displacement over the stated polytope.

    P(c)={|ux|+a|yaw|<=c/2, |uy|+a|yaw|<=c/2}.
    A full reversal is P-P=2P. This is rigid in-plane clearance only.
    """
    vertices = [(sx*c/2, sy*c/2, 0.0) for sx in [-1, 1] for sy in [-1, 1]]
    vertices += [(0.0, 0.0, sy*c/(2*station_radius)) for sy in [-1, 1]]
    sampled_exact_vertices = []
    for ux, uy, yaw in vertices:
        for x in [-face_halfwidth, face_halfwidth]:
            for y in [-face_halfwidth, face_halfwidth]:
                sampled_exact_vertices.append(2*math.hypot(ux-y*yaw, uy+x*yaw))
    formula = math.sqrt(2)*max(1.0, face_halfwidth/station_radius)*c
    assert abs(max(sampled_exact_vertices)-formula) < 1e-15
    return {'series_diametral_clearance_m': c,
            'exact_rigid_clearance_reversal_m': formula,
            'exact_yaw_reversal_rad': c/station_radius,
            'scope': 'linearized rigid clearance only; no elasticity, rocking, normal motion or strength'}


def rough_support_screen(missing_pair=None):
    total = 12
    R = 0.032
    p0 = 120.0
    alpha, beta = 0.7, 0.5
    s_max, compression_max = 150.0, 100.0
    fn_max, ft_max, moment_max = 100.0, 250.0, 10.0
    self_fn, self_ft, self_moment = 10.0, 10.0, 0.25
    tips_min, share_ratio, tip_capacity = 30, 1.2, 8.0
    omitted = set() if missing_pair is None else {missing_pair, (missing_pair+6) % 12}
    angles = [2*math.pi*i/total for i in range(total) if i not in omitted]
    n = len(angles)
    rows = [(1.0, R*math.sin(t), -R*math.cos(t)) for t in angles]
    gram = [[sum(r[i]*r[j] for r in rows) for j in range(3)] for i in range(3)]
    inv = inverse3(gram)
    stations = []
    for theta, row in zip(angles, rows):
        coeff = [sum(row[j]*inv[j][k] for j in range(3)) for k in range(3)]
        assert abs(coeff[0] - 1/n) < 1e-12
        cm = math.hypot(coeff[1], coeff[2])
        # For the reference simplex of a tensile segment and shear/moment balls,
        # support is MAX over those three inputs, not their sum.
        cone_reference = max(fn_max/n, alpha*ft_max/n, moment_max*cm)
        cone_self = self_fn/n + alpha*self_ft/n + self_moment*cm
        cone_margin = alpha*p0 - cone_reference - cone_self
        side_margin = beta*p0 - (ft_max+self_ft)*math.sqrt(1+beta*beta)/n
        radial_min = p0 - (ft_max+self_ft)/n
        radial_max = p0 + (ft_max+self_ft)/n
        compress_need = (moment_max+self_moment)*cm + self_fn/n
        # Triangle bound on vector force, conservative for this affine map.
        force_increment = max(fn_max/n, ft_max/n, moment_max*cm)
        self_increment = self_fn/n + self_ft/n + self_moment*cm
        vector_bound = p0 + force_increment + self_increment
        tip_bound = share_ratio*vector_bound/tips_min
        p_lower = (cone_reference+cone_self)/alpha
        p_upper = min(s_max-(ft_max+self_ft)/n,
                      tip_capacity*tips_min/share_ratio-force_increment-self_increment)
        stations.append({'angle_rad': theta, 'normal_wrench_coefficients': coeff,
                         'normal_cone_margin_N': cone_margin,
                         'side_cone_margin_N': side_margin,
                         'radial_force_min_N': radial_min,
                         'radial_force_max_N': radial_max,
                         'compression_requirement_N': compress_need,
                         'vector_force_triangle_bound_N': vector_bound,
                         'tip_force_bound_N_if_30_engaged_and_gamma_1p2': tip_bound,
                         'preload_lower_from_normal_cone_N': p_lower,
                         'preload_upper_from_radial_and_tip_bounds_N': p_upper})
    # Verify the affine normal-force allocation reproduces its three basis
    # wrenches. This is numerical algebra, not a physical validation.
    errors = []
    for k in range(3):
        values = [s['normal_wrench_coefficients'][k] for s in stations]
        actual = [sum(row[j]*v for row, v in zip(rows, values)) for j in range(3)]
        errors += [abs(a-float(j == k)) for j, a in enumerate(actual)]
    assert max(errors) < 1e-10
    margins = {
        'normal_cone_N': min(s['normal_cone_margin_N'] for s in stations),
        'side_cone_N': min(s['side_cone_margin_N'] for s in stations),
        'radial_upper_N': s_max-max(s['radial_force_max_N'] for s in stations),
        'radial_positive_N': min(s['radial_force_min_N'] for s in stations),
        'compression_N': compression_max-max(s['compression_requirement_N'] for s in stations),
        'tip_force_N': tip_capacity-max(s['tip_force_bound_N_if_30_engaged_and_gamma_1p2'] for s in stations)}
    return {'missing_opposed_pair': sorted(omitted), 'healthy_stations': n,
            'all_conditional_margins_positive': min(margins.values()) > 0,
            'margins': margins,
            'preload_feasible_interval_N': [max(s['preload_lower_from_normal_cone_N'] for s in stations),
                                           min(s['preload_upper_from_radial_and_tip_bounds_N'] for s in stations)],
            'maximum_vector_force_bound_N': max(s['vector_force_triangle_bound_N'] for s in stations),
            'minimum_required_engaged_tips_at_8N_gamma_1p2': math.ceil(share_ratio*max(s['vector_force_triangle_bound_N'] for s in stations)/tip_capacity),
            'maximum_basis_reconstruction_error': max(errors), 'stations': stations}


def run():
    finance_factor = sum(1/1.08**y for y in range(1, 11))
    headroom = 0.70*0.512 - 0.302
    rough = [rough_support_screen()] + [rough_support_screen(i) for i in range(6)]
    assert all(r['all_conditional_margins_positive'] for r in rough)
    D, C, delta, jet_d = 7e-10, 1000.0, 20e-6, 400e-6
    faraday, molar_mass = 96485.33212, 0.063546
    j = 2*faraday*D*C/delta
    area = math.pi*jet_d**2/4
    current = j*area
    grams_hour = current/(2*faraday)*molar_mass*1000*3600
    return {
        'status': 'INTRODUCED_MODELS_NOT_A_BUILT_INTERFACE',
        'prepared_joint_clearance': [clearance_screen(c) for c in [53e-6, 60e-6, 78e-6, 85e-6]],
        'finance_screen': {'producer_case_cost_USD_service': 1.474,
                          'producer_favorable_comparator_USD_service': 0.512,
                          'target_USD_service': 0.70*0.512,
                          'producer_comparison_specific_common_floor_USD_service': 0.302,
                          'unique_headroom_USD_service': headroom,
                          'ten_year_discounted_100_annual_services': 100*finance_factor,
                          'unique_upfront_allowance_USD_if_no_other_unique_cost': headroom*100*finance_factor,
                          'allowance_USD_if_same_cost_repeats_at_year5': headroom*100*finance_factor/(1+1/1.08**5),
                          'scope': 'conditional use of producer approximate cases, not a universal cost lower bound or quotation'},
        'issued_energy_boundary': {'module_J_attempt': 714,
                                   'introduced_rejection_fraction': 0.02,
                                   'module_J_potential_accepted': 714/0.98,
                                   'separate_robot_J_potential_accepted': 300*64/0.98,
                                   'note': 'robot belongs to full service cost/energy; issued 1kJ module target is not retroactively expanded'},
        'rough_support_parameters': {'station_count': 12, 'nominal_radial_preload_N': 120,
                                    'final_radius_m': 0.032,
                                    'normal_cone_alpha': 0.7, 'side_cone_beta': 0.5,
                                    'radial_upper_N': 150, 'compression_upper_N': 100,
                                    'fn_reference_N': 100, 'ft_reference_N': 250,
                                    'bending_reference_Nm': 10,
                                    'separate_self_normal_N': 10, 'separate_self_shear_N': 10,
                                    'separate_self_bending_Nm': 0.25,
                                    'minimum_engaged_tips_per_live_station': 30,
                                    'introduced_load_share_factor': 1.2,
                                    'introduced_tip_capacity_N': 8,
                                    'physical_contact_law_and_contact_observations': 'UNQUALIFIED_NOT_SUPPLIED'},
        'rough_support_cases': rough,
        'coarse_tile_swept_geometry': {'radial_stroke_m': 0.010,
                                      'center_radius_start_m': 0.042, 'center_radius_end_m': 0.032,
                                      'tile_radial_extent_m': 0.012, 'tile_tangential_extent_m': 0.008,
                                      'maximum_corner_radius_m': math.hypot(0.042+0.006, 0.004),
                                      'minimum_center_separation_m': 2*0.032*math.sin(math.pi/12),
                                      'conservative_separation_after_two_tile_circumradii_m': 2*0.032*math.sin(math.pi/12)-2*math.hypot(0.006, 0.004),
                                      'scope': 'contact-tile planar swept boxes only; no rear carriage, tendon, force sensor, body or arm CAD'},
        'preload_stock': {'sum_local_radial_preload_N': 12*120,
                          'introduced_constant_preload_times_drag_work_J': 12*120*0.010,
                          'opposite_pair_balance': 'EXACT_IN_MODEL_NOT_A_FREE_HARDWARE_PROPERTY',
                          'twelve_node_polygon_hoop_force_N': 120/(2*math.sin(math.pi/12))},
        'introduced_round_tip_shank_screen': {'diameter_m': 0.0005, 'loaded_lever_m': 0.0005,
                                            'force_N': 8,
                                            'nominal_bending_Pa': 32*8*0.0005/(math.pi*0.0005**3),
                                            'scope': 'simple bending stress, not a steel grade, sharp-tip contact or masonry asperity fracture qualification'},
        'independent_copper_manufacturing_screen': {'introduced_D_m2_s': D, 'introduced_C_mol_m3': C,
                                                   'introduced_delta_m': delta, 'introduced_jet_d_m': jet_d,
                                                   'diffusion_film_current_density_A_m2': j,
                                                   'ideal_one_jet_current_A': current,
                                                   'ideal_one_jet_g_h': grams_hour,
                                                   'ideal_parallel_jets_for_1g_h': math.ceil(1/grams_hour),
                                                   'scope': 'introduced diffusion-film and unity current use; no empirical rate, field localization, finished-part function, recycle or whole-cost guarantee'}
    }


if __name__ == '__main__':
    o = run()
    path = Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(o, indent=2)+'\n')
    print(json.dumps({'file': str(path), 'clearance': o['prepared_joint_clearance'],
                      'finance': o['finance_screen'],
                      'rough_summary': [{k:r[k] for k in ['missing_opposed_pair','all_conditional_margins_positive','margins','preload_feasible_interval_N','maximum_vector_force_bound_N','minimum_required_engaged_tips_at_8N_gamma_1p2']} for r in o['rough_support_cases']],
                      'tiles': o['coarse_tile_swept_geometry'],
                      'copper': o['independent_copper_manufacturing_screen']}))
