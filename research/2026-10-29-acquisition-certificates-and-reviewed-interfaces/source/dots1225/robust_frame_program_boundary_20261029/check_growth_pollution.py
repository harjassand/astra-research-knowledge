"""Exact two-class absorption law for IID labels with one noisy dark eigenvalue.
No Monte Carlo; no source-channel-to-label perturbation equivalence assumed.
"""
import sympy as s,json
from pathlib import Path
x=s.symbols('x',positive=True); a=(1-x)/8
v=s.Matrix([1-x,x]);expected=0;rows=[]
for k in range(1,8):
 S=s.Matrix([[(8-k)*a/(k+1),0],[x/(k+1),(9-k)*a/(k+1)]])
 f01=k*x/(k+1)**2;f10=(9-k)*a/(k+1)**2
 F=s.Matrix([[1-sum(S[:,0])-f01,f10],[f01,1-sum(S[:,1])-f10]])
 occupation=(s.eye(2)-F).inv()*v
 expected=s.factor(expected+sum(occupation))
 v=(S*occupation).applyfunc(s.factor)
 assert s.factor(sum(v)-1)==0
 rows.append(dict(k=k+1,pollution=str(v[1])))
res=dict(scope='IID isotropic almost-dark label state, ideal exact growth controls, no finite cap; expected count counts normalized minus records',infidelity=str(s.factor(v[1])),small_x_slope=str(s.limit(v[1]/x,x,0)),expected_minus_records=str(s.factor(1+expected)),rows=rows,values=[dict(epsilon=float(t),infidelity=float(v[1].subs(x,t)),expected_minus=float((1+expected).subs(x,t)),one_shot_infidelity=float((8*t/(a+8*t)).subs(x,t))) for t in [s.Rational(1,1000000),s.Rational(1,10000),s.Rational(1,1000),s.Rational(1,100),s.Rational(1,9)]])
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
