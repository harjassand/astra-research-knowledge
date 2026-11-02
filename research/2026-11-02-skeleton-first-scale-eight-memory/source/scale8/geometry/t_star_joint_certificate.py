"""Exact joint relative-boundary normal form for the compressed Fig.26 T star.
Not a proof that neighboring gadgets enforce the required trace conditions.
Physical subdivision-to-macroface transport is separately described in proof.
"""
import json

def linbasis(gens):
 d={}
 for j,g in enumerate(gens):
  x=g;c=1<<j
  while x:
   k=x.bit_length()-1
   if k in d:x^=d[k][0];c^=d[k][1]
   else:d[k]=(x,c);break
 return d

def solve(d,x):
 c=0
 while x:
  k=x.bit_length()-1
  if k not in d:return None
  y,z=d[k];x^=y;c^=z
 return c

reports=[]
for name,F in [('blue',[0,7]),('red',[0,3,5,6])]:
 def rep(x):return min((x^f for f in F),key=lambda y:(y.bit_count(),y))
 gens=[]
 for l in range(2):
  for j in range(3):gens.append((1<<(6*l+j))|(1<<(6*l+3+j))|(1<<(12+j)))
 for block in range(5):
  for f in F[1:]:gens.append(f<<(3*block))
 basis=linbasis(gens); admitted=0;examples=[];bad_unmatched=0
 for x in range(1<<15):
  am,ap,bm,bp,c=[(x>>(3*j))&7 for j in range(5)]
  U,V,W=rep(am^ap),rep(bm^bp),rep(ap^bp^c)
  if U!=V or W:continue
  admitted+=1
  residual=U|(U<<6)
  correction=solve(basis,x^residual)
  assert correction is not None
  y=0
  for j,g in enumerate(gens):
   if correction>>j&1:y^=g
  assert x^y==residual
  assert 2*U.bit_count()<=x.bit_count()
  if U and len(examples)<5:examples.append(dict(input=x,residual=residual,coarse=U,correction=correction))
 # Full kernel characterization checks dimensions; independent invariant
 # check that all physical generators have zero U,V,W cosets.
 for g in gens:
  a,p,b,q,c=[(g>>(3*j))&7 for j in range(5)]
  assert rep(a^p)==rep(b^q)==rep(p^q^c)==0
 expected_dim=15-3*(3-(1 if name=='blue' else 2))
 assert len(basis)==expected_dim
 reports.append(dict(old_seam_color=name,quotient_dimension=15-len(basis),generator_rank=len(basis),admitted_patterns=admitted,tested_patterns=32768,examples=examples,passed=True))
print(json.dumps(reports,indent=2))
