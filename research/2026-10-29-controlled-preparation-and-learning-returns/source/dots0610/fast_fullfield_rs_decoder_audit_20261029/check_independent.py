import sys,itertools,json,time,random
import numpy as np
from pathlib import Path
p=Path(__file__).parent;s=p.parent/'fast_fullfield_rs_decoder_20261029';sys.path.insert(0,str(s))
from fast_rs import Field,CSSDecoder,Compiler
# Independent polynomial arithmetic, not author's tables.
def mul(a,b,q,mod):
 c=0
 while b:
  if b&1:c^=a
  b>>=1;a<<=1
  if a&q:a^=mod
 return c
def moment(e,n,q,mod):
 out=[]
 for j in range(n):
  z=0
  for i,a in enumerate(e):
   v=1
   for _ in range(j):v=mul(v,i,q,mod)
   z^=mul(a,v,q,mod)
  out.append(z)
 return tuple(out)
f=Field(3,11);q=8;t=2;dictionary={}
for w in range(t+1):
 for loc in itertools.combinations(range(q),w):
  for amps in itertools.product(range(1,q),repeat=w):
   e=[0]*q
   for i,a in zip(loc,amps):e[i]=a
   S=moment(e,2*t,q,11);assert S not in dictionary;dictionary[S]=e
success=failure=0;cases={}
for S in itertools.product(range(q),repeat=2*t):
 e,ok,detail=f.decode(S,t)
 assert ok==(S in dictionary)
 if ok:assert list(e)==dictionary[S];success+=1
 else:assert not np.any(e);failure+=1
 cases[detail['case']]=cases.get(detail['case'],0)+1
# Full actual binary Pauli propagation, without field-transpose implementation.
rng=random.Random(202610290459);readout_checks=[]
for h,mod,t in [(3,11,1),(4,19,3),(5,37,5)]:
 d=CSSDecoder(h,mod,t);c=Compiler(h,mod);q=1<<h
 for rep in range(60):
  support=rng.sample(range(q),rng.randrange(t+1));e=np.zeros(q,np.uint16);z=e.copy()
  for i in support:e[i]=rng.randrange(q);z[i]=rng.randrange(q)
  xb=np.array([(int(a)>>j)&1 for a in e for j in range(h)],np.uint8)
  zb=np.array([(int(d.f.phase_codes[a])>>j)&1 for a in z for j in range(h)],np.uint8)
  for a,b in reversed(c.bits):xb[b]^=xb[a];zb[a]^=zb[b]
  xp=np.array([sum(int(xb[i*h+j])<<j for j in range(h)) for i in range(q)],np.uint16)
  zp=np.array([sum(int(zb[i*h+j])<<j for j in range(h)) for i in range(q)],np.uint16)
  read=(xp[-2*t:],zp[:2*t]);eh,zh,ok,detail=d.decode_readout(*read)
  assert ok and np.array_equal(eh,e) and np.array_equal(zh,z)
  xc,zc=d.logical_correction_bits(eh,zh)
  assert np.array_equal(xc,xp[2*t:-2*t]) and np.array_equal(zc,zp[2*t:-2*t])
 readout_checks.append({'h':h,'t':t,'binary_CNOT_readout_and_logical_correction_cases':60})
# Individually correctable streams on disjoint supports must not certify joint t-radius.
d=CSSDecoder(3,11,1);e=np.zeros(8,np.uint16);z=e.copy();e[0]=2;z[1]=3
eh,zh,ok,_=d.decode_readout(*d.actual_readout(e,z));assert not ok and np.array_equal(e,eh) and np.array_equal(z,zh)
out={'exhaustive_GF8_t2_syndromes':q**0*4096,'exact_representatives':success,'rejected_nonrepresentable':failure,'branch_counts':cases,'independent_polynomial_moment_dictionary':True,'actual_binary_readout_cases':readout_checks,'disjoint_XZ_support_rejected':True,'scope':'Finite exact checks; exhaustive arbitrary syndrome test includes valid and nonrepresentable syndromes, not a detector of all physical above-radius errors.'}
(p/'independent_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
