import sys,json
sys.dont_write_bytecode=True
from triad_core import *
from pathlib import Path
raw=json.loads((Path(__file__).parent/'free_third_char_aspect.json').read_text());P,Q,e=S.symbols('P Q e');groups={}
for m,c in raw:
 key=tuple(m[:2]);groups[key]=groups.get(key,0)+S.Rational(c)*P**m[2]*Q**m[3]*e**m[4]
for key,pol in groups.items():
 pp=S.Poly(pol,P,Q,e)
 neg=sum(1 for m,c in pp.terms() if c<0 and all(v%2==0 for v in m))
 if neg:
  print('group',key,'negative even',neg,'factor',S.factor(pol),flush=True)
