"""Qualify exact finite-temperature injectivity from the saved known-K frame.
No variances, candidate Gibbs integrals or inverse iterates are executed.
"""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter
import hashlib, json

P=Path(__file__).resolve().parent; start=perf_counter()
raw=(P/'FRAME.json').read_bytes(); d=json.loads(raw)
n=len(d['K']); A=F(d['prior_alpha_box'][1]); theta=F(d['finite_temperature'])
L=[[F(x) for x in row] for row in d['selected_frame_inverse']]
kappa=[F(x['kappa_floor']) for x in d['conditional_stationary_plans']]
q=F(101,2)*A*n*n*theta*max(sum(abs(L[i][j])/kappa[j]**5 for j in range(n)) for i in range(n))
assert 0<q<1
delta=F(d['target_all_parameter_linf_error']); stat=delta/2
steps=0; trunc=A
while trunc>delta/4:
    trunc*=q;steps+=1
forward=delta*(1-q)/8
radius=stat/(1-q)+forward/(1-q)+trunc
assert radius<delta
out={'status':'GLOBAL_FINITE_TEMPERATURE_INVERSE_QUALIFIED_NOT_EXECUTED',
 'scope':'Whole prior coefficient box for retained known-K n4 frame and actual positive finite temperature. General known endpoint-chain existence/rank proof is PROOF.txt sections2,4.',
 'FRAME_sha256':hashlib.sha256(raw).hexdigest(),
 'theta':str(theta),'q_global_contraction_upper':str(q),'q_display':float(q),
 'inverse_lipschitz_in_transformed_data':str(1/(1-q)),
 'target_parameter_radius':str(delta),'transformed_data_error_allowance':str(stat),
 'candidate_forward_transformed_error_required':str(forward),
 'contraction_steps_sufficient':steps,'finite_step_initial_error_upper':str(trunc),
 'resulting_parameter_radius_upper':str(radius),'radius_display':float(radius),
 'receiver_iteration':'clip_box(a-L*y_exact_candidate(a)+L*y_measured)',
 'actual_forward_integrals_evaluated':0,'actual_inverse_iterations':0,
 'actual_variance_observations':0,'new_frames_or_resolvents':0,
 'remaining':['actual justified variance inputs','finite-exposure/bath/shift/K calibration','physical validity of very small theta','qualified candidate forward integrals at displayed error','physical time mapping'],
 'ordinary_comparator':'Same-bath active FDT and full-data global likelihood/membership inversion remain admitted; no advantage or necessity inferred from this sufficient budget.',
 'elapsed_scalar_composition_seconds_after_imports':perf_counter()-start}
(P/'GLOBAL_INVERSE.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','q_display','contraction_steps_sufficient','radius_display','elapsed_scalar_composition_seconds_after_imports']},indent=2))
