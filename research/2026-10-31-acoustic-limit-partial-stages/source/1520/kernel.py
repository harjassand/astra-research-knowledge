"""Actual and continuously completed acoustic capacity kernels over Q.

A closed acoustic atom is a limiting ROC inequality. It is not an actual
finite-background Hessian evaluation at that singular direction.
"""
from pathlib import Path
from fractions import Fraction as R
from functools import lru_cache
import json
from receive import source,b,ca
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
    r_psd=__import__('receive').r.psd;r_psd(H)
    Y,_=ca.solve_range(H,G);W=ca.mm(ca.transpose(G),Y)
    assert W==ca.mm(ca.transpose(Y),ca.mm(H,Y))
    side=acoustic_side(ray)
    if side is not None and kind=='closed':
        u=[ray[0],ray[2]] if side==0 else [ray[1],ray[3]];x,y=u
        beta=[sum(d['charges'][side][j][i]*x**(3-j)*y**j for j in range(4)) for i in range(12)];den=d['sigma'][side]*(x*x+y*y)**2
        W=[[W[i][j]+beta[i]*beta[j]/den for j in range(12)] for i in range(12)]
    assert W==ca.transpose(W)
    return W
