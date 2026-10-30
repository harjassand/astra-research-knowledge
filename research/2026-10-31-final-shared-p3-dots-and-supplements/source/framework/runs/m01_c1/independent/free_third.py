import sys,json,time
sys.dont_write_bytecode=True
from triad_core import *
A,B,P,Q=S.symbols('A B P Q',real=True);rs=[conformal((0,A),(1,0)),conformal((B,0),(0,1)),conformal((P+Q,-P+Q),(1,1))]
N=moments([rr[0] for rr in rs],[rr[1] for rr in rs]);print('start restricted',flush=True)
det=S.Poly(N.det(method='domain-ge'),A,B,P,Q);terms=det.terms();print('terms',len(terms),'negative',sum(1 for m,c in terms if c<0),'odd',sum(1 for m,c in terms if any(i%2 for i in m)),flush=True)
open(__file__.replace('.py','.json'),'w').write(json.dumps([[list(mon),str(co)] for mon,co in terms]))
groups={}
for mon,co in terms:
 assert mon[0]%2==mon[1]%2==0
 key=mon[:2];groups[key]=groups.get(key,0)+co*P**mon[2]*Q**mon[3]
print('groups',len(groups),flush=True)
for key,pp in groups.items():
 pol=S.Poly(pp.subs({P:1,Q:S.Symbol('q')}),S.Symbol('q'));positive=False
 if pol.is_zero:positive=True
 elif pol.degree()%2==0 and pol.LC()>0:
  positive=not any(mult%2 for rr,mult in S.polys.polytools.intervals(pol,eps=S.Rational(1,100)))
 print(key,S.factor(pp),'NONNEG=',positive,flush=True)
