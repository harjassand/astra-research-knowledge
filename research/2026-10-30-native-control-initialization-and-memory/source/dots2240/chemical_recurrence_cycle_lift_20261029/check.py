from fractions import Fraction as F
from math import factorial
import json

q=[F(1),F(1,2),F(1,3)]
rates=[1,2,3]
layer_checks=0
for z in range(100):
    flux=[q[y]/factorial(z+y)*rates[y]*F(factorial(z+y),factorial(z)) for y in range(3)]
    assert flux[0]==flux[1]==flux[2]
    layer_checks+=1
assert q[1]**2 != q[0]*q[2]
gate_checks=0
for eps in [F(1,1000),F(1,10),F(1),F(3),F(1000)]:
    for M in range(1,12):
        for B in range(M+1):
            C=M-B
            for A in range(80):
                drift=eps*C-eps*A*C-eps*A*B+eps*B
                assert drift==eps*M*(1-A)
                gate_checks+=1
pi=lambda a: F(a+1,factorial(a)**2)
for a in range(100):
    assert pi(a)*F(1,a+1)==pi(a+1)*F((a+1)**2,a+2)
out={'exact_layer_flux_checks':layer_checks,'gluing_conflict':{'two_steps':'1/4','direct':'1/3'},'exact_gate_drift_checks':gate_checks,'averaged_stationary_ratio_checks':100,'scope':'finite rational diagnostics; analytic identities and limitations in RESULTS.md; no universal recurrence proof'}
print(json.dumps(out,indent=2))
