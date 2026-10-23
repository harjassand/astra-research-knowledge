#!/usr/bin/env python3
"""One fixed Cycle6 receiving calculation and its decisive failed-design witness.

All scientific input, action, decoder output and certificates are saved. Times
are observed computation bodies, not discovery or complete research costs.
"""
import json
import os
from pathlib import Path
import resource
import sys
from fractions import Fraction as F
from time import perf_counter, process_time

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
import recursive_network as net
import cut_balance as cert
import coordinate_decoder as dec


def dump(path, obj):
    path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')


def run_receiving(name, spec, uniform_K):
    times = {}
    begin = perf_counter()
    profiles = net.evaluate_profiles(spec)
    graph = net.build(spec)
    profile = net.graph_profile(graph['n'],graph['edges'],graph['colors'],graph['terminals'])
    predicted = profiles[spec['root']]
    assert profile['K'] == predicted['K'] and profile['boundary'] == predicted['boundary']
    assert graph['n'] == predicted['n'] and len(graph['edges']) == predicted['m']
    assert graph['applications'] == predicted['applications']
    assert profile['K'] <= uniform_K
    times['graph_coloring_profile_seconds'] = perf_counter()-begin
    n, edges, colors = graph['n'],graph['edges'],graph['colors']
    begin = perf_counter()
    plan = cert.prepare(n,edges,colors,q=3)
    times['prepare_seconds'] = perf_counter()-begin
    assert plan['certified_operator_constant_sq'] <= 2*uniform_K-1
    begin = perf_counter()
    diagonal_ints = [((37*i+11)%101)-50 for i in range(n)]
    edge_ints = [((13*u+29*v+7)%97)-48 for u,v in edges]
    noise_ints = [[((17*i+23*j+5)%31)-15 for j in range(3)] for i in range(n)]
    diagonal = [F(v,17) for v in diagonal_ints]
    values = {e:F(v,19) for e,v in zip(edges,edge_ints)}
    noise = [[F(v,997) for v in row] for row in noise_ints]
    times['input_construction_seconds'] = perf_counter()-begin
    begin = perf_counter()
    noiseless = dec.action(n,3,colors,diagonal,values)
    Y = [[x+e for x,e in zip(a,b)] for a,b in zip(noiseless,noise)]
    times['full_three_actions_and_noise_seconds'] = perf_counter()-begin
    begin = perf_counter()
    exact_diag, exact_values = dec.decode(plan,noiseless)
    assert exact_diag == diagonal and exact_values == values
    times['noiseless_decode_seconds'] = perf_counter()-begin
    begin = perf_counter()
    recovered_diag, recovered_values = dec.decode(plan,Y)
    times['noisy_decode_seconds'] = perf_counter()-begin
    begin = perf_counter()
    predicted_Y = dec.action(n,3,colors,recovered_diag,recovered_values)
    projected = [[F(0) for _ in range(3)] for _ in range(n)]
    for i in range(n):
        projected[i][colors[i]] = Y[i][colors[i]]
    for comp in plan['components']:
        a,b = comp['pair']
        order = comp['order']
        signed_total = sum((1 if colors[v] == a else -1)*Y[v][b if colors[v] == a else a]
                           for v in order)
        for v in order:
            sig = 1 if colors[v] == a else -1
            col = b if colors[v] == a else a
            projected[v][col] = Y[v][col]-sig*signed_total/len(order)
    assert predicted_Y == projected
    error_diag = [a-b for a,b in zip(recovered_diag,diagonal)]
    error_edges = {e:recovered_values[e]-values[e] for e in edges}
    row_sums = list(map(abs,error_diag))
    for (u,v),w in error_edges.items():
        row_sums[u] += abs(w); row_sums[v] += abs(w)
    error_infinity = max(row_sums)
    noise2 = dec.norm_sq(noise)
    assert error_infinity**2 <= plan['certified_operator_constant_sq']*noise2
    times['exact_residual_and_error_check_seconds'] = perf_counter()-begin
    degree = [0]*n
    for u,v in edges:
        degree[u] += 1; degree[v] += 1
    high_edge = next(([u,v] for u,v in edges if degree[u] == degree[v] == 4),None)
    result = {
        'name':name, 'spec':spec, 'graph':graph, 'all_symbolic_profiles':profiles,
        'actual_profile':profile, 'uniform_component_cap':uniform_K,
        'uniform_operator_constant_sq':2*uniform_K-1,
        'certificate':cert.summary(plan), 'adjacent_degree_four_vertices':high_edge,
        'matrix_input':{'diagonal_numerators':diagonal_ints,'diagonal_denominator':17,
                        'edge_numerators_in_graph_order':edge_ints,'edge_denominator':19},
        'noise_input':{'numerators':noise_ints,'denominator':997},
        'observed_full_actions':[[str(v) for v in row] for row in Y],
        'recovered':{'diagonal':[str(v) for v in recovered_diag],
                     'edge_values_in_graph_order':[str(recovered_values[e]) for e in edges]},
        'verification':{'noiseless_exact':True,'projected_action_residual_sq':'0',
                        'noise_frobenius_sq':str(noise2),
                        'actual_error_infinity_upper':str(error_infinity),
                        'actual_error_frobenius_sq':str(dec.matrix_frobenius_sq(error_diag,error_edges)),
                        'certified_operator_error_sq':str(plan['certified_operator_constant_sq']*noise2),
                        'operator_norm_not_numerically_diagonalized':True},
        'times_seconds':times}
    return result


def failed_receiving(depth):
    times = {}
    begin = perf_counter()
    spec = net.failed_spec(depth)
    profile = net.evaluate_profiles(spec,allow_even_failure=True)[spec['root']]
    graph = net.build(spec,allow_even_failure=True)
    audit = net.graph_profile(graph['n'],graph['edges'],graph['colors'],(0,1))
    assert profile['boundary'] == audit['boundary'] and profile['K'] == audit['K']
    assert audit['boundary'][0] == 2**depth
    assert graph['n'] == 7*2**depth-4 and len(graph['edges']) == 8*2**depth-6
    assert graph['maximum_degree'] == 3
    times['construction_profile_seconds'] = perf_counter()-begin
    begin = perf_counter()
    plan = cert.prepare(graph['n'],graph['edges'],graph['colors'],q=3)
    times['prepare_seconds'] = perf_counter()-begin
    begin = perf_counter()
    idx = next(i for i,c in enumerate(plan['components']) if c['pair'] == (0,1) and 0 in c['order'])
    witness = dec.cut_witness(plan,component_index=idx)
    assert witness['inverse_lower_sq'] == F(2**(2*depth-2)-1,2**depth)
    times['exact_cut_witness_seconds'] = perf_counter()-begin
    return {'name':'failed_even_series_rotation','depth':depth,'spec':spec,'graph':graph,
            'actual_profile':audit,'exact_symbolic_profile':profile,
            'q':3,'scope':'specified design only; no universal graph lower',
            'witness':{'edge':list(witness['edge']), 'cut_sides':[witness['a'],witness['b']],
                       'unit_edge_value':str(witness['edge_values'][witness['edge']]),
                       'nonzero_matrix_edges':[[u,v,str(w)] for (u,v),w in witness['edge_values'].items() if w],
                       'nonzero_action_cells':[[i,j,str(w)] for i,row in enumerate(witness['action']) for j,w in enumerate(row) if w],
                       'action_frobenius_sq':str(witness['action_norm_sq']),
                       'operator_inverse_lower_sq':str(witness['inverse_lower_sq'])},
            'times_seconds':times}


def main():
    wall0,cpu0 = perf_counter(),process_time()
    out = ROOT/'results'
    out.mkdir(exist_ok=True)
    results = [run_receiving('base_paths_odd_series_and_forks',net.standard_spec(),13),
               run_receiving('arbitrary_paths_odd_series_and_forks',net.path_extension_spec(),31),
               failed_receiving(8)]
    for row in results:
        dump(out/(row['name']+'.json'),row)
    summary = []
    for row in results:
        record = {'name':row['name'],'n':row['graph']['n'],'m':len(row['graph']['edges']),
                  'degree':row['graph']['maximum_degree'],'profile':row['actual_profile'],
                  'times_seconds':row['times_seconds']}
        if 'certificate' in row:
            record['certificate'] = row['certificate']
            record['verification'] = row['verification']
            record['adjacent_degree_four_vertices'] = row['adjacent_degree_four_vertices']
        else:
            record['inverse_lower_sq'] = row['witness']['operator_inverse_lower_sq']
        summary.append(record)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    result = {'results':summary, 'wall_seconds_including_input_and_output_serialization':perf_counter()-wall0,
              'cpu_seconds':process_time()-cpu0,
              'maximum_rss_bytes':usage.ru_maxrss*(1 if sys.platform == 'darwin' else 1024),
              'python':sys.version, 'pid':os.getpid(),
              'discovery_reading_reasoning_authoring_review_service_costs':'not included; unknown total'}
    dump(out/'RESOURCE_RESULTS.json',result)
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
