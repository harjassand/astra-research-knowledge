"""Two new native full-action receivers, with a matched star control.

No predecessor suite is run. All arithmetic inputs and recovered coefficients
are exact rationals. q is charged in full; recognizing the original support,
actual sparse action accumulation, projections, and output are separately timed.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib, json, resource, time
from block_spider_recovery import native_blocks, prepare_design
from coordinate_decoder import decode, action, norm_sq, matrix_frobenius_sq

ROOT = Path(__file__).resolve().parents[1]


def fraction_tree(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k):fraction_tree(v) for k,v in x.items()}
    if isinstance(x, (list, tuple)):
        return [fraction_tree(v) for v in x]
    return x


def vec_edges(es):
    return [[u,v,str(w)] for (u,v),w in sorted(es.items())]


def receiving(input_path):
    t0, c0 = time.perf_counter(), time.process_time()
    raw = input_path.read_bytes()
    inp = json.loads(raw)
    n, edges = inp['n'], inp['edges']
    stages = {}
    t = time.perf_counter()
    form = native_blocks(n, edges)
    stages['native_graph_recognition'] = time.perf_counter()-t
    t = time.perf_counter()
    diagonal = [F((37*i+11)%31-15,13) for i in range(n)]
    edge_values = {(u,v):F((23*u+17*v+5)%43-21,17) for u,v in form['edges']}
    p = form['p']
    common_noise = [[F((11*i+7*j+3)%19-9,101) for j in range(p+2)] for i in range(n)]
    stages['exact_input_and_noise_construction'] = time.perf_counter()-t
    operations = []
    for mode in ('stable','star'):
        sub = {}
        t = time.perf_counter()
        plan, design = prepare_design(form, mode)
        sub['coloring_decoder_preparation_shape_certificate'] = time.perf_counter()-t
        q, colors = design['q'], design['colors']
        noise = [r+[F(0)]*(q-(p+2)) for r in common_noise]
        t = time.perf_counter()
        exact_action = action(n,q,colors,diagonal,edge_values)
        observed = [[a+b for a,b in zip(r,s)] for r,s in zip(exact_action,noise)]
        sub['all_original_action_acquisition_and_noise_assembly'] = time.perf_counter()-t
        t = time.perf_counter()
        exact_recovered = decode(plan,exact_action)
        assert exact_recovered == (diagonal,edge_values)
        recovered_diagonal, recovered_edges = decode(plan,observed)
        sub['noiseless_and_noisy_decoding'] = time.perf_counter()-t
        t = time.perf_counter()
        projected = action(n,q,colors,recovered_diagonal,recovered_edges)
        residual = [[a-b for a,b in zip(r,s)] for r,s in zip(observed,projected)]
        assert all(residual[i][colors[i]] == 0 for i in range(n))
        assert all(residual[u][colors[v]]+residual[v][colors[u]] == 0 for u,v in form['edges'])
        delta_diag = [a-b for a,b in zip(recovered_diagonal,diagonal)]
        delta_edges = {e:recovered_edges[e]-w for e,w in edge_values.items()}
        noise_sq = norm_sq(noise)
        error_sq = matrix_frobenius_sq(delta_diag,delta_edges)
        ratio_sq = error_sq/noise_sq
        if mode == 'stable':
            assert ratio_sq <= 3 or (ratio_sq-3)**2 <= 5
        else:
            assert ratio_sq <= 2
        # Projected normal equations certify Pi(Y); projected-action residual
        # is zero exactly. Raw observation residual is generally nonzero.
        sub['exact_projection_and_error_check'] = time.perf_counter()-t
        operations.append(dict(design=design, original_action=exact_action,
                               noise=noise, observed=observed,
                               recovered_diagonal=recovered_diagonal,
                               recovered_edges=vec_edges(recovered_edges),
                               projected_action=projected,
                               normal_equations_exact=True,
                               noiseless_reconstruction_exact=True,
                               projected_action_residual_sq=F(0),
                               raw_observation_residual_sq=norm_sq(residual),
                               noise_frobenius_sq=noise_sq,
                               error_frobenius_sq=error_sq,
                               error_to_noise_frobenius_sq=ratio_sq,
                               stages_seconds=sub))
    assert operations[0]['noise_frobenius_sq'] == operations[1]['noise_frobenius_sq']
    result = dict(schema='astra-block-spider-full-action-receiver/v1', name=inp['name'],
                  input_filename=input_path.name,
                  input_bytes=len(raw), input_sha256=hashlib.sha256(raw).hexdigest(),
                  native_form=form, original_diagonal=diagonal,
                  original_edge_values=vec_edges(edge_values), operations=operations,
                  same_D_and_absolute_noise_norm=True, stages_seconds=stages,
                  exact_arithmetic='fractions.Fraction; bit cost additional',
                  scope='New original-edge-list preparation and full original-action recovery. No empirical speedup or sharp operator constant claimed.')
    t = time.perf_counter()
    out = ROOT/'results'/f"{inp['name']}_receiving.json"
    out.write_text(json.dumps(fraction_tree(result),indent=2)+'\n')
    serialization = time.perf_counter()-t
    return dict(input=input_path.name, result=out.name, n=n,m=len(edges),p=p,
                blocks=len(form['blocks']), max_degree=form['max_degree'],
                actions=[o['design']['q'] for o in operations],
                max_component_vertices=[max(w['vertices'] for w in o['design']['component_witnesses']) for o in operations],
                error_to_noise_frobenius_sq=[str(o['error_to_noise_frobenius_sq']) for o in operations],
                total_wall_seconds=time.perf_counter()-t0,
                total_cpu_seconds=time.process_time()-c0,
                serialization_seconds=serialization,
                peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)


def main():
    t0,c0=time.perf_counter(),time.process_time()
    records=[receiving(ROOT/'inputs'/name) for name in
             ('native_K24_obstruction_16.json','native_p3_unequal_branch_27.json')]
    costs=dict(records=records, total_wall_seconds=time.perf_counter()-t0,
               total_cpu_seconds=time.process_time()-c0,
               peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
               scope='Both new native receiver bodies and source serialization; excludes startup, this final cost write, research and authoring.')
    (ROOT/'results/RECEIVING_COSTS.json').write_text(json.dumps(costs,indent=2)+'\n')
    print(json.dumps(costs,indent=2))


if __name__=='__main__':
    main()
