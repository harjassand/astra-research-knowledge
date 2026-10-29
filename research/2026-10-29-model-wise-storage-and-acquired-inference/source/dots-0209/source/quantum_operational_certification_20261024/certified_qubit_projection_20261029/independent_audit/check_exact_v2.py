from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,gzip,hashlib,runpy
import numpy as np
P=Path(__file__).resolve().parents[1]
ns=runpy.run_path(str(Path(__file__).with_name('check_exact_v1.py')));validate=ns['validate'];vec=ns['vec']
files=[];out={}
def replay(records,certs,seed,N,meta):
 assert len(records)==N and list(records[:,1])==list(range(1,N+1))
 expect=[int(r[1]) for r in records if not meta or r[2]==0]
 assert [c['t'] for c in certs]==expect and all(c['seed']==seed for c in certs)
 known=[0] if meta else [];K=15 if meta else 16
 old=[[F(1),F(0),F(0),F(0)]]+([[F(0)]*4] if meta else [])
 maximum=F(0);it=iter(certs)
 for rec in records:
  if meta and rec[2]==1:continue
  if meta:_,t,role,x,wi,b,arm,z=map(int,rec)
  else:_,t,x,wi,b=map(int,rec)
  assert 0<=x<16 and 0<=wi<4 and b in [-1,1]
  c=next(it)
  if x not in known:
   default=old.pop();old.append([z/K for z in default]);known.append(x);K-=1
   if K:old.append([z*F(K,K+1) for z in default])
  old[known.index(x)][wi]+=F((2 if meta else 1)*b,isqrt(N))
  assert old==list(map(vec,c['input_Y']))
  assert list(map(int,c['multiplicities']))==[1]*len(known)+([K] if K else [])
  gap=validate(c);assert gap<=F(c['xi'])==F(1,256*N*N)
  maximum=max(maximum,gap);old=list(map(vec,c['output_E']))
 return {'certificates':len(certs),'maximum_gap':float(maximum)}
for seed in [7301,7302,7303]:
 stem=f'memory_certificates_seed{seed}_N4096_v2.json.gz';r=f'memory_records_seed{seed}_N4096_v2.npy'
 with gzip.open(P/stem,'rt') as f:certs=json.load(f)
 records=np.load(P/r);assert records.shape==(4096,5) and all(records[:,0]==seed)
 out[f'memory_{seed}']=replay(records,certs,seed,4096,False);files+=[stem,r]
records=np.load(P/'meta_records_N1024_v2.npy');assert records.shape==(3072,8)
for seed in [9201,9202,9203]:
 stem=f'meta_certificates_seed{seed}_N1024_v2.json.gz'
 with gzip.open(P/stem,'rt') as f:certs=json.load(f)
 out[f'meta_{seed}']=replay(records[records[:,0]==seed],certs,seed,1024,True);files.append(stem)
files+=['meta_records_N1024_v2.npy','certified_projection_v2.py','run_memory_v2.py','run_certified_meta_v2.py','memory_summary_N4096_v2.json','meta_summary_N1024_v2.json']
out['hashes']={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in files}
out['scope']='All stored learner projection certificates and exact record-to-iterate chains. No exact physical-source or EXP3 arithmetic claim.'
(Path(__file__).parent/'check_exact_v2.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
