"""Paired same-flux bounce actions for the source reference; no orbit ensemble.
Actual field lines and mirror events are integrated. Opposite offsets have
exactly the same source flux label because cd(x) is even. This is a finite
pitch action diagnostic, not a global confinement certificate.
"""
from pathlib import Path
import sys,importlib.util,json,time
sys.dont_write_bytecode=True
root=Path(__file__).parents[2]
sys.path.insert(0,str(root/'positive_current_operation/vendor'))
import numpy as np
from scipy.integrate import solve_ivp
spec=importlib.util.spec_from_file_location('frozen_reference',Path(__file__).parents[1]/'sources/worker_sengupta_paraboloid.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
r=json.loads(Path('results/reference_well.json').read_text())
z0=float(r['selected_min_zeta']);B0=float(r['B_min']);direction=np.array(list(map(float,r['maximizing_flux_normal_direction_du_dv'])))


def action(h,depth=.01,tol=1e-10):
 q0=np.array([f.U0+h*direction[0],h*direction[1],z0]);Bm=B0*(1+depth)
 if f.data(q0)['strength']>=Bm:raise ValueError('branch absent at anchor')
 total=0.;events=[]
 for sign in [-1.,1.]:
  def rhs(t,y):
   q=np.r_[y[:2],z0+sign*t];d=f.data(q);cv=d['contravariant']
   gap=max(0.,Bm-float(d['strength']));ds=float(d['strength']*d['D']/d['A'])
   return np.r_[sign*cv[:2]/cv[2],np.sqrt(gap)*ds]
  def mirror(t,y):return Bm-float(f.data(np.r_[y[:2],z0+sign*t])['strength'])
  mirror.terminal=True;mirror.direction=-1
  sol=solve_ivp(rhs,(0,.4),np.r_[q0[:2],0.],events=mirror,rtol=tol,atol=tol*.01,max_step=.003)
  assert sol.success and len(sol.t_events[0])==1
  assert np.all(f.regular(np.c_[sol.y[:2].T,z0+sign*sol.t]))
  total+=sol.y[2,-1];events.append(z0+sign*sol.t[-1])
 return dict(h=h,action=float(total),source_DeltaPsi=float(f.surface_label(q0)-f.PSI0),mirror_phases=events)

start=time.time();base=action(0.);rows=[]
for h in [.0005,.001,.002,.0024,.004]:
 plus=action(h);minus=action(-h)
 assert abs(plus['source_DeltaPsi']-minus['source_DeltaPsi'])<1e-12
 rows.append(dict(h=h,plus=plus,minus=minus,relative_half_spread=(minus['action']-plus['action'])/(2*base['action']),relative_directional_derivative=(plus['action']-minus['action'])/(2*h*base['action'])))
fine=[action(v['h'],tol=2e-12) for v in [rows[0]['plus'],rows[-1]['plus']]]
changes=[abs(a['action']-b['action'])/base['action'] for a,b in zip(fine,[rows[0]['plus'],rows[-1]['plus']])]
out=dict(status='PASS',well_phase=z0,mirror_depth_fraction=.01,base=base,rows=rows,harmonic_deep_trap_prediction_relative_derivative=-float(r['relative_half_well_bottom_spread_per_sqrt_DeltaPsi'])/.01,refined_solver_changes_relative_to_base=changes,seconds=time.time()-start,scope='Numerical finite-pitch paired actions on the same exact source flux label; not interval-certified action integrals or drift-surface closure.')
Path('results/finite_action.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
