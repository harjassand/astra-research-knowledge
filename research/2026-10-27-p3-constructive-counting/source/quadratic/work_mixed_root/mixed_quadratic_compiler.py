#!/usr/bin/env python3
"""Acquire a punctured alternating low-rank+sparse quadratic representation.

Only raw B, rank/error budgets, and a threshold enter acquisition. Hidden
low-rank and error matrices are used only to generate validation fixtures.
The exact finite counter is exhaustive, NOT the asymptotic phase engine.
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


def validate():
    rng=random.Random(2710202604)
    records=[]
    for n,mode in [(6,'none'),(9,'single'),(9,'star'),(12,'matching')]:
        types=[1+(i%3) for i in range(n)]
        A=matrix_from_edges(n,[(i,j) for i in range(n) for j in range(i)
                              if parity(types[i]&((types[j]>>1)|((types[j]&1)<<1)))])
        if mode=='none':edges=[]
        elif mode=='single':edges=[(0,1)]
        elif mode=='star':edges=[(0,j) for j in range(1,6)]
        else:edges=[(i,i+1) for i in range(0,n,2)]
        S=matrix_from_edges(n,edges)
        B=[a^s for a,s in zip(A,S)]
        # The public search sees B only; A and S are NOT passed to it.
        certificate=acquire(B,2,len(edges),threshold=1,total_removal_cap=min(n-3,5))
        assert certificate is not None
        assert [a^s for a,s in zip(certificate['low_rank_matrix'],certificate['sparse_matrix'])]==restrict(B,certificate['retained'])
        for b in (1,3):
            terms=[(sum(1<<j for j in range(i,min(n,i+3))),rng.randrange(1,1<<b))
                   for i in range(0,n,3)]
            terms += [(sum(1<<j for j in rng.sample(range(n),3)),rng.randrange(1,1<<b)) for _ in range(n)]
            expected=exact_original(B,terms,b)
            actual,normalization=exact_compiled(B,terms,b,certificate)
            assert actual==expected
            records.append(dict(inputs=n,phase_order=1<<b,mode=mode,
                                matrix_edges=edge_count(B),matrix_rank=len(independent(B)),
                                hidden_low_rank=len(independent(A)),hidden_errors=len(edges),
                                local_terms=terms,raw_matrix=B,certificate=certificate,
                                normalization=normalization,exact_sum=actual))
    gaussian_checks=0
    for n in range(7):
        for _ in range(5):
            rows=matrix_from_edges(n,[(i,j) for i in range(n) for j in range(i) if rng.randrange(2)])
            for linear in range(1<<n):
                expected=sum((-1)**(quadratic(x,rows)^parity(x&linear)) for x in range(1<<n))
                assert gaussian_sum(rows,linear)==expected
                gaussian_checks+=1
    C=matrix_from_edges(3,[(0,1),(0,2),(1,2)])
    U=independent(C)
    K,ell=compact_quadratic(C,U)
    assert ell != 0
    for x in range(8):
        latent=sum(parity(u&x)<<j for j,u in enumerate(U))
        assert quadratic(x,C)==(quadratic(latent,K)^parity(ell&x))
    return dict(status='all exact assertions passed',seed=2710202604,
                mixed_count_checks=len(records),gaussian_checks=gaussian_checks,
                unary_correction_checks=8,fixtures=records,
                backend='raw acquisition plus exhaustive exact finite phase sums; no asymptotic engine')


if __name__=='__main__':
    results=validate()
    path=Path(__file__).with_name('mixed_quadratic_results.json')
    path.write_text(json.dumps(results,indent=2)+'\n')
    summary={k:v for k,v in results.items() if k!='fixtures'}
    summary['acquired_profiles']=[dict(n=v['inputs'],mode=v['mode'],B_rank=v['matrix_rank'],
        deleted=len(v['certificate']['removed']),rank=v['certificate']['low_rank'],
        residual=v['certificate']['residual_edges'],candidates=v['certificate']['candidates_examined'])
        for v in results['fixtures'][::2]]
    print(json.dumps(summary))
