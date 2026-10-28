from pathlib import Path
import hashlib,json,datetime
import sympy as s
b=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Independent exact finite algebra diagnostic, not proof of infinite memory.
K,d=s.symbols('K d', positive=True)
for H in range(1,12):
 assert s.expand(sum(s.binomial(H,m)*K**(m+1)*d**m for m in range(1,H+1))-K*((1+K*d)**H-1))==0
# Four triangle terms: projection <=2eta+xi and two task comparisons.
e,x,z=s.symbols('eta xi zeta',nonnegative=True)
assert s.expand(2*(2*e+x)+z-(4*e+2*x+z))==0
# Interval inverse residual identity C-Chat=H^-1[(Hz-Hzhat)+(Hhat-H)Chat].
H=s.Matrix([[1,s.Rational(1,6)],[s.Rational(1,6),s.Rational(1,18)]])
Hhat=H+s.Matrix([[0,s.Rational(1,10000)],[s.Rational(-1,20000),s.Rational(1,30000)]])
Hz=s.Matrix([[s.Rational(1,3),s.Rational(1,12)],[s.Rational(1,8),s.Rational(1,30)]])
Hzhat=Hz+s.ones(2,2)/100000
Ch=Hhat.inv()*Hzhat
assert H.inv()*Hz-Ch==H.inv()*((Hz-Hzhat)+(Hhat-H)*Ch)
result={'status':'PASS_EXACT_ALGEBRA_DIAGNOSTICS','dyson_horizons':11,'interval_residual_identity':True,'projection_regret_constants':True,'limitations':'Finite algebra diagnostics only. Infinite trace-class claim is received by analytic argument and governing primitive, not numerical truncation. No new source calls or complete endpoint compiler executed.'}
(b/'signed_trace_class_synthesis_independent_check.json').write_text(json.dumps(result,indent=2)+'\n')
