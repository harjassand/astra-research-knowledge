"""Exact small diagnostics. These checks are not universal proof or novelty review."""
from itertools import combinations, product
import json
from pathlib import Path
import sympy as s


def resonance_identities():
    r, d = 2, 2
    coordinates = s.symbols('a:10', real=True)
    x = [coordinates[0]+s.I*coordinates[1], coordinates[4]+s.I*coordinates[5]]
    y = [coordinates[2]+s.I*coordinates[3], coordinates[6]+s.I*coordinates[7]]
    c = coordinates[8]+s.I*coordinates[9]
    K = s.Matrix(2, 2, s.symbols('K:4', real=True))
    v = s.Matrix(s.symbols('v:2', real=True))
    k = K*v
    dx = [-s.I*k[i]*s.conjugate(y[i])*c for i in range(r)]
    dy = [-s.I*k[i]*s.conjugate(x[i])*c for i in range(r)]
    dc = -s.I*sum(k[i]*x[i]*y[i] for i in range(r))
    real_rhs = []
    for i in range(r):
        real_rhs.extend([s.re(dx[i]), s.im(dx[i]), s.re(dy[i]), s.im(dy[i])])
    real_rhs.extend([s.re(dc), s.im(dc)])
    def deriv(f):
        return s.expand(sum(s.diff(f,q)*dq for q,dq in zip(coordinates,real_rhs)))
    b = [x[i]*y[i] for i in range(r)]
    z = [s.expand(bi*s.conjugate(c)) for bi in b]
    nx = [s.expand(xi*s.conjugate(xi)) for xi in x]
    ny = [s.expand(yi*s.conjugate(yi)) for yi in y]
    nc = s.expand(c*s.conjugate(c))
    actions = [nx[i]+ny[i] for i in range(r)]
    B = [sum(K[i,a]*b[i] for i in range(r)) for a in range(d)]
    Q = [[s.expand(b[i]*s.conjugate(B[a])) for a in range(d)] for i in range(r)]
    Z = [sum(K[i,a]*z[i] for i in range(r)) for a in range(d)]
    L = [sum(K[i,a]*k[i]*actions[i] for i in range(r)) for a in range(d)]
    checks = []
    for i in range(r):
        checks.extend([deriv(nx[i])+2*k[i]*s.im(z[i]),deriv(ny[i])+2*k[i]*s.im(z[i])])
        checks.append(deriv(z[i])-s.I*sum(v[a]*Q[i][a] for a in range(d))+s.I*k[i]*actions[i]*nc)
        for a in range(d):
            checks.append(deriv(Q[i][a])+s.I*k[i]*actions[i]*s.conjugate(Z[a])-s.I*L[a]*z[i])
    checks.append(deriv(nc)-2*sum(k[i]*s.im(z[i]) for i in range(r)))
    assert all(s.expand(expr)==0 for expr in checks)
    return {'r':r,'d':d,'symbolic_complex_polynomial_identities':len(checks)}


def consistent(rows):
    basis = {}
    for a,b in rows:
        while a:
            pivot = a.bit_length()-1
            if pivot not in basis:
                basis[pivot]=(a,b)
                break
            aa,bb=basis[pivot]
            a ^= aa
            b ^= bb
        if a==0 and b:
            return False
    return True


def flow_checks():
    count = 0
    for n in range(2,5):
        possible=list(combinations(range(n),2))
        for graphmask in range(1<<len(possible)):
            edges=[e for j,e in enumerate(possible) if graphmask>>j&1]
            for failed in range(1<<len(edges)):
                rows=[]
                for u in range(n):
                    mask=sum(1<<j for j,e in enumerate(edges) if u in e)
                    rows.append((mask,int(u in (0,n-1))))
                rows += [(1<<j,0) for j in range(len(edges)) if failed>>j&1]
                seen={0}
                while True:
                    old=len(seen)
                    for j,(u,v) in enumerate(edges):
                        if not(failed>>j&1) and (u in seen or v in seen):
                            seen.update((u,v))
                    if len(seen)==old:
                        break
                assert consistent(rows)==(n-1 in seen)
                count+=1
    return count


def helper_checks():
    count=0
    for arity in range(1,4):
        A=tuple(range(min(2,arity)))
        B=tuple(range(min(2,arity),arity))
        for rhs in (0,1):
            for mask in range(4):
                for x in product((0,1), repeat=arity):
                    projected=any((not(mask&1) or ((sum(x[j] for j in A)+z)%2==0))
                                  and (not(mask&2) or ((z+sum(x[j] for j in B))%2==rhs))
                                  for z in (0,1))
                    expected=mask!=3 or sum(x)%2==rhs
                    assert projected==expected
                    count+=1
    return count


if __name__=='__main__':
    receipt={'status':'PASS','scope':'exact symbolic identities and exhaustive finite diagnostics only',
             'sympy_version':s.__version__,'resonance':resonance_identities(),
             'flow_graph_failed_set_cases':flow_checks(),'private_helper_projection_cases':helper_checks(),
             'universal_proof_certified':False,'novelty_certified':False}
    Path(__file__).with_name('root_checks.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
