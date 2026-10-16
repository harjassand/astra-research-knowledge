"""Audit-only outputs. No predictor, feature generation, or new episode acquisition.
Exact byte equality obviates image hashes, which are never exported to predictors.
"""
import json, math, pathlib, hashlib
from safe_reader import parse, decode, require
BASE=pathlib.Path('/workspace/shared/stm_control_logs')
OUT=pathlib.Path(__file__).parent
NAMES=('00000.npy','01500.npy','02920.npy')
IMAGES=('img_forward','img_backward')
def main():
    endpoints=[];scans=[];manifest=[];threshold=0.288/math.sqrt(3)
    old_scans={x['episode']:x for x in json.loads((BASE/'diagnostic_scan_provenance.json').read_text())}
    for name in NAMES:
        path=BASE/'acquired/training_data_and_model_parameters/training_data'/name
        root=parse(path);d=root.state[4][0];ep=decode(root);t=ep['transitions'];n=len(t['action'])
        require(n>0 and all(len(t[k])==n for k in ('state','next_state','reward','done','info')),'Transition alignment')
        require(t['done']==[False]*(n-1)+[True],'Terminal flags')
        start=ep['episode_start_info']['info'];end=ep['episode_end_info'];error=math.dist(start['goal_absolute_nm'],end['atom_absolute_nm'])
        require(abs(error-t['info'][-1]['dist_destination'])<1e-10,'Endpoint distance')
        require(all(end[k]['shape']==(128,128) for k in IMAGES),'Terminal shape')
        require(t['info'][-1]['atom_absolute_nm']==end['atom_absolute_nm'],'Endpoint position')
        require(all(i['current_series']['length']==i['d']['length'] for i in t['info']),'Trace length')
        endpoints.append({'episode':name,'partition':'diagnostic_exclude_from_test','logged_actions':n,'terminal_error_nm':error,'terminal_success':error<threshold,'terminal_image_pair_present':True,'terminal_reason':'not separately logged','time_cost':'unavailable','policy_value':'not identifiable from this audit'})
        prev=d['episode_start_info'];rows=[]
        for idx,info in enumerate(d['transitions']['info']):
            img=info['img_info'];reuse=[img[k] is prev[k] for k in IMAGES]
            equal=[img[k].state[4]==prev[k].state[4] for k in IMAGES]
            old=old_scans[name]['transitions'][idx]
            require(reuse==old['same_serialized_image_object_as_prior'] and equal==old['same_image_bytes_as_prior'],'Legacy identity/bytes mismatch')
            rows.append({'transition_index':idx,'same_serialized_image_object_as_prior':reuse,'same_image_bytes_as_prior':equal,'distinct_serialized_image_pair':not any(reuse),'physical_new_scan_verified':False,'physical_new_scan_status':'unknown: distinct objects or bytes do not prove physical acquisition','current_trace_present':info['current_series'] is not None})
            prev=img
        scans.append({'episode':name,'diagnostic_only':True,'scan_flag_explicit':False,'transitions':rows,'terminal_images_reference_last_transition':[d['episode_end_info'][k] is prev[k] for k in IMAGES]})
        # File digest is provenance-only, never an image feature or predictor input.
        manifest.append({'episode':name,'bytes':path.stat().st_size,'file_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (OUT/'endpoint_audit.json').write_text(json.dumps({'scope':'three diagnostics only; no aggregate generalization statistic','success_threshold_nm':threshold,'records':endpoints},indent=2))
    (OUT/'scan_identity_audit.json').write_text(json.dumps({'artifact_role':'audit_only_never_predictor_input','records':scans},indent=2))
    (OUT/'input_manifest_audit_only.json').write_text(json.dumps(manifest,indent=2))
    print('Verified three diagnostic episodes; legacy endpoint summaries and image identity/byte observations match. No physical fresh-scan inference.')
if __name__=='__main__':main()
