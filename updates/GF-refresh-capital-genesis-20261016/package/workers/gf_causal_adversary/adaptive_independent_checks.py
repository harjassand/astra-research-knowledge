"""New exact finite checks of the adaptive/mean-action interface.

This code was authored independently after reading the two proposed proofs,
before reading any producer test output. It is not a universal proof.
"""
from pathlib import Path
from time import perf_counter
import json
import sympy as s

base=Path(__file__).resolve().parent
started=perf_counter()
checks=[]


def same(a,b):
    if hasattr(a,'shape'):
        assert a.shape==b.shape
        assert all(s.simplify(x)==0 for x in a-b)
    else:
        assert s.simplify(a-b)==0


def norm2(v):
    return s.simplify((v.conjugate().T*v)[0])


k=(s.pi+2)/4
p=s.symbols('p',positive=True)
low=s.asin(s.sqrt(p))/k
high=(s.pi/4+p-s.Rational(1,2))/k
same(low.subs(p,s.Rational(1,2)),high.subs(p,s.Rational(1,2)))
same(s.diff(low,p).subs(p,s.Rational(1,2)),s.diff(high,p))
same(low.subs(p,0),0)
same(high.subs(p,1),1)
same(s.diff(low,p,2),(2*p-1)/(4*k*(p*(1-p))**s.Rational(3,2)))
checks.append({'name':'potential_endpoints_join_and_second_derivative_identity','passed':True,
               'concavity_sign_reason':'2*p-1 <= 0 on the lower interval; upper derivative is constant'})


# A rational no-click amplitude permits an exact two-level branch calculation.
eps=s.Rational(3,4)
P=s.diag(0,1)
C=s.diag(0,s.sqrt(3)/2)
N=s.diag(1,s.Rational(1,2))
same(C.conjugate().T*C+N.conjugate().T*N,s.eye(2))
same(C*P,P*C)
same(N*P,P*N)
restore=s.Matrix([[3,-1],[1,3]])/s.sqrt(10)
half=s.Matrix([1,1])/s.sqrt(2)
same(restore.conjugate().T*restore,s.eye(2))
r=1-eps/2
same(restore*N*half,s.sqrt(r)*half)
same(norm2(C*half),eps/2)
checks.append({'name':'exact_weak_instrument_and_coherence_restoration','passed':True,
               'epsilon':'3/4','no_click_probability':'5/8','restore_angle':'atan(1/3)',
               'system_dimension':2})


n=3
state=half
success=0
charged_restore_coefficient=0
probe_reach_sum=0
for _ in range(n):
    probe_reach_sum+=norm2(state)
    success+=norm2(C*state)
    state=N*state
    charged_restore_coefficient+=norm2(state)
    state=restore*state
success+=norm2(P*state)
same(success,1-r**n/2)
same(charged_restore_coefficient,r*(1-r**n)/(1-r))
same(probe_reach_sum,(1-r**n)/(1-r))
A=s.pi/4+s.atan(s.Rational(1,3))*charged_restore_coefficient
checks.append({'name':'finite_complete_branch_weak_herald_protocol','passed':True,
               'weak_probes_max':n,'success_exact':str(success),
               'restore_cost_coefficient_exact':str(charged_restore_coefficient),
               'probe_reach_sum_exact':str(probe_reach_sum),
               'expected_odd_action_expression':str(A),
               'ratio_decimal_diagnostic_only':str((A/success).evalf(25)),
               'final_complete_measurement_included':True})


u=s.symbols('u',positive=True)
eps_u=4*u/(1+u)**2
same((2-eps_u)/eps_u,(1+u*u)/(2*u))
series=s.series((1+u*u)*s.atan(u)/(2*u),u,0,5)
same(s.expand(series.removeO()),s.Rational(1,2)+u*u/3-u**4/15)
checks.append({'name':'weak_limit_action_formula_and_series','passed':True,
               'k_star':str(k),'series_in_u':str(series),
               'epsilon_leading_correction':'epsilon^2/48'})


# Exact counterexample to replacing a hard hazard cap by expected stopped hazard.
P_success=s.Rational(3,4)
mean_H=s.Rational(3,2)*s.log(2)
jensen_expression=1-s.sqrt(2)/4
same(P_success-jensen_expression,(s.sqrt(2)-1)/4)
same(1-s.exp(-2*s.log(2)),P_success)
checks.append({'name':'expected_stopped_hazard_jensen_counterexample','passed':True,
               'attempts_max':2,'attempt_angle':'pi/4','stop_at_first_mismatch':True,
               'success':'3/4','expected_stopped_hazard':'(3/2)*log(2)',
               'invalid_expected_hazard_bound':'1-sqrt(2)/4',
               'positive_excess':'(sqrt(2)-1)/4',
               'valid_hard_ledger_cap':'2*log(2)'})


activation=s.Rational(1,4)
C_mean=s.pi/8
singleton_certificate=s.simplify(C_mean/k)
same(singleton_certificate,s.pi/(2*(s.pi+2)))
checks.append({'name':'shared_activation_mean_cost_product_failure','passed':True,
               'joint_success':'1/4','each_mean_odd_action':'pi/8',
               'each_mean_cost_certificate':str(singleton_certificate),
               'product_failure_reason':'each certificate < 1/2, so their product < 1/4',
               'product_of_actual_marginals':'1/16',
               'counterexample_to_fixed_schedule_product':False})


out={'self_authored':True,'producer_test_outputs_read':False,
     'proof_scope':'finite exact identities and witnesses only; universal claims use analytic adjudication',
     'all_passed':True,'checks':checks,'check_modules':len(checks),
     'maximum_system_dimension':2,'arithmetic':'SymPy exact rational/algebraic and symbolic expressions',
     'optimizations':0,'random_searches':0,'installs':0,
     'wall_seconds':perf_counter()-started,'thinking_tokens':'UNKNOWN; not measured or inferred'}
(base/'ADAPTIVE_EXACT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
