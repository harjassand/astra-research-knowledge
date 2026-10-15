import json,csv
import numpy as np
from benchmark import OUT
D=OUT/'joint_raw_fit';r=json.load(open(D/'results.json'));selected=[x for x in r if x['selected_by_training_loss']]
with (D/'selected_results.csv').open('w') as f:
 fields=['m','seed','design','restart','calibration_settings','calibration_readings','train_raw_mean_rmse','heldout_rmse','heldout_max_abs','all_table_rmse','all_table_max_abs','optimizer_success','runtime_all_starts_seconds'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for x in selected:
  row={k:x[k] for k in fields if k in x};row.update(heldout_rmse=x['heldout']['rmse'],heldout_max_abs=x['heldout']['max_abs'],all_table_rmse=x['all_table']['rmse'],all_table_max_abs=x['all_table']['max_abs'],runtime_all_starts_seconds=sum(y['runtime_seconds'] for y in r if all(x[k]==y[k] for k in ['m','seed','design'])));w.writerow(row)
with (D/'all_table_selected_errors.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['instance','subset_integer_bitmask','in_calibration','truth','prediction','signed_error'])
 for x in selected:
  tag=f'm{x["m"]}_seed{x["seed"]}_noise0.001_{x["design"]}';z=np.load(D/(tag+'.npz'));train=set(z['train']);k=x['restart'];truth=z['truth'];pred=z['predictions'][k];err=z['errors'][k]
  for j in range(len(truth)):w.writerow([tag,j,j in train,truth[j],pred[j],err[j]])
