import json, math
from fractions import Fraction
rows=[]
for n in range(2,202,2):
    total=sum((Fraction(j*(n-j),n-1) for j in range(1,n)),Fraction(0))
    assert total==Fraction(n*(n+1),6)
    assert sum(min(j,n-j) for j in range(1,n))==n*n//4
    rows.append({'n':n,'mean_crossing_sum':str(total),'mean_gate_lower_bound':str(total/2)})
print(json.dumps({'checks':len(rows),'rows':rows},indent=2))
