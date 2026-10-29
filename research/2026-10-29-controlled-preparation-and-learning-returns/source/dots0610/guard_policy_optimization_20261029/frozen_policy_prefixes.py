import numpy as np,json,hashlib
from pathlib import Path
from fractions import Fraction
from embedded_chain import evaluate_fast,finite_bounds
p=Path(__file__).parent;src=Path('producer-workspace/prefix_maps.npz');a=np.load(src);w=json.load(open(p/'policy_grid_v2.json'))['winners_guard_throughput'];rows=[]
for M in [100,1000,10000,100000,1000000]:
 for name,prefix in [('six_state','six'),('matching','matching')]:
  pol=w[name];sf=Fraction(pol['s']);ev=evaluate_fast(a[f'{prefix}_pass_{M}'],a[f'{prefix}_fail_{M}'],a[f'good_{M}']+a[f'bad_{M}'],a[f'sigma_{M}'],float(sf),pol['J'],pol['b']);fb=finite_bounds(ev['uncapped_acceptance'],ev['uncapped_expected_calls'],sf,pol['J'],pol['payload_qubits']);rows.append({'learning_calls':M,'test':name,'frozen_policy':{k:pol[k] for k in ['R','s','b','t','B','J','payload_qubits']},**ev,**fb,'single_learning_plus_guard_accepted_payload_per_call_lower':pol['payload_qubits']*max(0,ev['uncapped_acceptance']-fb['finite_cap_loss_upper_bound'])/(M+ev['uncapped_expected_calls'])})
out={'prefix_map_source':str(src),'prefix_map_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'scope':'Policies frozen from1m benchmark, applied unchanged to earlier nested prefixes. No per-prefix optimization. Each source stage switches to U0 carrying its actual prefix bath; conditional on one acquired history. Floating zeros may be underflow, not impossible acceptance. Controls/storage/outer compiler excluded from sourcecallmetric.','rows':rows};(p/'frozen_policy_prefixes.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(rows,indent=2))
