import json,time,math,resource
from pathlib import Path
import numpy as np
from scipy.special import logsumexp,expit
from scipy.stats import t
B=Path(__file__).resolve().parent
start=time.perf_counter();r=json.loads((B/'d21_optimized_result.json').read_text());z=np.load(B/'d21_optimized_partial.npz');tr=z['traces'];ts=z['ladder'];p=json.loads(Path(r['spec']['parameters']).read_text());q=np.array(p['q_numerators'],float)/2.**64
A=lambda v:float(np.log1p(q*np.expm1(v)).sum())
fwd=[];back=[]
for j in range(len(ts)-1):
 diff=ts[j+1]-ts[j];c=A(ts[j+1])-A(ts[j]);u=diff*tr[j].astype(float)-c;v=diff*tr[j+1].astype(float)-c
 fwd.append(float(logsumexp(u)-math.log(u.size)));back.append(float(-logsumexp(-v)+math.log(v.size)))
anchor=r['anchor']['estimate'];se=r.get('log_standard_error');point=r.get('point');familydelta=float(t.ppf(1-.001/6,r['spec']['chains']-1))*se
s=dict(complete=r['complete'],point=point,nominal_999_interval=r['nominal_999_interval'],nominal_bonferroni_per_design_interval=[point*math.exp(-familydelta),point*math.exp(familydelta)],interval_status='All intervals are Student-t/delta diagnostics excluding mixing and numerical bias, not certified coverage. Bonferroni alone cannot repair this.',rungs=len(ts),maximum_Rhat=max(x['Rhat'] for x in r['rungs']),maximum_IAT=max(x['max_IAT'] for x in r['rungs']),conservative_IAT_fail_rungs=sum(not x['maxIAT50_pass'] for x in r['rungs']),minimum_acceptance=min(x['acceptance'] for x in r['rungs']),maximum_acceptance=max(x['acceptance'] for x in r['rungs']),forward_only_point=anchor*math.exp(sum(fwd)),backward_only_point=anchor*math.exp(sum(back)),total_proposals=r['total_proposals'],decoder_calls=r['total_decoder_calls'],recorded_seconds_through_last_rung=r['total_seconds'],setup_seconds=r['setup_seconds'],anchor_and_starts_seconds=r['anchor']['seconds'],sum_rung_seconds=sum(x['seconds'] for x in r['rungs']),recorded_peak_before_final_analysis_kib=r['peak_rss_kib'],timing_caveat='Main timer starts before model load, excludes interpreter/import and the final BAR histogram analysis. Peak is captured before final analysis, so it is not whole-process peak. Concurrent host work means no isolated speedup claim.',forward_backward_note='Sensitivity cross-check only, not an independent-sample or mixed-chain certificate.',postprocess_seconds=time.perf_counter()-start,postprocess_peak_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(B/'SUMMARY.json').write_text(json.dumps(s,indent=2));print(json.dumps(s,indent=2))
