"""Independent exhaustive checker of the finite signature-set closure table.

Reads the certificate JSON only. No producer imports. Unlike the producer's
first-occurrence normalization, this checker minimizes over all 24 color
permutations. It exhausts the proper abstract signature universe independently.
"""
from functools import lru_cache
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
import hashlib
import json
import resource
import time

PALETTE=range(4)
RELABELINGS=list(permutations(PALETTE))


def renamed(s,p):
    return (p[s[0]],p[s[1]],p[s[2]],p[s[3]],int(s[4]),int(s[5]))


@lru_cache(None)
def representative(s):
    return min(renamed(s,p) for p in RELABELINGS)


@lru_cache(None)
def orbit(s):
    return tuple(sorted({renamed(s,p) for p in RELABELINGS}))


def abstract_universe():
    out=set()
    for a,b,p,q in product(PALETTE,repeat=4):
        if a==p or b==q: continue
        for f,g in product((0,1),repeat=2):
            out.add(representative((a,b,p,q,f,g)))
    return sorted(out)


def check(certificate_path):
    start=time.perf_counter(); cpu=time.process_time()
    source=certificate_path.read_bytes()
    data=json.loads(source)
    assert data['status']=='CLOSED'
    universe=abstract_universe(); number={s:i for i,s in enumerate(universe)}
    assert len(universe)==28
    full_mask=(1<<len(universe))-1
    types=[]
    for raw in data['types']:
        state_set=set()
        for value in raw:
            assert len(value)==6
            assert all(type(x) is int for x in value)
            assert all(x in PALETTE for x in value[:4])
            assert value[4] in (0,1) and value[5] in (0,1)
            s=tuple(value)
            assert s[0]!=s[2] and s[1]!=s[3]
            assert representative(s)==s
            assert s not in state_set
            state_set.add(s)
        assert state_set, 'Certificate explicitly contains an empty type'
        types.append(frozenset(state_set))
    assert len(types)==len(set(types))==17
    base=frozenset(((0,0,1,1,1,1),(0,1,2,2,0,0)))
    assert types[0]==base
    type_masks=[sum(1<<number[s] for s in t) for t in types]
    signatures=list(universe)

    @lru_cache(None)
    def series_pair(i,j):
        first=signatures[i]; answer=0
        for second in orbit(signatures[j]):
            if first[1]!=second[0]: continue
            # The new junction has exactly the two incident neighbor colors.
            bad=(first[3]==second[2]) and (first[5]==1 or second[4]==1)
            if bad: continue
            out=(first[0],second[1],first[2],second[3],first[4],second[5])
            answer|=1<<number[representative(out)]
        return answer

    @lru_cache(None)
    def parallel_tuple(indices):
        # Canonical order is valid because this graph operation is symmetric
        # in the disjoint children; all relative relabelings are still covered.
        first=signatures[indices[0]]
        aligned=[]
        for i in indices[1:]:
            aligned.append([s for s in orbit(signatures[i]) if s[:2]==first[:2]])
        answer=0
        for tail in product(*aligned):
            children=(first,)+tail
            C,D=first[:2]
            for A,B in product(PALETTE,repeat=2):
                if A==C or B==D: continue
                left=[A]+[s[2] for s in children]
                right=[B]+[s[3] for s in children]
                if any(s[4] and left.count(s[2])>=2 for s in children): continue
                if any(s[5] and right.count(s[3])>=2 for s in children): continue
                result=(A,B,C,D,int(any(s[2]==A for s in children)),
                        int(any(s[3]==B for s in children)))
                answer|=1<<number[representative(result)]
        return answer

    table={}
    for rec in data['transitions']:
        kind=rec['kind']; children=tuple(rec['children']); output=rec['output']
        assert kind in ('S','P')
        assert len(children)==2 if kind=='S' else len(children) in (2,3)
        assert all(type(i) is int and 0<=i<len(types) for i in children)
        assert type(output) is int and 0<=output<len(types)
        if kind=='P': assert tuple(sorted(children))==children
        key=(kind,children)
        assert key not in table
        table[key]=output
    required={('S',(i,j)) for i,j in product(range(len(types)),repeat=2)}
    required.update(('P',ch) for b in (2,3) for ch in combinations_with_replacement(range(len(types)),b))
    assert set(table)==required, 'Missing, duplicated or extra transitions'
    assert len(required)==1411
    indices=[tuple(number[s] for s in sorted(t)) for t in types]
    checked={'S':0,'P2':0,'P3':0}
    comparisons=[]
    for kind,ch in sorted(required):
        computed=0
        for states in product(*(indices[i] for i in ch)):
            if kind=='S': computed|=series_pair(*states)
            else: computed|=parallel_tuple(tuple(sorted(states)))
            if computed==full_mask: break
        expected=type_masks[table[(kind,ch)]]
        assert computed==expected, (kind,ch,computed,expected)
        assert computed!=0
        checked['S' if kind=='S' else 'P'+str(len(ch))]+=1
        comparisons.append({'kind':kind,'children':list(ch),'output':table[(kind,ch)],'output_state_count':computed.bit_count()})

    reachable={0}; provenance={0:None}
    while True:
        added=False
        for kind,ch in sorted(required):
            out=table[(kind,ch)]
            if out not in reachable and all(i in reachable for i in ch):
                reachable.add(out); provenance[out]={'kind':kind,'children':list(ch)}; added=True
        if not added: break
    assert reachable==set(range(len(types))), 'Some listed types are not reachable from path2'

    receipt={'status':'PASS','certificate':{'filename':certificate_path.name,'bytes':len(source),'sha256':hashlib.sha256(source).hexdigest()},
             'signature_universe_count':len(universe),'types':len(types),'type_sizes':[len(t) for t in types],
             'transitions_checked':checked,'total_transitions':len(required),
             'all_types_nonempty':True,'all_types_reachable_from_leaf':True,
             'empty_type_not_silently_removed':True,'canonicalization':'Lexicographic minimum over all 24 permutations, independently implemented',
             'palette_alignment':'Every relative four-color permutation consistent with identified terminal colors; global color symmetry fixes one first child.',
             'input_order':'S ordered; P unordered at type level and all signature choices included; commutativity justified by disjoint parallel children.',
             'provenance':provenance,'transition_checks':comparisons,
             'cost':{'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,
                     'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                     'excludes':'process startup, checker authoring/proof review, final receipt serialization'},
             'scope':'Universal closure certificate verified using proved exact interface. This establishes nonempty star-four state sets on every finite path2/S2/P2/P3 expression; no claim for all chordless supports, arbitrary precolors, historical originality or performance.'}
    return receipt


if __name__=='__main__':
    here=Path(__file__).resolve().parent
    receipt=check(here.parents[1]/'results/star_closure_attempt1.json')
    (here/'CLOSED_TABLE_RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('transition_checks','provenance')},indent=2))
