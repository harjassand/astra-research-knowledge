#!/usr/bin/env python3
"""Rank-one moment transfer plus four positive defect states; owned exact checks."""
from fractions import Fraction
from itertools import product
from pathlib import Path
from random import Random
from time import perf_counter
import json

from fixed_rank_micro_sampler import QI, TaggedSampler, det, sub


def add(a, b, cap):
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
            for i in range(cap+1)]


def conv(a, b, cap):
    out = [QI() for _ in range(cap+1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i+j <= cap:
                out[i+j] = out[i+j] + x*y
    return out


def conjugate(values):
    return [x.conj() if isinstance(x, QI) else x for x in values]


def local_table(sampler, t, fixed=None):
    B, off = sampler.blocks[t], sampler.offsets[t]
    cap = len(B)//2
    table = {name:[QI() for _ in range(cap+1)] for name in ('A','B','C','U','V')}
    choices = [fixed] if fixed is not None else range(len(sampler.configs[t]))
    for choice in choices:
        I, J = sampler.configs[t][choice]
        li, lj = len(I), len(J)
        if abs(li-lj)>1:
            continue
        M = sub(B, [i-off for i in I], [j-off for j in J])
        u, v = [sampler.X[i][0] for i in I], [sampler.Y[j][0] for j in J]
        weight = Fraction(1)
        for i in I:
            weight *= sampler.activities[i]
        if li == lj:
            d = det(M)
            delta = det([[M[i][j] + u[i]*v[j] for j in range(lj)] for i in range(li)]) - d
            table['A'][li] = table['A'][li] + weight*d.norm2()
            table['B'][li] = table['B'][li] + weight*d*delta.conj()
            table['C'][li] = table['C'][li] + weight*delta.norm2()
        elif li == lj+1:
            eta = det([[u[i]] + M[i] for i in range(li)])
            table['U'][lj] = table['U'][lj] + weight*eta.norm2()
        else:
            theta = det([v] + M)
            table['V'][li] = table['V'][li] + weight*theta.norm2()
    return table


def refined_completion(sampler, prefix=()):
    assert sampler.r == 1
    k = sampler.k
    P, Q, R = [QI(1)], [QI()], [QI()]
    E00, E10, E01, E11 = [QI(1)], [QI()], [QI()], [QI()]
    for t in range(len(sampler.blocks)):
        table = local_table(sampler,t,prefix[t] if t < len(prefix) else None)
        a,b,c,u,v = (table[name] for name in ('A','B','C','U','V'))
        Pn = conv(P,a,k)
        Qn = add(conv(Q,a,k),conv(P,b,k),k)
        Rn = add(add(conv(R,a,k),conv(P,c,k),k),
                 add(conv(conjugate(Q),b,k),conv(Q,conjugate(b),k),k),k)
        P,Q,R = Pn,Qn,Rn
        E00n = conv(E00,a,k)
        E10n = add(conv(E10,a,k),conv(E00,u,k),k)
        E01n = add(conv(E01,a,k),conv(E00,v,k),k)
        E11n = add(conv(E11,a,k),add(conv(E10,v,k),conv(E01,u,k),k),k)
        E00,E10,E01,E11 = E00n,E10n,E01n,E11n
    balanced = P[k]+Q[k]+Q[k].conj()+R[k]
    defects = E11[k-1] if k else QI()
    total = balanced+defects
    assert total.im == 0 and total.re >= 0
    return total.re, balanced.re, defects.re


class RankOneSampler(TaggedSampler):
    """Same actual draw/pair interface, using four-state completion masses."""
    def completion_mass(self, prefix=()):
        prefix = tuple(prefix)
        if prefix not in self.mass_cache:
            self.mass_calls += 1
            self.mass_cache[prefix] = refined_completion(self,prefix)[0]
        return self.mass_cache[prefix]


def main():
    start = perf_counter()
    checked = 0
    results = []
    blocks = [[[0,1],[2,-1]],[[1,1],[0,2]]]
    X = [[1],[-1],[2],[1]]
    Y = [[0],[1],[-1],[2]]
    for k in range(3):
        sampler = TaggedSampler(blocks,X,Y,k,[1,Fraction(2,3),2,3])
        for length in range(3):
            for prefix in product(*(range(len(sampler.configs[t])) for t in range(length))):
                got, _, _ = refined_completion(sampler,prefix)
                assert got == sampler.completion_mass(prefix) == sampler.direct_mass(prefix)
                checked += 1
        got,balanced,defects = refined_completion(sampler)
        results.append({'k':k,'coefficient':str(got),'balanced':str(balanced),'defects':str(defects)})
    complex_blocks = [[[QI(0,1),1],[1,QI(0,-1)]], [[QI(1,1),QI(0,1)],[1,QI(1,-1)]]]
    sampler = TaggedSampler(complex_blocks,[[QI(1,1)],[QI(0,-1)],[2],[QI(1,-1)]],
                            [[QI(0,1)],[1],[QI(-1,1)],[2]],2)
    got,balanced,defects = refined_completion(sampler)
    assert got == sampler.direct_mass() == 54
    odd_block = [[0,0,0],[1,0,1],[0,0,0]]
    odd = RankOneSampler([odd_block,odd_block], [[0],[0],[1],[0],[0],[2]],
                        [[1],[0],[0],[1],[0],[0]], 3,
                        [1,1,1,1,1,Fraction(3,2)])
    odd_got,odd_balanced,odd_defects = refined_completion(odd)
    assert odd_got == odd.direct_mass() == 7 and odd_balanced == 0 and odd_defects == 7
    rng = Random(114)
    A, B = odd.sample(rng), odd.sample(rng)
    for _ in range(32):
        A,B = odd.pair_step(A,B,rng)
        assert det(sub(odd.F,*A)).norm2() > 0 and det(sub(odd.F,*B)).norm2() > 0
    result = {'status':'PASS exact rank-one four-state refinement',
              'origin':'c02_l05 rank-one moments; c02_s02 replaces ordered defect-pair enumeration by four-state DP',
              'all_prefix_masses_checked':checked,'real_weighted_results':results,
              'complex_coefficient':str(got),'complex_balanced':str(balanced),'complex_defects':str(defects),
              'canonical_odd_blocks_full_sector':{'coefficient':str(odd_got),'balanced':str(odd_balanced),'defects':str(odd_defects),'actual_pair_steps_using_four_state_dp':32},
              'defect_dp_states':4,'transfer_cost':'O(m*k*b) exact arithmetic after O(m*3^b*poly(b,L)) preprocessing',
              'elapsed_seconds':perf_counter()-start,
              'scope':'Finite exact checks; universal four-state recurrence and cost proof are in MICROSCOPIC_PAIR_KERNEL.txt.'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
