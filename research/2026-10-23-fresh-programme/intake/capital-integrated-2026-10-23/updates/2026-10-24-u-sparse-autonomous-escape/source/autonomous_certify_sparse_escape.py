"""Exact rational active-basis solve for a fixed-V2 sparse support.

python-flint is used only to generate/check the 235x235 rational basis solve.
The resulting gate certificate is independently checkable with stdlib Fraction.
"""
from __future__ import annotations
import json
import hashlib
from pathlib import Path
import time
from fractions import Fraction as F
from flint import fmpq, fmpq_mat
from autonomous_certify_escape import rationals,strings,mm,verify

DIRECTORY=Path(__file__).resolve().parent
start=time.monotonic()
source=DIRECTORY/'AUTONOMOUS_ESCAPE_RATIONAL_V2_CERTIFICATE.json'
data=json.loads(source.read_text());n=data['n']
u,k=rationals(data['U']),rationals(data['K']);a=F(data['a'])
support_data=json.loads((DIRECTORY/'AUTONOMOUS_SPARSE_FLOAT_0.json').read_text())
edges=support_data['support'];ne=len(edges)
assert ne==5*(n-1)
aa=[[F(0) for _ in range(ne)] for _ in range(5*n-1)]
for e,(i,j) in enumerate(edges):
    for l in range(4):aa[4*i+l][e]=u[j][l]-u[i][l]
    if i<n-1:aa[4*n+i][e]+=1
    if j<n-1:aa[4*n+j][e]-=1
h=[[k[i][j]-(a if i==j else 0) for j in range(4)] for i in range(4)]
bb=[value for row in mm(u,h) for value in row]+[F(0)]*(n-1)
rows=support_data['independent_row_order'][:ne]
square=fmpq_mat([[fmpq(aa[row][col].numerator,aa[row][col].denominator) for col in range(ne)] for row in rows])
rhs=fmpq_mat([[fmpq(bb[row].numerator,bb[row].denominator)] for row in rows])
determinant=square.det()
assert determinant!=0
solution=square.solve(rhs,algorithm='dixon')
values=[F(str(solution[i,0])) for i in range(ne)]
assert min(values)>0
assert all(sum((x*y for x,y in zip(row,values)),F(0))==right for row,right in zip(aa,bb))
q=[[F(0) for _ in range(n)] for _ in range(n)]
for (i,j),value in zip(edges,values):
    q[i][j]=value;q[i][i]-=value
certificate={'schema':'rational-balanced-ctmc-returned-bit-v1','n':n,'a':str(a),'T':'pi',
             'epsilon':data['epsilon'],'Q':strings(q),'U':data['U'],'K':data['K'],
             'allow_zero_rates':True,
             'construction':{'source':source.name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                             'method':'fixed-intertwiner minimum-activity LP support, exact rational active-basis solve',
                             'support_count':ne,'basis_rows':rows,'constraint_rank_exact':ne,
                             'selected_minor_determinant':str(determinant)}}
path=DIRECTORY/'AUTONOMOUS_ESCAPE_SPARSE_RATIONAL_CERTIFICATE.json'
path.write_text(json.dumps(certificate,indent=2))
result=verify(certificate)
result.update({'constraint_rank_exact':ne,'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
               'elapsed_seconds':time.monotonic()-start})
(DIRECTORY/'AUTONOMOUS_ESCAPE_SPARSE_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
