"""Check the residual certificates and the unbalanced-l2 counterexample."""
from __future__ import annotations
import json,pathlib,resource,time
import numpy as np
from scipy.linalg import eigh
from recovery import SimplexRecovery, adjacency

ROOT=pathlib.Path(__file__).resolve().parent
SEED=202610230825


def main():
    start=time.perf_counter();cpu=time.process_time();rng=np.random.default_rng(SEED)
    results=[]
    for n in (32,128,512,1024):
        data=json.loads((ROOT/'data'/f'lift_{n}.json').read_text())
        q=data['q'];removed=tuple(data['removed_edge']);full=data['full_edges']
        edges=[e for e in full if tuple(e)!=removed]
        rec=SimplexRecovery(n,edges,data['colors'],q)
        g=float(np.diag(np.linalg.inv(rec.B.toarray())).max())
        gamma=float(eigh(q*np.eye(n)-adjacency(n,full).toarray(),eigvals_only=True,subset_by_index=[1,1])[0])
        s=np.zeros(n);s[list(removed)]=1
        S=rec.row_sum_matrix()
        def error(r):
            a=rec.factor.solve(r)
            h=rec.matrix((2*q/(q+1))*(S.T@a)).toarray()
            return float(np.max(np.abs(eigh(h,eigvals_only=True)))),a
        r=np.ones(n)/np.sqrt(n)
        err_unbalanced,a=error(r)
        lower=q*np.sqrt(n)/(2*(q+1))
        assert err_unbalanced+1e-9>=lower
        assert np.mean(a)+1e-9>=np.sqrt(n)/4
        r=rng.standard_normal(n);r-=r.mean();r/=np.linalg.norm(r)
        err_balanced,_=error(r)
        bound_balanced=2*q/gamma*(1+np.linalg.norm(s)/2)*np.linalg.norm(r)
        bound_l1=2*q*g*np.linalg.norm(r,1)
        assert err_balanced<=min(bound_balanced,bound_l1)+1e-8
        raw=rng.standard_normal(n)
        corrected=raw-s*(raw.sum()/2)
        assert abs(corrected.sum())<1e-10
        # Verify that a constant correction has exactly the stated residual.
        delta=np.full(n,raw.sum()/4)
        correction_identity=float(np.max(np.abs((raw-rec.B@delta)-corrected)))
        assert correction_identity<1e-10
        results.append({'n':n,'q':q,'unbalanced_unit_l2_operator_error':err_unbalanced,
              'proved_unbalanced_error_lower_bound':lower,'balanced_unit_l2_operator_error':err_balanced,
              'balanced_l2_certificate_using_observed_gap':float(bound_balanced),
              'l1_certificate_using_observed_Green_diagonal':float(bound_l1),
              'balanced_residual_sum':float(r.sum()),'constant_correction_identity_max_error':correction_identity})
    result={'schema':'astra-fresh-p1-residual-certificates-v1','seed':SEED,
            'evidence_type':'floating-point diagnostic of exact residual inequalities; not an interval certificate',
            'cases':results,'resources':{'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,
              'peak_process_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
              'additional_workers':0,'model_inference_tokens':'UNKNOWN','model_inference_cost':'UNKNOWN'}}
    (ROOT/'RESIDUAL_DIAGNOSTICS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
