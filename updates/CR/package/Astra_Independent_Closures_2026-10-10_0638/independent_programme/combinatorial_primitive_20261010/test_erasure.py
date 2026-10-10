"""Small exact searches for the concrete erase-and-prune operation."""
from itertools import combinations, product
from check_folds import sunflower
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix
import numpy as np
import json


def max_safe_subset(rows, time_limit=30):
    constraints=[]
    for a,b in combinations(range(len(rows)),2):
        if rows[a]==rows[b]: constraints.append((a,b))
    for ids in combinations(range(len(rows)),3):
        rr=[rows[i] for i in ids]
        if len(set(rr))==3 and sunflower(rr): constraints.append(ids)
    if not constraints:
        return list(range(len(rows))), True
    rowids=[]; cols=[]; data=[]; upper=[]
    for k,c in enumerate(constraints):
        for i in c: rowids.append(k); cols.append(i); data.append(1.)
        upper.append(len(c)-1)
    A=coo_matrix((data,(rowids,cols)),shape=(len(constraints),len(rows))).tocsr()
    res=milp(-np.ones(len(rows)),integrality=np.ones(len(rows)),bounds=Bounds(0,1),
        constraints=LinearConstraint(A,-np.inf,np.array(upper)),
        options={'time_limit':time_limit})
    assert res.x is not None
    keep=np.where(res.x>0.5)[0].tolist()
    chosen=[rows[i] for i in keep]
    assert len(set(chosen))==len(chosen)
    assert not any(sunflower(rr) for rr in combinations(chosen,3))
    return keep, res.status==0


def main():
    out=[]
    for q,w in [(3,2),(3,3),(4,3),(5,3)]:
        space=list(product(range(q),repeat=w))
        ids, exact=max_safe_subset(space,45)
        rows=[space[i] for i in ids]
        retain=[]
        for i in range(w):
            projected=[r[:i]+r[i+1:] for r in rows]
            keep, proved=max_safe_subset(projected,15)
            retain.append({'coordinate':i,'retained':len(keep),'optimal':proved})
        item={'alphabet':q,'rank':w,'size':len(rows),'maximum_proved':exact,
              'rows':rows,'erasure':retain}
        out.append(item)
        print(json.dumps(item),flush=True)
    with open('independent_programme/combinatorial_primitive_20261010/erasure_results.json','w') as f:
        json.dump(out,f,indent=2)

if __name__=='__main__': main()
