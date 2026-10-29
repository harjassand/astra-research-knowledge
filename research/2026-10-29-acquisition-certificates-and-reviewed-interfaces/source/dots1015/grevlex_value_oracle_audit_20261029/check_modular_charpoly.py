import json,sys,sympy as s,time
from fractions import Fraction as F
from pathlib import Path
from sympy.polys.matrices import DomainMatrix
sys.set_int_max_str_digits(0);r=Path('producer-workspace/grevlex_value_oracle_20261029');a=json.loads((r/'quotient.json').read_text());c=json.loads((r/'candidate.json').read_text());p=10000019;D=s.GF(p);n=40;st=time.time()
def cv(v):
 v=F(v);return v.numerator*pow(v.denominator%p,-1,p)%p
def dm(rows):return DomainMatrix.from_Matrix(s.Matrix(rows)).convert_to(D)
ms=[dm([[cv(col[i]) for col in cols] for i in range(n)]) for cols in a['multiplication_columns']];I=dm(s.eye(n).tolist());powers=[[I,M,M*M,M*M*M] for M in ms];norm=I+powers[0][2]+powers[1][2]+powers[2][2];num=I.scalarmul(D.zero)
for e,v in a['f0_terms']:
 m=I
 for j,k in enumerate(e):m=m*powers[j][k]
 num=num+m.scalarmul(D(cv(v)))
L=(norm.inv()*num).scalarmul(D(pow(4,-1,p)));char=[int(v)%p for v in L.charpoly()][::-1];expected=list(map(cv,c['monic_coefficients_low_to_high']));assert char==expected
res={'first_prime':p,'independent_domainmatrix_charpoly_matches':True,'degree':len(char)-1,'seconds':time.time()-st};Path(__file__).with_name('modular_checks.json').write_text(json.dumps(res,indent=2)+'\n');print(res)
