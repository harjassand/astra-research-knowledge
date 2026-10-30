"""Explicit PC-arc radius from exact rational coefficient perturbation bounds.

Requires the verified center eigenvalue bounds and the actual continuing
matrices. No parameter-grid or numerical eigenvalue value enters the proof.
"""
from pathlib import Path
from fractions import Fraction as R
import json,time
import sympy as S

HERE=Path(__file__).resolve().parent;start=time.time()
family=json.loads((HERE/'b0_pc_continuation.json').read_text())
center=json.loads((HERE/'b0_pc_verification.json').read_text())
ell=R(center['minimum_eigenvalue_exact_lower_bound']);assert ell>0
u,b=S.symbols('u b',real=True);u0=S.Rational(1,6);ref=R(1,1000)
cache={};den_radius=ref

def frac(x):return R(int(x.p),int(x.q))

def bounds(expr):
    global den_radius
    key=str(expr)
    if key in cache:return cache[key]
    ff=S.cancel(S.sympify(expr,locals={'u':u}));p,q=S.fraction(ff)
    if ff==0:cache[key]=R(0);return R(0)
    pp=S.Poly(p,u,domain=S.QQ).shift(u0);qq=S.Poly(q,u,domain=S.QQ).shift(u0)
    pc={j:frac(pp.nth(j)) for j in range(pp.degree()+1)}
    qc={j:frac(qq.nth(j)) for j in range(qq.degree()+1)}
    p0=pc.get(0,R(0));q0=qc.get(0,R(0));assert q0!=0
    Sq=sum((abs(qc[j])*ref**(j-1) for j in qc if j),R(0))
    Sf=sum((abs(pc.get(j,R(0))*q0-p0*qc.get(j,R(0)))*ref**(j-1) for j in range(1,max(max(pc),max(qc))+1)),R(0))
    if Sq:den_radius=min(den_radius,abs(q0)/(2*Sq))
    variation=2*Sf/(q0*q0)
    cache[key]=variation
    return variation

max_entry=R(0);max_b=max_d=0
for name in ('C','M'):
    for row in family[name]:
        for pp in row:
            total=R(0)
            for ib,id_,co in pp:
                max_b=max(max_b,ib);max_d=max(max_d,id_);total+=bounds(co)
            max_entry=max(max_entry,total)
# The acquired kernel and factors must also stay defined.
for pp in family['kernel']:
    for ib,id_,co in pp:bounds(co)
for co in S.Poly(S.sympify(family['g'],locals={'u':u,'b':b}),b).all_coeffs():bounds(co)
bounds(family['M_lambda'])
assert max_d<=6
amplification=3**max_d
L=amplification*max_entry
assert L>0
proposed=min(ref,den_radius,ell/(10*L),R(1,12))
assert proposed>0
exponent=max(0,proposed.denominator.bit_length()-proposed.numerator.bit_length())
h=R(1,2**exponent)
while h>proposed:exponent+=1;h/=2
assert h<=ref and h<=den_radius and h<=R(1,12)
assert 5*L*h<=ell/2
out={'center':'1/6','dyadic_radius_exponent':exponent,'radius':'2^(-%d)'%exponent,
     'minimum_center_eigenvalue_lower_bound':str(ell),
     'Bernstein_entry_variation_per_unit_parameter':str(L),
     'coefficient_denominator_radius_bound':str(den_radius),
     'reference_radius':str(ref),'maximum_b_degree':max_b,'maximum_d_degree':max_d,
     'Bernstein_amplification_bound':amplification,
     'unique_rational_functions_bounded':len(cache),
     'operator_change_at_radius':str(5*L*h),
     'all_radius_inequalities_exact':True,
     'conclusion':'For every real u with |u-1/6|<2^(-%d), the SAME acquired support rule and continuing acoustic lift prove polyconvexity of F_(beta(u),r(u)).'%exponent,
     'seconds':time.time()-start}
(HERE/'b0_pc_arc_radius.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({key:out[key] for key in ('radius','unique_rational_functions_bounded','all_radius_inequalities_exact','seconds')},indent=2))
