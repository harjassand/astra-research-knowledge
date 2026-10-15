#!/usr/bin/env python3
"""Exact algebra for a Schur countermodel at a true scalar global minimizer.

All full quartic terms are retained. The analytic scalar-minimum and smooth
approximation arguments are proved separately; no finite grid sign is used.
"""
import json
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
a,b,c,d,e,n,z,t,ep=s.symbols("a b c d e n z t ep",real=True)
u=a*a+c*c;v=b*b+d*d;q=a*d-b*c
G=3*(u+v-2*q)**2+s.Rational(35,24)*u*u+q*q-s.Rational(5,2)*q*u
checks={}

# Full rank-one acoustic Gram, independently rebuilt from nine coefficients.
A,B,C,E,Gc,H,L,M,N=(s.Rational(107,24),3,19,-13,0,0,-s.Rational(29,2),-12,0)
M11=s.Matrix([[12*A,3*Gc,0,3*L],[3*Gc,2*C+2*E,-L,N],
              [0,-L,4*A,Gc],[3*L,N,Gc,2*C]])
M12=s.Matrix([[3*Gc,2*C+2*E,-L,N],[2*C+2*E,3*H,-N,M],
              [-L,-N,Gc,E],[N,M,E,H]])
M22=s.Matrix([[2*C+2*E,3*H,-N,M],[3*H,12*B,-3*M,0],
              [-N,-3*M,2*C,H],[M,0,H,4*B]])
K=s.zeros(4)
for (i,j),entry in zip([(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
                       [11,s.Rational(91,6),0,0,11,s.Rational(41,3)]):
 K[i,j]=entry;K[j,i]=-entry
gram=M11.row_join(M12+K).col_join((M12-K).row_join(M22))
sx,sy,h=s.symbols("sx sy h")
ac=s.diff(G.subs({a:a+h*sx,b:b+h*sy},simultaneous=True),h,2).subs(h,0)
mon=s.Matrix([sx*a,sx*b,sx*c,sx*d,sy*a,sy*b,sy*c,sy*d])
assert s.expand(ac-(mon.T*gram*mon)[0])==0
minors=[gram[:j,:j].det() for j in range(1,7)]
assert all(x>0 for x in minors)
assert gram[6:,6:]-gram[6:,:6]*gram[:6,:6].inv()*gram[:6,6:]==s.zeros(2)
checks["full_G_acoustic_certificate"]={"rank":gram.rank(),"six_minors":list(map(str,minors))}

# The actual first-row minimizer has identically zero transverse row stress.
diag={a:1,b:0,c:0,d:1+e}
assert s.diff(G,b).subs(diag)==0
Hdiag=s.simplify(s.hessian(G,(a,b,c,d)).subs(diag))
aa=38*e*e-11*e+s.Rational(9,2)
bb=12*e*e
cc=12*e*e-5*e+s.Rational(5,6)
dd=36*e*e+2
bc=12*e*e-2*e+s.Rational(1,2)
assert Hdiag[0,0]==aa and Hdiag[1,1]==bb
assert Hdiag[2,2]==cc and Hdiag[3,3]==dd and Hdiag[1,2]==bc
assert s.expand(aa-38*(e-s.Rational(11,76))**2)==s.Rational(563,152)
assert s.expand(cc-12*(e-s.Rational(5,24))**2)==s.Rational(5,16)
assert s.expand(cc-(bc-s.Rational(1,2))**2/bb)==s.Rational(1,2)-e
checks["scalar_Euler_and_uniform_blocks"]={
 "first_row_transverse_stress":"identically zero",
 "H11_matrix":str(Hdiag[:2,:2]),"H22_matrix":str(Hdiag[2:,2:]),
 "first_row_lower":"min(563/152,1/12)",
 "second_row_lower":"min(5/16,2)",
 "completed_mixed_residual":"1/2-e"}

# Exact two-zone map and triangular compatible perturbation.
w=s.Rational(5,11);yy=s.symbols("yy",real=True)
zones=[(s.Rational(1,12),s.Integer(1),yy-s.Rational(5,22),0,w),
       (s.Integer(1),-s.Rational(5,6),s.Rational(5,22)-s.Rational(5,6)*(yy-w),w,1)]
S,Cc=s.symbols("S C",real=True)
def trig_mean(expr):
 out=0
 for (i,j),coef in s.Poly(s.expand(expr),S,Cc).terms():
  if i%2 or j%2:continue
  ai,bj=i//2,j//2
  out+=coef*s.factorial(2*ai)*s.factorial(2*bj)/(4**(ai+bj)*s.factorial(ai)*s.factorial(bj)*s.factorial(ai+bj))
 return s.expand(out)

gap=0;base=0
for ev,zprime,zexpr,lo,hi in zones:
 delta={a:1-ep*n*n*z*S,b:ep*n*zprime*Cc,c:ep*n*Cc,d:1+ev}
 ex=trig_mean(G.subs(delta,simultaneous=True)-G.subs({a:1,b:0,c:0,d:1+ev}))
 gap+=s.integrate(ex.subs(z,zexpr),(yy,lo,hi))
 base+=(hi-lo)*G.subs({a:1,b:0,c:0,d:1+ev})
gap=s.expand(gap)
C0=s.Rational(34075,104544)
D0=s.Rational(217,24)
D1=s.Rational(4175,139392)
D2=s.Rational(66875,74961920)
C2=C0*n**4/4-n*n/48
D4=n**4*(D0+D1*n*n+D2*n**4)
assert s.expand(gap-(ep*ep*C2+ep**4*D4))==0
assert s.expand(gap).coeff(ep,1)==0 and s.expand(gap).coeff(ep,3)==0
checks["full_exact_quartic_action"]={
 "epsilon_squared_coefficient":str(C2),
 "epsilon_fourth_coefficient":str(D4),
 "cubic_and_linear":"zero by exact integration",
 "C0":str(C0),"D0":str(D0),"D1":str(D1),"D2":str(D2)}

# Exact strict reduced midpoint violation: n=1/4, epsilon=1/10.
c2=s.factor(C2.subs(n,s.Rational(1,4)))
d4=s.factor(D4.subs(n,s.Rational(1,4)))
decrease=s.factor(gap.subs({n:s.Rational(1,4),ep:s.Rational(1,10)}))
assert c2<-s.Rational(9,10000)
assert d4<s.Rational(1,25)
assert decrease<-s.Rational(1,200000)
checks["finite_strict_decrease"]={
 "x_period":"8pi","y_period":"1","n":"1/4","epsilon":"1/10",
 "quadratic_coefficient":str(c2),"quartic_coefficient":str(d4),
 "exact_energy_change":str(decrease),
 "rational_upper_bound":"-1/200000"}

# This entire two-zone trial family cannot give a negative QC gap, including
# arbitrary real epsilon and arbitrary x period n>0.
mean_e=w/s.Integer(12)+(1-w)
assert mean_e==s.Rational(7,12)
reference=G.subs({a:1,b:0,c:0,d:1+mean_e})
basegap=s.factor(base-reference)
assert basegap==s.Rational(575,384)
maxdrop=s.factor(1/(s.Integer(9216)*D0))
assert maxdrop==s.Rational(1,83328)
familylower=s.factor(basegap-maxdrop)
assert familylower==s.Rational(62387,41664)>0
checks["uniform_failed_QC_construction"]={
 "base_Jensen_gap":str(basegap),
 "all_periods_all_scales_maximum_possible_drop":str(maxdrop),
 "strict_uniform_Jensen_lower_bound":str(familylower)}

# The true row-minimized endpoint energies also remain above the affine
# baseline, using a whole-cell stress residual rather than sampled solves.
ct=s.symbols("ct",real=True)
base_stress=s.Matrix([s.diff(G,a),s.diff(G,b)]).subs(diag)
pert_stress=s.Matrix([s.diff(G,a),s.diff(G,b)]).subs({a:1,b:0,c:ct,d:1+e})
stress_difference=s.simplify(pert_stress-base_stress)
assert s.expand(stress_difference[0]-ct**2*(s.Rational(10,3)-s.Rational(29,2)*e))==0
assert s.expand(stress_difference[1]-ct*(bc+s.Rational(29,2)*ct**2))==0
stress_upper=s.Rational(67,6)/1600+s.Rational(1,40)*(s.Rational(21,2)+s.Rational(29,2)/1600)
assert stress_upper==s.Rational(103567,384000)<s.Rational(1,3)
energy_with_a_x=s.expand(G.subs({a:1,b:0,c:ct,d:1+e})-G.subs(diag))
assert s.expand(energy_with_a_x-cc*ct**2/2-s.Rational(107,24)*ct**4)==0
assert s.Rational(1,12)<s.Rational(1,2)**3
endpoint_lower=basegap-s.Rational(1,8)
assert endpoint_lower==s.Rational(527,384)>0
checks["true_scalar_minimum_endpoint_lower_bound"]={
 "global_stress_residual_upper":str(stress_upper),
 "scalar_minimization_improvement_upper":"1/8",
 "Jensen_gap_at_actual_endpoint_minimum_lower":str(endpoint_lower),
 "scope":"Every admissible first component, no numerical optimizer"}

# The second row is not stationary: this is not a counterexample to the
# many-center/full vector Euler criterion.
row2flux=s.diff(G,d).subs(diag)
assert s.expand(row2flux)==12*e**3+2*e-s.Rational(1,2)
checks["full_stationarity_scope"]={
 "second_row_longitudinal_flux_small_zone":str(row2flux.subs(e,s.Rational(1,12))),
 "second_row_longitudinal_flux_large_zone":str(row2flux.subs(e,1)),
 "claim":"First-row scalar Euler holds; full vector Euler does not."}

out={"status":"PASS","groups":len(checks),"checks":checks,
 "scope":"Exact algebra and full trial action; analytic scalar optimality and Schur interpretation are proved in SCALAR_EULER_SCHUR_COUNTERMODEL.md"}
(ROOT/"exact_countermodel_checks.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
