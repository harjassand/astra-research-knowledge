#!/usr/bin/env python3
"""Saved learned SU2 inverse executed with continuous Hamiltonian/dephasing pulses."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import sys,json,numpy as np
from scipy.linalg import expm
HERE=Path(__file__).parent;Q=HERE.parent
sys.path.insert(0,str(Q/'noisy_code_boundaries_20261028'));import boundary_channel_v2 as b
m=b.m

def euler(U):
 U=U/np.sqrt(np.linalg.det(U));theta=2*np.arctan2(abs(U[1,0]),abs(U[0,0]));a=np.angle(U[1,0])-np.angle(U[0,0]);c=-np.angle(U[1,0])-np.angle(U[0,0])
 seq=[(2,c),(1,theta),(2,a)];V=np.eye(2,dtype=complex)
 for axis,ang in seq:V=m.old.rotation(m.P[axis+1],ang)@V
 assert abs(np.trace(V.conj().T@U)/2)>1-1e-12
 return seq

def pulse(axis,angle,duration,rate,eps,eta):
 # Constant Hamiltonian H=(angle*(1+eps)*sigma_axis + eta X)/(2 duration).
 v=np.zeros(3);v[axis]=angle*(1+eps);v[0]+=eta
 x,y,z=v;G=np.array([[0,-z,y],[z,0,-x],[-y,x,0]],float)/duration
 G+=np.diag([-rate,-rate,0]);M=np.eye(4);M[1:,1:]=expm(G*duration);return M

def build_native(rate,eps,eta,omega=np.pi,switch=.2):
 models=np.load(m.old.PILOT/'models.npz');sel=json.loads((m.old.PILOT/'results.json').read_text())['selected_calibration_N_per_site'];srcs=m.c.generator_sources();seqs=[];raw=[]
 for i,src in enumerate(srcs):
  W=models[f'learned_frame_N{sel}_site{i}'].astype(complex);seqs.append(euler(W.conj().T));raw.append(np.array(src['PTM'],float))
 durations=[[abs(angle)/omega+switch for axis,angle in seq] for seq in seqs];layers=np.max(durations,axis=0);out=[]
 for i,M0 in enumerate(raw):
  M=np.diag([1,np.exp(-rate),np.exp(-rate),1])@M0 # one native time unit, endpoint split
  for k,(axis,angle) in enumerate(seqs[i]):
   dur=durations[i][k];M=pulse(axis,angle,dur,rate,eps,eta)@M
   idle=layers[k]-dur;M=np.diag([1,np.exp(-rate*idle),np.exp(-rate*idle),1])@M
  out.append(M)
 return out,{'pulse_axes_angles':seqs,'site_pulse_durations':durations,'parallel_layer_durations':layers.tolist(),'native_and_inverse_time':float(1+sum(layers)),'max_nominal_angular_speed':omega,'pulse_switch_time':switch,'multiplicative_angle_error':eps,'integrated_unwanted_X_rotation_per_pulse':eta}

def run(integrated=.03,eta=.001,eps=.001,T=32,r=2):
 rate=integrated/201;native,timing=build_native(rate,eps,eta);dec,enc,U=b.synthesize();A=b.circuit(b.initial(eta,rate),enc,eta,rate);F,_=m.build_ec(eta,rate,b.CLOCK)
 for step in range(T):
  for q,M in enumerate(native):A=m.local(A,M,[q],5)
  if (step+1)%r==0:A=F@A
 A=b.circuit(A,dec,eta,rate);M=b.measured_decode(A,U,eta,rate)
 return {'integrated':integrated,'eta':eta,'eps':eps,'T':T,'r':r,'timing':timing,'full_elapsed_time':72+T*timing['native_and_inverse_time']+201*(T//r),'physical_output_PTM':M.tolist(),**m.old.metrics(M),'native_local_PTMs':[x.tolist() for x in native]}
if __name__=='__main__':
 zero,timing=build_native(0,0,0);old=m.native();err=max(np.max(abs(a-c)) for a,c in zip(zero,old));assert err<1e-12
 (HERE/'synthesis_check_v1.json').write_text(json.dumps({'zero_noise_native_PTM_max_error':float(err),'timing':timing},indent=2)+'\n')
 rows=[]
 for eps in [0.,.001,.01]:
  x=run(eps=eps);rows.append(x);print(eps,x['entanglement_infidelity'],x['full_elapsed_time'],flush=True)
 (HERE/'results_v1.json').write_text(json.dumps(rows,indent=2)+'\n')
