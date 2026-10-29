"""Replay both pilots against their frozen input lists without altering originals."""
from pathlib import Path
import json,hashlib,tempfile,shutil,importlib.util
import oracle_and_endpoint_fit_v1 as a
H=Path(__file__).parent;Q=H.parent
expected1=json.loads((H/'oracle_and_endpoint_fit_v1.json').read_text());expected2=json.loads((H/'direct_endpoint_no_per_round_inverse_v2.json').read_text())
frozen=[]
for row in expected1['oracle_rows']:
 p=Q/row['source_file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['source_sha256'];j=json.loads(p.read_text());bs=j.get('same_elapsed_unencoded',j.get('matched_unencoded'));frozen.append((row['source_label'],p,bs,row['comparison_scope']))
def compare(x,y,path='root'):
 if isinstance(x,dict):
  assert x.keys()==y.keys(),path
  for k in x:compare(x[k],y[k],path+'.'+str(k))
 elif isinstance(x,list):
  assert len(x)==len(y),path
  for i,(u,v) in enumerate(zip(x,y)):compare(u,v,path+'.'+str(i))
 elif isinstance(x,float):assert abs(x-y)<2e-12,path
 else:assert x==y,(path,x,y)
with tempfile.TemporaryDirectory(prefix='endpoint_frozen_replay_') as td:
 t=Path(td);shutil.copy2(H/'endpoint_sampled_counts_v1.npz',t/'endpoint_sampled_counts_v1.npz');a.HERE=t;a.source_sets=lambda:frozen;a.main();compare(expected1,json.loads((t/'oracle_and_endpoint_fit_v1.json').read_text()))
 spec=importlib.util.spec_from_file_location('v2',H/'direct_endpoint_no_per_round_inverse_v2.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b);b.HERE=t;b.Q=Q
 assert hashlib.sha256((Q/'five_qubit_acquired_frame_pilot_20261028/code_and_channels.py').read_bytes()).hexdigest()==expected2['source_generator_sha256']
 shutil.copy2(H/'direct_endpoint_counts_v2.npz',t/'direct_endpoint_counts_v2.npz');b.main();compare(expected2,json.loads((t/'direct_endpoint_no_per_round_inverse_v2.json').read_text()))
print('PASS: frozen-source replay, exact raw counts and numerical agreement; no original files altered')
