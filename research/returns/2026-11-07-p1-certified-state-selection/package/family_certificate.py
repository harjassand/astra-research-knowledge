"""Exact constants in the all-n addressability corollary (not finite-case tests)."""
from fractions import Fraction as Q
from plan import save, ROOT
from exact import require


def certificate():
    n_bound_note='n>=2, s=ceil(sqrt(n)), sqrt(n)<=s<=n; E<=1/(1000n)'
    face_other=Q(22,1000)+Q(10,1000)+Q(11,10000)
    m=Q(7,5);alpha=Q(1,2);ell=Q(9,8);BH=Q(33,16)
    q_displacement=face_other/Q(143,100)
    true_nominal_distance=Q(1,1000)+Q(11,10000)/m
    nu=Q(1,128000); ev=za=Q(1,16000)
    enlarged_coordinate=Q(11,10)+nu
    Knorm=Q(3021,1000)
    Lbound=Knorm+3*enlarged_coordinate**2
    Fbound=(Knorm+enlarged_coordinate**2)*enlarged_coordinate+Q(1,100)
    read_radius_ratio=ell*(Q(1101,1000)+Q(1,500))+Q(1,20)
    ew=Q(1201,1000000)
    w0=Q(41,10000)+ell*(Q(1,500)+ew)
    D0_ratio=7+za+Q(31,10000)+8*(Q(1,200)+ew)
    dynamic_floor=2*(Q(3,16000)+Q(1768,2097152))
    bound=w0+Q(16,262144)+dynamic_floor
    eval_round_bound=Q(3101,2000000000)
    require(face_other<Q(171,1000))
    require(Q(143,100)-Q(1,1000)>=m)
    require((m-alpha)*(1-alpha)>=alpha*Q(1,4))
    require(q_displacement+Q(1,20)<Q(1,10))
    require(true_nominal_distance<Q(1,500))
    require(Lbound<8 and Fbound<6 and read_radius_ratio<2)
    require(4*BH+4<=13 and 2*BH+7<=13 and D0_ratio<8)
    require(eval_round_bound<ev and Q(1,2000000)<Q(1,10000))
    require(bound<Q(1,100))
    require(q_displacement+Q(1,100)<Q(1,25))
    return {'status':'PASS','scope':'symbolic all-n reductions in THEOREM section 10; no new source acquisition or hardware run',
        'parameter_contract':n_bound_note,'competing_equilibria_lower_count':'2^n',
        'box_face_base_margin':Q(171,1000),'box_face_remaining_gradient_bound':face_other,
        'true_local_curvature_lower':m,'full_state_rate':alpha,'nominal_projected_gradient_ratio':Q(157,300),
        'equilibrium_coordinate_distance_to_address':q_displacement,
        'compiled_target_distance_to_true_equilibrium':true_nominal_distance,
        'full_state_basin_radius':Q(1,20),'read_error_norm':nu,'actuator_error_norm':za,
        'sample_and_actuator_time':'1/(262144*ceil(sqrt(n)))','maximum_read_age':'9 Delta/8',
        'write_duration':'1+ceil(log2(2000*ceil(sqrt(n))))',
        'write_handover_state_bound':w0,'write_handover_actuator_ratio_upper':D0_ratio,
        'feedback_Lipschitz_upper':Lbound,'feedback_norm_ratio_upper':Fbound,
        'retention_state_norm_ratio_upper':read_radius_ratio,'retention_error_floor':dynamic_floor,
        'complete_handover_and_retention_error':bound,
        'retained_coordinate_distance_to_address':q_displacement+Q(1,100),
        'controller_evaluation_error_bound_for_denominator_at_least_1000000_n_squared':eval_round_bound,
        'fixed_retention_law_for_all_addresses':True,'whole_internal_identification_required':False,
        'global_minimizer_search_claim':False}


if __name__=='__main__':
    result=certificate();save(ROOT/'results/FAMILY_CERTIFICATE.json',result)
    print('All-n family certificate PASS; uniform handover error =',float(result['complete_handover_and_retention_error']))
