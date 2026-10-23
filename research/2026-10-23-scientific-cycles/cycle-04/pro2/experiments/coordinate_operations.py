#!/usr/bin/env python3
"""One fixed exact experiment: two good operations and a same-graph bad seed."""
import json, sys, time, resource
from fractions import Fraction as F
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from coordinate_decoder import prepare, decode, action, norm_sq, matrix_frobenius_sq, squared_path, forest_prism, cut_witness


def encode(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x, (list,tuple)): return [encode(v) for v in x]
    return x


def edge_list(values):
    return [[u,v,str(w)] for (u,v),w in values.items()]


def test_operation(name, n, edges, colors, q, bound_sq):
    start, cpu = time.perf_counter(), time.process_time()
    plan = prepare(n, edges, colors, q)
    prep = time.perf_counter()-start
    diagonal = [F((7*i)%23-11,13) for i in range(n)]
    values = {e:F((11*e[0]+17*e[1])%29-14,17) for e in edges}
    t = time.perf_counter()
    Y = action(n,q,colors,diagonal,values)
    acquisition = time.perf_counter()-t
    t = time.perf_counter()
    exact_d, exact_e = decode(plan,Y)
    noiseless_decode = time.perf_counter()-t
    assert exact_d == diagonal and exact_e == values
    E = [[F((11*i+7*j)%19-9,101) for j in range(q)] for i in range(n)]
    Z = [[Y[i][j]+E[i][j] for j in range(q)] for i in range(n)]
    t = time.perf_counter()
    out_d,out_e = decode(plan,Z)
    noisy_decode = time.perf_counter()-t
    err_d = [out_d[i]-diagonal[i] for i in range(n)]
    err_e = {e:out_e[e]-values[e] for e in values}
    error2, noise2 = matrix_frobenius_sq(err_d,err_e), norm_sq(E)
    assert error2 <= bound_sq*noise2
    if name.startswith('period9'):
        assert all(len(c['order'])<=5 and c['max_degree']<=2 for c in plan['components'])
    if name.startswith('prism_good'):
        assert all(sum(1 for v in c['order'] if sum(v in e for e in edges if set((colors[e[0]], colors[e[1]])) == set(c['pair'])) > 1) <= 1
                   for c in plan['components'])
    return dict(name=name,n=n,q=q,edges=edges,colors=colors,
                diagonal=diagonal,edge_values=edge_list(values),noise=E,
                decoded_diagonal=out_d,decoded_edges=edge_list(out_e),
                noise_norm_sq=noise2,error_frobenius_sq=error2,verified_constant_sq=bound_sq,
                maximum_component_size=max((len(c['order']) for c in plan['components']),default=1),
                timings=dict(preparation_seconds=prep,synthetic_sparse_action_seconds=acquisition,
                             noiseless_decoder_seconds=noiseless_decode,noisy_decoder_seconds=noisy_decode,
                             body_wall_seconds=time.perf_counter()-start,body_cpu_seconds=time.process_time()-cpu))


def main():
    wall,cpu=time.perf_counter(),time.process_time()
    cases=[]
    es,cs=squared_path(61)
    cases.append(test_operation('period9_full',61,es,cs,4,F(16,3)))
    es,cs=squared_path(61,{(u,u+2) for u in range(0,59,5)})
    cases.append(test_operation('period9_subsupport',61,es,cs,4,F(16,3)))
    es,_=squared_path(61)
    cases.append(test_operation('period5_comparator',61,es,[i%5 for i in range(61)],5,F(1)))
    # One branching fixture, not a sweep: T is the complete binary tree of height6.
    parents=[None]+[(v-1)//2 for v in range(1,127)]
    es,cs=forest_prism(parents)
    cases.append(test_operation('prism_good',254,es,cs,4,F(2)))
    bad_es,bad_cs=forest_prism(parents,bad=True)
    bad_plan=prepare(254,bad_es,bad_cs,4)
    witness=cut_witness(bad_plan)
    good_Y=action(254,4,cs,witness['diagonal'],witness['edge_values'])
    assert norm_sq(good_Y)>=F(1,2)
    witness_record=dict(n=254,q=4,parents=parents,edges=es,good_colors=cs,bad_colors=bad_cs,
        diagonal=witness['diagonal'],edge_values=edge_list(witness['edge_values']),
        bad_action=witness['action'],good_action=good_Y,cut_edge=witness['edge'],
        a=witness['a'],b=witness['b'],bad_action_norm_sq=witness['action_norm_sq'],
        good_action_norm_sq=norm_sq(good_Y),operator_norm_lower=1,
        inverse_lower_sq=witness['inverse_lower_sq'],
        scope='Explicit bad proper four-coordinate seed on a graph that ALSO has a good four-query design. Not an all-design graph lower bound.')
    # Small exact noninjective seed; show the obstruction directly, not solver status.
    ce=[(0,1),(1,2),(2,3),(0,3)]
    cw={(0,1):F(1),(1,2):F(-1),(2,3):F(1),(0,3):F(-1)}
    cc=[0,1,0,1]
    assert norm_sq(action(4,4,cc,[F(0)]*4,cw))==0
    try:
        prepare(4,ce,cc,4)
        raise AssertionError('cycle must be rejected')
    except ValueError as exc:
        assert 'cycle' in str(exc)
    result=dict(cases=cases,same_graph_witness=witness_record,
        cycle_kernel=dict(n=4,q=4,edges=ce,colors=cc,diagonal=[F(0)]*4,edge_values=edge_list(cw)),
        counts=dict(fixed_operation_cases=4,branching_fixture_count=1,precision_or_optimization_tuning=0),
        costs=dict(body_wall_seconds=time.perf_counter()-wall,body_cpu_seconds=time.process_time()-cpu,
                   peak_process_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                   exclusion='Imports/startup, theorem development, source reading, authoring, independent verification and delivery additional. Sparse synthetic action timing is NOT application-oracle cost.'))
    out=ROOT/'results'/'coordinate_operations.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(encode(result),indent=2)+'\n')
    print(json.dumps(dict(output=str(out),costs=result['costs'],
        cases=[dict(name=c['name'],n=c['n'],q=c['q'],max_component=c['maximum_component_size'],
                    error_ratio_sq=str(c['error_frobenius_sq']/c['noise_norm_sq'])) for c in cases],
        witness=dict(a=witness['a'],b=witness['b'],bad_action_sq=str(witness['action_norm_sq']),
                     good_action_sq=str(norm_sq(good_Y)),inverse_lower_sq=str(witness['inverse_lower_sq']))),indent=2))


if __name__=='__main__': main()
