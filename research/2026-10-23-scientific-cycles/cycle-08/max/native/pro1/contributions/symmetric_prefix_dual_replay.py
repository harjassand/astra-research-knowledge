#!/usr/bin/env python3
"""New focused exact k5 scalar-gradient check from physical move/stay histories.

This does not prove an all-k assertion. The token normal form and its analytic
contraction do that. Here the coefficient is reconstructed independently from
the retained physical representation, not from the new counting formula.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
from math import comb
import hashlib,json,platform,resource,sys,time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'representation'))
from four_call_representation import history,charge

def run(k=5):
    start=time.perf_counter()
    words=list(product((0,1,2),repeat=k))
    baths=list(product((1,2),repeat=k))
    masks=[0]+[1<<j for j in range(k)]+[(1<<j)|(1<<l) for j,l in combinations(range(k),2)]
    groups=defaultdict(list)
    for i,x in enumerate(words):
        for u,bath in enumerate(baths):
            for mask in masks:
                y,seed,w,r=history(x,0,bath,mask)
                groups[(charge(x),y,seed,w)].append((i,u,r))
    # Only off-diagonal input entries are needed by H and by T(sigma H).
    # The zeroth-history cosine derivative is input diagonal and drops out.
    g1=defaultdict(int)
    for (q,y,seed,w),paths in groups.items():
        delta=len(w)-k
        if not delta:continue
        for i,u,r in paths:
            for j,v,s in paths:
                if i!=j and r+s==2:
                    g1[i,u,j,v]+=delta*(1 if r==s else -1)
    g1={key:a for key,a in g1.items() if a}
    del groups
    weight=[sum(x==1 for x in w) for w in baths]
    tau={(u,v):F(1,(k+1)*comb(k,weight[u]))
         for u in range(2**k) for v in range(2**k) if weight[u]==weight[v]}
    h=defaultdict(F)
    for (i,u,j,v),a in g1.items():h[i,j]+=a*tau.get((v,u),0)
    h={ij:a for ij,a in h.items() if a}
    assert all(h.get((j,i),0)==a for (i,j),a in h.items())
    sigma=[F(1,2**(k+charge(w))) for w in words]
    var=sum(sigma[i]*a*a for (i,j),a in h.items())
    operator=defaultdict(F)
    for (i,u,j,v),a in g1.items():operator[u,v]+=sigma[j]*h.get((j,i),0)*a
    operator={uv:a for uv,a in operator.items() if a}
    assert all(operator.get((u,v),0)==(var if u==v else 0)
               for u in range(2**k) for v in range(2**k))
    predicted=F(k*(k-1),8)-F(1,8)*sum(F((k-2*m-1)*comb(2*m,m),4**m) for m in range((k-2)//2+1))
    assert var==predicted
    source=ROOT/'representation/four_call_representation.py'
    return {'scope':'One new exact k5 physical-history check; analytic proof is not a finite-check count',
            'k':k,'input_dimension':3**k,'prefix_dimension':2**k,
            'offdiagonal_G1_entries':len(g1),'H_sym_nonzero_entries':len(h),
            'exact_v':str(var),'exact_count_formula':str(predicted),
            'scalar_operator_identity':True,'T_sigma_H_sym':'v times identity on the entire prefix',
            'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'wall_seconds':time.perf_counter()-start,'max_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'python':platform.python_version(),'total_discovery_inference_review_cost':'unknown'}

if __name__=='__main__':
    result=run()
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
