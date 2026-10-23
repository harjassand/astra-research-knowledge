"""Adversarial and algebraic diagnostics; these do not replace the proofs."""
from __future__ import annotations
import json, pathlib, resource, time, platform
import numpy as np
import scipy
from scipy import sparse
from scipy.linalg import eigh
from scipy.sparse.linalg import eigsh
from recovery import SimplexRecovery, complete_graph_lift, adjacency, torus, simplex

ROOT = pathlib.Path(__file__).resolve().parent
SEED = 202610230703


def small_case(n, edges, colors, q, rng):
    rec = SimplexRecovery(n, edges, colors, q)
    m = len(edges)
    a = rec.measurement_matrix().toarray()
    s = rec.row_sum_matrix().toarray()
    b = rec.B.toarray()
    gram = a.T @ a
    predicted = (q + 1) / q * np.eye(n + m) - s.T @ s / q
    spectrum = np.linalg.eigvalsh(gram)
    spectrum_pred = np.sort(np.r_[np.linalg.eigvalsh(b) / (2 * q), np.full(m, (q + 1) / q)])
    green = np.linalg.inv(b)
    inv_pred = q / (q + 1) * (np.eye(n + m) + 2 * s.T @ green @ s)
    inv_actual = np.linalg.inv(gram)
    h = rec.matrix(rng.standard_normal(n + m))
    y = h @ rec.X
    noise = rng.standard_normal((n, q)); noise /= np.linalg.norm(noise)
    decoded = rec.decode(y + noise)
    least_squares = rec.matrix(np.linalg.lstsq(a, (y + noise).ravel(), rcond=None)[0])
    i = int(np.argmax(np.diag(green)))
    col = inv_actual[:, i]
    e_adv = (a @ col / np.sqrt(inv_actual[i, i])).reshape(n, q)
    h_adv = rec.decode(e_adv).toarray()
    norm_op_adv = np.max(np.abs(np.linalg.eigvalsh(h_adv)))
    g = float(np.max(np.diag(green)))
    k_lower = np.sqrt(q / (q + 1) * (1 + 2 * g))
    k_upper = np.sqrt(q / (q + 1) * (1 + 2 * (q + 1) ** 2 * g))
    checks = {
        "gram_max_abs_error":float(np.max(np.abs(gram - predicted))),
        "full_spectrum_max_abs_error":float(np.max(np.abs(spectrum - spectrum_pred))),
        "inverse_max_abs_error":float(np.max(np.abs(inv_actual - inv_pred))),
        "noiseless_relative_F_error":float(np.linalg.norm((rec.decode(y) - h).toarray()) / np.linalg.norm(h.toarray())),
        "decoder_vs_dense_lstsq_F_error":float(np.linalg.norm((decoded - least_squares).toarray())),
        "diagonal_adversary_noise_F_norm":float(np.linalg.norm(e_adv)),
        "diagonal_adversary_target_error":float(abs(h_adv[i, i])),
        "predicted_target_error":float(k_lower),
        "diagonal_adversary_operator_error":float(norm_op_adv),
        "operator_lower_bound":float(k_lower),
        "operator_upper_bound":float(k_upper),
        "F_inverse_constant":float(1 / np.sqrt(spectrum[0])),
    }
    assert checks['gram_max_abs_error'] < 1e-11
    assert checks['full_spectrum_max_abs_error'] < 1e-10
    assert checks['inverse_max_abs_error'] < 1e-8
    assert checks['noiseless_relative_F_error'] < 1e-10
    assert checks['decoder_vs_dense_lstsq_F_error'] < 1e-8
    assert abs(checks['diagonal_adversary_noise_F_norm'] - 1) < 1e-9
    assert abs(abs(h_adv[i, i]) - k_lower) < 1e-8
    assert norm_op_adv <= k_upper + 1e-9
    return {"n":n,"m":m,"q":q,**checks}


def lift_case(sheets, rng):
    q = 3
    n, full_edges, colors = complete_graph_lift(q, sheets, rng)
    full_adj = adjacency(n, full_edges)
    components = sparse.csgraph.connected_components(full_adj, directed=False)[0]
    if components != 1:
        raise RuntimeError("fixed seed produced a disconnected lift; record instead of silently selecting")
    removed = full_edges[0]
    edges = full_edges[1:]
    rec = SimplexRecovery(n, edges, colors, q)
    lap = q * np.eye(n) - full_adj.toarray()
    values, vectors = eigh(lap, driver='evr')
    lp = (vectors[:, 1:] / values[None, 1:]) @ vectors[:, 1:].T
    a, b = removed
    z = lp[:, a] + lp[:, b]
    scalar = lp[a, a] + lp[b, b] + 2 * lp[a, b]
    green_formula = lp - (z[:, None] + z[None, :]) / 2 + (1 + scalar) / 4
    bmat = rec.B.toarray()
    green = np.linalg.inv(bmat)
    formula_error = float(np.max(np.abs(green - green_formula)))
    g = float(np.max(np.diag(green)))
    gap = float(values[1])
    bound_g = 1/4 + 3/(2*gap)
    lambda_min = float(eigh(bmat, subset_by_index=[0, 0], driver='evr', eigvals_only=True)[0])
    kf = np.sqrt(2*q/lambda_min)
    h = rec.matrix(rng.standard_normal(n + len(edges)))
    y = h @ rec.X
    out = rec.decode(y)
    relative_error = float(np.linalg.norm((out-h).data)/np.linalg.norm(h.data))
    assert formula_error < 1e-7
    assert g <= bound_g + 1e-8
    assert kf + 1e-8 >= np.sqrt(q*n/2)
    assert relative_error < 1e-9
    graph_record={"q":q,"n":n,"colors":colors.tolist(),"full_edges":full_edges,"removed_edge":removed}
    (ROOT/'data'/f'lift_{n}.json').write_text(json.dumps(graph_record))
    return {"n":n,"q":q,"m":len(edges),"observed_full_graph_laplacian_gap":gap,
            "max_Green_diagonal":g,"gap_based_Green_upper_bound":bound_g,
            "Green_rank_one_formula_max_abs_error":formula_error,
            "operator_lower_bound":float(np.sqrt(q/(q+1)*(1+2*g))),
            "operator_upper_bound":float(np.sqrt(q/(q+1)*(1+2*(q+1)**2*g))),
            "F_inverse_constant":float(kf),"noiseless_relative_F_error":relative_error}


def torus_fourier(d, side):
    q=2*d
    shape=(side,)*d
    axes=np.indices(shape)
    eigen=4*np.sum(np.sin(np.pi*axes/side)**2,axis=0)
    inverse=np.zeros(shape)
    mask=eigen>1e-14
    inverse[mask]=1/eigen[mask]
    kernel=np.fft.ifftn(inverse).real
    diag=float(kernel.flat[0])
    a=(0,)*d
    b=(1,)+(0,)*(d-1)
    rab=2*(diag-kernel[b])
    green_diag=1/4 + diag + (diag+kernel[b])/2 - kernel - np.roll(kernel, 1, axis=0)
    g=float(np.max(green_diag))
    n=side**d
    trace=n*(1/4+2*diag-rab/4)
    rayleigh=n*(1/4+diag-rab/4)
    assert trace/2-1e-8 <= rayleigh <= trace+1e-8
    assert 2*diag-1e-8 <= g <= 1/4+4*diag+1e-8
    return {"dimension":d,"side":side,"n":n,"q":q,"laplacian_pseudoinverse_diagonal":diag,
            "adjacent_effective_resistance":float(rab),"max_Green_diagonal":g,
            "operator_lower_bound":float(np.sqrt(q/(q+1)*(1+2*g))),
            "operator_upper_bound":float(np.sqrt(q/(q+1)*(1+2*(q+1)**2*g))),
            "F_inverse_lower_bound":float(np.sqrt(2*q*rayleigh)),
            "F_inverse_upper_bound":float(np.sqrt(2*q*trace))}


def negative_checks():
    # A whole q-regular cover has a genuine null matrix I+A.
    q=3; n=4; edges=[(i,j) for i in range(n) for j in range(i+1,n)]
    x=simplex(q); a=adjacency(n,edges).toarray(); kernel=(np.eye(n)+a)@x
    rejected=False
    try: SimplexRecovery(n,edges,np.arange(n),q)
    except ValueError as exc: rejected="noninjective" in str(exc)
    assert rejected
    # A four-leaf star in R^3 violates closed-neighborhood distinctness and
    # also the degree bound; it must not be silently treated by this theorem.
    wrong=False
    try: SimplexRecovery(5,[(0,j) for j in range(1,5)],[0,1,2,3,1],3)
    except ValueError: wrong=True
    assert wrong
    return {"unmodified_regular_cover_null_residual":float(np.linalg.norm(kernel)),
            "unmodified_regular_cover_rejected":rejected,"inadmissible_support_rejected":wrong}


def main():
    t0=time.perf_counter(); cpu0=time.process_time()
    (ROOT/'data').mkdir(exist_ok=True)
    rng=np.random.default_rng(SEED)
    small=[]
    for n in (6,12,24):
        edges=[(i,i+1) for i in range(n-1)]
        small.append(small_case(n,edges,np.arange(n)%3,2,rng))
    for q in (3,4,5):
        n,edges,colors=complete_graph_lift(q,3,rng)
        small.append(small_case(n,edges[1:],colors,q,rng))
    # A disconnected union with isolated vertices and several missing edges.
    small.append(small_case(8,[(0,1),(1,2),(3,4)],[0,1,2,0,1,0,0,0],2,rng))
    lifts=[lift_case(s,rng) for s in (8,16,32,64,128,256)]
    tori=[torus_fourier(d,l) for d,ls in ((1,(12,24,48,96,192,384)),
           (2,(10,20,40,80,160)),(3,(7,14,28,56))) for l in ls]
    result={"schema":"astra-fresh-p1-simplex-green-diagnostics-v1","seed":SEED,
            "evidence_type":"floating-point producer diagnostics; exact proofs are separate",
            "small_cases":small,"lift_cases":lifts,"torus_fourier_cases":tori,
            "negative_checks":negative_checks(),
            "resources":{"wall_seconds":time.perf_counter()-t0,"cpu_seconds":time.process_time()-cpu0,
            "peak_process_RSS_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
            "python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,
            "model_inference_tokens":"UNKNOWN","model_inference_cost":"UNKNOWN",
            "additional_workers":0}}
    (ROOT/'DIAGNOSTICS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({"small_cases":len(small),"largest_lift":lifts[-1],"torus_rows":len(tori),
                      "negative_checks":result['negative_checks'],"resources":result['resources']},indent=2))

if __name__=='__main__':main()
