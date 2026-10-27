#!/usr/bin/env python3
"""Independent exact reconstruction of three field-linear factors.

No exhaustive field search is used by factor_three_linear_forms. This is
an interface audit, not a point-counting implementation or speed test.
"""
import json
from pathlib import Path
import random
from field_acquisition_audit import (fixture_field, random_invertible_field_matrix,
    sum_xor, candidates, evaluation_vector, kernel, field_monomial)


def trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def add(a,b):
    return trim([(a[i] if i<len(a) else 0) ^ (b[i] if i<len(b) else 0)
                 for i in range(max(len(a),len(b)))])


def mul(field,a,b):
    if not a or not b:
        return []
    out = [0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j] ^= field.mul(x,y)
    return trim(out)


def divrem(field,a,b):
    a,b = trim(a),trim(b)
    assert b
    out = [0]*max(0,len(a)-len(b)+1)
    inv = field.pow(b[-1],field.q-2)
    while a and len(a)>=len(b):
        shift = len(a)-len(b)
        c = field.mul(a[-1],inv)
        out[shift] = c
        for j,y in enumerate(b):
            a[shift+j] ^= field.mul(c,y)
        a = trim(a)
    return trim(out),a


def gcd(field,a,b):
    while b:
        a,b = b,divrem(field,a,b)[1]
    if not a:
        return []
    inv = field.pow(a[-1],field.q-2)
    return [field.mul(c,inv) for c in a]


def ordinary_derivative(poly):
    return trim([poly[i] if i&1 else 0 for i in range(1,len(poly))])


def value(field,poly,x):
    out = 0
    for c in reversed(poly):
        out = field.mul(out,x)^c
    return out


def cubic_value(field,F,X):
    return sum_xor(field.mul(c,field_monomial(field,X,e)) for e,c in F.items())


def cubic_gradient(field,F,X):
    out = []
    for i in range(3):
        result = 0
        for e,c in F.items():
            if e[i]&1:
                powers = list(e)
                powers[i] -= 1
                result ^= field.mul(c,field_monomial(field,X,powers))
        out.append(result)
    return out


def cubic_on_line(field,F,u,v):
    out = []
    for exponent,coefficient in F.items():
        p = [coefficient]
        for i,power in enumerate(exponent):
            for _ in range(power):
                p = mul(field,p,[u[i],v[i]])
        out = add(out,p)
    return out


def multiply_linear_forms(field,forms):
    poly = {(0,0,0):1}
    for row in forms:
        out = {}
        for exponent,coefficient in poly.items():
            for j,a in enumerate(row):
                e = list(exponent)
                e[j] += 1
                e = tuple(e)
                out[e] = out.get(e,0)^field.mul(coefficient,a)
        poly = {e:c for e,c in out.items() if c}
    return poly


def field_matrix_rank(field,matrix):
    matrix = [row[:] for row in matrix]
    r = 0
    for column in range(3):
        pivot = next((i for i in range(r,len(matrix)) if matrix[i][column]),None)
        if pivot is None:
            continue
        matrix[pivot],matrix[r] = matrix[r],matrix[pivot]
        inv = field.pow(matrix[r][column],field.q-2)
        matrix[r] = [field.mul(x,inv) for x in matrix[r]]
        for i,row in enumerate(matrix):
            if i != r and row[column]:
                c = row[column]
                matrix[i] = [x ^ field.mul(c,y) for x,y in zip(row,matrix[r])]
        r += 1
    return r


def split_cubic(field,f):
    """Trace partitions separate roots, with polynomial work in field degree."""
    if len(f)!=4 or len(gcd(field,f,ordinary_derivative(f)))!=1:
        return None
    Xq = [0,1]
    for _ in range(field.d):
        Xq = divrem(field,mul(field,Xq,Xq),f)[1]
    if divrem(field,add(Xq,[0,1]),f)[1]:
        return None
    factors = [f]
    for i in range(field.d):
        t,trace = [0,1<<i],[]
        for _ in range(field.d):
            trace = add(trace,t)
            t = divrem(field,mul(field,t,t),f)[1]
        refined = []
        for h in factors:
            g = gcd(field,h,trace)
            if 1<len(g)<len(h):
                quotient,remainder = divrem(field,h,g)
                assert not remainder
                refined.extend([g,quotient])
            else:
                refined.append(h)
        factors = refined
    if any(len(h)!=2 for h in factors):
        return None
    roots = [field.mul(h[0],field.pow(h[1],field.q-2)) for h in factors]
    assert len(set(roots)) == 3 and all(value(field,f,r)==0 for r in roots)
    return roots


def factor_three_linear_forms(field,F):
    if field.d < 3:
        raise ValueError("the seven-element construction requires q>=8")
    v = None
    for tv in range(7):
        probe = [1,tv,field.mul(tv,tv)]
        if cubic_value(field,F,probe):
            v = probe
            break
    if v is None:
        return None
    u,h = None,None
    for su in range(7):
        probe = [1,su,field.mul(su,su)]
        p = cubic_on_line(field,F,probe,v)
        if len(p)==4 and len(gcd(field,p,ordinary_derivative(p)))==1:
            u,h = probe,p
            break
    if u is None:
        return None
    roots = split_cubic(field,h)
    if roots is None:
        return None
    forms = [cubic_gradient(field,F,[u[i]^field.mul(r,v[i]) for i in range(3)])
             for r in roots]
    if field_matrix_rank(field,forms)!=3:
        return None
    acquired = multiply_linear_forms(field,forms)
    if set(acquired)!=set(F):
        return None
    exponent = next(iter(F))
    multiplier = field.mul(F[exponent],field.pow(acquired[exponent],field.q-2))
    if any(F[e]!=field.mul(multiplier,c) for e,c in acquired.items()):
        return None
    return {"forms":forms,"multiplier":multiplier,"v_trials":tv+1,
            "u_trials":su+1,"roots":roots}


def uniqueness_audit(field):
    n = 3*field.d
    exponents = candidates(3,3)
    inputs = [mask for mask in range(1<<n) if mask.bit_count()<=3]
    columns = [evaluation_vector(field,3,e,1<<j,inputs)
               for e in exponents for j in range(field.d)]
    relations = kernel(columns)
    cubic_mask = sum(1<<(i*field.d+j) for i,e in enumerate(exponents)
                     if sum(e)==3 for j in range(field.d))
    cubic_aliases = sum(bool(rel&cubic_mask) for rel in relations)
    assert (cubic_aliases==0) == (field.d>=3)
    return {"field_degree":field.d,"coefficient_columns":len(columns),
            "relations":len(relations),"relations_involving_homogeneous_cubics":cubic_aliases}


def run():
    rng = random.Random(202610271531)
    records = []
    pointwise = 0
    for d in [3,4,5,6,8]:
        field = fixture_field(d)
        for _ in range(24):
            forms = random_invertible_field_matrix(field,3,rng)
            F = multiply_linear_forms(field,forms)
            acquired = factor_three_linear_forms(field,F)
            assert acquired is not None
            assert max(acquired['v_trials'],acquired['u_trials'])<=7
            for _ in range(32):
                X = [rng.randrange(field.q) for _ in range(3)]
                left = cubic_value(field,F,X)
                right = acquired['multiplier']
                for row in acquired['forms']:
                    right = field.mul(right,sum_xor(field.mul(a,x) for a,x in zip(row,X)))
                assert left==right
                pointwise += 1
            records.append({"field_degree":d,"v_trials":acquired['v_trials'],
                            "u_trials":acquired['u_trials']})
        bad = {(1,1,1):1,(3,0,0):1}
        assert factor_three_linear_forms(field,bad) is None
    uniqueness = [uniqueness_audit(fixture_field(d)) for d in [1,2,3,4,5]]
    return {"status":"all exact assertions passed","factor_cases":len(records),
            "pointwise_checks":pointwise,"nonfactor_rejections":5,
            "maximum_v_trials":max(r['v_trials'] for r in records),
            "maximum_u_trials":max(r['u_trials'] for r in records),
            "uniqueness_records":uniqueness,"factor_records":records,
            "algorithm_enumerates_field":False}


if __name__=='__main__':
    result = run()
    Path(__file__).with_name('triple_factor_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='factor_records'},indent=2))
