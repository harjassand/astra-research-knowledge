"""Replay exact shifts and Bernstein certificate, after triad_wedge.py."""
import json,math,runpy
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
base=Path(__file__).parent
data=json.loads((base/'triad_wedge_certificate.json').read_text())
assert len(data['terms'])==7197 and not data['negative_terms']
assert all(Fraction(v)>0 and k[0]%2==0 for k,v in data['terms'])
out=defaultdict(Fraction)
for (ee,j,a,b,c),co in data['terms']:
 for i in range(j+1):
  out[(ee,i,a,b,c)]+=Fraction(co)*math.comb(j,i)*(-1)**(j-i)
out={k:v for k,v in out.items() if v}
assert len(out)==5047 and all(v>0 for v in out.values())
(base/'shift_1.json').write_text(json.dumps({'shift':'1','negative_count':0,'terms':[(k,str(v)) for k,v in sorted(out.items())]},indent=2)+'\n')
runpy.run_path(str(base/'acute_test.py'),run_name='__main__')
acute=json.loads((base/'acute_test.json').read_text())
assert not acute['negative'] and acute['total']==4616
assert all(Fraction(v)>=0 for _,_,_,v in acute['bernstein_coefficients'])
print('PASS: every noncollinear characteristic-polarized triad, all amplitudes/phases/means')
