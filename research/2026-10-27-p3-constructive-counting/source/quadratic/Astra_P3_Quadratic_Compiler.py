#!/usr/bin/env python3
"""Astra P3 exact finite representation compiler.

Standalone Python 3 standard-library edition of the executed implementation.
The algorithm acquires symmetric low-rank completions with sparse residuals.
The finite inner phase counter enumerates inputs; it does not implement the
asymptotic replacement-form engine proved in the companion paper.

Run: python3 Astra_P3_Quadratic_Compiler.py
It executes deterministic exact validations and writes the result JSON.
The public functions acquire_symmetric and exact_compiled_symmetric are
available for custom raw matrices; see their definitions and validate().
"""
from itertools import combinations
from math import isqrt
from pathlib import Path
import json
import random


def parity(x): return x.bit_count() & 1


def xor_all(xs):
    out = 0
    for x in xs: out ^= x
    return out


def independent(xs):
    pivots, selected = {}, []
    for value in xs:
        x = value
        while x:
            p = x.bit_length()-1
            if p in pivots: x ^= pivots[p]
            else:
                pivots[p] = x
                selected.append(value)
                break
    return selected


def pack(mask, positions):
    return sum(((mask >> old) & 1) << new for new, old in enumerate(positions))


def unpack(mask, positions):
    return sum(((mask >> new) & 1) << old for new, old in enumerate(positions))


def codewords(generators):
    for coefficients in range(1 << len(generators)):
        yield coefficients, xor_all(v for i, v in enumerate(generators)
                                     if coefficients >> i & 1)


def alternating(rows):
    n = len(rows)
    return all(not (rows[i] >> i & 1) for i in range(n)) and all(
        ((rows[i] >> j) & 1) == ((rows[j] >> i) & 1)
        for i in range(n) for j in range(i))


def edge_count(rows): return sum(row.bit_count() for row in rows)//2


def restrict(rows, positions): return [pack(rows[i], positions) for i in positions]


def quadratic(mask, rows):
    return xor_all(parity(rows[i] & mask & ((1 << i)-1))
                   for i in range(len(rows)) if mask >> i & 1)


def candidate(B, pivots, initially_removed, threshold, error_budget,
              total_removal_cap=None):
    """Puncture short codewords, decode, and verify actual matrix equality."""
    n = len(B)
    removed = set(initially_removed)
    punctures = []
    while True:
        retained = [i for i in range(n) if i not in removed]
        U = independent([pack(B[i], retained) for i in pivots])
        short = None
        minimum = len(retained)+1
        for coefficients, word in codewords(U):
            if not coefficients: continue
            minimum = min(minimum, word.bit_count())
            if word.bit_count() <= 2*threshold:
                short = coefficients, word
                break
        if short is None: break
        coefficients, word = short
        support = [retained[j] for j in range(len(retained)) if word >> j & 1]
        assert support and len(support) <= 2*threshold
        before = len(U)
        removed.update(support)
        new_retained = [i for i in range(n) if i not in removed]
        after = len(independent([pack(B[i], new_retained) for i in pivots]))
        assert after < before
        punctures.append(dict(support=support, coefficients=coefficients,
                              rank_before=before, rank_after=after))
        if total_removal_cap is not None and len(removed) > total_removal_cap:
            return None
    assert len(punctures) <= len(pivots)
    if total_removal_cap is not None and len(removed) > total_removal_cap:
        return None
    target = restrict(B, retained)
    columns = []
    distances = []
    for column in target:
        decoded = None
        for _, word in codewords(U):
            distance = (column ^ word).bit_count()
            if distance <= threshold:
                assert decoded is None
                decoded = word
                decoded_distance = distance
        if decoded is None: return None
        columns.append(decoded)
        distances.append(decoded_distance)
    if not alternating(columns): return None
    sparse = [x ^ y for x, y in zip(target, columns)]
    if edge_count(sparse) > error_budget: return None
    assert len(independent(columns)) <= len(U)
    return dict(pivots=list(pivots), initially_removed=list(initially_removed),
                removed=sorted(removed), retained=retained, code_generators=U,
                final_code_dimension=len(U), minimum_code_distance=minimum,
                punctures=punctures, decoded_column_distances=distances,
                low_rank_matrix=columns, sparse_matrix=sparse,
                low_rank=len(independent(columns)), residual_edges=edge_count(sparse))


def acquire(B, rank_budget, error_budget, threshold=None,
            max_initial_removed=None, total_removal_cap=None):
    assert alternating(B)
    n = len(B)
    if rank_budget == 0:
        if edge_count(B) <= error_budget:
            return dict(pivots=[], initially_removed=[], removed=[], retained=list(range(n)),
                        code_generators=[], final_code_dimension=0,
                        minimum_code_distance=n+1, punctures=[],
                        decoded_column_distances=[row.bit_count() for row in B],
                        low_rank_matrix=[0]*n, sparse_matrix=list(B), low_rank=0,
                        residual_edges=edge_count(B), candidates_examined=1, threshold=0,
                        method='direct sparse certificate; no radius decoding')
        return None
    if threshold is None:
        threshold = max(1, isqrt((2*error_budget)//(3*rank_budget)))
        while 3*rank_budget*threshold*threshold < 2*error_budget: threshold += 1
    if threshold < 1: raise ValueError('positive threshold required')
    bound = min(n, (2*error_budget+threshold-1)//threshold+rank_budget*threshold)
    if max_initial_removed is not None: bound = min(bound, max_initial_removed)
    examined = 0
    for size in range(bound+1):
        for E in combinations(range(n), size):
            for d in range(min(rank_budget,n)+1):
                for I in combinations(range(n),d):
                    examined += 1
                    result = candidate(B,I,E,threshold,error_budget,total_removal_cap)
                    if result is not None:
                        result.update(candidates_examined=examined, threshold=threshold,
                                      initial_removal_bound=bound)
                        return result
    return None


def inverse(rows):
    n = len(rows)
    data = [row | (1 << (n+i)) for i,row in enumerate(rows)]
    for i in range(n):
        pivot = next((j for j in range(i,n) if data[j] >> i & 1), None)
        if pivot is None: raise ValueError('singular matrix')
        data[i],data[pivot] = data[pivot],data[i]
        for j in range(n):
            if j != i and data[j] >> i & 1: data[j] ^= data[i]
    return [row >> n for row in data]


def transpose(rows, ncols):
    return [sum(((row >> j)&1) << i for i,row in enumerate(rows)) for j in range(ncols)]


def multiply(A,B):
    return [xor_all(B[j] for j in range(len(B)) if row >> j & 1) for row in A]


def compact_quadratic(C, U):
    """C=U K U^T and q_C(x)=q_K(U^T x)+ell.x; keep unary correction."""
    n, d = len(C),len(U)
    rows_U = transpose(U,n)
    basis, J = [],[]
    for i,row in enumerate(rows_U):
        if len(independent(basis+[row])) > len(basis):
            basis.append(row);J.append(i)
        if len(J)==d: break
    assert len(J)==d
    inv = inverse(basis)
    CJJ = restrict(C,J)
    K = multiply(multiply(inv,CJJ),transpose(inv,d))
    reconstructed = multiply(multiply(rows_U,K),U)
    assert reconstructed == C and alternating(K)
    ell = sum(quadratic(row,K) << i for i,row in enumerate(rows_U))
    return K,ell


def gaussian_sum(rows, linear=0):
    """Exact quadratic Boolean Gauss sum in polynomial time and space."""
    n=len(rows)
    terms={1<<i for i in range(n) if linear >> i & 1}
    terms.update((1<<i)|(1<<j) for i in range(n) for j in range(i)
                 if rows[i] >> j & 1)
    active=set(range(n)); factor=1
    while True:
        edge=next((s for s in terms if s.bit_count()==2),None)
        if edge is None: break
        i=(edge&-edge).bit_length()-1
        j=(edge^(1<<i)).bit_length()-1
        bi,bj=1<<i,1<<j
        A={s^bi for s in terms if s&bi and not s&bj}
        D={s^bj for s in terms if s&bj and not s&bi}
        out={s for s in terms if not s&(bi|bj)}
        for a in A:
            for b in D:
                term=a|b
                if term in out: out.remove(term)
                else: out.add(term)
        terms=out;active.remove(i);active.remove(j);factor*=2
    if any(s for s in terms): return 0
    return (-factor if 0 in terms else factor) << len(active)


def root_vector(exponent,b):
    d=1<<(b-1);exponent%=2*d
    result=[0]*d;result[exponent%d]=1 if exponent<d else -1
    return result


def finite_phase(n,terms,b):
    answer=[0]*(1<<(b-1))
    for x in range(1<<n):
        exponent=sum(c for s,c in terms if x&s==s)
        value=root_vector(exponent,b)
        answer=[a+v for a,v in zip(answer,value)]
    return answer


def exact_original(B,terms,b):
    qhalf=1<<(b-1)
    augmented=list(terms)+[((1<<i)|(1<<j),qhalf)
                          for i in range(len(B)) for j in range(i) if B[i]>>j&1]
    return finite_phase(len(B),augmented,b)


def exact_compiled(B,terms,b,certificate):
    E,R=certificate['removed'],certificate['retained']
    U=certificate['code_generators'];d=len(U)
    K,ell=compact_quadratic(certificate['low_rank_matrix'],U)
    sparse=certificate['sparse_matrix'];half=1<<(b-1)
    answer=[0]*half
    Emask=sum(1<<i for i in E)
    nonzero_characters=0
    for fixed in range(1<<len(E)):
        original_fixed=unpack(fixed,E)
        base=[]
        for support,coefficient in terms:
            selected=support&Emask
            if original_fixed&selected==selected:
                base.append((pack(support&~Emask,R),coefficient))
        base += [((1<<i)|(1<<j),half) for i in range(len(R)) for j in range(i)
                 if sparse[i]>>j&1]
        cross=sum(parity(B[old]&original_fixed)<<i for i,old in enumerate(R))
        if quadratic(original_fixed,B):base.append((0,half))
        numerator=[0]*half
        for character,word in codewords(U):
            G=gaussian_sum(K,character)
            if not G:continue
            nonzero_characters+=1
            linear=cross^ell^word
            local=base+[(1<<i,half) for i in range(len(R)) if linear>>i&1]
            value=finite_phase(len(R),local,b)
            numerator=[a+G*v for a,v in zip(numerator,value)]
        assert all(v%(1<<d)==0 for v in numerator)
        answer=[a+(v>>d) for a,v in zip(answer,numerator)]
    return answer,dict(branches=1<<len(E),latent_dimension=d,
                       nonzero_character_calls=nonzero_characters,
                       unary_correction=ell,latent_quadratic=K)


def matrix_from_edges(n,edges):
    rows=[0]*n
    for i,j in edges:
        if i==j:raise ValueError('loop')
        rows[i]^=1<<j;rows[j]^=1<<i
    return rows


def symmetric(rows):
    return all(((rows[i] >> j) & 1) == ((rows[j] >> i) & 1)
               for i in range(len(rows)) for j in range(i))


def off_diagonal(rows):
    return [row & ~(1 << i) for i, row in enumerate(rows)]


def quadratic4(x, rows):
    return (sum((rows[i] >> i) & 1 for i in range(len(rows)) if x >> i & 1)
            + 2*quadratic(x, rows)) % 4


def candidate_symmetric(B, pivots, initially_removed, threshold, error_budget,
                        total_removal_cap=None):
    """Threshold bounds sparse off-diagonal degree; decoding radius adds one."""
    radius = threshold + 1
    removed = set(initially_removed)
    punctures = []
    while True:
        retained = [i for i in range(len(B)) if i not in removed]
        U = independent([pack(B[i], retained) for i in pivots])
        short = None
        minimum = len(retained)+1
        for coefficients, word in codewords(U):
            if not coefficients:
                continue
            minimum = min(minimum, word.bit_count())
            if word.bit_count() <= 2*radius:
                short = word
                break
        if short is None:
            break
        support = [retained[i] for i in range(len(retained)) if short >> i & 1]
        before = len(U)
        removed.update(support)
        new_retained = [i for i in range(len(B)) if i not in removed]
        after = len(independent([pack(B[i], new_retained) for i in pivots]))
        assert after < before
        punctures.append(dict(support=support, rank_before=before, rank_after=after))
        if total_removal_cap is not None and len(removed) > total_removal_cap:
            return None
    assert len(punctures) <= len(pivots)
    if total_removal_cap is not None and len(removed) > total_removal_cap:
        return None
    target = restrict(B, retained)
    decoded, distances = [], []
    for column in target:
        close = None
        for _, word in codewords(U):
            distance = (word ^ column).bit_count()
            if distance <= radius:
                assert close is None
                close = word
                recorded_distance = distance
        if close is None:
            return None
        decoded.append(close)
        distances.append(recorded_distance)
    if not symmetric(decoded):
        return None
    sparse = [x ^ y for x, y in zip(target, off_diagonal(decoded))]
    assert alternating(sparse)
    if edge_count(sparse) > error_budget:
        return None
    assert len(independent(decoded)) <= len(U)
    return dict(pivots=list(pivots), initially_removed=list(initially_removed),
                removed=sorted(removed), retained=retained, code_generators=U,
                final_code_dimension=len(U), minimum_code_distance=minimum,
                punctures=punctures, decoded_column_distances=distances,
                low_rank_matrix=decoded, sparse_matrix=sparse,
                low_rank=len(independent(decoded)), residual_edges=edge_count(sparse))


def acquire_symmetric(B, rank_budget, error_budget, threshold=None,
                      max_initial_removed=None, total_removal_cap=None):
    """Complete unordered-subset search; optional caps only restrict finite tests."""
    assert alternating(B)
    n = len(B)
    if rank_budget == 0:
        if edge_count(B) > error_budget:
            return None
        return dict(pivots=[], initially_removed=[], removed=[], retained=list(range(n)),
                    code_generators=[], final_code_dimension=0,
                    minimum_code_distance=n+1, punctures=[],
                    decoded_column_distances=[x.bit_count() for x in B],
                    low_rank_matrix=[0]*n, sparse_matrix=list(B), low_rank=0,
                    residual_edges=edge_count(B), candidates_examined=1, threshold=0,
                    method='direct sparse certificate')
    if threshold is None:
        radius = max(1, isqrt((2*error_budget)//(3*rank_budget)))
        while 3*rank_budget*radius*radius < 2*error_budget:
            radius += 1
        threshold = radius-1
    if threshold < 0:
        raise ValueError('nonnegative off-diagonal degree threshold required')
    radius = threshold+1
    bound = min(n, (2*error_budget)//radius+rank_budget*radius)
    if max_initial_removed is not None:
        bound = min(bound, max_initial_removed)
    examined = 0
    for size in range(bound+1):
        for E in combinations(range(n), size):
            for d in range(min(rank_budget,n)+1):
                for I in combinations(range(n), d):
                    examined += 1
                    result = candidate_symmetric(B, I, E, threshold, error_budget,
                                                 total_removal_cap)
                    if result is not None:
                        result.update(candidates_examined=examined, threshold=threshold,
                                      decoding_radius=radius,
                                      initial_removal_bound=bound)
                        return result
    return None


def compact_symmetric(D, U):
    """D=UKU^T and Q_D(x)=Q_K(U^T x)+2 ell.x modulo four."""
    n, d = len(D), len(U)
    rows_U = transpose(U,n)
    basis, J = [], []
    for i, row in enumerate(rows_U):
        if len(independent(basis+[row])) > len(basis):
            basis.append(row)
            J.append(i)
        if len(J) == d:
            break
    assert len(J) == d
    inv = inverse(basis)
    K = multiply(multiply(inv,restrict(D,J)),transpose(inv,d))
    assert symmetric(K)
    assert multiply(multiply(rows_U,K),U) == D
    ell = 0
    for i, row in enumerate(rows_U):
        difference = (((D[i] >> i)&1)-quadratic4(row,K)) % 4
        assert difference in (0,2)
        ell |= (difference//2) << i
    return K, ell


def gaussian_i_sum(K, character=0):
    """Exact sum i^[Q_K(z)+2 character.z] in Z[i], polynomial time/space."""
    n = len(K)
    a = [((K[i] >> i)&1)+2*((character >> i)&1) for i in range(n)]
    B = off_diagonal(K)
    active = set(range(n))
    factor = (1,0)
    while True:
        i = next((j for j in active if a[j] % 2), None)
        if i is None:
            break
        ai = a[i]
        sign = 1 if ai == 1 else -1
        u,v = factor
        factor = (u-sign*v, v+sign*u)
        neighbors = [j for j in active if j != i and (B[i] >> j)&1]
        for j in neighbors:
            a[j] = (a[j]-ai) % 4
        for j_index,j in enumerate(neighbors):
            for k in neighbors[:j_index]:
                B[j] ^= 1 << k
                B[k] ^= 1 << j
        active.remove(i)
        for j in active:
            B[j] &= ~(1 << i)
    R = sorted(active)
    linear = sum((a[j]//2) << i for i,j in enumerate(R))
    integer = gaussian_sum(restrict(B,R),linear)
    return factor[0]*integer, factor[1]*integer


def multiply_i_vector(value):
    """Multiply an integral cyclotomic coordinate vector by i; root order >=4."""
    dimension = len(value)
    assert dimension >= 2
    result = [0]*dimension
    for j,v in enumerate(value):
        shifted = j+dimension//2
        if shifted >= dimension:
            result[shifted-dimension] -= v
        else:
            result[shifted] += v
    return result


def exact_compiled_symmetric(B, terms, b, certificate):
    """Execute branch/Fourier identities using exhaustive finite inner sums."""
    effective_b = max(2,b)
    half,quarter = 1 << (effective_b-1),1 << (effective_b-2)
    scale = 1 << (effective_b-b)
    E,R = certificate['removed'],certificate['retained']
    U = certificate['code_generators']
    d = len(U)
    D,S = certificate['low_rank_matrix'],certificate['sparse_matrix']
    K,ell = compact_symmetric(D,U)
    Emask = sum(1 << i for i in E)
    answer = [0]*half
    calls = 0
    for fixed in range(1 << len(E)):
        original_fixed = unpack(fixed,E)
        base = []
        for support,coefficient in terms:
            selected = support & Emask
            if original_fixed & selected == selected:
                base.append((pack(support & ~Emask,R),scale*coefficient))
        base += [((1 << i)|(1 << j),half) for i in range(len(R)) for j in range(i)
                 if S[i] >> j & 1]
        base += [(1 << i,-quarter) for i in range(len(R)) if D[i] >> i & 1]
        cross = sum(parity(B[old]&original_fixed) << i for i,old in enumerate(R))
        if quadratic(original_fixed,B):
            base.append((0,half))
        numerator = [0]*half
        for character,word in codewords(U):
            re,im = gaussian_i_sum(K,character)
            if not re and not im:
                continue
            calls += 1
            linear = cross ^ ell ^ word
            local = base+[(1 << i,half) for i in range(len(R)) if linear >> i & 1]
            value = finite_phase(len(R),local,effective_b)
            ivalue = multiply_i_vector(value)
            numerator = [u+re*v+im*w for u,v,w in zip(numerator,value,ivalue)]
        assert all(v % (1 << d) == 0 for v in numerator)
        answer = [u+(v >> d) for u,v in zip(answer,numerator)]
    if b == 1:
        assert all(v == 0 for v in answer[1:])
        answer = answer[:1]
    return answer,dict(branches=1 << len(E),latent_dimension=d,
                       nonzero_character_calls=calls,unary_correction=ell,
                       diagonal_correction=sum(((D[i] >> i)&1) << i for i in range(len(D))),
                       latent_symmetric_form=K,effective_phase_order=1 << effective_b)


def validate():
    rng = random.Random(2710202605)
    gaussian_checks = substitution_checks = 0
    for d in range(5):
        slots = [(i,j) for i in range(d) for j in range(i+1)]
        for mask in range(1 << len(slots)):
            K = [0]*d
            for h,(i,j) in enumerate(slots):
                if mask >> h & 1:
                    K[i] |= 1 << j
                    K[j] |= 1 << i
            for character in range(1 << d):
                expected = [0,0]
                for x in range(1 << d):
                    exponent = (quadratic4(x,K)+2*parity(x&character)) % 4
                    expected[exponent % 2] += 1 if exponent < 2 else -1
                assert gaussian_i_sum(K,character) == tuple(expected)
                gaussian_checks += 1
    for n in range(1,10):
        for d in range(min(n,4)+1):
            U = independent([rng.randrange(1 << n) for _ in range(d)])
            d = len(U)
            K = [0]*d
            for i in range(d):
                for j in range(i+1):
                    if rng.randrange(2):
                        K[i] |= 1 << j
                        K[j] |= 1 << i
            D = multiply(multiply(transpose(U,n),K),U)
            compact,ell = compact_symmetric(D,U)
            for x in range(1 << n):
                z = sum(parity(u&x) << i for i,u in enumerate(U))
                assert quadratic4(x,D) == (quadratic4(z,compact)+2*parity(x&ell)) % 4
                substitution_checks += 1
    records = []
    for n,mode in [(8,'clique'),(12,'clique_matching'),(14,'rank_two_one_error')]:
        if mode.startswith('clique'):
            U = [(1 << n)-1]
            K = [1]
            edges = [] if mode == 'clique' else [(0,1),(2,3),(4,5)]
        else:
            types = [1+(i%3) for i in range(n)]
            U = [sum(((t >> j)&1) << i for i,t in enumerate(types)) for j in range(2)]
            K = [1,2]
            edges = [(0,1)]
        D = multiply(multiply(transpose(U,n),K),U)
        S = matrix_from_edges(n,edges)
        B = [x ^ y for x,y in zip(off_diagonal(D),S)]
        certificate = acquire_symmetric(B,len(U),len(edges),threshold=1,
                                        total_removal_cap=4)
        assert certificate is not None
        assert [x ^ y for x,y in zip(off_diagonal(certificate['low_rank_matrix']),
                                    certificate['sparse_matrix'])] == restrict(B,certificate['retained'])
        for b in (1,2,3):
            terms = [(sum(1 << j for j in rng.sample(range(n),3)),rng.randrange(1,1 << b))
                     for _ in range(n)]
            expected = exact_original(B,terms,b)
            actual,normalization = exact_compiled_symmetric(B,terms,b,certificate)
            assert actual == expected
            records.append(dict(inputs=n,mode=mode,phase_order=1 << b,
                                raw_matrix=B,raw_matrix_rank=len(independent(B)),
                                hidden_completion_rank=len(independent(D)),
                                hidden_error_edges=len(edges),terms=terms,
                                certificate=certificate,normalization=normalization,
                                exact_sum=actual))
    return dict(status='all exact assertions passed',seed=2710202605,
                gaussian_checks=gaussian_checks,quadratic_refinement_checks=substitution_checks,
                mixed_count_checks=len(records),fixtures=records,
                backend='raw acquisition plus exhaustive exact finite phase sums; no asymptotic engine')


if __name__ == '__main__':
    results = validate()
    Path(__file__).with_name('Astra_P3_Quadratic_Compiler_results.json').write_text(
        json.dumps(results,indent=2)+'\n')
    summary = {k:v for k,v in results.items() if k != 'fixtures'}
    summary['acquired_profiles'] = [dict(n=v['inputs'],mode=v['mode'],
        B_rank=v['raw_matrix_rank'],deleted=len(v['certificate']['removed']),
        completion_rank=v['certificate']['low_rank'],residual=v['certificate']['residual_edges'],
        candidates=v['certificate']['candidates_examined']) for v in results['fixtures'][::3]]
    print(json.dumps(summary))
