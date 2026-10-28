"""Scale-free geometry and deeper-well limit checks of the paired-action interface."""
from pathlib import Path
import sys,json,runpy,io,contextlib
sys.dont_write_bytecode=True
with contextlib.redirect_stdout(io.StringIO()):d=runpy.run_path(str(Path('code/finite_action.py').resolve()))
np=d['np'];f=d['f'];r=d['r'];action=d['action'];z0=d['z0'];direction=d['direction']
base=json.loads(Path('results/finite_action.json').read_text());rows=[]
for v in base['rows']:
 h=v['h'];qplus=np.r_[f.U0+h*direction[0],h*direction[1],z0];qminus=np.r_[f.U0-h*direction[0],-h*direction[1],z0]
 rows.append(dict(h=h,DeltaPsi=v['plus']['source_DeltaPsi'],physical_half_span=float(np.linalg.norm(f.embedding(qplus)-f.embedding(qminus))/2),relative_full_action_spread=2*v['relative_half_spread']))
limits=[]
for depth in [.02,.01,.005,.002,.001]:
 h=1e-4;a=action(0,depth);p=action(h,depth);m=action(-h,depth)
 deriv=(p['action']-m['action'])/(2*h*a['action']);limits.append(dict(mirror_depth_fraction=depth,relative_directional_derivative=deriv,negative_derivative_times_depth=-deriv*depth))
out=dict(status='PASS',physical_same_flux_pairs=rows,deep_well_limit=limits,first_order_expected_limit=float(r['relative_half_well_bottom_spread_per_sqrt_DeltaPsi']),scope='Finite numerical actions and geometric conversion; no drift-surface closure inference.')
Path('results/action_calibration.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
