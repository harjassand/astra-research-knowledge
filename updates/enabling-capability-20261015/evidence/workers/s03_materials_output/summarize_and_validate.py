from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.io import loadmat

B=Path(__file__).resolve().parent
R=B/'results_v2'
source=loadmat(B/'data/FeCoNi_benchmark_dataset_220501a.mat')
runs=json.loads((R/'ACQUISITION_RUNS.json').read_text())
pred=json.loads((R/'PREDICTION_RUNS.json').read_text())
checks=[]
for r in runs:
    ix=np.array(r['indices_0based']);y=source[r['output']].ravel()
    assert len(ix)==80 and len(np.unique(ix))==80 and ix.min()>=0 and ix.max()<921
    assert np.array_equal(y[ix],r['observed_values'])
    assert np.array_equal(np.maximum.accumulate(y[ix]),r['best_values'])
    assert np.allclose(y.max()-np.maximum.accumulate(y[ix]),r['regret'],rtol=0,atol=1e-15)
    for level,count in r['first_hit'].items():
        hits=np.flatnonzero(np.maximum.accumulate(y[ix])>=float(level)*y.max())
        assert count==(int(hits[0])+1 if len(hits) else None)
for output in ['Coer','Kerr']:
    for seed in range(12):
        rs=[r for r in runs if r['output']==output and r['seed']==seed]
        assert len(rs)==5
        assert all(r['indices_0based'][:8]==rs[0]['indices_0based'][:8] for r in rs)
for r in pred:
    train=np.array(r['train_indices_0based']);test=np.array(r['test_indices_0based'])
    assert len(train)==128 and not len(np.intersect1d(train,test))
    truth=source[r['output']].ravel()[test]
    assert np.array_equal(truth,r['source_observations'])
    assert abs(np.sqrt(np.mean((np.array(r['predictions'])-truth)**2))-r['rmse'])<1e-12
checks += ['all 120 trajectories select 80 distinct source rows',
           'every observed value and target regret recomputed from acquired MATLAB data',
           'paired arms have identical first 8 observations',
           'all prediction train/test row sets are disjoint',
           'prediction errors recomputed from source labels',
           'no target labels are used to produce PCA or spectrum partitions by code inspection',
           'corrected random arm preserves random continuation order by code inspection']

paired=[]
for output in ['Coer','Kerr']:
    rs={a:sorted([r for r in runs if r['output']==output and r['arm']==a],key=lambda x:x['seed'])
        for a in ['composition','continuous_spectra','partition','equally_informed_union']}
    baseline=np.array([r['first_hit']['0.95'] or 81 for r in rs['composition']])
    for arm,rows in rs.items():
        times=np.array([r['first_hit']['0.95'] or 81 for r in rows]);diff=baseline-times
        rng=np.random.default_rng(445566)
        boot=np.mean(rng.choice(diff,(10000,len(diff)),replace=True),axis=1)
        complete=all(r['first_hit']['0.95'] is not None for r in rows) and all(r['first_hit']['0.95'] is not None for r in rs['composition'])
        paired.append({'output':output,'arm':arm,'n_paired_seeds':12,
                       'all_95percent_hits_observed':complete,
                       'mean_95percent_hit_time_or_censored81':float(times.mean()),
                       'mean_saved_vs_composition':float(diff.mean()),
                       'paired_seed_bootstrap_95_descriptive_interval':np.quantile(boot,[.025,.975]).tolist(),
                       'wins_ties_losses':[int(sum(diff>0)),int(sum(diff==0)),int(sum(diff<0))],
                       'XRD_to_magnetic_cost_ratio_break_even_if_all_hits_observed':float(diff.mean()/921) if complete else None,
                       'qualification':'Seed bootstrap conditional on this one library. It excludes measurement uncertainty, new processes, kernel-family selection and generalization to other systems.'})

gate=json.loads((B/'IDENTIFICATION_GATES.json').read_text())
assert gate['kerr_gain_countermodel']['model_A_target_max_row_1based']!=gate['kerr_gain_countermodel']['model_B_target_max_row_1based']
assert gate['coercivity_top_two_rows_1based']==[65,211]

out={'status':'PASS_REPLAY_INTEGRITY_ONLY','checks':checks,'paired_actual_data_comparisons':paired,
     'scope':'integrity and stated finite calculations; not physical calibration, external validation, novelty or practical advantage',
     'current_script_sha256':hashlib.sha256((B/'actual_data_diagnostic.py').read_bytes()).hexdigest(),
     'used_results':'results_v2; initial random-arm results excluded by CORRECTION_v0001.txt'}
(B/'VALIDATION_AND_COST_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
