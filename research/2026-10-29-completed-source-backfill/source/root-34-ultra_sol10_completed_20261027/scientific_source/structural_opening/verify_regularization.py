#!/usr/bin/env python3
"""Exact algebra for the smooth near-graph regularization and error barrier.

The accepted global support certificate and its scientific review are inputs.
This replay verifies new identities/constants, not that earlier certificate.
"""
from pathlib import Path
import json,time
import sympy as s

start=time.perf_counter();OUT=Path(__file__).resolve().parent
a,b,c,d,t=s.symbols('a b c d t',real=True)
A=s.Matrix([a,b,c,d]);Amat=s.Matrix([[a,b],[c,d]])
u,v,w,q=a*a+c*c,b*b+d*d,a*b+c*d,a*d-b*c
T=u+v;x,y,z=u-v,2*w,2*q
p0=s.Rational(55220381,10000000000)
p2=s.Rational(114430029,625000000)
p3=s.Rational(-801761987,5000000000)
L0=s.Rational(118849817,4000000000)
F=s.expand(p0*(u*u+v*v)+p2*u*v+p3*w*w+L0*q*(u-v))
p=(s.Rational(6222019,200000000)*x**3
   +s.Rational(1686519911,10000000000)*x*x*z
   +s.Rational(81172813,2000000000)*x*z*z
   +s.Rational(1726116771,10000000000)*z**3
   +s.Rational(128626163,5000000000)*x*y*y
   +s.Rational(373321239,2000000000)*y*y*z)
P=sum(abs(cc) for cc in s.Poly(p,*A).coeffs())
assert P==s.Rational(1976430361,156250000)
delta=s.Rational(1,2400000)
epsilon=s.Rational(1,100)
sigma=s.factor(epsilon/(2*P));Lip=10*P
M=s.factor(2*Lip*Lip/delta)
gap=min(epsilon/2,delta/8,M/4)
assert gap==s.Rational(1,19200000)>0
k=p/(T+sigma)**2
for aa in A:
    expected=s.diff(p,aa)/(T+sigma)**2-4*p*aa/(T+sigma)**3
    assert s.cancel(s.diff(k,aa)-expected)==0

# Scalar denominator-shift error certificate, valid for all U>=0,Sig>0.
U,Sig=s.symbols('U Sig',nonnegative=True)
scalar_error=Sig*U*(2*U+Sig)/(U+Sig)**2
positive_slack=Sig**2*(3*U+2*Sig)/(U+Sig)**2
assert s.factor(2*Sig-scalar_error-positive_slack)==0

# Literal tangent identities for the rational normal extension.
ss=s.symbols('ss',real=True)
W=F+epsilon*T
h=W+k*(ss-q)+M*(ss-q)**2
cof=s.Matrix([d,-c,-b,a])
for ii,aa in enumerate(A):
    graph_derivative=s.diff(h,aa).subs(ss,q)
    assert s.cancel(graph_derivative-s.diff(W,aa)+k*cof[ii])==0
assert s.cancel(s.diff(h,ss).subs(ss,q)-k)==0
assert s.cancel(h.subs(ss,q)-W)==0

# Graph-Hessian Schur formula, proved as an identity for arbitrary jets.
vv=s.Matrix(s.symbols('v0:4'))
cc=s.Matrix(s.symbols('c0:4'))
mm=s.symbols('mm',positive=True)
hh=s.Matrix(4,4,s.symbols('h0:16'))
bb=hh-vv*cc.T-cc*vv.T+2*mm*cc*cc.T
bs=vv-2*mm*cc
assert s.simplify(bb-bs*bs.T/(2*mm)-(hh-vv*vv.T/(2*mm)))==s.zeros(4)
assert s.factor(2*delta-Lip*Lip/(2*M))==7*delta/4

# Exact planar identities behind h-ell and the global distance estimate.
X=s.Matrix(2,2,s.symbols('X0:4',real=True))
cof_pair=(cof.T*s.Matrix(list(X)))[0]
assert s.expand((Amat+X).det()-q-cof_pair-X.det())==0
assert s.expand(sum(zz*zz for zz in cof)-T)==0
Xnorm=sum(zz*zz for zz in X)
assert s.expand(Xnorm*Xnorm-4*X.det()**2-(
    (X[0,0]-X[1,1])**2+(X[0,1]+X[1,0])**2)*(
    (X[0,0]+X[1,1])**2+(X[0,1]-X[1,0])**2))==0

# Finite stencil: no derivative closeness between the model and F is used.
I=s.Matrix([1,0,0,1]);E=s.Matrix([1,0,0,0]);D=s.Matrix([-1,0,0,1])
def at(poly,B):return s.expand(poly.subs(dict(zip(A,B)),simultaneous=True))
def stencil(poly):
    return s.expand(at(poly,I+t*D)+at(poly,I-t*D)-2*at(poly,I)
                    +2*at(poly,E+t*D)+2*at(poly,E-t*D)-4*at(poly,E))
g0=L0-4*p0;f0=at(F,D)
assert g0==s.Rational(152486037,20000000000)
assert f0==s.Rational(970660613,5000000000)
assert stencil(q*q)==6*t**4
assert stencil(F)==-12*g0*t*t+6*f0*t**4
den=(sum(zz*zz for zz in I+t*D)**2+sum(zz*zz for zz in I-t*D)**2
     +2*sum(zz*zz for zz in I)**2
     +2*sum(zz*zz for zz in E+t*D)**2+2*sum(zz*zz for zz in E-t*D)**2
     +4*sum(zz*zz for zz in E)**2)
assert s.expand(den-24*(1+t*t)**2)==0
xx,gg,ff=s.symbols('xx gg ff',positive=True)
ratio=(2*gg*xx-ff*xx*xx)/(4*(1+xx)**2)
assert s.factor(s.diff(ratio,xx)-(gg-(gg+ff)*xx)/(2*(1+xx)**3))==0
assert s.factor(ratio.subs(xx,gg/(gg+ff))-gg**2/(4*(2*gg+ff)))==0
optimal_x=s.factor(g0/(g0+f0))
floor=s.factor(g0*g0/(4*(2*g0+f0)))
assert optimal_x==s.Rational(152486037,4035128489)
assert floor==s.Rational(23251991479965369,335009162080000000000)>0

# Affine minors shift transports the germ statement to any prescribed base.
Star=s.Matrix(2,2,s.symbols('S0:4',real=True))
Starcof=s.Matrix([Star[1,1],-Star[1,0],-Star[0,1],Star[0,0]])
assert s.expand((Amat-Star).det()-q+(Starcof.T*A)[0]-Star.det())==0

heat_path=OUT/'HEAT_DIAGNOSTIC.json'
heat=json.loads(heat_path.read_text())
best=min(heat['runs'],key=lambda rr:rr['objective'])
result={'status':'EXACT_NEW_ALGEBRA_PASS',
 'accepted_strict_support_delta':str(delta),'P':str(P),'Lipschitz_radial_constant':str(Lip),
 'example_epsilon':str(epsilon),'example_sigma':str(sigma),
 'normal_extension_M':str(M),'global_graph_tangent_gap_c':str(gap),
 'graph_Schur_lower':'epsilon I+(7 delta/4)|A|^2 I',
 'selector_denominator_shift_error_identity':'PASS',
 'smooth_graph_tangent_and_Schur_identities':'PASS',
 'finite_stencil_F':str(stencil(F)),'finite_stencil_det_squared':'6*t^4',
 'stencil_absolute_error_denominator':'24*(1+t^2)^2',
 'optimized_t_squared':str(optimal_x),'relative_quartic_error_floor':str(floor),
 'relative_quartic_error_floor_decimal':float(floor),
 'affine_minors_shift':'PASS',
 'stable_tangent_lemma_scope':'analytic proof in PROOF.md; not replaced by this replay',
 'compatible_heat_diagnostic_runs':len(heat['runs']),
 'compatible_heat_diagnostic_best_normalized':best['objective'],
 'new_nonPC_target_QC':'UNKNOWN',
 'runtime_seconds':time.perf_counter()-start}
(OUT/'EXACT_REGULARIZATION_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
