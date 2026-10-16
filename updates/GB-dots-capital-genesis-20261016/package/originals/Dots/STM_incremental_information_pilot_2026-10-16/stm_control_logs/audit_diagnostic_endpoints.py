"""Outcome audit of three designated diagnostics; not a policy evaluation.
Reads safe JSON produced by inspect_static.py, never opens untouched episodes.
"""
import json,math,pathlib
p=pathlib.Path(__file__).parent
data=json.loads((p/'sample_decoded_summary.json').read_text())
assert set(data)=={'00000.npy','01500.npy','02920.npy'}
threshold=0.288/math.sqrt(3)
out=[]
for name,ep in sorted(data.items()):
 t=ep['transitions'];n=len(t['action']);assert n>0
 assert all(len(t[k])==n for k in ['state','next_state','reward','done','info'])
 assert t['done']==[False]*(n-1)+[True]
 start=ep['episode_start_info']['info'];end=ep['episode_end_info']
 error=math.dist(start['goal_absolute_nm'],end['atom_absolute_nm'])
 assert abs(error-t['info'][-1]['dist_destination'])<1e-10
 assert end['img_forward']['shape']==[128,128] and end['img_backward']['shape']==[128,128]
 assert t['info'][-1]['atom_absolute_nm']==end['atom_absolute_nm']
 assert all(i['current_series']['length']==i['d']['length'] for i in t['info'])
 out.append({'episode':name,'partition':'diagnostic_exclude_from_test','logged_actions':n,'terminal_error_nm':error,'terminal_success':error<threshold,'terminal_image_pair_present':True,'terminal_reason':'not separately logged','time_cost':'unavailable','policy_value':'not identifiable from this audit'})
result={'scope':'three diagnostics only; no aggregate generalization statistic','success_threshold_nm':threshold,'records':out}
(p/'diagnostic_endpoint_audit.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
