"""Replay stored certified actions, exposing prequential actual-probe scores; no new optimization."""
import json
from pathlib import Path
root=Path(__file__).parent
old=json.loads((root/'bounded_live_three_role_result.json').read_text())
certificates=[x['certificate'] for row in old['oracle_calls'] for x in row]+old['retrospective_candidates']
iterator=iter(certificates)
source=(root/'run_bounded_three_role.py').read_text()
source=source.replace('from bounded_sos_oracle import solve as bounded_solve,verify as bounded_verify','from bounded_sos_oracle import verify as bounded_verify\ndef bounded_solve(query): return next(iterator)')
source=source.replace("if role=='learn':\n  c=", "if role=='learn':\n  c=")
source=source.replace('K=A[out];bath=', "record['probe_raw']=dict(input_axes=c.tolist(),input_signs=sign.tolist(),output_axes=a.tolist(),output_signs=yy.tolist(),outcome=out)\n  record['selected_probe_estimates']=[]\n  K=A[out];bath=")
source=source.replace('increment={e:2*h.get(e,0)/p for e in qo.exps};', "qexact=[F(x) for x in roundcert[edge]['certificate']['quaternion']]\n   estimate=F(3,4)+sum(v*__import__('functools').reduce(lambda a,b:a*b,[qexact[j]**e[j] for j in range(4)],F(1)) for e,v in h.items())\n   record['selected_probe_estimates'].append(str(estimate))\n   increment={e:2*h.get(e,0)/p for e in qo.exps};")
source=source.replace("bounded_live_three_role_result.json", "bounded_live_probe_replay.json")
exec(compile(source,str(root/'run_bounded_three_role.py'),'exec'),dict(__file__=str(root/'run_bounded_three_role.py'),iterator=iterator))
new=json.loads((root/'bounded_live_probe_replay.json').read_text())
for key in ['final_feedback','observed_squared_feedback_per_edge','roles','validation_failures','service_bad_sum','mean_service_bad','mean_selected_star_loss','retrospective_empirical_score','reported_gap_counters']:
 assert old[key]==new[key],key
print('Exact candidate-reuse replay matches all original physical summary and sufficient counters.')
