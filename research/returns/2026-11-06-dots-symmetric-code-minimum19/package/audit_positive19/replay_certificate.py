"""Standard-library-only exact replay. No root finding or external packages."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json

p=Path(__file__).resolve().parent
d=json.loads((p/'positive19_certificate.json').read_text())
x=[F(1)]+[F(v) for v in d['rational_box_center']]
r=F(d['rational_box_radius'])
R=[[F(v) for v in row] for row in d['contraction']['preconditioner']]

def add(poly,i,j,v):
    key=tuple(sorted([i,j]))
    poly[key]=poly.get(key,F(0))+v
    if poly[key]==0:del poly[key]
polys=[]
for a in [0,2,4]:
    for b in [1,3]:
        poly={}
        for k in range(8):add(poly,(2*k+a)//2,(19-2*k-b)//2,F(comb(15,2*k)))
        polys.append(poly)
for a,b in [(0,0),(0,2)]:
    poly={}
    for k in range(8):
        add(poly,(2*k+a)//2,(2*k+b)//2,F(comb(15,2*k)))
        add(poly,(2*k+4-a)//2,(2*k+4-b)//2,-F(comb(15,2*k)))
    polys.append(poly)
poly={}
for k in range(8):
    add(poly,(18-2*k)//2,(18-2*k)//2,F(comb(15,2*k)))
    add(poly,(16-2*k)//2,(16-2*k)//2,-F(comb(15,2*k)))
polys.append(poly)
f=[sum(c*x[i]*x[j] for (i,j),c in poly.items()) for poly in polys]
J=[[F(0) for _ in range(9)] for _ in range(9)]
H=[[[F(0) for _ in range(9)] for _ in range(9)] for _ in range(9)]
for l,poly in enumerate(polys):
    for (i,j),c in poly.items():
        if i>0:J[l][i-1]+=c*x[j]
        if j>0:J[l][j-1]+=c*x[i]
        if i>0 and j>0:
            H[l][i-1][j-1]+=c
            H[l][j-1][i-1]+=c
bmax=max(abs(sum(R[i][l]*f[l] for l in range(9))) for i in range(9))
Mnorm=max(sum(abs(F(i==j)-sum(R[i][l]*J[l][j] for l in range(9))) for j in range(9)) for i in range(9))
Hrow=max(sum(abs(sum(R[i][l]*H[l][j][k] for l in range(9))) for j in range(9) for k in range(9)) for i in range(9))
L=Mnorm+r*Hrow
assert bmax==F(d['contraction']['b_exact'])
assert Mnorm==F(d['contraction']['Mnorm_exact'])
assert Hrow==F(d['contraction']['Hrow_exact'])
assert L==F(d['contraction']['L_exact'])
assert L<1 and bmax+L*r<r

def z(logical,w):
    if logical==0:return w//2 if w%2==0 else None
    return (19-w)//2 if w%2 else None
def red(a,b,la,lb):
    out={}
    for k in range(16):
        i,j=z(la,k+a),z(lb,k+b)
        if i is not None and j is not None:add(out,i,j,F(comb(15,k)))
    return out
for row in d['reduced_KL_decompositions']:
    a,b=row['a'],row['b']
    actual=red(a,b,0,1) if row['kind']=='cross' else red(a,b,0,0)
    if row['kind']=='difference':
        for (i,j),v in red(a,b,1,1).items():add(actual,i,j,-v)
    expected={}
    for coeff,poly in zip(map(F,row['linear_combination']),polys):
        for (i,j),v in poly.items():add(expected,i,j,coeff*v)
    assert actual==expected

def kraw5(w):
    return sum((-1)**j*comb(w,j)*comb(19-w,5-j) for j in range(6) if j<=w and 5-j<=19-w)
coef=[F(2*comb(19,2*i)*kraw5(2*i)) for i in range(10)]
g0=sum(coef[i]*x[i]**2 for i in range(10))
gerr=r*sum(abs(2*coef[i]*x[i]) for i in range(1,10))+r*r*sum(abs(coef[i]) for i in range(1,10))
assert g0==F(d['distance5_witness']['center_value_exact'])
assert gerr==F(d['distance5_witness']['box_error_bound_exact'])
assert abs(g0)>gerr
print('PASS: exact rational existence/uniqueness, all 50 reduced KL identities, and nonzero five-site Z witness.')
print('b/r =',float(bmax/r),'L =',float(L))
