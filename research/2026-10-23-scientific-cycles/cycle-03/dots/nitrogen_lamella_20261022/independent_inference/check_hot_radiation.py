"""Read-only NO catalogue temperature-cap correction, not an all-gas bound.
1700 K is not an upper bound on the pre-threshold 2700 K inlet history.
This only repeats the parent model inequality at a genuinely encompassing cap.
"""
from pathlib import Path
import gzip,json,math,hashlib
D=Path(__file__).resolve().parent;P=D.parent/'radiation';src=P/'s_14n16o.dat.gz'
h,c,kb,NA=6.62607015e-34,299792458.,1.380649e-23,6.02214076e23
inventory=1.01*1.9050984107423;rows=[]
for line in gzip.open(src,'rt'):
 t=line.split();rows.append((float(t[1]),int(t[2]),math.inf if t[4]=='---' else float(t[4])))
gamma=max(1/tau for _,_,tau in rows);result=[]
for T in [1700.,2700.]:
 weights=[g*math.exp(-h*c*100*e/(kb*T)) for e,g,_ in rows];U=NA*sum(w*h*c*100*e for w,(e,_,_) in zip(weights,rows))/sum(weights)
 bound=gamma*U*inventory*110e-6
 result.append({'temperature_cap_K':T,'catalogue_U_J_mol':U,'gamma_max_s_inv':gamma,'NO_only_finite_model_envelope_J_kg_fresh_for_110us':bound,'ratio_of_53995_J_to_envelope':53995./bound})
res={'scope':__doc__,'rows':result,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'limitations':['Same unresolved catalogue lifetime-assignment integrity and excluded transitions as parent radiation report.','Constant 1.01 packet NOx cap and LTE populations throughout are imposed, not validated for vibrationally nonequilibrium gas.','The endpoint energy theorem does not impose a 110 microsecond deadline.','NO2, N2/O2, atomic and other channels remain unbounded; no all-gas exclusion.']}
(D/'hot_radiation_check.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
