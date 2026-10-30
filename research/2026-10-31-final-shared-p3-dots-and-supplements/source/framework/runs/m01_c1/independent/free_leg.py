import sys,json
sys.dont_write_bytecode=True
from triad_core import *
B,C,P,Q=S.symbols('B C P Q',real=True);rs=[conformal((Q,P),(1,0)),conformal((B,0),(0,1)),conformal((C,-C),(1,1))]
N=moments([r[0] for r in rs],[r[1] for r in rs]);det=S.Poly(N.det(method='domain-ge'),B,C,P,Q);print('terms',len(det.terms()),flush=True)
open(__file__.replace('.py','.json'),'w').write(json.dumps([[list(m),str(c)] for m,c in det.terms()]))
groups={}
for m,c in det.terms():groups.setdefault(m[:2],{})[m[2:]]=c
ok=0;bad=[];simple=True;q=S.symbols('q')
for key,pol in groups.items():
 expr=sum(c*P**m[0]*Q**m[1] for m,c in pol.items());pp=S.Poly(expr.subs({P:1,Q:q}),q)
 good=pp.degree()%2==0 and pp.LC()>0 and not any(mult%2 for rr,mult in S.polys.polytools.intervals(pp))
 if good:ok+=1
 else:bad.append((key,str(S.factor(expr))))
 residue={m:c for m,c in pol.items() if m[0]%2==0}
 for m,c in pol.items():
  if m[0]%2:
   n1=(m[0]+1,m[1]-1);n2=(m[0]-1,m[1]+1);residue[n1]=residue.get(n1,0)-abs(c)/2;residue[n2]=residue.get(n2,0)-abs(c)/2
 if any(c<0 for c in residue.values()):simple=False
print('groups',len(groups),'nonnegative',ok,'bad',bad,'simple SOS',simple)
