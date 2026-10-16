"""Analytic dimension parameter via delta-diagram contraction.

Uniform Schmidt reference u=sum_{i=0}^{d-1}|ii>, with p=q=d>=3.
This constructs a dimension-symbolic decomposition, not a numerical sweep.
"""
from collections import defaultdict
from itertools import product
from pathlib import Path
import json
import sympy as sp

d = sp.Symbol('d', real=True, positive=True)
x = sp.Symbol('x', real=True, nonnegative=True)
R = sp.Rational


def reduce_diagram(edges, keep):
    keep = set(keep)
    nodes = set(n for e in edges for n in e) | keep
    parent = {i:i for i in nodes}
    def root(i):
        while parent[i] != i:
            i = parent[i]
        return i
    for edge in edges:
        for j in edge[1:]:
            parent[root(j)] = root(edge[0])
    cc = defaultdict(list)
    for i in nodes:
        cc[root(i)].append(i)
    loops = sum(not keep.intersection(v) for v in cc.values())
    reduced = tuple(sorted(tuple(sorted(keep.intersection(v)))
                           for v in cc.values() if keep.intersection(v)))
    return reduced, d**loops


def clean(terms):
    return {k:sp.factor(v) for k,v in terms.items() if sp.factor(v) != 0}


def switched_diagrams():
    alpha = 1/(d-1)
    beta = 1/((d-1)*(5*d-4))
    left = [
        (1,[(4,5),(2,8),(3,9)]),
        (-R(1,2),[(2,4),(8,5),(3,9)]),
        (-R(1,2),[(3,5),(2,8),(9,4)]),
        (R(1,4),[(2,4),(3,5),(8,9)]),
    ]
    middle = [(alpha,[(8,10),(9,11)]),(-beta,[(8,9),(10,11)])]
    right = [
        (1,[(0,1),(6,10),(7,11)]),
        (-R(1,2),[(6,0),(10,1),(7,11)]),
        (-R(1,2),[(7,1),(6,10),(11,0)]),
        (R(1,4),[(6,0),(7,1),(10,11)]),
    ]
    ans = defaultdict(lambda:sp.Integer(0))
    for (a,A),(b,B),(c,C) in product(left,middle,right):
        key,mult = reduce_diagram(A+B+C,range(8))
        ans[key] += a*b*c*mult
    return clean(ans)


def cochoi_diagrams():
    terms = {}
    for ca,cb in product((0,1),repeat=2):
        perm = [4,5,6,7]
        if ca: perm[0],perm[2] = perm[2],perm[0]
        if cb: perm[1],perm[3] = perm[3],perm[1]
        key,_ = reduce_diagram([(i,perm[i]) for i in range(4)],range(8))
        terms[key] = (-R(1,2))**(ca+cb)
    return terms


T0 = [[(0,1),(2,3)],[(0,3),(2,1)]]
T1 = [[(0,1),(2,12),(3,13)],
      [(0,12),(1,13),(2,3)],
      [(0,3),(2,12),(1,13)],
      [(0,12),(3,13),(2,1)]]


def action(ops, tensors, adjoint=False):
    keep = list(range(4))+([12,13] if adjoint else [])
    targets = [reduce_diagram(t,keep)[0] for t in tensors]
    M = sp.zeros(len(tensors))
    leftovers = []
    for j, tensor in enumerate(tensors):
        coltensor = [tuple(i+4 if i < 4 else i for i in edge) for edge in tensor]
        ans = defaultdict(lambda:sp.Integer(0))
        for key, coeff in ops.items():
            new,mult = reduce_diagram(list(key)+coltensor,keep)
            # Closing the two X indices produces Tr(X)=0 in adjoint sector.
            if adjoint and any(12 in block and 13 in block for block in new):
                continue
            ans[new] += coeff*mult
        for key,coeff in clean(ans).items():
            if key not in targets:
                leftovers.append((j,key,coeff))
            else:
                M[targets.index(key),j] += coeff
    assert not leftovers, leftovers
    return M.applyfunc(sp.factor)


def scalar_actions(ops):
    """Fully contraction-free sector: only through permutations survive."""
    ans = {}
    for ea,eb in product((-1,1),repeat=2):
        value = 0
        for key,coeff in ops.items():
            if not all(len(block)==2 and sum(i<4 for i in block)==1 for block in key):
                # Every discarded diagram is killed on V^perp because it
                # contains one of these four input contractions.
                assert any(tuple(block) in ((4,5),(4,7),(5,6),(6,7)) for block in key)
                continue
            mapping = {next(i for i in block if i<4):next(i for i in block if i>=4)
                       for block in key}
            ca = mapping[0] == 6
            cb = mapping[1] == 7
            assert mapping == {0:6 if ca else 4, 2:4 if ca else 6,
                               1:7 if cb else 5, 3:5 if cb else 7}
            value += coeff*(ea if ca else 1)*(eb if cb else 1)
        ans[f'{ea},{eb}'] = sp.factor(value)
    return ans


def polynomial_psd(M):
    assert M == M.T
    H = M.subs(d,x+3).applyfunc(sp.cancel)
    denom = sp.lcm([sp.denom(v) for v in H])
    assert all(c>=0 for c in sp.Poly(denom,x).all_coeffs()) and denom.subs(x,0)>0
    H = (H*denom).applyfunc(sp.cancel)
    coeff = [sp.factor((-1)**j*c) for j,c in enumerate(H.charpoly().all_coeffs())]
    records = []
    for c in coeff:
        scalar,factors = sp.factor_list(c,x)
        okay = scalar>=0 and all(n%2==0 or all(v>=0 for v in sp.Poly(f,x).all_coeffs())
                                for f,n in factors)
        records.append({'coefficient':str(c),'certified':bool(okay)})
    return {'denominator':str(denom),'coefficient_records':records,
            'certified':all(r['certified'] for r in records)}


def main():
    C = cochoi_diagrams()
    S = switched_diagrams()
    C0,S0 = action(C,T0),action(S,T0)
    C1,S1 = action(C,T1,True),action(S,T1,True)
    G0 = sp.Matrix([[d*d,d],[d,d*d]])
    G1 = sp.Matrix([[d,0,1,1],[0,d,1,1],[1,1,d,0],[1,1,0,d]])
    CS,SS = scalar_actions(C),scalar_actions(S)
    out = {'status':'DIMENSION_SYMBOLIC_UNIFORM_SCHMIDT_CERTIFICATE',
           'scope':'p=q=d>=3 integer; u=sum_i|ii>; no nonuniform or inactive-label extension',
           'sharp_generalized_interval':'[-(5*d+1)/(9*(d-1)),1], contained in [-8/9,1] for d>=3',
           'C_trivial':str(C0),'S_trivial':str(S0),'G_trivial':str(G0),
           'C_adjoint':str(C1),'S_adjoint':str(S1),'G_adjoint':str(G1),
           'S_diagram_terms':[{'partition':key,'coefficient':str(v)} for key,v in S.items()],
           'C_scalars':{k:str(v) for k,v in CS.items()},
           'S_scalars':{k:str(v) for k,v in SS.items()},
           'certificates':{}}
    for sector,G,CC,SSS in [('trivial',G0,C0,S0),('adjoint',G1,C1,S1)]:
        for name,H in [('upper',G*(CC-SSS)),('lower_1',G*(SSS+CC)),
                       ('sharp_lower',G*(SSS+(5*d+1)/(9*(d-1))*CC)),
                       ('lower_11_over9',G*(SSS+R(11,9)*CC)),
                       ('lower_3',G*(SSS+3*CC))]:
            out['certificates'][f'{sector}_{name}'] = polynomial_psd(H.applyfunc(sp.factor))
        out[f'{sector}_generalized_charpoly'] = str(sp.factor((CC.inv()*SSS).charpoly().as_expr()))
    for k in CS:
        for name,expr in [('upper',CS[k]-SS[k]),('lower_1',SS[k]+CS[k]),
                          ('sharp_lower',SS[k]+(5*d+1)/(9*(d-1))*CS[k]),
                          ('lower_11_over9',SS[k]+R(11,9)*CS[k]),
                          ('lower_3',SS[k]+3*CS[k])]:
            out['certificates'][f'scalar_{k}_{name}'] = polynomial_psd(sp.Matrix([[expr]]))
    out['all_certified'] = all(v['certified'] for v in out['certificates'].values())
    target = Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('certificates','S_diagram_terms')},indent=2))


if __name__ == '__main__':
    main()
