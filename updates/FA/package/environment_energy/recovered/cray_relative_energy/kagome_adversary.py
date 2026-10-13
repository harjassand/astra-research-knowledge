"""A compatible ferromagnetic environment defeats sign prediction on a kagome patch."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from experiment import kagome,local_pair,heisenberg

if __name__=='__main__':
    _,edges=kagome();h0,h1,sites=local_pair(edges,[0,1],(0,1,1.))
    n=len(sites);collar=list(range(2,n));W=heisenberg(n,[(i,j,-1) for i in collar for j in collar if i<j]).toarray()+2.5*np.eye(2**n)
    # W has kernel in the fully symmetric S_C=5/2 sector, next eigenvalue 5/2.
    results=[]
    for M in [10,100,1000]:
        e0=float(eigh(h0+M*W,eigvals_only=True)[0]);e1=float(eigh(h1+M*W,eigvals_only=True)[0])
        results.append({'M':M,'Eweak':e0,'Estrong':e1,'difference_numeric':e1-e0})
    out={'sites':sites,'description':'Five collar spins with ferromagnetic all-to-all exchange -M; same environment for both central-bond strengths.',
         'analytic_limit_difference':'1/4','rigorous_difference_lower_at_M_100':'47/476',
         'proof_bounds':{'compressed_Eweak':'1/4-21/10','compressed_Estrong':'1/2-21/10','environment_gap_at_M_100':250,'local_Hstrong_norm_bound':6,'lower_formula':'1/4 - 36/(250-12) = 47/476'},'runs':results}
    (Path(__file__).parent/'kagome_adversary.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
