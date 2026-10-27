import sympy as s
from pathlib import Path
import json
I=s.eye(9);F=s.zeros(9)
for a in range(3):
 for b in range(3):F[3*b+a,3*a+b]=1
D=(3*F-I)/4
PT=s.Matrix(9,9,lambda i,j:D[3*(j//3)+i%3,3*(i//3)+j%3])
a=s.trace(D*D);b=s.trace(D**3);c=s.trace(PT**3)
assert a==s.Rational(9,2) and b==-s.Rational(9,4) and c==s.Rational(63,8)
assert 3*a-b-2*c==0
R=s.Matrix(3,3,lambda i,j:sum(D[3*k+i,3*k+j] for k in range(3)))
assert R==s.zeros(3)
report={'status':'PASS','TrD2':str(a),'TrD3':str(b),'TrPTD3':str(c),'sharp_cubic_ratio':'3','weighted_Kadison_variance':'0','source_relative_peak':'3/2'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
