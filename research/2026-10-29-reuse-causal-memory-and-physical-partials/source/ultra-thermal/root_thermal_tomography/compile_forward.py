"""Whole-box finite Gaussian-moment forward operator; no parameter table/data.
All polynomial coefficients are exact. No inverse iterate is executed.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from time import perf_counter
import hashlib, json
import sympy as S

P=Path(__file__).resolve().parent; start=perf_counter()
frame=json.loads((P/'FRAME.json').read_text())
glob=json.loads((P/'GLOBAL_INVERSE.json').read_text())
K=S.Matrix([[S.Rational(x) for x in row] for row in frame['K']])
n=K.rows; A=F(frame['prior_alpha_box'][1]); theta=F(frame['finite_temperature'])
L=[[F(x) for x in row] for row in frame['selected_frame_inverse']]
packets=[]; errors=[]; cache_states=0
for col,plan in enumerate(frame['conditional_stationary_plans']):
    lam=plan['shift']; kap=F(plan['kappa_floor'])
    Ri=(K+lam*S.eye(n)).inv(method='DM')
    R=[[F(str(x)) for x in row] for row in Ri.tolist()]
    @lru_cache(None)
    def moment(e):
        if not any(e):return F(1)
        if sum(e)%2:return F(0)
        i=next(j for j,x in enumerate(e) if x)
        left=list(e);left[i]-=1;out=F(0)
        for j,k in enumerate(left):
            if k:
                rem=left.copy();rem[j]-=1
                out+=k*R[i][j]*moment(tuple(rem))
        return out
    def mon(pairs):
        e=[0]*n
        for i,power in pairs:e[i]+=power
        return moment(tuple(e))
    mu=[mon([(i,4)])/4 for i in range(n)]
    n1=[mon([(0,2),(i,4)])/4 for i in range(n)]
    m2=[[mon([(i,4),(j,4)])/16 for j in range(n)] for i in range(n)]
    n2=[[mon([(0,2),(i,4),(j,4)])/16 for j in range(n)] for i in range(n)]
    assert all(n1[i]-R[0][0]*mu[i]==3*R[i][i]*R[0][i]**2 for i in range(n))
    assert m2==list(map(list,zip(*m2))) and n2==list(map(list,zip(*n2)))
    n2bound=F(945)*A*A*n*n/(16*kap**5)
    m3bound=F(10395)*(A*n/4)**3/kap**6
    n3bound=F(135135)*(A*n/4)**3/kap**7
    Nmax=1/kap+theta**2*n2bound/2
    err=theta**2*(n3bound+2*Nmax*m3bound)/9
    errors.append(err);cache_states+=moment.cache_info().currsize
    packets.append({'shift':lam,'R':[[str(x) for x in row] for row in R],
      'mu_linear':[str(x) for x in mu],'n1_linear':[str(x) for x in n1],
      'm2_quadratic':[[str(x) for x in row] for row in m2],
      'n2_quadratic':[[str(x) for x in row] for row in n2],
      'uniform_y2_error':str(err),'Wick_cache_states':moment.cache_info().currsize})
total=max(sum(abs(L[i][j])*errors[j] for j in range(n)) for i in range(n))
assert total<F(glob['candidate_forward_transformed_error_required'])
radius=F(glob['transformed_data_error_allowance'])/(1-F(glob['q_global_contraction_upper']))+total/(1-F(glob['q_global_contraction_upper']))+F(glob['finite_step_initial_error_upper'])
assert radius<F(glob['target_parameter_radius'])
out={'status':'WHOLE_BOX_POLYNOMIAL_FORWARD_INTERFACE_ACQUIRED',
 'scope':'Exact coefficient polynomials and finite Taylor remainder for ALL alpha in stated prior box. No physical variance, truth-alpha table, candidate equilibrium sample, new topology, or inverse iterate.',
 'prior_alpha_box':frame['prior_alpha_box'],'theta':str(theta),'packets':packets,
 'evaluation':'mu=a dot mu_linear; n1=a dot n1_linear; m2=a.T m2_quadratic a; n2=a.T n2_quadratic a; Z2=1-theta*mu+theta^2*m2/2; N2=Rpp-theta*n1+theta^2*n2/2; y2=(Rpp-N2/Z2)/(3theta), with exact rational arithmetic or outward rounding.',
 'uniform_transformed_forward_error':str(total),'error_display':float(total),
 'allowed_transformed_forward_error':glob['candidate_forward_transformed_error_required'],
 'same_conditional_receiver_radius_with_this_forward_bound':str(radius),
 'receiver_radius_display':float(radius),
 'Gaussian_moments_max_total_degree':10,'rational_known_K_resolvents':len(packets),
 'total_memoized_Wick_states':cache_states,'candidate_data_or_inverse_iterates':0,
 'elapsed_seconds_after_imports':perf_counter()-start,
 'scientific_status':'Root internal construction, peer review pending; not historical novelty or practical advantage.',
 'input_sha256':{name:hashlib.sha256((P/name).read_bytes()).hexdigest() for name in ['FRAME.json','GLOBAL_INVERSE.json','PROOF.txt']}}
(P/'FORWARD.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','error_display','receiver_radius_display','Gaussian_moments_max_total_degree','rational_known_K_resolvents','total_memoized_Wick_states','elapsed_seconds_after_imports']},indent=2))
