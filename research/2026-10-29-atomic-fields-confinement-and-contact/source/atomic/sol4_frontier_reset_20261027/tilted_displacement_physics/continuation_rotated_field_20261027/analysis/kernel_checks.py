from pathlib import Path
import json,numpy as np
from scipy.stats import ncx2
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'outputs/oblique_768_analytic_finite_dz1.json').read_text());z=np.load(ROOT/'outputs/oblique_768_analytic_finite_dz1_fields.npz');xy=z['positions'][:,:2]-np.array(d['target_position_A'][:2]);r2=np.sum(xy*xy,axis=1);cr=z['numbers']==24;ti=d['target_index'];sigma=.8/np.sqrt(8*np.log(2));rows=[]
for R in [0,.05,.1,.2,.4]:
 I=np.exp(-r2/(2*sigma*sigma))/(2*np.pi*sigma*sigma) if R==0 else ncx2.cdf((R/sigma)**2,2,r2/sigma**2)/(np.pi*R*R)
 rows.append(dict(kernel_radius_A=R,fraction=float(I[ti]/I[cr].sum()),target_density=float(I[ti]),species_sums={s:float(I[z['numbers']==num].sum()) for s,num in [('Cr',24),('S',16),('Br',35)]}))
(ROOT/'outputs/matched_ray_kernel_checks.json').write_text(json.dumps(rows,indent=2))
