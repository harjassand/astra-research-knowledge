#!/usr/bin/env python3
"""Uniform exact-rational monomial/denominator bounds on a one-jump enlarged box.
This is a continuous-domain proof, not a grid positivity inference.
"""
from fractions import Fraction as F
from pathlib import Path
import pickle,sympy as S,json
P=Path(__file__).parent;o=pickle.load(open(P/'complete_algebra.pkl','rb'));r,u,t,a,z,s=o['vars'];d=S.symbols('d')
polys=[]
for h in o['chi_power'][1:]:
 num,den=S.fraction(h);pol=S.Poly(S.expand(num.subs(s,1+d)),r,u,t,z,d)
 polys.append([(F(int(c.p),int(c.q)),ps) for ps,c in pol.terms()])
U=T=F(11,1000);Z=A=F(3,100);D=F(11,1000)
def prod(xs):
 out=F(1)
 for x in xs:out*=x
 return out
def monomial_bound(poly,rhi,weighted=None,derivative=None,divide_u=False):
 vals=(rhi,U,T,Z,D);ans=F(0)
 for c,ps in poly:
  ps=list(ps);cc=abs(c)
  if weighted is not None:cc*=ps[weighted]
  if derivative is not None:
   if ps[derivative]==0:continue
   cc*=ps[derivative];ps[derivative]-=1
  if divide_u:ps[1]-=1;assert ps[1]>=0
  ans+=cc*prod(v**p for v,p in zip(vals,ps))
 return ans
keys=['C_A','C_L','C_E','C_Z','C_n','chi_bound','F2_minus_R_bound']
maxima={key:F(0) for key in keys};records=[]
for box in range(65):
 rlo=F(49,100)+F(box,40);rhi=min(F(21,10),rlo+F(1,40))
 if rlo>=F(21,10):continue
 PP=rlo*(1-D-U)
 common=rlo*rlo*(2-T)**2*(1-T)**2*4
 hs=[]
 for idx,(poly,power,scale) in enumerate(zip(polys,[3,2,1],[48,8,3]),1):
  den=scale*common*PP**power
  bh=monomial_bound(poly,rhi)/den;bu=monomial_bound(poly,rhi,divide_u=True)/den
  logR=2+power*rhi*(1+D+U)/PP
  logU=power*U*(rhi+4*U*(1+T))/PP
  logT=T*(2/(2-T)+2/(1-T)+(2 if idx<3 else 0)+1+power*2*U*U/PP)
  rh=monomial_bound(poly,rhi,weighted=0)/den+bh*logR
  uh=monomial_bound(poly,rhi,weighted=1)/den+bh*logU
  th=monomial_bound(poly,rhi,weighted=2)/den+bh*logT
  zh=monomial_bound(poly,rhi,weighted=3)/den
  zu=monomial_bound(poly,rhi,derivative=3,divide_u=True)/den
  su=monomial_bound(poly,rhi,derivative=4,divide_u=True)/den+bu*power*rhi/PP
  hs.append(dict(bh=bh,bu=bu,rh=rh,uh=uh,th=th,zh=zh,zu=zu,su=su))
 CA=rhi+sum(j*A**(j-1)*h['bu'] for j,h in enumerate(hs,1))
 Fr=1+A*U+sum(A**j*h['rh']/rlo for j,h in enumerate(hs,1))
 CL=rhi*(1+A*U)+sum(A**j*(h['rh']+h['th']+h['zh']) for j,h in enumerate(hs,1))+A*U*CA
 CE=2*Fr+(rhi*A*U+sum(A**j*h['uh'] for j,h in enumerate(hs,1)))/rlo
 CZ=sum(A**j*h['zu'] for j,h in enumerate(hs,1))
 Cn=U*U/rlo*sum(A**j*h['su'] for j,h in enumerate(hs,1))
 cb=sum(A**j*h['bh'] for j,h in enumerate(hs,1));fb=rhi*A*U+cb
 bounds=dict(C_A=CA,C_L=CL,C_E=CE,C_Z=CZ,C_n=Cn,chi_bound=cb,F2_minus_R_bound=fb)
 for key,v in bounds.items():maxima[key]=max(maxima[key],v)
 records.append({'r_interval':[str(rlo),str(rhi)],'bounds':{k:str(v) for k,v in bounds.items()}})
rounded={'C_A':F(3),'C_L':F(3),'C_E':F(3),'C_Z':F(1),'C_n':F(1),'F2_minus_R_bound':F(1,1000)}
for key,ceil in rounded.items():assert maxima[key]<ceil,(key,float(maxima[key]),float(ceil))
print({key:float(v) for key,v in maxima.items()})
report={'status':'PASS_UNIFORM_CONTINUOUS_DOMAIN_BOUNDS','domain':{'r':['49/100','21/10'],'u':['0','11/1000'],'t':['0','11/1000'],'a':['0','3/100'],'z':['-3/100','3/100'],'s_minus_1':['-11/1000','11/1000']},'method':'Exact absolute monomial majorants after s=1+d; analytic positive denominator/log-derivative bounds; 65 rational r intervals cover the full box. This is not finite-grid positivity.','maxima':{k:str(v) for k,v in maxima.items()},'maxima_approx':{k:float(v) for k,v in maxima.items()},'accepted_rounded_constants':{k:str(v) for k,v in rounded.items()},'boxes':records}
(P/'uniform_derivative_and_endpoint_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
