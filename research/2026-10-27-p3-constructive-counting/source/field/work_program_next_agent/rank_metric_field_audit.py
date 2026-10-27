#!/usr/bin/env python3
"""Independent exact audit: acquired field blocks + low-rank quadratic defect.

The finite tests validate code construction, bounded-distance decoding,
symmetry, and real Gaussian-Walsh reconstruction. They do not implement
the large-field point-counting leaf used in the resulting theorem.
"""
from itertools import combinations
import json
from pathlib import Path
import random

from field_acquisition_audit import (fixture_field, rank, solve, kernel,
    linear_apply, sum_xor, random_invertible_field_matrix)
from triple_factor_audit import multiply_linear_forms, cubic_value


def qdegree(poly):
    return max((i for i,c in enumerate(poly) if c),default=-1)


def qeval(field,poly,x):
    out = 0
    for c in poly:
        out ^= field.mul(c,x)
        x = field.mul(x,x)
    return out


def qcompose(field,E,f):
    if qdegree(E)<0 or qdegree(f)<0:
        return []
    out = [0]*(qdegree(E)+qdegree(f)+1)
    for i,e in enumerate(E):
        for j,c in enumerate(f):
            if e and c:
                out[i+j] ^= field.mul(e,field.pow(c,1<<i))
    return out


def field_solve(field,rows,rhs,width):
    matrix = [row[:]+[b] for row,b in zip(rows,rhs)]
    pivot_columns = []
    pivot = 0
    for column in range(width):
        i = next((i for i in range(pivot,len(matrix)) if matrix[i][column]),None)
        if i is None:
            continue
        matrix[pivot],matrix[i] = matrix[i],matrix[pivot]
        inv = field.pow(matrix[pivot][column],field.q-2)
        matrix[pivot] = [field.mul(x,inv) for x in matrix[pivot]]
        for j in range(len(matrix)):
            if j != pivot and matrix[j][column]:
                c = matrix[j][column]
                matrix[j] = [x ^ field.mul(c,y) for x,y in zip(matrix[j],matrix[pivot])]
        pivot_columns.append(column)
        pivot += 1
    if any(not any(row[:-1]) and row[-1] for row in matrix):
        return None
    out = [0]*width
    for row,column in zip(matrix,pivot_columns):
        out[column] = row[-1]
    return out


def divide_composition(field,N,E,k):
    """Recover f in N=E composed with f. E is monic and on the LEFT."""
    remainder = list(N)
    t = qdegree(E)
    assert E[t] == 1
    f = [0]*k
    while qdegree(remainder)>=t:
        j = qdegree(remainder)-t
        if j>=k:
            return None
        c = field.pow(remainder[j+t],1<<((field.d-t)%field.d))
        f[j] ^= c
        for i,e in enumerate(E):
            remainder[j+i] ^= field.mul(e,field.pow(c,1<<i))
    if qdegree(remainder)>=0:
        return None
    assert qcompose(field,E,f) == N or all(a==b for a,b in zip(qcompose(field,E,f),N))
    return f


def gabidulin_decode(field,g,y,k=3,t=None):
    if t is None:
        t = (len(g)-k)//2
    if t<0 or k+2*t>len(g):
        raise ValueError('outside unique-decoding parameter range')
    rows,rhs = [],[]
    for gj,yj in zip(g,y):
        rows.append([field.pow(yj,1<<i) for i in range(t)] +
                    [field.pow(gj,1<<i) for i in range(k+t)])
        rhs.append(field.pow(yj,1<<t))
    solution = field_solve(field,rows,rhs,k+2*t)
    if solution is None:
        return None
    E = solution[:t]+[1]
    N = solution[t:]
    f = divide_composition(field,N,E,k)
    if f is None or rank([yj^qeval(field,f,gj) for gj,yj in zip(g,y)])>t:
        return None
    return f


def bilinear_block(field,L):
    d = field.d
    g = [1<<i for i in range(d)]
    return [sum(field.trace(field.mul(gi,L[j]))<<j for j in range(d)) for gi in g]


def block_to_images(field,B):
    d = field.d
    gram_columns = [sum(field.trace(field.mul(1<<i,1<<j))<<i for i in range(d))
                    for j in range(d)]
    out = []
    for j in range(d):
        values = sum(((B[i]>>j)&1)<<i for i in range(d))
        c = solve(gram_columns,values)
        assert c is not None
        out.append(c)
    return out


def decode_block(field,B):
    images = block_to_images(field,B)
    g = [1<<i for i in range(field.d)]
    # L composed with Frobenius has exponents 0,1,2.
    received = [linear_apply(images,field.mul(x,x)) for x in g]
    f = gabidulin_decode(field,g,received)
    if f is None:
        return None
    decoded_images = [qeval(field,f,field.pow(x,1<<(field.d-1))) for x in g]
    return bilinear_block(field,decoded_images)


def quadratic_matrix(value,n):
    constant = value(0)
    unary = [value(1<<i)^constant for i in range(n)]
    return [sum((value((1<<i)|(1<<j))^unary[i]^unary[j]^constant)<<j
                for j in range(n) if j!=i) for i in range(n)]


def quadratic_value(B,x):
    return sum((x>>i&1)*((B[i]&x&~((1<<(i+1))-1)).bit_count()&1)
               for i in range(len(B)))&1


def independent(vectors):
    out = []
    for v in vectors:
        if rank(out+[v])>len(out):
            out.append(v)
    return out


def low_rank_alternating(n,r,rng):
    columns = []
    while len(columns)<r:
        v = rng.randrange(1<<n)
        if rank(columns+[v])>len(columns):
            columns.append(v)
    D = [0]*n
    for u,v in zip(columns[::2],columns[1::2]):
        for i in range(n):
            if u>>i&1:
                D[i] ^= v
            if v>>i&1:
                D[i] ^= u
    assert rank(D)==r and all(not (row>>i&1) for i,row in enumerate(D))
    return D


def gaussian_sum(B,a):
    n = len(B)
    poly = {1<<i for i in range(n) if a>>i&1}
    poly |= {(1<<i)|(1<<j) for i in range(n) for j in range(i+1,n) if B[i]>>j&1}
    remaining = set(range(n))
    multiplier = 1
    while True:
        pair = next((m for m in poly if m.bit_count()==2),None)
        if pair is None:
            if any(m for m in poly):
                return 0
            return multiplier*((-1) if 0 in poly else 1)*(1<<len(remaining))
        i,j = [v for v in remaining if pair>>v&1]
        A = {m^(1<<i) for m in poly if m>>i&1 and not (m>>j&1)}
        C = {m^(1<<j) for m in poly if m>>j&1 and not (m>>i&1)}
        poly = {m for m in poly if not m&pair}
        for u in A:
            for v in C:
                m = u|v
                if m in poly:
                    poly.remove(m)
                else:
                    poly.add(m)
        remaining.remove(i)
        remaining.remove(j)
        multiplier *= 2


def acquire_walsh_support(D):
    n = len(D)
    rad = kernel(D)
    target = sum(quadratic_value(D,v)<<i for i,v in enumerate(rad))
    constraints = [sum(((v>>j)&1)<<i for i,v in enumerate(rad)) for j in range(n)]
    a0 = solve(constraints,target)
    assert a0 is not None
    code = independent(D)
    return [a0^linear_apply(code,z) for z in range(1<<len(code))]


def run():
    rng = random.Random(202610272531)
    records,decoder_cases,identity_checks = [],0,0
    # Check the full-field code first, including error rank smaller than t.
    for d in [3,4,5,6,7,9,11]:
        field = fixture_field(d)
        t = (d-3)//2
        g = [1<<i for i in range(d)]
        for s in range(t+1):
            for _ in range(8):
                f = [rng.randrange(field.q) for _ in range(3)]
                span = independent(rng.randrange(field.q) for _ in range(s+3))[:s]
                assert len(span)==s
                errors = [linear_apply(span,rng.randrange(1<<s)) for _ in g]
                received = [qeval(field,f,x)^e for x,e in zip(g,errors)]
                decoded = gabidulin_decode(field,g,received)
                assert decoded==f
                decoder_cases += 1
    for d,r in [(7,0),(7,2),(9,2),(11,4)]:
        field = fixture_field(d)
        n = 3*d
        for trial in range(4):
            forms = random_invertible_field_matrix(field,3,rng)
            F = multiply_linear_forms(field,forms)
            lam = F.get((1,1,1),0)
            assert lam
            quadratic = {(i,j):rng.randrange(field.q) for i in range(3) for j in range(i,3)}
            def background(x):
                X = [(x>>(i*d))&(field.q-1) for i in range(3)]
                z = cubic_value(field,F,X)^field.mul(lam,field.mul(X[0],field.mul(X[1],X[2])))
                for (i,j),c in quadratic.items():
                    z ^= field.mul(c,field.mul(X[i],X[j]))
                return field.trace(z)
            B0 = quadratic_matrix(background,n)
            D = low_rank_alternating(n,r,rng)
            B = [u^v for u,v in zip(B0,D)]
            acquired = [0]*n
            for a in range(3):
                for b in range(3):
                    block = [(B[a*d+i]>>(b*d))&(field.q-1) for i in range(d)]
                    corrected = decode_block(field,block)
                    assert corrected is not None
                    for i,row in enumerate(corrected):
                        acquired[a*d+i] |= row<<(b*d)
            assert acquired==B0
            assert all((acquired[i]>>i&1)==0 for i in range(n))
            assert all((acquired[i]>>j&1)==(acquired[j]>>i&1) for i in range(n) for j in range(n))
            defect = [x^y for x,y in zip(B,acquired)]
            assert defect==D and rank(defect)==r
            support = acquire_walsh_support(defect)
            W = [gaussian_sum(defect,a) for a in support]
            assert len(support)==1<<r and all(abs(w)==1<<(n-r//2) for w in W)
            for _ in range(64):
                x = rng.randrange(1<<n)
                numerator = sum(w*((-1)**((a&x).bit_count()&1)) for a,w in zip(support,W))
                assert numerator == (1<<n)*((-1)**quadratic_value(defect,x))
                identity_checks += 1
            # A parity character is field-linear under the trace pairing.
            for a in support:
                linear = []
                for b in range(3):
                    bits = (a>>(b*d))&(field.q-1)
                    gram = [sum(field.trace(field.mul(1<<i,1<<j))<<i for i in range(d)) for j in range(d)]
                    linear.append(solve(gram,bits))
                for _ in range(8):
                    x = rng.randrange(1<<n)
                    X = [(x>>(i*d))&(field.q-1) for i in range(3)]
                    assert ((a&x).bit_count()&1)==field.trace(sum_xor(field.mul(c,z) for c,z in zip(linear,X)))
            records.append({'field_degree':d,'inputs':n,'defect_rank':r,
                            'decoded_blocks':9,'Walsh_characters':len(support),
                            'background_binary_rank':rank(B0),
                            'defect_scalar_edges':sum(row.bit_count() for row in D)//2})
    gaussian_checks = 0
    for n in range(2,9):
        for _ in range(8):
            D = [0]*n
            for i,j in combinations(range(n),2):
                if rng.randrange(2):
                    D[i] |= 1<<j
                    D[j] |= 1<<i
            a = rng.randrange(1<<n)
            assert gaussian_sum(D,a)==sum((-1)**(quadratic_value(D,x)^((a&x).bit_count()&1)) for x in range(1<<n))
            gaussian_checks += 1
    return {'status':'all exact assertions passed','Gabidulin_decode_cases':decoder_cases,
            'hidden_field_matrix_cases':len(records),'decoded_matrix_blocks':9*len(records),
            'Gaussian_Walsh_identity_checks':identity_checks,'independent_Gaussian_sum_checks':gaussian_checks,
            'records':records,'point_counting_leaf_executed':False,'speed_claim':False}


if __name__=='__main__':
    result = run()
    Path(__file__).with_name('rank_metric_field_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
