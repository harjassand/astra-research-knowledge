"""Collect distinct observed computation receipts without double counting stages.

The subtotal is recorded script/process wall time, not elapsed programme time
or a price/energy estimate. Unmetered activities are explicitly not zero.
"""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]

def main():
    rows = []
    def add(name, file, wall, cpu=None, rss=None, note=''):
        data = json.loads((ROOT/'results'/file).read_text())
        rows.append({'activity':name,'receipt':'results/'+file,
                     'wall_seconds':data[wall],
                     'cpu_seconds':data.get(cpu) if cpu else None,
                     'peak_rss_bytes':data.get(rss) if rss else None,
                     'timer_field':wall,'note':note})
    rows.append({'activity':'Failed initial SVD exploration loader unpack',
                 'receipt':'results/attempt_record.json','wall_seconds':0.608256022,
                 'cpu_seconds':None,'peak_rss_bytes':None,
                 'note':'Enclosing command timer; expected3 loader outputs, actual2; fixed once.'})
    add('Successful SVD exploration and frozen dyadic preconditioner', 'common_action_exploration.json',
        'wall_seconds','cpu_seconds','peak_rss_bytes','Body timer; SVD0.125259032s is included.')
    add('Common-action certificate producer', 'common_action_producer.json',
        'wall_seconds','cpu_seconds','peak_rss_bytes','Input reconstruction, all exact products, proposal, verification included; prior exploration separate.')
    add('Independent common-action replay', 'common_action_audit.json',
        'enclosing_subprocess_wall_seconds','body_cpu_seconds','peak_rss_bytes',
        'Uses enclosing process39.758677765s rather than adding body39.306566515s again; CPU field is body only.')
    for name, file in [('Exact completion fixtures','completion_exact_checks.json'),
                       ('Exact integer kernel fixtures','exact_matmul_checks.json'),
                       ('Original8-core construction','eight_probe_core_preliminary.json'),
                       ('Original graph peeling construction','sparse_degeneracy_preliminary.json'),
                       ('Actual sparse-noise witness producer','sparse_condition_producer.json'),
                       ('Actual sparse-noise witness replay','sparse_condition_replay.json'),
                       ('Independent Fraction noise-witness audit','sparse_noise_audit.json'),
                       ('Forest constructive decoder fixtures','forest_recovery_checks.json')]:
        add(name,file,'wall_seconds','cpu_seconds','peak_rss_bytes')
    for name,file in [('Initial339-column rowwise producer','sparse_identifiability.json'),
                      ('Initial339-column selected-minor replay','sparse_identifiability_replay.json')]:
        add(name,file,'wall_seconds_including_python_imports','cpu_seconds_including_python_imports','process_peak_rss_bytes')
    for name,file in [('Nine-column symmetric producer including failed9-clique route','symmetric_sparse_identifiability.json'),
                      ('Nine-column selected-minor replay','symmetric_sparse_identifiability_replay.json'),
                      ('Independent graph-order and clique check','sparse_degeneracy_verification.json'),
                      ('Independent8-core and dimension-obstruction challenge','eight_probe_obstruction_challenge.json'),
                      ('Path flow and isometry exact fixtures','path_stability_challenge.json'),
                      ('Exact row-cap counterexample challenge','row_cap_counterexample_challenge.json')]:
        add(name,file,'wall_seconds_including_imports','cpu_seconds_including_imports','process_peak_rss_bytes')
    out = {'schema':'observed-cost-ledger-v1','distinct_numeric_activities':rows,
           'sum_of_listed_wall_seconds':sum(r['wall_seconds'] for r in rows),
           'sum_of_available_cpu_seconds':sum(r['cpu_seconds'] or 0 for r in rows),
           'activities_with_unknown_cpu':[r['activity'] for r in rows if r['cpu_seconds'] is None],
           'maximum_observed_process_peak_rss_bytes':max(r['peak_rss_bytes'] or 0 for r in rows),
           'subtotal_meaning':'Sum of disjoint activity timers, some body and some enclosing process. Not concurrent elapsed time, complete programme cost, monetary price or energy.',
           'not_in_subtotal':['original owner experiment and original independent replay',
                             'incoming moment construction and its receiving use (not rerun)',
                             'primary literature retrieval, reading, proof development and authoring',
                             'model inference, service/network overhead, price and energy',
                             'package construction, portable package check and private transport; separate receipts'],
           'literature_contributor_reported_source_latency_seconds':18.5+19.0+16.5+5.2,
           'literature_latency_note':'Four bounded notes; source access latency only, not proof/research totals. Root source reads additionally occurred.'}
    (ROOT/'results/cost_ledger.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='distinct_numeric_activities'},indent=2))

if __name__=='__main__':main()
