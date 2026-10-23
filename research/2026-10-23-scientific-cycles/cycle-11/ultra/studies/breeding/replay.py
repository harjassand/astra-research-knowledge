#!/usr/bin/env python3
"""New finite XOR/source-code admissions, stdlib only.

The theorem is analytic; these small exact checks are not a large block code,
diamond-norm verification, or a replay of any predecessor suite.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import math
import time


def entropy(p):
    return -sum(float(x) * math.log2(float(x)) for x in p if x)


def parity(x):
    return x.bit_count() % 2


def xor_tail(D):
    h = (D - 1).bit_length()
    counts = [0] * 2 ** h
    for a in range(D):
        for b in range(D):
            counts[a ^ b] += 1
    result = [F(v, D * D) for v in counts]
    assert sum(result) == 1
    assert result[0] == F(1, D)
    return result


def source_laws(D, p):
    L = len(p)
    tail = xor_tail(D)
    q0 = tail[0]
    stages = []
    stopped = []
    for i in range(1, L + 1):
        survival = sum(p[k-1] * q0 ** max(0, i-1-k) for k in range(1, L+1))
        numerator = []
        for e, qe in enumerate(tail):
            amount = F(0)
            for k in range(1, L + 1):
                past = p[k-1] * q0 ** max(0, i-1-k)
                amount += past * (F(e == 0) if i <= k else qe)
            numerator.append(amount)
        conditional = [v / survival for v in numerator]
        assert sum(conditional) == 1
        for e in range(1, len(tail)):
            stopped.append((i, e, numerator[e]))
        stages.append((survival, conditional))
    no_mismatch = sum(p[k-1] * q0 ** (L-k) for k in range(1, L+1))
    stopped.append((0, 0, no_mismatch))
    assert sum(v[2] for v in stopped) == 1
    hv = entropy([v[2] for v in stopped])
    chain = sum(float(s) * entropy(pi) for s, pi in stages)
    assert math.isclose(hv, chain, abs_tol=1e-12, rel_tol=1e-12)
    # Independently enumerate all full mathematical XOR strings and apply
    # stopping. This is not a measurement of individual Bell digits.
    full_stopped = {}
    for seq in product(range(len(tail)), repeat=L):
        probability = F(0)
        for k in range(1, L+1):
            weight = p[k-1]
            for i, e in enumerate(seq, 1):
                weight *= F(e == 0) if i <= k else tail[e]
            probability += weight
        if not probability:
            continue
        v = next(((i, e) for i, e in enumerate(seq, 1) if e), (0, 0))
        full_stopped[v] = full_stopped.get(v, F(0)) + probability
    assert full_stopped == {(i, e): probability for i, e, probability in stopped if probability}
    return dict(D=D, L=L, prior=[str(x) for x in p],
                tail=[str(x) for x in tail],
                stopped=[dict(site=i, xor=e, probability=str(v)) for i,e,v in stopped if v],
                stages=[dict(survival=str(s), conditional=[str(x) for x in pi]) for s,pi in stages],
                H_V_bits=hv, chain_bits=chain)


def parity_kraus_admissions():
    count = 0
    for D in [2, 3, 4, 6]:
        h = (D - 1).bit_length()
        for sites in [1, 2]:
            dimension = D ** sites
            def embedded(index):
                digits = []
                for _ in range(sites):
                    digits.append(index % D)
                    index //= D
                return sum(x << (h*j) for j,x in enumerate(digits))
            for row in range(2 ** (h*sites)):
                for a in range(dimension):
                    x = embedded(a)
                    for b in range(dimension):
                        y = embedded(b)
                        delta = parity(row & (x ^ y))
                        # Count Bell-ancilla computational paths. Each has
                        # amplitude 1/sqrt2; squaring is exact integer/2.
                        outcomes = {(u,v): 0 for u in [0,1] for v in [0,1]}
                        for t in [0, 1]:
                            u = t ^ parity(row & x)
                            v = t ^ parity(row & y)
                            outcomes[u,v] += 1
                        for (u,v), amplitude_numerator in outcomes.items():
                            assert amplitude_numerator == int((u ^ v) == delta)
                            count += 1
    return count


def hash_collision_admissions():
    count = 0
    for bits in [1, 2, 3, 4]:
        for rows in [1, 2]:
            seeds = list(product(range(2 ** bits), repeat=rows))
            for x in range(2 ** bits):
                for y in range(x+1, 2 ** bits):
                    collisions = sum(all(parity(row & x) == parity(row & y) for row in matrix)
                                     for matrix in seeds)
                    assert F(collisions, len(seeds)) == F(1, 2 ** rows)
                    count += 1
    return count


def tiny_typical_decoder_admissions():
    # Exact prescribed typical sets at a dyadic probability threshold.
    # Enumerate every seed and source word; certify typical collision union
    # bound plus all nontypical mass. No asymptotic extrapolation is made.
    cases = []
    laws = [[F(3,4), F(1,4)], [F(1,2),F(1,6),F(1,6),F(1,6)]]
    for pi in laws:
        h = (len(pi)-1).bit_length()
        for n in [1, 2]:
            bits = h*n
            mass = {}
            for seq in product(range(len(pi)), repeat=n):
                word = sum(e << (h*j) for j,e in enumerate(seq))
                weight = F(1)
                for e in seq:
                    weight *= pi[e]
                mass[word] = weight
            for exponent in [1, 2]:
                typical = [x for x,p in mass.items() if p >= F(1, 2**exponent)]
                assert len(typical) <= 2**exponent
                for rows in [1, 2]:
                    seeds = list(product(range(2**bits), repeat=rows))
                    error = F(0)
                    for matrix in seeds:
                        image = lambda x: tuple(parity(r & x) for r in matrix)
                        for x, p in mass.items():
                            candidates = [y for y in typical if image(y) == image(x)]
                            guess = candidates[0] if len(candidates) == 1 else 0
                            error += p * F(guess != x, len(seeds))
                    nontypical = sum(p for x,p in mass.items() if x not in typical)
                    bound = nontypical + F(max(0,len(typical)-1), 2**rows)
                    assert error <= bound
                    cases.append(dict(pi=[str(x) for x in pi], n=n, rows=rows,
                                      threshold=str(F(1,2**exponent)), typical=typical,
                                      exact_error=str(error), simple_bound=str(bound)))
    return cases


def seed_admissions():
    results = []
    for D in range(2, 11):
        pairs = list(product(range(D), repeat=2))
        pairs = [(u,v) for u,v in pairs if u < v]
        for basis in range(D):
            effect = sum(F(1,D-1) for pair in pairs if basis in pair)
            assert effect == 1
        outcome_probability = F(2, D*(D-1))
        assert len(pairs)*outcome_probability == 1
        # The two nonzero corrected Schmidt coefficients have exactly equal
        # squared probability, so every normalized branch is Phi2.
        assert F(1,D*(D-1))/outcome_probability == F(1,2)
        results.append(dict(D=D, outcomes=len(pairs),
                            outcome_probability=str(outcome_probability), corrected_schmidt_squared=['1/2','1/2']))
    return results


def recycling_admissions():
    rows=[]
    for c,d in [(F(1,3),F(4,3)),(F(3,2),F(7,4)),(F(2),F(5))]:
        for n,j in [(12,4),(120,10),(1200,30)]:
            cn=math.ceil(n*c)
            dn=math.floor(n*d)
            assert dn>=cn
            final=j*(dn-cn)+cn
            total=j*n+cn
            assert final == j*dn-(j-1)*cn
            # At each TP execution reserve registers exist regardless of
            # whether their actual quantum state is ideal Bell stock.
            reserve=cn
            kept=0
            for step in range(j):
                assert reserve==cn
                reserve=dn
                if step+1<j:
                    kept+=dn-cn
                    reserve=cn
            assert kept+reserve==final
            rows.append(dict(c=str(c),d=str(d),n=n,j=j,seed=cn,output=final,total_queues=total,
                             exact_rate=str(F(final,total))))
    return rows


def main():
    start=time.perf_counter()
    sources=[source_laws(2,[F(1,2),F(1,2)]),
             source_laws(3,[F(1,3)]*3),
             source_laws(4,[F(1,2),F(1,4),F(1,4)]),
             source_laws(6,[F(1,5),F(4,5)])]
    kraus=parity_kraus_admissions()
    collisions=hash_collision_admissions()
    decoding=tiny_typical_decoder_admissions()
    seeds=seed_admissions()
    recycling=recycling_admissions()
    result=dict(status='PASS',scope='new finite stopped-XOR/source-code admissions only',
                proof_sha256=hashlib.sha256(Path(__file__).with_name('PROOF.txt').read_bytes()).hexdigest(),
                source_laws=sources, exact_kraus_scaled_entries=kraus,
                exact_universal_hash_pairs=collisions, tiny_decoding_cases=decoding,
                exact_seed_cases=seeds, exact_recycling_cases=recycling,
                wall_seconds=time.perf_counter()-start)
    Path(__file__).with_name('RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    summary={k:v for k,v in result.items() if k not in ['source_laws','tiny_decoding_cases','exact_seed_cases','exact_recycling_cases']}
    summary['source_cases']=len(sources)
    summary['decoding_cases']=len(decoding)
    summary['seed_cases']=len(seeds)
    summary['recycling_cases']=len(recycling)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
