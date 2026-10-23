import json, math, hashlib
from pathlib import Path
from scipy.integrate import quad
root=Path(__file__).resolve().parent
# Path/source-binding correction only; numerical algorithm unchanged from preserved v1.
src=root/'inputs'/'input.json'
EXPECTED_ORIGINAL_SHA256='75de794a26ecaac2e8c4c938249bea1af08fa4fa7e563407962e9ecb58f10a34'
if hashlib.sha256(src.read_bytes()).hexdigest()!=EXPECTED_ORIGINAL_SHA256:
 raise RuntimeError('Pinned Cycle7 input SHA256 mismatch')
p=json.loads(src.read_text()); NA=float(p['Avogadro']); k=float(p['event_k_cm6_molecule2_s'])*1e-12*NA**2
c=float(p['pressure_Pa'])/(float(p['R_J_mol_K'])*float(p['T_K']))
F0=float(p['standard_flow_L_min'])/float(p['declared_standard_molar_volume_L_mol'])/60
rows=[]
for point in p['points']:
 a=float(point['initial_NO_fraction']); b=.21-a/2
 for target in ['99_percent_capture','100_ppm_after_complete_terminal_absorption']:
  Y=.99 if target=='99_percent_capture' else (a-1e-4)/(a*(1-1.75e-4))
  E=1.5*a*Y
  # Smooth transformation u=1/(1-Y).
  I,err=quad(lambda u:(1-1.75*a*(1-1/u))**3/(b-.75*a*(1-1/u)),1,1/(1-Y),epsabs=1e-10,epsrel=1e-12)
  V=3*F0/(4*k*c**3*a)*I
  stages={}
  for N in [256,1024,4096]:
   delta=E/N; total=0
   for j in range(N):
    e0=j*delta; s=e0
    assert a-(e0+delta)+s/3>0
    v,_=quad(lambda e:(1-e/2-2*s/3)**3/((a-e+s/3)**2*(b-e/2)),e0,e0+delta,epsabs=1e-9,epsrel=1e-10)
    total+=v
   stages[str(N)]=total*F0/(2*k*c**3)*1000
  g=E/3
  Ir,er=quad(lambda e:(1+g-e/2)**3/((a+g-e)**2*(b-e/2)),0,E,epsabs=1e-7,epsrel=1e-11)
  recycle_L=F0/(2*k*c**3)*Ir*1000
  rows.append(dict(selective_regenerated_NO_recycle_monomer_reaction_volume_L=recycle_L,configuration=point['configuration'],target=target,captured_fraction_Y=Y,cumulative_oxidation_extent_per_feed=E,oxygen_consumed_per_feed=E/2,regenerated_NO_per_feed=E/3,outlet_NO_ppm=1e6*a*(1-Y)/(1-1.75*a*Y),ideal_lower_bound_reaction_volume_L=V*1000,finite_stage_monomer_reaction_volume_L=stages,quad_error_integral_estimate=err,captured_N_mol_s=F0*a*Y))
result={'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'F0_mol_s':F0,'event_k_m6_mol2_s':k,'concentration_mol_m3':c,'method':'Analytic proof in DERIVATION.md; SciPy quadrature values are numerical checks, not certified rational enclosures. Monomer finite stages are feasible in the stipulated model only.','rows':rows}
(root/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
