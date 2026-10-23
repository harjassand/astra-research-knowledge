"""Saved-data arithmetic only; no thermo packages, kinetic integration or network."""
from pathlib import Path
import json, hashlib
from decimal import Decimal, getcontext
getcontext().prec=40
root=Path(__file__).resolve().parents[2]
src=root/'nitrogen_admissibility_20261022/recycle_quench/result.json'
data=json.loads(src.read_text(),parse_float=Decimal)
rows=[]
for x in data['rows']:
    h=x['hot_NOx_mol_kg']; n=x['once_through_product_NOx_mol_kg']; w=x['heater_positive_J_kg_fresh']
    recycle=x['net_product_NOx_mol_per_kg_fresh']
    row={'heater_K':x['heater_K'],'N_hot_mol_per_kg':h,'N_reference_mol_per_kg':n,'W_reference_J_per_kg':w,
         'reference_loss_mol_per_kg':h-n,'reference_retention_fraction':n/h,
         'maximum_SEC_reduction_fraction_relative_to_reference':1-n/h,
         'maximum_SEC_reduction_percent_relative_to_reference':100*(1-n/h),
         'perfect_retention_SEC_J_per_mol':w/h,'reference_SEC_J_per_mol':w/n,
         'strict_win_overhead_ceiling_J_per_kg':w*(h/n-1),
         'strict_win_overhead_ceiling_fraction_of_W_reference':h/n-1,
         'saved_recycle_loss_mol_per_kg':h-recycle,
         'saved_recycle_SEC_penalty_fraction':n/recycle-1,
         'pump_example_1percent_pressure_rise_J_per_kg':x['ideal_isothermal_recycle_pump_J_kg_fresh_by_pressure_ratio_increment']['0.01'],
         'pump_example_10percent_pressure_rise_J_per_kg':x['ideal_isothermal_recycle_pump_J_kg_fresh_by_pressure_ratio_increment']['0.1']}
    assert n<=h and recycle<=h
    rows.append({k:str(v) for k,v in row.items()})
output={'scope':'Conditional saved-data arithmetic, not a physical competitor or numerical interval certificate.',
        'source_path':str(src.relative_to(root)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'rows':rows}
out=Path(__file__).parent/'arithmetic.json';out.write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
