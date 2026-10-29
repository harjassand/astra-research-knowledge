from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,hashlib
import numpy as np
P=Path(__file__).resolve().parents[1]
certs=json.loads((P/'memory_certificates_N64_v1.json').read_text());records=np.load(P/'memory_records_N64_v1.npy')
def norm2(v):return sum(x*x for x in v)
def pos(v):return v[0]>=0 and v[0]*v[0]>=norm2(v[1:])
def parse(v):return list(map(F,v))
def rootbound(x,bits=192):
 D=1<<bits;v=isqrt(x.numerator*D*D//x.denominator);lo=F(v,D);hi=lo if lo*lo==x else F(v+1,D)
 assert lo*lo<=x<=hi*hi;return lo,hi
maxgap=F(0);chain=0
for seed in [7301,7302,7303]:
 known=[];K=16;old=[[F(1),F(0),F(0),F(0)]]
 for rec,c in zip(records[records[:,0]==seed],[c for c in certs if c['seed']==seed]):
  _,t,x,wi,b=map(int,rec);assert c['t']==t
  if x not in known:
   de=old.pop();old.append([z/K for z in de]);known.append(x);K-=1
   if K:old.append([z*F(K,K+1) for z in de])
  old[known.index(x)][wi]+=F(b,8)
  Y=[parse(v) for v in c['input_Y']];E=[parse(v) for v in c['output_E']];mul=list(map(int,c['multiplicities']));L=parse(c['dual_L'])
  assert old==Y and mul==[1]*len(known)+([K] if K else []);chain+=1
  assert all(pos(e) for e in E)
  assert [sum(e[j] for e in E) for j in range(4)]==[1,0,0,0]
  objective=sum(2*sum((a-b)**2 for a,b in zip(e,y))/k for e,y,k in zip(E,Y,mul))
  lower=-2*L[0]+sum(2*norm2(y)/k for y,k in zip(Y,mul))
  for y,k in zip(Y,mul):
   v=[2*a/k-b for a,b in zip(y,L)];lo,hi=rootbound(norm2(v[1:]));up=[v[0]+hi,v[0]-lo]
   lower-=F(k,4)*sum(max(F(0),z)**2 for z in up)
  assert objective==F(c['primal']) and lower==F(c['dual_lower'])
  gap=objective-lower;assert 0<=gap<=F(1,1048576) and gap==F(c['gap']);maxgap=max(maxgap,gap)
  old=E
oldrec=P.parent/'compact_prequential_flag_recovery_20261028/quantum_memory_records_v1.npy'
assert np.array_equal(records,np.load(oldrec))
result={'exact_certificates_checked':len(certs),'exact_record_to_iterate_chain_checks':chain,'every_output_PSD_and_sumI':True,'dual_normalization_independently_derived':'Lagrange multiplier L for sum E=I; min gives -TrL+sum w||Y||F²-sum||(2wY-L)_+||F²/(4w)','maximum_exact_gap':str(maxgap),'maximum_gap_float':float(maxgap),'xi':'1/1048576','source_records_equal_original':True,'scope':'Exact rational projection certificates and record-driven chain only; source physics remains floating and performance remains negative'}
(Path(__file__).with_suffix('.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
