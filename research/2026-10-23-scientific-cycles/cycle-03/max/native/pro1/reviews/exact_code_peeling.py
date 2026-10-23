"""Exact rational rank-one-error peeling; a sufficient no-code certificate.

If a K>=2 subspace exactly corrects a Kraus family and an error restricted to
its known ambient space has rank one, its code must lie in that error's kernel.
Iterate this necessary condition. No conclusion is made if dimension remains>1.
"""
from fractions import Fraction as F
import itertools
import math
import json
import argparse
import time
import numpy as np
from exact_code_system_probe import edge


def exact_operators(n, alpha, beta):
    letters = list(itertools.product(range(3), repeat=n))
    starts = [(0, w) for length in range(n+1)
              for w in itertools.product((1, 2), repeat=length)]
    d = 3**n
    ops = []
    records = []
    for v in starts:
        matrices = {}
        for column, word in enumerate(letters):
            states = {((), v): (1, 0)}
            for a in word:
                ns = {}
                for (out, bath), (re, im) in states.items():
                    key = out+(a,), bath
                    old = ns.get(key, (0, 0))
                    ns[key] = old[0]-beta*im, old[1]+beta*re
                    y, w = edge(a, bath)
                    key = out+(y,), w
                    old = ns.get(key, (0, 0))
                    ns[key] = old[0]+alpha*re, old[1]+alpha*im
                states = ns
            for (out, w), coeff in states.items():
                if w not in matrices:
                    matrices[w] = [np.zeros((d,d),dtype=object), np.zeros((d,d),dtype=object)]
                row = 0
                for a in out:
                    row = 3*row+a
                for component in (0,1):
                    matrices[w][component][row,column] = coeff[component]
        for w, pair in matrices.items():
            nonzero = [x for x in pair if np.any(x)]
            assert len(nonzero) <= 1, 'Endpoint parity must fix the global phase.'
            if nonzero:
                ops.append(nonzero[0])
                records.append({'start':v,'end':w})
    return ops, records


def primitive(v):
    denom = math.lcm(*(x.denominator for x in v))
    ints = [int(x*denom) for x in v]
    gcd = math.gcd(*ints)
    return [x//gcd for x in ints] if gcd else ints


def nullspace(rows, columns):
    a = [[F(int(x)) for x in row] for row in rows]
    pivots = []
    active = 0
    for col in range(columns):
        pivot = next((j for j in range(active,len(a)) if a[j][col]), None)
        if pivot is None:
            continue
        a[active],a[pivot] = a[pivot],a[active]
        scale = a[active][col]
        a[active] = [x/scale for x in a[active]]
        for j in range(len(a)):
            if j != active and a[j][col]:
                f = a[j][col]
                a[j] = [x-f*y for x,y in zip(a[j],a[active])]
        pivots.append(col)
        active += 1
        if active == len(a):
            break
    free = [j for j in range(columns) if j not in pivots]
    basis = []
    for col in free:
        v = [F(0) for _ in range(columns)]
        v[col] = F(1)
        for row, pivot in enumerate(pivots):
            v[pivot] = -a[row][col]
        basis.append(primitive(v))
    return np.array(basis,dtype=object).reshape(len(free),columns).T


def rank_one_row(a):
    rows = [list(row) for row in a if any(row)]
    if not rows:
        return None
    first = rows[0]
    pivot = next(j for j,x in enumerate(first) if x)
    for row in rows[1:]:
        if any(row[j]*first[pivot] != first[j]*row[pivot] for j in range(len(first))):
            return None
    return primitive([F(x) for x in first])


def run(n, alpha, beta):
    started=time.perf_counter()
    ops, records = exact_operators(n, alpha, beta)
    c = np.eye(3**n,dtype=object)
    rounds=[]
    while c.shape[1] > 1:
        constraints=[]; witnesses=[]
        for i,a in enumerate(ops):
            row=rank_one_row(a@c)
            if row is not None:
                constraints.append(row); witnesses.append(i)
        if not constraints:
            break
        kernel=nullspace(constraints,c.shape[1])
        rounds.append({'before':c.shape[1], 'after':kernel.shape[1],
                       'rank_one_error_indices':witnesses,
                       'coordinate_constraints':constraints,
                       'kernel_basis_columns':kernel.tolist()})
        c=c@kernel
    return {'slots':n,'alpha_beta_unnormalized':[alpha,beta],
            'kraus_count':len(ops),'rounds':rounds,
            'residual_dimension':c.shape[1],
            'no_nontrivial_subspace_certified':c.shape[1]<=1,
            'residual_basis_columns':c.tolist(),
            'kraus_records':records,'wall_seconds':time.perf_counter()-started}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--slots',type=int,default=3)
    p.add_argument('--alpha',type=int,default=3);p.add_argument('--beta',type=int,default=4)
    p.add_argument('--output',required=True);args=p.parse_args()
    out=run(args.slots,args.alpha,args.beta)
    with open(args.output,'w') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in
                     ('kraus_records','residual_basis_columns','rounds')},indent=2))
    print('peeling dimensions:',[(r['before'],r['after']) for r in out['rounds']])
