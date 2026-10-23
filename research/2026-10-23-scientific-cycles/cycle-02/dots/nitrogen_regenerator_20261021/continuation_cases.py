import json,time
from pathlib import Path
import reactive_average as r
base=Path(__file__).resolve().parent;initial=base/'reactive_continuation.npz';out=[]
for k,T in [(24.,3100.),(48.,3100.),(24.,2900.)]:
 d=base/f'case_k{int(k)}_T{int(T)}';d.mkdir(exist_ok=True);r.KS=k;r.HOT_T=T;r.ROOT=d;r.RESUME_FILE=initial
 r.main()
 p=d/'reactive_average_result.json'
 if p.exists():
  a=json.loads(p.read_text());out.append({z:a[z] for z in ['geometry','net_heater_heat_MJ_mol_NOx_exchanger_out','retained_mol_NOx_kg','hot_survival','maximum_solid_K','cold_out_K','hot_out_K','heat_balance_J_kg','wall_s']});print(json.dumps(out[-1]),flush=True)
 else:out.append({'k':k,'T':T,'status':'FAILED_NUMERICAL_CONTINUATION'})
(base/'continuation_summary.json').write_text(json.dumps(out,indent=2)+'\n')
