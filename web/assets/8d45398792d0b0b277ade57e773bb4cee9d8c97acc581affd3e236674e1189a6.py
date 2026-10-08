"""Exact finite collar normalization check; not a PDE/theorem certificate."""
from fractions import Fraction as F
import json
from pathlib import Path

cases=[]
for numerator in [1,2,3,5,10,30]:
    for denominator in [1,2,3,7,10]:
        alpha=F(numerator,denominator)
        p,q=alpha.numerator,alpha.denominator
        # L=q*log(2), so all needed exponentials are rational powers of 2.
        z=F(1,2**(2*p+q))
        ratio=alpha/(alpha+1)
        A=1/(1+ratio*z)
        B=A*ratio*z
        outer_value=A+B
        inner_derivative=A*alpha*F(1,2**p)-B*(alpha+1)*2**(p+q)
        q_formula=alpha*(1-z)/(1+ratio*z)
        outer_derivative=A*alpha-B*(alpha+1)
        energy=A*A*alpha*(1-z)+B*B*(alpha+1)*(1/z-1)
        assert outer_value==1
        assert inner_derivative==0
        assert q_formula==outer_derivative==energy
        assert F(0)<=alpha-q_formula<=2*alpha*z
        cases.append({"alpha":str(alpha),"L":"%d*log(2)"%q,"q":str(q_formula),"checks":"all exact equalities and inequalities passed"})

round_sums=[]
for degree in [1,2,10,100,1000]:
    actual=sum((2*l+1)*l for l in range(degree+1))
    closed=F(degree*(degree+1)*(4*degree+5),6)
    assert actual==closed
    p=(degree+1)**2
    round_sums.append({"degree":degree,"p":p,"sum_roots":str(closed),"sum_over_p_power_3_2":float(closed)/p**1.5})

record={"scope":"30 exact scalar collar checks plus 5 round-spectrum sums; no finite-dimensional fixture establishes the general PDE statement","arithmetic":"Python stdlib Fraction exact rational","cases":cases,"round_sums":round_sums,"passed":True}
Path(__file__).with_name('scalar_check_results.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({"passed":True,"exact_collar_cases":len(cases),"round_sum_cases":len(round_sums)}))
