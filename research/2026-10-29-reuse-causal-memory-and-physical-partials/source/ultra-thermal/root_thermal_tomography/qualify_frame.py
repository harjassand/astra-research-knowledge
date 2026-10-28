"""Known-K thermal interface qualification; acquires NO variance observations.

Exact Fraction/SymPy frame on already decoded K, with conservative finite
temperature/noise design. Does not read retained alpha as measured truth.
"""
from pathlib import Path
from fractions import Fraction as F
from time import perf_counter
import hashlib, json
import sympy as S

P=Path(__file__).resolve().parent
t0=perf_counter()
source=P.parent/'root_network_commutator/RESULT.json'
d=json.loads(source.read_text())
K=S.Matrix([[S.Rational(x) for x in row] for row in d['K_recovered']])
n=K.rows; p=0; A=F(3,2); delta=F(1,25); zeta=F(1,20)
base_floor=min(K[i,i]-sum(abs(K[i,j]) for j in range(n) if j!=i) for i in range(n))
assert base_floor>0
shifts=list(range(1,3*n-1)); frames=[]; b=[]; floors=[]
for lam in shifts:
    R=(K+lam*S.eye(n)).inv(method='DM')
    frames.append([R[i,i]*R[p,i]**2 for i in range(n)])
    b.append(F(str(R[p,p]))); floors.append(F(str(base_floor+lam)))
T=S.Matrix(frames)
selected=list(T.T.rref()[1])
assert len(selected)==n
M=T.extract(selected,list(range(n))); Li=M.inv(method='DM')
assert Li*M==S.eye(n)
L=[[F(str(Li[i,j])) for j in range(n)] for i in range(n)]
row_norm=max(sum(abs(x) for x in row) for row in L)
caps=[F(111,4)*A*A*n*n/floors[j]**5 for j in selected]
bias_norm=max(sum(abs(L[i][j])*caps[j] for j in range(n)) for i in range(n))
temperature=min([2*floors[j]**2/(3*n*A) for j in selected]+[delta/(2*bias_norm)])
assert temperature>0
noise_eta=delta/(2*row_norm)
variance_error=3*temperature*temperature*noise_eta
budgets=[]
def ceil(x):return -(-x.numerator//x.denominator)
for j in selected:
    plans=[]
    for sigma in [F(0),F(1,10**6)]:
        S0=temperature*b[j]+sigma*sigma
        Q=ceil(F(n,1)/zeta*18*S0*S0/(variance_error*variance_error))
        assert F(18)*S0*S0/Q<=zeta*variance_error**2/n
        plans.append({'sigma_per_point_read':str(sigma),'Q':Q,
                      'stationary_duration_upper_design_native_units':str(F(Q)/floors[j])})
    budgets.append({'shift':shifts[j],'kappa_floor':str(floors[j]),
        'b_Rpp':str(b[j]),'bias_eta_bound':str(caps[selected.index(j)]*temperature),
        'read_spacing':str(1/floors[j]),'conditional_point_read_plans':plans})
errs=[sum(abs(L[i][j])*(caps[j]*temperature+noise_eta) for j in range(n)) for i in range(n)]
assert max(errs)<=delta
out={'status':'EXACT_KNOWN_K_THERMAL_FRAME_QUALIFIED_NO_OBSERVATIONS',
 'scientific_scope':'Qualified scalar finite-temperature interface on retained decoded n4 K, with box prior on ALL quartics. General path rank theorem is analytical; this star is separately rank checked. No physical bath, K calibration, shunts, variances or samples acquired.',
 'source_decoded_K_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'K':d['K_recovered'],'source_alpha_read':False,
 'all_shifts':shifts,'frame':[[str(x) for x in row] for row in T.tolist()],
 'selected_row_indices':selected,'selected_shifts':[shifts[j] for j in selected],
 'selected_frame_inverse':[[str(x) for x in row] for row in Li.tolist()],
 'selected_frame_determinant':str(M.det()),'frame_linf_inverse_norm':str(row_norm),
 'prior_alpha_box':['0',str(A)],'target_all_parameter_linf_error':str(delta),
 'joint_failure_probability_upper':str(zeta),'finite_temperature':str(temperature),
 'finite_temperature_display':float(temperature),'variance_error_per_shift':str(variance_error),
 'variance_error_per_shift_display':float(variance_error),
 'resulting_parameter_error_bounds':[str(x) for x in errs],
 'conditional_stationary_plans':budgets,
 'receiver':'Given actual justified scalar variance intervals, use bounded-error box LP; displayed inverse bounds provide a conservative simple alternative.',
 'new_observed_variances':0,'new_H1_or_H3_observations':0,'new_topologies':0,
 'known_K_rational_resolvent_calculations':len(shifts),
 'elapsed_seconds_after_imports':perf_counter()-t0,
 'unacquired':['physical known K','uniform shift control/calibration','mechanical distributed bath and theta','stationary preparation','finite exposure','actual variance intervals','model validity at this temperature','physical time conversion','practical advantage','historical novelty'],
 'ordinary_comparator':'Same-bath active FDT has identical static variance information; ordinary all-data LP/likelihood may improve the deliberately conservative inverse/Chebyshev design.'}
(P/'FRAME.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','selected_shifts','finite_temperature_display','variance_error_per_shift_display','elapsed_seconds_after_imports']},indent=2))
for plan in budgets:
    print(json.dumps({'shift':plan['shift'],'Q':[x['Q'] for x in plan['conditional_point_read_plans']]}))
