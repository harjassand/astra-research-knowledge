"""Exact checks of the dimension-descent extension of the block identity."""
import json
from pathlib import Path
import numpy as np
from npt_core import endpoint_numerator,swap_metric_numerator
rng=np.random.default_rng(2026100911);records=[]
for m in (0,1,2):
    dims=(3,)*m;D=3**m
    for d in (3,4,5):
        for trial in range(4):
            u,v=[rng.integers(-2,3,D).astype(object) for _ in range(2)]
            X=rng.integers(-2,3,((d-2)*D,2)).astype(object)
            Y=rng.integers(-2,3,((d-2)*D,2)).astype(object)
            eps=trial%3+1
            U=np.vstack([np.column_stack([u,0*u]),np.column_stack([0*u,u]),eps*X])
            V=np.vstack([np.column_stack([v,0*v]),np.column_stack([0*v,v]),eps*Y])
            C=U@V.T;B=X@Y.T
            h=sum(swap_metric_numerator(np.kron(X[p*D:(p+1)*D,a],v)-np.kron(u,Y[p*D:(p+1)*D,a]),dims)
                  for p in range(d-2) for a in range(2))
            lhs=endpoint_numerator(C,(d,)+dims)
            rhs=2*eps**2*h+eps**4*endpoint_numerator(B,(d-2,)+dims)
            assert lhs==rhs and h>=0
            records.append({'remaining_sites':m,'local_dimension':d,'trial':trial,'epsilon':eps,'lhs':str(lhs),'rhs':str(rhs)})
out={'status':'exact finite consistency checks of proved algebraic identity','checks':len(records),'seed':2026100911,'records':records}
Path(__file__).with_name('GENERAL_BLOCK_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'checks':len(records),'status':'all passed'}))
