#!/usr/bin/env python3
"""Exact bounded algebra supporting SHEAR_DENSITY_AVERAGING.md.

General convexity, Sobolev limits, Holder and Fourier LH are analytic proofs.
No finite collection of these checks is labeled universal quasiconvexity.
"""
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parent
checks = {}
a,b,c,d,ss,tt = s.symbols("a b c d ss tt", real=True)
u,v,w,q = a*a+c*c,b*b+d*d,a*b+c*d,a*d-b*c
G = 3*(u+v-2*q)**2+s.Rational(35,24)*u*u+q*q-s.Rational(5,2)*q*u

# Independent exact full acoustic certificate for G.
A,B,C,E,Gc,H,L,M,N = (s.Rational(107,24),3,19,-13,0,0,-s.Rational(29,2),-12,0)
M11=s.Matrix([[12*A,3*Gc,0,3*L],
 [3*Gc,2*C+2*E,-L,N],[0,-L,4*A,Gc],[3*L,N,Gc,2*C]])
M12=s.Matrix([[3*Gc,2*C+2*E,-L,N],
 [2*C+2*E,3*H,-N,M],[-L,-N,Gc,E],[N,M,E,H]])
M22=s.Matrix([[2*C+2*E,3*H,-N,M],
 [3*H,12*B,-3*M,0],[-N,-3*M,2*C,H],[M,0,H,4*B]])
K=s.zeros(4)
for (i,j),entry in zip([(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
                       [11,s.Rational(91,6),0,0,11,s.Rational(41,3)]):
 K[i,j]=entry;K[j,i]=-entry
Q=M11.row_join(M12+K).col_join((M12-K).row_join(M22))
e=s.symbols("e", real=True)
acoustic=s.diff(G.subs({a:a+e*ss,b:b+e*tt}, simultaneous=True),e,2).subs(e,0)
z=s.Matrix([ss*a,ss*b,ss*c,ss*d,tt*a,tt*b,tt*c,tt*d])
assert s.expand(acoustic-(z.T*Q*z)[0])==0
leading=[s.factor(Q[:j,:j].det()) for j in range(1,7)]
assert all(x>0 for x in leading)
assert Q[6:,6:]-Q[6:,:6]*Q[:6,:6].inv()*Q[:6,6:]==s.zeros(2)
assert Q.rank()==6
checks["G_full_rank_one_convexity"]={
 "leading_six_minors":list(map(str,leading)),
 "rank":6,"last_schur_complement":"zero",
 "scope":"Full acoustic Gram plus left SO(2), not angular samples"}

# Rank-one value has exact minimum mu=3.
rank_one=G.subs({a:ss*a,b:tt*a,c:ss*c,d:tt*c},simultaneous=True)
rank_one_norm=((a*a+c*c)*(ss*ss+tt*tt))**2
assert s.expand(rank_one-3*rank_one_norm-s.Rational(35,24)*(ss*ss*(a*a+c*c))**2)==0
checks["G_mu_exact"]="3; equality for a nonzero rank-one matrix with first column zero"

# Cubic flux at a=0 in the polar row representation.
p1,p2,k1,k2,Lc,Mc,Nc = s.symbols("p1 p2 k1 k2 Lc Mc Nc",real=True)
odd=q*(Lc*u+Mc*v+Nc*w)
odd_rows=odd.subs({a:p1,b:p2,c:k1,d:k2},simultaneous=True)
flux=s.Matrix([s.diff(odd_rows,p1),s.diff(odd_rows,p2)]).subs({p1:0,p2:0})
h=Lc*k1*k1+Mc*k2*k2+Nc*k1*k2
assert s.simplify(flux-h*s.Matrix([k2,-k1]))==s.zeros(2,1)
checks["polar_odd_flux"]=str(flux)

# Compatible gradient decomposition for the averaged amplitude.
r,R,rx,ry,Rx,gp,k=s.symbols("r R rx ry Rx gp k",positive=True)
full=s.Matrix([[rx,ry],[r*gp,r*k]])
bar=s.Matrix([[Rx,0],[R*gp,R*k]])
error=s.Matrix([[rx-r*Rx/R,ry],[0,0]])
assert s.simplify(full-r*bar/R-error)==s.zeros(2)
checks["compatible_gradient_decomposition"]=True

# Rational lower constant used in the theorem.
assert s.Rational(29,20)**3>3
assert (1+2*s.Rational(29,20))**3<s.Integer(60)
checks["coercivity_constant"]={
 "exact":"mu / (1+2*3^(1/3))^3",
 "rational_lower":"mu/60",
 "G_rational_lower":"1/20"}

# Laurent-polynomial integration of the explicit resonant example.
zx,zy=s.symbols("zx zy",nonzero=True)
I=s.I
sx,cx=(zx-zx**-1)/(2*I),(zx+zx**-1)/2
c2y=(zy**2+zy**-2)/2
s2y=(zy**2-zy**-2)/(2*I)
f=1+sx/4
fy=1+c2y/3
rr=f*fy
rrx=cx*fy/4
rry=-2*f*s2y/3
gprime=cx/5
gsecond=-sx/5

def mean(expr):
 total=0
 for term in s.Add.make_args(s.expand(expr)):
  powers=term.as_powers_dict()
  if powers.get(zx,0)==0 and powers.get(zy,0)==0:
   total+=term
 return s.simplify(total)

cf=mean(fy**4)
sigma=cf*f**4
old_cancel=mean(sigma*gsecond)
assert cf==s.Rational(289,216)
assert old_cancel==-s.Rational(19363,138240)
energy=mean(G.subs({a:rrx,b:rry,c:rr*gprime,d:rr},simultaneous=True))
norm4=mean((rrx**2+rry**2+rr**2*(gprime**2+1))**2)
energy_bar=cf*mean(G.subs({a:cx/4,b:0,c:f*gprime,d:f},simultaneous=True))
remainder=mean(f**4)*mean((-2*s2y/3)**4)
assert energy-energy_bar>=remainder  # mu_G/3=1
assert energy>norm4/20>0
checks["exact_example"]={
 "conditional_density_factor":str(cf),
 "old_curvature_cancellation":str(old_cancel),
 "zero_background_G_energy":str(energy),
 "gradient_fourth_norm":str(norm4),
 "density_averaging_remainder":str(remainder),
 "actual_energy_minus_averaged_energy":str(energy-energy_bar),
 "energy_to_norm_ratio":str(energy/norm4),
 "scope":"Analytic all-background transfer uses antipodal symmetry and Fourier LH"}

# An exact failure of constant-reference pointwise dual positivity.
# theta=y+(1/2)sin(2x), at 2x=pi/4: K=(1/sqrt(2),1),
# div(h(K)*(K2,-K1))=29/1 with G's h; g_1=683/96-29/4.
G_phase_rank_one=3*(1+s.Rational(1,2))**2+s.Rational(35,24)*s.Rational(1,4)
constant_reference_residual=G_phase_rank_one-s.Rational(29,4)
assert constant_reference_residual==-s.Rational(13,96)
checks["constant_reference_flux_failure"]={
 "phase":"theta=y+(1/2)sin(2x)",
 "evaluation":"2x=pi/4",
 "g_sigma1":str(constant_reference_residual),
 "scope":"Negative local residual; theorem still gives positive complete action for every amplitude"}

out={"status":"PASS","groups":len(checks),"checks":checks,
     "scope":"Exact bounded algebra; analytic continuum theorem is in SHEAR_DENSITY_AVERAGING.md"}
(ROOT/"exact_shear_checks.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
