"""Final certificate: arbitrary path lengths and both series parities.
Four guaranteed signature families, 46 local cases. Reads the saved exact
invariant-discovery record; receiving construction reads only this certificate.
"""
from pathlib import Path
from itertools import product,combinations_with_replacement
from time import perf_counter,process_time
import resource,json
from finite_star_certificate import candidates

def construct():
    p=Path(__file__).resolve().parents[1]/'results/path_leaf_invariant_search.json'
    source=json.loads(p.read_text())
    assert source['status']=='CLOSED'
    families={name:tuple(map(tuple,f)) for name,f in zip('ABCD',source['families'])}
    assert list(map(len,families.values()))==[2,4,9,15]
    rows=[]
    for row in source['cases']:
        kind=row['kind'];classes=tuple('ABCD'[i] for i in row['child_indices'])
        parent='ABCD'[row['covers'][0]]
        targets=set(families[parent]);witness={}
        for out,child in candidates(kind,classes,families):
            if out in targets and out not in witness:
                witness[out]={'parent_signature':out,'child_signatures':child}
                if len(witness)==len(targets):break
        assert set(witness)==targets,(kind,classes,parent)
        rows.append({'kind':kind,'child_classes':classes,'parent_class':parent,
                     'witnesses':[witness[s] for s in families[parent]]})
    assert len(rows)==46
    return {'schema':'astra-star-four-all-series-paths/v1','palette_size':4,
            'signature_order':['s','t','neighbor_s','neighbor_t','left_flag','right_flag'],
            'leaf_classes':{'2':'A','3':'B'},
            'families':families,'transitions':rows,'case_count':len(rows),
            'witness_count':sum(len(r['witnesses']) for r in rows),
            'interpretation':'A family lists signatures guaranteed realizable under all color permutations; it need not be the complete set of a module. A module class is not a syntactic graph kind.'}

if __name__=='__main__':
    t=perf_counter();cpu=process_time();cert=construct()
    elapsed=perf_counter()-t;used=process_time()-cpu
    out=Path(__file__).resolve().parents[1]/'results'
    (out/'general_star_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
    cost={'wall_seconds':elapsed,'cpu_seconds':used,
          'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
          'cases':cert['case_count'],'witnesses':cert['witness_count'],
          'scope':'Exact generation including saved discovery read; serialization/startup, inference and authoring excluded.'}
    (out/'general_certificate_cost.json').write_text(json.dumps(cost,indent=2)+'\n')
    print(json.dumps(cost))

