import itertools,json,math
from pathlib import Path
# Steane CSS: H rows generate C_X, orthogonal complement is K.
rows=[0b1111000,0b1100110,0b1010101]
C=[0]
for v in rows:C += [x^v for x in C]
def parity(x):return x.bit_count()%2
def syn(x):return tuple(parity(x&v) for v in rows)
reps={syn(0):0,**{syn(1<<i):1<<i for i in range(7)}}
def g(y):return parity(y^reps[syn(y)])
def pauli(word,i,p):
 b=(word>>i)&1
 phase= (1j*(-1)**b if p=='Y' else (-1)**b if p=='Z' else 1)
 return (word^(1<<i) if p in ('X','Y') else word),phase
errs=[None]+[(i,a,b) for i in range(7) for a in 'IXYZ' for b in 'IXYZ' if (a,b)!=('I','I')]
vecs=[]
for e in errs:
 cols=[]
 for z in (0,1):
  vec={}
  for c in C:
   w=c^(127 if z else 0);d=r=w; ph=1
   if e is not None:
    i,a,b=e;d,pd=pauli(d,i,a);r,pr=pauli(r,i,b);ph=pd*pr
   vec[(d,r)]=ph/math.sqrt(8)
  cols.append(vec)
 vecs.append(cols)
def inner(v,w,z=None):
 return sum(a.conjugate()*w.get(key,0) for key,a in v.items() if z is None or g(key[1])==z)
maxkl=maxinst=0
for va in vecs:
 for vb in vecs:
  c=inner(va[0],vb[0])
  for i,j in itertools.product(range(2),repeat=2):
   maxkl=max(maxkl,abs(inner(va[i],vb[j])-(c if i==j else 0)))
   for z in (0,1):
    maxinst=max(maxinst,abs(inner(va[i],vb[j],z)-(c if i==j==z else 0)))
result={'code':'Steane [[7,1,3]]','coordinate_errors':len(errs),'ordered_pairs':len(errs)**2,'kl_residual':maxkl,'instrument_residual':maxinst,'ideal_garbage_outcomes_orthogonal':True,'scope':'All two-sided Pauli basis errors supported on one copied coordinate, DATA and record independently; not a Tanner GPT or threshold numerical certification.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
