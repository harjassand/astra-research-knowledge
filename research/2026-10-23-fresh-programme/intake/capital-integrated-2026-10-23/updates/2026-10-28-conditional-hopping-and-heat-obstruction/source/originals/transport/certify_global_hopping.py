from robust_decision import F,OUT,SRC,sup_sqrt,json
from math import factorial

def weighted(vals,k,h):return sum((h**(j-k)/factorial(j-k)*vals[j] for j in range(k,len(vals))),F())

def ev(poly,s):return sum((c*s**j for j,c in enumerate(poly)),F())

def calc(raw,rec,eps,H):
 ef=[weighted(raw['EF'],k,H) for k in range(3)];gn=[weighted(raw['GS'],k,H) for k in range(3)];rho=eps/(1-eps);m2=1/(1-eps)**2-1;bA=[];bo=[];qq=[]
 for k in range(3):
  c10=weighted(raw['C0'],k,H)+H*weighted(raw['C1'],k,H)+(k*weighted(raw['C1'],k-1,H) if k else 0)
  bA.append(rho*c10+eps*weighted(raw['CA'],k,H)+eps*rho*weighted(raw['Ccross'],k,H))
  bo.append(rho*ef[k]+eps*weighted(raw['CG'],k,H)+(eps/2 if not k else 0))
  qq.append(weighted([F(x) for x in rec['residual_norm_upper_exact']],k,H)+sup_sqrt(bo[k]**2+bA[k]**2))
 delta1=8*m2*ef[0]*ef[1]+8*(bA[1]*gn[0]+bA[0]*gn[1])
 delta2=8*m2*(ef[2]*ef[0]+ef[1]**2)+8*(bA[2]*gn[0]+2*bA[1]*gn[1]+bA[0]*gn[2])
 E1=4*(2*qq[0]*qq[1]+qq[0]**2);E2=4*(2*qq[0]*qq[2]+2*qq[1]**2+4*qq[0]*qq[1]+2*qq[0]**2)
 return dict(ef=ef,bA=bA,q=qq,delta1=delta1,delta2=delta2,E1=E1,E2=E2,m2=m2)

if __name__=='__main__':
 rr=json.loads((OUT/'CENTRAL_HOPPING_NORM_BOUNDS.json').read_text());raw={k:[F(x) for x in rr[k]] for k in ['EF','GS','C0','C1','CA','Ccross','CG']}
 rec=json.loads((SRC/'results/fresh/witness.json').read_text());poly=[F(x) for x in rec['corrected_D_polynomial_exact']];anchors=json.loads((OUT/'GLOBAL_HOPPING_UPPER_ANCHORS.json').read_text());assert len(anchors)==7
 eps=F(1,10000);Vc=F(1109,512);left=F(31,16);right=F(39,16);H=max(Vc-left,right-Vc)
 broad=calc(raw,rec,eps,H);center=calc(raw,rec,eps,F())
 nominal_second_upper=2*poly[2]+sum((abs(j*(j-1)*poly[j])*H**(j-2) for j in range(3,len(poly))),F())
 mu=-(nominal_second_upper+broad['delta2']+broad['E2']);grad=abs(poly[1])+center['delta1']+center['E1']
 lc=F(rr['nominal_D_lower'])-4*(center['m2']*center['ef'][0]**2+2*F(rr['A0_f_inverse_norm'])*center['bA'][0]+center['bA'][0]**2)
 cells=[]
 for i in range(3*256):
  a=F(i,256);b=F(i+1,256)
  if not (b<=left or a>=right):continue
  choices=[]
  for anchor in anchors:
   vv=F(anchor['V']);pp=[F(x) for x in anchor['upper_polynomial']];assert len(pp)==3 and pp[2]>=0
   nom=max(ev(pp,a-vv),ev(pp,b-vv));assert nom>=0;cc=eps*F(anchor['constants']['c_upper']);upper=nom+8*sup_sqrt(nom/4)*cc+4*cc*cc;choices.append((upper,anchor['name']))
  upper,name=min(choices);cells.append({'a':str(a),'b':str(b),'selected_anchor':name,'upper':str(upper)})
 assert len(cells)==640
 ou=max(F(c['upper']) for c in cells);gap=lc-ou
 result={'epsilon':str(eps),'chosen_control':str(Vc),'control_domain':['0','3'],'local_interval':[str(left),str(right)],'source_nominal_corrected_second_upper':str(nominal_second_upper),'actual_corrected_second_perturbation_upper':str(broad['delta2']),'actual_second_derivative_error_upper':str(broad['E2']),'strict_concavity_mu':str(mu),'chosen_gradient_upper':str(grad),'chosen_value_lower':str(lc),'outside_upper':str(ou),'outside_exclusion_gap':str(gap),'outside_cells':cells,'complete_output_span':max(23,int(rr['full_output_span'])),'min_ring_size':2*max(23,int(rr['full_output_span']))+1,'source_witness_sha256':rr['source_witness_sha256']}
 if mu>0 and gap>0:result['global_regret_upper']=str(grad*grad/(2*mu));result['status']='EXACT_PASS'
 else:result['status']='NOT_CERTIFIED'
 (OUT/'GLOBAL_ROBUST_HOPPING_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:(float(F(v)) if k in ['strict_concavity_mu','chosen_gradient_upper','chosen_value_lower','outside_upper','outside_exclusion_gap','global_regret_upper'] else v) for k,v in result.items() if k not in ['outside_cells','source_nominal_corrected_second_upper','actual_corrected_second_perturbation_upper','actual_second_derivative_error_upper']}),flush=True)
