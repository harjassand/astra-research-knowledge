#!/usr/bin/env python3
"""Exact/algebraic checks only; not a numerical global-attraction certificate."""
import itertools
import json
import math
from pathlib import Path
import sympy as sp

DIR = Path(__file__).resolve().parent
a,b,c,d,e,n = sp.symbols('a b c d e n', nonnegative=True)
x=sp.Matrix([a,b,c,d,e])
s=(sp.sqrt(7)-1)/2
q=sp.Matrix([1,s*s,s,s,2-s])*sp.Rational(2,9)
zero=(0,0,0,0,0)
A=(1,0,0,0,0); AA=(2,0,0,0,0)
AC=(1,0,1,0,0); AD=(1,0,0,1,0); AE=(1,0,0,0,1)
CD=(0,0,1,1,0); AB=(1,1,0,0,0)
internal=[
 (AA,AC,sp.Integer(1)), (AC,AA,sp.Integer(1)),
 (AA,AD,sp.Integer(1)), (AD,AA,sp.Integer(1)),
 (AA,AE,sp.Integer(1)), (AE,AA,sp.Integer(1)),
 (AE,CD,sp.Integer(1)), (CD,AE,sp.Integer(2)),
 (CD,AB,sp.Integer(1)), (AB,CD,sp.Integer(1)),
]
full=internal+[(zero,A,sp.Integer(1)),(A,zero,sp.Integer(1))]

def prop(source,k,variables,falling):
    value=k
    for exponent,var in zip(source,variables):
        value *= sp.prod(var-j for j in range(exponent)) if falling else var**exponent
    return value

def field(channels,falling=False,variables=x):
    out=sp.zeros(5,1)
    for src,dst,k in channels:
        out+=(sp.Matrix(dst)-sp.Matrix(src))*prop(src,k,variables,falling)
    return out.applyfunc(sp.expand)

def is_zero_matrix(v):
    return all(sp.simplify(z)==0 for z in v)

F=sp.Matrix([
 -3*a*a+a*(c+d-b)+3*c*d,
 c*d-a*b,
 a*a-a*c+a*e-3*c*d+a*b,
 a*a-a*d+a*e-3*c*d+a*b,
 a*a-2*a*e+2*c*d,
])
actual=field(full,True)
correction=sp.Matrix([2*a+1,0,-a,-a,-a])
competitor=[(src,dst,s if src==AA and dst in (AC,AD) else k)
            for src,dst,k in internal]+[(AA,CD,1-s)]
comp_F=field(competitor)
complexes=sorted(set([src for src,dst,k in competitor]+[dst for src,dst,k in competitor]))
balances={}
for y in complexes:
    incoming=sum(prop(src,k,q,False) for src,dst,k in competitor if dst==y)
    outgoing=sum(prop(src,k,q,False) for src,dst,k in competitor if src==y)
    balances[str(y)]=str(sp.simplify(incoming-outgoing))
stoich=sp.Matrix.hstack(*(sp.Matrix(dst)-sp.Matrix(src) for src,dst,k in internal))
J=F.jacobian(x)
# The absolute row sums are convex; on a cube their maxima are attained at vertices.
row_bound=[0]*5
for corner in itertools.product((0,2), repeat=5):
    jj=J.subs(dict(zip(x,corner)))
    for i in range(5):
        row_bound[i]=max(row_bound[i],int(sum(abs(jj[i,j]) for j in range(5))))

checks={
 'actual_internal_field_exact':is_zero_matrix(field(internal)-F),
 'full_falling_factorial_drift_exact':is_zero_matrix(actual-F-correction),
 'total_drift_one_minus_a':sp.simplify(sum(actual)-(1-a))==0,
 'internal_total_conserved':sp.simplify(sum(F))==0,
 'competitor_drift_equivalent':is_zero_matrix(comp_F-F),
 'complex_balances_all_zero':all(v=='0' for v in balances.values()),
 'stoichiometric_rank_four':stoich.rank()==4,
 'normalized_equilibrium':sp.simplify(sum(q)-1)==0 and is_zero_matrix(F.subs(dict(zip(x,q)))),
 'equilibrium_A_fraction_two_ninths':sp.simplify(q[0]-sp.Rational(2,9))==0,
 'every_actual_coordinate_jump_at_most_one':all(abs(zz)<=1 for src,dst,k in full for zz in sp.Matrix(dst)-sp.Matrix(src)),
 'Lipschitz_40_sufficient':max(row_bound)<=40,
 'B_path_flux_min_is_one_minus_s':bool(sp.simplify(s*s-(1-s))>0),
 'star_edges_have_at_least_common_kappa':bool(sp.simplify(2*s-(1-s))>0),
 'kappa_exact_simplification':sp.simplify((1-s)*q[0]**2/24-(1-s)/486)==0,
}
qnum=[float(v) for v in q]
qmin=min(qnum); h=qmin*qmin/64; LH=1+math.log(2/qmin)
alpha=min(.01,qmin/100,h/(100*LH))
kappa=float((1-s)/486); Delta=2/kappa
checks.update({
 'qmin_is_B':qnum.index(qmin)==1,
 'normalization_error_below_2h_over15':LH*(40/3)*alpha <= (2/15)*h*(1+1e-12),
 'relative_segment_min_above_half_qmin':1-1/math.sqrt(32)-(40/3)/100 > .5,
 'explicit_inward_contraction_margin':math.exp(-1.5)<.25,
 'endpoint_entropy_23over60_below_half':sp.Rational(23,60)<sp.Rational(1,2),
 'whole_tube_entropy_17over15_below_two':sp.Rational(17,15)<2,
 'positive_A_service':sp.Rational(3,4)*(sp.Rational(2,9)-sp.Rational(2,9)/4)>=sp.Rational(1,8),
 'four_service_time_units_give_half_n_compensator':4*sp.Rational(1,8)==sp.Rational(1,2),
 'hit_plus_immigration_yields_seven_eighths':sp.Rational(3,4)+sp.Rational(1,8)==sp.Rational(7,8),
})
checks={k:bool(v) for k,v in checks.items()}
result={
 'status':'PASS' if all(checks.values()) else 'FAIL',
 'scope':'Exact algebra and elementary margins, not independent theorem review or uniform numerical entry certification.',
 'checks':checks,
 'full_count_drift':[str(v) for v in actual],
 'complex_balance_residuals':balances,
 'jacobian_absolute_row_maxima_on_cube_0_2':row_bound,
 'q_numeric_illustration':qnum,
 'universal_entropy_tube_constants_numeric_illustration':{'q_min':qmin,'h':h,'L_H':LH,'alpha':alpha,'kappa':kappa,'Delta':Delta},
 'not_evaluated':['tau_epsilon','c_epsilon','n0_epsilon'],
}
(DIR/'check_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert all(checks.values()),checks
