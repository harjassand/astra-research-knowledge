import os,tempfile,shutil,pathlib,subprocess,sys,json,numpy as np
from scipy.linalg import expm
p=pathlib.Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
 root=pathlib.Path(td);q=root/p.name;q.mkdir();other=root/'compact_prequential_flag_recovery_20261028';other.mkdir()
 shutil.copy2(p/'high_oracle_meta_fixture_v1.py',q/'high_oracle_meta_fixture_v1.py')
 shutil.copy2(p.parent/'compact_prequential_flag_recovery_20261028/check_compressed_projection_v1.py',other/'check_compressed_projection_v1.py')
 subprocess.run([sys.executable,str(q/'high_oracle_meta_fixture_v1.py')],check=True,capture_output=True,text=True)
 identical_records=np.array_equal(np.load(q/'high_oracle_meta_records_v1.npy'),np.load(p/'high_oracle_meta_records_v1.npy'))
 identical_results=json.loads((q/'high_oracle_meta_fixture_v1.json').read_text())==json.loads((p/'high_oracle_meta_fixture_v1.json').read_text())
 assert identical_records and identical_results
 ns={'__file__':str(q/'high_oracle_meta_fixture_v1.py')};exec((q/'high_oracle_meta_fixture_v1.py').read_text().split('N=1024;')[0],ns)
 I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);Pdata=[np.eye(4),np.kron(Z,Z)]
 # Assemble the full physical isometry data*memory -> data*flag*memory, not only supplied Bell branch blocks.
 V=sum(np.kron(P,v) for P,v in zip(Pdata,ns['Vs']))
 assert np.max(abs(V.conj().T@V-np.eye(16)))<1e-13
 phi=np.eye(4).reshape(-1)/2;bell=[np.kron(np.eye(4),P)@phi for P in Pdata]
 rng=np.random.default_rng(97105);floor=(1+np.sqrt(1-.2**2)*np.cos(.02))/2;maxfloor=0;maxbranch=0;maxeffect=0
 for trial in range(50):
  z=rng.normal(size=(4,5))+1j*rng.normal(size=(4,5));mem=z@z.conj().T;mem/=np.trace(mem)
  initial=np.kron(np.outer(phi,phi.conj()),mem);full=np.kron(np.eye(4),V)@initial@np.kron(np.eye(4),V).conj().T
  blocks,sig=ns['emit'](mem)
  score=0
  for m,b in enumerate(bell):
   K=np.kron(b.conj()[None,:],np.eye(8));direct=K@full@K.conj().T
   maxbranch=max(maxbranch,float(np.max(abs(direct-blocks[m]))))
   effect=(I+(-1)**m*X)/2
   # Direct full Hilbert-space positive effect vs reduced flag formula.
   prob=np.trace(np.kron(np.outer(b,b.conj()),np.kron(effect,np.eye(4)))@full).real
   short=np.trace(effect@sig[m]).real;maxeffect=max(maxeffect,abs(prob-short));score+=prob
  maxfloor=max(maxfloor,abs(score-floor))
 assert maxfloor<1e-13 and maxbranch<1e-13 and maxeffect<1e-13
out={'temporary_replay_3072_records_identical':identical_records,'temporary_replay_results_identical':identical_results,'independent_full_isometry_fixtures':50,'max_full_vs_branch_state_error':maxbranch,'max_direct_success_probability_error':maxeffect,'exact_fixed_X_receiver_score':floor,'max_score_variation_from_exact_formula':maxfloor,'scope':'Floating trajectory replay and independent physical-isometry algebra; no confidence claim or exact finite OGD/EXP3 implementation.'}
pathlib.Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
