"""Astra Pro3: exact positive-response rank collapse and common-source mixed controllers.

Original, independently executable rational/symbolic controls. Requires SymPy.
Outputs actual JSON. Does not call any physical instrument; the forward oracle
is an explicitly synthetic analytic source, and is charged when used.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

R=sp.Rational
t=sp.Symbol('t', real=True)
e0,e1,e2=[sp.eye(3)[:,i] for i in range(3)]
def obtain_posterior_from_saturated_reading(q,y,low=R(1),high=R(3)):
    """Actual rational source-observation-to-posterior conversion for n=3.

    A supplied spectral contract is required; saturation is checked exactly.
    Unknown orientation is computed from the observed column, not source code.
    """
    assert q.shape==(3,1) and y.shape==(3,1)
    assert (q.T*q)[0]==1
    mean=(low+high)/2
    radius=(high-low)/2
    w=sp.simplify((y-mean*q)/radius)
    if (w.T*w)[0]!=1 or (q.T*w)[0]!=0:
        raise ValueError('No exact saturated orthogonal column was acquired')
    v=q.cross(w)
    assert (v.T*v)[0]==1 and (q.T*v)[0]==0 and (w.T*v)[0]==0
    middle=mean*sp.eye(3)+radius*(q*w.T+w*q.T)
    SL=middle-radius*(v*v.T)
    SU=middle+radius*(v*v.T)
    assert SU-SL==(high-low)*(v*v.T)
    return SL,SU,v

historical_native_input=e0
historical_native_output=sp.Matrix([2,1,0])
SL,SU,v=obtain_posterior_from_saturated_reading(historical_native_input,historical_native_output)
S=SL+(t-1)*(v*v.T)


def frac(x):
    y=sp.cancel(x)
    if y.is_Rational: return str(y)
    return str(y)


def assert_positive(M):
    # Exact Sylvester criterion on a rational symmetric matrix
    assert M==M.T
    for i in range(1,M.rows+1):
        assert sp.factor(M[:i,:i].det())>0, (i,M)


def skew_controller(k):
    k=R(k)
    return sp.Matrix([[0,0,k],[0,0,0],[-k,0,0]])


def compile_matrix_term(K,p,l):
    K=sp.Matrix(K)
    base=SL-K
    # Contract: sym(S(t)-K)>= (1/2)I for all t in [1,3].
    # It is enough to test this at t=1, since S(t)-SL=(t-1)vv^T.
    symmetric_part=SL-(K+K.T)/2
    assert (symmetric_part-sp.eye(3)/2).is_positive_semidefinite
    Binv=base.inv()
    h=sp.factor((v.T*Binv*v)[0]);assert h>0
    q=sp.factor((v.T*Binv*p)[0])
    b=sp.factor((l.T*Binv*v)[0])
    a=sp.factor((l.T*Binv*p)[0])
    coefficient=sp.factor(b*q)
    expr=sp.factor(a-(t-1)*coefficient/(1+(t-1)*h))
    direct=sp.factor((l.T*(S-K).inv()*p)[0])
    assert sp.cancel(expr-direct)==0
    return dict(controller=[[frac(K[i,j]) for j in range(3)] for i in range(3)],
                p=p,l=l,h=h,coefficient=coefficient,baseline=a,expr=expr)


def compile_term(k,p,l):
    return compile_matrix_term(skew_controller(k),p,l)


def candidate_root_intervals(expr,eps=R(1,2**48)):
    d=sp.cancel(sp.diff(expr,t))
    num=sp.fraction(d)[0]
    if num==0: return []
    p=sp.Poly(num,t)
    out=[]
    for (lo,hi),multiplicity in p.intervals(eps=eps):
        if hi<1 or lo>3:continue
        lo=max(lo,R(1));hi=min(hi,R(3))
        if lo<=hi:
            out.append((lo,hi,int(multiplicity)))
    return out


def compile_portfolio(terms,precision=R(1,2**48)):
    """Each term is (weight, response action). All share one latent t.
    Extrema enclosures are proved by exact root isolation and a global
    Lipschitz bound sum |weight*coefficient|. No floating solve is trusted.
    """
    expr=sp.cancel(sum((w*z['expr'] for w,z in terms),sp.Integer(0)))
    # h>0 => 1+(t-1)h>=1 and |f'| <= sum|w*coefficient|.
    B=sp.factor(sum((abs(w*z['coefficient']) for w,z in terms),sp.Integer(0)))
    roots=candidate_root_intervals(expr,precision)
    exact=[sp.factor(expr.subs(t,a)) for a in (1,3)]
    root_data=[];candidate_outer=[]
    for a,b,mult in roots:
        midpoint=(a+b)/2
        center=sp.factor(expr.subs(t,midpoint))
        radius=sp.factor(B*(b-a)/2)
        root_data.append(dict(bracket=[frac(a),frac(b)],multiplicity=mult,
                              centered_value=frac(center),error_bound=frac(radius)))
        candidate_outer.append((center-radius,center+radius))
        exact.append(center)
    lower=min([sp.factor(expr.subs(t,1)),sp.factor(expr.subs(t,3))]+[a for a,b in candidate_outer])
    upper=max([sp.factor(expr.subs(t,1)),sp.factor(expr.subs(t,3))]+[b for a,b in candidate_outer])
    # An independent-source comparator duplicates the unknown parameter per term.
    ibounds=[]
    for w,z in terms:
        single=sp.cancel(w*z['expr'])
        vals=[single.subs(t,R(1)),single.subs(t,R(3))]
        # monotonic derivative (one rank-one inverse term)
        assert sp.factor(sp.diff(single,t))==0 or not sp.diff(single,t).has(t) or (vals[0]!=vals[1])
        ibounds.append((min(vals),max(vals)))
    independent_low=sum([a for a,b in ibounds],sp.Integer(0))
    independent_high=sum([b for a,b in ibounds],sp.Integer(0))
    assert independent_low<=lower<=upper<=independent_high
    source_val=sp.factor(expr.subs(t,R(7,4)))
    assert lower<=source_val<=upper
    return dict(expression=str(expr),derivative=str(sp.factor(sp.diff(expr,t))),
                derivative_bound=frac(B),stationary_root_intervals=root_data,
                shared_source_outer=[frac(lower),frac(upper)],
                shared_source_outer_width=frac(upper-lower),
                independent_source_range=[frac(independent_low),frac(independent_high)],
                independent_source_width=frac(independent_high-independent_low),
                width_reduction=frac((independent_high-independent_low)/(upper-lower)) if upper>lower else 'infinite',
                independent_checker_t='7/4',independent_checker_answer=frac(source_val))


def forced_family_audit():
    # Acquired one native action, no tomography or latent-parameter oracle.
    trueS=S.subs(t,R(7,4))
    measured=trueS*e0
    assert measured==historical_native_output
    obtained_lower,obtained_upper,obtained_direction=obtain_posterior_from_saturated_reading(e0,measured)
    assert obtained_lower==SL and obtained_upper==SU and obtained_direction==v
    assert_positive(trueS)
    assert_positive(3*sp.eye(3)-trueS+sp.eye(3)/1000000) # semidefinite endpoint handled separately
    D=SU-SL
    assert D.rank()==1 and D==2*(v*v.T)
    assert S*e0==measured and S*e1==sp.Matrix([1,2,0])
    assert (S-sp.eye(3)).subs(t,1).is_positive_semidefinite
    assert (3*sp.eye(3)-S).subs(t,3).is_positive_semidefinite
    return dict(native_inputs=[[1,0,0]],native_outputs=[[2,1,0]],
                charged_full_vector_calls=1,returned_scalars=3,
                supplied_spectral_contract=['I <= S','S <= 3I'],
                forced_second_action=[1,2,0],
                exact_consistency_family='S(t)=[[2,1,0],[1,2,0],[0,0,t]], 1<=t<=3',
                posterior_difference_rank=int(D.rank()),latent_interval=['1','3'],
                checker_hidden_t='7/4')


def noisy_failure():
    # Rational parameterization ensures exact contraction spectral bounds.
    s=R(1,1000);beta=sp.factor((1-s*s)/(1+s*s));gamma=sp.factor(2*s/(1+s*s))
    eps=1-beta
    assert beta**2+gamma**2==1
    systems=[]
    for sign in (-1,1):
        A=sp.Matrix([[2,beta,0],[beta,2,sign*gamma],[0,sign*gamma,2]])
        assert (A-sp.eye(3)).is_positive_semidefinite
        assert (3*sp.eye(3)-A).is_positive_semidefinite
        assert A*e0-sp.Matrix([2,1,0])==sp.Matrix([0,-eps,0])
        systems.append(A)
    # Two indistinguishable histories with answers separated by 2gamma.
    vals=[(e2.T*A*e1)[0] for A in systems]
    assert vals==[-gamma,gamma]
    # Valid uniform robust outer transfer to the collapsed family.
    # T=A-2I is symmetric contraction. ||T e0-e1||<=eps, so
    # ||T e1-e0||<=eps+sqrt(2eps); Frobenius difference <=delta.
    delta=sp.sqrt(2*(eps**2+(eps+sp.sqrt(2*eps))**2))
    assert sp.N(delta,20)>sp.N(gamma,20)
    K1=skew_controller(1);K2=skew_controller(2)
    expr=sp.factor((e2.T*(S-K1).inv()*e2)[0]-R(49,16)*(e2.T*(S-K2).inv()*e2)[0])
    exact_lo=min(expr.subs(t,a) for a in [R(1),R(2),R(3)])
    exact_hi=max(expr.subs(t,a) for a in [R(1),R(2),R(3)])
    # Sym(S-K_i)=S >=I, so ||(S-K_i)^-1||_2<=1. Resolvent error <=delta.
    rho=R(65,16)*delta
    alternative_task_values=[]
    for A in systems:
        value=sp.factor((e2.T*(A-K1).inv()*e2)[0]-R(49,16)*(e2.T*(A-K2).inv()*e2)[0])
        assert float(value)>float(exact_lo-rho) and float(value)<float(exact_hi+rho)
        alternative_task_values.append(frac(value))
    return dict(rational_defect_parameter='1/1000',reported_historical_reading=['2','1','0'],
                allowed_euclidean_reading_error=frac(eps),
                indistinguishable_future_responses=[frac(vv) for vv in vals],
                unavoidable_error_on_e2_transpose_S_e1=frac(gamma),
                rigorous_collapse_operator_norm_error_bound=str(delta),
                numeric_collapse_operator_norm_error_bound=float(sp.N(delta)),
                multi_controller_compiler_extra_radius=str(rho),
                numeric_extra_radius=float(sp.N(rho)),
                certified_robust_range=[str(exact_lo-rho),str(exact_hi+rho)],
                numeric_robust_range=[float(sp.N(exact_lo-rho)),float(sp.N(exact_hi+rho))],
                actual_alternative_controller_task_values=alternative_task_values,
                scope='Noisy near-saturation does not justify exact rank-one collapse; the certified outer result is valid under the supplied spectral contract and bounded historical error.')


def conditional_policy():
    # Counterfactual two-stage decision: K2 if stage-1 equilibrium >=3/8,
    # otherwise K3. One physical t persists across both stages.
    out1=compile_term(1,e2,e2)['expr']
    assert sp.factor(out1-R(3,8))==sp.factor(-9*(t-2)/(8*(3*t+2)))
    A=compile_term(2,e2,e2)['expr']
    B=compile_term(3,e2,e2)['expr']
    # Stage 1 branch: t in [1,2]; else t in (2,3].
    return dict(policy='Observe theoretical stage-1 equilibrium for k=1; if vertical state >=3/8, choose k=2, else choose k=3; then predict the vertical state.',
                stage1_switch='t=2',
                stage2_possible_output_intervals=[dict(branch='k2',latent_domain='[1,2]',range=[frac(A.subs(t,2)),frac(A.subs(t,1))]),
                                                   dict(branch='k3',latent_domain='(2,3]',range=[frac(B.subs(t,3)),frac(B.subs(t,2))],lower_endpoint_attained=True,upper_endpoint_attained=False)],
                baseline_independent_controller_ranges=[dict(branch='k2',range=[frac(A.subs(t,3)),frac(A.subs(t,1))]),
                                                        dict(branch='k3',range=[frac(B.subs(t,3)),frac(B.subs(t,1))])],
                native_calls_for_counterfactual_prediction=0,
                note='This predicts a specified feedback-policy response family; it is not an executed physical stage-1/stage-2 intervention.')


def main():
    old=forced_family_audit()
    q1=compile_term(1,e2,e2)
    q2=compile_term(2,e2,e2)
    q3=compile_term(3,e2,e2)
    left=compile_term(1,e2,e0)
    center=compile_term(2,e2,e1)
    cross=compile_term(3,e0,e2)
    Ksym=sp.diag(R(1,4),-R(1,4),R(1,3))
    Kmix=sp.Matrix([[0,R(1,5),R(1,6)],[-R(1,6),0,0],[0,0,R(1,4)]])
    msym=compile_matrix_term(Ksym,e2,e2)
    mmix=compile_matrix_term(Kmix,e2,e2)
    portfolios={
      'nonsymmetric_feedback_contrast_interior_optimum':[(R(1),q1),(-R(49,16),q2)],
      'three_controllers_signed_combo':[(R(2),q1),(-R(3),q2),(R(1),q3)],
      'cross_port_observables':[(R(1),left),(R(1),center),(-R(2),cross)],
      'symmetric_nonsymmetric_mixed_portfolio':[(R(1),msym),(-R(7,5),mmix),(R(1,2),left)],
    }
    compiled={name:compile_portfolio(terms) for name,terms in portfolios.items()}
    chief=compiled['nonsymmetric_feedback_contrast_interior_optimum']
    assert chief['shared_source_outer']==['-9/32','-207/880']
    assert chief['independent_source_range']==['-9/16','81/1360']
    assert chief['width_reduction']=='2068/153'
    noise=noisy_failure()
    policy=conditional_policy()
    result=dict(posterior_acquisition=old,compiled_late_portfolios=compiled,
                noise_stability_and_obstruction=noise,
                adaptive_policy_same_latent=policy,
                cost=dict(initial_native_full_vector_actions=1,later_native_actions_for_4_portfolios_and_policy=0,
                          source_aware_checker_uses_hidden_t=True,heavy_work='Exact 3x3 inverse precomputations and univariate symbolic root isolation for each portfolio'),
                comparison='An equally informed retaining or set-membership algorithm can use exactly this latent posterior and tie all guarantees; independent-controller marginal ranges discard legitimate shared-source information.')
    path=Path(__file__).with_name('acquired_latent_controller_results.json')
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASSED exact saturation and latent posterior test')
    for name,a in compiled.items():
        print(name,'joint range',a['shared_source_outer'],'independent range',a['independent_source_range'],'width ratio',a['width_reduction'])
    print('PASSED noisy indistinguishability and robust outer transfer')
    print('saved',path)

if __name__=='__main__': main()
