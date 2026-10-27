"""Construct the3-phase pressure interface; replay actual PneuAct static data.
The matched first-order channel is a DECLARED model, not an acquired printed-gate
or loaded-motor response. No hardware, self-reproduction or torque qualification.
"""
from pathlib import Path
import csv,json,math,itertools
import numpy as np
ROOT=Path(__file__).resolve().parent
S=ROOT/'sources'
PHI=np.arange(3)*2*math.pi/3
E=np.exp(1j*PHI)
B=np.array([[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1]],float)
U=B@E
# Dimensionless exact q=1/2 witness; pressure example separately source-scaled.
def orbit(q,P=1.,n=1001):
 h=-math.log(q)
 p=(1-q)*sum(q**(5-j)*B[j]*P for j in range(6))/(1-q**6)
 c=(1-q)/(np.exp(1j*math.pi/3)-q)
 phase=[];tt=[];v=[];pp=[];errs=[];pstart=p.copy()
 for k in range(6):
  for s in np.linspace(0,h,n,endpoint=False):
   pv=B[k]*P+(p-B[k]*P)*math.exp(-s)
   z=pv@E;expect=P*np.exp(1j*k*math.pi/3)*(1+(c-1)*math.exp(-s))
   errs.append(abs(z-expect));v.append(z);pp.append(pv);tt.append(k*h+s)
  p=q*p+(1-q)*B[k]*P
 v.append(p@E);pp.append(p);tt.append(6*h)
 v=np.array(v);pp=np.array(pp)
 rmin=P*abs(c)*math.sqrt(3)/2
 # At each edge, minimum radius occurs at its midpoint, not its half-time.
 ystar=math.sqrt(1+q*q-q)
 omstar=(-c.imag)*ystar/abs(1+(c-1)*ystar)**2
 return {'q':q,'normalized_period':6*h,'winding':float((np.unwrap(np.angle(v))[-1]-np.unwrap(np.angle(v))[0])/(2*math.pi)),
 'minimum_radius_exact':rmin,'minimum_radius_grid':float(np.min(abs(v))),
 'maximum_phase_speed_times_tau':omstar,
 'minimum_phase_increment_grid':float(np.min(np.diff(np.unwrap(np.angle(v))))),
 'pressure_min':float(pp.min()),'pressure_max':float(pp.max()),
 'closed_state_residual':float(np.max(abs(p-pstart))),
 'phasor_formula_residual':float(max(errs))}
exact=orbit(.5)
# Convexity: maximum of norm of linear map on cube lies at a vertex.
err_cube=max(abs(np.array(v)@E) for v in itertools.product([-1.,1.],repeat=3))
# PneuAct paper Eq1: rise time parameter for1-8m,4mm-ID lines,2-7bar,
# fitted with ELECTRONIC valves. Illustrative source-model composition only.
source_f=4.2       # Kendre author version, reported loaded magnet-motor ring rate.
source_l=3.       # PneuAct Fig10 source line length.
source_tau=.020*math.exp(source_l/3)
source_delay=(10/3)*math.exp(source_l/3)/1000
source_h=1/(6*source_f)
source_q=math.exp(-source_h/source_tau)
P=200000.         # Proposed buffer output; Kendre's separate linear-robot rail200kPa.
scaled=orbit(source_q,P)
scaled.update({'source_example_ring_frequency_Hz':source_f,'source_empirical_line_length_m':source_l,
 'source_empirical_tau_s':source_tau,'source_empirical_common_delay_s':source_delay,
 'supplied_phasewise_pressure_error_Pa':10000.,'phasor_error_bound_Pa':2*10000.,
 'remaining_pressure_wrench_radius_Pa':scaled['minimum_radius_exact']-20000.,
 'warning':'4.2Hz is the observed magnet-motor ring, not a demonstrated PneuAct drive; Eq1 was fitted with electronic valves, not printed relays; loaded response is not acquired'})
# Exact geometry from PneuAct Fig10, NO frictionless value passed as usable torque.
A,r=15e-3*15e-3,3e-3
scaled['ideal_crank_wrench_amplitude_Nm_not_usable_torque']=A*r*scaled['minimum_radius_exact']
# Mandatory line-only pressure-swing inventory within the declared constant-V,
# isothermal RC model; regulator bleed, chamber motion, supply loss all extra.
V=math.pi*(.004/2)**2*source_l
p_swing=P*(1-source_q**3)/(1+source_q**3)
free_air_cycle=3*V*p_swing/100000.
scaled['declared_model_line_only_free_air_L_min']=free_air_cycle*source_f*60*1000
scaled['source_long_lines_volume_each_mL']=V*1e6
scaled['local_line_30mm_volume_each_mL']=math.pi*(.004/2)**2*.03*1e6
scaled['localization_scope']='Geometric inventory reduction100x only; no extrapolation of Eq1 below its1m source range; DC supply pressure regulation remains a real resource.'
# Replay explicitly documented dimensional measurements, not inferred clearances.
with (S/'PneuAct_Fig7_Fig7_3.csv').open() as f:
 rows=list(csv.DictReader(f))
a=np.array([[float(row[k]) for k in ['ideal gap','ideal length','xy length','z length']] for row in rows])
xy,z=a[:,2]-a[:,1],a[:,3]-a[:,1]
dim={'n':len(a),'xy_error_mean_mm':float(xy.mean()),'xy_error_range_mm':[float(xy.min()),float(xy.max())],
 'z_error_mean_mm':float(z.mean()),'z_error_range_mm':[float(z.min()),float(z.max())],
 'scope':'Source calls clearances nominal CAD values; these dimensions do not determine the actual mating bore or actual clearance.'}
# Fig9 preserves the actual measured pressure/holding-torque pairs in README.
# Parse only that explicitly named Mathematica data block.
import re
s=(S/'PneuAct_Fig9_README.md').read_text();block=s.split('data = {',1)[1].split('};',1)[0]
measured=[[float(x),float(y)] for x,y in re.findall(r'\{([0-9.]+)`?,\s*([0-9.]+)`?\}',block)]
# Fig10 raw timing header lacks a unit in the CSV. Do NOT call it Hz/period.
with (S/'PneuAct_Fig10_Fig10.csv').open() as f:
 raw=list(csv.reader(f))
unknown_header=[float(x) for x in raw[0][1:]]
points=[(float(row[0]),unknown_header[i],float(v)) for row in raw[1:] for i,v in enumerate(row[1:]) if v]
def published_fit(p,f):return .094*math.exp(-.026*f)*math.log(p)-.035*math.exp(-.116*f)
fitdiag={}
for label,fun in [('header_as_Hz_hypothesis',lambda x:x),('1000_over_header_as_Hz_hypothesis',lambda x:1000/x)]:
 resid=np.array([t-published_fit(p,fun(h)) for p,h,t in points])
 fitdiag[label]={'n':len(points),'RMSE_Nm':float(np.sqrt(np.mean(resid**2))),'maximum_abs_residual_Nm':float(np.max(abs(resid)))}
fitdiag['scope']='A source-model diagnostic, not an acquired header-time conversion or a stall certificate for printed control.'
# A passive load countermodel: constant static-friction bound exceeding maximum
# ideal source torque leaves theta fixed despite winding of the pressure vector.
load_counter={'declared_model_pressure_winds_once':True,'fixed_theta_is_admissible_if_static_friction_Nm_at_least':A*r*P*abs((1-source_q)/(np.exp(1j*math.pi/3)-source_q)),
 'scope':'Explicit no-free-work countermodel; no claim this is the actual source motor friction.'}
# Unequal charging/venting: same per-channel profile, not a shared LTI law.
def unequal_orbit(tau_up,tau_down,h,n=2001):
 qvec=np.exp(-h/np.where(B>0,tau_up,tau_down))
 off=np.zeros(3)
 for k in range(6):off=qvec[k]*off+(1-qvec[k])*B[k]
 p0=off/(1-np.prod(qvec,axis=0));p=p0.copy();zz=[]
 for k in range(6):
  tau=np.where(B[k]>0,tau_up,tau_down)
  for t in np.linspace(0,h,n,endpoint=False):
   pv=B[k]+(p-B[k])*np.exp(-t/tau);zz.append(pv@E)
  p=qvec[k]*p+(1-qvec[k])*B[k]
 zz.append(p@E);zz=np.array(zz)
 up=math.exp(-3*h/tau_up);down=math.exp(-3*h/tau_down)
 pmax=(1-up)/(1-up*down);pmin=down*pmax
 m=min((1-pmax)/tau_up,pmin/tau_down)
 return {'tau_up':tau_up,'tau_down':tau_down,'h':h,'sampled_minimum_radius':float(np.min(abs(zz))),
 'monotone_slope_floor':m,'proved_slope_based_radius_floor':math.sqrt(3)*h*m,
 'winding':float((np.unwrap(np.angle(zz))[-1]-np.unwrap(np.angle(zz))[0])/(2*math.pi)),
 'periodic_residual':float(np.max(abs(p-p0))),
 'scope':'Declared unequal-rate positive model; not a fit of source channels.'}
unequal=unequal_orbit(1.,.5,math.log(2))

out={'scope':'Conditional construction of a pressure-to-wrench interface and source-data replay; no composed drive or productive factory acquired.',
 'binary_states':B.astype(int).tolist(),'command_phasor_real_imag':[[float(z.real),float(z.imag)] for z in U],
 'q_half_exact_witness':exact,'unequal_charging_venting_witness':unequal,'phasewise_unit_error_cube_max_phasor_norm':float(err_cube),
 'source_scaled_example_NOT_acquired_join':scaled,'source_dimensional_replay':dim,
 'source_measured_holding_torque_pairs_bar_Nm':measured,'Fig10_header_ambiguity_diagnostic':fitdiag,
 'no_free_motor_rotation_countermodel':load_counter}
(ROOT/'phase_drive_join_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
