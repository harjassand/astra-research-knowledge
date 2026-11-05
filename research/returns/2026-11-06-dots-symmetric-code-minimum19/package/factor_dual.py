import json,numpy as np,sys,hashlib
from pathlib import Path
r=Path(__file__).resolve().parent
src=r/'certificate_n18_candidate.json'
if not src.exists():src=r/'certificate_n18_raw_duals.json'
x=json.loads(src.read_text())
from fractions import Fraction
x['n']=18;x['d']=5
x['constant_exact']=str(-Fraction(float(x['linear_duals'][1]))-Fraction(19,2)*Fraction(float(x['linear_duals'][2])))
factors=[];errors=[]
for Z in x['psd_duals']:
 Z=np.array(Z);L=np.linalg.cholesky(Z);factors.append(L.tolist());errors.append(float(np.max(np.abs(L@L.T-Z))))
x['psd_cholesky_factors']=factors
x['factor_interpretation']='Treat each listed binary64 factor entry as its exact dyadic value, and define each PSD dual matrix as L L^T using exact multiplication. psd_duals are diagnostic floating matrices only.'
x['max_float_factor_reconstruction_error']=max(errors)
out=r/'certificate_n18_factored.json';out.write_text(json.dumps(x,indent=2))
print(out,'factor blocks',len(factors),'max_float_reconstruction_error',max(errors),'sha256',hashlib.sha256(out.read_bytes()).hexdigest())
