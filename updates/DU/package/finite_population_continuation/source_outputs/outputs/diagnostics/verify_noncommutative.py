"""Exact diagnostics for the ordered-product candidate, using only stdlib.

These finite checks support the implementation of its algebra/samplers; they
are not a substitute for the universal proofs in NONCOMMUTATIVE_REPAIR.md.
"""
from collections import defaultdict, deque
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import gcd
from pathlib import Path
import json
import random


def cyclic_group(n):
    return [[(a+b) % n for b in range(n)] for a in range(n)]


def symmetric_group_3():
    ps = list(permutations(range(3)))
    idx = {p:i for i,p in enumerate(ps)}
    return [[idx[tuple(a[b[k]] for k in range(3))] for b in ps] for a in ps]


def rees(group, rows, cols, sandwich):
    elems = list(product(range(rows), range(len(group)), range(cols)))
    ix = {a:i for i,a in enumerate(elems)}
    table = []
    for i,g,l in elems:
        table.append([ix[(i,group[group[g][sandwich[l][j]]][u],k)]
                      for j,u,k in elems])
    return elems, table


def generated(table, alphabet):
    lengths = {a:1 for a in alphabet}
    queue = deque(alphabet)
    while queue:
        x = queue.popleft()
        for a in alphabet:
            y = table[x][a]
            if y not in lengths:
                lengths[y] = lengths[x]+1
                queue.append(y)
    return set(lengths), lengths


def green_classes(table, semigroup, right):
    keys = {x:frozenset(table[x][y] if right else table[y][x]
                       for y in semigroup) for x in semigroup}
    classes = defaultdict(set)
    for x,k in keys.items():
        classes[k].add(x)
    labels = {x:i for i,c in enumerate(classes.values()) for x in c}
    return list(classes.values()), labels


def row_period(table, alphabet, row):
    root = min(row)
    ds = {root:0}
    queue = deque([root])
    while queue:
        x = queue.popleft()
        for a in alphabet:
            y = table[x][a]
            assert y in row
            if y not in ds:
                ds[y] = ds[x]+1
                queue.append(y)
    assert set(ds) == row, "right row not strongly connected"
    period = 0
    for x in row:
        for a in alphabet:
            period = gcd(period, abs(ds[x]+1-ds[table[x][a]]))
    assert period > 0
    return period


def verify_structure(table, alphabet):
    semigroup, lengths = generated(table, alphabet)
    rows, rlabel = green_classes(table, semigroup, True)
    cols, llabel = green_classes(table, semigroup, False)
    h = row_period(table, alphabet, rows[0])
    assert all(row_period(table, alphabet, row) == h for row in rows)
    phase = {x:lengths[x] % h for x in semigroup}
    for x in semigroup:
        for y in semigroup:
            assert phase[table[x][y]] == (phase[x]+phase[y]) % h
            assert rlabel[table[x][y]] == rlabel[x]
            assert llabel[table[x][y]] == llabel[y]
    assert all(phase[a] == 1 % h for a in alphabet)
    count = len([x for x in rows[0] if phase[x] == 0])
    assert count > 0
    assert all(sum(phase[x] == r for x in row) == count
               for row in rows for r in range(h))
    ell = h*((count-1)**2+2)
    assert ell <= 2*len(semigroup)**2
    zero = {x for x in semigroup if phase[x] == 0}
    power = set(alphabet)
    for k in range(2,ell+1):
        power = {table[x][a] for x in power for a in alphabet}
    assert power == zero, "bounded power does not fill zero phase"
    repair_count = 0
    for p in semigroup:
        for q in semigroup:
            images = {table[table[p][b]][q] for b in zero}
            expected = {z for z in semigroup
                        if rlabel[z] == rlabel[p]
                        and llabel[z] == llabel[q]
                        and phase[z] == (phase[p]+phase[q]) % h}
            assert images == expected, "sandwich repair image wrong"
            repair_count += len(expected)
    return repair_count


def flag_law(ps):
    ss = [F(0)]
    for p in ps:
        assert 0 <= p <= 1
        ss.append(ss[-1]+p)
    assert ss[-1] >= 2
    breaks = sorted({F(0),F(1),*(s % 1 for s in ss)})
    law = []
    for lo,hi in zip(breaks,breaks[1:]):
        u = (lo+hi)/2
        flags = []
        for i,(start,end) in enumerate(zip(ss,ss[1:])):
            v = start-u
            integer = -((-v.numerator)//v.denominator)
            if u+integer < end:
                flags.append(i)
        assert len(flags) >= 2
        law.append((tuple(flags),hi-lo))
    for i,p in enumerate(ps):
        assert sum(w for flags,w in law if i in flags) == p
    return law


def group_identity_inverse(table):
    n = len(table)
    identity = next(e for e in range(n)
                    if all(table[e][x] == table[x][e] == x for x in range(n)))
    inv = [next(y for y in range(n)
                if table[x][y] == table[y][x] == identity) for x in range(n)]
    return identity, inv


def fold(table, xs, identity):
    r = identity
    for x in xs:
        r = table[r][x]
    return r


def verify_group_sampler(table, ps, residuals, privacy_k=1):
    size = len(table)
    e,inv = group_identity_inverse(table)
    count = 0
    coalitions = [c for k in range(2,privacy_k+1)
                  for c in combinations(range(len(ps)),k)]
    references = None
    for target in range(size):
        marginals = [defaultdict(F) for p in ps]
        coalition_laws = [defaultdict(F) for c in coalitions]
        mass = F(0)
        for flags,weight in flag_law(ps):
            j = flags[-1]
            free = flags[:-1]
            for values in product(range(size), repeat=len(free)):
                word = list(residuals)
                for i,x in zip(free,values):
                    word[i] = x
                left = fold(table,word[:j],e)
                right = fold(table,word[j+1:],e)
                word[j] = table[table[inv[left]][target]][inv[right]]
                assert fold(table,word,e) == target
                prob = weight/F(size**len(free))
                mass += prob
                for i,x in enumerate(word):
                    marginals[i][x] += prob
                for c,law in zip(coalitions,coalition_laws):
                    law[tuple(word[i] for i in c)] += prob
                count += 1
        assert mass == 1
        for i,p in enumerate(ps):
            expected = {x:p/F(size)+(1-p if x == residuals[i] else 0)
                        for x in range(size)}
            assert all(marginals[i][x] == expected[x] for x in range(size))
        if references is None:
            references = coalition_laws
        else:
            assert coalition_laws == references, "coalition reveals target"
    return count


def verify_rees_sampler(group):
    size = len(group)
    e,inv = group_identity_inverse(group)
    sandwich = [[e,e],[e,1]]
    elems,table = rees(group,2,2,sandwich)
    ix = {a:i for i,a in enumerate(elems)}
    pairs = [(0,0),(1,1)]
    p = F(2,3)
    residual = (0,e,0)
    mu = {x:(p/F(2*size) if (x[0],x[2]) in pairs else F(0))
          +(1-p if x == residual else 0) for x in elems}
    first = {i:sum(v for x,v in mu.items() if x[0] == i) for i in range(2)}
    last = {l:sum(v for x,v in mu.items() if x[2] == l) for l in range(2)}
    marginals = [defaultdict(F) for i in range(5)]
    output = defaultdict(F)
    mass = F(0)
    events = 0
    for ri,cl in product(range(2),repeat=2):
        target = (ri,(1+2*ri+cl) % size,cl)
        target_prob = first[ri]*last[cl]
        endpoints1 = [(x,prob/first[ri]) for x,prob in mu.items()
                      if x[0] == ri and prob]
        endpoints2 = [(x,prob/last[cl]) for x,prob in mu.items()
                      if x[2] == cl and prob]
        for (x1,w1),(x5,w5) in product(endpoints1,endpoints2):
            for flags,wflag in flag_law([p,p,p]):
                marked = tuple(i+1 for i in flags)
                j = marked[-1]
                for marked_pairs in product(pairs,repeat=len(marked)):
                    for gs in product(range(size),repeat=len(marked)-1):
                        word = [x1,residual,residual,residual,x5]
                        for pos,(r,l) in zip(marked,marked_pairs):
                            word[pos] = (r,e,l)
                        for pos,g in zip(marked[:-1],gs):
                            r,_,l = word[pos]
                            word[pos] = (r,g,l)
                        factors = []
                        for i,x in enumerate(word):
                            if i:
                                factors.append(sandwich[word[i-1][2]][x[0]])
                            factors.append(x[1])
                        variable = 2*j
                        left_g = fold(group,factors[:variable],e)
                        right_g = fold(group,factors[variable+1:],e)
                        completion = group[group[inv[left_g]][target[1]]][inv[right_g]]
                        r,_,l = word[j]
                        word[j] = (r,completion,l)
                        product_index = ix[word[0]]
                        for x in word[1:]:
                            product_index = table[product_index][ix[x]]
                        assert elems[product_index] == target
                        prob = target_prob*w1*w5*wflag/F(2**len(marked)*size**(len(marked)-1))
                        mass += prob
                        output[target] += prob
                        for i,x in enumerate(word):
                            marginals[i][x] += prob
                        events += 1
    assert mass == 1
    for i in range(5):
        assert all(marginals[i][x] == mu[x] for x in elems)
    for ri,cl in product(range(2),repeat=2):
        target = (ri,(1+2*ri+cl) % size,cl)
        assert output[target] == first[ri]*last[cl]
    return events


def main():
    structures = 0
    repairs = 0
    for twist in range(2):
        elems,table = rees(cyclic_group(2),2,2,[[0,0],[0,twist]])
        for mask in range(1,1 << len(elems)):
            alphabet = [i for i in range(len(elems)) if mask >> i & 1]
            repairs += verify_structure(table,alphabet)
            structures += 1
    s3 = symmetric_group_3()
    for mask in range(1,1 << len(s3)):
        alphabet = [i for i in range(len(s3)) if mask >> i & 1]
        repairs += verify_structure(s3,alphabet)
        structures += 1
    elems,table = rees(s3,2,2,[[0,0],[0,1]])
    rng = random.Random(81473)
    for case in range(20):
        alphabet = [i for i in range(len(elems)) if rng.randrange(3) == 0]
        if not alphabet:
            alphabet = [0]
        repairs += verify_structure(table,alphabet)
        structures += 1
    group_events = 0
    group_events += verify_group_sampler(s3,[F(1),F(1)],[1,2])
    group_events += verify_group_sampler(s3,[F(2,3)]*3,[1,2,3])
    group_events += verify_group_sampler(s3,[F(1,3)]*6,list(range(6)))
    group_events += verify_group_sampler(s3,[F(2,3),F(3,4),F(5,6)],[1,2,3])
    group_events += verify_group_sampler(s3,[F(3,4)]*4,[1,2,3,4],privacy_k=2)
    rees_events = verify_rees_sampler(s3)
    receipt = dict(status="all exact checks passed",
                   support_structures_checked=structures,
                   sandwich_target_repairs_checked=repairs,
                   exact_group_sampler_events=group_events,
                   pair_coalition_privacy_comparisons=30,
                   exact_rees_sampler_events=rees_events,
                   arithmetic="integer algebra and fractions.Fraction",
                   scope="finite diagnostics, not universal proof or novelty evidence")
    Path(__file__).with_name("noncommutative_verification_receipt.json").write_text(
        json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,indent=2))


if __name__ == "__main__":
    main()
