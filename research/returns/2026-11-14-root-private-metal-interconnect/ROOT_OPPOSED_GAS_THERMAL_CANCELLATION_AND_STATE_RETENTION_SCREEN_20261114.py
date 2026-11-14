#!/usr/bin/env python3
"""INTRODUCED opposed-gas passive-state model, not qualified hardware.
Closed mole stocks, explicit gas/wall energy, arbitrary temperature mismatch.
Serial Python standard library only; no external data/code/network.
"""
import math,json,itertools
from pathlib import Path
R=8.31446261815324
T0=298.15
P0=101325.
P={
 "gas_volume_each_m3":20e-9,"stroke_m3":.12e-9,
 "area_m2":math.pi*(.5e-3)**2,"total_membrane_k_N_m":5.,
 "gas_gamma":1.4,"wall_C_each_J_K":.01,
 "ambient_G_each_W_K":.003,"cross_G_W_K":.005,
 "fill_pressure_relative_error":.002,"volume_relative_error":.02,
 "area_relative_mismatch":.002,"hydraulic_R":50929581789.406494,
 "pin_pressure_Pa":5000.,"gravity_Pa":1176.798,
 "on_cell_R_ohm":.04084882636315677,"leg_s":.25,
 "hold_duration_s":86400.
}
def stocks(par,fill=(0.,0.),volume=(0.,0.)):
 v=[par['gas_volume_each_m3']*(1+x) for x in volume]
 n=[P0*(1+e)*vv/(R*T0) for e,vv in zip(fill,v)]
 return v,n
def geom(q,par,vol):
 e=par['area_relative_mismatch']
 a,b=1+e,1-e
 va,vb=vol[0]-a*q,vol[1]+b*q
 assert min(va,vb)>0
 return (va,vb),(a,b)
def gas_p(temps,q,par,vol,n):
 vv,ab=geom(q,par,vol)
 return [ni*R*t/v for ni,t,v in zip(n,temps,vv)]
def pressure(temps,q,par,vol,n):
 pp=gas_p(temps,q,par,vol,n);_,(a,b)=geom(q,par,vol)
 # Ambient-reference forces must actually be supplied on the complete
 # outer moving surfaces; this is a declared virtual-work organisation.
 diff=a*(pp[0]-P0)-b*(pp[1]-P0)
 spring=par['total_membrane_k_N_m']*q/par['area_m2']**2
 return diff+spring
def eig_exp(mat,h):
 a,b,c,d=mat;m=(a+d)/2;z=math.sqrt(((a-d)/2)**2+b*c)
 ep=math.exp((m+z)*h);em=math.exp((m-z)*h)
 f=(ep-em)/(2*z) if z else h*math.exp(m*h)
 g=(ep+em)/2
 return (g+f*(a-m),f*b,f*c,g+f*(d-m))
def mul(mat,v):
 return [mat[0]*v[0]+mat[1]*v[1],mat[2]*v[0]+mat[3]*v[1]]
def thermal_setup(par,n,ambient,power):
 cv=R/(par['gas_gamma']-1)
 C=[par['wall_C_each_J_K']+ni*cv for ni in n]
 H=par['ambient_G_each_W_K'];K=par['cross_G_W_K']
 M=(-(H+K)/C[0],K/C[0],K/C[1],-(H+K)/C[1])
 rhs=[(H*t+w)/cc for t,w,cc in zip(ambient,power,C)]
 a,b,c,d=M;det=a*d-b*c
 eq=[(-d*rhs[0]+b*rhs[1])/det,(c*rhs[0]-a*rhs[1])/det]
 return M,eq,C
def hold_segment(tstart,h,ambient,power,q,par,vol,n):
 M,eq,C=thermal_setup(par,n,ambient,power)
 delta=[t-e for t,e in zip(tstart,eq)]
 e=eig_exp(M,h);part=mul(e,delta);tend=[x+y for x,y in zip(eq,part)]
 # Pressure is affine in the two temperatures while q/moles are held.
 # Its exact interior extrema are included; no time grid certifies it.
 a,b,c,d=M;mid=(a+d)/2;z=math.sqrt(((a-d)/2)**2+b*c)
 l1,l2=mid+z,mid-z
 vv,(ga,gb)=geom(q,par,vol)
 w=[ga*n[0]*R/vv[0],-gb*n[1]*R/vv[1]]
 y0=sum(x*y for x,y in zip(w,delta));yd0=sum(x*y for x,y in zip(w,mul(M,delta)))
 c1=(yd0-l2*y0)/(l1-l2);c2=y0-c1
 times=[0.,h]
 if c1*l1 and c2*l2:
  ratio=-c2*l2/(c1*l1)
  if ratio>0:
   t=math.log(ratio)/(l1-l2)
   if 0<t<h:times.append(t)
 pp=[]
 for t in times:
  ee=eig_exp(M,t);tt=[x+y for x,y in zip(eq,mul(ee,delta))]
  pp.append({'seconds':t,'temperatures_K':tt,'pressure_Pa':pressure(tt,q,par,vol,n),
             'gas_pressure_Pa':gas_p(tt,q,par,vol,n)})
 return tend,pp
def schedule(par,kind):
 W=par['on_cell_R_ohm'] # 1 A useful current, all local heat assigned adversely to one thermal node.
 if kind=='common_ambient':
  return [(1800.,[288.15,288.15],[0.,0.]),(21600.,[313.15,313.15],[W,0.]),
          (21600.,[288.15,288.15],[0.,W]),(41400.,[313.15,313.15],[0.,0.])]
 if kind=='opposed_environment':
  return [(1800.,[288.15,313.15],[0.,0.]),(21600.,[313.15,288.15],[W,0.]),
          (21600.,[288.15,313.15],[0.,W]),(41400.,[313.15,288.15],[0.,0.])]
 raise ValueError(kind)
def hold_run(par,kind,fill,volume,q):
 vol,n=stocks(par,fill,volume);temp=[T0,T0];rows=[];elapsed=0.
 for h,amb,powr in schedule(par,kind):
  tend,points=hold_segment(temp,h,amb,powr,q,par,vol,n)
  for pt in points:
   pt['time_s']=elapsed+pt.pop('seconds');pt['ambient_K']=amb;pt['power_W']=powr
   rows.append(pt)
  temp=tend;elapsed+=h
 assert abs(elapsed-par['hold_duration_s'])<1e-9
 worst=max(rows,key=lambda r:abs(r['pressure_Pa']))
 maxp=max(abs(p-P0) for row in rows for p in row['gas_pressure_Pa'])
 return {'kind':kind,'fill_errors':fill,'volume_errors':volume,'q_m3':q,
         'max_total_disturbance_Pa':abs(worst['pressure_Pa'])+par['gravity_Pa'],
         'worst':worst,'retained_in_model':abs(worst['pressure_Pa'])+par['gravity_Pa']<par['pin_pressure_Pa'],
         'max_gas_abs_gauge_Pa':maxp,'final_temperatures_K':temp}
def quintic(s):return 10*s**3-15*s**4+6*s**5
def qmotion(t,par):
 leg=par['leg_s'];period=2*leg;local=t%period
 forward=local<leg
 s=local/leg if forward else (local-leg)/leg
 # At exact period end choose q=0 with zero velocity.
 f=quintic(s);df=30*s*s*(1-s)**2
 q=par['stroke_m3']*(f if forward else 1-f)
 qd=par['stroke_m3']*df/leg*(1 if forward else -1)
 return q,qd
def derivative(t,y,par,vol,n):
 q,qd=qmotion(t,par);vv,(a,b)=geom(q,par,vol)
 temps=y[:2];ps=[ni*R*tt/v for ni,tt,v in zip(n,temps,vv)]
 C=[par['wall_C_each_J_K']+ni*R/(par['gas_gamma']-1) for ni in n]
 H=par['ambient_G_each_W_K'];K=par['cross_G_W_K']
 env=[H*(T0-tt) for tt in temps]
 cross=K*(temps[1]-temps[0])
 D=par['pin_pressure_Pa']*abs(qd)+par['hydraulic_R']*qd*qd
 compression=[ps[0]*a*qd,-ps[1]*b*qd]
 dt=[(env[0]+cross+compression[0]+D/2)/C[0],
     (env[1]-cross+compression[1]+D/2)/C[1]]
 # Head pressure includes the ambient virtual-work reference; ambient
 # work is separately retained. Both sum to full gas compression work.
 phead=pressure(temps,q,par,vol,n)+(par['pin_pressure_Pa']*(1 if qd>0 else -1 if qd<0 else 0))+par['hydraulic_R']*qd
 wh=phead*qd;wa=2*par['area_relative_mismatch']*P0*qd
 return dt+[wh,wa,sum(env),D,max(wh,0.),max(-wh,0.)]
def rk4(t,y,h,par,vol,n):
 a=derivative(t,y,par,vol,n)
 b=derivative(t+h/2,[u+h*v/2 for u,v in zip(y,a)],par,vol,n)
 c=derivative(t+h/2,[u+h*v/2 for u,v in zip(y,b)],par,vol,n)
 d=derivative(t+h,[u+h*v for u,v in zip(y,c)],par,vol,n)
 return [u+h*(aa+2*bb+2*cc+dd)/6 for u,aa,bb,cc,dd in zip(y,a,b,c,d)]
def cycle_run(par,cycles,steps_per_leg):
 vol,n=stocks(par);y=[T0,T0]+[0.]*6
 dt=par['leg_s']/steps_per_leg
 C=[par['wall_C_each_J_K']+ni*R/(par['gas_gamma']-1) for ni in n]
 maxforce=0.;lastq=0.
 total_steps=cycles*2*steps_per_leg
 for i in range(total_steps):
  t=i*dt;y=rk4(t,y,dt,par,vol,n)
  q,qd=qmotion((i+1)*dt,par)
  pp=pressure(y[:2],q,par,vol,n)+par['pin_pressure_Pa']*(1 if qd>0 else -1 if qd<0 else 0)+par['hydraulic_R']*qd
  maxforce=max(maxforce,abs(pp)*par['area_m2']);lastq=q
 # End q is analytically zero; modulo may leave tiny floating residue.
 dthermal=sum(cc*(tt-T0) for cc,tt in zip(C,y[:2]))
 delastic=.5*par['total_membrane_k_N_m']*(lastq/par['area_m2'])**2
 residual=y[2]+y[3]+y[4]-dthermal-delastic
 return {'cycles':cycles,'steps_per_leg':steps_per_leg,'head_work_J':y[2],
         'ambient_boundary_work_J':y[3],'environment_heat_into_nodes_J':y[4],
         'capillary_and_viscous_heat_J':y[5],'positive_head_work_J':y[6],'negative_head_work_magnitude_J':y[7],
         'final_thermal_energy_change_J':dthermal,'final_elastic_energy_J':delastic,
         'energy_identity_residual_J':residual,'final_temperatures_K':y[:2],'max_head_force_N':maxforce,
         'scope':'temperatures carried continuously between cycles; no mole/temperature/energy reset; no real head or wetting'}
def main():
 # Equal temperatures cancel the q=0 common pressure exactly for equal
 # effective areas and matched fill pressure, regardless of temperature.
 pp={**P,'area_relative_mismatch':0.}
 vol,n=stocks(pp)
 static=[{'T_K':t,'q0_pressure_Pa':pressure([t,t],0.,pp,vol,n),
          'q_on_pressure_Pa':pressure([t,t],pp['stroke_m3'],pp,vol,n)} for t in (288.15,298.15,313.15)]
 assert max(abs(r['q0_pressure_Pa']) for r in static)<1e-9
 corners=[];e=P['fill_pressure_relative_error'];v=P['volume_relative_error']
 for total_k in (5.,10.):
  for cross in (.005,.020):
   par={**P,'total_membrane_k_N_m':total_k,'cross_G_W_K':cross}
   for kind in ('common_ambient','opposed_environment'):
    cases=[hold_run(par,kind,fill,volume,q) for fill in itertools.product((-e,e),repeat=2)
           for volume in itertools.product((-v,v),repeat=2) for q in (0.,par['stroke_m3'])]
    worst=max(cases,key=lambda c:c['max_total_disturbance_Pa'])
    corners.append({'total_membrane_k_N_m':total_k,'cross_G_W_K':cross,'kind':kind,
                    'cases':len(cases),'maximum_gas_abs_gauge_across_all_cases_Pa':max(c['max_gas_abs_gauge_Pa'] for c in cases),
                    'all_corners_retained_in_declared_schedule':all(c['retained_in_model'] for c in cases),
                    'worst':worst})
 cycles=[cycle_run(P,1,nstep) for nstep in (100,200,400)]
 continuity=cycle_run(P,100,100)
 # Inventory loss and pressure drift are different contracts.
 vol,n=stocks(P);loss_cases=[]
 for frac in (0.,.005,.01,.02,.05):
  nn=[n[0],n[1]*(1-frac)]
  pres=pressure([313.15,313.15],P['stroke_m3'],P,vol,nn)
  loss_cases.append({'one_chamber_mole_loss_fraction':frac,'retained_stock_fraction':1-frac,
                    'total_disturbance_Pa':abs(pres)+P['gravity_Pa'],
                    'retained_in_model':abs(pres)+P['gravity_Pa']<P['pin_pressure_Pa']})
 # Conservative independent leakage bound over 24h: each pocket loses
 # <=L*maxGauge*t moles; both errors can add. Actual permeability unknown.
 maxg=max(r['maximum_gas_abs_gauge_across_all_cases_Pa'] for r in corners)
 mol0=P0*P['gas_volume_each_m3']/(R*T0);budget=200.
 # Leakage contract is conditional on these explicit temperature/pressure
 # envelopes even with changing moles; leakage heat/flow is not simulated.
 # The sealed hold ODE obeys the displayed temperature maximum principle.
 t_leak_bound=313.15+P['on_cell_R_ohm']/P['ambient_G_each_W_K']
 v_leak_min=P['gas_volume_each_m3']*(1-P['volume_relative_error'])-(1+abs(P['area_relative_mismatch']))*P['stroke_m3']
 gauge_leak_bound=maxg+budget
 maxL=budget*v_leak_min/(2*R*t_leak_bound*gauge_leak_bound*P['hold_duration_s'])
 # Known star-current accounting: under balanced <=1 A positive current
 # per net, the sum of squared edge currents is <=1 for a 2-node net,
 # <=2 for >=3 nodes, and 0 for singletons. Enumerate compositions of 16
 # to bound total on-cell heat; this is not a new routing algorithm.
 heat_units=[0.]*17
 for size in range(1,17):
  heat_units[size]=max(heat_units[size-k]+(0. if k==1 else 1. if k==2 else 2.) for k in range(1,size+1))
 # Specific dielectric sandwich with two conducting heat-spreader plates:
 # K=k A/l and C=eps0 epsr A/l. Not every possible thermal layout has this
 # electrical topology, so no universal heat/crosstalk tradeoff is claimed.
 bridges=[]
 for name,k,eps in [('introduced_high_k_dielectric',150.,9.),('introduced_low_k_dielectric',.2,3.)]:
  for K in (.005,.020):
   cap=8.8541878128e-12*eps*K/k
   cell_cap=1.8692578558186488e-14+cap
   yy=64*complex(1.0000000314159265e-10,2*math.pi*1e5*cell_cap)
   gl=8/10000.;gs=1/1000.;det=(gl+gs+yy)*(gl+yy)-yy*yy
   vb=gs*yy/det;ideal=gl**-1/(1000.+gl**-1)
   ratio=abs(vb)/ideal
   bridges.append({'material_label':name,'k_W_m_K':k,'epsilon_r':eps,'cross_G_W_K':K,
     'added_capacitance_F':cap,'total_off_cell_C_F':cell_cap,
     'unwanted_transfer_ratio_in_two_8node_ideal_nets':ratio,'unwanted_dB':20*math.log10(ratio),
     'scope':'introduced homogeneous thermal/electrical sandwich, ideal zero-ohm within-net conductors; not installed material or all layouts'})
 out={'scope':'INTRODUCED opposed closed-gas/thermal/interface model, not physical cancellation hardware or useful fabric',
      'parameters':P,'equal_area_common_temperature_static':static,'exact_thermal_schedule_corner_results':corners,
      'write_return_energy_refinements':cycles,'continuous_same_stock_100_cycles':continuity,
      'asymmetric_stock_loss':loss_cases,'independent_leakage_contract':{
       'gas_moles_each_at_reference':mol0,'max_abs_gauge_bound_for_schedules_Pa':maxg,
       'imposed_temperature_envelope_K':t_leak_bound,'imposed_gauge_envelope_with_error_Pa':gauge_leak_bound,
       'minimum_volume_for_error_bound_m3':v_leak_min,
       'allowed_additional_pressure_error_Pa':budget,'max_molar_leak_conductance_each_mol_s_Pa':maxL,
       'scope':'conditional sufficient bound from per-pocket leak law and imposed temperature/pressure envelopes; changing-mole thermal flow and actual seal not supplied'},
      'geometric_inventory':{'two_pockets_total_mL_for_120_cells':2*120*P['gas_volume_each_m3']*1e6,
       'fraction_of_25mm_cube_occupied_by_gas_alone':2*120*P['gas_volume_each_m3']/(.025**3),
       'scope':'gas volume alone, no reservoir/walls/contacts/thermal bridge/diaphragm/rails/head/dielectric/CAD'},
      'whole_star_network_heat_bound':{'maximum_sum_squared_edge_currents_A2':heat_units[16],
       'maximum_on_cell_heat_W':heat_units[16]*P['on_cell_R_ohm'],
       'attaining_example':'five 3-terminal nets with zero hub current and +/-1A leaves, plus one singleton',
       'scope':'known complete-graph/star current model, excluding rails and contact heating outside on-cell R; no full package heat rejection'},
      'specific_thermal_bridge_capacitance_cases':bridges,
      'verification':{'energy_refinement_span_J':max(r['head_work_J'] for r in cycles)-min(r['head_work_J'] for r in cycles),
       'maximum_energy_identity_residual_J':max(abs(r['energy_identity_residual_J']) for r in cycles+[continuity])},
      'limits':['pinning/wetting law, membrane stiffness and sealed stock are introduced simultaneous requirements',
       'thermal conductance, node capacity, fill matching, symmetry and ambient-force reference are unconstructed',
       'temperature cancellation at q=0 does not eliminate finite-displacement spring pressure or temperature differences',
       'given piecewise schedules and listed material corners are not arbitrary environment/function/life certification',
       'thermal bridge must preserve electrical isolation and full installed parasitic/packaging budgets',
       'passive pressure-balanced switching is prior art; no novelty, useful fabricated device or whole advantage established']}
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:out[k] for k in ('equal_area_common_temperature_static','exact_thermal_schedule_corner_results',
       'write_return_energy_refinements','continuous_same_stock_100_cycles','asymmetric_stock_loss',
       'independent_leakage_contract','geometric_inventory','verification')}))
if __name__=='__main__':main()
