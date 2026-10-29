"""Independent density-boundary/native composition; reviewed EC PTM dependency."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import importlib.util,json,hashlib,numpy as np
D=Path(__file__).parent;spec=importlib.util.spec_from_file_location('independent_boundary',D/'check_boundaries_v1.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
a=b.author;Q=b.Q
# Fixed matrices are data from the received acquisition, not a new learner input.
models=np.load(Q/'five_qubit_acquired_frame_pilot_20261028/models.npz');sel=json.loads((Q/'five_qubit_acquired_frame_pilot_20261028/results.json').read_text())['selected_calibration_N_per_site']
ks=[]
for i,source in enumerate(a.m.c.generator_sources()):
 W=models[f'learned_frame_N{sel}_site{i}'].astype(complex);ks.append([b.emb(W.conj().T@np.array(K,complex),[i]) for K in source['Ks']])
def prepare(p,eta,rate):
 r=p.copy()
 for _ in range(4):r=np.kron(r,np.diag([1.,0.]))
 for q in range(1,5):
  g=b.emb(b.rotate(b.pn[2],eta),[q]);r=g@r@g.conj().T;r=b.bg(r,rate,2,list(range(q+1)))
 return b.noise_circuit(r,b.enc,eta,rate)
cache={};records=[]
for row in json.loads((D.parent/'results_v2.json').read_text()):
 eta=row['eta'];rate=row['integrated']/201;T=row['T'];cad=row['r'];rho=np.array([prepare(p,eta,rate) for p in b.pn])
 if T:
  key=(eta,rate)
  if key not in cache:cache[key]=a.m.build_ec(eta,rate,a.CLOCK)[0]
  F=cache[key]
  for t in range(1,T+1):
   for local in ks:rho=np.array([sum(K@r@K.conj().T for K in local) for r in rho])
   if t%cad==0:
    coeff=np.einsum('aij,kji->ak',b.basis,rho).real
    coeff=F@coeff;rho=np.einsum('ak,aij->kij',coeff,b.basis)/32
 out=[b.measured(b.noise_circuit(r,b.ops,eta,rate),eta,rate) for r in rho]
 M=np.array([[np.trace(p@r).real/2 for r in out] for p in b.pn]);diff=float(np.max(abs(M-np.array(row['physical_output_PTM']))));assert diff<2e-12
 records.append({'T':T,'r':cad,'integrated':row['integrated'],'PTM_max_difference':diff,'entanglement_fidelity':float((1+np.trace(M[1:,1:]))/4),'time':72+2*T+201*(T//cad)})
 print(records[-1],flush=True)
files=[D.parent/'results_v2.json',D.parent/'AUTHOR_MANIFEST_v2.json',D/'check_boundaries_v1.py',Path(__file__)]
out={'status':'PASS_COMPLETE_MODEL_COMPOSITION_CONDITIONAL_ON_RECEIVED_EC_PRIMITIVE','rows':records,'source_draws':0,'sha256':{str(p.relative_to(Q)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(D/'replay_full_channel_v1.json').write_text(json.dumps(out,indent=2)+'\n')
