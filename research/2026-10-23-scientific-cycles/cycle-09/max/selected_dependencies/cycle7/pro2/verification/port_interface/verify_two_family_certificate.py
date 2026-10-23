"""Independent literal checker of the 92 constructive port witnesses.

No root producer import, search, optimization or floating arithmetic. Each row
is checked directly against the universal local interface lemma in PROOF.md.
"""
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
import hashlib
import json
import resource
import time

PALETTE=range(4)
PERMS=list(permutations(PALETTE))
FAMILIES={
    'L':{(0,0,1,1,1,1),(0,1,2,2,0,0)},
    'N':{(0,0,1,2,0,0),(0,0,1,2,1,1),(0,1,1,0,0,0),
         (0,1,1,2,0,0),(0,1,1,2,1,0),(0,1,2,0,0,0),
         (0,1,2,0,0,1),(0,1,2,3,0,1),(0,1,2,3,1,0)},
}


def normalized(s):
    return min(tuple(p[x] for x in s[:4])+tuple(s[4:]) for p in PERMS)


def valid_shape(s):
    assert len(s)==6 and all(type(x) is int for x in s)
    assert all(x in PALETTE for x in s[:4])
    assert s[4] in (0,1) and s[5] in (0,1)
    assert s[0]!=s[2] and s[1]!=s[3]


def actual_series(children):
    assert len(children)==2
    x,y=children
    assert x[1]==y[0]
    assert not (x[3]==y[2] and (x[5] or y[4]))
    return (x[0],y[1],x[2],y[3],x[4],y[5])


def actual_parallel(children,parent):
    A,B=parent[:2]
    C,D=children[0][:2]
    assert A!=C and B!=D
    assert all(s[:2]==(C,D) for s in children)
    # The complete neighbor-color lists at the joined vertices include the
    # new outer leaf. Multiplicity at least two is exactly the bad-edge flag.
    left=[A]+[s[2] for s in children]
    right=[B]+[s[3] for s in children]
    for s in children:
        assert not (s[4] and left.count(s[2])>=2)
        assert not (s[5] and right.count(s[3])>=2)
    return (A,B,C,D,int(A in left[1:]),int(B in right[1:]))


def main():
    t0=time.perf_counter();cpu=time.process_time()
    here=Path(__file__).resolve().parent
    source=here.parents[1]/'results/star_four_certificate.json'
    raw=source.read_bytes(); cert=json.loads(raw)
    assert cert['palette_size']==4
    assert cert['signature_order']==['s','t','neighbor_s','neighbor_t','left_flag','right_flag']
    assert {k:{tuple(s) for s in v} for k,v in cert['families'].items()}==FAMILIES
    assert all(len(cert['families'][k])==len(FAMILIES[k]) for k in FAMILIES)
    assert cert['case_count']==11 and cert['witness_count']==92
    expected={('S',classes):'N' for classes in product(('L','N'),repeat=2)}
    for arity in (2,3):
        for classes in combinations_with_replacement(('L','N'),arity):
            expected[('P',classes)]='L' if classes==('N','N','N') else 'N'
    seen=set(); result=[]; rows=0
    for case in cert['transitions']:
        kind=case['kind']; classes=tuple(case['child_classes']); parent_class=case['parent_class']
        key=(kind,classes)
        assert key in expected and key not in seen
        seen.add(key); assert parent_class==expected[key]
        requested=set()
        for witness in case['witnesses']:
            parent=tuple(witness['parent_signature'])
            children=[tuple(s) for s in witness['child_signatures']]
            valid_shape(parent)
            assert parent in FAMILIES[parent_class] and parent not in requested
            requested.add(parent)
            assert len(children)==len(classes)
            for child,cls in zip(children,classes):
                valid_shape(child); assert normalized(child) in FAMILIES[cls]
            output=actual_series(children) if kind=='S' else actual_parallel(children,parent)
            assert output==parent
            rows+=1
        assert requested==FAMILIES[parent_class]
        result.append({'kind':kind,'child_classes':classes,'parent_class':parent_class,
                       'witness_count':len(requested),'status':'PASS'})
    assert seen==set(expected) and rows==92
    receipt={'status':'PASS','certificate':{'filename':source.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},
             'case_count':len(seen),'witness_count':rows,'family_sizes':{k:len(v) for k,v in FAMILIES.items()},
             'checks':['Exact pinned family definitions','All 11 class cases present once','Every requested parent signature present once',
                       'All colored child signatures in the declared family orbit','All terminal identifications and stub edges proper',
                       'All new bad-edge conditions false','Output flags and colors exactly equal the requested parent',
                       'L base states realized by the two-edge path'],
             'cases':result,
             'cost':{'wall_seconds':time.perf_counter()-t0,'cpu_seconds':time.process_time()-cpu,
                     'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                     'excludes':'process startup, reading/authoring/proof review, final receipt serialization'},
             'consequence':'Together with the proved exact interface lemma, induction realizes every requested state in the assigned family for every finite L/S2/P2/P3 expression. Each expression therefore has a proper star-four coloring. No arbitrary boundary assignment or full partial-two-tree conclusion is asserted.'}
    (here/'TWO_FAMILY_CERTIFICATE_RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__': main()
