"""Exact two-dimensional formula checked against a small dense Nystrom fixture."""
from pathlib import Path
import json
import numpy as np


def run():
    eta=.001
    rows=[]
    for r in [1,4,16,64,128]:
        U=np.eye(r+1)[:,:r]
        h=np.eye(r+1)[:,-1]
        Z=U+eta*h[:,None]
        C=U@U.T
        B=Z@np.linalg.inv(U.T@Z)@Z.T
        error=float(np.max(np.abs(np.linalg.eigvalsh(B-C))))
        expected=(r*eta**2+np.sqrt(r*r*eta**4+4*r*eta**2))/2
        assert abs(error-expected)<1e-12
        assert np.max(np.linalg.norm(Z-U,axis=0))<=eta+1e-12
        rows.append({'rank':r,'per_query_error':eta,'sampled_core_condition':1.0,
            'operator_error':error,'operator_error_over_eta':error/eta,
            'formula':float(expected)})
    return {'status':'coherent_noise_failure_reproduced','rows':rows,
            'meaning':'Individual action errors do not form one operator perturbation of the same norm.'}


if __name__=='__main__':
    result=run()
    Path(__file__).with_name('higher_rank_failure_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
