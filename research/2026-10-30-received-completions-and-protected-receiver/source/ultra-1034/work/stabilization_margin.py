"""Acquire an exact uniform margin for the already acquired angular cover."""
from pathlib import Path
from fractions import Fraction as R
import json,importlib.util,time
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('base_receiver',root/'outputs/hopf_structure/receive.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
cert=json.loads((root/'outputs/hopf_structure/certificate.json').read_text())
start=time.perf_counter();mu=R(1,2**64);oldpd=b.pd;checked=0
def shifted_pd(mat):
    global checked
    oldpd([[x-(mu if i==j else 0) for j,x in enumerate(row)] for i,row in enumerate(mat)])
    checked+=1
b.pd=shifted_pd
M=[[b.literal(p,2) for p in row] for row in cert['M']]
C=[[b.literal(p,2) for p in row] for row in cert['C_permuted']]
b.bernstein_signs(M,tuple(map(R,cert['cover']['local_box'])))
for leaf in cert['cover']['leaves']:
    if leaf['proof']=='C':b.bernstein_signs(C,tuple(map(R,leaf['box'])))
out={'uniform_margin':str(mu),'shifted_coefficient_matrices':checked,'seconds':time.perf_counter()-start}
(root/'work/stabilization_margin.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
