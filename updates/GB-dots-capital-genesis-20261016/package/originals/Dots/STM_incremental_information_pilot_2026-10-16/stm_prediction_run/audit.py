"""Frozen v1.1 eligibility auditor. Author sources are read as text, never imported.
Only safe_reader parses archive bytes. No test outcome is printed or summarized.
"""
import argparse, collections, hashlib, json, math, os, pathlib, struct, sys
sys.path.insert(0, '/workspace/shared/stm_reader_audit')
from safe_reader import parse, Node, dtype, numbers, ReaderError
BASE=pathlib.Path('/workspace/shared/stm_prediction_run')
CONTROL=pathlib.Path('/workspace/shared/stm_control_logs')
PROTOCOL=pathlib.Path('/workspace/shared/stm_prediction_protocol')
IMAGES=('img_forward','img_backward')
THRESHOLD=.288*math.sqrt(3)/3
class GateError(ValueError): pass
def need(x,why):
    if not x: raise GateError(why)
def close(a,b): return len(a)==len(b) and all(abs(x-y)<=1e-9 for x,y in zip(a,b))
def scalar(v):
    if isinstance(v,Node):
        need(v.args[0].args=='numpy.core.multiarray scalar','scalar_type')
        return numbers(dtype(v.args[1][0]),v.args[1][1])[0]
    need(type(v) in (int,float,bool),'scalar_type');return v
def array(v,shape=None):
    need(isinstance(v,Node) and v.args[0].args=='numpy.core.multiarray _reconstruct','array_type')
    s=v.state;dt=dtype(s[2]);need(dt in ('f8','f4'),'array_dtype')
    if shape is not None:need(s[1]==shape,'array_shape')
    return numbers(dt,s[4])
def vec(v):return array(v,(2,))
def num(v):
    x=scalar(v);need(type(x) in (int,float) and math.isfinite(x),'numeric_scalar');return float(x)
def image(v):
    vals=array(v);need(len(v.state[1])==2 and min(v.state[1])>0,'image_shape')
    # Canonical little-endian numerical bytes, signed zero canonicalized; dtype/shape included.
    dt=dtype(v.state[2]);fmt='<'+('d' if dt=='f8' else 'f')
    b=b''.join(struct.pack(fmt,0. if x==0 else x) for x in vals)
    return hashlib.sha256(json.dumps({'dtype':dt,'shape':v.state[1]},sort_keys=True,separators=(',',':')).encode()+b'\0'+b).hexdigest()
def frame(im):
    off=vec(im['offset_nm']); ln=im['len_nm']
    # Documented controller returns two-dimensional scan extent.
    length=vec(ln) if isinstance(ln,Node) and ln.args[0].args.endswith('_reconstruct') else list(ln) if type(ln) in (list,tuple) else [num(ln)]*2
    need(len(length)==2 and all(type(x) in (float,int) and math.isfinite(x) and x>0 for x in length),'image_extent')
    need(im[IMAGES[0]].state[1]==im[IMAGES[1]].state[1],'pair_shape')
    return off+length
def coords(info,prefix):
    out={k:vec(info[prefix+k]) for k in ('absolute_nm','relative_nm','absolute_nm_f','absolute_nm_b','relative_nm_f','relative_nm_b')}
    for k in ('absolute_nm','relative_nm'):
        need(close(out[k],[(a+b)/2 for a,b in zip(out[k+'_f'],out[k+'_b'])]),'coordinate_mean')
    return out
def source_audit():
    provenance=json.loads((CONTROL/'provenance.json').read_text());checked={}
    for a in provenance['artifacts']:
        if a['path'].endswith(('Env_new.py','createc_control.py','episode_memory.py','single_atom_training.ipynb')):
            b=(CONTROL/a['path']).read_bytes();need(len(b)==a['bytes'] and hashlib.sha256(b).hexdigest()==a['sha256'],'source_hash')
            checked[a['path']]=a['sha256']
    s=(CONTROL/'acquired/AMRL/Environment/Env_new.py').read_text()
    step=s[s.index('    def step(self'):s.index('    def calculate_potential')]
    need(step.index('current_series, d = self.step_latman')<step.index('if done or jump:')<step.index('self.check_similarity()'),'source_timing')
    need('self.img_info =' not in step and "'img_info':self.img_info" in step,'source_reuse')
    need('d = np.sqrt(((x-x[0])**2 + (y-y[0])**2))' in s,'source_radial_d')
    nb=json.loads((CONTROL/'acquired/single_atom_training.ipynb').read_text())
    text='\n'.join(''.join(c.get('source',[])) for c in nb['cells'])
    need('step_nm = 0.4' in text and 'goal_nm  = 2' in text,'source_declared_mapping')
    return {'verified_source_sha256':checked,'mapping':'published notebook declares step_nm=0.4, goal_nm=2, but archive has no run-specific declaration; stored requests retained without mapping or hardware calibration certification','timing':'documented source compatible; physical timing and freshness remain conditional','current_units':'source-implied A; downstream conversion to numerical nA is 1e9; hardware gain calibration unverified','frame_gate':'offset, two-dimensional extent, and image shape fixed within episode; no future drift correction or cross-episode position stitching'}
def episode(path,eid,split,root=None):
    e=(parse(path) if root is None else root).state[4][0]
    need(set(e)=={'episode_start_info','transitions','episode_end_info'},'episode_schema')
    t=e['transitions'];need(set(t)=={'state','action','next_state','reward','done','info'},'transition_schema')
    need(all(type(v) is list for v in t.values()),'transition_list_type')
    n=len(t['action']);need(n>0 and all(len(v)==n for v in t.values()),'transition_lengths')
    start=e['episode_start_info']
    need(set(start['info'])=={'start_absolute_nm','start_relative_nm','goal_absolute_nm','goal_relative_nm','start_absolute_nm_f','start_absolute_nm_b','start_relative_nm_f','start_relative_nm_b'},'reset_info_schema')
    prev=start;pc=coords(start['info'],'start_')
    p=pc['absolute_nm'];goal=vec(start['info']['goal_absolute_nm']);vec(start['info']['goal_relative_nm'])
    fr=frame(start);sh=start[IMAGES[0]].state[1]
    fingerprints=set();fingerprint_records=[];object_coords={};object_images={}
    def record(im,coordinates,where):
        f=frame(im);need(close(f,fr),'frame_change');need(im[IMAGES[0]].state[1]==sh,'frame_shape_change')
        for k in IMAGES:
            h=image(im[k]);fingerprints.add(h);fingerprint_records.append({'location':where,'direction':k,'sha256':h})
            key=id(im[k]); coord=coordinates['absolute_nm_'+('f' if k=='img_forward' else 'b')]+coordinates['relative_nm_'+('f' if k=='img_forward' else 'b')]
            need(key not in object_coords or close(object_coords[key],coord),'reused_image_coordinate_conflict')
            object_coords[key]=coord;object_images[key]=im[k]
    record(start,pc,'start');seen_hashes=set(fingerprints)
    rows=[];labels=[];routing=[];history=[];anchor=True;reasons=collections.Counter();prior=math.dist(pc['absolute_nm_f'],pc['absolute_nm_b'])
    for j in range(n):
        a=array(t['action'][j],(6,));need(all(-1-1e-7<=x<=1+1e-7 for x in a),'normalized_action_range')
        array(t['state'][j],(4,));array(t['next_state'][j],(4,));num(t['reward'][j]);need(type(scalar(t['done'][j])) is bool,'done_type')
        info=t['info'][j]
        need(set(info)=={'current_series','d','start_nm','end_nm','dist_destination','atom_absolute_nm','atom_relative_nm','atom_absolute_nm_f','atom_relative_nm_f','atom_absolute_nm_b','atom_relative_nm_b','img_info'},'info_schema')
        reqs=vec(info['start_nm']);reqe=vec(info['end_nm'])
        num(info['dist_destination']);c=coords(info,'atom_');im=info['img_info'];record(im,c,j)
        reuse=[im[k] is prev[k] for k in IMAGES]
        need(reuse[0]==reuse[1],'mixed_image_freshness')
        if all(reuse):need(all(close(c[k],pc[k]) for k in c),'reused_coordinate_change')
        current=info['current_series'];d=info['d'];trace_ok=current is not None and d is not None
        if trace_ok:
            iv=array(current);dv=array(d)
            need(current.state[1]==(len(iv),) and d.state[1] in ((len(dv),),(len(dv),1)),'trace_shape')
            need(len(iv)==len(dv) and len(iv)>=2 and all(x>=0 for x in dv) and abs(dv[0])<=1e-9,'trace_gate')
            history.append({'action':a,'start_nm':reqs,'end_nm':reqe,'d':dv,'current':iv})
        else:
            anchor=False;history=[];reasons['missing_trace']+=1
        fresh=not any(reuse)
        changed=any(im[k].state[4]!=prev[k].state[4] for k in IMAGES)
        # Reappearance of an earlier distinct pair is copied/ambiguous, not an eligible boundary.
        old_ids=seen_ids if j else set(id(start[k]) for k in IMAGES)
        nonadjacent_copy=any(image(im[k]) in seen_hashes and image(im[k])!=image(prev[k]) for k in IMAGES)
        ambiguous=fresh and (not changed or any(id(im[k]) in old_ids for k in IMAGES) or nonadjacent_copy)
        if ambiguous:
            reasons['copied_or_unchanged_new_pair']+=1;anchor=False;history=[]
        elif fresh:
            if anchor and trace_ok:
                nxt=c['absolute_nm'];r=math.dist(nxt,goal)
                rows.append({'p':p[:],'g_minus_p':[g-x for g,x in zip(goal,p)],'prior_disagreement':prior,'history':history[:]})
                labels.append({'delta':[x-y for x,y in zip(nxt,p)],'r':r,'y':int(r<THRESHOLD),'disagreement':math.dist(c['absolute_nm_f'],c['absolute_nm_b'])})
                routing.append({'episode_id':eid,'transition_index':j})
            else: reasons['dependent_boundary_without_anchor']+=1
            p=c['absolute_nm'];prior=math.dist(c['absolute_nm_f'],c['absolute_nm_b']);history=[];anchor=True
        seen_ids=old_ids|{id(im[k]) for k in IMAGES};seen_hashes.update(image(im[k]) for k in IMAGES);prev=im;pc=c
    end=e['episode_end_info']
    need(scalar(t['done'][-1]) is True and all(scalar(x) is False for x in t['done'][:-1]),'normal_completion_flags')
    need(all(end[k] is prev[k] for k in IMAGES),'end_image_alias')
    need(close(vec(end['atom_absolute_nm']),pc['absolute_nm']) and close(vec(end['atom_relative_nm']),pc['relative_nm']),'end_coordinate_alias')
    record(end,pc,'end')
    return {'episode_id':eid,'split':split,'rows':rows,'labels':labels,'routing':routing,'fingerprints':fingerprints,'fingerprint_records':fingerprint_records,'row_exclusions':dict(reasons),'transitions':n}
def collect_images(root):
    """Visit all inert graph images even in excluded episodes; aliases retained."""
    seen=set();hashes=set();records=[]
    def walk(x,path):
        if type(x) in (dict,list,tuple) or isinstance(x,Node):
            if id(x) in seen:return
            seen.add(id(x))
        if type(x) is dict:
            for k,v in x.items():
                if k in IMAGES:
                    h=image(v);hashes.add(h);records.append({'location':path+'.'+k,'sha256':h})
                else:walk(v,path+'.'+k)
        elif type(x) in (list,tuple):
            for i,v in enumerate(x):walk(v,path+f'[{i}]')
        elif isinstance(x,Node) and x.state and dtype(x.state[2])=='O8':walk(x.state[4][0],path)
    walk(root,'root');need(bool(hashes),'no_image_graph');return hashes,records

def deduplicate(all_eps):
    parent={x['episode_id']:x['episode_id'] for x in all_eps}
    def find(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    def union(a,b):parent[find(a)]=find(b)
    owner={}
    for ep in all_eps:
        for h in ep['fingerprints']:
            if h in owner:union(ep['episode_id'],owner[h])
            else:owner[h]=ep['episode_id']
    groups=collections.defaultdict(list)
    for ep in all_eps:groups[find(ep['episode_id'])].append(ep)
    eligible=[];excluded=[]
    for comp in groups.values():
        splits={x['split'] for x in comp};ids=sorted(x['episode_id'] for x in comp)
        for ep in comp:
            if ep['split']=='burned':continue
            reason='component_touches_burned' if 'burned' in splits else 'component_crosses_splits' if len(splits)>1 else 'later_duplicate_within_split' if ep['episode_id']!=min(ids) else None
            if reason:excluded.append({'episode_id':ep['episode_id'],'split':ep['split'],'reason':reason,'component_episode_ids':ids})
            elif not ep.get('schema_excluded'):eligible.append(ep)
    return eligible,excluded

def dump(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+'\n')
def jsonl(path,records):
    with path.open('x') as f:
        for row in records:f.write(json.dumps(row,separators=(',',':'),allow_nan=False)+'\n')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--diagnostics-only',action='store_true');args=ap.parse_args()
    source=source_audit();manifest=json.loads((PROTOCOL/'split_manifest.json').read_text());all_eps=[];failures=[];received=[]
    targets=[(eid,'burned',CONTROL/f'acquired/training_data_and_model_parameters/training_data/{eid:05d}.npy',None) for eid in manifest['burned_episode_ids']]
    if not args.diagnostics_only:
        for split,part in manifest['splits'].items():
            for item in part['episodes']: targets.append((item['episode_id'],split,BASE/f"acquired/{item['episode_id']:05d}.npy",item))
    for eid,split,path,item in targets:
        b=path.read_bytes();sha=hashlib.sha256(b).hexdigest()
        if item:need(len(b)==item['bytes'] and hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==item['git_blob_sha1'],'acquisition_integrity')
        received.append({'episode_id':eid,'split':split,'bytes':len(b),'sha256':sha})
        try:
            root=parse(path);hashes,hash_records=collect_images(root)
        except (GateError,ReaderError,KeyError,TypeError,IndexError) as exc:
            dump(BASE/'audit_report.json',{'status':'STOP_UNSAFE_OR_AMBIGUOUS_IMAGE_GRAPH','episode_id':eid,'reason':str(exc),'files':received})
            print('STOP_UNSAFE_OR_AMBIGUOUS_IMAGE_GRAPH');return
        try:all_eps.append(episode(path,eid,split,root))
        except (GateError,ReaderError,KeyError,TypeError,IndexError) as exc:
            reason=str(exc);failures.append({'episode_id':eid,'split':split,'reason':reason})
            all_eps.append({'episode_id':eid,'split':split,'fingerprints':hashes,'fingerprint_records':hash_records,'schema_excluded':True,'rows':[],'labels':[],'routing':[],'row_exclusions':{},'transitions':None})
            # Unrecognized structures stop immediately; repeated numerical/provenance contradictions are systemic.
            unknown=isinstance(exc,(ReaderError,KeyError,TypeError,IndexError)) or any(w in reason for w in ('schema','type','shape','lengths'))
            if not args.diagnostics_only and (unknown or sum(x['reason']==reason for x in failures)>=2):
                dump(BASE/'audit_report.json',{'status':'STOP_SYSTEMIC_OR_UNKNOWN_SCHEMA_GATE','source':source,'schema_exclusions':failures,'files':received,'systemic_schema_failure':True})
                print('STOP_SYSTEMIC_OR_UNKNOWN_SCHEMA_GATE: see audit_report.json');return
    # A repeated incompatibility is a systemic pattern: stop without adaptation.
    counts=collections.Counter(x['reason'] for x in failures)
    report={'source':source,'files':received,'schema_exclusions':failures,'systemic_schema_failure':any(v>=2 for v in counts.values()),'diagnostics_only':args.diagnostics_only}
    if args.diagnostics_only:
        report['compatible_diagnostic_count']=len(all_eps)-len(failures);dump(BASE/'diagnostic_builder_audit.json',report)
        print(json.dumps({'diagnostic_compatible':len(all_eps)-len(failures),'schema_failures':failures}));return
    eligible,dedup=deduplicate(all_eps)
    report['dedup_exclusions']=dedup
    report['counts']={s:{'eligible_episodes':sum(x['split']==s and bool(x['rows']) for x in eligible),'eligible_boundaries':sum(len(x['rows']) for x in eligible if x['split']==s)} for s in manifest['splits']}
    report['episode_audit']=[{k:ep[k] for k in ('episode_id','split','row_exclusions','transitions')}|{'eligible_boundaries_before_dedup':len(ep['rows'])} for ep in all_eps]
    report['image_fingerprints_audit_only']=[{'episode_id':ep['episode_id'],'images':ep['fingerprint_records']} for ep in all_eps]
    minima={'train':(80,100),'development':(25,30),'test':(35,40)}
    feasible=all(report['counts'][s]['eligible_episodes']>=a and report['counts'][s]['eligible_boundaries']>=b for s,(a,b) in minima.items())
    report['status']='PASS' if feasible else 'STOP_INFEASIBLE'
    report['audit_code_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    dump(BASE/'audit_report.json',report)
    if not feasible:print(json.dumps({'status':report['status'],'counts':report['counts']}));return
    out=BASE/'sanitized';out.mkdir(exist_ok=True);sealed=BASE/'sealed';sealed.mkdir(exist_ok=True);os.chmod(sealed,0o700)
    for split in manifest['splits']:
        eps=sorted((x for x in eligible if x['split']==split),key=lambda x:x['episode_id'])
        jsonl(out/f'{split}_inputs.jsonl',(r for x in eps for r in x['rows']))
        jsonl(out/f'{split}_routing.jsonl',(r for x in eps for r in x['routing']))
        labelpath=(sealed if split=='test' else out)/f'{split}_labels.jsonl'
        jsonl(labelpath,(r for x in eps for r in x['labels']));os.chmod(labelpath,0o400)
    print(json.dumps({'status':report['status'],'counts':report['counts'],'test_labels':'sealed; not inspected or summarized'}))
if __name__=='__main__':main()
