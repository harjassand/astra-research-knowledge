"""Static object-identity audit; author functions never run.
Uses only three burned diagnostic .npy files and original inert parser.
"""
import pathlib,json,hashlib
from inspect_static import parse,Node
p=pathlib.Path(__file__).parent
out=[]
def image_hash(node):
 assert isinstance(node,Node)
 return hashlib.sha256(node.state[4]).hexdigest()
for name in ['00000.npy','01500.npy','02920.npy']:
 root=parse(p/'acquired/training_data_and_model_parameters/training_data'/name)
 d=root.state[4][0];prev=d['episode_start_info'];rows=[]
 for idx,info in enumerate(d['transitions']['info']):
  img=info['img_info'];reuse=[img[k] is prev[k] for k in ['img_forward','img_backward']]
  equal=[image_hash(img[k])==image_hash(prev[k]) for k in ['img_forward','img_backward']]
  rows.append({'transition_index':idx,'same_serialized_image_object_as_prior':reuse,'same_image_bytes_as_prior':equal,'source_supported_new_scan':not any(reuse),'current_trace_present':info['current_series'] is not None})
  prev=img
 out.append({'episode':name,'diagnostic_only':True,'scan_flag_explicit':False,'transitions':rows,'terminal_images_reference_last_transition':[d['episode_end_info'][k] is prev[k] for k in ['img_forward','img_backward']]})
(p/'diagnostic_scan_provenance.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
