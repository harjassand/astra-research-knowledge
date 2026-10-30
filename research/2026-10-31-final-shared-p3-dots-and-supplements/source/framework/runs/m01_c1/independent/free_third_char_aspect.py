import sys,json
sys.dont_write_bytecode=True
from triad_core import *
A,B,P,Q,e=S.symbols('A B P Q e',real=True)
r=e*(3-e*e);s=1-3*e*e
rs=[conformal((0,A),(1,0)),conformal((B,0),(0,1)),conformal((P*r-Q*s,P*s+Q*r),(1,e))]
N=moments([rr[0] for rr in rs],[rr[1] for rr in rs]);print('char aspect matrix built',flush=True)
det=S.Poly(N.det(method='domain-ge'),A,B,P,Q,e);terms=det.terms();print('terms',len(terms),'negative',sum(1 for m,c in terms if c<0),flush=True)
open(__file__.replace('.py','.json'),'w').write(json.dumps([[list(mon),str(co)] for mon,co in terms]))
# Every A^2 B^2 coefficient must be nonnegative in (P,Q,e); test direct diagonal dominance with neighboring even powers.
groups={}
for m,c in terms:groups.setdefault(tuple(m[:2]),{})[tuple(m[2:])]=c
print('groups',len(groups),'negative even',sum(1 for pol in groups.values() for m,c in pol.items() if c<0 and all(v%2==0 for v in m)),flush=True)
