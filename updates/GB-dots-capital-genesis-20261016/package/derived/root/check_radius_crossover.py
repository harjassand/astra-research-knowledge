"""Exact finite identity checks only; analytic quantifiers are in the proof."""
import json
import sympy as s
r,c,h,z,e=s.symbols('r c h z e', real=True)
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1)
a=(I+r*(c*Z+h*X))/2;b=(I+r*(c*Z-h*X))/2
M=(a.inv()+b.inv())/2
raw=s.factor(1-s.trace(M.inv()))
assert s.factor((raw-r*r*h*h/(1-r*r*c*c)).subs(h*h,1-c*c))==0
A=1-r*r*c*c; B=r*r*(1-c*c); t=s.symbols('t',real=True)
f=B*A*(1-t)/(A-B*t)
assert s.factor(s.diff(f,t)+B*A*(1-r*r)/(A-B*t)**2)==0
v=s.Rational(99,100); co=s.Rational(4,5);si=s.Rational(3,5)
assert v*v*si*si/(1-v*v*co*co)==s.Rational(88209,93184)
print(json.dumps({'checks':3,'complete_example':'88209/93184','ordinary_example':str(v*v*si*si),'scope':'Exact algebra; no physical/calibration/priority certification.'},indent=2))
