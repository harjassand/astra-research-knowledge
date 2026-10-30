from pathlib import Path
import json,sympy as S,os
p=Path(os.environ.get('ASTRA_ANGULAR_CASE',Path(__file__).parent))
b,d=S.symbols('b d',real=True);loc={'b':b,'d':d}
bl=json.loads((p/'acoustic_blowup.json').read_text())
raw={'C':json.loads((p/'boundary_matrix.json').read_text()),'M':bl['M']}
out={}
for key,mat in raw.items():
    polys=[[S.Poly(S.sympify(x,locals=loc),b,d) for x in row] for row in mat]
    entries=[[[[int(ib),int(id_),int(co.p),int(co.q)] for (ib,id_),co in poly.terms()] for poly in row] for row in polys]
    out[key]={'size':len(mat),'degrees':[max(poly.degree(b) for row in polys for poly in row),max(poly.degree(d) for row in polys for poly in row)],'entries':entries}
(p/'polynomial_matrices.json').write_text(json.dumps(out))
print({k:(v['size'],v['degrees']) for k,v in out.items()})
