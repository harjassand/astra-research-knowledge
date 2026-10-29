"""Independent direct decoder wiring from emitted binary gates, not decoded_error."""
from pathlib import Path
import sys,json,random,hashlib
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent/'outer_grs_distillation_20261028'))
from grs_wrapper_v1 import GF,construct,decode_syndrome
rows=json.loads((P/'direct_outer_checks_v1.json').read_text())['cases'];rng=random.Random(991037)
def apply(x,z,gates):
 x=x[:];z=z[:]
 for gate in gates:
  kind,*ij=gate
  if kind=='H':
   i=ij[0];x[i],z[i]=z[i],x[i]
  elif kind=='CX':
   i,j=ij;x[j]^=x[i];z[i]^=z[j]
  elif kind=='SW':
   i,j=ij;x[i],x[j]=x[j],x[i];z[i],z[j]=z[j],z[i]
  else:raise AssertionError(kind)
 return x,z
results=[]
for row in rows:
 B=row['B'];h=row['h'];t=row['t'];n=B*h;g=GF(h,row['field_modulus']);c=construct(g,B,t);a=2*t;ell=B-4*t
 enc=row['binary_encoder_gates'];dec=row['binary_decoder_gates'];assert dec==list(reversed(enc))
 zmap={f:[g.trace(g.mul(f,1<<j)) for j in range(h)] for f in range(g.q)};inv={tuple(z):f for f,z in zmap.items()};assert len(inv)==g.q
 count=0
 cases=[([0]*B,[0]*B)]
 for site in range(B):
  for ex in range(g.q):
   for ez in range(g.q):
    if not(ex or ez):continue
    e=[0]*B;f=[0]*B;e[site]=ex;f[site]=ez;cases.append((e,f))
 for _ in range(100):
  e=[0]*B;f=[0]*B
  for site in rng.sample(range(B),rng.randrange(t+1)):e[site]=rng.randrange(g.q);f[site]=rng.randrange(g.q)
  cases.append((e,f))
 for e,f in cases:
  xb=[(v>>j)&1 for v in e for j in range(h)];zb=sum((zmap[v] for v in f),[])
  xx,zz=apply(xb,zb,dec)
  dx=[sum(xx[i*h+j]<<j for j in range(h)) for i in range(B)]
  sf=dx[:a];last=dx[a+ell:];se=[g.dot(row,last) for row in c['HRt']]
  assert sf==[g.dot(row,f) for row in c['H']] and se==[g.dot(row,e) for row in c['H']]
  eh,ok=decode_syndrome(g,c,se);fh,ok2=decode_syndrome(g,c,sf);assert ok and ok2
  cx,cz=apply([(v>>j)&1 for v in eh for j in range(h)],sum((zmap[v] for v in fh),[]),dec)
  assert all(xx[j]==cx[j] and zz[j]==cz[j] for j in range(a*h,(a+ell)*h))
  # Entire emitted unitary followed by inverse is labelwise identity.
  x=[rng.randrange(2) for _ in range(n)];z=[rng.randrange(2) for _ in range(n)];assert apply(*apply(x,z,enc),dec)==(x,z)
  count+=1
 results.append({'B':B,'h':h,'t':t,'exact_single_site_and_random_fault_checks':count})
result={'status':'PASS','cases':results,'total':sum(r['exact_single_site_and_random_fault_checks'] for r in results),'scope':'Independent emitted-gate propagation and direct single-system ancilla syndrome wiring; accepted total finite-field decoder reused.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
