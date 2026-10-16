"""One-shot, separately root-authorized held-out evaluator.
The exclusive marker is created before ANY held-out label access; even failure
burns the evaluation attempt. Never delete it or retry without explicit amendment.
"""
import argparse
import json
import hashlib
from pathlib import Path
import stat
import numpy as np
import train
import prediction_stage as stage


def support(labels,ids):
    counts=train.classification_support(labels,ids)['counts']
    return {'counts':counts,'meets_test_requirement':all(x['rows']>=15 and x['episodes']>=10 for x in counts.values())}

def classification(predictions,records,labels,ids,fit):
    supports={'train':fit['classification_support']['train'],'development':fit['classification_support']['development'],'test':support(labels,ids)}
    available=all(all(c['rows']>=20 and c['episodes']>=10 for c in supports[s]['counts'].values()) for s in ('train','development')) and supports['test']['meets_test_requirement']
    result={'available':available,'support':supports,'threshold_nm':float(train.THRESHOLD),'weighting':'pooled rows; deterministic threshold only'}
    if not available:
        result['reason']='Prespecified support gate failed; classification unavailable. Support counts only.'
        return result
    y=np.array([r['y'] for r in labels]); goal=np.array([r['g_minus_p'] for r in records]); metrics={}
    for name,p in predictions.items():
        yh=np.linalg.norm(p-goal,axis=1)<train.THRESHOLD
        tp=int(np.sum(yh & (y==1))); tn=int(np.sum(~yh & (y==0))); fp=int(np.sum(yh & (y==0))); fn=int(np.sum(~yh & (y==1)))
        sensitivity=tp/(tp+fn); specificity=tn/(tn+fp)
        metrics[name]={'balanced_accuracy':(sensitivity+specificity)/2,'sensitivity':sensitivity,'specificity':specificity,'precision':tp/(tp+fp) if tp+fp else None,'precision_status':'defined' if tp+fp else 'undefined: no predicted positives','tp':tp,'tn':tn,'fp':fp,'fn':fn}
    result['metrics']=metrics
    return result

def report(predictions,records,routing,labels,fit):
    n=len(records); stage.require(n==len(routing)==len(labels),'Unaligned labels')
    ids=np.array([r['episode_id'] for r in routing]); target=np.array([r['delta'] for r in labels],dtype=float)
    stage.require(target.shape==(n,2) and np.isfinite(target).all(),'Invalid displacement labels')
    for inp,label in zip(records,labels):
        stage.require(set(label)=={'delta','r','y','disagreement'},'Invalid label schema')
        stage.require(np.isfinite(label['r']) and label['r']>=0 and np.isfinite(label['disagreement']) and label['disagreement']>=0,'Invalid radius/disagreement')
        stage.require(type(label['y']) is int and label['y'] in (0,1) and label['y']==int(label['r']<train.THRESHOLD),'Invalid attainment label')
        stage.require(abs(np.linalg.norm(np.asarray(label['delta'])-np.asarray(inp['g_minus_p']))-label['r'])<=1e-9,'Label radius mismatch')
    expected={f'{a}:{i}' for a in train.ARMS for i in (1,2,3)}|{'persistence','command_request_endpoint'}
    stage.require(set(predictions)==expected,'Missing or extra prediction models')
    predictions={k:np.asarray(v,dtype=float) for k,v in predictions.items()}
    for p in predictions.values(): stage.require(p.shape==(n,2) and np.isfinite(p).all(),'Invalid predictions')
    selected={a:predictions[f'{a}:{fit["selected"][a]["candidate"]}'] for a in train.ARMS}
    main={**selected,**{a:predictions[a] for a in ('persistence','command_request_endpoint')}}
    result={'reporting_caveat':train.CAVEAT,'units':'nm unless squared','selected_models':fit['selected'],'counts':{'rows':n,'episodes':len(set(ids))},'metrics':{},'paired':{},'same_hyperparameter_paired':{},'chronology_blocks':{},'empirical_residual_envelopes':{}}
    for name,p in main.items():
        result['metrics'][name]=train.metric_summary(p,target,ids,records,labels)
        result['metrics'][name]['label_quality']=train.quality_strata(p,target,ids,records,labels)
    comparisons=list(stage.PAIRS)+[(base,a) for base in ('persistence','command_request_endpoint') for a in train.ARMS]
    for ref,a in comparisons: result['paired'][f'{a}_versus_{ref}']=train.paired_improvements(main[ref],main[a],target,ids)
    for i in (1,2,3): result['same_hyperparameter_paired'][str(i)]={f'{a}_versus_{ref}':train.paired_improvements(predictions[f'{ref}:{i}'],predictions[f'{a}:{i}'],target,ids) for ref,a in stage.PAIRS}
    for bi,planned in enumerate(stage.BLOCKS,1):
        mask=np.isin(ids,planned); ix=np.flatnonzero(mask)
        block={'planned_episode_ids':planned,'eligible_episode_ids':sorted(int(i) for i in set(ids[mask])),'rows':len(ix),'episodes':len(set(ids[mask])),'interpretation':'Chronology sensitivity, not known physical tip regimes'}
        if len(ix):
            rr=[records[i] for i in ix]; ll=[labels[i] for i in ix]
            block['metrics']={a:train.metric_summary(p[mask],target[mask],ids[mask],rr,ll) for a,p in main.items()}
            block['paired']={f'{a}_versus_{ref}':train.paired_improvements(main[ref][mask],main[a][mask],target[mask],ids[mask]) for ref,a in comparisons}
            block['same_hyperparameter_paired']={str(i):{f'{a}_versus_{ref}':train.paired_improvements(predictions[f'{ref}:{i}'][mask],predictions[f'{a}:{i}'][mask],target[mask],ids[mask]) for ref,a in stage.PAIRS} for i in (1,2,3)}
        else: block['status']='unavailable: no eligible episodes'
        result['chronology_blocks'][str(bi)]=block
    for arm,p in selected.items():
        q=fit['selected'][arm]['q']; maxima=train.per_episode(np.linalg.norm(p-target,axis=1),ids,np.max)
        result['empirical_residual_envelopes'][arm]={'q_nm':q,'mean_radius_nm':q,'fraction_episodes_every_residual_within_q':float(np.mean([v<=q for v in maxima.values()])),'episodes':len(maxima),'interpretation':'Empirical development-residual envelope; neither guaranteed confidence set nor conformal coverage'}
    result['classification']=classification(main,records,labels,ids,fit)
    primary=result['paired']['A+F_versus_A']; a=result['metrics']['A']['macro_endpoint_error']; full=result['metrics']['A+F']['macro_endpoint_error']
    relative=(a-full)/a if a>0 else None
    conditions={'relative_reduction_at_least_10_percent':relative is not None and relative>=.10,'absolute_reduction_at_least_0_02_nm':primary['mean']>=.02,'beats_both_baselines':all(full<result['metrics'][b]['macro_endpoint_error'] for b in ('persistence','command_request_endpoint')),'positive_improvement_in_each_fixed_block':all(b.get('paired',{}).get('A+F_versus_A',{}).get('mean',float('-inf'))>0 for b in result['chronology_blocks'].values()),'strict_episode_win_fraction_at_least_60_percent':primary['strict_win_fraction']>=.6,'at_least_two_same_hyperparameter_improvements':sum(v['A+F_versus_A']['mean']>0 for v in result['same_hyperparameter_paired'].values())>=2}
    result['screening']={'decision':'GO' if all(conditions.values()) else 'NO-GO','conditions':conditions,'primary_relative_reduction':relative,'F_beyond_C_lower_paired_macro_error':result['paired']['A+F_versus_A+C']['mean']>0,'meaning':'GO recommends only a larger independently held-out study with better metadata; no download, deployment, scanning change or scan-skipping authorization. No significance claim.'}
    result['limitations']=['Recorded-scan proxy and changed-byte selection may omit genuine scans; serialized freshness cannot establish physical freshness.', 'Observed selectively imaged Ag/Ag(111) subset; no counterfactual controller evaluation, proof of saved scans, physical safety guarantee or unique current-to-site inversion.', 'Unknown tip/session boundaries and chronological dependence prevent IID confidence or significance claims.', 'Radial d is not cumulative tip travel or atom displacement; archived traces lack per-sample time and full XY/Z trajectories.', 'Current gain calibration and instrument servo mode are unverified; exact image hashes cannot rule out near-duplicates.', 'Mode 0400 and separate entry points enforce a procedural seal, not OS-level isolation from the owner.']
    return result

def evaluate(lock,expected_lock,predictions,expected_predictions,output,approval):
    stage.require(approval=='ROOT_ONE_SHOT_EVALUATION_APPROVED','Separate root evaluation approval required')
    frozen,fit=stage.verify_lock(lock,expected_lock)
    stage.check_hash(predictions,expected_predictions)
    artifact=stage.read_json(predictions)
    stage.require(artifact['lock_sha256']==expected_lock,'Prediction lock mismatch')
    stage.require(artifact['fit_lock_sha256']==train.digest(Path(frozen['fitdir'])/'fit_lock.json'),'Prediction fit mismatch')
    records,routing=stage.inputs(frozen)
    stage.require(artifact['routing']==routing,'Prediction routing mismatch')
    # Marker lives beside the one sealed label file, independent of output path.
    sealed=Path(frozen['sanitized']).parent/'sealed'; labels_path=sealed/'test_labels.jsonl'
    stage.require(stat.S_IMODE(labels_path.stat().st_mode)==0o400,'Sealed labels must remain mode 0400')
    stage.require(not Path(output).exists(),'Result already exists')
    marker=sealed/'TEST_EVALUATION_STARTED.json'
    train.save_new(marker,{'status':'attempt consumed, including failures','lock_sha256':expected_lock,'prediction_sha256':expected_predictions,'output':str(Path(output).resolve())})
    # No exception path removes this exclusive marker.
    label_bytes=labels_path.read_bytes()
    labels=[json.loads(line) for line in label_bytes.splitlines() if line.strip()]
    result=report(artifact['predictions'],records,routing,labels,fit)
    stage.verify_lock(lock,expected_lock); stage.check_hash(predictions,expected_predictions)
    result['provenance']={'lock_sha256':expected_lock,'prediction_sha256':expected_predictions,'test_labels_sha256':hashlib.sha256(label_bytes).hexdigest(),'test_use':'single joint held-out evaluation; all outcomes now burned'}
    train.save_new(output,result)
    return train.digest(output)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for arg in ('lock','expected-lock','predictions','expected-predictions','output','approval'): p.add_argument('--'+arg,required=True)
    print(json.dumps({'result_sha256':evaluate(**vars(p.parse_args()))}))
