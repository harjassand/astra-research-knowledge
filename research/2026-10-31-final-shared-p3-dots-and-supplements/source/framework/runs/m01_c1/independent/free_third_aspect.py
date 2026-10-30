import sys,json
sys.dont_write_bytecode=True
from triad_core import *
A,B,P,Q,e=S.symbols('A B P Q e',real=True)
# The axial mode amplitudes absorb the frequency lengths.
rs=[conformal((0,A),(1,0)),conformal((B,0),(0,1)),conformal((P+Q,-P+Q),(1,e))]
N=moments([rr[0] for rr in rs],[rr[1] for rr in rs]);print('aspect matrix built',flush=True)
det=S.Poly(N.det(method='domain-ge'),A,B,P,Q,e);terms=det.terms();print('terms',len(terms),flush=True)
open(__file__.replace('.py','.json'),'w').write(json.dumps([[list(mon),str(co)] for mon,co in terms]))
# Split on A^2 B^2 and on powers of s=e-1, testing every binary homogeneous coefficient.
s=S.symbols('s',nonnegative=True)
shift=S.Poly(det.as_expr().subs(e,1+s).expand(),A,B,s,P,Q)
groups={}
for mon,co in shift.terms():
 key=mon[:3];groups[key]=groups.get(key,0)+co*P**mon[3]*Q**mon[4]
passes=0;fails=[];q=S.symbols('q')
for key,pp in groups.items():
 pol=S.Poly(pp.subs({P:1,Q:q}),q)
 good=pol.degree()%2==0 and pol.LC()>0 and not any(mult%2 for rr,mult in S.polys.polytools.intervals(pol))
 if good:passes+=1
 else:fails.append((key,str(S.factor(pp))))
print('groups',len(groups),'pass',passes,'fail',len(fails));print('first fails',fails[:6],flush=True)
