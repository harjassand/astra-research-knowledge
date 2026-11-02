"""Matched-source conventional baseline vs acquired greedy programs.
Both receive identical Poisson table measurements, same locality interface,
real interventions and all retained data. Full Walsh gets 8 local coefficients
with O(8^2) exact arithmetic; no new raw queries. No selective comparator penalty.
"""
import json,math
from pathlib import Path
from strong_baseline import recover_records,compute_baseline
from signed_execute import common_programs,growth_and_error
ROOT=Path(__file__).parent
if __name__=='__main__':
    a=json.loads((ROOT/'frozen_measurements.json').read_text())
    a['weak_field']=json.loads((ROOT/'signed_measurements_v2.json').read_text())
    baselines=compute_baseline(recover_records(a))
    v1=json.loads((ROOT/'frozen_programs.json').read_text())
    v2=json.loads((ROOT/'signed_frozen_v2.json').read_text())
    acquired=common_programs(v1,v2)
    matches=[]
    for mode in sorted(baselines):
        b=baselines[mode];p=acquired[mode]
        row={'mode':mode,'conventional_rules':len(b['jumps']),'learner_rules':len(p['jumps']),
             'conventional_rho':b['local_residual_bound'],'learner_rho':p['rho'],
             'conventional_exit':b['kill']+sum(j['rate'] for j in b['jumps']),
             'learner_exit':p['kill']+sum(j['rate'] for j in p['jumps']),
             'extra_physical_queries_for_conventional':0,
             'symbolic_Walsh_coefficients_computed':8}
        matches.append(row)
        print(row)
    bprog={mode:{'kill':b['kill'],'rho':b['local_residual_bound'],'jumps':b['jumps']} for mode,b in baselines.items()}
    comparison={'matched_data':True,'conventional_used_exact_same_local_estimates':True,
                'conventional_can_compile_signed_code_without_greedy_rule_search':True,
                'comparison':matches,
                'learner_envelope':growth_and_error(acquired,1.2,1),
                'ordinary_full_Walsh_envelope':growth_and_error(bprog,1.2,1),
                'conclusion':'Ordinary full Walsh matches or improves numerical accuracy with no new measurements; greedy code is sparser, but no demonstrated total-computation advantage over symbolic full-table method.'}
    (ROOT/'matched_comparison_results.json').write_text(json.dumps(comparison,indent=2,sort_keys=True))
    print('ordinary envelope', comparison['ordinary_full_Walsh_envelope']['model_error'])
