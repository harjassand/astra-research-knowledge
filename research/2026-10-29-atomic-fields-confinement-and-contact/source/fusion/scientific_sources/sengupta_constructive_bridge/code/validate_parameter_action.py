"""Actual finite-volume matching and all located well-class paired actions."""
from pathlib import Path
import sys,importlib.util,json,time
sys.dont_write_bytecode=True
from parameter_action import np,leggauss,brentq
from scipy.integrate import solve_ivp
spec=importlib.util.spec_from_file_location('frozen_member',Path(__file__).parents[1]/'sources/worker_sengupta_paraboloid.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
input_data=json.loads(Path('results/parameter_action.json').read_text())
def configure(p):
 f.M=p['m'];f.KMOD=p['k'];f.K=p['K'];f.KP=p['KP'];f.KAPPA=p['kappa'];f.U0=p['u0'];f.PSI0=1/f.KMOD-1

def volume(q,nz=48,nt=64,nr=6):
 zn,zw=leggauss(nz);rn,rw=leggauss(nr);z=(zn+1)*np.pi;zw=zw*np.pi
 theta=np.arange(nt)*2*np.pi/nt;th,zz=np.meshgrid(theta,z,indexing='ij');co=np.cos(th);si=np.sin(th)
 cap=np.sqrt(2)*np.arccos(1-q)/(f.KAPPA*np.sqrt(1-f.M))
 rr=[]
 for c,s,phase in zip(co.flat,si.flat,zz.flat):
  root=brentq(lambda r:float(f.surface_label([f.U0+r*c,r*s,phase])-f.PSI0)-q,0,cap,xtol=2e-13)
  rr.append(root)
 R=np.array(rr).reshape(nt,nz);rad=R[:,:,None]*(rn+1)/2
 u=f.U0+rad*co[:,:,None];v=rad*si[:,:,None];phase=zz[:,:,None]
 P=np.cosh(u)*np.cosh(v);E=np.sinh(u)*np.sinh(v)-np.sin(2*phase);J=P*(P*P-E*E)
 return float(np.sum(J*rad*(R[:,:,None]/2)*rw[None,None,:]*zw[None,:,None])*(2*np.pi/nt))

def action(member,well,h):
 z0=well['zeta'];dr=np.array(well['direction']);q0=np.r_[f.U0+h*dr[0],h*dr[1],z0];mirror=well['B']*1.01
 assert float(f.data(q0)['strength'])<mirror
 total=0;events=[]
 for sign in [-1.,1.]:
  def rhs(t,y):
   d=f.data(np.r_[y[:2],z0+sign*t]);cv=d['contravariant'];gap=max(0.,mirror-float(d['strength']))
   return np.r_[sign*cv[:2]/cv[2],np.sqrt(gap)*float(d['strength']*d['D']/d['A'])]
  def event(t,y):return mirror-float(f.data(np.r_[y[:2],z0+sign*t])['strength'])
  event.terminal=True;event.direction=-1
  sol=solve_ivp(rhs,(0,.5),np.r_[q0[:2],0.],events=event,rtol=1e-10,atol=1e-12,max_step=.0025)
  assert sol.success and len(sol.t_events[0])==1 and np.all(f.regular(np.c_[sol.y[:2].T,z0+sign*sol.t]))
  phase=z0+sign*sol.t[-1]
  assert int(np.floor((phase+1e-10)/(np.pi/4)))==int(np.floor((z0+1e-10)/(np.pi/4)))
  total+=sol.y[2,-1];events.append(float(phase))
 return float(total),events
start=time.time();records=[]
for name in ['reference','candidate']:
 member=input_data[name];configure(member);target=np.pi*input_data['alpha']**2*member['axis_length']**3
 q=member['near_axis_DeltaPsi'];initial=volume(q);q*=target/initial;matched=volume(q);fine=volume(q,72,96,8)
 rows=[]
 for well in member['minima']:
  direction=np.array(well['direction']);z0=well['zeta']
  h=brentq(lambda h:float(f.surface_label([f.U0+h*direction[0],h*direction[1],z0])-f.PSI0)-q,0,2*np.sqrt(q),xtol=1e-13)
  j0,_=action(member,well,0);jp,ep=action(member,well,h);jm,em=action(member,well,-h)
  delta_plus=float(f.surface_label([f.U0+h*direction[0],h*direction[1],z0])-f.PSI0)
  delta_minus=float(f.surface_label([f.U0-h*direction[0],-h*direction[1],z0])-f.PSI0);assert abs(delta_plus-delta_minus)<1e-12
  rows.append(dict(zeta=z0,h=h,DeltaPsi=delta_plus,base_action=j0,plus_action=jp,minus_action=jm,relative_half_spread=(jm-jp)/(2*j0),mirror_phases_plus=ep,mirror_phases_minus=em))
 record=dict(name=name,sigma=member['sigma'],matched_DeltaPsi=q,target_normalized_volume=input_data['alpha']**2*np.pi,computed_normalized_volume=fine/member['axis_length']**3,volume_refinement_relative_change=abs(fine-matched)/target,volume_target_relative_error=abs(fine-target)/target,well_count=len(rows),worst_actual_relative_half_action_variation=max(abs(v['relative_half_spread']) for v in rows),all_wells=rows,reported_costs={k:member[k] for k in ['max_near_axis_elongation_diagnostic','normalized_axis_max_curvature','minimum_relative_barrier','complete_tube_margin_sufficient','isolated_well_isotropic_pitch_fraction_at_bottom']})
 records.append(record);print(json.dumps({k:v for k,v in record.items() if k!='all_wells'},indent=2),flush=True)
out=dict(status='PASS',records=records,ratio_actual_worst_candidate_to_reference=records[1]['worst_actual_relative_half_action_variation']/records[0]['worst_actual_relative_half_action_variation'],seconds=time.time()-start,scope='Finite numerical tube-volume matching and all located near-axis well classes at1% depth; not a broad orbit/confinement or global optimum theorem.')
Path('results/validated_parameter_action.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2),flush=True)
