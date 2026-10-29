"""Actual CP Pauli ledgers and received35-qubit total outer decoding, SOS/six-state only."""
import sys,json,numpy as np
from pathlib import Path
P=Path(__file__).parent;Q=P/'received_dependencies/outer_grs_distillation_20261028';sys.path.insert(0,str(Q))
from grs_wrapper_v1 import GF,construct,decoded_error,decode_syndrome
z=np.load(P/'maps_and_fixture.npz');E=z['E_sos'];U=z['source_unitary'];sigma=z['sigma'];I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);ps=[I,X,Y,Z]
# Complete fixed-isometry decoder, not merely E† compression.
Qe=np.linalg.qr(E,mode='complete')[0];Ds=[E.conj().T]
for w in Qe[:,2:].T:
 D=np.zeros((2,16),complex);D[0]=w.conj();Ds.append(D)
Ls=[(np.kron(D,I)@U@np.kron(E,I)).reshape(2,2,2,2) for D in Ds]
def superof(As):return sum(np.einsum('ab,cd->acbd',A,A.conj()).reshape(4,4) for A in As)
paulimaps=[]
for p in ps:
 Bs=[np.einsum('ba,aibj->ij',p.conj().T,L)/2 for L in Ls];paulimaps.append(superof(Bs))
resI=np.linalg.norm(paulimaps[0]-z['sos_completed_good']);resS=np.linalg.norm(sum(paulimaps)-z['sos_service']);assert max(resI,resS)<1e-12
rng=np.random.default_rng(2991635);g=GF(5,37);code=construct(g,31,6);r=code['s'];ell=code['ell'];fmap={sum(g.trace(g.mul(f,1<<j))<<j for j in range(5)):f for f in range(32)}
rows=[];acc=0;aborted=0;decoder_failures=0;paulifaults=[]
for trial in range(300):
 bath=sigma.reshape(-1).copy();ledger=[];stop='cap'
 for call in range(1400):
  if rng.random()<.4:
   probs=np.array([np.trace((T@bath).reshape(2,2)).real for T in paulimaps]);probs=np.maximum(probs,0);probs/=probs.sum();k=int(rng.choice(4,p=probs));bath=paulimaps[k]@bath;bath/=bath[0]+bath[3];ledger.append(k)
   if len(ledger)==155:stop='accept';break
  else:
   pp=float(np.trace((z['sos_six_pass']@bath).reshape(2,2)).real)
   if rng.random()<pp:bath=z['sos_six_pass']@bath;bath/=bath[0]+bath[3]
   else:stop='test_fail';break
 if stop!='accept':aborted+=1;continue
 acc+=1;e=[];f=[]
 for i in range(31):
  block=ledger[5*i:5*i+5];e.append(sum((k in [1,2])<<j for j,k in enumerate(block)));phase=sum((k in [2,3])<<j for j,k in enumerate(block));f.append(fmap[phase])
 dx,dz=decoded_error(g,code,e,f);last=dx[r+ell:];se=[g.dot(row,last) for row in code['HRt']];sf=dx[:r]
 # decoded_error already applies Fourier on first r, so phase syndrome is dx[:r].
 eh,okx=decode_syndrome(g,code,se);fh,okz=decode_syndrome(g,code,sf);cx,cz=decoded_error(g,code,eh,fh)
 corrected=all(dx[i]==cx[i] and dz[i]==cz[i] for i in range(r,r+ell));decoder_failures+=not corrected
 faults=sum(k!=0 for k in ledger);paulifaults.append(faults);rows.append({'trial':trial,'calls':call+1,'native_pauli_faults':faults,'outer_decoder_flags':[bool(okx),bool(okz)],'logical_residual_zero':bool(corrected)})
 if faults<=6:assert corrected
res={'scope':'300 independent counterfactual single-guard simulations each starting from the SAME ACTUAL final training bath, not bath-reset deployment or long-run throughput. Within each attempt bath is retained and updated. Fixed SOS candidate/six-state policy; truth only evaluator.','trials':300,'accepted':acc,'aborted':aborted,'actual_total_outer_decoder_failures':int(decoder_failures),'Pauli_I_CP_map_residual':float(resI),'Pauli_sum_CP_map_residual':float(resS),'outer_length':31,'outer_radius':6,'payload_qubits':35,'max_accepted_native_faults':max(paulifaults,default=0),'accepted_runs':rows}
(P/'sampled_decoder_results.json').write_text(json.dumps(res,indent=2)+'\n');print({k:v for k,v in res.items() if k!='accepted_runs'})
