#!/usr/bin/env python3
"""Independent exact summary/cell checker; no principal imports or Pauli rebuild."""
from fractions import Fraction as F
from pathlib import Path
from math import factorial,isqrt
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING
import json,hashlib
BASE=Path('/Users/harjas/Documents/ChatGPT/coordination/work/astra-opportunity-retrieval-20261027')
T=BASE/'ultra/transport';S=BASE/'published_repo/updates/EX/package/frontier_residual/recovered/astra_frontier_residual_response/results'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def qlist(r,k):return [F(x) for x in r[k]]
def norm_up_square_root(x):
 n=x.numerator*(1<<120);d=x.denominator;k=isqrt(n//d)
 return F(k+(k*k*d<n),1<<60)
def envelope(a,k,r):return sum((a[j]*r**(j-k)/factorial(j-k) for j in range(k,len(a))),F())
def polynomial(p,x):
 value=F()
 for c in reversed(p):value=value*x+c
 return value
raw_record=read(T/'CENTRAL_HOPPING_NORM_BOUNDS.json')
raw={k:qlist(raw_record,k) for k in ['EF','GS','C0','C1','CA','Ccross','CG']}
assert all(len(a)==4 and all(x>=0 for x in a) for a in raw.values())
source=read(S/'fresh/witness.json');p=qlist(source,'corrected_D_polynomial_exact')
q=qlist(source,'residual_norm_upper_exact');qsq=qlist(source,'residual_norms_squared_exact')
assert len(p)==8 and len(q)==len(qsq)==5
assert all(x*x>=y for x,y in zip(q,qsq))
for j,v in enumerate(source['corrected_D_derivatives_exact']):assert F(v)==p[j]*factorial(j)
assert F(raw_record['nominal_D_lower'])==F(source['D_interval_exact'][0])
assert raw_record['source_witness_sha256']==sha(S/'fresh/witness.npz')

def bounds(eps,r):
 rho=eps/(1-eps);m=(1-eps)**-2-1
 ef=[envelope(raw['EF'],k,r) for k in range(3)]
 gs=[envelope(raw['GS'],k,r) for k in range(3)]
 da=[];qq=[]
 for k in range(3):
  c=envelope(raw['C0'],k,r)+r*envelope(raw['C1'],k,r)
  if k:c+=k*envelope(raw['C1'],k-1,r)
  da.append(rho*c+eps*envelope(raw['CA'],k,r)+eps*rho*envelope(raw['Ccross'],k,r))
  od=rho*ef[k]+eps*envelope(raw['CG'],k,r)+(eps/2 if k==0 else 0)
  qq.append(envelope(q,k,r)+norm_up_square_root(od*od+da[k]*da[k]))
 d1=8*m*ef[0]*ef[1]+8*(da[1]*gs[0]+da[0]*gs[1])
 d2=8*m*(ef[2]*ef[0]+ef[1]*ef[1])+8*(da[2]*gs[0]+2*da[1]*gs[1]+da[0]*gs[2])
 e1=4*(2*qq[0]*qq[1]+qq[0]*qq[0])
 e2=4*(2*qq[0]*qq[2]+2*qq[1]*qq[1]+4*qq[0]*qq[1]+2*qq[0]*qq[0])
 return ef,da,d1,d2,e1,e2,m

# First check the already-computed correlated near-control comparison.
near=read(T/'ROBUST_NEAR_OPTIMAL_DECISION.json');h=F(27,512)
assert F(near['half_interval'])==h
assert F(near['nominal_corrected_gain_exact'])==p[0]-polynomial(p,h)
near_rows=[]
for row in near['bounds']:
 eps=F(row['epsilon']);_,_,d1,_,e1,_,_=bounds(eps,h)
 gain=p[0]-polynomial(p,h)-h*(d1+e1)
 assert d1==F(row['delta_corrected_derivative_upper'])
 assert e1==F(row['derivative_error_upper'])
 assert gain==F(row['improvement_lower_exact'])
 near_rows.append({'epsilon':str(eps),'improvement_lower':str(gain)})

cert_path=T/'GLOBAL_ROBUST_HOPPING_CERTIFICATE.json';cert=read(cert_path)
eps=F(cert['epsilon']);vc=F(cert['chosen_control']);left,right=map(F,cert['local_interval'])
assert eps==F(1,10000) and vc==F(1109,512) and [left,right]==[F(31,16),F(39,16)]
assert cert['control_domain']==['0','3']
r=max(vc-left,right-vc);assert r==F(139,512)
ef,da,d1,d2,e1,e2,m=bounds(eps,r)
ce,cda,cd1,cd2,ce1,ce2,cm=bounds(eps,F())
second_upper=2*p[2]+sum((abs(j*(j-1)*p[j])*r**(j-2) for j in range(3,len(p))),F())
mu=-(second_upper+d2+e2)
grad=abs(p[1])+cd1+ce1
lc=F(raw_record['nominal_D_lower'])-4*(cm*ce[0]**2+2*F(raw_record['A0_f_inverse_norm'])*cda[0]+cda[0]**2)
checks={'source_nominal_corrected_second_upper':second_upper,'actual_corrected_second_perturbation_upper':d2,'actual_second_derivative_error_upper':e2,'strict_concavity_mu':mu,'chosen_gradient_upper':grad,'chosen_value_lower':lc}
for k,v in checks.items():assert v==F(cert[k]),k
anchors=read(T/'GLOBAL_HOPPING_UPPER_ANCHORS.json');assert len(anchors)==7
by_name={a['name']:a for a in anchors};assert len(by_name)==7
for a in anchors:
 s=read(S/'anchors'/(a['name']+'.json'))
 assert a['V']==s['parameters']['V']
 assert s['parameters']['U']=='4' and s['parameters']['d']=='2' and s['parameters']['t']=='1'
 assert a['upper_polynomial']==s['upper_D_polynomial_exact']
 pp=qlist(a,'upper_polynomial');assert len(pp)==3 and pp[2]>=0
 assert pp[0]==F(a['constants']['nominal_D_upper'])==F(s['D_interval_exact'][1])
 assert F(a['constants']['residual_inverse_norm'])**2<=pp[0]/4
 assert F(a['constants']['c_upper'])>=F(1,2)
# Independent interval list: the endpoints are exact grid boundaries.
expected=[(F(i,256),F(i+1,256)) for i in list(range(496))+list(range(624,768))]
cells=cert['outside_cells'];actual=[(F(c['a']),F(c['b'])) for c in cells]
assert actual==expected and len(actual)==640
assert actual[0][0]==0 and actual[495][1]==left and actual[496][0]==right and actual[-1][1]==3
cell_uppers=[]
for cell,(a,b) in zip(cells,expected):
 choices={}
 for anchor in anchors:
  av=F(anchor['V']);pp=qlist(anchor,'upper_polynomial')
  nominal=max(polynomial(pp,a-av),polynomial(pp,b-av));assert nominal>=0
  c=eps*F(anchor['constants']['c_upper'])
  choices[anchor['name']]=nominal+8*norm_up_square_root(nominal/4)*c+4*c*c
 selected=choices[cell['selected_anchor']]
 assert selected==F(cell['upper'])==min(choices.values())
 cell_uppers.append(selected)
outside=max(cell_uppers);gap=lc-outside;regret=grad*grad/(2*mu)
assert mu>0 and gap>0 and cert['status']=='EXACT_PASS'
for k,v in [('outside_upper',outside),('outside_exclusion_gap',gap),('global_regret_upper',regret)]:assert F(cert[k])==v
assert cert['source_witness_sha256']==raw_record['source_witness_sha256']
assert cert['complete_output_span']>=max(23,int(raw_record['full_output_span'])) and cert['min_ring_size']==2*cert['complete_output_span']+1==47
with localcontext() as ctx:
 ctx.prec=90
 display={}
 for k,v in [('strict_concavity_mu',mu),('chosen_gradient_upper',grad),('chosen_value_lower',lc),('outside_upper',outside),('outside_exclusion_gap',gap),('global_regret_upper',regret)]:
  decimal=Decimal(v.numerator)/Decimal(v.denominator)
  rounding=ROUND_CEILING if k in ['chosen_gradient_upper','outside_upper','global_regret_upper'] else ROUND_FLOOR
  display[k]={'decimal':str(decimal),'outward_21dp':str(decimal.quantize(Decimal('0.000000000000000000001'),rounding=rounding))}
report={'status':'EXACT_FORMULA_AND_640_CELL_PASS','verification_scope':'Independent rational reconstruction from stored norm bounds and pinned source polynomial/anchor records; no principal module import or heavy Pauli/norm regeneration','global_certificate_sha256':sha(cert_path),'raw_norm_summary_sha256':sha(T/'CENTRAL_HOPPING_NORM_BOUNDS.json'),'upper_anchor_summary_sha256':sha(T/'GLOBAL_HOPPING_UPPER_ANCHORS.json'),'source_central_witness_sha256':raw_record['source_witness_sha256'],'source_polynomial_derivative_factorials':'EXACT_PASS','all_five_source_residual_derivatives_and_upper_norm_squares':'EXACT_PASS','local_radius':str(r),'seven_source_anchor_polynomials_and_endpoints':'EXACT_PASS','continuous_complement_cells_checked':640,'coverage':'[0,31/16] union [39/16,3], exact 1/256 cells','near_control_rows_exactly_checked':near_rows,'display':display,'finite_ring_minimum':47,'scope':'Uniform global regret over V in [0,3] in the specified four-amplitude box; inherited actual thermodynamic D; no physical acquisition or independent heavy norm regeneration.'}
(BASE/'ultra/helper/GLOBAL_HOPPING_INDEPENDENT_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='near_control_rows_exactly_checked'},indent=2))
