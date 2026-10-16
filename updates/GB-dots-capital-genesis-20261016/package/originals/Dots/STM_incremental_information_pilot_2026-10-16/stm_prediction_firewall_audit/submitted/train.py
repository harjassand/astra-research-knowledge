"""Train/development-only frozen STM pilot. No test-loading or scoring entry point.
Numeric JSON model snapshots contain no executable objects or pickle payloads.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import scipy
import sklearn
from sklearn.ensemble import ExtraTreesRegressor, HistGradientBoostingRegressor
from features import feature_maps, schema, schema_hash

SEED=20261016
ARMS=('A','A+C','A+F')
THRESHOLD=.288*np.sqrt(3)/3
CAVEAT='Recorded-scan proxy subset: numerical prediction of recorded image-localization labels; physical pre-scan timing/freshness interpretation is conditional on documented logger semantics. Current gain calibration is unverified.'
PINNED={'numpy':'2.3.5','scipy':'1.17.0','sklearn':'1.8.0'}

def versions():
    actual={'numpy':np.__version__,'scipy':scipy.__version__,'sklearn':sklearn.__version__}
    if actual!=PINNED: raise RuntimeError(f'Library mismatch: {actual}')
    return actual

def estimators():
    return [ExtraTreesRegressor(n_estimators=512,min_samples_leaf=k,max_features=1.0,bootstrap=False,random_state=SEED,n_jobs=1) for k in (2,8)]+[HistGradientBoostingRegressor(max_iter=300,learning_rate=.05,max_leaf_nodes=15,min_samples_leaf=10,l2_regularization=1,early_stopping=False,random_state=SEED)]

def parameters():
    return [e.get_params(deep=False) for e in estimators()]

def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def save_new(path,obj):
    with Path(path).open('xb') as f: f.write(canonical(obj))

def episode_weights(ids):
    ids=np.asarray(ids); unique,counts=np.unique(ids,return_counts=True)
    lookup=dict(zip(unique,counts)); weights=np.array([1/lookup[i] for i in ids])
    return weights/weights.mean()

def per_episode(values, ids, operation=np.mean):
    ids=np.asarray(ids)
    return {str(i):float(operation(np.asarray(values)[ids==i])) for i in np.unique(ids)}

def macro_error(pred,target,ids):
    return float(np.mean(list(per_episode(np.linalg.norm(pred-target,axis=1),ids).values())))

def choose(scores):
    best=min(scores)
    return next(i for i,s in enumerate(scores) if s<=best+1e-9)

def envelope(pred,target,ids):
    maxima=per_episode(np.linalg.norm(pred-target,axis=1),ids,np.max)
    return float(np.quantile(list(maxima.values()),.9,method='linear'))

def metric_summary(pred,target,ids,records,labels):
    error=np.linalg.norm(pred-target,axis=1)
    goal_difference=np.array([r['g_minus_p'] for r in records])
    radius=np.array([r['r'] for r in labels],dtype=float)
    radius_error=np.abs(np.linalg.norm(pred-goal_difference,axis=1)-radius)
    mse=float(np.mean(list(per_episode(error**2,ids).values())))
    return {'rows':len(target),'episodes':len(set(ids)),
            'macro_endpoint_error':float(np.mean(list(per_episode(error,ids).values()))),
            'macro_squared_euclidean_error':mse,'root_macro_squared_euclidean_error':float(np.sqrt(mse)),
            'pooled_median_endpoint_error':float(np.quantile(error,.5,method='linear')),
            'pooled_p90_endpoint_error':float(np.quantile(error,.9,method='linear')),
            'pooled_quantile_weighting':'each row equally weighted',
            'macro_absolute_target_radius_error':float(np.mean(list(per_episode(radius_error,ids).values()))),
            'per_episode_endpoint_error':per_episode(error,ids)}

def quality_strata(pred,target,ids,records,labels):
    disagreement=np.array([r['disagreement'] for r in labels])
    result={}
    for name,mask in [('at_or_below_threshold',disagreement<=THRESHOLD),('above_threshold',disagreement>THRESHOLD)]:
        ix=np.flatnonzero(mask)
        result[name]=metric_summary(pred[mask],target[mask],ids[mask],[records[i] for i in ix],[labels[i] for i in ix]) if len(ix) else {'rows':0,'episodes':0}
    return {'threshold_nm':float(THRESHOLD),'interpretation':'Label-quality sensitivity only; no exclusion or adjusted primary result','strata':result}

def paired_improvements(reference,pred,target,ids):
    ref=per_episode(np.linalg.norm(reference-target,axis=1),ids)
    candidate=per_episode(np.linalg.norm(pred-target,axis=1),ids)
    improvements={i:ref[i]-candidate[i] for i in ref}
    values=np.array(list(improvements.values()))
    return {'direction':'positive favors candidate','mean':float(values.mean()),'median':float(np.median(values)),
            'min':float(values.min()),'max':float(values.max()),'strict_win_fraction':float(np.mean(values>0)),
            'episodes':len(values),'per_episode':improvements}

def classification_support(labels,ids):
    y=np.array([r['y'] for r in labels]); ids=np.asarray(ids)
    counts={str(k):{'rows':int(np.sum(y==k)),'episodes':len(set(ids[y==k]))} for k in (0,1)}
    return {'counts':counts,'meets_train_development_requirement':all(v['rows']>=20 and v['episodes']>=10 for v in counts.values())}

def freeze_model(model):
    if isinstance(model,ExtraTreesRegressor):
        trees=[]
        for e in model.estimators_:
            t=e.tree_
            trees.append({'left':t.children_left.tolist(),'right':t.children_right.tolist(),'feature':t.feature.tolist(),'threshold':t.threshold.tolist(),'value':t.value[:,:,0].tolist()})
        return {'kind':'extra_trees','n_features':model.n_features_in_,'trees':trees}
    if isinstance(model,list):
        coords=[]
        for e in model:
            trees=[]
            for iteration in e._predictors:
                if len(iteration)!=1: raise ValueError('Unexpected HGB predictors')
                nodes=iteration[0].nodes
                if np.any(nodes['is_categorical']): raise ValueError('Categorical split unsupported')
                trees.append({key:nodes[field].tolist() for key,field in [('left','left'),('right','right'),('feature','feature_idx'),('threshold','num_threshold'),('value','value'),('leaf','is_leaf')]})
            coords.append({'baseline':float(e._baseline_prediction[0,0]),'trees':trees})
        return {'kind':'hist_gradient_boosting','n_features':model[0].n_features_in_,'coordinates':coords}
    raise TypeError('Unregistered estimator')

def _tree_predict(tree,X,hgb=False):
    n=len(X); node=np.zeros(n,dtype=np.int64)
    left=np.asarray(tree['left']); right=np.asarray(tree['right']); feature=np.asarray(tree['feature']); threshold=np.asarray(tree['threshold'])
    leaf=np.asarray(tree['leaf'],dtype=bool) if hgb else left==-1
    for _ in range(len(left)+1):
        active=np.flatnonzero(~leaf[node])
        if not len(active): return np.asarray(tree['value'])[node]
        k=node[active]
        node[active]=np.where(X[active,feature[k]]<=threshold[k],left[k],right[k])
    raise ValueError('Cyclic tree')

def predict_frozen(snapshot,X):
    X=np.asarray(X,dtype=np.float64)
    if X.ndim!=2 or X.shape[1]!=snapshot['n_features'] or not np.isfinite(X).all(): raise ValueError('Invalid predictor matrix')
    if snapshot['kind']=='extra_trees':
        # sklearn tree ensembles convert raw predictors to float32 before routing.
        X=X.astype(np.float32)
        out=np.zeros((len(X),2))
        for t in snapshot['trees']: out+=_tree_predict(t,X)
        return out/len(snapshot['trees'])
    if snapshot['kind']=='hist_gradient_boosting':
        out=np.zeros((len(X),2))
        for j,c in enumerate(snapshot['coordinates']):
            out[:,j]=c['baseline']
            for t in c['trees']: out[:,j]+=_tree_predict(t,X,True)
        return out
    raise ValueError('Unknown frozen model')

def baseline_predictions(records):
    return {'persistence':np.zeros((len(records),2)), 'command_request_endpoint':np.array([r['history'][-1]['end_nm'] for r in records],dtype=np.float64)}

def _jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]

def load_split(directory,split):
    if split not in ('train','development'): raise ValueError('Training process cannot open test inputs or labels')
    base=Path(directory)
    inputs=_jsonl(base/f'{split}_inputs.jsonl')
    routing=_jsonl(base/f'{split}_routing.jsonl')
    labels=_jsonl(base/f'{split}_labels.jsonl')
    if not inputs or not(len(inputs)==len(routing)==len(labels)): raise ValueError('Unaligned data')
    for row in inputs:
        if set(row)!={'p','g_minus_p','prior_disagreement','history'}: raise ValueError('Unsanitized top-level predictor fields')
        for h in row['history']:
            if set(h)!={'action','start_nm','end_nm','d','current'}: raise ValueError('Unsanitized history fields')
    target=np.array([r['delta'] for r in labels],dtype=np.float64)
    if target.shape!=(len(inputs),2) or not np.isfinite(target).all(): raise ValueError('Invalid labels')
    ids=np.array([r['episode_id'] for r in routing])
    maps=[feature_maps(r) for r in inputs]
    matrices={a:np.vstack([row[a] for row in maps]) for a in ARMS}
    return inputs,ids,target,matrices,labels

def run(directory,output,approval,audit_report=None):
    if approval!='ROOT_AUDIT_GATES_APPROVED': raise RuntimeError('Explicit parent gate approval required')
    versions()
    if audit_report is None or not Path(audit_report).is_file(): raise ValueError('Explicit audit report path required for freeze')
    protocol=Path('/workspace/shared/stm_prediction_protocol/PROTOCOL_v1.1.md')
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    if list(output.iterdir()): raise RuntimeError('Refuse existing fit output: amendment required for rerun')
    ti,tid,ty,tx,tl=load_split(directory,'train'); di,did,dy,dx,dl=load_split(directory,'development')
    weights=episode_weights(tid)
    summary={'reporting_caveat':CAVEAT,'protocol_sha256':digest(protocol),'audit_report_sha256':digest(audit_report),'protocol':'v1.1','versions':versions(),'schema_hash':schema_hash(),'candidate_parameters':parameters(),'selected':{},'development_candidates':{},'model_hashes':{},'code_hashes':{name:digest(Path(__file__).parent/name) for name in ('features.py','train.py','test_features_train.py')},'input_hashes':{f'{s}_{k}.jsonl':digest(Path(directory)/f'{s}_{k}.jsonl') for s in ('train','development') for k in ('inputs','routing','labels')}}
    save_new(output/'feature_schema.json',schema())
    all_predictions={}
    selected_predictions={}
    for arm in ARMS:
        scores=[]; predictions=[]
        for index,estimator in enumerate(estimators()):
            try:
                if index<2:
                    model=estimator.fit(tx[arm],ty,sample_weight=weights)
                    pred=model.predict(dx[arm])
                else:
                    model=[HistGradientBoostingRegressor(**estimator.get_params()).fit(tx[arm],ty[:,j],sample_weight=weights) for j in range(2)]
                    pred=np.column_stack([m.predict(dx[arm]) for m in model])
                snap=freeze_model(model)
                frozen_pred=predict_frozen(snap,dx[arm])
                if not np.allclose(pred,frozen_pred,rtol=1e-12,atol=1e-12): raise RuntimeError('Frozen model prediction mismatch')
                filename=f'{arm.replace("+","_")}_{index+1}.json'
                save_new(output/filename,snap)
                summary['model_hashes'][filename]=digest(output/filename)
                score=macro_error(pred,dy,did); scores.append(score); predictions.append(pred)
                summary['development_candidates'][f'{arm}:{index+1}']=metric_summary(pred,dy,did,di,dl)
                summary['development_candidates'][f'{arm}:{index+1}']['label_quality']=quality_strata(pred,dy,did,di,dl)
                all_predictions[(arm,index)]=pred
            except Exception as e:
                save_new(output/'FAILED.json',{'arm':arm,'candidate':index+1,'error':repr(e),'reason':'No substitution or rerun under frozen protocol'})
                raise
        selected=choose(scores)
        selected_predictions[arm]=predictions[selected]
        summary['selected'][arm]={'candidate':selected+1,'model_file':f'{arm.replace("+","_")}_{selected+1}.json','development_macro_endpoint_error':scores[selected],'q':envelope(predictions[selected],dy,did)}
    baselines=baseline_predictions(di)
    summary['development_baselines']={name:metric_summary(p,dy,did,di,dl) for name,p in baselines.items()}
    for name,p in baselines.items(): summary['development_baselines'][name]['label_quality']=quality_strata(p,dy,did,di,dl)
    summary['development_selected_paired']={f'{candidate}_versus_{ref}':paired_improvements(selected_predictions[ref],selected_predictions[candidate],dy,did) for ref,candidate in [('A','A+C'),('A','A+F'),('A+C','A+F')]}
    for arm,pred in selected_predictions.items():
        for name,reference in baselines.items(): summary['development_selected_paired'][f'{arm}_versus_{name}']=paired_improvements(reference,pred,dy,did)
    summary['development_same_hyperparameter_paired']={str(i+1):{f'{candidate}_versus_{ref}':paired_improvements(all_predictions[(ref,i)],all_predictions[(candidate,i)],dy,did) for ref,candidate in [('A','A+C'),('A','A+F'),('A+C','A+F')]} for i in range(3)}
    summary['classification_support']={'train':classification_support(tl,tid),'development':classification_support(dl,did)}
    summary['train_counts']={'rows':len(ti),'episodes':len(set(tid))}; summary['development_counts']={'rows':len(di),'episodes':len(set(did))}
    save_new(output/'fit_lock.json',summary)
    save_new(output/'fit_lock.sha256.json',{'sha256':digest(output/'fit_lock.json')})
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--audit-report',required=True); parser.add_argument('--sanitized',required=True); parser.add_argument('--output',required=True); parser.add_argument('--approval',required=True)
    args=parser.parse_args(); result=run(args.sanitized,args.output,args.approval,args.audit_report)
    print(json.dumps({key:result[key] for key in ('reporting_caveat','selected','train_counts','development_counts','classification_support')},indent=2))
