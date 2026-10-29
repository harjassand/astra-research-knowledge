"""Independent phase checks and cumulative direct error for genus-one adapter."""
import genus_one_relative_doubling as g
import mpmath as mp
import json,hashlib
from pathlib import Path
r=g.r
initial=mp.mpf('1.3');theta=initial;A0=g.independent_phase(mp.pi/2);Ai=g.independent_phase(initial)
period=g.independent_phase(2*mp.pi);bound=mp.mpf(0);records=[]
for step in range(1,13):
 rec=r.run_case('chain_'+str(step),[mp.pi/2],[theta],160,24,True)
 assert rec['matching_below_quarter_input_separation'] and rec['output_one_point_per_gap']
 theta=mp.mpf(rec['projected_output_angles'][0]);target=2**step*Ai-(2**step-1)*A0
 delta=g.independent_phase(theta)-target;error=abs(delta-mp.nint(delta/period)*period)
 percall=mp.mpf(rec['abel_perturbation_norm'])+mp.mpf(rec['abel_perturbed_section_residual']['residual_norm'])
 bound=2*bound+percall
 record=dict(step=step,independent_abel_error=r.outnum(error),two_e_plus_delta_budget=r.outnum(bound),below_budget=bool(error<bound+mp.mpf('1e-29')),result=rec)
 records.append(record)
 Path(__file__).with_suffix('.json').write_text(json.dumps(dict(warning='Noncertified numerical direct-error composition check',source_sha256=hashlib.sha256(Path(g.__file__).read_bytes()).hexdigest(),records=records),indent=2))
 print(json.dumps({k:v for k,v in record.items() if k!='result'}),flush=True)
