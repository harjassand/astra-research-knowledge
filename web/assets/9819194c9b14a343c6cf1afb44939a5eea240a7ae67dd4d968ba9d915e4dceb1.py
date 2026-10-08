#!/usr/bin/env python3
"""Independent checks using actual tuple descriptors, not only canonical object IDs.
These finite tests validate mechanisms; they are not an asymptotic proof.
"""
from itertools import product
from collections import defaultdict
import json
from pathlib import Path

A0=('atom',0); A1=('atom',1)
Z=frozenset(); O=frozenset([Z]); AT=frozenset([A0,A1])
U=(A0,A1,Z,O,AT)
S=lambda x:isinstance(x,frozenset)
M=lambda x:set(x) if S(x) else set()
def closure(x):
    todo=[x]; seen=set()
    while todo:
        y=todo.pop()
        if y not in seen:
            seen.add(y); todo.extend(M(y))
    return seen

oldC={(x,y) for y in U for x in closure(y)}
oldE={(x,y) for y in U for x in M(y)}
params=list(product(U,repeat=2))
allrows=[frozenset(x for i,x in enumerate(U) if mask>>i&1) for mask in range(32)]
stats={'batches':0,'raw_descriptors':0,'descriptor_pairs':0,'quotient_membership_pairs':0,'quotient_closure_pairs':0,'card_collision_cases':0}
for shift in (0,9,23):
    rows={p:allrows[(i+shift)%32] for i,p in enumerate(params)}
    # A descriptor is a 4-tuple. d[2]=d[3] means old(d[0]),
    # with d[1],d[2] irrelevant. Otherwise it means new(d[0],d[1]).
    D=list(product(U,repeat=4))
    isold=lambda d:d[2]==d[3]
    den=lambda d:d[0] if isold(d) else rows[d[:2]]
    def eq(d,e):
        if isold(d) and isold(e): return d[0]==e[0]
        if not isold(d) and not isold(e): return rows[d[:2]]==rows[e[:2]]
        if isold(d): d,e=e,d
        return S(e[0]) and rows[d[:2]]==e[0]
    expectedU=set(U)|set(rows.values())
    # Check the interpreted equality formula on every raw pair.
    for d,e in product(D,repeat=2):
        assert eq(d,e)==(den(d)==den(e))
    # The quotient image of raw relations equals their saturated quotient image.
    raw_image_E=set(); raw_image_C=set()
    for d,e in product(D,repeat=2):
        raw_e=False; raw_c=d==e
        if isold(d) and isold(e):
            raw_e=(d[0],e[0]) in oldE
            raw_c |= (d[0],e[0]) in oldC
        if isold(d) and not isold(e):
            raw_e=d[0] in rows[e[:2]]
            raw_c |= any((d[0],z) in oldC for z in rows[e[:2]])
        if raw_e: raw_image_E.add((den(d),den(e)))
        if raw_c: raw_image_C.add((den(d),den(e)))
    expectedE={(x,y) for y in expectedU for x in M(y)}
    expectedC={(x,y) for y in expectedU for x in closure(y)}
    assert raw_image_E==expectedE
    assert raw_image_C==expectedC
    # Pullback of quotient relations is precisely saturated and invariant.
    satE=lambda d,e:(den(d),den(e)) in raw_image_E
    satC=lambda d,e:(den(d),den(e)) in raw_image_C
    groups=defaultdict(list)
    for d in D: groups[den(d)].append(d)
    for x,dx in groups.items():
        for y,dy in groups.items():
            values={(satE(d,e),satC(d,e)) for d in dx for e in dy}
            assert values=={((x,y) in expectedE,(x,y) in expectedC)}
    # Any roots plus the permanent base give a transitive GC restriction.
    for root in expectedU:
        live=set(U)|closure(root)
        assert all(M(x)<=live for x in live)
        assert {(x,y) for x,y in expectedC if x in live and y in live}=={(x,y) for y in live for x in closure(y)}
    # Copy retained old binary relation and add a new result table, then saturate.
    oldT={(A0,Z),(A1,AT)}
    resultT={(p[0],p[1],rows[p]) for p in params}
    assert len({(den(d),den(e)) for d,e in product(D,repeat=2) if isold(d) and isold(e) and (d[0],e[0]) in oldT})==len(oldT)
    assert all(out in expectedU for _,_,out in resultT)
    stats['batches']+=1; stats['raw_descriptors']+=len(D); stats['descriptor_pairs']+=len(D)**2
    stats['quotient_membership_pairs']+=len(expectedE); stats['quotient_closure_pairs']+=len(expectedC)

# Existing ordinals above the current reserve may be reused when growing it.
ordinals=[Z]
for k in range(1,9): ordinals.append(frozenset(ordinals))
for k in range(0,9):
    live=set(U)|set(ordinals) # all targets already represented
    reserve={Z,O}; R=1
    # Härtig's two unary sets are interpreted here by exact member cardinality.
    argument=ordinals[k]
    while not any(len(M(argument))==len(M(o)) for o in reserve):
        successor=frozenset(reserve)
        assert successor in live # every new descriptor must merge with an old object
        reserve.add(successor); R+=1
    assert R==max(1,k)
    assert [o for o in reserve if len(M(o))==len(M(argument))]==[ordinals[k]]
    stats['card_collision_cases']+=1
# Atoms have zero members and match zero, not the atom itself.
assert len(M(A0))==0 and A0!=Z and not S(A0)
# Initialization equality patterns really supply n+3 classes at n=2.
trips=list(product((0,1),repeat=3))
classes=[]
for a,b,c in trips:
    if a==b==c: classes.append(('atom',a))
    elif a==b: classes.append(('empty',))
    elif a==c: classes.append(('true',))
    elif b==c: classes.append(('Atoms',))
    else: raise AssertionError('impossible with two atoms')
assert len(set(classes))==5
stats['all_checks_passed']=True
p=Path(__file__).with_name('raw_descriptor_test_results.json')
p.write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats,indent=2))
