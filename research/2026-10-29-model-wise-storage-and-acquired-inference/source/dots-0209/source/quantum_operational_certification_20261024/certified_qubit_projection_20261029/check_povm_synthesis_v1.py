from finite_povm_synthesis_v1 import *
from pathlib import Path
import json,time
P=Path(__file__).parent;src=json.loads((P/'check_pruned_receiver_v1.json').read_text());out=[];start=time.time()
for run in src['runs']:
 E=[[F(x) for x in e] for e in run['sampled_output_effects']]
 c=synthesis(E);c['seed']=run['seed'];c['labels']=run['sampled_output_labels'];out.append(c)
 print(run['seed'],len(c['gates']),c['correction_channel_half_diamond_upper_float'],flush=True)
(P/'check_povm_synthesis_v1.json').write_text(json.dumps({'status':'EXACT_RATIONAL_UNITARY_MODEL_CERTIFICATES','elapsed_seconds':time.time()-start,'runs':out},indent=2)+'\n')
