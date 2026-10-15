import json,csv
from pathlib import Path
import numpy as np
from benchmark import OUT
r=json.load(open(OUT/'results.json'));d=json.load(open(OUT/'diagnostics.json')); selected=[x for x in r if x['selected_by_training_loss']]
with (OUT/'selected_results.csv').open('w') as f:
 fields=['m','seed','noise_raw_sd','design','calibration_settings','repeats','calibration_readings','restart','train_measured_rmse','heldout_rmse','heldout_max_abs','all_table_rmse','all_table_max_abs','exact_predictive_success','runtime_all_starts_seconds'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for x in selected:
  z={k:x[k] for k in fields if k in x};z.update(heldout_rmse=x['heldout']['rmse'],heldout_max_abs=x['heldout']['max_abs'],all_table_rmse=x['all_table']['rmse'],all_table_max_abs=x['all_table']['max_abs'],runtime_all_starts_seconds=sum(y['runtime_seconds'] for y in r if all(y[k]==x[k] for k in ['m','seed','noise_raw_sd','design'])));w.writerow(z)
with (OUT/'all_table_selected_errors.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['instance','subset_integer_bitmask','in_calibration','truth','prediction','signed_error'])
 for path in sorted(OUT.glob('m*.npz')):
  data=np.load(path);tag=path.stem; row=next(x for x in selected if tag==f'm{x["m"]}_seed{x["seed"]}_noise{x["noise_raw_sd"]:g}_{x["design"]}');k=row['restart'];train=set(data['train'])
  for j in range(len(data['truth'])):w.writerow([tag,j,j in train,data['truth'][j],data['predictions'][k,j],data['errors'][k,j]])
print('truth condition range',min(x['true_full_condition'] for x in r),max(x['true_full_condition'] for x in r))
print('dual parameter distances',min(x['dual_parameter_difference'] for x in d),max(x['dual_parameter_difference'] for x in d))
print('counts',[(m,next(x['calibration_settings'] for x in r if x['m']==m),2**m) for m in range(5,11)])
print('selected successful parameter error',[(x['m'],x['seed'],x['design'],x['parameter_frobenius_error']) for x in selected if x['exact_predictive_success']][:12])
