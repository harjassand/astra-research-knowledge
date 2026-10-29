"""Independent conditional-instrument replay of recorded mixed roles (float physics)."""
from pathlib import Path
from fractions import Fraction
import numpy as np,json,gzip
P=Path(__file__).resolve().parents[1]
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);pa=np.array([I,X,Y,Z]);unit=np.eye(4,dtype=complex)
for angle,A,B in [(.37,X,X),(.53,Z,Y),(.29,Y,I)]:unit=(np.cos(angle)*np.eye(4)-1j*np.sin(angle)*np.kron(A,B))@unit
coupling=np.cos(.01)*np.eye(8)-1j*np.sin(.01)*np.kron(Z,np.kron(I,X))
V=[]
for m in range(2):
 flag=np.array([np.sqrt(.6),(-1)**m*np.sqrt(.4)])[:,None]
 proj=np.kron(np.diag([int(m==0),int(m==1)]),I)
 V.append(coupling@np.kron(flag,proj@unit))
def mat(e):return sum(float(Fraction(x))*a for x,a in zip(e,pa))
def conditional(block,e):return sum(e[b,a]*block[a*4:(a+1)*4,b*4:(b+1)*4] for a in range(2) for b in range(2))
records=np.load(P/'meta_records_N1024_v2.npy');summary=json.loads((P/'meta_summary_N1024_v2.json').read_text());results=[]
for run in summary['runs']:
 seed=run['seed'];mem=np.ones((4,4))/4;M=np.zeros((16,2,2),complex);M[0]=I;known=[0];K=15;weights=np.array([.9,.1]);scores=np.zeros(4);minprob=1.;maxterr=0.
 with gzip.open(P/f'meta_certificates_seed{seed}_N1024_v2.json.gz','rt') as f:certs={c['t']:c for c in json.load(f)}
 for rec in records[records[:,0]==seed]:
  _,t,role,x,wi,b,arm,z=map(int,rec);m=int(x==15);assert x in [0,15]
  blocks=[v@mem@v.conj().T for v in V];sig=[np.array([[np.trace(bl[a*4:(a+1)*4,bb*4:(bb+1)*4]) for bb in range(2)] for a in range(2)]) for bl in blocks]
  p=(31/32)*weights+1/64
  base=np.trace(sig[0]).real;learn=sum(np.trace(M[l]@s).real for l,s in zip([0,15],sig));fixed=sum(np.trace((I+(-1)**j*X)/2@s).real for j,s in enumerate(sig));meta=p@[base,learn];scores+=[base,learn,fixed,meta]
  if t==run['terminal']['t']:
   maxterr=max(abs(base-run['terminal']['baseline_score']),abs(learn-run['terminal']['learner_score']),abs(meta-run['terminal']['meta_averaged_score']))
   assert np.max(abs(p-run['terminal']['meta_probabilities']))<1e-12
  if role==0:
   effect=I if wi==0 else (I+b*pa[wi])/2
   post=conditional(blocks[m],effect)
   if x not in known:known.append(x);K-=1
   effects=list(map(mat,certs[t]['output_E']));M=np.zeros((16,2,2),complex)
   for label,e in zip(known,effects):M[label]=e
   if K:
    for label in set(range(16))-set(known):M[label]=effects[-1]/K
  else:
   assert arm in [0,1]
   if arm==0:assert z==0
   effect=I if arm==0 else M[z];post=conditional(blocks[m],effect)
   weights[arm]*=np.exp(-int(z!=x)/(128*.75*p[arm]));weights/=sum(weights)
  prob=np.trace(post).real;assert prob>0;minprob=min(minprob,prob)
  mem=post/prob;mem=(mem+mem.conj().T)/2
  assert np.linalg.eigvalsh(mem)[0]>-1e-12
 expected=np.array([run['average_baseline_score'],run['average_predictable_learner_score'],run['average_informed_fixed_X_score'],run['average_meta_score']]);err=max(abs(scores/1024-expected));assert err<1e-12 and maxterr<1e-12
 assert np.max(abs(weights-run['final_meta_weights']))<1e-12
 results.append({'seed':seed,'maximum_average_score_difference':err,'terminal_score_difference':maxterr,'minimum_realized_branch_probability':minprob})
old=np.load(P.parent/'baseline_protected_flag_recovery_20261028/high_oracle_meta_records_v1.npy')
result={'runs':results,'records_identical_to_original_float_fixture':bool(np.array_equal(records,old)),'scope':'Independent float conditional-instrument replay; exact learner certificates reviewed separately. No statistical significance or exact EXP3 arithmetic.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
