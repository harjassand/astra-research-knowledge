#!/usr/bin/env python3
"""Summarize fresh-vs-archived source replay differences without modifying source."""
import json
from pathlib import Path
ROOT=Path(__file__).parent
src=ROOT/'source_snapshot'/'escape'
out=ROOT/'replay'
rows=[]
for name in sorted(p.name for p in src.glob('acquired_*.json')):
    rp=out/name
    if not rp.exists(): continue
    a=json.load(open(src/name)); b=json.load(open(rp))
    rows.append({
      'case':name,
      'same_input_n_t':(a.get('n'),a.get('t'))==(b.get('n'),b.get('t')),
      'energy_queries_source':a.get('energy_queries'),
      'energy_queries_replay':b.get('energy_queries'),
      'ratio_source':a.get('ratio'), 'ratio_replay':b.get('ratio'),
      'ratio_abs_delta':abs(a.get('ratio',0)-b.get('ratio',0)),
      'tau_lo_source':a.get('tau_lo'),'tau_lo_replay':b.get('tau_lo'),
      'tau_hi_source':a.get('tau_hi'),'tau_hi_replay':b.get('tau_hi'),
      'tau_lo_rel_delta':abs(a.get('tau_lo',0)-b.get('tau_lo',0))/max(abs(a.get('tau_lo',0)),1e-300),
      'tau_hi_rel_delta':abs(a.get('tau_hi',0)-b.get('tau_hi',0))/max(abs(a.get('tau_hi',0)),1e-300),
      'exact_endpoint_strings_identical':a.get('lower_exact')==b.get('lower_exact') and a.get('upper_exact')==b.get('upper_exact'),
      'state_counts_match':all(a.get(k)==b.get(k) for k in ('low_states','residual_neighborhood','full_states')),
      'source_run_seconds':a.get('run_s'),'replay_run_seconds':b.get('end_to_end_seconds')
    })
preps=[]
for name in ['prepared_n24_t1000.json']:
    a=json.load(open(src/name)); b=json.load(open(out/name))
    preps.append({'case':name,
      'point_ratio_source':a.get('point_ratio'),'point_ratio_replay':b.get('point_ratio'),
      'equilibrium_lo_source':a.get('equilibrium_lo'),'equilibrium_lo_replay':b.get('equilibrium_lo'),
      'equilibrium_hi_source':a.get('equilibrium_hi'),'equilibrium_hi_replay':b.get('equilibrium_hi'),
      'equilibrium_lo_rel_delta':abs(a.get('equilibrium_lo',0)-b.get('equilibrium_lo',0))/max(abs(a.get('equilibrium_lo',0)),1e-300),
      'equilibrium_hi_rel_delta':abs(a.get('equilibrium_hi',0)-b.get('equilibrium_hi',0))/max(abs(a.get('equilibrium_hi',0)),1e-300),
      'point_exact_endpoints_identical':a.get('point_lo_exact')==b.get('point_lo_exact') and a.get('point_hi_exact')==b.get('point_hi_exact'),
      'source_total_s':a.get('total_s'),'replay_total_s':b.get('total_s')})
result={'fresh_replay_cases':rows,'preparation_cases':preps,
 'interpretation':'Fresh exact certificates remain valid; endpoint rational strings can differ because floating sparse solves propose different dyadic witnesses. Compare interval containment/width and states rather than exact endpoint byte equality unless proposal/runtime versions are pinned.'}
(ROOT/'replay'/'source_difference_summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
