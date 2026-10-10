"""Exact symbolic identities and separately labelled numerical checks.
No floating point result is used as a proof of the all-dimension statements.
"""
import json
from pathlib import Path
import sympy as s
from scipy.integrate import quad
from scipy.special import gammaln
from math import exp, log, pi, sqrt

l1,l2=s.symbols('l1 l2', real=True)
p=4
I=s.eye(p); O=s.zeros(p)
b1=s.Matrix([1,0,0,0]); b2=s.Matrix([0,1,0,0])
A1=I.row_join(O).row_join(b1)
A2=O.row_join(I).row_join(b2)
Al=l1*A1+l2*A2
r2=l1*l1+l2*l2
K=I+Al*Al.T
expected=(1+r2)**3*(1+2*r2)
assert s.expand(K.det()-expected)==0
x=s.Matrix(s.symbols('x0:4', real=True))
F=s.Matrix.vstack(x.T*A1,x.T*A2)
S=F*F.T
rx2=(x.T*x)[0]
v=s.Matrix([x[0],x[1]])
assert S==rx2*s.eye(2)+v*v.T
assert s.simplify(S.det()-rx2*(rx2+(v.T*v)[0]))==0
u=s.symbols('u', nonnegative=True)
angle_integral=s.integrate((1+u)**(-s.Rational(1,2)),(u,0,1))
assert s.simplify(angle_integral-2*(s.sqrt(2)-1))==0

# Verify one affine completed-square identity by exact rational arithmetic.
lam=s.Matrix([s.Rational(2,3),s.Rational(-3,5)])
A=lam[0]*A1+lam[1]*A2
c=s.Matrix([1,-2,0,0,0,1,0,0,2])*lam[0]+s.Matrix([0,1,1,0,-1,0,0,0,1])*lam[1]
Kr=I+A*A.T
assert s.simplify((c.T*(s.eye(9)-A.T*Kr.inv()*A)*c)[0]-(c.T*(s.eye(9)+A.T*A).inv()*c)[0])==0

# Independent continuous quadrature: radial dual integral divided by t envelope.
f=lambda r: 2*pi*r*(1+r*r)**(-1.5)*(1+2*r*r)**(-.5)
dual_integral,err=quad(f,0,float('inf'),epsabs=1e-11,epsrel=1e-11)
accept=dual_integral/pi

# A deliberately poor but valid t envelope: A_lambda A_lambda^T=
# kappa^2 ||lambda||^2 I gives success kappa^{-m}; this is repairable by rescaling.
res={
 'symbolic_identities_passed':4,
 'coupled_example':{
  'dimensions':{'m':2,'p':4,'n':9},
  'A1':str(A1),'A2':str(A2),
  'det_I_A_lambda_A_lambda_T':str(s.factor(K.det())),
  'S_identity':'||x||^2 I_2 + (x0,x1)(x0,x1)^T',
  'exact_base_normalization_W0':'sqrt(2)-1',
  'exact_acceptance':'2*(sqrt(2)-1)',
  'acceptance_quadrature':accept,
  'quadrature_error_bound_reported_by_quad':err,
  'exact_expected_trials':'(sqrt(2)+1)/2',
  'nonlinear_target':'g_i=x_i*(x0*x1)/(1+(x0*x1)^2), i=0,1',
  'nonlinear_energy_bound':'g^T S^{-1} g <= 1/8',
  'nonlinear_acceptance_lower_bound':2*(sqrt(2)-1)*exp(-1/16)
 },
 'envelope_scaling_failure':[
  {'m':m,'kappa':2,'success_using_only_s_1_floor':2.0**(-m)} for m in [2,10,50,100]
 ],
 'jensen_bound_when_m_even_R_4m_squared':[
  {'m':m,'R':4*m*m,'expected_trials_upper_bound':exp(sum(-log(1-2*j/(4*m*m)) for j in range(1,m//2+1)))} for m in [2,10,50,100]
 ]
}
out=Path(__file__).with_name('EXACT_AND_NUMERICAL_CHECKS.json')
out.write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
