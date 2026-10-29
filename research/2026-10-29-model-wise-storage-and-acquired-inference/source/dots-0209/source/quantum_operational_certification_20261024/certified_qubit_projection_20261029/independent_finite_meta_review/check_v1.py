from pathlib import Path
from fractions import Fraction as F
from math import isqrt,factorial
import numpy as np,json,gzip,random,sys,hashlib
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P))
from exact_meta_arithmetic_v1 import ExactMeta,exp_factor,rational_coin
# Reuse the prior independent exact weak-duality verifier, without executing its file I/O.
source=(P/'independent_audit/check_exact_v1.py').read_text().split('certs=json.loads',1)[0]
ns={'__file__':str(P/'independent_audit/check_exact_v1.py')};exec(source,ns);validate=ns['validate'];vec=ns['vec']
def bounded_json_gzip(path,limit=32*1024*1024):
 with gzip.open(path,'rb') as f:blob=f.read(limit+1)
 assert len(blob)<=limit;return json.loads(blob)
def check_factor(n,d):
 q,rho=exp_factor(n,d);D=1<<64;xx=F(n,d);lo=F(n*D//d,D);hi=lo if lo==xx else lo+F(1,D)
 # Independently form exact Taylor polynomials by powers/factorials.
 lower=sum((-hi)**j/F(factorial(j)) for j in range(34));upper=sum((-lo)**j/F(factorial(j)) for j in range(33))
 assert F(q,D)<=lower<=upper and (lower-F(q,D))<F(1,D)
 assert rho>= (upper-F(q,D))/lower and rho<F(1,2)
 assert rho<=F(5,D)
 return q,rho
manifest=json.loads((P/'FINITE_META_REVIEW_INPUTS_v1.json').read_text())
for item in manifest['files']:
 path=P/item['path'];assert path.stat().st_size==item['bytes'];assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
records=np.load(P/'finite_meta_records_N1024_v1.npy',allow_pickle=False);summary=json.loads((P/'finite_meta_summary_N1024_v1.json').read_text());assert records.shape==(3072,8)
# Source replay follows previous independent occupation reviewer, not author emit/update.
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);pa=np.array([I,X,Y,Z]);U=np.eye(4,dtype=complex)
for angle,A,B in [(.37,X,X),(.53,Z,Y),(.29,Y,I)]:U=(np.cos(angle)*np.eye(4)-1j*np.sin(angle)*np.kron(A,B))@U
C=np.cos(.01)*np.eye(8)-1j*np.sin(.01)*np.kron(Z,np.kron(I,X));Vs=[]
for m in range(2):
 flag=np.array([np.sqrt(.6),(-1)**m*np.sqrt(.4)])[:,None];proj=np.kron(np.diag([int(m==0),int(m==1)]),I);Vs.append(C@np.kron(flag,proj@U))
def mat(e):return sum(float(F(v))*p for v,p in zip(e,pa))
def post(bl,E):return sum(E[b,a]*bl[a*4:(a+1)*4,b*4:(b+1)*4] for a in range(2) for b in range(2))
results=[];allcert=0
for run in summary['runs']:
 seed=run['seed'];rr=records[records[:,0]==seed];assert list(rr[:,1])==list(range(1,1025))
 cs=bounded_json_gzip(P/f'meta_certificates_seed{seed}_N1024_finite_meta_v1.json.gz');assert [c['t'] for c in cs]==[int(r[1]) for r in rr if r[2]==0]
 certs={c['t']:c for c in cs};known=[0];K=15;old=[[F(1),F(0),F(0),F(0)],[F(0)]*4]
 exact=ExactMeta(1024);private=random.Random(seed+100000);maxgap=F(0);mem=np.ones((4,4))/4;M=np.zeros((16,2,2),complex);M[0]=I;scores=np.zeros(4);minprob=1.
 for rec in rr:
  _,t,role,x,wi,b,arm,z=map(int,rec);m=int(x==15);assert x in [0,15]
  n,d=exact.probability();p=np.array([n/d,(d-n)/d]);assert F(1,64)<=F(n,d)<=F(63,64)
  blocks=[v@mem@v.conj().T for v in Vs];sig=[np.array([[np.trace(bl[a*4:(a+1)*4,bb*4:(bb+1)*4]) for bb in range(2)] for a in range(2)]) for bl in blocks]
  vals=[np.trace(sig[0]).real,sum(np.trace(M[l]@s).real for l,s in zip([0,15],sig)),sum(np.trace((I+(-1)**j*X)/2@s).real for j,s in enumerate(sig))];scores+=vals+[p@vals[:2]]
  expected_role=0 if private.getrandbits(2)==0 else 1;assert role==expected_role
  if not role:
   effect=I if wi==0 else (I+b*pa[wi])/2;new=post(blocks[m],effect)
   if x not in known:
    default=old.pop();old.append([v/K for v in default]);known.append(x);K-=1
    if K:old.append([v*F(K,K+1) for v in default])
   old[known.index(x)][wi]+=F(b,16);c=certs[t]
   assert list(map(vec,c['input_Y']))==old and list(map(int,c['multiplicities']))==[1]*len(known)+[K]
   gap=validate(c);assert gap<=F(c['xi'])==F(1,256*1024**2);maxgap=max(maxgap,gap);old=list(map(vec,c['output_E']))
   M=np.zeros((16,2,2),complex)
   for label,e in zip(known,old):M[label]=mat(e)
   for label in set(range(16))-set(known):M[label]=mat(old[-1])/K
  else:
   assert arm==exact.select(private)
   if arm==0:assert z==0
   new=post(blocks[m],I if arm==0 else M[z]);loss=int(z!=x)
   if loss:check_factor(d,3*32*(n if arm==0 else d-n))
   exact.update(arm,loss)
  prob=np.trace(new).real;assert prob>0;minprob=min(minprob,prob);mem=new/prob;mem=(mem+mem.conj().T)/2;assert np.linalg.eigvalsh(mem)[0]>-1e-12
 assert exact.budgets()==run['exact_meta_budgets']
 expected=[run[k] for k in ['average_baseline_score','average_predictable_learner_score','average_informed_fixed_X_score','average_meta_score']];scoreerr=max(abs(scores/1024-expected));assert scoreerr<1e-12
 allcert+=len(cs);results.append({'seed':seed,'certificates':len(cs),'max_gap':float(maxgap),'private_expert_bits':exact.coin_bits,'role_bits_additional':2048,'weight_bits':exact.max_weight_bits,'score_replay_error':float(scoreerr),'min_realized_branch_probability':float(minprob),'exact_ledger_match':True})
# Endpoint factors and deliberately capped failure: flags cannot be omitted.
for x in [F(0),F(1,3),F(2,3),F(1,1<<64),F(2,3)-F(1,1<<80)]:check_factor(x.numerator,x.denominator)
class Reject:
 def getrandbits(self,b):return (1<<b)-1
assert rational_coin(1,3,Reject(),128)==(0,True,256)
class Enumerate:
 def __init__(self,u):self.u=u
 def getrandbits(self,b):return self.u
for d in range(1,100):
 for n in range(d+1):
  outcomes=[rational_coin(n,d,Enumerate(u),1) for u in range(d)]
  assert sum(o[0]==0 for o in outcomes)==n and not any(o[1] for o in outcomes)
stress=json.loads((P/'check_finite_dual_v4.json').read_text());passed=[];failed=[]
for c in stress['cases']:
 if c.get('certified',False):assert validate(c)<=F(c['xi']);passed.append(c)
 else:failed.append({'K_power':c['K_power'],'trial':c['trial'],'failure':c.get('failure')})
assert len(passed)==58 and len(failed)==2
repairs=json.loads((P/'repaired_face_certificates_v5.json').read_text())
failed_inputs=[(c['input_Y'],c['multiplicities']) for c in stress['cases'] if not c.get('certified',False)]
assert len(repairs)==2
for c in repairs:
 assert (c['input_Y'],c['multiplicities']) in failed_inputs
 assert validate(c)<=F(c['xi'])==F(1,10**9)
out={'manifest_hashes_match':True,'recorded_calls':3072,'certificates':allcert,'runs':results,'v5_same_input_certificates_checked':len(repairs),'v4_stress_passed':len(passed),'v4_fail_closed':failed,'scope':'Exact classical ledger/role/expert replay and all stored projection certificates; floating conditional-source replay only. No quantum-source exactness or generic solver termination.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
