"""Readable actual coupled port data; zero-time bounds kept separate."""
from pathlib import Path
import csv,json,sys
import numpy as np
import cycle as c
HERE=Path(__file__).resolve().parent
z=json.loads((HERE/(sys.argv[1] if len(sys.argv)>1 else 'physical_coil_RESULT.json')).read_text())
prefix=sys.argv[2] if len(sys.argv)>2 else ''
h=c.half(z['initial_high_low_T'],dense=True,**z['parameters'])
recs=h['_records'];rw=z['parameters']['r_arms'];now=0.
headers=['time_s','phase','TA_K','TB_K','VA_V','VB_V','j_A_m2','Tnode_K',
 'QFE_A_C_m2','QFE_B_C_m2','IFE_A_A_m2','IFE_B_A_m2',
 'qh_A_W_m2','qh_B_W_m2','qc_A_W_m2','qc_B_W_m2','qwire_A_W_m2','qwire_B_W_m2']
for bank in ['A','B']:
 for face in ['hot','cold']:
  headers += [f'mu_{bank}_{face}_eV',f'Vg_{bank}_{face}_V',f'Qg_{bank}_{face}_C_m2',f'Ig_{bank}_{face}_A_m2']
rows=[];events=[];stages=[];maxima={'EFE_V_m':0.,'ESiC_V_m':0.,'Eiso_V_m':0.}
for label,sol,mus,mudots,modes,duration in recs:
 vals=[]
 for tt in np.linspace(0,sol.t[-1],81):
  y=sol.sol(tt);mm=mus(tt) if callable(mus) else mus;md=mudots(tt) if callable(mudots) else mudots
  controls=[];flux=[];Q=[];I=[];gates=[]
  for k in range(2):
   T,V=y[k],y[k+2]
   qh,qc=(0.,0.) if duration==0 else c.thermal(T,modes[k],409.)
   qw=0. if duration==0 else 4*c.L0/rw*(y[19]**2-T*T)
   heat=qh+qc+qw+(.25*rw*y[4]**2 if label=='LC_exchange' else 0.)
   if label=='LC_exchange':
    cur=(-1 if k==0 else 1)*y[4];td,vd,fl=c.gate.coupled_derivatives(T,V,mm[k],md[k],cur,heat,c.fp(T,V))
   else:
    vd=0. if label!='endpoint_correction' else ((c.VL if k==0 else c.VH)-sol.y[k+2,0])/duration
    td,cur,fl=c.at_fixed_dv(T,V,mm[k],md[k],vd,heat)
   I.append(cur);Q.append(c.fp(T,V)['Q']+sum(f['Qfe_iso'] for f in fl));flux.append((qh,qc,qw))
   for f in fl:
    gates += [f['mu'],f['Vg'],f['Qg'],f['Ig']]
    maxima['ESiC_V_m']=max(maxima['ESiC_V_m'],abs(f['ESiC_V_m']))
    maxima['Eiso_V_m']=max(maxima['Eiso_V_m'],abs(f['Eiso_V_m']))
   maxima['EFE_V_m']=max(maxima['EFE_V_m'],abs(V)/260e-9)
  row=[now+tt if duration else now,label,*y[:5],y[19],*Q,*I,flux[0][0],flux[1][0],flux[0][1],flux[1][1],flux[0][2],flux[1][2],*gates]
  if duration:rows.append(row)
  else:events.append([now,label,tt,*row[2:]])
 if duration:now+=duration
 d=sol.y[:,-1]-sol.y[:,0]
 stages.append({'phase':label,'duration_s':float(duration),'W_FE_terminal_out_J_m2':d[7],
 'W_gate_out_J_m2':d[8],'FE_abs_processed_J_m2':d[9],'gate_abs_processed_J_m2':d[10],
 'Qh_J_m2':d[5],'Qc_J_m2':d[6],
 'gate_I2_physical_A2s_m4':d[15] if duration else None,
 'gate_dQdx_squared_C2_m4':d[15] if not duration else None,
 'FE_I2_physical_A2s_m4':d[16] if duration else None,
 'FE_dQdx_squared_C2_m4':d[16] if not duration else None})
with (HERE/(prefix+'finite_phase_ports_halfcycle.csv')).open('w') as f:
 w=csv.writer(f);w.writerow(headers);w.writerows(rows)
with (HERE/(prefix+'adiabatic_gate_events.csv')).open('w') as f:
 # In this file all reported currents have units dQ/dx, not A/m2.
 w=csv.writer(f);w.writerow(['physical_time_s','phase','dimensionless_transition_x']+[v.replace('_A_m2','_dQdx_C_m2') for v in headers[2:]]);w.writerows(events)
(HERE/(prefix+'stage_ports.json')).write_text(json.dumps({'stages':stages,'sampled_field_maxima':maxima,
 'units':'peronebankA; pairhalf totals. Gateevents are zero-duration bounds; event derivativeunitsdQ/dx. For finite linearx=t/dtgate, eventI2=integral(dQdx²)/dtgate, but thermal/circuitdynamicsmustthenberesolved.'},indent=2)+'\n')
print(json.dumps(maxima))
