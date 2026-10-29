"""Exact small hidden-process construction; no native or physical claim."""
from pathlib import Path
import json,time
import sympy as s
import numpy as np
from scipy.linalg import expm

tic=time.perf_counter()
t=s.symbols('t',positive=True)
p=s.Matrix([[s.Rational(1,2),s.Rational(1,2)]])
one=s.ones(2,1)
H1=s.Matrix([[-1,1],[0,-2]])
Hhalf=s.Matrix([[-1,1],[0,-1]])
assert p*H1 == -p
baseline=s.simplify((p*(H1*t).exp()*one)[0])
half=s.simplify((p*(Hhalf*t).exp()*one)[0])
assert s.simplify(baseline-s.exp(-t))==0
assert s.simplify(half-s.exp(-t)*(1+t/2))==0
eventA=1-s.exp(-s.Rational(1,2))
eventB=1-s.Rational(3,2)*s.exp(-1)
lower=(1-s.exp(-1))/2
upper=s.Rational(1,2)
z,b,u=s.symbols('z b u',positive=True)
Q=s.Matrix([[-2,2,0],[u/2,-u,u/2],[0,0,0]])
D=s.diag(0,1,2)
reset=s.Matrix([[0,1,0]])
assert Q*s.ones(3,1)==s.zeros(3,1)
H=Q-b*D
L=s.factor((reset*(z*s.eye(3)-H).inv()*s.ones(3,1))[0])
delta=s.factor(L-1/(z+b))
expected=b*u*(b-1)/((z+b)*(z+2*b)*(z*z+(2+u+b)*z+u+2*b))
assert s.simplify(delta-expected)==0
assert s.simplify(L.subs(b,1)-1/(z+1))==0
third=(reset*H**3*s.ones(3,1))[0]
assert s.simplify(third-(-b**3-u*b*(1-b)))==0
native_abstract_H=np.array(H.subs({u:2,b:s.Rational(1,2)}),float)
strong_event=1-float(np.array([0.,1.,0.])@expm(native_abstract_H)@np.ones(3))
u1_H=np.array(H.subs({u:1,b:s.Rational(1,2)}),float)
u1_event=1-float(np.array([0.,1.,0.])@expm(u1_H)@np.ones(3))
assert s.simplify(L.subs(u,2)-L.subs(u,1))!=0
out=dict(status='EXACT ABSTRACT COUNTERMODEL; NOT NATIVE CATALYTIC NO-GO',
    baseline_survival=str(baseline),target_b='1/2',target_horizon='1',
    model_A_event_exact=str(eventA),model_B_event_exact=str(eventB),
    target_difference_exact=str(s.simplify(eventB-eventA)),
    target_difference_float=float(eventB-eventA),
    ordinary_coarse_envelope=[str(lower),str(upper)],
    numeric_envelope=[float(lower),float(upper)],
    target_event_probabilities=[float(eventA),float(eventB)],
    same_known_reset_construction=dict(
        Q_u=str(Q),controlled_D=str(D),reset=str(reset),
        survival_laplace=str(L),difference_from_u0_laplace=str(delta),
        target_third_derivative=str(s.factor(third)),
        b='1/2',u='2',T='1',
        target_event_probabilities=[float(eventA),strong_event],
        target_event_probability_difference=strong_event-float(eventA),
        identical_positive_support_comparison=dict(u_values=[1,2],
            target_event_probabilities=[u1_event,strong_event],
            difference=strong_event-u1_event),
        numerical_scope='binary64 matrix-exponential diagnostic; exact identities and proof give scope'),
    seconds_after_imports=time.perf_counter()-tic,
    review='root internal construction; no independent audit at creation')
Path(__file__).with_name('RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
