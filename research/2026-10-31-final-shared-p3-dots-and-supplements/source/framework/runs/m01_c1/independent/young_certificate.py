import sys,json
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as S
here=Path(__file__).parent
raw=json.loads((here/'free_third.json').read_text());groups={}
for m,c in raw:
 key=tuple(m[:2]);groups.setdefault(key,{})[tuple(m[2:])]=S.Rational(c)
allgood=True;certificate=[]
for key,pol in groups.items():
 residue={m:c for m,c in pol.items() if all(e%2==0 for e in m)};squares=[]
 for m,c in pol.items():
  if m[0]%2==0:continue
  m1=(m[0]+1,m[1]-1);m2=(m[0]-1,m[1]+1);w=abs(c)/2
  residue[m1]=residue.get(m1,0)-w;residue[m2]=residue.get(m2,0)-w
  squares.append((str(w),list(m1),list(m2),1 if c>0 else -1))
 neg={m:c for m,c in residue.items() if c<0}
 if neg:allgood=False;print('FAIL',key,neg)
 certificate.append({'AB':list(key),'pair_squares':squares,'residual':[[list(m),str(c)] for m,c in residue.items() if c]})
print('ALL SIMPLE YOUNG CERTIFICATES',allgood)
(here/'young_certificate.json').write_text(json.dumps(certificate,indent=2))
