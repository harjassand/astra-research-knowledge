"""Independent rational validation, never imports the proposal/repair solver."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json, hashlib
import numpy as np
P=Path(__file__).resolve().parents[1]
def vec(x): return list(map(F,x))
def norm(x):return sum(y*y for y in x)
def validate(c):
 Y=list(map(vec,c['input_Y'])); E=list(map(vec,c['output_E']));L=vec(c['dual_L']);ks=list(map(int,c['multiplicities']))
 assert len(E)==len(Y)==len(ks)>0 and all(k>0 for k in ks)
 assert all(len(x)==4 for x in E+Y+[L])
 assert all(e[0]>=0 and e[0]**2>=norm(e[1:]) for e in E)
 assert [sum(e[j] for e in E) for j in range(4)]==[1,0,0,0]
 primal=sum(2*sum((e[j]-y[j])**2 for j in range(4))/k for e,y,k in zip(E,Y,ks))
 dual=-2*L[0]+sum(2*norm(y)/k for y,k in zip(Y,ks))
 D=1<<int(c['interval_bits'])
 for y,k in zip(Y,ks):
  v=[2*y[j]/k-L[j] for j in range(4)];r2=norm(v[1:]);a=isqrt(r2.numerator*D*D//r2.denominator);lo=F(a,D);hi=lo if lo*lo==r2 else F(a+1,D)
  assert lo*lo<=r2<=hi*hi
  dual-=F(k,4)*(max(F(0),v[0]+hi)**2+max(F(0),v[0]-lo)**2)
 assert primal==F(c['primal']) and dual==F(c['dual_lower'])
 gap=primal-dual;assert gap==F(c['gap']) and gap>=0
 return gap
certs=json.loads((P/'memory_certificates_N64_v1.json').read_text());records=np.load(P/'memory_records_N64_v1.npy')
assert records.shape==(192,5) and len(certs)==192
assert len(set((c['seed'],c['t']) for c in certs))==192
maximum=F(0)
for seed in [7301,7302,7303]:
 rr=records[records[:,0]==seed];cc=[c for c in certs if c['seed']==seed]
 assert len(rr)==len(cc)==64 and list(rr[:,1])==list(range(1,65))
 known=[];K=16;old=[[F(1),F(0),F(0),F(0)]]
 for rec,c in zip(rr,cc):
  _,t,x,wi,b=map(int,rec);assert c['t']==t and 0<=x<16 and 0<=wi<4 and b in [-1,1]
  if x not in known:
   default=old.pop();old.append([z/K for z in default]);known.append(x);K-=1
   if K:old.append([z*F(K,K+1) for z in default])
  old[known.index(x)][wi]+=F(b,8)
  assert old==list(map(vec,c['input_Y']))
  assert list(map(int,c['multiplicities']))==[1]*len(known)+([K] if K else [])
  gap=validate(c);assert gap<=F(c['xi'])==F(1,1048576)
  maximum=max(maximum,gap);old=list(map(vec,c['output_E']))
assert np.array_equal(records,np.load(P.parent/'compact_prequential_flag_recovery_20261028/quantum_memory_records_v1.npy'))
extreme=json.loads((P/'check_extreme_K_v1.json').read_text())['cases'];assert [c['K_power'] for c in extreme]==[60,120,512,2048]
for c in extreme: assert validate(c)<=F(1,10**7)
files=['certified_projection_v1.py','run_memory_v1.py','memory_certificates_N64_v1.json','memory_records_N64_v1.npy','memory_summary_N64_v1.json','check_extreme_K_v1.py','check_extreme_K_v1.json','independent_collective_review/check_certificates_v1.py','independent_collective_review/check_certificates_v1.json']
out={'status':'PASS_SCOPED','memory_certificates':192,'exact_record_chain_steps':192,'extreme_K_powers':[60,120,512,2048],'maximum_memory_gap':float(maximum),'hashes':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in files},'scope':'Exact feasibility and objective gap of recorded outputs; same-record replay for N64. Extreme K certificates use a separate candidate factory, not the public project_certified route. No generic solver termination/scaling, physical experiment, or performance advantage claim.'}
(Path(__file__).parent/'check_exact_v1.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
