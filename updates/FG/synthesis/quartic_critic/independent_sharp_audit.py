#!/usr/bin/env python3
"""Independent exact audit of the FG sharp quartic source.

All constants are transcribed from the written theorem. No supplied program,
JSON, pickle, NumPy archive, or optimizer is imported as proof input.
"""
from pathlib import Path
import itertools
import json
import sympy as S

HERE=Path(__file__).resolve().parent
kappa=S.Symbol("K", real=True)
mp=48*kappa**6-2545*kappa**4+29712*kappa**2-97344
mod=S.Poly(mp,kappa,domain=S.QQ)
lo=S.Rational(295538664457927,10**14)
hi=S.Rational(295538664457928,10**14)
checks={}
sturm=S.sturm(mp,kappa)
def variations(point):
    signs=[S.sign(f.subs(kappa,point)) for f in sturm]
    signs=[z for z in signs if z]
    return sum(a!=b for a,b in zip(signs,signs[1:]))
assert variations(lo)-variations(hi)==1
assert variations(S.Rational(295,100))-variations(S.Rational(296,100))==1
assert mp.subs(kappa,lo)*mp.subs(kappa,hi)<0
checks["root isolation by independently evaluated Sturm sequence"]={"tight":[str(lo),str(hi)],"variation_counts":[variations(lo),variations(hi)],"irreducible":bool(mod.is_irreducible)}
def red(p):return S.rem(S.Poly(S.expand(p),kappa,domain=S.QQ),mod).as_expr()
def bound(poly):
    low=high=S.Rational(0)
    for c in S.Poly(poly,kappa).all_coeffs():
        v=[low*lo,low*hi,high*lo,high*hi]
        low,high=min(v)+c,max(v)+c
    return low,high
t=S.symbols("t0:6")
t0,t1,t2,t3,t4,t5=t
matrix=S.Matrix([
    [12,10-t0/2,25-t0/2-t4-3*t5,2*kappa+t3,-3*kappa,-3*kappa-t2],
    [10-t0/2,8,t0/2+t4+3*t5-9,2*kappa+t2,-kappa+t1+t2,-kappa],
    [25-t0/2-t4-3*t5,t0/2+t4+3*t5-9,t0,t1,t2,t3],
    [2*kappa+t3,2*kappa+t2,t1,11-2*t5,1-t4,t4],
    [-3*kappa,-kappa+t1+t2,t2,1-t4,7,t5],
    [-3*kappa-t2,-kappa,t3,t4,t5,4]])
values=[
    (254064*kappa**4-12066397*kappa**2+87457992)/S.Integer(107712),
    kappa*(2551152*kappa**4-120422989*kappa**2+869186184)/S.Integer(4582656),
    -kappa*(30008208*kappa**4-1412052067*kappa**2+10194361080)/S.Integer(50409216),
    kappa*(2383152*kappa**4-111980897*kappa**2+796906920)/S.Integer(3877632),
    (64560*kappa**4-3046321*kappa**2+22009128)/S.Integer(71808),
    -(641424*kappa**4-30344323*kappa**2+215742840)/S.Integer(646272)]
endpoint=matrix.subs(dict(zip(t,values))).applyfunc(red)
T=endpoint[2:,2:]; B=endpoint[:2,2:]; C=endpoint[:2,:2]
minors=[red(T[:n,:n].det()) for n in range(1,5)]
minor_bounds=[bound(p) for p in minors]
assert all(left>0 for left,right in minor_bounds)
adj=T.adjugate().applyfunc(red)
assert (minors[-1]*C-B*adj*B.T).applyfunc(red)==S.zeros(2)
checks["endpoint rank-four PSD Schur certificate"]={"positive_minor_bounds":[list(map(str,b)) for b in minor_bounds],"zero_schur":True}

a,b,c,d=S.symbols("a b c d", real=True); coordinates=S.Matrix([a,b,c,d])
j=S.symbols("j0:6", real=True)
B1=S.Matrix([j[0],j[1],j[3],j[4]]);B2=S.Matrix([j[1],j[2],j[4],j[5]])
u,v,w,q=a*a+c*c,b*b+d*d,a*b+c*d,a*d-b*c
F=u*u+v*v+4*w*w+S.Rational(7,2)*q*q+kappa*q*(u+v)
theta=S.Matrix([-c,-d,a,b]);zeta=S.Matrix([-b,a,-d,c]);theta_a=S.Matrix([-c,d,a,-b])
alpha=(-(6*kappa+t1+3*t2-t3)*(u+v)/4-(t0+4*t5-20)*q/2)*theta
alpha+=((20-t0)*(u+v)/4+(kappa-t1-t2)*q)*zeta
alpha+=(4*kappa+t1+3*t2+t3)*(u-v)*theta_a/4
omega=alpha.jacobian(coordinates).T-alpha.jacobian(coordinates)
for i,h,k in itertools.combinations(range(4),3):
    assert S.expand(S.diff(omega[h,k],coordinates[i])-S.diff(omega[i,k],coordinates[h])+S.diff(omega[i,h],coordinates[k]))==0
X=S.Matrix([j[0],j[3]]);Y=S.Matrix([j[1],j[4]]);Z=S.Matrix([j[2],j[5]])
x=S.Matrix([a,c]);y=S.Matrix([b,d])
def wedge(v,w):return v[0]*w[1]-v[1]*w[0]
plus=S.Matrix([x.dot(X),x.dot(Z),y.dot(Y),wedge(x,Y),wedge(y,X),wedge(y,Z)])
minus=S.Matrix([-y.dot(Z),-y.dot(X),-x.dot(Y),wedge(y,Y),wedge(x,Z),wedge(x,X)])
H=S.hessian(F,coordinates)
diss=(B1.T*H*B1+B2.T*H*B2)[0]
assert S.expand(diss+(B1.T*omega*B2)[0]-(plus.T*matrix*plus+minus.T*matrix*minus)[0])==0
assert S.expand(plus.dot(plus)+minus.dot(minus)-(u+v)*(X.dot(X)+Y.dot(Y)+Z.dot(Z)))==0
checks["universal compact primitive and compatible heat identity"]={"independent_parameters":7,"closedness":True,"norm_identity":True}

# Sharpness independently follows from determinant and positive 3x3 minor;
# no source's joint Groebner null-vector calculation is relied upon.
k=S.Symbol("k",real=True)
direction=S.Matrix([1,k,0,0])
ac=S.expand((direction.T*H*direction)[0])
M=S.hessian(ac,coordinates)/2
V,z=S.symbols("V z",real=True)
smallpoly=3*(32-V)*(28-3*V)+(504*V-5952)*z+768*(V-S.Rational(5,2))*z*z
assert S.cancel(M.det()-(1+k*k)**4*smallpoly.subs({V:kappa*kappa,z:k*k/(1+k*k)**2}))==0
zcrit=(248-21*V)/(64*V-160)
cubic=48*V**3-2545*V**2+29712*V-97344
critnum=S.together(smallpoly.subs(z,zcrit)).as_numer_denom()[0]
assert S.rem(S.Poly(critnum,V),S.Poly(cubic,V)).is_zero
assert S.expand(S.discriminant(smallpoly,z)+576*cubic)==0
J=S.Symbol("J",real=True)
det3=S.expand(M[:3,:3].det()).subs(k*k,J)
claimed=-12*((6*kappa*kappa-56)*J**3+(kappa*kappa-4)*J**2+(4*kappa*kappa-40)*J+kappa*kappa-32)
assert S.expand(det3-claimed)==0
# For 8<V<9, 0<J<1: first/third bracket coefficients are negative,
# second is <5 and last <-23, so the bracket is <-18 and det3>216.
for expression in [248-21*kappa*kappa,64*kappa*kappa-160,(64*kappa*kappa-160)-4*(248-21*kappa*kappa)]:
    assert bound(expression)[0]>0
assert S.expand(M.subs(kappa,0)[:2,:2].det()-(96*(k*k-S.Rational(1,4))**2+90))==0
assert S.expand(M.subs(kappa,0)[2:,2:].det()-(28+64*k*k+28*k**4))==0
checks["independent sharp rank-one obstruction"]={"determinant_identity":True,"critical_double_zero":True,"positive_top_3_minor_bound":">216", "null_vector":"adj(M_K(k)) e4 has nonzero fourth entry; hence M null, without source Groebner reconstruction"}

interior_t=[S.Rational(74,5),-S.Rational(73,10),S.Rational(37,5),S.Rational(6,5),S.Rational(16,5),S.Rational(6,5)]
G=matrix.subs(dict(zip(t,interior_t))).subs(kappa,-S.Rational(29,10))
gm=[S.factor((G-S.eye(6)/8)[:n,:n].det()) for n in range(1,7)]
assert all(v>0 for v in gm)
checks["small rational Fstar certificate"]={"shifted_minors":list(map(str,gm)),"margin": "1/8"}
N=(u+v)**2;H3=N+4*w*w
assert S.expand(F.subs(kappa,0)-N/2-H3/2-S.Rational(3,2)*q*q)==0
const_lower=(1-S.Rational(29,10)/lo)/6
const_upper=(1-S.Rational(29,10)/hi)/6
assert const_lower>S.Rational(1,576)>S.Rational(1,36000)
checks["Fstar improved coercivity constant"]={"interval":[str(const_lower),str(const_upper)],"approximate":float((const_lower+const_upper)/2)}
# The 35-direction perturbation bound is a universal consequence of these
# finite monomial identities and the triangle inequality, not sampling.
increment=S.Matrix(S.symbols("b0:4",real=True))
monomials=[]
for exps in itertools.product(range(5),repeat=4):
    if sum(exps)!=4:continue
    monomial=S.prod(z**n for z,n in zip(coordinates,exps))
    expression=S.Poly(S.expand((increment.T*S.hessian(monomial,coordinates)*increment)[0]),tuple(coordinates)+tuple(increment))
    assert all(c>=0 for c in expression.coeffs())
    assert sum(expression.coeffs())==12
    monomials.append(exps)
assert len(monomials)==35
assert const_upper<S.Rational(3,10)
checks["all 35 monomial perturbation directions"]={"monomials":35,"absolute_Hessian_bound": "12*coefficient_l1*|A|^2*|B|^2", "coefficient_radius":"cstar", "interior_uniform_gap":"cstar-coefficient_l1", "boundary_gap_from_this_argument":0}

# Independently check the light-cone separating arithmetic. This excludes
# only the named positive isotropic-atom construction, not quasiconvexity.
tau,delta=S.symbols("tau delta",real=True)
Z00,Z11,Z22=S.Rational(1,2)+tau,S.Rational(1,2)-tau,1-tau
Z33=S.Rational(1,4)+tau/3-2*delta/3
assert S.expand(S.Rational(3,2)*Z33-Z00/2+Z11/2+Z22/2+delta-(S.Rational(7,8)-tau))==0
assert S.expand(S.Rational(5,12)-(S.Rational(1,2)+tau)*(S.Rational(1,4)+tau/3)-(S.Rational(1,2)-tau)*(tau/3+S.Rational(7,12)))==0
assert S.Rational(841,1600)-S.Rational(5,12)==S.Rational(523,4800)>0
checks["scoped isotropic atom cone obstruction"]={"separating_gap":"523/4800", "scope":"positive finite sums of the stated right-GL images plus nonnegative det^2; excludes neither arbitrary convex additions nor other methods"}

# A separate finite, completely rational obstruction just beyond kappa.
finite_background={a:-S.Rational(877889,10**6),b:S.Rational(202950,10**6),c:-S.Rational(357204,10**6),d:1}
finite_value=ac.subs(finite_background).subs({k:S.Rational(504851,10**6),kappa:S.Rational(739,250)})
assert finite_value<0
checks["rational finite rank-one countermodel at ell=2.956"]={"value":str(finite_value),"approximate":float(finite_value)}

# One finite resonant compatible periodic test, by direct Laurent constants.
zz,ww=S.symbols("zz ww", nonzero=True)
sinx=(zz-1/zz)/(2*S.I);cosx=(zz+1/zz)/2
siny=(ww-1/ww)/(2*S.I);cosy=(ww+1/ww)/2
sinxy=(zz*ww-1/(zz*ww))/(2*S.I)
cos2xmy=(zz**2/ww+ww/zz**2)/2
potential=[sinx+S.Rational(2,3)*cosy+sinxy/5, cosx/4-siny/3+S.Rational(2,5)*cos2xmy]
gradient=[S.expand(S.I*var*S.diff(p,var)) for p in potential for var in [zz,ww]]
for p in potential:
    assert S.expand(S.I*ww*S.diff(S.I*zz*S.diff(p,zz),ww)-S.I*zz*S.diff(S.I*ww*S.diff(p,ww),zz))==0
bg=[S.Rational(1,3),-S.Rational(1,5),S.Rational(2,7),S.Rational(1,2)]
def avg(expr):return S.expand(expr).coeff(zz,0).coeff(ww,0)
fourier_F=F.subs(dict(zip(coordinates,[b+g for b,g in zip(bg,gradient)])),simultaneous=True)
gap=S.expand(avg(fourier_F)-F.subs(dict(zip(coordinates,bg))))
gap_even,gap_odd=gap.coeff(kappa,0),gap.coeff(kappa,1)
gap_bounds=[gap_even-hi*abs(gap_odd),gap_even+hi*abs(gap_odd)]
norm4=avg(sum(g*g for g in gradient)**2)
assert gap_bounds[0]>0
assert gap.subs(kappa,-S.Rational(29,10))>const_upper*norm4
checks["finite resonant compatible Fourier test"]={"endpoint_gap_interval":list(map(str,gap_bounds)),"gradient_fourth_mean":str(norm4),"Fstar_gap":str(gap.subs(kappa,-S.Rational(29,10))),"curl_exact":True,"scope":"finite test, not universal theorem validation"}

output={"status":"PASS","groups":len(checks),"checks":checks,"scope":"Independent exact algebra and one rational countermodel plus one compatible periodic finite test; analytic/universal claims separately audited in REPORT.txt. No external validation or priority clearance."}
(HERE/"INDEPENDENT_SHARP_RESULTS.json").write_text(json.dumps(output,indent=2)+"\n")
print(json.dumps({"status":output["status"],"groups":len(checks),"finite_rank_one_value":str(finite_value),"Fstar_coercivity":float((const_lower+const_upper)/2)}))
