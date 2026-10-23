"""Nonperturbative full-support construction: t=1, three matrix actions."""
from __future__ import annotations
import json,pathlib,resource,time
import numpy as np
from scipy import sparse
from scipy.linalg import eigh
from anchored import triangle_cover, StarAnchoredRecovery
from recovery import adjacency

ROOT=pathlib.Path(__file__).resolve().parent
SEED=202610230755


def case(sheets,rng):
    n,edges,colors,v,_,(nb,eb)=triangle_cover(sheets,rng)
    a=adjacency(n,edges)
    gap=float(eigh(3*np.eye(n)-a.toarray(),eigvals_only=True,subset_by_index=[1,1])[0])
    bound_g=1/4+3/(2*gap)
    K=np.sqrt(3/4*(1+32*bound_g))
    rec=StarAnchoredRecovery(n,edges,colors,v,1.0,K)
    green_diag=np.diag(np.linalg.inv(rec.base.B.toarray()))
    actual_g=float(green_diag.max())
    tighter_K=np.sqrt(3/4*(1+32*actual_g))
    tighter_bound=rec.rho*(tighter_K+(1+tighter_K*np.sqrt(rec.rho**2+4/3))*rec.anchor_gain)
    assert actual_g<=bound_g+1e-8
    h=rec.full_matrix(rng.standard_normal(n+len(edges)))
    out=rec.decode(h@rec.X)
    relative=float(np.linalg.norm((out-h).data)/np.linalg.norm(h.data))
    assert relative<1e-10
    noise=rng.standard_normal((n,3));noise/=np.linalg.norm(noise)
    noisy=rec.decode(noise).toarray()
    noise_op=float(np.max(np.abs(eigh(noisy,eigvals_only=True))))
    assert noise_op<tighter_bound+1e-8
    # A deliberately targeted error: one normalized cycle witness.
    cycle_error=rec.decode(rec.Z[1]).toarray()
    cycle_op=float(np.max(np.abs(eigh(cycle_error,eigvals_only=True))))
    # A lower bound on every exact decoder, using a consistent noisy input.
    H0=sparse.eye(n,format='csr')+a
    old_kernel_measurement=H0@rec.X
    observed=float(np.linalg.norm(rec.decode(old_kernel_measurement/np.linalg.norm(old_kernel_measurement)).data))
    predicted=np.sqrt(2*n)
    assert abs(observed-predicted)<1e-8
    explicit_left=None
    if n<=48:
        M=rec.full_measurement_matrix().toarray();p=n+len(edges)
        decoder=[];e=np.zeros(3*n)
        for j in range(3*n):
            e[j]=1;z=rec.decode(e.reshape(n,3));e[j]=0
            ee=np.asarray(rec.full_edges)
            decoder.append(np.r_[z.diagonal(),np.sqrt(2)*np.asarray(z[ee[:,0],ee[:,1]]).ravel()])
        decoder=np.column_stack(decoder)
        explicit_left=float(np.max(np.abs(decoder@M-np.eye(p))))
        assert explicit_left<1e-10
    graph={"n":n,"full_edges":edges,"colors":colors.tolist(),"vertex":v,"t":1.0,
           "cycles":rec.cycles,"base_n":nb,"base_edges":eb}
    (ROOT/'data'/f'star_full_cover_{n}.json').write_text(json.dumps(graph))
    return {"n":n,"q":3,"m":len(edges),"t":1.0,"observed_full_graph_laplacian_gap":gap,
            "max_Green_diagonal_after_star_deletion":actual_g,"gap_based_Green_diagonal_upper_bound":bound_g,
            "cycle_pairings":rec.pairings.tolist(),"cycle_Gram_max_error":float(np.max(np.abs(rec.Z.reshape(3,-1)@rec.Z.reshape(3,-1).T-np.eye(3)))),
            "row_norm_max":float(np.linalg.norm(rec.X,axis=1).max()),
            "operator_bound_using_observed_gap":float(rec.operator_bound),"operator_bound_using_observed_Green_diagonal":float(tighter_bound),
            "sample_unit_noise_operator_error":noise_op,"targeted_cycle_noise_operator_error":cycle_op,
            "F_inverse_lower_bound":predicted,"F_gain_observed_on_old_kernel_noise":observed,
            "noiseless_relative_F_error":relative,"explicit_left_inverse_max_abs_error":explicit_left}


def main():
    start=time.perf_counter();cpu=time.process_time();rng=np.random.default_rng(SEED)
    cases=[case(s,rng) for s in (1,2,4,8,16,32,64,128)]
    result={"schema":"astra-fresh-p1-star-anchoring-v1","seed":SEED,
            "evidence_type":"floating-point producer diagnostics; not a statistical performance study or interval certificate",
            "cases":cases,"resources":{"wall_seconds":time.perf_counter()-start,"cpu_seconds":time.process_time()-cpu,
              "peak_process_RSS_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
              "additional_workers":0,"model_inference_tokens":"UNKNOWN","model_inference_cost":"UNKNOWN"}}
    (ROOT/'STAR_DIAGNOSTICS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({"cases":len(cases),"largest":cases[-1],"resources":result['resources']},indent=2))

if __name__=='__main__':main()
