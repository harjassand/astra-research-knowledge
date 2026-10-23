"""Check the owner's necessary scalar entropy envelope from saved values only.
No thermochemistry, source fit, ODE or PDE is evaluated. The analytic all-population
statement follows from nonnegativity of discrete Shannon entropy.
"""
from pathlib import Path
import hashlib,json,math

BASE=Path(__file__).resolve().parents[2]
OWNER=BASE/'sources/dots/Astra_Amplification_Cycle4_DOTS_20261022'
MOMENT=OWNER/'nitrogen_cycle0001_20261022/state_contraction/moment_bounds.json'
MANIFEST=OWNER/'nitrogen_finite_cycle_20261021/thermo_helper/manifest.json'
d=json.loads(MOMENT.read_text())
R=json.loads(MANIFEST.read_text())['constants']['R_J_kmol_K']/1000
n=d['N2_mol_kgfresh'];initial=d['initial_entropy_J_kgfresh_K']
rows=[]
for row in d['rows']:
    for endpoint in ['min','max']:
        probs=[x['probability'] for x in row[endpoint+'_support']]
        H=-sum(p*math.log(p) for p in probs if p>0)
        base=row[endpoint+'_global_entropy_J_kgfresh_K']-n*R*H
        rows.append({'variant':row['variant'],'endpoint':endpoint,
                     'H_dimensionless':H,'baseS_J_kgfresh_K':base,
                     'baseS_minus_initial_J_kgfresh_K':base-initial})
assert max(x['baseS_J_kgfresh_K'] for x in rows)-min(x['baseS_J_kgfresh_K'] for x in rows)<1e-8
assert min(x['baseS_minus_initial_J_kgfresh_K'] for x in rows)>700
out={'scope':__doc__,'formula':'S(p)=baseS+n_N2*R*H(p), H(p)>=0',
     'source_hashes':{str(p.relative_to(OWNER)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [MOMENT,MANIFEST]},
     'R_J_mol_K':R,'N2_mol_kgfresh':n,'owner_bath_K':d['same_H_bath_T_K'],
     'mean_excitation_eV':d['mean_excitation_eV'],'initial_entropy_J_kgfresh_K':initial,
     'rows':rows,'conclusion':'Every normalized population at the same owner composition, bath and mean energy passes this necessary scalar entropy screen.',
     'limits':['Saved float arithmetic, not a new validated caloric solution.','No kinetic reachability, local entropy-production history or apparatus follows.','Other bath temperatures in the information experiment change enthalpy and are not covered by the same packet reset comparison.']}
(Path(__file__).parent/'ENTROPY_ENVELOPE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
