"""Independent literal gate for the final 200-witness four-family certificate.

Only independent review helpers are imported; no root producer module or
invariant-search result is used. All-size consequence rests on PROOF.md's
exact port lemma and the complete finite table checked here.
"""
from itertools import combinations_with_replacement, product
from pathlib import Path
import hashlib
import json
import resource
import time
from check_port_interface import path,actual_states
from verify_two_family_certificate import normalized,valid_shape,actual_series,actual_parallel,FAMILIES as OLD

EXPECTED={
    'A':OLD['L'],
    'B':{(0,0,1,2,0,0),(0,1,1,2,0,1),(0,1,2,0,1,0),(0,1,2,3,0,0)},
    'C':OLD['N'],
    'D':{(0,0,1,2,0,1),(0,0,1,2,1,0),(0,0,1,2,1,1),
         (0,1,1,0,0,0),(0,1,1,0,0,1),(0,1,1,0,1,0),
         (0,1,1,2,0,0),(0,1,1,2,1,0),(0,1,1,2,1,1),
         (0,1,2,0,0,0),(0,1,2,0,0,1),(0,1,2,0,1,1),
         (0,1,2,3,0,1),(0,1,2,3,1,0),(0,1,2,3,1,1)},
}


def main():
    t0=time.perf_counter();cpu=time.process_time()
    here=Path(__file__).resolve().parent
    source=here.parents[1]/'results/general_star_certificate.json'
    raw=source.read_bytes();cert=json.loads(raw)
    assert cert['palette_size']==4
    assert cert['signature_order']==['s','t','neighbor_s','neighbor_t','left_flag','right_flag']
    assert cert['leaf_classes']=={'2':'A','3':'B'}
    families={k:{tuple(s) for s in v} for k,v in cert['families'].items()}
    assert families==EXPECTED
    assert all(len(cert['families'][k])==len(families[k]) for k in families)
    for f in families.values():
        assert f
        for s in f: valid_shape(s);assert normalized(s)==s
    leaves={}
    for length,label in [(2,'A'),(3,'B')]:
        states,counts=actual_states(path(length),palette=4)
        assert {normalized(s) for s in states}==families[label]
        leaves[label]={'length':length,'canonical_state_count':len(families[label]),
                       'all_actual_signatures':len(states),**counts,'status':'PASS'}
    required={('S',ch) for ch in product('ABCD',repeat=2)}
    required.update(('P',ch) for arity in (2,3) for ch in combinations_with_replacement('ABCD',arity))
    assert len(required)==46
    seen={};row_count=0; results=[];operation_counts={'S':0,'P2':0,'P3':0}
    for case in cert['transitions']:
        kind=case['kind'];classes=tuple(case['child_classes']);parent_class=case['parent_class']
        key=(kind,classes)
        assert key in required and key not in seen
        assert parent_class in families
        seen[key]=parent_class
        requested=set()
        for witness in case['witnesses']:
            parent=tuple(witness['parent_signature']);children=[tuple(s) for s in witness['child_signatures']]
            valid_shape(parent)
            assert parent in families[parent_class] and parent not in requested
            requested.add(parent)
            assert len(children)==len(classes)
            for child,label in zip(children,classes):
                valid_shape(child);assert normalized(child) in families[label]
            output=actual_series(children) if kind=='S' else actual_parallel(children,parent)
            assert output==parent
            row_count+=1
        assert requested==families[parent_class]
        operation_counts['S' if kind=='S' else 'P'+str(len(classes))]+=1
        results.append({'kind':kind,'child_classes':classes,'parent_class':parent_class,'witness_count':len(requested),'status':'PASS'})
    assert set(seen)==required
    assert cert['case_count']==46 and cert['witness_count']==row_count==200
    reachable={'A','B'}
    while True:
        new=reachable|{out for (_,ch),out in seen.items() if all(c in reachable for c in ch)}
        if new==reachable:break
        reachable=new
    assert reachable==set(families)
    receipt={'status':'PASS','certificate':{'filename':source.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},
             'family_sizes':{k:len(v) for k,v in families.items()},'case_counts':operation_counts,
             'case_count':len(seen),'witness_count':row_count,'leaves':leaves,
             'checks':['All four pinned nonempty canonical families','Exact path2 and path3 base-state sets',
                       'All16 ordered series,10 unordered P2 and20 unordered P3 class cases covered once',
                       'Every requested output signature witnessed exactly once',
                       'Every colored child signature belongs to its declared family orbit',
                       'All identifications/stubs proper; every new-edge collision rejected',
                       'Output flags/colors equal the requested signature exactly','Every family label reachable from admitted leaves'],
             'cases':results,'cost':{'wall_seconds':time.perf_counter()-t0,'cpu_seconds':time.process_time()-cpu,
                                    'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                                    'excludes':'process startup, scientific source reading/checker authoring/proof review, final receipt serialization'},
             'consequence':'The local lemma and these constructive rows prove star-four coloring at every depth for arbitrary path leaves of length>=2 and every series arity>=2, with P2/P3 stubbed parallel joins. Decompose length2a+3b into path2 and path3 leaves. No graph recognition or all-chordless-atom coverage follows.'}
    (here/'GENERAL_CERTIFICATE_RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
