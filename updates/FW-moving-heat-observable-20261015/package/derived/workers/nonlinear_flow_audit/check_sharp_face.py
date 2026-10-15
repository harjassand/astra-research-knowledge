#!/usr/bin/env python3
"""Independent contact-face/extremality algebra, not the Gram certificate audit."""
from pathlib import Path
import json
import sympy as s

ROOT = Path(__file__).resolve().parent
a,b,c,d,n,m,r,eps = s.symbols('a b c d n m r eps', real=True)
x = s.Matrix([a,b,c,d])
p = s.Matrix(s.symbols('p0:9'))
u,v,w,j = a*a+c*c,b*b+d*d,a*b+c*d,a*d-b*c
H = (u+v-2*j)**2
basis = [u*u,v*v,u*v,w*w,u*w,v*w,u*j,v*j,w*j]
G = sum(p[i]*basis[i] for i in range(9))
R = s.Matrix([n,m,0,0])
Q = (R.T*s.hessian(G,x)*R)[0]
at = {a:1,b:0,c:0,d:1,n:0,m:1}
equations = [Q.subs(at)] + [s.diff(Q,xx).subs(at) for xx in (a,b,c,d,n,m)]
L = s.Matrix([[s.diff(eq,pp) for pp in p] for eq in equations])
assert L.rank() == 5
alpha,beta,gamma,delta = s.symbols('alpha beta gamma delta',real=True)
face = s.Matrix([alpha+beta,alpha,6*alpha+gamma,-4*alpha-gamma,
                 0,0,-4*alpha+delta,-4*alpha,0])
assert L*face == s.zeros(7,1)
T = face.jacobian([alpha,beta,gamma,delta])
assert T.rank() == 4
# The kernel is exactly this face because 9-5=4.

astar = 3*r/(8*(r+2))
bstar = r*(r-1)/6
M1 = s.Matrix([[6*beta+delta,delta],[delta,gamma]])
M2 = s.Matrix([[8*alpha,delta],[delta,2*beta+delta]])
star = {alpha:astar,beta:bstar,gamma:1,delta:r}
M1star, M2star = s.simplify(M1.subs(star)), s.simplify(M2.subs(star))
assert M1star == s.Matrix([[r*r,r],[r,1]])
assert M2star == s.Matrix([[3*r/(r+2),r],[r,r*(r+2)/3]])
assert s.simplify(M1star.det()) == s.simplify(M2star.det()) == 0
assert M1star.rank() == M2star.rank() == 1
F = astar*H+bstar*u*u+j*j+r*u*j
A0 = {a:0,b:(2*r+1)/3,c:1,d:0}
subH = s.factor(s.diff(F-eps*H,a,2).subs(A0))
assert s.simplify(subH+16*(r+2)**2*eps/9) == 0
h,k = s.symbols('h k')
averaged_h4 = (h**4+k**4+((h+k)**4+(h-k)**4)/4)/4
assert s.expand(averaged_h4-s.Rational(3,8)*(h*h+k*k)**2) == 0

receipt = {
  'status':'EXACT_PASS',
  'generic_invariant_quartic_dimension':9,
  'contact_criticality_matrix_shape':list(L.shape),
  'contact_criticality_rank':5,
  'contact_face_dimension':4,
  'contact_face_basis':['H','u^2','j^2','u j'],
  'sharp_M1':str(M1star), 'sharp_M2':str(M2star),
  'sharp_rank_pair':[1,1],
  'H_subtraction_acoustic_value':str(subH),
  'rotational_average_h4':'3 H / 8',
  'analytic_scope':'Together with the verified four-coefficient ROC PSD criterion, proves extremality in the full left-SO(2)-invariant ROC cone; no unrestricted noninvariant or exposed-ray claim.'
}
(ROOT/'sharp_face_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
