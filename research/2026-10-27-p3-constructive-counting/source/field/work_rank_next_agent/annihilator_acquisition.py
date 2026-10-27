#!/usr/bin/env python3
"""Exact raw-matrix acquisition using a sparse part's annihilating polynomial.

Standard-library finite validators. No asymptotic phase counter is implemented.
The decoder receives only B, h and a maximum sparse-row-weight budget.
"""
from itertools import combinations
from pathlib import Path
import json
import random


def independent(words):
    pivots = {}
    basis = []
    for original in words:
        x = original
        while x:
            p = x.bit_length()-1
            if p in pivots:
                x ^= pivots[p]
            else:
                pivots[p] = x
                basis.append(original)
                break
    return basis


def in_span(x, basis):
    return len(independent(basis+[x])) == len(basis)


def matmul(A, B):
    out = []
    for row in A:
        value = 0
        while row:
            bit = row & -row
            value ^= B[bit.bit_length()-1]
            row ^= bit
        out.append(value)
    return out


def matvec(A, vector):
    return sum(((row & vector).bit_count() & 1) << i
               for i, row in enumerate(A))


def transpose(A, width=None):
    width = len(A) if width is None else width
    return [sum(((row >> j)&1) << i for i,row in enumerate(A))
            for j in range(width)]


def polynomial(A, coefficients):
    n = len(A)
    power = [1 << i for i in range(n)]
    result = [0]*n
    for t in range(coefficients.bit_length()):
        if (coefficients >> t)&1:
            result = [x ^ y for x,y in zip(result,power)]
        if t+1 < coefficients.bit_length():
            power = matmul(power,A)
    return result


def codewords(basis):
    word = previous = 0
    yield 0, 0
    for index in range(1, 1 << len(basis)):
        gray = index ^ (index >> 1)
        change = gray ^ previous
        word ^= basis[change.bit_length()-1]
        yield gray, word
        previous = gray


def symmetric(A):
    return A == transpose(A)


def edge_count(A):
    return sum((row & ((1 << i)-1)).bit_count() for i,row in enumerate(A))


def acquire(B, h, delta):
    """Return a checked decomposition, or a concrete failed acquisition test."""
    n = len(B)
    if h < 2 or delta < 0 or not symmetric(B):
        raise ValueError('nonconstant monic polynomial, nonnegative delta, symmetric B required')
    annihilator = polynomial(B,h)
    basis = independent(annihilator)
    distance = n+1
    for coefficient,word in codewords(basis):
        if coefficient:
            distance = min(distance,word.bit_count())
            if distance <= 2*delta:
                return dict(accepted=False, reason='acquired code lacks decoding margin',
                            code_dimension=len(basis), short_weight=distance)
    decoded, residual = [], []
    for column in B:
        found = None
        for _,word in codewords(basis):
            if (column ^ word).bit_count() <= delta:
                assert found is None
                found = word
        if found is None:
            return dict(accepted=False,reason='row has no codeword in budget',
                        code_dimension=len(basis),code_distance=distance)
        decoded.append(found)
        residual.append(found ^ column)
    if not symmetric(decoded) or not symmetric(residual):
        return dict(accepted=False,reason='decoded matrix is not symmetric')
    if any(polynomial(residual,h)):
        return dict(accepted=False,reason='residual fails annihilator identity')
    assert [x ^ y for x,y in zip(decoded,residual)] == B
    return dict(accepted=True,code_generators=basis,code_dimension=len(basis),
                code_distance=distance,low_rank_matrix=decoded,
                low_rank=len(independent(decoded)),sparse_matrix=residual,
                residual_edges=edge_count(residual),
                maximum_residual_row_weight=max(map(int.bit_count,residual),default=0),
                annihilator_polynomial=h)


def alternating_form(columns,n):
    assert len(columns)%2 == 0
    out = [0]*n
    for a in range(0,len(columns),2):
        u,v = columns[a:a+2]
        for i in range(n):
            if (u >> i)&1:
                out[i] ^= v
            if (v >> i)&1:
                out[i] ^= u
    assert symmetric(out)
    assert all(not (row >> i)&1 for i,row in enumerate(out))
    return out


def permute(A, permutation):
    return [sum(((A[permutation[i]] >> permutation[j])&1) << j
                for j in range(len(A))) for i in range(len(A))]


def matching(n):
    assert n%2 == 0
    return [1 << (i^1) for i in range(n)]


def hypercube(d):
    n = 1 << d
    return [sum(1 << (i ^ (1 << a)) for a in range(d)) for i in range(n)]


def path_blocks(length, count):
    n = length*count
    out = [0]*n
    for block in range(count):
        for a in range(length-1):
            i,j = block*length+a,block*length+a+1
            out[i] |= 1 << j
            out[j] |= 1 << i
    p0,p1 = 1,2
    for _ in range(2,length+1):
        p0,p1 = p1,(p1 << 1) ^ p0
    return out,p1


def inverse(rows):
    n = len(rows)
    a = [row | (1 << (n+i)) for i,row in enumerate(rows)]
    for j in range(n):
        pivot = next(i for i in range(j,n) if (a[i] >> j)&1)
        a[j],a[pivot] = a[pivot],a[j]
        for i in range(n):
            if i != j and (a[i] >> j)&1:
                a[i] ^= a[j]
    return [row >> n for row in a]


def core_factor(matrix, columns):
    """Recover the unique H in matrix=W H W^T for full-column-rank W."""
    n,d = len(matrix),len(columns)
    rows = transpose(columns,n)
    J,b = [],[]
    for i,row in enumerate(rows):
        if len(independent(b+[row])) > len(b):
            J.append(i)
            b.append(row)
            if len(J)==d:
                break
    assert len(J)==d
    inv = inverse(b)
    minor = [sum(((matrix[i] >> j)&1) << a for a,j in enumerate(J)) for i in J]
    H = matmul(matmul(inv,minor),transpose(inv))
    assert matmul(matmul(rows,H),columns) == matrix
    return H


def quadratic(A,x):
    return sum(((row & x & ((1 << i)-1)).bit_count()&1)
               for i,row in enumerate(A) if (x >> i)&1)&1


def fixture(S,h,r,seed,finite_count=False):
    rng = random.Random(seed)
    n = len(S)
    permutation = list(range(n))
    rng.shuffle(permutation)
    S = permute(S,permutation)
    q = h.bit_length()-1
    delta = max(map(int.bit_count,S))
    assert not any(polynomial(S,h))
    trials = 0
    while True:
        trials += 1
        if trials > 1000:
            raise AssertionError('fixture search exhausted')
        U = [rng.getrandbits(n) for _ in range(r)]
        W,power = [],list(U)
        for _ in range(q):
            W.extend(power)
            power = [matvec(S,v) for v in power]
        if len(independent(W)) != q*r:
            continue
        distance = min(word.bit_count() for a,word in codewords(W) if a)
        if distance <= 2*delta:
            continue
        D = alternating_form(U,n)
        B = [a ^ b for a,b in zip(D,S)]
        result = acquire(B,h,delta)
        assert result['accepted']
        assert result['low_rank_matrix'] == D
        assert result['sparse_matrix'] == S
        assert result['code_dimension'] == q*r
        assert result['low_rank'] == r
        assert result['code_distance'] == distance
        H = core_factor(polynomial(B,h),W)
        for a in range(q):
            for b in range(q):
                for i in range(r):
                    blockrow = (H[a*r+i] >> (b*r)) & ((1 << r)-1)
                    if a+b > q-1:
                        assert blockrow == 0
                    elif a+b == q-1:
                        assert blockrow == (1 << (i^1))
        pointwise = 0
        for _ in range(min(2000,1 << min(n,12))):
            x = rng.getrandbits(n)
            assert quadratic(B,x) == (quadratic(D,x)^quadratic(S,x))
            pointwise += 1
        output = dict(n=n,rank=r,annihilator_degree=q,annihilator=h,
                      code_dimension=q*r,code_distance=distance,
                      maximum_sparse_degree=delta,residual_edges=edge_count(S),
                      latent_columns=U,raw_matrix=B,acquired_matrix=D,
                      sparse_matrix=S,generation_trials=trials,
                      pointwise_quadratic_identities=pointwise,
                      product_rM=r*edge_count(S),original_n_squared=n*n)
        if finite_count:
            terms=[tuple(rng.sample(range(n),3)) for _ in range(n//2)]
            def foreground(x):
                return sum(all((x >> i)&1 for i in term) for term in terms)&1
            direct = sum((-1 if quadratic(B,x)^foreground(x) else 1)
                         for x in range(1 << n))
            compiled = sum((-1 if quadratic(D,x)^quadratic(S,x)^foreground(x) else 1)
                           for x in range(1 << n))
            assert direct == compiled
            output.update(exhaustive_mixed_phase_assignments=1 << n,
                          exact_phase_sum=direct,local_cubic_terms=terms)
        return output


def main():
    records=[]
    records.append(fixture(matching(12),0b101,2,1,True))
    records.append(fixture(matching(16),0b101,2,2,True))
    for dimension,r,seed in [(5,2,3),(6,2,4),(7,4,5),(9,6,6)]:
        records.append(fixture(hypercube(dimension),0b100 | (dimension%2),r,seed))
    for length,count,seed in [(3,8,7),(4,10,8),(5,10,9),(6,10,10)]:
        S,h = path_blocks(length,count)
        records.append(fixture(S,h,2,seed))
    rejected=[]
    # Full acquired ambient code cannot satisfy the sparse decoding margin.
    for n in [6,10,14]:
        rng=random.Random(100+n)
        B=[0]*n
        for i in range(n):
            for j in range(i):
                if rng.randrange(2):
                    B[i] ^= 1 << j
                    B[j] ^= 1 << i
        result=acquire(B,0b101,1)
        assert not result['accepted']
        rejected.append(dict(n=n,result=result))
    # A nontransverse latent space can disappear entirely under h(B).
    n=16
    S=matching(n)
    D=[(((1 << 8)-1) << 8) if i<8 else ((1 << 8)-1) for i in range(n)]
    B=[a ^ b for a,b in zip(D,S)]
    assert len(independent(D))==2 and not any(polynomial(B,0b101))
    result=acquire(B,0b101,1)
    assert not result['accepted'] and result['reason']=='row has no codeword in budget'
    rejected.append(dict(n=n,mechanism='nontransverse perturbation vanishes under h(B)',result=result))
    # Transversality alone does not supply a Hamming decoding margin.
    n=12
    S=matching(n)
    D=alternating_form([1,4],n)
    B=[a ^ b for a,b in zip(D,S)]
    assert len(independent(polynomial(B,0b101)))==4
    result=acquire(B,0b101,1)
    assert not result['accepted'] and result['reason']=='acquired code lacks decoding margin'
    rejected.append(dict(n=n,mechanism='full orbit rank with small code distance',result=result))
    result=dict(status='all exact assertions passed',fixtures=len(records),
                raw_decompositions_recovered=len(records),
                all_annihilator_core_identities_checked=True,
                finite_mixed_phase_counts=2,
                pointwise_quadratic_identities=sum(x['pointwise_quadratic_identities'] for x in records),
                exhaustive_mixed_phase_assignments=sum(x.get('exhaustive_mixed_phase_assignments',0) for x in records),
                rejection_checks=rejected,records=records,
                asymptotic_phase_engine_executed=False,practical_speed_claim=False)
    destination=Path(__file__).with_name('annihilator_acquisition_results.json')
    destination.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','rejection_checks')},indent=2))
    print(json.dumps([dict(n=x['n'],r=x['rank'],q=x['annihilator_degree'],
                           distance=x['code_distance'],delta=x['maximum_sparse_degree'],
                           residual=x['residual_edges']) for x in records]))


if __name__ == '__main__':
    main()
