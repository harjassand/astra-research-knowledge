#!/usr/bin/env python3
"""A uniform rational coefficient majorant, not point sampling."""
from fractions import Fraction as F
from pathlib import Path
import pickle,sympy as S,json
P=Path(__file__).parent;o=pickle.load(open(P/'complete_algebra.pkl','rb'));r,u,t,a,z,s=o['vars'];d=S.symbols('d')
polys=[]
for h in o['chi_power'][1:]:
 num,den=S.fraction(h)
 poly=S.Poly(S.expand(num.subs(s,1+d)),r,u,t,z,d)
 polys.append([(F(int(c.p),int(c.q)),powers) for powers,c in poly.terms()])
def nbound(poly,rhi):
 maxs=(rhi,F(1,100),F(1,100),F(1,100),F(1,100))
 return sum(abs(c)*prod(v**p for v,p in zip(maxs,ps)) for c,ps in poly)
def prod(xs):
 out=F(1)
 for x in xs:out*=x
 return out
best=[F(0)]*3;maxsum=F(0);boxes=[]
for j in range(60):
 rlo=F(1,2)+F(j,40);rhi=rlo+F(1,40)
 common=rlo*rlo*F(199,100)**2*F(99,100)**2*4
 ds=[48*common*(F(98,100)*rlo)**3,8*common*(F(98,100)*rlo)**2,3*common*(F(98,100)*rlo)]
 bounds=[nbound(poly,rhi)/den for poly,den in zip(polys,ds)]
 for k,b in enumerate(bounds):best[k]=max(best[k],b)
 total=sum(b*F(1,100)**i for i,b in enumerate(bounds,1));maxsum=max(maxsum,total)
 boxes.append({'r_interval':[str(rlo),str(rhi)],'coefficient_abs_bounds':[str(b) for b in bounds],'chi_abs_bound':str(total)})
print('global h bounds',list(map(float,best)),'chi',float(maxsum))
report={'status':'EXACT_CONTINUOUS_DOMAIN_MAJORANT','domain':{'r':['1/2','2'],'u':['0','1/100'],'t':['0','1/100'],'z':['-1/100','1/100'],'s_minus_1':['-1/100','1/100'],'a':['0','1/100']},'method':'60 rational r intervals; absolute monomial majorants of shifted numerators and analytic positive denominator lower bounds. No finite grid positivity inference.','max_coefficient_bounds':[str(b) for b in best],'max_chi_bound':str(maxsum),'max_chi_bound_approx':float(maxsum),'boxes':boxes}
(P/'uniform_endpoint_bound.json').write_text(json.dumps(report,indent=2)+'\n')
