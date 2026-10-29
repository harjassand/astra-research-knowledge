"""Independent complex Liouvillian pulse solver and physical pipeline replay."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import sys,importlib.util,json,hashlib,numpy as np
from scipy.linalg import expm
D=Path(__file__).parent;A=D.parent;Q=A.parent
sys.path.insert(0,str(A));import pulse_pipeline_v1 as author
spec=importlib.util.spec_from_file_location('density_boundary',Q/'noisy_code_boundaries_20261028/independent_audit/check_boundaries_v1.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
P=b.pn;I=P[0];Z=P[3]
def independent_pulse(axis,angle,duration,rate,eps,eta):
 H=((1+eps)*angle*P[axis+1]+eta*P[1])/(2*duration)
 L=-1j*(np.kron(I,H)-np.kron(H.T,I))+(rate/2)*(np.kron(Z.T,Z)-np.eye(4))
 S=expm(duration*L);out=[(S@p.reshape(4,order='F')).reshape((2,2),order='F') for p in P]
 return np.array([[np.trace(p@r).real/2 for r in out] for p in P])
def choi(M):return sum(M[i,j]*np.kron(P[i],P[j].T)/4 for i in range(4) for j in range(4))
models=np.load(Q/'five_qubit_acquired_frame_pilot_20261028/models.npz');sel=json.loads((Q/'five_qubit_acquired_frame_pilot_20261028/results.json').read_text())['selected_calibration_N_per_site'];src=author.m.c.generator_sources()
results=json.loads((A/'results_v1.json').read_text());pulse_checks=[];full=[];F=None
for row in results:
 rate=row['integrated']/201;eta=row['eta'];eps=row['eps'];T=row['T'];cad=row['r'];timing=row['timing'];seqs=timing['pulse_axes_angles'];durations=np.array(timing['site_pulse_durations']);layers=durations.max(axis=0)
 assert np.max(abs(layers-np.array(timing['parallel_layer_durations'])))<1e-14
 native=[]
 for i,seq in enumerate(seqs):
  # Verify compiler target directly by complex unitary product, without author.euler.
  U=np.eye(2,dtype=complex)
  for axis,theta in seq:U=expm(-1j*theta*P[axis+1]/2)@U
  target=models[f'learned_frame_N{sel}_site{i}'].conj().T
  assert abs(np.trace(U.conj().T@target)/2)>1-1e-12
  rawK=[np.array(K,complex) for K in src[i]['Ks']]
  M=np.array([[sum(np.trace(p@K@q@K.conj().T).real/2 for K in rawK) for q in P] for p in P]);M=np.diag([1,np.exp(-rate),np.exp(-rate),1])@M
  for k,(axis,theta) in enumerate(seq):
   duration=abs(theta)/np.pi+.2;assert abs(duration-durations[i,k])<1e-14
   Mp=independent_pulse(axis,theta,duration,rate,eps,eta);err=float(np.max(abs(Mp-author.pulse(axis,theta,duration,rate,eps,eta))))
   assert err<1e-12;mineig=float(np.linalg.eigvalsh(choi(Mp)).min());assert mineig>-1e-12
   M=Mp@M;idle=layers[k]-duration;assert idle>=-1e-14;M=np.diag([1,np.exp(-rate*idle),np.exp(-rate*idle),1])@M
   pulse_checks.append({'eps':eps,'site':i,'layer':k,'complex_Liouvillian_PTM_difference':err,'Choi_min_eigenvalue':mineig})
  assert np.max(abs(M-np.array(row['native_local_PTMs'][i])))<1e-12;native.append(M)
 # Independent physical density preparation and encoder.
 rho=[]
 for p in P:
  r=p.copy()
  for _ in range(4):r=np.kron(r,np.diag([1.,0.]))
  for q in range(1,5):
   g=b.emb(b.rotate(P[2],eta),[q]);r=g@r@g.conj().T;r=b.bg(r,rate,2,list(range(q+1)))
  rho.append(b.noise_circuit(r,b.enc,eta,rate))
 rho=np.array(rho)
 if F is None:F=author.m.build_ec(eta,rate,author.b.CLOCK)[0]
 # Propagate full physical Pauli coordinates with independently assembled local maps.
 coeff=np.einsum('aij,kji->ak',b.basis,rho).real
 # Explicit full tensor native PTM, avoids author.local implementation in the loop.
 N=np.ones((1,1))
 for M in native:N=np.kron(N,M)
 for t in range(1,T+1):
  coeff=N@coeff
  if t%cad==0:coeff=F@coeff
 rho=np.einsum('ak,aij->kij',coeff,b.basis)/32
 outs=[b.measured(b.noise_circuit(r,b.ops,eta,rate),eta,rate) for r in rho]
 M=np.array([[np.trace(p@r).real/2 for r in outs] for p in P]);difference=float(np.max(abs(M-np.array(row['physical_output_PTM']))));assert difference<2e-12
 elapsed=72+T*(1+sum(layers))+201*(T//cad);assert abs(elapsed-row['full_elapsed_time'])<1e-10
 # The accepted theorem permits arbitrary adaptive controls by Trotter segmentation.
 upper=(1+(399/401)**T*np.exp(-rate*elapsed))/2
 actual=float((1+np.trace(M[1:,1:]))/4)
 comparator=json.loads((A/'comparator_application_v1.json').read_text())[len(full)]
 assert abs(upper-comparator['same_elapsed_all_adaptive_single_carrier_Fe_upper'])<1e-14
 full.append({'eps':eps,'PTM_max_difference':difference,'entanglement_fidelity':actual,'elapsed_time':float(elapsed),'single_carrier_upper':float(upper),'gap':float(actual-upper)})
 print(full[-1],flush=True)
files=[A/'pulse_pipeline_v1.py',A/'GOVERNING_PULSE_PIPELINE_v1.md',A/'results_v1.json',A/'comparator_application_v1.json',A/'AUTHOR_MANIFEST_v1.json',Path(__file__)]
out={'status':'PASS_COMPLEX_LIOUVILLIAN_AND_FULL_MODEL_REPLAY','pulse_checks':pulse_checks,'complete_pipeline_checks':full,'dependency':'Received full clocked EC map reused; density boundaries independently replayed','source_draws':0,'sha256':{str(p.relative_to(Q)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(D/'check_pulse_pipeline_v1.json').write_text(json.dumps(out,indent=2)+'\n')
