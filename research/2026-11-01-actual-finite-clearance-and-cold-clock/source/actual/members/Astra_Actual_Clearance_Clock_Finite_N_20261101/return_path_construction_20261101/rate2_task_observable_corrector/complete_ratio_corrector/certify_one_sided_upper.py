#!/usr/bin/env python3
"""Sign-preserving upper drift, without the adaptive A gate.
Reuses the frozen continuous coefficient majorants, but recomputes the
parameter-L bound with the exact nonpositive AE->2A / H_t contribution removed.
"""
from fractions import Fraction as F
from pathlib import Path
import sympy as S,pickle,json,hashlib
P=Path(__file__).parent
source=P/'adaptive_uniform_drift_certificate.json';data=json.loads(source.read_text());ff={n:{k:F(v) for k,v in d.items()} for n,d in data['field_maxima'].items()}
o=pickle.load(open(P/'complete_algebra.pkl','rb'));r,u,t,a,z,s=o['vars'];d=S.symbols('d')
num,den=S.fraction(o['chi_power'][1]);poly=S.Poly(S.expand(num.subs(s,1+d)),r,u,t,z,d);nt=S.Integer(0)
for ps,c in poly.terms():
 ps=list(ps);ps[1]-=1
 if ps[4] or ps[1]:continue
 assert ps[2]>0;ps[2]-=1
 nt+=c*S.prod(v**p for v,p in zip([r,u,t,z,d],ps))
PP=r*(1+d-u)+2*u*u*(1-t)
assert S.cancel(nt/den.subs(s,1+d)-r**4/((1+t)*PP**3))==0
# Verify the physical positive component and the sign of its L derivative.
AA,LL,EE,SS,NN=S.symbols('AA LL EE SS NN',positive=True);kk=SS+2*LL-EE-2
ct=AA*NN*EE**3/(LL**2*(LL+1)*kk**3)
norm_ct=u*t*a*r**4/((1+t)*PP**3)
physical=norm_ct.subs({r:EE**2/(NN*LL),u:EE/NN,t:1/LL,a:AA/LL,d:SS/NN-1},simultaneous=True)
assert S.cancel(physical-ct)==0
assert S.cancel(S.diff(ct,LL)+ct*(2/LL+1/(LL+1)+6/kk))==0
U=T=A=F(1,100);B=A+T;Rhi=F(2);Rlo=F(1,2);beta=F(51,50);etap=F(11,1000)
def f(name,key):return ff[name][key]
def xyzbase(key):
 return beta**3*B*(etap*U*f('Hd',key)+beta*T*f('Ht',key)+beta*U*f('Hu',key))+beta**5*U*B*B*f('H2',key)+beta**7*U*U*B**3*f('H3',key)
SL0=T*T+A*T+2*A*A+A
# There is intentionally no theta_A variable or a^2*t/u bound in this expression.
PL=SL0*xyzbase('CL')+beta**3*Rhi*A*B*etap*f('Hd','CL')+beta**4*Rhi*A*B*f('Hu','CL')+beta**5*Rhi*A*B*B*f('H2','CL')+beta**7*Rhi*A*U*B**3*f('H3','CL')
base=data['normalized_drift_error_parts'];parts={k:F(base[k]) for k in ['mean','frozen','parameter_E','parameter_Z','parameter_n']};parts['parameter_L_upper']=PL
TOTAL=sum(parts.values());assert TOTAL<F(2,5)
assert PL<F(1,20)
report={'status':'PASS_UNIFORM_ONE_SIDED_UPPER_CANDIDATE_NO_ADAPTIVE_A_GATE','received_field_certificate_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'symbolic_checks':['exact H_t=r^4/[(1+t)P^3]','physical chi_t=A N E^3/[L^2(L+1)k^3]','partial_L chi_t=-chi_t[2/L+1/(L+1)+6/k]'],'preconditions':{'ratio_local_band':['3/2','2'],'E_over_N':'<=1/100','A_over_L':'<=1/100','abs_Z_over_L':'<=1/100','E5_over_N3':'>=32','L':'>=100','abs_S_minus_N':'<=E/100'},'adaptive_A_gate_used':False,'upper_error_parts':{k:str(v) for k,v in parts.items()},'upper_error_parts_approx':{k:float(v) for k,v in parts.items()},'upper_error_total':str(TOTAL),'upper_error_total_approx':float(TOTAL),'proven_upper_error_ceiling':'2/5','proven_normalized_drift_ceiling':'-1/10 on R in [3/2,2]','scope':'Local actual upper drift near the upper ratio face; no lower-ratio admission, no adaptive-A gate, and no global path/exit acquisition claimed.'}
(P/'one_sided_upper_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['upper_error_parts']},indent=2))
