#!/usr/bin/env python3
"""Exact infinite-bath two-call algebra, with symbolic alpha,beta.

Standard library only. Coefficients are Gaussian-rational polynomials modulo
alpha**2 + beta**2 = 1. This is an algebraic replay, not a cutoff simulation.
"""
from __future__ import annotations
import argparse, importlib.util, json, platform, resource, sys, time
from fractions import Fraction as F
from itertools import product
from pathlib import Path

HERE=Path(__file__).resolve().parent
REP=HERE.parent/'starting_source/Astra_Amplification_Cycle3_PRO1_20261022/representation/exact_representation.py'
if not REP.exists(): REP=HERE.parent/'representation/exact_representation.py'
spec=importlib.util.spec_from_file_location('two_call_native_representation',REP)
r=importlib.util.module_from_spec(spec); sys.modules[spec.name]=r; spec.loader.exec_module(r)

class P:
    def __init__(self,d=None): self.d={k:v for k,v in (d or {}).items() if v}
    def __add__(self,o):
        o=pp(o); d=dict(self.d)
        for k,v in o.d.items(): d[k]=d.get(k,r.G())+v
        return P(d)
    __radd__=__add__
    def __neg__(self): return P({k:-v for k,v in self.d.items()})
    def __sub__(self,o): return self+-pp(o)
    def __rsub__(self,o): return pp(o)+-self
    def __mul__(self,o):
        o=pp(o); d={}
        for (i,j),v in self.d.items():
            for (k,l),w in o.d.items():
                # Canonical alpha power is 0 or 1; only alpha^2 needs reduction.
                if i+k<2: d[(i+k,j+l)]=d.get((i+k,j+l),r.G())+v*w
                else:
                    d[(0,j+l)]=d.get((0,j+l),r.G())+v*w
                    d[(0,j+l+2)]=d.get((0,j+l+2),r.G())-v*w
        return P(d)
    __rmul__=__mul__
    def conjugate(self): return P({k:v.conjugate() for k,v in self.d.items()})
    def __bool__(self): return bool(self.d)
    def __eq__(self,o): return self.d==pp(o).d
    def serial(self): return [{'alpha_power':k[0],'beta_power':k[1],
                               're':str(v.re),'im':str(v.im)} for k,v in sorted(self.d.items())]
def pp(x): return x if isinstance(x,P) else P({(0,0):r.asg(x)})
A=P({(1,0):r.G(F(1))}); B=P({(0,1):r.G(F(1))}); J=pp(r.I_G)
def clean(x): return {k:v for k,v in x.items() if v}
def add(*xs):
    d={}
    for x in xs:
        for k,v in x.items(): d[k]=d.get(k,P())+v
    return clean(d)
def scale(x,c): return clean({k:pp(c)*v for k,v in x.items()})
def mul(x,y):
    d={}
    for k,v in x.items():
        for l,w in y.items():
            for m,s in r.basis_product(k,l): d[m]=d.get(m,P())+s*v*w
    return clean(d)
def adj(x): return {(kind,v,u):c.conjugate() for (kind,u,v),c in x.items()}
I={('F',(),()):pp(1)}; R={('K',(),()):pp(1)}
S={a:{('F',(a,),()):pp(1)} for a in (1,2)}
P0=mul(R,R); P1=add(*(mul(mul(S[a],P0),adj(S[a])) for a in (1,2)))
V=[[{} for _ in range(3)] for _ in range(3)]
V[0][0]=add(scale(R,A),scale(I,J*B))
for a in (1,2):
    V[0][a]=scale(S[a],A); V[a][0]=scale(adj(S[a]),A); V[a][a]=scale(I,J*B)
words=list(product(range(3),repeat=2))
T={(o,i):mul(V[o[1]][i[1]],V[o[0]][i[0]]) for o in words for i in words}
def charge(w): return sum(a!=0 for a in w)
def gram_by_shift(entries):
    gs={k:{} for k in range(-2,3)}
    for i,j,c in entries:
        assert charge(i)==charge(j)
        for o in words:
            k=charge(i)-charge(o)
            gs[k]=add(gs[k],scale(mul(adj(T[o,j]),T[o,i]),c))
    return gs
def family_entries():
    return {
      'x':[((0,0),(0,0),1)],
      'y':[(w,w,1) for a in (1,2) for w in ((a,0),(0,a))],
      'z':[(w,w,1) for w in product((1,2),repeat=2)],
      'c':[(i,j,1) for a in (1,2) for i,j in (((a,0),(0,a)),((0,a),(a,0)))]}
def add_map(d,L,Q,c=1):
    # L X Q* in a unique tensor product of the inherited operator normal forms.
    for k,v in L.items():
        for l,w in Q.items(): d[(k,l)]=d.get((k,l),P())+pp(c)*v*w.conjugate()
def compose_left(x,y): return mul(x,y)
def cross_direct():
    d={}
    for i,j,c in family_entries()['c']:
        for o in words: add_map(d,T[o,i],T[o,j],c)
    return clean(d)
def cross_formula():
    d={}; ab=A*A*B*B; a3b=A*A*A*B
    for a in (1,2):
        add_map(d,S[a],S[a],2*ab); add_map(d,adj(S[a]),adj(S[a]),2*ab)
    add_map(d,I,I,-6*ab); add_map(d,P0,I,ab); add_map(d,I,P0,ab)
    # i alpha^3 beta [ C([X,R]) + 2[R,X] + R X P - P X R ].
    for a in (1,2):
        add_map(d,S[a],mul(S[a],R),J*a3b)
        add_map(d,mul(S[a],R),S[a],-J*a3b)
    add_map(d,R,I,2*J*a3b); add_map(d,I,R,-2*J*a3b)
    Pr=add(I,scale(P0,-1))
    add_map(d,R,Pr,J*a3b); add_map(d,Pr,R,-J*a3b)
    return clean(d)
def main():
    start=time.perf_counter(); a=A*A; b=B*B
    assert cross_direct()==cross_formula()
    expected={
      'x':add(scale(I,-2*a),scale(P0,2*a),scale(P1,a*a)),
      'y':scale(P0,2*a*(1+b)),
      'z':scale(I,8*a),
      'c':add(scale(I,2*a*b),scale(P0,2*a*b))}
    normalization={'x':1,'y':4,'z':4,'c':0}
    # Coefficients of f(l+k) at depth >=2; exact root/level-1 corrections checked.
    bulk={
       'x':{-2:a*a,-1:2*a*b,0:b*b,1:pp(0),2:pp(0)},
       'y':{-2:pp(0),-1:4*a*b,0:4*(a*a+b*b),1:4*a*b,2:pp(0)},
       'z':{-2:pp(0),-1:pp(0),0:4*b*b,1:8*a*b,2:4*a*a},
       'c':{-2:pp(0),-1:2*a*b,0:-6*a*b,1:4*a*b,2:pp(0)}}
    root={
       'x':{0:pp(1),1:pp(0),2:pp(0)},
       'y':{0:2*a*a+4*b,1:2*a*(1+b),2:pp(0)},
       'z':{0:4*b*b,1:8*a*b,2:4*a*a},
       'c':{0:-4*a*b,1:4*a*b,2:pp(0)}}
    actual={}
    for name,entries in family_entries().items():
        gs=gram_by_shift(entries)
        assert add(*gs.values())==scale(I,normalization[name])
        drift=add(*(scale(g,k) for k,g in gs.items()))
        assert drift==expected[name]
        for k,g in gs.items():
            at_one=pp(0) if k==-2 else (bulk[name][-2]+bulk[name][-1] if k==-1 else bulk[name][k])
            at_zero=root[name].get(k,pp(0))
            target=add(scale(I,bulk[name][k]),
                       scale(P0,at_zero-bulk[name][k]),
                       scale(P1,at_one-bulk[name][k]))
            assert g==target
        # Exact Kraus grades prove that the remaining operator coefficients are
        # supported at levels 0,1, independent of every deeper coordinate.
        residual={k:add(g,scale(I,-bulk[name][k])) for k,g in gs.items()}
        for z in residual.values():
            # Multiply outside P0+P1: residual vanishes on all levels >=2.
            assert mul(z,add(I,scale(P0,-1),scale(P1,-1)))=={}
        actual[name]={'drift_terms':len(drift),'grade_gram_terms':{str(k):len(g) for k,g in gs.items()}}
    out={'status':'passed','symbolic_parameters':'Gaussian rational polynomials modulo alpha^2+beta^2=1',
         'bath_cutoff':None,'full_cross_superoperator_identity':True,
         'families':actual,'scope':'Algebra only; recurrence and coding require written proofs.',
         'wall_seconds':time.perf_counter()-start,
         'max_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'python':platform.python_version()}
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output');args=p.parse_args()
    text=json.dumps(main(),indent=2)+'\n'
    if args.output: Path(args.output).write_text(text)
    print(text,end='')
