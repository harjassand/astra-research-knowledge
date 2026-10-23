"""New full-original-action receiving operations; no historical suite replay."""
from pathlib import Path
from fractions import Fraction as F
import hashlib, json, resource, time, traceback
from coordinate_decoder import prepare, decode, action, norm_sq, matrix_frobenius_sq
from block_reset_recovery import prepare_recovery
from marked_atom import prepare_marked_certificate
import theta_hub_split

ROOT = Path(__file__).resolve().parents[1]


def jsonify(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {str(k): jsonify(v) for k,v in x.items()}
    if isinstance(x, (list,tuple)): return [jsonify(v) for v in x]
    return x


def coefficients(diag, ev):
    return dict(diagonal=[str(x) for x in diag],
                edges=[dict(edge=list(e),value=str(w)) for e,w in sorted(ev.items())])


def one(obj, mode, bundle):
    wall, cpu = time.perf_counter(), time.process_time()
    n = obj['n']; edges = sorted(tuple(sorted(e)) for e in obj['edges'])
    p0 = time.perf_counter()
    if mode == 'block_reset':
        form, design, plan = prepare_recovery(n, edges, bundle)
        summary = dict(blocks=len(form['blocks']), depth=max(form['depth']),
                       maximum_degree=form['maximum_degree'],
                       stop_messages=len(design['messages']))
    elif mode == 'theta_explicit':
        form, design = theta_hub_split.prepare(n, edges)
        plan = prepare(n, edges, design['colors'], 4)
        degrees = [0]*n
        for u,v in edges:
            degrees[u] += 1; degrees[v] += 1
        summary = dict(blocks=len(form['blocks']), maximum_degree=max(degrees))
    else:
        raise ValueError('operation')
    preparation = time.perf_counter()-p0
    colors = design['colors']; q = 4
    diag = [F((37*i+11)%31-15,13) for i in range(n)]
    ev = {(u,v):F((23*u+17*v+5)%43-21,17) for u,v in edges}
    noise = [[F((11*i+7*j+3)%19-9,101) for j in range(q)] for i in range(n)]
    p0 = time.perf_counter(); dx = action(n,q,colors,diag,ev)
    acquisition = time.perf_counter()-p0
    y = [[a+b for a,b in zip(row,e)] for row,e in zip(dx,noise)]
    p0 = time.perf_counter()
    d0,w0 = decode(plan,dx); assert d0 == diag and w0 == ev
    dh,wh = decode(plan,y)
    decode_seconds = time.perf_counter()-p0
    projected = action(n,q,colors,dh,wh)
    residual = [[a-b for a,b in zip(yr,pr)] for yr,pr in zip(y,projected)]
    # Orthogonality on every supported symmetric coefficient, in original cells.
    assert all(residual[i][colors[i]] == 0 for i in range(n))
    assert all(residual[u][colors[v]]+residual[v][colors[u]] == 0 for u,v in edges)
    err_d = [a-b for a,b in zip(dh,diag)]; err_w = {e:wh[e]-ev[e] for e in edges}
    f2 = matrix_frobenius_sq(err_d,err_w); e2=norm_sq(noise)
    ratio = f2/e2
    assert ratio <= 3 or (ratio-3)**2 <= 5  # Exact comparison with 3+sqrt(5).
    record = dict(mode=mode,n=n,m=len(edges),q=q,summary=summary,design=design,
                  original_coefficients=coefficients(diag,ev), noise=noise,
                  full_noiseless_actions=dx,observations=y,
                  output=coefficients(dh,wh),projected_actions=projected,
                  raw_residual=residual,raw_residual_norm_sq=norm_sq(residual),
                  exact_noiseless_reconstruction=True,
                  projected_numerical_residual_norm_sq='0',normal_equations_pass=True,
                  error_frobenius_sq=f2,noise_frobenius_sq=e2,ratio=ratio,
                  largest_component_vertices=max(map(lambda c:len(c['order']),plan['components'])),
                  actual_cut_gamma=plan['kappa2'],
                  timing=dict(preparation_seconds=preparation,
                              explicit_full_action_seconds=acquisition,
                              two_decodes_seconds=decode_seconds,
                              wall_seconds_before_serialization=time.perf_counter()-wall,
                              cpu_seconds_before_serialization=time.process_time()-cpu))
    return jsonify(record)


def main():
    wall,cpu = time.perf_counter(),time.process_time()
    stage='fixed_certificate_preparation'
    try:
        t=time.perf_counter()
        bundle=prepare_marked_certificate(ROOT/'sources/loaded_star_certificate.json',
                                           ROOT/'sources/marked_root_projection.json')
        certificate_time=time.perf_counter()-t
        result=dict(schema='astra-cycle10-original-actions/v1',operations=[],inputs=[],
                    shared_certificate_preparation_seconds=certificate_time,
                    source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in (ROOT/'src').glob('*.py')})
        for filename,modes in [
            ('adjacent_marks_mixed_theta_57.json',['block_reset','theta_explicit']),
            ('mixed_non_theta_adjacent_marks.json',['block_reset'])]:
            path=ROOT/'inputs'/filename; raw=path.read_bytes(); obj=json.loads(raw)
            result['inputs'].append(dict(path='inputs/'+filename,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
            for mode in modes:
                stage=filename+':'+mode
                record=one(obj,mode,bundle); record['input']='inputs/'+filename
                result['operations'].append(record)
        first,second=result['operations'][:2]
        assert first['original_coefficients']==second['original_coefficients']
        assert first['noise']==second['noise']
        result['same_theta_D_and_absolute_noise']=True
        out=ROOT/'results/RECEIVING.json'
        out.write_text(json.dumps(result,indent=2)+'\n')
        receipt=dict(wall_seconds=time.perf_counter()-wall,cpu_seconds=time.process_time()-cpu,
                      peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                      includes_serialization=True,result_bytes=out.stat().st_size,
                      result_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
                      operations=[{k:r[k] for k in ['input','mode','n','m','q','ratio','largest_component_vertices','summary']}
                                  for r in result['operations']])
        (ROOT/'results/RECEIVING_COST.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print(json.dumps(receipt,indent=2))
    except Exception:
        receipt=dict(stage=stage,wall_seconds=time.perf_counter()-wall,
                      cpu_seconds=time.process_time()-cpu,traceback=traceback.format_exc(),
                      peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)
        p=ROOT/'failed'/'RECEIVING_FAILURE.json'
        p.write_text(json.dumps(receipt,indent=2)+'\n')
        raise


if __name__=='__main__':
    main()
