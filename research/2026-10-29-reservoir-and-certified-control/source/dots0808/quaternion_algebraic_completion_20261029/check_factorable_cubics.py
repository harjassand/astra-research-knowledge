import sympy as s,itertools,time,json
from pathlib import Path
from macaulay_template import resultant
q=s.symbols('q0:4');B=s.Matrix([[3,1,2,1],[2,5,1,3],[1,2,7,2],[3,1,2,11]])
H=[q[i]*sum(B[i,j]*q[j]**2 for j in range(4)) for i in range(4)];expected=s.Integer(1);terms=[]
for k in range(1,5):
 for S in itertools.combinations(range(4),k):
  d=B.extract(S,S).det();assert d!=0;expected*=d**(2**(k-1));terms.append(dict(support=list(S),minor=str(d),exponent=2**(k-1)))
st=time.time();actual=resultant(H,q);assert actual==expected
out=dict(B=[list(map(int,B.row(i))) for i in range(4)],principal_minor_terms=terms,exact_resultant=str(actual),seconds=time.time()-st,scope='Nontrivial factorable-cubic exact Macaulay quotient vs independent principal-minor product. Not universal derivatives/global optimizer.')
Path(__file__).with_name('factorable_cubics_check.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
