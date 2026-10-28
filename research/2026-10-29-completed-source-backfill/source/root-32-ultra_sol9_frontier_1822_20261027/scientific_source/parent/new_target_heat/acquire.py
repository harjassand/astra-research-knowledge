"""Bounded matched heat-dissipation acquisition on the genuinely new target."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import sys,json,time,hashlib
import numpy as np

OUT=Path(__file__).resolve().parent
SOURCE=OUT.parents[2]/'sol8_opportunity_selection_20261027/quartic_alternative/combined_full_cone'
assert (SOURCE/'MAPS.npz').exists() # Never regenerate or mutate frozen maps.
sys.path.insert(0,str(SOURCE))
from models import Primal
from maps import load

d=load();model=Primal(d,'heat')
jobs=[('ordinary_norm4',[1,1,2,0,0,0,0,0,0]),
      ('ordinary_DM',[1,1,2,0,0,0,-2.2,-2.2,0]),
      ('new_even_hopf',[1,1,2+252/25,-252/25,0,0,99/25,-99/25,0])]
results=[]
for name,p in jobs:
    result=model.solve(p)
    result['name']=name;results.append(result)
    if model.rho.value is not None:
        np.savez(OUT/(name+'.npz'),**{k:v.value for k,v in model.variables.items()},
                 equality_dual=model.eq[0].dual_value,rho=model.rho.value,p=np.asarray(p))
    print(json.dumps(result),flush=True)
(OUT/'ACQUISITION.json').write_text(json.dumps({'scope':'Numerical acquisition only. No QC or failure theorem before exact reconstruction.','map_sha256':hashlib.sha256((SOURCE/'MAPS.npz').read_bytes()).hexdigest(),'results':results},indent=2)+'\n')
