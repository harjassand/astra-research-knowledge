"""Actual and continuously completed acoustic capacity kernels over Q.

A closed acoustic atom is a limiting ROC inequality. It is not an actual
finite-background Hessian evaluation at that singular direction.
"""
from pathlib import Path
from fractions import Fraction as R
from functools import lru_cache
import json
from receive import source,b,ca,r
HERE=Path(__file__).resolve().parent
@lru_cache(maxsize=1)
def data():
    F,T,basis,powers,polys,HF,nulls=source();cert=json.loads((HERE/'certificate.json').read_text())
    return {'F':F,'T':T,'basis':basis,'powers':powers,'polys':polys,'HF':HF,'nulls':nulls,'charges':[[list(map(R,row)) for row in chart['charge_on_normal_basis']] for chart in cert['acoustic_charts']],'sigma':[R(chart['sigma']) for chart in cert['acoustic_charts']]}

def acoustic_side(ray):
    if not ray[1] and not ray[3]:return 0
    if not ray[0] and not ray[2]:return 1
    return None

def capacity_kernel(ray,kind='closed'):
    ray=list(map(R,ray));assert len(ray)==4 and any(ray) and ray[0]*ray[3]-ray[1]*ray[2]==0 and kind in ('closed','ordinary')
    d=data();H=[[b.evaluate(p,ray) for p in row] for row in d['HF']];G=[[b.evaluate(b.diff(p,j),ray) for p in d['polys']] for j in range(4)]
    r.psd(H)
    Y,_=ca.solve_range(H,G);W=ca.mm(ca.transpose(G),Y)
    assert W==ca.mm(ca.transpose(Y),ca.mm(H,Y))
    side=acoustic_side(ray)
    if side is not None and kind=='closed':
        u=[ray[0],ray[2]] if side==0 else [ray[1],ray[3]];x,y=u
        beta=[sum(d['charges'][side][j][i]*x**(3-j)*y**j for j in range(4)) for i in range(12)];den=d['sigma'][side]*(x*x+y*y)**2
        W=[[W[i][j]+beta[i]*beta[j]/den for j in range(12)] for i in range(12)]
    assert W==ca.transpose(W)
    return W

def feature_factor(ray,kind='closed'):
    """Return M,J with capacity kernel J^T M^+ J, retaining jet features."""
    ray=list(map(R,ray));d=data();side=acoustic_side(ray)
    if side is None or kind=='ordinary':
        M=[[b.evaluate(p,ray) for p in row] for row in d['HF']];J=[[b.evaluate(b.diff(P,j),ray) for P in d['polys']] for j in range(4)]
    else:
        cert=json.loads((HERE/'certificate.json').read_text());u=[ray[0],ray[2]] if side==0 else [ray[1],ray[3]];x,y=u
        def rot(v):return [x*v[0]-y*v[2],x*v[1]-y*v[3],y*v[0]+x*v[2],y*v[1]+x*v[3]]
        null=rot(d['nulls'][side]);perp=[rot([R(int(i==j)) for i in range(4)]) for j in range(3)];deriv=[0,x,0,y] if side==0 else [x,0,y,0]
        gamma=[]
        for P in d['polys']:
            HC=[[b.evaluate(b.diff(b.diff(P,i),j),ray) for j in range(4)] for i in range(4)];gamma.append(sum(null[i]*HC[i][j]*deriv[j] for i in range(4) for j in range(4)))
        J=[gamma]+[[sum(v[i]*b.evaluate(b.diff(P,i),ray) for i in range(4)) for P in d['polys']] for v in perp]
        M=[[R(co)*(x*x+y*y)**2 for co in row] for row in cert['acoustic_charts'][side]['deflated_Hessian_at_zero']]
    Y,_=ca.solve_range(M,J);assert ca.mm(ca.transpose(J),Y)==capacity_kernel(ray,kind)
    return M,J
