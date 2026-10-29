import sympy as s, json
from finite_boundary_tests import exclusion,q_r
r=s.symbols('r');states,L=exclusion(q_r(r),k=2);L=L.applyfunc(s.factor)
a=s.zeros(1,6);a[0,0]=1;b=s.Matrix([int(0 in z) for z in states]);v=a;mom=[]
for j in range(6):
 mom.append(s.factor((v*b)[0]));v=(v*L).applyfunc(s.factor)
assert s.factor(mom[4]-mom[4].subs(r,0))==2*r*(r-1)
assert s.simplify(mom[5]-mom[5].subs(r,1-r)-23*(2*r-1))==0
out={'states':states,'generator':[[str(v) for v in z] for z in L.tolist()],'boundary_occupancy_derivatives_0_to_5':list(map(str,mom)),'derivative_4_minus_r0':str(s.factor(mom[4]-mom[4].subs(r,0))),'derivative_5_minus_1_minus_r':str(s.factor(mom[5]-mom[5].subs(r,1-r))),'assertions':'PASS'}
print(json.dumps(out,indent=2))
