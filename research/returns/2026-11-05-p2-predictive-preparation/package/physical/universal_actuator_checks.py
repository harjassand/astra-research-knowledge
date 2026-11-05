"""Exact checks of the finite smooth actuator constants.

These are algebraic checks, not a physical prototype or numerical validation
of an unknown passive plant.
"""
import json
from pathlib import Path
import sympy as sp

s=sp.symbols('s', real=True)
R=10*s**3-15*s**4+6*s**5
r1=sp.diff(R,s)
r2=sp.diff(r1,s)
r3=sp.diff(r2,s)
assert sp.integrate(r1,(s,0,1))==1
assert sp.factor(r1)==30*s**2*(s-1)**2
assert r1.subs(s,sp.Rational(1,2))==sp.Rational(15,8)
z=(3-sp.sqrt(3))/6
assert sp.simplify(r2.subs(s,z)-10*sp.sqrt(3)/3)==0
assert all(sp.diff(R,s,j).subs(s,0)==0 for j in (0,1,2))
assert R.subs(s,1)==1
assert all(sp.diff(R,s,j).subs(s,1)==0 for j in (1,2))
tv1=sp.Rational(15,4)
tv2=40*sp.sqrt(3)/3
assert sp.simplify(2*r1.subs(s,sp.Rational(1,2))-tv1)==0
assert sp.simplify(4*r2.subs(s,z)-tv2)==0

E,k,mu,f,v=sp.symbols('E k mu f v', positive=True)
assert sp.simplify(f*v-v**2-f**2/4+(v-f/2)**2)==0

data={
 "status":"exact symbolic actuator and energy checks",
 "ramp":"10s^3-15s^4+6s^5",
 "positive_normalized_derivative":True,
 "max_ramp_slope":str(sp.Rational(15,8)),
 "kernel_first_derivative_L1_times_width":str(tv1),
 "kernel_second_derivative_L1_times_width_squared":str(tv2),
 "kernel_mean_delay_divided_by_width":str(sp.integrate(s*r1,(s,0,1))),
 "energy_completion_identity":"f v-v^2 = f^2/4-(v-f/2)^2",
 "hardware_comparison":{
  "moving_viscous_support":"reaction f-v requires a peak-velocity bound",
  "permanent_spring":"reaction f-kx is bounded by F+k sqrt(2E_max/mu)",
  "unknown_stiffness_native_center":"gain cancels if unchanged between acquisition and deployment"
 },
 "scope":"No unknown-plant ODE, random-clock trial, or raw sensor record was simulated."
}
path=Path(__file__).with_name('universal_actuator_checks.json')
path.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
