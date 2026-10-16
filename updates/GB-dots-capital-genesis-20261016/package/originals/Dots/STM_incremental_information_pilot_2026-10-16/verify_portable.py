"""Portable independent arithmetic replay on SAME released records; no model execution.
Requires Python 3 and NumPy. Run: python verify_portable.py --output /tmp/check.json
Manifest file hashes detect discrepancies, not malicious replacement of this script
and manifest together. Production lock/prediction/result digests are pinned below.
"""
import argparse
import json, hashlib, math
from pathlib import Path, PurePosixPath
import numpy as np

ROOT = Path(__file__).resolve().parent
B = ROOT / 'stm_prediction_run'
ORIGINAL_B = Path('/workspace/shared/stm_prediction_run')
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', required=True, type=Path)
args = parser.parse_args()
OUTPUT = args.output.resolve()
if OUTPUT == ROOT or ROOT in OUTPUT.parents:
    raise ValueError('Output must be outside the immutable extracted bundle')
if OUTPUT.exists():
    raise FileExistsError('Refusing to overwrite output: ' + str(OUTPUT))

def require(condition, message):
    if not bool(condition):
        raise ValueError('Verification discrepancy: ' + message)

def relative_path(value):
    require(isinstance(value, str), 'manifest path must be a string')
    p = PurePosixPath(value)
    require(bool(value) and not p.is_absolute() and '..' not in p.parts
            and str(p) == value, 'unsafe/noncanonical bundle path: ' + value)
    target = ROOT.joinpath(*p.parts)
    require(ROOT in target.resolve().parents, 'path escapes bundle: ' + value)
    require(not any(x.is_symlink() for x in [target, *target.parents] if x != ROOT),
            'symlinks are forbidden: ' + value)
    return target

def raw_digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

MANIFEST = json.loads((ROOT / 'portable_manifest.json').read_text())
require(MANIFEST.get('schema_version') == 1, 'manifest schema_version must be 1')
FILES = MANIFEST['files']
PATH_MAP = MANIFEST['original_path_map']
require(isinstance(FILES, dict) and isinstance(PATH_MAP, dict), 'invalid manifest maps')
require('portable_manifest.json' not in FILES, 'manifest cannot hash itself')
require('verify_portable.py' in FILES, 'manifest must include verifier')
for name, record in FILES.items():
    p = relative_path(name)
    require(p.is_file(), 'missing bundled file: ' + name)
    require(p.stat().st_size == record['size'], 'size mismatch: ' + name)
    require(raw_digest(p) == record['sha256'], 'SHA-256 mismatch: ' + name)
actual = set()
for p in ROOT.rglob('*'):
    require(not p.is_symlink(), 'symlink in bundle: ' + str(p))
    if p.is_file() and p != ROOT / 'portable_manifest.json':
        actual.add(p.relative_to(ROOT).as_posix())
require(actual == set(FILES), 'manifest does not enumerate all and only bundled files: '
        + repr(sorted(actual.symmetric_difference(FILES))))
for original, relative in PATH_MAP.items():
    require(original.startswith('/workspace/shared/'), 'unexpected original path: ' + original)
    require(relative == original[len('/workspace/shared/'):],
            'original path mapping changes artifact identity: ' + original)
    require(relative in FILES, 'original path maps to unlisted file: ' + original)
OMISSIONS = {}
for record in MANIFEST['intentional_omissions']:
    original = record['original_path']
    require(original not in OMISSIONS and original not in PATH_MAP, 'duplicate/present omission: ' + original)
    require(original.startswith('/workspace/shared/'), 'invalid omitted original path')
    relative = original[len('/workspace/shared/'):]
    require(relative not in FILES and not relative_path(relative).exists(), 'omitted file is present: ' + original)
    require(isinstance(record.get('reason'), str) and bool(record['reason'].strip()), 'omission requires reason')
    require(isinstance(record.get('size'), int) and record['size'] >= 0, 'omission requires size')
    require(isinstance(record.get('sha256'), str) and len(record['sha256']) == 64
            and all(c in '0123456789abcdef' for c in record['sha256']), 'omission requires sha256')
    OMISSIONS[original] = record

def resolve(p):
    p = Path(p)
    resolved = p.resolve()
    if ROOT in resolved.parents:
        require(resolved.relative_to(ROOT).as_posix() in FILES,
                'dependency is not manifest verified: ' + str(p))
        return resolved
    if str(p).startswith('/workspace/shared/'):
        require(str(p) in PATH_MAP, 'missing unexpected original dependency: ' + str(p))
        return relative_path(PATH_MAP[str(p)])
    raise ValueError('Verification discrepancy: dependency outside bundle: ' + str(p))

checks = 0
def equal(a, b):
    global checks
    checks += 1
    if isinstance(a, (float, np.floating)) or isinstance(b, (float, np.floating)):
        require(math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12), repr((a, b)))
    else:
        require(a == b, repr((a, b)))
def digest(p): return raw_digest(resolve(p))
def read(p): return json.loads(resolve(p).read_text())
def rows(p): return [json.loads(x) for x in resolve(p).read_text().splitlines() if x.strip()]
EXPECTED={'heldout_lock.json':'3b87badab6afb6c954dd47fb239f911b68c3b64e58b1cde55333ab984ea6a936','test_predictions.json':'7563650baeb98d1f38729391ff4bc1daee9eea2b513c3ba1b003036137bf5f20','test_result_once.json':'9996114c744bf58c1fa68c0d3e227c4e7e943b7fa77483b82caf4de5382a16e2'}
for n,h in EXPECTED.items():equal(digest(B/n),h)
lock=read(B/'heldout_lock.json');pred=read(B/'test_predictions.json');result=read(B/'test_result_once.json');fit=read(B/'fits/fit_lock.json')
missing_models = []
model_originals = {str(ORIGINAL_B/'fits'/n): h for n,h in fit['model_hashes'].items()}
require(len(model_originals) == 9, 'expected nine original numeric model snapshots')
for p,h in lock['hashes'].items():
 if p in OMISSIONS:
  require(p in model_originals, 'locked non-model dependency cannot be omitted: ' + p)
  require(OMISSIONS[p]['sha256'] == h == model_originals[p], 'omitted model hash declarations disagree: ' + p)
  missing_models.append({'original_path':p, 'expected_sha256':h, 'status':'NOT VERIFIED: bytes intentionally omitted', 'reason':OMISSIONS[p]['reason']})
 else:equal(digest(p),h)
require(set(model_originals).issubset(lock['hashes']), 'model absent from original lock')
equal(digest(B/'fits/fit_lock.json'),read(B/'fits/fit_lock.sha256.json')['sha256'])
for n,h in fit['model_hashes'].items():
 if str(ORIGINAL_B/'fits'/n) not in OMISSIONS:equal(digest(B/'fits'/n),h)
for n,h in fit['input_hashes'].items():equal(digest(B/'sanitized'/n),h)
equal(pred['lock_sha256'],EXPECTED['heldout_lock.json']);equal(pred['fit_lock_sha256'],digest(B/'fits/fit_lock.json'))
seal=read(lock['label_seal']['artifact_path']);equal(digest(lock['label_seal']['artifact_path']),lock['label_seal']['artifact_sha256'])
lh=digest(B/'sealed/test_labels.jsonl');equal(lh,lock['label_seal']['expected_label_sha256']);equal(lh,seal['label_sha256']);equal(lh,result['provenance']['test_labels_sha256'])
equal(result['provenance']['lock_sha256'],EXPECTED['heldout_lock.json']);equal(result['provenance']['prediction_sha256'],EXPECTED['test_predictions.json'])
marker=read(B/'sealed/TEST_EVALUATION_STARTED.json');equal(marker['lock_sha256'],EXPECTED['heldout_lock.json']);equal(marker['prediction_sha256'],EXPECTED['test_predictions.json']);equal(marker['output'],str(ORIGINAL_B/'test_result_once.json'))
pm=read(B/'fits/TEST_PREDICTION_STARTED.json');equal(pm['lock_sha256'],EXPECTED['heldout_lock.json']);equal(pm['output'],str(ORIGINAL_B/'test_predictions.json'))
labels=rows(B/'sealed/test_labels.jsonl');routing=rows(B/'sanitized/test_routing.jsonl');inputs=rows(B/'sanitized/test_inputs.jsonl');equal(pred['routing'],routing)
ids=np.array([x['episode_id'] for x in routing]);unique=np.unique(ids);Y=np.asarray([x['delta'] for x in labels]);R=np.array([x['r'] for x in labels]);goal=np.array([x['g_minus_p'] for x in inputs]);y=np.array([x['y'] for x in labels]);dis=np.array([x['disagreement'] for x in labels]);threshold=.288*np.sqrt(3)/3
require(np.allclose(np.linalg.norm(Y-goal,axis=1),R,rtol=0,atol=1e-9), 'label radius identity');require(np.array_equal(y,R<threshold), 'label threshold identity')
equal(len(ids),100);equal(len(unique),60);equal(result['counts'],{'rows':100,'episodes':60})
allp={k:np.asarray(v) for k,v in pred['predictions'].items()};arms=('A','A+C','A+F');main={a:allp[f'{a}:{fit["selected"][a]["candidate"]}'] for a in arms};main.update({b:allp[b] for b in ('persistence','command_request_endpoint')})
require(np.array_equal(main['persistence'],np.zeros((100,2))), 'persistence identity');require(np.array_equal(main['command_request_endpoint'],np.array([x['history'][-1]['end_nm'] for x in inputs])), 'command endpoint identity')
def ep(values,idx=ids):return {str(i):float(np.mean(values[idx==i])) for i in np.unique(idx)}
def compare_metric(p,reported,mask=None):
 mask=np.ones(len(ids),dtype=bool) if mask is None else mask
 idx=ids[mask];err=np.sqrt(np.sum((p[mask]-Y[mask])**2,axis=1));episode=ep(err,idx);mse=np.mean(list(ep(err**2,idx).values()))
 vals={'rows':len(err),'episodes':len(set(idx)),'macro_endpoint_error':np.mean(list(episode.values())),'macro_squared_euclidean_error':mse,'root_macro_squared_euclidean_error':np.sqrt(mse),'pooled_median_endpoint_error':np.quantile(err,.5,method='linear'),'pooled_p90_endpoint_error':np.quantile(err,.9,method='linear'),'macro_absolute_target_radius_error':np.mean(list(ep(np.abs(np.linalg.norm(p[mask]-goal[mask],axis=1)-R[mask]),idx).values()))}
 for k,v in vals.items():equal(v,reported[k])
 for k,v in episode.items():equal(v,reported['per_episode_endpoint_error'][k])
 return vals
for name,p in main.items():
 compare_metric(p,result['metrics'][name])
 for label,mask in [('at_or_below_threshold',dis<=threshold),('above_threshold',dis>threshold)]:
  rr=result['metrics'][name]['label_quality']['strata'][label]
  if mask.any():compare_metric(p,rr,mask)
  else:equal(rr,{'rows':0,'episodes':0})
def compare_pair(ref,p,reported,mask=None):
 mask=np.ones(len(ids),dtype=bool) if mask is None else mask;idx=ids[mask]
 a=ep(np.linalg.norm(ref[mask]-Y[mask],axis=1),idx);b=ep(np.linalg.norm(p[mask]-Y[mask],axis=1),idx);d=np.array([a[k]-b[k] for k in a])
 for k,v in {'mean':d.mean(),'median':np.median(d),'min':d.min(),'max':d.max(),'strict_win_fraction':np.mean(d>0),'episodes':len(d)}.items():equal(v,reported[k])
 for k,v in zip(a,d):equal(v,reported['per_episode'][k])
 return d
pairs=[('A','A+C'),('A','A+F'),('A+C','A+F')]+[(b,a) for b in ('persistence','command_request_endpoint') for a in arms]
for ref,a in pairs:compare_pair(main[ref],main[a],result['paired'][f'{a}_versus_{ref}'])
paired_hp=[]
for i in (1,2,3):
 for ref,a in pairs[:3]:
  ds=compare_pair(allp[f'{ref}:{i}'],allp[f'{a}:{i}'],result['same_hyperparameter_paired'][str(i)][f'{a}_versus_{ref}'])
  if (ref,a)==('A','A+F'):paired_hp.append(float(ds.mean()))
block_d=[]
for bi,start in enumerate((2201,2401,2601),1):
 planned=list(range(start,start+200,10));mask=np.isin(ids,planned);br=result['chronology_blocks'][str(bi)];equal(br['planned_episode_ids'],planned)
 equal(br['eligible_episode_ids'],sorted(set(ids[mask])));equal(br['rows'],int(mask.sum()));equal(br['episodes'],len(set(ids[mask])))
 for a,p in main.items():compare_metric(p,br['metrics'][a],mask)
 for ref,a in pairs:
  d=compare_pair(main[ref],main[a],br['paired'][f'{a}_versus_{ref}'],mask)
  if (ref,a)==('A','A+F'):block_d.append(float(d.mean()))
 for i in (1,2,3):
  for ref,a in pairs[:3]:compare_pair(allp[f'{ref}:{i}'],allp[f'{a}:{i}'],br['same_hyperparameter_paired'][str(i)][f'{a}_versus_{ref}'],mask)
primary=compare_pair(main['A'],main['A+F'],result['paired']['A+F_versus_A']);wins=int((primary>0).sum());equal(wins,27)
macro={a:float(np.mean(list(ep(np.linalg.norm(p-Y,axis=1)).values()))) for a,p in main.items()};relative=(macro['A']-macro['A+F'])/macro['A']
conditions={'relative_reduction_at_least_10_percent':relative>=.1,'absolute_reduction_at_least_0_02_nm':primary.mean()>=.02,'beats_both_baselines':all(macro['A+F']<macro[b] for b in ('persistence','command_request_endpoint')),'positive_improvement_in_each_fixed_block':all(x>0 for x in block_d),'strict_episode_win_fraction_at_least_60_percent':wins/len(unique)>=.6,'at_least_two_same_hyperparameter_improvements':sum(x>0 for x in paired_hp)>=2}
for k,v in conditions.items():equal(bool(v),result['screening']['conditions'][k])
equal('GO' if all(conditions.values()) else 'NO-GO',result['screening']['decision']);equal(relative,result['screening']['primary_relative_reduction']);equal(macro['A+F']<macro['A+C'],result['screening']['F_beyond_C_lower_paired_macro_error'])
support={}
for split in ('train','development','test'):
 ll=labels if split=='test' else rows(B/f'sanitized/{split}_labels.jsonl');ii=ids if split=='test' else np.array([r['episode_id'] for r in rows(B/f'sanitized/{split}_routing.jsonl')]);yy=np.array([r['y'] for r in ll]);support[split]={str(v):{'rows':int((yy==v).sum()),'episodes':len(set(ii[yy==v]))} for v in (0,1)}
 equal(support[split],result['classification']['support'][split]['counts'])
available=all(c['rows']>=(15 if s=='test' else 20) and c['episodes']>=10 for s,counts in support.items() for c in counts.values());equal(available,result['classification']['available'])
confusion={}
for a,p in main.items():
 yh=np.linalg.norm(p-goal,axis=1)<threshold;tp=int(np.sum(yh&(y==1)));tn=int(np.sum(~yh&(y==0)));fp=int(np.sum(yh&(y==0)));fn=int(np.sum(~yh&(y==1)));sens=tp/(tp+fn);spec=tn/(tn+fp)
 vals={'tp':tp,'tn':tn,'fp':fp,'fn':fn,'sensitivity':sens,'specificity':spec,'balanced_accuracy':(sens+spec)/2,'precision':tp/(tp+fp) if tp+fp else None};confusion[a]=vals
 for k,v in vals.items():equal(v,result['classification']['metrics'][a][k])
envelopes={}
for a in arms:
 q=fit['selected'][a]['q'];err=np.linalg.norm(main[a]-Y,axis=1);covered=sum(np.max(err[ids==i])<=q for i in unique);rr=result['empirical_residual_envelopes'][a]
 equal(q,rr['q_nm']);equal(q,rr['mean_radius_nm']);equal(covered/len(unique),rr['fraction_episodes_every_residual_within_q']);equal(len(unique),rr['episodes']);envelopes[a]={'locked_q_nm':q,'covered_episodes':int(covered),'episodes':len(unique),'fraction':covered/len(unique)}
output={'status':'PASS','interpretation':'Independent arithmetic reconstruction on the SAME released held-out records; not new experimental validation','checks':checks,'hash_bindings':'PASS for included bytes only; omitted model bytes NOT VERIFIED', 'bundled_files_verified':len(FILES), 'omitted_models_not_verified':missing_models, 'intentional_omissions':MANIFEST['intentional_omissions'], 'replay_scope':'Arithmetic only on SAME released predictions and labels; no refitting, model execution, stage execution, new downloads, or new validation','rows':100,'episodes':60,'macro_endpoint_error_nm':macro,'primary_A_F_vs_A':{'mean_improvement_nm':float(primary.mean()),'relative_reduction':relative,'strict_wins':wins,'episodes':60,'chronological_block_mean_improvements_nm':block_d,'same_hyperparameter_mean_improvements_nm':paired_hp},'screening':{k:bool(v) for k,v in conditions.items()},'decision':'NO-GO','classification_support':support,'classification':confusion,'empirical_residual_envelopes':envelopes}
with OUTPUT.open('x') as f:json.dump(output,f,indent=2);f.write('\n')
print(json.dumps(output,indent=2))
