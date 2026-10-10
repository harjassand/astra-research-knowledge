from fractions import Fraction
import json
checks=[]
for m in range(2,101):
    s=Fraction(1,3**(m-1)); t=Fraction(1,2**m-1)
    assert s<=t
    checks.append(m)
print(json.dumps({'checked_integer_orders':checks,'proof':'Induction in RESULT.md covers all integer m>=2; finite checks are redundant verification.','same_mean_occupation':1,'entropy_gap':'log(4/3)>0','channel_output_realizability_claimed':False},indent=2))
