"""Independent symbolic checks of the circuit weighted-jet primitive."""
import sys,json
from pathlib import Path
from fractions import Fraction as F
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import circuit_jets as C
x,y=S.symbols('x y'); variables=(x,y)
raw=[x-x*x,7*y-x*y]
c=C.Circuit(2); roots=[c.compile(f,variables) for f in raw]; q=c.manufacture_q(roots)
qs=-sum(S.diff(raw[i],variables[i]) for i in range(2))/3
checks=[]
for m in [0,1,4]:
    jets,bits=c.jets(roots,q,m,[F(2,3),F(-1,5)],7)
    for i,p in enumerate([S.Integer(1),x,y]):
        for k in range(8):
            val=p.subs({x:S.Rational(2,3),y:S.Rational(-1,5)})
            assert val==jets[i][k],(m,i,k,val,jets[i][k])
            checks.append([m,i,k,True])
            p=S.expand(raw[0]*S.diff(p,x)+raw[1]*S.diff(p,y)+m*qs*p)
(ROOT/'audit'/'circuit_jet_checks.json').write_text(json.dumps({'checks':checks,'count':len(checks)},indent=2))
print('Exact independent weighted jet checks passed:',len(checks))
