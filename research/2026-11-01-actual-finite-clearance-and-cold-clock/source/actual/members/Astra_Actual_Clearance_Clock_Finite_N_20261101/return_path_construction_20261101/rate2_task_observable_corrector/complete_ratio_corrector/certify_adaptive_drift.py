#!/usr/bin/env python3
"""Uniform rational majorants for the complete corrected drift under paid gates.
No sampled positivity is used. All bounds cover continuous rational boxes and
use the explicit polynomial gates t^2/u<=r^2/32, a^2*t/u<=1/100.
"""
from fractions import Fraction as F
from pathlib import Path
import pickle,sympy as S,json
P=Path(__file__).parent;o=pickle.load(open(P/'complete_algebra.pkl','rb'));r,u,t,a,z,s=o['vars'];d=S.symbols('d')
fields={};powers={};scales={}
for idx,h in enumerate(o['chi_power'][1:],1):
 num,den=S.fraction(h);pol=S.Poly(S.expand(num.subs(s,1+d)),r,u,t,z,d)
 if idx==1:
  bucket={name:[] for name in ['Hd','Ht','Hu']}
  for ps,c in pol.terms():
   ps=list(ps);ps[1]-=1;assert ps[1]>=0
   if ps[4]:name='Hd';ps[4]-=1
   elif ps[1]:name='Hu';ps[1]-=1
   else:name='Ht';assert ps[2]>0;ps[2]-=1
   bucket[name].append((F(int(c.p),int(c.q)),tuple(ps)))
  fields.update(bucket)
  for name in bucket:powers[name]=3;scales[name]=48
 else:
  name='H'+str(idx);terms=[]
  for ps,c in pol.terms():
   ps=list(ps);ps[1]-=idx;assert ps[1]>=0
   terms.append((F(int(c.p),int(c.q)),tuple(ps)))
  fields[name]=terms;powers[name]=4-idx;scales[name]=8 if idx==2 else 3
Ue=Te=F(11,1000);Ze=F(3,100);De=F(22,100000)
def prod(xs):
 ans=F(1)
 for x in xs:ans*=x
 return ans
def bound(poly,rhi,weighted=None,derivative=None):
 vals=(rhi,Ue,Te,Ze,De);ans=F(0)
 for c,ps in poly:
  ps=list(ps);cc=abs(c)
  if weighted is not None:cc*=ps[weighted]
  if derivative is not None:
   if ps[derivative]==0:continue
   cc*=ps[derivative];ps[derivative]-=1
  ans+=cc*prod(v**p for v,p in zip(vals,ps))
 return ans
quantities=['abs','rh','uh','th','zh','dz','dd','CL','CE']
maxf={name:{q:F(0) for q in quantities} for name in fields};boxrecords=[]
for box in range(65):
 rlo=F(49,100)+F(box,40);rhi=min(F(21,10),rlo+F(1,40))
 if rlo>=F(21,10):continue
 PP=rlo*(1-De-Ue);common=rlo*rlo*(2-Te)**2*(1-Te)**2*4
 rec={}
 for name,poly in fields.items():
  m=powers[name];scale=scales[name];den=scale*common*PP**m;bh=bound(poly,rhi)/den
  rlog=2+m*rhi*(1+De+Ue)/PP
  ulog=m*Ue*(rhi+4*Ue*(1+Te))/PP
  tlog=Te*(2/(2-Te)+2/(1-Te)+(0 if name=='H3' else 2)+1+m*2*Ue*Ue/PP)
  rh=bound(poly,rhi,weighted=0)/den+bh*rlog;uh=bound(poly,rhi,weighted=1)/den+bh*ulog
  th=bound(poly,rhi,weighted=2)/den+bh*tlog;zh=bound(poly,rhi,weighted=3)/den
  dz=bound(poly,rhi,derivative=3)/den;dd=bound(poly,rhi,derivative=4)/den+bh*m*rhi/PP
  adegree=2 if name=='H2' else 3 if name=='H3' else 1
  upower=2 if name in ['Hu','H2'] else 3 if name=='H3' else 1
  CL=rh+th+zh+(adegree+(1 if name=='Ht' else 0))*bh
  CE=2*rh+uh+upower*bh
  bb=dict(abs=bh,rh=rh,uh=uh,th=th,zh=zh,dz=dz,dd=dd,CL=CL,CE=CE)
  for q,v in bb.items():maxf[name][q]=max(maxf[name][q],v)
  rec[name]={q:str(v) for q,v in bb.items()}
 boxrecords.append({'r_interval':[str(rlo),str(rhi)],'field_bounds':rec})
print('field maxima', {name:{q:float(vals[q]) for q in ['abs','CL','CE','dz','dd']} for name,vals in maxf.items()},flush=True)
# Uniform normalized mean minus the nominal D0, on the pre-stop box.
err=S.factor(S.cancel(o['mean']-o['D0']));num,den=S.fraction(err)
mpoly=[(F(int(c.p),int(c.q)),ps) for ps,c in S.Poly(S.expand(num.subs(s,1+d)),r,u,t,z,d).terms()]
U=T=A=F(1,100);Z=F(1,100);eta=F(1,100);meanmax=F(0);meanboxes=[]
for box in range(60):
 rlo=F(1,2)+F(box,40);rhi=rlo+F(1,40);bn=F(0)
 for c,ps in mpoly:
  rp,up,tp,zp,dp=ps;up+=dp-1
  term=abs(c)*rhi**rp*Z**zp*eta**dp
  if up>=0:term*=U**up*T**tp
  else:assert up==-1 and tp>=2;term*=T**(tp-2)*rhi*rhi/32
  bn+=term
 DD=64*rlo*rlo*(2-T)**2*(1-T)**2*4*(rlo*(1-U-eta*U))**3
 mb=bn/DD;meanmax=max(meanmax,mb);meanboxes.append([str(rlo),str(rhi),str(mb)])
print('mean error',float(meanmax),flush=True)
# Actual parameter motion. Segment geometry factors are bounded by beta=1.02.
B=A+T;Rhi=F(2);Rlo=F(1,2);beta=F(51,50);etap=F(11,1000);theta=F(1,100)
def f(name,key):return maxf[name][key]
def xyzbase(key):
 return beta**3*B*(etap*U*f('Hd',key)+beta*T*f('Ht',key)+beta*U*f('Hu',key))+beta**5*U*B*B*f('H2',key)+beta**7*U*U*B**3*f('H3',key)
SL0=T*T+A*T+2*A*A+A
PL=SL0*xyzbase('CL')+beta**3*Rhi*A*B*etap*f('Hd','CL')+beta**4*Rhi*(theta+A*Rhi*Rhi/32)*f('Ht','CL')+beta**4*Rhi*A*B*f('Hu','CL')+beta**5*Rhi*A*B*B*f('H2','CL')+beta**7*Rhi*A*U*B**3*f('H3','CL')
EEinner=etap*U*f('Hd','CE')+beta*T*f('Ht','CE')+beta*U*f('Hu','CE')
PE=(A*A+2)*(beta**5*U*B/Rlo*EEinner+beta**7*U*U*B*B/Rlo*f('H2','CE')+beta**9*U**3*B**3/Rlo*f('H3','CE'))+2*beta**5*A*B*EEinner+2*beta**7*A*U*B*B*f('H2','CE')+2*beta**9*A*U*U*B**3*f('H3','CE')
PZ=2*A*xyzbase('dz')
PN=(T*T+A*T)*(beta**6*U*U*B/Rlo*(f('Hd','abs')+etap*U*f('Hd','dd')+beta*T*f('Ht','dd')+beta*U*f('Hu','dd'))+beta**8*U**3*B*B/Rlo*f('H2','dd')+beta**10*U**4*B**3/Rlo*f('H3','dd'))
FAST=3*A*A*(eta*U*f('Hd','abs')+T*f('Ht','abs')+U*f('Hu','abs'))+(6*A**3+5*A*A*T+8*A*T)*U*f('H2','abs')+(9*A**4+15*A**3*T+24*A*A*T+3*A*A*T*T)*U*U*f('H3','abs')
TOTAL=meanmax+FAST+PL+PE+PZ+PN
parts=dict(mean=meanmax,frozen=FAST,parameter_L=PL,parameter_E=PE,parameter_Z=PZ,parameter_n=PN,total=TOTAL)
ceilings={'mean':F(8,25),'frozen':F(1,10000),'parameter_L':F(813,1000),'parameter_E':F(17,5000),'parameter_Z':F(1,10**8),'parameter_n':F(1,10**8)}
for key,ceiling in ceilings.items():assert parts[key]<ceiling,(key,float(parts[key]))
print('drift majorants', {q:float(v) for q,v in parts.items()},flush=True)
report={'status':'UNIFORM_MAJORANT_COMPUTED','pre_domain':{'r':['1/2','2'],'u':['0','1/100'],'t':['0','1/100'],'a':['0','1/100'],'abs_z':'<=1/100','abs_s_minus_1':'<=u/100','t_squared_over_u':'<=r^2/32','a_squared_times_t_over_u':'<=1/100'},'method':'Continuous-domain rational monomial majorants and exact parameter derivative bounds; no sampled positivity.','field_maxima':{name:{q:str(v) for q,v in vals.items()} for name,vals in maxf.items()},'normalized_drift_error_parts':{q:str(v) for q,v in parts.items()},'normalized_drift_error_parts_approx':{q:float(v) for q,v in parts.items()},'mean_boxes':meanboxes,'field_boxes':boxrecords}
assert TOTAL<F(6,5)
report['status']='PASS_UNIFORM_ADAPTIVE_INWARD_CANDIDATE'
report['proven_error_ceiling']='6/5'
report['lower_face_band']=['1/2','3/5']
report['upper_face_band']=['9/5','2']
report['lower_normalized_drift_floor']='9/10'
report['upper_normalized_drift_ceiling']='-1/5'
(P/'adaptive_uniform_drift_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
