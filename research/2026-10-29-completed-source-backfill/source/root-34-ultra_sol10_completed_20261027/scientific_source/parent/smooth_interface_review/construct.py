"""Independent literal stencil replay and explicit strong-convex tube bounds."""
import json, math
from fractions import Fraction as F
from pathlib import Path
import sympy as s
OUT=Path(__file__).resolve().parent
a,b,c,d,t=s.symbols('a b c d t',real=True)
variables=(a,b,c,d)
u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
x=u-v;y=2*w;z=2*q
energy=s.Rational(55220381,10**10)*(u*u+v*v)+s.Rational(114430029,625000000)*u*v-s.Rational(801761987,5000000000)*w*w+s.Rational(118849817,4000000000)*q*(u-v)
numerator=s.Rational(6222019,200000000)*x**3+s.Rational(1686519911,10**10)*x*x*z+s.Rational(81172813,2000000000)*x*z*z+s.Rational(1726116771,10**10)*z**3+s.Rational(128626163,5000000000)*x*y*y+s.Rational(373321239,2000000000)*y*y*z
def frac(x): return F(int(s.numer(x)),int(s.denom(x)))
C=sum(abs(frac(cc)) for cc in s.Poly(energy,*variables).coeffs())
P=sum(abs(frac(cc)) for cc in s.Poly(numerator,*variables).coeffs())
assert C==F(2535570311,2500000000)
assert P==F(1976430361,156250000)
def at(p,A):return s.expand(p.subs(dict(zip(variables,A)),simultaneous=True))
I=(1,0,0,1);E=(1,0,0,0);D=(-1,0,0,1)
def shift(A,sgn):return tuple(A[j]+sgn*t*D[j] for j in range(4))
def stencil(p):return s.expand(at(p,shift(I,1))+at(p,shift(I,-1))-2*at(p,I)+2*at(p,shift(E,1))+2*at(p,shift(E,-1))-4*at(p,E))
g0=F(152486037,20000000000);f0=F(970660613,5000000000)
assert stencil(energy)==s.Rational(-12*g0.numerator,g0.denominator)*t*t+s.Rational(6*f0.numerator,f0.denominator)*t**4
assert stencil(q*q)==6*t**4
eta=g0*g0/(4*(2*g0+f0))
assert eta==F(23251991479965369,335009162080000000000)

delta=F(1,2400000);epsilon=F(1,100);sigma=epsilon/(2*P)
L=10*P;M=2*L*L/delta
gap=min(epsilon/2,delta/8,M/4)
kappa=gap/2
# k=p/(T+sigma)^2 has ||D^2 k||<=106P and
# ||D^3 k||<=1248P/sqrt(sigma) globally. Use integer upper sqrt bound.
inv_sqrt=1
while inv_sqrt*inv_sqrt*sigma<1:inv_sqrt+=1
K2=106*P;K3=1248*P*inv_sqrt
rows=[]
for R in [F(1),F(10),F(100)]:
    bnd=R+1;normal=R+F(3,2);gradient=R+2
    K0=P*bnd*bnd;K1=L*bnd
    H2=12*C*bnd*bnd+2*epsilon+normal*K2+2*K1*gradient+K0+2*M*(gradient*gradient+normal)
    H3=24*C*bnd+normal*K3+3*K2*gradient+3*K1+6*M*gradient
    # htilde=h-kappa|z|^2, graph gap=gap/2 and graph Hessian>=gap I.
    K=H2+gap
    r=min(F(1,2),gap/(4*H3))
    tube=min(r/4,gap*r/(16*K))
    assert 2*r*H3 <= gap/2
    assert K*tube/r <= gap/16
    rows.append({'matrix_norm_limit':str(R),'Hessian_norm_upper_in_unit_graph_ball':str(H2),
                 'third_derivative_upper_in_unit_graph_ball':str(H3),
                 'strongly_convex_graph_tube_radius':str(tube),
                 'display_only_radius':float(tube)})
result={'status':'INDEPENDENT_LITERAL_REPLAY_AND_ROOT_CONSTRUCTION',
        'coefficient_l1_F':str(C),'coefficient_l1_p6':str(P),
        'stencil_error_floor':str(eta),'epsilon':str(epsilon),'sigma':str(sigma),
        'M':str(M),'graph_gap_c':str(gap),'kappa':str(kappa),
        'global_strong_convexity_modulus':str(2*kappa),
        'second_derivative_selector_bound':str(K2),'third_derivative_selector_bound':str(K3),
        'uniform_tubes':rows,
        'scope':'Analytic arguments reviewed separately. Conservative tubes are extremely small, not practical numerical conditioning or global envelope complexity guarantees.'}
(OUT/'EXACT_CONSTRUCTION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
