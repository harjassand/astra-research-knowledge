"""Read-only extraction from published workbook through independently saved sheet JSON."""
import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
src=root/'peroxide_evidence/source_data_small_sheets.json'
d=json.loads(src.read_text())
out={'source_doi':'10.1038/s41467-025-60696-3','data_doi':'10.6084/m9.figshare.28210994','sheet_json_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'unit_interpretation':'SI workbook headers say micromolar, but SI Figure1 rendered axis is mM, caption gives .5mM nitrite/1mM peroxide, and main Figure1a shares identical nitrite entries in mM. mM interpretation adopted with explicit source header correction; raw workbook unchanged.','volume_mL_nominal':100,'peroxide_mM_nominal':1,'sampling_mL_scenarios':[0,1,2],'sampling_scope':'Sensitivity, not measured interval. Four equal pre-endpoint aliquots at listed times including t=0. No replacement; well mixed. Final sample may be partitioned without changing retained+sampled inventory.','arms':{}}
for name,key in [('H2O2','Supplementary Fig. 1a'),('tert_butyl_hydroperoxide','Supplementary Fig. 1b'),('cumene_hydroperoxide','Supplementary Fig. 1c'),('2_butanone_peroxide','Supplementary Fig. 1d')]:
 rows=[x for x in d[key] if x and isinstance(x[0],(int,float))]
 out['arms'][name]={'sheet':key,'columns':['time_min','nitrite_value','nitrate_value','inorganic_N_value','nitrite_SD','nitrate_SD','inorganic_N_SD'],'rows':rows}
out['blank_nitrite']=[r for r in d['Figure 1a'][34:] if r and isinstance(r[0],(float,int))]
(root/'calculations/inputs.json').write_text(json.dumps(out,indent=2)+'\n')
