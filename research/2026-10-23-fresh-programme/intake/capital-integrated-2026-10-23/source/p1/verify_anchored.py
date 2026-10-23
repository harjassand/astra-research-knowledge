"""Full-support checks, cycle witnesses, and failed perturbations."""
from __future__ import annotations
import json, pathlib, resource, time
import numpy as np
from scipy import sparse
from scipy.linalg import eigh
from anchored import triangle_cover, AnchoredRecovery
from recovery import adjacency, simplex, torus

ROOT = pathlib.Path(__file__).resolve().parent
SEED = 202610230734


def case(sheets, rng):
    n, edges, colors, v, cycle, (nb, eb) = triangle_cover(sheets, rng)
    a = adjacency(n, edges).toarray()
    ab = adjacency(nb, eb).toarray()
    gap_b = float(eigh(3*np.eye(nb)-ab, eigvals_only=True, subset_by_index=[1, 1])[0])
    gap_f = float(eigh(3*np.eye(n)-a, eigvals_only=True, subset_by_index=[1, 1])[0])
    transfer = 1/(6/gap_b+1/3)
    assert gap_f + 1e-10 >= transfer
    # A fixed t across all sampled sizes.  The theorem uses an all-size gap
    # bound, not the fact that finitely many sampled instances passed.
    t = 0.01
    g_bound = 1/4 + 3/(2*gap_f)
    K = np.sqrt(3/4*(1+32*g_bound))
    rec = AnchoredRecovery(n, edges, colors, 3, v, cycle, t, K)
    m = len(edges)
    h = rec.full_matrix(rng.standard_normal(n+m))
    y = h @ rec.X
    decoded = rec.decode(y)
    err = float(np.linalg.norm((decoded-h).data)/np.linalg.norm(h.data))
    anchor_error = float(abs(decoded[rec.u, rec.v]-h[rec.u, rec.v]))
    noise = rng.standard_normal((n, 3)); noise /= np.linalg.norm(noise)
    error_noise = rec.decode(noise).toarray()
    error_op = float(np.max(np.abs(eigh(error_noise, eigvals_only=True))))
    # The measurement has a nonzero response to the old kernel H0.
    kernel_noise = rec.H0 @ rec.X
    kernel_noise /= np.linalg.norm(kernel_noise)
    kernel_response = rec.decode(kernel_noise).toarray()
    observed_f_ratio = float(np.linalg.norm(kernel_response))
    predicted_f_lower = rec.rho*np.sqrt(n)/t
    # Left-null witness on the unmodified design and exact anchor functional.
    probe0 = rec.X.copy(); rec.X = rec.X0
    M0 = rec.full_measurement_matrix()
    rec.X = probe0
    null_residual = float(np.linalg.norm(M0.T @ rec.Z.ravel()))
    anchor_from_y = float(np.sqrt(3)/t * np.sum(rec.Z*(rec.rho*y)))
    # Correct local linear system formula, independent of full Gram inversion.
    explicit_left_inverse_error = None
    if n <= 48:
        M = rec.full_measurement_matrix().toarray()
        # Form reconstruction-coordinate matrix by applying the actual decoder.
        columns=[]
        e=np.zeros(n*3)
        for j in range(n*3):
            e[j]=1
            out=rec.decode(e.reshape(n,3))
            off=np.asarray(out[np.asarray(edges)[:,0],np.asarray(edges)[:,1]]).ravel()
            columns.append(np.r_[out.diagonal(), np.sqrt(2)*off])
            e[j]=0
        # Full model sorts edges, so the output coordinate order must match it.
        edge_index={tuple(sorted(edge)):i for i,edge in enumerate(edges)}
        order=np.r_[np.arange(n), n+np.array([edge_index[e] for e in rec.full_edges])]
        decoder=np.column_stack(columns)[order]
        explicit_left_inverse_error=float(np.max(np.abs(decoder@M-np.eye(n+m))))
        assert explicit_left_inverse_error < 1e-8
    assert err < 1e-9
    assert null_residual < 1e-12
    assert abs(anchor_from_y - float(h[rec.u,rec.v])) < 1e-9
    assert abs(observed_f_ratio-predicted_f_lower) < 1e-6*predicted_f_lower
    assert error_op <= rec.operator_bound + 1e-8
    record={"n":n,"full_edges":edges,"colors":colors.tolist(),"vertex":v,"cycle":cycle,"t":t,
            "base_n":nb,"base_edges":eb}
    (ROOT/'data'/f'full_triangle_cover_{n}.json').write_text(json.dumps(record))
    return {"n":n,"m":m,"q":3,"t":t,"base_laplacian_gap":gap_b,"full_laplacian_gap":gap_f,
            "proved_gap_transfer_lower_bound_using_observed_base_gap":transfer,
            "cycle_witness_F_norm":float(np.linalg.norm(rec.Z)),"left_null_witness_residual":null_residual,
            "row_norm_max":float(np.max(np.linalg.norm(rec.X,axis=1))),
            "internal_decoder_K_upper_bound_using_observed_gap":float(K),
            "operator_error_upper_bound_using_observed_gap":float(rec.operator_bound),
            "sample_unit_noise_operator_error":error_op,"F_amplification_constructive_lower_bound":predicted_f_lower,
            "F_amplification_observed_on_old_kernel_noise":observed_f_ratio,
            "noiseless_relative_F_error":err,"anchor_entry_absolute_error":anchor_error,
            "explicit_left_inverse_max_abs_error":explicit_left_inverse_error,
            "small_system_condition_number":float(np.linalg.cond(rec.small))}


def torus_case(rng):
    d=3; side=7; q=2*d
    n,edges,colors=torus(d,side)
    idx=lambda x:int(np.ravel_multi_index(tuple(x),(side,)*d))
    v=idx([0,0,0])
    cycle=[idx(x) for x in ([1,0,0],[2,0,0],[2,1,0],[1,1,0])]
    rec=AnchoredRecovery(n,edges,colors,q,v,cycle,0.01)
    g=float(np.max(np.diag(np.linalg.inv(rec.base.B.toarray()))))
    K=np.sqrt(q/(q+1)*(1+2*(q+1)**2*g))
    assert rec.t*K<1
    h=rec.full_matrix(rng.standard_normal(n+len(edges)))
    relative=float(np.linalg.norm((rec.decode(h@rec.X)-h).data)/np.linalg.norm(h.data))
    assert relative<1e-9
    return {"dimension":d,"side":side,"n":n,"q":q,"t":rec.t,"internal_Green_diagonal_max":g,
            "internal_decoder_K_bound":float(K),"noiseless_relative_F_error":relative,
            "full_support":True,"anchor_cycle":cycle,"row_norm_max":float(np.linalg.norm(rec.X,axis=1).max())}


def failed_scalar_perturbation(rng):
    n,edges,colors,v,cycle,_=triangle_cover(2,rng)
    A=adjacency(n,edges).toarray(); H0=np.eye(n)+A
    X0=simplex(3)[colors]
    scale=np.ones(n); scale[v]=0.7
    X=scale[:,None]*X0
    H=H0/(scale[:,None]*scale[None,:])
    residual=float(np.linalg.norm(H@X))
    assert residual<1e-12
    return {"row_rescaling_only_null_residual":residual,"explanation":"Row scaling preserves a congruent nonzero stress; a change of projective direction is essential."}


def main():
    start=time.perf_counter(); cpu=time.process_time()
    rng=np.random.default_rng(SEED)
    cases=[case(s,rng) for s in (1,2,4,8,16,32,64)]
    result={"schema":"astra-fresh-p1-anchored-full-support-v1","seed":SEED,
            "evidence_type":"floating-point producer diagnostics, not independent or interval-certified verification",
            "triangle_cover_cases":cases,"full_torus_case":torus_case(rng),
            "failed_scalar_perturbation":failed_scalar_perturbation(rng),
            "resources":{"wall_seconds":time.perf_counter()-start,"cpu_seconds":time.process_time()-cpu,
                         "peak_process_RSS_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                         "additional_workers":0,"model_inference_tokens":"UNKNOWN","model_inference_cost":"UNKNOWN"}}
    (ROOT/'ANCHORED_DIAGNOSTICS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({"case_count":len(cases),"largest_full_support_case":cases[-1],
                      "full_torus_case":result['full_torus_case'],"failed_scalar_perturbation":result['failed_scalar_perturbation'],
                      "resources":result['resources']},indent=2))

if __name__=='__main__':main()
