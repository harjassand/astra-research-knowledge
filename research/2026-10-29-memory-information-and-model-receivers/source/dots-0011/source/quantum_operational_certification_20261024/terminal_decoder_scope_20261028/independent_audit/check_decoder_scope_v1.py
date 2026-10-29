"""Independent bit-symplectic family and polynomial enumeration."""
from pathlib import Path
import numpy as np, sympy as s, itertools,json,hashlib,sys
D=Path(__file__).parent;A=D.parent;Q=A.parent
chars='IXYZ';n=5
def bits(word):return (sum((c in 'XY')<<(4-i) for i,c in enumerate(word)),sum((c in 'YZ')<<(4-i) for i,c in enumerate(word)))
gens=[bits(w) for w in ['XZZXI','IXZZX','XIXZZ','ZXIXZ']]
stab=[]
for mask in range(16):
 x=z=0
 for j,(a,b) in enumerate(gens):
  if mask>>j&1:x^=a;z^=b
 stab.append((x,z))
def anti(a,b):return ((a[0]&b[1]).bit_count()+(a[1]&b[0]).bit_count())%2
def wt(a):return (a[0]|a[1]).bit_count()
p=s.symbols('p');hist={};records=[]
errors=[(x,z) for x in range(32) for z in range(32)]
for kx,kz in itertools.product(range(16),repeat=2):
 x=(31^stab[kx][0],stab[kx][1]);z=(stab[kz][0],31^stab[kz][1]);y=(x[0]^z[0],x[1]^z[1]);weights=[wt(x),wt(y),wt(z)]
 assert anti(x,z)==1 and min(weights)>=3
 assert all(anti(x,g)==anti(z,g)==0 for g in gens)
 counts=[0]*6
 for e in errors:
  if not anti(e,x) and not anti(e,z):counts[wt(e)]+=1
 polynomial=s.Poly(sum(counts[w]*(p/3)**w*(1-p)**(5-w) for w in range(6)),p)
 target=s.Poly((1+sum((1-4*p/3)**w for w in weights))/4,p)
 assert polynomial==target
 coefficient=str(s.Rational(sum(weights),3));hist[coefficient]=hist.get(coefficient,0)+1
 records.append({'kx':kx,'kz':kz,'weights':weights,'logical_identity_error_counts_by_weight':counts})
assert hist=={'5':6,'13/3':90,'11/3':90,'3':70}
author=json.loads((A/'bare_decoder_obstruction_check_v1.json').read_text());assert author['histogram']==hist
for mine,theirs in zip(records,author['rows']):assert mine['weights']==theirs['weights']
# Reduced maps are a unital Pauli *-homomorphism in Heisenberg form: TP/CP follows.
# Exactly 256 distinct pairs, each same logical action, all fail at least one weight1 error.
for row in records:
 k=row['kz'];z=(stab[k][0],31^stab[k][1]);assert any(anti(e,z) for e in errors if wt(e)==1)
out={'status':'PASS_EXACT_RESTRICTED_DECODER_FAMILY_AND_POLYNOMIAL_OBSTRUCTION','number_of_extensions':256,'histogram':hist,'enumerated_physical_error_words_per_extension':1024,'polynomial_identity_exact':True,'sha256':{str(p.relative_to(Q)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [A/'GOVERNING_DECODER_EXTENSION_v1.md',A/'compare_decoder_extensions_v1.py',A/'check_bare_decoder_obstruction_v1.py',A/'bare_decoder_obstruction_check_v1.json',Path(__file__)]}}
(D/'check_decoder_scope_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
