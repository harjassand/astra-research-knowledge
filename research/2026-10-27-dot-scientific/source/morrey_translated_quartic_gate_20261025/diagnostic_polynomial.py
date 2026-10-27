import sympy as s,json
from fractions import Fraction
m0=json.load(open('morrey_translated_quartic_gate_20261025/diagnostic_moments.json'))
a=s.symbols('a'); get=lambda v:s.Rational(str(v)); sig=get(m0['s']); b=s.Rational(99,200)
m=3*b/2-25*sig/4
M=s.Matrix([[b/2-9*sig/4,3*sig],[3*sig,b-4*sig]])
c=s.Matrix([15*sig/4,b-5*sig])
m1=get(m0['m1']);m2=get(m0['m2']);m3=s.Matrix(list(map(get,m0['m3'])));m4=s.Matrix(list(map(get,m0['m4'])))
A4=get(m0['A4'])-s.Rational(81,22400);B4=get(m0['B4'])-s.Rational(51,22400);C4=get(m0['C4'])-s.Rational(57,22400)
al=6*a*a+8*a+2;be=12*(1-a*a);ga=6*a*a-8*a+2
k=al*A4+be*B4+ga*C4
L=(3*a+1)*m1+3*(1-a)*m2
N=3*(1+a)*m3-(3*a-1)*m4
E=2*m*m*s.eye(2)-m*(3*a-1)*M-3*(1-a)*c*c.T
v=m*N-L*c
P=s.Poly(s.expand((3*m*k-2*L**2)*E.det()-6*(1-a)*(v.T*E.adjugate()*v)[0]),a)
t=s.symbols('t');pt=s.Poly(P.as_expr().subs(a,2*t-1),t);co=[pt.nth(i) for i in range(5)]
bc=[sum(co[i]*s.binomial(j,i)/s.binomial(4,i) for i in range(j+1)) for j in range(5)]
print('P degree',P.degree(),'Bernstein',list(map(float,bc)))
print('E-1 evals',[float(x) for x in E.subs(a,-1).eigenvals()]);print('E1 evals',[float(x) for x in E.subs(a,1).eigenvals()]);print('Pmonomial',list(map(float,co)))
