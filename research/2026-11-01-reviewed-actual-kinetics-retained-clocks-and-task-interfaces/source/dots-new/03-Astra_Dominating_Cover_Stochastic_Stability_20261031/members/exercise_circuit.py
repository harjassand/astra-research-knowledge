from itertools import combinations,product
from fractions import Fraction as F
import json,copy,sys
import cover_circuit as C
B=C.B
counts=dict(graphs=0,accepted_graphs=0,capacity_states=0,minimum_cover_witnesses=0,bad_edges_detected=0,active_edge_queries=0,large_binary_evaluations=0,numerical_equality_states=0,mutations=0)
for m in range(2,6):
    vs=tuple(range(1,m+1));possible=list(combinations(vs,2))
    for mask in range(1,1<<len(possible)):
        edges=tuple(e for j,e in enumerate(possible)if mask>>j&1);rec=dict(satellites=vs,edges=edges)
        covers=B.covers(rec);es=set(edges)
        valid=all(all(any(tuple(sorted((w,z)))in es for z in (u,v))for w in vs if w not in cc)for cc in covers for u,v in edges if u in cc and v in cc)
        counts['graphs']+=1
        if not valid:continue
        circuit=C.compile_inventory(rec);counts['accepted_graphs']+=1
        for xx in product(range(3),repeat=m):
            x=(0,)+xx;tau=min(sum(x[v]for v in cc)for cc in covers)
            assert C.cover_weight(circuit,x)==tau
            witness=C.optimal_minimal_cover(circuit,x)
            assert witness in covers and sum(x[v]for v in witness)==tau
            opt=[cc for cc in covers if sum(x[v]for v in cc)==tau]
            expected=tuple(e for e in edges if x[e[0]] and x[e[1]] and any(e[0]in cc and e[1]in cc for cc in opt))
            assert C.bad_active_edges(circuit,x)==expected
            counts['capacity_states']+=1;counts['minimum_cover_witnesses']+=1;counts['bad_edges_detected']+=len(expected);counts['active_edge_queries']+=sum(bool(x[u]and x[v])for u,v in edges)
        x=(0,)+tuple(10**200+i for i in vs)
        assert C.cover_weight(circuit,x)==min(sum(x[v]for v in cc)for cc in covers);counts['large_binary_evaluations']+=1
raw=B.fixture();old=B.numerical(raw,F(2));new=C.numerical(raw,F(2));rec=B.recognize(raw)
assert old['constants']==new['constants']and old['profile_head']==new['profile_head']and old['Foster']==new['Foster']and old['stationary_moment']==new['stationary_moment']
# Production compilation cannot fall back to either exhaustive constructor.
def prohibited(*args,**kwargs):raise AssertionError('hidden exhaustive dependency')
B.covers=prohibited;B.numerical=prohibited
assert C.numerical(raw,F(2))==new
for x in list(product(range(3),repeat=5))+[(0,1,1,0,10**30),(0,10**30,1,1,10**30),(1,0,0,0,10**30)]:
    assert C.hvalue(rec,new,x)==B.hvalue(rec,old,x)
    assert C.scaled_drift(rec,new,x)==B.scaled_drift(rec,old,x);counts['numerical_equality_states']+=1
# Any circuit/constant mutation is refused by the same-implementation receiving routine.
for key in ['inventory','constants','profile_head','Foster','stationary_moment','work','qualitative','t']:
    cc=copy.deepcopy(new);cc[key]=None
    assert not C.receive_numerical(raw,F(2),cc);counts['mutations']+=1
q=C.qualitative(raw);small=C.numerical(raw,F(2),max_profile_steps=0)
assert small['status']=='UNKNOWN_NUMERICAL_BUDGET'and small['qualitative']==q
assert new['work']['cover_masks_enumerated']==q['work']['cover_masks_enumerated']==0
print(json.dumps(C.encode(dict(status='PASS',counts=counts,main_inventory=new['inventory'],main_work=new['work'],same_Foster_constant_as_frozen=True,main_certificate_sha256=C.digest(new),no_simulation=True,no_cover_enumeration_in_compiler=True,exhaustive_enumeration_used_only_as_test_comparator=True)),indent=2))
