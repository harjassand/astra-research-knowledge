import tempfile,shutil,pathlib,subprocess,sys,json,hashlib,os,numpy as np
p=pathlib.Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
 q=pathlib.Path(td)
 for f in ['quantum_memory_fixture_v1.py','check_compressed_projection_v1.py']:shutil.copy2(p/f,q/f)
 run=subprocess.run([sys.executable,str(q/'quantum_memory_fixture_v1.py')],capture_output=True,text=True,check=True)
 records_equal=np.array_equal(np.load(q/'quantum_memory_records_v1.npy'),np.load(p/'quantum_memory_records_v1.npy'))
 result_equal=json.loads((q/'quantum_memory_fixture_v1.json').read_text())==json.loads((p/'quantum_memory_fixture_v1.json').read_text())
 assert records_equal and result_equal
 sys.path.insert(0,td)
 # Define the source only, excluding trajectory execution; imported projection touches only temporary files.
 ns={'__file__':str(q/'quantum_memory_fixture_v1.py')};exec((q/'quantum_memory_fixture_v1.py').read_text().split('max_grad=0;')[0],ns)
 rng=np.random.default_rng(807141);mx=0.; checks=0
 for trial in range(8):
  z=rng.normal(size=(2,3))+1j*rng.normal(size=(2,3));mem=z@z.conj().T;mem/=np.trace(mem)
  rho,rdg,blocks,sig=ns['emit'](mem)
  for x,bell in enumerate(ns['bells']):
   for wi,W in enumerate(ns['pa']):
    ev,vec=np.linalg.eigh(W)
    for b in ([1] if wi==0 else [-1,1]):
     direct=np.zeros((2,2),complex)
     for i,value in enumerate(ev):
      if abs(value-b)>1e-9:continue
      # Kraus from (R,D,M,G) to M, an explicit Bell/flag bra contraction.
      K=np.kron(np.kron(bell.conj()[None,:],np.eye(2)),vec[:,i].conj()[None,:])
      direct+=K@rho@K.conj().T
     short=ns['memory_after'](blocks[x],W,b)
     mx=max(mx,float(np.max(abs(direct-short))));checks+=1
 assert mx<1e-13
out={'temporary_full_replay_records_identical':records_equal,'temporary_full_replay_results_identical':result_equal,'independent_explicit_measurement_kraus_checks':checks,'maximum_memory_instrument_error':mx,'scope':'Floating diagnostic and record replay only; projection algorithm not independently certified, no confidence or advantage claim.'}
pathlib.Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
