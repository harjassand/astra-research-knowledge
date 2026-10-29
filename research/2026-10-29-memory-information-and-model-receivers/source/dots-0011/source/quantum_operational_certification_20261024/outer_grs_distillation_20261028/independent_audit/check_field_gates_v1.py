import json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent; R=D.parent
A=json.loads((R/'field_and_gate_checks_v1.json').read_text()); S=json.loads((R/'exact_wrapper_checks_v1.json').read_text())
def rem(x,f):
 while x.bit_length()>=f.bit_length(): x^=f<<(x.bit_length()-f.bit_length())
 return x
def mul(x,y,f):
 z=0
 while y:
  if y&1:z^=x
  x<<=1;y>>=1
 return rem(z,f)
def irr(f):
 h=f.bit_length()-1
 return all(rem(f,g) for k in range(1,h//2+1) for g in range(1<<k,1<<(k+1)))
def act(x,gates):
 for name,a,b in gates:
  if name=='CX':x^=((x>>a)&1)<<b
  elif name=='SWAP':
   u=((x>>a)^(x>>b))&1;x^=(u<<a)|(u<<b)
  else:raise ValueError(name)
 return x
for row in A['fields']:
 h=row['h'];f=int(row['polynomial_bits'],2)
 assert irr(f)
 candidates=list(range((1<<h)|1,f+1,2))
 assert len(candidates)==row['candidates_tested']
 assert not any(irr(g) for g in candidates[:-1])
checks=[]
for row in A['cases']:
 h,B,t=row['h'],row['B'],row['t']
 source=next(x for x in S['cases'] if (x['m'],x['construction']['B'],x['construction']['t'])==(h,B,t))
 f=int(source['irreducible_polynomial_bits'],2);c=source['construction'];nb=B*h
 for tag,mat in [('encoder',c['T']),('decoder',c['Ti'])]:
  gates=row['binary_'+tag+'_linear_gates']
  for bit in range(nb):
   i,k=divmod(bit,h);want=0
   for j in range(B):want|=mul(1<<k,mat[i][j],f)<<(j*h)
   assert act(1<<bit,gates)==want
 # H followed by this linear map must implement Tr(xy) Fourier, not dot-product Fourier.
 G=row['trace_Gram'];gates=[]
 for kind,i,j,a in row['trace_Fourier_after_H_linear_gates']:
  assert kind in ('swap','add') and (kind=='swap' or a==1)
  gates.append(('SWAP' if kind=='swap' else 'CX',i,j))
 for x in range(1<<h):
  for y0 in range(1<<h):
   y=act(y0,gates);v=mul(x,y,f);tr=0
   for _ in range(h):tr^=v;v=mul(v,v,f)
   assert tr in (0,1) and tr==((x&y0).bit_count()%2)
 checks.append({'h':h,'B':B,'t':t,'linear_basis_checks':2*nb,'Fourier_amplitude_sign_checks':1<<(2*h)})
out={'status':'PASS','irreducibles_independently_trial_factored':len(A['fields']),'cases':checks,'source_sha256':hashlib.sha256((R/'field_and_gate_checks_v1.json').read_bytes()).hexdigest(),'scope':'Independent polynomial trial division and execution of saved elementary binary gates; no imported author routines.'}
(D/'field_gate_results_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
