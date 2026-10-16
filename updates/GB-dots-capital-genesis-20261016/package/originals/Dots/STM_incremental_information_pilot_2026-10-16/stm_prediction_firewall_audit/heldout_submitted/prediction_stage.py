"""Root-authorized freeze/prediction stages. Never opens held-out outcomes.
Only numeric model snapshots and sanitized inputs/routing enter prediction.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import train
from features import feature_maps, schema, schema_hash

HERE=Path(__file__).resolve().parent
PAIRS=(('A','A+C'),('A','A+F'),('A+C','A+F'))
CODE=('features.py','train.py','audit.py','test_features_train.py','prediction_stage.py','evaluate_once.py','test_heldout_stages.py')
BLOCKS=[list(range(start,start+200,10)) for start in (2201,2401,2601)]

def require(condition,message):
    if not condition: raise ValueError(message)

def read_json(path): return json.loads(Path(path).read_text())
def read_jsonl(path): return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
def check_hash(path,expected): require(train.digest(path)==expected,f'Hash mismatch: {path}')
def models(): return {f'{a.replace("+","_")}_{i}.json' for a in train.ARMS for i in (1,2,3)}

def verify_fit(fitdir,sanitized,protocol,audit):
    fitdir=Path(fitdir); sanitized=Path(sanitized)
    fit=read_json(fitdir/'fit_lock.json')
    check_hash(fitdir/'fit_lock.json',read_json(fitdir/'fit_lock.sha256.json')['sha256'])
    check_hash(protocol,fit['protocol_sha256']); check_hash(audit,fit['audit_report_sha256'])
    require(read_json(audit)['status']=='PASS','Audit not PASS')
    check_hash(HERE/'audit.py',read_json(audit)['audit_code_sha256'])
    require(fit['versions']==train.versions(),'Version mismatch')
    require(fit['schema_hash']==schema_hash() and read_json(fitdir/'feature_schema.json')==schema(),'Schema mismatch')
    require(fit['candidate_parameters']==train.parameters(),'Candidate parameters changed')
    require(set(fit['model_hashes'])==models(),'Require all nine frozen models')
    for name,h in fit['model_hashes'].items(): check_hash(fitdir/name,h)
    require(set(fit['code_hashes'])=={'features.py','train.py','test_features_train.py'},'Fit code list')
    for name,h in fit['code_hashes'].items(): check_hash(HERE/name,h)
    expected={f'{s}_{k}.jsonl' for s in ('train','development') for k in ('inputs','routing','labels')}
    require(set(fit['input_hashes'])==expected,'Fit input list')
    for name,h in fit['input_hashes'].items(): check_hash(sanitized/name,h)
    require(set(fit['selected'])==set(train.ARMS),'Selection arms')
    for arm in train.ARMS:
        sel=fit['selected'][arm]; scores=[fit['development_candidates'][f'{arm}:{i}']['macro_endpoint_error'] for i in (1,2,3)]
        require(sel['candidate']==train.choose(scores)+1,'Selection changed')
        require(sel['model_file']==f'{arm.replace("+","_")}_{sel["candidate"]}.json','Selection file mismatch')
        require(np.isfinite(sel['q']) and sel['q']>=0,'Invalid locked envelope')
    return fit

def freeze(fitdir,sanitized,protocol,manifest,audit,lock,approval):
    require(approval=='ROOT_FREEZE_APPROVED','Root freeze approval required')
    fitdir=Path(fitdir).resolve(); sanitized=Path(sanitized).resolve()
    verify_fit(fitdir,sanitized,protocol,audit)
    planned=[r['episode_id'] for r in read_json(manifest)['splits']['test']['episodes']]
    require(planned==sum(BLOCKS,[]),'Unexpected planned test membership')
    files=[Path(protocol),Path(manifest),Path(audit),fitdir/'fit_lock.json',fitdir/'fit_lock.sha256.json',fitdir/'feature_schema.json']
    files += [HERE/n for n in CODE]+[fitdir/n for n in sorted(models())]
    files += [Path('/workspace/shared/stm_reader_audit/safe_reader.py')]
    files += [sanitized/f'{s}_{k}.jsonl' for s in ('train','development') for k in ('inputs','routing','labels')]
    files += [sanitized/'test_inputs.jsonl',sanitized/'test_routing.jsonl']
    frozen={'version':'heldout-v1','fitdir':str(fitdir),'sanitized':str(sanitized),'protocol':str(Path(protocol).resolve()),'manifest':str(Path(manifest).resolve()),'audit':str(Path(audit).resolve()),'planned_blocks':BLOCKS,'hashes':{str(p.resolve()):train.digest(p) for p in files},'schema_hash':schema_hash(),'reporting_caveat':train.CAVEAT}
    train.save_new(lock,frozen)
    return train.digest(lock)

def verify_lock(lock,expected):
    check_hash(lock,expected); frozen=read_json(lock)
    require(frozen['version']=='heldout-v1' and frozen['planned_blocks']==BLOCKS,'Invalid frozen design')
    for path,h in frozen['hashes'].items(): check_hash(path,h)
    fit=verify_fit(frozen['fitdir'],frozen['sanitized'],frozen['protocol'],frozen['audit'])
    require(frozen['schema_hash']==schema_hash(),'Feature schema changed')
    return frozen,fit

def inputs(frozen):
    base=Path(frozen['sanitized']); records=read_jsonl(base/'test_inputs.jsonl'); routing=read_jsonl(base/'test_routing.jsonl')
    require(bool(records) and len(records)==len(routing),'Unaligned test inputs')
    for row in records:
        require(set(row)=={'p','g_minus_p','prior_disagreement','history'},'Unsanitized predictor')
        for h in row['history']: require(set(h)=={'action','start_nm','end_nm','d','current'},'Unsanitized history')
    keys=[]
    for row in routing:
        require(set(row)=={'episode_id','transition_index'},'Unexpected routing fields')
        require(type(row['episode_id']) is int and type(row['transition_index']) is int and row['transition_index']>=0,'Invalid routing key')
        require(row['episode_id'] in sum(BLOCKS,[]),'Unplanned episode')
        keys.append((row['episode_id'],row['transition_index']))
    require(keys==sorted(set(keys)),'Duplicate or unsorted routing')
    counts=read_json(frozen['audit'])['counts']['test']
    require(len(records)==counts['eligible_boundaries'] and len({k[0] for k in keys})==counts['eligible_episodes'],'Audit count mismatch')
    return records,routing

def predict(lock,expected,output,approval):
    require(approval=='ROOT_PREDICTION_APPROVED','Root prediction approval required')
    frozen,fit=verify_lock(lock,expected)
    # Canonical marker prevents retry under an alternative output path.
    train.save_new(Path(frozen['fitdir'])/'TEST_PREDICTION_STARTED.json',{'lock_sha256':expected,'output':str(Path(output).resolve())})
    records,routing=inputs(frozen); maps=[feature_maps(r) for r in records]
    matrices={a:np.vstack([r[a] for r in maps]) for a in train.ARMS}
    predictions={}
    for arm in train.ARMS:
        for i in (1,2,3):
            filename=f'{arm.replace("+","_")}_{i}.json'
            p=train.predict_frozen(read_json(Path(frozen['fitdir'])/filename),matrices[arm])
            require(p.shape==(len(records),2) and np.isfinite(p).all(),'Invalid model prediction')
            predictions[f'{arm}:{i}']=p.tolist()
    predictions.update({name:p.tolist() for name,p in train.baseline_predictions(records).items()})
    artifact={'lock_sha256':expected,'fit_lock_sha256':train.digest(Path(frozen['fitdir'])/'fit_lock.json'),'routing':routing,'predictions':predictions,'reporting_caveat':train.CAVEAT}
    # Recheck every dependency before committing predictions.
    verify_lock(lock,expected)
    train.save_new(output,artifact)
    return train.digest(output)

if __name__=='__main__':
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='stage',required=True)
    f=sub.add_parser('freeze')
    for arg in ('fitdir','sanitized','protocol','manifest','audit','lock','approval'): f.add_argument('--'+arg,required=True)
    r=sub.add_parser('predict')
    for arg in ('lock','expected-lock-sha256','output','approval'): r.add_argument('--'+arg,required=True)
    a=vars(p.parse_args()); stage=a.pop('stage')
    if stage=='predict': a['expected']=a.pop('expected_lock_sha256')
    print(json.dumps({'sha256':(freeze(**a) if stage=='freeze' else predict(**a))}))
